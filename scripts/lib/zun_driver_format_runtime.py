"""Independent formatter contracts, including original signed padding/overflow.

Real formatter, print, reverse and strlen instructions execute. Only DOS AH=2
character output is a bounded interface. Forward string operations require DF=0.
The 208-byte print wrapper is tested through its saved-BP overwrite, stopping
before an output terminator can overwrite the caller's return address.
"""
import hashlib
import json
import struct

from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR
from unicorn.x86_const import *
from lib.zun_driver_format_layout import RANGES,control_flow

ENTRIES={n.removeprefix('sprite16_'):(a,s) for n,a,s in RANGES}
REG={n:globals()['UC_X86_REG_'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp','sp','cs','ds','es','ss','ip')}
GPRS={n:globals()['UC_X86_REG_E'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp')}


def need(value,message):
    if not value:raise ValueError('ZUN formatter contract: '+str(message))
def parity(value):return 4 if (value&255).bit_count()%2==0 else 0
def cmp16(a,b):
    value=(a-b)&65535
    return int(a<b)|parity(value)|((a^b^value)&16)|(64 if value==0 else 0)|(value>>8&128)|(((a^b)&(a^value)&0x8000)>>4)
def dec16(value):
    result=(value-1)&65535
    return parity(result)|((value^1^result)&16)|(64 if result==0 else 0)|(result>>8&128)|(0x800 if value==0x8000 else 0)
def digits(value,radix,lower):
    table=b'0123456789abcdef' if lower else b'0123456789ABCDEF';out=bytearray()
    while True:
        out.append(table[value%radix]);value//=radix
        if not value:return bytes(reversed(out))
def padding(width,used):
    value=(width-used)&65535
    return value if 0<value<0x8000 else 0


class Prediction:
    def __init__(self,initial):
        self.memory=bytearray(initial);self.writes=[];self.count=0;self.last_number=None
    def store(self,address,value):
        self.writes.append((address,1,value));self.memory[address]=value
    def reverse(self,address,text):
        current=bytearray(text)
        for i in range(len(text)//2):
            j=len(text)-1-i;a,b=current[i],current[j]
            self.store(address+j,a);self.store(address+i,b);current[i],current[j]=b,a
    def format(self,text,args,destination):
        text=text.split(b'\0',1)[0];i=0;argument=0;pointer=destination
        def emit(raw):
            nonlocal pointer
            for byte in raw:self.store(pointer,byte);pointer+=1
        def append(raw):
            nonlocal pointer
            emit(raw+b'\0');pointer-=1
        while i<len(text):
            if text[i]!=37:
                if text[i:i+2] in (b'\\n',b'\\r',b'\\t'):
                    emit({b'\\n':b'\r\n',b'\\r':b'\r',b'\\t':b'\t'}[text[i:i+2]]);i+=2
                else:emit(text[i:i+1]);i+=1
                continue
            i+=1;left=i<len(text) and text[i]==45
            if left:i+=1
            zero=i<len(text) and text[i]==48
            if zero:i+=1
            width=0
            while i<len(text) and 48<=text[i]<=57:width=(width*10+text[i]-48)&65535;i+=1
            kind=text[i:i+1]
            if kind not in (b'u',b'd',b'x',b'X',b'b',b's',b'c'):continue
            need(argument<len(args),'format consumes an available four-byte SS slot')
            value=args[argument];argument+=1;i+=1
            if kind==b'c':need(isinstance(value,int),'character DWORD slot');emit(bytes((value&255,)));continue
            if kind==b's':
                need(isinstance(value,bytes),'bounded far string slot');raw=value.split(b'\0',1)[0];used=len(raw)
            else:
                need(isinstance(value,int),'numeric DWORD slot');value&=0xFFFFFFFF;negative=kind==b'd' and bool(value&0x80000000)
                if negative:value=(-value)&0xFFFFFFFF;emit(b'-')
                self.last_number=value
                radix={b'u':10,b'd':10,b'x':16,b'X':16,b'b':2}[kind];raw=digits(value,radix,kind==b'x');used=len(raw)+negative
            amount=padding(width,used)
            if left:append(raw);emit(b' '*amount)
            else:emit((b'0' if zero and kind!=b's' else b' ')*amount);append(raw)
        self.store(pointer,0);self.count=pointer-destination
        return bytes(self.memory[destination:pointer+1])


class Machine:
    def __init__(self,image,load):
        need(len(image)==4224 and image[0x7DC:0x7EC]==b'0123456789ABCDEF','complete driver / external CS digits')
        self.load,self.base=load,load*16;self.instructions,self.reachable,self.cfg=control_flow(image)
        self.uc=Uc(UC_ARCH_X86,UC_MODE_16);self.uc.mem_map(0,1<<20)
        self.initial=bytearray(b'\xA5'*(1<<20));self.initial[self.base+256:self.base+256+len(image)]=image
        self.covered=set();self.maximum_stack=0
        self.hooks=[self.uc.hook_add(UC_HOOK_CODE,self.code),self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write),self.uc.hook_add(UC_HOOK_INTR,self.interrupt)]
    def close(self):
        for h in self.hooks:self.uc.hook_del(h)
        self.hooks=[];self.uc=None
    def r(self,n):return self.uc.reg_read(REG[n])&65535
    def fail(self,error):self.error=str(error);self.uc.emu_stop()
    def code(self,uc,address,size,_):
        try:
            if address==self.base+0xFFFF:self.returned=True;uc.emu_stop();return
            ip=address-self.base
            need(ip in self.instructions and self.instructions[ip].size==size,'execution inside complete formatter/strlen instructions')
            self.covered.update(set(range(ip,ip+size))&self.reachable)
            self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
        except Exception as error:self.fail(error)
    def write(self,uc,access,address,size,value,_):
        try:
            if self.stack_base+self.stack-512<=address and address+size<=self.stack_base+self.stack:return
            need(self.write_index<len(self.expected_writes) and (address,size,value)==self.expected_writes[self.write_index],'ordered non-stack buffer writes')
            self.write_index+=1
        except Exception as error:self.fail(error)
    def interrupt(self,uc,number,_):
        try:
            need(number==0x21 and self.r('ax')>>8==2,'DOS character output only')
            value=self.r('dx')&255;i=len(self.output)
            need(i<len(self.console) and value==self.console[i],'ordered DOS bytes')
            self.output.append(value);uc.reg_write(REG['ax'],self.r('ax')&0xFF00|value)
            uc.reg_write(UC_X86_REG_EFLAGS,(self.flags&0x600)|0x8D7|2)
        except Exception as error:self.fail(error)
    def run(self,kind,*,text=b'abc',args=(7,),value=0xFFFFFFFF,radix=16,lower=0,width=6,used=2,fill=0x58,
            flags=0x202,stack=0xF800,pattern=0,split_stack=False,in_cs=False):
        need(kind in ENTRIES and len(text)<=1024 and len(args)<=32,'bounded inputs')
        need(kind in ('print_string','print_stack_string') or not flags&0x400,'forward DF precondition')
        need(2<=radix<=16 and 0<=lower<=65535 and 0<=width<=65535 and 0<=used<=65535,'bounded radix/shared frame words')
        self.uc.mem_write(0,bytes(self.initial));self.stack,self.flags=stack,flags
        ds=self.load if in_cs else 0x5000;es=0x6000;ss=0x7000 if split_stack else self.load
        self.stack_base=ss*16;data=ds*16;destination=es*16+0x4001
        def put(base,off,raw):self.uc.mem_write(base+off,raw)
        put(self.stack_base,stack-512,b'\xA5'*512);put(self.stack_base,stack,b'\xFF\xFF\x53\xA9\x65\x87')
        put(data,0x2001,text+b'\0');put(self.stack_base,0x2201,text+b'\0')
        slots=[]
        for i,v in enumerate(args):
            if isinstance(v,bytes):
                need(len(v)<=1024,'bounded far string');seg=0x4000;off=0x2401+i*0x440;put(seg*16,off,v+b'\0');slots.append(seg<<16|off)
            else:slots.append(v&0xFFFFFFFF)
        put(self.stack_base,0x3000,b''.join(struct.pack('<I',v) for v in slots))
        initial16=dict(ax=0xB53A^pattern,bx=0x3000,cx=0x1298^pattern,dx=0x2001,si=0x2001,di=0x4001,
            bp=0x5000 if kind in ('pad_field','pad_zeroes','pad_spaces','format_unsigned') else 0xA675^pattern,
            cs=self.load,ds=ds,es=es,ss=ss)
        if kind=='format_unsigned':initial16.update(bx=0x4001,dx=value&65535,cx=radix);destination=data+0x4001
        if kind=='print_stack_string':put(self.stack_base,stack+2,struct.pack('<H',0x2201))
        put(self.stack_base,0x5000-0x18,struct.pack('<H',lower));put(self.stack_base,0x5000-4,struct.pack('<H',width));put(self.stack_base,0x5000-8,struct.pack('<H',used))
        high={n:((0xA5A5^pattern)<<16) for n in GPRS};full={n:high[n]|initial16[n] for n in GPRS}
        if kind=='format_unsigned':full.update(dx=value,cx=radix)
        if kind in ('pad_field','pad_zeroes','pad_spaces'):initial16['ax']=initial16['ax']&0xFF00|fill;full['ax']=high['ax']|initial16['ax']
        before=bytes(self.uc.mem_read(0,1<<20));self.prediction=Prediction(before);p=self.prediction
        expected=dict(initial16);expected_full=dict(full);mask,flag_value=0x8D5,0x44;raw=None;self.console=b''
        if kind in ('format_into','format_print'):
            if kind=='format_print':destination=self.stack_base+stack-210
            raw=p.format(text,args,destination)
            need(kind!='format_print' or len(raw)<=210,'print wrapper bounded before caller return-address overwrite')
            if p.last_number is not None:expected_full['cx']&=65535;expected_full['dx']=p.last_number&0xFFFF0000|expected['dx']
            if kind=='format_print':
                self.console=raw.split(b'\0',1)[0];mask=0x8C5
                saved=bytearray(initial16['bp'].to_bytes(2,'little'))
                for i,b in enumerate(raw):
                    if 208<=i<=209:saved[i-208]=b
                expected['bp']=int.from_bytes(saved,'little');expected_full['bp']=high['bp']|expected['bp']
        elif kind in ('print_string','print_stack_string'):
            self.console=text.split(b'\0',1)[0];mask=0x8C5
        elif kind in ('pad_field','pad_zeroes','pad_spaces'):
            char=fill if kind=='pad_field' else 48 if kind=='pad_zeroes' else 32;amount=padding(width,used)
            for i in range(amount):p.store(destination+i,char)
            expected.update(ax=initial16['ax']&0xFF00|char,cx=0 if amount else (width-used)&65535,di=0x4001+amount)
            flag_value=cmp16((width-used)&65535,1)
        elif kind=='append_string':
            raw=text.split(b'\0',1)[0]
            for i,b in enumerate(raw+b'\0'):p.store(destination+i,b)
            expected.update(ax=initial16['ax']&0xFF00,si=0x2001+len(raw)+1,di=0x4001+len(raw));flag_value=dec16(expected['di']+1)
        elif kind=='reverse_string':
            raw=text.split(b'\0',1)[0];p.reverse(data+0x2001,raw)
            half=len(raw)//2;flag_value=cmp16(0x2001+half,0x2001+len(raw)-1-half)
        else:
            raw=digits(value,radix,lower!=0)
            for i,b in enumerate(raw[::-1]+b'\0'):p.store(destination+i,b)
            p.reverse(destination,raw[::-1]);half=len(raw)//2;flag_value=cmp16(0x4001+half,0x4001+len(raw)-1-half)
        for n in GPRS:expected_full[n]=expected_full[n]&0xFFFF0000|expected[n]
        lo,hi=self.stack_base+stack-512,self.stack_base+stack
        self.expected_writes=[w for w in p.writes if not lo<=w[0]<hi]
        for n,val in full.items():self.uc.reg_write(GPRS[n],val)
        for n in ('cs','ds','es','ss'):self.uc.reg_write(REG[n],initial16[n])
        self.uc.reg_write(UC_X86_REG_ESP,stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        self.write_index,self.error,self.returned=0,None,False;self.output=bytearray()
        try:self.uc.emu_start(self.base+ENTRIES[kind][0],self.base+0x10000,count=1000000)
        except UcError as error:raise ValueError('ZUN formatter contract: guest fault') from error
        need(self.error is None,self.error or 'guest error')
        need(self.returned and self.uc.reg_read(UC_X86_REG_ESP)==stack+(4 if kind=='print_stack_string' else 2),'near frame and exact callee cleanup')
        actual={n:self.r(n) for n in expected};actual_full={n:self.uc.reg_read(GPRS[n]) for n in GPRS}
        need(actual==expected,'full WORD/segment register result: '+str([(n,hex(actual[n]),hex(v)) for n,v in expected.items() if actual[n]!=v]))
        need(actual_full==expected_full,'DWORD register high halves: '+str([(n,hex(actual_full[n]),hex(v)) for n,v in expected_full.items() if actual_full[n]!=v]))
        actual_flags=self.uc.reg_read(UC_X86_REG_EFLAGS)
        need(actual_flags&mask==flag_value&mask,'defined final flags')
        need(actual_flags&0x600==flags&0x600,'IF/DF inherited')
        need(self.write_index==len(self.expected_writes) and self.output==self.console,'complete writes and DOS output')
        actual_memory=bytes(self.uc.mem_read(0,1<<20))
        if kind=='format_print':need(actual_memory[destination:destination+len(raw)]==raw,'actual unchecked 208-byte wrapper buffer')
        p.memory[lo:hi]=actual_memory[lo:hi];need(actual_memory==p.memory,'whole memory outside bounded stack')
        return dict(registers=actual,full_registers=actual_full,flags_mask=mask,result_flags=actual_flags&mask,
            output_hex=self.output.hex(),ordered_writes=len(self.expected_writes),writes_sha256=hashlib.sha256(json.dumps(self.expected_writes).encode()).hexdigest(),
            buffer_sha256=hashlib.sha256(raw or b'').hexdigest())


def cases():
    for kind in ('format_into','format_print'):
        for fmt,args in ((b'',()),(b'hello\\nworld\\r\\t!',()),(b'%% %q end%',()),(b'%s/%c/%u/%d/%x/%X/%b',(b'string',0,0xFFFFFFFF,0x80000000,0xDEADBEEF,0xDEADBEEF,0x80000001))):
            yield kind,dict(text=fmt,args=args)
        for value in (0,1,9,10,15,16,255,256,65535,65536,0x7FFFFFFF,0x80000000,0xFFFFFFFF):
            for spec in (b'u',b'd',b'x',b'X',b'b'):
                for prefix in (b'',b'08',b'-08'):yield kind,dict(text=b'['+b'%'+prefix+spec+b']',args=(value,))
        for value in range(256):
            yield kind,dict(text=b'%c!',args=(value,))
            yield kind,dict(text=b'%'+bytes((value,))+b'!',args=((b'Q' if value==115 else 0x12345678),))
            yield kind,dict(text=b'\\'+bytes((value,))+b'!')
        for fmt in (b'%s',b'%08s',b'%-08s',b'%2s'):
            for string in (b'',b'abc',b'\x81\xFF',b'ab\0ignored'):yield kind,dict(text=fmt,args=(string,))
    for length in (0,1,2,3,15,64,207,208,209):yield 'format_print',dict(text=b'A'*length,args=())
    for kind in ('print_string','print_stack_string','append_string','reverse_string'):
        for length in (0,1,2,3,4,15,64,255):yield kind,dict(text=bytes(65+i%26 for i in range(length)))
    for kind in ('print_string','print_stack_string'):
        for value in range(256):yield kind,dict(text=bytes((value,)),flags=0xED7)
    for kind in ('pad_field','pad_zeroes','pad_spaces'):
        for width,used in ((0,0),(0,1),(1,0),(1,1),(6,2),(0x7FFF,0),(0x8000,0),(0x8000,1),(0xFFFF,0),(0,0xFFFF),(0x7FFF,0x8000)):
            yield kind,dict(width=width,used=used,fill=0x81)
    for radix in range(2,17):
        for lower in (0,1,0xFFFF):
            for value in (0,1,9,10,15,16,255,65535,65536,0x80000000,0xFFFFFFFF):yield 'format_unsigned',dict(value=value,radix=radix,lower=lower)
    for fmt,args in ((b'%32768u',(1,)),(b'%32768s',(b'',)),(b'%65535s',(b'',)),(b'%65536u',(1,)),(b'%65537u',(1,)),(b'%65535c',(65,))):
        yield 'format_into',dict(text=fmt,args=args)


def verify(target,candidate):
    observations=[]
    for image in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(image,load)
            try:
                trace=hashlib.sha256()
                for count,(kind,options) in enumerate(cases(),1):
                    options=dict(options);options.setdefault('flags',(2,0x202,0x2D7)[count%3])
                    row=m.run(kind,pattern=0 if count&1 else 0x5A5A,stack=0xF800 if count&1 else 0xE800,split_stack=bool(count&1),in_cs=bool(count&2),**options)
                    trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.reachable,'all 666 CFG-reachable owner bytes execute; eleven dead bytes separately reviewed')
                loads.append(dict(load_segment=load,cases=count,covered_owner_bytes=len(m.covered),unreachable_owner_bytes=11,
                    maximum_observed_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'target/candidate independent formatter observations')
    return dict(images=2,functions=10,code_bytes=677,executed_owner_bytes=666,unreachable_owner_bytes=11,
        cases_per_image=sum(o['cases'] for o in observations[0]),exhaustive_byte_domains=256,observations=observations[0],
        wrapper_buffer_bytes=208,maximum_wrapper_output_bytes=209,private_data_bytes=0,private_bss_bytes=0,
        scope='real formatter/strlen instructions; forward DF precondition except print routines; DOS AH2 bounded; no output capacity checks')


def negative_controls(image):
    controls=(
        ('wrapper-reserves-208-bytes',0x641,b'\xD0',b'\xCF','format_print',{}),
        ('DOS-character-command',0x66C,b'\x02',b'\x09','print_string',{}),
        ('print-near-return',0x675,b'\xC3',b'\xCB','print_string',{}),
        ('stack-string-segment',0x67E,b'\x16',b'\x1E','print_stack_string',dict(split_stack=True)),
        ('stack-word-callee-pop',0x687,b'\x02',b'\0','print_stack_string',{}),
        ('numeric-SS-slots',0x715,b'\x36',b'\x3E','format_into',dict(text=b'%u',args=(7,),split_stack=True)),
        ('four-byte-slot-stride',0x71A,b'\x04',b'\x02','format_into',dict(text=b'%u/%u',args=(7,8))),
        ('unsigned-decimal-radix',0x71F,b'\x0A',b'\x10','format_into',dict(text=b'%u',args=(10,))),
        ('minus-before-padding',0x791,b'\x2D',b'\x2B','format_into',dict(text=b'%6d',args=(0xFFFFFFFB,))),
        ('sign-counts-in-width',0x795,b'\xF8',b'\xFC','format_into',dict(text=b'%6d',args=(0xFFFFFFFB,))),
        ('lowercase-hex-flag',0x7BB,b'\x01',b'\0','format_into',dict(text=b'%x',args=(0xABCD,))),
        ('upper-hex-radix',0x7D4,b'\x10',b'\x0A','format_into',dict(text=b'%X',args=(0xABCD,))),
        ('binary-radix',0x7F4,b'\x02',b'\x0A','format_into',dict(text=b'%b',args=(10,))),
        ('far-string-segment',0x80A,b'\x36',b'\x3E','format_into',dict(text=b'%s',args=(b'Q',),split_stack=True)),
        ('terminal-NUL-store',0x877,b'\0',b'\x01','format_into',{}),
        ('zero-padding-byte',0x87E,b'\x30',b'\x20','pad_zeroes',{}),
        ('space-padding-byte',0x884,b'\x20',b'\x30','pad_spaces',{}),
        ('padding-is-signed',0x892,b'\x7C',b'\x72','pad_field',dict(width=0x8000,used=0)),
        ('append-leaves-DI-on-NUL',0x89D,b'\x4F',b'\x47','append_string',{}),
        ('32-bit-unsigned-divisor',0x8B0,b'\xF1',b'\xF3','format_unsigned',{}),
        ('CS-digit-table',0x8B2,b'\x2E',b'\x3E','format_unsigned',{}),
        ('ASCII-case-fold-mask',0x8C1,b'\x20',b'\x40','format_unsigned',dict(lower=1,value=0xABC)),
        ('reverse-exchanges-both-bytes',0x906,b'\x86',b'\x88','reverse_string',{}),
        ('reverse-unsigned-endpoint',0x90E,b'\x73',b'\x72','reverse_string',{}),
    )
    rejected=[]
    for name,at,old,new,kind,options in controls:
        raw=bytearray(image);need(raw[at-256:at-256+len(old)]==old,'literal mutation anchor '+name)
        raw[at-256:at-256+len(new)]=new;m=None
        try:
            try:m=Machine(bytes(raw),0x3000);m.run(kind,**options)
            except ValueError:rejected.append(name)
            else:raise ValueError('ZUN formatter mutation survived: '+name)
        finally:
            if m:m.close()
    return dict(count=len(rejected),rejected=rejected)
