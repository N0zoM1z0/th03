"""Real OP consumers expose initializer meanings without changing old contracts.

Explicit native memory operands are decoded rather than installing a Unicorn
memory-read hook. Text/file callbacks read their actual pointer arguments under
an explicit bounded library-reader contract; no font pixels or DOS are proved.
"""
import hashlib
import json
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16,CS_AC_READ
from capstone.x86_const import X86_OP_MEM,X86_OP_REG
from unicorn import x86_const as x
from lib.op_entry_data_layout import DS,START,SIZE,PARTS,BY_NAME,STRINGS,STATIC_ONLY,semantic_image,STAGE7,PAIRINGS,SEEDS,need
from lib.op_render_runtime import Machine as RenderBase
from lib.op_story_runtime import Machine as StoryBase
from lib.op_dispatch_runtime import Machine as DispatchBase
from lib.op_main_menu_runtime import Machine as MainBase
from lib.op_option_runtime import Machine as OptionBase
from lib.op_startup_runtime import Machine as StartupBase

NUMERIC=set(range(16,25))|set(range(52,76))|set(range(126,131))


class Observe:
    def __init__(self,*args):
        self.read=set()
        self.strings=[]
        self.screens=[]
        self.pending_load=None
        self.current_rva=None
        self.copy_destination=None
        super().__init__(*args)
        decoder=Cs(CS_ARCH_X86,CS_MODE_16)
        decoder.detail=True
        self.decoded={at:next(decoder.disasm(self.image_bytes[at:at+size],at))
            for at,size in self.instructions.items()}

    @property
    def image_bytes(self):
        return self.owner_image.program_image

    def reg(self,name):
        return self.uc.reg_read(getattr(x,'UC_X86_REG_'+name.upper()))

    def string(self,offset,segment,kind,attribute=None):
        need(segment==self.ds and offset in STRINGS,'semantic declared string argument identity')
        raw=bytearray()
        for at in range(offset,START+SIZE):
            value=self.uc.mem_read(segment*16+at,1)[0]
            raw.append(value)
            self.read.add(at-START)
            if value==0:break
        need(bytes(raw)==STRINGS[offset],'semantic bounded '+kind+' text/filename output at '+hex(offset))
        self.strings.append(dict(kind=kind,offset=offset,raw=raw.hex(),attribute=attribute))

    def observe(self,at):
        if self.pending_load is not None:
            register,value=self.pending_load
            need(self.reg(register)==value,'semantic native numeric register transfer: '+register)
            self.pending_load=None
        rva=at-self.base
        self.current_rva=rva
        ins=self.decoded.get(rva)
        if ins is not None and ins.mnemonic!='lea' and not (ins.mnemonic.startswith('rep ') and self.reg('cx')==0):
            for operand in ins.operands:
                if operand.type!=X86_OP_MEM or not operand.access&CS_AC_READ:continue
                m=operand.mem
                base,index=ins.reg_name(m.base),ins.reg_name(m.index)
                segment=ins.reg_name(m.segment) or ('ss' if base in ('bp','sp') else 'ds')
                offset=((self.reg(base) if base else 0)+(self.reg(index)*m.scale if index else 0)+m.disp)&65535
                physical=self.reg(segment)*16+offset
                first=physical-(self.ds*16+START)
                self.read.update(range(max(0,first),min(SIZE,first+operand.size)))
                if first in NUMERIC and ins.mnemonic in ('mov','movzx','movsx') and ins.operands[0].type==X86_OP_REG:
                    raw=semantic_image()[first:first+operand.size]
                    value=int.from_bytes(raw,'little',signed=ins.mnemonic=='movsx')
                    size=ins.operands[0].size
                    self.pending_load=(ins.reg_name(ins.operands[0].reg),value&((1<<(size*8))-1))
        sp=self.reg('sp')
        stack=self.reg('ss')*16+sp
        if rva in (0xFCC,0x2254):
            attribute,offset,segment,_,_=struct.unpack('<5H',self.uc.mem_read(stack+4,10))
            self.string(offset,segment,'gaiji' if rva==0xFCC else 'text',attribute)
        elif rva in (0x9A8,0x7C8,0x688,0xF36,0x2B60):
            offset,segment=struct.unpack('<HH',self.uc.mem_read(stack+4,4))
            self.string(offset,segment,{0x9A8:'open',0x7C8:'append',0x688:'puts',0xF36:'gaiji-load',0x2B60:'archive'}[rva])
        elif rva==0x9119:
            for skip in (4,8):
                offset,segment=struct.unpack('<HH',self.uc.mem_read(stack+skip,4))
                self.string(offset,segment,'execl')
        elif rva==0xB0DB:self.screens.append('shrink')
        elif rva==0x337E:
            off,seg=struct.unpack('<HH',self.uc.mem_read(stack+8,4))
            self.copy_destination=seg*16+off

    def code(self,uc,at,size,user):
        try:self.observe(at)
        except Exception as error:self.fail(error);return
        super().code(uc,at,size,user)

    def write(self,uc,access,at,size,value,user):
        try:
            if self.copy_destination is not None and self.current_rva in range(0x337E,0x339A) and self.copy_destination<=at<self.copy_destination+8:
                need(value==0,'semantic actual CRT zero-template stack output, including overwritten first3 bytes')
        except Exception as error:self.fail(error);return
        super().write(uc,access,at,size,value,user)


def consumer(base):
    class Machine(Observe,base):
        def __init__(self,image,load):
            self.owner_image=image
            super().__init__(image,load)
    return Machine


CLASSES={name:consumer(base) for name,base in
    (('render',RenderBase),('story',StoryBase),('demo',DispatchBase),('main',MainBase),('option',OptionBase),('startup',StartupBase))}


def fixture(image,load,kind,parameters,mutation=None):
    machine=CLASSES[kind](image,load)
    data=bytearray(image.relocated_program_image(load)[DS*16+START:DS*16+START+SIZE])
    need(data==semantic_image(),'canonical relocated input before optional mutant')
    if mutation is not None:
        offset,bit=mutation
        data[offset]^=1<<bit
    initial=bytearray(machine.initial)
    initial[machine.data+START:machine.data+START+SIZE]=data
    machine.initial=bytes(initial)
    try:
        if kind=='render':
            function,arguments=parameters
            result=machine.run(function,**arguments)
        elif kind=='story':
            alias=isinstance(parameters,tuple)
            character=parameters[1] if alias else parameters
            result=machine.run(selected_char=character)
            if alias:
                need(character in (221,223,225,227,229),'declared unchecked character fixture')
                need((result['nonterminal'],result['retries'])==((True,1) if character<229 else (False,0)),
                     'semantic unchecked story alias return/prefix classification')
            else:
                need(not result['nonterminal'],'semantic initially empty seen set completes the ordinary story')
                base=0x60000+0x31
                need(machine.uc.mem_read(base+0x2F,1)[0]==2*STAGE7[(character-1)//2]+1,'semantic seventh story opponent')
        elif kind=='demo':
            result=machine.run('start_demo',demo=parameters)
        elif kind=='main':
            result=machine.run(selection=data[209],initialized=data[212],in_main=data[211],quit=data[210])
            need(result['returned'] and machine.uc.mem_read(machine.data+0x161,1)[0]==0,'semantic initial main selection remains zero')
            need('shrink' not in machine.screens,'semantic initial in_main=true skips shrink')
            gaiji=[s for s in machine.strings if s['kind']=='gaiji']
            need(len(gaiji)==6 and [s['attribute'] for s in gaiji]==[0xE1,1,1,1,1,1],
                'semantic initial main=false draws all six choices with first highlighted')
        elif kind=='option':
            if parameters=='disabled':
                result=machine.run('option',selection=1,input=8,disabled=data[0],bgm=0)
                need(machine.uc.mem_read(0x60031+0x15,1)[0]==1,'semantic initially enabled BGM choice changes OFF to FM')
            else:
                result=machine.run('option',initialized=data[213],disabled=data[0])
                need(len(machine.strings)==8,'semantic initial option=false draws all four choices and values')
        else:
            result=machine.run(**(dict(quit=data[210]) if parameters=='quit' else parameters))
            if parameters=='quit':need(result['returned'] and result['iterations']==1,'semantic initial quit=false enters the real input loop')
        return dict(kind=kind,parameters=parameters,result=result,strings=machine.strings),machine.read
    finally:machine.close()


def cases():
    for selection in range(3):yield 'render',('vs',dict(selection=selection))
    for selection in range(6):yield 'render',('main',dict(selection=selection))
    for selection,field,count in ((0,'rank',4),(1,'bgm',3),(2,'key',3)):
        for value in range(count):yield 'render',('option',dict(selection=selection,**{field:value}))
    yield 'render',('option',dict(selection=3))
    for character in range(1,18,2):yield 'story',character
    for character in (221,223,225,227,229):yield 'story',('alias',character)
    for demo in (0,1,2,3,4,255):yield 'demo',demo
    for options in ({},dict(zoom=1),dict(assign=1),'quit'):yield 'startup',options
    yield 'main',None
    yield 'option',None
    yield 'option','disabled'


def verify(target,candidate):
    observations=[]
    for image in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            digest=hashlib.sha256()
            read=set()
            counts={name:0 for name in CLASSES}
            prefixes=0
            for kind,parameters in cases():
                row,used=fixture(image,load,kind,parameters)
                read|=used
                counts[kind]+=1
                prefixes+=int(kind=='story' and row['result']['nonterminal'])
                digest.update(json.dumps(row,sort_keys=True).encode())
            need(read==set(range(SIZE))-set(STATIC_ONLY),'all472 fixture-consumed initializer bytes; type strings15 remain static: '+str(sorted((set(range(SIZE))-set(STATIC_ONLY))-read)))
            loads.append(dict(load_segment=load,cases=sum(counts.values()),ordinary_returns=sum(counts.values())-prefixes,
                closed_story_prefixes=prefixes,consumers=counts,
                initialized_bytes_read=len(read),static_only_unused_bytes=len(STATIC_ONLY),trace_sha256=digest.hexdigest()))
        observations.append(loads)
    need(observations[0]==observations[1],'complete target/candidate DATA-consumer observations')
    return dict(images=2,initialized_data_bytes=SIZE,cases_per_image=sum(r['cases'] for r in observations[0]),observations=observations[0],
        semantic_numeric_register_transfers=True,semantic_CRT_stack_copy=True,explicit_native_operand_reads=True,
        argument_derived_bounded_library_string_reads=True,borrowed_private_stack_bytes=dict(render=40,story=80,demo=80,main=96,option=64,startup=96),
        old_full_state_contracts_preserved=True,new_CODE_ownership_bytes=0,new_BSS_ownership_bytes=0,
        physical_text_pixels_DOS_or_successful_exec_proved=False)


def control_case(offset):
    for p in PARTS:
        if not p['offset']<=offset<p['offset']+p['size']:continue
        name=p['name']
        if offset==0:return 'option','disabled'
        if offset<9:return 'startup',{}
        if offset<16:return 'story',3 if offset==10 else 1
        if offset<25:return 'story',1+2*(offset-16)
        if offset<52:return 'render',('vs',dict(selection=(offset-25)//9))
        if offset<60:return 'demo',((offset-52)//2)
        if offset<76:return 'demo',((offset-60)//4)
        if 126<=offset<131:return 'story',('alias',1+2*(offset-16))
        if name.startswith('COMMAND_'):return 'render',('main',dict(selection=['COMMAND_STORY','COMMAND_VS','COMMAND_MUSICROOM','COMMAND_REGIST_VIEW','COMMAND_OPTION','COMMAND_QUIT'].index(name)))
        if name in ('LABEL_RANK','LABEL_MUSIC','LABEL_KEYCONFIG'):
            return 'render',('option',dict(selection=['LABEL_RANK','LABEL_MUSIC','LABEL_KEYCONFIG'].index(name)))
        if name in ('VALUE_EASY','VALUE_NORMAL','VALUE_HARD','VALUE_LUNATIC'):
            return 'render',('option',dict(selection=0,rank=['VALUE_EASY','VALUE_NORMAL','VALUE_HARD','VALUE_LUNATIC'].index(name)))
        if name in ('VALUE_OFF','VALUE_FM','VALUE_MIDI'):
            return 'render',('option',dict(selection=1,bgm=['VALUE_OFF','VALUE_FM','VALUE_MIDI'].index(name)))
        if name in ('VALUE_KEY_KEY','VALUE_JOY_KEY','VALUE_KEY_JOY'):
            return 'render',('option',dict(selection=2,key=['VALUE_KEY_KEY','VALUE_JOY_KEY','VALUE_KEY_JOY'].index(name)))
        if name in ('menu_sel','in_main','main_initialized'):return 'main',None
        if name=='option_initialized':return 'option',None
        if name=='quit':return 'startup','quit'
        if name=='BINARY_MAINL':return 'story',1
        if name=='TEXT_SPACES':return 'render',('option',dict(selection=0))
        if name.startswith('ERROR_GDC'):return 'startup',dict(zoom=1)
        if name=='ERROR_OUT_OF_MEMORY':return 'startup',dict(assign=1)
        return 'startup',{}
    raise ValueError('DATA offset absent')


def negative_controls(target):
    rejected=[]
    for offset in range(SIZE):
        if offset in STATIC_ONLY:continue
        kind,parameters=control_case(offset)
        for bit in ((0,) if offset==211 else range(8)):
            try:fixture(target,0x3000,kind,parameters,(offset,bit))
            except ValueError as error:
                need('semantic ' in str(error),'control must reach a semantic consumer output: '+str((offset,bit,error)))
                rejected.append((offset,bit))
            else:raise ValueError('initializer bit mutation survived: '+str((offset,bit,kind,parameters)))
    return dict(actual_initializer_bit_mutations=len(rejected),rejected_sha256=hashlib.sha256(json.dumps(rejected).encode()).hexdigest(),
        mutated_bytes=len({o for o,_ in rejected}),unused_static_bytes=list(STATIC_ONLY),
        boolean_nonzero_equivalent_bits=[[211,bit] for bit in range(1,8)],
        raw_extent_equality_or_fixture_rejection_counts=False)
