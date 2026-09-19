from datetime import datetime, timezone
from uuid import uuid4
from storage import put, all_records, enqueue

def _now(): return datetime.now(timezone.utc).isoformat()
def _records(kind): return [r for r in all_records() if r.get("record_type")==kind]
def _audit_event(action,actor,resource_id,detail=None):
    e={"id":str(uuid4()),"record_type":"audit","action":action,"actor":actor,"resource_id":resource_id,"at":_now(),"detail":detail or {}}
    put(e); enqueue({"event_type":action,"source":"UNG-NEMESIS","data":e}); return e

def declare_incident(title,severity,actor="unknown"):
    if not title.strip(): raise ValueError("title_required")
    if severity not in {"low","moderate","high","critical"}: raise ValueError("invalid_severity")
    r={"id":str(uuid4()),"record_type":"incident","title":title.strip(),"severity":severity,"status":"open","created_at":_now(),"created_by":actor}
    put(r); _audit_event("incident.declared",actor,r["id"],{"severity":severity}); return r
def list_incidents(): return _records("incident")

def executive_summary():
    incidents=list_incidents(); counts={}
    for i in incidents: counts[i["severity"]]=counts.get(i["severity"],0)+1
    return {"system":"UNG-NEMESIS","generated_at":_now(),"open_incidents":sum(1 for i in incidents if i["status"]=="open"),"severity_counts":counts,"incidents":incidents}

def request_military_support(incident_id,support_type,reason,actor,location=None):
    if not any(x["id"]==incident_id for x in list_incidents()): raise KeyError("incident_not_found")
    rid=f"NEM-NEP-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{uuid4().hex[:10].upper()}"
    r={"id":rid,"record_type":"military_support","request_id":rid,"incident_id":incident_id,"support_type":support_type.strip(),"reason":reason.strip(),"location":location,"status":"requested","requested_by":actor,"requested_at":_now(),"updated_at":_now()}
    put(r); _audit_event("military_support.requested",actor,rid,{"incident_id":incident_id,"support_type":support_type}); return r
def list_military_support(): return _records("military_support")

def update_military_support(request_id,status,actor,note=None):
    rows=[x for x in list_military_support() if x["request_id"]==request_id]
    if not rows: raise KeyError("request_not_found")
    if status not in {"requested","acknowledged","approved","declined","in_progress","completed","cancelled"}: raise ValueError("invalid_status")
    r=rows[0]; r["status"]=status; r["updated_at"]=_now()
    if note:r["note"]=note
    put(r); _audit_event("military_support.updated",actor,request_id,{"status":status,"note":note}); return r
def audit_log(): return sorted(_records("audit"),key=lambda x:x.get("at",""),reverse=True)
