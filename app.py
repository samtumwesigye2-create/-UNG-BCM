from fastapi import FastAPI,Header,HTTPException
from pydantic import BaseModel
from domain import declare_incident,list_incidents
from integration import dependencies
SYSTEM_ID="UNG-NEMSIS"; LEGACY_ID="UNG-BCM"; VERSION="0.2.0"
app=FastAPI(title=SYSTEM_ID,version=VERSION,description="National Emergency Management Services Information System")
class IncidentIn(BaseModel): title:str; severity:str
def auth(p,h):
 s={x.strip() for x in (h or "").split(",") if x.strip()}
 if p not in s and "ung.admin" not in s: raise HTTPException(403,"UNG-JANUS permission required")
@app.get("/")
def root(): return {"system":SYSTEM_ID,"legacy_id":LEGACY_ID,"name":"National Emergency Management Services Information System","status":"online","version":VERSION}
@app.get("/health")
def health(): return {"status":"ok","service":SYSTEM_ID,"version":VERSION}
@app.get("/ready")
def ready(): return {"status":"ready","service":SYSTEM_ID,"dependencies":dependencies()}
@app.get("/v1/system")
def system(): return {"system_id":SYSTEM_ID,"legacy_id":LEGACY_ID,"domain":"emergency-management","dependencies":dependencies()}
@app.get("/v1/incidents")
def incidents(x_ung_permissions:str|None=Header(None)): auth("nemsis.incidents.read",x_ung_permissions); return list_incidents()
@app.post("/v1/incidents",status_code=201)
def declare(body:IncidentIn,x_ung_permissions:str|None=Header(None)): auth("nemsis.incidents.declare",x_ung_permissions); return declare_incident(body.title,body.severity)
