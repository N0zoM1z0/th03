"""Independent scalar contracts against original/candidate relocated x86 instructions.
Historical ignored-path execution is documented separately; each run binds its actual source path. External device/game callees are ABI
fixtures; POLAR and foreground conversion execute actual image instructions.
"""
from pathlib import Path
import argparse,collections,hashlib,itertools,json,re,struct,sys,time
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
from lib.pc98 import parse_mz
import capstone
from functools import lru_cache
from importlib.metadata import version
from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn import x86_const as R
BASE=0x2000;CS=0x139d;DS=0x1d56;STACK=0x70000;SP=0xffc0
# entry, complete contribution size, far return, callee argument cleanup
FUNCS={'target':(0x2fb3,210,True,2),'reset':(0x3085,15,True,0),'add':(0x3094,41,True,4),'update':(0x30bd,127,True,0),'hit':(0x313c,169,True,0),'ring':(0x31e5,176,False,6),'render':(0x3295,355,True,0),'gauge':(0x33f8,504,False,2),'pellet':(0x35f0,24,True,0),'bullet':(0x3608,24,True,0)}
TABLE=(0x35d0,0x35f0)
# Foreign ABI contracts, not replacements for any owned instruction.
FOREIGN={(0xe8f,0x34a):('sound',1,2),(0x96e,0x205a):('hitcircle',3,6),(0xe8f,0x810):('sprite',3,6),(0x96e,0xcc8):('palette',1,2),(0x96e,0x377b):('axis',3,6),(CS,0x3d60):('bullets',0,0)}
REAL={(0xe8f,0x16d):(0x187,'polar',3),(0x96e,0xbf0):(0xc11,'screen',2)}
def sha(x):return hashlib.sha256(x).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def s16(x):x&=65535;return x-65536 if x&32768 else x
def word(x):return struct.pack('<H',x&65535)
@lru_cache(maxsize=16)
def instruction_map(image):
 decoder=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_16);allowed={}
 ranges=[(CS,e,TABLE[0] if k=='gauge' else e+n) for k,(e,n,_,_) in FUNCS.items()]+[(seg,start,end) for (seg,start),(end,_,_) in REAL.items()]
 for seg,start,end in ranges:
  ins=list(decoder.disasm(image[seg*16+start:seg*16+end],start));need(sum(i.size for i in ins)==end-start,'complete executable span decode')
  for i in ins:allowed[(seg,i.address)]=i.size
 return allowed

def run_case(mz,c):
 kind=c['kind'];pid=c.get('pid',0);state=c.get('state',2);frame=c.get('frame',0);x=c.get('x',2304);y=c.get('y',3200);flags=c.get('flags',0x602)
 allowed=instruction_map(bytes(mz.program_image));u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x100000);image=bytearray(mz.program_image)
 for r in mz.relocations:
  a=r.segment*16+r.offset;struct.pack_into('<H',image,a,(struct.unpack_from('<H',image,a)[0]+BASE)&65535)
 u.mem_write(BASE*16,bytes(image));data=(BASE+DS)*16;u.mem_write(data,bytes((i*13+7)&255 for i in range(65536)));u.mem_write(STACK,b'\xa5'*65536)
 def put(off,b):u.mem_write(data+off,b)
 def p8(off,v):put(off,bytes([v&255]))
 def p16(off,v):put(off,word(v))
 p8(0x2928,pid);p8(0x6590,c.get('pid_struct',1-pid));p8(0x38da,pid)
 put(0x4b80+pid*6,struct.pack('<BBHH',state,frame,x&65535,y&65535));p16(0x65be+pid*128,0xbeef)
 p16(0x659c,c.get('scroll0',-17));p16(0x659e,c.get('scroll1',29))
 # Trigonometric arrays overlap by design; fixture is arbitrary signed input,
 # not a claim to regenerate historical sine/cosine tables.
 for i in range(320):p16(0x316+2*i,((i*97+31)%1025)-512)
 box=c.get('box',(x-20,y-20,x+20,y+20))
 for off,v in zip((0x38ce,0x38d0,0x38d6,0x38d8),box):p16(off,v)
 p16(0x1dca+2*pid,c.get('boss',0));p16(0x1dc6,c.get('bossx',0x8123));p16(0x1dc8,c.get('bossy',0x7fff))
 for i in range(40):put(0x3ed6+i*48,b'\0'*48)
 for idx,ef,ep,ex,ey,formation in c.get('enemies',[]):
  off=0x3ed6+idx*48;p8(off,ef);p8(off+8,ep);p16(off+2,ex);p16(off+4,ey);p8(off+30,formation)
 p8(0x2d54+pid,c.get('active',2));p8(0x2d56+pid,c.get('level',1));p8(0x4b7e+pid,frame)
 p8(0x2d58+4*pid,c.get('count',29));p8(0x2d59+4*pid,c.get('speed',37))
 def setr(n,v):u.reg_write(getattr(R,'UC_X86_REG_'+n),v)
 def get(n):return u.reg_read(getattr(R,'UC_X86_REG_'+n))
 for n,v in dict(CS=BASE+CS,DS=BASE+DS,ES=0x3333,SS=STACK//16,SP=SP,BP=0x7777,SI=0x1357,DI=0x2468,AX=0xa135,BX=0xb246,CX=0xc357,DX=0xd468,EFLAGS=flags).items():setr(n,v)
 entry,size,far,cleanup=FUNCS[kind];ret=[0x1234,0x6000] if far else [0xff00]
 args={'target':[pid],'add':[y,x],'ring':[c.get('phase',0),c.get('radius',512),c.get('sprite',0x1234)],'gauge':[c.get('type',1)]}.get(kind,[])
 u.mem_write(STACK+SP,b''.join(word(v) for v in ret+args));expected=bytearray(u.mem_read(data,65536));initial_physical=bytes(u.mem_read(0,0x100000));pred=[];observed=[];raw_calls=[];visited=set();foreign_seen=set();stopped=False;errors=[];steps=0;result=None;pending_real=None
 def rd8(a):return expected[a]
 def rd16(a):return int.from_bytes(expected[a:a+2],'little')
 def wr(a,v,n=1):
  b=bytes([v&255]) if n==1 else word(v);expected[a:a+n]=b;pred.append(['write',a,n,int.from_bytes(b,'little')])
 def event(name,*a):pred.append([name,*[v&65535 for v in a]])
 slot=0x4b80+pid*6
 def screen(px):
  event('screen',pid,px);return ((s16(px)>>4)+(320 if pid else 0)+s16(rd16(0x659c+2*pid))+16)&65535
 def ring(sprite,radius,phase):
  cx=(x-256)&65535;cy=(y-256)&65535
  for i in range(16):
   angle=(frame*2+i*16)&255;rx=rd16(0x396+2*angle);ry=rd16(0x316+2*((angle+phase)&255))
   event('polar',cx,radius,rx);px=(s16(cx)+((s16(radius)*s16(rx))>>8))&65535
   event('polar',cy,radius,ry);py=(s16(cy)+((s16(radius)*s16(ry))>>8))&65535
   left=screen(px);top=(s16(py)>>4)+16;event('sprite',sprite,top,left)
 def gauge(typ):
  active=rd8(0x2d54+pid);flag=3 if typ==2 else 1
  if active==flag:
   wr(0x4b7e+pid,0);wr(0x2d54+pid,active+1);wr(0x2d58+4*pid,rd8(0x2d56+pid)+24);wr(0x2d59+4*pid,rd8(0x2d56+pid)+32);return
  if active!=flag+1:return
  f=rd8(0x4b7e+pid);other=1-pid
  if f%8==0:
   for a,v in [(0x68ee,typ),(0x68e2,rd8(0x2d59+4*pid)),(0x68e4,other),(0x68e3,0),(0x68e5,44),(0x68e7,rd8(0x2d58+4*pid))]:wr(a,v)
   vertices=[(2304,512),(1536,1280),(3072,1280),(1536,896),(3072,896),(2304,1664)]
   if 16<=f<=56:
    bx,by=vertices[f//8-2];wr(0x68de,bx,2);wr(0x68e0,by,2)
   if f==56:
    wr(0x2d54+pid,0)
    # Caller pushes a word at BP-1: high byte belongs to saved BP and is
    # not part of the pid_t parameter. Compare semantic low byte only.
    event('palette',other)
   if f<=40:
    bx,by=vertices[f//8];event('axis',other,by,bx)
   if f>=16:pred.append(['bullets',bytes(expected[0x68de:0x68ef]).hex()])
  wr(0x4b7e+pid,f+1)
 if kind=='reset':wr(0x4b80,0);wr(0x4b86,0)
 elif kind=='add':
  dest=0x4b80+6*rd8(0x6590);wr(dest,1);wr(dest+1,0);wr(dest+2,x,2);wr(dest+4,y,2)
 elif kind=='update':
  if state:
   f=(frame+1)&255;wr(slot+1,f)
   if state==1:
    yy=(y-64)&65535;wr(slot+4,yy,2)
    if f>=64 or s16(yy)<=0:wr(slot,2);wr(slot+1,0);event('sound',7)
   else:
    if f>=24 and f%2==0:event('sound',15)
    if f>=64:wr(slot,0)
   wr(0x65be+pid*128,0,2)
 elif kind=='target':
  if rd16(0x1dca+2*pid):wr(0x38e8,254);wr(0x3ece,rd16(0x1dc6),2);wr(0x3ed0,rd16(0x1dc8),2)
  else:
   formation=255;selected=None
   for i in range(40):
    a=0x3ed6+48*i;ex=s16(rd16(a+2));ey=s16(rd16(a+4));f=rd8(a+30)
    if rd8(a)!=1 or rd8(a+8)!=pid or not 0<=ex<=4608 or not 0<=ey<=6144 or f>=formation:continue
    formation=f;selected=a;wr(0x4adc,a,2)
    if f==0:break
   if selected is None:wr(0x3ece,2304,2);wr(0x3ed0,4800,2);wr(0x38e8,255)
   else:
    tx=(rd16(selected+2)-256)&65535;ty=(rd16(selected+4)+1760)&65535
    wr(0x3ece,tx,2);wr(0x3ed0,ty,2);wr(0x38e8,formation)
    if not (0<s16(tx)<4608 and 0<s16(ty)<6144):wr(0x3ece,2304,2);wr(0x3ed0,4800,2)
 elif kind=='hit':
  result=0;r=128 if state==1 else 896
  hit=state and s16(x-r)<=s16(box[2]) and s16(x+r)>=s16(box[0]) and s16(y-r)<=s16(box[3]) and s16(y+r)>=s16(box[1])
  if hit:
   if state==1:wr(slot,2);wr(slot+1,0);event('sound',7)
   else:event('hitcircle',pid,box[1],box[0]);result=1
 elif kind=='ring':ring(c.get('sprite',0x1234),c.get('radius',512),c.get('phase',0))
 elif kind=='render':
  if state:
   wr(0x1d8a,2);wr(0x1d88,16,2);wr(0x1d84,320*pid,2);wr(0x1d86,320*pid+319,2)
   sprite=rd8(0x6590)+0xc80+(4 if frame&1 else 0)
   if state==1:event('sprite',sprite,s16(y)>>4,screen(x)-16)
   elif frame<64:
    sprite+=0x500
    if frame<8:rings=[(frame*128,0)]
    elif frame<16:rings=[((frame-7)*128,32)]
    elif frame<24:rings=[((frame-15)*128,224)]
    elif frame<32:rings=[((frame-24)*128,0)]
    elif frame<40:rings=[((frame-31)*128,32)]
    elif frame<48:rings=[((frame-39)*128,224)]
    elif frame<56:rings=[((frame-47)*128,32),((frame-47)*128,224),((frame-48)*128,0)]
    else:rings=[((frame-48)*128,0)]
    for radius,phase in rings:ring(sprite,radius,phase)
 elif kind=='gauge':gauge(c.get('type',1))
 elif rd8(0x2d54+pid):gauge(1 if kind=='pellet' else 2)
 def onwrite(uc,access,address,n,value,user):
  if STACK+SP-128<=address and address+n<=STACK+SP:return
  observed.append(['write',address-data,n,value&((1<<(n*8))-1)])
 def hook(uc,address,n,user):
  nonlocal stopped,steps,pending_real
  steps+=1
  try:
   if address==(0x61234 if far else (BASE+CS)*16+0xff00):stopped=True;uc.emu_stop();return
   seg=get('CS')-BASE;off=get('IP');key=(seg,off)
   inside_real=any(seg==s and start<=off<end for (s,start),(end,_,_) in REAL.items())
   if pending_real is not None and not inside_real:
    target_ip,target_cs,target_sp=pending_real;need((off,get('CS'),get('SP'))==(target_ip,target_cs,target_sp),'actual dependency return frame');pending_real=None
   if key in FOREIGN:
    name,nargs,clean=FOREIGN[key];sp=get('SP');ip,cs=struct.unpack('<HH',uc.mem_read(STACK+sp,4));need(cs==BASE+CS and 0x2fb3<=ip<0x3620 and SP-128<=sp<SP,'foreign far-call return frame');a=list(struct.unpack('<'+'H'*nargs,uc.mem_read(STACK+sp+4,2*nargs))) if nargs else []
    raw_calls.append([name,*a])
    if name=='palette':a[0]&=255
    observed.append([name,bytes(uc.mem_read(data+0x68de,17)).hex()] if name=='bullets' else [name,*a]);foreign_seen.add(key)
    setr('SP',sp+4+clean);setr('CS',cs);setr('IP',ip);return
   if key in REAL:
    end,name,nargs=REAL[key];need(pending_real is None,'unexpected nested dependency');rsp=get('SP');rip,rcs=struct.unpack('<HH',uc.mem_read(STACK+rsp,4));need(rcs==BASE+CS and 0x2fb3<=rip<0x3620,'actual dependency caller');pending_real=(rip,rcs,rsp+(4 if name=='polar' else 8));a=list(struct.unpack('<'+'H'*nargs,uc.mem_read(STACK+get('SP')+4,2*nargs)));observed.append([name,*a]);foreign_seen.add(key)
   need(allowed.get(key)==n,'instruction boundary/size outside decoded whitelist')
   if inside_real:return
   need(seg==CS and 0x2fb3<=off<0x3620 and not TABLE[0]<=off<TABLE[1],'escape owned code or execute switch data: '+hex(seg)+':'+hex(off));visited.add(off)
  except Exception as e:errors.append(str(e));uc.emu_stop()
 u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_WRITE,onwrite);u.emu_start((BASE+CS)*16+entry,0x100000,count=20000)
 need(not errors and stopped,'terminal native return: '+str(errors));need(get('SP')==SP+len(ret)*2+cleanup,'near/far Pascal stack cleanup');need([get(n) for n in ['BP','SI','DI','DS','ES','SS']]==[0x7777,0x1357,0x2468,BASE+DS,0x3333,STACK//16],'callee-preserved registers');need(get('EFLAGS')&0x600==flags&0x600,'IF/DF preserved')
 if result is not None:need(get('AX')&255==result,'hit AL result')
 actual=bytes(u.mem_read(0,0x100000));want=bytearray(initial_physical);want[data:data+65536]=expected
 need(actual[:STACK+SP-128]==want[:STACK+SP-128] and actual[STACK+SP:]==want[STACK+SP:],'whole physical memory outside bounded 128-byte callee stack; caller frame unchanged')
 if observed!=pred:
  delta=next((i for i,(a,b) in enumerate(zip(observed,pred)) if a!=b),min(len(observed),len(pred)))
  raise ValueError('ordered stores/calls at '+str(delta)+' observed='+repr(observed[delta:delta+3])+' expected='+repr(pred[delta:delta+3]))
 need(pending_real is None,'unreturned actual dependency')
 observation=dict(registers={n:get(n) for n in ('AX','BX','CX','DX','SI','DI','BP','SP','CS','IP','DS','ES','SS','EFLAGS')},events=observed,raw_foreign_arguments=raw_calls,data_sha256=sha(actual[data:data+65536]),callee_stack_sha256=sha(actual[STACK+SP-128:STACK+SP]),caller_frame_sha256=sha(actual[STACK+SP:STACK+SP+32]))
 return visited,foreign_seen,steps,sha(json.dumps(observation,sort_keys=True,separators=(',',':')).encode())

def cases():
 for pid in (0,1):
  for kind in ('reset','add'):
   for y in (0,1,0x7fff,0x8000,0xffff):yield dict(kind=kind,pid=pid,y=y,x=0x8123)
  for state,frame,y in itertools.product((0,1,2,3,255),(0,22,23,24,62,63,64,254,255),(0,1,63,64,65,0x8000,0xffff)):yield dict(kind='update',pid=pid,state=state,frame=frame,y=y)
  yield dict(kind='target',pid=pid,boss=1)
  yield dict(kind='target',pid=pid,boss=65535,bossx=0,bossy=65535)
  yield dict(kind='target',pid=pid)
  for flag,ep,x,y,f in [(0,pid,1000,1000,1),(3,pid,1000,1000,1),(1,1-pid,1000,1000,1),(1,pid,-1,1000,1),(1,pid,4609,1000,1),(1,pid,1000,-1,1),(1,pid,1000,6145,1),(1,pid,1000,1000,255),(1,pid,256,1000,1),(1,pid,257,1000,1),(1,pid,4608,1000,1),(1,pid,1000,4384,1),(1,pid,1000,4383,1),(1,pid,1000,0,1),(1,pid,1000,6144,1),(1,pid,0,1000,1)]:yield dict(kind='target',pid=pid,enemies=[(39,flag,ep,x,y,f)])
  for forms in ((9,3,3,7),(3,0,1,0),(255,254,253,1)):
   yield dict(kind='target',pid=pid,enemies=[(i,1,pid,1000+i,1000+i,f) for i,f in enumerate(forms)])
  for state in (0,1,2,255):
   r=128 if state==1 else 896;x=2304;y=3200
   boxes=[(x,y,x,y),(x+r,y,x+r,y),(x+r+1,y,x+r+1,y),(x-r,y,x-r,y),(x-r-1,y,x-r-1,y),(x,y+r,x,y+r),(x,y+r+1,x,y+r+1),(x,y-r,x,y-r),(x,y-r-1,x,y-r-1)]
   for box in boxes:yield dict(kind='hit',pid=pid,state=state,box=box)
   for x,y in itertools.product((0,32767,32768,65535),repeat=2):yield dict(kind='hit',pid=pid,state=state,x=x,y=y,box=(0,0,65535,65535))
  for frame,phase,radius in itertools.product((0,1,63,127,128,255),(0,32,224,255),(0,128,-128,32767)):
   yield dict(kind='ring',pid=pid,frame=frame,phase=phase,radius=radius,x=0x8123,y=0x7ffe)
  for state,frame in itertools.product((0,1,2,255),(0,1,7,8,15,16,23,24,31,32,39,40,47,48,55,56,63,64,255)):yield dict(kind='render',pid=pid,state=state,frame=frame)
  for kind in ('gauge','pellet','bullet'):
   for typ in ((1,2,0,0x102) if kind=='gauge' else (1 if kind=='pellet' else 2,)):
    for active in (0,1,2,3,4,5,255):
     for frame in (0,1,7,8,15,16,24,32,40,48,56,57,64,248,255):yield dict(kind=kind,pid=pid,type=typ,active=active,frame=frame,level=255)
  # Additional level wrap boundaries and explicit opposite IF/DF state.
  for level in (0,1,223,224,231,232,254):
   for typ in (1,2):yield dict(kind='gauge',pid=pid,type=typ,active=typ*2-1,level=level)
  for kind in FUNCS:yield dict(kind=kind,pid=pid,flags=2)

MUTANTS=[
 ('target-default-x',0x302d,'0009','0109',dict(kind='target')),
 ('reset-state',0x308c,'00','01',dict(kind='reset')),
 ('add-state',0x30a7,'01','02',dict(kind='add')),
 ('update-delta',0x30e7,'40','41',dict(kind='update',state=1,y=1000)),
 ('hit-return',0x31dd,'01','00',dict(kind='hit',state=2)),
 ('ring-count',0x328c,'10','0f',dict(kind='ring')),
 ('render-width',0x32b3,'02','03',dict(kind='render',state=1)),
 ('gauge-speed',0x345f,'20','21',dict(kind='gauge',active=1)),
 ('pellet-type',0x3602,'01','02',dict(kind='pellet',active=1)),
 ('bullet-type',0x361a,'02','01',dict(kind='bullet',active=3)),
]

def run_controls(mz,raw):
 rows=[]
 for name,off,old,new,c in MUTANTS:
  start=CS*16+off;old=bytes.fromhex(old);new=bytes.fromhex(new);need(mz.program_image[start:start+len(old)]==old,'mutation site guard '+name)
  run_case(mz,c)
  data=bytearray(mz.program_image);data[start:start+len(old)]=new;bad=SimpleNamespace(program_image=bytes(data),relocations=mz.relocations)
  try:run_case(bad,c)
  except ValueError as e:rows.append(dict(name=name,rejected=True,reason=str(e)))
  else:raise ValueError('undetected semantic mutant '+name)
 return dict(kind='yumemi-charge-native-negative-controls',pass_=True,exe_sha256=sha(raw),model_sha256=sha(Path(__file__).read_bytes()),control_source_sha256=sha(Path(__file__).read_bytes()),source_inputs=closure(),package_versions=versions(),inputs_unchanged=True,controls=rows,target_files_modified=False,exact_acceptance=False)

def closure():
 return {str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in (Path(__file__).resolve(),ROOT/'scripts/lib/pc98.py',ROOT/'scripts/lib/__init__.py') if p.exists()}
def versions():return {k:version(k) for k in ('unicorn','capstone')}

def main():
 consumed=closure();packages=versions()
 p=argparse.ArgumentParser();p.add_argument('--exe',required=True);p.add_argument('--expected-sha256',required=True);p.add_argument('--output','--json',dest='output',required=True);p.add_argument('--negative-controls',action='store_true');p.add_argument('--seconds',type=int,default=240);a=p.parse_args();out=Path(a.output);need(not out.exists(),'fresh output required');raw=Path(a.exe).read_bytes();need(re.fullmatch('[0-9a-f]{64}',a.expected_sha256) and sha(raw)==a.expected_sha256,'pinned input identity');m=parse_mz(raw);need(m.valid,'valid MZ');
 if a.negative_controls:
  report=run_controls(m,raw);need(closure()==consumed and versions()==packages and sha(Path(a.exe).read_bytes())==sha(raw),'consumed input drift during controls');out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));return
 start=time.monotonic();seen=set();foreign=set();counts=collections.Counter();max_steps=0;observations=[]
 for i,c in enumerate(cases()):
  need(time.monotonic()-start<a.seconds,'bounded wall budget')
  try:v,f,n,digest=run_case(m,c)
  except Exception as e:raise ValueError('case '+str(i)+' '+repr(c)+': '+str(e)) from e
  seen.update(v);foreign.update(f);counts[c['kind']]+=1;max_steps=max(max_steps,n);observations.append([sha(json.dumps(c,sort_keys=True,separators=(',',':')).encode()),digest])
 decoder=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_16);coverage={};missing=[]
 for k,(entry,size,_,_) in FUNCS.items():
  end=TABLE[0] if k=='gauge' else entry+size;ins=list(decoder.disasm(m.program_image[CS*16+entry:CS*16+end],entry));need(sum(i.size for i in ins)==end-entry,'complete code decode');positions={i.address for i in ins};absent=positions-seen;missing+=sorted(absent);coverage[k]=dict(instructions=len(positions),visited=len(positions&seen),missing=sorted(absent))
 need(closure()==consumed and versions()==packages and sha(Path(a.exe).read_bytes())==sha(raw),'consumed input drift during run')
 report=dict(source_inputs=consumed,package_versions=packages,inputs_unchanged=True,kind='yumemi-charge-native-byte-semantic-model',pass_=not missing,exe_sha256=sha(raw),source_sha256=sha(Path(__file__).read_bytes()),cases=sum(counts.values()),case_counts=dict(counts),observations_sha256=sha(json.dumps(observations,separators=(',',':')).encode()),case_observation_digests=observations,coverage=coverage,visited=sorted(seen),foreign_entries=[list(x) for x in sorted(foreign)],maximum_instructions_per_case=max_steps,instruction_budget=20000,owned_extent_bytes=1645,owned_instruction_bytes=1613,switch_data_bytes=32,functions=10,external_contract='sound, sprite, hitcircle, palette, bomb-axis, bullets are declared no-side-effect ABI fixtures; polar and screen conversion run original image instructions',nontermination='No nontermination is claimed: owned enemy/switch/ring loops are bounded at 40/8/16; 20000 instruction exhaustion is failure, not success.',exact_acceptance=False,elapsed_seconds=time.monotonic()-start)
 out.write_text(json.dumps(report,indent=2)+'\n');need(not missing,'unvisited instruction positions: '+repr(missing));print(json.dumps(report))
if __name__=='__main__':main()
