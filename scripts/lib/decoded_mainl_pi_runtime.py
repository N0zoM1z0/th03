"""Full physical PI caller contracts with real PI_FREE and CRT memcpy context.

Graphics, decoder and heap replies are bounded interfaces, not device/allocator
execution. Interfaces preserve SI/DI/BP/DS/SS and DWORD high halves; selected
WORD scratch registers, arithmetic flags and DF replies are explicit fixtures.
"""
import hashlib
import itertools
import json
import struct
from dataclasses import replace
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import *
from lib.decoded_mainl_pi_layout import CS, DS, DATA, CALLS, ENTRIES
from lib.decoded_mainl_pi_free_runtime import specification as free_spec, REPLIES, TEST_FLAGS, address
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG, logical

ARITH = 0x8D5
CONTEXT = ((0xFEC, 76), (0x4B7D, 36))


def need(value, message):
    if not value:
        raise ValueError('MAINL PI contract: ' + str(message))


def signed(value):
    return value - 65536 if value & 0x8000 else value


def arithmetic(left, right, subtract=False):
    value = (left - right if subtract else left + right) & 65535
    carry = left < right if subtract else left + right > 65535
    overflow = ((left ^ right) & (left ^ value) if subtract else ~(left ^ right) & (left ^ value)) & 0x8000
    return value, logical(value, 16) | int(carry) | (16 if (left ^ right ^ value) & 16 else 0) | (0x800 if overflow else 0)


def reply(regs, flags, seed, status, clear_df):
    out = dict(regs)
    out.update(ax=status, bx=seed ^ 0xA55A, cx=seed ^ 0x1234, dx=seed ^ 0x5AA5, es=0x6000)
    return out, (flags & 0x600 & (0x200 if clear_df else 0x600)) | (seed & ARITH) | 2


class Spec:
    """Source-level row recurrence plus independently predicted native ABI frames."""
    def __init__(self, memory, regs, high, flags, options):
        self.memory, self.r, self.high = memory, dict(regs), dict(high)
        self.flags, self.o, self.events, self.counts = flags, options, [], {}
        self.s, self.ss = regs['sp'], regs['ss']
        self.ds = regs['ds']

    def word(self, segment, offset):
        at = address(segment, offset)
        return int.from_bytes(self.memory[at:at+2], 'little')

    def store(self, at, size, value):
        self.events.append(('store', at, size, value))
        self.memory[at:at+size] = value.to_bytes(size, 'little')

    def push(self, value, size=2):
        self.r['sp'] -= size
        self.store(address(self.ss, self.r['sp']), size, value)

    def pop(self, name):
        self.r[name] = self.word(self.ss, self.r['sp'])
        self.r['sp'] += 2

    def enter(self, locals_size=0):
        self.push(self.r['bp'])
        self.r['bp'] = self.r['sp']
        self.r['sp'] -= locals_size

    def frame(self, continuation):
        self.r['sp'] -= 4
        at = address(self.ss,self.r['sp'])
        self.memory[at:at+4] = struct.pack('<2H',continuation,self.r['cs'])
        # Unicorn's far CALL helper may omit either word's write hook. Check
        # both native return words at callee entry, before its first instruction.
        self.events.append(('far-frame',at,continuation,self.r['cs']))
        self.r['cs'] = self.o['load']

    def returned(self, cleanup):
        sp = self.r['sp']
        self.r['cs'] = self.word(self.ss, sp+2)
        self.r['sp'] += 4 + cleanup

    def full(self):
        return {n: self.high[n] | self.r[n] if n in GPRS else self.r[n] for n in self.r}

    def call(self, kind, args, continuation, cleanup, mask):
        self.frame(continuation)
        self.events.append(('call', kind, args, self.full(), self.flags & mask, mask))
        index = self.counts.get(kind, 0) + 1
        self.counts[kind] = index
        for call_kind, call_index, at, raw in self.o['writes']:
            if (call_kind, call_index) == (kind, index):
                self.events.append(('interface-write', at, raw.hex()))
                self.memory[at:at+len(raw)] = raw
        self.r, self.flags = reply(self.r, self.flags, self.o['reply_seed'], self.o['status'], self.o['clear_df'])
        self.returned(cleanup)

    def flag_operation(self, left, right, subtract=False):
        value, flags = arithmetic(left, right, subtract)
        self.flags = (self.flags & 0x600) | flags | 2
        return value

    def normalize(self, offset, segment):
        # Truncate the WORD addition before paragraph normalization. EAX's high
        # half becomes zero through the real DWORD load/SHR 16, unlike EDX.
        offset &= 65535
        segment = (segment + (offset >> 4)) & 65535
        offset &= 15
        self.high['ax'] = 0
        self.r.update(ax=segment, dx=offset)
        self.flags = (self.flags & 0x600) | logical(offset,16) | 2
        self.store(address(self.ss,self.s-4),2,segment)
        self.store(address(self.ss,self.s-6),2,offset)
        return offset, segment

    def finish(self, args):
        self.r['sp'] = self.r['bp']
        self.pop('bp')
        self.returned(args)

    def run(self, kind):
        o, r = self.o, self.r
        slot = o['slot']
        header, buffer = (DATA['_pi_headers']+slot*72)&65535, (DATA['_pi_buffers']+slot*4)&65535
        if kind == 'load':
            self.enter(2)
            self.push(r['si'])
            r['si'] = slot
            r['ax'] = header
            self.push(self.ds)
            self.push(header)
            r['bx'] = (slot*4)&65535
            pointer = self.word(self.ds,buffer) | self.word(self.ds,(buffer+2)&65535)<<16
            self.push(pointer,4)
            self.frame(0xCEC)
            # Compose the accepted release's scalar contract on this memory and
            # frame, while the guest executes its actual instructions on one UC.
            out, flags, _, events, count = free_spec(self.memory,self.r,self.flags,REPLIES)
            self.events.extend(events)
            self.counts['heap'] = count
            self.r = r = out
            self.flags = flags
            r['cs'] = o['load']+CS
            self.push(o['filename'][0] | o['filename'][1]<<16,4)
            r['ax'] = header
            self.push(self.ds)
            self.push(header)
            r['ax'] = self.flag_operation((slot*4)&65535,DATA['_pi_buffers'])
            self.push(self.ds)
            self.push(buffer)
            self.call('decoder',[buffer,self.ds,header,self.ds,*o['filename']],0xD09,12,ARITH|0x600)
            self.store(address(self.ss,self.s-4),2,self.r['ax'])
            self.pop('si')
            self.finish(6)
        elif kind == 'palette':
            self.enter()
            self.push(48)
            self.push(self.ds)
            r['ax'] = self.flag_operation((slot*72)&65535,DATA['_pi_headers']+24)
            source = r['ax']
            self.push(source)
            self.push(self.ds)
            self.push(DATA['_Palettes'])
            self.frame(0x543)
            self.enter()
            self.push(r['si'])
            self.push(r['di'])
            for i in range(24):
                self.store(address(self.ds,DATA['_Palettes']+2*i),2,self.word(self.ds,(source+2*i)&65535))
            r.update(dx=self.ds,ds=self.ds,es=self.ds,cx=0,ax=DATA['_Palettes'])
            self.flags = (self.flags & 0x200) | 2 | logical(24,16)
            self.pop('di')
            self.pop('si')
            self.pop('bp')
            self.returned(0)
            r['sp'] = self.flag_operation(r['sp'],10)
            self.call('show',[],0x54B,0,ARITH|0x600)
            self.pop('bp')
            self.returned(2)
        else:
            self.enter(6)
            self.push(r['si'])
            self.push(r['di'])
            r.update(si=o['top'],di=o['quarter'] if kind=='quarter' else slot,bx=(slot*4)&65535)
            offset, segment = self.word(self.ds,buffer), self.word(self.ds,(buffer+2)&65535)
            r.update(ax=segment,dx=offset)
            self.store(address(self.ss,self.s-4),2,segment)
            self.store(address(self.ss,self.s-6),2,offset)
            if kind == 'quarter':
                delta = {1:160,2:64000,3:64160}.get(o['quarter'],0)
                if delta:
                    offset = (offset+delta)&65535
                    self.store(address(self.ss,self.s-6),2,offset)
                offset, segment = self.normalize(offset,segment)
            self.store(address(self.ss,self.s-8),2,0)
            counter = 0
            rows = 0
            while True:
                if o['prefix'] and rows == o['prefix']:
                    break  # Before the native guard, not at a budget expiry.
                height = 200 if kind=='quarter' else self.word(self.ds,(header+22)&65535)
                if kind == 'quarter':
                    self.flag_operation(counter,200,True)
                else:
                    self.r.update(ax=height,bx=(slot*72)&65535)
                    self.flag_operation(height,counter,True)
                if counter >= height:
                    break
                width = 320 if kind=='quarter' else self.word(self.ds,(header+20)&65535)
                self.push(o['left'])
                self.push(self.r['si'])
                self.push(offset | segment<<16,4)
                if kind != 'quarter':
                    self.r['bx'] = (slot*72)&65535
                    product = signed(slot)*72
                    overflow = product < -32768 or product > 32767
                    self.flags = (self.flags & ~0x801) | (0x801 if overflow else 0)
                self.push(width)
                continuation = {'put':0x58B,'interlace':0x613,'quarter':0xD86}[kind]
                self.call('packed',[width,offset,segment,self.r['si'],o['left']],continuation,10,0xE01)
                r = self.r
                top = (r['si']+1)&65535
                if signed(top) >= 400:
                    top = (top-400)&65535
                r['si'] = top
                if kind != 'quarter':
                    r['bx'] = (slot*72)&65535
                    width = self.word(self.ds,(header+20)&65535)
                delta = width//2 if kind=='put' else width
                offset = (offset+delta)&65535
                self.store(address(self.ss,self.s-6),2,offset)
                offset, segment = self.normalize(offset,segment)
                step = 2 if kind=='interlace' else 1
                counter = self.flag_operation(counter,step)
                self.store(address(self.ss,self.s-8),2,counter)
                rows += 1
            self.counts['rows'] = rows
            if not o['prefix']:
                self.pop('di')
                self.pop('si')
                self.finish(8 if kind=='quarter' else 6)
        return self.full(), self.flags, self.events, self.counts


class Machine:
    def __init__(self, image, load):
        need(image.valid, 'valid decoded MZ')
        self.load, self.base = load, load*16
        self.cs, self.ds = load+CS, load+DS
        self.u = Uc(UC_ARCH_X86,UC_MODE_16)
        self.u.mem_map(0,1<<20)
        memory = bytearray(b'\xA5'*(1<<20))
        raw = image.relocated_program_image(load)
        memory[self.base:self.base+len(raw)] = raw
        self.initial = bytes(memory)
        self.instructions = {}
        self.owner = set()
        for start, size, *_ in ENTRIES.values():
            self.owner.update(range(start,start+size))
        for start,size in [(s,n) for s,n,_ in ENTRIES.values()]+list(CONTEXT):
            ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[start:start+size],start))
            need(sum(i.size for i in ins)==size,'complete owner/context instruction boundaries')
            self.instructions.update({i.address:i.size for i in ins})
        self.covered = set()
        self.hooks = [self.u.hook_add(UC_HOOK_CODE,self.code), self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)]

    def close(self):
        for hook in self.hooks:
            self.u.hook_del(hook)
        self.hooks = []
        self.u = None

    def regs(self, full=False):
        return {n:self.u.reg_read(GPRS[n] if full and n in GPRS else REG[n]) for n in REG if n!='ip'}

    def event(self, event):
        need(self.index<len(self.events) and event==self.events[self.index],
             f'event {self.index}: {event}; expected {self.events[self.index:self.index+1]}')
        self.index += 1

    def fail(self, error):
        self.error = str(error)
        self.u.emu_stop()

    def code(self, u, at, size, _):
        try:
            self.max_depth = max(self.max_depth,self.o['stack']-u.reg_read(REG['sp']))
            if at-self.base in CALLS.values() and self.index < len(self.events) and self.events[self.index][0]=='far-frame':
                sp, ss = u.reg_read(REG['sp']), u.reg_read(REG['ss'])
                ip, cs = struct.unpack('<2H',bytes(u.mem_read(address(ss,sp),4)))
                self.event(('far-frame',address(ss,sp),ip,cs))
                self.far_frames += 1
            if at == self.cs*16+0xFFFF:
                self.returned = True
                u.emu_stop()
                return
            if self.o['prefix'] and at == self.cs*16+0x64A and self.counts.get('packed',0)==self.o['prefix']:
                self.stopped_prefix = True
                u.emu_stop()
                return
            offset = at-self.base
            if offset in (CALLS['GRAPH_PACK_PUT_8'],CALLS['GRAPH_PI_LOAD_PACK'],CALLS['PALETTE_SHOW'],0x22B2):
                sp, ss = u.reg_read(REG['sp']), u.reg_read(REG['ss'])
                ip, cs = struct.unpack('<2H',bytes(u.mem_read(address(ss,sp),4)))
                if offset == 0x22B2:
                    segment = int.from_bytes(u.mem_read(address(ss,sp+4),2),'little')
                    index = self.counts.get('heap',0)
                    response = REPLIES[index]
                    self.event(('heap',segment,ip,self.regs(),u.reg_read(UC_X86_REG_EFLAGS)&TEST_FLAGS,response))
                    need(all(u.reg_read(GPRS[n])==self.high[n]|self.regs()[n] for n in GPRS),'heap preserves enclosing high halves')
                    u.reg_write(REG['ax'],response[0])
                    u.reg_write(UC_X86_REG_EFLAGS,(u.reg_read(UC_X86_REG_EFLAGS)&0x600)|(response[1]&ARITH)|2)
                    kind, cleanup = 'heap', 2
                else:
                    kind, cleanup = {CALLS['GRAPH_PACK_PUT_8']:('packed',10),CALLS['GRAPH_PI_LOAD_PACK']:('decoder',12),CALLS['PALETTE_SHOW']:('show',0)}[offset]
                    args = list(struct.unpack('<'+'H'*(cleanup//2),bytes(u.mem_read(address(ss,sp+4),cleanup)))) if cleanup else []
                    expected = self.events[self.index]
                    need(expected[:2]==('call',kind),'declared interface call order')
                    mask = expected[-1]
                    self.event(('call',kind,args,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                    call_index = self.counts.get(kind,0)+1
                    for call_kind, index, address_, raw in self.o['writes']:
                        if (call_kind,index)==(kind,call_index):
                            self.event(('interface-write',address_,raw.hex()))
                            u.mem_write(address_,raw)
                    out, flags = reply(self.regs(),u.reg_read(UC_X86_REG_EFLAGS),self.o['reply_seed'],self.o['status'],self.o['clear_df'])
                    for name in ('ax','bx','cx','dx','es'):
                        u.reg_write(REG[name],out[name])
                    u.reg_write(UC_X86_REG_EFLAGS,flags)
                self.counts[kind] = self.counts.get(kind,0)+1
                u.reg_write(REG['sp'],sp+4+cleanup)
                u.reg_write(REG['cs'],cs)
                u.reg_write(REG['ip'],ip)
                return
            need(self.instructions.get(offset)==size,'only actual owner/PI_FREE/memcpy instructions and declared interfaces')
            self.covered.update(range(offset,offset+size))
            self.max_depth = max(self.max_depth,self.o['stack']-u.reg_read(REG['sp']))
        except Exception as error:
            self.fail(error)

    def write(self,u,access,at,size,value,_):
        try:
            if self.index < len(self.events) and self.events[self.index][0]=='far-frame':
                _, wanted, ip, cs = self.events[self.index]
                if (at,size,value) in ((wanted,2,ip),(wanted+2,2,cs)):
                    self.far_word_hooks += 1
                    return  # The full frame is checked at the very next entry.
            self.event(('store',at,size,value))
        except Exception as error:
            self.fail(error)

    def run(self, kind, *, slot=0, width=640, height=3, pointer=(0xFFFE,0x5000),
            left=0xFFF9, top=399, quarter=0, segments=(0x1111,0x2222), filename=(0xFFFF,0x6000),
            status=0xFFFF, reply_seed=0xA55A, clear_df=False, writes=(), prefix=0,
            ss=0x7000, stack=0xF800, seed=0x1357, flags=0x202, persistent=False):
        need(kind in ENTRIES and all(0<=v<=65535 for v in (slot,width,height,*pointer,left,top,quarter,*segments,*filename,status,reply_seed)), 'bounded WORD fixtures')
        need(ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),'bounded flags / foreign SS')
        need(not prefix or kind=='interlace' and height==0xFFFF and prefix in (1,4,7) and not writes,'proved readonly FFFF interlace prefix')
        need(all(k in ('packed','show','decoder') and i>=1 and isinstance(raw,bytes) and self.ds*16<=at<at+len(raw)<=self.ds*16+65536 for k,i,at,raw in writes),'bounded explicit interface DATA writes')
        memory = bytearray(self.u.mem_read(0,1<<20) if persistent else self.initial)
        header, buffer = (DATA['_pi_headers']+slot*72)&65535, (DATA['_pi_buffers']+slot*4)&65535
        if not persistent:
            for i in range(72):
                memory[address(self.ds,header,i)] = (seed+i*37)&255
            for off,value in ((2,segments[0]),(18,segments[1]),(20,width),(22,height)):
                at = address(self.ds,header,off)
                memory[at:at+2] = struct.pack('<H',value)
            for off,value in ((0,pointer[0]),(2,pointer[1])):
                at = address(self.ds,buffer,off)
                memory[at:at+2] = struct.pack('<H',value)
        if kind=='interlace' and int.from_bytes(memory[address(self.ds,header,22):address(self.ds,header,22)+2],'little')==0xFFFF and not prefix:
            at = address(self.ds,header,22)
            need(any(k=='packed' and i==1 and target==at and len(raw)==2 and raw!=b'\xff\xff' for k,i,target,raw in writes),
                 'readonly FFFF interlace needs its explicit proved prefix')
        args = [slot] if kind=='palette' else [*filename,slot] if kind=='load' else [quarter,slot,top,left] if kind=='quarter' else [slot,top,left]
        frame = struct.pack('<'+'H'*(len(args)+2),0xFFFF,self.cs,*args)
        memory[address(ss,stack):address(ss,stack)+len(frame)] = frame
        self.u.mem_write(0,bytes(memory))
        regs = {n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)}
        regs.update(sp=stack,cs=self.cs,ds=self.ds,es=0x6666,ss=ss)
        self.high = {n:((seed^0x5AA5)<<16) for n in GPRS}
        for n in GPRS:
            self.u.reg_write(GPRS[n],self.high[n]|regs[n])
        for n in ('cs','ds','es','ss'):
            self.u.reg_write(REG[n],regs[n])
        self.u.reg_write(UC_X86_REG_FS,0x3456)
        self.u.reg_write(UC_X86_REG_GS,0x4567)
        self.u.reg_write(UC_X86_REG_EFLAGS,flags)
        self.o = dict(load=self.load,slot=slot,top=top,left=left,quarter=quarter,filename=filename,
                      reply_seed=reply_seed,status=status,clear_df=clear_df,writes=writes,prefix=prefix,stack=stack)
        spec = Spec(memory,regs,self.high,flags,self.o)
        expected, final, self.events, counts = spec.run(kind)
        self.index,self.error,self.returned,self.stopped_prefix,self.counts,self.max_depth = 0,None,False,False,{},0
        self.far_frames,self.far_word_hooks = 0,0
        try:
            self.u.emu_start(self.base+ENTRIES[kind][0],1<<20,count=10000000)
        except UcError as error:
            raise ValueError('MAINL PI contract: guest fault') from error
        need(self.error is None,self.error or 'guest error')
        need(self.stopped_prefix if prefix else self.returned,'explicit native return or proved guard prefix, never budget exhaustion')
        need(self.index==len(self.events),'complete ordered events')
        need(self.regs(True)==expected,'all DWORD/WORD/segment state '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)==final&(ARITH|0x600),'defined flags / IF / DF')
        need((self.u.reg_read(UC_X86_REG_FS),self.u.reg_read(UC_X86_REG_GS))==(0x3456,0x4567),'FS/GS preserved')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'all physical memory including native private stack and caller bytes')
        digest = hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest()
        return dict(kind=kind,registers=expected,flags=final&(ARITH|0x600),events=len(self.events),events_sha256=digest,
                    counts=counts,stack_depth=self.max_depth,nonterminal=bool(prefix),
                    checked_far_frames=self.far_frames,far_return_WORD_write_hooks=self.far_word_hooks)


def closed_prefix_proof(image):
    start, size, _ = ENTRIES['interlace']
    raw = image.program_image[start:start+size]
    ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(raw,0x5D7))
    need(sum(i.size for i in ins)==135,'complete interlace CFG')
    edges = [(i.address,i.mnemonic,i.op_str) for i in ins if i.mnemonic.startswith('j') or i.mnemonic in ('lcall','call','retf','int','loop')]
    need(edges==[(0x5FB,'jmp','0x64a'),(0x60E,'lcall','0, 0x1632'),(0x618,'jl','0x61e'),
                 (0x656,'ja','0x5fd'),(0x65B,'retf','6')], 'closed body / reconverging top branch / sole unsigned exit')
    by = {i.address:i for i in ins}
    need(bytes(by[0x5F6].bytes)==b'\xc7\x46\xfa\0\0' and bytes(by[0x646].bytes)==b'\x83\x46\xfa\x02'
         and bytes(by[0x64F].bytes)==b'\x8b\x87\x3c\x1f' and bytes(by[0x653].bytes)==b'\x3b\x46\xfa',
         'zero WORD initializer / plus-two update / live readonly height guard')
    writes = [(i.address,i.mnemonic) for i in ins if i.op_str.startswith('word ptr [bp - 6],')]
    need(writes==[(0x5F6,'mov'),(0x646,'add')],'only two native counter definitions')
    evens = set(range(0,65536,2))
    need({(v+2)&65535 for v in evens}==evens and all(0xFFFF>v for v in evens),'inductive even WORD cycle always takes JA')
    return dict(entry=0x5D7,guard=0x64A,backedge=0x656,body=0x5FD,counter_initializer=0,counter_step=2,
                invariant_counter_states=32768,readonly_height=65535,only_exit_guard_always_taken=True,
                native_CFG_proved=True,budget_expiry_used=False,
                assumptions=['packed interface returns preserving SI/DI/BP/DS/SS and high halves',
                             'header height remains FFFF; no interface DATA writes',
                             'DGROUP and private stack fixtures are disjoint'],
                live_invariant=['WORD counter remains even','balanced row-call frame at each guard',
                                'offset below 16 after each row; segment and top remain WORDs',
                                'DI slot, DS, SS, BP and caller return words remain fixed'])


def cases(load):
    ds = (load+DS)*16
    slots = (0,1,3,7,0x100,0x1000,0x8000,0xFFFF)
    for kind,slot,flags,ss in itertools.product(ENTRIES,slots,(2,0x202,0x402,0xED7),(0x7000,0x8000)):
        yield kind,dict(slot=slot,flags=flags,ss=ss)
    for kind,width,height,pointer in itertools.product(('put','interlace'),(0,1,2,3,319,320,639,640,0x8000,0xFFFF),
                                                      (0,1,2,3,7),((0,0xFFFF),(0xFFFE,0x5000),(0xFFFF,0))):
        yield kind,dict(width=width,height=height,pointer=pointer)
    for kind,shift,value in itertools.product(('palette','load'),(0,8),range(256)):
        yield kind,dict(slot=value<<shift)
    for kind,shift,value in itertools.product(('put','interlace'),(0,8),range(256)):
        yield kind,dict(top=value<<shift,height=2,left=(value*257)&65535)
    for top,quarter in itertools.product((0,398,399,400,401,0x7FFF,0x8000,0xFFFF),(0,1,2,3,0x100,0xFFFF)):
        yield 'quarter',dict(top=top,quarter=quarter,left=top^0x8000,pointer=(0xFFFF,0xFFF0),width=1,height=0)
    for kind,slot,height in itertools.product(('put','interlace'),slots,(0x7FFF,0x8000,0xFFFE,0xFFFF)):
        header = (DATA['_pi_headers']+slot*72)&65535
        yield kind,dict(slot=slot,height=height,writes=(('packed',1,ds+((header+22)&65535),b'\0\0'),
                                                    ('packed',1,ds+((header+20)&65535),b'\xff\xff')))
    for prefix,width,flags,ss in itertools.product((1,4,7),(0,1,0xFFFF),(2,0x202,0x402,0xED7),(0x7000,0x8000)):
        yield 'interlace',dict(height=0xFFFF,prefix=prefix,width=width,flags=flags,ss=ss)
    # All source/destination starts are congruent modulo eight. These native
    # forward word copies include overlapping propagation and SI offset wrap.
    for delta in (-40,-16,-8,0,8,16,40):
        slot = (((DATA['_Palettes']-(DATA['_pi_headers']+24)+delta)//8)*pow(9,-1,8192))&8191
        yield 'palette',dict(slot=slot,flags=0xED7)
    for source in (0xFFF6,0xFFFE):
        slot = (((source-(DATA['_pi_headers']+24))//8)*pow(9,-1,8192))&8191
        yield 'palette',dict(slot=slot,flags=0x402)
    for mask,status,flags in itertools.product(range(8),(0,7,0xFFFF),(2,0x202,0x402,0xED7)):
        yield 'load',dict(segments=tuple(0xFFFF if mask&(1<<i) else 0 for i in (0,1)),
                          pointer=(0xFFFF,0x8000 if mask&4 else 0),status=status,flags=flags)
    for kind in ('put','interlace'):
        for width in (0,1,0xFFFF):
            yield kind,dict(height=4,width=width,writes=(('packed',1,ds+DATA['_pi_headers']+20,b'\x03\0'),
                ('packed',1,ds+DATA['_pi_buffers'],b'\x34\x12\x67\x45')),clear_df=True)


def verify(target,candidate):
    proof = closed_prefix_proof(target)
    need(proof==closed_prefix_proof(candidate),'both complete native closed CFGs')
    results = []
    for image in (target,candidate):
        rows = []
        for load in (0x1000,0x3000):
            machine = Machine(image,load)
            trace = hashlib.sha256()
            counts = {k:0 for k in ENTRIES}
            prefixes = 0
            maximum = 0
            far_frames = 0
            try:
                for count,(kind,parameters) in enumerate(cases(load),1):
                    p = dict(seed=0x1357 if count&1 else 0xECA8,stack=0x80 if count&1 else 0xF800,
                             reply_seed=0xA55A if count&1 else 0x5AA5,clear_df=not bool(count&1))
                    p.update(parameters)
                    r = machine.run(kind,**p)
                    counts[kind] += 1
                    prefixes += r['nonterminal']
                    maximum = max(maximum,r['stack_depth'])
                    far_frames += r['checked_far_frames']
                    # Hook availability is an emulator/TB detail. Every actual
                    # frame is checked immediately; it is not an ABI observation.
                    r.pop('far_return_WORD_write_hooks')
                    trace.update(json.dumps(r,sort_keys=True).encode())
                for index in range(3):
                    buffer = machine.ds*16+DATA['_pi_buffers']
                    r = machine.run('load',persistent=index>0,writes=(('decoder',1,buffer,b'\x07\0\0\x50'),))
                    count += 1
                    counts['load'] += 1
                    far_frames += r['checked_far_frames']
                    r.pop('far_return_WORD_write_hooks')
                    trace.update(json.dumps(r,sort_keys=True).encode())
                need(machine.covered & machine.owner == machine.owner,'all 555 owner bytes execute')
                need(set(range(0xFEC,0x1038))<=machine.covered,'all 76 real nested release bytes execute')
                library = machine.covered & set(range(0x4B7D,0x4BA1))
                need(library==set(range(0x4B7D,0x4BA1))-{0x4B94},'35 real memcpy context bytes; fixed even count excludes MOVSB')
                rows.append(dict(load_segment=load,cases=count,cases_by_function=counts,nonterminal_prefixes=prefixes,
                    executed_owner_bytes=555,nested_release_bytes=76,library_context_bytes=35,
                    maximum_stack_depth=maximum,checked_far_frames=far_frames,trace_sha256=trace.hexdigest()))
                print(f'PI contracts: load {load:04X}, {count} cases, all 555 owner bytes',flush=True)
            finally:
                machine.close()
        results.append(rows)
    need(results[0]==results[1],'complete target/candidate observations including nested physical state')
    return dict(images=2,functions=5,code_bytes=555,executed_owner_bytes=555,
                cases_per_image=sum(o['cases'] for o in results[0]),observations=results[0],closed_interlace_prefix=proof,
                ignored_stack_bytes=0,heap_decoder_or_pixels_executed=False,
                far_return_words_checked_at_entry=True,library_context_accepted=False)


def negative_controls(target):
    # Actual guest changes; ordinary library context is counted separately.
    controls = (
        ('palette-slot-scale',0x535,1,'palette',dict(slot=1)),
        ('palette-source-field',0x537,2,'palette',{}),('palette-destination',0x53C,2,'palette',{}),
        ('palette-copy-count',0x52E,2,'palette',{}),('palette-caller-cleanup',0x545,2,'palette',{}),
        ('palette-Pascal-cleanup',0x54D,2,'palette',{}),
        ('put-slot-argument',0x55A,2,'put',dict(slot=1)),('put-buffer-segment',0x562,2,'put',{}),
        ('put-buffer-offset',0x566,2,'put',{}),('put-initial-counter',0x571,1,'put',{}),
        ('put-width-field',0x584,2,'put',{}),('put-call-destination',0x587,1,'put',{}),
        ('put-signed-top',0x591,4,'put',dict(top=0x7FFF)),('put-half-width',0x5A0,8,'put',dict(width=3)),
        ('put-truncate-before-normalizing',0x5A2,2,'put',{}),('put-DWORD-shift',0x5AB,1,'put',{}),
        ('put-paragraph-shift',0x5B1,1,'put',{}),('put-offset-mask',0x5B9,1,'put',dict(pointer=(0xFFFF,0x5000))),
        ('put-counter-increment',0x5C1,8,'put',{}),('put-unsigned-height',0x5CF,0x08,'put',dict(height=0x8000,
             writes=(('packed',1,0x10000+DS*16+DATA['_pi_headers']+22,b'\0\0'),))),
        ('interlace-top-step',0x613,8,'interlace',{}),('interlace-full-width',0x628,2,'interlace',{}),
        ('interlace-counter-step',0x649,1,'interlace',{}),('interlace-height-field',0x651,2,'interlace',{}),
        ('interlace-closed-cycle-parity',0x649,1,'interlace',dict(height=0xFFFF,prefix=4)),
        ('load-slot-argument',0xCD2,2,'load',dict(slot=1)),('load-header-scale',0xCD7,1,'load',dict(slot=1)),
        ('load-header-pointer',0xCD9,2,'load',{}),('load-image-pointer',0xCE5,2,'load',{}),
        ('load-release-call',0xCE8,1,'load',{}),('load-filename-pointer',0xCEF,2,'load',{}),
        ('load-decoder-header',0xCF6,2,'load',{}),('load-decoder-output',0xD00,2,'load',{}),
        ('load-result-store',0xD0B,2,'load',{}),('load-Pascal-cleanup',0xD0F,2,'load',{}),
        ('quarter-selector-argument',0xD1C,2,'quarter',dict(quarter=1)),
        ('quarter-one-offset',0xD39,1,'quarter',dict(quarter=1)),
        ('quarter-two-offset',0xD45,1,'quarter',dict(quarter=2)),
        ('quarter-three-offset',0xD51,1,'quarter',dict(quarter=3)),
        ('quarter-normalize-first',0xD60,1,'quarter',{}),('quarter-fixed-width',0xD7F,1,'quarter',{}),
        ('quarter-top-step',0xD86,8,'quarter',{}),('quarter-signed-wrap',0xD8C,4,'quarter',dict(top=0x7FFF)),
        ('quarter-row-stride',0xD94,1,'quarter',{}),('quarter-fixed-200',0xDB8,1,'quarter',{}),
        ('quarter-Pascal-cleanup',0xDC0,2,'quarter',{}),
        ('nested-release-clear',0x1005,2,'load',{}),
        ('memcpy-real-CLD',0x4B8F,1,'palette',dict(flags=0xED7)),
        ('memcpy-word-copy',0x4B91,1,'palette',{}))
    rejected = []
    for name,offset,xor,kind,parameters in controls:
        at = offset if offset in (0x1005,0x4B8F,0x4B91) else CS*16+offset
        raw = bytearray(target.program_image)
        raw[at] ^= xor
        machine = None
        try:
            machine = Machine(replace(target,program_image=bytes(raw)),0x1000)
            machine.run(kind,**parameters)
        except (ValueError,UcError):
            rejected.append(name)
        else:
            raise ValueError('PI actual instruction mutation escaped: '+name)
        finally:
            if machine:
                machine.close()
    return dict(count=len(rejected),rejected=rejected,owner_instruction_mutations=len(rejected)-3,
                nested_release_mutations=1,library_context_mutations=2,actual_guest_instruction_mutations=True)
