"""Independent ONGCHK port/store protocol and complete returning CPU contracts.

Real instructions, including all spin and busy loops and nested register writes,
execute. Device replies are finite fixtures; no elapsed time or physical sound
hardware is inferred. A 48-byte private stack is bounded; caller words and all
other physical memory are checked.
"""
import hashlib,json,struct
from dataclasses import replace
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
from unicorn.x86_const import *

PATTERN=b'*+=-PMD ADPCM RAM Check Data-=+*'
CODE_START,CODE_END=0x100,0x47C
SPINS={0x15F,0x167,0x172,0x1F0,0x1F9,0x291,0x29A,0x35C,0x387,0x439,0x46D}
LOOPS={
 'register':(0x461,{0x461,0x462,0x464},16),
 'write_idle':(0x350,{0x350,0x351,0x353},6),
 'write_complete':(0x377,{0x377,0x378,0x37A,0x37C,0x37D},6),
 'dummy_idle':(0x42D,{0x42D,0x42E,0x430},8),
 'read_idle':(0x3FE,{0x3FE,0x3FF,0x401},6),
 'read_ready':(0x407,{0x407,0x408,0x40A},6),
 'read_data':(0x40D,{0x40D,0x40E,0x410},6)}
GPRS={n:globals()['UC_X86_REG_E'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp','sp')}
REG={n:globals()['UC_X86_REG_'+n.upper()] for n in (*GPRS,'cs','ds','es','ss','ip')}

def need(v,m):
    if not v:raise ValueError('ONGCHK contract: '+str(m))

def arith(a,b,bits=8,subtract=False):
    mask=(1<<bits)-1;v=(a-b if subtract else a+b)&mask;sign=1<<(bits-1)
    overflow=((a^b)&(a^v)&sign) if subtract else (~(a^b)&(a^v)&sign)
    return ((int(a<b) if subtract else int(a+b>mask))|(4 if (v&255).bit_count()%2==0 else 0)
        |((a^b^v)&16)|(64 if v==0 else 0)|(128 if v&sign else 0)|(0x800 if overflow else 0))

class Prediction:
    def __init__(self,regs,flags,p):
        self.regs=dict(regs);self.flags=flags;self.p=p;self.iflag=flags&0x200;self.events=[]
        self.base=regs['cs']*16;self.result=0;self.bl=regs['bx']&255
        self.devices={bank:(1,255,255) if kind==3 else (1,0,0) for bank,kind in p['boards']}
        self.devices.update(p['board_replies'])
        self.config=p['config'] if p['config'] is not None else (7 if any(kind==3 for _,kind in p['boards']) else 255)
        self.spins=self.calls=0;self.polls=0;self.loop_points={}
    def store(self,offset,size,value):self.events.append(('store',self.base+offset,size,value))
    def read(self,port,value):
        self.events.append(('in',port,1,value,self.iflag,0));self.polls+=1
        return value
    def out(self,port,value):self.events.append(('out',port,1,value,self.iflag,0))
    def spin(self):self.events.append(('spin',100));self.spins+=1
    def point(self,name):self.loop_points.setdefault(name,len(self.events))
    def idle(self,port,name):
        self.point(name)
        for _ in range(self.p['busy']):self.read(port,0x80)
        self.read(port,8)
    def regwrite(self,index,value):
        self.events.append(('reg',(index<<8)|value));self.calls+=1
        saved=self.iflag;self.iflag=0
        self.read(self.port+4,self.p['noise']);self.idle(self.port+4,'register')
        self.out(self.port+4,index);self.spin();self.out(self.port+6,value)
        self.iflag=saved
    def failed(self):self.result=0;self.store(0x49D,1,0)
    def found(self,port):
        self.port=port
        for i in range(4):self.store(0x49E+2*i,2,port+2*i)
    def detector(self,kind):
        p=self.p;self.result=kind;self.store(0x49D,1,kind);self.store(0x4A6,1,0)
        has=p['rom_word']==0x2A27;self.rom=has
        if has:self.store(0x4A6,1,1)
        if kind==3 and has and p['rom_version']<6:self.failed();return False
        if kind==3 or not has or p['rom_version']>=6:
            value=self.read(0xA460,self.config)
            if value==255:
                if kind==3:self.failed();return False
            else:self.out(0x5F,value);self.out(0xA460,value&0xFC)
        banks=(0x188,0x288) if kind==3 else (0x88,0x188,0x288,0x388)
        if p['override']!=255:banks=((p['override']<<8)|0x88,)
        for bank in banks:
            self.iflag=0;self.spin();self.out(bank,255);self.spin()
            self.read(bank+2,self.devices.get(bank,(255,0,0))[0]);self.iflag=0x200
            status,left,right=self.devices.get(bank,(255,0,0))
            if status!=1:continue
            self.read(bank+4,left);self.bl=left;self.read(bank+6,right)
            if ((left&right)==255)!=(kind==3):continue
            if kind==3:
                self.iflag=0;v=self.read(0xA460,p['config_second'] if p['config_second'] is not None else self.config)
                self.out(0x5F,v);self.out(0xA460,(v&0xFC)|1)
                v=self.read(0xA66E,p['config2']);self.out(0x5F,v);self.out(0xA66E,v&0xFE)
                if has:self.out(0x6E,1)
                self.iflag=0x200
            self.found(bank);return True
        self.failed();return False
    def ram(self):
        setup=((0,1),(0x10,0x17),(0x10,0x80),(0,0x60),(1,2),(12,255),(13,255),(2,255),(3,31),(4,255),(5,255))
        for i,v in setup:self.regwrite(i,v)
        p=self.p
        for index,value in enumerate(PATTERN):
            self.iflag=0;self.read(self.port+4,p['noise']);self.idle(self.port+4,'write_idle')
            self.out(self.port+4,8);self.spin();self.out(self.port+6,value);self.iflag=0x200
            self.read(self.port+4,p['noise'])
            if index==p['timeout_index']:
                for _ in range(10000):self.read(self.port+4,0)
                self.regs.update(si=0x47D+index,cx=32-index,dx=self.port+4,bx=self.port+6)
                self.flags,self.mask=0x44,0x8C5
                return
            for _ in range(p['busy']):self.read(self.port+4,0)
            self.read(self.port+4,8);self.read(self.port+4,p['noise'])
            self.point('write_complete')
            for _ in range(p['busy']):self.read(self.port+4,0x80);self.read(self.port+4,p['noise'])
            self.read(self.port+4,8)
            self.iflag=0;self.out(self.port+4,16);self.spin();self.out(self.port+6,128);self.iflag=0x200
        for i,v in ((16,0),(16,128),(0,1)):self.regwrite(i,v)
        for i,v in ((0,1),(16,0),(16,128),(0,32),(1,2),(12,255),(13,255),(2,255),(3,31),(4,255),(5,255)):self.regwrite(i,v)
        for value in p['dummy_values']:
            self.iflag=0;self.idle(self.port+4,'dummy_idle');self.out(self.port+4,8);self.spin()
            self.read(self.port+6,value);self.iflag=0x200;self.regwrite(16,128)
        for index,value in enumerate(PATTERN):
            self.iflag=0;self.idle(self.port+4,'read_idle');self.out(self.port+4,8)
            self.read(self.port+4,p['noise'])
            self.point('read_ready')
            for _ in range(p['busy']):self.read(self.port+4,0)
            self.read(self.port+4,8);self.read(self.port+4,p['noise']);self.idle(self.port+4,'read_data')
            if index==p['mismatch_index']:value^=p['mismatch_mask']
            self.read(self.port+6,value);self.iflag=0x200;self.store(0x4A8+index,1,value)
            self.regwrite(16,128)
        self.regwrite(0,1)
        count=p['mismatch_index']+1 if p['mismatch_index']>=0 else 32
        self.regs.update(si=0x47C+count,di=0x4A8+count,cx=32-count,dx=1,bx=0x1FFF)
        self.mask=0x8D5
        if p['mismatch_index']>=0:
            v=PATTERN[p['mismatch_index']];self.flags=arith(v,v^p['mismatch_mask'],subtract=True)&~1
        else:
            self.flags=arith(self.result,2);self.result+=2;self.store(0x49D,1,self.result)
    def run(self):
        p=self.p;self.store(0x4A7,1,0)
        raw=bytes((p['length_byte'],))+p['tail']+b'\r';index=0
        while raw[index]==32:index+=1
        priority=raw[index]==56
        if priority:self.store(0x4A7,1,1)
        self.scan_si=0x81+index
        self.regs.update(ds=self.regs['cs'],es=0xFD80,si=self.scan_si,cx=0)
        found=False
        for kind in ((2,3) if priority else (3,2)):
            if self.detector(kind):found=True;break
        if found:
            self.regs['es']=self.regs['cs'];self.ram()
        else:
            self.result=1;self.store(0x49D,1,1)
            banks=(0x88,0x188,0x288,0x388) if p['override']==255 else ((p['override']<<8)|0x88,)
            for bank in banks:
                self.iflag=0;self.spin();self.out(bank,11);self.spin();self.out(bank+2,170);self.spin()
                value=self.read(bank+2,170 if bank==p['fallback'] else 255);self.iflag=0x200
                if value==170:
                    self.found(bank);self.regs['dx']=bank+6
                    self.flags,self.mask=arith(bank+4,2,16),0x8D5
                    break
            else:
                self.failed();self.regs['dx']=banks[-1];self.flags,self.mask=0x45,0x8D5
            self.regs['bx']=(self.regs['bx']&0xFF00)|self.bl
        self.regs['ax']=0x4C00|self.result
        self.flags=(self.flags&~0x600)|self.iflag
        self.events.append(('exit',0x21,0x4C00|self.result))
        return self

class Machine:
    def __init__(self,image,load):
        need(len(image)==926,'complete inner COM');self.load=load;self.base=load*16
        self.u=Uc(UC_ARCH_X86,UC_MODE_16);self.u.mem_map(0,1<<20)
        initial=bytearray(b'\xA5'*(1<<20));initial[self.base+0x100:self.base+0x49E]=image;self.initial=bytes(initial)
        ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image[:892],0x100))
        need(sum(i.size for i in ins)==892,'complete instruction boundaries')
        self.instructions={i.address:i.size for i in ins};self.owned=set(range(0x100,0x47C));self.covered=set();self.maximum_stack=0
        self.fast_spins={i.address for i in ins if i.address in SPINS and i.mnemonic=='loop' and i.op_str==hex(i.address)}
        self.hooks=[self.u.hook_add(UC_HOOK_CODE,self.code),self.u.hook_add(UC_HOOK_MEM_WRITE,self.write),self.u.hook_add(UC_HOOK_INTR,self.interrupt),
            self.u.hook_add(UC_HOOK_INSN,self.input,None,1,0,UC_X86_INS_IN),self.u.hook_add(UC_HOOK_INSN,self.output,None,1,0,UC_X86_INS_OUT)]
    def close(self):
        for h in self.hooks:self.u.hook_del(h)
        self.hooks=[];self.u=None
    def r(self,n):return self.u.reg_read(REG[n])&65535
    def regs(self):return {n:self.r(n) for n in REG if n!='ip'}
    def fail(self,error):self.error=str(error);self.u.emu_stop()
    def event(self,event):
        need(self.index<len(self.expected.events) and event==self.expected.events[self.index],
             f'event {self.index}: {event}; expected {self.expected.events[self.index:self.index+1]}')
        self.index+=1
    def code(self,u,address,size,_):
        try:
            ip=address-self.base
            if self.spin is not None and ip==self.spin[0] and ip in self.fast_spins:
                # The immutable self-LOOP has no stores or stack effects. Its
                # first visit recorded coverage/depth; every actual native CX
                # decrement remains checked, with flags checked at loop exit.
                at,left,flags=self.spin
                need(self.r('cx')==left-1 and left>1,'complete LOOP decrement')
                self.spin=(at,left-1,flags)
                return
            if self.hold:
                head,cycle,depth=LOOPS[self.hold]
                if self.holding:
                    need(ip in cycle,'held device reply stays in the proved native polling cycle')
                    if ip==head:
                        self.hold_rounds+=1
                        if self.hold_rounds==5:self.stalled=True;u.emu_stop();return
                elif ip==head:
                    need(self.index==self.expected.loop_points[self.hold],'independent first polling transaction boundary')
                    need(self.r('sp')==self.stack-depth,'independent live polling frame depth')
                    self.holding=True;self.hold_index=self.index;self.hold_rounds=0
            if self.spin is not None:
                at,left,flags=self.spin
                if ip==at:
                    need(self.r('cx')==left-1 and left>1,'complete LOOP decrement');self.spin=(at,left-1,flags)
                else:
                    need(left==1 and self.r('cx')==0,'all 100 native spin iterations')
                    need(u.reg_read(UC_X86_REG_EFLAGS)&0xED5==flags,'LOOP preserves flags/IF/DF');self.spin=None
            if self.call is not None and ip==self.call['return']:
                c=self.call;need(self.r('sp')==c['sp']+2,'real near register-write frame')
                need(u.reg_read(GPRS['sp'])==c['full']['sp']+2,'register-write preserves ESP high half')
                need(all(u.reg_read(GPRS[n])==v for n,v in c['full'].items() if n!='sp'),'register-write preserves DWORD caller registers')
                need(all(self.r(n)==c['regs'][n] for n in ('cs','ds','es','ss')),'register-write preserves segments')
                need(u.reg_read(UC_X86_REG_EFLAGS)&0xED5==c['flags'],'register-write restores incoming defined flags/IF/DF')
                self.call=None;self.register_calls+=1
            if ip in SPINS and self.spin is None:
                self.event(('spin',100));need(self.r('cx')==100,'literal 100-iteration spin input')
                self.spin=(ip,100,u.reg_read(UC_X86_REG_EFLAGS)&0xED5);self.spin_calls+=1
            if ip==0x455:
                need(self.call is None,'register-write helper is not recursive');self.event(('reg',self.r('dx')))
                sp=self.r('sp');ret=int.from_bytes(u.mem_read(self.ss*16+sp,2),'little')
                need(ret in self.instructions,'real maintained near caller')
                self.call=dict(return_=ret,sp=sp,full={n:u.reg_read(v) for n,v in GPRS.items()},regs=self.regs(),flags=u.reg_read(UC_X86_REG_EFLAGS)&0xED5)
                self.call['return']=self.call.pop('return_')
            need(self.instructions.get(ip)==size,'only selected complete owner instructions')
            self.covered.update(range(ip,ip+size));self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
        except Exception as e:self.fail(e)
    def write(self,u,access,address,size,value,_):
        try:
            lo=self.ss*16+self.stack-48;hi=self.ss*16+self.stack
            if lo<=address and address+size<=hi:
                self.maximum_stack=max(self.maximum_stack,hi-address);return
            self.event(('store',address,size,value))
        except Exception as e:self.fail(e)
    def input(self,u,port,size,_):
        try:
            if self.holding:
                e=self.expected.events[self.hold_index];f=u.reg_read(UC_X86_REG_EFLAGS)
                need((port,size,f&0x200,f&0x400)==(e[1],1,e[4],0),'bounded held port/width/IF/DF')
                self.reads+=1;return 0 if self.hold=='read_ready' else 0x80
            need(self.index<len(self.expected.events),'complete finite device input')
            e=self.expected.events[self.index];need(e[0]=='in','only predicted IN requests')
            value=e[3];f=u.reg_read(UC_X86_REG_EFLAGS)
            self.event(('in',port,size,value,f&0x200,f&0x400));self.reads+=1
            return value
        except Exception as e:self.fail(e);return 0
    def output(self,u,port,size,value,_):
        try:
            f=u.reg_read(UC_X86_REG_EFLAGS);self.event(('out',port,size,value,f&0x200,f&0x400))
        except Exception as e:self.fail(e)
    def interrupt(self,u,vector,_):
        try:self.event(('exit',vector,self.r('ax')));self.returned=True;u.emu_stop()
        except Exception as e:self.fail(e)
    def run(self,*,boards=(),board_replies=None,fallback=None,override=None,rom_word=0,rom_version=6,
            config=None,config_second=None,config2=255,tail=b'',length_byte=None,busy=0,noise=0xA7,
            mismatch_index=-1,mismatch_mask=1,timeout_index=-1,dummy_values=(0xC3,0x5A),
            seed=0x1357,flags=0x602,stack=0xFFF0,ss=0x7000,hold=None):
        need((override is None or 0<=override<=255) and 0<=rom_word<=65535 and 0<=rom_version<=255,'BYTE override/version and WORD ROM signature')
        need(isinstance(tail,bytes) and len(tail)<=126 and flags in (2,0x202,0x402,0x602,0xED7),'raw bounded PSP bytes / flags')
        need(0<=busy<=3 and 0<=noise<=255 and -1<=mismatch_index<32 and 1<=mismatch_mask<=255 and -1<=timeout_index<32,'finite device waits and RAM response fixtures')
        need(hold is None or hold in LOOPS and busy==0 and timeout_index==-1 and mismatch_index==-1,'explicit first-transaction nonterminal device reply')
        need(48<=stack<=0xFFF0 and ss in (0x7000,0x8000),'bounded disjoint private stack')
        p=dict(boards=boards,board_replies=board_replies or {},fallback=fallback,override=255 if override is None else override,rom_word=rom_word,rom_version=rom_version,
            config=config,config_second=config_second,config2=config2,tail=tail,length_byte=len(tail) if length_byte is None else length_byte,
            busy=busy,noise=noise,mismatch_index=mismatch_index,mismatch_mask=mismatch_mask,timeout_index=timeout_index,dummy_values=dummy_values)
        need(0<=p['length_byte']<=255 and all(0<=v<=255 for v in dummy_values) and len(dummy_values)==2,'raw PSP count / dummy device bytes')
        need(all(k in (2,3) and port&255==0x88 and 0<=port<=65535 for port,k in boards),'bounded explicit device profile')
        need(all(0<=v<=255 for v in (config2,*[v for v in (config,config_second) if v is not None])),'BYTE configuration replies')
        memory=bytearray(self.initial);memory[self.base+0x80:self.base+0x82+len(tail)]=bytes((p['length_byte'],))+tail+b'\r'
        if override is not None:memory[self.base+0x49C]=override
        memory[0xFD802:0xFD806]=struct.pack('<HH',rom_word,rom_version)
        memory[self.base+0x49E:self.base+0x4C8]=bytes((seed+i*17)&255 for i in range(42))
        memory[ss*16+stack:ss*16+stack+4]=b'\x5C\xA7\x69\xC3';self.u.mem_write(0,bytes(memory))
        regs={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)};regs.update(sp=stack,cs=self.load,ds=seed,es=seed^0x3456,ss=ss)
        high={n:(seed^0x5AA5)<<16 for n in GPRS}
        for n in GPRS:self.u.reg_write(GPRS[n],high[n]|regs[n])
        for n in ('cs','ds','es','ss'):self.u.reg_write(REG[n],regs[n])
        self.u.reg_write(UC_X86_REG_EFLAGS,flags)
        self.expected=Prediction(regs,flags,p).run();self.ss,self.stack=ss,stack
        selected_events=self.expected.events if hold is None else self.expected.events[:self.expected.loop_points[hold]]
        for e in selected_events:
            if e[0]=='store':_,at,size,value=e;memory[at:at+size]=value.to_bytes(size,'little')
        self.index,self.error,self.returned,self.spin,self.call=0,None,False,None,None
        self.hold,self.holding,self.stalled,self.hold_rounds=hold,False,False,0
        self.reads,self.spin_calls,self.register_calls=0,0,0
        try:self.u.emu_start(self.base+0x100,0x100000,count=250000)
        except UcError as e:raise ValueError('ONGCHK contract: guest fault') from e
        need(self.error is None,self.error or 'guest error')
        if hold is not None:
            need(self.stalled and not self.returned and self.index==self.expected.loop_points[hold] and self.spin is None,
                 'bounded nonterminal prefix, never a DOS exit')
            # Independent first-byte/first-register protocol states. Only AL and
            # defined logic flags can change in any of these closed polling loops.
            want=dict(regs,ax=(self.load&0xFF00)|(0 if hold=='read_ready' else 0x80),
                ds=self.load,es=self.load,dx=self.expected.port+4,sp=stack-LOOPS[hold][2])
            if hold=='register':want.update(bx=1,cx=0,si=self.expected.scan_si)
            elif hold in ('write_idle','write_complete'):
                want.update(bx=self.expected.port+6,cx=32,si=0x47C+int(hold=='write_complete'))
            elif hold=='dummy_idle':want.update(bx=0x1FFF,cx=0,si=0x49C)
            else:want.update(bx=0x1FFF,cx=32,si=0x49C,di=0x4A8)
            need(self.regs()==want,'independent live WORD/segment polling registers: '+str((self.regs(),want)))
            need(all(self.u.reg_read(GPRS[n])==high[n]|want[n] for n in GPRS),'live polling DWORD high halves')
            f=self.u.reg_read(UC_X86_REG_EFLAGS);value=0 if hold=='read_ready' else 0x80
            logic=(4 if value.bit_count()%2==0 else 0)|(64 if value==0 else 0)|(value&128)
            e=self.expected.events[self.hold_index]
            need(f&0x8C5==logic and f&0x600==e[4],'held-loop defined logic flags / IF / DF')
            need(self.reads==sum(e[0]=='in' for e in selected_events)+5*(2 if hold=='write_complete' else 1)
                 and self.spin_calls==sum(e[0]=='spin' for e in selected_events)
                 and self.register_calls==sum(e[0]=='reg' for e in selected_events)-int(hold=='register'),
                 'complete independent prefix polls / spins / actual register-write returns')
            actual=bytes(self.u.mem_read(0,1<<20));lo=ss*16+stack-48;hi=ss*16+stack;memory[lo:hi]=actual[lo:hi]
            need(actual==memory,'complete nonterminal-prefix physical memory outside private stack')
            return dict(nonterminal=True,held_loop=hold,rounds=self.hold_rounds,registers=self.regs(),flags=f&0xEC5,
                protocol_prefix_sha256=hashlib.sha256(json.dumps(selected_events).encode()).hexdigest())
        need(self.returned and self.index==len(self.expected.events) and self.spin is None and self.call is None,'complete terminal protocol and native frames')
        need(self.regs()==self.expected.regs,'independent whole WORD/segment terminal registers: '+str((self.regs(),self.expected.regs)))
        need(all(self.u.reg_read(GPRS[n])==high[n]|self.expected.regs[n] for n in GPRS),'all returning DWORD high halves including ESP')
        f=self.u.reg_read(UC_X86_REG_EFLAGS);mask=self.expected.mask
        need(f&mask==self.expected.flags&mask and f&0x600==self.expected.flags&0x600,'independent defined terminal flags / IF / DF')
        actual=bytes(self.u.mem_read(0,1<<20));lo=ss*16+stack-48;hi=ss*16+stack;memory[lo:hi]=actual[lo:hi]
        need(actual==memory,'all physical memory outside 48 private stack bytes, including retained caller count')
        need(self.reads==self.expected.polls and self.spin_calls==self.expected.spins and self.register_calls==self.expected.calls,'all real device polls / spin loops / register-write returns')
        return dict(result=self.expected.result,registers=self.regs(),flags=f&(mask|0x600),flags_mask=mask,
            polls=self.reads,spin_calls=self.spin_calls,register_write_calls=self.register_calls,
            protocol_sha256=hashlib.sha256(json.dumps(self.expected.events).encode()).hexdigest())

def cases():
    for value in range(256):
        for kind in (2,3):
            bank=((value<<8)|0x88) if value!=255 else (0x88 if kind==2 else 0x188)
            yield dict(boards=((bank,kind),),override=value,config=7)
        for priority in (False,True):
            yield dict(boards=((0x88,2),(0x188,3)),rom_word=0x2A27,rom_version=value,
                       tail=b'x'*56 if priority else b'')
        yield dict(boards=((0x188,3),),config=value,config_second=value^255)
        yield dict(boards=((0x188,3),),rom_word=0x2A27,config2=value)
        yield dict(boards=((0x88,2),(0x188,3)),tail=b' '*7+b'8',length_byte=value)
        yield dict(boards=((0x88,2),(0x188,3)),tail=bytes((value,))+b'x'*31,length_byte=32)
        yield dict(board_replies={0x188:(1,value,255)},config=7)
        yield dict(board_replies={0x188:(1,255,value)},config=7)
        yield dict(board_replies={0x188:(value,255,255)},config=7)
        yield dict(boards=((0x88,2),(0x188,3)),rom_word=0x2A00|value,rom_version=5)
        yield dict(boards=((0x88,2),(0x188,3)),rom_word=(value<<8)|0x27,rom_version=5)
    for count in range(127):
        yield dict(boards=((0x88,2),(0x188,3)),tail=b'x'*count)
    for kind,bank in ((2,0x88),(3,0x188)):
        for index in range(32):
            for mask in (1,0x80,255):
                yield dict(boards=((bank,kind),),mismatch_index=index,mismatch_mask=mask)
            yield dict(boards=((bank,kind),),timeout_index=index)
        for bank in (0x88,0x188,0x288,0x388):
            yield dict(boards=((bank,kind),))
            yield dict(boards=((bank,kind),),override=bank>>8)
    for bank in (0x88,0x188,0x288,0x388,0xFE88):
        yield dict(fallback=bank,override=None if bank<0x400 else 254)
    yield dict(boards=((0x188,3),),tail=b'x'*56)
    yield dict(tail=b'x'*56)
    yield dict(fallback=0x288,tail=b'x'*56)
    yield dict(boards=((0x588,3),),override=5,tail=b'x'*56)
    yield dict(boards=((0x88,2),),tail=b' '*32)
    for seed in (0,0x1357,0xFFFF):
        for flags in (2,0x202,0x402,0x602,0xED7):
            for ss in (0x7000,0x8000):
                for profile in ({},{'fallback':0x388},{'boards':((0x188,3),),'busy':2},
                                {'boards':((0x88,2),),'timeout_index':31}):
                    yield dict(profile,seed=seed,flags=flags,ss=ss,noise=seed&255)
                for hold in LOOPS:yield dict(boards=((0x188,3),),hold=hold,seed=seed,flags=flags,ss=ss)

def verify(target,candidate):
    results=[]
    for image in (target,candidate):
        rows=[]
        for load in (0x1000,0x3000):
            m=Machine(image,load);trace=hashlib.sha256();terminal=nonterminal=0;maxpoll=maxspin=maxreg=0
            try:
                for count,p in enumerate(cases(),1):
                    q=dict(seed=0x1357 if count&1 else 0xECA8,stack=0x80 if count&1 else 0xFFF0);q.update(p)
                    r=m.run(**q)
                    if r.get('nonterminal'):nonterminal+=1
                    else:
                        terminal+=1;maxpoll=max(maxpoll,r['polls']);maxspin=max(maxspin,r['spin_calls']);maxreg=max(maxreg,r['register_write_calls'])
                    trace.update(json.dumps(r,sort_keys=True).encode())
                need(m.covered==m.owned,'all 892 actual instruction bytes execute')
                rows.append(dict(load_segment=load,cases=count,terminal_cases=terminal,nonterminal_cases=nonterminal,
                    covered_owner_bytes=len(m.covered),maximum_observed_stack_depth=m.maximum_stack,
                    maximum_polls=maxpoll,maximum_spin_calls=maxspin,maximum_actual_register_write_calls=maxreg,
                    trace_sha256=trace.hexdigest()))
            finally:m.close()
        results.append(rows)
    need(results[0]==results[1],'independent target/native complete observations agree')
    return dict(images=2,source_extents=1,entry_points=10,code_bytes=892,data_bytes=34,bss_bytes=42,
        executed_owner_bytes=892,cases_per_image=sum(r['cases'] for r in results[0]),observations=results[0],
        exhaustive_BYTE_domains=256,maximum_private_stack_window=48,held_native_polling_cycles=len(LOOPS),
        all_nested_helpers_executed=True,spin_iterations_executed=True,physical_timing_or_devices_emulated=False)

def negative_controls(target):
    controls=(
        ('startup-CLD',0x100,1,dict(flags=0x602)),('startup-DS-from-CS',0x104,8,{}),
        ('PSP-count-byte-address',0x10D,1,dict(tail=b'x'*56,boards=((0x88,2),(0x188,3)))),
        ('PSP-priority-character',0x115,1,dict(tail=b'x'*56,boards=((0x88,2),(0x188,3)))),
        ('type2-first-dispatch',0x12C,1,dict(tail=b'x'*56,boards=((0x88,2),(0x188,3)))),
        ('FM-echo-value',0x16D,1,dict(fallback=0x188)),('FM-echo-spin-count',0x15D,1,{}),
        ('FM-bank-step',0x189,1,dict(fallback=0x388)),('RAM-result-increment',0x19D,1,dict(boards=((0x188,3),))),
        ('type3-result-code',0x1A4,1,dict(boards=((0x188,3),))),
        ('ROM-word-signature',0x1B4,1,dict(boards=((0x88,2),(0x188,3)),rom_word=0x2A27,rom_version=5)),
        ('ROM-version-bound',0x1C2,1,dict(boards=((0x188,3),),rom_word=0x2A27,rom_version=6)),
        ('type3-config-mask',0x1D6,1,dict(boards=((0x188,3),))),
        ('override-sentinel',0x1E1,1,dict(boards=((0x188,3),))),
        ('type3-CLI',0x1EA,1,dict(boards=((0x188,3),))),
        ('type3-aux-pair',0x20C,2,dict(boards=((0x188,3),))),
        ('config-commit-bit',0x22D,1,dict(boards=((0x188,3),))),
        ('secondary-config-mask',0x236,1,dict(boards=((0x188,3),))),
        ('ROM-control-port',0x242,1,dict(boards=((0x188,3),),rom_word=0x2A27)),
        ('type2-result-code',0x24B,1,dict(boards=((0x88,2),))),
        ('type2-aux-predicate',0x2B6,1,dict(boards=((0x88,2),))),
        ('failure-result-byte',0x2E1,1,{}),('failure-carry',0x2E2,1,{}),
        ('port-table-WORD',0x2C2,1,dict(boards=((0x188,3),))),
        ('RAM-write-transfer-count',0x344,1,dict(boards=((0x188,3),))),
        ('RAM-write-register',0x356,1,dict(boards=((0x188,3),))),
        ('RAM-write-STI',0x363,1,dict(boards=((0x188,3),))),
        ('RAM-write-timeout-count',0x368,1,dict(boards=((0x188,3),),timeout_index=0)),
        ('RAM-write-ready-mask',0x36D,8,dict(boards=((0x188,3),))),
        ('RAM-write-timeout-carry',0x373,1,dict(boards=((0x188,3),),timeout_index=0)),
        ('RAM-write-complete-predicate',0x37A,1,dict(boards=((0x188,3),),busy=1)),
        ('RAM-reset-register',0x380,1,dict(boards=((0x188,3),))),
        ('RAM-reset-data',0x38D,1,dict(boards=((0x188,3),))),
        ('RAM-dummy-read-count',0x3F1,3,dict(boards=((0x188,3),))),
        ('RAM-read-transfer-count',0x3F4,1,dict(boards=((0x188,3),))),
        ('RAM-read-register',0x404,1,dict(boards=((0x188,3),))),
        ('RAM-read-ready-mask',0x409,8,dict(boards=((0x188,3),),busy=1)),
        ('RAM-read-STI',0x417,1,dict(boards=((0x188,3),))),
        ('RAM-compare-size',0x450,1,dict(boards=((0x188,3),))),
        ('register-write-preserve-flags',0x477,1,dict(boards=((0x188,3),))),
        ('register-write-port-WORD',0x45C,1,dict(boards=((0x188,3),))),
        ('DOS-result-load',0x123,1,dict(boards=((0x188,3),))),
        ('DOS-exit-vector',0x126,1,{}))
    rejected=[]
    for name,at,xor,p in controls:
        image=bytearray(target);image[at-0x100]^=xor;m=Machine(bytes(image),0x1000)
        try:m.run(**p)
        except (ValueError,UcError):rejected.append(name)
        else:raise ValueError('actual instruction mutation escaped: '+name)
        finally:m.close()
    static=[];consumed=[]
    for i in range(34):
        image=bytearray(target);image[892+i]^=1
        if bytes(image[892:])!=PATTERN+b'\xFF\0':static.append(i)
        if i==33:continue # The result initializer is overwritten before any read.
        m=Machine(bytes(image),0x1000)
        try:m.run(boards=((0x188,3),))
        except (ValueError,UcError):consumed.append(i)
        else:raise ValueError('actual consumed DATA mutation escaped: '+str(i))
        finally:m.close()
    return dict(instruction_mutations=len(rejected),instructions_rejected=rejected,
        static_initialized_DATA_mutations_rejected=len(static),actual_consumed_DATA_mutations=len(consumed),
        consumed_DATA_indices_rejected=consumed,static_DATA_controls_have_instruction_credit=False,
        result_initializer_is_consumed_before_store=False)
