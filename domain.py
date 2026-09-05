from dataclasses import dataclass, asdict
from uuid import uuid4
@dataclass
class Incident:
    id:str; title:str; severity:str; status:str="open"
_incidents={}
def declare_incident(title:str, severity:str):
    i=Incident(str(uuid4()),title,severity); _incidents[i.id]=i; return asdict(i)
def list_incidents(): return [asdict(x) for x in _incidents.values()]
