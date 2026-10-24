"""Independent guest contracts for shared keyboard/joystick mode policy.

The actual nine owned functions execute. Keyboard sampling, joystick sampling
and frame timing are explicit far-call interfaces; physical devices and the
unbounded lifetime of an interactive wait remain outside this contract.
"""
import hashlib
import json
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
from unicorn.x86_const import *
from lib.shared_input_layout import PROFILES, FUNCTIONS

REG={n:globals()['UC_X86_REG_'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp','sp','cs','ds','es','ss','ip')}
KINDS=tuple(name for _,name,_,_ in FUNCTIONS)


def need(value,message):
    if not value:raise ValueError('shared input contract: '+str(message))


def parity(value):return 4 if (value&255).bit_count()%2==0 else 0

def logical(value,byte=False):
    return parity(value)|(64 if not value else 0)|(128 if value&(0x80 if byte else 0x8000) else 0)

def cmp16(a,b):
    v=(a-b)&65535
    return int(a<b)|logical(v)|(16 if (a^b^v)&16 else 0)|(0x800 if (a^b)&(a^v)&0x8000 else 0)


def service_reply(registers,index,seed,flags):
    result=dict(registers)
    for j,name in enumerate(('ax','cx','dx','es')):result[name]=(seed^(0x1234+index*0x101+j*0x231))&65535
    return result,(flags&0x600)|((seed+index*0x149)&0x8D5)|2


class Prediction:
    def __init__(self,initial,registers,profile,data,seed,flags,samples,present,frames):
        self.memory=bytearray(initial);self.regs=dict(registers);self.p=PROFILES[profile]
        self.data,self.seed,self.flags=data,seed,flags;self.samples=samples;self.present=present
        self.events=[];self.poll=0;self.service_count=0;self.frames=frames
        self.flags_mask,self.flags_value=0,0
    def word(self,field):
        at=self.data+self.p[field];return int.from_bytes(self.memory[at:at+2],'little')
    def put(self,field,value,owned=True):
        value&=65535;at=self.data+self.p[field];self.memory[at:at+2]=value.to_bytes(2,'little')
        if owned:self.events.append(('write',at,2,value))
    def service(self,kind):
        self.service_count+=1
        post=None
        if kind=='sense':
            need(self.poll<len(self.samples),'bounded keyboard sample stream')
            sample=self.samples[self.poll];self.poll+=1
            for field,value in zip(('single','player1','player2','joystick'),(*sample[:3],0)):self.put(field,value,False)
            post=dict(single=sample[0],player1=sample[1],player2=sample[2],joystick=0)
        elif kind=='js':
            value=self.samples[self.poll-1][3];self.put('joystick',value,False);post=dict(joystick=value)
        self.events.append(('service',kind,post,1 if kind=='delay' else None))
        self.regs,self.flags_value=service_reply(self.regs,self.service_count,self.seed,self.flags)
        self.flags_mask=0x8D5
    def mode(self,kind):
        self.service('sense');sp,p1,p2=self.word('single'),self.word('player1'),self.word('player2')
        if kind=='input_mode_key_vs_key':return
        if kind=='input_mode_cpu_vs_cpu':
            high=sp>>8;tested=high&0x10 if high&0x10 else high&0x20
            self.flags_mask,self.flags_value=0x8C5,logical(tested,True)
            if sp&0x3000:self.put('single',0x1000)
            self.put('player1',0);self.put('player2',0);return
        if kind=='input_mode_1p_vs_cpu':self.regs['ax']=sp;self.put('player1',p1|sp)
        elif kind=='input_mode_cpu_vs_1p':self.regs['ax']=sp|p1;self.put('player2',sp|p1)
        if self.present:self.service('js')
        else:self.flags_mask,self.flags_value=0x8D5,cmp16(0,0)
        joy=self.word('joystick')
        if kind in ('input_mode_interface','input_mode_attract'):
            if self.present:
                self.regs['ax']=joy;self.put('single',sp|joy)
            self.regs['ax']=p1;self.put('single',self.word('single')|p1)
            self.flags_mask,self.flags_value=0x8C5,logical(self.word('single'))
            if kind=='input_mode_attract':self.put('player1',0);self.put('player2',0)
        elif kind=='input_mode_joy_vs_key' and self.present:
            self.regs['ax']=joy;self.put('player1',joy);self.regs['ax']=sp;self.put('player2',sp)
        elif kind=='input_mode_key_vs_joy' and self.present:
            self.regs['ax']=joy;self.put('player2',joy);self.regs['ax']=sp;self.put('player1',sp)
        elif kind in ('input_mode_1p_vs_cpu','input_mode_cpu_vs_1p'):
            field='player1' if kind=='input_mode_1p_vs_cpu' else 'player2'
            if self.present:
                self.regs['ax']=joy;self.put(field,self.word(field)|joy)
                self.flags_mask,self.flags_value=0x8C5,logical(self.word(field))
            self.put('player2' if field=='player1' else 'player1',0)
    def run(self,kind):
        if kind!='input_wait_for_change':self.mode(kind);return
        while True:
            self.mode('input_mode_interface')
            if not self.word('single'):break
            self.service('delay')
        limit=self.frames if self.frames else 9999
        signed=limit if limit<0x8000 else limit-65536
        waited=0
        while waited<signed:
            self.mode('input_mode_interface');value=self.word('single')
            if value:
                self.flags_mask,self.flags_value=0x8D5,cmp16(value,0);return
            waited+=1;self.service('delay')
            if limit==9999:waited=0
        self.flags_mask,self.flags_value=0x8D5,cmp16(waited&65535,limit)


class Machine:
    def __init__(self,mz,load,profile):
        need(mz.valid,'valid MZ')
        self.p=PROFILES[profile];self.profile=profile;self.base=load*16
        self.code_segment=load+self.p['code_segment'];self.data_segment=load+self.p['data_segment'];self.data=self.data_segment*16
        self.uc=Uc(UC_ARCH_X86,UC_MODE_16);self.uc.mem_map(0,1<<20)
        self.initial=bytearray(b'\xA5'*(1<<20));body=mz.relocated_program_image(load);self.initial[self.base:self.base+len(body)]=body
        start=self.p['code_segment']*16+self.p['start'];self.start=start
        self.entries={name:(start+off,size) for _,name,off,size in FUNCTIONS}
        self.instructions={}
        for entry,size in self.entries.values():
            decoded=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[entry:entry+size],entry))
            need(sum(i.size for i in decoded)==size and decoded[-1].mnemonic.startswith('retf'),'whole far Pascal procedures')
            self.instructions.update({i.address:i.size for i in decoded})
        self.services={self.p['code_segment']*16+self.p['sense']:'sense',self.p['code_segment']*16+self.p['delay']:'delay',self.p['js']:'js'}
        self.covered=set();self.maximum_stack=0
        self.hooks=[self.uc.hook_add(UC_HOOK_CODE,self.code),self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write),self.uc.hook_add(UC_HOOK_INTR,lambda uc,n,_:self.fail('unexpected interrupt '+str(n)))]
    def close(self):
        for hook in self.hooks:self.uc.hook_del(hook)
        self.hooks=[];self.uc=None
    def r(self,name):return self.uc.reg_read(REG[name])&65535
    def fail(self,message):self.error=str(message);self.uc.emu_stop()
    def event(self,actual):
        need(self.event_index<len(self.expected.events) and actual==self.expected.events[self.event_index],f'ordered mode event #{self.event_index}: {actual}')
        self.event_index+=1
    def code(self,uc,address,size,_):
        try:
            if address==0x60000:self.returned=True;uc.emu_stop();return
            rva=address-self.base
            if rva in self.services:
                kind=self.services[rva];need(self.event_index<len(self.expected.events),'bounded service schedule')
                row=self.expected.events[self.event_index]
                need(row[0:2]==('service',kind),'ordered service target')
                stack=0x70000+self.r('sp');ip,cs=struct.unpack('<HH',bytes(uc.mem_read(stack,4)))
                caller=cs*16+ip-self.base
                need(cs==self.code_segment and caller in self.instructions,'actual far-call return into owned code')
                if kind=='delay':need(int.from_bytes(uc.mem_read(stack+4,2),'little')==1,'far Pascal delay argument WORD one')
                self.event(row);self.service_count+=1
                if row[2]:
                    for field,value in row[2].items():uc.mem_write(self.data+self.p[field],value.to_bytes(2,'little'))
                regs={n:self.r(n) for n in REG if n not in ('sp','ip')}
                reply,flags=service_reply(regs,self.service_count,self.seed,self.flags)
                for n in ('ax','cx','dx','es'):uc.reg_write(REG[n],reply[n])
                uc.reg_write(UC_X86_REG_EFLAGS,flags)
                uc.reg_write(REG['sp'],self.r('sp')+(6 if kind=='delay' else 4));uc.reg_write(REG['cs'],cs);uc.reg_write(REG['ip'],ip)
                return
            need(self.instructions.get(rva)==size,'execution outside owned input/service boundaries')
            self.covered.update(range(rva,rva+size))
        except Exception as error:self.fail(error)
    def write(self,uc,access,address,size,value,_):
        try:
            if 0x70000+self.stack-40<=address and address+size<=0x70000+self.stack:
                self.maximum_stack=max(self.maximum_stack,0x70000+self.stack-address);return
            self.event(('write',address,size,value))
        except Exception as error:self.fail(error)
    def run(self,kind,*,sample=(0x102,0x200,0x400,0x8000),samples=None,present=1,frames=2,seed=0x1357,flags=0x202,stack=0xF800):
        need(kind in self.entries and 0<=present<=65535 and 0<=frames<=65535,'bounded WORD interface inputs')
        samples=[sample] if samples is None else samples
        need(all(len(s)==4 and all(0<=v<=65535 for v in s) for s in samples),'bounded WORD sample states')
        self.uc.mem_write(0,bytes(self.initial));self.stack,self.seed,self.flags=stack,seed,flags
        self.uc.mem_write(self.data+self.p['presence'],present.to_bytes(2,'little'))
        self.uc.mem_write(0x70000+stack,struct.pack('<HHH',0,0x6000,frames))
        registers={n:(seed+i*0x231)&65535 for i,n in enumerate(('ax','bx','cx','dx','si','di','bp','es'))}
        registers.update(cs=self.code_segment,ds=self.data_segment,ss=0x7000)
        initial=bytes(self.uc.mem_read(0,1<<20));self.expected=Prediction(initial,registers,self.profile,self.data,seed,flags,samples,present,frames)
        self.expected.run(kind)
        for n,v in registers.items():self.uc.reg_write(REG[n],v)
        self.uc.reg_write(REG['sp'],stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        self.event_index,self.service_count,self.error,self.returned=0,0,None,False
        try:self.uc.emu_start(self.base+self.entries[kind][0],0x100000,count=1000000)
        except UcError as error:raise ValueError('shared input contract: guest fault') from error
        need(self.error is None,self.error or 'guest error')
        need(self.returned and self.r('sp')==stack+(6 if kind=='input_wait_for_change' else 4),'far Pascal caller cleanup')
        expected=dict(self.expected.regs);expected.update(cs=0x6000)
        actual={n:self.r(n) for n in expected}
        need(actual==expected,'independent result and full register contract: '+str([(n,hex(actual[n]),hex(v)) for n,v in expected.items() if actual[n]!=v]))
        final_flags=self.uc.reg_read(UC_X86_REG_EFLAGS)
        need(final_flags&self.expected.flags_mask==self.expected.flags_value&self.expected.flags_mask,'independent defined return flags')
        need(final_flags&0x600==flags&0x600,'inherited IF/DF')
        need(self.event_index==len(self.expected.events),'complete sample/write/frame schedule')
        actual_memory=bytes(self.uc.mem_read(0,1<<20));lo,hi=0x70000+stack-40,0x70000+stack
        self.expected.memory[lo:hi]=actual_memory[lo:hi]
        need(actual_memory==self.expected.memory,'whole physical memory outside bounded stack')
        trace=hashlib.sha256(json.dumps(self.expected.events,separators=(',',':')).encode()).hexdigest()
        return dict(registers=actual,result_flags=final_flags&self.expected.flags_mask,flags_mask=self.expected.flags_mask,
                    sample_polls=self.expected.poll,service_calls=self.service_count,ordered_events_sha256=trace,
                    states={field:self.expected.word(field) for field in ('single','player1','player2','joystick')})


def cases():
    values=[0,1,0xFFFF,0x7FFF,0x8000,0x5555,0xAAAA,0x1000,0x2000,0x3000]+[1<<i for i in range(16)]
    for kind in KINDS[:-1]:
        for present in (0,1,0x8000,0xFFFF):
            for value in values:
                yield kind,dict(present=present,sample=(value,(value*257+0x31)&65535,(~value)&65535,value^0xA55A))
    for high in range(256):yield 'input_mode_cpu_vs_cpu',dict(sample=(high*256+0xA5,0x1234,0xABCD,0))
    zero=(0,0,0xBEEF,0);held=(1,0,0x55,0);pressed=(0x2000,0x40,0x80,0x100)
    for frames in (0,1,2,9998,9999,0x7FFF,0x8000,0xFFFF):
        for present in (0,1):
            yield 'input_wait_for_change',dict(frames=frames,present=present,samples=[held]*3+[zero]+[zero]*2+[pressed])
    for frames in (1,2,7):yield 'input_wait_for_change',dict(frames=frames,samples=[zero]*(frames+1))
    for frames in (0,9999):yield 'input_wait_for_change',dict(frames=frames,samples=[zero]*10002+[pressed])


def verify(target,candidate,profile):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(mz,load,profile)
            try:
                trace=hashlib.sha256();maximum_polls=0
                for count,(kind,options) in enumerate(cases(),1):
                    row=m.run(kind,seed=0x1357 if count&1 else 0xECA8,flags=(2,0x202,0x402,0xED7)[count%4],stack=0xF800 if count&1 else 0xE800,**options)
                    maximum_polls=max(maximum_polls,row['sample_polls']);trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==set(range(m.start,m.start+367)),'all 367 owned instruction bytes execute at both loads')
                loads.append(dict(load_segment=load,cases=count,covered_owner_bytes=len(m.covered),maximum_observed_stack_depth=m.maximum_stack,maximum_sample_polls=maximum_polls,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent target/candidate input observations')
    return dict(profile=profile,images=2,functions=9,code_bytes=367,cases_per_image=sum(o['cases'] for o in observations[0]),
                executed_owner_bytes=367,observations=observations[0],exhaustive_high_input_bytes=256,
                scope='input mode policy and bounded waits; keyboard/joystick/frame services remain interfaces')


def negative_controls(target,profile):
    from dataclasses import replace
    p=PROFILES[profile];start=p['code_segment']*16+p['start']
    zero=(0,0,0,0);held=(1,0,0,0)
    long=[zero]*10002+[(0x2000,0,0,0)]
    controls=(
        ('interface-merges-player1',30,b'\x09',b'\x89','input_mode_interface',{}),
        ('input-word-width',30,b'\x09',b'\x08','input_mode_interface',{}),
        ('absent-joystick-branch',13,b'\x74',b'\x75','input_mode_interface',dict(present=0)),
        ('key-mode-samples-input',39,b'\x90\x0E',b'\x90'*5,'input_mode_key_vs_key',{}),
        ('joystick-player1-store',69,b'\xA3',b'\xA1','input_mode_joy_vs_key',{}),
        ('joystick-player2-store',103,b'\xA3',b'\xA1','input_mode_key_vs_joy',{}),
        ('cpu-player2-cleared',152,b'\0',b'\x01','input_mode_1p_vs_cpu',{}),
        ('cpu-player1-cleared',197,b'\0',b'\x01','input_mode_cpu_vs_1p',{}),
        ('cancel-input-mask',213,b'\x10',b'\x08','input_mode_cpu_vs_cpu',dict(sample=(0x800,0,0,0))),
        ('cancel-normalization',228,b'\x10',b'\x20','input_mode_cpu_vs_cpu',dict(sample=(0x1000,0,0,0))),
        ('attract-player1-clear',281,b'\0',b'\x01','input_mode_attract',{}),
        ('signed-wait-limit',359,b'\x7C',b'\x72','input_wait_for_change',dict(frames=0x8000,samples=[zero])),
        ('explicit-9999-sentinel',351,b'\x0F',b'\x0E','input_wait_for_change',dict(frames=9999,samples=long)),
        ('zero-wait-sentinel',326,b'\x0F',b'\x0E','input_wait_for_change',dict(frames=0,samples=long)),
        ('release-before-timeout',310,b'\x74',b'\x75','input_wait_for_change',dict(frames=0xFFFF,samples=[held]*3+[zero])),
        ('wait-counter-increments',341,b'\x47',b'\x4F','input_wait_for_change',dict(frames=1,samples=[zero]*2)),
        ('Pascal-argument-cleanup',365,b'\x02',b'\0','input_wait_for_change',dict(frames=0xFFFF,samples=[zero])),
        ('frame-delay-word-one',313,b'\x01',b'\x02','input_wait_for_change',dict(frames=0xFFFF,samples=[held]*3+[zero])),
        ('joystick-service-target',16,bytes((p['js']&255,)),bytes(((p['js']&255)^1,)),'input_mode_interface',{}),
    )
    rejected=[]
    for name,offset,old,new,kind,options in controls:
        raw=bytearray(target.program_image);at=start+offset
        need(raw[at:at+len(old)]==old,'literal mutation anchor '+name)
        raw[at:at+len(new)]=new;m=Machine(replace(target,program_image=bytes(raw)),0x3000,profile)
        try:
            try:m.run(kind,**options)
            except ValueError:rejected.append(name)
            else:raise ValueError('shared input mutation survived: '+name)
        finally:m.close()
    return dict(count=len(rejected),rejected=rejected)
