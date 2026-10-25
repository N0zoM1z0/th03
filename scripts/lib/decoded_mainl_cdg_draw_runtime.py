"""Raw SMC/VRAM operand contracts, not a physical PC-98 GRCG pixel model.

Actual owned GRCG setup executes. Ports are logged; memory reads/writes use a
flat 1MiB bus fixture. No GRCG latches, planar RMW or timing are inferred.
"""
import hashlib
import itertools
import json
import struct
from dataclasses import replace
from functools import lru_cache
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INSN
from unicorn.x86_const import *
from lib.decoded_mainl_cdg_draw_layout import CS, DS, SLOTS, LUT, COLOR, ENTRIES, PATCHES
from lib.decoded_mainl_pi_runtime import Spec as Frames, Machine as Physical, arithmetic, signed, ARITH
from lib.decoded_mainl_pi_free_runtime import address
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG, logical, specification as color_spec

ALPHA = bytes((i*13+23)&255 for i in range(65536))
COLORS = bytes((i*29+71)&255 for i in range(65536))
VRAM = bytes((i*7+0x55)&255 for i in range(0x60000))


def need(value,message):
    if not value:
        raise ValueError('MAINL CDG draw contract: '+str(message))


def reverse_bits(value):
    return sum(((value>>i)&1)<<(7-i) for i in range(8))


def next_plane(segment):
    segment = (segment+0x800)&65535
    if segment<0xC000:
        return segment,True
    if segment>=0xC800:
        return segment,False
    return (segment+0x2000)&65535,True


class Spec(Frames):
    def read(self,segment,offset,size):
        at = address(segment,offset)
        return int.from_bytes(self.memory[at:at+size],'little')

    def flags_op(self,left,right,subtract=False):
        return self.flag_operation(left,right,subtract)

    def patch(self,kind,values):
        start = ENTRIES[kind][0]
        for relative,value in zip(PATCHES[kind],values):
            self.store((self.o['load']+CS)*16+start+relative,2,value)

    def color(self,continuation):
        self.push(0xC00000,4)
        self.frame(continuation)
        frame = bytes(self.memory[address(self.ss,self.r['sp']):address(self.ss,self.r['sp'])+8])
        self.events.append(('color-entry',self.full(),frame.hex(),self.flags&(ARITH|0x600)))
        out,_,_,events,_ = color_spec('setcolor',self.r,self.flags,random_seed=0,mode=0xC0,color=0,
            strings=(b'\0',b'\0'),pointers=((0x5000,0),(0x6000,0)),dos_status=0,reply_seed=0)
        self.events.extend(events)
        for event in events:
            if event[0]=='store':
                _,at,size,value = event
                self.memory[at:at+size] = value.to_bytes(size,'little')
        self.r = out
        self.r['cs'] = self.o['load']+CS

    def run(self,kind):
        o,r = self.o,self.r
        self.enter()
        self.push(r['si'])
        self.push(r['di'])
        if kind!='noalpha':
            self.color(ENTRIES[kind][0]+16)
            r = self.r
        slot = (SLOTS+o['slot']*16)&65535
        r['si'] = slot
        origin = ((signed(o['left'])>>3)+self.word(self.ds,(slot+6)&65535))&65535
        width = self.word(self.ds,(slot+8)&65535)
        w = (width*4)&65535
        colors = self.word(self.ds,(slot+14)&65535)
        last = (origin+w-1)&65535
        stride = ((80-w) if kind=='hflip' else (80+w))&65535
        values = (colors,origin,width,width,stride) if kind=='alpha' else (last,last,w,w,stride,stride) if kind=='hflip' else (width,)
        self.patch(kind,values)
        segment = (0xA800+o['top']*5)&65535
        r['es'] = segment
        r['dx'] = stride
        if kind!='hflip':
            self.push(self.ds)
            self.flags &= ~0x400
        r['bx'] = LUT if kind=='hflip' else o['top'] if kind=='alpha' else origin
        source = self.word(self.ds,(slot+(14 if kind=='noalpha' else 12))&65535)
        if kind=='hflip':
            r['fs'] = source
        else:
            r['ds'] = source
        si = 0
        r['ax'] = segment if kind=='hflip' else source
        graph_stores,rows,maximum_inner = 0,0,0

        def render(combine):
            nonlocal si,graph_stores,rows,maximum_inner
            di = last if kind=='hflip' else origin
            while True:
                count = (w or 65536) if kind=='hflip' else (width or 65536) if combine else width
                maximum_inner = max(maximum_inner,count)
                for _ in range(count):
                    value = self.read(source,si,1 if kind=='hflip' else 4)
                    if kind=='hflip':
                        value = self.read(self.ds,(LUT+value)&65535,1)
                        r['ax'] = (r['ax']&0xFF00)|value
                    elif combine:
                        self.high['ax'],r['ax'] = value&0xFFFF0000,value&65535
                    size = 1 if kind=='hflip' else 4
                    destination = address(segment,di)
                    need(0xA0000<=destination<destination+size<=1<<20,'bounded flat VRAM operands, disjoint from CODE/DGROUP/stack')
                    need(graph_stores<400000,'bounded complete-entry trace fixture, not an execution prefix')
                    if combine:
                        value |= self.read(segment,di,size)
                    self.store(destination,size,value)
                    graph_stores += 1
                    si = (si+size)&65535
                    di = (di+(-1 if kind=='hflip' else 4))&65535
                rows += 1
                di = self.flags_op(di,stride,True)
                if signed(di)<0:
                    return

        if kind!='noalpha':
            render(False)
            r['ax'] &= 0xFF00
            self.flags = (self.flags&0x600)|2|logical(0,8)
            self.events.append(('out',0x7C,1,0,self.flags&0x200))
            source = self.word(self.ds,(slot+14)&65535) if kind=='hflip' else colors
            si = 0
            if kind=='hflip':
                r['fs'] = source
            else:
                r['ds'] = source
                r['ax'] = source
                r['bx'] = origin
        planes = 0
        while True:
            render(kind!='noalpha')
            planes += 1
            new = (segment+0x800)&65535
            r['ax'] = new
            self.flags_op(new,0xC000,True)
            if new<0xC000:
                segment = new
                continue
            self.flags_op(new,0xC800,True)
            if new>=0xC800:
                segment = new
                break
            segment = self.flags_op(new,0x2000)
            r['ax'] = segment
        r.update(es=segment,cx=0)
        if kind!='hflip':
            self.pop('ds')
        self.pop('di')
        self.pop('si')
        self.pop('bp')
        self.returned(6)
        return self.full(),self.flags,self.events,dict(graph_stores=graph_stores,rows=rows,color_planes=planes,
            maximum_inner_iterations=maximum_inner,SMC_WORD_writes=len(values))


class Machine(Physical):
    def __init__(self,image,load):
        need(image.valid,'valid decoded image')
        self.load,self.base,self.cs,self.ds = load,load*16,load+CS,load+DS
        self.u = Uc(UC_ARCH_X86,UC_MODE_16)
        self.u.mem_map(0,1<<20)
        memory = bytearray(b'\xA5'*(1<<20))
        raw = image.relocated_program_image(load)
        memory[self.base:self.base+len(raw)] = raw
        memory[0xA0000:0x100000] = VRAM
        self.initial = bytes(memory)
        self.instructions,self.samples,self.owner = {},set(),set()
        for start,size in [(CS*16+a,n) for a,n in ENTRIES.values()]+[(COLOR,41)]:
            ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[start:start+size],start))
            need(sum(i.size for i in ins)==size,'complete blitter and actual color-helper boundaries')
            self.instructions.update({i.address:i.size for i in ins})
            self.samples.add(start)
            for i in ins:
                if i.mnemonic in ('push','pushf','pop','popf'):
                    self.samples.add(i.address+i.size)
            if start!=COLOR:
                self.owner.update(range(start,start+size))
        self.covered = set()
        self.hooks = [self.u.hook_add(UC_HOOK_CODE,self.code),self.u.hook_add(UC_HOOK_MEM_WRITE,self.write),
                      self.u.hook_add(UC_HOOK_INSN,self.out,None,1,0,UC_X86_INS_OUT)]

    def regs(self,full=False):
        values = super().regs(full)
        values.update(fs=self.u.reg_read(UC_X86_REG_FS),gs=self.u.reg_read(UC_X86_REG_GS))
        return values

    def code(self,u,at,size,_):
        try:
            offset = at-self.base
            if at==self.cs*16+0xFFFF:
                self.returned = True
                u.emu_stop()
                return
            if offset==COLOR:
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                ip,cs = struct.unpack('<2H',bytes(u.mem_read(address(ss,sp),4)))
                self.event(('far-frame',address(ss,sp),ip,cs))
                frame = bytes(u.mem_read(address(ss,sp),8))
                self.event(('color-entry',self.regs(True),frame.hex(),u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)))
                self.color_calls += 1
            need(self.instructions.get(offset)==size,'only complete blitter or actual color instructions')
            if offset not in self.seen_instructions:
                self.seen_instructions.add(offset)
                self.covered.update(range(offset,offset+size))
            if offset in self.samples:
                self.max_depth = max(self.max_depth,self.o['stack']-u.reg_read(REG['sp']))
        except Exception as error:
            self.fail(error)

    def out(self,u,port,size,value,_):
        try:
            self.event(('out',port,size,value,u.reg_read(UC_X86_REG_EFLAGS)&0x200))
            self.port_count += 1
        except Exception as error:
            self.fail(error)

    def run(self,kind,*,width=1,bottom=0,left=0,top=0,slot=0,alpha=0x5000,colors=0x6000,
            lookup='reverse',source_byte=None,flags=0x202,ss=0x7000,stack=0xF800,seed=0x1357,persistent=False):
        need(kind in ENTRIES and all(0<=v<=65535 for v in (width,bottom,left,top,slot,alpha,colors)), 'WORD metadata and coordinate fixtures')
        need(ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),'bounded incoming flags / foreign SS')
        need(alpha in (0,0x5000,0x6000,self.ds) and colors in (0,0x5000,0x6000,self.ds),'disjoint source fixture segments')
        need(lookup in ('reverse','identity','xor') and (source_byte is None or 0<=source_byte<=255),'bounded BYTE source and external LUT')
        memory = bytearray(self.u.mem_read(0,1<<20) if persistent else self.initial)
        for segment,raw in ((alpha,ALPHA),(colors,COLORS)):
            if source_byte is not None:
                raw = bytes([source_byte])*65536
            memory[segment*16:segment*16+65536] = raw
        table = bytes(reverse_bits(i) if lookup=='reverse' else i if lookup=='identity' else i^0x5A for i in range(256))
        memory[self.ds*16+LUT:self.ds*16+LUT+256] = table
        first = (SLOTS+slot*16)&65535
        for off,value in ((0,0),(2,1),(4,0x7FFF),(6,bottom),(8,width),(10,0),(12,alpha),(14,colors)):
            at = address(self.ds,first,off)
            memory[at:at+2] = struct.pack('<H',value)
        frame = struct.pack('<5H',0xFFFF,self.cs,slot,top,left)
        memory[address(ss,stack):address(ss,stack)+len(frame)] = frame
        self.u.mem_write(0,bytes(memory))
        regs = {n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)}
        regs.update(sp=stack,cs=self.cs,ds=self.ds,es=0x6666,ss=ss,fs=0x4444,gs=0x4567)
        high = {n:((seed^0x5AA5)<<16) for n in GPRS}
        for n in GPRS:
            self.u.reg_write(GPRS[n],high[n]|regs[n])
        for n in ('cs','ds','es','ss'):
            self.u.reg_write(REG[n],regs[n])
        self.u.reg_write(UC_X86_REG_FS,regs['fs'])
        self.u.reg_write(UC_X86_REG_GS,regs['gs'])
        self.u.reg_write(UC_X86_REG_EFLAGS,flags)
        self.o = dict(load=self.load,slot=slot,left=left,top=top,stack=stack)
        spec = Spec(memory,regs,high,flags,self.o)
        expected,final,self.events,summary = spec.run(kind)
        self.index,self.error,self.returned,self.max_depth,self.color_calls,self.port_count = 0,None,False,0,0,0
        self.far_word_hooks = 0
        self.seen_instructions = set()
        try:
            self.u.emu_start(self.cs*16+ENTRIES[kind][0],1<<20,count=12000000)
        except UcError as error:
            raise ValueError('MAINL CDG draw contract: guest fault') from error
        need(self.error is None,self.error or 'guest error')
        need(self.returned and self.index==len(self.events),'complete native return and ordered requests; no budget-prefix inference')
        need(self.regs(True)==expected,'complete DWORD/segment effects '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)==final&(ARITH|0x600),'defined return flags, IF and DF')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'whole physical memory including SMC, private stack and caller bytes')
        need(self.color_calls==(0 if kind=='noalpha' else 1) and self.port_count==(0 if kind=='noalpha' else 6),'real nested setup and all native BYTE OUTs')
        return dict(kind=kind,registers=expected,flags=final&(ARITH|0x600),summary=summary,
            events=len(self.events),trace_sha256=hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest(),
            stack_depth=self.max_depth,actual_color_calls=self.color_calls,ports=self.port_count)


@lru_cache(maxsize=1)
def word_bounds():
    """Image-independent arithmetic; native opcode checks below always rerun."""
    for width in range(65536):
        amount = (width*4)&65535
        need((width*4-(80+amount))&65535==0xFFB0,'REP row cancels its byte width')
        need(((width or 65536)*4-(80+amount))&65535==0xFFB0,'DWORD LOOP zero counter is finite')
        need((-(amount or 65536)-(80-amount))&65535==0xFFB0,'BYTE LOOP zero counter is finite')
    maximum_rows = max(1 if (start-80)&0x8000 else 2+((start-80)&65535)//80 for start in range(65536))
    maximum_planes = 0
    for initial in range(65536):
        segment,count = initial,0
        while True:
            segment,again = next_plane(segment)
            count += 1
            need(count<=26,'plane successor always reaches the unsigned exit')
            if not again:
                break
        maximum_planes = max(maximum_planes,count)
    need((maximum_rows,maximum_planes)==(411,26),'complete WORD row and plane bounds')
    return maximum_rows,maximum_planes


def geometry_proof(image):
    """Native WORD recurrence, not a timeout or an instruction-skipping model."""
    for at,raw in ((0x259,b'\xf3\x66\xa5'),(0xF7B,b'\xf3\x66\xa5'),
        (0x280,b'\xe2\xf1'),(0x31E,b'\xe2\xf5'),(0x34A,b'\xe2\xf5'),
        (0x22F,b'\xc1\xe0\x02'),(0x232,b'\x05\x50\0'),
        (0x2CE,b'\xc1\xe3\x02'),(0x2E8,b'\xb8\x50\0'),(0x2EB,b'\x2b\xc3'),
        (0xF55,b'\xc1\xe0\x02'),(0xF58,b'\x05\x50\0')):
        need(image.program_image[CS*16+at:CS*16+at+len(raw)]==raw,'native REP/LOOP widths and stride definitions')
    for at,branch in ((0x25C,b'\x79\xf6'),(0x282,b'\x79\xea'),(0x320,b'\x79\xee'),
                      (0x34C,b'\x79\xee'),(0xF7E,b'\x79\xf6')):
        need(image.program_image[CS*16+at:CS*16+at+4]==b'\x2b\xfa'+branch,'native SUB DI,DX / signed row backedge')
    maximum_rows,maximum_planes = word_bounds()
    return dict(WORD_width_states=65536,WORD_origin_states=65536,WORD_segment_states=65536,
        row_delta_mod_WORD=0xFFB0,maximum_rows_per_plane=411,maximum_color_planes=26,
        LOOP_zero_counter_iterations=65536,REP_zero_counter_iterations=0,
        budget_expiry_used=False,nonterminal_claim=False,
        assumptions=['flat bus operands remain in mapped fixture memory',
                     'VRAM writes are disjoint from CODE, DGROUP and private stack',
                     'actual SMC immediate widths/strides remain unchanged during rows'])


def cases(load):
    ds = load+DS
    geometries = ((1,0,0,0,0),(2,80,7,5,31),(3,160,0xFFFF,0xFFFF,32),
        (2,240,641,399,0xFFFF),(1,0,0xFFFF,0,0),(4,0,0x7FFF,1023,0),
        (3,80,0x8000,1638,0),(8,320,0,0,32),(1,0x804F,0,0,1),(1,0x804C,0,0,1))
    for kind,g,flags,ss in itertools.product(ENTRIES,geometries,(2,0x202,0x402,0xED7),(0x7000,0x8000)):
        width,bottom,left,top,slot = g
        yield kind,dict(width=width,bottom=bottom,left=left,top=top,slot=slot,flags=flags,ss=ss)
    for kind,shift,value in itertools.product(ENTRIES,(0,8),range(256)):
        yield kind,dict(left=value<<shift)
    for kind,shift,value in itertools.product(ENTRIES,(0,8),range(256)):
        yield kind,dict(slot=value<<shift)
    for value,lookup in itertools.product(range(256),('reverse','identity','xor')):
        yield 'hflip',dict(source_byte=value,lookup=lookup)
    for kind,(alpha,colors) in itertools.product(ENTRIES,((0,0),(0x5000,0x5000),(ds,0x6000),(0x5000,ds))):
        yield kind,dict(alpha=alpha,colors=colors,flags=0xED7)
    for kind,value in itertools.product(ENTRIES,(0,1,2,4,8,0x80,0xA5,0xFF)):
        yield kind,dict(source_byte=value)
    for width,flags in itertools.product((0x4001,0x8001,0xC001),(2,0x202,0x402,0xED7)):
        yield 'hflip',dict(width=width,flags=flags)
    for kind,top in itertools.product(ENTRIES,(0xCCCC,0xCCCD,0x4000)):
        yield kind,dict(top=top)
    # Execute every real iteration and the eventual RETF, including both LOOP
    # zero-counter cases that historical instruction-budget prefixes did not finish.
    for kind in ENTRIES:
        yield kind,dict(width=0,flags=0xED7)


def verify(target,candidate):
    proof = geometry_proof(target)
    need(proof==geometry_proof(candidate),'both complete native loop geometry proofs')
    observations = []
    for image_index,image in enumerate((target,candidate),1):
        rows = []
        for load in (0x1000,0x3000):
            m = Machine(image,load)
            trace = hashlib.sha256()
            counts = {k:0 for k in ENTRIES}
            maximum = 0
            zero = {}
            stores = 0
            try:
                for count,(kind,parameters) in enumerate(cases(load),1):
                    p = dict(seed=0x1357 if count&1 else 0xECA8,stack=0x80 if count&1 else 0xF800)
                    p.update(parameters)
                    result = m.run(kind,**p)
                    counts[kind] += 1
                    maximum = max(maximum,result['stack_depth'])
                    stores += result['summary']['graph_stores']
                    trace.update(json.dumps(result,sort_keys=True).encode())
                    if parameters.get('width')==0:
                        zero[kind] = result['summary']
                    if count%512==0:
                        print(f'CDG draw: image {image_index}, load {load:04X}, {count} complete entries',flush=True)
                for kind in ENTRIES:
                    for index in range(3):
                        result = m.run(kind,width=index+1,bottom=index*80,flags=0xED7,persistent=index>0)
                        count += 1
                        counts[kind] += 1
                        stores += result['summary']['graph_stores']
                        trace.update(json.dumps(result,sort_keys=True).encode())
                need(m.owner<=m.covered,'every one of the 493 owner bytes executes')
                need(set(range(COLOR,COLOR+41))<=m.covered,'all 41 actual owned GRCG setup bytes execute')
                rows.append(dict(load_segment=load,cases=count,cases_by_function=counts,executed_owner_bytes=493,
                    actual_color_helper_bytes=41,maximum_stack_depth=maximum,flat_graph_stores=stores,
                    zero_width_terminal_summaries=zero,trace_sha256=trace.hexdigest()))
                print(f'CDG draw: image {image_index}, load {load:04X}, {count} entries / 493 owner bytes pass',flush=True)
            finally:
                m.close()
        observations.append(rows)
    need(observations[0]==observations[1],'complete independent target/candidate draw observations')
    return dict(images=2,functions=3,code_bytes=493,executed_owner_bytes=493,
        cases_per_image=sum(o['cases'] for o in observations[0]),observations=observations[0],native_geometry_proof=proof,
        ignored_stack_bytes=0,actual_owned_color_helper=True,flat_memory_operand_contract=True,
        physical_GRCG_or_pixels_emulated=False,external_LUT_owned=False)


def negative_controls(target):
    controls = (
        ('alpha-color-mode',0x1FD,1,'alpha',{}),('alpha-slot-frame',0x206,2,'alpha',dict(slot=1)),
        ('alpha-slot-stride',0x209,1,'alpha',dict(slot=1)),('alpha-color-segment-field',0x210,2,'alpha',{}),
        ('alpha-SMC-color-address',0x213,2,'alpha',{}),('alpha-signed-left',0x21A,8,'alpha',dict(left=0x8000)),
        ('alpha-bottom-field',0x21D,2,'alpha',{}),('alpha-SMC-origin-address',0x222,2,'alpha',{}),
        ('alpha-width-field',0x226,2,'alpha',{}),('alpha-SMC-mask-width',0x229,2,'alpha',{}),
        ('alpha-SMC-color-width',0x22D,2,'alpha',{}),('alpha-DWORD-stride',0x231,1,'alpha',{}),
        ('alpha-row-distance',0x233,1,'alpha',{}),('alpha-top-times-five',0x244,2,'alpha',dict(top=1)),
        ('alpha-plane-base',0x247,1,'alpha',{}),('alpha-alpha-segment-field',0x24D,2,'alpha',{}),
        ('alpha-CLD',0x255,1,'alpha',dict(flags=0xED7)),('alpha-DWORD-mask-copy',0x25B,1,'alpha',{}),
        ('alpha-signed-row-stop',0x25F,1,'alpha',dict(bottom=80)),('alpha-port-disable',0x263,1,'alpha',{}),
        ('alpha-color-OR',0x278,0x20,'alpha',{}),('alpha-source-DWORD-step',0x27C,1,'alpha',{}),
        ('alpha-destination-DWORD-step',0x27F,1,'alpha',dict(width=2)),('alpha-loop-target',0x281,1,'alpha',dict(width=2)),
        ('alpha-plane-step',0x28C,1,'alpha',{}),('alpha-G-E-gap',0x29B,1,'alpha',{}),
        ('alpha-Pascal-pop',0x2A5,2,'alpha',{}),
        ('hflip-last-byte',0x2D3,8,'hflip',{}),('hflip-SMC-last-alpha',0x2D8,2,'hflip',{}),
        ('hflip-SMC-last-color',0x2DC,2,'hflip',{}),('hflip-width-byte-scale',0x2D0,1,'hflip',{}),
        ('hflip-stride-subtract',0x2EC,8,'hflip',{}),('hflip-LUT-base',0x307,1,'hflip',{}),
        ('hflip-alpha-FS',0x30B,2,'hflip',{}),('hflip-alpha-XLAT',0x318,1,'hflip',{}),
        ('hflip-alpha-backwards',0x31D,8,'hflip',{}),('hflip-disable-GRCG',0x327,1,'hflip',{}),
        ('hflip-slot-reload',0x32D,2,'hflip',dict(slot=1)),('hflip-color-FS',0x337,2,'hflip',{}),
        ('hflip-color-OR',0x347,0x20,'hflip',{}),('hflip-color-backwards',0x349,8,'hflip',{}),
        ('hflip-plane-step',0x357,1,'hflip',{}),('hflip-G-E-gap',0x366,1,'hflip',{}),
        ('hflip-Pascal-pop',0x36F,2,'hflip',{}),
        ('noalpha-slot-frame',0xF39,2,'noalpha',dict(slot=1)),('noalpha-signed-left',0xF46,8,'noalpha',dict(left=0x8000)),
        ('noalpha-bottom-field',0xF49,2,'noalpha',{}),('noalpha-width-field',0xF4E,2,'noalpha',{}),
        ('noalpha-SMC-width',0xF51,2,'noalpha',{}),('noalpha-DWORD-stride',0xF57,1,'noalpha',{}),
        ('noalpha-row-distance',0xF59,1,'noalpha',{}),('noalpha-top-times-five',0xF66,2,'noalpha',dict(top=1)),
        ('noalpha-colors-segment',0xF6F,2,'noalpha',{}),('noalpha-CLD',0xF76,1,'noalpha',dict(flags=0xED7)),
        ('noalpha-copy-size',0xF7D,1,'noalpha',{}),('noalpha-plane-step',0xF88,1,'noalpha',{}),
        ('noalpha-G-E-gap',0xF97,1,'noalpha',{}),('noalpha-Pascal-pop',0xFA1,2,'noalpha',{}),
        ('actual-color-CLI',0xC44,1,'alpha',dict(flags=0x202)))
    rejected = []
    for name,offset,xor,kind,parameters in controls:
        at = offset if offset==0xC44 else CS*16+offset
        raw = bytearray(target.program_image)
        raw[at] ^= xor
        machine = None
        try:
            machine = Machine(replace(target,program_image=bytes(raw)),0x1000)
            machine.run(kind,**parameters)
        except (ValueError,UcError):
            rejected.append(name)
        else:
            raise ValueError('CDG draw actual instruction mutation escaped: '+name)
        finally:
            if machine:
                machine.close()
    return dict(count=len(rejected),rejected=rejected,owner_instruction_mutations=len(rejected)-1,
                actual_color_helper_mutations=1,actual_guest_instruction_mutations=True,alignment_mutations_counted=False)
