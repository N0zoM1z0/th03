"""Attract wait with actual input/demo instructions and independent contracts.

Ordinary cases enter the complete function. Explicit loop-continuation cases
also execute its prologue, then supply SI at the first poll boundary; they test
signed WORD wrap without pretending that 32768 frames elapsed. Device sampling,
frame delays, graphics libraries and failed execl remain bounded interfaces.
"""
import hashlib,json,struct
from dataclasses import replace
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import UcError
from unicorn.x86_const import UC_X86_REG_EFLAGS
from lib.op_attract_layout import START,SIZE
from lib.op_dispatch_runtime import Machine as DispatchMachine,ENTRIES as DISPATCH_ENTRIES,HELPERS,REG,GPRS,PAIRINGS,SEEDS,add_flags
from lib.op_cfg_runtime import RESIDENT,ACTIVE,MIDI,reply
from lib.op_exit_runtime import specification as exit_events
from lib.shared_input_layout import PROFILES
from lib.shared_input_runtime import Prediction as InputPrediction,service_reply,cmp16

P=PROFILES['op'];INPUT=P['code_segment']*16+P['start'];DEMO=DISPATCH_ENTRIES['start_demo'][0]
ROOT_SERVICES={P['code_segment']*16+P['delay']:('delay',2,4),0x28D8:('super',6,4),0xB10A:('unput',2,2)}
INPUT_SERVICES={P['code_segment']*16+P['sense']:'sense',P['js']:'js'}
def need(v,m):
    if not v:raise ValueError('OP attract contract: '+str(m))
def u16(memory,a):return int.from_bytes(memory[a:a+2],'little')
def u32(memory,a):return int.from_bytes(memory[a:a+4],'little')

class DemoPrediction:
    """Compose the accepted demo specification with the actual incoming stack."""
    def __init__(self,m,regs,sp):
        self.memory=bytearray(m.shadow);self.events=[];self.sp=sp;self.name='demo';self.delta=2
        self.regs=dict(regs);self.flags=m.uc.reg_read(UC_X86_REG_EFLAGS);self.mask=0x8D5;self.if_df=self.flags&0x600
        off=u16(self.memory,m.data+RESIDENT);seg=u16(self.memory,m.data+RESIDENT+2);base=seg*16+off
        def store(off,size,value):
            self.events.append(('store',base+off,size,value));self.memory[base+off:base+off+size]=value.to_bytes(size,'little')
        store(0xE,1,1);store(0xF,1,1);num=(self.memory[base+0x39]+1)&255;store(0x39,1,num)
        if num>4:num=1;store(0x39,1,1)
        for off,val in ((0x17,0),(0x33,0),(0x28,0x7F),(0x35,0)):store(off,1,val)
        pair=PAIRINGS[(num-1)*2:num*2] if num else (0x8F,0)
        for off,val in zip((0xC,0xD),pair):store(off,1,val)
        self.random=SEEDS[num-1] if num else 0x05090B07;store(0x10,4,self.random)
        for i in range(16):store(0x18+i,1,0)
        self.events.append(('service','palette_black_out',1))
        buffer=sp-16;options=bytes(self.memory[base+v] for v in (0x15,0x16,0xB));trash=self.memory[0x70000+buffer+3]
        self.file=options+bytes((trash,))+bytes(m.file[4:])
        self.events += [('service','append',b'YUME.CFG\0'.hex()),('service','seek',(0,0)),
            ('service','write',(0x7000,buffer,4,self.file[:4].hex())),('service','close',None),('service','gaiji_restore',None)]
        if self.memory[m.data+ACTIVE]:self.events.append(('interrupt',0x61 if self.memory[m.data+MIDI]==1 else 0x60,0x100))
        self.events += [row if row[0]=='out' else ('service',row[0],None) for row in exit_events('exit')]
        self.events.append(('service','execl',(0x16F,m.ds,0x16F,m.ds,0,0)))
        self.count=sum(e[0] in ('service','interrupt') for e in self.events)
        self.regs,_=reply(self.regs,self.count,m.seed,self.flags,m.status);self.value=add_flags(sp-16,12)
        self.full={n:m.uc.reg_read(GPRS[n])&0xFFFF0000|self.regs[n] for n in GPRS}
        self.full['ax']=self.random&0xFFFF0000|self.regs['ax'];self.index=0

class Machine(DispatchMachine):
    def __init__(self,mz,load):
        super().__init__(mz,load)
        self.owned=set(range(START,START+SIZE));self.nested=set(range(DEMO,DEMO+202))|set(range(INPUT,INPUT+36))
        for a,s in HELPERS:self.nested.update(range(a,a+s))
        for a,s in ((START,SIZE),(INPUT,36)):
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[a:a+s],a));need(sum(i.size for i in rows)==s,'complete added instructions')
            self.instructions.update({i.address:i.size for i in rows})
        self.instructions={a:s for a,s in self.instructions.items() if a in self.owned|self.nested}
    def registers(self):return {n:self.r(n) for n in (*GPRS,'cs','ds','es','ss')}
    def outside_stack(self,expected):
        actual=bytes(self.uc.mem_read(0,1<<20));lo,hi=0x70000+self.stack-80,0x70000+self.stack
        expected[lo:hi]=actual[lo:hi];need(actual==expected,'complete memory outside 80 stack bytes')
    def root_event(self,e):
        need(self.root_index<len(self.plan) and e==self.plan[self.root_index],f'root event {self.root_index}: {e}; expected {self.plan[self.root_index:self.root_index+1]}')
        self.root_index+=1
    def event(self,e):
        if self.active is None:
            self.root_event(e)
            if e[0]=='store':self.shadow[e[1]:e[1]+e[2]]=e[3].to_bytes(e[2],'little')
        else:
            h=self.active
            if h.name=='input' and e[0]=='store':e=('write',*e[1:])
            need(h.index<len(h.events) and e==h.events[h.index],f'{h.name} event {h.index}: {e}; expected {h.events[h.index:h.index+1]}');h.index+=1
    def begin_helper(self,name):
        self.root_event(('helper',name));self.outside_stack(self.shadow);regs=self.registers();sp=self.r('sp')
        if name=='demo':h=DemoPrediction(self,regs,sp);self.calls=0
        else:
            need(self.poll<len(self.samples),'bounded input sample stream');sample=self.samples[self.poll];self.poll+=1
            h=InputPrediction(self.shadow,regs,'op',self.data,self.seed,self.uc.reg_read(UC_X86_REG_EFLAGS),[sample],self.present,0)
            h.run('input_mode_interface');h.regs['cs']=self.cs;h.name='input';h.index=0;h.sp=sp;h.delta=4;h.mask,h.value=h.flags_mask,h.flags_value
            h.if_df=self.uc.reg_read(UC_X86_REG_EFLAGS)&0x600;h.full={n:self.uc.reg_read(GPRS[n])&0xFFFF0000|h.regs[n] for n in GPRS};h.service_index=0;h.sample=sample
        h.return_rva=(self.cs*16+u16(bytes(self.uc.mem_read(0x70000+sp,2)),0)-self.base);self.active=h
    def finish_helper(self):
        h=self.active;need(self.r('sp')==h.sp+h.delta,'actual helper cleanup')
        need(self.registers()==h.regs,'independent '+h.name+' WORD registers')
        need(all(self.uc.reg_read(GPRS[n])==h.full[n] for n in GPRS),'independent '+h.name+' DWORD effects')
        f=self.uc.reg_read(UC_X86_REG_EFLAGS);need(f&h.mask==h.value&h.mask and f&0x600==h.if_df,'independent '+h.name+' flags')
        need(h.index==len(h.events),'complete '+h.name+' event protocol');self.outside_stack(h.memory)
        if h.name=='demo':need(self.calls==h.count and bytes(self.file)==h.file,'complete real demo file transaction')
        self.helper_trace.update(json.dumps((h.name,h.events),sort_keys=True).encode())
        self.shadow=h.memory;self.helper_calls+=1;self.active=None
    def input_service(self,kind):
        h=self.active;need(h is not None and h.name=='input','device service inside real input helper')
        sample=h.sample;post=dict(single=sample[0],player1=sample[1],player2=sample[2],joystick=0) if kind=='sense' else dict(joystick=sample[3])
        self.event(('service',kind,post,None))
        for field,value in post.items():self.uc.mem_write(self.data+P[field],struct.pack('<H',value))
        h.service_index+=1;regs,flags=service_reply(self.registers(),h.service_index,self.seed,self.uc.reg_read(UC_X86_REG_EFLAGS))
        for n in ('ax','cx','dx','es'):self.uc.reg_write(REG[n],regs[n])
        self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
    def code(self,uc,address,size,_):
        try:
            rva=address-self.base
            if self.active and rva==self.active.return_rva:self.finish_helper()
            if rva==0x9E24 and self.continuation is not None and not self.resumed:self.parked=True;uc.emu_stop();return
            if rva in (INPUT,DEMO):self.begin_helper('input' if rva==INPUT else 'demo')
            if rva in INPUT_SERVICES:
                sp=self.r('sp');ip,cs=struct.unpack('<HH',bytes(uc.mem_read(0x70000+sp,4)))
                need(cs*16+ip-self.base in self.instructions,'real device far frame');self.input_service(INPUT_SERVICES[rva])
                uc.reg_write(REG['sp'],sp+4);uc.reg_write(REG['cs'],cs);uc.reg_write(REG['ip'],ip);return
            if rva in ROOT_SERVICES:
                need(self.active is None,'graphics/delay only in root protocol');name,args,frame=ROOT_SERVICES[rva];sp=self.r('sp')
                payload=struct.unpack('<'+'H'*(args//2),bytes(uc.mem_read(0x70000+sp+frame,args)))
                self.root_event(('library',name,payload));ip=u16(bytes(uc.mem_read(0x70000+sp,2)),0);cs=self.cs if frame==2 else u16(bytes(uc.mem_read(0x70000+sp+2,2)),0)
                need(cs*16+ip-self.base in self.instructions,'real root library frame');self.root_calls+=1
                values,flags=reply(self.registers(),self.root_calls,self.seed,self.uc.reg_read(UC_X86_REG_EFLAGS),self.status)
                for n in ('ax','bx','cx','dx','es'):uc.reg_write(REG[n],values[n])
                uc.reg_write(UC_X86_REG_EFLAGS,flags);uc.reg_write(REG['sp'],sp+frame+args);uc.reg_write(REG['cs'],cs);uc.reg_write(REG['ip'],ip);return
            super().code(uc,address,size,_)
        except Exception as e:self.fail(e)
    def run(self,*,polls=1,samples=None,present=0,random=0xFFFFFFFF,demo=0,active=1,midi=0,continuation=None,
            seed=0x1357,status=0xFFFF,flags=0x202,stack=0xF800,resseg=0x6000,resoff=0x31):
        need(1<=polls<=523 and (continuation is None or 0<=continuation<=65535),'bounded polls / explicit continuation')
        need(0<=present<=65535 and 0<=random<=0xFFFFFFFF and all(0<=v<=255 for v in (demo,active,midi)), 'WORD/DWORD/BYTE fixture widths')
        need(80<=stack<=0xFFF0 and resseg in (0x5000,0x6000) and 0<=resoff<=0xFF80,'disjoint resident and 80-byte stack')
        self.uc.mem_write(0,bytes(self.initial));self.stack,self.seed,self.status=stack,seed,status
        self.file=bytearray(b'\x02\x01\x03\x48\x57\0\x50\xA7');self.uc.mem_write(0x70000+stack-80,b'\xD3'*80);self.uc.mem_write(0x70000+stack,b'\xFF\xFF\x5A\xA5')
        self.uc.mem_write(self.data+RESIDENT,struct.pack('<HH',resoff,resseg));self.uc.mem_write(self.data+ACTIVE,bytes((active,)));self.uc.mem_write(self.data+MIDI,bytes((midi,)))
        base=resseg*16+resoff;self.uc.mem_write(base,b'\xA5'*0x60);self.uc.mem_write(base+0x10,struct.pack('<I',random));self.uc.mem_write(base+0x39,bytes((demo,)))
        self.uc.mem_write(self.data+P['presence'],struct.pack('<H',present));self.uc.mem_write(self.data+P['single'],b'\xFF\xFF')
        self.samples=list(samples) if samples is not None else [(0,0,0,0)]*(polls-1)+[(0x8000,0,0,0)]
        need(1<=len(self.samples)<=523 and all(len(s)==4 and all(0<=v<=65535 for v in s) for s in self.samples),'bounded WORD sample stream')
        self.present,self.poll=present,0;self.shadow=bytearray(self.uc.mem_read(0,1<<20));self.plan=[('store',self.data+P['single'],2,0)]
        frame=continuation or 0;rand=random;d=demo;self.demo_count=0
        for i,sample in enumerate(self.samples):
            self.plan.append(('helper','input'));rand=(rand+1)&0xFFFFFFFF;self.plan.append(('store',base+0x10,4,rand));frame=(frame+1)&65535
            if 520<frame<0x8000:
                self.plan.append(('helper','demo'));self.demo_count+=1;d=(d+1)&255;d=1 if d>4 else d;rand=SEEDS[d-1] if d else 0x05090B07
            self.plan.append(('library','delay',(1,)))
            value=sample[0]|sample[1]|(sample[3] if present else 0)
            if value:need(i==len(self.samples)-1,'stream ends at first merged input');break
        else:raise ValueError('OP attract contract: finite stream must terminate')
        self.plan.append(('library','super',(0,256,160)))
        for x in range(176,288,8):self.plan.extend((('library','unput',(x,)),('library','super',(2,256,x)),('library','delay',(1,))))
        self.initial_regs={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)};self.high={n:(seed^0x5AA5)<<16 for n in GPRS}
        for n in GPRS:self.uc.reg_write(GPRS[n],self.high[n]|self.initial_regs[n])
        self.initial_regs.update(cs=self.cs,ds=self.ds,es=seed,ss=0x7000)
        for n in ('cs','ds','es','ss'):self.uc.reg_write(REG[n],self.initial_regs[n])
        self.uc.reg_write(REG['sp'],stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        self.continuation,self.resumed,self.parked=continuation,False,False;self.active=None;self.root_index,self.root_calls,self.helper_calls,self.calls=0,0,0,0;self.error,self.returned=None,False
        self.helper_trace=hashlib.sha256()
        try:
            self.uc.emu_start(self.base+START,0x100000,count=1000000)
            if self.parked:
                self.uc.reg_write(REG['si'],continuation);self.resumed=True;self.uc.emu_start(self.base+0x9E24,0x100000,count=1000000)
        except UcError as e:raise ValueError('OP attract contract: guest fault') from e
        need(self.error is None,self.error or 'guest error');need(self.returned and self.r('sp')==stack+2,'near root return')
        need(self.active is None and self.root_index==len(self.plan) and self.poll==len(self.samples),'complete root/helper protocol')
        expected,_=reply(self.initial_regs,self.root_calls,seed,flags,status);need(self.registers()==expected,'root final WORD registers')
        for n in GPRS:
            high=(rand&0xFFFF0000) if n=='ax' and self.demo_count else self.high[n]
            need(self.uc.reg_read(GPRS[n])==high|expected[n],'root DWORD high halves')
        f=self.uc.reg_read(UC_X86_REG_EFLAGS);need(f&0x8D5==cmp16(288,288) and f&0x600==flags&0x600,'final column compare and inherited IF/DF')
        self.outside_stack(self.shadow)
        return dict(polls=self.poll,demo_calls=self.demo_count,continuation=continuation,registers=self.registers(),flags=f&0xED5,
            events=len(self.plan),trace_sha256=hashlib.sha256(json.dumps(self.plan).encode()).hexdigest(),helper_trace_sha256=self.helper_trace.hexdigest(),random=u32(self.shadow,base+0x10),file_hex=self.file.hex())

def cases():
    for demo in range(256):yield dict(demo=demo,continuation=520)
    for present in (0,1,0x8000,0xFFFF):
        for lane in range(4):
            for bit in range(16):
                sample=[0,0,0,0];sample[lane]=1<<bit;rows=[tuple(sample)]
                if lane==2 or (lane==3 and not present):rows.append((1,0,0,0))
                yield dict(present=present,samples=rows)
    for polls in (1,2,519,520,521,522,523):
        for random in (0,0x7FFFFFFF,0xFFFFFFFF):
            for present in (0,1):yield dict(polls=polls,random=random,present=present)
    for frame in (519,520,521,0x7FFE,0x7FFF,0x8000,0xFFFE,0xFFFF):
        for status in (0,0x7FFF,0x8000,0xFFFF):yield dict(continuation=frame,status=status)
    for segment in (0x5000,0x6000):
        for off in (0,0x31,0xFF80):
            for flags in (2,0x202,0x402,0xED7):yield dict(continuation=520,demo=255,resseg=segment,resoff=off,flags=flags)
    for active,midi in ((0,0),(0,1),(1,1),(1,2),(0x80,0xFF)):yield dict(continuation=520,active=active,midi=midi)

def verify(target,candidate):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(mz,load)
            try:
                trace=hashlib.sha256();normal=continuations=0;maximum_polls=0
                for count,options in enumerate(cases(),1):
                    row=m.run(seed=0x1357 if count&1 else 0xECA8,stack=0x80 if count&1 else 0xFFF0,**options)
                    if options.get('continuation') is None:normal+=1
                    else:continuations+=1
                    maximum_polls=max(maximum_polls,row['polls']);trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.owned and m.nested_covered==m.nested,'all 105 root and 402 actual helper instruction bytes execute')
                loads.append(dict(load_segment=load,cases=count,ordinary_entry_cases=normal,loop_continuation_cases=continuations,
                    covered_owner_bytes=len(m.covered),executed_nested_bytes=len(m.nested_covered),maximum_observed_stack_depth=m.maximum_stack,
                    maximum_sample_polls=maximum_polls,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent target/candidate attract observations')
    return dict(images=2,functions=1,code_bytes=105,executed_owner_bytes=105,cases_per_image=sum(o['cases'] for o in observations[0]),
        exhaustive_demo_bytes=256,observations=observations[0],
        scope='actual maintained input/demo/cfg/sound/cleanup; bounded device/timing/graphics/failed exec; explicit loop-continuation fixtures supply SI after real prologue, not elapsed-frame claims')

def negative_controls(target):
    controls=(
        ('input-clear-is-WORD',0x9E1A,b'\xC7',b'\xC6',{}),
        ('initial-input-is-cleared',0x9E1E,b'\0',b'\x01',{}),
        ('real-input-interface',0x9E25,b'\xD6',b'\xFA',{}),
        ('resident-random-is-DWORD',0x9E2D,b'\x66',b'\x90',{}),
        ('resident-random-increments',0x9E30,b'\x47',b'\x4F',{}),
        ('frame-increments-before-compare',0x9E32,b'\x46',b'\x4E',dict(continuation=520)),
        ('threshold-is-520',0x9E35,b'\x08',b'\x09',dict(continuation=520)),
        ('threshold-is-signed',0x9E37,b'\x7E',b'\x76',dict(continuation=0x7FFF)),
        ('input-on-521-still-starts-demo',0x9E3A,b'\x10',b'\x11',dict(continuation=520)),
        ('poll-delay-is-one-frame',0x9E3D,b'\x01',b'\x02',{}),
        ('merged-input-ends-wait',0x9E48,b'\x74',b'\x75',{}),
        ('left-box-tile-number',0x9E51,b'\0',b'\x01',{}),
        ('right-column-origin',0x9E58,b'\xB0',b'\xB8',{}),
        ('near-unput-target',0x9E5E,b'\xAA',b'\xAB',{}),
        ('right-box-tile-number',0x9E63,b'\x02',b'\x03',{}),
        ('animation-delay-one-frame',0x9E6D,b'\x01',b'\x02',{}),
        ('column-step-eight',0x9E75,b'\x08',b'\x10',{}),
        ('last-column-bound',0x9E78,b'\x20',b'\x18',{}),
        ('near-root-return',0x9E7E,b'\xC3',b'\xCB',{}),
        ('actual-input-merges-player1',INPUT+30,b'\x09',b'\x89',dict(samples=[(0,1,0,0)])),
        ('actual-demo-keeps-BYTE-wrap',0x9D60,b'\x47',b'\x4F',dict(continuation=520,demo=255)),
    )
    rejected=[]
    for name,at,old,new,options in controls:
        raw=bytearray(target.program_image);need(raw[at:at+len(old)]==old,'literal mutation anchor '+name);raw[at:at+len(new)]=new;m=None
        try:
            try:m=Machine(replace(target,program_image=bytes(raw)),0x3000);m.run(**options)
            except ValueError:rejected.append(name)
            else:raise ValueError('OP attract mutation survived: '+name)
        finally:
            if m:m.close()
    return dict(count=len(rejected),rejected=rejected)
