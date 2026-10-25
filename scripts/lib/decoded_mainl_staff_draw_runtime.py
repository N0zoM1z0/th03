"""Independent flat WORD-memory contracts for complete staff drawing bodies.

Synthetic DGROUP words are external input, not ownership of sprite assets or
the slot array. Flat x86 operand effects do not model planar hardware or timing.
"""
import hashlib
import itertools
import json
import struct
from dataclasses import replace
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import *
from lib.decoded_mainl_staff_draw_layout import CS, DS, SPRITE, SLOTS, ENTRIES
from lib.decoded_mainl_pi_runtime import Spec as Frames, Machine as Physical, arithmetic, signed, ARITH
from lib.decoded_mainl_pi_free_runtime import address
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG, logical

DGROUP = bytes(((i*29)^(i>>8)^0x57)&255 for i in range(65536))
GRAPH = bytes(((i*13)^(i>>7)^0xA5)&255 for i in range(65538))


def need(value,message):
    if not value:
        raise ValueError('MAINL staff draw contract: '+str(message))


def half(value):
    v = signed(value)
    return (v+int(v<0))//2


def rotate(value,count):
    return ((value>>count)|(value<<(16-count)))&65535 if count else value


class Spec(Frames):
    def run(self,kind):
        r,o = self.r,self.o
        self.enter(4 if kind=='unput' else 0)
        self.push(r['si'])
        self.push(r['di'])
        if kind=='flake':
            origin = ((signed(o['left'])>>3)+o['top']*80)&65535
            source = (SPRITE+o['index']*16)&65535
            rotation = o['left']&7
            r.update(es=0xA800,cx=rotation,dx=(o['top']*16)&65535)
            di = origin
            for row in range(8):
                r['ax'] = rotate(self.word(self.ds,source),rotation)
                value = self.word(0xA800,di)|r['ax']
                self.store(address(0xA800,di),2,value)
                di = (di+80)&65535
                source,flags = arithmetic(source,2)
                # Native DEC BX defines every arithmetic flag except CF, which
                # it inherits from the immediately preceding source advance.
                _,dec = arithmetic(8-row,1,True)
                self.flags = (self.flags&0x600)|2|(dec&~1)|(flags&1)
            r['bx'] = 0
            stores = 8
        else:
            shifted = (o['index']*16)&65535
            width = self.word(self.ds,(SLOTS+shifted+2)&65535)
            height = self.word(self.ds,(SLOTS+shifted+4)&65535)
            self.store(address(self.ss,r['bp']-2),2,width)
            self.store(address(self.ss,r['bp']-4),2,height)
            left = (o['left']-half(width))&65535
            top = (o['top']+half(height)-2)&65535
            # The compiled source updates its actual caller-owned argument
            # words. No caller-frame window is ignored or restored artificially.
            self.store(address(self.ss,r['bp']+8),2,left)
            self.store(address(self.ss,r['bp']+6),2,top)
            count = width>>4
            stride = (80-2*count)&65535
            di = ((signed(left)>>3)+top*80)&65535
            direction = -2 if self.flags&0x400 else 2
            for row in range(3):
                for _ in range(count):
                    self.store(address(0xE000,di),2,0)
                    di = (di+direction)&65535
                if row<2:
                    di = self.flag_operation(di,stride)
            r.update(ax=0,bx=shifted,cx=0,dx=count,es=0xE000)
            stores = 3*count
        self.pop('di')
        self.pop('si')
        r['sp'] = r['bp']
        self.pop('bp')
        r['sp'] += 8
        return self.full(),self.flags,stores


class Machine(Physical):
    def __init__(self,image,load):
        need(image.valid,'valid decoded MZ')
        self.load,self.base,self.cs,self.ds = load,load*16,load+CS,load+DS
        self.u = Uc(UC_ARCH_X86,UC_MODE_16)
        self.u.mem_map(0,1<<20)
        memory = bytearray(b'\xA5'*(1<<20))
        raw = image.relocated_program_image(load)
        memory[self.base:self.base+len(raw)] = raw
        memory[self.ds*16:self.ds*16+65536] = DGROUP
        for base in (0xA8000,0xE0000):
            memory[base:base+len(GRAPH)] = GRAPH
        self.initial = bytes(memory)
        self.instructions,self.owner,self.covered = {},set(),set()
        for offset,size in ENTRIES.values():
            start = CS*16+offset
            ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[start:start+size],start))
            need(sum(i.size for i in ins)==size,'complete drawing instruction boundaries')
            self.instructions.update({i.address:i.size for i in ins})
            self.owner.update(range(start,start+size))
        self.hooks = [self.u.hook_add(UC_HOOK_CODE,self.code),self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)]

    def regs(self,full=False):
        values = super().regs(full)
        values.update(fs=self.u.reg_read(UC_X86_REG_FS),gs=self.u.reg_read(UC_X86_REG_GS))
        return values

    def code(self,u,at,size,_):
        try:
            self.max_depth = max(self.max_depth,self.o['stack']-u.reg_read(REG['sp']))
            if at==self.cs*16+0xFFFF:
                self.returned = True
                u.emu_stop()
                return
            offset = at-self.base
            need(self.instructions.get(offset)==size,'only complete selected native drawing instructions')
            self.covered.update(range(offset,offset+size))
        except Exception as error:
            self.fail(error)

    def run(self,kind,*,left=320,top=200,index=0,width=32,height=16,source_word=None,
            flags=0x202,ss=0x7000,stack=0xF800,seed=0x1357,persistent=False):
        need(kind in ENTRIES and all(0<=v<=65535 for v in (left,top,index,width,height)),'WORD coordinates/index/metadata')
        need(source_word is None or 0<=source_word<=65535,'external WORD sprite input')
        need(ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),
             'mapped foreign SS and incoming IF/DF/defined-flag fixtures')
        memory = bytearray(self.u.mem_read(0,1<<20) if persistent else self.initial)
        def word(segment,offset,value):
            at = address(segment,offset)
            memory[at:at+2] = struct.pack('<H',value)
        if kind=='unput':
            for field,value in ((2,width),(4,height)):
                word(self.ds,(SLOTS+index*16+field)&65535,value)
        elif source_word is not None:
            for row in range(8):
                word(self.ds,(SPRITE+index*16+row*2)&65535,source_word)
        frame = struct.pack('<4H',0xFFFF,index,top,left)
        at = address(ss,stack)
        memory[at:at+len(frame)] = frame
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
        self.o = dict(load=self.load,stack=stack,left=left,top=top,index=index)
        spec = Spec(memory,regs,self.high,flags,self.o)
        expected,final,stores = spec.run(kind)
        self.events = spec.events
        self.index,self.error,self.returned,self.max_depth,self.far_word_hooks = 0,None,False,0,0
        try:
            self.u.emu_start(self.cs*16+ENTRIES[kind][0],1<<20,count=50000)
        except UcError as error:
            raise ValueError('MAINL staff draw contract: guest fault') from error
        need(self.error is None,self.error or 'guest failure')
        need(self.returned and self.index==len(self.events),'complete near return / ordered stores, without prefix credit')
        need(self.regs(True)==expected,'complete DWORD/segment registers '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)==final&(ARITH|0x600),'defined flags / IF / inherited DF')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'all flat memory, locals and actual caller argument writes')
        return dict(kind=kind,registers=expected,flags=final&(ARITH|0x600),graph_WORD_stores=stores,stack_depth=self.max_depth,
                    events=len(self.events),trace_sha256=hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest())


def geometry_proof(image):
    for at,raw in ((0x24BA,b'\xC1\xE6\x04'),(0x24C9,b'\x81\xE1\x07\0'),(0x24CD,b'\xBB\x08\0'),
        (0x24D2,b'\xD3\xC8'),(0x24D7,b'\x83\xC7\x50'),(0x24DA,b'\x83\xC6\x02'),(0x24DD,b'\x4B\x75\xF0'),
        (0x2509,b'\x99\x2B\xC2\xD1\xF8'),(0x2514,b'\x99\x2B\xC2\xD1\xF8'),(0x253F,b'\xC1\xEA\x04'),
        (0x2542,b'\xBE\x50\0\x29\xD6\x29\xD6'),(0x254D,b'\xF3\xAB'),(0x2553,b'\xF3\xAB'),(0x2559,b'\xF3\xAB')):
        need(image.program_image[CS*16+at:CS*16+at+len(raw)]==raw,'native index / count / row recurrence instructions')
    indices = set()
    for value in range(65536):
        indices.add((SPRITE+value*16)&65535)
        sign = 65535 if value&0x8000 else 0
        need((signed((value-sign)&65535)>>1)==half(value),'all WORD signed halves truncate toward zero')
        count = value>>4
        need(0<=count<=4095 and ((2*count+(80-2*count))&65535)==80
             and ((-2*count+(80-2*count))&65535)==((80-4*count)&65535),'both inherited DF row recurrences')
    need(len(indices)==4096,'all WORD cels collapse to4096 physical source offsets')
    return dict(WORD_index_states=65536,distinct_flake_source_offsets=4096,flake_rows=8,WORD_dimension_states=65536,
                maximum_unput_WORDs_per_row=4095,unput_rows=3,maximum_unput_WORD_stores=12285,
                zero_REP_iterations=0,DF_clear_row_delta=80,DF_set_row_delta='80 - 4 * (unsigned_width >> 4), modulo WORD',
                budget_expiry_used=False,nonterminal_claim=False,
                assumptions=['flat mapped WORD operands; a WORD at FFFF spans two physical bytes',
                             'VRAM is disjoint from DGROUP, CODE and the private/caller stack',
                             'external sprite/slot fixture data; no planar hardware or asset ownership'])


GEOMETRIES = ((0,0,0,0,0),(0xFFFF,0,15,0xFFFF,1),(0x8000,0xFFFF,16,0x8000,0xFFFF),
    (0x7FFF,0x8000,17,0x7FFF,32),(641,399,32,16,31),(320,200,640,400,0),
    (7,3,0xFFFF,0xFFFF,0x8000),(15,0x7FFF,0x8000,1,0x1000),
    (8,0x8000,0x7FFF,0x8001,0xFFF),(0xFFF8,1,1,1,0xA52),(1,0xFFFF,48,3,0x1001),
    (0xFFFF,0xFFFF,0xFFF0,0xFFF0,0xFFFF))


def cases():
    for index in range(4096):
        yield 'flake',dict(index=index,left=index&7,top=(index>>3)&255)
    for kind,arg,shift,value in itertools.product(ENTRIES,('left','top','index'),(0,8),range(256)):
        yield kind,{arg:value<<shift}
    for shift,value,rotation in itertools.product((0,8),range(256),range(8)):
        yield 'flake',dict(source_word=value<<shift,left=rotation)
    for bit,rotation in itertools.product(range(16),range(8)):
        yield 'flake',dict(source_word=1<<bit,left=rotation)
    for field,shift,value in itertools.product(('width','height'),(0,8),range(256)):
        yield 'unput',{field:value<<shift}
    for kind,g,flags,ss,stack in itertools.product(ENTRIES,GEOMETRIES,(2,0x202,0x402,0xED7),(0x7000,0x8000),(0x80,0xF800)):
        left,top,width,height,index = g
        yield kind,dict(left=left,top=top,width=width,height=height,index=index,flags=flags,ss=ss,stack=stack)


def verify(target,candidate):
    proof = geometry_proof(target)
    need(proof==geometry_proof(candidate),'both complete native arithmetic/count proofs')
    observations = []
    for image_index,image in enumerate((target,candidate),1):
        rows = []
        for load in (0x1000,0x3000):
            m = Machine(image,load)
            trace = hashlib.sha256()
            counts,depths = {k:0 for k in ENTRIES},{k:0 for k in ENTRIES}
            total,maximum,minimum = 0,0,12285
            try:
                def entry(kind,parameters):
                    nonlocal total,maximum,minimum
                    result = m.run(kind,**parameters)
                    counts[kind] += 1
                    depths[kind] = max(depths[kind],result['stack_depth'])
                    total += result['graph_WORD_stores']
                    if kind=='unput':
                        maximum = max(maximum,result['graph_WORD_stores'])
                        minimum = min(minimum,result['graph_WORD_stores'])
                    trace.update(json.dumps(result,sort_keys=True).encode())
                for count,(kind,parameters) in enumerate(cases(),1):
                    entry(kind,dict(seed=0x1357 if count&1 else 0xECA8,**parameters))
                    if count%512==0:
                        print(f'Staff draw: image {image_index}, load {load:04X}, {count} complete entries',flush=True)
                for kind in ENTRIES:
                    for index in range(3):
                        entry(kind,dict(left=index,top=index*80,width=16+index*16,persistent=index>0,flags=0xED7))
                        count += 1
                need(m.owner<=m.covered,'every one of199 owner bytes executes')
                rows.append(dict(load_segment=load,cases=count,cases_by_function=counts,executed_owner_bytes=199,
                    maximum_stack_depth_by_function=depths,graph_WORD_stores=total,minimum_unput_WORD_stores=minimum,
                    maximum_unput_WORD_stores=maximum,trace_sha256=trace.hexdigest()))
                print(f'Staff draw: image {image_index}, load {load:04X}, {count} entries / 199 owner bytes pass',flush=True)
            finally:
                m.close()
        observations.append(rows)
    need(observations[0]==observations[1],'independent target/candidate complete observations')
    return dict(images=2,functions=2,code_bytes=199,executed_owner_bytes=199,cases_per_image=sum(r['cases'] for r in observations[0]),
        observations=observations[0],native_geometry_proof=proof,ignored_stack_bytes=0,
        caller_argument_stores_checked=True,flat_memory_operand_contract=True,
        helper_interfaces=0,sprite_assets_or_physical_graphics_owned=False)


def negative_controls(target):
    controls = (
        ('flake-save-SI',0x249D,1,'flake',{}),('flake-left-frame',0x24A1,2,'flake',{}),
        ('flake-signed-left',0x24A3,8,'flake',dict(left=0x8000)),('flake-top-scale64',0x24AA,1,'flake',dict(top=3)),
        ('flake-top-scale16',0x24B2,1,'flake',dict(top=3)),('flake-cel-frame',0x24B9,2,'flake',dict(index=1)),
        ('flake-cel-scale',0x24BC,1,'flake',dict(index=1)),('flake-source-base',0x24BF,2,'flake',{}),
        ('flake-blue-segment',0x24C3,1,'flake',{}),('flake-rotation-mask',0x24CB,8,'flake',dict(left=15,source_word=1)),
        ('flake-rotation-direction',0x24D3,8,'flake',dict(left=1,source_word=1)),('flake-OR',0x24D5,0x20,'flake',{}),
        ('flake-row-stride',0x24D9,1,'flake',{}),('flake-source-WORD-step',0x24DC,1,'flake',{}),
        ('flake-eight-rows',0x24CE,1,'flake',{}),('flake-row-backedge',0x24DF,1,'flake',{}),
        ('flake-Pascal-pop',0x24E4,2,'flake',{}),
        ('unput-local-frame',0x24E7,2,'unput',{}),('unput-slot-frame',0x24EE,2,'unput',dict(index=1)),
        ('unput-slot-scale',0x24F1,1,'unput',dict(index=1)),('unput-width-field',0x24F4,2,'unput',{}),
        ('unput-height-field',0x2501,2,'unput',{}),('unput-width-signed-half',0x250D,8,'unput',dict(width=0x8001)),
        ('unput-height-signed-half',0x2518,8,'unput',dict(height=0x8001)),('unput-vertical-minus-two',0x251A,1,'unput',{}),
        ('unput-caller-left-store',0x250F,2,'unput',{}),('unput-caller-top-store',0x251D,0x28,'unput',{}),
        ('unput-signed-left',0x2523,8,'unput',dict(left=0x8000)),('unput-unsigned-width-count',0x2541,1,'unput',{}),
        ('unput-row-distance',0x2543,1,'unput',{}),('unput-second-width-subtraction',0x2548,2,'unput',{}),
        ('unput-zero-fill',0x254A,8,'unput',{}),('unput-first-WORD-store',0x254E,1,'unput',{}),
        ('unput-first-row-add',0x2550,0x28,'unput',{}),('unput-second-row-add',0x2556,0x28,'unput',{}),
        ('unput-third-WORD-store',0x255A,1,'unput',{}),('unput-Pascal-pop',0x2560,2,'unput',{}))
    rejected = []
    for name,offset,xor,kind,parameters in controls:
        raw = bytearray(target.program_image)
        raw[CS*16+offset] ^= xor
        m = None
        try:
            m = Machine(replace(target,program_image=bytes(raw)),0x1000)
            m.run(kind,**parameters)
        except (ValueError,UcError):
            rejected.append(name)
        else:
            raise ValueError('MAINL staff draw actual instruction mutation escaped: '+name)
        finally:
            if m:
                m.close()
    return dict(count=len(rejected),rejected=rejected,actual_guest_instruction_mutations=True,
                flake_instruction_mutations=17,unput_instruction_mutations=20,unowned_data_mutations_counted=False)
