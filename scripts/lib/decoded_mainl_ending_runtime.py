"""Ending orchestration with actual accepted callees on one physical UC.

Scripts, staff, registration, DOS/exec and remaining library bodies are explicit
returning interfaces. Counter updates do not establish physical IRQ timing.
"""
import hashlib
import itertools
import json
import struct
from dataclasses import replace
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INSN
from unicorn.x86_const import *
from lib.decoded_mainl_ending_layout import CS, DS, START, SIZE, DATA
from lib.decoded_mainl_cdg_runtime import Spec as CDGSpec
from lib.decoded_mainl_pi_runtime import Machine as Physical, ARITH
from lib.decoded_mainl_pi_free_runtime import specification as pi_free_spec, address, TEST_FLAGS
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG, logical

CONTEXT = {'cdg':(0xC7E,0x950,63),'pi':(0,0xFEC,76),'delay':(0xC7E,0x372,21),'exit':(0xC7E,0x1B0,67)}
SERVICES = {0x17D0:('palette',0,True),0xE72:('clear',0,True),0x1758:('show',0,True),
 CS*16+0xB3E:('load',4,False),CS*16+0x167E:('animate',0,False),
 CS*16+0xB84:('script_free',0,False),CS*16+0x2E1D:('staff',0,False),
 CS*16+0x21E2:('regist',0,False),0x1F20:('text_clear',0,True),0xC96:('gaiji',0,True),
 0x2912:('pfend',0,True),0x201C:('vsync_end',0,True),0x235A:('unassign',0,True),
 0x17CA:('js_end',0,True),0x75A:('egc_start',0,True),0x8E37:('execl',12,True)}
BY_NAME = {name:(at,pop,far) for at,(name,pop,far) in SERVICES.items()}


def need(value,message):
    if not value:
        raise ValueError('MAINL ending contract: '+str(message))


def environment(regs,flags,seed,status,clear_df):
    out = dict(regs)
    out.update(ax=status,cx=seed^0x1234,dx=seed^0x5AA5,es=0x6000)
    return out,(flags&0x600&(0x200 if clear_df else 0x600))|(seed&ARITH)|2


class Spec(CDGSpec):
    def far_frame(self,continuation,segment):
        self.frame(continuation)
        self.r['cs'] = self.o['load']+segment

    def service(self,name,args,continuation):
        at,pop,far = BY_NAME[name]
        if far:
            self.far_frame(continuation,0)
        else:
            self.push(continuation)
        mask = ARITH|0x600
        self.events.append(('service',name,args,self.full(),self.flags&mask,mask))
        index = self.counts.get(name,0)+1
        self.counts[name] = index
        for role,number,location,raw in self.o['writes']:
            if (role,number)==(name,index):
                self.events.append(('interface-write',location,raw.hex()))
                self.memory[location:location+len(raw)] = raw
        self.r,self.flags = environment(self.r,self.flags,self.o['reply_seed']^index,self.o['status'],self.o['clear_df'])
        if far:
            self.returned(0 if name=='execl' else pop)
        else:
            self.r['sp'] += 2+pop

    def out(self,port,value):
        self.r['dx'] = port
        self.r['ax'] = (self.r['ax']&0xFF00)|value
        self.events.append(('out',port,1,value,self.flags&0x200))

    def byte_op(self,left,right):
        value = (left+right)&255
        flags = logical(value,8)|int(left+right>255)|(16 if (left^right^value)&16 else 0)
        flags |= 0x800 if (~(left^right)&(left^value))&128 else 0
        self.flags = (self.flags&0x600)|flags|2
        self.mask = ARITH
        return value

    def pointer(self,offset):
        return self.dg(offset),self.dg(offset+2)

    def les(self,offset):
        self.r['bx'],self.r['es'] = self.pointer(offset)

    def byte(self,segment,offset,displacement=0):
        return self.memory[address(segment,offset,displacement)]

    def delay(self):
        self.enter()
        self.field(0x144E,0)
        for value in self.o['ticks']:
            self.events.append(('clock',value))
            self.memory[address(self.ds,0x144E):address(self.ds,0x144E)+2] = struct.pack('<H',value)
            self.r['ax'] = value
            self.op(value,96,True)
            if value>=96:
                break
        else:
            raise ValueError('ending counter fixture must reach unsigned96; no timeout proof')
        self.pop('bp')
        self.returned(2)

    def exit(self):
        self.enter()
        self.service('pfend',[],0x1B8)
        self.out(0xA6,1)
        self.service('clear',[],0x1C3)
        self.out(0xA6,0)
        self.service('clear',[],0x1CE)
        self.out(0xA6,0)
        self.out(0xA4,0)
        for name,continuation in (('vsync_end',0x1DD),('unassign',0x1E2),('text_clear',0x1E7),
                                   ('js_end',0x1EC),('egc_start',0x1F1)):
            self.service(name,[],continuation)
        self.pop('bp')
        self.returned(0)

    def run(self):
        self.enter(2)
        for slot,continuation in enumerate((0x238D,0x2394,0x239B)):
            self.push(slot)
            self.far_frame(continuation,0xC7E)
            self.invoke('free')
        self.push(self.ds)
        self.push(DATA['headers'])
        pointer = self.dg(DATA['buffers'],4)
        self.push(pointer,4)
        self.far_frame(0x23A9,0)
        frame = bytes(self.memory[address(self.ss,self.r['sp']):address(self.ss,self.r['sp'])+12])
        self.events.append(('pi-entry',self.full(),frame.hex()))
        out,flags,mask,events,calls = pi_free_spec(self.memory,self.r,self.flags,self.o['heap_replies'])
        self.events.extend(events)
        self.counts['pi_heap'] = calls
        self.r,self.flags,self.mask = out,flags,mask
        self.r['cs'] = self.o['load']+CS
        r = self.r
        self.les(DATA['resident'])
        character = self.byte(r['es'],r['bx'],12)
        playchar = max(0,(character-1)//2)
        r['ax'],r['dx'] = playchar,0xFFFF if character==0 else 0
        local = address(self.ss,r['bp']-1)
        self.store(local,1,playchar)
        # CMP byte local,10, not a WORD comparison of the original resident.
        self.flags = (self.flags&0x600)|2|logical((playchar-10)&255,8)|int(playchar<10)
        if (playchar^10^((playchar-10)&255))&16:
            self.flags |= 16
        if ((playchar^10)&(playchar^((playchar-10)&255)))&128:
            self.flags |= 0x800
        if playchar>=10:
            self.les(DATA['script'])
            r['ax'] = (r['ax']&0xFF00)|self.byte(r['es'],r['bx'],1)
            self.push(r['ax'])
            quotient,remainder = divmod(playchar,10)
            r['ax'] = quotient
            self.pop('dx')
            low = self.byte_op(r['dx']&255,quotient)
            r['dx'] = (r['dx']&0xFF00)|low
            r['bx'] = self.dg(DATA['script'])
            self.store(address(r['es'],r['bx'],1),1,low)
            r['ax'],r['dx'] = quotient,remainder
            self.store(local,1,remainder)
        self.les(DATA['script'])
        r['ax'] = (r['ax']&0xFF00)|self.memory[local]
        at = address(r['es'],r['bx'],2)
        self.store(at,1,self.byte_op(self.memory[at],r['ax']&255))
        self.field(DATA['tone'],0)
        self.service('palette',[],0x2403)
        self.push(96)
        self.far_frame(0x240A,0xC7E)
        self.delay()
        self.out(0xA6,0)
        self.out(0xA4,0)
        self.service('clear',[],0x2419)
        self.service('show',[],0x241E)
        lo,seg = self.pointer(DATA['script'])
        self.push(lo|seg<<16,4)
        self.service('load',[lo,seg],0x2426)
        self.service('animate',[],0x2429)
        self.service('script_free',[],0x242C)
        self.service('staff',[],0x242F)
        r = self.r
        self.les(DATA['resident'])
        self.store(address(r['es'],r['bx'],0x33),1,99)
        self.service('regist',[],0x243B)
        r = self.r
        self.les(DATA['resident'])
        credits = self.byte(r['es'],r['bx'],0x36)
        # Both native comparisons have BYTE width.
        def cmp8(left,right):
            value = (left-right)&255
            self.flags = (self.flags&0x600)|2|logical(value,8)|int(left<right)
            self.flags |= 16 if (left^right^value)&16 else 0
            self.flags |= 0x800 if ((left^right)&(left^value))&128 else 0
        cmp8(credits,3)
        bonus = False
        if credits==3:
            character = self.byte(r['es'],r['bx'],12)
            cmp8(character,15)
            bonus = character<15
        if bonus:
            self.out(0xA6,1)
            self.service('clear',[],0x2458)
            self.out(0xA6,0)
            self.service('clear',[],0x2463)
            self.out(0xA4,0)
            self.push(self.ds)
            self.push(DATA['bonus'])
            self.service('load',[DATA['bonus'],self.ds],0x2470)
            self.service('animate',[],0x2473)
            self.service('script_free',[],0x2476)
        self.service('text_clear',[],0x247B)
        self.service('gaiji',[],0x2480)
        self.far_frame(0x2485,0xC7E)
        self.exit()
        self.push(0,4)
        self.push(self.ds)
        self.push(DATA['op'])
        self.push(self.ds)
        self.push(DATA['op'])
        self.service('execl',[DATA['op'],self.ds,DATA['op'],self.ds,0,0],0x2495)
        self.r['sp'] = self.op(self.r['sp'],12)
        self.r['sp'] = self.r['bp']
        self.pop('bp')
        self.r['sp'] += 2
        return self.full(),self.flags,dict(self.counts,bonus=int(bonus))


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
        self.instructions,self.owner,self.covered = {},set(range(CS*16+START,CS*16+START+SIZE)),set()
        for segment,offset,size in [(CS,START,SIZE),*CONTEXT.values()]:
            start = segment*16+offset
            ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[start:start+size],start))
            need(sum(i.size for i in ins)==size,'complete ending and real helper instruction boundaries')
            self.instructions.update({i.address:i.size for i in ins})
        self.hooks = [self.u.hook_add(UC_HOOK_CODE,self.code),self.u.hook_add(UC_HOOK_MEM_WRITE,self.write),
                      self.u.hook_add(UC_HOOK_INSN,self.out,None,1,0,UC_X86_INS_OUT)]

    def regs(self,full=False):
        values = super().regs(full)
        values.update(fs=self.u.reg_read(UC_X86_REG_FS),gs=self.u.reg_read(UC_X86_REG_GS))
        return values

    def out(self,u,port,size,value,_):
        try:
            self.event(('out',port,size,value,u.reg_read(UC_X86_REG_EFLAGS)&0x200))
        except Exception as error:
            self.fail(error)

    def code(self,u,at,size,_):
        try:
            self.max_depth = max(self.max_depth,self.o['stack']-u.reg_read(REG['sp']))
            if at==self.cs*16+0xFFFF:
                self.returned = True
                u.emu_stop()
                return
            offset = at-self.base
            valid_entry = offset in SERVICES or offset in (0x22B2,*[s*16+a for s,a,_ in CONTEXT.values()])
            if valid_entry and self.index<len(self.events) and self.events[self.index][0]=='far-frame':
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                ip,cs = struct.unpack('<2H',bytes(u.mem_read(address(ss,sp),4)))
                self.event(('far-frame',address(ss,sp),ip,cs))
            if offset==0xC7E*16+0x950:
                e = self.events[self.index]
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                frame = bytes(u.mem_read(address(ss,sp),6)).hex()
                mask = e[-1]
                self.event(('entry','free',self.regs(True),frame,u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
            if offset==0xFEC:
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                self.event(('pi-entry',self.regs(True),bytes(u.mem_read(address(ss,sp),12)).hex()))
            if offset==0xC7E*16+0x37B:
                value = self.o['ticks'][self.polls]
                self.event(('clock',value))
                u.mem_write(address(self.ds,0x144E),struct.pack('<H',value))
                self.polls += 1
            if offset==0x22B2:
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                ip,cs,arg = struct.unpack('<3H',bytes(u.mem_read(address(ss,sp),6)))
                e = self.events[self.index]
                if e[0]=='heap':
                    response = self.o['heap_replies'][self.pi_heaps]
                    self.event(('heap',arg,ip,self.regs(),u.reg_read(UC_X86_REG_EFLAGS)&TEST_FLAGS,response))
                    u.reg_write(REG['ax'],response[0])
                    u.reg_write(UC_X86_REG_EFLAGS,(u.reg_read(UC_X86_REG_EFLAGS)&0x600)|(response[1]&ARITH)|2)
                    self.pi_heaps += 1
                else:
                    mask = e[-1]
                    self.event(('call','free',[arg],self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                    u.reg_write(REG['ax'],self.o['status'])
                    u.reg_write(UC_X86_REG_EFLAGS,(u.reg_read(UC_X86_REG_EFLAGS)&0x600)|(self.o['reply_seed']&ARITH)|2)
                u.reg_write(REG['sp'],sp+6)
                u.reg_write(REG['cs'],cs)
                u.reg_write(REG['ip'],ip)
                return
            if offset in SERVICES:
                name,pop,far = SERVICES[offset]
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                frame_size = 4 if far else 2
                ip = int.from_bytes(u.mem_read(address(ss,sp),2),'little')
                cs = int.from_bytes(u.mem_read(address(ss,sp+2),2),'little') if far else u.reg_read(REG['cs'])
                args = list(struct.unpack('<'+'H'*(pop//2),bytes(u.mem_read(address(ss,sp+frame_size),pop)))) if pop else []
                mask = ARITH|0x600
                self.event(('service',name,args,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                index = self.counts.get(name,0)+1
                self.counts[name] = index
                for role,number,location,raw in self.o['writes']:
                    if (role,number)==(name,index):
                        self.event(('interface-write',location,raw.hex()))
                        u.mem_write(location,raw)
                out,flags = environment(self.regs(),u.reg_read(UC_X86_REG_EFLAGS),self.o['reply_seed']^index,self.o['status'],self.o['clear_df'])
                for n in ('ax','cx','dx','es'):
                    u.reg_write(REG[n],out[n])
                u.reg_write(UC_X86_REG_EFLAGS,flags)
                u.reg_write(REG['sp'],sp+frame_size+(0 if name=='execl' else pop))
                u.reg_write(REG['cs'],cs)
                u.reg_write(REG['ip'],ip)
                return
            need(self.instructions.get(offset)==size,'only ending / actual accepted helpers / declared returning interfaces')
            self.covered.update(range(offset,offset+size))
        except Exception as error:
            self.fail(error)

    def run(self,*,character=1,credits=3,script=(0x200,0x6000),resident=(0x80,0x5000),digits=(48,48),
            segments=(0x1111,0x2222,0x3333),cdg_segments=(0x4444,0x5555),ticks=(0,1,95,96),
            status=0xFFFF,reply_seed=0xA55A,clear_df=False,writes=(),ss=0x7000,stack=0xF800,
            seed=0x1357,flags=0x202,persistent=False):
        need(all(0<=v<=255 for v in (character,credits,*digits)),'BYTE resident and mutable script fixture')
        need(all(0<=v<=65535 for v in (*script,*resident,*segments,*cdg_segments,*ticks,status,reply_seed)), 'WORD pointers/segments/replies')
        need(script[1] in (0x5000,0x6000,self.ds) and resident[1] in (0x5000,0x6000,self.ds),'mapped DATA / foreign pointer fixture')
        need(ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),'foreign SS / incoming flag fixture')
        need(ticks and any(v>=96 for v in ticks),'complete progressing counter fixture')
        need(all(role in BY_NAME and number>=1 and isinstance(raw,bytes) and any(
            lo<=at<at+len(raw)<=hi for lo,hi in ((self.ds*16,self.ds*16+65536),(0x50000,0x70000)))
            for role,number,at,raw in writes),'bounded external DATA writes')
        memory = bytearray(self.u.mem_read(0,1<<20) if persistent else self.initial)
        def write(segment,offset,value,size=2):
            at = address(segment,offset)
            memory[at:at+size] = value.to_bytes(size,'little')
        if not persistent:
            for off,value in zip((2,18),segments):
                write(self.ds,DATA['headers']+off,value)
            write(self.ds,DATA['buffers'],0xFFFE)
            write(self.ds,DATA['buffers']+2,segments[2])
            for slot in range(3):
                for off,value in zip((12,14),cdg_segments):
                    write(self.ds,0x1D0E+slot*16+off,value)
            for off,value in zip((1,2),digits):
                write(script[1],(script[0]+off)&65535,value,1)
        write(self.ds,DATA['script'],script[0]|script[1]<<16,4)
        write(self.ds,DATA['resident'],resident[0]|resident[1]<<16,4)
        write(resident[1],(resident[0]+12)&65535,character,1)
        write(resident[1],(resident[0]+0x36)&65535,credits,1)
        write(ss,stack,0xFFFF)
        self.u.mem_write(0,bytes(memory))
        regs = {n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)}
        regs.update(sp=stack,cs=self.cs,ds=self.ds,es=0x6666,ss=ss,fs=0x3456,gs=0x4567)
        self.high = {n:((seed^0x5AA5)<<16) for n in GPRS}
        for n in GPRS:
            self.u.reg_write(GPRS[n],self.high[n]|regs[n])
        for n in ('cs','ds','es','ss'):
            self.u.reg_write(REG[n],regs[n])
        self.u.reg_write(UC_X86_REG_FS,regs['fs'])
        self.u.reg_write(UC_X86_REG_GS,regs['gs'])
        self.u.reg_write(UC_X86_REG_EFLAGS,flags)
        self.o = dict(load=self.load,stack=stack,status=status,reply_seed=reply_seed,clear_df=clear_df,writes=writes,ticks=ticks,
                      heap_replies=((status,reply_seed&ARITH),)*3)
        spec = Spec(memory,regs,self.high,flags,self.o)
        expected,final,counts = spec.run()
        self.events = spec.events
        self.index,self.error,self.returned,self.max_depth,self.far_word_hooks,self.polls,self.pi_heaps = 0,None,False,0,0,0,0
        self.counts = {}
        try:
            self.u.emu_start(self.cs*16+START,1<<20,count=100000)
        except UcError as error:
            raise ValueError('MAINL ending contract: guest fault') from error
        need(self.error is None,self.error or 'guest failure')
        need(self.returned and self.index==len(self.events),'complete return / ordered requests; no prefix credit')
        need(self.regs(True)==expected,'all DWORD/segment registers '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)==final&(ARITH|0x600),'defined flags / IF / DF')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'complete flat physical memory including all private/caller frames')
        return dict(registers=expected,flags=final&(ARITH|0x600),counts=counts,stack_depth=self.max_depth,polls=self.polls,
            events=len(self.events),trace_sha256=hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest())


def cases(load):
    ds = load+DS
    for character,credits in itertools.product(range(256),(0,2,3,255)):
        yield dict(character=character,credits=credits)
    for credits,character in itertools.product(range(256),(0,14,15,255)):
        yield dict(character=character,credits=credits)
    for digit,which in itertools.product(range(256),(0,1)):
        yield dict(character=255,digits=(digit,0xFF) if which==0 else (0xFF,digit))
    for value,shift in itertools.product(range(256),(0,8)):
        yield dict(script=(value<<shift,0x6000))
        yield dict(resident=(value<<shift,0x5000))
        tick = value<<shift
        yield dict(ticks=(tick,96) if tick<96 else (tick,))
        yield dict(status=value<<shift)
    for flags,clear_df,ss,stack,reply in itertools.product((2,0x202,0x402,0xED7),(False,True),
            (0x7000,0x8000),(0x80,0xF800),(0,0x8D5,0xA55A)):
        yield dict(flags=flags,clear_df=clear_df,ss=ss,stack=stack,reply_seed=reply,character=255)
    for segments,cdg_segments in itertools.product(((0,0,0),(0,0xFFFF,0),(0xFFFF,0,0xFFFF),(1,1,1),(0xFFFF,0xFFFF,0xFFFF)),
            ((0,0),(0,0xFFFF),(0xFFFF,0),(0xFFFF,0xFFFF))):
        yield dict(segments=segments,cdg_segments=cdg_segments)
    for pointer in ((0xFFFF,0x6000),(0,ds),(0xA5D,ds),(0xA5E,ds),(0x21E9,ds)):
        yield dict(character=255,script=pointer)
    for pointer in ((0xFFFF,0x5000),(0,ds),(0x21DE,ds),(0x21B4,ds)):
        yield dict(character=21,resident=pointer)
    for role,character,credits in itertools.product(('staff','regist'),(0,14,15,255),(0,3,255)):
        yield dict(character=255,credits=0,writes=((role,1,0x5008C,bytes([character])),(role,1,0x500B6,bytes([credits]))))
    for role in ('staff','regist'):
        yield dict(writes=((role,1,ds*16+DATA['resident'],struct.pack('<HH',0x80,0x6000)),
                          (role,1,0x6008C,b'\x0E'),(role,1,0x600B6,b'\x03')))
    yield dict(writes=(('show',1,ds*16+DATA['script'],struct.pack('<HH',0xFFFF,0x6000)),))


def verify(target,candidate):
    observations = []
    expected_context = {a for s,o,n in CONTEXT.values() for a in range(s*16+o,s*16+o+n)}
    for image_index,image in enumerate((target,candidate),1):
        rows = []
        for load in (0x1000,0x3000):
            m = Machine(image,load)
            trace = hashlib.sha256()
            maximum,bonus,ports,polls = 0,0,0,0
            try:
                for count,parameters in enumerate(cases(load),1):
                    result = m.run(**parameters)
                    maximum = max(maximum,result['stack_depth'])
                    bonus += result['counts']['bonus']
                    ports += sum(e[0]=='out' for e in m.events)
                    polls += result['polls']
                    trace.update(json.dumps(result,sort_keys=True).encode())
                    if count%512==0:
                        print(f'Ending: image {image_index}, load {load:04X}, {count} complete entries',flush=True)
                for index,character in enumerate((21,255,0,14)):
                    result = m.run(character=character,persistent=index>0)
                    count += 1
                    maximum = max(maximum,result['stack_depth'])
                    bonus += result['counts']['bonus']
                    ports += sum(e[0]=='out' for e in m.events)
                    polls += result['polls']
                    trace.update(json.dumps(result,sort_keys=True).encode())
                need(m.owner<=m.covered and expected_context<=m.covered,'all280 ending and227 actual helper bytes execute')
                rows.append(dict(load_segment=load,cases=count,executed_owner_bytes=SIZE,actual_helper_bytes=227,
                    maximum_stack_depth=maximum,bonus_entries=bonus,byte_port_requests=ports,counter_polls=polls,
                    trace_sha256=trace.hexdigest()))
                print(f'Ending: image {image_index}, load {load:04X}, {count} entries / 280 owner bytes pass',flush=True)
            finally:
                m.close()
        observations.append(rows)
    need(observations[0]==observations[1],'independent target/candidate full-state observations')
    return dict(images=2,functions=1,code_bytes=SIZE,executed_owner_bytes=SIZE,cases_per_image=sum(r['cases'] for r in observations[0]),
        observations=observations[0],ignored_stack_bytes=0,actual_owned_nested_helpers=True,
        actual_helper_bytes=227,complete_near_return=True,flat_memory_operand_contract=True,
        interface_bodies_or_assets_owned=False,physical_IRQ_graphics_exec_proved=False)


def negative_controls(target):
    controls = (
        ('ending-local-frame',0x2383,2,{}),('first-free-slot',0x2387,1,{}),
        ('second-free-slot',0x238E,1,{}),('third-free-slot',0x2395,1,{}),
        ('PI-header-pointer',0x239D,2,{}),('PI-buffer-DWORD',0x23A2,4,{}),
        ('resident-character-field',0x23B0,1,{}),('character-decrement',0x23B3,1,dict(character=21)),
        ('character-half',0x23B8,8,dict(character=255)),('signed-BYTE-tens-compare',0x23BF,1,dict(character=21)),
        ('tens-branch',0x23C0,1,dict(character=255)),('tens-position',0x23C9,1,dict(character=255)),
        ('decimal-divisor',0x23D0,1,dict(character=255)),('tens-addition',0x23D7,8,dict(character=255)),
        ('tens-store-position',0x23DF,1,dict(character=255)),('ones-divisor',0x23E5,1,dict(character=255)),
        ('ones-remainder',0x23EC,1,dict(character=255)),('ones-store-position',0x23F7,1,dict(character=255)),
        ('palette-tone-zero',0x23FC,1,{}),('delay-96',0x2404,1,{}),('initial-page',0x240E,1,{}),
        ('initial-show-page-port',0x2411,2,{}),('script-far-pointer',0x2421,4,{}),
        ('story-stage',0x2437,1,{}),('credit-compare',0x2443,1,{}),('credit-branch',0x2444,1,{}),
        ('bonus-character-limit',0x244A,1,dict(character=29)),('bonus-character-branch',0x244B,1,dict(character=255)),
        ('bonus-first-page',0x2451,1,{}),('bonus-script-name',0x246B,2,{}),('OP-name-first',0x248A,2,{}),
        ('OP-name-second',0x248E,2,{}),('execl-null-DWORD',0x2487,1,{}),('cdecl-cleanup',0x2497,2,{}),
        ('near-return',0x2499,8,{}))
    helper_controls = (('actual-CDG-free-clear',0xC7E*16+0x981,1,{}),
        ('actual-PI-free-clear',0x1005,2,{}),('actual-delay-reset',0xC7E*16+0x379,1,{}),
        ('actual-exit-page-order',0xC7E*16+0x1BC,1,{}))
    rejected = []
    for name,at,xor,parameters in (*[(n,CS*16+a,x,p) for n,a,x,p in controls],*helper_controls):
        raw = bytearray(target.program_image)
        raw[at] ^= xor
        m = None
        try:
            m = Machine(replace(target,program_image=bytes(raw)),0x1000)
            m.run(**parameters)
        except (ValueError,UcError):
            rejected.append(name)
        else:
            raise ValueError('MAINL ending actual instruction mutation escaped: '+name)
        finally:
            if m:
                m.close()
    return dict(count=len(rejected),rejected=rejected,owner_instruction_mutations=len(controls),
                actual_helper_instruction_mutations=len(helper_controls),actual_guest_mutations=True)
