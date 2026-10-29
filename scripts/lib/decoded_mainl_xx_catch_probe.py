"""Concrete native catch-copy,free-callback and virtual-base ABI observations."""
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from build_th03_mainl_resources_work import need
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

CALLBACKS=b'''
public _xx_probe_catch_ctor
_xx_probe_catch_ctor proc far
push bp
mov bp,sp
mov ax,[bp+6]
mov ss:[0800h],ax
mov ax,[bp+8]
mov ss:[0802h],ax
mov ax,[bp+10]
mov ss:[0804h],ax
mov ax,[bp+12]
mov ss:[0806h],ax
mov ax,[bp+14]
mov ss:[0808h],ax
mov ss:[080ah],ds
inc word ptr ss:[080ch]
pop bp
retf
_xx_probe_catch_ctor endp
public _xx_probe_catch_free
_xx_probe_catch_free proc far
push bp
mov bp,sp
mov ax,[bp+6]
mov ss:[0800h],ax
mov ax,[bp+8]
mov ss:[0802h],ax
mov ss:[0804h],ds
inc word ptr ss:[080ch]
pop bp
retf
_xx_probe_catch_free endp
'''


def context(traps):
    need(traps.count(b'_TEXT ends')==1,'one diagnostic context CODE segment')
    return traps.replace(b'_TEXT ends',CALLBACKS+b'_TEXT ends')


def callbacks(raw):
    need(not literal_fields(raw),'real catch callbacks have no relocated operands')
    p=payload(raw);pubs=code_publics(raw,1);size=segment_definitions(raw)[0]['size'];result={}
    for i,(at,name) in enumerate(pubs):
        if not name.startswith('_xx_probe_catch_'):continue
        end=pubs[i+1][0] if i+1<len(pubs) else size
        code=bytes(p[1,q] for q in range(at,end));ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code,at))
        need(sum(q.size for q in ins)==len(code) and ins[-1].mnemonic=='retf','complete actual catch callback: '+name);result[name]=code
    need(set(result)=={'_xx_probe_catch_ctor','_xx_probe_catch_free'},'both actual TASM catch callbacks')
    return result


def run(image,entry,kind,callback=None):
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_INTR
    from unicorn.x86_const import UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_SP,UC_X86_REG_BP,UC_X86_REG_SI,UC_X86_REG_DI,UC_X86_REG_AX,UC_X86_REG_DX
    u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x80000);u.mem_write(0,image)
    ss,sp,finish=0x7000,0xFF00,0xF100
    def words(at,*v):u.mem_write(at,struct.pack('<'+'H'*len(v),*v))
    def read(at,n):return list(struct.unpack('<'+'H'*n,u.mem_read(at,n*2)))
    regs=[UC_X86_REG_SP,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_BP,UC_X86_REG_SI,UC_X86_REG_DI]
    for reg,value in [(UC_X86_REG_CS,0),(UC_X86_REG_DS,0xE3F),(UC_X86_REG_SS,ss),(UC_X86_REG_SP,sp),(UC_X86_REG_BP,0xAAAA),(UC_X86_REG_SI,0x7777),(UC_X86_REG_DI,0x8888)]:u.reg_write(reg,value)
    words(ss*16+0x16,0x200,0x6000);words(0x60206,0x6400)
    if callback:u.mem_write(0x65100,callback)
    if kind=='class-copy':
        words(ss*16+sp,finish,0x600,0x6300,0x200,0x1000,0x6000,0x700,0x6300,0x4000)
        words(0x63600,0,0,0x100,0x6300,1,0x100,0x6500,0x1005)
        words(0x63100,8,3,38,0,1);words(0x63700,0xFFF0,8)
        words(0x61004,0x100,0x6300);words(0x6100E,8,0x100,0x6300,3)
        words(0x61024,0x200);words(0x61026,0x600,0x6300)
        u.mem_write(0x61038,b'\x01\0ABCDEFGH')
        expected_callback=[0x3FF0,ss,0,0x103A,0x6000,0x6400,1];pop=2
    elif kind=='catch-free':
        words(ss*16+sp,finish,0);words(ss*16+0x14,0x200)
        words(0x60200,0x1000,0x6000);words(0x61000,0x1100,0x6000)
        words(0x61018,0x6300,0x100,0x6500);words(0x61024,0x200)
        words(ss*16+0x206,0x700,0x6300);words(ss*16+0x20C,6);words(0x63706,2)
        expected_callback=[0x1000,0x6000,0x6300,0,0,0,1];pop=4
    else:
        need(kind=='virtual-base','bounded catch ABI probe selection')
        words(ss*16+sp,finish,0,0x100,0x6500,0x200,0x6300,0x380,0x6300)
        words(0x63200,8,3,38,0,0,0x40,0x50)
        words(0x63240,0,0);words(0x63250,0x300,0x6300,6,0);words(0x63258,0,0)
        for at in (0x63300,0x63380):
            words(at,8,3,38);u.mem_write(at+38,b'Base\xe9\0')
        words(0x65106,0x220);expected_callback=None;pop=4
    returned=[];called=[]
    def stop(uc,site,count,data):
        if site==0x65100:called.append(True)
        if site==finish:returned.append(True);uc.emu_stop()
    def interrupt(uc,number,data):raise ValueError('catch probe reached unresolved helper/interrupt: '+str(number))
    u.hook_add(UC_HOOK_CODE,stop);u.hook_add(UC_HOOK_INTR,interrupt);u.emu_start(entry,0x80000,count=10000)
    frame=[u.reg_read(q) for q in regs]
    need(returned==[True] and frame==[sp+pop,0xE3F,ss,0xAAAA,0x7777,0x8888],'actual catch near/far cdecl frame and preserved incoming registers')
    result=dict(case=kind,sp=frame[0],ds=frame[1],ss=frame[2],bp=frame[3],si=frame[4],di=frame[5],actual_callback_calls=len(called))
    if expected_callback:
        observed=read(ss*16+0x800,7);need(called==[True] and observed==expected_callback,'actual catch callback receives original DS and arguments exactly once');result['callback_words']=observed
    if kind=='class-copy':
        result.update(argument_type=read(0x61032,2),argument_address=read(0x61036,1)[0],buffer_and_copy=list(u.mem_read(0x61038,2)))
        need((result['argument_type'],result['argument_address'],result['buffer_and_copy'])==([0x100,0x6300],0x3FF0,[1,1]),'original class catch records a copy and retains thrown object')
    elif kind=='catch-free':
        result.update(exception_head=read(0x60200,2),context=read(ss*16+0x20C,1)[0],chain=read(ss*16+0x14,1)[0])
        need((result['exception_head'],result['context'],result['chain'])==([0x1100,0x6000],2,0x200),'original catch pops descriptor,updates outer context and leaves ERR chain')
    else:
        result['address']=[u.reg_read(UC_X86_REG_AX),u.reg_read(UC_X86_REG_DX)]
        need(not called and result['address']==[0x220,0x6500],'virtual-base WORD retains object segment with nonidentical equal-named type descriptors')
    return result
