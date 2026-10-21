"""Execute CFG/windows CPU bodies with independent memory-only foreign contracts.
No DOS, filesystem, graphics, or device implementation is executed.
"""
import hashlib, json, struct, time
from pathlib import Path
from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn import x86_const as reg
CS, DS, BASE = 0x95f, 0xe3f, 0x2000
RANGES = [(3,49),(0x34,282),(0x14e,56)]
# Explicit foreign ABI: far entry => (name, stack argument words).
FOREIGN = {(0,0x966):('open',2),(0,0x8b2):('read',3),(0,0x846):('close',0),
 (0,0x1a68):('rgb',2),(0,0x17d0):('palette',0),(0xc7e,0x934):('logo_all',3),
 (0xc7e,0x73e):('logo_single',4),(0xc7e,0x7c8):('winner_pic',4),
 (0,0x9a2):('seek',3),(0xc7e,0x9b7):('text',5)}
def sha(b): return hashlib.sha256(b).hexdigest()
class Probe:
 def __init__(self,mz,entry,payloads=(),result=0,flags=0x202):
  self.uc=Uc(UC_ARCH_X86,UC_MODE_16); self.uc.mem_map(0,0x100000)
  image=bytearray(mz.program_image)
  for r in mz.relocations:
   a=r.segment*16+r.offset;struct.pack_into('<H',image,a,(struct.unpack_from('<H',image,a)[0]+BASE)&65535)
  self.uc.mem_write(BASE*16,bytes(image));self.data=(BASE+DS)*16
  self.uc.mem_write(0x40000,b'\xa5'*65536)
  for k,v in dict(CS=BASE+CS,DS=BASE+DS,SS=0x4000,ES=0x3333,BP=0x7777,SI=0x1357,DI=0x2468,SP=0xfff0,EAX=0,EDX=0,EFLAGS=flags).items():self.set(k,v)
  self.uc.mem_write(0x4fff0,struct.pack('<H',0xff00))
  self.events=[];self.errors=[];self.stop=False;self.payloads=list(payloads);self.result=result;self.entry=entry
  self.foreign={(BASE+s)*16+o:(s,o) for s,o in FOREIGN}
  self.uc.hook_add(UC_HOOK_CODE,self.hook)
  self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write_hook)
 def write_hook(self,uc,access,address,size,value,user):
  # Executed CPU writes may only touch the current stack or declared outputs.
  outputs=[(self.data+0x21ea,self.data+0x21ee)] if self.entry==3 else [(self.data+x,self.data+x+1) for x in (0x1378,0x13b5,0x13f2)] if self.entry==0x34 else []
  if not any(lo<=address and address+size<=hi for lo,hi in [(0x40000,0x50000)]+outputs):
   self.errors.append('CPU write outside stack/declared output');uc.emu_stop()
 def get(self,k):return self.uc.reg_read(getattr(reg,'UC_X86_REG_'+k))
 def set(self,k,v):self.uc.reg_write(getattr(reg,'UC_X86_REG_'+k),v)
 def write(self,off,b):self.uc.mem_write(self.data+off,b)
 def hook(self,uc,a,n,u):
  try:
   if a==(BASE+CS)*16+0xff00:
    assert self.get('CS')==BASE+CS;self.stop=True;uc.emu_stop();return
   if a in self.foreign:
    s,o=self.foreign[a];assert self.get('CS')==BASE+s
    name,count=FOREIGN[s,o];sp=self.get('SP');words=list(struct.unpack('<'+'H'*(count+2),uc.mem_read(0x40000+sp,4+count*2)));args=words[2:]
    self.events.append([name,args])
    if name=='read':
     blob=self.payloads.pop(0);assert len(blob)<=args[0]
     if blob:uc.mem_write(args[2]*16+args[1],blob)
    self.set('AX',self.result)
    self.set('SP',sp+4+count*2);self.set('CS',words[1]);self.set('IP',words[0]);return
   off=a-(BASE+CS)*16
   start,size=next(x for x in RANGES if x[0]==self.entry)
   assert self.get('CS')==BASE+CS and start<=off<start+size,'escaped scope'
  except Exception as e:self.errors.append(str(e));uc.emu_stop()
 def run(self):
  self.uc.emu_start((BASE+CS)*16+self.entry,0x100000,count=2000)
  assert not self.errors and self.stop, self.errors or 'no return'
  assert self.get('SP')==0xfff2 and [self.get(x) for x in ('BP','SI','DI')]==[0x7777,0x1357,0x2468],'near ABI'
  assert self.get('DS')==BASE+DS and self.get('SS')==0x4000,'segment ABI'
  assert not self.payloads,'missing reads'
 def snapshot(self):return bytes(self.uc.mem_read(self.data,0x4000))
def cfg_case(mz,segment,n,result,flags=0x202):
 raw=b'\x91\x82\x73\x64\x55'+struct.pack('<H',segment)+b'\x46'
 p=Probe(mz,3,[raw[:n]],result,flags);before=bytearray(p.snapshot());p.run()
 expected=bytearray(b'\xa5'*8);expected[:n]=raw[:n];value=struct.unpack_from('<H',expected,5)[0]
 before[0x21ea:0x21ee]=struct.pack('<HH',0,value)
 assert p.snapshot()==before,'CFG data writes'
 assert p.get('AX')==value,'CFG return'
 assert p.events==[['open',[0x35a,BASE+DS]],['read',[8,0xffe6,0x4000]],['close',[]]],'CFG interfaces'
 return dict(kind='cfg',segment=segment,n=n,result=result,flags=flags,value=value,events=p.events)
def window_case(mz,a,b,winner,stage,lengths=(60,60,60),result=0,flags=0x202):
 blobs=[bytes((r*67+i*11+3)&255 for i in range(n)) for r,n in enumerate(lengths)]
 p=Probe(mz,0x34,blobs,result,flags)
 p.write(0x21ea,struct.pack('<HH',0x120,0x5000));p.uc.mem_write(0x50137,bytes([winner]));p.uc.mem_write(0x50153,bytes([stage]))
 p.write(0x13f3,bytes([a,b]));p.write(0x133c,b'\xce'*183)
 # Synthetic pointer tables separate input control from candidate table contents.
 for i in range(128):
  # Only valid winner IDs are table indexed; loser bytes may span all uint8.
  if i<9:
   p.write(0x90+i*2,struct.pack('<H',0x600+i*13));p.write(0xa2+i*4,struct.pack('<HH',0x700+i*17,0x6100+i))
 before=bytearray(p.snapshot());p.run()
 c=(a if winner==0 else b);char=c//2;message=(9 if stage==6 else 10 if stage==7 else b//2) if winner==0 else a//2
 expected=[['rgb',[0x363,BASE+DS]],['palette',[]],['logo_all',[0x36d,BASE+DS,0]],
 ['logo_single',[0,0x376,BASE+DS,5]],['winner_pic',[c&1,0x600+char*13,BASE+DS,6]],
 ['open',[0x700+char*17,0x6100+char]],['seek',[0,message*180,0]]]
 for row,blob in enumerate(blobs):
  at=0x133c+61*row;expected.append(['read',[60,at,BASE+DS]]);before[at:at+len(blob)]=blob;before[at+60]=0
 expected.append(['close',[]])
 assert p.events==expected,('window interfaces',p.events,expected)
 assert p.snapshot()==before,'window data writes or missing NUL'
 assert p.get('AX')==result,'close return preserved'
 return dict(kind='window',a=a,b=b,winner=winner,stage=stage,lengths=list(lengths),result=result,flags=flags,events=p.events,text=bytes(before[0x133c:0x13f3]).hex())
def text_case(mz,result,flags):
 p=Probe(mz,0x14e,(),result,flags);p.write(0x133c,bytes((i*7)&255 for i in range(183)));before=p.snapshot();p.run()
 assert p.events==[['text',[0x133c+61*r,BASE+DS,0x2f,272+16*r,80]] for r in range(3)],'text ABI/coordinates'
 assert p.snapshot()==before and p.get('AX')==result,'text data/return'
 return dict(kind='text',result=result,flags=flags,events=p.events)
def matrix(mz):
 rows=[]
 for segment in (0,1,0x5678,0xffff):
  for n in range(9):
   for result in (0,0xffff):rows.append(cfg_case(mz,segment,n,result))
 for a in range(18):
  for b in range(18):rows.append(window_case(mz,a,b,0,0))
 for c in range(18):
  for winner,stage in ((0,6),(0,7),(1,6),(255,7)):
   rows.append(window_case(mz,c,17-c,winner,stage))
 for lengths in ((0,0,0),(1,30,59),(60,0,7)):
  for flags in (0x202,0x603):
   rows.append(window_case(mz,17,0,0,255,lengths,0xffff,flags))
 for loser in (18,127,128,254,255):rows.append(window_case(mz,17,loser,0,255,(0,30,60),0xffff))
 for n in (0,6,7,8):rows.append(cfg_case(mz,0x4321,n,0xffff,0x603))
 for result in (0,1,0xffff):
  for flags in (0x202,0x603):rows.append(text_case(mz,result,flags))
 return rows

def analyze(image):
 from capstone import Cs,CS_ARCH_X86,CS_MODE_16
 from capstone.x86_const import X86_OP_IMM
 decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
 for start,size in RANGES:
  body=image[CS*16+start:CS*16+start+size];ins=list(decoder.disasm(body,start));bounds={i.address for i in ins};edges=[]
  assert sum(i.size for i in ins)==size and ins[-1].mnemonic=='ret' and not ins[-1].op_str,'complete near body'
  for i in ins:
   if i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall'):
    assert all(o.type==X86_OP_IMM for o in i.operands),'indirect edge'
    dest=tuple(o.imm for o in i.operands)
    if i.mnemonic=='lcall':assert dest in FOREIGN,'foreign ABI'
    else:assert i.mnemonic!='call' and dest[0] in bounds,'branch outside instruction boundaries'
    edges.append([i.address,i.mnemonic,list(dest)])
  rows.append(dict(start=start,size=size,instructions=len(ins),sha256=sha(body),edges=edges))
 return rows
