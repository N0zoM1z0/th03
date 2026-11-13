"""Unchanged original COM execution with bounded DOS/OPN device replies.

Driver adapter from TH04 port/modern-64 1ba7107 (MIT). TH03 supplies its own
COM files, installation flags, resources and independently checked identities.
"""
import struct
import hashlib
sha = lambda data: hashlib.sha256(data).hexdigest()
import unicorn as U
from unicorn.x86_const import *

READ_PORTS={2,0x88,0x8a,0x8c,0x8e,0x188,0x18a,0x18c,0x18e,0x288,0x28a,0x388,0x38a,0xa460,0xa468,0xa66e}
# PMD86 emits an A466 board volume byte during a running-song fade.
# It is recorded as an external hardware seam; no physical PCM is simulated.
WRITE_PORTS=READ_PORTS|{0,0x5f,0x71,0x77,0xa466}

class Driver:
 def __init__(self,data,filename,tail,load=0x2000,calibration_interval=100):
  self.data=data;self.filename=filename.removesuffix('.COM').ljust(8).encode()+b'COM';self.calibration_interval=calibration_interval;self.load=load;self.u=U.Uc(U.UC_ARCH_X86,U.UC_MODE_16);self.u.mem_map(0,0x110000)
  self.u.mem_write(load*16+0x100,self.data);self.u.mem_write(load*16,b'\xcd\x20');self.u.mem_write((load-1)*16+3,struct.pack('<H',0x5000));self.u.mem_write(load*16+0x2c,struct.pack('<H',0x900));self.u.mem_write(0x9000,b'\0\0\x01\0C:\\YUMEZIKU\\'+filename.encode()+b'\0')
  self.u.mem_write(load*16+0x80,bytes([len(tail)])+tail.encode()+b'\r')
  self.u.mem_write(0x2100,b'\xcf');self.u.mem_write(0x2200,b'\xf4')
  for n in range(256):self.u.mem_write(n*4,struct.pack('<HH',0,0x210))
  for r in (UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_ES,UC_X86_REG_SS):self.u.reg_write(r,load)
  self.u.reg_write(UC_X86_REG_IP,0x100);self.u.reg_write(UC_X86_REG_SP,0xff00)
  self.messages=[];self.read_ports=set();self.ports=[];self.ints=[];self.selected={};self.registers={};self.error=None;self.end=False;self.last=0;self.alloc=0x6000;self.ticks=0;self.a460=0x41;self.pic=255;self.instructions=0;self.fm_status=0
  self.u.hook_add(U.UC_HOOK_INTR,self.guarded_interrupt);self.u.hook_add(U.UC_HOOK_INSN,self.guarded_input,None,1,0,UC_X86_INS_IN);self.u.hook_add(U.UC_HOOK_INSN,self.guarded_output,None,1,0,UC_X86_INS_OUT)
  self.code_hook=self.u.hook_add(U.UC_HOOK_CODE,self.code)
 def installed(self):
  # All subsequent service/IRQ frames disable IF; the installation-only PIT
  # calibration cannot fire. Retain only the real return sentinel hook.
  self.u.hook_del(self.code_hook)
  def finished(u,address,size,user):self.end=True;u.emu_stop()
  self.code_hook=self.u.hook_add(U.UC_HOOK_CODE,finished,begin=0x2200,end=0x2200)
 def code(self,u,address,size,user):
  self.last=address;self.instructions+=1
  if self.instructions%self.calibration_interval==0 and (u.reg_read(UC_X86_REG_EFLAGS)&0x200) and not (self.pic&1) and self.vector(8)!=(0,0x210):
   flags=u.reg_read(UC_X86_REG_EFLAGS);ip,cs=self.vector(8);self.push(flags);self.push(self.reg(UC_X86_REG_CS));self.push(self.reg(UC_X86_REG_IP));u.reg_write(UC_X86_REG_CS,cs);u.reg_write(UC_X86_REG_IP,ip);u.reg_write(UC_X86_REG_EFLAGS,flags&~0x300)
  if address==0x2200:self.end=True;u.emu_stop()
 def guarded_input(self,u,p,size,user):
  if p not in READ_PORTS or size!=1:self.error=ValueError(f'unexpected IN {p:x}/{size}');self.end=True;u.emu_stop();return 0
  return self.input(u,p,size,user)
 def guarded_output(self,u,p,size,value,user):
  if p not in WRITE_PORTS or size!=1:self.error=ValueError(f'unexpected OUT {p:x}/{size}');self.end=True;u.emu_stop();return
  self.output(u,p,size,value,user)
 def output(self,u,p,size,v,user):
  self.ports.append([self.ticks,p,size,v])
  if p==0xa460:self.a460=v
  if p==2:self.pic=v
  if p in (0x88,0x8c,0x188,0x18c,0x288,0x28c):self.selected[p]=v
  elif p in (0x8a,0x8e,0x18a,0x18e,0x28a,0x28e):
   reg=self.selected.get(p-2,0);self.registers[(p-2,reg)]=v
   if reg==0x27:
    if v&0x10:self.fm_status&=~1
    if v&0x20:self.fm_status&=~2
 def input(self,u,p,size,user):
  self.read_ports.add(p)
  if p in (0x18c,0x18e) and not self.a460&1:return 255
  if p in (0x8a,0x8e,0x18a,0x18e,0x28a,0x28e):
   if self.selected.get(p-2,0)==255:return 1
   return self.registers.get((p-2,self.selected.get(p-2,0)),0)
  if p in (0x88,0x8c,0x188,0x18c,0x288,0x28c):return self.fm_status
  if p==0xa460:return self.a460
  return 0
 def reg(self,r):return self.u.reg_read(r)&65535
 def push(self,n):
  sp=(self.reg(UC_X86_REG_SP)-2)&65535;self.u.reg_write(UC_X86_REG_SP,sp);self.u.mem_write(self.reg(UC_X86_REG_SS)*16+sp,struct.pack('<H',n&65535))
 def vector(self,n):return struct.unpack('<HH',self.u.mem_read(n*4,4))
 def guarded_interrupt(self,u,n,user):
  try:self.interrupt(u,n,user)
  except Exception as e:self.error=e;self.end=True;u.emu_stop()
 def interrupt(self,u,n,user):
  ax=self.reg(UC_X86_REG_AX);bx=self.reg(UC_X86_REG_BX);cx=self.reg(UC_X86_REG_CX);dx=self.reg(UC_X86_REG_DX);ds=self.reg(UC_X86_REG_DS);self.ints.append([n,ax,bx,cx,dx])
  flags=u.reg_read(UC_X86_REG_EFLAGS)
  if n==0x2f and ax==0x1600:u.reg_write(UC_X86_REG_AX,0);return
  if n==0x21:
   ah=ax>>8;u.reg_write(UC_X86_REG_EFLAGS,flags&~1)
   if ah==2:return
   if ah==9:
    data=bytes(u.mem_read(ds*16+dx,min(2048,0x10000-dx)));end=data.find(b'$')
    if end<0:raise ValueError('unterminated DOS print adapter')
    self.messages.append(data[:end].hex());return
   if ah==0x30:u.reg_write(UC_X86_REG_AX,5);u.reg_write(UC_X86_REG_BX,0);return
   if ah==0x52:
    u.reg_write(UC_X86_REG_ES,0x800);u.reg_write(UC_X86_REG_BX,0x100);u.mem_write(0x8104,struct.pack('<HH',0x200,0x800));u.mem_write(0x8200,struct.pack('<HHH',65535,0,1));u.mem_write(0x8226,self.filename);u.mem_write(0x8217,struct.pack('<I',len(self.data)));return
   if ah==0x35:
    ip,cs=self.vector(ax&255);u.reg_write(UC_X86_REG_ES,cs);u.reg_write(UC_X86_REG_BX,ip);return
   if ah==0x25:u.mem_write((ax&255)*4,struct.pack('<HH',dx,ds));return
   if ah==0x48:u.reg_write(UC_X86_REG_AX,self.alloc);self.alloc+=bx+1;return
   if ah in (0x49,0x4a):return
   if ah in (0x31,0x4c):self.end=True;self.exit=ax;u.emu_stop();return
   if ah==0x2f:u.reg_write(UC_X86_REG_ES,self.load);u.reg_write(UC_X86_REG_BX,0x80);return
   raise ValueError(f'DOS {ax:04x} at {self.last:x}')
  if n in (0x60,0x64):
   ip,cs=self.vector(n);self.push(flags);self.push(self.reg(UC_X86_REG_CS));self.push(self.reg(UC_X86_REG_IP));u.reg_write(UC_X86_REG_CS,cs);u.reg_write(UC_X86_REG_IP,ip);u.reg_write(UC_X86_REG_EFLAGS,flags&~0x300);return
  raise ValueError(f'INT {n:02x}/{ax:04x} at {self.last:x}')
 def invoke(self,number,ax=0,dx=0):
  self.error=None;self.u.reg_write(UC_X86_REG_CS,0x220);self.u.reg_write(UC_X86_REG_IP,0)
  self.u.reg_write(UC_X86_REG_SS,self.load);self.u.reg_write(UC_X86_REG_SP,0xff00)
  self.u.reg_write(UC_X86_REG_AX,ax);self.u.reg_write(UC_X86_REG_DX,dx)
  self.u.reg_write(UC_X86_REG_DS,self.load)
  flags=2;ip,cs=self.vector(number);self.push(flags);self.push(0x220);self.push(0)
  self.u.reg_write(UC_X86_REG_CS,cs);self.u.reg_write(UC_X86_REG_IP,ip);self.u.reg_write(UC_X86_REG_EFLAGS,flags)
  self.run();return dict(ax=self.reg(UC_X86_REG_AX),bx=self.reg(UC_X86_REG_BX),dx=self.reg(UC_X86_REG_DX),ds=self.reg(UC_X86_REG_DS)-self.load)
 def run(self,limit=2000000):
  self.end=False;self.u.emu_start(self.reg(UC_X86_REG_CS)*16+self.reg(UC_X86_REG_IP),0x110000,count=limit)
  if self.error:raise self.error
  if not self.end:raise ValueError(f'bounded run exhausted at {self.last:x}')

 def service(self,ax):return self.invoke(0x60,ax)
 def irq(self,status):
  if status not in (0,1,2,3):raise ValueError('invalid OPN timer status')
  irq=[n for n in range(8,16) if self.vector(n)!=(0,0x210)]
  if len(irq)!=1:raise ValueError('resident FM vector ownership differs')
  self.fm_status=status;self.invoke(irq[0])
  if self.fm_status:raise ValueError('original IRQ did not clear injected timer flag')
 def write_resource(self,ax,data):
  address=self.service(ax);sizes=self.service(0x2200)
  limit=sizes['ax' if ax==0x600 else 'dx']*1024
  if len(data)>limit:raise ValueError('resource exceeds configured driver buffer')
  segment=self.load+address['ds'];offset=address['dx']
  if offset+limit>65536:raise ValueError('resident buffer crosses segment')
  self.u.mem_write(segment*16+offset,data)
  return dict(segment_relative=address['ds'],offset=offset,size=len(data),limit=limit,sha256=sha(data))
 def snapshot(self):
  return dict(measure=self.service(0x500)['ax'],volume=self.service(0x800)['ax'],status=self.service(0xa00)['ax'])
