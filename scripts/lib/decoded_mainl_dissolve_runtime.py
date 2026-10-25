"""Complete dissolve with actual SMC blitters and color setup on one physical UC.

All x86 memory operands use a flat synthetic bus. External slot/pattern/source
fixtures and port events do not establish assets, planar pixels or IRQ timing.
"""
import hashlib
import itertools
import json
import struct
from dataclasses import replace
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INSN
from unicorn.x86_const import *
from lib.decoded_mainl_dissolve_layout import CS, DS, START, SIZE, DATA
from lib.decoded_mainl_cdg_draw_runtime import Spec as BlitSpec, ALPHA, COLORS, VRAM
from lib.decoded_mainl_cdg_draw_layout import CS as BLIT_CS, ENTRIES as BLITS, COLOR
from lib.decoded_mainl_pi_runtime import Spec as Frames, Machine as Physical, signed, ARITH
from lib.decoded_mainl_pi_free_runtime import address
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG, logical
from lib.decoded_mainl_staff_draw_runtime import half

CONTEXT = {BLIT_CS*16+BLITS[k][0]:(k,BLITS[k][1]) for k in ('alpha','noalpha')}
CONTEXT[COLOR] = ('color',41)
PATTERNS = tuple(((i*0x3187)^0xA55A)&65535 for i in range(32))


def need(value,message):
    if not value:
        raise ValueError('MAINL dissolve contract: '+str(message))


def inner_count(width):
    quotient = (abs(signed(width))//16)*(-1 if signed(width)<0 else 1)
    return (quotient&65535) or 65536


def row_count(top,height):
    end,first = (top+height)&65535,(top+1)&65535
    return 1+max(0,end-first)


class Spec(Frames):
    def dg(self,offset):
        return self.word(self.ds,offset&65535)

    def local(self,offset,value):
        self.store(address(self.ss,self.r['bp']+offset),2,value&65535)

    def op(self,left,right,subtract=False):
        return self.flag_operation(left,right,subtract)

    def run(self):
        r = self.r
        strength,slot,top,left = [self.word(self.ss,r['sp']+2+i*2) for i in range(4)]
        self.enter(6)
        self.push(r['si'])
        self.push(r['di'])
        r['bx'] = (slot*16)&65535
        width = self.dg(DATA['slots']+r['bx']+2)
        r['ax'] = width
        self.local(-4,width)
        height = self.dg(DATA['slots']+r['bx']+4)
        r['ax'] = height
        self.local(-6,height)
        r['dx'] = 65535 if signed(width)<0 else 0
        r['ax'] = half(width)&65535
        left = self.op(left,r['ax'],True)
        self.local(10,left)
        r['dx'] = 65535 if signed(height)<0 else 0
        r['ax'] = half(height)&65535
        top = self.op(top,r['ax'],True)
        self.local(8,top)
        enabled = self.memory[address(self.ds,DATA['enabled'])]
        self.flags = (self.flags&0x600)|2|logical(enabled,8)
        alpha = False
        if enabled:
            requested = self.memory[address(self.ds,DATA['requested'])]
            self.flags = (self.flags&0x600)|2|logical(requested,8)
            alpha = bool(requested)
        kind = 'alpha' if alpha else 'noalpha'
        for v in (left,top,slot):
            self.push(v)
        self.frame(0x2793 if alpha else 0x2783)
        r['cs'] = self.o['load']+BLIT_CS
        at = address(self.ss,r['sp'])
        self.events.append(('blit-entry',kind,self.full(),bytes(self.memory[at:at+10]).hex(),self.flags&ARITH))
        child = BlitSpec(self.memory,r,self.high,self.flags,dict(load=self.o['load'],slot=slot,left=left,top=top))
        _,_,_,child_summary = child.run(kind)
        self.events.extend(child.events)
        self.r,self.high,self.flags = child.r,child.high,child.flags
        r = self.r
        strength &= 7
        self.local(4,strength)
        self.op(strength,0,True)
        rows,words = 0,0
        if strength:
            r['bx'] = 16
            r['dx'] = (signed(width)-int(signed(width)/16)*16)&65535
            width = int(signed(width)/16)&65535
            r['ax'] = width
            self.local(-4,width)
            r['ax'] = top
            end = self.op(height,top)
            self.local(-6,end)
            r['ax'] = (signed(left)>>3)&65535
            r['dx'] = (top<<6)&65535
            r['ax'] = self.op(r['ax'],r['dx'])
            r['dx'] = (top<<4)&65535
            r['ax'] = self.op(r['ax'],r['dx'])
            offset = r['ax']
            self.local(-2,offset)
            r.update(ax=0xE000,es=0xE000,bx=DATA['pattern']+strength*8,dx=top)
            while True:
                r['si'] = (r['dx']&3)*2
                r['ax'] = self.dg(r['bx']+r['si'])^65535
                r['di'],r['cx'] = offset,width
                count = width or 65536
                need(words+count<=150000,'bounded complete-entry fixture; mathematical bounds are separate')
                for _ in range(count):
                    at = address(0xE000,r['di'])
                    value = int.from_bytes(self.memory[at:at+2],'little')&r['ax']
                    self.store(at,2,value)
                    r['di'] = (r['di']+2)&65535
                r['cx'] = 0
                words += count
                rows += 1
                offset = (offset+80)&65535
                self.local(-2,offset)
                r['dx'] = (r['dx']+1)&65535
                self.op(r['dx'],end,True)
                if r['dx']>=end:
                    break
        self.pop('di')
        self.pop('si')
        r['sp'] = r['bp']
        self.pop('bp')
        r['sp'] += 10
        return self.full(),self.flags,dict(blitter=kind,blitter_summary=child_summary,rows=rows,WORD_stores=words)


class Machine(Physical):
    def __init__(self,image,load):
        need(image.valid,'valid decoded MZ')
        self.load,self.base,self.cs,self.ds = load,load*16,load+CS,load+DS
        self.u = Uc(UC_ARCH_X86,UC_MODE_16)
        self.u.mem_map(0,1<<20)
        memory = bytearray(b'\xA5'*(1<<20))
        raw = image.relocated_program_image(load)
        memory[self.base:self.base+len(raw)] = raw
        memory[0xA0000:1<<20] = VRAM
        for segment,data in ((0x5000,ALPHA),(0x6000,COLORS)):
            memory[segment*16:segment*16+len(data)] = data
        self.initial = bytes(memory)
        self.instructions,self.covered = {},set()
        self.owner = set(range(CS*16+START,CS*16+START+SIZE))
        for start,size in [(CS*16+START,SIZE),*[(a,n) for a,(_,n) in CONTEXT.items()]]:
            ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[start:start+size],start))
            need(sum(i.size for i in ins)==size,'complete owner / actual blitter and setup boundaries')
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
            if offset in CONTEXT:
                kind,_ = CONTEXT[offset]
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                ip,cs = struct.unpack('<2H',bytes(u.mem_read(address(ss,sp),4)))
                self.event(('far-frame',address(ss,sp),ip,cs))
                if kind=='color':
                    self.event(('color-entry',self.regs(True),bytes(u.mem_read(address(ss,sp),8)).hex(),u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)))
                else:
                    self.event(('blit-entry',kind,self.regs(True),bytes(u.mem_read(address(ss,sp),10)).hex(),u.reg_read(UC_X86_REG_EFLAGS)&ARITH))
            need(self.instructions.get(offset)==size,'only actual owner / owned blitter / color setup instructions')
            self.covered.update(range(offset,offset+size))
        except Exception as error:
            self.fail(error)

    def run(self,*,left=320,top=200,slot=0,strength=3,width=32,height=1,blit_width=1,bottom=None,
            enabled=0,requested=1,patterns=PATTERNS,flags=0x202,ss=0x7000,stack=0xF800,seed=0x1357,persistent=False):
        need(all(0<=v<=65535 for v in (left,top,slot,strength,width,height,blit_width)),'WORD arguments and metadata')
        need(0<=enabled<=255 and 0<=requested<=255 and len(patterns)==32 and all(0<=v<=65535 for v in patterns),'BYTE flags / external pattern WORDs')
        need(ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),'foreign SS and inherited flags')
        memory = bytearray(self.u.mem_read(0,1<<20) if persistent else self.initial)
        for i,value in enumerate(patterns):
            at = address(self.ds,DATA['pattern']+i*2)
            memory[at:at+2] = struct.pack('<H',value)
        adjusted_left = (left-half(width))&65535
        if bottom is None:
            bottom = (-(signed(adjusted_left)>>3))&65535
        first = (DATA['slots']+slot*16)&65535
        for delta,value in ((0,0),(2,width),(4,height),(6,bottom),(8,blit_width),(10,0),(12,0x5000),(14,0x6000)):
            at = address(self.ds,(first+delta)&65535)
            memory[at:at+2] = struct.pack('<H',value)
        for name,value in (('enabled',enabled),('requested',requested)):
            memory[address(self.ds,DATA[name])] = value
        at = address(ss,stack)
        memory[at:at+10] = struct.pack('<5H',0xFFFF,strength,slot,top,left)
        self.u.mem_write(0,bytes(memory))
        regs = {n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)}
        regs.update(sp=stack,cs=self.cs,ds=self.ds,es=0x6666,ss=ss,fs=0x3456,gs=0x4567)
        high = {n:((seed^0x5AA5)<<16) for n in GPRS}
        for n in GPRS:
            self.u.reg_write(GPRS[n],high[n]|regs[n])
        for n in ('cs','ds','es','ss'):
            self.u.reg_write(REG[n],regs[n])
        self.u.reg_write(UC_X86_REG_FS,regs['fs'])
        self.u.reg_write(UC_X86_REG_GS,regs['gs'])
        self.u.reg_write(UC_X86_REG_EFLAGS,flags)
        self.o = dict(load=self.load,stack=stack)
        spec = Spec(memory,regs,high,flags,self.o)
        expected,final,summary = spec.run()
        self.events,self.index,self.error,self.returned,self.max_depth,self.far_word_hooks = spec.events,0,None,False,0,0
        try:
            self.u.emu_start(self.cs*16+START,1<<20,count=6000000)
        except UcError as error:
            raise ValueError('MAINL dissolve contract: guest fault') from error
        need(self.error is None,self.error or 'guest failure')
        need(self.returned and self.index==len(self.events),'real near return and every ordered event; no budget-prefix inference')
        need(self.regs(True)==expected,'complete DWORD/segment effects '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)==final&(ARITH|0x600),'defined flags / IF / DF')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'all physical memory, real frames, caller arguments and SMC bytes')
        return dict(registers=expected,flags=final&(ARITH|0x600),summary=summary,stack_depth=self.max_depth,
            events=len(self.events),trace_sha256=hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest())


def geometry_proof(image):
    for at,raw in ((0x2793,b'\x83\x66\x04\x07\x83\x7E\x04\0\x74\x61'),
        (0x279D,b'\xBB\x10\0\x8B\x46\xFC\x99\xF7\xFB\x89\x46\xFC'),
        (0x27A9,b'\x8B\x46\x08\x01\x46\xFA'),
        (0x27DA,b'\x89\xD6\x81\xE6\x03\0\xD1\xE6\x8B\0\xF7\xD0'),
        (0x27E6,b'\x8B\x7E\xFE\x8B\x4E\xFC\x26\x21\x05\x83\xC7\x02\xE2\xF8'),
        (0x27F4,b'\x83\x46\xFE\x50\x42\x3B\x56\xFA\x72\xDC')):
        need(image.program_image[CS*16+at:CS*16+at+len(raw)]==raw,'literal signed-width / masked-pattern / nested finite CFG')
    widths = [inner_count(v) for v in range(65536)]
    need(min(widths)==1 and max(widths)==65536,'complete WORD quotient-to-LOOP domain')
    need(all((v&7)==v%8 for v in range(65536)),'all WORD strengths reduce to eight pattern rows')
    # Once INC has wrapped (possibly on the first row), the unsigned counter
    # increases monotonically to end. The first comparison exits if end==0.
    # There is no second wrap while DX<end<=FFFF, hence at most65536 rows.
    for top,end in itertools.chain(itertools.product(range(65536),(0,1,0x7FFF,0x8000,0xFFFF)),
                                    itertools.product((0,1,0x7FFF,0x8000,0xFFFF),range(65536))):
        first = (top+1)&65535
        count = row_count(top,(end-top)&65535)
        need(1<=count<=65536 and (count==1 if first>=end else (top+count)&65535==end),
             'unsigned postincrement recurrence and exact terminal boundary')
    return dict(width_WORD_states=65536,strength_WORD_states=65536,maximum_inner_iterations=65536,
        maximum_rows=65536,maximum_combined_WORD_stores=1<<32,maximum_combined_case_executed=False,
        row_count_formula='1 + max(0, end - ((top+1) & FFFF)); end=(height+top)&FFFF',
        assumptions=['mapped disjoint CODE/DGROUP/stack and E000 flat operand plane',
                     'owned blitters return; readonly metadata/patterns after their return'],
        budget_expiry_used=False,guest_iterations_skipped=False,physical_planar_pixels_or_timing_proved=False)


def cases():
    for enabled,requested,strength in itertools.product((0,1,2,128,255),(0,1,2,128,255),(0,1,7,8,0xFFFF)):
        yield dict(enabled=enabled,requested=requested,strength=strength)
    for field,shift,value in itertools.product(('left','top','strength'),(0,8),range(256)):
        yield dict(width=16,height=1,blit_width=0,**{field:value<<shift})
    for field,shift,value in itertools.product(('slot','width','height'),(0,8),range(256)):
        yield dict(strength=0,blit_width=0,**{field:value<<shift})
    for name,value in itertools.product(('enabled','requested'),range(256)):
        yield dict(enabled=value if name=='enabled' else 1,requested=value if name=='requested' else 1)
    # Every active pattern WORD receives both BYTE lanes and all256 values,
    # while top selects each of the four native DX&3 rows independently.
    for strength,phase,shift,value in itertools.product(range(1,8),range(4),(0,8),range(256)):
        patterns = list(PATTERNS)
        patterns[strength*4+phase] = value<<shift
        yield dict(width=16,height=1,top=phase,strength=strength,patterns=tuple(patterns),blit_width=0)
    for width in (0,1,15,16,17,31,32,0x7FFF,0x8000,0x8001,0xFFFF):
        for top in (0,1,0xFFFF):
            yield dict(width=width,height=1,top=top,blit_width=0)
    # Actually execute both maxima separately; the 2**32 Cartesian product is
    # a mathematical bound, never claimed as an executed complete fixture.
    yield dict(width=0,height=1,top=0,blit_width=0)
    yield dict(width=16,height=0,top=0xFFFF,blit_width=0)
    for height,top in ((0,0),(0,0xFFFE),(1,0xFFFF),(2,0xFFFE),(3,0xFFFF),(16,8),
                       (0xFFFF,0xFFFF),(0x8000,0x7FFF)):
        yield dict(width=16,height=height,top=(top+half(height))&65535,blit_width=0)
    for slot in (0,0xFFF,0x1000,0xFFFF):
        for flags,ss,stack in itertools.product((2,0x202,0x402,0xED7),(0x7000,0x8000),(0x80,0xF800)):
            yield dict(slot=slot,flags=flags,ss=ss,stack=stack,enabled=1)
    # Actual child SMC and color words survive reentry, but no new ownership.
    for enabled in (0,1):
        yield dict(width=32,height=3,top=1,blit_width=0,enabled=enabled)


def verify(target,candidate):
    proof = geometry_proof(target)
    need(proof==geometry_proof(candidate),'both native finite-loop proofs')
    observations = []
    context = {b for a,(_,n) in CONTEXT.items() for b in range(a,a+n)}
    for image_index,image in enumerate((target,candidate),1):
        rows = []
        for load in (0x1000,0x3000):
            m = Machine(image,load)
            trace,counts = hashlib.sha256(),dict(alpha=0,noalpha=0)
            peak,max_rows,max_inner,max_stores = 0,0,0,0
            try:
                def entry(parameters):
                    nonlocal peak,max_rows,max_inner,max_stores
                    result = m.run(**parameters)
                    summary = result['summary']
                    counts[summary['blitter']] += 1
                    peak = max(peak,result['stack_depth'])
                    max_rows = max(max_rows,summary['rows'])
                    max_stores = max(max_stores,summary['WORD_stores'])
                    max_inner = max(max_inner,summary['WORD_stores']//summary['rows'] if summary['rows'] else 0)
                    trace.update(json.dumps(result,sort_keys=True).encode())
                for count,parameters in enumerate(cases(),1):
                    entry(dict(seed=0x1357 if count&1 else 0xECA8,**parameters))
                    if count%2048==0:
                        print(f'Dissolve: image {image_index}, load {load:04X}, {count} complete entries',flush=True)
                for i in range(3):
                    entry(dict(enabled=i&1,patterns=PATTERNS,persistent=i>0))
                    count += 1
                need(m.owner<=m.covered and context<=m.covered,'all211 owner bytes and333 real owned context bytes execute')
                rows.append(dict(load_segment=load,cases=count,calls_by_blitter=counts,executed_owner_bytes=211,
                    actual_context_bytes=333,maximum_stack_depth=peak,maximum_rows=max_rows,maximum_inner_iterations=max_inner,
                    maximum_WORD_stores=max_stores,trace_sha256=trace.hexdigest()))
                print(f'Dissolve: image {image_index}, load {load:04X}, {count} complete entries / all211 bytes pass',flush=True)
            finally:
                m.close()
        observations.append(rows)
    need(observations[0]==observations[1],'independent complete target/candidate observations')
    return dict(images=2,functions=1,code_bytes=211,cases_per_image=sum(o['cases'] for o in observations[0]),
        observations=observations[0],executed_owner_bytes=211,actual_owned_context_bytes=333,ignored_stack_bytes=0,
        native_geometry_proof=proof,external_patterns_or_slots_owned=False,physical_planar_pixels_or_timing_proved=False)


def negative_controls(target):
    controls = (
        ('local-frame',0x2732,2,{}),('saved-SI',0x2735,1,{}),
        ('pixel-width-field',0x2740,2,{}),('pixel-height-field',0x274D,2,{}),
        ('width-local',0x2743,2,{}),('signed-width-half',0x2755,0x28,dict(width=0xFFFF,strength=0,blit_width=0)),
        ('signed-height-half',0x2760,0x28,dict(height=0xFFFF,strength=0,blit_width=0)),
        ('caller-left-WORD',0x275B,2,{}),('caller-top-WORD',0x2766,2,{}),
        ('enabled-BYTE',0x276B,1,{}),('requested-BYTE',0x2772,1,dict(enabled=1,requested=0)),
        ('actual-noalpha-call',0x277F,1,{}),('actual-alpha-call',0x278F,1,dict(enabled=1)),
        ('strength-mask',0x2796,1,dict(strength=1)),('zero-strength-branch',0x279C,1,dict(strength=0)),
        ('signed-width-divisor',0x279E,1,{}),('width-CWD',0x27A3,8,{}),('quotient-local',0x27A8,2,{}),
        ('wrapped-end-local',0x27AE,2,{}),('left-SAR3',0x27B4,1,{}),
        ('top-SHL6',0x27BA,1,dict(top=1)),('top-SHL4',0x27C2,1,dict(top=1)),
        ('fixed-E000-plane',0x27CA,1,{}),('strength-times8',0x27D2,1,{}),
        ('pattern-base',0x27D5,2,{}),('pattern-phase-mask',0x27DE,1,dict(top=1)),
        ('pattern-phase-WORD',0x27E1,1,dict(top=1)),('pattern-read',0x27E3,1,{}),
        ('pattern-NOT',0x27E5,8,{}),('VRAM-WORD-AND',0x27ED,8,{}),
        ('inner-WORD-stride',0x27F1,1,{}),('inner-LOOP',0x27F3,1,{}),
        ('row-stride80',0x27F7,1,{}),('row-INC',0x27F8,1,{}),
        ('row-bound-local',0x27FB,2,{}),('unsigned-row-backedge',0x27FD,1,dict(height=3)),
        ('near-Pascal-pop8',0x2802,1,{}))
    context = (
        ('actual-alpha-pop6',BLIT_CS*16+0x2A5,1,dict(enabled=1)),
        ('actual-noalpha-pop6',BLIT_CS*16+0xFA1,1,{}),
        ('actual-color-frame',COLOR+2,1,dict(enabled=1)))
    rejected = []
    for name,at,xor,parameters in (*[(n,CS*16+a,x,p) for n,a,x,p in controls],*context):
        raw = bytearray(target.program_image)
        raw[at] ^= xor
        m = None
        try:
            m = Machine(replace(target,program_image=bytes(raw)),0x1000)
            m.run(**parameters)
        except (ValueError,UcError):
            rejected.append(name)
        else:
            raise ValueError('MAINL dissolve actual instruction mutation escaped: '+name)
        finally:
            if m:
                m.close()
    return dict(count=len(rejected),rejected=rejected,owner_instruction_mutations=len(controls),
        actual_context_instruction_mutations=len(context),actual_guest_instruction_mutations=True,unowned_DATA_mutations_counted=False)
