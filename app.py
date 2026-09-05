from fastapi import FastAPI
SYSTEM_ID="UNG-NEMSIS"; LEGACY_ID="UNG-BCM"; VERSION="0.1.0"
app=FastAPI(title=SYSTEM_ID,version=VERSION,description="National Emergency Management Services Information System")
@app.get("/")
def root(): return {"system":SYSTEM_ID,"legacy_id":LEGACY_ID,"name":"National Emergency Management Services Information System","status":"foundation-online","version":VERSION}
@app.get("/health")
def health(): return {"status":"ok","service":SYSTEM_ID,"version":VERSION}
@app.get("/ready")
def ready(): return {"status":"ready","service":SYSTEM_ID}
@app.get("/v1/system")
def system_contract(): return {"system_id":SYSTEM_ID,"legacy_id":LEGACY_ID,"domain":"emergency-management","iam":"UNG-JANUS","control_plane":"UNG-ATLAS"}
