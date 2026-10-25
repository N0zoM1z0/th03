"""Natural same-CS far-call layout and its complete four-byte call frame.

This is a five-byte producer/ABI observation. It grants no enclosing menu,
Music Room implementation or whole-product source acceptance.
"""
from dataclasses import replace
from pathlib import Path
import hashlib,json,re,struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn import x86_const as x
from lib.omf import parse_omf
from lib.op_cfg_layout import OBJECT,SEGMENT,OFFSET,verify as containing_layout

SOURCE='src/op/menu/menu_state.inl'
PRAGMA='#pragma samecodeseg musicroom_menu\n'
SITE,ENTRY=0xA1B4,0xAC06
REGS={n:getattr(x,'UC_X86_REG_E'+n.upper()) for n in ('ax','bx','cx','dx','si','di','bp','sp')}

def need(v,m):
    if not v:raise ValueError('OP Music Room call: '+str(m))
def sha(raw):return hashlib.sha256(raw).hexdigest()

def native_field(raw):
    names=[];block=None;found=[]
    for r in parse_omf(raw):
        if r.name=='EXTDEF':
            at=0
            while at<len(r.data):
                size=r.data[at];at+=1;names.append(r.data[at:at+size].decode());at+=size
                need(r.data[at]==0,'untyped native externals');at+=1
        elif r.name=='LEDATA':block=(r.data[0],int.from_bytes(r.data[1:3],'little'))
        elif r.name=='FIXUPP' and block[0]==1:
            at=0
            while at<len(r.data):
                loc,low,fd=r.data[at:at+3];at+=3;frame=None
                need(fd in (0x14,0x16,0x56),'literal native field form')
                if fd in (0x14,0x16):frame=r.data[at];at+=1
                target=r.data[at];at+=1
                if fd!=0x14 and names[target-1]=='@musicroom_menu$qv':
                    found.append([block[1]+(loc&3)*256+low,4 if loc>>2&15==3 else 2,loc,fd,frame,target])
    need(len(found)==1,'one complete symbolic Music Room field')
    return found[0]

def layout(root,work,target,candidate):
    from probe_th03_main_boss_marisa_cpp import code_bytes
    containing_layout(work,target,candidate)
    source=(root/SOURCE).read_bytes()
    need(source==(work/SOURCE).read_bytes() and source.count(PRAGMA.encode())==1
         and source.count(b'\t\t\tmusicroom_menu();')==1 and b'_asm' not in source,
         'maintained ordinary call and one genuine same-CS declaration')
    raw=(work/OBJECT).read_bytes();field=native_field(raw);code=code_bytes(raw,1)[0]
    need(field==[2221,4,0xCC,0x16,1,14] and code[2220]==0x9A
         and int.from_bytes(code[2221:2225],'little')==0,'unlinked native far CALL, group frame and zero symbolic addend')
    need(SEGMENT*16+OFFSET+2220==SITE,'literal full producer site')
    text=(work/'obj/th03/op.map').read_text()
    for off,name in ((0x1306,'musicroom_menu()'),(0x7E0,'main_update_and_render()')):
        need(len(re.findall(rf'(?m)^\s*0990:{off:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,'both same-CS MAP tables: '+name)
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    for mz in (target,candidate):
        rows=list(decoder.disasm(mz.program_image[SITE:SITE+5],SITE))
        need([(i.mnemonic,i.size) for i in rows]==[('nop',1),('push',1),('call',3)]
             and rows[1].op_str=='cs' and rows[2].operands[0].imm==ENTRY,
             'actual TLINK NOP/PUSH CS/near CALL relaxation')
        need(not any(SITE<=r.linear<SITE+5 for r in mz.relocations),'no residual far segment MZ relocation')
    need(target.program_image[SITE:SITE+5]==candidate.program_image[SITE:SITE+5],'all five native linked bytes')
    return dict(source=SOURCE,object=OBJECT,site=SITE,size=5,callee_entry=ENTRY,source_far_call=True,
        native_field=field,linked_instruction_kinds=['nop','push cs','near call'],ordered_relocations=[],
        shared_code_segment=SEGMENT,callee_implementation_executed=False,source_acceptance=False,
        enclosing_menu_accepted=False,whole_product_accepted=False)

def run(mz,load,*,seed=0x1357,flags=0x202,ss=0x7000,stack=0xFFF0):
    base=load*16;cs=load+SEGMENT;u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,1<<20)
    before=bytearray(b'\xA5'*(1<<20));body=mz.relocated_program_image(load);before[base:base+len(body)]=body
    u.mem_write(0,bytes(before));expected=bytearray(before)
    initial={n:(((seed^0x5AA5)<<16)|((seed+i*0x231)&65535)) for i,n in enumerate(REGS)}
    initial['sp']=(initial['sp']&0xFFFF0000)|stack
    for n,r in REGS.items():u.reg_write(r,initial[n])
    segments=dict(cs=cs,ds=load+0xD7F,es=seed,ss=ss,fs=seed^0xA55A,gs=seed^0x5AA5)
    for n,v in segments.items():u.reg_write(getattr(x,'UC_X86_REG_'+n.upper()),v)
    u.reg_write(x.UC_X86_REG_EFLAGS,flags)
    return_ip=SITE-SEGMENT*16+5;events=[(ss*16+stack-2,2,cs),(ss*16+stack-4,2,return_ip)]
    for at,size,value in events:expected[at:at+size]=value.to_bytes(size,'little')
    instructions={i.address:i.size for i in Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[SITE:SITE+5],SITE)}
    observed=[];covered=set();arrived=False;error=None
    def fail(e):
        nonlocal error
        error=str(e);u.emu_stop()
    def code(uc,address,size,data):
        nonlocal arrived
        try:
            rva=address-base
            if rva==ENTRY:arrived=True;uc.emu_stop();return
            need(instructions.get(rva)==size,'only complete call-site instructions before callee entry')
            covered.update(range(rva,rva+size))
        except Exception as e:fail(e)
    def write(uc,access,address,size,value,data):observed.append((address,size,value))
    hooks=[u.hook_add(UC_HOOK_CODE,code),u.hook_add(UC_HOOK_MEM_WRITE,write)]
    try:
        try:u.emu_start(base+SITE,1<<20,count=8)
        except UcError as e:raise ValueError('OP Music Room call guest fault') from e
        need(error is None,error or 'guest error');need(arrived and len(covered)==5,'arrival before any callee instruction')
        actual={n:u.reg_read(r) for n,r in REGS.items()};want=dict(initial,sp=(initial['sp']&0xFFFF0000)|(stack-4))
        need(actual==want,'complete WORD/DWORD registers including ESP')
        need(all(u.reg_read(getattr(x,'UC_X86_REG_'+n.upper()))==v for n,v in segments.items()),'all segment registers')
        need(u.reg_read(x.UC_X86_REG_IP)==0x1306,'actual callee IP')
        need(u.reg_read(x.UC_X86_REG_EFLAGS)&0xED5==flags&0xED5,'all defined flags and IF/DF preserved')
        need(observed==events and bytes(u.mem_read(0,1<<20))==expected,'complete ordered stores and every physical memory byte')
        return dict(registers=actual,segments=segments,flags=flags&0xED5,stores=observed,callee_instruction_executed=False)
    finally:
        for h in hooks:u.hook_del(h)

def runtime(target,candidate):
    observations=[]
    for mz in (target,candidate):
        loads=[]
        for load in (0x1000,0x3000):
            trace=hashlib.sha256();count=0
            for seed in (0,1,0x1357,0xECA8,0x8000,0xFFFF):
                for flags in (2,0x202,0x402,0xED7):
                    for ss in (0x7000,0x8000):
                        for stack in (0x80,0xFFF0):
                            trace.update(json.dumps(run(mz,load,seed=seed,flags=flags,ss=ss,stack=stack),sort_keys=True).encode());count+=1
            loads.append(dict(load_segment=load,cases=count,executed_call_bytes=5,maximum_stack_depth=4,ignored_stack_bytes=0,trace_sha256=trace.hexdigest()))
        observations.append(loads)
    need(observations[0]==observations[1],'independent target/candidate call-frame observations')
    return dict(images=2,cases_per_image=192,observations=observations[0],callee_implementation_executed=False,source_acceptance=False)

def negative_controls(target):
    rejected=[]
    for name,at,old,new in (('preserve-incoming-CF',SITE,0x90,0xF8),('push-real-CS',SITE+1,0x0E,0x1E),
                            ('real-callee-displacement',SITE+3,target.program_image[SITE+3],target.program_image[SITE+3]^1)):
        raw=bytearray(target.program_image);need(raw[at]==old,'instruction mutation anchor');raw[at]=new
        try:run(replace(target,program_image=bytes(raw)),0x3000,flags=0xED7)
        except ValueError:rejected.append(name)
        else:raise ValueError('OP Music Room instruction control survived: '+name)
    return dict(actual_instruction_mutations=3,rejected=rejected,source_or_stored_product_modified=False)
