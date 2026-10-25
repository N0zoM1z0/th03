"""Independent story policy with actual LCG, cfg, sound and cleanup instructions.

The character selector and DOS/library replies are bounded interfaces. A fully
blocked candidate domain proves nontermination; a budget expiry never does.
"""
from dataclasses import replace
import hashlib,json,struct
from lib.op_nested_context import configure
from types import SimpleNamespace
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import UcError
from unicorn.x86_const import UC_X86_REG_EFLAGS,UC_X86_REG_ESP
from lib.op_vs_runtime import Machine as Base,REG,GPRS,CFG,KAJA,EXIT
from lib.op_story_layout import START,SIZE,RANDOM,RANDOM_SIZE
from lib.op_cfg_runtime import RESIDENT,ACTIVE,MIDI,reply
from lib.op_dispatch_runtime import add_flags

HELPERS=((CFG,67),(KAJA,30),(EXIT,67),(RANDOM,RANDOM_SIZE))
LOOP=0x9A85
SELECT=0xBD9A

def need(v,m):
    if not v:raise ValueError('OP story contract: '+str(m))
def word(memory,at):return int.from_bytes(memory[at:at+2],'little')
def parity(v):return 4 if (v&255).bit_count()%2==0 else 0
def logical8(v):return parity(v)|(64 if v==0 else 0)|(v&128)
def lcg(value):return (value*22695477+1)&0xFFFFFFFF

class Machine(Base):
    def __init__(self,mz,load):
        super().__init__(mz,load)
        self.instructions={};self.owned=set(range(START,START+SIZE));self.nested=set()
        for start,size in ((START,SIZE),*HELPERS):
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+size],start))
            need(sum(i.size for i in rows)==size,'complete caller/helper instructions')
            self.instructions.update({i.address:i.size for i in rows})
            if start!=START:self.nested.update(range(start,start+size))
        self.covered=set();self.nested_covered=set();self.maximum_stack=0

    def outside_stack(self,expected):
        actual=bytes(self.uc.mem_read(0,1<<20));lo,hi=0x70000+self.stack-48,0x70000+self.stack
        expected[lo:hi]=actual[lo:hi]
        need(actual==expected,'whole physical memory outside 48 private stack bytes, including caller words')

    def write(self,uc,access,address,size,value,data):
        try:
            if 0x70000+self.stack-48<=address and address+size<=0x70000+self.stack:
                self.maximum_stack=max(self.maximum_stack,0x70000+self.stack-address);return
            self.event(('store',address,size,value))
        except Exception as error:self.fail(error)

    def begin_random(self):
        e=self.plan[self.root_index];need(e[0]=='random','independent RNG call order')
        _,stage,before,after=e;self.root_event(e)
        sp=self.r('sp');regs=self.registers();flags=self.uc.reg_read(UC_X86_REG_EFLAGS)
        need((sp,self.r('si'),self.r('bp'),self.r('ss'))==(self.stack-12,stage,self.stack-2,0x7000),'actual random far frame and stage')
        need(bytes(self.uc.mem_read(0x70000+sp,4))==struct.pack('<HH',0x18A,self.cs),'real random return address')
        need(int.from_bytes(self.shadow[self.data+0x312:self.data+0x316],'little')==before
             and bytes(self.uc.mem_read(self.data+0x312,4))==before.to_bytes(4,'little')
             and lcg(before)==after,'independent full DWORD seed transition')
        mix=((before>>16)*0x4E35+(before&65535)*0x15A)&65535
        regs.update(ax=(after>>16)&0x7FFF,cx=mix,dx=after>>16,cs=self.cs)
        # Every guest write is checked by the ordered write hook. This helper
        # has only two allowed WORD stores and no external service. Update the
        # independent shadow in place; do the full MiB comparison at the next
        # service boundary/end, avoiding a full image copy on every LCG step.
        memory=self.shadow;memory[self.data+0x312:self.data+0x316]=after.to_bytes(4,'little')
        full={n:(self.uc.reg_read(GPRS[n])&0xFFFF0000)|regs[n] for n in GPRS}
        self.active=SimpleNamespace(name='random',sp=sp,index=0,if_df=flags&0x600,
            return_rva=0x9A8A,events=[('store',self.data+0x312,2,after&65535),('store',self.data+0x314,2,after>>16)],
            regs=regs,full=full,mask=0x8C5,flags=logical8((after>>24)&0x7F),memory=memory,delta=4)
        self.random_calls+=1

    def finish(self):
        if self.active.name=='random':
            h=self.active
            need(self.r('sp')==h.sp+4 and self.registers()==h.regs,'complete random return WORD/segment ABI')
            need(all(self.uc.reg_read(GPRS[n])==h.full[n] for n in GPRS),'complete random DWORD ABI')
            f=self.uc.reg_read(UC_X86_REG_EFLAGS)
            need(f&h.mask==h.flags&h.mask and f&0x600==h.if_df,'defined random flags and IF/DF')
            need(h.index==len(h.events) and bytes(self.uc.mem_read(self.data+0x312,4))
                 ==bytes(h.memory[self.data+0x312:self.data+0x316]),'two exact ordered random stores')
            self.helper_trace.update(json.dumps((h.name,h.events),sort_keys=True).encode())
            self.shadow,self.active=h.memory,None;self.helper_calls+=1
        else:super().finish()
        need(self.uc.reg_read(UC_X86_REG_ESP)&0xFFFF0000==self.esp_high,'helper preserves ESP high half')

    def code(self,uc,address,size,data):
        try:
            rva=address-self.base
            if rva==SELECT:
                need(self.active is None,'selector is a separate unowned boundary')
                self.root_event(('selection',))
                sp,ip,cs,args=self.frame(0,False)
                need((sp,ip,cs)==(self.stack-10,0x150,self.cs),'real near selector frame')
                expected=dict(self.initial_regs,bx=self.resoff,es=self.resseg,bp=self.stack-2)
                need(self.registers()==expected,'complete selector request WORD/segment registers')
                need(all(self.uc.reg_read(GPRS[n])==self.high[n]|expected[n] for n in GPRS),'selector request DWORD high halves')
                need(uc.reg_read(UC_X86_REG_EFLAGS)&0xED5==self.flags&0xED5,'selector incoming defined flags and IF/DF')
                self.outside_stack(self.shadow)
                for off,raw in self.selection_transfers:
                    uc.mem_write(self.resbase+off,raw);self.shadow[self.resbase+off:self.resbase+off+len(raw)]=raw
                self.root_calls+=1;self.respond(self.root_calls,self.selection_ax)
                self.leave_service(sp,ip,cs,0,False);return
            if rva==RANDOM:self.begin_random()
            if rva==LOOP and self.nonterminal and self.root_index==len(self.plan):
                need(self.active is None,'closed polling prefix leaves no active helper')
                self.held=True;uc.emu_stop();return
            super().code(uc,address,size,data)
        except Exception as error:self.fail(error)

    def run(self,*,selected_char=1,random_seed=0x12345678,rank=0,selection_ax=0,
            active=1,midi=0,seed=0x1357,status=0xFFFF,flags=0x202,stack=0xF800,
            resseg=0x6000,resoff=0x31,options=(0x81,0x52),seen=None,reenter=False,_context=None):
        configure(self,_context)
        if _context is not None:
            need(not reenter and seen is None,'nested entry preserves actual static state')
            stack,flags=_context.stack,_context.flags;resoff,resseg,base=_context.resident(self)
            active,midi=_context.memory[self.data+ACTIVE],_context.memory[self.data+MIDI]
        need(all(0<=v<=255 for v in (selected_char,rank,active,midi,*options)) and len(options)==2,'BYTE selector/resident domain')
        need(0<=random_seed<=0xFFFFFFFF and all(0<=v<=65535 for v in (selection_ax,seed,status)),'DWORD random and WORD service domains')
        need(80<=stack<=0xFFF0 and resseg in (0x5000,0x6000) and 0<=resoff<=0xFF80,'disjoint resident and private stack')
        if _context is None:
            if not reenter:self.uc.mem_write(0,bytes(self.initial))
            self.stack,self.seed,self.status,self.flags=stack,seed,status,flags
            self.resseg,self.resoff,self.resbase=resseg,resoff,resseg*16+resoff
            self.uc.mem_write(0x70000+stack-80,b'\xD3'*80);self.uc.mem_write(0x70000+stack,b'\xFF\xFF\x5A\xA5')
            self.uc.mem_write(self.data+RESIDENT,struct.pack('<HH',resoff,resseg));self.uc.mem_write(self.resbase,b'\xA5'*0x60)
            self.uc.mem_write(self.data+ACTIVE,bytes((active,)));self.uc.mem_write(self.data+MIDI,bytes((midi,)))
            if seen is not None:
                need(len(seen)==7 and all(0<=v<=255 for v in seen),'seven explicit mutable seen BYTEs')
                self.uc.mem_write(self.data+0x99,bytes(seen))
        self.stack,self.seed,self.status,self.flags=stack,seed,status,flags
        self.resseg,self.resoff,self.resbase=resseg,resoff,resseg*16+resoff
        self.file=bytearray(b'\x02\x01\x03\x48\x57\0\x50\xA7' if _context is None else _context.file)
        self.selection_ax=selection_ax
        self.selection_transfers=[(0xC,bytes((selected_char,))),(0x10,struct.pack('<I',random_seed)),
            (0xB,bytes((rank,))),(0x15,bytes(options))]
        self.shadow=bytearray(self.uc.mem_read(0,1<<20));self.plan=[]
        def store_at(at,size,value):self.plan.append(('store',at,size,value))
        def store(off,value):store_at(self.resbase+off,1,value)
        for off,value in ((0x39,0),(0x17,0),(0x33,0),(0xE,0),(0xF,1),(0x28,1),(0x34,2),(0x35,0),(0xD,255)):store(off,value)
        self.plan.append(('selection',));self.cancelled=bool(selection_ax&255)
        seen_state=list(self.shadow[self.data+0x99:self.data+0xA0]);self.nonterminal=False;self.retries=0;self.last_random=None
        if not self.cancelled:
            # C++ signed division truncates toward zero: character zero also
            # indexes row zero. Other unchecked BYTE values may read past row8.
            index=max(0,(selected_char-1)//2)
            excluded=self.shadow[self.data+0xA0+index];opponents=[]
            while True:
                state=random_seed;store_at(self.data+0x312,4,state)
                opponents=[]
                for stage in range(6):
                    available=[v for v in range(7) if not seen_state[v] and v!=excluded]
                    extra=8 if not available else None
                    attempts=0
                    while True:
                        before=state;state=lcg(state);candidate=((state>>16)&0x7FFF)%7
                        self.plan.append(('random',stage,before,state));attempts+=1
                        self.last_random=(before,state,candidate,stage,excluded)
                        need(attempts<=10000,'finite returning witness, without an all-seeds delay bound')
                        if extra is not None:
                            extra-=1
                            if extra==0:self.nonterminal=True;break
                        elif not seen_state[candidate] and candidate!=excluded:break
                    if self.nonterminal:break
                    seen_state[candidate]=1;store_at(self.data+0x99+candidate,1,1)
                    paletted=2*candidate+1;store(0x29+stage,paletted)
                    if paletted==selected_char:paletted+=1;store(0x29+stage,paletted)
                    opponents.append(paletted)
                if self.nonterminal:break
                store(0xD,opponents[0]);paletted=(2*excluded+1)&255
                store(0x2F,paletted);opponents.append(paletted)
                store(0x30,15)
                if selected_char==15:store(0x30,16)
                opponents.append(16 if selected_char==15 else 15)
                store(0x31,17)
                if selected_char==17:store(0x31,18)
                opponents.append(18 if selected_char==17 else 17)
                if any(max(0,(v-1)//2)>=9 for v in opponents):
                    self.retries+=1;need(self.retries==1,'retry dirties at least six static slots');continue
                for i in range(16):store(0x18+i,0)
                for off,value in ((0x36,3),(0x37,0),(0x38,(70+rank*25)&255)):store(off,value)
                self.plan += [('cfg',),('library','gaiji_restore',()),('kaja',),('exit',),
                    ('library','execl',(0x16F,self.ds,0x16F,self.ds,0,0))]
                break
        if _context is None:
            self.initial_regs={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)}
            self.high={n:(seed^0x5AA5)<<16 for n in GPRS};self.esp_high=(seed^0xA55A)<<16
            for n in GPRS:self.uc.reg_write(GPRS[n],self.high[n]|self.initial_regs[n])
            self.initial_regs.update(cs=self.cs,ds=self.ds,es=seed,ss=0x7000)
            for n in ('cs','ds','es','ss'):self.uc.reg_write(REG[n],self.initial_regs[n])
            self.uc.reg_write(UC_X86_REG_ESP,self.esp_high|stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        else:
            self.initial_regs,self.high=_context.initial();self.esp_high=_context.full_registers['sp']&0xFFFF0000
        self.root_index,self.root_calls,self.helper_calls,self.random_calls=0,0,0,0
        self.active,self.box_return,self.error,self.returned,self.held=None,None,None,False,False
        self.helper_trace=hashlib.sha256()
        try:self.uc.emu_start(self.base+START,0x100000,count=1000000)
        except UcError as error:raise ValueError('OP story contract: guest fault') from error
        need(self.error is None,self.error or 'guest error')
        need(self.root_index==len(self.plan) and self.active is None,'complete independent caller/helper plan')
        f=self.uc.reg_read(UC_X86_REG_EFLAGS)
        if self.nonterminal:
            need(self.held and not self.returned and self.r('sp')==stack-8,'explicit closed-loop prefix, not a budget exit')
            before,state,candidate,stage,excluded=self.last_random
            need(all(seen_state[v] or v==excluded for v in range(7)),'all possible random candidate exits blocked')
            expected=dict(self.initial_regs,ax=((state>>16)&0x7FFF)//7 if seen_state[candidate] else excluded,
                bx=candidate,cx=((before>>16)*0x4E35+(before&65535)*0x15A)&65535,dx=candidate,
                si=stage,bp=stack-2,es=resseg)
            mask,value=0x8D5,logical8(seen_state[candidate]) if seen_state[candidate] else 0x44
        else:
            need(self.returned and not self.held and self.r('sp')==stack+2,'near root return and far cdecl cleanup')
            expected,_=reply(self.initial_regs,self.root_calls,seed,flags,selection_ax if self.cancelled else status)
            expected['ax']=(expected['ax']&0xFF00)|int(self.cancelled)
            mask,value=(0x8C5,logical8(selection_ax&255)) if self.cancelled else (0x8D5,add_flags(stack-20,12))
        need(self.registers()==expected,'independent final WORD/segment registers: '+str((self.registers(),expected)))
        full={n:self.uc.reg_read(GPRS[n]) for n in GPRS}
        for n in GPRS:
            upper=random_seed&0xFFFF0000 if n=='ax' and not self.cancelled else self.high[n]
            need(full[n]==upper|expected[n],'complete DWORD effects: '+n)
        need(self.uc.reg_read(UC_X86_REG_ESP)==self.esp_high|self.r('sp'),'complete ESP high/low effects')
        need(f&mask==value&mask and f&0x600==flags&0x600,'defined final flags and inherited IF/DF')
        self.outside_stack(self.shadow)
        if _context is not None:
            output_high=dict(self.high)
            if not self.cancelled:output_high['ax']=random_seed&0xFFFF0000
            _context.accept(self,expected,output_high,mask,value,self.shadow,file=self.file,held=self.nonterminal)
        return dict(cancelled=self.cancelled,nonterminal=self.nonterminal,retries=self.retries,
            random_calls=self.random_calls,helper_calls=self.helper_calls,registers=self.registers(),full_registers=full,
            esp=self.uc.reg_read(UC_X86_REG_ESP),flags=f&(mask|0x600),flags_mask=mask,
            seen=list(self.shadow[self.data+0x99:self.data+0xA0]),file_hex=self.file.hex(),
            plan_sha256=hashlib.sha256(json.dumps(self.plan).encode()).hexdigest(),helper_trace_sha256=self.helper_trace.hexdigest())


def cases():
    for value in range(256):
        yield dict(selected_char=value)
        yield dict(selection_ax=0xA500|value,selected_char=value,random_seed=(value*0x01010101))
        yield dict(rank=value,selected_char=1+2*(value%9))
        yield dict(active=value,midi=1)
        yield dict(active=1,midi=value)
        for lane in range(4):yield dict(random_seed=value<<(lane*8),selected_char=1+2*((value+lane)%9))
    for lo in (0,1,0x7FFF,0x8000,0xFFFF):
        for hi in (0,1,0x7FFF,0x8000,0xFFFF):
            for char in range(19):yield dict(random_seed=(hi<<16)|lo,selected_char=char)
    for mask in range(128):
        for value in (1,0x80,0xFF):
            yield dict(seen=[value if mask>>i&1 else 0 for i in range(7)],selected_char=1+2*(mask%9))
    for bit in range(32):
        for value in (1<<bit,0xFFFFFFFF^(1<<bit)):
            yield dict(random_seed=value,selected_char=1+2*(bit%9))
    for segment in (0x5000,0x6000):
        for off in (0,0x31,0xFF80):
            for f in (2,0x202,0x402,0xED7):
                for response in (0,0x100,0x8000,0xFFFF):
                    yield dict(resseg=segment,resoff=off,flags=f,selection_ax=response,status=(off^response)&65535)
    for response in (0,1,0x100,0x8000,0x80FF,0xFFFF):
        for value in (0,0x7FFF,0x8000,0xFFFF):
            yield dict(selection_ax=response,status=value,random_seed=(value<<16)|value)


def verify(target,candidate):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(mz,load)
            try:
                trace=hashlib.sha256();counts=dict(terminal=0,nonterminal=0,retries=0);maximum_random=0
                for count,options in enumerate(cases(),1):
                    options=dict(options);options.setdefault('flags',(2,0x202,0x402,0xED7)[count%4])
                    row=m.run(seed=0x1357 if count&1 else 0xECA8,stack=0x80 if count&1 else 0xFFF0,**options)
                    counts['nonterminal' if row['nonterminal'] else 'terminal']+=1;counts['retries']+=row['retries']
                    maximum_random=max(maximum_random,row['random_calls']);trace.update(json.dumps(row,sort_keys=True).encode())
                ordinary=count
                # These are three consecutive calls on the same actual memory.
                # Selector cancellation after the held prefix is independently valid.
                for char in range(1,19,2):
                    for options in (dict(selected_char=char),dict(selected_char=char,reenter=True),
                                    dict(selected_char=char,reenter=True,selection_ax=0xA580)):
                        row=m.run(**options);count+=1
                        counts['nonterminal' if row['nonterminal'] else 'terminal']+=1;counts['retries']+=row['retries']
                        maximum_random=max(maximum_random,row['random_calls']);trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.owned and m.nested_covered==m.nested,'all caller and real nested helper instruction bytes execute')
                loads.append(dict(load_segment=load,cases=count,ordinary_cases=ordinary,actual_consecutive_reentry_cases=27,
                    terminal_cases=counts['terminal'],nonterminal_cases=counts['nonterminal'],retry_paths=counts['retries'],
                    covered_owner_bytes=len(m.covered),executed_nested_bytes=len(m.nested_covered),
                    maximum_observed_stack_depth=m.maximum_stack,maximum_actual_random_calls=maximum_random,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent target/candidate story observations')
    return dict(images=2,functions=1,code_bytes=SIZE,cases_per_image=sum(o['cases'] for o in observations[0]),
        exhaustive_selected_character_BYTE=256,exhaustive_selection_AL=256,exhaustive_rank_BYTE=256,
        exhaustive_sound_state_BYTE=256,exhaustive_each_seed_BYTE_lane=256,seen_masks=128,
        executed_owner_bytes=SIZE,executed_nested_bytes=sum(n for _,n in HELPERS),maximum_private_stack_window=48,
        closed_nonterminal_candidate_domain=7,all_32bit_seeds_termination_proved=False,
        character_selection_implementation_executed=False,successful_exec_or_physical_hardware_emulated=False,observations=observations[0])


def negative_controls(target):
    controls=(
      ('CPU-player-two',0x9A38,b'\1',b'\0',{}),('story-mode',0x9A3D,b'\1',b'\2',{}),
      ('credit-lives',0x9A42,b'\2',b'\3',{}),('opponent-sentinel',0x9A4C,b'\xFF',b'\0',{}),
      ('selection-result-is-AL',0x9A51,b'\xC0',b'\xE4',dict(selection_ax=0x100)),
      ('true-is-one',0x9A55,b'\1',b'\2',dict(selection_ax=0x80)),
      ('character-one-origin',0x9A63,b'\x48',b'\x90',dict(selected_char=2)),
      ('stage-seven-table-origin',0x9A6D,b'\xA0',b'\xA1',{}),
      ('full-DWORD-resident-seed',0x9A78,b'\x66',b'\x90',{}),
      ('full-DWORD-global-seed',0x9A7D,b'\x66',b'\x90',{}),
      ('seven-random-opponents',0x9A8B,b'\7',b'\6',{}),
      ('separate-candidate-local',0x9A92,b'\xFE',b'\xFC',{}),
      ('seen-table-origin',0x9A98,b'\x99',b'\x98',{}),
      ('exclude-fixed-opponent',0x9AA3,b'\x74',b'\x75',{}),
      ('seen-value-one',0x9AA9,b'\1',b'\2',{}),
      ('double-candidate',0x9AAE,b'\xC0',b'\xC1',{}),
      ('paletted-one-origin',0x9AAF,b'\x40',b'\x48',{}),
      ('self-palette-increment',0x9AD5,b'\xC0',b'\xC8',{}),
      ('six-random-stages',0x9ADD,b'\6',b'\5',{}),
      ('fixed-stage-seven-slot',0x9AF6,b'\x2F',b'\x2E',{}),
      ('Chiyuri-palette-slot',0x9B06,b'\x30',b'\x31',dict(selected_char=15)),
      ('Yumemi-palette-slot',0x9B1A,b'\x31',b'\x30',dict(selected_char=17)),
      ('all-nine-character-IDs-valid',0x9B32,b'\11',b'\10',{}),
      ('invalid-opponent-retries',0x9B35,b'\x8D',b'\x8E',{}),
      ('all-sixteen-score-digits',0x9B50,b'\20',b'\17',{}),
      ('remaining-credits',0x9B5B,b'\3',b'\2',{}),('slow-animation',0x9B60,b'\0',b'\1',{}),
      ('rank-multiplier',0x9B69,b'\31',b'\30',dict(rank=255)),('skill-base',0x9B6B,b'\x46',b'\x47',{}),
      ('song-stop-command',0x9B79,b'\0',b'\1',{}),
      ('far-NULL-exec-terminator',0x9B85,b'\x66',b'\x90',{}),
      ('exec-filename-pointer',0x9B8A,b'\x6F',b'\x70',{}),
      ('cdecl-twelve-byte-cleanup',0x9B97,b'\14',b'\10',{}),('false-is-zero',0x9B99,b'\0',b'\1',{}),
      ('real-random-multiplier',0x1D13,b'\x35',b'\x34',{}),
      ('real-random-low-carry',0x1D2E,b'\x13',b'\x03',dict(random_seed=(-pow(0x4E35,-1,65536))&65535)),
      ('real-random-nonnegative-result',0x1D3A,b'\x7F',b'\xFF',{}),
      ('real-cfg-write-size',0x99B6,b'\4',b'\10',{}),
      ('real-KAJA-MIDI-one',0xC414,b'\1',b'\0',dict(midi=1)),
      ('real-exit-page-order',0xBFCE,b'\1',b'\0',{}),
    )
    rejected=[]
    for name,at,old,new,options in controls:
        raw=bytearray(target.program_image);need(raw[at:at+len(old)]==old,'literal mutation anchor: '+name)
        raw[at:at+len(new)]=new;m=None
        try:
            try:
                m=Machine(replace(target,program_image=bytes(raw)),0x3000);m.run(**options)
            except ValueError:rejected.append(name)
            else:raise ValueError('OP story mutation survived: '+name)
        finally:
            if m:m.close()
    return dict(count=len(rejected),rejected=rejected,actual_guest_instruction_mutations=True,
        source_or_payload_patched=False,character_selection_code_mutated=False)
