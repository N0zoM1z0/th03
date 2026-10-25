"""Independent arithmetic/string/port contracts for five actual root procedures.

No stack bytes are ignored. DOS INT 21h is an explicit bounded trap interface;
GRCG port requests are checked without inferring physical pixel behavior.
"""
import hashlib,json,struct
from dataclasses import replace
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INTR,UC_HOOK_INSN
from unicorn.x86_const import *
from lib.decoded_mainl_root_helpers_layout import ENTRIES,DS

GPRS={n:globals()['UC_X86_REG_E'+n.upper()] for n in ('ax','bx','cx','dx','si','di','bp','sp')}
REG={n:globals()['UC_X86_REG_'+n.upper()] for n in (*GPRS,'cs','ds','es','ss','ip')}

def need(value,message):
    if not value:raise ValueError('MAINL root helper contract: '+str(message))

def logical(value,bits):
    return (4 if (value&255).bit_count()%2==0 else 0)|(64 if value==0 else 0)|(128 if value&(1<<(bits-1)) else 0)

def folded(value):
    return value-32 if 97<=value<=122 else value

def specification(kind,regs,flags,*,random_seed,mode,color,strings,pointers,dos_status,reply_seed):
    out=dict(regs);events=[];mask=0x8C5;final=flags;depth=0
    sp,ss=regs['sp'],regs['ss']*16
    if kind=='rand':
        new=(random_seed*0x015A4E35+1)&0xFFFFFFFF
        out.update(ax=(new>>16)&0x7FFF,dx=new>>16,
                   cx=(0x4E35*(random_seed>>16)+0x15A*(random_seed&65535))&65535)
        events=[('store',regs['ds']*16+0x5B6,2,new&65535),('store',regs['ds']*16+0x5B8,2,new>>16)]
        final=(flags&0x600)|logical((new>>24)&127,8)
    elif kind=='setcolor':
        out.update(bx=sp,dx=0x7E,ax=((color&255)>>4)<<8 | (255 if color&8 else 0))
        events=[('store',ss+sp-2,2,flags),('out',0x7C,1,mode&255,0)]
        events += [('out',0x7E,1,255 if color&(1<<i) else 0,0) for i in range(4)]
        mask,depth=0x8D5,2
    elif kind=='off':
        out['ax'] &= 0xFF00;final=(flags&0x600)|logical(0,8)
        events=[('out',0x7C,1,0,flags&0x200)]
    elif kind=='keyclear':
        request=dict(regs,ax=0xC00)
        events=[('dos',0x21,request,flags)]
        for i,n in enumerate((*GPRS.keys(), 'ds','es')):
            if n!='sp':out[n]=((reply_seed+i*0x315)^dos_status)&65535
        final=(flags&0x600)|(dos_status&0x8D5)|2;mask=0x8D5
    else:
        need(kind=='compare','known complete procedure')
        a,b=strings;count=0
        for x,y in zip(a,b):
            count+=1
            if folded(x)!=folded(y):value=0;break
            if x==0:value=0x9F00;break
        else:raise ValueError('MAINL root helper contract: finite NUL/mismatch string fixture required')
        out.update(ax=value,bx=(pointers[0][1]+count)&65535,es=pointers[0][0])
        final=(flags&0x200)|logical(value,16)
        events=[('store',ss+sp-2,2,regs['bp']),('store',ss+sp-4,2,regs['si']),('store',ss+sp-6,2,regs['ds'])]
        depth=6
    out['sp']=sp+(10 if kind=='compare' else 8 if kind=='setcolor' else 4)
    return out,mask,final,events,depth

class Machine:
    def __init__(self,mz,load):
        need(mz.valid,'valid decoded MZ');self.load=load;self.base=load*16;self.ds=load+DS
        self.u=Uc(UC_ARCH_X86,UC_MODE_16);self.u.mem_map(0,1<<20)
        initial=bytearray(b'\xA5'*(1<<20));raw=mz.relocated_program_image(load)
        initial[self.base:self.base+len(raw)]=raw;self.initial=bytes(initial)
        self.instructions={};self.owned={p for s,n in ENTRIES.values() for p in range(s,s+n)}
        for start,size in ENTRIES.values():
            ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+size],start))
            need(sum(i.size for i in ins)==size,'complete instruction boundaries')
            self.instructions.update({i.address:i.size for i in ins})
        self.covered=set();self.maximum_stack=0
        self.hooks=[self.u.hook_add(UC_HOOK_CODE,self.code),self.u.hook_add(UC_HOOK_MEM_WRITE,self.write),
                    self.u.hook_add(UC_HOOK_INTR,self.interrupt),self.u.hook_add(UC_HOOK_INSN,self.out,None,1,0,UC_X86_INS_OUT)]

    def close(self):
        for h in self.hooks:self.u.hook_del(h)
        self.hooks=[];self.u=None

    def regs(self):return {n:self.u.reg_read(REG[n])&65535 for n in REG if n!='ip'}
    def fail(self,error):self.error=str(error);self.u.emu_stop()

    def event(self,event):
        need(self.index<len(self.events) and event==self.events[self.index],
             f'ordered event {self.index}: {event}; expected {self.events[self.index:self.index+1]}')
        self.observed.append(event);self.index+=1

    def code(self,u,address,size,_):
        try:
            if address==self.base+0xFFFF:self.returned=True;u.emu_stop();return
            at=address-self.base
            need(self.instructions.get(at)==size and self.start<=at<self.start+self.size,'only complete selected helper instructions')
            self.covered.update(range(at,at+size))
            self.maximum_stack=max(self.maximum_stack,self.stack-(self.u.reg_read(REG['sp'])&65535))
        except Exception as error:self.fail(error)

    def write(self,u,access,address,size,value,_):
        try:self.event(('store',address,size,value))
        except Exception as error:self.fail(error)

    def out(self,u,port,size,value,_):
        try:self.event(('out',port,size,value,u.reg_read(UC_X86_REG_EFLAGS)&0x200))
        except Exception as error:self.fail(error)

    def interrupt(self,u,vector,_):
        try:
            need(self.kind=='keyclear','DOS trap belongs only to keyclear')
            self.event(('dos',vector,self.regs(),u.reg_read(UC_X86_REG_EFLAGS)&0xED7))
            for n in (*GPRS,'ds','es'):
                if n!='sp':u.reg_write(REG[n],self.expected[n])
            u.reg_write(UC_X86_REG_EFLAGS,self.final|2)
        except Exception as error:self.fail(error)

    def run(self,kind,*,random_seed=0x89ABCDEF,mode=0xA5C0,color=0xFE0B,
            strings=(b'Abc\0',b'aBC\0'),pointers=((0x5000,0xFFFE),(0x6000,0x31)),
            seed=0x1357,flags=0x202,stack=0xF800,ss=0x7000,dos_status=0xA55A,reply_seed=0x3C69):
        need(kind in ENTRIES and 0<=random_seed<=0xFFFFFFFF and all(0<=v<=65535 for v in (mode,color,seed,dos_status,reply_seed)),'valid helper WORD/DWORD inputs')
        need(flags in (2,0x202,0x402,0xED7) and 8<=stack<=0xFFF0 and ss in (0x7000,0x8000),'bounded flags/SS/private stack')
        need(len(strings)==2 and all(isinstance(s,bytes) and 1<=len(s)<=65 and s[-1]==0 for s in strings),'bounded raw NUL strings')
        need(len(pointers)==2 and all(seg in (0x5000,0x6000) and 0<=off<=65535 for seg,off in pointers) and pointers[0][0]!=pointers[1][0],'disjoint raw string segments')
        expected=bytearray(self.initial)
        def put(at,raw):expected[at:at+len(raw)]=raw
        put(self.ds*16+0x5B6,struct.pack('<I',random_seed))
        for (seg,off),raw in zip(pointers,strings):
            for i,v in enumerate(raw):expected[seg*16+((off+i)&65535)]=v
        frame=struct.pack('<HH',0xFFFF,self.load)
        if kind=='compare':
            (a,ao),(b,bo)=pointers
            frame=struct.pack('<5H',0xFFFF,bo,b,ao,a)
        elif kind=='setcolor':frame+=struct.pack('<2H',color,mode)
        put(ss*16+stack,frame+b'\x5A\xA5');self.u.mem_write(0,bytes(expected))
        regs={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)}
        regs.update(sp=stack,cs=self.load,ds=self.ds,es=seed,ss=ss)
        high={n:((seed^0x5AA5)<<16) for n in GPRS}
        for n in GPRS:self.u.reg_write(GPRS[n],high[n]|regs[n])
        for n in ('cs','ds','es','ss'):self.u.reg_write(REG[n],regs[n])
        self.u.reg_write(UC_X86_REG_EFLAGS,flags)
        self.expected,self.mask,self.final,self.events,depth=specification(kind,regs,flags,
            random_seed=random_seed,mode=mode,color=color,strings=strings,pointers=pointers,dos_status=dos_status,reply_seed=reply_seed)
        for event in self.events:
            if event[0]=='store':_,at,size,value=event;put(at,value.to_bytes(size,'little'))
        self.kind,self.start,self.size,self.stack=kind,*ENTRIES[kind],stack
        self.index,self.error,self.returned,self.observed=0,None,False,[]
        try:self.u.emu_start(self.base+self.start,0x100000,count=10000)
        except UcError as error:raise ValueError('MAINL root helper contract: guest fault') from error
        need(self.error is None,self.error or 'guest error')
        need(self.returned and self.index==len(self.events),'complete events and native return')
        actual=self.regs();need(actual==self.expected,'complete independent WORD/segment return ABI: '+str((actual,self.expected)))
        need(all(self.u.reg_read(GPRS[n])==high[n]|self.expected[n] for n in GPRS),'all DWORD GPR high halves including ESP')
        final=self.u.reg_read(UC_X86_REG_EFLAGS)
        need(final&self.mask==self.final&self.mask and final&0x600==self.final&0x600,'defined arithmetic flags / IF / DF')
        need(bytes(self.u.mem_read(0,1<<20))==expected,'whole physical memory including every stack and caller argument byte')
        return dict(kind=kind,registers=actual,flags=final&(self.mask|0x600),events=self.observed,
                    random_seed=int.from_bytes(self.u.mem_read(self.ds*16+0x5B6,4),'little'),stack_depth=depth)

def cases():
    for value in range(65536):
        yield 'rand',dict(random_seed=0xA7F00000|value)
        yield 'rand',dict(random_seed=(value<<16)|0xD263)
    for a in range(256):
        for b in range(256):yield 'compare',dict(strings=(bytes((a,0)),bytes((b,0))))
    for value in range(256):
        yield 'setcolor',dict(mode=value,color=0xA50B)
        yield 'setcolor',dict(mode=0xA5C0,color=value)
        yield 'setcolor',dict(mode=value<<8|0xC0,color=value<<8|0x0B)
        yield 'off',dict(seed=value<<8|0x53)
        yield 'keyclear',dict(dos_status=value)
        yield 'keyclear',dict(dos_status=value<<8)
    for text in (b'',b'aBcDeF',bytes(range(1,65)),b'\x80\xFF\x60\x7B',b'X'*64):
        for off in (0,1,0xFFFE,0xFFFF):
            for flags in (2,0x202,0x402,0xED7):
                yield 'compare',dict(strings=(text+b'\0',text.swapcase()+b'\0'),pointers=((0x5000,off),(0x6000,off)),flags=flags)
    for kind in ENTRIES:
        for flags in (2,0x202,0x402,0xED7):
            for ss in (0x7000,0x8000):
                yield kind,dict(flags=flags,ss=ss,random_seed=0xFFFFFFFF)

def verify(target,candidate):
    results=[]
    for image in (target,candidate):
        rows=[]
        for load in (0x1000,0x3000):
            m=Machine(image,load);trace=hashlib.sha256();counts={n:0 for n in ENTRIES}
            try:
                for count,(kind,p) in enumerate(cases(),1):
                    q=dict(seed=0x1357 if count&1 else 0xECA8,stack=0x80 if count&1 else 0xFFF0);q.update(p)
                    r=m.run(kind,**q)
                    counts[kind]+=1;trace.update(json.dumps(r,sort_keys=True).encode())
                need(m.covered==m.owned,'all 150 owner bytes execute; no alignment credit')
                rows.append(dict(load_segment=load,cases=count,cases_by_function=counts,executed_owner_bytes=len(m.covered),
                    maximum_observed_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        results.append(rows)
    need(results[0]==results[1],'independent target/candidate helper observations agree')
    return dict(images=2,functions=5,code_bytes=150,executed_owner_bytes=150,cases_per_image=sum(o['cases'] for o in results[0]),
        observations=results[0],exhaustive_random_seed_WORD_lanes=65536,exhaustive_character_pairs=65536,
        ignored_stack_bytes=0,physical_DOS_or_pixels_emulated=False)

def negative_controls(target):
    controls=(
        ('keyclear-AH-request',0x700,1,'keyclear',{}),('keyclear-interrupt-vector',0x702,1,'keyclear',{}),
        ('keyclear-far-return',0x703,8,'keyclear',{}),('mode-stack-slot',0xC3B,2,'setcolor',{}),
        ('color-stack-slot',0xC3F,2,'setcolor',{}),('tile-port',0xC41,1,'setcolor',{}),
        ('mode-port',0xC46,2,'setcolor',{}),('CLI-through-all-port-writes',0xC44,1,'setcolor',{}),
        ('fourth-color-bit',0xC57,1,'setcolor',{}),('restore-incoming-flags',0xC5B,1,'setcolor',{}),
        ('far-Pascal-pop-four',0xC5D,2,'setcolor',{}),('off-clears-AL',0xC60,1,'off',{}),
        ('off-port',0xC63,1,'off',{}),('random-low-multiplier',0x1A3F,1,'rand',{}),
        ('random-high-multiplier',0x1A48,1,'rand',{}),('random-add-one',0x1A58,1,'rand',{}),
        ('random-carry',0x1A5A,0x10,'rand',dict(random_seed=(65535*pow(0x4E35,-1,65536))&65535)),
        ('random-WORD-store',0x1A5C,1,'rand',{}),('random-return-mask',0x1A66,0x80,'rand',dict(random_seed=0xFFFFFFFF)),
        ('compare-clears-DF',0x2C35,1,'compare',dict(flags=0xED7)),
        ('compare-first-far-pointer-slot',0x2C38,2,'compare',{}),
        ('compare-case-range',0x2C44,1,'compare',dict(strings=(b'Z\0',b'z\0'))),
        ('compare-second-uppercase',0x2C53,1,'compare',{}),
        ('compare-NUL-loop',0x2C59,1,'compare',dict(strings=(b'\0',b'\0'))),
        ('compare-mismatch-zero',0x2C5E,1,'compare',dict(strings=(b'A\0',b'B\0'))),
        ('compare-near-pop-eight',0x2C66,2,'compare',{}))
    rejected=[]
    for name,address,xor,kind,p in controls:
        raw=bytearray(target.program_image);raw[address]^=xor
        m=Machine(replace(target,program_image=bytes(raw)),0x1000)
        try:m.run(kind,**p)
        except (ValueError,UcError):rejected.append(name)
        else:raise ValueError('actual root instruction mutation escaped: '+name)
        finally:m.close()
    return dict(count=len(rejected),rejected=rejected,actual_guest_instruction_mutations=True,alignment_mutations_counted=False)
