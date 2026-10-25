"""Independent PSP/FCB/stack/copy contracts; stop before payload execution.

DOS replies preserve registers/flags except AL under three explicit policies.
They are bounded interfaces, not claims about a physical DOS implementation.
The two transfer entries also execute independently, including zero-length REP.
"""
import hashlib
import json
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INTR, UC_HOOK_MEM_WRITE
from unicorn.x86_const import *
from lib.zun import parse_launcher
from lib.zun_wrapper_layout import instructions, need

REG = dict(ax=UC_X86_REG_AX,bx=UC_X86_REG_BX,cx=UC_X86_REG_CX,dx=UC_X86_REG_DX,
           si=UC_X86_REG_SI,di=UC_X86_REG_DI,bp=UC_X86_REG_BP,sp=UC_X86_REG_SP,
           cs=UC_X86_REG_CS,ds=UC_X86_REG_DS,es=UC_X86_REG_ES,ss=UC_X86_REG_SS)
FULL = dict(ax=UC_X86_REG_EAX,bx=UC_X86_REG_EBX,cx=UC_X86_REG_ECX,dx=UC_X86_REG_EDX,
            si=UC_X86_REG_ESI,di=UC_X86_REG_EDI,bp=UC_X86_REG_EBP,sp=UC_X86_REG_ESP)
ERROR = b'No COM-Soft !!!\r\n\n'


def arithmetic(flags,left,right,width=16,subtract=False):
    mask,sign = (1<<width)-1,1<<(width-1)
    raw = left-right if subtract else left+right
    value = raw&mask
    carry = raw<0 if subtract else raw>mask
    overflow = ((left^right)&(left^value)&sign) if subtract else (~(left^right)&(left^value)&sign)
    out = int(carry) | (int((value&255).bit_count()%2 == 0)<<2) | ((left^right^value)&0x10)
    out |= (int(value == 0)<<6) | (int(bool(value&sign))<<7) | (int(bool(overflow))<<11)
    return value,(flags&~0x8D5)|out


def logical(flags,value,width=16):
    value &= (1<<width)-1
    out = (int((value&255).bit_count()%2 == 0)<<2) | (int(value == 0)<<6)
    out |= int(bool(value&(1<<(width-1))))<<7
    return (flags&~0x8C5)|out


class Prediction:
    def __init__(self,m,kind,command,fcb,count,reply,length,payload_index,size):
        self.m = m
        self.memory = bytearray(m.uc.mem_read(0,1<<20))
        self.regs = dict(m.initial)
        self.flags,self.flag_mask = m.flags,0xFFFF
        self.output,self.writes = bytearray(),hashlib.sha256()
        self.events,self.write_count,self.copied = [],0,0
        self.stack,self.stack_base,self.base = self.regs['sp'],self.regs['ss']*16,m.base
        self.reply,self.outcome = reply,None
        if kind == 'launcher':
            self.launcher(command,fcb,count,length)
        else:
            source = m.directory['payloads'][payload_index]['runtime_start']
            self.regs.update(si=source,di=0x100,cx=size)
            if kind == 'call':
                self.store_stack(self.stack-2,0x326)
                self.regs['sp'] = self.stack-2
            self.transfer(source,size)

    def store(self,address,size,value):
        value &= (1<<(size*8))-1
        self.memory[address:address+size] = value.to_bytes(size,'little')
        self.writes.update(struct.pack('<IBI',address,size,value))
        self.write_count += 1

    def store_stack(self,offset,value):
        self.store(self.stack_base+(offset&65535),2,value)

    def copy(self,source,dest,size):
        for i in range(size):
            self.store(self.base+((dest+i)&65535),1,self.memory[self.base+((source+i)&65535)])

    def ah(self,value):
        self.regs['ax'] = (self.regs['ax']&255)|(value<<8)

    def al(self,value):
        self.regs['ax'] = (self.regs['ax']&0xFF00)|value

    def dos(self,service,raw):
        self.events.append((service,raw.hex()))
        self.output.extend(raw)
        if self.reply:
            self.al((raw[-1] if service == 2 else 0x24) if self.reply == 1 else 0xA7)

    def exit(self):
        self.ah(0x4C)
        self.events.append((0x4C,self.regs['ax']))
        self.outcome = 'dos-exit'

    def error(self):
        self.regs['dx'] = 0x104
        self.ah(9)
        self.dos(9,ERROR)
        self.exit()

    def launcher(self,command,fcb,count,length):
        self.flags &= ~0x400
        self.regs['cx'] = count
        self.flags = logical(self.flags,count)
        self.flag_mask &= ~0x10
        if count == 0:
            self.error()
            return
        self.regs['si'] = 0x81
        self.al(length)
        self.flags = logical(self.flags,length,8)
        stripped = command.lstrip(b' ')
        listing = length == 0 or not stripped
        if length and not stripped:
            self.al(13)
            _,self.flags = arithmetic(self.flags,13,13,8,True)
            self.flag_mask = 0xFFFF
        if listing:
            self.regs.update(cx=0,si=0x1E1+8*count)
            self.ah(2)
            self.regs['dx'] = (self.regs['dx']&0xFF00)|13
            self.dos(2,b'\r')
            self.regs['dx'] = (self.regs['dx']&0xFF00)|10
            self.dos(2,b'\n')
            for index in range(count):
                self.store_stack(self.stack-2,count-index)
                name = self.memory[self.base+0x1E1+8*index:self.base+0x1E9+8*index]
                self.regs['dx'] = (self.regs['dx']&0xFF00)|32
                self.dos(2,b' ')
                for value in name:
                    self.al(value)
                    self.regs['dx'] = (self.regs['dx']&0xFF00)|value
                    self.dos(2,bytes((value,)))
                self.regs['dx'] = (self.regs['dx']&0xFF00)|32
                self.dos(2,b' ')
            for value in (13,10):
                self.regs['dx'] = (self.regs['dx']&0xFF00)|value
                self.dos(2,bytes((value,)))
            self.exit()
            return
        self.al(stripped[0])
        chosen = None
        for index in range(count):
            pointer = 0x1E1+8*index
            self.store(self.base+0x102,2,pointer)
            self.store_stack(self.stack-2,count-index)
            name = bytes(self.memory[self.base+pointer:self.base+pointer+8])
            compared = next((i+1 for i,(a,b) in enumerate(zip(name,fcb)) if a != b),8)
            self.regs['di'] = 0x5D+compared
            if name == fcb:
                chosen = index
                break
            self.regs['si'] = pointer+8
            _,self.flags = arithmetic(self.flags,pointer,8)
        if chosen is None:
            self.regs.update(cx=0,bx=0x2E1+2*count)
            self.flag_mask = 0xFFFF
            self.error()
            return
        self.copy(0x6C,0x5C,16)
        separator = command.find(b' ',len(command)-len(stripped))
        tail = command[separator:] if separator >= 0 else b''
        self.store(self.base+0x80,1,len(tail))
        tail_source = 0x81+separator if separator >= 0 else 0x81+len(command)
        self.copy(tail_source,0x81,len(tail))
        self.store(self.base+0x81+len(tail),1,13)
        child = self.m.directory['payloads'][chosen]
        start,size = child['runtime_start'],child['size']
        self.regs.update(bx=0x2E1+2*chosen,dx=(self.regs['dx']&0xFF00)|len(tail),sp=self.stack-4)
        _,self.flags = arithmetic(self.flags,start+size,start,16,True)
        self.flag_mask = 0xFFFF
        self.store_stack(self.stack-4,0x326)
        self.transfer(start,size)

    def transfer(self,start,size):
        self.copy(start,0x100,size)
        self.copied = size
        self.regs.update(si=(start+size)&65535,di=(0x100+size)&65535,cx=0,ax=0x100)
        self.store_stack(self.regs['sp'],0x100)
        self.regs['sp'] = (self.regs['sp']+2)&65535
        self.outcome = 'payload-entry'


class Machine:
    def __init__(self,image,load,split_stack=False):
        self.image,self.load,self.base = image,load,load*16
        self.directory = parse_launcher(image,223)
        self.instructions = instructions(image)
        self.uc = Uc(UC_ARCH_X86,UC_MODE_16)
        self.uc.mem_map(0,1<<20)
        self.split_stack = split_stack
        self.covered,self.maximum_stack = set(),0
        self.hooks = [self.uc.hook_add(UC_HOOK_CODE,self.guard(self.code)),
                      self.uc.hook_add(UC_HOOK_INTR,self.guard(self.interrupt)),
                      self.uc.hook_add(UC_HOOK_MEM_WRITE,self.guard(self.write))]

    def guard(self,callback):
        def invoke(uc,*args):
            try:
                callback(uc,*args)
            except Exception as error:
                self.failure = str(error)
                uc.emu_stop()
        return invoke

    def close(self):
        for hook in self.hooks:
            self.uc.hook_del(hook)
        self.hooks.clear()

    def regs(self):
        return {n:self.uc.reg_read(reg) for n,reg in REG.items()}

    def code(self,uc,address,size,_):
        ip = address-self.base
        if self.transferring:
            need(ip == 0x100, 'transfer must enter 0100 before any payload instruction')
            self.outcome = 'payload-entry'
            uc.emu_stop()
            return
        need(ip in self.instructions and self.instructions[ip].size == size, 'only complete source-owned instructions')
        self.covered.update(range(ip,ip+size))
        depth = (self.stack-self.uc.reg_read(REG['sp']))&65535
        if depth < 0x8000:
            self.maximum_stack = max(self.maximum_stack,depth)
        if ip == self.directory['helper_offset']+256+7:
            self.transferring = True

    def write(self,uc,access,address,size,value,_):
        need(size in (1,2), '8086 byte/WORD stores')
        self.writes.update(struct.pack('<IBI',address,size,value&((1<<(size*8))-1)))
        self.write_count += 1

    def interrupt(self,uc,number,_):
        need(number == 0x21, 'bounded DOS only')
        ax = uc.reg_read(REG['ax'])
        ah = ax>>8
        if ah == 2:
            raw = bytes((uc.reg_read(REG['dx'])&255,))
        elif ah == 9:
            pointer = uc.reg_read(REG['ds'])*16+uc.reg_read(REG['dx'])
            raw = bytes(uc.mem_read(pointer,256)).split(b'$',1)
            need(len(raw) == 2, 'bounded dollar-terminated error message')
            raw = raw[0]
        else:
            need(ah == 0x4C, 'known terminal DOS service')
            self.events.append((ah,ax))
            self.outcome = 'dos-exit'
            uc.emu_stop()
            return
        self.events.append((ah,raw.hex()))
        self.output.extend(raw)
        if self.reply:
            value = (raw[-1] if ah == 2 else 0x24) if self.reply == 1 else 0xA7
            uc.reg_write(REG['ax'],(ax&0xFF00)|value)

    def run(self,kind='launcher',*,command=b'',fcb=b'-1',count=5,reply=0,flags=0x602,seed=0,
            payload_index=0,size=0,length=None):
        need(len(command) <= 126 and len(fcb) <= 8 and 0 <= count <= 5, 'bounded PSP/directory inputs')
        need(kind in ('launcher','call','helper') and reply in (0,1,2), 'explicit entry and DOS response policy')
        need(kind == 'launcher' or not flags&0x400, 'direct transfer ABI requires forward direction')
        need(0 <= payload_index < 5 and 0 <= size <= self.directory['payloads'][payload_index]['size'],
             'bounded copy inside one complete canonical payload')
        need(length is None or length in (0,len(command)), 'normal or explicitly suppressed PSP length')
        length = len(command) if length is None else length
        self.uc.mem_write(0,bytes(1<<20))
        self.uc.mem_write(self.base,bytes((i*29+seed*17)&255 for i in range(65536)))
        self.uc.mem_write(self.base+256,self.image)
        self.uc.mem_write(self.base+0x80,bytes((length,))+command+b'\r')
        fcb = fcb.ljust(8,b' ')
        self.uc.mem_write(self.base+0x5D,fcb)
        self.uc.mem_write(self.base+0x6C,b'0123456789ABCDEF')
        self.uc.mem_write(self.base+0x1DF,count.to_bytes(2,'little'))
        self.stack = 0xFFFE if seed%2 == 0 else 0xF300
        for n,reg in FULL.items():
            value = ((0xA579+seed*0x123)&65535)<<16 | ((0x1234+len(n)*0x222+list(FULL).index(n)*0x321+seed)&65535)
            self.uc.reg_write(reg,value)
        for n in ('cs','ds','es','ss'):
            self.uc.reg_write(REG[n],0x8000 if n == 'ss' and self.split_stack else self.load)
        self.uc.reg_write(REG['sp'],self.stack)
        self.flags,self.reply = flags,reply
        self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        if kind != 'launcher':
            source = self.directory['payloads'][payload_index]['runtime_start']
            for n,v in dict(si=source,di=0x100,cx=size).items():
                self.uc.reg_write(REG[n],v)
            self.uc.mem_write(self.uc.reg_read(REG['ss'])*16+self.stack,b'\xEF\xBE')
        self.initial = self.regs()
        self.initial_full = {n:self.uc.reg_read(reg) for n,reg in FULL.items()}
        predicted = Prediction(self,kind,command,fcb,count,reply,length,payload_index,size)
        self.output,self.events,self.writes,self.write_count = bytearray(),[],hashlib.sha256(),0
        self.failure,self.outcome,self.transferring = None,None,False
        entry = 0x100 if kind == 'launcher' else 0x323 if kind == 'call' else self.directory['helper_offset']+256
        try:
            self.uc.emu_start(self.base+entry,0,count=200000)
        except UcError as error:
            raise ValueError('wrapper CPU execution failed') from error
        need(self.failure is None,self.failure or 'guarded callback')
        need(self.outcome == predicted.outcome and self.outcome is not None, 'bounded outcome')
        need(self.regs() == predicted.regs, 'independent final WORD/segment registers: '+str((self.regs(),predicted.regs)))
        for n,reg in FULL.items():
            need(self.uc.reg_read(reg) == (self.initial_full[n]&0xFFFF0000)|predicted.regs[n], 'preserved DWORD high halves')
        actual_flags = self.uc.reg_read(UC_X86_REG_EFLAGS)
        need(actual_flags&predicted.flag_mask == predicted.flags&predicted.flag_mask,
             f'defined flags / IF / DF: {actual_flags:X} versus {predicted.flags:X}')
        need(self.events == predicted.events and self.output == predicted.output, 'ordered DOS calls/output and terminal AL')
        need(self.write_count == predicted.write_count and self.writes.digest() == predicted.writes.digest(),
             'every ordered byte/WORD store, including transient stack and overlapping copies')
        memory = bytes(self.uc.mem_read(0,1<<20))
        need(memory == predicted.memory, 'complete memory, with no ignored stack windows')
        return dict(kind=kind,outcome=self.outcome,registers=self.regs(),flags=actual_flags,
            output=self.output.hex(),stores=self.write_count,store_sha256=self.writes.hexdigest(),
            memory_sha256=hashlib.sha256(memory).hexdigest(),copied_bytes=predicted.copied,
            terminal_AX=self.regs()['ax'] if self.outcome == 'dos-exit' else None)


def domain():
    for count in range(6):
        for command in (b'',b' ',b' '*126,b' -X',b'-5'):
            for reply in range(3):
                yield 'launcher',dict(command=command,fcb=b'-5',count=count,reply=reply,seed=reply,flags=(2,0x602,0xED7)[reply])
    for index in range(5):
        name = f'-{index+1}'.encode()
        for leading in (0,1,2,17):
            for tail in (b'',b' ',b'  hello',b'\targ',b'  a b  '):
                for reply in range(3):
                    yield 'launcher',dict(command=b' '*leading+name+tail,fcb=name,reply=reply,seed=reply,flags=(2,0x602,0xED7)[reply])
        # Every valid PSP length from selector-only through 126 bytes.
        for length in range(2,127):
            yield 'launcher',dict(command=name+(b' '+b'x'*(length-3) if length>2 else b''),fcb=name,seed=length%2)
        for at in range(8):
            fcb = bytearray(name.ljust(8,b' '))
            fcb[at] ^= 0x80
            yield 'launcher',dict(command=b' -1 ignored',fcb=bytes(fcb),seed=at%2)
        yield 'launcher',dict(command=b' -X hello',fcb=name)
        yield 'launcher',dict(command=b' -1 hello',fcb=name,length=0)
    for kind in ('call','helper'):
        for index,size in enumerate((926,1390,10096,4224,5618)):
            for length in (0,1,2,15,16,17,255,256,size):
                yield kind,dict(payload_index=index,size=length,flags=0x202,seed=index%2)


def verify(target,candidate):
    results = []
    for image in (target,candidate):
        rows = []
        for load,split in ((0x1000,False),(0x3000,True)):
            m = Machine(image,load,split)
            trace,cases,kinds = hashlib.sha256(),0,dict(launcher=0,call=0,helper=0)
            try:
                for kind,parameters in domain():
                    observation = m.run(kind,**parameters)
                    trace.update(json.dumps(observation,sort_keys=True).encode())
                    cases += 1
                    kinds[kind] += 1
                owned = {p for at,i in m.instructions.items() for p in range(at,at+i.size)}
                need(m.covered == owned and len(owned) == 213, 'all 213 instruction bytes execute')
                need(m.maximum_stack == 4, 'four-byte maximum observed stack depth')
                rows.append(dict(load_segment=load,split_stack=split,cases=cases,cases_by_entry=kinds,
                    covered_owner_bytes=len(m.covered),maximum_observed_stack_depth=m.maximum_stack,
                    trace_sha256=trace.hexdigest()))
            finally:
                m.close()
        results.append(rows)
    need(results[0] == results[1], 'independently specified target/candidate observations agree')
    return dict(images=2,functions=3,code_bytes=213,data_bytes=21,
        cases_per_image=sum(r['cases'] for r in results[0]),observations=results[0],
        maximum_DOS_command_bytes=126,DOS_AL_reply_policies=3,canonical_payloads=5,
        directory_count_dependency_domain=[0,1,2,3,4,5],payload_instructions_executed=False,
        stack_windows_ignored=False,all_memory_and_ordered_stores_checked=True)


def negative_controls(image):
    helper = len(image)+256-8
    controls = (
        ('entry-transfer',0x101,1,dict(command=b' -1 hello')),
        ('DF-clear',0x117,1,dict(command=b' -1 hello')),
        ('zero-count-branch',0x11E,1,dict(count=0)),
        ('empty-tail-branch',0x126,1,dict(command=b' -1 hello')),
        ('space-scan',0x12F,1,dict(command=b'   ')),
        ('name-width',0x179,1,dict(command=b' -1 hello')),
        ('FCB-match-branch',0x17D,1,dict(command=b' -5 hello',fcb=b'-5')),
        ('search-stack-pop',0x189,3,dict(command=b' -X',fcb=b'-X')),
        ('FCB-copy-width',0x19E,1,dict(command=b' -1 hello')),
        ('strip-spaces',0x1AD,1,dict(command=b'  -1 hello')),
        ('selector-end-branch',0x1B4,1,dict(command=b' -1 hello')),
        ('empty-arguments',0x1C4,1,dict(command=b' -1 hello')),
        ('copy-count',0x1C8,1,dict(command=b' -1 hello')),
        ('tail-terminator',0x1CF,1,dict(command=b' -1 hello')),
        ('selected-length',0x1D4,1,dict(command=b' -1 hello')),
        ('cross-payload-CALL',0x324,1,dict(command=b' -1 hello')),
        ('helper-MOVSB-width',helper+1,1,dict(command=b' -1 hello')),
        ('helper-discard-register',helper+2,1,dict(command=b' -1 hello')),
        ('helper-entry-address',helper+4,1,dict(command=b' -1 hello')),
        ('helper-push-register',helper+6,1,dict(command=b' -1 hello')),
        ('helper-return-width',helper+7,8,dict(command=b' -1 hello')),
    )
    rejected = []
    for name,address,xor,parameters in controls:
        m = Machine(image,0x1000)
        changed = bytearray(image)
        changed[address-256] ^= xor
        m.image = bytes(changed)
        try:
            m.run(**parameters)
        except (ValueError,UcError):
            rejected.append(name)
        else:
            raise ValueError('actual wrapper mutation escaped: '+name)
        finally:
            m.close()
    return dict(count=len(rejected),rejected=rejected,actual_guest_instruction_changes=True,
                payload_bytes_mutated=False,directory_mutations_counted_as_instructions=False)
