"""Independent command-parser contracts for the actual -4 guest instructions.

All scalar and print helpers execute. DOS character/exit services and unowned
option callbacks are explicit bounded interfaces, not hardware/DOS acceptance.
"""
import hashlib
import json
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
from unicorn.x86_const import UC_X86_REG_EFLAGS
from lib.zun_driver_scalar_runtime import REG, ENTRIES as SCALARS, cmp8, number, upper, parity
from verify_th03_zun_driver_hybrid import COMMAND_PROCS

ENTRIES = {n.removeprefix('sprite16_'): (a, b-a) for n,a,b in COMMAND_PROCS[:9]}
COUNT, VECTOR, CURSOR, TABLE = 0x1070, 0x1072, 0x10F2, 0x101C
MESSAGES = dict(quote=0x10F4, argument=0x1114, number=0x112B, option=0x1152)
SEPARATORS = (32, 44, 9)


def need(value, message):
    if not value: raise ValueError('ZUN command contract: ' + str(message))


def arithmetic(a, b, subtract=False):
    result = (a-b if subtract else a+b) & 65535
    overflow = ((a ^ b) & (a ^ result) if subtract else ~(a ^ b) & (a ^ result)) & 0x8000
    return (int(a < b) if subtract else int(a+b > 65535)) | parity(result) | (16 if (a ^ b ^ result) & 16 else 0) | (64 if not result else 0) | (128 if result & 0x8000 else 0) | (0x800 if overflow else 0)


class Prediction:
    """A byte/string/state specification; it never decodes guest instructions."""
    def __init__(self, initial, registers, base, stack_base, stack):
        self.memory = bytearray(initial); self.regs = dict(registers)
        self.base, self.stack_base, self.stack = base, stack_base, stack
        self.writes, self.callbacks, self.output = [], [], []
        self.flags_mask, self.flags_value, self.exit, self.sp_delta = 0, 0, False, 2

    def byte(self, offset, segment=None): return self.memory[(self.base if segment is None else segment) + (offset & 65535)]
    def word(self, offset):
        address=self.base+(offset&65535)
        return int.from_bytes(self.memory[address:address+2],"little")
    def store(self, offset, size, value):
        address = self.base + (offset & 65535)
        self.writes.append((address, size, value))
        self.memory[address:address+size] = value.to_bytes(size, 'little')
    def al(self, value): self.regs['ax'] = self.regs['ax'] & 0xFF00 | value
    def text(self, offset, segment=None):
        value = bytearray()
        while self.byte(offset+len(value),segment):
            value.append(self.byte(offset+len(value),segment)); need(len(value)<2048,'bounded text specification')
        return bytes(value)
    def error(self, kind, stack_delta):
        self.output = list(self.text(MESSAGES[kind], self.stack_base))
        self.regs['ax'] = 0x4C01; self.flags_mask, self.flags_value = 0x8C5, 0x44
        self.exit, self.sp_delta = True, stack_delta
    def scan(self, kind):
        si = self.regs['si']
        if kind == 'skip_separators':
            while self.byte(si) in SEPARATORS: self.store(si,1,0); si=(si+1)&65535
            value=self.byte(si); mask,flags=0x8D5,cmp8(value,9)
        elif kind == 'find_token_end':
            while self.byte(si) not in (*SEPARATORS,0,13): si=(si+1)&65535
            value=self.byte(si); mask,flags=(0x8C5 if value==0 else 0x8D5),0x44
        else:
            while self.byte(si) not in (34,0,13): si=(si+1)&65535
            value=self.byte(si); mask,flags=(0x8C5 if value==0 else 0x8D5),0x44 | int(value!=34)
        self.regs['si']=si; self.al(value); self.flags_mask,self.flags_value=mask,flags
    def argument(self, required, stack_delta=0):
        count=self.word(COUNT)
        if not count:
            if required: self.error('argument',stack_delta)
            else: self.flags_mask,self.flags_value=0x8D5,0x45
            return False
        self.store(COUNT,2,(count-1)&65535)
        cursor=self.word(CURSOR); self.store(CURSOR,2,(cursor+2)&65535)
        self.regs['si']=self.word(cursor)
        self.flags_mask,self.flags_value=0x8D5,arithmetic(cursor,2)
        if not required: self.flags_value &= ~1
        return True
    def parse(self):
        pointer=self.regs['si']; raw=bytes(self.byte(pointer+i) for i in range(len(self.text(pointer))+9))
        value,carry,suffix=number(raw,self.byte(pointer-1))
        if suffix is not None:
            original=self.byte(pointer+suffix); self.store(pointer+suffix,1,0); self.store(pointer+suffix,1,original)
        self.regs['ax']=value; self.flags_mask,self.flags_value=1,carry
        return carry
    def run(self, kind, callback_consume):
        saved=dict(self.regs)
        if kind in ('skip_separators','find_token_end','find_quote_end'): self.scan(kind)
        elif kind == 'tokenize_command':
            self.store(COUNT,2,0); self.regs['di']=VECTOR
            while True:
                self.scan('skip_separators'); si=self.regs['si']; value=self.byte(si)
                if value in (0,13,59):
                    self.store(si,1,0)
                    self.flags_mask,self.flags_value=(0x8C5 if not value else 0x8D5),0x44
                    break
                quoted=value==34
                if quoted: si=(si+1)&65535; self.regs['si']=si
                self.store(self.regs['di'],2,si); self.regs['di']=(self.regs['di']+2)&65535
                self.store(COUNT,2,(self.word(COUNT)+1)&65535)
                if quoted:
                    self.scan('find_quote_end')
                    if self.flags_value & 1: self.error('quote',-12); return
                    self.store(self.regs['si'],1,0); self.regs['si']=(self.regs['si']+1)&65535
                self.scan('find_token_end')
            for name in ('ax','bx','cx','dx','si','di'): self.regs[name]=saved[name]
        elif kind in ('require_argument','optional_argument'):
            self.argument(kind=='require_argument')
        elif kind in ('require_number','optional_number_legacy'):
            required=kind=='require_number'
            if not required: self.regs['ax']=0
            available=self.argument(required,-6)
            if self.exit: return
            if required or not available:
                self.regs['dx']=self.regs['si']
                if self.parse() and required: self.error('number',-4); return
            self.regs['si'],self.regs['dx']=saved['si'],saved['dx']
        else:
            self.store(CURSOR,2,VECTOR)
            while True:
                cursor=self.word(CURSOR); self.store(CURSOR,2,(cursor+2)&65535); self.regs['si']=self.word(cursor)
                if not self.word(COUNT): self.flags_mask,self.flags_value=0x8D5,0x44; return
                self.store(COUNT,2,(self.word(COUNT)-1)&65535)
                pointer=self.regs['si']; first=self.byte(pointer)
                if first==45: first=47; self.store(pointer,1,47)
                self.al(first); row=TABLE
                while self.word(row):
                    self.regs['di']=self.word(row)
                    if bytes(upper(b) for b in self.text(pointer)) == bytes(upper(b) for b in self.text(self.word(row))): break
                    row+=4
                self.regs['bx']=row
                if not self.word(row): self.error('option',0); return
                self.callbacks.append(dict(address=self.word(row+2), registers=dict(self.regs)))
                if callback_consume:
                    need(self.word(COUNT)>0,'callback consumption precondition')
                    self.store(COUNT,2,(self.word(COUNT)-1)&65535)
                    self.store(CURSOR,2,(self.word(CURSOR)+2)&65535)


class Machine:
    def __init__(self,image,load):
        need(len(image)==4224,'complete driver image')
        self.load,self.base=load,load*16; self.image=image
        self.uc=Uc(UC_ARCH_X86,UC_MODE_16); self.uc.mem_map(0,1<<20)
        self.initial=bytearray(b'\xA5'*(1<<20)); self.initial[self.base+256:self.base+256+len(image)]=image
        ranges=list(ENTRIES.values())+list(SCALARS.values())+[(0x660,22),(0x676,19)]
        self.instructions={}
        for start,size in ranges:
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image[start-256:start-256+size],start))
            need(sum(i.size for i in rows)==size,'complete actual helper/procedure decoding')
            self.instructions.update({i.address:i.size for i in rows})
        self.owner_bytes={p for start,size in ENTRIES.values() for p in range(start,start+size)}
        self.covered=set(); self.maximum_stack=0
        self.hooks=[self.uc.hook_add(UC_HOOK_CODE,self.code),self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write),self.uc.hook_add(UC_HOOK_INTR,self.interrupt)]
    def close(self):
        for hook in self.hooks:self.uc.hook_del(hook)
        self.hooks=[]; self.uc=None
    def r(self,name):return self.uc.reg_read(REG[name])
    def fail(self,error):self.error=str(error);self.uc.emu_stop()
    def code(self,uc,address,size,_):
        try:
            if address==self.base+0xFFFF:self.stopped=True;uc.emu_stop();return
            ip=address-self.base
            if ip in self.callback_addresses:
                need(self.callback_index<len(self.expected.callbacks),'unexpected option callback')
                row=self.expected.callbacks[self.callback_index]; regs=row['registers']
                need(ip==row['address'] and all(self.r(n)==v for n,v in regs.items() if n!='flags'),'ordered callback target/arguments')
                need(self.r('sp')==self.stack-20,'near callback frame depth')
                frame=struct.unpack('<10H',bytes(uc.mem_read(self.stack_base+self.stack-20,20)))
                need(frame==(0xA7D,regs['es'],regs['di'],regs['si'],regs['bp'],self.stack,regs['bx'],regs['dx'],regs['cx'],regs['ax']),'complete PUSHA/ES/near callback frame')
                if self.callback_consume:
                    for offset in (COUNT,CURSOR):
                        old=int.from_bytes(uc.mem_read(self.base+offset,2),'little')
                        val=(old+(-1 if offset==COUNT else 2))&65535
                        uc.mem_write(self.base+offset,val.to_bytes(2,'little'))
                        # API writes do not invoke the guest memory hook.
                        self.check_write(self.base+offset,2,val)
                for index,name in enumerate(('ax','bx','cx','dx','si','di','bp','es')):uc.reg_write(REG[name],0x5A00+index)
                uc.reg_write(UC_X86_REG_EFLAGS,(regs['flags']&0x600)|0x8D7|2)
                uc.reg_write(REG['sp'],self.stack-18);uc.reg_write(REG['ip'],frame[0])
                self.callback_index+=1;return
            need(self.instructions.get(ip)==size,'execution outside command/scalar/print procedures')
            self.covered.update(set(range(ip,ip+size))&self.owner_bytes)
        except Exception as error:self.fail(error)
    def check_write(self,address,size,value):
        need(self.write_index<len(self.expected.writes) and (address,size,value)==self.expected.writes[self.write_index],f'ordered parser write #{self.write_index}: {address:x}/{size}/{value:x}')
        self.write_index+=1
    def write(self,uc,access,address,size,value,_):
        try:
            if self.stack_base+self.stack-96<=address and address+size<=self.stack_base+self.stack:
                self.maximum_stack=max(self.maximum_stack,self.stack_base+self.stack-address);return
            self.check_write(address,size,value)
        except Exception as error:self.fail(error)
    def interrupt(self,uc,number,_):
        try:
            need(number==0x21,'DOS interface only')
            if self.r('ax')>>8==2:
                i=len(self.output);value=self.r('dx')&255
                need(i<len(self.expected.output) and value==self.expected.output[i],'ordered DOS character output')
                self.output.append(value);uc.reg_write(REG['ax'],self.r('ax')&0xFF00|value)
                uc.reg_write(UC_X86_REG_EFLAGS,(self.flags&0x600)|0x8D7|2)
            else:
                need(self.r('ax')==0x4C01 and self.expected.exit,'DOS error exit status')
                self.exited=True;uc.emu_stop()
        except Exception as error:self.fail(error)
    def run(self,kind,*,text=b'one two',arguments=(b'12',),remaining=None,flags=0x202,stack=0xF800,pattern=0,split_stack=False,callback_consume=False,cursor=VECTOR):
        need(kind in ENTRIES and len(text)<1024,'bounded command inputs')
        parse=kind=='require_number' or kind=='optional_number_legacy' and (remaining==0 or not arguments)
        need(not parse or not flags&0x400,'forward numeric helper precondition')
        self.stack,self.flags,self.callback_consume=stack,flags,callback_consume
        ss=0x7000 if split_stack else self.load;self.stack_base=ss*16
        self.uc.mem_write(0,bytes(self.initial))
        def put(offset,raw,base=None):self.uc.mem_write((self.base if base is None else base)+offset,raw)
        pointer=0x3001;put(pointer-1,b'\xA5'+text+b'\0'+b'\xA5'*8)
        pointers=[]
        for i,value in enumerate(arguments):
            at=0x4001+i*128;need(len(value)<120,'bounded argument string');pointers.append(at);put(at-1,b'\xA5'+value+b'\0'+b'\xA5'*8)
        for i,value in enumerate(pointers+[0xDEAD]):put(VECTOR+2*i,struct.pack('<H',value))
        count=len(arguments) if remaining is None else remaining
        put(COUNT,struct.pack('<H',count));put(CURSOR,struct.pack('<H',cursor))
        if cursor!=VECTOR and pointers: put(cursor,struct.pack('<H',pointers[0]))
        if split_stack:
            for name,offset in MESSAGES.items():put(offset,('foreign SS '+name+'\r\n').encode()+b'\0',self.stack_base)
        put(stack,b'\xFF\xFF\x53\xA9',self.stack_base)
        registers=dict(ax=0xB53A^pattern,bx=0x37C1^pattern,cx=0x1298^pattern,dx=0x2481^pattern,si=pointer,di=0x2A01^pattern,bp=0xA675^pattern,cs=self.load,ds=self.load,es=self.load if kind=='dispatch_options' else 0x6000,ss=ss,flags=flags)
        initial=bytes(self.uc.mem_read(0,1<<20));self.expected=Prediction(initial,registers,self.base,self.stack_base,stack)
        self.expected.run(kind,callback_consume)
        self.callback_addresses={int.from_bytes(self.image[at-256:at-254],'little') for at in range(TABLE+2,TABLE+32,4)} if kind=='dispatch_options' else set()
        for name,val in registers.items():
            if name!='flags':self.uc.reg_write(REG[name],val)
        self.uc.reg_write(REG['sp'],stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        self.write_index,self.callback_index,self.output,self.error,self.stopped,self.exited=0,0,[],None,False,False
        try:self.uc.emu_start(self.base+ENTRIES[kind][0],self.base+0x10000,count=60000)
        except UcError as error:raise ValueError('ZUN command contract: guest failure') from error
        need(self.error is None,self.error or 'guest error')
        need(self.exited==self.expected.exit and (self.exited or self.stopped),'near return or specified terminal DOS exit')
        need(self.r('sp')==(stack+self.expected.sp_delta)&65535,'near/error caller frame')
        actual={name:self.r(name) for name in registers if name!='flags'}
        expected={name:val for name,val in self.expected.regs.items() if name!='flags'}
        need(actual==expected, f'independent command registers: {[(n,hex(actual[n]),hex(v)) for n,v in expected.items() if actual[n]!=v]}')
        final_flags=self.uc.reg_read(UC_X86_REG_EFLAGS);mask=self.expected.flags_mask
        need(final_flags&mask==self.expected.flags_value,'independent command flags')
        need(final_flags&0x600==flags&0x600,'inherited IF/DF across bounded services')
        need(self.write_index==len(self.expected.writes) and self.callback_index==len(self.expected.callbacks) and self.output==self.expected.output,'complete writes/callbacks/output')
        actual_memory=bytes(self.uc.mem_read(0,1<<20));lo,hi=self.stack_base+stack-96,self.stack_base+stack
        self.expected.memory[lo:hi]=actual_memory[lo:hi]
        need(actual_memory==self.expected.memory,'complete physical memory outside bounded stack')
        return dict(registers=actual,flags_mask=mask,result_flags=final_flags&mask,exit=self.exited,writes=self.expected.writes,callbacks=[c['address'] for c in self.expected.callbacks],output=self.output)


def base_cases():
    for value in range(256):
        text=bytes((value,))+b'Z\0'
        for kind in ('skip_separators','find_token_end','find_quote_end'):yield kind,dict(text=text)
    for text in (b'',b' ,\t',b';tail',b'one;two',b'one ;two',b'one\rtwo',b'one\0two',b'""',b'"a,b c"suffix next',b'"semi;colon" , next',b'"open',b'"open\rjunk',b'a "open',b' '.join([b'x']*64),b' '.join([b'x']*65),b' '.join([b'x']*66)):
        yield 'tokenize_command',dict(text=text)
    for kind in ('require_argument','optional_argument'):
        for remaining in (0,1,2,0x7FFF,0x8000,0xFFFF):yield kind,dict(remaining=remaining,arguments=(b'one',b'two'))
        for cursor in (0x7FFF,0xFFFE,0xFFFF):yield kind,dict(cursor=cursor)
    for text in (b'',b'123',b'-32768',b'65536',b'$ff',b'ffh',b'101b',b'ON',b'off',b"'AB'",b'garbage',b'12X'):
        yield 'require_number',dict(arguments=(text,))
        yield 'optional_number_legacy',dict(text=text,remaining=0)
        yield 'optional_number_legacy',dict(text=text,arguments=(b'garbage',))
    yield 'require_number',dict(arguments=())
    for arguments in ((),(b'/R',),(b'-r',),(b'/Z',),(b'/V',),(b'MASKTEST',),(b'PRESSY',),(b'COPYUL',),(b'CLSU',),(b'SPRITE',),(b'/R',b'/z',b'ClSu'),(b'bad',),(b'/R',b'bad')):
        yield 'dispatch_options',dict(arguments=arguments)
    yield 'dispatch_options',dict(arguments=(b'/R',b'123',b'/Z',b'456'),callback_consume=True)


def cases():
    for kind,options in base_cases():
        variants=(2,0x202) if kind in ('require_number','optional_number_legacy') else (2,0x202,0x402,0xED7)
        for flags in variants: yield kind,dict(options,flags=flags)
    yield 'optional_number_legacy',dict(arguments=(b'garbage',),flags=0xED7)


def verify(target,candidate):
    observations=[]
    for image in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(image,load)
            try:
                trace=hashlib.sha256()
                for count,(kind,options) in enumerate(cases(),1):
                    row=m.run(kind,stack=0xF800 if count&1 else 0xE800,pattern=0 if count&1 else 0xFFFF,split_stack=count%2==0,**options)
                    trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.owner_bytes,'all 361 owned command instruction bytes execute')
                loads.append(dict(load_segment=load,cases=count,covered_owner_bytes=len(m.covered),maximum_observed_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent target/candidate observations')
    return dict(images=2,functions=9,code_bytes=361,private_data_bytes=0,private_bss_bytes=0,cases_per_image=sum(o['cases'] for o in observations[0]),executed_owner_bytes=361,observations=observations[0],exhaustive_byte_domains=256,scope='nine command procedures; DOS and option callbacks remain bounded interfaces')


def negative_controls(target):
    controls=(
        ('semicolon-at-token-start',0x93D,b'\x3B',b'\x3A','tokenize_command',dict(text=b'one ;tail')),
        ('quoted-tail-is-skipped',0x968,b'\xE8\x2E\0',b'\x90'*3,'tokenize_command',dict(text=b'"a"suffix next')),
        ('quoted-terminator-write',0x966,b'\0',b'\x01','tokenize_command',dict(text=b'"a"')),
        ('count-word-width',0x950,b'\xFF',b'\xFE','tokenize_command',dict(text=b'"a"')),
        ('tab-separator',0x98D,b'\x09',b'\x08','skip_separators',dict(text=b'\tX')),
        ('CR-token-end',0x9AC,b'\x0D',b'\x0B','find_token_end',dict(text=b'a\rb')),
        ('missing-quote-carry',0x9C6,b'\xF9',b'\xF8','find_quote_end',dict(text=b'open')),
        ('required-count-decrements',0x9E0,b'\x0E',b'\x06','require_argument',{}),
        ('optional-empty-carry',0x9F6,b'\xF9',b'\xF8','optional_argument',dict(arguments=())),
        ('optional-present-clear',0xA08,b'\xF8',b'\xF9','optional_argument',{}),
        ('required-number-success',0xA14,b'\x73',b'\x72','require_number',{}),
        ('legacy-optional-branch',0xA2C,b'\x73',b'\x72','optional_number_legacy',dict(arguments=(b'garbage',))),
        ('minus-becomes-slash',0xA5B,b'\x2F',b'\x5C','dispatch_options',dict(arguments=(b'-r',))),
        ('option-row-width',0xA83,b'\x04',b'\x08','dispatch_options',dict(arguments=(b'/R',))),
        ('callback-pusha-frame',0xA78,b'\x60',b'\x90','dispatch_options',dict(arguments=(b'/R',))),
        ('callback-ES-restore',0xA7D,b'\x07',b'\x90','dispatch_options',dict(arguments=(b'/R',))),
        ('zero-count-still-reads-vector',0xA4C,b'\x75',b'\x74','dispatch_options',dict(arguments=())),
        ('required-error-message',0x9D5,b'\x14',b'\x15','require_argument',dict(arguments=())),
        ('error-exit-status',0x9DB,b'\x01',b'\x02','require_argument',dict(arguments=())),
    )
    rejected=[]
    for name,at,old,new,kind,options in controls:
        need(target[at-256:at-256+len(old)]==old,'literal mutation site '+name)
        changed=bytearray(target);changed[at-256:at-256+len(new)]=new;m=Machine(bytes(changed),0x3000)
        try:
            try:m.run(kind,**options)
            except ValueError:rejected.append(name)
            else:raise ValueError('ZUN command mutation escaped: '+name)
        finally:m.close()
    return dict(count=len(rejected),rejected=rejected)
