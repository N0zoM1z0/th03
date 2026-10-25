"""An explicit near-call input contract for one shared physical Unicorn machine.

No address projection, fresh fixture stores or synthetic callee return occurs.
The caller supplies independent expected registers/memory and an actual return
boundary. Only the existing per-scope private stack input remains unconstrained.
Each callee still executes its maintained instructions and checks its own
independent specification before exposing a predicted result to the caller.
"""
from dataclasses import dataclass
import struct
from unicorn import x86_const as x
GPRS={n:getattr(x,'UC_X86_REG_E'+n.upper()) for n in ('ax','bx','cx','dx','si','di','bp','sp')}
SEGMENTS={n:getattr(x,'UC_X86_REG_'+n.upper()) for n in ('cs','ds','es','ss','fs','gs')}

def need(v,m):
    if not v:raise ValueError('OP nested context: '+str(m))

def configure(machine,context):
    machine.contract_result=None
    machine.boundary_return=machine.cs*16+0xFFFF if context is None else context.return_address
    if context is not None:context.enter(machine)

@dataclass
class Context:
    memory: bytearray
    registers: dict
    full_registers: dict
    flags: int
    flags_mask: int
    stack: int
    return_address: int
    file: bytes=b'\x02\x01\x03\x48\x57\0\x50\xA7'

    def enter(self,machine):
        uc=machine.uc
        need(self.registers['ss']==0x7000 and 80<=self.stack<=0xFFF0,'existing disjoint callee stack profile')
        need(all(uc.reg_read(r)==self.full_registers[n] for n,r in GPRS.items()),'independent entering DWORD registers including ESP')
        need(all(uc.reg_read(r)==self.registers[n] for n,r in SEGMENTS.items()),'all six independent entering segments')
        need(self.full_registers['sp']&65535==self.stack,'actual near frame SP')
        need(uc.reg_read(x.UC_X86_REG_EFLAGS)&self.flags_mask==self.flags&self.flags_mask,'entering defined flags')
        need(bytes(uc.mem_read(0,1<<20))==self.memory,'all caller-supplied physical input bytes')
        ip=struct.unpack('<H',self.memory[0x70000+self.stack:0x70000+self.stack+2])[0]
        need(self.registers['cs']*16+ip==self.return_address,'actual unmodified near return word')

    def resident(self,machine):
        off,seg=struct.unpack('<HH',self.memory[machine.data+0x2464:machine.data+0x2468])
        need(seg in (0x5000,0x6000) and 0<=off<=0xFF80,'disjoint far resident input')
        return off,seg,seg*16+off

    def initial(self):
        return ({n:self.registers[n] for n in (*tuple(GPRS)[:-1],'cs','ds','es','ss')},
                {n:self.full_registers[n]&0xFFFF0000 for n in tuple(GPRS)[:-1]})

    def accept(self,machine,registers,high,mask,flags,memory,*,file=None,held=False):
        # This result is built from the callee's independent specification.
        # Actual returning values are checked, never used as predicted outputs.
        regs=dict(registers,sp=self.stack-8 if held else self.stack+2)
        regs.update({n:self.registers[n] for n in ('fs','gs')})
        full={n:high[n]|regs[n] for n in high}
        full['sp']=(self.full_registers['sp']&0xFFFF0000)|regs['sp']
        need(all(machine.uc.reg_read(r)==full[n] for n,r in GPRS.items()),'complete independent composed DWORD result')
        need(all(machine.uc.reg_read(r)==regs[n] for n,r in SEGMENTS.items()),'composed six-segment preservation')
        f=machine.uc.reg_read(x.UC_X86_REG_EFLAGS)
        need(f&mask==flags&mask and f&0x600==self.flags&0x600,'composed defined flags / IF / DF')
        if not held:need(machine.uc.reg_read(x.UC_X86_REG_CS)*16+machine.uc.reg_read(x.UC_X86_REG_IP)==self.return_address,'stops before actual caller continuation')
        machine.contract_result=dict(registers=regs,full_registers=full,flags=(flags&mask)|(self.flags&0x600)|2,
            flags_mask=mask,memory=bytearray(memory),file=bytes(self.file if file is None else file),held=held)
