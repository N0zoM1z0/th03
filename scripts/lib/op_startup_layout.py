"""Whole far OP startup in the natural 15-procedure OP_01 TC4 producer."""
import hashlib
import re
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.op_cfg_layout import SOURCE,WRAPPER,OBJECT,SEGMENT,OFFSET,DATA_SEGMENT,verify as enclosing_layout
from lib.op_option_layout import native_image

START,SIZE,NATIVE=0xA417,263,2831
FUNCTIONS=(('th03-op-decoded-entry-startup','startup',NATIVE,SIZE,'_main',0),)
EXTERNALS={2:('GAIJI_BACKUP',0,0xEF6),3:('GAIJI_RESTORE',0,0xF1A),4:('GAIJI_ENTRY_BFNT',0,0xF36),
 5:('_graph_VramZoom',DATA_SEGMENT,0x2C8),6:('GRAPH_400LINE',0,0x10FE),10:('TEXT_CLEAR',0,0x21F4),
 13:('@FRAME_DELAY$QI',0xBEB,0x2EE),15:('_resident',DATA_SEGMENT,0x2464),16:('_input_sp',DATA_SEGMENT,0x1AA6),
 17:('@INPUT_MODE_INTERFACE$QV',0xBEB,0xAD6),18:('DOS_PUTS2',0,0x688),27:('RESPAL_CREATE',0,0x2AC6),
 28:('RESPAL_FREE',0,0x2B3C),29:('@game_exit_to_dos$qv',0xBEB,8),30:('@game_init_op$qnxuc',0xBEB,0x571),
 37:('@op_animate$qv',SEGMENT,0x14E2),38:('@op_fadein_animate$qv',SEGMENT,0x1708),
 39:('@select_cdg_load_part1_of_4$qv',SEGMENT,0x1A8D),40:('@select_cdg_load_part2_of_4$qv',SEGMENT,0x1AC3),
 41:('@select_cdg_load_part3_of_4$qv',SEGMENT,0x1AEF),45:('_getch',0,0x952E)}
MAP_NAMES={13:'frame_delay(int)',17:'input_mode_interface()',29:'game_exit_to_dos()',
 30:'game_init_op(const unsigned char far*)',37:'op_animate()',38:'op_fadein_animate()',
 39:'select_cdg_load_part1_of_4()',40:'select_cdg_load_part2_of_4()',41:'select_cdg_load_part3_of_4()'}
FIELDS=((3058, 4, 207, 86, None, 13, 0),
 (3048, 2, 199, 22, 2, 15, 0),
 (3024, 2, 199, 20, 2, 3, 2),
 (3019, 4, 207, 86, None, 17, 0),
 (3014, 2, 135, 22, 1, 40, 0),
 (3006, 2, 199, 22, 2, 16, 0),
 (3001, 2, 199, 20, 2, 3, 2),
 (2994, 2, 135, 22, 1, 38, 0),
 (2986, 2, 199, 22, 2, 15, 0),
 (2975, 2, 199, 22, 2, 15, 0),
 (2971, 2, 135, 22, 1, 37, 0),
 (2961, 2, 199, 22, 2, 15, 0),
 (2954, 2, 135, 22, 1, 40, 0),
 (2951, 2, 135, 22, 1, 41, 0),
 (2948, 2, 135, 22, 1, 39, 0),
 (2931, 2, 199, 22, 2, 15, 0),
 (2922, 4, 207, 86, None, 4, 0),
 (2919, 2, 199, 20, 2, 2, 476),
 (2913, 4, 207, 86, None, 2, 0),
 (2908, 2, 199, 20, 2, 2, 417),
 (2895, 4, 207, 86, None, 30, 0),
 (2892, 2, 199, 20, 2, 2, 405),
 (2884, 4, 207, 86, None, 45, 0),
 (2879, 4, 207, 86, None, 18, 0),
 (2876, 2, 199, 20, 2, 2, 344),
 (2870, 4, 207, 86, None, 18, 0),
 (2867, 2, 199, 20, 2, 2, 280),
 (2861, 4, 207, 86, None, 18, 0),
 (2858, 2, 199, 20, 2, 2, 238),
 (2851, 2, 199, 22, 2, 5, 0),
 (2845, 4, 207, 86, None, 27, 0),
 (2840, 4, 207, 86, None, 10, 0),
 (2835, 4, 207, 86, None, 6, 0),
 (3088, 4, 204, 86, None, 28, 0),
 (3083, 4, 204, 86, None, 29, 0),
 (3078, 4, 204, 86, None, 10, 0),
 (3073, 4, 204, 86, None, 3, 0),
 (3064, 2, 196, 20, 2, 2, 210))


def need(value,message):
    if not value:
        raise ValueError('OP startup layout: '+str(message))


def verify(root,work,target,candidate):
    enclosing_layout(work,target,candidate)
    raw=(work/OBJECT).read_bytes()
    image=native_image(raw,FUNCTIONS,FIELDS,EXTERNALS)[NATIVE:NATIVE+SIZE]
    need(image==target.program_image[START:START+SIZE]==candidate.program_image[START:START+SIZE],
         'entire independently resolved native startup body')
    rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image,START))
    need(sum(i.size for i in rows)==SIZE and rows[-1].mnemonic=='retf' and not rows[-1].op_str,
         'complete far cdecl no-argument body,including common early-return tail')
    near=[(i.address,int(i.op_str,16)) for i in rows if i.mnemonic=='call']
    need(near==[(0xA476,0x9908),(0xA48B,0xB38D),(0xA48E,0xB3EF),(0xA491,0xB3C3),
        (0xA494,0x9BDF),(0xA4A2,0xADE2),(0xA4B9,0xB008),(0xA4BC,0x9E16),
        (0xA4CA,0xA0E0),(0xA4CD,0xB3C3),(0xA4E6,0xA0E0),(0xA4EB,0xA203),(0xA505,0x99C3)],
         'all13 real internal or GROUP_01 near calls')
    far=[(i.address,tuple(int(v.strip(),16) for v in i.op_str.split(','))) for i in rows if i.mnemonic=='lcall']
    need(len(far)==16,'all16 real native far calls')
    text=(work/'obj/th03/op.map').read_text()
    for index,(name,segment,offset) in EXTERNALS.items():
        symbol=MAP_NAMES.get(index,name)
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,'both external MAP tables: '+symbol)
    need(len(re.findall(r'(?m)^\s*0990:0B17\s+_main\s*$',text))==2,'both native startup publics')
    relocations=[[SEGMENT,OFFSET+site+2] for site,width,_,method,*_ in FIELDS if width==4 and method==0x56]
    for mz in (target,candidate):
        need([[r.segment,r.offset] for r in mz.relocations if START<=r.linear<START+SIZE]==relocations,'complete literal ordered MZ vector')
        need(not any(r.linear<START+SIZE and r.linear+2>START and not START<=r.linear<=START+SIZE-2 for r in mz.relocations),'no straddling owner field')
    digest=hashlib.sha256(image).hexdigest()
    owner=dict(unit_id=FUNCTIONS[0][0],name='_main',source=SOURCE,object=OBJECT,segment=SEGMENT,offset=0xB17,
        start=START,size=SIZE,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=digest,candidate_sha256=digest,ordered_relocations=relocations,argument_bytes=0,callee_pop_bytes=0,
        private_data_bytes=0,private_bss_bytes=0,abi='far cdecl noargs; saved BP; real common RETF and cdecl game-init filename cleanup4')
    return dict(owners=[owner],functions=1,code_bytes=SIZE,instruction_bytes=SIZE,ordered_native_fields=[list(f) for f in FIELDS],
        ordered_relocations=relocations,near_calls=[list(v) for v in near],far_calls=[[a,list(t)] for a,t in far],
        containing_CODE_bytes=3094,containing_DATA_bytes=487,containing_BSS_bytes=6,
        containing_DATA_BSS_or_other_CODE_newly_accepted=False,whole_product_accepted=False)
