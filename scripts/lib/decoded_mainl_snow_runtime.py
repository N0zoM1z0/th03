"""Live snow state, real RNG/vector/flake instructions and native call frames.

The vector's table and particle/sprite storage are external data. PMD is a
bounded AX/flags reply; counter updates and ports do not prove physical timing.
"""
import hashlib
import itertools
import json
import struct
from dataclasses import replace
from functools import lru_cache
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR, UC_HOOK_INSN
from unicorn.x86_const import *
from lib.decoded_mainl_snow_layout import CS, DS, START, SIZE, DATA, ENTRIES
from lib.decoded_mainl_pi_runtime import Spec as Frames, Machine as Physical, arithmetic, signed, ARITH
from lib.decoded_mainl_pi_free_runtime import address
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG, logical, specification as random_spec
from lib.decoded_mainl_staff_draw_runtime import Spec as FlakeSpec

CONTEXT = {'rand':(0,0x1A3E,42,4),'vector':(0xC7E,0x110,69,16),'flake':(CS,0x249A,76,8)}
CONTEXT_AT = {s*16+a:(kind,n,frame) for kind,(s,a,n,frame) in CONTEXT.items()}
ENTRY_AT = {CS*16+a:(kind,n,args+2) for kind,(a,n,args) in ENTRIES.items()}
GRAPH = bytes(((i*13)^(i>>7)^0xA5)&255 for i in range(65538))


@lru_cache(maxsize=16)
def particle_fixture(alive,alive_byte):
    # Cache only immutable external input construction, never guest execution.
    return b''.join(struct.pack('<BB5H4B',alive_byte if alive=='all' or alive=='mixed' and i%3 else 0,
        0x71,(160+i*16)&65535,(320+i*16)&65535,(-17)&65535,31,i%4,1,2,3,4) for i in range(255))


def need(value,message):
    if not value:
        raise ValueError('MAINL snow contract: '+str(message))


def signed32(value):
    return value-(1<<32) if value&(1<<31) else value


class Spec(Frames):
    def __init__(self,*args):
        super().__init__(*args)
        self.mask = ARITH
        self.calls = {}
        self.prefix = False
        self.polls = 0

    def dg(self,offset,size=2):
        at = address(self.ds,offset)
        return int.from_bytes(self.memory[at:at+size],'little')

    def field(self,offset,value,size=2):
        self.store(address(self.ds,offset),size,value)

    def op(self,left,right,subtract=False,bits=16):
        mask = (1<<bits)-1
        value = (left-right if subtract else left+right)&mask
        carry = left<right if subtract else left+right>mask
        overflow = ((left^right)&(left^value) if subtract else ~(left^right)&(left^value))&(1<<(bits-1))
        self.flags = (self.flags&0x600)|2|logical(value,bits)|int(carry)|(16 if (left^right^value)&16 else 0)|(0x800 if overflow else 0)
        self.mask = ARITH
        return value

    def logical(self,value,bits=16):
        self.flags = (self.flags&0x600)|2|logical(value,bits)
        self.mask = 0x8C5

    def full32(self,name,value):
        value &= 0xFFFFFFFF
        self.high[name],self.r[name] = value&0xFFFF0000,value&65535

    def entry(self,kind,size):
        at = address(self.ss,self.r['sp'])
        self.events.append(('entry',kind,self.full(),bytes(self.memory[at:at+size]).hex()))
        self.calls[kind] = self.calls.get(kind,0)+1

    def near(self,kind,continuation):
        self.push(continuation)
        self.invoke(kind)

    def rand(self,continuation):
        self.frame(continuation)
        self.entry('rand',4)
        entry_sp = self.r['sp']
        out,mask,flags,events,_ = random_spec('rand',self.r,self.flags,random_seed=self.dg(DATA['seed'],4),
            mode=0,color=0,strings=(b'\0',b'\0'),pointers=((0x5000,0),(0x6000,0)),dos_status=0,reply_seed=0)
        self.events.extend(events)
        for _,at,size,value in events:
            self.memory[at:at+size] = value.to_bytes(size,'little')
        self.r,self.flags,self.mask = out,flags|2,mask
        self.r['cs'] = self.word(self.ss,entry_sp+2)

    def vector(self,continuation):
        self.frame(continuation)
        self.r['cs'] = self.o['load']+0xC7E
        self.entry('vector',16)
        sp = self.r['sp']
        length = self.word(self.ss,sp+4)
        angle = self.memory[address(self.ss,sp+6)]
        vy = (self.word(self.ss,sp+8),self.word(self.ss,sp+10))
        vx = (self.word(self.ss,sp+12),self.word(self.ss,sp+14))
        self.enter()
        self.push(self.r['si'])
        self.r['si'] = length
        cosine = signed(self.dg(DATA['cos']+2*angle))
        sine = signed(self.dg(DATA['sin']+2*angle))
        self.full32('dx',cosine)
        self.full32('cx',sine)
        self.full32('ax',(signed(length)*cosine)>>8)
        self.r['bx'],self.r['es'] = vx
        self.store(address(vx[1],vx[0]),2,self.r['ax'])
        product = (signed(length)*sine)&0xFFFFFFFF
        result = (signed32(product)>>8)&0xFFFFFFFF
        self.full32('ax',result)
        self.r['bx'],self.r['es'] = vy
        self.store(address(vy[1],vy[0]),2,self.r['ax'])
        self.flags = (self.flags&0x600)|2|logical(result,32)|((product>>7)&1)
        self.mask = 0xC5  # Multi-bit SAR leaves OF/AF undefined.
        self.pop('si')
        self.pop('bp')
        self.returned(12)

    def flake(self):
        self.entry('flake',8)
        sp = self.r['sp']
        index,top,left = [self.word(self.ss,sp+2+2*i) for i in range(3)]
        child = FlakeSpec(self.memory,self.r,self.high,self.flags,dict(load=self.o['load'],stack=sp,left=left,top=top,index=index))
        child.run('flake')
        self.events.extend(child.events)
        self.r,self.high,self.flags,self.mask = child.r,child.high,child.flags,ARITH

    def finish(self,args=0,locals_=False):
        if locals_:
            self.r['sp'] = self.r['bp']
        self.pop('bp')
        self.r['sp'] += 2+args

    def invoke(self,kind):
        self.entry(kind,2+ENTRIES[kind][2])
        args = [self.word(self.ss,self.r['sp']+2+2*i) for i in range(ENTRIES[kind][2]//2)]
        self.enter(2 if kind=='spawn' else 0)
        if kind=='clear':
            self.push(self.r['di'])
            self.r.update(ax=0,cx=0,es=0xA800)
            self.logical(0)
            di = 0
            step = -2 if self.flags&0x400 else 2
            for _ in range(16000):
                self.store(address(0xA800,di),2,0)
                di = (di+step)&65535
            self.pop('di')
            self.finish()
        elif kind=='reset':
            self.push(self.r['si'])
            for i in range(80):
                self.field(DATA['flakes']+i*16,0,1)
            self.r['ax'] = 80
            self.op(80,80,True)
            self.pop('si')
            self.finish()
        elif kind in ('spawn','update','render'):
            self.push(self.r['si'])
            if kind!='update':
                self.push(self.r['di'])
            self.r['si'] = DATA['flakes']
            index = 0
            if kind=='update':
                self.r['dx'] = 0
            else:
                self.r['di'] = 0
            while True:
                cap = self.dg(DATA['cap'],1)
                self.r['ax'] = cap
                self.op(cap,index,True)
                if cap<=index:
                    break
                at = self.r['si']
                alive = self.dg(at,1)
                self.op(alive,0,True,bits=8)
                if kind=='spawn':
                    if not alive:
                        self.r['ax'] = index*8
                        frame = self.dg(DATA['frame'])
                        self.op(self.r['ax'],frame,True)
                        if index*8<=signed(frame):
                            self.field(at,1,1)
                            self.logical(index&3)
                            if index&3:
                                self.rand(0x25BE)
                                self.r['bx'] = 10112
                                self.r['ax'],self.r['dx'] = divmod(self.r['ax'],10112)
                                self.field(at+2,self.r['dx'])
                                self.field(at+4,0)
                            else:
                                self.field(at+2,10112)
                                self.rand(0x25D8)
                                self.r['bx'] = 6272
                                self.r['ax'],self.r['dx'] = divmod(self.r['ax'],6272)
                                self.field(at+4,self.r['dx'])
                            self.rand(0x25E6)
                            self.r['bx'] = 32
                            self.r['ax'],self.r['dx'] = divmod(self.r['ax'],32)
                            self.r['dx'] = self.op(self.r['dx'],80,bits=8)
                            self.store(address(self.ss,self.r['bp']-1),1,self.r['dx'])
                            self.rand(0x25F7)
                            self.r['bx'] = 64
                            self.r['ax'],self.r['dx'] = divmod(self.r['ax'],64)
                            self.r['dx'] = self.op(self.r['dx'],48,bits=8)
                            self.store(address(self.ss,self.r['bp']-2),1,self.r['dx'])
                            self.rand(0x2608)
                            self.r['ax'] &= 3
                            self.logical(self.r['ax'])
                            self.field(at+10,self.r['ax'])
                            self.push(self.ds)
                            self.r['ax'] = (at+6)&65535
                            self.push(self.r['ax'])
                            self.push(self.ds)
                            self.r['ax'] = (at+8)&65535
                            self.push(self.r['ax'])
                            # This WORD includes the byte next to the angle;
                            # the actual vector consumes only its low BYTE.
                            self.push(self.word(self.ss,self.r['bp']-1))
                            self.r['ax'] = self.memory[address(self.ss,self.r['bp']-2)]
                            self.push(self.r['ax'])
                            self.vector(0x2626)
                elif alive and kind=='update':
                    self.field(at,1,1)
                    self.r['ax'] = self.dg(at+6)
                    self.field(at+2,self.op(self.dg(at+2),self.r['ax']))
                    self.r['ax'] = self.dg(at+8)
                    self.field(at+4,self.op(self.dg(at+4),self.r['ax']))
                    left = self.dg(at+2)
                    self.op(left,0,True)
                    if signed(left)<=0:
                        self.field(at+2,self.op(left,10112))
                    top = self.dg(at+4)
                    self.op(top,6272,True)
                    if signed(top)>=6272:
                        self.field(at+4,self.op(top,6272,True))
                elif alive and kind=='render':
                    self.r['ax'] = (signed(self.dg(at+2))>>4)&65535
                    self.push(self.r['ax'])
                    self.r['ax'] = (signed(self.dg(at+4))>>4)&65535
                    self.push(self.r['ax'])
                    self.push(self.dg(at+10))
                    self.push(0x26A4)
                    self.flake()
                index += 1
                self.r['dx' if kind=='update' else 'di'] = index
                self.r['si'] = self.op(at,16)
            if kind!='update':
                self.pop('di')
            self.pop('si')
            self.finish(locals_=kind=='spawn')
        elif kind=='gate':
            frames,measure = args
            active = self.dg(DATA['active'],1)
            self.op(active,0,True,bits=8)
            if active:
                self.r['ax'] = (self.r['ax']&255)|0x500
                mask = ARITH|0x600
                self.events.append(('pmd',0x60,self.full(),self.flags&mask,mask))
                for offset,raw in self.o['pmd_writes']:
                    location = address(self.ds,offset)
                    self.events.append(('pmd-write',location,raw.hex()))
                    self.memory[location:location+len(raw)] = raw
                self.r['ax'] = self.o['pmd_measure']
                self.flags = (self.flags&0x600)|2|(self.o['pmd_flags']&ARITH)
                self.op(self.r['ax'],measure,True)
                yes = self.r['ax']>=measure
                if yes:
                    frame = self.dg(DATA['frame'])
                    self.op(frame,192,True)
                    yes = signed(frame)>192
            else:
                self.r['ax'] = self.dg(DATA['frame'])
                self.op(self.r['ax'],frames,True)
                yes = signed(self.r['ax'])>signed(frames)
            self.r['ax'] = int(yes)
            if not yes:
                self.logical(0)
            self.finish(4)
        else:
            need(kind=='tick','known full snow procedure')
            for name,continuation in (('spawn',0x26EB),('update',0x26EE),('render',0x26F1)):
                self.near(name,continuation)
            adapt = self.dg(DATA['adapt'],1)
            self.op(adapt,0,True,bits=8)
            if adapt:
                value = self.dg(DATA['vsync'])
                self.op(value,1,True)
                if value>1:
                    self.field(DATA['slow'],0,1)
                    self.field(DATA['cap'],50,1)
                    self.field(DATA['adapt'],0,1)
            while True:
                if self.o['prefix'] and self.polls==self.o['prefix']:
                    mask = ARITH|0x600
                    self.events.append(('prefix',self.polls,self.full(),self.flags&mask))
                    self.prefix = True
                    return
                ticks = self.o['ticks']
                if ticks is None:
                    value = self.dg(DATA['vsync'])
                    need(value!=0 or self.o['prefix'],'readonly zero requires the native closed-cycle prefix contract')
                else:
                    need(self.polls<len(ticks),'complete progressing counter fixture')
                    value = ticks[self.polls]
                    self.memory[address(self.ds,DATA['vsync']):address(self.ds,DATA['vsync'])+2] = struct.pack('<H',value)
                self.events.append(('poll',value))
                self.polls += 1
                self.op(value,0,True)
                if value:
                    break
            self.field(DATA['vsync'],0)
            self.r['dx'] = 0xA4
            page = self.dg(DATA['page'],1)
            self.r['ax'] = (self.r['ax']&0xFF00)|page
            self.events.append(('out',0xA4,1,page,self.flags&0x200))
            value = self.op(1,page,True,bits=8)
            self.r['ax'] = (self.r['ax']&0xFF00)|value
            self.field(DATA['page'],value,1)
            self.r['dx'] = 0xA6
            self.events.append(('out',0xA6,1,value,self.flags&0x200))
            self.finish()

    def run(self,kind):
        self.invoke(kind)
        return self.full(),self.flags,self.mask,self.calls


class Machine(Physical):
    def __init__(self,image,load):
        need(image.valid,'valid decoded MZ')
        self.load,self.base,self.cs,self.ds = load,load*16,load+CS,load+DS
        self.u = Uc(UC_ARCH_X86,UC_MODE_16)
        self.u.mem_map(0,1<<20)
        memory = bytearray(b'\xA5'*(1<<20))
        raw = image.relocated_program_image(load)
        memory[self.base:self.base+len(raw)] = raw
        memory[0xA8000:0xA8000+len(GRAPH)] = GRAPH
        self.initial = bytes(memory)
        self.instructions,self.covered = {},set()
        self.owner = set(range(CS*16+START,CS*16+START+SIZE))
        for start,size in [(CS*16+START,SIZE),*[(s*16+a,n) for s,a,n,_ in CONTEXT.values()]]:
            ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[start:start+size],start))
            need(sum(i.size for i in ins)==size,'complete snow/RNG/vector/flake boundaries')
            self.instructions.update({i.address:i.size for i in ins})
        self.hooks = [self.u.hook_add(UC_HOOK_CODE,self.code),self.u.hook_add(UC_HOOK_MEM_WRITE,self.write),
                      self.u.hook_add(UC_HOOK_INTR,self.interrupt),self.u.hook_add(UC_HOOK_INSN,self.out,None,1,0,UC_X86_INS_OUT)]

    def regs(self,full=False):
        values = super().regs(full)
        values.update(fs=self.u.reg_read(UC_X86_REG_FS),gs=self.u.reg_read(UC_X86_REG_GS))
        return values

    def out(self,u,port,size,value,_):
        try:
            self.event(('out',port,size,value,u.reg_read(UC_X86_REG_EFLAGS)&0x200))
        except Exception as error:
            self.fail(error)

    def interrupt(self,u,number,_):
        try:
            mask = ARITH|0x600
            self.event(('pmd',number,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
            for offset,raw in self.o['pmd_writes']:
                location = address(self.ds,offset)
                self.event(('pmd-write',location,raw.hex()))
                u.mem_write(location,raw)
            u.reg_write(REG['ax'],self.o['pmd_measure'])
            u.reg_write(UC_X86_REG_EFLAGS,(u.reg_read(UC_X86_REG_EFLAGS)&0x600)|2|(self.o['pmd_flags']&ARITH))
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
            if offset in ENTRY_AT or offset in CONTEXT_AT:
                kind,_,frame_size = (ENTRY_AT if offset in ENTRY_AT else CONTEXT_AT)[offset]
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                if self.index<len(self.events) and self.events[self.index][0]=='far-frame':
                    ip,cs = struct.unpack('<2H',bytes(u.mem_read(address(ss,sp),4)))
                    self.event(('far-frame',address(ss,sp),ip,cs))
                self.event(('entry',kind,self.regs(True),bytes(u.mem_read(address(ss,sp),frame_size)).hex()))
            if offset==CS*16+0x270E:
                if self.o['prefix'] and self.polls==self.o['prefix']:
                    self.event(('prefix',self.polls,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)))
                    self.stopped_prefix = True
                    u.emu_stop()
                    return
                ticks = self.o['ticks']
                value = int.from_bytes(u.mem_read(address(self.ds,DATA['vsync']),2),'little') if ticks is None else ticks[self.polls]
                self.event(('poll',value))
                if ticks is not None:
                    u.mem_write(address(self.ds,DATA['vsync']),struct.pack('<H',value))
                self.polls += 1
            need(self.instructions.get(offset)==size,'only actual snow / RNG / vector / owned flake instructions')
            self.covered.update(range(offset,offset+size))
        except Exception as error:
            self.fail(error)

    def run(self,kind,*,cap=80,frame=639,alive='mixed',alive_byte=2,random_seed=1,vsync=1,page=0,slow=1,adapt=1,
            active=0,measure=4,frames=100,pmd_measure=4,pmd_flags=0x8D5,pmd_writes=(),ticks=(1,),prefix=0,
            particle0=None,table='native',flags=0x202,ss=0x7000,stack=0xF800,seed=0x1357,persistent=False):
        need(kind in ENTRIES and all(0<=v<=255 for v in (cap,alive_byte,page,slow,adapt,active)),'BYTE live state fixture')
        need(all(0<=v<=65535 for v in (frame,vsync,measure,frames,pmd_measure,pmd_flags)) and 0<=random_seed<=0xFFFFFFFF,
             'WORD/DWORD counters, arguments and RNG seed')
        need(alive in ('none','all','mixed') and table in ('native','signed','zero'),'bounded particle/table fixture')
        need(ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),'foreign SS and incoming flag fixture')
        need(prefix in (0,1,3,7) and (not prefix or kind=='tick' and ticks is None and vsync==0),'native immutable-zero polling prefix')
        need(ticks is None or ticks and all(0<=v<=65535 for v in ticks),'bounded counter update sequence')
        need(all(0<=off<off+len(raw)<=65536 and isinstance(raw,bytes) for off,raw in pmd_writes),'bounded PMD DATA writes')
        memory = bytearray(self.u.mem_read(0,1<<20) if persistent else self.initial)
        def put(offset,value,size=2):
            at = address(self.ds,offset)
            memory[at:at+size] = value.to_bytes(size,'little')
        if not persistent:
            at = address(self.ds,DATA['flakes'])
            memory[at:at+255*16] = particle_fixture(alive,alive_byte)
            for name,value in (('cap',cap),('page',page),('slow',slow),('adapt',adapt),('active',active)):
                put(DATA[name],value,1)
            for name,value in (('frame',frame),('vsync',vsync)):
                put(DATA[name],value)
            put(DATA['seed'],random_seed,4)
            if table!='native':
                for i in range(320):
                    put(DATA['sin']+2*i,((i*3187)^0xA55A)&65535 if table=='signed' else 0)
        if particle0 is not None:
            on,left,top,vx,vy,cel = particle0
            need(0<=on<=255 and all(0<=v<=65535 for v in (left,top,vx,vy,cel)),'explicit raw first particle')
            put(DATA['flakes'],on,1)
            for delta,value in zip((2,4,6,8,10),(left,top,vx,vy,cel)):
                put(DATA['flakes']+delta,value)
        args = (frames,measure) if kind=='gate' else ()
        at = address(ss,stack)
        memory[at:at+2+len(args)*2] = struct.pack('<'+'H'*(1+len(args)),0xFFFF,*args)
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
        self.o = dict(load=self.load,stack=stack,pmd_measure=pmd_measure,pmd_flags=pmd_flags,pmd_writes=pmd_writes,ticks=ticks,prefix=prefix)
        spec = Spec(memory,regs,self.high,flags,self.o)
        expected,final,mask,calls = spec.run(kind)
        self.events = spec.events
        self.index,self.error,self.returned,self.stopped_prefix,self.max_depth,self.polls,self.far_word_hooks = 0,None,False,False,0,0,0
        try:
            self.u.emu_start(self.cs*16+ENTRIES[kind][0],1<<20,count=500000)
        except UcError as error:
            raise ValueError('MAINL snow contract: guest fault') from error
        need(self.error is None,self.error or 'guest failure')
        need(self.index==len(self.events) and (self.stopped_prefix if prefix else self.returned),'complete expected events and real return / proved prefix boundary')
        need(self.regs(True)==expected,'all DWORD/segment effects '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(mask|0x600)==final&(mask|0x600),'defined return / prefix flags and IF/DF')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'whole flat memory including live aliases, native frames and every caller byte')
        return dict(kind=kind,registers=expected,flags=final&(mask|0x600),flag_mask=mask|0x600,calls=calls,
            polls=self.polls,nonterminal_prefix=bool(prefix),stack_depth=self.max_depth,events=len(self.events),
            final_seed=int.from_bytes(memory[address(self.ds,DATA['seed']):address(self.ds,DATA['seed'])+4],'little'),
            trace_sha256=hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest())


def geometry_proof(image):
    for at,raw in ((0x256A,b'\x31\xC0\x89\xC7\xB9\x80\x3E\xF3\xAB'),
        (0x257D,b'\x33\xC0'),(0x2584,b'\x40\x83\xC6\x10\x3D\x50\0\x7C\xF4'),
        (0x2599,b'\x33\xFF'),(0x2626,b'\x47\x83\xC6\x10\xA0\xC0\x22\xB4\0\x3B\xC7\x0F\x8F\x69\xFF'),
        (0x2640,b'\x33\xD2'),(0x266F,b'\x42\x83\xC6\x10\xA0\xC0\x22\xB4\0\x3B\xC2\x7F\xC8'),
        (0x2687,b'\x33\xFF'),(0x26A4,b'\x47\x83\xC6\x10\xA0\xC0\x22\xB4\0\x3B\xC7\x7F\xDA'),
        (0x25BE,b'\xBB\x80\x27\x99\xF7\xFB'),(0x25D8,b'\xBB\x80\x18\x99\xF7\xFB'),
        (0x25E6,b'\xBB\x20\0\x99\xF7\xFB\x80\xC2\x50'),(0x25F7,b'\xBB\x40\0\x99\xF7\xFB\x80\xC2\x30'),
        (0x2608,b'\x25\x03\0'),(0x270E,b'\x83\x3E\x4E\x14\0\x74\xF9')):
        need(image.program_image[CS*16+at:CS*16+at+len(raw)]==raw,'native finite loops / positive IDIV domains / closed polling CFG')
    for value in range(32768):
        need(0<=value%10112<10112 and 0<=value%6272<6272 and 80<=value%32+80<=111
             and 48<=value%64+48<=111 and 0<=value&3<=3,'all masked RNG outputs and native quotient/remainder bounds')
    for cap in range(256):
        need(all(DATA['flakes']+16*i>=DATA['cap']+2 and DATA['flakes']+16*i+15<65536 for i in range(cap)),
             'all BYTE capacities stay disjoint from the live capacity byte without WORD pointer wrap')
    return dict(BYTE_capacity_states=256,maximum_loop_iterations=255,clear_WORD_stores=16000,reset_alive_BYTES=80,
        masked_random_output_states=32768,maximum_rand_calls_per_spawn=1020,maximum_vector_calls_per_spawn=255,
        maximum_flake_calls_per_render=255,maximum_render_WORD_stores=2040,
        closed_poll=dict(segment=CS,offset=0x270E,bytes=7,counter_offset=DATA['vsync'],counter_value=0,
                         cfg_instructions=['CMP WORD [vsync_Count1],0','JE same CMP'],
                         invariant='all registers, stack and memory fixed; defined flags after CMP are ZF/PF with CF/OF/AF/SF clear',
                         assumptions=['counter stays zero; no external IRQ/device/DOS memory changes',
                                      'all preparatory native callees return; mapped disjoint CODE/DGROUP/stack']),
        budget_expiry_used=False,guest_iterations_skipped=False,physical_IRQ_or_timing_proved=False)


def seed_for_first_output(value):
    return (((value<<16)|0xA55A)-1)*pow(0x015A4E35,-1,1<<32)&0xFFFFFFFF


@lru_cache(maxsize=1)
def vector_pair_seeds():
    found = {}
    for seed in range(1<<20):
        state = (seed*0x015A4E35+1)&0xFFFFFFFF
        state = (state*0x015A4E35+1)&0xFFFFFFFF
        angle = ((state>>16)&0x7FFF)%32+80
        state = (state*0x015A4E35+1)&0xFFFFFFFF
        length = ((state>>16)&0x7FFF)%64+48
        found.setdefault((angle,length),seed)
        if len(found)==2048:
            break
    need(len(found)==2048,'deterministic seed fixtures cover every32x64 vector pair')
    return tuple((a,n,s) for (a,n),s in sorted(found.items()))


def cases():
    for flags,ss,stack in itertools.product((2,0x202,0x402,0xED7),(0x7000,0x8000),(0x80,0xF800)):
        yield 'clear',dict(flags=flags,ss=ss,stack=stack)
    for value in range(32768):
        yield 'spawn',dict(cap=1,alive='none',frame=0,random_seed=seed_for_first_output(value))
    for _,_,seed in vector_pair_seeds():
        yield 'spawn',dict(cap=1,alive='none',frame=0,random_seed=seed,table='signed')
    for kind,cap in itertools.product(('reset','spawn','update','render','tick'),range(256)):
        yield kind,dict(cap=cap,alive='none' if kind=='spawn' else 'mixed',frame=0x7F00)
    for kind,cap,frame,alive in itertools.product(('spawn','update','render','tick'),(0,1,4,50,79,80,81,82,85,255),
            (0xFFFF,0,7,8,639,640,647,648,2040,0x7FFF,0x8000),('none','all','mixed')):
        yield kind,dict(cap=cap,frame=frame,alive=alive)
    for kind,field,shift,value in itertools.product(('gate',),('frame','frames','measure','pmd_measure'),(0,8),range(256)):
        for active in (0,255):
            yield kind,dict(cap=0,active=active,**{field:value<<shift})
    for kind,fields in (('update',range(4)),('render',(0,1,4))):
        for field,shift,value in itertools.product(fields,(0,8),range(256)):
            particle = [2,32,64,0xFFFF,1,0]
            particle[field+1] = value<<shift
            yield kind,dict(cap=1,particle0=tuple(particle))
    for kind,value in itertools.product(('update','render'),range(256)):
        yield kind,dict(cap=1,particle0=(value,0x8000,0xFFFF,0xFFFF,1,0xFFFF))
    for value,shift in itertools.product(range(256),(0,8)):
        yield 'spawn',dict(cap=2,alive='none',frame=8,random_seed=value<<shift)
    for field in ('page','adapt','slow','vsync'):
        for value,shift in itertools.product(range(256),(0,8) if field=='vsync' else (0,)):
            yield 'tick',dict(cap=1,frame=0,alive='none',**{field:value<<shift})
    for kind,flags,ss,stack in itertools.product(ENTRIES,(2,0x202,0x402,0xED7),(0x7000,0x8000),(0x80,0xF800)):
        yield kind,dict(cap=2,flags=flags,ss=ss,stack=stack,table='signed',active=255,pmd_measure=0xFFFF)
    for kind in ('spawn','tick'):
        yield kind,dict(cap=255,frame=0x7F00,alive='none',table='signed')
    for frame in (0,192,193,0x7FFF,0xFFFF):
        yield 'gate',dict(active=255,pmd_writes=((DATA['frame'],struct.pack('<H',frame)),))
    for cap,prefix,flags in itertools.product((0,81,255),(1,3,7),(2,0xED7)):
        yield 'tick',dict(cap=cap,vsync=0,ticks=None,prefix=prefix,flags=flags)


def verify(target,candidate):
    proof = geometry_proof(target)
    need(proof==geometry_proof(candidate),'both complete native loop/poll proofs')
    observations = []
    context = {a for s,o,n,_ in CONTEXT.values() for a in range(s*16+o,s*16+o+n)}
    for image_index,image in enumerate((target,candidate),1):
        rows = []
        for load in (0x1000,0x3000):
            m = Machine(image,load)
            trace = hashlib.sha256()
            counts,maximums = {k:0 for k in ENTRIES},{k:0 for k in ('rand','vector','flake')}
            peak,prefixes,pairs = 0,0,set()
            try:
                def entry(kind,parameters):
                    nonlocal peak,prefixes
                    result = m.run(kind,**parameters)
                    counts[kind] += 1
                    peak = max(peak,result['stack_depth'])
                    prefixes += int(result['nonterminal_prefix'])
                    for k in maximums:
                        maximums[k] = max(maximums[k],result['calls'].get(k,0))
                    for e in m.events:
                        if e[:2]==('entry','vector'):
                            frame = struct.unpack('<8H',bytes.fromhex(e[3]))
                            pairs.add((frame[3]&255,frame[2]))
                    trace.update(json.dumps(result,sort_keys=True).encode())
                for count,(kind,parameters) in enumerate(cases(),1):
                    entry(kind,dict(seed=0x1357 if count&1 else 0xECA8,**parameters))
                    if count%2048==0:
                        print(f'Snow: image {image_index}, load {load:04X}, {count} complete entries / proved prefixes',flush=True)
                for kind in ('spawn','update','render','tick'):
                    for i in range(3):
                        entry(kind,dict(cap=81,frame=0x7F00,alive='none',vsync=2,ticks=(0,1),persistent=i>0))
                        count += 1
                need(m.owner<=m.covered and context<=m.covered,'all464 owner bytes and187 actual context bytes execute')
                need(pairs=={(a,n) for a in range(80,112) for n in range(48,112)},'all2048 actual vector argument pairs')
                rows.append(dict(load_segment=load,cases=count,cases_by_function=counts,executed_owner_bytes=464,
                    actual_context_bytes=187,maximum_stack_depth=peak,nonterminal_prefix_cases=prefixes,
                    terminal_cases=count-prefixes,maximum_actual_calls=maximums,actual_vector_pairs=len(pairs),trace_sha256=trace.hexdigest()))
                print(f'Snow: image {image_index}, load {load:04X}, {count} entries / 464 owner bytes pass',flush=True)
            finally:
                m.close()
        observations.append(rows)
    need(observations[0]==observations[1],'independent complete target/candidate observations')
    return dict(images=2,extents=1,functions=7,code_bytes=464,executed_owner_bytes=464,
        cases_per_image=sum(r['cases'] for r in observations[0]),observations=observations[0],native_geometry_proof=proof,
        ignored_stack_bytes=0,actual_owned_RNG_and_flake=True,actual_vector_context=True,actual_context_bytes=187,
        vector_library_or_tables_owned=False,physical_IRQ_audio_pixels_or_timing_proved=False)


def negative_controls(target):
    free = dict(cap=1,alive='none',frame=0)
    live = dict(cap=1,alive='all')
    adapt = dict(cap=0,vsync=2,adapt=1)
    controls = (
        ('clear-plane',0x2567,1,'clear',{}),('clear-zero-AX',0x256B,8,'clear',{}),
        ('clear-start-DI',0x256D,1,'clear',{}),('clear-16000-WORDs',0x256F,1,'clear',{}),
        ('clear-save-DI',0x2564,1,'clear',{}),
        ('reset-base',0x257B,1,'reset',{}),('reset-alive-zero',0x2583,1,'reset',{}),
        ('reset-stride',0x2587,1,'reset',{}),('reset-eighty',0x2589,1,'reset',{}),('reset-near-return',0x258F,8,'reset',{}),
        ('spawn-local-frame',0x2591,1,'spawn',free),('spawn-base',0x2597,1,'spawn',free),
        ('spawn-alive-test',0x25A2,1,'spawn',free),('spawn-signed-frame',0x25AE,1,'spawn',free),
        ('spawn-eight-frame-threshold',0x25A9,1,'spawn',dict(cap=2,alive='none',frame=7)),
        ('spawn-alive-one',0x25B2,1,'spawn',free),('spawn-edge-selection',0x25B7,1,'spawn',free),
        ('spawn-mod10112',0x25BF,1,'spawn',dict(cap=2,alive='none',frame=8,particle0=(1,0,0,0,0,0),random_seed=seed_for_first_output(32767))),
        ('spawn-mod6272',0x25D9,1,'spawn',dict(free,random_seed=seed_for_first_output(32767))),
        ('spawn-angle-mod32',0x25E7,1,'spawn',free),('spawn-angle-base80',0x25EE,1,'spawn',free),
        ('spawn-length-mod64',0x25F8,1,'spawn',free),('spawn-length-base48',0x25FF,1,'spawn',free),
        ('spawn-cel-mask',0x2609,1,'spawn',dict(free,random_seed=2)),('spawn-vector-x-pointer',0x2611,2,'spawn',free),
        ('spawn-vector-y-pointer',0x2616,2,'spawn',free),('spawn-angle-WORD-frame',0x261A,1,'spawn',free),
        ('spawn-length-zero-extension',0x261F,1,'spawn',free),('spawn-iterator-stride',0x2629,1,'spawn',dict(cap=2,alive='none',frame=8)),
        ('spawn-live-capacity',0x262B,1,'spawn',free),('spawn-capacity-zero-extension',0x262E,1,'spawn',dict(cap=0)),
        ('update-base',0x263E,1,'update',live),('update-alive-test',0x2647,1,'update',live),
        ('update-alive-one',0x264B,1,'update',live),('update-vx-field',0x264E,2,'update',live),
        ('update-vy-field',0x2654,2,'update',live),('update-x-add',0x264F,0x28,'update',live),
        ('update-y-add',0x2655,0x28,'update',live),
        ('update-signed-x-stop',0x265C,1,'update',dict(cap=1,particle0=(2,1,0,0xFFFF,0,0))),
        ('update-x-wrap',0x2661,1,'update',dict(cap=1,particle0=(2,0,0,0,0,0))),
        ('update-signed-y-stop',0x2668,1,'update',dict(cap=1,particle0=(2,1,6272,0,0,0))),
        ('update-y-wrap',0x266D,1,'update',dict(cap=1,particle0=(2,1,6272,0,0,0))),
        ('update-iterator-stride',0x2672,1,'update',dict(cap=2,alive='all')),
        ('render-left-subpixel-shift',0x2695,1,'render',dict(cap=1,particle0=(2,16,32,0,0,0))),
        ('render-top-subpixel-shift',0x269C,1,'render',live),('render-cel-field',0x26A0,2,'render',live),
        ('render-real-flake-call',0x26A2,1,'render',live),('render-live-capacity',0x26A9,1,'render',live),
        ('render-iterator-stride',0x26A7,1,'render',dict(cap=2,alive='all')),
        ('gate-music-flag',0x26BA,1,'gate',dict(active=255)),('gate-signed-frame',0x26C5,1,'gate',dict(frame=100,frames=100)),
        ('gate-PMD-AH',0x26CA,1,'gate',dict(active=255)),('gate-PMD-interrupt',0x26CC,1,'gate',dict(active=255)),
        ('gate-unsigned-measure',0x26D0,1,'gate',dict(active=255,pmd_measure=3,measure=4)),
        ('gate-minimum192-frames',0x26D6,1,'gate',dict(active=255,frame=193)),
        ('gate-true-result',0x26DB,1,'gate',{}),('gate-Pascal-pop',0x26E3,2,'gate',{}),
        ('tick-real-spawn-call',0x26E9,1,'tick',dict(cap=0)),('tick-adapt-branch',0x26F6,1,'tick',adapt),
        ('tick-unsigned-vsync-threshold',0x26FC,1,'tick',dict(cap=0,vsync=1)),('tick-clear-alpha-request',0x2703,1,'tick',adapt),
        ('tick-capacity50',0x2708,1,'tick',adapt),('tick-clear-adaptation',0x270D,1,'tick',adapt),
        ('tick-closed-poll-backedge',0x2713,1,'tick',dict(cap=0,vsync=0,ticks=None,prefix=3)),
        ('tick-counter-reset',0x2719,1,'tick',dict(cap=0)),('tick-showpage-port',0x271D,2,'tick',dict(cap=0)),
        ('tick-BYTE-page-toggle',0x2724,2,'tick',dict(cap=0,page=255)),('tick-accesspage-port',0x272D,2,'tick',dict(cap=0)),
        ('tick-near-return',0x2730,8,'tick',dict(cap=0)))
    context = (('actual-rand-multiplier',0x1A3F,1,'spawn',free),
        ('actual-vector-signed-EDX',0xC7E*16+0x126,8,'spawn',free),
        ('actual-owned-flake-rotation',CS*16+0x24D3,8,'render',dict(cap=1,particle0=(2,16,32,0,0,0))))
    rejected = []
    by_kind = {k:0 for k in ENTRIES}
    for name,at,xor,kind,parameters in (*[(n,CS*16+a,x,k,p) for n,a,x,k,p in controls],*context):
        raw = bytearray(target.program_image)
        raw[at] ^= xor
        m = None
        try:
            m = Machine(replace(target,program_image=bytes(raw)),0x1000)
            m.run(kind,**parameters)
        except (ValueError,UcError):
            rejected.append(name)
            if not name.startswith('actual-'):
                by_kind[kind] += 1
        else:
            raise ValueError('MAINL snow actual instruction mutation escaped: '+name)
        finally:
            if m:
                m.close()
    return dict(count=len(rejected),rejected=rejected,owner_instruction_mutations=len(controls),
                by_function=by_kind,actual_context_instruction_mutations=len(context),actual_guest_instruction_mutations=True,
                unowned_DATA_mutations_counted=False)
