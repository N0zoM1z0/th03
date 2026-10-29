"""Concrete DOS RTTI address/access questions;execute only actual native code."""
import struct
from build_th03_mainl_resources_work import need

CASES=('virtual-shared-address','distinct-base-ambiguity','downcast-source-address',
    'typeinfo-vtable-adjustment','jump-to-catch-registers')


def run(image,entry,kind,search=None):
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_INTR
    from unicorn.x86_const import UC_X86_REG_CS,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_SP,UC_X86_REG_BP,UC_X86_REG_SI,UC_X86_REG_DI,UC_X86_REG_AX,UC_X86_REG_BX,UC_X86_REG_CX,UC_X86_REG_DX
    need(kind in CASES,'bounded RTTI question')
    u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x80000);u.mem_write(0,image)
    ss,sp,finish=0x7000,0xFF00,0xF100
    def words(at,*v):u.mem_write(at,struct.pack('<'+'H'*len(v),*v))
    def descriptor(off,name,has_bases=False):
        words(0x63000+off,8,3,38,0,4 if has_bases else 0,0x60,0x80)
        u.mem_write(0x63000+off+38,name+b'\0')
        words(0x63000+off+0x60,0,0);words(0x63000+off+0x80,0,0)
    def bases(off,entries):
        for i,(base,delta,flags) in enumerate(entries):
            words(0x63000+off+0x60+i*8,base,0x6300,delta,flags)
        words(0x63000+off+0x60+len(entries)*8,0,0)
    preserved=[UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_BP,UC_X86_REG_SI,UC_X86_REG_DI]
    expected_preserved=[0xE3F,ss,0xAAAA,0x7777,0x8888]
    for r,v in [(UC_X86_REG_CS,0),(UC_X86_REG_SP,sp),*zip(preserved,expected_preserved)]:u.reg_write(r,v)
    descriptor(0x100,b'Complete',True);descriptor(0x300,b'Left',True)
    descriptor(0x500,b'Right',True);descriptor(0x700,b'Base')
    descriptor(0x900,b'Base')
    words(0x641F8,0x100,0x6300,0,0)
    object_offset=0x100;wanted=0x900;source=0x100;expected_calls=None
    if kind=='virtual-shared-address':
        bases(0x100,[(0x300,0x20,2),(0x500,0x40,3)])
        bases(0x300,[(0x700,4,7)]);bases(0x500,[(0x700,4,7)])
        words(0x65124,0x500);words(0x65144,0x500)
        expected,expected_calls=(0x500,0x6500),3
    elif kind=='distinct-base-ambiguity':
        bases(0x100,[(0x300,0x20,3),(0x500,0x40,3)])
        bases(0x300,[(0x700,4,3)]);bases(0x500,[(0x700,4,3)])
        expected,expected_calls=(0,0),3
    elif kind=='downcast-source-address':
        # DOS downcast validates the actual source subobject address. The
        # containment search does not require public links in this path.
        bases(0x100,[(0x300,0x20,2)]);bases(0x300,[(0x700,8,2)])
        words(0x641FC,0x28,0);object_offset=0x128;wanted=0x300;source=0x700
        expected,expected_calls=(0x120,0x6500),2
    elif kind=='typeinfo-vtable-adjustment':
        # A secondary vtable points back16 bytes;only tpp,+4,may change.
        words(0x6420E,16);words(0x66100,0x1234,0x5678,0,0)
        words(ss*16+sp,finish,0,0x100,0x6500,0x210,0x6400,0,0,0x100,0x6600)
        expected=(0x100,0x6600)
    else:
        u.reg_write(UC_X86_REG_AX,finish);u.reg_write(UC_X86_REG_DX,0)
        u.reg_write(UC_X86_REG_BX,0xE000);u.reg_write(UC_X86_REG_CX,0x2222)
        expected=(finish,0);expected_preserved[2]=0x2222
    if kind in CASES[:3]:
        words(ss*16+sp,finish,0,object_offset,0x6500,0x200,0x6400,
            source,0x6300,wanted,0x6300,0)
    returned=[];search_calls=[]
    def code(uc,site,size,data):
        if search is not None and site==search:search_calls.append(True)
        if site==finish:returned.append(True);uc.emu_stop()
    def interrupt(uc,number,data):raise ValueError('RTTI probe reached an unresolved helper/interrupt: '+str(number))
    u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_INTR,interrupt)
    u.emu_start(entry,0x80000,count=15000)
    value=(u.reg_read(UC_X86_REG_AX),u.reg_read(UC_X86_REG_DX))
    need(returned==[True] and value==expected,'actual RTTI/jump return: '+kind)
    final_sp=0xE000 if kind=='jump-to-catch-registers' else sp+4
    need(u.reg_read(UC_X86_REG_SP)==final_sp and [u.reg_read(r) for r in preserved]==expected_preserved,'actual far return or register jump with original DS/SS/BP/SI/DI')
    if expected_calls is not None:need(len(search_calls)==expected_calls,'actual recursive searches,without replacing the search helper')
    result=dict(case=kind,ax=value[0],dx=value[1],sp=final_sp,registers=expected_preserved,actual_recursive_search_calls=len(search_calls))
    if kind=='typeinfo-vtable-adjustment':
        obj=list(struct.unpack('<4H',u.mem_read(0x66100,8)))
        need(obj==[0x1234,0x5678,0x100,0x6300],'original typeinfo vptr survives while tpp takes the complete type')
        result['typeinfo_words']=obj
    return result
