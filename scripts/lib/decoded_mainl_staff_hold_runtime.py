"""Stateful hold loops with actual staff, snow, RNG/vector and blitter code.

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
from lib.decoded_mainl_staff_hold_layout import CS, DS, START, SIZE, DATA
from lib.decoded_mainl_staff_callers_runtime import Machine as CallerMachine, Spec as CallerSpec, ClearSpec, CONTEXT as CALLER_CONTEXT
from lib.decoded_mainl_staff_callers_layout import DATA as STAFF
from lib.decoded_mainl_snow_runtime import Spec as SnowSpec, CONTEXT as SNOW_CONTEXT, particle_fixture
from lib.decoded_mainl_snow_layout import ENTRIES as SNOW_ENTRIES, DATA as SNOW
from lib.decoded_mainl_dissolve_layout import DATA as DISSOLVE
from lib.decoded_mainl_dissolve_runtime import PATTERNS
from lib.decoded_mainl_pi_runtime import ARITH, signed
from lib.decoded_mainl_pi_free_runtime import address
from lib.decoded_mainl_root_helpers_runtime import GPRS, REG

NODES = {'enter':(CS,0x2804,211,4),**{k:(CS,*SNOW_ENTRIES[k][:2],SNOW_ENTRIES[k][2]+2)
         for k in ('spawn','update','render','tick','gate')},**SNOW_CONTEXT}
ENTRY_AT = {s*16+a:(kind,n,frame) for kind,(s,a,n,frame) in NODES.items()}
CONTEXT = {a:v for a,v in CALLER_CONTEXT.items() if v[0]!='off'}
CONTEXT.update({s*16+a:(kind,n) for kind,(s,a,n,_) in NODES.items()})
RETURNS = {0x2C53:'enter',0x2C56:'tick',0x2C63:'gate',0x2C70:'clear',0x2C73:'tick',0x2C80:'gate'}
RETURN_AT = {CS*16+a:k for a,k in RETURNS.items()}
DEFAULT_SCHEDULE = ((0xFFFF,((STAFF['frame'],b'\xC1\0'),),0x8D5),)


def need(value,message):
    if not value:
        raise ValueError('MAINL staff hold contract: '+str(message))


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
        options = dict(self.o,kind='enter')
        if kind=='enter':
            self.entry('enter',4)
            child = CallerSpec(self.memory,self.r,self.high,self.flags,options)
            _,_,mask,fault = child.run('enter')
            if fault:
                self.stopped = 'divide-fault'
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

    def run(self):
        self.enter()
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
                    self.events.append(('hold-prefix',self.iterations[0],self.full(),self.flags&(self.mask|0x600),self.mask|0x600))
                    self.stopped = 'enter-prefix'
                    return self.full(),self.flags,self.mask,self.stopped
                if phase==0:
                    self.push(self.word(self.ss,self.r['bp']+8))
                    self.call('enter',0x2C53)
                else:
                    self.call('clear',0x2C70)
                if self.stopped:
                    return self.full(),self.flags,self.mask,self.stopped
                self.call('tick',0x2C56 if phase==0 else 0x2C73)
                if self.stopped:
                    return self.full(),self.flags,self.mask,self.stopped
                carry = self.flags&1
                self.field(DATA['frame'],self.op(self.dg(DATA['frame']),1))
                self.flags = (self.flags&~1)|carry
                self.push(self.word(self.ss,self.r['bp']+(6 if phase==0 else 4)))
                self.push(256)
                self.call('gate',0x2C63 if phase==0 else 0x2C80)
                self.logical(self.r['ax'])
                self.iterations[phase] += 1
                if self.r['ax']:
                    break
                need(sum(self.iterations)<600,'bounded complete fixture or explicitly proved prefix; not a program bound')
        at = self.page()
        self.r['ax'] = self.dg(at)
        self.field(DATA['secondary_y'],self.r['ax'])
        self.pop('bp')
        self.r['sp'] += 8
        return self.full(),self.flags,ARITH,'return'


class Machine(CallerMachine):
    def __init__(self,image,load):
        super().__init__(image,load)
        self.instructions,self.samples,self.seen,self.owner = {},set(),set(),set(range(CS*16+START,CS*16+START+SIZE))
        for start,size in [(CS*16+START,SIZE),*[(a,n) for a,(_,n) in CONTEXT.items()]]:
            ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[start:start+size],start))
            need(sum(i.size for i in ins)==size,'complete hold and actual context instruction boundaries')
            self.instructions.update({i.address:i.size for i in ins})
            self.samples.add(start)
            self.samples.update(i.address+i.size for i in ins if i.mnemonic in ('push','pushf','enter'))
        from lib.decoded_mainl_staff_callers_runtime import OWNED_RETURN_AT
        self.samples.update(OWNED_RETURN_AT)
        self.samples.update(RETURN_AT)

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
            if offset==CS*16+0x2C4D and self.o['loop_prefix'] and self.phase_counts[0]==self.o['loop_prefix']:
                mask = self.events[self.index][-1]
                self.event(('hold-prefix',self.phase_counts[0],self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
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
            if offset in RETURN_AT:
                expected = self.events[self.index]
                need(expected[:2]==('owned-return',RETURN_AT[offset]),'actual immediate owned return in hold')
                mask = expected[-1]
                self.event(('owned-return',expected[1],self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                if offset==CS*16+0x2C63:
                    self.phase_counts[0] += 1
                elif offset==CS*16+0x2C80:
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

    def run(self,*,slot=1,enter_measure=1,hold_measure=2,speed=3,height_offset=0,duration=640,page=0,
            limit=180,secondary=1,enabled=0,requested=1,cap=0,alive='none',vsync=1,adapt=1,
            blit_width=1,active=1,schedule=DEFAULT_SCHEDULE,ticks=(1,),clock_prefix=0,loop_prefix=0,
            particle0=None,flags=0x202,ss=0x7000,stack=0xF800,seed=0x1357,persistent=False):
        if self.faulted:
            old_memory = bytes(self.u.mem_read(0,1<<20)) if persistent else None
            covered,image,load = self.covered,self.image,self.load
            self.close()
            self.__init__(image,load)
            self.covered = covered
            if old_memory is not None:
                self.u.mem_write(0,old_memory)
        need(all(0<=v<=65535 for v in (slot,enter_measure,hold_measure,speed,height_offset,duration,limit,vsync,blit_width)),'WORD controller inputs')
        need(all(0<=v<=255 for v in (page,secondary,enabled,requested,cap,adapt,active)) and alive in ('none','all','mixed'),'raw BYTE state and particles')
        need(ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),'foreign stack and flags')
        need(schedule and all(0<=measure<=65535 and 0<=f<=65535 and all(0<=off<off+len(raw)<=65536 and isinstance(raw,bytes) for off,raw in writes) for measure,writes,f in schedule),'bounded PMD reply schedule')
        need(ticks is None or ticks and all(0<=v<=65535 for v in ticks),'bounded counter schedule')
        need(clock_prefix in (0,1,3,7) and (not clock_prefix or ticks is None and vsync==0),'native readonly clock prefix')
        if loop_prefix:
            need(loop_prefix in (1,3,7) and (slot,speed,height_offset,duration,page,limit,secondary,enabled,requested,cap,active,enter_measure)==(1,3,0,640,0,180,1,0,1,0,1,1)
                 and schedule==((0,(),0x8D5),) and ticks==(1,) and (vsync,adapt,alive,blit_width)==(1,1,'none',1)
                 and particle0 is None and not clock_prefix and not persistent,'closed entrance-loop fixture assumptions')
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
            for index in (slot,secondary):
                first = (DISSOLVE['slots']+index*16)&65535
                for delta,value in ((0,0),(2,16),(4,1),(6,65535),(8,blit_width),(10,0),(12,0x5000),(14,0x6000)):
                    put(first+delta,value)
            for off,value in ((STAFF['speed'],speed),(DATA['height_offset'],height_offset),(STAFF['duration'],duration),
                              (STAFF['limit'],limit),(DATA['secondary_y'],200),(SNOW['vsync'],vsync),(SNOW['seed'],1)):
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
        memory[at:at+8] = struct.pack('<4H',0xFFFF,hold_measure,enter_measure,slot)
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
                      kind='enter',box_seed=0xA55A,box_writes=())
        spec = Spec(memory,regs,high,flags,self.o)
        expected,final,mask,ending = spec.run()
        self.events,self.index,self.error,self.returned,self.faulted,self.max_depth,self.far_word_hooks = spec.events,0,None,False,False,0,0
        self.clear_progress,self.actual_clear_stores,self.gate_index,self.tick_index,self.polls = 0,0,0,0,0
        self.phase_counts,self.prefix_stopped = [0,0],False
        try:
            self.u.emu_start(self.cs*16+START,1<<20,count=100000000)
        except UcError as error:
            raise ValueError('MAINL staff hold contract: guest fault') from error
        need(self.error is None,self.error or 'guest failure')
        need(self.index==len(self.events) and (self.faulted if ending=='divide-fault' else self.prefix_stopped if ending.endswith('prefix') else self.returned),'complete actual return / native fault / proved prefix, never budget expiry')
        need(self.regs(True)==expected,'all DWORD/segment effects '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(mask|0x600)==final&(mask|0x600),'defined flags and IF/DF')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'whole physical memory, persistent state, native frames and SMC')
        return dict(ending=ending,registers=expected,flags=final&(mask|0x600),flag_mask=mask|0x600,
            phase_iterations=spec.iterations,gates=spec.gates,ticks=spec.ticks,actual_clear_WORD_callbacks=self.actual_clear_stores,
            stack_depth=self.max_depth,events=len(self.events),trace_sha256=hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest())


def geometry_proof(image):
    for at,raw in ((0x2C47,b'\xC7\x06\xC2\x27\0\0\xFF\x76\x08\xE8\xB1\xFB\xE8\x8F\xFA\xFF\x06\xC2\x27\xFF\x76\x06\x68\0\x01\xE8\x52\xFA\x0B\xC0\x74\xE6'),
        (0x2C67,b'\xC7\x06\xC2\x27\0\0\xE8\xF1\xF8\xE8\x72\xFA\xFF\x06\xC2\x27\xFF\x76\x04\x68\0\x01\xE8\x35\xFA\x0B\xC0\x74\xE9'),
        (0x26B5,b'\x55\x8B\xEC\x80\x3E\x80\x08\0'),
        (0x26C9,b'\xB4\x05\xCD\x60\x3B\x46\x06\x72'),
        (0x270E,b'\x83\x3E\x4E\x14\0\x74\xF9')):
        need(image.program_image[CS*16+at:CS*16+at+len(raw)]==raw,'native two-stage CFG, gate and readonly clock edges')
    for frame in range(65536):
        value = signed(frame)
        if value<=640:
            q = (abs(value)//80)*(-1 if value<0 else 1)
            need(-409<=q<=8 and -1<=7-q<=416,'entire WORD frame domain has safe entrance IDIV and bounded strength')
    need(all(180<=max(180,y-3)<=280 for y in range(180,281)),'both positive center coordinates remain invariant')
    return dict(normal_no_music_phase_iterations=257,normal_no_music_total_ticks=514,
        enter_loop_head=0x2C4D,enter_loop_tail=0x2C65,hold_loop_head=0x2C6D,hold_loop_tail=0x2C82,
        conditional_enter_loop_invariant='frame is any WORD; page in{0,1}; centers in[180,280]; cap0; duration640; speed3; valid readonly slot metadata',
        conditional_enter_loop_assumptions=['active music stays nonzero; PMD always returns0 below enter_measure1 without DATA writes',
            'counter replies1 make every tick return; disjoint mapped CODE/DGROUP/stack/VRAM; no other external writes',
            'slot1, width16/height1, blit width1, secondary1, requested1; all nested native calls return'],
        conditional_enter_loop_nontermination_proved=True,readonly_zero_clock_loop_proved=True,
        loop_prefixes_are_not_terminal_calls=True,guest_iterations_skipped=False,budget_expiry_used=False,
        physical_driver_IRQ_assets_or_timing_proved=False)


def cases():
    for field,shift,value in itertools.product(('enter_measure','hold_measure'),(0,8),range(256)):
        yield {field:value<<shift}
    for field,shift,value in itertools.product(('height_offset','speed'),(0,8),range(256)):
        yield dict(secondary=0,requested=0,enabled=0,blit_width=0,**{field:value<<shift})
    for shift,value in itertools.product((0,8),range(256)):
        yield dict(slot=value<<shift,secondary=0,requested=0,enabled=0,blit_width=0)
    for speed,page in itertools.product((2,3),range(256)):
        yield dict(speed=speed,page=page)
    for active in range(256):
        yield dict(active=active)
    for cap in range(256):
        yield dict(cap=cap)
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
                        print('Staff hold failing case',image_index,load,count,parameters,flush=True)
                        raise
                    if count%256==0:
                        print(f'Staff hold: image {image_index}, load {load:04X}, {count} complete entries / proved prefixes',flush=True)
                for i in range(3):
                    entry(dict(persistent=i>0,cap=2))
                    count += 1
                if not m.owner<=m.covered or not context<=m.covered:
                    print('Missing owner/context instruction bytes',sorted(m.owner-m.covered),sorted(context-m.covered),flush=True)
                need(m.owner<=m.covered and context<=m.covered,'all139 owner bytes and1503 actual context bytes execute')
                rows.append(dict(load_segment=load,cases=count,endings=counts,executed_owner_bytes=139,actual_context_bytes=1503,
                    maximum_stack_depth=peak,maximum_phase_iterations=max_phase,maximum_ticks=max_ticks,
                    maximum_actual_clear_WORD_callbacks=max_clear,trace_sha256=trace.hexdigest()))
                print(f'Staff hold: image {image_index}, load {load:04X}, {count} entries / all139 bytes pass',flush=True)
            finally:
                m.close()
        observations.append(rows)
    need(observations[0]==observations[1],'independent full target/candidate observations')
    return dict(images=2,functions=1,code_bytes=139,cases_per_image=sum(o['cases'] for o in observations[0]),
        observations=observations[0],executed_owner_bytes=139,actual_context_bytes=1503,unowned_vector_context_bytes=69,
        ignored_stack_bytes=0,native_geometry_proof=proof,immediate_owned_return_checks=True,
        guest_iterations_skipped=False,physical_driver_IRQ_assets_or_vector_library_proved=False)


def negative_controls(target):
    quiet = dict(secondary=0,requested=0,enabled=0,blit_width=0)
    loop = dict(loop_prefix=3,schedule=((0,(),0x8D5),))
    two_hold = dict(schedule=(*DEFAULT_SCHEDULE,(0,((STAFF['frame'],b'\xC1\0'),),0x8D5),*DEFAULT_SCHEDULE))
    controls = (
        ('frame',0x2C0D,1,{}),('speed-two',0x2C14,1,{}),('speed-branch',0x2C15,1,{}),
        ('page-zero-extension',0x2C1B,1,dict(speed=2,page=255)),('first-center-slot',0x2C22,2,dict(speed=2)),
        ('first-center264',0x2C24,1,dict(speed=2)),('other-page-XOR1',0x2C2C,1,dict(speed=2)),
        ('second-center263',0x2C36,1,dict(speed=2)),('height-subtract',0x2C3D,0x28,dict(quiet,height_offset=17)),
        ('both-default-centers',0x2C45,2,{}),('entrance-frame-zero',0x2C4B,1,{}),
        ('slot-argument',0x2C4F,2,{}),('actual-enter-call',0x2C51,1,{}),('actual-first-tick',0x2C54,1,{}),
        ('first-frame-INC-field',0x2C58,2,{}),('enter-measure-argument',0x2C5C,2,{}),
        ('first-256-frame-argument',0x2C5F,1,{}),('actual-first-gate',0x2C61,1,{}),
        ('first-gate-result-register',0x2C64,8,{}),('entrance-backedge',0x2C66,1,loop),
        ('hold-frame-zero',0x2C6B,1,{}),('actual-clear-call',0x2C6E,1,{}),('actual-second-tick',0x2C71,1,{}),
        ('hold-measure-argument',0x2C79,2,{}),('second-256-frame-argument',0x2C7C,1,{}),
        ('actual-second-gate',0x2C7E,1,{}),('second-gate-result-register',0x2C81,8,{}),
        ('hold-backedge',0x2C83,1,two_hold),('final-page-zero-extension',0x2C88,1,{}),
        ('final-live-center',0x2C8F,2,{}),('secondary-Y-store',0x2C93,2,{}),
        ('saved-BP',0x2C94,1,{}),('Pascal-pop6',0x2C96,1,{}))
    context = (('actual-enter-clamp',CS*16+0x2890,1,{}),('actual-tick-page',CS*16+0x2724,2,{}),
               ('actual-gate-minimum192',CS*16+0x26D6,1,{}),('actual-RNG-multiplier',0x1A3F,1,dict(cap=1)),
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
            raise ValueError('MAINL staff hold actual instruction mutation escaped: '+name)
        finally:
            if m:
                m.close()
    return dict(count=len(rejected),rejected=rejected,owner_instruction_mutations=len(controls),
        actual_context_instruction_mutations=len(context),actual_guest_instruction_mutations=True,
        unowned_DATA_mutations_counted=False)
