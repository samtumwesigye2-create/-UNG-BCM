import os,json
from urllib.request import Request,urlopen
JANUS_BASE_URL=os.getenv("JANUS_BASE_URL",os.getenv("IAM_BASE_URL","")).rstrip("/")
ATLAS_BASE_URL=os.getenv("ATLAS_BASE_URL","")
PULSAR_BASE_URL=os.getenv("PULSAR_BASE_URL","")
NEPTUNE_BASE_URL=os.getenv("NEPTUNE_BASE_URL","").rstrip("/")
ORION_BASE_URL=os.getenv("ORION_BASE_URL","").rstrip("/")

def _json(url,method="GET",payload=None,headers=None):
 data=json.dumps(payload).encode() if payload is not None else None
 h={"Content-Type":"application/json",**(headers or {})}
 with urlopen(Request(url,data=data,headers=h,method=method),timeout=5) as r:return json.load(r)

def introspect(token):
 if not JANUS_BASE_URL or not token:return None
 try:
  x=_json(JANUS_BASE_URL+"/v1/auth/introspect","POST",None,{"Authorization":"Bearer "+token})
  return x.get("principal") if x.get("active") else None
 except Exception:return None

def send_neptune(record,incident):
 if not NEPTUNE_BASE_URL:return {"delivered":False,"reason":"not_configured"}
 try:
  p={"domain":"civilian","type":"emergency_support_request","title":record["support_type"]+": "+incident["title"],"source":"UNG-NEMESIS","confidence":1.0,"classification":"RESTRICTED","releasability":"INTERNAL","latitude":incident.get("latitude"),"longitude":incident.get("longitude")}
  return {"delivered":True,"response":_json(NEPTUNE_BASE_URL+"/api/events","POST",p)}
 except Exception as e:return {"delivered":False,"reason":type(e).__name__}

def dependencies(): return {"identity":{"system":"UNG-JANUS","configured":bool(JANUS_BASE_URL)},"control_plane":{"system":"UNG-ATLAS","configured":bool(ATLAS_BASE_URL)},"event_relay":{"system":"UNG-PULSAR","configured":bool(PULSAR_BASE_URL)},"military_support":{"system":"UNG-NEPTUNE","configured":bool(NEPTUNE_BASE_URL)},"national_command":{"system":"UNG-ORION","configured":bool(ORION_BASE_URL)}}
