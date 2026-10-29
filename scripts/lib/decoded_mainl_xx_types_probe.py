"""Native probes for three DOS type-rule questions and the emergency far slot."""
import struct
from build_th03_mainl_resources_work import need

CASES=('public-reference-base','private-reference-base','near-far-unrelated',
    'void-equal-cv','void-added-cv','emergency-free')


def run(image,entry,equal_entry,kind):
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_INTR
    from unicorn.x86_const import UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_SP,UC_X86_REG_BP,UC_X86_REG_SI,UC_X86_REG_DI,UC_X86_REG_AX
    need(kind in CASES,'bounded type-rule question')
    u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x80000);u.mem_write(0,image)
    ss,sp,finish=0x7000,0xFF00,0xF100
    def words(at,*values):u.mem_write(at,struct.pack('<'+'H'*len(values),*values))
    def type_at(off,mask,name,size=8):
        at=0x63000+off;words(at,size,mask,38);u.mem_write(at+38,name+b'\0')
    regs=[UC_X86_REG_SP,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_BP,UC_X86_REG_SI,UC_X86_REG_DI]
    for reg,value in [(UC_X86_REG_CS,0),(UC_X86_REG_DS,0xE3F),(UC_X86_REG_SS,ss),(UC_X86_REG_SP,sp),(UC_X86_REG_BP,0xAAAA),(UC_X86_REG_SI,0x7777),(UC_X86_REG_DI,0x8888)]:u.reg_write(reg,value)
    if kind=='emergency-free':
        words(ss*16+sp,finish,0,0x1200,0x6000)
        words(ss*16+0x16,0x200,0x6000);words(0x60204,0xA501)
        words(0x60220,0x1200,0x6000);pop=4;expected=None
    else:
        # A public ordinary link followed by a virtual link exercises both
        # searches. The friend list is valid but the DOS helpers never read it.
        type_at(0x100,3,b'Derived');type_at(0x200,3,b'Middle');type_at(0x300,3,b'Base')
        words(0x63108,4,0x40,0x60);words(0x63208,4,0x40,0x60)
        words(0x63140,0x200,0x6300,0,2 if kind=='private-reference-base' else 3)
        words(0x63148,0,0);words(0x63160,0,0);words(0x63240,0,0)
        words(0x63260,0x300,0x6300,0,3);words(0x63268,0,0)
        words(0x63500,0x300,0x6300,0,0)
        source,destination=0x100,0x400
        type_at(0x400,0x2020,b'Base&',4);words(0x63406,0x300,0x6300)
        expected=0 if kind=='private-reference-base' else 1
        if kind=='near-far-unrelated':
            source,destination=0x600,0x700
            type_at(source,0x1010,b'Base near*',2);words(0x63606,0x300,0x6300)
            type_at(destination,0x2010,b'Middle far*',4);words(0x63706,0x200,0x6300)
        elif kind.startswith('void-'):
            source,destination=0x600,0x700
            type_at(source,0x2010,b'Base far*',4);words(0x63606,0x300,0x6300)
            type_at(destination,0x2150 if kind=='void-added-cv' else 0x2050,b'void far*',4)
            words(0x63706,0x800,0x6300);type_at(0x800,0,b'void',0)
            expected=0 if kind=='void-added-cv' else 1
        words(ss*16+sp,finish,source,0x6300,0x500,0x6300,destination,0x6300,0,1)
        pop=2
    returned=[];comparisons=[]
    def stop(uc,site,count,data):
        if site==equal_entry:comparisons.append(True)
        if site==finish:returned.append(True);uc.emu_stop()
    def interrupt(uc,number,data):raise ValueError('type probe reached unresolved helper/interrupt: '+str(number))
    u.hook_add(UC_HOOK_CODE,stop);u.hook_add(UC_HOOK_INTR,interrupt);u.emu_start(entry,0x80000,count=10000)
    frame=[u.reg_read(q) for q in regs]
    need(returned==[True] and frame==[sp+pop,0xE3F,ss,0xAAAA,0x7777,0x8888],'real type/free adapter near/far cdecl frame and preserved DS/SS/BP/SI/DI')
    result=dict(case=kind,sp=frame[0],ds=frame[1],ss=frame[2],bp=frame[3],si=frame[4],di=frame[5],actual_name_comparisons=len(comparisons))
    if kind=='emergency-free':
        result['runtime_flags']=int.from_bytes(u.mem_read(0x60204,2),'little')
        need(result['runtime_flags']==0xA500 and not comparisons,'actual emergency free clears only occupied bit; no allocation failure is modeled')
    else:
        result['matched']=u.reg_read(UC_X86_REG_AX);need(result['matched']==expected,'actual original DOS type rule: '+kind)
        if kind=='near-far-unrelated':need(not comparisons,'older width-only success does not compare pointee types')
    return result
