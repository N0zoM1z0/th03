"""Main caller contracts composed with actual owned callee instructions.

The same physical Unicorn memory, registers and native return frames flow into
story/VS/score/attract. Callee specifications provide checked predicted outputs;
the caller never infers an expected result from a guest's final observation.
Music Room, fade/CDG/shrink and SDK graphics/text remain bounded interfaces.
"""
import hashlib,json,struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import UC_HOOK_INSN,UcError
from unicorn import x86_const as x
from lib.op_option_runtime import Machine as Base,Prediction as Policy,REG,GPRS,SEL,PUT,INOPT,INPUT,RESIDENT,ACTIVE,MIDI,DISABLED,FM,compare,add_flags
from lib.op_cfg_runtime import reply
from lib.op_main_menu_layout import START,SIZE,INSTRUCTIONS
from lib.op_nested_context import Context
from lib.op_story_runtime import Machine as Story
from lib.op_vs_runtime import Machine as VS
from lib.op_dispatch_runtime import Machine as Dispatch
from lib.op_attract_runtime import Machine as Attract
from lib.shared_input_layout import PROFILES
QUIT,INMAIN,INIT,LOCK=0x162,0x163,0x164,0x118A
SCREENS={0xB0DB:('shrink',False),0xB008:('fade',False),0xB3C3:('cdg',False),0xAC06:('music',True)}
CALLEES={'story':(0x9A17,0xA187),'vs':(0x9BDF,0xA19A),'score':(0x9E7F,0xA1BE),'wait':(0x9E16,0xA1A0)}

def need(v,m):
    if not v:raise ValueError('OP main menu contract: '+str(m))

class Prediction(Policy):
    def screen(self,name,sp,far=False):
        before=dict(self.r);self.calls+=1;after,flags=reply(before,self.calls,self.p['seed'],self.flags,self.p['status'])
        self.events.append(dict(kind='screen',name=name,sp=sp,args=(),far=far,request=before,mask=self.mask,flags=self.flags,post=after,post_flags=flags))
        self.r=after;self.flags,self.mask=flags,0x8D5
    def call(self,name,sp):
        address,ret=CALLEES[name]
        self.events.append(dict(kind='nested',name=name,address=address,return_rva=ret,sp=sp,args=(),request=dict(self.r),mask=self.mask,flags=self.flags))
        result=yield name
        self.r={n:v for n,v in result['registers'].items() if n!='sp'};self.flags,self.mask=result['flags'],result['flags_mask'];self.memory=result['memory']
        self.held=result['held']
        if self.held:self.r['sp']=result['registers']['sp']
    def main(self,sp):
        old=dict(self.r);self.held=False;self.r['bp']=sp-2;self.cmp(self.byte(INIT),0,True)
        if not self.byte(INIT):
            self.service('clear',sp-8);self.cmp(self.byte(INMAIN),0,True)
            if not self.byte(INMAIN):self.screen('shrink',sp-6)
            self.store(INMAIN,0);self.store(LOCK,0);self.r['si']=0;self.logical(0)
            for choice in range(6):
                self.cmp(choice,6);self.selection_ax();self.cmp(self.r['ax'],choice);attribute=0xE1 if self.r['ax']==choice else 1
                self.r['ax']=attribute;self.render('main',choice,attribute,sp-10);self.r['si']=choice+1
            self.cmp(6,6);self.store(PUT,0x5DD,2);self.store(INIT,1);self.store(LOCK,0)
        self.cmp(self.word(INPUT),0)
        if not self.word(INPUT):self.store(LOCK,1)
        self.cmp(self.byte(LOCK),0,True)
        if self.byte(LOCK):
            for bit,direction in ((1,0xFFFF),(2,1)):
                self.logical(self.word(INPUT)&bit,8)
                if self.word(INPUT)&bit:self.move(5,direction,sp-10)
            self.logical((self.word(INPUT)>>8)&0x20,8);confirm=bool(self.word(INPUT)&0x2000)
            if not confirm:self.logical(self.word(INPUT)&0x20,8);confirm=bool(self.word(INPUT)&0x20)
            if confirm:
                self.selection_ax();selection=self.r['ax'];self.r['bx']=selection;self.cmp(selection,5)
                if selection<=5:
                    self.r['bx']=2*selection;self.flags=(self.flags&0x600)|add_flags(selection,selection)|2;self.mask=0x8D5
                    if selection in (0,1,2):
                        if selection==0:yield from self.call('story',sp-6)
                        elif selection==1:
                            self.les();self.put(0xC,1);self.put(0xD,1);yield from self.call('vs',sp-6)
                        else:self.screen('music',sp-8,True)
                        if self.held:return
                        self.screen('fade',sp-6);yield from self.call('wait',sp-6)
                        self.screen('cdg',sp-6);self.store(INIT,0);self.store(LOCK,0);self.store(INMAIN,1)
                        self.r['bp'],self.r['si']=old['bp'],old['si'];self.r['sp']=sp+2;return
                    if selection==3:yield from self.call('score',sp-6)
                    elif selection==4:self.store(INIT,0);self.store(INOPT,1);self.store(SEL,0)
                    elif selection==5:self.store(INIT,0);self.store(QUIT,1)
            self.logical((self.word(INPUT)>>8)&0x10,8)
            if self.word(INPUT)&0x1000:self.store(QUIT,1)
            self.cmp(self.word(INPUT),0)
            if self.word(INPUT):self.store(LOCK,0)
        self.r['bp'],self.r['si']=old['bp'],old['si'];self.r['sp']=sp+2

class Machine(Base):
    def __init__(self,mz,load):
        self.active_child=None;super().__init__(mz,load)
        self.owned=set(range(START,START+INSTRUCTIONS));rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[START:START+INSTRUCTIONS],START))
        need(sum(i.size for i in rows)==INSTRUCTIONS,'all main instruction boundaries')
        self.instructions.update({i.address:i.size for i in rows});self.covered=set();self.nested_covered=set()
        self.children={name:cls(mz,load) for name,cls in (('story',Story),('vs',VS),('score',Dispatch),('wait',Attract))}
        for child in self.children.values():
            # Drop only its unused private UC/hooks. All execution below uses
            # the caller's one actual UC; no address or register proxy exists.
            for hook in child.hooks:child.uc.hook_del(hook)
            child.hooks=[];child.uc=self.uc
        self.hooks.append(self.uc.hook_add(UC_HOOK_INSN,self.out,None,1,0,x.UC_X86_INS_OUT))
    def close(self):
        for child in self.children.values():child.uc=None
        self.children={};super().close()
    def outside_stack(self,expected):
        actual=bytes(self.uc.mem_read(0,1<<20));lo,hi=0x70000+self.stack-96,0x70000+self.stack
        expected[lo:hi]=actual[lo:hi];need(actual==expected,'complete root memory outside 96 private stack bytes')
    def code(self,uc,address,size,data):
        self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
        if self.active_child is not None:self.active_child.code(uc,address,size,data);return
        try:
            rva=address-self.base
            if self.index<len(self.expected.events):
                e=self.expected.events[self.index]
                if e['kind']=='nested' and rva==e['address']:
                    self.check_regs(e['request'],e['mask'],e['flags']);self.frame(e,False);self.outside_stack(self.expected.memory)
                    ip=int.from_bytes(uc.mem_read(0x70000+e['sp'],2),'little');need(self.cs*16+ip==self.base+e['return_rva'],'exact actual caller continuation')
                    self.pending=e;self.index+=1;uc.emu_stop();return
            if rva in SCREENS:
                name,far=SCREENS[rva];e=self.peek('screen');need((name,far)==(e['name'],e['far']),'bounded screen sequence')
                self.check_regs(e['request'],e['mask'],e['flags']);sp,ip,cs=self.frame(e,far);self.index+=1
                for n in ('ax','bx','cx','dx','es'):uc.reg_write(REG[n],e['post'][n])
                uc.reg_write(x.UC_X86_REG_EFLAGS,e['post_flags']);uc.reg_write(REG['sp'],sp+(4 if far else 2));uc.reg_write(REG['cs'],cs);uc.reg_write(REG['ip'],ip);return
            super().code(uc,address,size,data)
        except Exception as error:self.fail(error)
    def write(self,uc,access,address,size,value,data):
        if self.active_child is not None:self.active_child.write(uc,access,address,size,value,data);return
        try:
            if 0x70000+self.stack-96<=address and address+size<=0x70000+self.stack:
                self.maximum_stack=max(self.maximum_stack,0x70000+self.stack-address);return
            e=self.peek('store');need(e==dict(kind='store',address=address,size=size,value=value),'exact ordered caller store');self.index+=1
        except Exception as error:self.fail(error)
    def interrupt(self,uc,vector,data):
        if self.active_child is not None:self.active_child.interrupt(uc,vector,data)
        else:super().interrupt(uc,vector,data)
    def out(self,uc,port,size,value,data):
        if self.active_child is not None:self.active_child.out(uc,port,size,value,data)
        else:self.fail('unexpected port outside real callee')
    def run_child(self,event):
        name=event['name'];child=self.children[name];regs=dict(event['request'],sp=event['sp'])
        full={n:self.high[n]|regs[n] for n in GPRS};ctx=Context(bytearray(self.expected.memory),regs,full,event['flags'],event['mask'],event['sp'],self.base+event['return_rva'],bytes(self.file))
        self.active_child=child
        try:
            p=dict(seed=self.seed,status=self.status,_context=ctx)
            if name=='story':row=child.run(selection_ax=self.p['selection_ax'],selected_char=self.p['selected_char'],random_seed=self.p['random_seed'],rank=self.p['rank'],**p)
            elif name=='vs':
                resoff,resseg,base=ctx.resident(child);mode=ctx.memory[base+0x28]
                row=child.run(selection_ax=self.p['selection_ax'],samples=() if mode>=128 else self.p['vs_samples'],**p)
            elif name=='score':row=child.run('score_menu',**p)
            else:row=child.run(samples=self.p['wait_samples'],**p)
            result=child.contract_result;need(result is not None,'callee exported an independently verified result')
            self.nested_observations.append(dict(name=name,observation=row));self.file=bytearray(result['file'])
            self.high={n:result['full_registers'][n]&0xFFFF0000 for n in GPRS};return result
        finally:self.active_child=None
    def run(self,*,selection=0,input=0,initialized=1,allowed=1,in_main=0,in_option=0,quit=0,callback='main',rank=0,bgm=0,key=0,active=1,midi=0,mode=0,selection_ax=1,selected_char=1,random_seed=0x12345678,vs_samples=((0x20,0,0,0),),wait_samples=((1,0,0,0),),seed=0x1357,status=0xFFFF,flags=0x202,stack=0xF800,resseg=0x6000,resoff=0x31,reenter=False):
        p=dict(locals());p.pop('self');self.p=p;self.stack,self.flags,self.seed,self.status=stack,flags,seed,status
        need(all(0<=p[n]<=255 for n in ('selection','initialized','allowed','in_main','in_option','quit','rank','bgm','key','active','midi','mode','selected_char')),'BYTE caller/resident domain')
        need(0<=input<=65535 and 0<=selection_ax<=65535 and 0<=random_seed<=0xFFFFFFFF and 0x100<=stack<=0xFFF0 and callback in ('main','option') and resseg in (0x5000,0x6000) and 0<=resoff<=0xFF80,'bounded WORD/DWORD, callback and disjoint memory profiles')
        if not reenter:
            self.uc.mem_write(0,bytes(self.initial));self.file=bytearray(b'\x02\x01\x03\x48\x57\0\x50\xA7')
            self.uc.mem_write(self.data+RESIDENT,struct.pack('<HH',resoff,resseg));res=resseg*16+resoff;self.uc.mem_write(res,b'\xA5'*0x60)
            for off,value in ((SEL,selection),(INIT,initialized),(LOCK,allowed),(INMAIN,in_main),(INOPT,in_option),(QUIT,quit),(ACTIVE,active),(MIDI,midi)):
                self.uc.mem_write(self.data+off,bytes((value,)))
            self.uc.mem_write(self.data+PUT,struct.pack('<H',0x5DD if callback=='main' else 0x657))
            for off,value in ((0xB,rank),(0x15,bgm),(0x16,key),(0x28,mode)):self.uc.mem_write(res+off,bytes((value,)))
            self.uc.mem_write(res+0x10,struct.pack('<I',random_seed));self.uc.mem_write(self.data+PROFILES['op']['presence'],b'\0\0')
        self.uc.mem_write(0x70000+stack-96,b'\xD3'*96);self.uc.mem_write(0x70000+stack,b'\xFF\xFF\x5A\xA5');self.uc.mem_write(self.data+INPUT,struct.pack('<H',input))
        regs={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)};regs['sp']=stack;regs.update(cs=self.cs,ds=self.ds,es=seed,ss=0x7000,fs=seed^0xA55A,gs=seed^0x5AA5)
        self.high={n:(seed^0x5AA5)<<16 for n in GPRS}
        for n in GPRS:self.uc.reg_write(GPRS[n],self.high[n]|regs[n])
        for n in ('cs','ds','es','ss','fs','gs'):self.uc.reg_write(REG[n],regs[n])
        self.uc.reg_write(x.UC_X86_REG_EFLAGS,flags);self.expected=Prediction(self.uc.mem_read(0,1<<20),regs,p,self.load)
        self.index,self.error,self.returned,self.pending=0,None,False,None;self.nested_observations=[]
        plan=self.expected.main(stack)
        try:next(plan);planned=True
        except StopIteration:planned=False
        resume=START
        while True:
            try:self.uc.emu_start(self.base+resume,1<<20,count=100000)
            except UcError as e:raise ValueError('OP main menu guest fault') from e
            need(self.error is None,self.error or 'guest error')
            if self.pending is None:break
            event=self.pending;self.pending=None;result=self.run_child(event)
            try:plan.send(result);planned=True
            except StopIteration:planned=False
            if result['held']:break
            resume=event['return_rva']
        need(not planned and self.index==len(self.expected.events),'complete independent caller continuation plan')
        need(self.returned!=self.expected.held,'actual near return or independently proved callee loop')
        self.check_regs(self.expected.r,self.expected.mask,self.expected.flags)
        need(all(self.uc.reg_read(GPRS[n])==self.high[n]|self.expected.r[n] for n in GPRS),'complete final DWORD registers including ESP')
        self.outside_stack(self.expected.memory)
        return dict(returned=self.returned,held=self.expected.held,registers=self.registers(),full_registers={n:self.uc.reg_read(r) for n,r in GPRS.items()},flags=self.uc.reg_read(x.UC_X86_REG_EFLAGS)&(self.expected.mask|0x600),flags_mask=self.expected.mask,events=len(self.expected.events),plan_sha256=hashlib.sha256(json.dumps(self.expected.events,sort_keys=True).encode()).hexdigest(),nested=self.nested_observations,file_hex=self.file.hex())

def cases():
    for selection in range(256):
        for input in (0,1,2,3,0x20,0x2000,0x1000):yield dict(selection=selection,input=input)
    for selection in (0,1,2,3,4,5,128,255):
        for arrows in range(4):
            for buttons in (0,0x20,0x2000,0x1000,0x3020,0x8000):yield dict(selection=selection,input=arrows|buttons)
    for initialized in (0,1,255):
        for allowed in (0,1,255):
            for in_main in (0,1,255):
                for input in (0,3,0x20,0x1000,0x3020):yield dict(initialized=initialized,allowed=allowed,in_main=in_main,input=input,selection=4)
    for mode in (0,127,128,129,130,131,255):
        for selection_ax in (0,1,0x100,0xA580,0xFFFF):yield dict(selection=1,input=0x20,mode=mode,selection_ax=selection_ax)
    for selected_char in (0,1,2,15,17,21,255):
        for selection_ax in (0,1,0x100,0xA580):yield dict(input=0x3020,selected_char=selected_char,selection_ax=selection_ax,rank=255)
    for callback in ('main','option'):
        for selection in (0,1,2,3,4,5,128,255):
            for input in (1,2,3,0x23):yield dict(callback=callback,selection=selection,input=input,bgm=2,key=2,rank=3)
    for seed in (0,1,0x1357,0xECA8,0x8000,0xFFFF):
        for flags in (2,0x202,0x402,0xED7):
            for stack in (0x100,0xFFF0):
                for selection in range(6):yield dict(selection=selection,input=0x3020,seed=seed,flags=flags,stack=stack,resseg=0x5000,resoff=0xFF80,status=seed)
    yield dict(selection=2,input=0x20,wait_samples=((0,0,0,0),)*520+((1,0,0,0),))
    yield dict(selection=1,input=0x20,selection_ax=0,vs_samples=((3,0,0,0),(0,0,0,0),(0x20,0,0,0)))
    for input in (0,0x20,0x1000,0x8000):
        for quit in (0,1,255):yield dict(input=input,quit=quit,initialized=0,selection=255)


def verify(target,candidate):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(mz,load);trace=hashlib.sha256();calls={name:0 for name in CALLEES};terminal=held=0;count=0
            def record(row):
                nonlocal terminal,held,count
                trace.update(json.dumps(row,sort_keys=True).encode());count+=1;terminal+=int(row['returned']);held+=int(row['held'])
                for child in row['nested']:calls[child['name']]+=1
            try:
                for p in cases():
                    try:record(m.run(**p))
                    except ValueError as e:raise ValueError(f'main {p}: {e}') from e
                ordinary=count
                # Actual main-entry reentry: release reinitializes the menu,
                # then a second returning story consumes the persistent seen
                # array and reaches the independently closed retry loop.
                for selected_char in (0,1,15,17):
                    first=m.run(input=0x20,selection_ax=0,selected_char=selected_char)
                    need(first['returned'],'reentry follows an actual completed caller return');record(first);ordinary+=1
                    record(m.run(input=0,reenter=True))
                    record(m.run(input=0x20,reenter=True,selection_ax=0,selected_char=selected_char))
                    need(m.expected.held,'actual repeated story reaches its proved blocked candidate domain')
                need(m.covered==m.owned,'all 278 main instruction bytes execute, excluding thirteen inline bytes')
                need(all(calls.values()),'all four owned caller boundaries execute real instructions')
                loads.append(dict(load_segment=load,cases=count,ordinary_cases=ordinary,actual_consecutive_reentry_cases=count-ordinary,terminal_cases=terminal,nonterminal_cases=held,executed_owner_bytes=len(m.covered),inline_non_instruction_bytes=13,nested_calls=calls,executed_callee_bytes={name:len(child.covered) for name,child in m.children.items()},maximum_stack_depth=m.maximum_stack,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent target/candidate full-state main observations')
    return dict(images=2,functions=1,code_bytes=291,instruction_bytes=278,inline_non_instruction_bytes=13,cases_per_image=sum(o['cases'] for o in observations[0]),observations=observations[0],exhaustive_selection_BYTE=256,shared_physical_machine=True,synthetic_owned_callee_returns=False,ignored_private_stack_bytes=96,whole_product_accepted=False)


def negative_controls(target):
    from dataclasses import replace
    controls=(
      ('preserve-caller-BP',0xA0E0,6,{}),
      ('main-init-condition',0xA0E9,1,dict(initialized=0)),
      ('shrink-only-after-option',0xA0F5,1,dict(initialized=0,in_main=1)),
      ('initial-in-main-clear',0xA0FE,1,dict(initialized=0)),
      ('all-six-main-choices',0xA120,1,dict(initialized=0)),
      ('live-main-callback-pointer',0xA127,1,dict(initialized=0)),
      ('mark-initialized',0xA12D,1,dict(initialized=0)),
      ('zero-input-releases-lock',0xA13E,1,dict(allowed=0)),
      ('locked-input-does-not-dispatch',0xA145,1,dict(input=0x20,selection=4,allowed=0)),
      ('UP-before-DOWN',0xA14C,1,dict(input=3,selection=0)),
      ('DOWN-independent-mask',0xA15A,2,dict(input=2)),
      ('confirm-high-BYTE-mask',0xA168,32,dict(input=0x2000,selection=4)),
      ('confirm-low-BYTE-mask',0xA16F,32,dict(input=0x20,selection=4)),
      ('signed-selection-extension',0xA175,8,dict(input=0x20,selection=255)),
      ('switch-bound-is-unsigned',0xA17B,8,dict(input=0x20,selection=255)),
      ('switch-index-is-WORD-times-two',0xA17E,8,dict(input=0x20,selection=1)),
      ('real-story-entry',0xA185,1,dict(input=0x20)),
      ('VS-player-one-char-init',0xA191,1,dict(input=0x20,selection=1)),
      ('VS-player-two-char-init',0xA196,1,dict(input=0x20,selection=1)),
      ('real-VS-entry',0xA198,1,dict(input=0x20,selection=1)),
      ('fade-after-screen',0xA19B,1,dict(input=0x20)),
      ('real-attract-entry',0xA19E,1,dict(input=0x20)),
      ('CDG-after-wait',0xA1A1,1,dict(input=0x20)),
      ('clear-init-after-screen',0xA1A7,1,dict(input=0x20)),
      ('clear-lock-after-screen',0xA1AC,1,dict(input=0x20)),
      ('mark-main-after-screen',0xA1B1,1,dict(input=0x20)),
      ('native-relaxation-preserves-CF',0xA1B4,0x69,dict(input=0x20,selection=2)),
      ('far-Music-Room-pushes-CS',0xA1B5,0x10,dict(input=0x20,selection=2)),
      ('real-Music-Room-entry',0xA1B7,1,dict(input=0x20,selection=2)),
      ('real-score-entry',0xA1BC,1,dict(input=0x20,selection=3)),
      ('option-entry-state',0xA1C9,1,dict(input=0x20,selection=4)),
      ('option-selection-zero',0xA1CE,1,dict(input=0x20,selection=4)),
      ('quit-state',0xA1DA,1,dict(input=0x20,selection=5)),
      ('cancel-is-independent',0xA1DF,16,dict(input=0x1000)),
      ('nonzero-input-locks-again',0xA1F2,1,dict(input=0x8000)),
      ('near-main-return',0xA1F5,8,{}),
    )
    rejected=[]
    for name,at,mask,p in controls:
        raw=bytearray(target.program_image);raw[at]^=mask;m=Machine(replace(target,program_image=bytes(raw)),0x3000)
        try:
            try:m.run(**p)
            except ValueError:rejected.append(name)
            else:raise ValueError('OP main menu instruction mutation survived: '+name)
        finally:m.close()
    tables=[]
    for selection in range(6):
        at=0xA1F7+2*selection;raw=bytearray(target.program_image);raw[at:at+2]=(0x8D1 if selection!=5 else 0x8C0).to_bytes(2,'little');m=Machine(replace(target,program_image=bytes(raw)),0x3000)
        try:
            try:m.run(input=0x20,selection=selection)
            except ValueError:tables.append(selection)
            else:raise ValueError('OP main menu table mutation survived: '+str(selection))
        finally:m.close()
    return dict(actual_instruction_mutations=len(controls),rejected=rejected,consumed_table_WORD_mutations=len(tables),rejected_table_entries=tables,separator_executed=False)
