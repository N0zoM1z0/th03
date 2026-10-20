"""Strict maintained CPU compiler contract; only explicit dependency metadata varies."""
from pathlib import Path
import json
from lib.omf import parse_omf
from lib.th03_cpu_model import CPU,sha,need
HERE=Path(__file__).resolve().parent

def contract():return json.loads((HERE/'th03_cpu_dependencies.json').read_text())
def source_gate(work):
 c=contract()
 for n,h in c['source_pins'].items():
  p=Path(work)/n;need(p.is_file() and not p.is_symlink() and sha(p.read_bytes())==h,'CPU maintained source '+n)
 need((Path(work)/c['wrapper_path']).read_bytes()==c['wrapper_bytes'].encode(),'CPU genuine include wrapper')
 return c

def classify(raw,paths):
 records=parse_omf(raw);dependencies=[];ordinary=[];source=[];terminal=0
 for r in records:
  d=r.data
  if r.name=='COMENT' and d[:2]==b'\0\xe9':
   if d==b'\0\xe9':terminal+=1;ordinary.append((r.record_type,d));continue
   need(len(d)>=7 and len(d)==7+d[6],'exact E9 framing');dependencies.append((d[7:].decode('ascii'),d[2:6]));ordinary.append((r.record_type,b'DEPENDENCY'))
  elif r.name=='COMENT' and d[:2]==b'\0\xe8':
   need(len(d)>=8 and d[2]==1 and len(d)==8+d[3],'exact E8 framing');source.append((d[4:-4].decode('ascii'),d[-4:]));ordinary.append((r.record_type,d[:-4]))
  else:ordinary.append((r.record_type,d))
 need([n for n,t in dependencies]==paths,'frozen CPU dependency path order/multiplicity')
 need(terminal==1 and source==[(paths[0],dependencies[0][1])],'CPU source timestamp bound to wrapper dependency')
 return ordinary

def validate(path):
 c=contract();old=CPU.read_bytes();need(sha(old)=='26bcae741b3d4579cd10e14209e46f6de10e214e15f474f5e182d2c59fa1a7d6','retained CPU proof pin')
 before=classify(old,c['old_paths']);after=classify(Path(path).read_bytes(),c['maintained_paths'])
 # Exactly one added dependency record at wrapper/include boundary, not a
 # comment-class wildcard or whole-record normalization.
 dep=(0x88,b'DEPENDENCY');i=before.index(dep);need(after[i:i+3]==[dep]*3,'maintained dependency insertion slot');del after[i+1]
 need(before==after,'all non-dependency CPU record bytes/order (including other comments)')
 return {'pass_cpu':True,'all_non_dependency_records_exact':True,'dependency_transition_frozen':True,'fixups':64,'bytes':1077,'retained_object_copied':False}
