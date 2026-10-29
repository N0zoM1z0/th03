"""Diagnostic native callbacks for three concrete decoded DOS member-call ABIs."""
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from build_th03_mainl_resources_work import need
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

CALLBACKS=b'''
public _xx_probe_copy
_xx_probe_copy proc far
mov ss:[0800h],ax
mov ss:[0802h],dx
mov ss:[0804h],bx
mov ss:[0806h],ds
inc word ptr ss:[0808h]
retf
_xx_probe_copy endp
public _xx_probe_dtor
_xx_probe_dtor proc far
push bp
mov bp,sp
mov ss:[0800h],ds
mov ss:[0802h],si
mov ax,[bp+6]
mov ss:[0804h],ax
inc word ptr ss:[0808h]
pop bp
retf
_xx_probe_dtor endp
public _xx_probe_member
_xx_probe_member proc far
push bp
mov bp,sp
mov ax,[bp+6]
mov ss:[0800h],ax
mov ax,[bp+8]
mov ss:[0802h],ax
mov ss:[0804h],ds
inc word ptr ss:[0808h]
pop bp
retf 4
_xx_probe_member endp
'''


def context(traps):
    need(traps.count(b'_TEXT ends')==1,'one actual diagnostic context CODE segment')
    return traps.replace(b'_TEXT ends',CALLBACKS+b'_TEXT ends')


def callbacks(raw):
    """Use actual assembler output; none of the callback bodies is modeled."""
    need(not literal_fields(raw),'callback fixture has no relocated operands')
    data=payload(raw);pubs=code_publics(raw,1);size=segment_definitions(raw)[0]['size'];result={}
    for index,(at,name) in enumerate(pubs):
        if not name.startswith('_xx_probe_'):continue
        end=pubs[index+1][0] if index+1<len(pubs) else size
        code=bytes(data[1,i] for i in range(at,end));ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code,at))
        need(sum(i.size for i in ins)==len(code) and ins[-1].mnemonic=='retf','whole actual callback instructions: '+name)
        result[name]=code
    need(set(result)=={'_xx_probe_copy','_xx_probe_dtor','_xx_probe_member'},'all three actual native callback fixtures')
    return result


def run(image,entry,kind,callback):
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_INTR
    from unicorn.x86_const import UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_SP,UC_X86_REG_BP,UC_X86_REG_SI,UC_X86_REG_DI
    u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x80000);u.mem_write(0,image)
    ss,sp,finish=0x7000,0xFF00,0xF100
    # Put the real assembled callback in separate probe memory, outside both
    # immutable program images. It uses SS operands and has no native fixups.
    u.mem_write(0x65100,callback)
    registers=[UC_X86_REG_SP,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_BP,UC_X86_REG_SI,UC_X86_REG_DI]
    for reg,value in [(UC_X86_REG_CS,0),(UC_X86_REG_DS,0xE3F),(UC_X86_REG_SS,ss),(UC_X86_REG_SP,sp),(UC_X86_REG_BP,0xAAAA),(UC_X86_REG_SI,0x7777),(UC_X86_REG_DI,0x8888)]:u.reg_write(reg,value)
    u.mem_write(ss*16+0x16,struct.pack('<2H',0x200,0x6000))
    u.mem_write(0x60206,struct.pack('<H',0x6400))
    if kind=='copy-fastcall-virtual':
        args=[0x3456,0x6600,0x4567,0x6700,0x100,0x6500,0x1121]
        expected=[0,0x3456,0x4567,0x6400,1]
    elif kind=='dtor-far-fastthis':
        args=[0x3456,0x6600,0x100,0x6500,0x85,1]
        expected=[0x6600,0x3456,2,0,1]
    else:
        need(kind=='member-far-pascal','bounded call-adapter probe selection')
        args=[0x3456,0x6600,0x100,0x6500,7]
        expected=[0x3456,0x6600,0x6400,0,1]
    u.mem_write(ss*16+sp,struct.pack('<'+'H'*(len(args)+1),finish,*args))
    returned=[];called=[]
    def stop(uc,site,count,data):
        if site==0x65100:called.append(True)
        if site==finish:returned.append(True);uc.emu_stop()
    def interrupt(uc,number,data):raise ValueError('call adapter reached an unresolved runtime helper/interrupt: '+str(number))
    u.hook_add(UC_HOOK_CODE,stop);u.hook_add(UC_HOOK_INTR,interrupt);u.emu_start(entry,0x80000,count=2000)
    observed=list(struct.unpack('<5H',u.mem_read(ss*16+0x800,10)))
    frame=[u.reg_read(r) for r in registers]
    need(returned==[True] and called==[True] and observed==expected,'actual '+kind+' callback receives original register/stack arguments exactly once')
    need(frame==[sp+2,0xE3F,ss,0xAAAA,0x7777,0x8888],'near cdecl adapter restores caller DS/SS/BP/SI/DI and exact SP')
    return dict(case=kind,callback_words=observed,sp=frame[0],ds=frame[1],ss=frame[2],bp=frame[3],si=frame[4],di=frame[5],actual_callback_calls=len(called))
