from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from uuid import uuid4

def _now(): return datetime.now(timezone.utc).isoformat()

@dataclass
class Incident:
    id:str; title:str; severity:str; status:str="open"; created_at:str=""

_incidents={}
_military_support={}
_audit=[]

def _audit_event(action:str, actor:str, resource_id:str, detail:dict|None=None):
    event={"id":str(uuid4()),"action":action,"actor":actor,"resource_id":resource_id,"at":_now(),"detail":detail or {}}
    _audit.append(event)
    return event

def declare_incident(title:str, severity:str, actor:str="unknown"):
    i=Incident(str(uuid4()),title,severity,"open",_now()); _incidents[i.id]=i
    _audit_event("incident.declared",actor,i.id,{"severity":severity})
    return asdict(i)

def list_incidents(): return [asdict(x) for x in _incidents.values()]

def executive_summary():
    incidents=list_incidents()
    counts={}
    for i in incidents: counts[i["severity"]]=counts.get(i["severity"],0)+1
    return {"system":"UNG-NEMESIS","generated_at":_now(),"open_incidents":sum(1 for i in incidents if i["status"]=="open"),"severity_counts":counts,"incidents":incidents}

def request_military_support(incident_id:str, support_type:str, reason:str, actor:str, location:str|None=None):
    if incident_id not in _incidents: raise KeyError("incident_not_found")
    rid=f"NEM-NEP-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid4().hex[:10].upper()}"
    record={"request_id":rid,"incident_id":incident_id,"support_type":support_type,"reason":reason,"location":location,"status":"requested","requested_by":actor,"requested_at":_now(),"updated_at":_now()}
    _military_support[rid]=record
    _audit_event("military_support.requested",actor,rid,{"incident_id":incident_id,"support_type":support_type})
    return record

def list_military_support(): return list(_military_support.values())

def update_military_support(request_id:str,status:str,actor:str,note:str|None=None):
    if request_id not in _military_support: raise KeyError("request_not_found")
    if status not in {"requested","acknowledged","approved","declined","in_progress","completed","cancelled"}: raise ValueError("invalid_status")
    r=_military_support[request_id]; r["status"]=status; r["updated_at"]=_now()
    if note: r["note"]=note
    _audit_event("military_support.updated",actor,request_id,{"status":status,"note":note})
    return r

def audit_log(): return list(reversed(_audit))
