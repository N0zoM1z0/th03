"""Whole OP startup with real primitive and existing same-CPU menu contracts.

Only existing borrowed callee private windows remain unconstrained. Native
caller frames and every byte outside those declared windows stay checked.
"""
import hashlib
import json
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import UcError,UC_HOOK_INSN
from unicorn import x86_const as x
from lib.op_startup_layout import START,SIZE
from lib.op_startup_state import State,REG,GPRS,ARITH,address,need
from lib.op_startup_primitives import Primitive,ENTRIES,LIBRARIES,NEAR_LIBRARIES,SAMPLES
from lib.op_startup_children import Main,Option
from lib.op_option_runtime import Machine as Base
from lib.op_attract_runtime import Machine as Attract
from lib.op_vs_runtime import Machine as VS
from lib.op_nested_context import Context
from lib.op_cfg_runtime import reply

BORROWED={'vs':0x9BDF,'wait':0x9E16,'main':0xA0E0,'option':0xA203}


class Prediction(Primitive):
    def __init__(self,*args):
        super().__init__(*args)
        self.held=False
        self.prefix=False
        self.iterations=0
        self.borrowed=[]

    def borrow(self,name,continuation):
        self.push(continuation)
        at=address(self.ss,self.r['sp'])
        mask=self.mask|0x600
        self.events.append(('borrow',name,self.full(),bytes(self.memory[at:at+2]).hex(),self.flags&mask,mask,continuation))
        result=yield name
        self.r=dict(result['registers'])
        self.high={n:result['full_registers'][n]&0xFFFF0000 for n in GPRS}
        self.flags,self.mask=result['flags'],result['flags_mask']
        self.memory=bytearray(result['memory'])
        self.file=bytearray(result['file'])
        self.held=result['held']
        self.borrowed.append(name)
        if not self.held:
            self.done(name)

    def run(self):
        self.enter()
        self.service('graph400',0xB1F)
        self.service('text_clear',0xB24)
        self.service('resident_create',0xB29)
        zoom=self.dg(0x2C8)
        self.op(zoom,0,True)
        if zoom:
            for offset,continuation in ((0x17E,0xB39),(0x1A8,0xB42),(0x1E8,0xB4B)):
                self.push(self.ds)
                self.push(offset)
                self.service('puts',continuation,4,(offset,self.ds))
            self.service('getch',0xB50)
        else:
            self.push(self.ds)
            self.push(0x225)
            self.call('init',0xB5B)
            self.r['sp']=self.op(self.r['sp'],4)
            self.logic(self.r['ax'])
            if self.r['ax']:
                self.push(self.ds)
                self.push(0x231)
                self.service('puts',0xB4B,4,(0x231,self.ds))
                self.service('getch',0xB50)
            else:
                self.service('gaiji_backup',0xB6D)
                self.push(self.ds)
                self.push(0x26C)
                self.service('gaiji_load',0xB76,4,(0x26C,self.ds))
                self.call('cfg_load',0xB79,far=False)
                if self.o['cfg_boundary']:
                    mask=self.mask|0x600
                    self.events.append(('cfg-boundary',self.full(),self.flags&mask,mask))
                    self.prefix=True
                    return
                self.les()
                mode=self.word(self.r['es'],self.r['bx']+0x28,1)
                self.op(mode,128,True,bits=8)
                if mode>=128:
                    demo=self.word(self.r['es'],self.r['bx']+0x39,1)
                    self.op(demo,0,True,bits=8)
                    if not demo:
                        self.service('cdg1',0xB8E,far=False)
                        self.service('cdg3',0xB91,far=False)
                        self.service('cdg2',0xB94,far=False)
                        yield from self.borrow('vs',0xB97)
                        if self.held:return
                self.les()
                fast=self.word(self.r['es'],self.r['bx']+0x37,1)
                self.op(fast,0,True,bits=8)
                if not fast:
                    self.service('animate',0xBA5,far=False)
                    self.les()
                    self.store(address(self.r['es'],self.r['bx']+0x37),1,1)
                else:
                    self.les()
                    self.store(address(self.r['es'],self.r['bx']+0x37),1,0)
                    self.service('fade',0xBBC,far=False)
                yield from self.borrow('wait',0xBBF)
                if self.held:return
                self.field(0x118C,0,1)
                self.field(0x1AA6,0)
                yield from self.borrow('main',0xBCD)
                if self.held:return
                self.service('cdg2',0xBD0,far=False)
                while True:
                    if self.o['loop_prefix'] and self.iterations==self.o['loop_prefix']:
                        need(self.dg(0x118C,1)==self.o['raw_dispatch'] and not self.dg(0x162,1),'live raw-dispatch invariant')
                        mask=self.mask|0x600
                        self.events.append(('loop-prefix',self.iterations,self.full(),self.flags&mask,mask))
                        self.prefix=True
                        return
                    quit=self.dg(0x162,1)
                    self.op(quit,0,True,bits=8)
                    if quit:
                        break
                    need(self.iterations<len(self.o['samples']),'finite startup input stream or explicit closed prefix')
                    self.o['sample']=self.o['samples'][self.iterations]
                    self.call('input',0xBD7)
                    raw=self.dg(0x118C,1)
                    self.r['ax']=raw if raw<128 else raw|0xFF00
                    self.logic(self.r['ax'])
                    if self.r['ax']==0:
                        yield from self.borrow('main',0xBE9)
                    else:
                        self.op(self.r['ax'],1,True)
                        if self.r['ax']==1:
                            yield from self.borrow('option',0xBEE)
                    if self.held:return
                    self.les()
                    at=address(self.r['es'],self.r['bx']+0x10)
                    value=int.from_bytes(self.memory[at:at+4],'little')
                    carry=self.flags&1
                    self.store(at,4,self.op(value,1,bits=32))
                    self.flags=(self.flags&~1)|carry
                    self.push(1)
                    self.call('delay',0xBFE)
                    self.iterations+=1
                self.call('cfg_exit',0xC08,far=False)
                self.service('gaiji_restore',0xC0D)
                self.service('text_clear',0xC12)
                self.call('exit_dos',0xC17)
                self.service('resident_free',0xC1C)
        self.pop('bp')
        self.returned()


class Machine(Base):
    def __init__(self,image,load):
        self.active_child=None
        super().__init__(image,load)
        self.image=image
        self.instructions={}
        self.owned=set(range(START,START+SIZE))
        self.covered=set()
        self.return_targets={}
        for start,size in [(START,SIZE),*[(a,n) for a,n,_ in ENTRIES.values()]]:
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[start:start+size],start))
            need(sum(i.size for i in rows)==size,'all startup and primitive instructions')
            self.instructions.update({i.address:i.size for i in rows})
            for i in rows:
                if i.mnemonic=='call':self.return_targets[i.address+i.size]=int(i.op_str,16)
                elif i.mnemonic=='lcall':
                    segment,offset=(int(v.strip(),16) for v in i.op_str.split(','))
                    self.return_targets[i.address+i.size]=segment*16+offset
        self.children={'main':Main(image,load),'option':Option(image,load),'wait':Attract(image,load),'vs':VS(image,load)}
        for child in self.children.values():
            for hook in child.hooks:child.uc.hook_del(hook)
            child.hooks=[]
            child.uc=self.uc
            if isinstance(child,Main):
                for nested in child.children.values():nested.uc=self.uc
        self.hooks.append(self.uc.hook_add(UC_HOOK_INSN,self.out,None,1,0,x.UC_X86_INS_OUT))

    def close(self):
        for child in self.children.values():
            if isinstance(child,Main):
                for nested in child.children.values():nested.uc=None
                child.children={}
            child.uc=None
        self.children={}
        super().close()

    def event(self,event):
        need(self.index<len(self.expected.events) and self.expected.events[self.index]==event,
             f'startup event{self.index}: {event}; expected {self.expected.events[self.index:self.index+1]}')
        self.index+=1

    def full(self):
        registers={n:self.uc.reg_read(r) for n,r in GPRS.items()}
        registers.update({n:self.r(n) for n in ('cs','ds','es','ss','fs','gs')})
        return registers

    def frame_event(self):
        if self.index<len(self.expected.events) and self.expected.events[self.index][0]=='far-frame':
            sp,ss=self.r('sp'),self.r('ss')
            ip,cs=struct.unpack('<HH',bytes(self.uc.mem_read(address(ss,sp),4)))
            self.event(('far-frame',address(ss,sp),ip,cs))

    def far_return(self,cleanup,far=True):
        sp,ss=self.r('sp'),self.r('ss')
        ip=self.uc.mem_read(address(ss,sp),2)
        cs=int.from_bytes(self.uc.mem_read(address(ss,sp)+2,2),'little') if far else self.r('cs')
        self.uc.reg_write(REG['sp'],sp+(4 if far else 2)+cleanup)
        self.uc.reg_write(REG['cs'],cs)
        self.uc.reg_write(REG['ip'],int.from_bytes(ip,'little'))

    def code(self,uc,at,size,user):
        if self.active_child is not None:
            self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
            self.active_child.code(uc,at,size,user)
            return
        try:
            offset=at-self.base
            if at==self.base+0xFFFF:
                self.returned=True
                uc.emu_stop()
                return
            self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
            event=self.expected.events[self.index] if self.index<len(self.expected.events) else None
            entries={a:k for k,(a,_,_) in ENTRIES.items()}
            if offset in entries or offset in LIBRARIES or offset in NEAR_LIBRARIES or offset in SAMPLES:
                self.frame_event()
            event=self.expected.events[self.index] if self.index<len(self.expected.events) else None
            target=self.return_targets.get(offset)
            name=next((k for k,v in ENTRIES.items() if v[0]==target),None)
            if name is None:name=next((k for k,v in BORROWED.items() if v==target),None)
            if event and event[:2]==('owned-return',name):
                mask=event[-1]
                self.event(('owned-return',name,self.full(),uc.reg_read(x.UC_X86_REG_EFLAGS)&mask,mask))
                event=self.expected.events[self.index] if self.index<len(self.expected.events) else None
            if event and event[0]=='loop-prefix' and offset==0xA4FE:
                mask=event[-1]
                self.event(('loop-prefix',event[1],self.full(),uc.reg_read(x.UC_X86_REG_EFLAGS)&mask,mask))
                self.prefix_stopped=True
                uc.emu_stop()
                return
            if event and event[0]=='cfg-boundary' and offset==0xA479:
                mask=event[-1]
                self.event(('cfg-boundary',self.full(),uc.reg_read(x.UC_X86_REG_EFLAGS)&mask,mask))
                self.cfg_stopped=True
                uc.emu_stop()
                return
            if offset in entries:
                need(event is not None and event[:2]==('entry',entries[offset]),'actual expected primitive entry '+hex(offset)+' '+str(event))
                mask=event[-1]
                frame=bytes(uc.mem_read(address(self.r('ss'),self.r('sp')),ENTRIES[entries[offset]][2])).hex()
                self.event(('entry',entries[offset],self.full(),frame,uc.reg_read(x.UC_X86_REG_EFLAGS)&mask,mask))
            if offset in BORROWED.values():
                need(event and event[0]=='borrow' and BORROWED[event[1]]==offset,'actual expected borrowed near entry')
                _,name,_,frame,_,mask,continuation=event
                actual=bytes(uc.mem_read(address(self.r('ss'),self.r('sp')),2)).hex()
                self.event(('borrow',name,self.full(),actual,uc.reg_read(x.UC_X86_REG_EFLAGS)&mask,mask,continuation))
                need(bytes(uc.mem_read(0,1<<20))==self.expected.memory,'all independent caller input before borrowed callee')
                self.pending=event
                uc.emu_stop()
                return
            if offset in LIBRARIES or offset in NEAR_LIBRARIES:
                event=self.expected.events[self.index]
                _,name,_,frame,_,mask,cleanup,far,count=event
                actual_name=LIBRARIES[offset][0] if offset in LIBRARIES else NEAR_LIBRARIES[offset]
                need(name==actual_name and far==(offset in LIBRARIES),'bounded library entry/ABI identity')
                actual=bytes(uc.mem_read(address(self.r('ss'),self.r('sp')),len(bytes.fromhex(frame)))).hex()
                self.event(('service',name,self.full(),actual,uc.reg_read(x.UC_X86_REG_EFLAGS)&mask,mask,cleanup,far,count))
                if name=='read':
                    amount,off,seg=struct.unpack('<HHH',bytes.fromhex(frame)[4:10])
                    raw=self.o['cfg'][:min(amount,self.o['read_bytes'])]
                    if raw:
                        dest=address(seg,off)
                        self.event(('file-bytes',dest,raw.hex()))
                        uc.mem_write(dest,raw)
                elif name=='write':
                    amount,off,seg=struct.unpack('<HHH',bytes.fromhex(frame)[4:10])
                    raw=bytes(uc.mem_read(address(seg,off),amount))
                    self.event(('file-write',raw.hex()))
                    self.file[:amount]=raw
                if name=='cdg2' and int.from_bytes(bytes.fromhex(frame)[:2],'little')==0xBD0 and self.o['raw_dispatch'] is not None:
                    dest=self.data+0x118C
                    self.event(('surface-write',dest,self.o['raw_dispatch']))
                    uc.mem_write(dest,bytes([self.o['raw_dispatch']]))
                values,flags=reply(self.registers(),count,self.seed,uc.reg_read(x.UC_X86_REG_EFLAGS),self.o['assign'] if name=='assign' else self.status)
                for n in ('ax','bx','cx','dx','es'):uc.reg_write(REG[n],values[n])
                uc.reg_write(x.UC_X86_REG_EFLAGS,flags)
                self.far_return(cleanup,far)
                return
            if offset in SAMPLES:
                kind=SAMPLES[offset]
                event=self.expected.events[self.index]
                _,_,_,_,mask,count=event
                self.event(('sample',kind,self.full(),uc.reg_read(x.UC_X86_REG_EFLAGS)&mask,mask,count))
                sample=self.o['samples'][self.loop_count]
                values=((0x1AA6,sample[0]),(0x1AA2,sample[1]),(0x1AA4,sample[2]),(0x11B4,0)) if kind=='sense' else ((0x11B4,sample[3]),)
                for off,value in values:
                    dest=self.data+off
                    self.event(('sample-write',dest,value))
                    uc.mem_write(dest,value.to_bytes(2,'little'))
                result,flags=reply(self.registers(),count,self.seed,uc.reg_read(x.UC_X86_REG_EFLAGS),self.status)
                for n in ('ax','bx','cx','dx','es'):uc.reg_write(REG[n],result[n])
                uc.reg_write(x.UC_X86_REG_EFLAGS,flags)
                self.far_return(0)
                return
            if offset==0xC1A7:
                event=self.expected.events[self.index]
                need(event[0]=='tick','explicit counter read event')
                self.event(event)
                uc.mem_write(self.data+0x11E8,event[1].to_bytes(2,'little'))
            if offset==0xA4FE and self.loop_started:
                self.loop_count+=1
                self.loop_started=False
            if offset==0xA4D2:self.loop_started=True
            need(self.instructions.get(offset)==size,'only actual startup/primitive instructions: '+hex(offset))
            self.covered.update(set(range(offset,offset+size))&self.owned)
        except Exception as error:
            self.fail(error)

    def write(self,uc,access,at,size,value,user):
        if self.active_child is not None:
            self.active_child.write(uc,access,at,size,value,user)
            return
        try:
            if self.index<len(self.expected.events) and self.expected.events[self.index][0]=='far-frame':
                _,dest,ip,cs=self.expected.events[self.index]
                need(size==2 and (at,value) in ((dest,ip),(dest+2,cs)),'only real far return words')
                return
            self.event(('store',at,size,value))
        except Exception as error:
            self.fail(error)

    def interrupt(self,uc,vector,user):
        if self.active_child is not None:
            self.active_child.interrupt(uc,vector,user)
            return
        try:
            event=self.expected.events[self.index]
            _,_,_,mask,count=event
            need(vector==0x60 and self.r('ax')>>8==9,'actual driver query')
            self.event(('driver',self.full(),uc.reg_read(x.UC_X86_REG_EFLAGS)&mask,mask,count))
            values,flags=reply(self.registers(),count,self.seed,uc.reg_read(x.UC_X86_REG_EFLAGS),self.status)
            for n in ('bx','cx','dx','es'):uc.reg_write(REG[n],values[n])
            uc.reg_write(REG['ax'],(values['ax']&0xFF00)|self.o['driver'])
            uc.reg_write(x.UC_X86_REG_EFLAGS,flags)
        except Exception as error:
            self.fail(error)

    def out(self,uc,port,size,value,user):
        if self.active_child is not None:
            need(hasattr(self.active_child,'out'),'no unexpected port in borrowed option')
            self.active_child.out(uc,port,size,value,user)
            return
        try:self.event(('out',port,size,value,uc.reg_read(x.UC_X86_REG_EFLAGS)&0x200))
        except Exception as error:self.fail(error)

    def run_child(self,event):
        _,name,_,_,flags,mask,continuation=event
        child=self.children[name]
        regs=dict(self.expected.r)
        full=self.expected.full()
        context=Context(bytearray(self.expected.memory),regs,{n:full[n] for n in GPRS},flags,mask,
                        regs['sp'],self.cs*16+continuation,bytes(self.expected.file))
        self.active_child=child
        try:
            options=dict(self.o,driver_ax=self.o['driver_ax'],vs_samples=self.o['vs_samples'],wait_samples=self.o['wait_samples'])
            if name in ('main','option'):
                row=child.run_context(context,options)
            elif name=='wait':
                row=child.run(samples=self.o['wait_samples'],seed=self.seed,status=self.status,_context=context)
            else:
                _,_,res=context.resident(child)
                row=child.run(selection_ax=self.o['selection_ax'],samples=() if context.memory[res+0x28]>=128 else self.o['vs_samples'],
                    seed=self.seed,status=self.status,_context=context)
            result=child.contract_result
            need(result is not None,'independently accepted borrowed result')
            self.file=bytearray(result['file'])
            self.child_rows.append(dict(name=name,observation=row))
            return result
        finally:
            self.active_child=None

    def run(self,*,zoom=0,assign=0,mode=0,demo=0,fast=0,quit=0,midi=0,driver=0,present=0,random=0x12345678,
            cfg=b'\x02\x01\x03\x48\x57\x00\x50\xA7',read_bytes=8,samples=((0x1000,0,0,0),),
            wait_samples=((1,0,0,0),),vs_samples=((0x20,0,0,0),),selection_ax=1,selected_char=1,
            raw_dispatch=None,loop_prefix=0,cfg_boundary=False,seed=0x1357,status=0xFFFF,flags=0x202,stack=0xF800):
        options=dict(locals())
        options.pop('self')
        need(all(0<=v<=255 for v in (mode,demo,fast,quit,midi,driver,selected_char)),'BYTE startup/resident fields')
        need(0<=zoom<=65535 and 0<=assign<=65535 and len(cfg)==8 and 0<=read_bytes<=8,'WORD setup and eight-byte cfg')
        need(0x100<=stack<=0xFFF0 and flags in (2,0x202,0x402,0xED7),'inherited mapped callee stack and IF/DF profiles')
        need(raw_dispatch is None or raw_dispatch in range(256),'raw unchecked dispatch BYTE')
        need(not loop_prefix or loop_prefix in (1,3,7) and raw_dispatch not in (None,0,1) and not quit,'conditional raw-dispatch loop')
        memory=bytearray(self.initial)
        def put(seg,off,value,size=1):
            at=address(seg,off)
            memory[at:at+size]=value.to_bytes(size,'little')
        segment=int.from_bytes(cfg[5:7],'little')
        need(segment in (0x5000,0x6000),'existing disjoint resident context profile')
        put(self.ds,0x2464,segment<<16,4)
        for offset,value in ((0x28,mode),(0x39,demo),(0x37,fast)):
            put(segment,offset,value)
        put(segment,0x10,random,4)
        put(self.ds,0x2C8,zoom,2)
        put(self.ds,0x2CC,present,2)
        put(self.ds,0x1A0B,midi)
        for off,value in ((0x161,0),(0x162,quit),(0x163,0),(0x164,0),(0x165,0),(0x118A,0),(0x118B,0),(0x118C,0)):
            put(self.ds,off,value)
        put(self.ds,0x118E,0x5DD,2)
        put(0x7000,stack,0xFFFF,2)
        put(0x7000,stack+2,self.load,2)
        self.uc.mem_write(0,bytes(memory))
        regs={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)}
        regs.update(sp=stack,cs=self.cs,ds=self.ds,es=seed,ss=0x7000,fs=seed^0xA55A,gs=seed^0x5AA5)
        high={n:(seed^0x5AA5)<<16 for n in GPRS}
        for n,reg in GPRS.items():self.uc.reg_write(reg,high[n]|regs[n])
        for n in ('cs','ds','es','ss','fs','gs'):self.uc.reg_write(REG[n],regs[n])
        self.uc.reg_write(x.UC_X86_REG_EFLAGS,flags)
        self.stack,self.seed,self.status=stack,seed,status
        self.o=options
        self.o.update(load=self.load,file=cfg,sample=(0,0,0,0),driver_ax=driver)
        self.expected=Prediction(memory,regs,high,flags,self.o)
        self.index,self.error,self.returned,self.pending=0,None,False,None
        self.prefix_stopped=False
        self.cfg_stopped=False
        self.file=bytearray(cfg)
        self.child_rows=[]
        self.loop_count=0
        self.loop_started=False
        self.maximum_stack=0
        plan=self.expected.run()
        try:
            next(plan)
            planned=True
        except StopIteration:
            planned=False
        resume=START
        while True:
            try:self.uc.emu_start(self.base+resume,1<<20,count=2000000)
            except UcError as error:raise ValueError('OP startup guest exception') from error
            need(self.error is None,self.error or 'guest failure')
            if self.pending is None:
                break
            event=self.pending
            self.pending=None
            result=self.run_child(event)
            try:
                plan.send(result)
                planned=True
            except StopIteration:
                planned=False
            if result['held']:break
            resume=self.cs*16+event[-1]-self.base
        need(not planned and self.index==len(self.expected.events),'complete source-level startup continuation plan')
        need(self.returned or self.expected.held or self.prefix_stopped or self.cfg_stopped,'actual far return or explicitly classified conditional prefix')
        need(self.full()==self.expected.full(),'complete predicted DWORD/segment state '+str((self.full(),self.expected.full())))
        mask=self.expected.mask|0x600
        need(self.uc.reg_read(x.UC_X86_REG_EFLAGS)&mask==self.expected.flags&mask,'defined flags/IF/DF,including real cfg-copy CLD')
        need(bytes(self.uc.mem_read(0,1<<20))==self.expected.memory,'all physical memory after declared inherited callee-private windows')
        need(self.file==self.expected.file,'complete independent cfg transaction')
        return dict(returned=self.returned,held=self.expected.held,loop_prefix=self.prefix_stopped,cfg_boundary=self.cfg_stopped,iterations=self.expected.iterations,
            registers=self.expected.full(),flags=self.expected.flags&mask,flag_mask=mask,file_hex=self.file.hex(),
            events=len(self.expected.events),trace_sha256=hashlib.sha256(json.dumps(self.expected.events,sort_keys=True).encode()).hexdigest(),
            borrowed=self.child_rows,maximum_stack_depth=self.maximum_stack,inherited_private_stack_bytes=96 if self.child_rows else 0)


def stream(*words):
    return tuple((value,0,0,0) for value in words)


OPTION_PATH=stream(1,0,1,0,0x20,0,0x1000,0,0x1000)


def cases():
    # Independent exhaustive BYTE axes, not a claim of their Cartesian product.
    for value in range(256):
        yield dict(mode=value)
        yield dict(mode=128,demo=value)
        yield dict(fast=value)
        yield dict(driver=255,midi=value)
    for raw in range(2,256):
        count=(1,3,7)[raw%3]
        yield dict(raw_dispatch=raw,loop_prefix=count,samples=stream(*([0]*count)),random=0xFFFFFFFF)
    for index in range(3):
        for value in (0,1,2,3,127,128,255):
            cfg=bytearray(b'\x02\x01\x03\x48\x57\x00\x50\xA7')
            cfg[index]=value
            yield dict(cfg=bytes(cfg))
    for flags in (2,0x202,0x402,0xED7):
        for stack in (0x100,0xFFF0):
            for read_bytes in range(9):
                yield dict(flags=flags,stack=stack,read_bytes=read_bytes,cfg_boundary=True)
            for seed in (0,1,0x1357,0x8000,0xFFFF):
                yield dict(flags=flags,stack=stack,seed=seed,status=seed,fast=255,
                    cfg=b'\xFF\x80\xFE\xDE\xAD\x00\x60\x77',read_bytes=7)
            yield dict(flags=flags,stack=stack,samples=OPTION_PATH)
            yield dict(flags=flags,stack=stack,mode=129,selection_ax=0)
            yield dict(flags=flags,stack=stack,samples=stream(0x20,0,0x20),selection_ax=0,selected_char=17)
    for value in (1,127,128,255,256,32767,32768,65535):
        yield dict(zoom=value)
        yield dict(assign=value)
    for value in (0,1,255):
        yield dict(quit=value)
    for present in (0,1,65535):
        for channel in (0,1,2,3):
            row=[0,0,0,0]
            row[channel]=0x1000
            # Player2 is deliberately not merged; follow it with a real exit.
            samples=(tuple(row),(0x1000,0,0,0)) if channel==2 or channel==3 and not present else (tuple(row),)
            yield dict(present=present,samples=samples)
    for count in (1,3,7):
        for raw in (2,127,128,255):
            yield dict(raw_dispatch=raw,loop_prefix=count,samples=stream(*([0]*count)))
    yield dict(samples=stream(2,0,0x20,0,0x1000),selection_ax=0)
    yield dict(samples=stream(2,0,2,0,2,0,0x20,0,0x1000))
    yield dict(wait_samples=stream(*([0]*520),1))
    yield dict(samples=stream(0x20,0,0x1000),selection_ax=1)


def verify(target,candidate):
    observations=[]
    for image in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            machine=Machine(image,load)
            digest=hashlib.sha256()
            totals=dict(cases=0,ordinary_returns=0,held_descendant_prefixes=0,raw_dispatch_prefixes=0,cfg_preparation_boundaries=0)
            borrowed={name:0 for name in BORROWED}
            maximum=iterations=0
            try:
                for options in cases():
                    try:row=machine.run(**options)
                    except ValueError as error:raise ValueError(f'startup {options}: {error}') from error
                    totals['cases']+=1
                    totals['ordinary_returns']+=row['returned']
                    totals['held_descendant_prefixes']+=row['held']
                    totals['raw_dispatch_prefixes']+=row['loop_prefix']
                    totals['cfg_preparation_boundaries']+=row['cfg_boundary']
                    for child in row['borrowed']:borrowed[child['name']]+=1
                    maximum=max(maximum,row['maximum_stack_depth'])
                    iterations=max(iterations,row['iterations'])
                    digest.update(json.dumps(row,sort_keys=True).encode())
                need(sum(totals[k] for k in totals if k!='cases')==totals['cases'],'disjoint actual outcomes')
                need(machine.covered==machine.owned,'all263 startup instruction bytes execute')
                need(all(borrowed.values()),'all four real borrowed callee entries')
                loads.append(dict(load_segment=load,**totals,executed_owner_bytes=len(machine.covered),
                    borrowed_calls=borrowed,maximum_stack_depth=maximum,maximum_completed_iterations=iterations,trace_sha256=digest.hexdigest()))
            finally:machine.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent complete target/candidate startup outcomes')
    return dict(images=2,functions=1,code_bytes=SIZE,instruction_bytes=SIZE,
        cases_per_image=sum(row['cases'] for row in observations[0]),observations=observations[0],
        exhaustive_independent_BYTE_axes=['game_mode','demo_num','op_animation_fast','midi_possible'],
        unchecked_dispatch_BYTE_values=list(range(2,256)),unchecked_dispatch_prefix_lengths=[1,3,7],
        unchecked_dispatch_assumption='explicit post-main external CDG callback writes in_option; no normal keyboard reachability inferred',
        unchecked_dispatch_invariant='quit=0; in_option outside0/1; disjoint resident rand increments modulo2^32; input writes only device WORDs; delay counter replies0/1',
        short_cfg_boundary='actual cfg_load return before first resident read; no downstream arbitrary-segment acceptance',
        shared_physical_machine=True,synthetic_owned_callee_returns=False,borrowed_private_stack_bytes=dict(main=96,option=64,wait=80,vs=80),
        primitive_private_stack_bytes=0,external_CRT_copy_executes=True,physical_hardware_or_successful_exec_proved=False,whole_product_accepted=False)


def negative_controls(target):
    from dataclasses import replace
    controls=(
        ('saved-BP',0xA417,6,{}),
        ('zoom-WORD-high-half',0xA42A,1,dict(zoom=256)),
        ('zoom-condition',0xA42E,1,{}),
        ('first-error-message',0xA432,1,dict(zoom=1)),
        ('common-early-RETF',0xA451,8,dict(zoom=1)),
        ('init-filename',0xA454,1,{}),
        ('init-cdecl-cleanup4',0xA45D,2,{}),
        ('init-failure-branch',0xA460,1,dict(assign=1)),
        ('out-of-memory-message',0xA464,1,dict(assign=1)),
        ('gaiji-filename',0xA46F,1,{}),
        ('cfg-near-call',0xA477,1,{}),
        ('mode-threshold',0xA481,1,dict(mode=128)),
        ('mode-unsigned',0xA482,14,dict(mode=0)),
        ('demo-field',0xA487,1,dict(mode=128,demo=0)),
        ('demo-condition',0xA489,1,dict(mode=128,demo=1)),
        ('part1-before-part3',0xA48C,1,dict(mode=128)),
        ('real-VS-call',0xA495,1,dict(mode=128)),
        ('animation-fast-test',0xA49F,1,{}),
        ('animation-choice',0xA4A0,1,{}),
        ('fast-set-one',0xA4AD,1,{}),
        ('fast-clear-zero',0xA4B8,1,dict(fast=255)),
        ('real-wait-call',0xA4BD,1,{}),
        ('clear-option-BYTE',0xA4C3,1,{}),
        ('clear-input-WORD',0xA4C8,1,{}),
        ('initial-main-call',0xA4CB,1,{}),
        ('skip-initial-input',0xA4D1,1,{}),
        ('input-far-call',0xA4D3,1,{}),
        ('dispatch-field',0xA4D8,1,{}),
        ('dispatch-sign-extension',0xA4DA,8,dict(raw_dispatch=128,loop_prefix=1,samples=stream(0))),
        ('main-dispatch-condition',0xA4DD,1,{}),
        ('option-case-one',0xA4E0,1,dict(samples=OPTION_PATH)),
        ('real-main-loop-call',0xA4E7,1,{}),
        ('real-option-loop-call',0xA4EC,1,dict(samples=OPTION_PATH)),
        ('rand-DWORD-width',0xA4F2,1,dict(random=0xFFFFFFFF)),
        ('rand-field',0xA4F6,1,{}),
        ('delay-one',0xA4F8,1,{}),
        ('quit-field',0xA500,1,{}),
        ('quit-backedge',0xA503,1,{}),
        ('cfg-exit-call',0xA506,1,{}),
        ('actual-owned-init',0xC425,1,{}),
        ('actual-owned-input',0xC9A4,1,{}),
        ('actual-owned-delay',0xC1A6,1,{}),
        ('actual-CRT-copy',0x3388,1,dict(flags=0x402)),
        ('actual-owned-exit',0xBFCB,1,{}),
        ('respal-free-tail',0xA518,1,{}),
        ('final-RETF',0xA51D,8,{}),
    )
    rejected=[]
    for name,at,mask,options in controls:
        raw=bytearray(target.program_image)
        raw[at]^=mask
        machine=None
        try:
            try:
                machine=Machine(replace(target,program_image=bytes(raw)),0x3000)
                machine.run(**options)
            except ValueError:rejected.append(name)
            else:raise ValueError('OP startup mutation survived: '+name)
        finally:
            if machine is not None:machine.close()
    return dict(actual_instruction_mutations=len(controls),rejected=rejected)
