"""Finite charge root transition; read-only. No relocation or record normalization.
Only dependency timestamps are outside nondependency record expectation; dependency
names/order are checked separately. The enclosing build must bind actual mtimes.
"""
import sys,json,hashlib,argparse
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from lib.th03_cpu_gates import describe,fixups,identity,rows
D=Path(__file__).resolve().parent
A=ROOT/Path('.analysis/th03-main-exact/gpt-dots-player-cpu-default-cold-v01/round1/source')
B=Path('.analysis/toolchain/wineprefix/drive_c/MCY01')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def need(v,s):
 if not v:raise ValueError(s)
def deps(o):
 out=[]
 for r in o['records']:
  if r.name=='COMENT' and r.data[:2]==b'\x40\xe9':
   d=r.data
   if len(d)==2:out.append(None);continue
   need(len(d)>=7 and len(d)==7+d[6],'dependency shape');out.append(d[7:].decode('ascii'))
 return out
def records(o):return [[r.record_type,r.data.hex()] for r in o['records'] if not(r.name=='COMENT' and r.data[:2]==b'\x40\xe9')]
def check(obj,mapfile,contract):
 c=json.loads(Path(contract).read_text());need(sha(A/'obj/th03/main.obj')==c['old_obj_sha256'],'accepted root pin');need(sha(A/'obj/th03/main.map')==c['old_map_sha256'],'accepted MAP pin')
 a=describe(A/'obj/th03/main.obj',rows(A/'obj/th03/main.map'));b=describe(obj,rows(mapfile))
 need(b['module']==a['module']=='th03_main.asm','module')
 need(b['segments']==[(n,0 if n=='PELLET_PUT' else z,at,cl,ov) for n,z,at,cl,ov in a['segments']],'only owner segment removal')
 for typ in ('LIDATA','GRPDEF','LNAMES','MODEND','THEADR'):
  need([r.data for r in a['records'] if r.name==typ]==[r.data for r in b['records'] if r.name==typ],typ)
 need(deps(b)==deps(a),'all dependency names/order')
 need(b['ext']==[tuple(x) for x in c['expected_ext']],'exact ordered EXTDEF')
 need(b['pub']==[tuple(x) for x in c['expected_pub']],'exact ordered PUBDEF')
 af=[identity(f) for f in fixups(a)];bf=[identity(f) for f in fixups(b)]
 removal=[f for f in af if f[1]=='PELLET_PUT'];need(len(removal)==117,'117 owned fixups')
 swaps={v['old'][0]:(tuple(v['old']),tuple(v['new'])) for v in c['dispatch_changes']};need(len(swaps)==24,'24 dispatch fields')
 expected=[]
 for f in af:
  if f[1]=='PELLET_PUT':continue
  if f[0] in swaps:need(f==swaps[f[0]][0],'old dispatch');f=swaps[f[0]][1]
  expected.append(f)
 need(bf==expected,'all surviving fixup identities and traversal order')
 for n,z,*_ in b['segments']:
  before=bytearray(a['data'].get(n,bytearray(z))[:z]);after=b['data'].get(n,bytearray(z))
  need(a['coverage'].get(n,bytearray(z))[:z]==b['coverage'].get(n,bytearray(z)),'coverage '+n)
  if n=='HITCIRC_TEXT':
   start=next(r['start'] for r in rows(A/'obj/th03/main.map') if r['module']==a['module'] and r['segment']==n)
   for old,new in swaps.values():
    if old[2]==1:
     off=old[0]-start;need(int.from_bytes(before[off:off+2],'little')==c['old_addends'][new[5]],'original named target offset');before[off:off+2]=b'\0\0'
  need(before==after,'all surviving bytes/addends '+n)
 need(records(b)==c['expected_nondependency_records'],'complete ordered nondependency record vector')
 return dict(pass_root_transition=True,removed_owner_bytes=1645,removed_owned_fixups=117,externalized_dispatch_fields=24,surviving_ordered_fixups=len(bf),unchanged_other_fixups=len(bf)-24,all_remaining_storage_and_bytes_equal=True,dependency_names_order_equal=True)

def verify(obj):
 contract=D/"th03_charge_root_contract.json"
 need(sha(contract)=="b5ac26eacea68a8ba25313dbc894f70bf88d16dd6e9327e72aeb5b17baecad40","root contract identity")
 return check(Path(obj),Path(obj).with_suffix(".map"),contract)
