"""Two native questions: resumable 386 register context and target-chain unwind."""
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from build_th03_mainl_resources_work import need
from build_th03_mainl_display_work import payload,literal_fields
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

CALLBACK=b'''
public _xx_probe_raise_handler
_xx_probe_raise_handler proc far
push bp
mov bp,sp
push ds
push si
push di
push ss
pop es
mov ax,[bp+10]
mov ss:[07f2h],ax
mov ax,[bp+16]
mov ss:[07f4h],ax
mov ax,[bp+18]
mov ss:[07f6h],ax
inc word ptr ss:[07f8h]
lds si,[bp+6]
mov di,0800h
mov cx,38
cld
rep movsw
cmp word ptr ss:[07f0h],0
jne short xx_probe_unwind
lds si,[bp+12]
add si,140
mov di,0900h
mov cx,32
rep movsw
les bx,[bp+12]
mov word ptr es:[bx+176],0beefh
mov word ptr es:[bx+178],0deadh
xor ax,ax
jmp short xx_probe_return
xx_probe_unwind:
mov ax,1
xx_probe_return:
pop di
pop si
pop ds
pop bp
retf
_xx_probe_raise_handler endp
'''


def callback(raw):
    need(not literal_fields(raw),'diagnostic handler has no native fields')
    p=payload(raw);pubs=code_publics(raw,1);size=segment_definitions(raw)[0]['size']
    entries=[(at,n) for at,n in pubs if n=='_xx_probe_raise_handler']
    need(len(entries)==1,'one actual TASM callback')
    at=entries[0][0];code=bytes(p[1,q] for q in range(at,size))
    instructions=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code,at))
    need(sum(i.size for i in instructions)==len(code) and instructions[-1].mnemonic=='retf','whole assembled callback body')
    return code


def run(image,entry,kind,handler,cpu_offset=None,memcpy_entry=None,memcpy_code=None,stack_offset=0xFF00):
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_INTR
    from unicorn.x86_const import UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_ES,UC_X86_REG_FS,UC_X86_REG_GS,UC_X86_REG_SS,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_ESI,UC_X86_REG_EDI,UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ECX,UC_X86_REG_EDX,UC_X86_REG_IP,UC_X86_REG_SP
    need(kind in ('raise-386-context','global-unwind-target'),'bounded throw probe')
    u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x80000);u.mem_write(0,image)
    ss,sp,finish=0x7000,stack_offset,0xF100
    def words(at,*v):u.mem_write(at,struct.pack('<'+'H'*len(v),*v))
    def read(at,n):return list(struct.unpack('<'+'H'*n,u.mem_read(at,n*2)))
    initial=[(UC_X86_REG_EAX,0x12341111),(UC_X86_REG_EBX,0x23452222),
        (UC_X86_REG_ECX,0x34563333),(UC_X86_REG_EDX,0x45674444),
        (UC_X86_REG_ESI,0x56775555),(UC_X86_REG_EDI,0x67886666),
        (UC_X86_REG_EBP,0x78997777),(UC_X86_REG_ESP,sp),
        (UC_X86_REG_DS,0xE3F),(UC_X86_REG_ES,0x6600),
        (UC_X86_REG_FS,0x6300),(UC_X86_REG_GS,0x6400),
        (UC_X86_REG_SS,ss),(UC_X86_REG_CS,0)]
    for reg,value in initial:u.reg_write(reg,value)
    u.mem_write(0x65100,handler)
    words(ss*16+0x14,0x200)
    words(ss*16+0x200,0x240,0x100,0x6500)
    words(ss*16+0x240,0xFFFF,0x100,0x6500)
    if kind=='raise-386-context':
        need(cpu_offset is not None and memcpy_entry is not None,'actual native CPU slot and memcpy entry')
        u.mem_write(0xE3F0+cpu_offset,b'\x03')
        # Ordinary continuable exception,17 supplied DWORDs cap to15. All
        # general-register high halves are observable through actual PUSHAD.
        words(ss*16+sp,finish,0,0x1234,0x1234,0,0,17,0,0x100,0x6300)
        u.mem_write(0x63100,struct.pack('<17I',*range(0xA000,0xA011)))
        if memcpy_code:
            # Execute the actual fixed target's entire relocation-free memcpy
            # in separate fixture memory. Redirect the miniature's imported
            # trap entry; neither program image nor object is patched.
            u.mem_write(0x66100,memcpy_code)
    else:
        words(ss*16+0x7F0,1)
        words(ss*16+sp,finish,0,0x240,0)
    returned=[];copies=[]
    def code(uc,site,size,data):
        if kind=='raise-386-context' and site==memcpy_entry:
            copies.append(True)
            if memcpy_code:
                uc.reg_write(UC_X86_REG_CS,0x6600);uc.reg_write(UC_X86_REG_IP,0x100)
        if site==finish:
            returned.append(True);uc.emu_stop()
    def interrupt(uc,number,data):raise ValueError('throw probe reached unresolved trap/interrupt: '+str(number))
    u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_INTR,interrupt)
    u.emu_start(entry,0x80000,count=10000)
    need(returned==[True] and read(ss*16+0x7F2,4)==[0x200,0,0,1],'one actual handler call with near registration and zero dispatcher argument')
    result=dict(case=kind,handler_calls=1,chain=read(ss*16+0x14,1)[0])
    if kind=='raise-386-context':
        need(len(copies)==2,'two actual native memcpy calls; no memory helper model')
        record=read(ss*16+0x800,38)
        context=list(struct.unpack('<16I',u.mem_read(ss*16+0x900,64)))
        expected=[0x6400,0x6300,0x6600,0xE3F,0x67886666,0x56775555,
            0x23452222,0x45674444,0x34563333,0x12341111,0x78997777,
            finish,0,None,0x78990000|((sp+4)&65535),ss]
        need(all(b is None or a==b for a,b in zip(context,expected)),'native 204-byte context segment/general-register layout')
        need(record[:8]==[0x1234,0x234,0,0,0,finish,0,15] and list(struct.unpack('<15I',u.mem_read(ss*16+0x810,60)))==list(range(0xA000,0xA00F)),'reserved code bit clear,far PC,count cap and native argument DWORDs')
        restored=[u.reg_read(reg) for reg,_ in initial[:8]]
        need(restored==[0xDEADBEEF]+[v for _,v in initial[1:7]]+[sp+4] and [u.reg_read(r) for r,_ in initial[8:]]==[v for _,v in initial[8:]],'actual POPAD/POPFD/RETF resumes modified EAX and original caller register/segment frame: '+str((restored,[u.reg_read(r) for r,_ in initial[8:]])))
        result.update(record_header=record[:8],information=list(range(0xA000,0xA00F)),context=context,restored_registers=restored,sp=sp+4,actual_memcpy_calls=2)
    else:
        record=read(ss*16+0x800,8)
        need(record[:4]==[0x26,0,2,0] and record[7]==0 and result['chain']==0x240,'local unwind record and stop-before-target chain update')
        need(u.reg_read(UC_X86_REG_SP)==sp+4 and all(u.reg_read(r)==v for r,v in initial if r in (UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_EBP,UC_X86_REG_ESI,UC_X86_REG_EDI)),'far cdecl global unwind frame')
        result.update(code=0x26,flags=2,information_count=0,sp=sp+4)
    return result


def forward(image,entry,toss,kind):
    """Observe actual wrapper arguments before any allocation or EH helper."""
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_INTR
    from unicorn.x86_const import UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_SP,UC_X86_REG_BP
    need(kind in ('throw-forward','rethrow-ss-forward'),'bounded throw wrapper')
    u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x80000);u.mem_write(0,image)
    ss,sp=0x7000,0xFF00
    def words(at,*v):u.mem_write(at,struct.pack('<'+'H'*len(v),*v))
    for reg,value in [(UC_X86_REG_CS,0),(UC_X86_REG_DS,0xE3F),(UC_X86_REG_SS,ss),(UC_X86_REG_SP,sp),(UC_X86_REG_BP,0xAAAA)]:u.reg_write(reg,value)
    common=[0x100,0x6300,0x300,ss,0x500,0x6300,0x600,0x6500,0x25,0x12,37,0x700,0x6300]
    if kind=='throw-forward':
        words(ss*16+sp,0xF100,0,*common);expected=common+[0xF100,0,0]
    else:
        words(ss*16+sp,0xF100,0,37,0x700,0x6300)
        words(ss*16+0x16,0x200,0x6000);words(0x60200,0x1000,0x6000)
        words(0x61004,0x100,0x6300,0x500,0x6300,0x12)
        words(0x6101E,0x600,0x6500,0x25);words(0x61036,0x300)
        u.mem_write(0x61038,b'\0');expected=common+[0xF100,0,1]
    observed=[]
    def stop(uc,site,size,data):
        if site==toss:
            at=ss*16+uc.reg_read(UC_X86_REG_SP)
            observed.extend(struct.unpack('<16H',uc.mem_read(at+4,32)));uc.emu_stop()
    def interrupt(uc,number,data):raise ValueError('throw wrapper reached an unexpected helper/interrupt: '+str(number))
    u.hook_add(UC_HOOK_CODE,stop);u.hook_add(UC_HOOK_INTR,interrupt);u.emu_start(entry,0x80000,count=1000)
    need(observed==expected and u.reg_read(UC_X86_REG_SS)==ss and u.reg_read(UC_X86_REG_DS)==0xE3F,'actual32-byte far toss frame,caller PC and SS-relative rethrow argument')
    return dict(case=kind,toss_arguments=observed,ss=ss,ds=0xE3F)
