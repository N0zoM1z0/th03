"""Complete CDG CPU contracts; file and heap effects are explicit interfaces.

Every owned nested free/all instruction executes on one physical UC. Synthetic
file replies write a bounded flat prefix (not a wrapped huge-pointer copy).
Unowned file/heap bodies and their internal private stack effects are not run.
"""
import hashlib
import itertools
import json
import struct
from dataclasses import replace
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import *
from lib.decoded_mainl_cdg_layout import CS, DS, START, SIZE, SLOTS, FLAG, ENTRIES, CALLS
from lib.decoded_mainl_pi_runtime import Spec as Frames, Machine as Physical, arithmetic, signed, ARITH
from lib.decoded_mainl_pi_free_runtime import address
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG, logical

CLEANUP = dict(open=4,read=6,seek=6,close=0,alloc=2,free=2)


def need(value,message):
    if not value:
        raise ValueError('MAINL CDG contract: '+str(message))


def header(size=4,count=1,segments=(0,0),bottom=80,layout=0x7F):
    return struct.pack('<5H2B2H',size,32,2,bottom,1,count,layout,*segments)


def effects(kind,args,index,options,regs,flags):
    """The shared environment reply, independent of either caller algorithm."""
    out = dict(regs)
    value = options['status']
    writes = []
    if kind=='alloc':
        values = options['allocations']
        value = values[(index-1)%len(values)]
    if kind=='read':
        amount,offset,segment = args
        raw = options['header'] if index==1 else options['payload']
        limits = options['read_limits']
        limit = limits[(index-1)%len(limits)] if limits else amount
        raw = raw[:min(amount,limit)]
        if raw:
            writes.append((segment*16+offset,raw))
    if kind in ('alloc','free'):
        out['ax'] = value
        final = (flags&0x600)|(options['reply_seed']&ARITH)|2
    else:
        seed = options['reply_seed']
        out.update(ax=value,bx=seed^0xA55A,cx=seed^0x1234,dx=seed^0x5AA5,es=0x6000)
        final = (flags&0x600&(0x200 if options['clear_df'] else 0x600))|(seed&ARITH)|2
    return out,final,writes


class Spec(Frames):
    def __init__(self,memory,regs,high,flags,options):
        super().__init__(memory,regs,high,flags,options)
        self.mask = ARITH
        self.native = {n:0 for n in ENTRIES}

    def dg(self,offset,size=2):
        at = address(self.ds,offset)
        return int.from_bytes(self.memory[at:at+size],'little')

    def field(self,offset,value,size=2):
        self.store(address(self.ds,offset),size,value)

    def slot(self,index):
        return (SLOTS+index*16)&65535

    def op(self,left,right,subtract=False):
        value = self.flag_operation(left,right,subtract)
        self.mask = ARITH
        return value

    def shift_ax(self,count):
        value = self.r['ax']
        result = (value<<count)&65535
        self.r['ax'] = result
        self.flags = (self.flags&0x600)|2|logical(result,16)|((value>>(16-count))&1)
        self.mask = 0xC5  # AF and multi-bit SHL's OF are undefined.
        return result

    def eax(self,value):
        value &= 0xFFFFFFFF
        self.high['ax'],self.r['ax'] = value&0xFFFF0000,value&65535

    def call(self,kind,args,continuation):
        self.frame(continuation)
        mask = self.mask|0x600
        self.events.append(('call',kind,args,self.full(),self.flags&mask,mask))
        index = self.counts.get(kind,0)+1
        self.counts[kind] = index
        out,flags,writes = effects(kind,args,index,self.o,self.r,self.flags)
        for at,raw in writes:
            self.events.append(('file-bytes',at,raw.hex()))
            self.memory[at:at+len(raw)] = raw
        for name,count,at,raw in self.o['writes']:
            if (name,count)==(kind,index):
                self.events.append(('interface-write',at,raw.hex()))
                self.memory[at:at+len(raw)] = raw
        self.r,self.flags,self.mask = out,flags,ARITH
        self.returned(CLEANUP[kind])

    def bridge(self,kind,args,continuation):
        for value,size in reversed(args):
            self.push(value,size)
        self.push(self.r['cs'])
        self.push(continuation)
        self.invoke(kind)

    def read(self,offset,segment,amount,continuation):
        self.push(segment)
        self.push(offset)
        self.push(amount)
        self.call('read',[amount,offset,segment],continuation)

    def seek(self,value,continuation):
        self.push(value,4)
        self.push(1)
        self.call('seek',[1,value&65535,value>>16],continuation)

    def colors(self,at,allocation_return,read_return):
        self.r['ax'] = self.dg(at)
        amount = self.shift_ax(2)
        self.push(amount)
        self.call('alloc',[amount],allocation_return)
        self.field(at+14,self.r['ax'])
        # The read length is reloaded after the allocation reply; callbacks can
        # change it. Neither a zero allocation nor a failed reply suppresses it.
        segment = self.dg(at+14)
        self.push(segment)
        self.push(0)
        self.r['ax'] = self.dg(at)
        amount = self.shift_ax(2)
        self.push(amount)
        self.call('read',[amount,0,segment],read_return)

    def alpha(self,at,allocation_return,read_return):
        amount = self.dg(at)
        self.push(amount)
        self.call('alloc',[amount],allocation_return)
        self.field(at+12,self.r['ax'])
        self.read(0,self.dg(at+12),self.dg(at),read_return)

    def invoke(self,kind):
        r = self.r
        entry_sp = r['sp']
        args = [self.word(self.ss,entry_sp+4+2*i) for i in range(ENTRIES[kind][2]//2)]
        frame = bytes(self.memory[address(self.ss,entry_sp):address(self.ss,entry_sp)+4+ENTRIES[kind][2]])
        self.events.append(('entry',kind,self.full(),frame.hex(),self.flags&(self.mask|0x600),self.mask|0x600))
        self.native[kind] += 1
        self.enter(4 if kind.startswith('single') else 2 if kind=='all' else 0)
        if kind=='all_noalpha':
            self.field(FLAG,1,1)
            fn = args[0]|args[1]<<16
            self.bridge('all',[(fn,4),(args[2],2)],0x947)
            self.field(FLAG,0,1)
            self.pop('bp')
            self.returned(6)
            return
        self.push(r['si'])
        self.push(r['di'])
        if kind=='free':
            slot = args[0]
            r['ax'] = slot
            shifted = self.shift_ax(4)
            r['ax'] = self.op(shifted,SLOTS)
            r['di'] = r['ax']
            r['si'] = 0
            for i in range(2):
                self.op(r['si'],2,True)
                r['bx'] = self.op(i,i)
                segment = self.dg(r['di']+r['bx']+12)
                self.op(segment,0,True)
                if segment:
                    r['bx'] = self.op(i,i)
                    self.push(segment)
                    self.call('free',[segment],0x97A)
                    r = self.r
                    r['bx'] = self.op(i,i)
                    self.field(r['di']+r['bx']+12,0)
                r['si'] = self.op(i,1)
            self.op(r['si'],2,True)
        elif kind.startswith('single'):
            n,fn_lo,fn_hi,slot = args
            r['di'] = slot
            continuation = 0x74D if kind=='single' else 0x7D7
            self.bridge('free',[(slot,2)],continuation)
            r = self.r
            r['ax'] = slot
            shifted = self.shift_ax(4)
            r['ax'] = self.op(shifted,SLOTS)
            r['si'] = at = r['ax']
            self.push(fn_lo|fn_hi<<16,4)
            self.call('open',[fn_lo,fn_hi],0x760 if kind=='single' else 0x7EA)
            self.read(at,self.ds,16,0x769 if kind=='single' else 0x7F3)
            r = self.r
            image_size = (self.dg(at)*5)&65535
            self.eax(image_size)
            self.store(address(self.ss,entry_sp-6),4,image_size)
            displacement = (signed(n)*image_size)&0xFFFFFFFF
            self.eax(displacement)
            self.flags &= ~0x801  # This signed DWORD product always fits.
            self.mask = 0x801
            self.seek(displacement,0x789 if kind=='single' else 0x813)
            if kind=='single':
                self.alpha(at,0x790,0x79F)
                self.colors(at,0x7AA,0x7BD)
                self.call('close',[],0x7C2)
            else:
                self.eax(self.dg(at))
                self.seek(self.dg(at),0x820)
                self.field(at+12,0)
                self.colors(at,0x830,0x843)
                self.call('close',[],0x848)
        else:
            need(kind=='all','known complete CDG entry')
            fn_lo,fn_hi,slot = args
            self.push(fn_lo|fn_hi<<16,4)
            self.call('open',[fn_lo,fn_hi],0x85D)
            self.bridge('free',[(slot,2)],0x865)
            r = self.r
            r['ax'] = slot
            shifted = self.shift_ax(4)
            r['ax'] = self.op(shifted,SLOTS)
            r['si'] = first = r['ax']
            self.read(first,self.ds,16,0x879)
            r = self.r
            r['di'] = first
            counter = 1
            local = address(self.ss,entry_sp-4)
            self.store(local,2,counter)
            while True:
                r['ax'] = self.dg(first+10,1)
                self.op(r['ax'],counter,True)
                if r['ax']<=counter:
                    break
                r['ax'] = self.op(slot,counter)
                self.bridge('free',[(r['ax'],2)],0x88E)
                r = self.r
                counter += 1
                self.store(local,2,counter)
            counter = 0
            self.store(local,2,0)
            while True:
                r['ax'] = self.dg(first+10,1)
                self.op(r['ax'],counter,True)
                if r['ax']<=counter:
                    break
                at = r['si']
                for field in (0,2,4,6,8):
                    r['ax'] = self.dg(first+field)
                    self.field(at+field,r['ax'])
                count = self.dg(first+10,1)
                r['ax'] = (r['ax']&0xFF00)|count
                self.field(at+10,count,1)
                self.field(at+11,0,1)
                flag = self.dg(FLAG,1)
                self.flags = (self.flags&0x600)|2|logical(flag,8)
                self.mask = ARITH
                if not flag:
                    self.alpha(at,0x8D6,0x8E5)
                else:
                    self.field(at+12,0)
                    self.eax(self.dg(at))
                    self.seek(self.dg(at),0x8F9)
                self.colors(at,0x904,0x917)
                r = self.r
                counter += 1
                self.store(local,2,counter)
                r['si'] = self.op(r['si'],16)
            self.call('close',[],0x92E)
        self.pop('di')
        self.pop('si')
        self.finish(ENTRIES[kind][2])


class Machine(Physical):
    def __init__(self,image,load):
        need(image.valid,'valid decoded MZ')
        self.load,self.base,self.cs,self.ds = load,load*16,load+CS,load+DS
        self.u = Uc(UC_ARCH_X86,UC_MODE_16)
        self.u.mem_map(0,1<<20)
        memory = bytearray(b'\xA5'*(1<<20))
        raw = image.relocated_program_image(load)
        memory[self.base:self.base+len(raw)] = raw
        self.initial = bytes(memory)
        ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[CS*16+START:CS*16+START+SIZE],CS*16+START))
        need(sum(i.size for i in ins)==SIZE,'complete CDG instruction boundaries')
        self.instructions = {i.address:i.size for i in ins}
        self.owner = set(range(CS*16+START,CS*16+START+SIZE))
        self.covered = set()
        self.entries = {self.cs*16+at:name for name,(at,_,_) in ENTRIES.items()}
        self.hooks = [self.u.hook_add(UC_HOOK_CODE,self.code),self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)]

    def safe_write(self,at,raw):
        lo,hi = self.base+CS*16+START,self.base+CS*16+START+SIZE
        slo,shi = self.o['ss']*16+self.o['stack']-64,self.o['ss']*16+self.o['stack']+16
        need(0<=at<at+len(raw)<=1<<20 and not(at<hi and at+len(raw)>lo)
             and not(at<shi and at+len(raw)>slo),'interface fixture must not overwrite owned CODE or live caller frames')

    def code(self,u,at,size,_):
        try:
            self.max_depth = max(self.max_depth,self.o['stack']-u.reg_read(REG['sp']))
            if at-self.base in CALLS.values() and self.index<len(self.events) and self.events[self.index][0]=='far-frame':
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                ip,cs = struct.unpack('<2H',bytes(u.mem_read(address(ss,sp),4)))
                self.event(('far-frame',address(ss,sp),ip,cs))
                self.far_frames += 1
            if at==self.cs*16+0xFFFF:
                self.returned = True
                u.emu_stop()
                return
            if at in self.entries:
                kind = self.entries[at]
                event = self.events[self.index]
                need(event[:2]==('entry',kind),'real owned nested entry order')
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                frame = bytes(u.mem_read(address(ss,sp),4+ENTRIES[kind][2]))
                self.event(('entry',kind,self.regs(True),frame.hex(),u.reg_read(UC_X86_REG_EFLAGS)&event[-1],event[-1]))
                self.native[kind] += 1
            offset = at-self.base
            if offset in CALLS.values():
                kind = next(k for k,v in CALLS.items() if v==offset)
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                ip,cs = struct.unpack('<2H',bytes(u.mem_read(address(ss,sp),4)))
                amount = CLEANUP[kind]
                args = list(struct.unpack('<'+'H'*(amount//2),bytes(u.mem_read(address(ss,sp+4),amount)))) if amount else []
                event = self.events[self.index]
                need(event[:2]==('call',kind),'declared interface order')
                self.event(('call',kind,args,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&event[-1],event[-1]))
                index = self.counts.get(kind,0)+1
                self.counts[kind] = index
                out,flags,writes = effects(kind,args,index,self.o,self.regs(),u.reg_read(UC_X86_REG_EFLAGS))
                for target,raw in writes:
                    self.safe_write(target,raw)
                    self.event(('file-bytes',target,raw.hex()))
                    u.mem_write(target,raw)
                for name,count,target,raw in self.o['writes']:
                    if (name,count)==(kind,index):
                        self.safe_write(target,raw)
                        self.event(('interface-write',target,raw.hex()))
                        u.mem_write(target,raw)
                for name in ('ax','bx','cx','dx','es'):
                    u.reg_write(REG[name],out[name])
                u.reg_write(UC_X86_REG_EFLAGS,flags)
                u.reg_write(REG['sp'],sp+4+amount)
                u.reg_write(REG['cs'],cs)
                u.reg_write(REG['ip'],ip)
                return
            need(self.instructions.get(offset)==size,'only complete CDG instructions or declared interfaces')
            self.covered.update(range(offset,offset+size))
        except Exception as error:
            self.fail(error)

    def run(self,kind,*,slot=0,n=0,size=4,count=1,noalpha=0,old_segments=(0x2222,0x3333),
            other_segments=(0,0),header_segments=(0,0),bottom=80,header_raw=None,read_limits=(),
            payload=b'\x37\xC9\x18\xAF\xE1',allocations=(0x5000,0x6000),status=0xFFFF,reply_seed=0xA55A,
            filename=(0xFFFF,0x6000),clear_df=False,writes=(),flags=0x202,ss=0x7000,stack=0xF800,
            seed=0x1357,persistent=False):
        need(kind in ENTRIES and all(0<=v<=65535 for v in (slot,n,size,*old_segments,*other_segments,*header_segments,bottom,*allocations,status,reply_seed,*filename)), 'WORD fixtures')
        need(0<=count<=255 and 0<=noalpha<=255 and allocations and len(payload)<=32 and all(0<=v<=65535 for v in read_limits),'BYTE count/flag and bounded file prefixes')
        need(ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),'foreign SS / incoming flags')
        need(all(k in CALLS and i>=1 and isinstance(raw,bytes) and self.ds*16<=at<at+len(raw)<=self.ds*16+65536 for k,i,at,raw in writes),'bounded declared DGROUP writes')
        header_reply = header(size,count,header_segments,bottom) if header_raw is None else header_raw
        need(isinstance(header_reply,bytes) and len(header_reply)<=16,'bounded raw header reply')
        memory = bytearray(self.u.mem_read(0,1<<20) if persistent else self.initial)
        if not persistent:
            for index in range(256):
                offset = (SLOTS+(slot+index)*16)&65535
                raw = header(size,count,old_segments if index==0 else other_segments,bottom)
                for i,b in enumerate(raw):
                    memory[address(self.ds,offset,i)] = b
            memory[self.ds*16+FLAG] = noalpha
        args = [slot] if kind=='free' else [n,*filename,slot] if kind.startswith('single') else [*filename,slot]
        frame = struct.pack('<'+'H'*(2+len(args)),0xFFFF,self.cs,*args)
        memory[address(ss,stack):address(ss,stack)+len(frame)] = frame
        self.u.mem_write(0,bytes(memory))
        regs = {name:(seed+i*0x231)&65535 for i,name in enumerate(GPRS)}
        regs.update(sp=stack,cs=self.cs,ds=self.ds,es=0x6666,ss=ss)
        self.high = {name:((seed^0x5AA5)<<16) for name in GPRS}
        for name in GPRS:
            self.u.reg_write(GPRS[name],self.high[name]|regs[name])
        for name in ('cs','ds','es','ss'):
            self.u.reg_write(REG[name],regs[name])
        self.u.reg_write(UC_X86_REG_FS,0x3456)
        self.u.reg_write(UC_X86_REG_GS,0x4567)
        self.u.reg_write(UC_X86_REG_EFLAGS,flags)
        self.o = dict(load=self.load,slot=slot,header=header_reply,payload=payload,read_limits=read_limits,
                      allocations=allocations,status=status,reply_seed=reply_seed,clear_df=clear_df,writes=writes,ss=ss,stack=stack)
        spec = Spec(memory,regs,self.high,flags,self.o)
        spec.invoke(kind)
        expected,final,self.events = spec.full(),spec.flags,spec.events
        self.index,self.error,self.returned,self.max_depth,self.far_frames,self.far_word_hooks = 0,None,False,0,0,0
        self.counts,self.native = {},{name:0 for name in ENTRIES}
        try:
            self.u.emu_start(self.cs*16+ENTRIES[kind][0],1<<20,count=1000000)
        except UcError as error:
            raise ValueError('MAINL CDG contract: guest fault') from error
        need(self.error is None,self.error or 'guest error')
        need(self.returned and self.index==len(self.events),'complete native return and ordered events, never budget expiry')
        need(self.regs(True)==expected,'full DWORD/WORD/segment state '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)==final&(ARITH|0x600),'defined return flags and IF/DF')
        need((self.u.reg_read(UC_X86_REG_FS),self.u.reg_read(UC_X86_REG_GS))==(0x3456,0x4567),'FS/GS preserved')
        need(self.native==spec.native and self.counts==spec.counts,'all real nested entries and external requests')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'complete physical memory including all stack and caller bytes')
        return dict(kind=kind,registers=expected,flags=final&(ARITH|0x600),events=len(self.events),
            events_sha256=hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest(),
            native_entries=self.native,interfaces=self.counts,checked_far_frames=self.far_frames,
            stack_depth=self.max_depth,noalpha=memory[self.ds*16+FLAG])


def cases(load):
    ds = (load+DS)*16
    for kind,slot,flags,ss in itertools.product(ENTRIES,(0,1,31,32,0x1000,0x7FFF,0x8000,0xFFFF),
                                               (2,0x202,0x402,0xED7),(0x7000,0x8000)):
        yield kind,dict(slot=slot,flags=flags,ss=ss)
    for kind,field,shift,value in itertools.product(('single','single_noalpha'),('size','n'),(0,8),range(256)):
        yield kind,{field:value<<shift}
    for shift,value in itertools.product((0,8),range(256)):
        yield 'free',dict(slot=value<<shift)
    for count in range(256):
        yield 'all',dict(count=count,noalpha=count&1)
    yield 'all',dict(count=255,noalpha=0)
    yield 'all',dict(count=255,noalpha=0,other_segments=(0x1111,0x2222))
    for flag in range(256):
        yield 'all',dict(count=2,noalpha=flag)
    for count,flag in itertools.product((0,1,2,3,32,127,128,254,255),(0,1,2,0x80,0xFF)):
        yield 'all_noalpha',dict(count=count,noalpha=flag)
    for kind,values in itertools.product(ENTRIES,((0,),(0,0x5000),(0x5000,0),(0,0,0x6000),(0x8000,))):
        yield kind,dict(count=2,allocations=values)
    for kind,segments in itertools.product(ENTRIES,((0,0),(0x100,0),(0,0x8000),(0xFFFF,0xFFFF))):
        yield kind,dict(count=2,old_segments=segments,other_segments=segments)
    for kind,size,n in itertools.product(('single','single_noalpha'),(0,1,0x3333,0x3334,0x3FFF,0x4000,0x7FFF,0x8000,0xCCCC,0xCCCD,0xFFFF),
                                        (0,1,0xFFFF,0x8000,0x7FFF)):
        yield kind,dict(size=size,n=n)
    for kind,limits in itertools.product(ENTRIES,((0,),(1,),(2,),(10,),(12,),(15,),(16,0,3))):
        yield kind,dict(count=3,read_limits=limits,header_segments=(0x4444,0x5555))
    for kind,filename in itertools.product(('single','single_noalpha','all','all_noalpha'),((0,0),(0xFFFF,0xFFFF),(0x1234,0x5678))):
        yield kind,dict(filename=filename,count=2)
    for kind in ('all','single','single_noalpha'):
        yield kind,dict(count=0,header_segments=(0x4444,0x5555))
    for kind in ('all','all_noalpha'):
        for slot in (0xE2F,0xEB8):
            yield kind,dict(slot=slot,count=2,bottom=0,noalpha=0xFF)
    yield 'single',dict(writes=(('alloc',1,ds+SLOTS,b'\x03\0'),))
    yield 'single_noalpha',dict(writes=(('seek',1,ds+SLOTS,b'\xff\xff'),))
    yield 'all',dict(count=1,writes=(('read',2,ds+SLOTS,b'\x03\0'),('read',2,ds+SLOTS+10,b'\x03')))
    yield 'all',dict(count=2,other_segments=(0x1111,0x2222),writes=(('free',3,ds+SLOTS+10,b'\x05'),))
    yield 'all',dict(count=3,writes=(('read',3,ds+FLAG,b'\xff'),))
    yield 'all_noalpha',dict(count=3,noalpha=0xFF,writes=(('open',1,ds+FLAG,b'\0'),('close',1,ds+FLAG,b'\xff')))
    yield 'all',dict(slot=0xE30,count=3,allocations=(load+DS,),payload=b'\0'*32)


def verify(target,candidate):
    results = []
    for image_index,image in enumerate((target,candidate)):
        rows = []
        for load in (0x1000,0x3000):
            machine = Machine(image,load)
            trace = hashlib.sha256()
            counts = {k:0 for k in ENTRIES}
            maximum = 0
            maxima = {k:0 for k in CALLS}
            maximum_free_entries = 0
            far_frames = 0
            try:
                for count,(kind,parameters) in enumerate(cases(load),1):
                    p = dict(seed=0x1357 if count&1 else 0xECA8,stack=0x80 if count&1 else 0xF800,
                             reply_seed=0xA55A if count&1 else 0x5AA5,clear_df=not bool(count&1))
                    p.update(parameters)
                    r = machine.run(kind,**p)
                    counts[kind] += 1
                    maximum = max(maximum,r['stack_depth'])
                    maximum_free_entries = max(maximum_free_entries,r['native_entries']['free'])
                    for k in maxima:
                        maxima[k] = max(maxima[k],r['interfaces'].get(k,0))
                    far_frames += r['checked_far_frames']
                    trace.update(json.dumps(r,sort_keys=True).encode())
                    if count%512==0:
                        print(f'CDG contracts: image {image_index+1}, load {load:04X}, {count} entries',flush=True)
                for kind in ('single','all','all_noalpha'):
                    for index in range(3):
                        r = machine.run(kind,count=2,persistent=index>0,noalpha=0x80)
                        count += 1
                        counts[kind] += 1
                        far_frames += r['checked_far_frames']
                        trace.update(json.dumps(r,sort_keys=True).encode())
                need(machine.owner<=machine.covered,'all 593 owner bytes execute including every real nested path')
                rows.append(dict(load_segment=load,cases=count,cases_by_function=counts,executed_owner_bytes=593,
                    maximum_stack_depth=maximum,maximum_native_free_entries=maximum_free_entries,
                    maximum_interface_calls=maxima,checked_far_frames=far_frames,trace_sha256=trace.hexdigest()))
                print(f'CDG contracts: image {image_index+1}, load {load:04X}, {count} cases / all 593 bytes pass',flush=True)
            finally:
                machine.close()
        results.append(rows)
    need(results[0]==results[1],'complete independent target/candidate state observations')
    return dict(images=2,functions=5,code_bytes=593,executed_owner_bytes=593,
                cases_per_image=sum(o['cases'] for o in results[0]),observations=results[0],
                exhaustive_image_count_BYTE=256,exhaustive_flag_BYTE=256,exhaustive_size_and_signed_index_BYTE_lanes=256,
                ignored_stack_bytes=0,far_return_words_checked_at_entry=True,actual_owned_nested_helpers=True,
                physical_DOS_or_heap_executed=False)


def negative_controls(target):
    controls = (
        ('single-slot-frame',0x746,2,'single',dict(slot=1)),('single-slot-scale',0x751,1,'single',dict(slot=1)),
        ('single-slot-base',0x753,2,'single',{}),('single-filename-frame',0x75A,2,'single',{}),
        ('single-header-length',0x763,2,'single',{}),('single-five-before-widen',0x76D,1,'single',dict(size=0x3334)),
        ('single-zero-extension',0x770,8,'single',dict(size=0xFFFF)),('single-signed-n',0x779,8,'single',dict(n=0xFFFF)),
        ('single-image-index-frame',0x77A,2,'single',dict(n=0x8000)),('single-DWORD-product',0x77D,1,'single',dict(n=0xFFFF)),
        ('single-relative-seek',0x783,1,'single',{}),('single-alpha-segment-store',0x792,2,'single',{}),
        ('single-alpha-read-offset',0x797,1,'single',{}),('single-color-length',0x7A3,1,'single',{}),
        ('single-color-segment-store',0x7AC,2,'single',{}),('single-color-read-length',0x7B6,1,'single',{}),
        ('single-far-Pascal-return',0x7C6,2,'single',{}),
        ('noalpha-five-before-widen',0x7F7,1,'single_noalpha',dict(size=0x3334)),
        ('noalpha-signed-index',0x803,8,'single_noalpha',dict(n=0xFFFF)),
        ('noalpha-second-seek-value',0x816,2,'single_noalpha',{}),('noalpha-skip-plane',0x81A,1,'single_noalpha',{}),
        ('noalpha-clear-alpha',0x824,1,'single_noalpha',{}),('noalpha-color-size',0x829,1,'single_noalpha',{}),
        ('all-first-slot-frame',0x85F,2,'all',dict(slot=1,count=2)),('all-slot-stride',0x86A,1,'all',dict(slot=1)),
        ('all-header-length',0x873,2,'all',{}),('all-prefree-initial-index',0x87E,1,'all',dict(count=3)),
        ('all-next-slot-add',0x887,2,'all',dict(count=3)),('all-prefree-step',0x88F,8,'all',dict(count=3)),
        ('all-image-count-field',0x893,1,'all',dict(count=3)),('all-unsigned-BYTE-count',0x895,0x80,'all',dict(count=128)),
        ('all-first-size-copy',0x8A5,2,'all',dict(count=2)),('all-pixel-width-copy',0x8AB,2,'all',dict(count=2)),
        ('all-pixel-height-copy',0x8B1,2,'all',dict(count=2)),('all-bottom-copy',0x8B7,2,'all',dict(count=2)),
        ('all-dword-width-copy',0x8BD,2,'all',dict(count=2)),('all-count-copy',0x8C3,1,'all',dict(count=2)),
        ('all-plane-layout-zero',0x8C7,1,'all',{}),('all-global-flag-field',0x8CA,2,'all',dict(noalpha=0x80)),
        ('all-noalpha-branch',0x8CE,1,'all',dict(noalpha=0x80)),('all-alpha-segment-store',0x8D8,2,'all',{}),
        ('all-noalpha-clear-segment',0x8EB,1,'all',dict(noalpha=1)),
        ('all-noalpha-seek-WORD',0x8EF,2,'all',dict(noalpha=1)),('all-color-size-wrap',0x8FD,1,'all',dict(size=0x4000)),
        ('all-color-segment-store',0x906,2,'all',{}),('all-read-color-length',0x910,1,'all',{}),
        ('all-loading-index-step',0x918,8,'all',dict(count=2)),('all-next-CDG-stride',0x91C,1,'all',dict(count=2)),
        ('all-live-count-read',0x91F,1,'all',dict(count=2)),('all-Pascal-cleanup',0x932,2,'all',{}),
        ('wrapper-force-true',0x93B,1,'all_noalpha',{}),('wrapper-slot-frame',0x93E,2,'all_noalpha',dict(slot=1)),
        ('wrapper-real-all-call',0x945,1,'all_noalpha',{}),('wrapper-reset-zero-not-restore',0x94B,1,'all_noalpha',dict(noalpha=0xFF)),
        ('wrapper-Pascal-cleanup',0x94E,2,'all_noalpha',{}),
        ('free-slot-frame',0x957,2,'free',dict(slot=1)),('free-slot-scale',0x95A,1,'free',dict(slot=1)),
        ('free-pointer-base',0x95C,2,'free',{}),('free-initial-plane',0x961,1,'free',{}),
        ('free-first-segment-field',0x96A,2,'free',dict(old_segments=(0x2222,0))),('free-zero-check',0x96D,1,'free',dict(old_segments=(0,0))),
        ('free-native-heap-call',0x976,1,'free',{}),('free-clear-field',0x980,2,'free',{}),
        ('free-increment-plane',0x983,8,'free',{}),('free-two-planes',0x986,1,'free',{}),
        ('free-far-Pascal-pop',0x98D,2,'free',{}))
    rejected = []
    for name,at,xor,kind,parameters in controls:
        raw = bytearray(target.program_image)
        raw[CS*16+at] ^= xor
        machine = None
        try:
            machine = Machine(replace(target,program_image=bytes(raw)),0x1000)
            machine.run(kind,**parameters)
        except (ValueError,UcError):
            rejected.append(name)
        else:
            raise ValueError('CDG actual instruction mutation escaped: '+name)
        finally:
            if machine:
                machine.close()
    return dict(count=len(rejected),rejected=rejected,actual_guest_instruction_mutations=True,
                alignment_mutations_counted=False)
