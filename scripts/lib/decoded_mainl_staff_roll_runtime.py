"""Complete staff-roll source specification and actual nested native execution.

No acceptance is implied by this module until the complete review gates pass.
"""
import hashlib
import json
import struct
from unicorn import UcError,UC_HOOK_CODE
from unicorn.x86_const import *
from lib.decoded_mainl_staff_roll_layout import CS,DS,START,SIZE,DATA,FILES
from lib.decoded_mainl_staff_roll_services import State,SoundSpec,InputSpec,need
from lib.decoded_mainl_staff_roll_machine import Machine as Physical,external_reply
from lib.decoded_mainl_staff_callers_runtime import Spec as CallerSpec,ClearSpec
from lib.decoded_mainl_staff_single_runtime import Spec as SingleSpec,DEFAULT_SCHEDULE
from lib.decoded_mainl_staff_hold_runtime import Spec as HoldSpec
from lib.decoded_mainl_staff_pair_runtime import Spec as PairSpec
from lib.decoded_mainl_staff_verdict_runtime import Spec as VerdictSpec
from lib.decoded_mainl_cdg_runtime import Spec as CdgSpec
from lib.decoded_mainl_pi_runtime import ARITH,signed
from lib.decoded_mainl_pi_free_runtime import address
from lib.decoded_mainl_root_helpers_runtime import GPRS,REG,specification as root_spec,logical


class Spec(State):
    def __init__(self,*args):
        super().__init__(*args)
        self.counts={}
        self.input_iterations=0
        self.fade_iterations=0

    def child(self,child):
        self.events.extend(child.events)
        self.r,self.high,self.flags,self.mask=child.r,child.high,child.flags,child.mask

    def inc(self,name,field=False):
        carry=self.flags&1
        if field:
            self.field(DATA[name],self.op(self.dg(DATA[name]),1))
        else:
            self.r[name]=self.op(self.r[name],1)
        self.flags=(self.flags&~1)|carry

    def al(self,value):
        self.r['ax']=(self.r['ax']&0xFF00)|(value&255)

    def half(self):
        self.r['dx']=65535 if signed(self.r['ax'])<0 else 0
        self.r['ax']=self.op(self.r['ax'],self.r['dx'],True)
        value=self.r['ax']
        self.r['ax']=(signed(value)>>1)&65535
        self.flags=(self.flags&0x600)|2|logical(self.r['ax'],16)|(value&1)
        self.mask=0x8C5

    def les(self):
        value=self.dg(DATA['resident'],4)
        self.r['bx'],self.r['es']=value&65535,value>>16

    def resident_byte(self,offset):
        return self.memory[address(self.r['es'],(self.r['bx']+offset)&65535)]

    def external(self,kind,continuation,cleanup,arguments=0):
        self.frame(continuation)
        if kind=='volume':
            self.r['cs']=self.o['load']+0xC7E
        at=address(self.ss,self.r['sp'])
        mask=self.mask|0x600
        self.events.append(('roll-external',kind,self.full(),bytes(self.memory[at:at+4+arguments]).hex(),self.flags&mask,mask,cleanup))
        self.r,self.flags=external_reply(self.r,self.flags,self.o)
        self.mask=ARITH
        self.returned(cleanup)

    def far(self,kind,continuation):
        self.frame(continuation)
        self.r['cs']=self.o['load']+0xC7E
        at=address(self.ss,self.r['sp'])
        if kind in ('single','single_noalpha','free'):
            child=CdgSpec(self.memory,self.r,self.high,self.flags,self.o['cdg'])
            child.invoke(kind)
        else:
            mask=self.mask|0x600
            frame=4+(6 if kind=='load' else 2 if kind in ('kaja','delay') else 0)
            self.events.append(('roll-entry',kind,self.full(),bytes(self.memory[at:at+frame]).hex(),self.flags&mask,mask))
            child=(InputSpec if kind=='input' else SoundSpec)(self.memory,self.r,self.high,self.flags,self.o)
            child.run() if kind=='input' else child.run(kind)
        self.child(child)
        self.events.append(('owned-return',kind,self.full(),self.flags&(self.mask|0x600),self.mask|0x600))
        label='cdg-'+kind if kind in ('single','single_noalpha','free') else kind
        self.counts[label]=self.counts.get(label,0)+1

    def near(self,kind,continuation):
        self.push(continuation)
        options=dict(self.o)
        if kind in ('single','hold','pair','gallery','verdict'):
            at=address(self.ss,self.r['sp'])
            frame=dict(single=8,hold=8,pair=8,gallery=8,verdict=2)[kind]
            mask=self.mask|0x600
            self.events.append(('roll-entry',kind,self.full(),bytes(self.memory[at:at+frame]).hex(),self.flags&mask,mask))
            if kind=='gallery':
                options['kind']='gallery'
                child=CallerSpec(self.memory,self.r,self.high,self.flags,options)
                _,_,_,fault=child.run(kind)
                need(not fault,'gallery returns in complete roll')
            elif kind=='verdict':
                options.update(writes=self.o['verdict_writes'],flag_schedule=())
                child=VerdictSpec(self.memory,self.r,self.high,self.flags,options)
                child.run()
            else:
                child={'single':SingleSpec,'hold':HoldSpec,'pair':PairSpec}[kind](self.memory,self.r,self.high,self.flags,options)
                _,_,mask,stopped=child.run()
                child.mask=mask
                need(stopped=='return','owned controller returns in complete roll')
        elif kind=='clear':
            child=ClearSpec(self.memory,self.r,self.high,self.flags,options)
            child.run()
        else:
            if kind=='gate':
                measure,writes,flags=self.o['schedule'][0]
                options.update(pmd_measure=measure,pmd_writes=writes,pmd_flags=flags)
            child=State(self.memory,self.r,self.high,self.flags,options)
            child.invoke(kind)
            need(not child.prefix,'complete roll does not inherit prefix credit')
        self.child(child)
        self.events.append(('owned-return',kind,self.full(),self.flags&(self.mask|0x600),self.mask|0x600))
        self.counts[kind]=self.counts.get(kind,0)+1

    def color(self,color,continuation):
        self.push((0xC0<<16)|color,4)
        self.frame(continuation)
        at=address(self.ss,self.r['sp'])
        self.events.append(('color-entry',self.full(),bytes(self.memory[at:at+8]).hex(),self.flags&(ARITH|0x600)))
        out,mask,flags,events,_=root_spec('setcolor',self.r,self.flags,random_seed=0,mode=0xC0,color=color,
            strings=(b'\0',b'\0'),pointers=((0x5000,0),(0x6000,0)),dos_status=0,reply_seed=0)
        self.events.extend(events)
        for event in events:
            if event[0]=='store':
                _,at,width,value=event
                self.memory[at:at+width]=value.to_bytes(width,'little')
        self.r,self.flags,self.mask=out,flags|2,mask
        self.r['cs']=self.o['load']+CS
        self.events.append(('owned-return','color',self.full(),self.flags&(self.mask|0x600),self.mask|0x600))

    def out(self,port,value):
        self.r['dx']=port
        self.al(value)
        self.events.append(('out',port,1,value&255,self.flags&0x200))

    def box(self,inner,continuation):
        self.push(0x10008 if inner else 0,4)
        self.push(0x4E0187 if inner else 0x4F018F,4)
        self.frame(continuation)
        at=address(self.ss,self.r['sp'])
        self.events.append(('box',self.full(),bytes(self.memory[at:at+12]).hex(),self.flags&(ARITH|0x600)))
        self.r,self.flags=external_reply(self.r,self.flags,self.o)
        self.mask=ARITH
        self.returned(8)

    def prepare(self):
        self.enter()
        self.push(self.r['si'])
        self.push(self.r['di'])
        self.push(0x210)
        self.far('kaja',0x2E2A)
        self.push(4)
        self.external('palette-black',0x2E31,2,2)
        self.push(255)
        self.external('volume',0x2E39,0,2)
        self.pop('cx')
        self.push(0x100)
        self.far('kaja',0x2E42)
        self.field(DATA['cap'],80,1)
        self.r['si']=1
        while True:
            self.op(self.r['si'],9,True)
            if signed(self.r['si'])>=9:
                break
            self.les()
            self.r['bx']=self.op(self.r['bx'],self.r['si'])
            self.al(self.resident_byte(0x17))
            self.field(DATA['score']+self.r['si'],self.r['ax']&255,1)
            self.inc('si')
        self.les()
        self.al(3)
        self.al(self.op(3,self.resident_byte(0x36),True,bits=8))
        self.field(DATA['score'],self.r['ax']&255,1)
        self.r['ax']=self.resident_byte(12)
        carry=self.flags&1
        self.r['ax']=self.op(self.r['ax'],1,True)
        self.flags=(self.flags&~1)|carry
        self.half()
        self.field(DATA['playchar'],self.r['ax']&255,1)
        self.al(self.resident_byte(11))
        self.field(DATA['rank'],self.r['ax']&255,1)
        self.al(self.resident_byte(0x38))
        self.field(DATA['skill'],self.r['ax']&255,1)
        self.r['ax']=self.dg(DATA['score']+7,1)
        self.op(self.r['ax'],3,True)
        case=self.r['ax']
        if case!=3:
            self.op(self.r['ax'],4,True)
        if case in (3,4):
            for add in ((2,7) if case==3 else (7,)):
                self.r['ax']=self.dg(DATA['score']+6,1)
                self.half()
                self.al(self.op(self.r['ax']&255,self.dg(DATA['skill'],1),bits=8))
                self.al(self.op(self.r['ax']&255,add,bits=8))
                self.field(DATA['skill'],self.r['ax']&255,1)
        digit=self.dg(DATA['score']+7,1)
        self.op(digit,5,True,bits=8)
        if digit>=5:
            self.al(self.dg(DATA['skill'],1))
            self.al(self.op(self.r['ax']&255,15,bits=8))
            self.field(DATA['skill'],self.r['ax']&255,1)
        digit=self.dg(DATA['score']+8,1)
        self.op(digit,0,True,bits=8)
        if digit:
            self.field(DATA['skill'],100,1)
        skill=self.dg(DATA['skill'],1)
        self.op(skill,100,True,bits=8)
        if skill>100:
            self.field(DATA['skill'],100,1)

    def run(self):
        self.prepare()
        self.push(0x600)
        self.push(self.ds)
        self.push(0xC28)
        self.far('load',0x2EF4)
        self.r['sp']=self.op(self.r['sp'],6)
        self.field(DATA['tone'],0)
        self.external('palette-show',0x2F02,0)
        self.push(self.ds)
        self.push(0xC2D)
        self.external('palette-entry',0x2F0B,4,4)
        self.external('palette-show',0x2F10,0)
        self.color(8,0x2F1B)
        self.out(0xA6,1)
        self.box(False,0x2F2F)
        self.out(0xA6,0)
        self.box(False,0x2F43)
        self.color(0,0x2F4E)
        self.out(0xA6,1)
        self.box(True,0x2F65)
        self.out(0xA6,0)
        self.box(True,0x2F7C)
        self.frame(0x2F81)
        self.entry('off',4)
        self.al(0)
        self.logical(0,8)
        self.events.append(('out',0x7C,1,0,self.flags&0x200))
        self.returned(0)
        self.events.append(('owned-return','off',self.full(),self.flags&(self.mask|0x600),self.mask|0x600))
        self.out(0xA4,1)
        for slot,(_,_,filename) in enumerate(FILES):
            self.push(slot)
            self.push(self.ds)
            self.push(filename)
            self.push(0)
            self.far('single' if slot in (2,3) else 'single_noalpha',0x2F94+slot*13)
        self.near('reset',0x3026)
        self.field(DATA['frame'],0)
        self.les()
        value=int.from_bytes(self.memory[address(self.r['es'],(self.r['bx']+16)&65535):address(self.r['es'],(self.r['bx']+16)&65535)+4],'little')
        self.full32('ax',value)
        self.field(DATA['seed'],value,4)
        self.field(DATA['page'],0,1)
        self.field(DATA['tone'],100)
        self.external('palette-show',0x3049,0)
        self.push(0)
        self.far('kaja',0x3050)
        self.field(DATA['adapt'],1,1)
        self.field(DATA['requested'],1,1)
        self.push(1)
        self.far('delay',0x3061)
        self.field(DATA['vsync'],0)
        while True:
            self.near('clear',0x306A)
            self.near('tick',0x306D)
            self.inc('frame',field=True)
            self.push(0x40100,4)
            self.near('gate',0x307A)
            self.logical(self.r['ax'])
            if self.r['ax']:
                break
        for name,value,size in (('enabled',0,1),('height',0,2),('limit',200,2),('speed',2,2),('duration',65,2),('secondary',0,1)):
            self.field(DATA[name],value,size)
        def controller(kind,slot,enter,leave,continuation):
            self.push((slot<<16)|enter,4)
            self.push(leave)
            self.near(kind,continuation)
        controller('single',0,8,10,0x30A8)
        self.field(DATA['speed'],1)
        self.field(DATA['duration'],161)
        self.field(DATA['adapt'],0,1)
        controller('single',1,16,20,0x30C4)
        self.field(DATA['height'],32)
        self.field(DATA['limit'],168)
        controller('hold',2,22,24,0x30DB)
        self.field(DATA['secondary'],7,1)
        self.field(DATA['limit'],216)
        self.field(DATA['height'],0xFFF0)
        controller('pair',3,32,34,0x30F7)
        self.field(DATA['secondary'],0,1)
        self.field(DATA['limit'],200)
        self.field(DATA['height'],0)
        for slot,enter,leave,continuation in ((4,36,38,0x3113),(11,42,44,0x311E),(5,48,50,0x3129),(6,54,56,0x3134),(10,60,62,0x313F)):
            controller('single',slot,enter,leave,continuation)
        self.field(DATA['frame'],0)
        while True:
            self.near('clear',0x3148)
            for packed,slot,continuation in ((0x1400080,8,0x3153),(0xC000F0,9,0x315E)):
                self.push(packed,4)
                self.push(slot)
                self.near('gallery',continuation)
            self.near('tick',0x3161)
            self.inc('frame',field=True)
            self.push(0x420100,4)
            self.near('gate',0x316E)
            self.logical(self.r['ax'])
            if self.r['ax']:
                break
        self.al(1)
        self.al(self.op(1,self.dg(DATA['page'],1),True,bits=8))
        self.r['dx']=0xA6
        self.events.append(('out',0xA6,1,self.r['ax']&255,self.flags&0x200))
        self.near('verdict',0x317F)
        self.out(0xA6,self.dg(DATA['page'],1))
        self.near('verdict',0x3189)
        self.field(DATA['frame'],0)
        self.r['di']=0
        self.logical(0)
        while True:
            if self.o['input_prefix'] and self.input_iterations==self.o['input_prefix']:
                mask=self.mask|0x600
                self.events.append(('roll-input-prefix',self.input_iterations,self.full(),self.flags&mask,mask))
                return self.full(),self.flags,self.mask
            self.far('input',0x3196)
            self.near('clear',0x3199)
            self.near('tick',0x319C)
            self.inc('frame',field=True)
            self.logical(self.r['di'])
            if self.r['di']:
                self.fade_iterations+=1
                self.field(DATA['tone'],self.r['di'])
                self.external('palette-show',0x31AD,0)
                odd=self.dg(DATA['frame'],1)&1
                self.logical(odd,8)
                if odd:
                    carry=self.flags&1
                    self.r['di']=self.op(self.r['di'],1,True)
                    self.flags=(self.flags&~1)|carry
                    self.logical(self.r['di'])
                    if not self.r['di']:
                        break
            else:
                self.input_iterations+=1
                value=self.dg(DATA['input'])
                self.op(value,0,True)
                if not value:
                    continue
                frame=self.dg(DATA['frame'])
                self.op(frame,256,True)
                if signed(frame)>256:
                    self.push(0x208)
                    self.far('kaja',0x31D2)
                    self.r['di']=100
                    self.field(DATA['frame'],0)
        self.r['si']=0
        self.logical(0)
        while True:
            self.op(self.r['si'],32,True)
            if signed(self.r['si'])>=32:
                break
            self.push(self.r['si'])
            self.far('free',0x31E7)
            self.inc('si')
        self.pop('di')
        self.pop('si')
        self.pop('bp')
        self.r['sp']+=2
        return self.full(),self.flags,self.mask


class Machine(Physical):
    def run(self,*,score=(1,2,3,4,5,6,3,0),character=1,credits=3,rank=0,skill=0,rng=1,midi=0,
            sample=(1,0,0,0),joystick=0,active=1,resident=(0x9000,0x100),flags=0x202,ss=0x7000,stack=0xF800,seed=0x1357,prepare_only=False,input_prefix=0):
        need(len(score)==8 and all(0<=v<=255 for v in (*score,character,credits,rank,skill,midi)),'resident BYTE fields')
        need(len(sample)==4 and all(0<=v<=65535 for v in sample),'bounded input samples')
        need(active in range(256) and ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),'bounded BYTE/stack/flag fixtures')
        need(not input_prefix or input_prefix in (1,3,7) and sample==(0,0,0,0),'explicit no-input prefix')
        need(all(0<=v<=65535 for v in resident) and resident[0] in (0x9000,self.ds),'mapped resident segment and WORD offset')
        need(prepare_only or input_prefix or any(sample),'terminal input or explicit native prefix')
        memory=bytearray(self.initial)
        def put(seg,off,value,size=2):
            at=address(seg,off)
            memory[at:at+size]=value.to_bytes(size,'little')
        put(self.ds,DATA['resident'],(resident[0]<<16)|resident[1],4)
        for i,value in enumerate(score):
            put(resident[0],(resident[1]+0x18+i)&65535,value,1)
        for off,value in ((12,character),(11,rank),(0x36,credits),(0x38,skill)):
            put(resident[0],(resident[1]+off)&65535,value,1)
        put(resident[0],(resident[1]+0x10)&65535,rng,4)
        put(self.ds,0x880,active,1)
        put(self.ds,0x1C71,midi,1)
        put(self.ds,0x570,joystick)
        memory[address(self.ds,0x1D0E):address(self.ds,0x1D0E)+32*16]=bytes(32*16)
        put(ss,stack,0xFFFF)
        self.u.mem_write(0,bytes(memory))
        regs={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)}
        regs.update(sp=stack,cs=self.cs,ds=self.ds,es=0x6666,ss=ss,fs=0x3456,gs=0x4567)
        high={n:((seed^0x5AA5)<<16) for n in GPRS}
        for name,register in GPRS.items():
            self.u.reg_write(register,high[name]|regs[name])
        for name in ('cs','ds','es','ss'):
            self.u.reg_write(REG[name],regs[name])
        self.u.reg_write(UC_X86_REG_FS,regs['fs'])
        self.u.reg_write(UC_X86_REG_GS,regs['gs'])
        self.u.reg_write(UC_X86_REG_EFLAGS,flags)
        self.o=dict(load=self.load,stack=stack,prepare_only=prepare_only,input_prefix=input_prefix,box_seed=0xA55A,box_writes=(),schedule=DEFAULT_SCHEDULE,
            ticks=(1,),delay_ticks=(1,),prefix=0,loop_prefix=0,song_bytes=4,sample=sample,sample_seed=0x3210,
            verdict_writes=(),reply_seed=0x89ABCDEF,reply_flags=0x202,
            cdg=dict(load=self.load,status=1,reply_seed=0xA55A,allocations=(0x5000,0x6000),
                header=struct.pack('<5H2B2H',4,16,1,65535,1,1,0x7F,0,0),payload=bytes(range(64)),
                read_limits=(),clear_df=False,writes=()))
        spec=Spec(memory,regs,high,flags,self.o)
        if prepare_only:
            spec.prepare()
            expected,final,mask=spec.full(),spec.flags,spec.mask
        else:
            expected,final,mask=spec.run()
        self.events,self.index,self.observed,self.error,self.returned,self.max_depth=spec.events,0,[],None,False,0
        self.clear_progress,self.actual_clear_stores,self.polls=0,0,0
        self.file_counts={}
        try:
            self.u.emu_start(self.cs*16+START,1<<20,count=200000000)
        except UcError as error:
            raise ValueError('MAINL roll guest exception') from error
        need(self.error is None,self.error or 'guest failure')
        need(self.returned and self.index==len(self.events),'complete native roll return or explicitly selected preparation boundary')
        need(self.regs(True)==expected,'complete DWORD/segment state '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(mask|0x600)==final&(mask|0x600),'defined flags and IF/DF')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'all physical memory including every native frame and caller byte')
        return dict(registers=expected,flags=final&(mask|0x600),flag_mask=mask|0x600,counts=spec.counts,
            input_iterations=spec.input_iterations,fade_iterations=spec.fade_iterations,stack_depth=self.max_depth,
            actual_clear_WORD_callbacks=self.actual_clear_stores,prepare_only=prepare_only,input_prefix=input_prefix,
            trace_sha256=hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest())


def preparation_cases(load):
    for name in ('character','credits','rank','skill','midi','active'):
        for value in range(256):
            yield {name:value}
    for pos in range(8):
        for value in range(256):
            score=[0]*8
            score[pos]=value
            yield dict(score=tuple(score))
    for shift in (0,8):
        for value in range(256):
            yield dict(resident=(0x9000,value<<shift))
    for offset in (0x21B4,0x21DE,0x21EA,0x27C0,0x27DC,0xFFFF):
        yield dict(resident=(load+DS,offset),character=255,credits=255)
    for skill in (0,1,100,127,128,200,254,255):
        for lower in (0,1,100,127,128,200,254,255):
            for upper in (0,3,4,5):
                yield dict(skill=skill,score=(0,0,0,0,0,lower,upper,0))
    for flags in (2,0x202,0x402,0xED7):
        for ss in (0x7000,0x8000):
            for stack in (0x80,0xF800):
                yield dict(flags=flags,ss=ss,stack=stack)


FULL_CASES=({},dict(midi=1,character=0,credits=4,rank=255,skill=255,
    score=(0,0,0,0,0,255,4,0),ss=0x8000,stack=0x80,flags=0xED7,rng=0xFFFFFFFF,seed=0xECA8),
    dict(midi=2,character=255,credits=0,rank=3,skill=250,score=(9,8,7,6,5,4,5,1),
         joystick=1,sample=(0,0,0,65535),flags=2,rng=0x80000000))


def verify(target,candidate):
    from lib.decoded_mainl_staff_roll_proofs import geometry_proof
    proof=geometry_proof(target)
    need(proof==geometry_proof(candidate),'both complete native arithmetic/CFG obligations')
    observations=[]
    for image_index,image in enumerate((target,candidate),1):
        rows=[]
        for load in (0x1000,0x3000):
            machine=Machine(image,load)
            trace=hashlib.sha256()
            complete=[]
            prefixes=[]
            try:
                for count,parameters in enumerate(preparation_cases(load),1):
                    result=machine.run(prepare_only=True,**parameters)
                    trace.update(json.dumps(result,sort_keys=True).encode())
                print(f'Roll: image{image_index} load{load:04X}, {count} complete preparation boundaries',flush=True)
                for parameters in FULL_CASES:
                    result=machine.run(**parameters)
                    need((result['input_iterations'],result['fade_iterations'],result['counts']['cdg-free'],result['stack_depth'],result['actual_clear_WORD_callbacks'])
                         ==(257,199,32,78,7616000),'complete native roll,exact waits/fade/cleanup and every clear WORD callback')
                    complete.append(result)
                    trace.update(json.dumps(result,sort_keys=True).encode())
                    print(f'Roll: image{image_index} load{load:04X}, {len(complete)} actual complete near returns',flush=True)
                for iterations in (1,3,7):
                    result=machine.run(sample=(0,0,0,0),input_prefix=iterations)
                    need(result['input_iterations']==iterations and result['fade_iterations']==0 and 'cdg-free' not in result['counts'],
                         'checked no-input prefixes have no fade/cleanup/near-return credit')
                    prefixes.append(result)
                    trace.update(json.dumps(result,sort_keys=True).encode())
                need(machine.owner<=machine.covered,'all980 owner bytes execute across separately classified full returns and preparation/polling boundaries')
                rows.append(dict(load_segment=load,preparation_boundaries=count,complete_near_returns=len(complete),
                    no_input_prefixes=len(prefixes),executed_owner_bytes=SIZE,maximum_stack_depth=78,
                    clear_WORD_callbacks_per_return=7616000,complete_observations=complete,prefix_observations=prefixes,trace_sha256=trace.hexdigest()))
            finally:
                machine.close()
        observations.append(rows)
    need(observations[0]==observations[1],'independent entire target/candidate observations')
    return dict(images=2,functions=1,code_bytes=SIZE,observations=observations[0],executed_owner_bytes=SIZE,
        ignored_stack_bytes=0,complete_returns_per_image=6,preparation_boundaries_per_image=sum(r['preparation_boundaries'] for r in observations[0]),
        no_input_prefixes_per_image=6,native_geometry_proof=proof,guest_iterations_skipped=False,budget_expiry_used_as_proof=False,
        cold_file_equality_is_whole_source_acceptance=False,physical_IRQ_audio_input_or_pixels_proved=False)


def negative_controls(target):
    controls=(('score-member-addend',0x2E58,1,True),('continues-BYTE-subtraction',0x2E64,1,True),
        ('character-signed-half',0x2E78,1,True),('score3-fallthrough',0x2EAB,1,True),
        ('unsigned-skill-clamp',0x2EDD,1,True),('initial-GRCG-color',0x2F12,1,False),
        ('first-CDG-filename',0x2F8B,1,False),('first-controller-measure',0x30A0,1,False),
        ('second-verdict-call',0x3187,1,False),('input-frame-reset',0x318D,1,False),
        ('signed-input-frame-bound',0x31C6,1,False),('fade-start100',0x31D3,1,False),
        ('fade-odd-frame-mask',0x31B1,1,False),('cleanup32',0x31EA,1,False),
        ('restore-saved-SI',0x31EE,1,False))
    contexts=(('actual-kaja-pop2',0xC7E*16+0x6FE,1,True),('actual-input-far-return',0xC7E*16+0xDE5,8,False))
    rejected=[]
    absolute_controls=tuple((name,CS*16+offset,xor,preparation) for name,offset,xor,preparation in controls)+contexts
    for name,offset,xor,preparation in absolute_controls:
        machine=Machine(target,0x1000)
        at=machine.base+offset
        initial=bytearray(machine.initial)
        initial[at]^=xor
        machine.initial=bytes(initial)
        try:
            try:
                machine.run(prepare_only=preparation)
            except ValueError:
                rejected.append(name)
            else:
                raise ValueError('MAINL roll control survived: '+name)
        finally:
            machine.close()
        print(f'Roll control: rejected {name}',flush=True)
    return dict(count=len(rejected),owner_instruction_mutations=len(controls),actual_context_mutations=len(contexts),
        rejected=rejected,actual_guest_instructions_mutated=True,layout_failure_counted=False,
        prefix_failure_does_not_prove_nontermination=True)
