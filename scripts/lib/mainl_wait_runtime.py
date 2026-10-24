"""Ending waits execute real nested input policy, with bounded sound/IRQ replies.

The music query's AX is overwritten by input_mode_interface(): the loop really
compares unsigned player-1 input against measure. Preserve this target behavior.
"""
import hashlib
import json
import struct
from dataclasses import replace

from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import UcError,UC_HOOK_INTR
from unicorn.x86_const import UC_X86_REG_EFLAGS
from lib.shared_input_runtime import Machine as InputMachine, Prediction as InputPrediction, REG, service_reply
from lib.mainl_wait_layout import CODE_SEGMENT,OFFSET,COUNTER,ACTIVE,MIDI,FUNCTIONS

ENTRIES={name:(CODE_SEGMENT*16+OFFSET+off,size,args) for _,name,off,size,args in FUNCTIONS}
FIELDS=dict(counter=COUNTER,active=ACTIVE,midi=MIDI)


def need(value,message):
    if not value:raise ValueError('MAINL wait contract: '+str(message))


class Prediction(InputPrediction):
    def __init__(self,*args,measure=0,replies=(),**kwargs):
        super().__init__(*args,**kwargs);self.p=dict(self.p,**FIELDS);self.measure=measure;self.replies=replies;self.query=0
    def byte(self,field):return self.memory[self.data+self.p[field]]
    def service(self,kind):
        index=self.poll;super().service(kind)
        if kind=='sense':
            tick=self.samples[index][4];self.put('counter',tick,False)
            self.events[-1][2]['counter']=tick
    def interrupt(self):
        midi=self.byte('midi')==1;self.regs['ax']=self.regs['ax']&255|0x500
        if midi:self.regs['dx']=0xC0
        self.events.append(('interrupt',0x61 if midi else 0x60,self.regs['ax'],0xC0 if midi else None))
        need(self.query<len(self.replies),'bounded sound reply stream')
        answer=self.replies[self.query];self.query+=1;self.service_count+=1
        self.regs,self.flags_value=service_reply(self.regs,self.service_count,self.seed,self.flags)
        self.regs['ax']=answer
    def result(self,value):
        self.regs['ax']=int(value);self.flags_mask,self.flags_value=0x8C5,0 if value else 0x44
    def wait_ok(self):
        self.put('counter',0)
        while True:
            self.mode('input_mode_interface')
            if self.word('single')&0x2020:self.result(True);return
            if self.word('counter')>=self.frames:self.result(False);return
    def run(self,kind):
        if kind=='input_wait_for_ok':self.wait_ok();return
        if not self.byte('active'):self.wait_ok();return
        while True:
            self.interrupt();self.mode('input_mode_interface')
            if self.word('single')&0x2020:self.result(True);return
            # _AX is an unsigned register pseudo-variable. The actual owned
            # interface leaves player1 in AX, replacing the music query reply.
            if self.regs['ax']>=self.measure:self.result(False);return


class Machine(InputMachine):
    def __init__(self,mz,load):
        super().__init__(mz,load,'mainl');self.p=dict(self.p,**FIELDS)
        self.wait_bytes=set()
        for start,size,_ in ENTRIES.values():
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+size],start))
            need(sum(r.size for r in rows)==size and rows[-1].mnemonic=='retf','complete far wait boundaries')
            self.instructions.update({r.address:r.size for r in rows});self.wait_bytes.update(range(start,start+size))
        self.uc.hook_del(self.hooks.pop());self.hooks.append(self.uc.hook_add(UC_HOOK_INTR,self.interrupt))
    def interrupt(self,uc,number,_):
        try:
            need(self.event_index<len(self.expected.events),'bounded sound interrupt schedule')
            expected=self.expected.events[self.event_index]
            actual=('interrupt',number,self.r('ax'),self.r('dx') if number==0x61 else None)
            self.event(actual);need(expected==actual and self.r('ax')>>8==5,'sound measure command and MIDI selector')
            self.service_count+=1;regs={n:self.r(n) for n in REG if n not in ('sp','ip')}
            reply,flags=service_reply(regs,self.service_count,self.seed,self.flags)
            for name in ('cx','dx','es'):uc.reg_write(REG[name],reply[name])
            uc.reg_write(REG['ax'],self.replies[self.query]);self.query+=1
            uc.reg_write(UC_X86_REG_EFLAGS,flags)
        except Exception as error:self.fail(error)
    def run(self,kind,*,samples=((0,0,0,0,1),(0,0,0,0,2)),frames=2,measure=2,active=1,midi=0,present=1,
            replies=None,seed=0x1357,flags=0x202,stack=0xF800):
        need(kind in ENTRIES and all(0<=v<=65535 for v in (frames,measure,present)) and all(0<=v<=255 for v in (active,midi)),'WORD arguments and BYTE sound state')
        need(samples and all(len(s)==5 and all(0<=v<=65535 for v in s) for s in samples),'bounded input/tick scripts')
        replies=[0xFFFF]*len(samples) if replies is None else replies
        need(all(0<=v<=65535 for v in replies),'WORD sound query replies')
        self.uc.mem_write(0,bytes(self.initial));self.stack,self.seed,self.flags=stack,seed,flags
        self.uc.mem_write(self.data+self.p['presence'],present.to_bytes(2,'little'))
        self.uc.mem_write(self.data+ACTIVE,bytes((active,)));self.uc.mem_write(self.data+MIDI,bytes((midi,)))
        self.uc.mem_write(0x70000+stack,struct.pack('<HHHH',0,0x6000,frames,measure))
        registers={n:(seed+i*0x231)&65535 for i,n in enumerate(('ax','bx','cx','dx','si','di','bp','es'))}
        registers.update(cs=self.code_segment,ds=self.data_segment,ss=0x7000)
        initial=bytes(self.uc.mem_read(0,1<<20))
        self.expected=Prediction(initial,registers,'mainl',self.data,seed,flags,samples,present,frames,measure=measure,replies=replies)
        self.expected.run(kind)
        for name,value in registers.items():self.uc.reg_write(REG[name],value)
        self.uc.reg_write(REG['sp'],stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        self.replies,self.query=replies,0;self.event_index,self.service_count,self.error,self.returned=0,0,None,False
        try:self.uc.emu_start(self.base+ENTRIES[kind][0],0x100000,count=20000)
        except UcError as error:raise ValueError('MAINL wait contract: guest fault') from error
        need(self.error is None,self.error or 'guest error')
        need(self.returned and self.r('sp')==stack+4+ENTRIES[kind][2],'far Pascal argument cleanup')
        expected=dict(self.expected.regs);expected.update(cs=0x6000);actual={n:self.r(n) for n in expected}
        need(actual==expected,'independent full register result: '+str([(n,hex(actual[n]),hex(v)) for n,v in expected.items() if actual[n]!=v]))
        final_flags=self.uc.reg_read(UC_X86_REG_EFLAGS)
        need(final_flags&self.expected.flags_mask==self.expected.flags_value,'defined BOOL16 return flags')
        need(final_flags&0x600==flags&0x600,'inherited IF/DF')
        need(self.event_index==len(self.expected.events) and self.query==self.expected.query,'complete sound/input/IRQ schedule')
        actual_memory=bytes(self.uc.mem_read(0,1<<20));lo,hi=0x70000+stack-40,0x70000+stack
        self.expected.memory[lo:hi]=actual_memory[lo:hi]
        need(actual_memory==self.expected.memory,'whole physical memory outside bounded stack')
        return dict(registers=actual,result_flags=final_flags&self.expected.flags_mask,polls=self.expected.poll,
                    sound_queries=self.query,ordered_events_sha256=hashlib.sha256(json.dumps(self.expected.events,separators=(',',':')).encode()).hexdigest(),counter=self.expected.word('counter'))


def cases():
    zero=(0,0,0,0,0);shot=(0x20,0,0,0,0);ok=(0x2000,0,0,0,0)
    for active in range(256):
        for midi in (0,1,2,0xFF):yield 'input_wait_for_ok_or_measure',dict(active=active,midi=midi,measure=0,frames=0,samples=[zero])
    for midi in range(256):yield 'input_wait_for_ok_or_measure',dict(midi=midi,measure=0,samples=[zero])
    for kind in ENTRIES:
        for present in (0,1,0x8000,0xFFFF):
            for bit in range(16):
                value=1<<bit
                for field in (0,1,3):
                    first=[0,0,0,0,1];first[field]=value
                    yield kind,dict(present=present,samples=[tuple(first),shot],frames=0xFFFF,measure=0xFFFF)
        for frames in (0,1,2,0x7FFF,0x8000,0xFFFF):
            samples=[(0,0,0,0,0),(0,0,0,0,(frames-1)&65535),(0,0,0,0,frames)]
            yield kind,dict(active=0,frames=frames,samples=samples)
        for value in (0x20,0x2000,0x2020,0xFFFF):yield kind,dict(samples=[(value,0,0,0,0)])
    yield 'input_wait_for_ok_or_measure',dict(measure=0x100,samples=[zero,(0,0x100,0,0,0)],replies=[0xFFFF,0xFFFF])
    yield 'input_wait_for_ok_or_measure',dict(measure=0x100,samples=[(0,0x4000,0,0,0)],replies=[0])
    yield 'input_wait_for_ok_or_measure',dict(measure=0x8000,samples=[(0,0x4000,0,0,0),(0,0x8000,0,0,0)],replies=[0xFFFF,0])
    yield 'input_wait_for_ok',dict(frames=0xFFFF,samples=[(0,0,0,0,0xFFFE),zero,(0,0,0,0,0xFFFF)])
    yield 'input_wait_for_ok',dict(frames=0x8000,samples=[(0,0,0,0,0x4000),(0,0,0,0,0x8000)])


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
                need(m.covered&m.wait_bytes==m.wait_bytes,'every 126 owned wait byte executes at both loads')
                loads.append(dict(load_segment=load,cases=count,covered_owner_bytes=len(m.covered&m.wait_bytes),maximum_observed_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'target/candidate independent wait observations')
    return dict(images=2,functions=2,code_bytes=126,executed_owner_bytes=126,cases_per_image=sum(o['cases'] for o in observations[0]),
                observations=observations[0],exhaustive_sound_flag_bytes=256,
                scope='two ending wait functions and real owned input interface; sound and input/IRQ services remain bounded interfaces')


def negative_controls(target):
    zero=(0,0,0,0,0);shot=(0x20,0,0,0,0)
    controls=(
        ('sound-active-byte-branch',0xC55,b'\x75',b'\x74','input_wait_for_ok_or_measure',dict(active=0,frames=0,samples=[zero])),
        ('MIDI-exactly-one',0xC6A,b'\x74',b'\x75','input_wait_for_ok_or_measure',dict(midi=0,measure=0,samples=[zero])),
        ('sound-query-command',0xC64,b'\x05',b'\x06','input_wait_for_ok_or_measure',dict(measure=0,samples=[zero])),
        ('MIDI-query-port',0xC71,b'\xC0',b'\0','input_wait_for_ok_or_measure',dict(midi=1,measure=0,samples=[zero])),
        ('sound-interrupt-vector',0xC6D,b'\x60',b'\x61','input_wait_for_ok_or_measure',dict(measure=0,samples=[zero])),
        ('shot-input-bit',0xC7E,b'\x20',b'\x10','input_wait_for_ok_or_measure',dict(measure=0,samples=[(0x10,0,0,0,0)])),
        ('OK-input-bit',0xC85,b'\x20',b'\x10','input_wait_for_ok_or_measure',dict(measure=0,samples=[(0x1000,0,0,0,0)])),
        ('unsigned-input-AX-compare',0xC92,b'\x72',b'\x7C','input_wait_for_ok_or_measure',dict(measure=0x8000,samples=[(0,0x4000,0,0,0),(0,0x8000,0,0,0)])),
        ('real-interface-overwrites-query-AX',0xC75,b'\x90\x0E',b'\x90'*5,'input_wait_for_ok_or_measure',dict(measure=0x100,samples=[zero,(0,0x100,0,0,0)],replies=[0xFFFF,0xFFFF])),
        ('counter-cleared-before-poll',0xCA1,b'\0',b'\x01','input_wait_for_ok',dict(frames=0,samples=[zero])),
        ('unsigned-frame-compare',0xCC3,b'\x72',b'\x7C','input_wait_for_ok',dict(frames=0x8000,samples=[(0,0,0,0,0x4000),(0,0,0,0,0x8000)])),
        ('zero-frames-still-poll',0xCA3,b'\x90\x0E',b'\x90'*5,'input_wait_for_ok',dict(frames=0,samples=[zero])),
        ('counter-word-width',0xCBD,b'\xA1',b'\xA0','input_wait_for_ok',dict(frames=0x100,samples=[(0,0,0,0,1),(0,0,0,0,0x100)])),
        ('measure-Pascal-cleanup',0xC61,b'\x04',b'\x02','input_wait_for_ok_or_measure',dict(active=0,frames=0,samples=[zero])),
        ('frame-Pascal-cleanup',0xCC9,b'\x02',b'\x04','input_wait_for_ok',dict(frames=0,samples=[zero])),
        ('measure-true-is-one',0xC89,b'\x01',b'\x02','input_wait_for_ok_or_measure',dict(samples=[shot])),
        ('frame-true-is-one',0xCB7,b'\x01',b'\x02','input_wait_for_ok',dict(samples=[shot])),
        ('false-is-zero-AX',0xC95,b'\xC0',b'\xC9','input_wait_for_ok_or_measure',dict(measure=0,samples=[(0,0x4000,0,0,0)])),
    )
    rejected=[]
    for name,offset,old,new,kind,options in controls:
        raw=bytearray(target.program_image);at=CODE_SEGMENT*16+offset
        need(raw[at:at+len(old)]==old,'literal mutation anchor '+name)
        raw[at:at+len(new)]=new;m=Machine(replace(target,program_image=bytes(raw)),0x3000)
        try:
            try:m.run(kind,**options)
            except ValueError:rejected.append(name)
            else:raise ValueError('MAINL wait mutation survived: '+name)
        finally:m.close()
    return dict(count=len(rejected),rejected=rejected)
