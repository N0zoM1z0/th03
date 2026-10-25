"""One physical CPU for roll and its owned callees; external entries stay bounded."""
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import UcError
from unicorn.x86_const import *
from lib.decoded_mainl_staff_callers_runtime import Machine as Parent,CONTEXT as CALLERS
from lib.decoded_mainl_staff_pair_runtime import CONTEXT as PAIR
from lib.decoded_mainl_snow_layout import ENTRIES as SNOW
from lib.decoded_mainl_cdg_layout import ENTRIES as CDG
from lib.decoded_mainl_staff_roll_layout import CS,DS,START,SIZE
from lib.decoded_mainl_staff_roll_services import sound_reply,sample_reply,need
from lib.decoded_mainl_cdg_runtime import effects,CLEANUP
from lib.decoded_mainl_staff_verdict_runtime import renderer_reply,reply_flags,RENDER
from lib.decoded_mainl_pi_free_runtime import address
from lib.decoded_mainl_pi_runtime import ARITH
from lib.decoded_mainl_root_helpers_runtime import REG,GPRS

NODES=dict(PAIR)
NODES.update({CS*16+at:(name,n) for name,at,n in (
    ('reset',0x2576,26),('single',0x29C2,229),('pair',0x2AA7,358),('hold',0x2C0D,139),
    ('gallery',0x298E,52),('verdict',0x2C98,389),('roll',START,SIZE))})
NODES.update({0xC7E*16+at:(name,n) for name,at,n in (
    ('sound-load',0xA0,112),('delay',0x372,21),('kaja',0x6E2,30),('input',0xDC2,36))})
NODES.update({0xC7E*16+CDG[name][0]:(name,CDG[name][1]) for name in ('single','single_noalpha','free')})
# Names with shared spelling retain distinct physical entries.
ROLL_ENTRY={'load':0xC7E*16+0xA0,'kaja':0xC7E*16+0x6E2,'delay':0xC7E*16+0x372,
    'input':0xC7E*16+0xDC2,'single':CS*16+0x29C2,'pair':CS*16+0x2AA7,
    'hold':CS*16+0x2C0D,'gallery':CS*16+0x298E,'verdict':CS*16+0x2C98}
EXTERNAL={'palette-black':0x57A,'palette-show':0x17D0,'palette-entry':0x1A68,'volume':0xC7E*16+0x84}
FILE_ENTRIES={0x966:'open',0x8B2:'read',0x9A2:'seek',0x846:'close',0x21AE:'alloc',0x22B2:'free'}
SAMPLE_ENTRIES={0xC7E*16+0x388:'sense',0x2AEA:'js'}


def external_reply(regs,flags,options):
    out=dict(regs)
    value=options['box_seed']
    out.update(ax=value,cx=value^0x1234,dx=value^0x5AA5,es=0x6666)
    return out,(flags&0x600)|2|(value&ARITH)


class Machine(Parent):
    def __init__(self,image,load):
        super().__init__(image,load)
        self.instructions={}
        self.samples=set()
        self.returns=set()
        self.return_targets={}
        self.rep_offsets=set()
        self.seen=set()
        self.owner=set(range(CS*16+START,CS*16+START+SIZE))
        for at,(_,length) in NODES.items():
            ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[at:at+length],at))
            need(sum(i.size for i in ins)==length,'complete actual roll context instruction boundaries')
            self.instructions.update({i.address:i.size for i in ins})
            self.rep_offsets.update(i.address for i in ins if i.mnemonic=='rep stosw')
            self.samples.add(at)
            self.samples.update(i.address+i.size for i in ins if i.mnemonic in ('push','enter','pushf'))
            self.returns.update(i.address+i.size for i in ins if i.mnemonic in ('call','lcall'))
            for i in ins:
                if i.mnemonic=='call':
                    self.return_targets[i.address+i.size]=int(i.op_str,16)
                elif i.mnemonic=='lcall':
                    segment,ip=(int(v.strip(),16) for v in i.op_str.split(','))
                    self.return_targets[i.address+i.size]=segment*16+ip
        self.covered=set()

    def set_regs(self,registers):
        for name,value in registers.items():
            if name in REG and name!='ip':
                self.u.reg_write(REG[name],value)

    def far_return(self,cleanup):
        sp,ss=self.u.reg_read(REG['sp']),self.u.reg_read(REG['ss'])
        ip,cs=struct.unpack('<2H',bytes(self.u.mem_read(address(ss,sp),4)))
        self.u.reg_write(REG['sp'],sp+4+cleanup)
        self.u.reg_write(REG['cs'],cs)
        self.u.reg_write(REG['ip'],ip)

    def frame_event(self):
        if self.index<len(self.events) and self.events[self.index][0]=='far-frame':
            sp,ss=self.u.reg_read(REG['sp']),self.u.reg_read(REG['ss'])
            ip,cs=struct.unpack('<2H',bytes(self.u.mem_read(address(ss,sp),4)))
            self.event(('far-frame',address(ss,sp),ip,cs))

    def write(self,u,access,at,size,value,user):
        if self.index<len(self.events) and self.events[self.index][0]=='far-frame':
            try:
                _,dest,ip,cs=self.events[self.index]
                need(size==2 and (at,value) in ((dest,ip),(dest+2,cs)),'only actual native far return words')
            except Exception as error:
                self.fail(error)
            return
        super().write(u,access,at,size,value,user)

    def interrupt(self,u,number,user):
        try:
            event=self.events[self.index]
            if event[0]=='sound-interrupt':
                _,kind,want,_,_,mask=event
                self.event(('sound-interrupt',kind,number,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                regs,flags,writes=sound_reply(kind,self.regs(),u.reg_read(UC_X86_REG_EFLAGS),self.o)
                for at,raw in writes:
                    self.event(('song-bytes',at,raw.hex()))
                    u.mem_write(at,raw)
                self.set_regs(regs)
                u.reg_write(UC_X86_REG_EFLAGS,flags)
            else:
                need(event[0]=='pmd' and number==0x60,'explicit actual PMD gate interrupt')
                mask=ARITH|0x600
                self.event(('pmd',number,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                measure,writes,flags=self.o['schedule'][0]
                for off,raw in writes:
                    at=address(self.ds,off)
                    self.event(('pmd-write',at,raw.hex()))
                    u.mem_write(at,raw)
                u.reg_write(REG['ax'],measure)
                u.reg_write(UC_X86_REG_EFLAGS,(u.reg_read(UC_X86_REG_EFLAGS)&0x600)|2|(flags&ARITH))
        except Exception as error:
            self.fail(error)

    def code(self,u,at,size,user):
        try:
            offset=at-self.base
            if self.o.get('prepare_only') and at==self.cs*16+0x2EE8:
                self.returned=True
                u.emu_stop()
                return
            if offset==CS*16+0x3191 and self.index<len(self.events) and self.events[self.index][0]=='roll-input-prefix':
                event=self.events[self.index]
                mask=event[-1]
                self.event(('roll-input-prefix',event[1],self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                self.returned=True
                u.emu_stop()
                return
            if at==self.cs*16+0xFFFF:
                self.returned=True
                u.emu_stop()
                return
            if offset in self.rep_offsets and self.index<len(self.events) and self.events[self.index][0]=='rep-clear':
                need(self.instructions.get(offset)==size,'actual REP clear instruction')
                if offset not in self.seen:
                    self.covered.update(range(offset,offset+size))
                    self.seen.add(offset)
                return
            self.frame_event() if offset in NODES or offset in FILE_ENTRIES or offset in SAMPLE_ENTRIES or offset in EXTERNAL.values() or offset==RENDER[0]*16+RENDER[1] or offset==0xB9E else None
            sp,ss=u.reg_read(REG['sp']),u.reg_read(REG['ss'])
            if offset in self.samples:
                self.max_depth=max(self.max_depth,self.o['stack']-sp)
            event=self.events[self.index] if self.index<len(self.events) else None
            returned_target=self.return_targets.get(offset)
            returned_kind=NODES.get(returned_target,(None,))[0]
            if returned_kind=='sound-load':returned_kind='load'
            if event and ((event[0]=='owned-return' and event[1]==returned_kind) or
                          (event[0]=='renderer-return' and returned_target==RENDER[0]*16+RENDER[1])):
                mask=event[-1]
                item=(event[0],event[1],self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask) if event[0]=='owned-return' else (event[0],self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask)
                self.event(item)
                event=self.events[self.index] if self.index<len(self.events) else None
            if event and event[0]=='roll-entry' and offset==ROLL_ENTRY[event[1]]:
                _,kind,_,frame,_,mask=event
                self.event(('roll-entry',kind,self.regs(True),bytes(u.mem_read(address(ss,sp),len(bytes.fromhex(frame)))).hex(),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
            elif event and event[0]=='entry' and offset in NODES and event[1]==NODES[offset][0]:
                raw=bytes(u.mem_read(address(ss,sp),len(bytes.fromhex(event[3])))).hex()
                item=('entry',event[1],self.regs(True),raw)
                if len(event)==6:
                    item+=u.reg_read(UC_X86_REG_EFLAGS)&event[-1],event[-1]
                self.event(item)
                if offset in {0xC7E*16+CDG[k][0] for k in ('single','single_noalpha','free')}:
                    self.file_counts={}
                if event[1]=='tick':
                    self.polls=0
            elif event and event[0]=='color-entry' and offset==0xC36:
                self.event(('color-entry',self.regs(True),bytes(u.mem_read(address(ss,sp),8)).hex(),u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)))
            elif event and event[0]=='blit-entry' and offset in NODES and NODES[offset][0]==event[1]:
                self.event(('blit-entry',event[1],self.regs(True),bytes(u.mem_read(address(ss,sp),10)).hex(),u.reg_read(UC_X86_REG_EFLAGS)&ARITH))
            if offset in EXTERNAL.values() or offset==0xB9E:
                event=self.events[self.index]
                if offset==0xB9E:
                    self.event(('box',self.regs(True),bytes(u.mem_read(address(ss,sp),12)).hex(),u.reg_read(UC_X86_REG_EFLAGS)&(ARITH|0x600)))
                    cleanup=8
                else:
                    _,kind,_,frame,_,mask,cleanup=event
                    need(EXTERNAL[kind]==offset,'declared external entry')
                    self.event(('roll-external',kind,self.regs(True),bytes(u.mem_read(address(ss,sp),len(bytes.fromhex(frame)))).hex(),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask,cleanup))
                regs,flags=external_reply(self.regs(),u.reg_read(UC_X86_REG_EFLAGS),self.o)
                self.set_regs(regs)
                u.reg_write(UC_X86_REG_EFLAGS,flags)
                self.far_return(cleanup)
                return
            if offset in FILE_ENTRIES:
                kind=FILE_ENTRIES[offset]
                event=self.events[self.index]
                _,want,args,_,_,mask=event
                need(kind==want,'declared CDG file/heap entry')
                self.event(('call',kind,args,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                self.file_counts[kind]=self.file_counts.get(kind,0)+1
                regs,flags,writes=effects(kind,args,self.file_counts[kind],self.o['cdg'],self.regs(),u.reg_read(UC_X86_REG_EFLAGS))
                for dest,raw in writes:
                    self.event(('file-bytes',dest,raw.hex()))
                    u.mem_write(dest,raw)
                self.set_regs(regs)
                u.reg_write(UC_X86_REG_EFLAGS,flags)
                self.far_return(CLEANUP[kind])
                return
            if offset in SAMPLE_ENTRIES:
                kind=SAMPLE_ENTRIES[offset]
                event=self.events[self.index]
                mask=event[-1]
                self.event(('sample',kind,self.regs(True),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                from lib.decoded_mainl_staff_roll_services import INPUT
                values=dict(zip(('single','player1','player2','joystick'),self.o['sample'])) if kind=='sense' else dict(joystick=self.o['sample'][3])
                if kind=='sense':values['joystick']=0
                for name,value in values.items():
                    dest=address(self.ds,INPUT[name])
                    self.event(('sample-write',dest,value))
                    u.mem_write(dest,value.to_bytes(2,'little'))
                regs,flags=sample_reply(kind,self.regs(),u.reg_read(UC_X86_REG_EFLAGS),self.o)
                self.set_regs(regs)
                u.reg_write(UC_X86_REG_EFLAGS,flags)
                self.far_return(0)
                return
            if offset==RENDER[0]*16+RENDER[1]:
                event=self.events[self.index]
                _,count,_,_,_,mask=event
                self.event(('render-entry',count,self.regs(True),bytes(u.mem_read(address(ss,sp),14)).hex(),u.reg_read(UC_X86_REG_EFLAGS)&mask,mask))
                for index,off,raw in self.o['verdict_writes']:
                    if index==count:
                        dest=address(self.ds,off)
                        self.event(('renderer-write',dest,raw.hex()))
                        u.mem_write(dest,raw)
                for name,value in renderer_reply(self.o['reply_seed'],count).items():
                    u.reg_write(GPRS[name] if name in GPRS else REG[name],value)
                u.reg_write(UC_X86_REG_EFLAGS,2|(self.o['reply_flags']&(ARITH|0x600)))
                self.far_return(10)
                return
            if offset==0xC7E*16+0x37B:
                value=self.o['delay_ticks'][0]
                self.event(('delay-poll',value))
                u.mem_write(address(self.ds,0x144E),value.to_bytes(2,'little'))
            if offset==CS*16+0x270E:
                value=self.o['ticks'][0]
                self.event(('poll',value))
                u.mem_write(address(self.ds,0x144E),value.to_bytes(2,'little'))
            need(self.instructions.get(offset)==size,'only actual owned roll/context instructions: '+hex(offset))
            if offset not in self.seen:
                self.covered.update(range(offset,offset+size))
                self.seen.add(offset)
        except Exception as error:
            self.fail(error)
