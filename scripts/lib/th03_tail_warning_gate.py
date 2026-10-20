"""Strict observed target-frame four-call transition validator. No native or EXE/MAP reads."""
from pathlib import Path
import hashlib
from lib.omf import parse_omf
from review_th03_cpu_link_order import omf,index
REFERENCE='.analysis/gpt-dots-tail-warning-probe-v08/compile-first-v01/source/obj/th03/warning.obj'
REFERENCE_SHA='67197a27bb95516f2322c218cc516544fc480c71c74de0db03158df8ff4cd02a'
SOURCE='.analysis/gpt-dots-warning-explicit-calls-stage-v01/warning.cpp'
SOURCE_SHA='6e98cfcd5841b821b2f9a5cadbb81d9cbf854c40816ce90b553eae1c3b044c88'
CALLS={0xca61:('@HUD_STATIC_GAUGE_LEVELS_PUT$QI',0xba91),0xca68:('@HUD_STATIC_GAUGE_LEVELS_PUT$QI',0xba91),0xcc46:('PALETTE_RESTORE_FOR_PID',0xa3a8),0xccd6:('PALETTE_RESTORE_FOR_PID',0xa3a8)}
ROWS=[dict(module='src/main/player/warning.cpp',segment='PLAYER_M_TEXT',start=0xc7a5)]
CRITICAL=('THEADR','LNAMES','SEGDEF','GRPDEF','EXTDEF','PUBDEF','LEDATA','FIXUPP','MODEND')
ALLOWED=set(CRITICAL)|{'COMENT','LINNUM'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def identity(f):return tuple(f[k] for k in ('site','kind','target_method','target','frame_method','frame'))
def expected_records(reference):
 """Construct comparison tuples only; never writes or substitutes an OMF object."""
 raw=Path(reference).read_bytes();need(sha(raw)==REFERENCE_SHA,'warning reference pin');records=parse_omf(raw);mod,blocks=omf(Path(reference),ROWS);need(mod==ROWS[0]['module'],'warning module');out=[];calls=0;fixups=0;block=None
 for ri,r in enumerate(records):
  d=r.data;need(r.name in ALLOWED,'warning reference supported records')
  if r.name=='LEDATA':
   block=next(b for b in blocks if b['record']==ri);si,k=index(d,0);off=int.from_bytes(d[k:k+2],'little');k+=2;d=bytearray(d)
   for a in CALLS:
    local=a-0xc7a5
    if off<=local and local+5<=off+len(d)-k:
     need(si==4,'warning code segment');p=k+local-off;need(d[p:p+5]==b'\x9a\0\0\0\0','warning old far bytes');d[p:p+5]=b'\x90\x0e\xe8\0\0';calls+=1
   d=bytes(d)
  elif r.name=='FIXUPP':
   need(block is not None,'warning FIXUPP owner');need(b''.join(bytes.fromhex(f['raw']) for f in block['fixups'])==d,'warning complete one-record FIXUPP coverage');chunks=[]
   for f in block['fixups']:
    b=bytes.fromhex(f['raw']);a=f['site']-1
    if a in CALLS:
     need(identity(f)==(a+1,3,2,CALLS[a][0],5,None),'warning old exact far identity');need(len(b)==4 and b[2]==0x56,'warning old far encoding');loc=((b[0]&3)<<8)|b[1];loc+=2;need(loc<1024,'warning near operand within LEDATA');b=bytes([0x84|(loc>>8),loc&255,0x56,b[3]]);fixups+=1
    chunks.append(b)
   d=b''.join(chunks)
  out.append((r.record_type,r.name,d))
 need(calls==fixups==4,'warning exactly four transitions')
 return out

def validate(path,repo):
 path=Path(path);repo=Path(repo);expected=expected_records(repo/REFERENCE);raw=path.read_bytes();rs=parse_omf(raw)
 need(all(r.name in ALLOWED for r in rs),'warning unsupported extra record')
 need([(r.name,r.data) for r in rs if r.name in CRITICAL]==[(n,d) for _,n,d in expected if n in CRITICAL],'warning exact four-call critical record delta')
 mod,blocks=omf(path,ROWS);fs=[f for b in blocks for f in b['fixups']]
 need(len(fs)==125 and sum(f['kind']==1 for f in fs)==88 and sum(f['kind']==3 for f in fs)==37,'warning125/88offset/37far')
 near=[f for f in fs if f['kind']==1 and f['target_method']==2 and not(int(f['raw'][:2],16)&64)];need(len(near)==11,'warning eleven genuine external near fixups')
 transitions=[]
 for a,(symbol,dest) in CALLS.items():
  hits=[f for f in fs if f['site']==a+3];need(len(hits)==1,'warning one exact near operand');f=hits[0]
  need(identity(f)==(a+3,1,2,symbol,5,None) and bytes.fromhex(f['raw'])[2]==0x56 and not(int(f['raw'][:2],16)&64),'warning exact target-frame56 selfrelative near identity')
  transitions.append(dict(call_site=a,operand_site=a+3,target=symbol,target_load_address=dest,required_link_group='MAIN_01',resolved_target_semantics='PENDING actual linked raw-byte gate',required_linked_displacement=(dest-a-5)&65535,stack_contract='NOP; PUSH CS; near CALL to unchanged far-return callee'))
 literals=[f['mz_site'] for f in fs if 'mz_site' in f];need(len(literals)==37,'warning37 real literal sites')
 return dict(code_bytes=1560,fixups=125,literal_sites=37,publics=7,offset16=88,pointer32=37,external_near=11,full_body_ABI_proof_rebound=False,object_body_ABI_structure_rebound=True,resolved_target_semantics='PENDING actual link',ABI_scope='All original code, operands, PUBDEF, allocation and fixup bytes unchanged except four explicit equivalent far-return call sequences. Object-only structure; four target-frame56 near-call resolved semantics are PENDING. Resolved operands and linked full-body equality still mandatory.',exact_four_transition_proof=transitions,literal_site_order=literals,object_sha256=sha(raw),reference_sha256=REFERENCE_SHA,projected_lowerings=0,accepted_credit=0)
