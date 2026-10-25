"""Staff callers with actual clear/unput/dissolve/blitter/color/off contexts.

The unowned bytebox routine is a bounded ABI reply. INT0 is a CPU divide-fault
observation before handler dispatch, not DOS/physical-device execution.
"""
import hashlib
import itertools
import json
import struct
from dataclasses import replace
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import UcError, UC_HOOK_INTR
from unicorn.x86_const import *
from lib.decoded_mainl_staff_callers_layout import CS, DS, DATA, ENTRIES
from lib.decoded_mainl_dissolve_runtime import Machine as DissolveMachine, Spec as DissolveSpec, CONTEXT as BLITTERS, PATTERNS
from lib.decoded_mainl_dissolve_layout import DATA as DISSOLVE_DATA
from lib.decoded_mainl_staff_draw_runtime import Spec as UnputSpec
from lib.decoded_mainl_snow_runtime import Spec as SnowSpec
from lib.decoded_mainl_pi_runtime import signed, ARITH
from lib.decoded_mainl_pi_free_runtime import address
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG, logical, specification as root_spec

CONTEXT = dict(BLITTERS)
CONTEXT.update({CS*16+0x2561:('clear',21),CS*16+0x24E6:('unput',123),CS*16+0x2731:('dissolve',211),0xC60:('off',5)})
BOX = 0xB9E
OWNED_RETURNS = {0x280F:'clear',0x28E2:'clear',0x282E:'unput',0x2908:'unput',
                 0x28B2:'dissolve',0x28CC:'dissolve',0x2946:'dissolve',0x2960:'dissolve',0x29BD:'dissolve',
                 0x2972:'color',0x2988:'off'}
OWNED_RETURN_AT = {CS*16+a:kind for a,kind in OWNED_RETURNS.items()}


def need(value,message):
    if not value:
        raise ValueError('MAINL staff callers contract: '+str(message))


def quotient(a,b):
    return (abs(a)//abs(b))*(-1 if (a<0)!=(b<0) else 1)


class ClearSpec(SnowSpec):
    def run(self):
        self.entry('clear',2)
        self.enter()
        self.push(self.r['di'])
        self.r.update(ax=0,cx=0,es=0xA800)
        self.logical(0)
        step = -2 if self.flags&0x400 else 2
        self.events.append(('rep-clear',0xA8000,16000,step))
        if step==2:
            self.memory[0xA8000:0xA8000+32000] = bytes(32000)
        else:
            self.memory[0xA8000:0xA8002] = bytes(2)
            self.memory[0xA8000+65536-31998:0xA8000+65536] = bytes(31998)
        self.pop('di')
        self.finish()


class Spec(SnowSpec):
    def page(self):
        self.r['ax'] = self.dg(DATA['page'],1)
        self.r['ax'] = self.op(self.r['ax'],self.r['ax'])
        self.r['bx'] = self.r['ax']
        return DATA['centers']+self.r['bx']

    def predicate(self,name):
        value = self.dg(DATA[name],1)
        self.op(value,0,True,bits=8)
        return bool(value)

    def owned(self,kind,continuation):
        self.push(continuation)
        sp = self.r['sp']
        if kind=='clear':
            child = ClearSpec(self.memory,self.r,self.high,self.flags,self.o)
            child.run()
        elif kind=='unput':
            self.entry('unput',8)
            slot,top,left = [self.word(self.ss,sp+2+i*2) for i in range(3)]
            child = UnputSpec(self.memory,self.r,self.high,self.flags,dict(self.o,index=slot,top=top,left=left))
            child.run('unput')
        else:
            need(kind=='dissolve','known owned near helper')
            self.entry('dissolve',10)
            child = DissolveSpec(self.memory,self.r,self.high,self.flags,self.o)
            child.run()
        self.events.extend(child.events)
        self.r,self.high,self.flags = child.r,child.high,child.flags
        self.mask = 0x8C5 if kind=='clear' else ARITH
        self.events.append(('owned-return',kind,self.full(),self.flags&(self.mask|0x600),self.mask|0x600))

    def color(self):
        self.push(0xC00000,4)
        self.frame(0x2972)
        at = address(self.ss,self.r['sp'])
        self.events.append(('color-entry',self.full(),bytes(self.memory[at:at+8]).hex(),self.flags&(ARITH|0x600)))
        out,mask,flags,events,_ = root_spec('setcolor',self.r,self.flags,random_seed=0,mode=0xC0,color=0,
            strings=(b'\0',b'\0'),pointers=((0x5000,0),(0x6000,0)),dos_status=0,reply_seed=0)
        self.events.extend(events)
        for event in events:
            if event[0]=='store':
                _,at,size,value = event
                self.memory[at:at+size] = value.to_bytes(size,'little')
        self.r,self.flags,self.mask = out,flags|2,mask
        self.r['cs'] = self.o['load']+CS
        self.events.append(('owned-return','color',self.full(),self.flags&(self.mask|0x600),self.mask|0x600))

    def box(self):
        self.push(0x10008,4)
        self.push(0x4E0187,4)
        self.frame(0x2983)
        at = address(self.ss,self.r['sp'])
        self.events.append(('box',self.full(),bytes(self.memory[at:at+12]).hex(),self.flags&(ARITH|0x600)))
        for offset,raw in self.o['box_writes']:
            at = address(self.ds,offset)
            self.events.append(('box-write',at,raw.hex()))
            self.memory[at:at+len(raw)] = raw
        value = self.o['box_seed']
        self.r.update(ax=value,cx=value^0x1234,dx=value^0x5AA5,es=0x6666)
        self.flags = (self.flags&0x600)|2|(value&ARITH)
        self.mask = ARITH
        self.returned(8)
        self.frame(0x2988)
        self.entry('off',4)
        self.r['ax'] &= 0xFF00
        self.logical(0,8)
        self.events.append(('out',0x7C,1,0,self.flags&0x200))
        self.returned(0)
        self.events.append(('owned-return','off',self.full(),self.flags&(self.mask|0x600),self.mask|0x600))

    def strength(self,frame,denominator,enter):
        if enter:
            self.r['ax'] = denominator&65535
            self.r['bx'] = 8
            self.r['dx'] = 65535 if denominator<0 else 0
            den = quotient(denominator,8)
            self.r['ax'],self.r['dx'] = den&65535,(denominator-den*8)&65535
            self.push(self.r['ax'])
            self.r['ax'] = frame&65535
            self.r['dx'] = 65535 if frame<0 else 0
            self.pop('bx')
            if den==0 or frame==-32768 and den==-1:
                self.mask = 0
                self.events.append(('divide-error',0x2885,self.full(),self.flags&0x600))
                return False
        else:
            den = 20
            self.r.update(ax=frame&65535,bx=20,dx=65535 if frame<0 else 0)
        result = quotient(frame,den)
        self.r['ax'],self.r['dx'] = result&65535,(frame-result*den)&65535
        if enter or self.o['kind']=='gallery':
            self.r['dx'] = self.op(7,self.r['ax'],True)
            self.r['si'] = self.r['dx']
            self.logical(self.r['si'])
            if signed(self.r['si'])<0:
                self.r['si'] = 0
                self.logical(0)
        else:
            self.r['si'] = self.r['ax']
            self.op(self.r['si'],7,True)
            if signed(self.r['si'])>7:
                self.r['si'] = 7
        return True

    def run(self,kind):
        self.enter()
        self.push(self.r['si'])
        if kind!='gallery':
            self.push(self.r['di'])
            self.r['di'] = self.word(self.ss,self.r['bp']+4)
            self.owned('clear',0x280F if kind=='enter' else 0x28E2)
        frame = self.dg(DATA['frame'])
        if kind=='gallery':
            self.op(frame,160,True)
            active = signed(frame)<=160
        elif kind=='enter':
            self.r['ax'] = frame
            self.op(frame,self.dg(DATA['duration']),True)
            active = signed(frame)<=signed(self.dg(DATA['duration']))
        else:
            self.op(frame,161,True)
            active = signed(frame)<=161
            if active:
                self.op(frame,160,True)
                if signed(frame)>=160:
                    self.color()
                    self.box()
                    active = False
        fault = False
        if active:
            if kind!='gallery':
                self.push(320)
                at = self.page()
                self.push(self.dg(at))
                self.push(self.r['di'])
                self.owned('unput',0x282E if kind=='enter' else 0x2908)
                at = self.page()
                if kind=='enter':
                    self.r['ax'] = self.dg(at)
                    self.op(self.r['ax'],self.dg(DATA['limit']),True)
                    if signed(self.r['ax'])>signed(self.dg(DATA['limit'])):
                        at = self.page()
                        self.r['dx'] = self.dg(DATA['speed'])
                        self.field(at,self.op(self.dg(at),self.r['dx'],True))
                        at = self.page()
                        self.r['ax'] = self.dg(at)
                        self.op(self.r['ax'],self.dg(DATA['limit']),True)
                        if signed(self.r['ax'])<signed(self.dg(DATA['limit'])):
                            at = self.page()
                            self.r['dx'] = self.dg(DATA['limit'])
                            self.field(at,self.r['dx'])
                else:
                    carry = self.flags&1
                    self.field(at,self.op(self.dg(at),1,True))
                    self.flags = (self.flags&~1)|carry
            frame = signed(self.dg(DATA['frame']))
            fault = not self.strength(frame,signed(self.dg(DATA['duration'])),kind=='enter')
            if not fault:
                if kind=='gallery':
                    for delta in (8,6,4):
                        self.push(self.word(self.ss,self.r['bp']+delta))
                    self.push(self.r['si'])
                    self.owned('dissolve',0x29BD)
                else:
                    if self.predicate('requested') and self.predicate('secondary'):
                        self.push(0x1F800C8,4)
                        self.r['ax'] = self.dg(DATA['secondary'],1)
                        self.push(self.r['ax'])
                        self.push(self.r['si'])
                        self.owned('dissolve',0x28B2 if kind=='enter' else 0x2946)
                        self.field(DATA['enabled'],1,1)
                    self.push(320)
                    at = self.page()
                    self.push(self.dg(at))
                    self.push(self.r['di'])
                    self.push(self.r['si'])
                    self.owned('dissolve',0x28CC if kind=='enter' else 0x2960)
                    self.field(DATA['enabled'],0,1)
        if not fault:
            if kind!='gallery':
                self.pop('di')
            self.pop('si')
            self.finish(6 if kind=='gallery' else 2)
        return self.full(),self.flags,self.mask,fault


class Machine(DissolveMachine):
    def __init__(self,image,load):
        super().__init__(image,load)
        self.image,self.faulted = image,False
        self.instructions,self.owner,self.samples = {},set(),{BOX,*OWNED_RETURN_AT}
        for kind,(offset,size,args) in ENTRIES.items():
            start = CS*16+offset
            self.owner.update(range(start,start+size))
        for start,size in [*[(CS*16+a,n) for a,n,_ in ENTRIES.values()],*[(a,n) for a,(_,n) in CONTEXT.items()]]:
            ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[start:start+size],start))
            need(sum(i.size for i in ins)==size,'complete owner / actual owned context instruction boundaries')
            self.instructions.update({i.address:i.size for i in ins})
            self.samples.add(start)
            self.samples.update(i.address+i.size for i in ins if i.mnemonic in ('push','pushf','enter'))
        self.seen = set()
        self.hooks.append(self.u.hook_add(UC_HOOK_INTR,self.interrupt))

    def write(self,u,access,at,size,value,_):
        if self.index<len(self.events) and self.events[self.index][0]=='rep-clear':
            try:
                _,base,count,step = self.events[self.index]
                need((at,size,value)==(base+(self.clear_progress*step&65535),2,0),
                     'every actual ordered REP clear WORD, including direction and count')
                self.clear_progress += 1
                self.actual_clear_stores += 1
                if self.clear_progress==count:
                    self.index += 1
                    self.clear_progress = 0
            except Exception as error:
                self.fail(error)
            return
        super().write(u,access,at,size,value,_)

    def interrupt(self,u,number,_):
        try:
            ip = u.reg_read(UC_X86_REG_IP)
            need(number==0 and ip==0x2885,('actual native divide exception site',number,ip))
            self.event(('divide-error',ip,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&0x600))
            self.faulted = True
            u.emu_stop()
        except Exception as error:
            self.fail(error)

    def code(self,u,at,size,_):
        try:
            offset = at-self.base
            if at==self.cs*16+0xFFFF:
                self.returned = True
                u.emu_stop()
                return
            if offset!=BOX:
                need(self.instructions.get(offset)==size,'only actual owned staff/context instructions')
                if offset not in self.seen:
                    self.covered.update(range(offset,offset+size))
                    self.seen.add(offset)
            if offset not in self.samples:
                return
            self.max_depth = max(self.max_depth,self.o['stack']-u.reg_read(REG['sp']))
            if offset in OWNED_RETURN_AT and self.index<len(self.events) and self.events[self.index][:2]==('owned-return',OWNED_RETURN_AT[offset]):
                expected = self.events[self.index]
                mask = expected[-1]
                self.event(('owned-return',expected[1],self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
            if offset in CONTEXT or offset==BOX:
                kind = CONTEXT[offset][0] if offset!=BOX else 'box'
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                if self.index<len(self.events) and self.events[self.index][0]=='far-frame':
                    ip,cs = struct.unpack('<2H',bytes(u.mem_read(address(ss,sp),4)))
                    self.event(('far-frame',address(ss,sp),ip,cs))
                if kind=='box':
                    self.event(('box',self.regs(True),bytes(u.mem_read(address(ss,sp),12)).hex(),u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)))
                    for off,raw in self.o['box_writes']:
                        location = address(self.ds,off)
                        self.event(('box-write',location,raw.hex()))
                        u.mem_write(location,raw)
                    value = self.o['box_seed']
                    for name,v in dict(ax=value,cx=value^0x1234,dx=value^0x5AA5,es=0x6666).items():
                        u.reg_write(REG[name],v)
                    u.reg_write(UC_X86_REG_EFLAGS,(u.reg_read(UC_X86_REG_EFLAGS)&0x600)|2|(value&ARITH))
                    ip,cs = struct.unpack('<2H',bytes(u.mem_read(address(ss,sp),4)))
                    u.reg_write(REG['sp'],sp+12)
                    u.reg_write(REG['cs'],cs)
                    u.reg_write(REG['ip'],ip)
                    return
                if kind in ('clear','unput','dissolve','off'):
                    frame_size = dict(clear=2,unput=8,dissolve=10,off=4)[kind]
                    self.event(('entry',kind,self.regs(True),bytes(u.mem_read(address(ss,sp),frame_size)).hex()))
                elif kind=='color':
                    self.event(('color-entry',self.regs(True),bytes(u.mem_read(address(ss,sp),8)).hex(),u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)))
                else:
                    self.event(('blit-entry',kind,self.regs(True),bytes(u.mem_read(address(ss,sp),10)).hex(),u.reg_read(UC_X86_REG_EFLAGS)&ARITH))
        except Exception as error:
            self.fail(error)

    def run(self,kind,*,slot=0,frame=64,duration=640,page=0,center=200,speed=3,limit=180,
            secondary=1,enabled=0,requested=1,left=320,top=200,width=16,height=1,blit_width=1,
            box_seed=0xA55A,box_writes=(),flags=0x202,ss=0x7000,stack=0xF800,seed=0x1357,persistent=False):
        if self.faulted:
            # A stopped QEMU exception leaves hidden exception-dispatch state.
            # Begin the next independent entry on a fresh CPU, retaining the
            # exact memory when persistent reentry is explicitly requested.
            memory = bytes(self.u.mem_read(0,1<<20)) if persistent else None
            covered,image,load = self.covered,self.image,self.load
            self.close()
            self.__init__(image,load)
            self.covered = covered
            if memory is not None:
                self.u.mem_write(0,memory)
        need(kind in ENTRIES and all(0<=v<=65535 for v in (slot,frame,duration,center,speed,limit,left,top,width,height,blit_width,box_seed)),'WORD state / arguments')
        need(all(0<=v<=255 for v in (page,secondary,enabled,requested)),'unchecked raw BYTE state')
        need(ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),'bounded foreign SS and incoming IF/DF')
        need(all(0<=off<off+len(raw)<=65536 and isinstance(raw,bytes) for off,raw in box_writes),'bounded bytebox reply writes')
        memory = bytearray(self.u.mem_read(0,1<<20) if persistent else self.initial)
        def put(offset,value,size=2):
            at = address(self.ds,offset&65535)
            memory[at:at+size] = value.to_bytes(size,'little')
        if not persistent:
            for i in range(256):
                put(DATA['centers']+i*2,center)
            for i,v in enumerate(PATTERNS):
                put(DISSOLVE_DATA['pattern']+i*2,v)
            for index in (slot,secondary):
                first = (DISSOLVE_DATA['slots']+index*16)&65535
                for delta,value in ((0,0),(2,width),(4,height),(6,0xFFFF),(8,blit_width),(10,0),(12,0x5000),(14,0x6000)):
                    put(first+delta,value)
            for name,value in (('frame',frame),('duration',duration),('speed',speed),('limit',limit),('adapt',0)):
                put(DATA[name],value)
            put(0x27D2,0)
            put(0x27D4,0)
            for name,value in (('page',page),('secondary',secondary),('enabled',enabled),('requested',requested)):
                put(DATA[name],value,1)
        args = (slot,top,left) if kind=='gallery' else (slot,)
        at = address(ss,stack)
        memory[at:at+2+len(args)*2] = struct.pack('<'+'H'*(1+len(args)),0xFFFF,*args)
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
        self.o = dict(load=self.load,stack=stack,kind=kind,box_seed=box_seed,box_writes=box_writes)
        spec = Spec(memory,regs,high,flags,self.o)
        expected,final,mask,fault = spec.run(kind)
        self.events,self.index,self.error,self.returned,self.faulted,self.max_depth,self.far_word_hooks = spec.events,0,None,False,False,0,0
        self.clear_progress,self.actual_clear_stores = 0,0
        try:
            self.u.emu_start(self.cs*16+ENTRIES[kind][0],1<<20,count=6000000)
        except UcError as error:
            raise ValueError('MAINL staff callers contract: guest fault') from error
        need(self.error is None,self.error or 'guest failure')
        need(self.index==len(self.events) and (self.faulted if fault else self.returned),'actual full near return / native INT0 and ordered events')
        need(self.regs(True)==expected,'complete DWORD/segment effects '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(mask|0x600)==final&(mask|0x600),'defined flags and IF/DF')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'all physical memory / nested frames / caller bytes / live state / SMC')
        counts = {name:sum(e[:2]==('entry',name) for e in self.events) for name in ('clear','unput','dissolve','off')}
        counts.update(alpha=sum(e[:2]==('blit-entry','alpha') for e in self.events),noalpha=sum(e[:2]==('blit-entry','noalpha') for e in self.events),
                      box=sum(e[0]=='box' for e in self.events),color=sum(e[0]=='color-entry' for e in self.events))
        return dict(kind=kind,registers=expected,flags=final&(mask|0x600),flag_mask=mask|0x600,divide_fault=fault,
            actual_calls=counts,actual_clear_WORD_stores=self.actual_clear_stores,stack_depth=self.max_depth,
            events=len(self.events),trace_sha256=hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest())


def geometry_proof(image):
    for at,raw in ((0x2876,b'\xA1\xCE\x27\xBB\x08\0\x99\xF7\xFB\x50\xA1\xC2\x27\x99\x5B\xF7\xFB'),
        (0x28E2,b'\x81\x3E\xC2\x27\xA1\0\x0F\x8F\x9C\0\x81\x3E\xC2\x27\xA0\0\x7D\x73'),
        (0x2915,b'\xA1\xC2\x27\xBB\x14\0\x99\xF7\xFB\x8B\xF0\x83\xFE\x07\x7E\x03\xBE\x07\0'),
        (0x2992,b'\x81\x3E\xC2\x27\xA0\0\x7F\x23\xA1\xC2\x27\xBB\x14\0\x99\xF7\xFB'),
        (0x256A,b'\x31\xC0\x89\xC7\xB9\x80\x3E\xF3\xAB')):
        need(image.program_image[CS*16+at:CS*16+at+len(raw)]==raw,'native signed division / readonly frame gates / clear CFG')
    zero,overflow = [],[]
    for value in range(65536):
        den = quotient(signed(value),8)
        if den==0:
            zero.append(value)
        if den==-1:
            overflow.append(value)
        if signed(value)<160:
            need(quotient(signed(value),20)<=7,'all WORD frames prove leave cap instruction unreachable')
    need(zero==list(range(8))+list(range(0xFFF9,0x10000)) and overflow==list(range(0xFFF1,0xFFF9)),
         'complete zero/overflow duration classes')
    need(all(DATA['centers']+2*p>DATA['enabled'] and DATA['centers']+2*p+1<65536 for p in range(256)),
         'all raw BYTE pages remain disjoint from the readonly frame and controls')
    return dict(frame_WORD_states=65536,duration_WORD_states=65536,page_BYTE_states=256,
        zero_divisor_duration_WORDs=zero,overflow_duration_WORDs=overflow,overflow_frame_WORD=0x8000,
        divide_fault_site=0x2885,proved_unreachable_ranges=[dict(segment=CS,offset=0x2925,size=3)],
        complete_raw_owner_bytes=446,executed_owner_bytes=443,proved_unreachable_bytes=3,
        actual_clear_WORDs_per_call=16000,rep_log_compacted=True,every_actual_clear_WORD_checked=True,
        guest_iterations_skipped=False,budget_expiry_used=False,
        assumptions=['disjoint CODE/DGROUP/stack/VRAM; no external writes until strength division',
                     'owned unput writes graph/stack only; BYTE page indexes centers without WORD wrap'],
        bytebox_body_or_INT0_handler_or_physical_graphics_proved=False)


def cases():
    for kind,shift,value in itertools.product(ENTRIES,(0,8),range(256)):
        yield kind,dict(frame=value<<shift)
    for shift,value in itertools.product((0,8),range(256)):
        yield 'enter',dict(duration=value<<shift,frame=0)
    for field,shift,value in itertools.product(('speed','limit','center'),(0,8),range(256)):
        yield 'enter',dict(requested=0,secondary=0,enabled=0,blit_width=0,**{field:value<<shift})
    for kind,page in itertools.product(('enter','leave'),range(256)):
        yield kind,dict(page=page)
    for kind,secondary in itertools.product(('enter','leave'),range(256)):
        yield kind,dict(frame=0,secondary=secondary)
    for kind,field,value in itertools.product(ENTRIES,('enabled','requested'),range(256)):
        yield kind,dict(**{field:value})
    for field,shift,value in itertools.product(('slot','left','top'),(0,8),range(256)):
        yield 'gallery',dict(frame=140,center=0,duration=0,speed=0,limit=0,requested=0,secondary=0,enabled=0,blit_width=0,**{field:value<<shift})
    for duration in range(-7,8):
        for frame in (duration,duration-1,-32768):
            yield 'enter',dict(duration=duration&65535,frame=frame&65535)
    for duration in range(-15,-7):
        yield 'enter',dict(duration=duration&65535,frame=0x8000)
    for center,speed,limit in ((200,100,180),(200,3,180),(180,3,180),(179,3,180),
        (0x7FFF,0xFFFF,180),(0x8000,1,180),(0,0x8000,0xFFFF),(1,2,0),
        (0x8000,1,0x8001),(0x7FFF,0x8000,0),(0xFFFF,0xFFFF,0x8000),(1,0,0)):
        yield 'enter',dict(center=center,speed=speed,limit=limit,requested=0,secondary=0,blit_width=0)
    for kind,flags,ss,stack in itertools.product(ENTRIES,(2,0x202,0x402,0xED7),(0x7000,0x8000),(0x80,0xF800)):
        yield kind,dict(flags=flags,ss=ss,stack=stack)
    for flags,ss,stack in itertools.product((2,0x202,0x402,0xED7),(0x7000,0x8000),(0x80,0xF800)):
        yield 'enter',dict(duration=7,frame=0,flags=flags,ss=ss,stack=stack)
    for shift,value in itertools.product((0,8),range(256)):
        yield 'leave',dict(frame=160,box_seed=value<<shift)
    for flags,ss,stack in itertools.product((2,0x202,0x402,0xED7),(0x7000,0x8000),(0x80,0xF800)):
        yield 'leave',dict(frame=160,flags=flags,ss=ss,stack=stack)
    yield 'leave',dict(frame=161,box_writes=((DATA['page'],b'\xFE'),(DATA['enabled'],b'\xFF'),(DATA['frame'],b'\0\x80')))
    for kind,frame in (('enter',639),('enter',640),('enter',641),('enter',0x8000),('leave',159),('leave',160),('leave',161),('leave',162),('gallery',159),('gallery',160),('gallery',161)):
        yield kind,dict(frame=frame,duration=8 if frame==0x8000 else 640)


def verify(target,candidate):
    proof = geometry_proof(target)
    need(proof==geometry_proof(candidate),'both complete native fault / unreachable / clear proofs')
    observations = []
    unreachable = set(range(CS*16+0x2925,CS*16+0x2928))
    context = {b for a,(_,n) in CONTEXT.items() for b in range(a,a+n)}
    for image_index,image in enumerate((target,candidate),1):
        rows = []
        for load in (0x1000,0x3000):
            m = Machine(image,load)
            trace,counts,faults,peaks,maximums,clear_stores = hashlib.sha256(),{k:0 for k in ENTRIES},{k:0 for k in ENTRIES},{k:0 for k in ENTRIES},{k:0 for k in ('clear','unput','dissolve','off','alpha','noalpha','box','color')},0
            try:
                def entry(kind,parameters):
                    nonlocal clear_stores
                    result = m.run(kind,**parameters)
                    counts[kind] += 1
                    faults[kind] += int(result['divide_fault'])
                    peaks[kind] = max(peaks[kind],result['stack_depth'])
                    clear_stores += result['actual_clear_WORD_stores']
                    need(result['actual_clear_WORD_stores']==result['actual_calls']['clear']*16000,'all actual clear WORD callbacks checked')
                    for k in maximums:
                        maximums[k] = max(maximums[k],result['actual_calls'][k])
                    trace.update(json.dumps(result,sort_keys=True).encode())
                for count,(kind,parameters) in enumerate(cases(),1):
                    try:
                        entry(kind,dict(seed=0x1357 if count&1 else 0xECA8,**parameters))
                    except Exception:
                        print('Staff callers failing case',image_index,load,count,kind,parameters,flush=True)
                        raise
                    if count%256==0:
                        print(f'Staff callers: image {image_index}, load {load:04X}, {count} complete returns / native faults',flush=True)
                for kind in ENTRIES:
                    for i in range(3):
                        entry(kind,dict(persistent=i>0))
                        count += 1
                need(m.owner-m.covered==unreachable and context<=m.covered,'exact443 executed owner bytes / three proved unreachable / all693 actual context bytes')
                rows.append(dict(load_segment=load,cases=count,cases_by_function=counts,divide_faults_by_function=faults,
                    returned_calls=count-sum(faults.values()),native_divide_faults=sum(faults.values()),
                    complete_raw_owner_bytes=446,executed_owner_bytes=443,proved_unreachable_bytes=3,
                    actual_context_bytes=693,maximum_stack_depth_by_function=peaks,maximum_actual_calls=maximums,
                    actual_clear_WORD_callbacks=clear_stores,trace_sha256=trace.hexdigest()))
                print(f'Staff callers: image {image_index}, load {load:04X}, {count} entries /443 executed +3 unreachable bytes pass',flush=True)
            finally:
                m.close()
        observations.append(rows)
    need(observations[0]==observations[1],'independent full target/candidate observations')
    return dict(images=2,functions=3,code_bytes=446,cases_per_image=sum(o['cases'] for o in observations[0]),
        observations=observations[0],executed_owner_bytes=443,proved_unreachable_bytes=3,actual_owned_context_bytes=693,
        ignored_stack_bytes=0,native_geometry_proof=proof,bytebox_body_or_INT0_handler_or_physical_graphics_proved=False,
        fresh_CPU_after_stopped_divide_exception=True,immediate_owned_return_checks=True,guest_iterations_skipped=False)


def negative_controls(target):
    controls = (
        ('enter-frame',0x2804,1,'enter',{}),('enter-slot',0x280B,2,'enter',{}),
        ('enter-real-clear',0x280D,1,'enter',{}),('enter-signed-frame',0x2817,1,'enter',{}),
        ('enter-real-unput',0x282C,1,'enter',{}),('enter-page-zero-extension',0x2821,1,'enter',{}),
        ('enter-center-test',0x283F,1,'enter',{}),('enter-speed-field',0x284A,2,'enter',{}),
        ('enter-center-SUB',0x284E,8,'enter',{}),('enter-center-clamp',0x2863,1,'enter',dict(speed=100)),
        ('enter-duration-divisor',0x287A,1,'enter',{}),('enter-signed-IDIV',0x2886,8,'enter',dict(frame=0xFFFF)),
        ('enter-native-divide-fault',0x2885,0x20,'enter',dict(duration=7,frame=0)),
        ('enter-strength-SUB',0x288B,1,'enter',dict(frame=80)),('enter-lower-clamp',0x2890,1,'enter',{}),
        ('enter-requested-BYTE',0x2898,1,'enter',{}),('enter-secondary-BYTE',0x289F,1,'enter',{}),
        ('enter-DWORD-coordinates',0x28A4,1,'enter',{}),('enter-secondary-zero-extension',0x28AC,1,'enter',{}),
        ('enter-enable-alpha',0x28B6,1,'enter',{}),('enter-main-page',0x28BE,1,'enter',{}),
        ('enter-real-dissolve',0x28CA,1,'enter',{}),('enter-reset-alpha',0x28D0,1,'enter',{}),
        ('enter-Pascal-pop2',0x28D5,1,'enter',{}),
        ('leave-real-clear',0x28E0,1,'leave',{}),('leave-last161',0x28E6,1,'leave',dict(frame=161)),
        ('leave-box160',0x28F0,1,'leave',dict(frame=160)),('leave-page',0x28FB,1,'leave',{}),
        ('leave-DEC-center',0x2912,8,'leave',{}),('leave-divisor20',0x2919,1,'leave',{}),
        ('leave-unreachable-cap-guard',0x2923,1,'leave',{}),('leave-requested',0x292C,1,'leave',{}),
        ('leave-secondary',0x2933,1,'leave',{}),('leave-coordinates',0x2938,1,'leave',{}),
        ('leave-enable-alpha',0x294A,1,'leave',{}),('leave-real-dissolve',0x295E,1,'leave',{}),
        ('leave-reset-alpha',0x2964,1,'leave',{}),('leave-color-argument',0x2969,1,'leave',dict(frame=160)),
        ('leave-box-argument',0x2974,1,'leave',dict(frame=160)),('leave-box-call',0x297F,1,'leave',dict(frame=160)),
        ('leave-off-call',0x2984,1,'leave',dict(frame=160)),('leave-Pascal-pop2',0x298C,1,'leave',{}),
        ('gallery-save-SI',0x2991,1,'gallery',{}),('gallery-last160',0x2996,1,'gallery',dict(frame=161)),
        ('gallery-divisor20',0x299E,1,'gallery',dict(frame=20)),('gallery-lower-clamp',0x29AC,1,'gallery',{}),
        ('gallery-left',0x29B2,2,'gallery',{}),('gallery-top',0x29B5,2,'gallery',{}),
        ('gallery-slot',0x29B8,2,'gallery',{}),('gallery-real-dissolve',0x29BB,1,'gallery',{}),
        ('gallery-Pascal-pop6',0x29C0,1,'gallery',{}))
    context = (
        ('actual-clear-REP-count',CS*16+0x256F,1,'enter',{}),
        ('actual-unput-slot',CS*16+0x24EF,2,'enter',{}),
        ('actual-dissolve-mask',CS*16+0x2796,1,'gallery',dict(frame=0)),
        ('actual-alpha-cleanup',0xC7E*16+0x2A5,1,'enter',{}),
        ('actual-color-frame',0xC38,1,'leave',dict(frame=160)))
    rejected,by_function = [],{k:0 for k in ENTRIES}
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
                by_function[kind] += 1
        else:
            raise ValueError('MAINL staff callers actual instruction mutation escaped: '+name)
        finally:
            if m:
                m.close()
    return dict(count=len(rejected),rejected=rejected,owner_instruction_mutations=len(controls),by_function=by_function,
        actual_context_instruction_mutations=len(context),actual_guest_instruction_mutations=True,
        unreachable_bytes_counted_as_executed_controls=False,unowned_DATA_mutations_counted=False)
