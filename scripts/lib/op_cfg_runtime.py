"""Independent file/resident contracts for three real near OP cfg functions.

The actual PMD-mode and F_SCOPY helper instructions execute. File services and
PMD replies are bounded interfaces; no DOS filesystem or device is emulated.
Uninitialized save bytes and unchecked partial cfg reads remain target behavior.
"""
import hashlib
import json
import struct
from dataclasses import replace

from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
from unicorn.x86_const import *
from lib.op_cfg_layout import SEGMENT,OFFSET,DATA_SEGMENT,FUNCTIONS

REG={n:globals()['UC_X86_REG_'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp','sp','cs','ds','es','ss','ip')}
ENTRIES={name:(SEGMENT*16+OFFSET+off,size) for _,name,off,size in FUNCTIONS}
SERVICES={0x9A8:('open',4),0x8F4:('read',6),0x7C8:('append',4),0xA26:('write',6),0x9E4:('seek',6),0x888:('close',0)}
RESIDENT,ACTIVE,FM,MIDI,DISABLED=0x2464,0x5DC,0x1A0A,0x1A0B,0x90
COPY_START,COPY_SIZE,MODE_START,MODE_SIZE=0x337E,28,0xBEFA,29


def need(value,message):
    if not value:raise ValueError('OP cfg contract: '+str(message))

def parity(v):return 4 if (v&255).bit_count()%2==0 else 0

def reply(registers,index,seed,flags,status):
    result=dict(registers)
    for j,n in enumerate(('ax','bx','cx','dx','es')):result[n]=(seed^(0x1357+index*0x101+j*0x231))&65535
    result['ax']=status
    return result,(flags&0x600)|((seed+index*0x149)&0x8D5)|2


class Prediction:
    def __init__(self,initial,registers,data,stack,kind,cfg,read_bytes,resoff,resseg,driver,midi,seed,flags,status):
        self.memory=bytearray(initial);self.regs=dict(registers);self.data=data;self.stack=stack
        self.kind,self.cfg,self.read_bytes=kind,cfg,read_bytes;self.resoff,self.resseg=resoff,resseg
        self.driver,self.midi,self.seed,self.flags,self.status=driver,midi,seed,flags,status
        self.events=[];self.count=0;self.file=bytearray(cfg);self.local=stack-10
        self.flags_mask,self.flags_value=0x8D5,0;self.env_flags=flags&~(0x400 if kind=='cfg_save_exit' else 0)
    def store(self,address,size,value):
        self.events.append(('store',address,size,value));self.memory[address:address+size]=value.to_bytes(size,'little')
    def service(self,kind,payload=None):
        self.events.append(('file',kind,payload));self.count+=1
        self.regs,self.flags_value=reply(self.regs,self.count,self.seed,self.env_flags,self.status)
    def run(self):
        local=bytearray(self.memory[0x70000+self.local:0x70000+self.local+8])
        if self.kind=='cfg_load':
            self.service('open',b'YUME.CFG\0'.hex());self.service('read',(0x7000,self.local,8))
            local[:self.read_bytes]=self.cfg[:self.read_bytes]
            self.service('close');segment=int.from_bytes(local[5:7],'little')
            need(segment<=0xFFFE,'resident storage below the mapped real-mode boundary')
            self.resoff,self.resseg=0,segment;self.store(self.data+RESIDENT+2,2,segment);self.store(self.data+RESIDENT,2,0)
            base=segment*16;self.store(base+0x15,1,local[0])
            self.events.append(('PMD',0x900|local[0]));self.count+=1
            self.regs,self.flags_value=reply(self.regs,self.count,self.seed,self.env_flags,self.status)
            available=self.driver!=0xFF;active=1 if available else self.midi
            if available:self.store(self.data+FM,1,1)
            self.store(self.data+ACTIVE,1,active);self.store(self.data+DISABLED,1,0)
            if not active:
                self.store(base+0x15,1,0);self.store(self.data+DISABLED,1,1)
            elif not local[0]:self.store(self.data+ACTIVE,1,0)
            self.store(base+0x16,1,local[1]);self.store(base+0xB,1,local[2])
            self.regs.update(ax=local[2],bx=0,es=segment)
            value=local[0] if active and local[0] else 0
            self.flags_value=parity(value)|(64 if not value else 0)|(value&128)
        else:
            if self.kind=='cfg_save_exit':
                local[:]=bytes(8);self.events.append(('copy',self.regs['ds'],0x91,0x7000,self.local,8))
            self.service('append',b'YUME.CFG\0'.hex());self.service('seek',(0,0))
            base=self.resseg*16+self.resoff
            for i,offset in enumerate((0x15,0x16,0xB)):local[i]=self.memory[base+offset]
            count=8 if self.kind=='cfg_save_exit' else 4
            self.service('write',(0x7000,self.local,count,bytes(local[:count]).hex()))
            self.file[:count]=local[:count];self.service('close')


class Machine:
    def __init__(self,mz,load):
        need(mz.valid,'valid decoded MZ')
        self.base=load*16;self.cs=load+SEGMENT;self.ds=load+DATA_SEGMENT;self.data=self.ds*16
        self.uc=Uc(UC_ARCH_X86,UC_MODE_16);self.uc.mem_map(0,1<<20)
        self.initial=bytearray(b'\xA5'*(1<<20));body=mz.relocated_program_image(load);self.initial[self.base:self.base+len(body)]=body
        self.instructions={};self.owned={p for start,size in ENTRIES.values() for p in range(start,start+size)}
        for start,size in (*ENTRIES.values(),(COPY_START,COPY_SIZE),(MODE_START,MODE_SIZE)):
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+size],start))
            need(sum(r.size for r in rows)==size,'whole root/helper instruction boundaries')
            self.instructions.update({r.address:r.size for r in rows})
        self.covered=set();self.maximum_stack=0
        self.hooks=[self.uc.hook_add(UC_HOOK_CODE,self.code),self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write),self.uc.hook_add(UC_HOOK_INTR,self.interrupt)]
    def close(self):
        for hook in self.hooks:self.uc.hook_del(hook)
        self.hooks=[];self.uc=None
    def r(self,n):return self.uc.reg_read(REG[n])&65535
    def fail(self,error):self.error=str(error);self.uc.emu_stop()
    def event(self,event):
        need(self.index<len(self.expected.events) and event==self.expected.events[self.index],f'ordered cfg event #{self.index}: {event}')
        self.index+=1
    def code(self,uc,address,size,_):
        try:
            if address==self.cs*16+0xFFFF:self.returned=True;uc.emu_stop();return
            rva=address-self.base
            if rva in SERVICES:
                kind,args=SERVICES[rva];sp=0x70000+self.r('sp');ip,cs=struct.unpack('<HH',bytes(uc.mem_read(sp,4)))
                need(cs==self.cs and cs*16+ip-self.base in self.instructions,'real far file call returns to owned root')
                payload=None
                if kind in ('open','append'):
                    off,seg=struct.unpack('<HH',bytes(uc.mem_read(sp+4,4)))
                    need((off,seg)==(0x166,self.ds),'actual large-model filename pointer')
                    payload=bytes(uc.mem_read(seg*16+off,9)).hex()
                elif kind in ('read','write'):
                    count,off,seg=struct.unpack('<HHH',bytes(uc.mem_read(sp+4,6)))
                    payload=(seg,off,count)
                    if kind=='write':payload+= (bytes(uc.mem_read(seg*16+off,count)).hex(),)
                elif kind=='seek':
                    origin,offset=struct.unpack('<HI',bytes(uc.mem_read(sp+4,6)));payload=(offset,origin)
                self.event(('file',kind,payload));self.calls+=1
                if kind=='read':uc.mem_write(payload[0]*16+payload[1],self.cfg[:self.read_bytes])
                if kind=='write':self.file[:payload[2]]=bytes.fromhex(payload[3])
                regs={n:self.r(n) for n in self.regs};values,flags=reply(regs,self.calls,self.seed,uc.reg_read(UC_X86_REG_EFLAGS),self.status)
                for n in ('ax','bx','cx','dx','es'):uc.reg_write(REG[n],values[n])
                uc.reg_write(UC_X86_REG_EFLAGS,flags);uc.reg_write(REG['sp'],self.r('sp')+4+args);uc.reg_write(REG['cs'],cs);uc.reg_write(REG['ip'],ip)
                return
            if rva==COPY_START:
                sp=0x70000+self.r('sp');ip,cs,so,ss,do,ds=struct.unpack('<6H',bytes(uc.mem_read(sp,12)))
                need(cs==self.cs and self.r('cx')==8,'real F_SCOPY caller/CX contract')
                self.event(('copy',ss,so,ds,do,self.r('cx')))
            need(self.instructions.get(rva)==size,'execution outside whole cfg and real helper instructions')
            self.covered.update(set(range(rva,rva+size))&self.owned)
        except Exception as error:self.fail(error)
    def write(self,uc,access,address,size,value,_):
        try:
            if 0x70000+self.stack-80<=address and address+size<=0x70000+self.stack:
                self.maximum_stack=max(self.maximum_stack,0x70000+self.stack-address);return
            self.event(('store',address,size,value))
        except Exception as error:self.fail(error)
    def interrupt(self,uc,number,_):
        try:
            need(number==0x60 and self.r('ax')>>8==9,'PMD driver type/version command')
            self.event(('PMD',self.r('ax')));self.calls+=1
            values,flags=reply({n:self.r(n) for n in self.regs},self.calls,self.seed,uc.reg_read(UC_X86_REG_EFLAGS),self.status)
            for n in ('bx','cx','dx','es'):uc.reg_write(REG[n],values[n])
            uc.reg_write(REG['ax'],values['ax']&0xFF00|self.driver);uc.reg_write(UC_X86_REG_EFLAGS,flags)
        except Exception as error:self.fail(error)
    def run(self,kind,*,cfg=b'\x02\x01\x03\x48\x57\x00\x50\xA7',read_bytes=8,resoff=0x31,resseg=0x6000,
            resident=(0x81,0x52,0xA3),driver=0,midi=0,fm=0xA5,trash=0xD3,status=0xFFFF,seed=0x1357,flags=0x202,stack=0xF800):
        need(kind in ENTRIES and len(cfg)==8 and 0<=read_bytes<=8 and 0<=trash<=255,'bounded packed cfg input')
        need(0<=resoff<=0xFFE9 and 0<=resseg<=0xFFFE and all(0<=v<=255 for v in (*resident,driver,midi,fm)),'bounded BYTE fields and resident storage')
        self.uc.mem_write(0,bytes(self.initial));self.stack,self.cfg,self.read_bytes,self.driver,self.seed,self.status=stack,cfg,read_bytes,driver,seed,status
        self.uc.mem_write(0x70000+stack-80,bytes((trash,))*80);self.uc.mem_write(0x70000+stack,b'\xFF\xFF\x5A\xA5')
        self.uc.mem_write(self.data+RESIDENT,struct.pack('<HH',resoff,resseg));self.uc.mem_write(self.data+MIDI,bytes((midi,)));self.uc.mem_write(self.data+FM,bytes((fm,)))
        self.uc.mem_write(self.data+ACTIVE,b'\xA5');self.uc.mem_write(self.data+DISABLED,b'\xA5')
        for offset,value in zip((0x15,0x16,0xB),resident):self.uc.mem_write(resseg*16+resoff+offset,bytes((value,)))
        registers={n:(seed+i*0x231)&65535 for i,n in enumerate(('ax','bx','cx','dx','si','di','bp','es'))}
        registers.update(cs=self.cs,ds=self.ds,ss=0x7000);self.regs=registers
        initial=bytes(self.uc.mem_read(0,1<<20));self.expected=Prediction(initial,registers,self.data,stack,kind,cfg,read_bytes,resoff,resseg,driver,midi,seed,flags,status)
        self.expected.run()
        for n,v in registers.items():self.uc.reg_write(REG[n],v)
        self.uc.reg_write(REG['sp'],stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        self.index,self.calls,self.error,self.returned=0,0,None,False;self.file=bytearray(cfg)
        try:self.uc.emu_start(self.base+ENTRIES[kind][0],0x100000,count=2000)
        except UcError as error:raise ValueError('OP cfg contract: guest fault') from error
        need(self.error is None,self.error or 'guest error')
        need(self.returned and self.r('sp')==stack+2,'near cdecl return, no far frame or callee argument cleanup')
        actual={n:self.r(n) for n in registers};expected=self.expected.regs
        need(actual==expected,'independent full cfg register result: '+str([(n,hex(actual[n]),hex(v)) for n,v in expected.items() if actual[n]!=v]))
        actual_flags=self.uc.reg_read(UC_X86_REG_EFLAGS)
        need(actual_flags&self.expected.flags_mask==self.expected.flags_value&self.expected.flags_mask,'independent return flags')
        need(actual_flags&0x600==self.expected.env_flags&0x600,'IF/DF, including real exit-save CLD')
        need(self.index==len(self.expected.events) and self.file==self.expected.file,'complete file/resident transaction')
        actual_memory=bytes(self.uc.mem_read(0,1<<20));lo,hi=0x70000+stack-80,0x70000+stack
        self.expected.memory[lo:hi]=actual_memory[lo:hi]
        need(actual_memory==self.expected.memory,'whole physical memory outside bounded stack')
        return dict(registers=actual,file_hex=self.file.hex(),flags_mask=self.expected.flags_mask,result_flags=actual_flags&self.expected.flags_mask,
                    final_df=bool(actual_flags&0x400),events=self.expected.events)


def cases():
    for value in range(256):
        cfg=bytes((value,value^0x55,value^0xAA,0x48,0x57,0,0x50,0xA7))
        for driver,midi in ((0,0),(0xFF,0),(0xFF,1),(0xFF,0x80)):
            yield 'cfg_load',dict(cfg=cfg,driver=driver,midi=midi)
    for value in range(256):
        yield 'cfg_load',dict(driver=value,midi=0x80)
        yield 'cfg_load',dict(driver=0xFF,midi=value)
        yield 'cfg_save',dict(trash=value,resident=(value,value^0x55,value^0xAA))
        yield 'cfg_save_exit',dict(trash=value,resident=(value,value^0x55,value^0xAA))
    for count in range(9):
        for trash in (0,0x5A,0xA5):
            for status in (0,0x7FFF,0x8000,0xFFFF):yield 'cfg_load',dict(read_bytes=count,trash=trash,status=status)
    for kind in ENTRIES:
        for segment in (0,0x4000,0x8000,0xA5A5):
            for status in (0,0x7FFF,0x8000,0xFFFF):yield kind,dict(resseg=segment,status=status)


def verify(target,candidate):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(mz,load)
            try:
                trace=hashlib.sha256()
                for count,(kind,options) in enumerate(cases(),1):
                    row=m.run(kind,seed=0x1357 if count&1 else 0xECA8,flags=(2,0x202,0x402,0xED7)[count%4],stack=0xF800 if count&1 else 0xE800,**options)
                    trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.owned,'all 271 owned cfg instruction bytes execute at both loads')
                loads.append(dict(load_segment=load,cases=count,covered_owner_bytes=len(m.covered),maximum_observed_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent target/candidate cfg observations')
    return dict(images=2,functions=3,code_bytes=271,executed_owner_bytes=271,cases_per_image=sum(o['cases'] for o in observations[0]),
                observations=observations[0],exhaustive_byte_domains=256,read_prefix_lengths=9,
                scope='three near cfg functions; real PMD-mode/CRT helper instructions; file and PMD services remain bounded interfaces')


def negative_controls(target):
    controls=(
        ('near-return-frame',0x997F,b'\xC3',b'\xCB','cfg_load',{}),
        ('large-model-filename',0x990E,b'\x66',b'\x67','cfg_load',{}),
        ('read-packed-eight-bytes',0x991B,b'\x08',b'\x07','cfg_load',{}),
        ('unaligned-resident-segment',0x9928,b'\xFD',b'\xFC','cfg_load',{}),
        ('resident-offset-is-zero',0x9933,b'\0',b'\x01','cfg_load',{}),
        ('BGM-resident-field',0x993F,b'\x15',b'\x16','cfg_load',{}),
        ('rank-resident-field',0x997D,b'\x0B',b'\x0C','cfg_load',{}),
        ('PMD-query-command',0xBEFB,b'\x09',b'\x0A','cfg_load',{}),
        ('PMD-unsupported-byte',0xBF01,b'\xFF',b'\xFE','cfg_load',dict(driver=0xFF,midi=0)),
        ('MIDI-is-one-byte',0xBF0C,b'\x8A',b'\x8B','cfg_load',dict(driver=0xFF,midi=0x80)),
        ('selection-enabled-first',0x9949,b'\0',b'\x01','cfg_load',{}),
        ('unavailable-BGM-off',0x9959,b'\0',b'\x01','cfg_load',dict(driver=0xFF,midi=0)),
        ('requested-BGM-off',0x996B,b'\0',b'\x01','cfg_load',dict(cfg=b'\0\x01\x03\x48\x57\0\x50\xA7')),
        ('ordinary-save-writes-four',0x99B6,b'\x04',b'\x05','cfg_save',{}),
        ('ordinary-save-rank-slot',0x99AF,b'\xFA',b'\xFB','cfg_save',{}),
        ('seek-offset-is-DWORD',0x998D,b'\x66',b'\x90','cfg_save',{}),
        ('write-buffer-uses-SS',0x99B0,b'\x16',b'\x1E','cfg_save',{}),
        ('exit-zeroes-eight',0x99D1,b'\x08',b'\x07','cfg_save_exit',{}),
        ('real-zero-template',0x99CE,b'\x91',b'\x92','cfg_save_exit',{}),
        ('CRT-copy-clears-DF',0x338A,b'\xFC',b'\x90','cfg_save_exit',dict(flags=0xED7)),
        ('exit-save-near-return',0x9A16,b'\xC3',b'\xCB','cfg_save_exit',{}),
    )
    rejected=[]
    for name,at,old,new,kind,options in controls:
        raw=bytearray(target.program_image);need(raw[at:at+len(old)]==old,'literal mutation anchor '+name)
        raw[at:at+len(new)]=new;m=Machine(replace(target,program_image=bytes(raw)),0x3000)
        try:
            try:m.run(kind,**options)
            except ValueError:rejected.append(name)
            else:raise ValueError('OP cfg mutation survived: '+name)
        finally:m.close()
    return dict(count=len(rejected),rejected=rejected)
