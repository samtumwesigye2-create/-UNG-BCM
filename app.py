from fastapi import FastAPI,Header,HTTPException
from pydantic import BaseModel
from domain import declare_incident,list_incidents,executive_summary,request_military_support,list_military_support,update_military_support,audit_log
from integration import dependencies
SYSTEM_ID="UNG-NEMESIS"; LEGACY_ID="UNG-BCM"; VERSION="0.3.0"
app=FastAPI(title=SYSTEM_ID,version=VERSION,description="National Emergency Management System")
class IncidentIn(BaseModel): title:str; severity:str
class MilitarySupportIn(BaseModel): incident_id:str; support_type:str; reason:str; location:str|None=None
class MilitarySupportUpdate(BaseModel): status:str; note:str|None=None
def auth(p,h):
 s={x.strip() for x in (h or "").split(",") if x.strip()}
 if p not in s and "ung.admin" not in s: raise HTTPException(403,"UNG-JANUS permission required")
def actor(h): return (h or "unknown").strip()[:160] or "unknown"
@app.get("/")
def root(): return {"system":SYSTEM_ID,"legacy_id":LEGACY_ID,"name":"National Emergency Management System","status":"online","version":VERSION}
@app.get("/health")
def health(): return {"status":"ok","service":SYSTEM_ID,"version":VERSION}
@app.get("/ready")
def ready(): return {"status":"ready","service":SYSTEM_ID,"dependencies":dependencies()}
@app.get("/v1/system")
def system(): return {"system_id":SYSTEM_ID,"legacy_id":LEGACY_ID,"domain":"emergency-management","command_chain":["UNG-PRESIDENT","ORION","UNG-NEMESIS"],"dependencies":dependencies()}
@app.get("/v1/incidents")
def incidents(x_ung_permissions:str|None=Header(None)): auth("nemesis.incidents.read",x_ung_permissions); return list_incidents()
@app.post("/v1/incidents",status_code=201)
def declare(body:IncidentIn,x_ung_permissions:str|None=Header(None),x_ung_actor:str|None=Header(None)): auth("nemesis.incidents.declare",x_ung_permissions); return declare_incident(body.title,body.severity,actor(x_ung_actor))
@app.get("/v1/executive/summary")
def exec_summary(x_ung_permissions:str|None=Header(None)): auth("nemesis.executive.read",x_ung_permissions); return executive_summary()
@app.get("/v1/neptune/support")
def military_requests(x_ung_permissions:str|None=Header(None)): auth("nemesis.military_support.read",x_ung_permissions); return list_military_support()
@app.post("/v1/neptune/support",status_code=201)
def military_request(body:MilitarySupportIn,x_ung_permissions:str|None=Header(None),x_ung_actor:str|None=Header(None)):
 auth("nemesis.military_support.request",x_ung_permissions)
 try:return request_military_support(body.incident_id,body.support_type,body.reason,actor(x_ung_actor),body.location)
 except KeyError:raise HTTPException(404,"incident_not_found")
@app.patch("/v1/neptune/support/{request_id}")
def military_update(request_id:str,body:MilitarySupportUpdate,x_ung_permissions:str|None=Header(None),x_ung_actor:str|None=Header(None)):
 auth("nemesis.military_support.update",x_ung_permissions)
 try:return update_military_support(request_id,body.status,actor(x_ung_actor),body.note)
 except KeyError:raise HTTPException(404,"request_not_found")
 except ValueError:raise HTTPException(400,"invalid_status")
@app.get("/v1/audit")
def audit(x_ung_permissions:str|None=Header(None)): auth("nemesis.audit.read",x_ung_permissions); return audit_log()
