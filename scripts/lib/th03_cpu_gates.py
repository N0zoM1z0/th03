"""Read-only CPU retained probe gates. No subprocesses or OMF changes."""
from pathlib import Path
import json,sys,struct,hashlib
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
from lib.th03_cpu_model import B,CPU,ROOT,PINS,sha,need,expectation
from lib.omf import parse_omf
from lib.pc98 import parse_mz
from review_th03_cpu_link_order import rows,omf,mz
DISPATCH=0xdb0f
NEW_PUBLICS={'_cpu_dodge_patterns':('_DATA',0x67e),'_cpu_retry_directions':('_DATA',0x756),'_cpu_dodge_pattern':('_BSS',0x38ea)}
def index(d,i):
 need(i<len(d),'index bound');v=d[i];i+=1
 if v&128:need(i<len(d),'wide index bound');v=((v&127)<<8)|d[i];i+=1
 return v,i

def describe(path,maprows):
 records=parse_omf(Path(path).read_bytes());names=[''];segments=[];data={};coverage={};ext=[];pub=[]
 for r in records:
  d=r.data
  need(r.name not in ('LIDATA32','COMDAT','COMDAT32','COMDEF','LCOMDEF','LEDATA32','FIXUPP32','SEGDEF32','LPUBDEF','PUBDEF32','LEXTDEF'),'unsupported allocation/dialect '+r.name)
  if r.name=='LNAMES':
   i=0
   while i<len(d):n=d[i];i+=1;need(i+n<=len(d),'lname bound');names.append(d[i:i+n].decode('ascii'));i+=n
  elif r.name=='SEGDEF':
   need(d[0]>>5!=0,'SEGDEF dialect');n,i=index(d,3);c,i=index(d,i);o,i=index(d,i);need(i==len(d),'SEGDEF trailing');segments.append((names[n],int.from_bytes(d[1:3],'little'),d[0],names[c],names[o]))
  elif r.name=='LEDATA':
   si,i=index(d,0);off=int.from_bytes(d[i:i+2],'little');i+=2;n,z,*_=segments[si-1];need(off+len(d)-i<=z,'data bound');data.setdefault(n,bytearray(z));coverage.setdefault(n,bytearray(z));need(not any(coverage[n][off:off+len(d)-i]),'LEDATA overlap');data[n][off:off+len(d)-i]=d[i:];coverage[n][off:off+len(d)-i]=b'\1'*(len(d)-i)
  elif r.name=='EXTDEF':
   i=0
   while i<len(d):n=d[i];i+=1;name=d[i:i+n].decode('ascii');i+=n;t,i=index(d,i);ext.append((name,t))
  elif r.name=='PUBDEF':
   g,i=index(d,0);s,i=index(d,i)
   segname=segments[s-1][0] if s else 'ABS:'+d[i:i+2].hex()
   if not s:i+=2
   while i<len(d):
    n=d[i];i+=1;name=d[i:i+n].decode('ascii');i+=n;off=int.from_bytes(d[i:i+2],'little');i+=2;t,i=index(d,i);pub.append((name,g,segname,off,t))
 mod,blocks=omf(Path(path),maprows)
 return dict(records=records,segments=segments,data=data,coverage=coverage,ext=ext,pub=pub,module=mod,blocks=blocks)
def fixups(obj):return [dict(f,segment=b['segment']) for b in obj['blocks'] for f in b['fixups']]
def identity(f):
 raw=bytes.fromhex(f['raw']);need(len(raw)>=3,'fixup raw bound');fd=raw[2]
 return (f['site'],f['segment'],f['kind'],bool(raw[0]&0x40),f['target_method'],f['target'],f['frame_method'],f['frame'],bool(fd&4),None if fd&4 else int.from_bytes(raw[-2:],'little'))
def root_gate(path):
 expectation() # All immutable baseline and CPU pins, plus frozen derivation.
 rs=rows(B/'obj/th03/main.map');old=describe(B/'obj/th03/main.obj',rs)
 newrs=[dict(r,size=664) if r['module']=='th03_main.asm' and r['segment']=='PLAYER_M_TEXT' else r for r in rs]
 new=describe(path,newrs);need(new['module']==old['module']=='th03_main.asm','module identity')
 expected=[(n,664 if n=='PLAYER_M_TEXT' else z,a,c,o) for n,z,a,c,o in old['segments']];need(new['segments']==expected,'entire SEGDEF vector')
 for typ in ('LIDATA','GRPDEF','LNAMES','MODEND'):
  need([r.data for r in new['records'] if r.name==typ]==[r.data for r in old['records'] if r.name==typ],'complete '+typ)
 dispatch='@PLAYER_CPU_UPDATE$QP14PLAYER_STUFF_T'
 need(new['ext'].count((dispatch,0))==1,'one dispatcher import')
 need([x for x in new['ext'] if x[0]!=dispatch]==old['ext'],'all existing EXTDEF order/type')
 need([x for x in new['pub'] if x[0] not in NEW_PUBLICS]==old['pub'],'all existing PUBDEF order/address/type')
 for name,(segment,ds) in NEW_PUBLICS.items():
  matches=[x for x in new['pub'] if x[0]==name];need(len(matches)==1,'single storage alias '+name)
  row=next(r for r in rs if r['module']==old['module'] and r['segment']==segment)
  need(matches[0][1:]==(1,segment,0x1d560+ds-row['start'],0),'exact existing storage alias '+name)
 of=[f for f in fixups(old) if not 0xc370<=f['site']<0xc7a5];nf=fixups(new)
 # All symbolic frames/targets, location modes and explicit displacements remain
 # exact, except the one source-authorized internal-to-external dispatcher call.
 om={f['site']:identity(f) for f in of};nm={f['site']:identity(f) for f in nf}
 need(len(om)==len(of) and len(nm)==len(nf),'unique operand sites')
 need(om.pop(DISPATCH)==(DISPATCH,'MAIN_010_TEXT',1,False,0,'PLAYER_M_TEXT',1,2,True,None),'old genuine dispatcher binding')
 need(nm.pop(DISPATCH)==(DISPATCH,'MAIN_010_TEXT',1,False,2,dispatch,1,2,True,None),'new exact dispatcher binding')
 need(nm==om,'every surviving symbolic fixup identity/addend')
 for n,z,*_ in new['segments']:
  before=old['data'].get(n,bytearray(dict((s[0],s[1]) for s in old['segments'])[n]))[:z];after=new['data'].get(n,bytearray(z))
  need(old['coverage'].get(n,bytearray(len(before)))[:z]==new['coverage'].get(n,bytearray(z)),'coverage '+n)
  if n=='MAIN_010_TEXT':
   off=DISPATCH-next(r['start'] for r in rs if r['module']==old['module'] and r['segment']==n)
   need(before[off-1]==after[off-1]==0xe8 and after[off:off+2]==b'\0\0','dispatcher E8 zero external addend')
   need(int.from_bytes(before[off:off+2],'little')==0xc54a-0xc0d8,'old dispatcher target offset')
   before=before[:off]+b'\0\0'+before[off+2:]
  need(before==after,'all emitted bytes and operand addends '+n)
 need(len(new['coverage']['PLAYER_M_TEXT'])==664 and all(new['coverage']['PLAYER_M_TEXT']),'complete genuine prefix')
 lower={(0x2c49,3,0,'_TEXT',5,None),(0x2c82,3,0,'_TEXT',5,None)}
 far=[f for f in nf if 'mz_site' in f];survivors=[];known=[]
 for f in far:
  key=tuple(f[k] for k in ('site','kind','target_method','target','frame_method','frame'))
  (known if key in lower else survivors).append(f)
 need(len(far)==423 and len(known)==2 and len(survivors)==421,'root FAR counts')
 prior=mz(B/'bin/th03/main.exe',rs);expected=[r['site'] for r in prior if r['module']==old['module'] and not 0xc370<=r['site']<0xc7a5]
 need([f['mz_site'] for f in survivors]==expected,'complete residual root421 actual FIXUPP traversal')
 prefix=[f for f in nf if 0xc0d8<=f['site']<0xc370 and f['target']=='_TEXT'];need(len(prefix)==6,'six genuine same-module prefix references')
 return dict(pass_prelink_root=True,root_sha256=sha(Path(path).read_bytes()),residual_literal_count=421,far_fixups=423,all_surviving_fixups=len(nf),prefix_same_module_refs=6,all_emitted_bytes_and_addends_equal=True)


def linked_bytes(work):
 model=json.loads((HERE/'th03_cpu_expectation.json').read_text());before=(B/'bin/th03/main.exe').read_bytes();raw=(Path(work)/'bin/th03/main.exe').read_bytes();a=parse_mz(before);b=parse_mz(raw)
 need(a.valid and b.valid,'valid MZ');need(a.program_image==b.program_image,'entire load image including outside CPU')
 pairs=lambda m:[[r.segment,r.offset] for r in m.relocations]
 need(pairs(b)==model['complete_literal_pairs'],'complete predicted literal1553')
 outside=[[r.segment,r.offset] for r in b.relocations if not 0xc370<=r.linear<0xc7a5]
 need(outside==model['outside_literal_pairs'],'outside literal1551')
 off=struct.unpack_from('<H',raw,24)[0];end=off+4*1553
 need(raw[:off]==before[:off] and raw[end:]==before[end:],'all file bytes outside exact relocation table')
 target=(ROOT/'.analysis/targets/th03/main.exe').read_bytes();need(sha(target)=='f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b','original target identity');t=parse_mz(target)
 need(b.program_image[0xc370:0xc7a5]==t.program_image[0xc370:0xc7a5],'CPU entire original1077')
 need([[r.segment,r.offset] for r in b.relocations if 0xc370<=r.linear<0xc7a5]==[[r.segment,r.offset] for r in t.relocations if 0xc370<=r.linear<0xc7a5],'CPU target literal order')
 return dict(pass_bytes=True,whole_load_image_equal=True,outside1551_equal=True,full1553_predicted_equal=True,all_non_relocation_file_bytes_equal=True)
