"""Eight complete driver lifecycle procedures under terminal DOS contracts."""
import hashlib
import re
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.zun_driver_layout import review,resolve_native
from stage_th03_zun_driver import bodies,dos_text
from verify_th03_zun_driver_hybrid import RESIDENT_PROCS
SOURCE='src/zun/driver_resident.inl'
RANGES=tuple((n,a,b-a) for n,a,b in RESIDENT_PROCS)
TERMINAL={0x15F,0x182,0x18F,0x1AE,0x1CB,0x2A2}
FIXUPS=((0x10E,0xF7A),(0x111,0x676),(0x11C,0x100),(0x121,0x102),(0x131,0xF40),(0x139,0xF40),
 (0x145,0xF43),(0x148,0xF38),(0x14E,0xF43),(0x157,0xC80),(0x15A,0x676),(0x173,0x920),(0x177,0x1070),
 (0x17D,0xA36),(0x187,0xFB9),(0x18A,0x676),(0x194,0xF40),(0x1A6,0xF47),(0x1A9,0x676),(0x1B1,0xF3C),
 (0x1B5,0xF43),(0x1C3,0xF47),(0x1C6,0x676),(0x1CE,0xF3E),(0x1D2,0xF43),(0x1D8,0xA0A),(0x1DB,0xF42),
 (0x1E2,0x520),(0x1E5,0x540),(0x1E8,0x610),(0x1EE,0xF3C),(0x205,0x540),(0x208,0xA0A),(0x20D,0xA0A),
 (0x212,0xA0A),(0x217,0xA0A),(0x21B,0xA0A),(0x221,0xBD0),(0x227,0xC10),(0x234,0x103E),(0x239,0xF45),
 (0x240,0xF45),(0x24A,0xF42),(0x26E,0x22A),(0x272,0xF42),(0x282,0xF38),(0x285,0xF3A),(0x28C,0xF42),
 (0x293,0xF5E),(0x296,0x640),(0x29D,0xF43),(0x2A7,0xC9D),(0x2AA,0x676),(0x2B3,0xF42),(0x2CE,0xF38),
 (0x2D2,0xF3A),(0x2DB,0xF42),(0x2F7,0xCB6),(0x2FA,0x676),(0x30A,0xCC9),(0x30D,0x676),(0x31D,0xCE4),
 (0x320,0x676),(0x32A,0xCFD),(0x32D,0x676),(0x332,0xD12),(0x335,0x676),(0x33A,0xD23),(0x33D,0x676))
RELATIVE={0x111,0x15A,0x173,0x17D,0x18A,0x1A9,0x1C6,0x1D8,0x1E2,0x1E5,0x1E8,0x205,0x208,0x20D,
 0x212,0x217,0x21B,0x221,0x227,0x296,0x2AA,0x2FA,0x30D,0x320,0x32D,0x335,0x33D}
def need(v,m):
    if not v:raise ValueError('ZUN lifecycle layout: '+m)
def control_flow(image):
    ins={i.address:i for _,a,s in RANGES for i in Cs(CS_ARCH_X86,CS_MODE_16).disasm(image[a-256:a-256+s],a)}
    need(sum(i.size for i in ins.values())==564,'whole instruction boundaries')
    for address,ax in ((0x15F,'0x4c01'),(0x182,'0x4c00'),(0x18F,'0x4c01'),(0x1AE,'0x4c01'),(0x1CB,'0x4c01'),(0x2A2,'0x3100')):
        need(ins[address].mnemonic=='int' and ins[address].op_str=='0x21' and ins[address-3].mnemonic=='mov'
             and ins[address-3].op_str=='ax, '+ax,'literal terminal DOS service and AX predecessor')
    seen=set();todo=[a for _,a,_ in RANGES]
    while todo:
        a=todo.pop()
        if a in seen:continue
        need(a in ins,'bounded direct edge');i=ins[a];seen.add(a)
        if i.mnemonic in ('ret','iret') or a in TERMINAL:continue
        if i.mnemonic.startswith('j'):todo.append(int(i.op_str,16))
        if i.mnemonic=='call' and i.op_str.startswith('0x') and int(i.op_str,16) in ins:todo.append(int(i.op_str,16))
        if i.mnemonic!='jmp':todo.append(a+i.size)
    dead=[(a,i.size) for a,i in ins.items() if a not in seen]
    need(dead==[(0x184,2),(0x191,6),(0x197,2),(0x199,2),(0x19B,1),(0x2A4,2)],'fifteen DOS-terminal-unreachable bytes')
    reachable={p for a in seen for p in range(a,a+ins[a].size)}
    return ins,reachable,dict(code_bytes=564,reachable_owner_bytes=549,terminal_unreachable_owner_bytes=15,
        terminal_DOS_sites=sorted(TERMINAL),unreachable_instructions=[dict(address=a,size=s) for a,s in dead],unchecked_indirect_service_table=True)
def verify(work,target,candidate,at,files,maintained):
    obj=(work/'driver/driver.obj').read_bytes();physical=review(obj,(work/'driver/driver.map').read_bytes());im,fixups,blocks=resolve_native(obj)
    need(im==target==candidate and len(im)==4224,'whole native driver equality')
    source=bodies(maintained[SOURCE].decode());need(set(source)=={n for n,_,_ in RANGES},'eight whole maintained bodies');owners=[]
    for name,a,size in RANGES:
        raw=dos_text(source[name]);slots=[n for n,b in files.items() if n.startswith('driver/procs/') and b==raw];need(len(slots)==1,'unique source slot');slot=slots[0]
        need((work/slot).read_bytes()==raw and len(re.findall(rb'(?m)^include '+re.escape(slot.removeprefix('driver/').encode())+rb'\r?$',files['driver/driver.asm']))==1,'actual consumed source')
        fs=[f for f in fixups if a<=f['address']<a+size];digest=hashlib.sha256(im[a-256:a-256+size]).hexdigest()
        owners.append(dict(unit_id='th03-zun-decoded-driver-'+name.removeprefix('sprite16_').replace('_','-'),source=SOURCE,procedure=name,object='driver/driver.obj',include=slot,start=a,size=size,origin='library',
            coordinate_space='decoded-payload-com',payload_option='-4',payload_file_offset=a-256,decoded_file_offset=at+a-256,canonical_file_offset=None,format='COM',argument_bytes=0,callee_pop_bytes=0,
            private_data_bytes=0,private_bss_bytes=0,abi='near register/DOS lifecycle, except IRET service dispatcher; DS=driver group; terminal DOS 4C/31 contracts',
            ordered_relocations=[],ordered_native_fixups=fs,target_sha256=digest,candidate_sha256=digest))
    fs=[f for o in owners for f in o['ordered_native_fixups']]
    need([(f['address'],f['target_address']) for f in fs]==list(FIXUPS) and all(f['width']==2 and f['self_relative']==(f['address'] in RELATIVE) for f in fs),'69 literal WORD fields, 27 relative')
    _,_,cfg=control_flow(im)
    return dict(owners=owners,functions=8,code_bytes=564,ordered_native_fixups=fs,control_flow=cfg,native_layout=physical,native_records=blocks,
        private_data_bytes=0,private_bss_bytes=0,enclosing_driver_accepted=False,reserved_spans_owned=False,original_assembler_identified=False)
