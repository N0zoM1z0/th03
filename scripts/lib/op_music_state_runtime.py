"""Whole real track/list/snapshot/free bodies, independent state and exact stack.

Text and HMEM entries are bounded unowned replies. All21 nested track bodies
and all8000 DWORD copy iterations execute; DF does not alter the explicit copy.
"""
import hashlib
import json
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_INSN
from unicorn import x86_const as x
from lib.op_music_state_layout import CS,DS,START,SIZE,PROCEDURES
from lib.op_startup_state import State,REG,GPRS,address,logical,ARITH
from lib.op_cfg_runtime import reply

class ContractError(ValueError):
    """Explicit guest contract mismatch; never an arbitrary implementation error."""

def need(value,message):
    if not value:raise ContractError('OP Music state contract: '+str(message))

PAGE,HEAP,TABLE,PLANE=0x2039,0x203A,0x5F2,0x19FA
ENTRIES={n:(START+off,size,pop) for n,off,size,pop in PROCEDURES}
SERVICES={0xC6DB:('text',10,0xBEB),0x24CA:('alloc',2,0),0x25CE:('free',2,0)}


class Prediction(State):
    def shift(self,value,count):
        result=(value<<count)&65535
        self.flags=(self.flags&0x600)|2|logical(result)|((value>>(16-count))&1)
        self.mask=0xC5  # SHL count>1 leaves OF/AF undefined.
        return result

    def port(self):
        self.events.append(('out',0xA6,1,self.r['ax']&255,self.full(),self.flags&0x600))

    def service(self,name,continuation,cleanup):
        self.frame(continuation,0xBEB if name=='text' else 0)
        self.calls+=1
        at=address(self.ss,self.r['sp']);mask=self.mask|0x600
        self.events.append(('service',name,self.full(),bytes(self.memory[at:at+4+cleanup]).hex(),self.flags&mask,mask,self.calls))
        if name=='text' and self.calls==1:
            for off,size,key in ((PAGE,1,'page_after_first'),(TABLE+4*(self.o['index']&255),4,'pointer_after_first')):
                value=self.o[key]
                if value is not None:
                    at=address(self.ds,off)
                    self.events.append(('surface',at,size,value))
                    self.memory[at:at+size]=value.to_bytes(size,'little')
        status=self.o['allocated'] if name=='alloc' else self.o['status']
        self.r,self.flags=reply(self.r,self.calls,self.o['seed'],self.flags,status)
        self.mask=ARITH
        self.returned(cleanup)

    def track(self):
        self.enter(2)
        self.al(1);self.al(self.op(1,self.dg(PAGE,1),True,bits=8))
        self.store(address(self.ss,self.r['bp']-1),1,self.r['ax']&255)
        self.r['dx']=0xA6;self.port()
        for iteration,continuation in enumerate((0xC5A,0xC8C)):
            if iteration:
                self.r['dx']=0xA6;self.al(self.dg(PAGE,1));self.port()
            self.push(16)
            index=self.word(self.ss,self.r['bp']+6,1)
            self.r['ax']=index
            self.r['ax']=self.shift(self.r['ax'],4)
            self.r['ax']=self.op(self.r['ax'],40);self.push(self.r['ax'])
            self.r['ax']=self.word(self.ss,self.r['bp']+4,1)|0x20
            self.logic(self.r['ax']);self.push(self.r['ax'])
            self.r['ax']=self.shift(index,2);self.r['bx']=self.r['ax']
            self.push(self.word(self.ds,TABLE+self.r['bx'],4),4)
            self.service('text',continuation,10)
        self.r['sp']=self.r['bp'];self.pop('bp');self.r['sp']+=6

    def run(self,kind):
        if kind=='track_put_both':self.track();return
        self.enter()
        if kind in ('tracklist_put_both','nopoly_B_snap'):self.push(self.r['si'])
        if kind=='tracklist_put_both':
            self.r['si']=0;self.logic(0)
            while True:
                self.op(self.r['si'],21,True)
                if self.r['si']==21:break
                self.push(self.r['si'])
                self.r['ax']=self.word(self.ss,self.r['bp']+4,1)
                self.op(self.r['ax'],self.r['si'],True)
                self.al(15 if self.r['ax']==self.r['si'] else 3)
                self.push(self.r['ax']);self.push(0xCAC)
                self.entry('track',6);self.track();self.done('track')
                carry=self.flags&1
                self.r['si']=self.op(self.r['si'],1)
                self.flags=(self.flags&~1)|carry
        elif kind=='nopoly_B_snap':
            self.push(32000);self.service('alloc',0xCC3,2)
            self.field(HEAP,self.r['ax'])
            self.r['si']=0;self.logic(0)
            while True:
                self.op(self.r['si'],32000,True)
                if self.r['si']==32000:break
                pointer=self.dg(PLANE,4)
                self.r['bx'],self.r['es']=pointer&65535,pointer>>16
                self.r['bx']=self.op(self.r['bx'],self.r['si'])
                value=self.word(self.r['es'],self.r['bx'],4)
                self.r['ax']=value&65535;self.high['ax']=value&0xFFFF0000
                self.r['es']=self.dg(HEAP)
                self.store(address(self.r['es'],self.r['si']),4,value)
                self.r['si']=self.op(self.r['si'],4)
        else:
            need(kind=='nopoly_B_free','known whole procedure')
            self.push(self.dg(HEAP));self.service('free',0xCF4,2)
        if kind in ('tracklist_put_both','nopoly_B_snap'):self.pop('si')
        self.pop('bp');self.r['sp']+=2+(2 if kind=='tracklist_put_both' else 0)


class Machine:
    def __init__(self,image,load):
        self.image,self.load=image,load
        self.base=load*16;self.cs,self.ds=load+CS,load+DS
        self.uc=Uc(UC_ARCH_X86,UC_MODE_16);self.uc.mem_map(0,1<<20)
        memory=bytearray(1<<20);raw=image.relocated_program_image(load)
        memory[self.base:self.base+len(raw)]=raw;self.initial=bytes(memory)
        self.instructions={i.address:i.size for i in Cs(CS_ARCH_X86,CS_MODE_16).disasm(image.program_image[START:START+SIZE],START)}
        need(sum(self.instructions.values())==SIZE,'complete native instructions')
        self.covered=set()
        self.hooks=[self.uc.hook_add(UC_HOOK_CODE,self.code),self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write),
            self.uc.hook_add(UC_HOOK_INSN,self.out,None,1,0,x.UC_X86_INS_OUT)]

    def close(self):
        for hook in self.hooks:self.uc.hook_del(hook)
        self.hooks=[];self.uc=None

    def r(self,name):return self.uc.reg_read(REG[name])&65535

    def full(self):
        result={n:self.uc.reg_read(reg) for n,reg in GPRS.items()}
        result.update({n:self.r(n) for n in ('cs','ds','es','ss','fs','gs')})
        return result

    def fail(self,error):self.error=error;self.uc.emu_stop()

    def event(self,event):
        need(self.index<len(self.expected.events) and self.expected.events[self.index]==event,
            'event'+str(self.index)+': '+str(event)+' expected '+str(self.expected.events[self.index:self.index+1]))
        self.index+=1

    def code(self,uc,at,size,user):
        try:
            if at==self.cs*16+0xFFFF:self.returned=True;uc.emu_stop();return
            rva=at-self.base
            self.maximum_stack=max(self.maximum_stack,self.stack-self.r('sp'))
            if rva in SERVICES:
                sp=self.r('sp');physical=address(self.r('ss'),sp)
                ip,cs=struct.unpack('<HH',uc.mem_read(physical,4))
                self.event(('far-frame',physical,ip,cs))
                name,cleanup,_=SERVICES[rva]
                e=self.expected.events[self.index];mask=e[-2];count=e[-1]
                self.event(('service',name,self.full(),bytes(uc.mem_read(physical,4+cleanup)).hex(),uc.reg_read(x.UC_X86_REG_EFLAGS)&mask,mask,count))
                if name=='text':
                    pointer,segment,fx,y,left=struct.unpack('<5H',uc.mem_read(physical+4,10))
                    self.text.append([pointer,segment,fx,y,left])
                    if count==1:
                        for off,width,key in ((PAGE,1,'page_after_first'),(TABLE+4*(self.o['index']&255),4,'pointer_after_first')):
                            value=self.o[key]
                            if value is not None:
                                dest=address(self.ds,off);self.event(('surface',dest,width,value));uc.mem_write(dest,value.to_bytes(width,'little'))
                status=self.o['allocated'] if name=='alloc' else self.o['status']
                values,flags=reply({n:self.r(n) for n in (*GPRS,'cs','ds','es','ss','fs','gs')},count,self.o['seed'],uc.reg_read(x.UC_X86_REG_EFLAGS),status)
                for n in ('ax','bx','cx','dx','es'):uc.reg_write(REG[n],values[n])
                uc.reg_write(x.UC_X86_REG_EFLAGS,flags);uc.reg_write(REG['sp'],sp+4+cleanup)
                uc.reg_write(REG['cs'],cs);uc.reg_write(REG['ip'],ip);return
            if rva==START and self.index<len(self.expected.events) and self.expected.events[self.index][:2]==('entry','track'):
                e=self.expected.events[self.index];mask=e[-1]
                self.event(('entry','track',self.full(),bytes(uc.mem_read(address(self.r('ss'),self.r('sp')),6)).hex(),uc.reg_read(x.UC_X86_REG_EFLAGS)&mask,mask))
            if rva==0xA5AC and self.index<len(self.expected.events) and self.expected.events[self.index][:2]==('owned-return','track'):
                mask=self.expected.events[self.index][-1]
                self.event(('owned-return','track',self.full(),uc.reg_read(x.UC_X86_REG_EFLAGS)&mask,mask))
            need(self.instructions.get(rva)==size,'only whole state/track instructions: '+hex(rva))
            self.covered.update(range(rva,rva+size))
        except Exception as error:self.fail(error)

    def write(self,uc,access,at,size,value,user):
        try:
            if self.index<len(self.expected.events) and self.expected.events[self.index][0]=='far-frame':
                _,dest,ip,cs=self.expected.events[self.index]
                need(size==2 and (at,value) in ((dest,ip),(dest+2,cs)),'actual native far return words');return
            self.event(('store',at,size,value))
        except Exception as error:self.fail(error)

    def out(self,uc,port,size,value,user):
        try:
            self.event(('out',port,size,value,self.full(),uc.reg_read(x.UC_X86_REG_EFLAGS)&0x600));self.ports.append(value)
        except Exception as error:self.fail(error)

    def run(self,kind,*,index=0,color=15,page=0,allocated=0x5000,source_segment=0xA800,source_offset=0,
            page_after_first=None,pointer_after_first=None,seed=0x1357,status=0xFFFF,flags=0x202,stack=0xF800,reenter=False):
        need(kind in ENTRIES and index in range(65536) and color in range(65536) and page in range(256),'WORD slots/BYTE page')
        need(allocated in (0,0x5000,0x6000,0x9000,0xA800,0xA801,0xF800) and source_segment in (0xA000,0xA800,0xB000) and source_offset in range(65536),
            'mapped copy profile disjoint from CODE/DGROUP/caller stack; source/destination overlap remains live')
        need(page_after_first is None or page_after_first in range(256),'explicit foreign page BYTE')
        need(pointer_after_first is None or pointer_after_first in range(1<<32),'explicit foreign table DWORD')
        need(0x100<=stack<=0xFFF0 and flags in (2,0x202,0x402,0xED7),'mapped WORD stack / IF / DF')
        memory=bytearray(self.expected.memory if reenter else self.initial)
        def put(seg,off,value,width):memory[address(seg,off):address(seg,off)+width]=value.to_bytes(width,'little')
        if not reenter:
            put(self.ds,PAGE,page,1);put(self.ds,HEAP,allocated,2);put(self.ds,PLANE,(source_segment<<16)|source_offset,4)
            if kind=='nopoly_B_snap':
                memory[allocated*16:allocated*16+32000]=b'\xA5'*32000
                memory[source_segment*16:source_segment*16+0x10003]=bytes((i*73+(i>>8)*19+seed)&255 for i in range(0x10003))
        memory[0x70000+stack-64:0x70000+stack]=b'\xD3'*64
        frame=struct.pack('<3H',0xFFFF,color,index) if kind=='track_put_both' else struct.pack('<2H',0xFFFF,index) if kind=='tracklist_put_both' else b'\xFF\xFF'
        memory[0x70000+stack:0x70000+stack+len(frame)]=frame
        self.uc.mem_write(0,bytes(memory))
        registers={n:(seed+i*0x231)&65535 for i,n in enumerate(GPRS)}
        registers.update(sp=stack,cs=self.cs,ds=self.ds,es=seed,ss=0x7000,fs=seed^0xA55A,gs=seed^0x5AA5)
        high={n:(seed^0x5AA5)<<16 for n in GPRS}
        for n,reg in GPRS.items():self.uc.reg_write(reg,high[n]|registers[n])
        for n in ('cs','ds','es','ss','fs','gs'):self.uc.reg_write(REG[n],registers[n])
        self.uc.reg_write(x.UC_X86_REG_EFLAGS,flags)
        self.o=dict(index=index,color=color,page_after_first=page_after_first,pointer_after_first=pointer_after_first,allocated=allocated,seed=seed,status=status,load=self.load)
        self.expected=Prediction(memory,registers,high,flags,self.o);self.expected.run(kind)
        self.index,self.error,self.returned=0,None,False
        self.stack,self.maximum_stack=stack,0;self.text=[];self.ports=[]
        try:self.uc.emu_start(self.base+ENTRIES[kind][0],1<<20,count=500000)
        except UcError as error:raise ContractError('Music state guest fault') from error
        if self.error is not None:raise self.error
        need(self.returned and self.index==len(self.expected.events),'complete actual near return/event plan')
        need(self.full()==self.expected.full(),'all DWORD registers and six segments '+str((self.full(),self.expected.full())))
        mask=self.expected.mask|0x600
        need(self.uc.reg_read(x.UC_X86_REG_EFLAGS)&mask==self.expected.flags&mask,'all defined flags/IF/DF')
        need(bytes(self.uc.mem_read(0,1<<20))==self.expected.memory,'all memory including every private stack byte and live overlapping copy')
        return dict(registers=self.expected.full(),flags=self.expected.flags&mask,flags_mask=mask,events=self.index,
            text=self.text,ports=self.ports,maximum_stack_depth=self.maximum_stack,
            heap=self.expected.dg(HEAP),copied_DWORDs=8000 if kind=='nopoly_B_snap' else 0,
            trace_sha256=hashlib.sha256(json.dumps(self.expected.events,sort_keys=True).encode()).hexdigest())


def cases():
    yield 'tracklist_put_both',dict(index=0,page=128,page_after_first=255,pointer_after_first=0xDEADBEEF)
    for value in range(256):
        yield 'track_put_both',dict(index=value,color=0xA503,page=value)
        yield 'track_put_both',dict(index=0xA5FF,color=value,page=255)
        yield 'tracklist_put_both',dict(index=0xA500|value,page=value)
    for index in (0,20,21,40,128,255):
        for upper in (0x100,0x8000,0xFF00):
            yield 'track_put_both',dict(index=upper|index,color=upper|15,page=128,
                page_after_first=255,pointer_after_first=0xDEADBEEF)
    for flags in (2,0x202,0x402,0xED7):
        for stack in (0x100,0xFFF0):
            for seed in (0,0x1357,0x8000,0xFFFF):
                yield 'track_put_both',dict(index=0xFF80,color=0xA5FF,page=255,flags=flags,stack=stack,seed=seed,status=seed,
                    page_after_first=128,pointer_after_first=0xFFFF0001)
                yield 'tracklist_put_both',dict(index=0xA514,page=255,flags=flags,stack=stack,seed=seed,status=seed)
            yield 'nopoly_B_snap',dict(source_offset=65535,flags=flags,stack=stack)
            yield 'nopoly_B_free',dict(allocated=0,flags=flags,stack=stack)
    for allocated in (0,0x5000,0x6000,0x9000,0xF800):
        for offset in (0,1,65535):yield 'nopoly_B_snap',dict(allocated=allocated,source_offset=offset)
    for allocated in (0xA800,0xA801):
        for offset in (0,1,65535):yield 'nopoly_B_snap',dict(allocated=allocated,source_offset=offset)
    for segment in (0xA000,0xB000):yield 'nopoly_B_snap',dict(source_segment=segment,source_offset=65535)


def verify(target,candidate):
    observations=[]
    for image in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            machine=Machine(image,load);digest=hashlib.sha256()
            counts={name:0 for name in ENTRIES};copy=depth=0
            def record(kind,row):
                nonlocal copy,depth
                counts[kind]+=1;copy+=row['copied_DWORDs'];depth=max(depth,row['maximum_stack_depth'])
                digest.update(json.dumps(row,sort_keys=True).encode())
            try:
                for kind,options in cases():
                    try:record(kind,machine.run(kind,**options))
                    except ValueError as error:raise ValueError(str((kind,options,error))) from error
                for allocated in (0,0x6000):
                    record('nopoly_B_snap',machine.run('nopoly_B_snap',allocated=allocated,flags=0xED7))
                    record('nopoly_B_free',machine.run('nopoly_B_free',reenter=True,flags=0xED7))
                    need(machine.expected.dg(HEAP)==allocated,'actual consecutive free leaves saved segment untouched')
                need(machine.covered==set(range(START,START+SIZE)),'all216 owner bytes execute')
                loads.append(dict(load_segment=load,cases=sum(counts.values()),complete_returns=counts,consecutive_reentry_cases=2,
                    executed_owner_bytes=len(machine.covered),actual_copy_DWORD_callbacks=copy,maximum_stack_depth=depth,trace_sha256=digest.hexdigest()))
            finally:machine.close()
        observations.append(loads)
    need(observations[0]==observations[1],'independent complete target/candidate observations')
    return dict(images=2,functions=4,code_bytes=SIZE,instruction_bytes=SIZE,observations=observations[0],
        cases_per_image=sum(r['cases'] for r in observations[0]),exhaustive_independent_BYTE_axes=['track index','color','page','list selection'],
        actual_nested_track_bodies=True,synthetic_owned_returns=False,ignored_stack_bytes=0,
        copy_iterations_per_snap=8000,copy_is_explicit_DWORD_loop=True,DF_changes_copy_direction=False,
        live_overlapping_source_and_destination=True,pointer_offset_WORD_wrap=True,null_allocation_is_not_checked=True,
        foreign_page_and_table_reloads=True,physical_graphics_text_or_heap_proved=False,whole_product_accepted=False)


def negative_controls(target):
    from dataclasses import replace
    controls=(
        ('track-ENTER-locals',0xA51F,2,'track_put_both',{}),
        ('other-page-BYTE-wrap',0xA523,1,'track_put_both',dict(page=255)),
        ('page-field',0xA526,1,'track_put_both',dict(page=128)),
        ('port-A6',0xA52C,2,'track_put_both',{}),
        ('left-coordinate',0xA530,1,'track_put_both',{}),
        ('index-low-BYTE',0xA533,1,'track_put_both',dict(index=0xFF80)),
        ('index-zero-extension',0xA535,1,'track_put_both',dict(index=0xFF80)),
        ('row-times16',0xA538,1,'track_put_both',dict(index=255)),
        ('row-origin40',0xA53A,1,'track_put_both',{}),
        ('color-low-BYTE',0xA53F,1,'track_put_both',dict(color=0xA580)),
        ('bold-FX',0xA543,1,'track_put_both',dict(color=0)),
        ('far-pointer-index4',0xA54D,1,'track_put_both',dict(index=255)),
        ('far-pointer-storage',0xA553,1,'track_put_both',{}),
        ('first-text-entry',0xA556,1,'track_put_both',{}),
        ('live-page-second-read',0xA55F,1,'track_put_both',dict(page_after_first=255)),
        ('live-pointer-second-read',0xA585,1,'track_put_both',dict(pointer_after_first=0xDEADBEEF)),
        ('track-Pascal-pop4',0xA58E,2,'track_put_both',{}),
        ('list-saved-SI',0xA593,1,'tracklist_put_both',{}),
        ('list-selector-low-BYTE',0xA59B,1,'tracklist_put_both',dict(index=0xA514)),
        ('selected-color15',0xA5A3,1,'tracklist_put_both',{}),
        ('unselected-color3',0xA5A7,1,'tracklist_put_both',{}),
        ('actual-nested-track-call',0xA5AA,1,'tracklist_put_both',{}),
        ('all21-tracks',0xA5AF,1,'tracklist_put_both',{}),
        ('list-Pascal-pop2',0xA5B5,2,'tracklist_put_both',{}),
        ('allocation32000-bytes',0xA5BC,1,'nopoly_B_snap',{}),
        ('allocator-entry',0xA5BF,1,'nopoly_B_snap',{}),
        ('saved-allocation-segment',0xA5C4,1,'nopoly_B_snap',{}),
        ('source-far-pointer',0xA5CC,1,'nopoly_B_snap',dict(source_offset=65535)),
        ('source-WORD-offset-add',0xA5CF,1,'nopoly_B_snap',dict(source_offset=65535)),
        ('DWORD-load',0xA5D0,1,'nopoly_B_snap',{}),
        ('destination-segment',0xA5D6,1,'nopoly_B_snap',{}),
        ('DWORD-store',0xA5D8,1,'nopoly_B_snap',{}),
        ('copy-step4',0xA5DE,1,'nopoly_B_snap',{}),
        ('copy-bound32000',0xA5E1,1,'nopoly_B_snap',{}),
        ('snap-near-return',0xA5E7,8,'nopoly_B_snap',{}),
        ('free-saved-segment',0xA5ED,1,'nopoly_B_free',{}),
        ('real-free-entry',0xA5F0,1,'nopoly_B_free',{}),
        ('free-near-return',0xA5F5,8,'nopoly_B_free',{}),
    )
    rejected=[]
    for name,at,mask,kind,options in controls:
        raw=bytearray(target.program_image);raw[at]^=mask
        machine=None
        try:
            try:machine=Machine(replace(target,program_image=bytes(raw)),0x3000)
            except Exception as error:
                raise ValueError('Music state control construction failed: '+name) from error
            try:machine.run(kind,**options)
            except ContractError:rejected.append(name)
            else:raise ValueError('Music state mutation survived: '+name)
        finally:
            if machine is not None:machine.close()
    need(len(controls)==len(set(rejected))==38,'all38 runtime mutations must reject')
    return dict(actual_instruction_mutations=len(controls),rejected=rejected)
