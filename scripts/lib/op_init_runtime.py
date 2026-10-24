"""Complete OP initialization with actual plane setup and independent ABI/state.

Library replies are bounded, including failed allocation and ignored later errors.
The library's raster/device effects and resource-package contents remain external.
"""
import hashlib,json,struct
from dataclasses import replace
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import UcError
from unicorn.x86_const import UC_X86_REG_EFLAGS
from lib.op_dispatch_runtime import Machine as BaseMachine,REG,GPRS
from lib.op_cfg_runtime import reply
START=0xC421;SIZE=105;PLANES=0xBED1;PLANE_BYTES=41
SERVICES={0x245A:('assign',2),0x19F6:('graph_start',0),0x114C:('graph_clear',0),0x22CA:('vsync_start',0),
 0x1A22:('key_beep_off',0),0x2232:('systemline_hide',0),0x2226:('cursor_hide',0),0x708:('egc_start',0),
 0x2DB8:('js_start',0),0x2B60:('pfstart',4)}
POINTERS=(0xA8000000,0xB0000000,0xB8000000,0xE0000000)
def need(v,m):
    if not v:raise ValueError('OP init contract: '+str(m))
def logic(value):return (4 if (value&255).bit_count()%2==0 else 0)|(0x80 if value&0x8000 else 0)|(0x40 if not value else 0)
class Machine(BaseMachine):
    def __init__(self,mz,load):
        super().__init__(mz,load);self.cs=load+0xBEB;self.instructions={};self.owned=set(range(START,START+SIZE));self.nested=set(range(PLANES,PLANES+PLANE_BYTES))
        for start,size in ((START,SIZE),(PLANES,PLANE_BYTES)):
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+size],start));need(sum(i.size for i in rows)==size,'complete init/plane instructions');self.instructions.update({i.address:i.size for i in rows})
    def registers(self):return {n:self.r(n) for n in (*GPRS,'cs','ds','es','ss')}
    def code(self,uc,address,size,_):
        try:
            if address==0x80040:self.returned=True;uc.emu_stop();return
            rva=address-self.base;self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
            if rva==PLANES:self.plane_calls+=1
            if rva in SERVICES:
                name,args=SERVICES[rva];sp=self.r('sp');at=0x70000+sp;ip,cs=struct.unpack('<HH',bytes(uc.mem_read(at,4)))
                need(cs*16+ip-self.base in self.instructions,'real far service frame returns into init')
                payload=struct.unpack('<H',bytes(uc.mem_read(at+4,2)))[0] if name=='assign' else tuple(struct.unpack('<HH',bytes(uc.mem_read(at+4,4)))) if name=='pfstart' else None
                self.event(('service',name,payload));self.calls+=1
                regs,flags=reply(self.registers(),self.calls,self.seed,uc.reg_read(UC_X86_REG_EFLAGS),self.assign if name=='assign' else self.status)
                for n in ('ax','bx','cx','dx','es'):uc.reg_write(REG[n],regs[n])
                uc.reg_write(UC_X86_REG_EFLAGS,flags);uc.reg_write(REG['sp'],sp+4+args);uc.reg_write(REG['cs'],cs);uc.reg_write(REG['ip'],ip);return
            need(self.instructions.get(rva)==size,'execution outside complete init/plane instructions')
            self.covered.update(set(range(rva,rva+size))&self.owned);self.nested_covered.update(set(range(rva,rva+size))&self.nested)
        except Exception as e:self.fail(e)
    def run(self,*,assign=0,status=0xFFFF,filename=(0xFFFF,0x5000),seed=0x1357,flags=0x202,stack=0xF800):
        need(all(0<=v<=65535 for v in (assign,status,*filename,seed)) and len(filename)==2 and 80<=stack<=0xFFF0,'bounded WORD state and far pointer')
        self.uc.mem_write(0,bytes(self.initial));self.stack,self.seed,self.status,self.assign=stack,seed,status,assign
        self.uc.mem_write(0x70000+stack-80,b'\xD3'*80);self.uc.mem_write(0x70000+stack,struct.pack('<4H',0x40,0x8000,*filename))
        self.memory=bytearray(self.uc.mem_read(0,1<<20));self.events=[('service','assign',22000)]
        if not assign:
            for i,pointer in enumerate(POINTERS):
                at=self.data+0x19FA+i*4;self.events.append(('store',at,4,pointer));self.memory[at:at+4]=pointer.to_bytes(4,'little')
            self.events += [('service','graph_start',None),('out',0xA6,1),('service','graph_clear',None),('out',0xA6,0),('service','graph_clear',None),
                ('out',0xA6,0),('out',0xA4,0),('service','vsync_start',None),('service','key_beep_off',None),('service','systemline_hide',None),
                ('service','cursor_hide',None),('service','egc_start',None),('service','js_start',None),('service','pfstart',filename)]
        initial={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)};high={n:(seed^0x5AA5)<<16 for n in GPRS}
        for n in GPRS:self.uc.reg_write(GPRS[n],high[n]|initial[n])
        initial.update(cs=self.cs,ds=self.ds,es=seed,ss=0x7000)
        for n in ('cs','ds','es','ss'):self.uc.reg_write(REG[n],initial[n])
        self.uc.reg_write(REG['sp'],stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        self.error,self.returned,self.index,self.calls,self.plane_calls=None,False,0,0,0
        try:self.uc.emu_start(self.base+START,0x100000,count=500)
        except UcError as e:raise ValueError('OP init contract: guest fault') from e
        need(self.error is None,self.error or 'guest error');need(self.returned and self.r('sp')==stack+4,'far cdecl return leaves filename for caller')
        count=1 if assign else 11;need(self.calls==count and self.plane_calls==int(not assign) and self.index==len(self.events),'complete init call/store/port protocol')
        expected,_=reply(initial,count,seed,flags,assign if assign else status);expected.update(ax=int(bool(assign)),cs=0x8000)
        need(self.registers()==expected,'independent returning WORD/segment registers')
        for n in GPRS:need(self.uc.reg_read(GPRS[n])==high[n]|expected[n],'independent DWORD high halves: '+n)
        f=self.uc.reg_read(UC_X86_REG_EFLAGS);need(f&0x8C5==logic(assign) and f&0x600==flags&0x600,'defined logic flags and inherited IF/DF; AF undefined')
        memory=bytes(self.uc.mem_read(0,1<<20));lo,hi=0x70000+stack-80,0x70000+stack;self.memory[lo:hi]=memory[lo:hi]
        need(memory==self.memory,'complete memory outside 80-byte stack; caller filename preserved')
        return dict(registers=self.registers(),full_registers={n:self.uc.reg_read(GPRS[n]) for n in GPRS},flags=f&0xEC5,events=self.events,actual_plane_calls=self.plane_calls,library_calls=self.calls)
def cases():
    for assign in sorted(set(range(256))|{v<<8 for v in range(256)}|{0x7FFF,0xFFFF}):yield dict(assign=assign)
    for segment in (0,1,0x5000,0x6000,0x7000,0xFFFF):
        for offset in (0,1,0x7FFF,0x8000,0xFFFE,0xFFFF):
            for status in (0,1,0x7FFF,0x8000,0xFFFF):yield dict(filename=(offset,segment),status=status)
    for assign in (0,0x8000):
        for seed in (0,1,0x1357,0xECA8,0xA55A,0xFFFF):
            for flags in (2,0x202,0x402,0xED7):
                for stack in (0x80,0xFFF0):yield dict(assign=assign,seed=seed,flags=flags,stack=stack)
def verify(target,candidate):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(mz,load)
            try:
                trace=hashlib.sha256();success=failure=0
                for count,p in enumerate(cases(),1):
                    options=dict(seed=0x1357 if count&1 else 0xECA8,flags=(2,0x202,0x402,0xED7)[count%4],stack=0x80 if count&1 else 0xFFF0);options.update(p)
                    row=m.run(**options);success+=int(not p.get('assign',0));failure+=int(bool(p.get('assign',0)));trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.owned and m.nested_covered==m.nested,'all 105 owner and 41 plane helper bytes execute')
                loads.append(dict(load_segment=load,cases=count,allocation_success_cases=success,allocation_failure_cases=failure,covered_owner_bytes=len(m.covered),executed_nested_bytes=len(m.nested_covered),maximum_observed_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent init target/candidate observations')
    return dict(images=2,functions=1,code_bytes=105,executed_owner_bytes=105,cases_per_image=sum(o['cases'] for o in observations[0]),observations=observations[0],scope='actual initializer and accepted plane setter; bounded allocation/device/package replies, no physical display/resource payload claim')
def negative_controls(target):
    controls=(('allocation-22000-paragraphs',4,b'\xF0',b'\xF1',{}),('allocation-any-nonzero-fails',13,b'\x74',b'\x75',dict(assign=0x8000)),
        ('failure-returns-one',16,b'\x01',b'\0',dict(assign=1)),('real-plane-call',23,b'\x97',b'\x98',{}),
        ('first-clear-page-one',34,b'\x01',b'\0',{}),('BYTE-output',35,b'\xEE',b'\xEF',{}),
        ('final-clear-page-zero',56,b'\0',b'\x01',{}),('display-page-A4',59,b'\xA4',b'\xA6',{}),
        ('filename-is-DWORD',92,b'\x66',b'\x90',{}),('original-far-filename-slot',95,b'\x06',b'\x08',{}),
        ('success-ignores-service-status',101,b'\x33',b'\x0B',{}),('far-cdecl-return',104,b'\xCB',b'\xC3',{}))
    rejected=[]
    for name,at,old,new,p in controls:
        at+=START;raw=bytearray(target.program_image);need(raw[at:at+len(old)]==old,'literal init mutation anchor '+name);raw[at:at+len(new)]=new;m=None
        try:
            try:m=Machine(replace(target,program_image=bytes(raw)),0x3000);m.run(**p)
            except ValueError:rejected.append(name)
            else:raise ValueError('OP init mutation survived: '+name)
        finally:
            if m:m.close()
    # A maintained nested helper cannot silently become a service stub.
    at=PLANES+8;raw=bytearray(target.program_image);need(raw[at:at+1]==b'\0','literal plane DWORD anchor');raw[at]=1;m=None
    try:
        try:m=Machine(replace(target,program_image=bytes(raw)),0x3000);m.run()
        except ValueError:rejected.append('actual-plane-DWORD-store')
        else:raise ValueError('OP init mutation survived: actual-plane-DWORD-store')
    finally:
        if m:m.close()
    return dict(count=len(rejected),rejected=rejected)
