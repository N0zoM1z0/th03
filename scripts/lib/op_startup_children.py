"""Borrow existing OP callee contracts without resetting the shared CPU state.

Old standalone witnesses and their private-window bounds remain unchanged. No
register/address proxy or fresh callee fixture is introduced by these adapters.
"""
import hashlib
import json
from unicorn import UcError
from unicorn import x86_const as x
from lib.op_main_menu_runtime import Machine as MainMachine,Prediction as MainPrediction,START as MAIN
from lib.op_option_runtime import Machine as OptionMachine,Prediction as OptionPrediction,OPTION,REG,GPRS
from lib.op_nested_context import Context
from lib.op_startup_state import need


class Main(MainMachine):
    def code(self,uc,address,size,data):
        if self.active_child is None and address==getattr(self,'startup_boundary',None):
            self.returned=True
            uc.emu_stop()
            return
        super().code(uc,address,size,data)

    def run_context(self,context,options):
        context.enter(self)
        self.startup_boundary=context.return_address
        self.stack,self.flags,self.seed,self.status=context.stack,context.flags,options['seed'],options['status']
        off,seg,res=context.resident(self)
        p=dict(options,flags=context.flags,stack=context.stack,resoff=off,resseg=seg,
            rank=context.memory[res+0xB],bgm=context.memory[res+0x15],key=context.memory[res+0x16],
            mode=context.memory[res+0x28],random_seed=int.from_bytes(context.memory[res+0x10:res+0x14],'little'))
        self.p=p
        self.file=bytearray(context.file)
        self.high={n:context.full_registers[n]&0xFFFF0000 for n in GPRS}
        self.expected=MainPrediction(context.memory,context.registers,p,self.load)
        self.index,self.error,self.returned,self.pending=0,None,False,None
        self.nested_observations=[]
        plan=self.expected.main(self.stack)
        try:
            next(plan)
            planned=True
        except StopIteration:
            planned=False
        resume=MAIN
        while True:
            try:
                self.uc.emu_start(self.base+resume,1<<20,count=100000)
            except UcError as error:
                raise ValueError('OP startup main-menu guest fault') from error
            need(self.error is None,self.error or 'main child failure')
            if self.pending is None:
                break
            event=self.pending
            self.pending=None
            result=self.run_child(event)
            try:
                plan.send(result)
                planned=True
            except StopIteration:
                planned=False
            if result['held']:
                break
            resume=event['return_rva']
        need(not planned and self.index==len(self.expected.events),'complete independent main-menu plan')
        need(self.returned!=self.expected.held,'real child near return or separately proved held callee')
        self.check_regs(self.expected.r,self.expected.mask,self.expected.flags)
        need(all(self.uc.reg_read(GPRS[n])==self.high[n]|self.expected.r[n] for n in GPRS),'child DWORD results including ESP')
        self.outside_stack(self.expected.memory)
        if self.expected.held:
            # The nested story contract already proves its closed retry loop.
            # Its live SP includes the main frame and must propagate verbatim;
            # Context.accept's direct-callee stack-8 rule is not transitive.
            regs=dict(self.expected.r,fs=context.registers['fs'],gs=context.registers['gs'])
            full={n:self.high[n]|regs[n] for n in GPRS}
            need(all(self.uc.reg_read(REG[n])==regs[n] for n in ('cs','ds','es','ss','fs','gs')),
                 'all held descendant segment results')
            need(self.uc.reg_read(x.UC_X86_REG_EFLAGS)&0x600==context.flags&0x600,'held IF/DF')
            self.contract_result=dict(registers=regs,full_registers=full,
                flags=(self.expected.flags&self.expected.mask)|(context.flags&0x600)|2,
                flags_mask=self.expected.mask,memory=bytearray(self.expected.memory),file=bytes(self.file),held=True)
        else:
            context.accept(self,self.expected.r,self.high,self.expected.mask,self.expected.flags,self.expected.memory,
                           file=self.file)
        return dict(returned=self.returned,held=self.expected.held,events=len(self.expected.events),
            plan_sha256=hashlib.sha256(json.dumps(self.expected.events,sort_keys=True).encode()).hexdigest(),nested=self.nested_observations)


class Option(OptionMachine):
    def code(self,uc,address,size,data):
        if address==getattr(self,'startup_boundary',None):
            self.returned=True
            uc.emu_stop()
            return
        super().code(uc,address,size,data)

    def run_context(self,context,options):
        context.enter(self)
        self.startup_boundary=context.return_address
        self.stack,self.flags=context.stack,context.flags
        off,seg,res=context.resident(self)
        p=dict(options,flags=context.flags,stack=context.stack,resoff=off,resseg=seg,
            driver_ax=options['driver_ax'],rank=context.memory[res+0xB],bgm=context.memory[res+0x15],key=context.memory[res+0x16])
        self.high={n:context.full_registers[n]&0xFFFF0000 for n in GPRS}
        self.expected=OptionPrediction(context.memory,context.registers,p,self.load).run('option',self.stack)
        self.index,self.error,self.returned=0,None,False
        try:
            self.uc.emu_start(self.base+OPTION,1<<20,count=100000)
        except UcError as error:
            raise ValueError('OP startup option-menu guest fault') from error
        need(self.error is None,self.error or 'option child failure')
        need(self.returned and self.index==len(self.expected.events),'complete actual option return')
        self.check_regs(self.expected.r,self.expected.mask,self.expected.flags)
        need(all(self.uc.reg_read(GPRS[n])==self.high[n]|self.expected.r[n] for n in GPRS),'all child DWORD results')
        memory=bytes(self.uc.mem_read(0,1<<20))
        expected=self.expected.memory
        lo,hi=0x70000+self.stack-64,0x70000+self.stack
        expected[lo:hi]=memory[lo:hi]
        need(memory==expected,'all memory outside inherited64-byte private option window')
        context.accept(self,self.expected.r,self.high,self.expected.mask,self.expected.flags,expected,file=context.file)
        return dict(events=self.index,event_sha256=hashlib.sha256(json.dumps(self.expected.events,sort_keys=True).encode()).hexdigest())
