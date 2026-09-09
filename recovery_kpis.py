from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field
import os, psycopg
from psycopg.rows import dict_row
from app import auth

router=APIRouter(prefix='/v1/kpis',tags=['Recovery KPIs'])
DB=os.getenv('DATABASE_URL','')
def conn():
    if not DB: raise HTTPException(503,'database_not_configured')
    return psycopg.connect(DB,row_factory=dict_row)
def now(): return datetime.now(timezone.utc)
def ensure_schema():
    with conn() as c:c.execute('''CREATE TABLE IF NOT EXISTS nemsis_recovery_observations(id UUID PRIMARY KEY,incident_id TEXT NOT NULL,disrupted_at TIMESTAMPTZ NOT NULL,recovered_at TIMESTAMPTZ NULL,critical_supply_chain BOOLEAN NOT NULL DEFAULT TRUE,measured_at TIMESTAMPTZ NOT NULL)''')
class RecoveryIn(BaseModel):
    incident_id:str=Field(min_length=1,max_length=120);disrupted_at:datetime;recovered_at:datetime|None=None;critical_supply_chain:bool=True
@router.post('/recovery-observations',status_code=201)
def record(b:RecoveryIn,x_ung_permissions:str|None=Header(None)):
    auth('nemsis.incidents.declare',x_ung_permissions);ensure_schema()
    if b.recovered_at and b.recovered_at < b.disrupted_at: raise HTTPException(422,'recovered_at_before_disrupted_at')
    with conn() as c:return c.execute('INSERT INTO nemsis_recovery_observations VALUES(%s,%s,%s,%s,%s,%s) RETURNING *',(str(uuid4()),b.incident_id,b.disrupted_at,b.recovered_at,b.critical_supply_chain,now())).fetchone()
@router.get('/supply-chain')
def snapshot(x_ung_permissions:str|None=Header(None)):
    auth('nemsis.incidents.read',x_ung_permissions);ensure_schema()
    with conn() as c:rows=c.execute('SELECT * FROM nemsis_recovery_observations WHERE critical_supply_chain=TRUE AND recovered_at IS NOT NULL ORDER BY measured_at DESC LIMIT 500').fetchall()
    if not rows:return {'source_system':'UNG-NEMSIS','status':'no-data','observations':[],'generated_at':now()}
    mins=[(r['recovered_at']-r['disrupted_at']).total_seconds()/60 for r in rows]
    return {'source_system':'UNG-NEMSIS','recovered_incidents':len(rows),'observations':[{'kpi_key':'time_to_recover','value':sum(mins)/len(mins),'entity_id':'enterprise','source_system':'UNG-NEMSIS'}],'generated_at':now()}
