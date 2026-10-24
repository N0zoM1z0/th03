"""Independent scalar renderer requests, register ABI and complete memory contract.

Actual renderer instructions and the native switch table execute. Gaiji/text
library replies are explicit register/flag interfaces; no physical TRAM pixels
or gaiji asset shapes are inferred.
"""
import hashlib,json,struct
from dataclasses import replace
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import UcError
from unicorn.x86_const import UC_X86_REG_EFLAGS
from lib.op_dispatch_runtime import Machine as BaseMachine,REG,GPRS,add_flags
from lib.op_cfg_runtime import RESIDENT,reply
from lib.shared_sound_runtime import compare
from lib.op_render_layout import ENTRIES
SERVICES={0xFCC:'gaiji',0x2254:'text'}
STRINGS={0xA9:'88898a8b8c8d8e8f00',0xB2:'88898a8b9697989900',0xBB:'929394958c8d8e8f00',
 0xDC:'30313200',0xE0:'33343536373800',0xE7:'4142434445464700',0xEF:'828384858600',0xF5:'3d3e3f4000',0xFA:'48494a00',
 0xFE:'6e6f7000',0x102:'4b4c4d4e00',0x107:'5c5d5e5f606100',0x113:'71727300',0x117:'7475767700',0x11C:'78797a00',0x120:'7b7c7d7e00',
 0x125:'cfcf5a5bcfcfcf00',0x12D:'cf4f505152cfcf00',0x135:'5354555657585900',0x14C:'68696c6d686900',0x153:'6a6b6c6d686900',0x15A:'68696c6d6a6b00',0x175:'202020202020202000'}
def need(v,m):
    if not v:raise ValueError('OP renderer contract: '+str(m))
def logic(v):return (4 if (v&255).bit_count()%2==0 else 0)|(64 if not v else 0)|(128 if v&0x8000 else 0)
class Prediction:
    def __init__(self,initial,p,ds,load):
        self.regs=dict(initial);self.original=dict(initial);self.p=p;self.ds=ds;self.load=load;self.events=[];self.flags=p['flags'];self.mask=0x8D5;self.calls=0
    def logical(self,v):self.flags=(self.flags&0x600)|logic(v);self.mask=0x8C5
    def cmp(self,a,b):self.flags=(self.flags&0x600)|compare(a,b);self.mask=0x8D5
    def call(self,kind,x,y,offset,attribute):
        before=dict(self.regs);before['cs']=self.load
        event=dict(service=kind,arguments=(attribute,offset,self.ds,y,x),string_hex=STRINGS[offset],request=before,flags_mask=self.mask,flags_value=self.flags&self.mask)
        self.calls+=1;self.regs,self.flags=reply(self.regs,self.calls,self.p['seed'],self.flags,self.p['status']);self.mask=0x8D5
        event.update(post=dict(self.regs),post_flags=self.flags);self.events.append(event)
    def run(self,kind):
        p=self.p;sel,attr=p['selection'],p['attribute'];self.regs['bp']=p['stack']-2
        self.regs.update(si=sel,di=attr) if kind=='main' else self.regs.update(di=sel,si=attr)
        if kind=='vs':
            self.logical(sel)
            if sel:self.cmp(sel,1)
            n=sel if sel in (0,1) else 2;self.call('gaiji',27,18+n,(0xA9,0xB2,0xBB)[n],attr)
        elif kind=='main':
            self.logical(sel)
            if sel:self.cmp(sel,min(sel,5))
            if sel<6:self.call('gaiji',(25,23,22,24,25,26)[sel],17+sel,(0xDC,0xE0,0xE7,0xEF,0xF5,0xFA)[sel],attr)
        else:
            self.logical(sel)
            if sel:self.cmp(sel,min(sel,3))
            if sel==3:self.call('gaiji',32,22,0xFA,attr)
            elif sel<3:
                self.call('gaiji',(25,25,23)[sel],17+2*sel,(0xFE,0x102,0x107)[sel],attr)
                if sel==0:self.call('text',37,17,0x175,0xE1)
                value=(p['rank'],p['bgm'],p['key'])[sel];self.regs.update(ax=value,bx=value if sel==0 else p['resoff'],es=p['resseg'])
                if sel==0:
                    self.cmp(value,3)
                    if value<4:
                        self.regs['bx']=2*value;self.flags=(self.flags&0x600)|add_flags(value,value);self.mask=0x8D5
                        self.call('gaiji',(38,37,38,37)[value],17,(0x113,0x117,0x11C,0x120)[value],attr)
                else:
                    self.logical(value)
                    if value:self.cmp(value,min(value,2))
                    if value<3:self.call('gaiji',35 if sel==1 else 37,17+2*sel,((0x125,0x12D,0x135) if sel==1 else (0x14C,0x153,0x15A))[value],attr)
        for n in ('bp','si','di'):self.regs[n]=self.original[n]
        return self
class Machine(BaseMachine):
    def __init__(self,mz,load):
        super().__init__(mz,load);self.load=load;self.instructions={};self.owned=set();self.executable=set();self.nested=set()
        for start,size,ins in ENTRIES.values():
            rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+ins],start));need(sum(i.size for i in rows)==ins,'complete renderer instructions')
            self.instructions.update({i.address:i.size for i in rows});self.owned.update(range(start,start+size));self.executable.update(range(start,start+ins))
    def registers(self):return {n:self.r(n) for n in (*GPRS,'cs','ds','es','ss')}
    def code(self,uc,address,size,_):
        try:
            if address==self.cs*16+0xFFFF:self.returned=True;uc.emu_stop();return
            rva=address-self.base;self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
            if rva in SERVICES:
                need(self.index<len(self.expected.events),'bounded renderer library protocol');e=self.expected.events[self.index];self.index+=1
                need(e['service']==SERVICES[rva] and self.registers()==e['request'],'independent library request registers')
                need(all(uc.reg_read(GPRS[n])==self.high[n]|e['request'][n] for n in GPRS),'complete request DWORD registers')
                f=uc.reg_read(UC_X86_REG_EFLAGS);need(f&e['flags_mask']==e['flags_value'] and f&0x600==self.flags&0x600,'defined request flags and IF/DF')
                sp=self.r('sp');need(sp==self.stack-20,'real near renderer/far library stack depth')
                ip,cs=struct.unpack('<HH',bytes(uc.mem_read(0x70000+sp,4)));need(cs==self.cs and cs*16+ip-self.base in self.instructions,'real far return to renderer')
                args=tuple(struct.unpack('<5H',bytes(uc.mem_read(0x70000+sp+4,10))));need(args==e['arguments'],'all five physical Pascal argument WORDs')
                _,off,seg,_,_=args;raw=bytes.fromhex(e['string_hex']);need(bytes(uc.mem_read(seg*16+off,len(raw)))==raw,'complete gaiji/text string bytes including NUL')
                for n in ('ax','bx','cx','dx','es'):uc.reg_write(REG[n],e['post'][n])
                uc.reg_write(UC_X86_REG_EFLAGS,e['post_flags']);uc.reg_write(REG['sp'],sp+14);uc.reg_write(REG['cs'],cs);uc.reg_write(REG['ip'],ip);return
            need(self.instructions.get(rva)==size,'execution outside renderer instructions, including inline table')
            self.covered.update(range(rva,rva+size))
        except Exception as e:self.fail(e)
    def write(self,uc,access,address,size,value,_):
        try:
            need(0x70000+self.stack-40<=address and address+size<=0x70000+self.stack,'renderer writes only bounded private stack')
            self.maximum_stack=max(self.maximum_stack,0x70000+self.stack-address)
        except Exception as e:self.fail(e)
    def run(self,kind,*,selection=0,attribute=0xE1,rank=0,bgm=0,key=0,resseg=0x6000,resoff=0x31,seed=0x1357,status=0xFFFF,flags=0x202,stack=0xF800):
        need(kind in ENTRIES and all(0<=v<=65535 for v in (selection,attribute,seed,status)) and all(0<=v<=255 for v in (rank,bgm,key)),'WORD selection/attribute and BYTE option state')
        need(resseg in (0x5000,0x6000) and 0<=resoff<=0xFF80 and 40<=stack<=0xFFF0,'disjoint far resident and private stack')
        self.uc.mem_write(0,bytes(self.initial));self.stack,self.flags=stack,flags
        self.uc.mem_write(0x70000+stack-40,b'\xD3'*40);self.uc.mem_write(0x70000+stack,struct.pack('<3H',0xFFFF,attribute,selection))
        self.uc.mem_write(self.data+RESIDENT,struct.pack('<HH',resoff,resseg));base=resseg*16+resoff;self.uc.mem_write(base,b'\xA5'*0x60)
        for off,value in ((0xB,rank),(0x15,bgm),(0x16,key)):self.uc.mem_write(base+off,bytes((value,)))
        self.memory=bytearray(self.uc.mem_read(0,1<<20));initial={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)};self.high={n:(seed^0x5AA5)<<16 for n in GPRS}
        for n in GPRS:self.uc.reg_write(GPRS[n],self.high[n]|initial[n])
        initial.update(cs=self.cs,ds=self.ds,es=seed,ss=0x7000)
        for n in ('cs','ds','es','ss'):self.uc.reg_write(REG[n],initial[n])
        self.uc.reg_write(REG['sp'],stack);self.uc.reg_write(UC_X86_REG_EFLAGS,flags)
        p=dict(selection=selection,attribute=attribute,rank=rank,bgm=bgm,key=key,resseg=resseg,resoff=resoff,seed=seed,status=status,flags=flags,stack=stack)
        self.expected=Prediction(initial,p,self.ds,self.load).run(kind);self.index,self.error,self.returned=0,None,False
        try:self.uc.emu_start(self.base+ENTRIES[kind][0],0x100000,count=1000)
        except UcError as e:raise ValueError('OP renderer contract: guest fault') from e
        need(self.error is None,self.error or 'guest error');need(self.returned and self.r('sp')==stack+6,'near Pascal return pops four argument bytes')
        e=self.expected;need(self.index==len(e.events) and self.registers()==e.regs,'complete independent event/WORD register contract')
        need(all(self.uc.reg_read(GPRS[n])==self.high[n]|e.regs[n] for n in GPRS),'returning DWORD high halves')
        f=self.uc.reg_read(UC_X86_REG_EFLAGS);need(f&e.mask==e.flags&e.mask and f&0x600==flags&0x600,'defined returning flags and inherited IF/DF')
        memory=bytes(self.uc.mem_read(0,1<<20));lo,hi=0x70000+stack-40,0x70000+stack;self.memory[lo:hi]=memory[lo:hi]
        need(memory==self.memory,'complete memory outside 40 stack bytes, including live caller arguments')
        return dict(registers=self.registers(),full_registers={n:self.uc.reg_read(GPRS[n]) for n in GPRS},flags_mask=e.mask,flags=f&(e.mask|0x600),events=e.events)
def cases():
    words=sorted(set(range(256))|{v<<8 for v in range(256)}|{0x7FFF,0xFFFF})
    for kind in ENTRIES:
        for sel in words:yield kind,dict(selection=sel,attribute=(sel*257^0xF3A5)&65535,rank=sel&255,bgm=sel&255,key=sel&255)
    for sel,field in enumerate(('rank','bgm','key')):
        for v in range(256):
            for attr in (0,1,0xE1,0x8000,0xFFFF):yield 'option',dict(selection=sel,attribute=attr,**{field:v})
    for kind in ENTRIES:
        for ai,attr in enumerate((0,1,0xE1,0x8000,0xF3A5,0xFFFF)):
            for si,seed in enumerate((0,1,0x1357,0xECA8,0xA55A,0xFFFF)):
                for flags in (2,0x202,0x402,0xED7):yield kind,dict(selection=(0,1,2,3,5,0xFFFF)[si],attribute=attr,seed=seed,flags=flags,resseg=0x5000 if si&1 else 0x6000,resoff=(0,0x31,0xFF80)[ai%3],stack=0x80 if ai&1 else 0xFFF0)
def verify(target,candidate):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            m=Machine(mz,load)
            try:
                trace=hashlib.sha256();counts={k:0 for k in ENTRIES};max_calls=0
                for count,(kind,p) in enumerate(cases(),1):
                    options=dict(seed=0x1357 if count&1 else 0xECA8,flags=(2,0x202,0x402,0xED7)[count%4],stack=0x80 if count&1 else 0xFFF0);options.update(p)
                    row=m.run(kind,**options);counts[kind]+=1;max_calls=max(max_calls,len(row['events']));trace.update(json.dumps(row,sort_keys=True).encode())
                need(m.covered==m.executable and len(m.owned-m.covered)==9,'all 509 instruction bytes execute; nine inline non-instruction bytes separate')
                loads.append(dict(load_segment=load,cases=count,cases_by_function=counts,executed_owner_bytes=len(m.covered),inline_non_instruction_bytes=len(m.owned-m.covered),maximum_observed_stack_depth=m.maximum_stack,maximum_library_calls=max_calls,trace_sha256=trace.hexdigest()))
            finally:m.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent renderer target/candidate observations')
    return dict(images=2,functions=3,code_bytes=518,executed_owner_bytes=509,inline_non_instruction_bytes=9,cases_per_image=sum(o['cases'] for o in observations[0]),exhaustive_option_BYTE_states=256,observations=observations[0],scope='all three maintained renderer bodies and four native switch entries; bounded gaiji/text replies, no physical TRAM/asset-shape claim')

def negative_controls(target):
    controls=(
        ('VS-full-WORD-selector-slot',0x2A4,b'\x06',b'\x07','vs',dict(selection=0x100)),
        ('VS-full-WORD-attribute-slot',0x2A7,b'\x04',b'\x06','vs',{}),
        ('VS-zero-selects-first-label',0x2AA,b'\x75',b'\x74','vs',{}),
        ('VS-first-label-row',0x2AE,b'\x12',b'\x13','vs',{}),
        ('VS-default-is-CPU-CPU',0x2D1,b'\xBB',b'\xB2','vs',dict(selection=0xFFFF)),
        ('VS-Pascal-pop-four',0x2DD,b'\x04',b'\x06','vs',{}),
        ('main-invalid-selection-draws-nothing',0x63E,b'\x05',b'\x06','main',dict(selection=6)),
        ('main-selector-is-WORD',0x5E2,b'\x8B',b'\x8A','main',{}),
        ('main-story-column',0x5F0,b'\x19',b'\x18','main',{}),
        ('main-quit-label-pointer',0x649,b'\xFA',b'\xF5','main',dict(selection=5)),
        ('main-attribute-is-WORD',0x5E5,b'\x8B',b'\x8A','main',dict(attribute=0xF3A5)),
        ('main-Pascal-pop-four',0x655,b'\x04',b'\x02','main',{}),
        ('option-attribute-slot',0x661,b'\x04',b'\x06','option',{}),
        ('rank-erasure-is-always-white',0x681,b'\xE1',b'\x01','option',dict(attribute=0)),
        ('rank-resident-field',0x68F,b'\x0B',b'\x15','option',dict(rank=3,bgm=0)),
        ('rank-zero-extends-BYTE',0x691,b'\0',b'\xFF','option',{}),
        ('rank-switch-bounds-before-table',0x698,b'\x87',b'\x86','option',dict(rank=4)),
        ('rank-first-relocated-table-WORD',0x799,b'\xA2\x06',b'\xAF\x06','option',{}),
        ('BGM-unknown-value-has-no-value-label',0x6FF,b'\x02',b'\x03','option',dict(selection=1,bgm=3)),
        ('key-mode-resident-field',0x746,b'\x16',b'\x15','option',dict(selection=2,key=2,bgm=1)),
        ('option-four-is-not-quit',0x77F,b'\x03',b'\x04','option',dict(selection=4)),
        ('option-selector-is-full-WORD',0x65E,b'\x06',b'\x05','option',dict(selection=0x100)),
        ('rank-uses-text-library',0x684,b'\x54\x22',b'\xCC\x0F','option',{}),
        ('value-attribute-survives-library-replies',0x78C,b'\x56',b'\x57','option',dict(attribute=0xF3A5)),
    )
    rejected=[]
    for name,off,old,new,kind,p in controls:
        at=0x9900+off;raw=bytearray(target.program_image);need(raw[at:at+len(old)]==old,'literal renderer mutation anchor '+name);raw[at:at+len(new)]=new;m=None
        try:
            try:m=Machine(replace(target,program_image=bytes(raw)),0x3000);m.run(kind,**p)
            except ValueError:rejected.append(name)
            else:raise ValueError('OP renderer mutation survived: '+name)
        finally:
            if m:m.close()
    return dict(count=len(rejected),rejected=rejected)
