"""Actual verdict code with explicit far text-renderer replies, not renderer credit."""
import hashlib
import itertools
import json
import struct
from dataclasses import replace
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import UcError,UC_HOOK_INTR,UC_HOOK_INSN
from unicorn.x86_const import *
from lib.decoded_mainl_staff_verdict_layout import CS,DS,START,SIZE,DATA,RENDER,CALLS
from lib.decoded_mainl_snow_runtime import Spec as State
from lib.decoded_mainl_pi_free_runtime import Machine as Physical,address
from lib.decoded_mainl_pi_runtime import ARITH,signed
from lib.decoded_mainl_root_helpers_runtime import GPRS,REG,logical

RETURNS=tuple(at+5 for at in CALLS)
DEFAULT_SCORE=(2,8,7,6,5,4,3,2,1)
TABLE_START,TABLE_END=DATA['playchars'],DATA['numbers']+256*4


def need(value,message):
    if not value:
        raise ValueError('MAINL verdict contract: '+str(message))


def renderer_reply(seed,index):
    value=(seed+index*0x01020304)&0xFFFFFFFF
    return dict(ax=value,bx=value^0x11223344,cx=value^0x55667788,dx=value^0x99AABBCC,
                es=((value>>16)^0x5AA5)&65535)


def reply_flags(options,index):
    schedule=options['flag_schedule']
    return schedule[min(index-1,len(schedule)-1)] if schedule else options['reply_flags']


class Spec(State):
    def __init__(self,*args):
        super().__init__(*args)
        self.render_count=0
        self.rendered=[]
        self.loop_iterations=0

    def shift(self,value,count):
        result=(value<<count)&65535
        self.flags=(self.flags&0x600)|2|logical(result,16)|((value>>(16-count))&1)
        # For count>1, OF and AF are undefined; CF/PF/ZF/SF are defined.
        self.mask=0xC5
        return result

    def local(self,delta,value=None):
        offset=(self.r['bp']+delta)&65535
        if value is None:
            return self.word(self.ss,offset)
        self.store(address(self.ss,offset),2,value)

    def pointer(self,table,index_register):
        if index_register=='ax':
            self.r['ax']=self.shift(self.r['ax'],2)
            self.r['bx']=self.r['ax']
        else:
            self.r['bx']=self.r[index_register]
            self.r['bx']=self.shift(self.r['bx'],2)
        at=address(self.ds,(DATA[table]+self.r['bx'])&65535)
        value=int.from_bytes(self.memory[at:at+4],'little')
        self.push(value,4)

    def render(self,continuation):
        self.frame(continuation)
        self.r['cs']=self.o['load']+RENDER[0]
        at=address(self.ss,self.r['sp'])
        frame=bytes(self.memory[at:at+14])
        mask=self.mask|0x600
        self.render_count+=1
        self.events.append(('render-entry',self.render_count,self.full(),frame.hex(),self.flags&mask,mask))
        ip,cs,off,seg,fx,y,x=struct.unpack('<7H',frame)
        self.rendered.append(dict(x=x,y=y,fx=fx,pointer=[seg,off],continuation=ip))
        for index,offset,raw in self.o['writes']:
            if index==self.render_count:
                dest=address(self.ds,offset)
                self.events.append(('renderer-write',dest,raw.hex()))
                self.memory[dest:dest+len(raw)]=raw
        reply=renderer_reply(self.o['reply_seed'],self.render_count)
        for name in ('ax','bx','cx','dx'):
            self.full32(name,reply[name])
        self.r['es']=reply['es']
        self.flags=2|(reply_flags(self.o,self.render_count)&(ARITH|0x600))
        self.mask=ARITH
        self.returned(10)
        self.events.append(('renderer-return',self.full(),self.flags&(ARITH|0x600),ARITH|0x600))

    def number(self,continuation):
        self.pointer('numbers','di')
        self.render(continuation)

    def divide(self,divisor):
        self.r['bx']=divisor
        value=signed(self.r['ax'])
        self.r['dx']=65535 if value<0 else 0
        q=(abs(value)//divisor)*(-1 if value<0 else 1)
        self.r['ax'],self.r['dx']=q&65535,(value-q*divisor)&65535
        self.mask=0

    def run(self):
        self.enter(4)
        self.push(self.r['si'])
        self.push(self.r['di'])
        for field,table,packed,continuation in (('playchar','playchars',0x16000AE,0x2CBA),('rank','ranks',0x16800C7,0x2CD6)):
            self.push(packed,4)
            self.push(0x2F)
            self.r['ax']=self.dg(DATA[field],1)
            self.pointer(table,'ax')
            self.render(continuation)
        self.r['si']=408
        self.local(-4,0)
        self.local(-2,8)
        while True:
            digits=self.local(-2)
            self.op(digits,0,True)
            if signed(digits)<=0:
                break
            self.r['bx']=digits
            self.r['ax']=self.dg((DATA['score']+digits)&65535,1)
            self.r['di']=self.r['ax']
            seen=self.local(-4)
            self.op(seen,0,True)
            if not seen:
                self.logical(self.r['di'])
                if self.r['di']:
                    self.r['ax']=digits
                    self.r['ax']=self.shift(self.r['ax'],3)
                    self.r['si']=self.op(self.r['si'],self.r['ax'],True)
                    self.local(-4,1)
            seen=self.local(-4)
            self.op(seen,0,True)
            if seen:
                self.push(self.r['si'])
                self.push(0xE0002F,4)
                self.number(0x2D23)
                self.r['si']=self.op(self.r['si'],16)
            carry=self.flags&1
            self.local(-2,self.op(self.local(-2),1,True))
            self.flags=(self.flags&~1)|carry
            self.loop_iterations+=1
        self.r['ax']=self.dg(DATA['score'],1)
        self.r['di']=self.r['ax']
        self.push(self.r['si'])
        self.push(0xE0002F,4)
        self.number(0x2D4C)
        self.push(0x19800F8,4)
        self.push(0x2F)
        self.number(0x2D63)
        self.r['ax']=self.dg(DATA['skill'],1)
        self.divide(100)
        self.r['di']=self.r['ax']
        self.r['si']=408
        self.local(-4,0)
        self.logical(self.r['di'])
        if self.r['di']:
            self.r['si']=self.op(self.r['si'],16,True)
            self.local(-4,1)
            self.push(self.r['si'])
            self.push(0x123002F,4)
            self.number(0x2D9A)
            self.r['si']=self.op(self.r['si'],16)
        self.r['ax']=self.dg(DATA['skill'],1)
        self.divide(100)
        self.r['bx']=10
        self.r['ax']=self.r['dx']
        self.divide(10)
        self.r['di']=self.r['ax']
        self.logical(self.r['di'])
        if self.r['di']:
            seen=self.local(-4)
            self.op(seen,0,True)
            if not seen:
                self.local(-4,1)
                self.r['si']=self.op(self.r['si'],8,True)
        seen=self.local(-4)
        self.op(seen,0,True)
        if seen:
            self.push(self.r['si'])
            self.push(0x123002F,4)
            self.number(0x2DE0)
            self.r['si']=self.op(self.r['si'],16)
        self.r['ax']=self.dg(DATA['skill'],1)
        self.divide(10)
        self.r['di']=self.r['dx']
        self.push(self.r['si'])
        self.push(0x123002F,4)
        self.number(0x2E06)
        self.r['ax']=(self.r['si']+16)&65535  # Native LEA preserves flags.
        self.push(self.r['ax'])
        self.push(0x123002F,4)
        self.push(self.ds)
        self.push(DATA['unit'])
        self.render(0x2E19)
        self.pop('di')
        self.pop('si')
        self.finish(locals_=True)
        return self.full(),self.flags,self.mask


class Machine(Physical):
    def __init__(self,image,load):
        super().__init__(image,load)
        self.image,self.cs,self.ds=image,load+CS,load+DS
        start=CS*16+START
        ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[start:start+SIZE],start))
        need(sum(i.size for i in ins)==SIZE,'all389 owner bytes are complete instructions')
        self.instructions={i.address:i.size for i in ins}
        self.owner=set(range(start,start+SIZE))
        self.seen=set()
        self.hooks += [self.u.hook_add(UC_HOOK_INTR,self.interrupt),self.u.hook_add(UC_HOOK_INSN,self.out,None,1,0,UC_X86_INS_OUT)]

    def regs(self,full=False):
        r={n:self.u.reg_read(reg) if full else self.u.reg_read(reg)&65535 for n,reg in GPRS.items()}
        r.update({n:self.u.reg_read(REG[n]) for n in ('cs','ds','es','ss')})
        r.update(fs=self.u.reg_read(UC_X86_REG_FS),gs=self.u.reg_read(UC_X86_REG_GS))
        return r

    def interrupt(self,u,number,_):
        self.fail('no interrupt boundary belongs to verdict: '+str(number))

    def out(self,u,port,size,value,_):
        self.fail('no direct port boundary belongs to verdict')

    def write(self,u,access,at,size,value,_):
        if self.index<len(self.events) and self.events[self.index][0]=='far-frame':
            try:
                _,dest,ip,cs=self.events[self.index]
                need(size==2 and (at,value) in ((dest,ip),(dest+2,cs)),'only real native far-frame return words')
            except Exception as error:
                self.fail(error)
            return
        super().write(u,access,at,size,value,_)

    def code(self,u,at,size,_):
        try:
            offset=at-self.base
            if at==self.cs*16+0xFFFF:
                self.returned=True
                u.emu_stop()
                return
            self.max_depth=max(self.max_depth,self.o['stack']-u.reg_read(REG['sp']))
            if offset==RENDER[0]*16+RENDER[1]:
                sp,ss=u.reg_read(REG['sp']),u.reg_read(REG['ss'])
                frame=bytes(u.mem_read(address(ss,sp),14))
                ip,cs=struct.unpack('<2H',frame[:4])
                self.event(('far-frame',address(ss,sp),ip,cs))
                self.calls+=1
                expected=self.events[self.index]
                mask=expected[-1]
                self.event(('render-entry',self.calls,self.regs(True),frame.hex(),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                for index,off,raw in self.o['writes']:
                    if index==self.calls:
                        dest=address(self.data_ds,off)
                        self.event(('renderer-write',dest,raw.hex()))
                        u.mem_write(dest,raw)
                reply=renderer_reply(self.o['reply_seed'],self.calls)
                for name in ('ax','bx','cx','dx'):
                    u.reg_write(GPRS[name],reply[name])
                u.reg_write(REG['es'],reply['es'])
                u.reg_write(UC_X86_REG_EFLAGS,2|(reply_flags(self.o,self.calls)&(ARITH|0x600)))
                u.reg_write(REG['sp'],sp+14)
                u.reg_write(REG['cs'],cs)
                u.reg_write(REG['ip'],ip)
                return
            need(self.instructions.get(offset)==size,'only actual verdict instructions or the explicit unowned renderer entry')
            if offset not in self.seen:
                self.covered.update(range(offset,offset+size))
                self.seen.add(offset)
            if offset-CS*16 in RETURNS:
                self.event(('renderer-return',self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600),ARITH|0x600))
        except Exception as error:
            self.fail(error)

    def run(self,*,score=DEFAULT_SCORE,playchar=2,rank=3,skill=255,pointer=None,writes=(),reply_seed=0x89ABCDEF,
            reply_flags=0xED7,flag_schedule=(),foreign_ds=False,flags=0x202,ss=0x7000,stack=0xF800,seed=0x1357,persistent=False):
        need(len(score)==9 and all(0<=v<=255 for v in (*score,playchar,rank,skill)),'nine score bytes with continues alias0 and raw BYTE selectors/skill')
        need(0<=reply_seed<=0xFFFFFFFF and reply_flags&~(ARITH|0x602)==0 and all(f&~(ARITH|0x602)==0 for f in flag_schedule),'explicit DWORD/flag renderer replies')
        need(all(1<=i<=16 and 0<=off<off+len(raw)<=65536 and isinstance(raw,bytes) for i,off,raw in writes),'bounded renderer DGROUP writes')
        need(ss in (0x7000,0x8000) and stack in (0x80,0xF800) and flags in (2,0x202,0x402,0xED7),'foreign stacks and defined initial flags')
        need(pointer is None or len(pointer)==2 and TABLE_START<=pointer[0]<=TABLE_END-4 and (pointer[0]-TABLE_START)%4==0 and 0<=pointer[1]<=0xFFFFFFFF,'explicit complete DWORD table cell')
        self.data_ds=0x5000 if foreign_ds else self.ds
        memory=bytearray(self.u.mem_read(0,1<<20) if persistent else self.initial)
        def put(off,raw):
            at=address(self.data_ds,off)
            memory[at:at+len(raw)]=raw
        if not persistent:
            for i,off in enumerate(range(TABLE_START,TABLE_END,4)):
                value=(((0x5000+i*0x11)&65535)<<16)|((0xFFF0+i*0x27)&65535)
                put(off,struct.pack('<I',value))
            put(DATA['score'],bytes(score))
            for name,value in (('playchar',playchar),('rank',rank),('skill',skill)):
                put(DATA[name],bytes([value]))
        if pointer is not None:
            put(pointer[0],struct.pack('<I',pointer[1]))
        at=address(ss,stack)
        memory[at:at+2]=b'\xFF\xFF'
        self.u.mem_write(0,bytes(memory))
        regs={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)}
        regs.update(sp=stack,cs=self.cs,ds=self.data_ds,es=0x6666,ss=ss,fs=0x3456,gs=0x4567)
        high={n:((seed^0x5AA5)<<16) for n in GPRS}
        for n,reg in GPRS.items():
            self.u.reg_write(reg,high[n]|regs[n])
        for n in ('cs','ds','es','ss'):
            self.u.reg_write(REG[n],regs[n])
        self.u.reg_write(UC_X86_REG_FS,regs['fs'])
        self.u.reg_write(UC_X86_REG_GS,regs['gs'])
        self.u.reg_write(UC_X86_REG_EFLAGS,flags)
        self.o=dict(load=self.load,stack=stack,writes=writes,reply_seed=reply_seed,reply_flags=reply_flags,flag_schedule=flag_schedule)
        spec=Spec(memory,regs,high,flags,self.o)
        expected,final,mask=spec.run()
        self.events,self.index,self.observed,self.error,self.returned,self.calls,self.max_depth=spec.events,0,[],None,False,0,0
        try:
            self.u.emu_start(self.cs*16+START,1<<20,count=100000)
        except UcError as error:
            raise ValueError('MAINL verdict guest exception') from error
        need(self.error is None,self.error or 'guest failure')
        need(self.returned and self.index==len(self.events),'complete native near return; never budget expiry')
        need(self.regs(True)==expected,'complete DWORD/segment state '+str((self.regs(True),expected)))
        need(self.u.reg_read(UC_X86_REG_EFLAGS)&(mask|0x600)==final&(mask|0x600),'defined flags and IF/DF')
        need(bytes(self.u.mem_read(0,1<<20))==memory,'all physical memory including native far frames and every caller-stack byte')
        need(spec.loop_iterations==8 and 6<=self.calls<=16,'all eight native score iterations and bounded renderer calls')
        return dict(registers=expected,flags=final&(mask|0x600),flag_mask=mask|0x600,renderer_calls=self.calls,
            score_iterations=spec.loop_iterations,stack_depth=self.max_depth,rendered=spec.rendered,
            trace_sha256=hashlib.sha256(json.dumps(self.events,sort_keys=True).encode()).hexdigest())


def geometry_proof(image):
    for at,raw in ((0x2C98,bytes.fromhex('c80400005657')),
                   (0x2CAB,bytes.fromhex('c1e0028bd866ffb7e20a')),
                   (0x2CC7,bytes.fromhex('c1e0028bd866ffb7060b')),
                   (0x2CDE,bytes.fromhex('c746fe0800eb44')),
                   (0x2D26,bytes.fromhex('ff4efe837efe007fb6')),
                   (0x2D3D,bytes.fromhex('8bdfc1e30266ffb7160b')),
                   (0x2D63,bytes.fromhex('a0e827b400bb640099f7fb')),
                   (0x2D9D,bytes.fromhex('a0e827b400bb640099f7fbbb0a008bc299f7fb')),
                   (0x2DE3,bytes.fromhex('a0e827b400bb0a0099f7fb')),
                   (0x2E06,bytes.fromhex('8d44105066682f0023011e68250c'))):
        need(image.program_image[CS*16+at:CS*16+at+len(raw)]==raw,'native fixed loop, independent BYTE skill reads and full far-pointer argument CFG')
    for value in range(256):
        need(0<=value//100<=2 and 0<=value%100//10<=9 and 0<=value%10<=9,'all BYTE skill values have safe signed IDIV100/10')
        for table in ('playchars','ranks','numbers'):
            at=DATA[table]+value*4
            need(TABLE_START<=at<at+4<=TABLE_END<65536,'unchecked BYTE index reads a full far DWORD inside the explicit table fixture')
    for k in range(9):
        start=408-k*8
        need(344<=start<=408 and 408<=start+k*16<=472,'all score leading positions have bounded WORD coordinates')
    return dict(score_iterations=8,renderer_call_bounds=[6,16],maximum_stack_depth=24,
        score_digit_indices=[8,1],continues_alias_byte=0,local_stack_bytes=4,far_string_bytes=4,renderer_argument_bytes=10,
        BYTE_index_range=[0,255],WORD_table_shift=2,table_fixture_range=[TABLE_START,TABLE_END],
        skill_BYTE_domain=[0,255],skill_divisors=[100,10],skill_read_sites=[0x2D63,0x2D9D,0x2DE3],
        skill_hundreds_range=[0,2],skill_tens_and_ones_range=[0,9],score_x_range=[344,472],skill_x_range=[392,440],
        loop_counter_assumptions=['renderer preserves BP/SI/DI/SS and returns with far Pascal pop10',
            'renderer may write declared DGROUP bytes; mapped CODE/DGROUP/stack are disjoint and private loop locals receive no external writes'],
        loop_termination_proved=True,all_DIV_inputs_safe=True,guest_iterations_skipped=False,budget_expiry_used=False,
        renderer_code_strings_tables_or_physical_pixels_proved=False)


def cases():
    for field,value in itertools.product(('playchar','rank','skill'),range(256)):
        yield {field:value}
    for pos,value in itertools.product(range(9),range(256)):
        score=[0]*9
        score[pos]=value
        yield dict(score=tuple(score))
    for table,index,lane,value in itertools.product(('playchars','ranks','numbers'),(0,),range(4),range(256)):
        cell=DATA[table]+({'playchars':2,'ranks':3,'numbers':8}[table])*4
        yield dict(pointer=(cell,(0xA55A3CC3&~(255<<(lane*8)))|(value<<(lane*8))))
    for value in range(256):
        yield dict(writes=((1,DATA['rank'],bytes([value])),))
        yield dict(writes=((3,DATA['score']+7,bytes([value])),))
        yield dict(writes=((10,DATA['score'],bytes([value])),))
        yield dict(writes=((12,DATA['skill'],bytes([value])),))
        yield dict(score=(0,)*9,skill=200,writes=((5,DATA['skill'],bytes([value])),))
        yield dict(score=(0,)*9,skill=200,writes=((6,DATA['skill'],bytes([value])),))
    for pos,value in itertools.product(range(9),range(256)):
        score=[0]*9
        score[pos]=value
        yield dict(writes=((2,DATA['score'],bytes(score)),))
    for flags,ss,stack,foreign,reply in itertools.product((2,0x202,0x402,0xED7),(0x7000,0x8000),(0x80,0xF800),(False,True),(2,0x202,0x402,0xED7)):
        yield dict(flags=flags,ss=ss,stack=stack,foreign_ds=foreign,reply_flags=reply)
    for lane,value in itertools.product(range(4),range(256)):
        yield dict(reply_seed=value<<(lane*8))
    yield dict(score=(0,)*9,skill=0)
    yield dict(score=(0,)*9,skill=10,foreign_ds=True,flag_schedule=(2,0x202,0x402,0xED7))
    yield dict(writes=((11,DATA['score'],b'\xFF'),(11,DATA['numbers']+2*4,bytes.fromhex('ffffcdab'))))
    yield dict(writes=((1,DATA['ranks']+3*4,bytes.fromhex('ffff0000')),(1,DATA['playchar'],b'\xFF')))
    yield dict(score=(0,)*9,skill=100,writes=((5,DATA['skill'],b'\x09'),(6,DATA['skill'],b'\xFF')))


def verify(target,candidate):
    proof=geometry_proof(target)
    need(proof==geometry_proof(candidate),'both native fixed-loop / arithmetic / far-pointer proofs')
    observations=[]
    for image_index,image in enumerate((target,candidate),1):
        rows=[]
        for load in (0x1000,0x3000):
            m=Machine(image,load)
            trace=hashlib.sha256()
            low,high,peak=16,0,0
            try:
                def entry(parameters):
                    nonlocal low,high,peak
                    result=m.run(**parameters)
                    low=min(low,result['renderer_calls'])
                    high=max(high,result['renderer_calls'])
                    peak=max(peak,result['stack_depth'])
                    trace.update(json.dumps(result,sort_keys=True).encode())
                for count,parameters in enumerate(cases(),1):
                    try:
                        entry(dict(seed=0x1357 if count&1 else 0xECA8,**parameters))
                    except Exception:
                        print('Verdict failing case',image_index,load,count,parameters,flush=True)
                        raise
                    if count%512==0:
                        print(f'Verdict: image {image_index}, load {load:04X}, {count} complete entries',flush=True)
                for index in range(3):
                    entry(dict(persistent=index>0,writes=((1,DATA['skill'],bytes([index*100])),)))
                    count+=1
                need(m.owner<=m.covered,'all389 owner bytes execute')
                need((low,high,peak)==(6,16,24),'actual complete callback/stack bounds')
                rows.append(dict(load_segment=load,cases=count,complete_near_returns=count,executed_owner_bytes=389,
                    minimum_renderer_calls=low,maximum_renderer_calls=high,maximum_stack_depth=peak,score_iterations_per_entry=8,
                    trace_sha256=trace.hexdigest()))
                print(f'Verdict: image {image_index}, load {load:04X}, {count} entries / all389 bytes pass',flush=True)
            finally:
                m.close()
        observations.append(rows)
    need(observations[0]==observations[1],'independent full target/candidate observations')
    return dict(images=2,functions=1,code_bytes=389,cases_per_image=sum(o['cases'] for o in observations[0]),
        observations=observations[0],executed_owner_bytes=389,actual_context_bytes=0,ignored_stack_bytes=0,
        native_geometry_proof=proof,immediate_renderer_return_checks=True,full_renderer_DWORD_replies=True,
        real_far_frames_checked=True,guest_iterations_skipped=False,renderer_body_or_table_storage_accepted=False,
        physical_text_pixels_or_timing_proved=False)


def negative_controls(target):
    zero=dict(score=(0,)*9,skill=0)
    ten=dict(score=(0,)*9,skill=10)
    hundred=dict(skill=100)
    controls=(
        ('ENTER4',0x2C99,1,{}),('saved-SI',0x2C9C,1,{}),('saved-DI',0x2C9D,1,{}),
        ('playchar-x352',0x2CA2,1,{}),('playchar-y174',0x2CA0,1,{}),('playchar-fx47',0x2CA5,1,{}),
        ('live-playchar-field',0x2CA7,1,{}),('playchar-zero-extension',0x2CAA,1,{}),
        ('playchar-DWORD-index',0x2CAD,1,{}),('playchar-far-pointer-width',0x2CB0,1,{}),
        ('playchar-table-base',0x2CB3,1,{}),('playchar-render-call',0x2CB6,1,{}),
        ('rank-x360',0x2CBE,1,{}),('rank-y199',0x2CBC,1,{}),('live-rank-field',0x2CC3,1,{}),
        ('rank-zero-extension',0x2CC6,1,{}),('rank-DWORD-index',0x2CC9,1,{}),
        ('rank-table-base',0x2CCF,1,{}),('rank-render-call',0x2CD2,1,{}),
        ('score-x408',0x2CD7,1,{}),('score-seen-zero',0x2CDC,1,{}),('score-eight-digits',0x2CE1,1,{}),
        ('score-initial-loop-edge',0x2CE4,1,{}),('score-local-index',0x2CE7,2,{}),
        ('live-score-digit-byte',0x2CEA,1,{}),('score-digit-zero-extension',0x2CED,1,{}),
        ('first-seen-predicate',0x2CF3,1,{}),('digit-OR-predicate',0x2CF7,8,{}),
        ('leading-zero-skip',0x2CF9,1,zero),('leading-position-times8',0x2CFF,1,{}),
        ('leading-position-subtract',0x2D00,0x28,{}),('seen-one-store',0x2D05,1,{}),
        ('second-seen-predicate',0x2D0A,1,{}),('score-x-argument',0x2D0D,1,{}),
        ('score-fx',0x2D10,1,{}),('score-y224',0x2D12,1,{}),('score-saved-digit-index',0x2D15,8,{}),
        ('score-DWORD-index',0x2D18,1,{}),('score-number-table',0x2D1C,1,{}),('score-render-call',0x2D1F,1,{}),
        ('score-x-step16',0x2D25,1,{}),('score-counter-decrement',0x2D27,8,{}),
        ('score-counter-zero-test',0x2D2C,1,{}),('score-loop-signed-branch',0x2D2D,1,{}),
        ('continues-alias-byte0',0x2D30,1,{}),('continues-saved-DI',0x2D35,8,{}),
        ('continues-first-x',0x2D36,1,{}),('continues-first-render',0x2D48,1,{}),
        ('continues-second-x408',0x2D50,1,{}),('continues-second-y248',0x2D4E,1,{}),
        ('continues-second-saved-digit',0x2D55,8,{}),('continues-second-render',0x2D5F,1,{}),
        ('hundreds-live-skill',0x2D64,1,{}),('hundreds-zero-extension',0x2D67,1,{}),
        ('hundreds-divisor100',0x2D69,1,{}),('hundreds-CWD',0x2D6B,8,{}),('hundreds-IDIV-BX',0x2D6D,1,{}),
        ('hundreds-digit-to-DI',0x2D6F,8,hundred),('skill-x408',0x2D71,1,{}),('skill-seen-reset',0x2D76,1,{}),
        ('hundreds-nonzero',0x2D79,8,{}),('hundreds-zero-skip',0x2D7B,1,zero),
        ('hundreds-left16',0x2D7E,1,{}),('hundreds-seen-one',0x2D82,1,{}),
        ('hundreds-render-call',0x2D96,1,{}),('hundreds-x-step16',0x2D9C,1,{}),
        ('tens-live-skill',0x2D9E,1,{}),('tens-divisor100',0x2DA3,1,{}),
        ('tens-remainder-to-AX',0x2DAC,8,{}),('tens-divisor10',0x2DA9,1,{}),('tens-CWD',0x2DAD,8,{}),
        ('tens-nonzero',0x2DB3,8,{}),('tens-zero-branch',0x2DB5,1,hundred),
        ('tens-first-seen-test',0x2DB9,1,ten),('tens-first-seen-store',0x2DBF,1,ten),
        ('tens-leading-left8',0x2DC3,1,ten),('tens-second-seen-test',0x2DC7,1,{}),
        ('tens-render-call',0x2DDC,1,{}),('tens-x-step16',0x2DE2,1,{}),
        ('ones-live-skill',0x2DE4,1,{}),('ones-divisor10',0x2DE9,1,{}),
        ('ones-remainder-to-DI',0x2DEF,8,{}),('ones-render-call',0x2E02,1,{}),
        ('unit-LEA-plus16',0x2E08,1,{}),('unit-x-argument',0x2E09,1,{}),
        ('unit-fx',0x2E0C,1,{}),('unit-y291',0x2E0E,1,{}),('unit-real-DS',0x2E10,1,{}),
        ('unit-literal-offset',0x2E12,1,{}),('unit-render-call',0x2E15,1,{}),
        ('restore-DI',0x2E19,1,{}),('restore-SI',0x2E1A,1,{}),('near-RET',0x2E1C,8,{}))
    rejected=[]
    for name,at,xor,parameters in controls:
        raw=bytearray(target.program_image)
        raw[CS*16+at]^=xor
        m=None
        try:
            m=Machine(replace(target,program_image=bytes(raw)),0x1000)
            m.run(**parameters)
        except (ValueError,UcError):
            rejected.append(name)
        else:
            raise ValueError('MAINL verdict actual instruction mutation escaped: '+name)
        finally:
            if m:
                m.close()
    return dict(count=len(rejected),rejected=rejected,owner_instruction_mutations=len(controls),actual_context_instruction_mutations=0,
        actual_guest_instruction_mutations=True,unowned_renderer_or_DATA_mutations_counted=False)
