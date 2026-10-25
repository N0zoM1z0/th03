"""Stateful pair loops with actual staff, snow, RNG/vector and blitter code.

PMD replies and counter writes are explicit interfaces. Conditional prefixes
prove software CFG/invariants; no physical IRQ, driver or elapsed-frame claim.
"""
import hashlib
import itertools
import json
import struct
from dataclasses import replace
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import UcError
from unicorn.x86_const import *
from lib.decoded_mainl_staff_pair_layout import CS, DS, START, SIZE, DATA
from lib.decoded_mainl_staff_callers_runtime import Machine as CallerMachine, Spec as CallerSpec, ClearSpec, UnputSpec, DissolveSpec, CONTEXT as CALLER_CONTEXT
from lib.decoded_mainl_staff_callers_layout import DATA as STAFF
from lib.decoded_mainl_snow_runtime import Spec as SnowSpec, CONTEXT as SNOW_CONTEXT, particle_fixture
from lib.decoded_mainl_snow_layout import ENTRIES as SNOW_ENTRIES, DATA as SNOW
from lib.decoded_mainl_dissolve_layout import DATA as DISSOLVE
from lib.decoded_mainl_dissolve_runtime import PATTERNS
from lib.decoded_mainl_pi_runtime import ARITH, signed
from lib.decoded_mainl_pi_free_runtime import address
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG

NODES = {'enter':(CS,0x2804,211,4),'leave':(CS,0x28D7,183,4),**{k:(CS,*SNOW_ENTRIES[k][:2],SNOW_ENTRIES[k][2]+2)
         for k in ('spawn','update','render','tick','gate')},**SNOW_CONTEXT}
ENTRY_AT = {s*16+a:(kind,n,frame) for kind,(s,a,n,frame) in NODES.items()}
CONTEXT = dict(CALLER_CONTEXT)
CONTEXT.update({s*16+a:(kind,n) for kind,(s,a,n,_) in NODES.items()})
RETURNS = {0x2AF0:'enter',0x2B05:'dissolve',0x2B0D:'tick',0x2B1A:'gate',0x2B3A:'unput',
           0x2B3E:'leave',0x2B81:'dissolve',0x2B8E:'color',0x2BA4:'off',0x2BAC:'tick',0x2BB9:'gate',
           0x2BCA:'color',0x2BE0:'off',0x2BE3:'tick',0x2BEE:'color',0x2C04:'off',0x2C07:'tick'}
RETURN_AT = {CS*16+a:k for a,k in RETURNS.items()}
DEFAULT_SCHEDULE = ((0xFFFF,((STAFF['frame'],b'\xC1\0'),),0x8D5),)


def need(value,message):
    if not value:
        raise ValueError('MAINL staff pair contract: '+str(message))


def driver(schedule,index):
    return schedule[min(index,len(schedule)-1)]


class Spec(SnowSpec):
    def __init__(self,*args):
        super().__init__(*args)
        self.gates,self.ticks,self.iterations,self.stopped = 0,0,[0,0],None

    def page(self,xor=False):
        self.r['ax'] = self.dg(DATA['page'],1)
        if xor:
            self.r['ax'] ^= 1
            self.logical(self.r['ax'])
        self.r['ax'] = self.op(self.r['ax'],self.r['ax'])
        self.r['bx'] = self.r['ax']
        return DATA['centers']+self.r['bx']

    def call(self,kind,continuation):
        self.push(continuation)
        options = dict(self.o,kind=kind)
        if kind in ('enter','leave'):
            self.entry(kind,4)
            child = CallerSpec(self.memory,self.r,self.high,self.flags,options)
            _,_,mask,fault = child.run(kind)
            if fault:
                self.stopped = 'divide-fault'
        elif kind=='unput':
            self.entry('unput',8)
            sp = self.r['sp']
            slot,top,left = [self.word(self.ss,sp+2+i*2) for i in range(3)]
            child = UnputSpec(self.memory,self.r,self.high,self.flags,dict(options,index=slot,top=top,left=left))
            child.run('unput')
            mask = ARITH
        elif kind=='dissolve':
            self.entry('dissolve',10)
            child = DissolveSpec(self.memory,self.r,self.high,self.flags,options)
            child.run()
            mask = ARITH
        elif kind=='clear':
            child = ClearSpec(self.memory,self.r,self.high,self.flags,options)
            child.run()
            mask = child.mask
        else:
            if kind=='gate':
                measure,writes,flags = driver(self.o['schedule'],self.gates)
                options.update(pmd_measure=measure,pmd_writes=writes,pmd_flags=flags)
                self.gates += 1
            else:
                need(kind=='tick','known actual child')
                self.ticks += 1
            child = SnowSpec(self.memory,self.r,self.high,self.flags,options)
            child.invoke(kind)
            mask = child.mask
            if child.prefix:
                self.stopped = 'clock-prefix'
        self.events.extend(child.events)
        self.r,self.high,self.flags,self.mask = child.r,child.high,child.flags,mask
        if self.stopped is None:
            self.events.append(('owned-return',kind,self.full(),self.flags&(self.mask|0x600),self.mask|0x600))

    def color(self,continuation):
        # Independent root interface model; the native setcolor body executes.
        from lib.decoded_mainl_root_helpers_runtime import specification as root_spec
        self.push(0xC00000,4)
        self.frame(continuation)
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

    def box(self,continuation,off_return):
        self.push(0x10008,4)
        self.push(0x4E0187,4)
        self.frame(continuation)
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
        self.frame(off_return)
        self.entry('off',4)
        self.r['ax'] &= 0xFF00
        self.logical(0,8)
        self.events.append(('out',0x7C,1,0,self.flags&0x200))
        self.returned(0)
        self.events.append(('owned-return','off',self.full(),self.flags&(self.mask|0x600),self.mask|0x600))

    def secondary(self,strength,continuation):
        self.push(320)
        self.push(self.dg(DATA['secondary_y']))
        self.r['ax'] = (self.r['si']-1)&65535  # Native LEA leaves all flags unchanged.
        self.push(self.r['ax'])
        if strength is not None:
            self.push(strength)
        self.call('unput' if strength is None else 'dissolve',continuation)

    def run(self):
        self.enter()
        self.push(self.r['si'])
        self.push(self.r['di'])
        self.r['si'] = self.word(self.ss,self.r['bp']+8)
        speed = self.dg(DATA['speed'])
        self.op(speed,2,True)
        if speed==2:
            self.field(self.page(),264)
            self.field(self.page(xor=True),263)
        else:
            self.r['ax'] = self.op(280,self.dg(DATA['height_offset']),True)
            self.field(DATA['centers'],self.r['ax'])
            self.field(DATA['centers']+2,self.r['ax'])
        for phase in (0,1):
            self.field(DATA['frame'],0)
            while True:
                if phase==0 and self.o['loop_prefix'] and self.iterations[0]==self.o['loop_prefix']:
                    self.events.append(('pair-prefix',self.iterations[0],self.full(),self.flags&(self.mask|0x600),self.mask|0x600))
                    self.stopped = 'enter-prefix'
                    return self.full(),self.flags,self.mask,self.stopped
                if phase==0:
                    self.push(self.r['si'])
                    self.call('enter',0x2AF0)
                    if self.stopped:
                        return self.full(),self.flags,self.mask,self.stopped
                    self.field(DATA['enabled'],1,1)
                    self.secondary(0,0x2B05)
                    self.field(DATA['enabled'],0,1)
                else:
                    frame = self.dg(DATA['frame'])
                    self.op(frame,161,True)
                    if signed(frame)<=161:
                        self.secondary(None,0x2B3A)
                    self.push(self.r['si'])
                    self.call('leave',0x2B3E)
                    frame = self.dg(DATA['frame'])
                    self.op(frame,161,True)
                    if signed(frame)<=161:
                        self.r['ax'] = frame
                        carry = self.flags&1
                        self.r['ax'] = self.op(self.r['ax'],1,True)
                        self.flags = (self.flags&~1)|carry
                        self.r['bx'] = 20
                        value = signed(self.r['ax'])
                        self.r['dx'] = 65535 if value<0 else 0
                        q = (abs(value)//20)*(-1 if value<0 else 1)
                        self.r['ax'],self.r['dx'] = q&65535,(value-q*20)&65535
                        self.r['di'] = self.r['ax']
                        self.op(self.r['di'],7,True)
                        if signed(self.r['di'])>7:
                            self.r['di'] = 7
                        page = self.dg(DATA['page'],1)
                        self.op(page,0,True,bits=8)
                        if page==0:
                            carry = self.flags&1
                            self.field(DATA['secondary_y'],self.op(self.dg(DATA['secondary_y']),1,True))
                            self.flags = (self.flags&~1)|carry
                        self.field(DATA['enabled'],1,1)
                        frame = self.dg(DATA['frame'])
                        self.op(frame,160,True)
                        if signed(frame)<160:
                            self.secondary(self.r['di'],0x2B81)
                        else:
                            self.color(0x2B8E)
                            self.box(0x2B9F,0x2BA4)
                        self.field(DATA['enabled'],0,1)
                self.call('tick',0x2B0D if phase==0 else 0x2BAC)
                if self.stopped:
                    return self.full(),self.flags,self.mask,self.stopped
                carry = self.flags&1
                self.field(DATA['frame'],self.op(self.dg(DATA['frame']),1))
                self.flags = (self.flags&~1)|carry
                self.push(self.word(self.ss,self.r['bp']+(6 if phase==0 else 4)))
                self.push(256)
                self.call('gate',0x2B1A if phase==0 else 0x2BB9)
                self.logical(self.r['ax'])
                self.iterations[phase] += 1
                if self.r['ax']:
                    break
                need(sum(self.iterations)<600,'bounded complete fixture or explicitly proved prefix; not a program bound')
        for color,box,off,tick in ((0x2BCA,0x2BDB,0x2BE0,0x2BE3),(0x2BEE,0x2BFF,0x2C04,0x2C07)):
            self.color(color)
            self.box(box,off)
            self.call('tick',tick)
            if self.stopped:
                return self.full(),self.flags,self.mask,self.stopped
        self.pop('di')
        self.pop('si')
        self.pop('bp')
        self.r['sp'] += 8
        return self.full(),self.flags,self.mask,'return'


class Machine(CallerMachine):
    def __init__(self,image,load):
        super().__init__(image,load)
        self.instructions,self.samples,self.seen,self.owner = {},set(),set(),set(range(CS*16+START,CS*16+START+SIZE))
        for start,size in [(CS*16+START,SIZE),*[(a,n) for a,(_,n) in CONTEXT.items()]]:
            ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[start:start+size],start))
            need(sum(i.size for i in ins)==size,'complete pair and actual context instruction boundaries')
            self.instructions.update({i.address:i.size for i in ins})
            self.samples.add(start)
            self.samples.update(i.address+i.size for i in ins if i.mnemonic in ('push','pushf','enter'))
        from lib.decoded_mainl_staff_callers_runtime import OWNED_RETURN_AT
        self.samples.update(OWNED_RETURN_AT)
        self.samples.update(RETURN_AT)
        self.samples.add(0xB9E)

    def interrupt(self,u,number,_):
        if number==0:
            super().interrupt(u,number,_)
            return
        try:
            need(number==0x60 and self.gate_index>0,'bounded PMD interrupt at actual gate')
            mask = ARITH|0x600
            self.event(('pmd',number,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
            measure,writes,flags = driver(self.o['schedule'],self.gate_index-1)
            for off,raw in writes:
                at = address(self.ds,off)
                self.event(('pmd-write',at,raw.hex()))
                u.mem_write(at,raw)
            u.reg_write(REG['ax'],measure)
            u.reg_write(UC_X86_REG_EFLAGS,(u.reg_read(UC_X86_REG_EFLAGS)&0x600)|2|(flags&ARITH))
        except Exception as error:
            self.fail(error)

    def code(self,u,at,size,_):
        try:
            offset = at-self.base
            if offset==CS*16+0x2AEC and self.o['loop_prefix'] and self.phase_counts[0]==self.o['loop_prefix']:
                mask = self.events[self.index][-1]
                self.event(('pair-prefix',self.phase_counts[0],self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                self.prefix_stopped = True
                u.emu_stop()
                return
            if offset in ENTRY_AT:
                kind,_,frame_size = ENTRY_AT[offset]
                sp,ss = u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                if self.index<len(self.events) and self.events[self.index][0]=='far-frame':
                    ip,cs = struct.unpack('<2H',bytes(u.mem_read(address(ss,sp),4)))
                    self.event(('far-frame',address(ss,sp),ip,cs))
                self.event(('entry',kind,self.regs(True),bytes(u.mem_read(address(ss,sp),frame_size)).hex()))
                if kind=='gate':
                    self.gate_index += 1
                elif kind=='tick':
                    self.tick_index += 1
                    self.polls = 0
            if offset in RETURN_AT and (offset not in (CS*16+0x2B3A,CS*16+0x2BA4) or
                    self.index<len(self.events) and self.events[self.index][:2]==('owned-return',RETURN_AT[offset])):
                expected = self.events[self.index]
                need(expected[:2]==('owned-return',RETURN_AT[offset]),'actual immediate owned return in pair')
                mask = expected[-1]
                self.event(('owned-return',expected[1],self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                if offset==CS*16+0x2B1A:
                    self.phase_counts[0] += 1
                elif offset==CS*16+0x2BB9:
                    self.phase_counts[1] += 1
            if offset==CS*16+0x270E:
                prefix = self.o['prefix']
                if prefix and self.polls==prefix:
                    self.event(('prefix',self.polls,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)))
                    self.prefix_stopped = True
                    u.emu_stop()
                    return
                ticks = self.o['ticks']
                value = int.from_bytes(u.mem_read(address(self.ds,SNOW['vsync']),2),'little') if ticks is None else ticks[self.polls]
                self.event(('poll',value))
                if ticks is not None:
                    u.mem_write(address(self.ds,SNOW['vsync']),struct.pack('<H',value))
                self.polls += 1
        except Exception as error:
            self.fail(error)
            return
        super().code(u,at,size,_)

    def run(self,*,slot=1,enter_measure=1,leave_measure=2,speed=3,height_offset=0,secondary_y=200,duration=640,page=0,
            limit=180,secondary=1,enabled=0,requested=1,cap=0,alive='none',vsync=1,adapt=1,
            blit_width=1,active=1,schedule=DEFAULT_SCHEDULE,ticks=(1,),clock_prefix=0,loop_prefix=0,
            particle0=None,box_seed=0xA55A,box_writes=(),flags=0x202,ss=0x7000,stack=0xF800,seed=0x1357,persistent=False):
        if self.faulted:
            old_memory = bytes(self.u.mem_read(0,1<<20)) if persistent else None
            covered,image,load = self.covered,self.image,self.load
            self.close()
            self.__init__(image,load)
            self.covered = covered
            if old_memory is not None:
                self.u.mem_write(0,old_memory)
        need(all(0<=v<=65535 for v in (slot,enter_measure,leave_measure,speed,height_offset,secondary_y,duration,limit,vsync,blit_width)),'WORD controller inputs')
        need(all(0<=v<=255 for v in (page,secondary,enabled,requested,cap,adapt,active)) and alive in ('none','all','mixed'),'raw BYTE state and particles')
        need(ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),'foreign stack and flags')
        need(schedule and all(0<=measure<=65535 and 0<=f<=65535 and all(0<=off<off+len(raw)<=65536 and isinstance(raw,bytes) for off,raw in writes) for measure,writes,f in schedule),'bounded PMD reply schedule')
        need(ticks is None or ticks and all(0<=v<=65535 for v in ticks),'bounded counter schedule')
        need(clock_prefix in (0,1,3,7) and (not clock_prefix or ticks is None and vsync==0),'native readonly clock prefix')
        if loop_prefix:
            need(loop_prefix in (1,3,7) and (slot,speed,height_offset,duration,page,limit,secondary,enabled,requested,cap,active,enter_measure)==(1,3,0,640,0,180,1,0,1,0,1,1)
                 and schedule==((0,(),0x8D5),) and ticks==(1,) and (vsync,adapt,alive,blit_width)==(1,1,'none',1)
                 and secondary_y==200 and particle0 is None and not clock_prefix and not persistent,'closed entrance-loop fixture assumptions')
        need(0<=box_seed<=65535 and all(0<=off<off+len(raw)<=65536 and isinstance(raw,bytes) for off,raw in box_writes),'bounded unowned bytebox reply')
        memory = bytearray(self.u.mem_read(0,1<<20) if persistent else self.initial)
        def put(off,value,size=2):
            at = address(self.ds,off&65535)
            memory[at:at+size] = value.to_bytes(size,'little')
        if not persistent:
            at = address(self.ds,SNOW['flakes'])
            memory[at:at+255*16] = particle_fixture(alive,2)
            for i in range(256):
                put(DATA['centers']+i*2,0)
            for i,v in enumerate(PATTERNS):
                put(DISSOLVE['pattern']+i*2,v)
            for index in (slot,(slot-1)&65535,secondary):
                first = (DISSOLVE['slots']+index*16)&65535
                for delta,value in ((0,0),(2,16),(4,1),(6,65535),(8,blit_width),(10,0),(12,0x5000),(14,0x6000)):
                    put(first+delta,value)
            for off,value in ((STAFF['speed'],speed),(DATA['height_offset'],height_offset),(STAFF['duration'],duration),
                              (STAFF['limit'],limit),(DATA['secondary_y'],secondary_y),(SNOW['vsync'],vsync),(SNOW['seed'],1)):
                put(off,value,4 if off==SNOW['seed'] else 2)
            for off,value in ((SNOW['cap'],cap),(SNOW['adapt'],adapt),(STAFF['page'],page),(STAFF['secondary'],secondary),
                              (STAFF['enabled'],enabled),(STAFF['requested'],requested),(SNOW['active'],active)):
                put(off,value,1)
        if particle0 is not None:
            on,left,top,vx,vy,cel = particle0
            need(0<=on<=255 and all(0<=v<=65535 for v in (left,top,vx,vy,cel)),'explicit raw first particle')
            put(SNOW['flakes'],on,1)
            for off,value in zip((2,4,6,8,10),(left,top,vx,vy,cel)):
                put(SNOW['flakes']+off,value)
        at = address(ss,stack)
        memory[at:at+8] = struct.pack('<4H',0xFFFF,leave_measure,enter_measure,slot)
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
        self.o = dict(load=self.load,stack=stack,schedule=schedule,ticks=ticks,prefix=clock_prefix,loop_prefix=loop_prefix,
                      kind='enter',box_seed=box_seed,box_writes=box_writes)
        spec = Spec(memory,regs,high,flags,self.o)
        expected,final,mask,ending = spec.run()
        self.events,self.index,self.error,self.returned,self.faulted,self.max_depth,self.far_word_hooks = spec.events,0,None,False,False,0,0
        self.clear_progress,self.actual_clear_stores,self.gate_index,self.tick_index,self.polls = 0,0,0,0,0
        self.phase_counts,self.prefix_stopped = [0,0],False
        try:
            self.u.emu_start(self.cs*16+START,1<<20,count=100000000)
        except UcError as error:
            raise ValueError('MAINL staff pair contract: guest fault') from error
        need(self.error is None,self.error or 'guest failure')
        need(self.index==len(self.events) and (self.faulted if ending=='divide-fault' else self.prefix_stopped if ending.endswith('prefix') else self.returned),'complete actual return / native fault / proved prefix, never budget expiry')
        need(self.regs(True)==expected,'all DWORD/segment effects '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(mask|0x600)==final&(mask|0x600),'defined flags and IF/DF')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'whole physical memory, persistent state, native frames and SMC')
        return dict(ending=ending,registers=expected,flags=final&(mask|0x600),flag_mask=mask|0x600,
            phase_iterations=spec.iterations,gates=spec.gates,ticks=spec.ticks,actual_clear_WORD_callbacks=self.actual_clear_stores,
            stack_depth=self.max_depth,events=len(self.events),trace_sha256=hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest())


def geometry_proof(image):
    from lib.decoded_mainl_staff_single_runtime import geometry_proof as previous_proof
    p = previous_proof(image)
    for at,raw in ((0x2AE6,bytes.fromhex('c706c227000056e814fd')),
                   (0x2B11,bytes.fromhex('ff7606680001e89bfb0bc074ce')),
                   (0x2B1E,bytes.fromhex('c706c2270000813ec227a1007f0e')),
                   (0x2BB0,bytes.fromhex('ff7604680001e8fcfa0bc00f8465ff')),
                   (0x2B46,bytes.fromhex('a1c22748bb140099f7fb8bf883ff077e03bf0700')),
                   (0x2B5A,bytes.fromhex('803ec427007504ff0ed227c606d72701813ec227a000'))):
        need(image.program_image[CS*16+at:CS*16+at+len(raw)]==raw,'native pair loops, WORD wrap, signed clamp and live alpha/page sequencing')
    quotients,clamped = [],[]
    for frame in range(65536):
        if signed(frame)<=161:
            value = signed((frame-1)&65535)
            q = (abs(value)//20)*(-1 if value<0 else 1)
            quotients.append(q)
            if q>7:
                clamped.append(frame)
    need(clamped==[161,32768] and (min(quotients),max(quotients))==(-1638,1638),'entire WORD frame domain; pair clamp is reachable at161 and8000')
    p.update(enter_loop_head=0x2AEC,enter_loop_tail=0x2B1C,leave_loop_head=0x2B24,leave_loop_tail=0x2BBB,
        pair_clamp_frame_WORDs=clamped,pair_IDIV_quotient_range=[min(quotients),max(quotients)],pair_strength_range=[min(quotients),7],
        secondary_y_entrance_invariant=200,secondary_slot_entrance_invariant=0,
        conditional_enter_loop_invariant=p['conditional_enter_loop_invariant']+'; secondary_y200; slot0 metadata valid readonly; alpha1 only during explicit draw')
    p['conditional_enter_loop_assumptions'][2] = 'slots0/1, width16/height1, blit width1, secondary1, requested1; secondary_y200 unchanged during entrance; all nested native calls return'
    return p


def exit_schedule(frame):
    # Finish entrance, then require one more live leave iteration at this WORD.
    return (*DEFAULT_SCHEDULE,(0,((STAFF['frame'],struct.pack('<H',frame)),),0x8D5),*DEFAULT_SCHEDULE)


def cases():
    for field,shift,value in itertools.product(('enter_measure','leave_measure'),(0,8),range(256)):
        yield {field:value<<shift}
    for field,shift,value in itertools.product(('height_offset','speed'),(0,8),range(256)):
        yield dict(secondary=0,requested=0,enabled=0,blit_width=0,**{field:value<<shift})
    for shift,value in itertools.product((0,8),range(256)):
        yield dict(slot=value<<shift,secondary=0,requested=0,enabled=0,blit_width=0)
    for speed,page in itertools.product((2,3),range(256)):
        yield dict(speed=speed,page=page)
    for active in range(256):
        yield dict(active=active)
    # Unchecked particle rows alias staff globals. Keep every capacity live,
    # with zero graphics width so mutated geometry remains within the flat
    # drawing interface; other lanes exercise actual normal blitters.
    for cap in range(256):
        yield dict(cap=cap,secondary=0,requested=0,enabled=0,blit_width=0)
    for field,value in itertools.product(('enabled','requested','secondary'),range(256)):
        yield {field:value}
    for shift,value in itertools.product((0,8),range(256)):
        yield dict(duration=value<<shift)
    for flags,ss,stack in itertools.product((2,0x202,0x402,0xED7),(0x7000,0x8000),(0x80,0xF800)):
        yield dict(flags=flags,ss=ss,stack=stack,cap=2)
        yield dict(flags=flags,ss=ss,stack=stack,duration=0)
        for prefix in (1,3,7):
            yield dict(flags=flags,ss=ss,stack=stack,clock_prefix=prefix,ticks=None,vsync=0)
            yield dict(flags=flags,ss=ss,stack=stack,loop_prefix=prefix,schedule=((0,(),0x8D5),))
    for duration in (*range(-7,8),*range(-15,-7)):
        yield dict(schedule=((0,((STAFF['frame'],b'\0\x80'),(STAFF['duration'],struct.pack('<H',duration&65535))),0x8D5),))
    for frame,duration in ((8,8),(641,640),(192,640)):
        yield dict(cap=2 if frame==8 else 0,schedule=((0,((STAFF['frame'],struct.pack('<H',frame)),(STAFF['duration'],struct.pack('<H',duration))),0x8D5),*DEFAULT_SCHEDULE))
    yield dict(schedule=((0xFFFF,((STAFF['frame'],b'\xC0\0'),),0x8D5),*DEFAULT_SCHEDULE))
    for cap,alive in itertools.product((1,2,80,81,255),('all','mixed')):
        yield dict(cap=cap,alive=alive,vsync=2)
    yield dict(active=0,speed=2)
    yield dict(ticks=(0,0,1),cap=1)
    yield dict(cap=1,particle0=(2,1,6271,65535,1,3))
    for shift,value in itertools.product((0,8),range(256)):
        yield dict(secondary_y=value<<shift,secondary=0,requested=0,enabled=0,blit_width=0)
        yield dict(schedule=exit_schedule(value<<shift),secondary=0,requested=0,enabled=0,blit_width=0)
    for flags,ss,stack,frame in itertools.product((2,0x202,0x402,0xED7),(0x7000,0x8000),(0x80,0xF800),(161,0x8000)):
        yield dict(flags=flags,ss=ss,stack=stack,schedule=exit_schedule(frame))
    for frame in (0,162,0x8000):
        yield dict(schedule=exit_schedule(160),box_writes=((DATA['frame'],struct.pack('<H',frame)),))
    for page in (0,255):
        yield dict(schedule=exit_schedule(161),box_writes=((DATA['page'],bytes([page])),))
    yield dict(schedule=exit_schedule(160),box_writes=((DATA['frame'],b'\xA2\0'),(DATA['enabled'],b'\x07')))


def verify(target,candidate):
    proof = geometry_proof(target)
    need(proof==geometry_proof(candidate),'both complete native CFG/invariant proofs')
    observations = []
    context = {b for a,(_,n) in CONTEXT.items() for b in range(a,a+n)}
    for image_index,image in enumerate((target,candidate),1):
        rows = []
        for load in (0x1000,0x3000):
            m = Machine(image,load)
            trace,counts,peak,max_phase,max_ticks,max_clear = hashlib.sha256(),{k:0 for k in ('return','divide-fault','clock-prefix','enter-prefix')},0,[0,0],0,0
            try:
                def entry(parameters):
                    nonlocal peak,max_ticks,max_clear
                    result = m.run(**parameters)
                    counts[result['ending']] += 1
                    peak = max(peak,result['stack_depth'])
                    max_ticks = max(max_ticks,result['ticks'])
                    max_clear = max(max_clear,result['actual_clear_WORD_callbacks'])
                    for i in (0,1):
                        max_phase[i] = max(max_phase[i],result['phase_iterations'][i])
                    trace.update(json.dumps(result,sort_keys=True).encode())
                for count,parameters in enumerate(cases(),1):
                    try:
                        entry(dict(seed=0x1357 if count&1 else 0xECA8,**parameters))
                    except Exception:
                        print('Staff pair failing case',image_index,load,count,parameters,flush=True)
                        raise
                    if count%256==0:
                        print(f'Staff pair: image {image_index}, load {load:04X}, {count} complete entries / proved prefixes',flush=True)
                for i in range(3):
                    entry(dict(persistent=i>0,cap=2))
                    count += 1
                if not m.owner<=m.covered or context-m.covered!=set(range(CS*16+0x2925,CS*16+0x2928)):
                    print('Missing owner/context instruction bytes',sorted(m.owner-m.covered),sorted(context-m.covered),flush=True)
                need(m.owner<=m.covered and context-m.covered==set(range(CS*16+0x2925,CS*16+0x2928)),'all358 owner bytes and1688 reachable context bytes execute; three leave-clamp bytes proved unreachable')
                rows.append(dict(load_segment=load,cases=count,endings=counts,executed_owner_bytes=358,actual_context_bytes=1688,
                    maximum_stack_depth=peak,maximum_phase_iterations=max_phase,maximum_ticks=max_ticks,
                    maximum_actual_clear_WORD_callbacks=max_clear,trace_sha256=trace.hexdigest()))
                print(f'Staff pair: image {image_index}, load {load:04X}, {count} entries / all358 bytes pass',flush=True)
            finally:
                m.close()
        observations.append(rows)
    need(observations[0]==observations[1],'independent full target/candidate observations')
    return dict(images=2,functions=1,code_bytes=358,cases_per_image=sum(o['cases'] for o in observations[0]),
        observations=observations[0],executed_owner_bytes=358,actual_context_bytes=1688,unowned_vector_context_bytes=69,
        ignored_stack_bytes=0,proved_unreachable_context_bytes=3,
        capacity_lane_fixture=dict(capacity_range=[0,255],secondary=0,requested=0,enabled=0,blit_width=0,capacity_clamped=False),native_geometry_proof=proof,immediate_owned_return_checks=True,
        guest_iterations_skipped=False,physical_driver_IRQ_assets_or_vector_library_proved=False)


def negative_controls(target):
    quiet = dict(secondary=0,requested=0,enabled=0,blit_width=0)
    enter_prefix = dict(loop_prefix=3,schedule=((0,(),0x8D5),))
    f161,f8000,f162 = [dict(schedule=exit_schedule(f)) for f in (161,0x8000,162)]
    controls = (
        ('saved-frame',0x2AA7,1,{}),('saved-slot',0x2AAE,2,{}),('speed-two',0x2AB3,1,{}),
        ('speed-branch',0x2AB5,1,{}),('raw-page-zero-extension',0x2ABA,1,dict(speed=2,page=255)),
        ('center264',0x2AC3,1,dict(speed=2)),('speed2-page-XOR1',0x2ACB,1,dict(speed=2,page=255)),
        ('center263',0x2AD5,1,dict(speed=2)),('height-subtract',0x2ADC,0x28,dict(quiet,height_offset=17)),
        ('default-second-fixed-center',0x2AE4,2,{}),('enter-frame-zero',0x2AEA,1,{}),
        ('selected-slot-push',0x2AEC,1,{}),('actual-enter-call',0x2AEE,1,{}),
        ('entrance-alpha-one',0x2AF4,1,{}),('entrance-left320',0x2AF6,1,{}),
        ('entrance-secondary-Y',0x2AFA,1,{}),('entrance-slot-minus-one',0x2AFE,1,{}),
        ('entrance-strength-zero',0x2B01,1,{}),('entrance-actual-dissolve',0x2B03,1,{}),
        ('entrance-alpha-zero',0x2B09,1,{}),('first-tick',0x2B0B,1,{}),
        ('enter-frame-INC',0x2B0F,2,{}),('enter-measure',0x2B13,2,{}),
        ('enter-256-argument',0x2B16,1,{}),('enter-gate',0x2B18,1,{}),
        ('enter-gate-result',0x2B1B,8,{}),('enter-backedge',0x2B1D,1,enter_prefix),
        ('leave-frame-zero',0x2B22,1,{}),('pre-leave161-bound',0x2B28,1,f161),
        ('pre-leave-skip',0x2B2B,1,f162),('unput-left320',0x2B2D,1,{}),
        ('unput-secondary-Y',0x2B31,1,{}),('unput-slot-minus-one',0x2B35,1,{}),
        ('actual-unput-call',0x2B38,1,{}),('actual-leave-call',0x2B3C,1,{}),
        ('post-leave-live161-bound',0x2B42,1,f161),('post-leave-skip',0x2B45,1,f162),
        ('live-frame-reload',0x2B47,2,f8000),('WORD-DEC-wrap',0x2B49,1,f8000),
        ('signed-divisor20',0x2B4B,1,f161),('CWD-before-IDIV',0x2B4D,8,f8000),
        ('IDIV-BX',0x2B4F,1,f8000),('strength-to-DI',0x2B51,8,{}),
        ('strength-bound7',0x2B54,15,f161),('strength-clamp-branch',0x2B56,1,{}),
        ('reachable-MOV-DI7',0x2B58,1,f161),('page-zero-predicate',0x2B5E,1,{}),
        ('page-branch',0x2B60,1,{}),('secondary-Y-decrement',0x2B63,1,f161),
        ('leave-alpha-one',0x2B69,1,{}),('draw-below160-bound',0x2B6E,1,dict(schedule=exit_schedule(160))),
        ('draw-or-box-branch',0x2B71,1,f161),('leave-slot-minus-one',0x2B7B,1,{}),
        ('leave-strength-argument',0x2B7D,1,{}),('leave-actual-dissolve',0x2B7F,1,{}),
        ('inner-color-mode',0x2B87,1,f161),('inner-color-call',0x2B8A,1,f161),
        ('inner-box-geometry',0x2B90,1,f161),('inner-box-call',0x2B9B,1,f161),
        ('inner-off-call',0x2BA0,1,f161),('leave-alpha-zero',0x2BA8,1,{}),
        ('second-tick',0x2BAA,1,{}),('leave-frame-INC',0x2BAE,2,{}),
        ('leave-measure',0x2BB2,2,{}),('leave-256-argument',0x2BB5,1,{}),
        ('leave-gate',0x2BB7,1,{}),('leave-gate-result',0x2BBA,8,{}),('near-leave-backedge',0x2BBD,1,f161),
        ('first-final-color-mode',0x2BC3,1,{}),('first-final-color-call',0x2BC6,1,{}),
        ('first-final-box-geometry',0x2BCC,1,{}),('first-final-box-call',0x2BD7,1,{}),
        ('first-final-off-call',0x2BDC,1,{}),('first-final-tick',0x2BE1,1,{}),
        ('second-final-color-mode',0x2BE7,1,{}),('second-final-color-call',0x2BEA,1,{}),
        ('second-final-box-geometry',0x2BF6,1,{}),('second-final-box-call',0x2BFB,1,{}),
        ('second-final-off-call',0x2C00,1,{}),('second-final-tick',0x2C05,1,{}),
        ('restore-DI',0x2C07,1,{}),('restore-SI',0x2C08,1,{}),('Pascal-pop6',0x2C0B,1,{}))
    context = (('actual-enter-clamp',CS*16+0x2890,1,{}),('actual-leave-center',CS*16+0x290F,2,{}),
               ('actual-tick-page',CS*16+0x2724,2,{}),('actual-gate-minimum192',CS*16+0x26D6,1,{}),
               ('actual-RNG-multiplier',0x1A3F,1,dict(cap=1)),
               ('actual-vector-signed-EDX',0xC7E*16+0x126,8,dict(cap=1)))
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
            raise ValueError('MAINL staff pair actual instruction mutation escaped: '+name)
        finally:
            if m:
                m.close()
    return dict(count=len(rejected),rejected=rejected,owner_instruction_mutations=len(controls),
        actual_context_instruction_mutations=len(context),actual_guest_instruction_mutations=True,
        unowned_DATA_or_unreachable_mutations_counted=False)
