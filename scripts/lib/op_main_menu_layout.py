"""Complete main menu caller, including the six-way compiler switch table."""
import hashlib,re,struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.op_cfg_layout import OBJECT,SEGMENT,OFFSET,DATA_SEGMENT,verify as containing_layout
from lib.op_option_layout import native_image
from lib.op_music_call import layout as music_layout
START,SIZE,INSTRUCTIONS=0xA0E0,291,278
FUNCTIONS=(('th03-op-decoded-menu-state','main',2008,SIZE,'main_update_and_render()',0),)
EXTERNALS={10:('TEXT_CLEAR',0,0x21F4),14:('@musicroom_menu$qv',SEGMENT,0x1306),
 15:('_resident',DATA_SEGMENT,0x2464),16:('_input_sp',DATA_SEGMENT,0x1AA6),
 36:('@box_submenu_to_main_animate$qv',SEGMENT,0x17DB),38:('@op_fadein_animate$qv',SEGMENT,0x1708),
 40:('@select_cdg_load_part2_of_4$qv',SEGMENT,0x1AC3)}
FIELDS=(
 (2036, 2, 199, 20, 2, 2, 211),
 (2032, 2, 135, 22, 1, 36, 0),
 (2026, 2, 199, 20, 2, 2, 211),
 (2020, 4, 207, 86, None, 10, 0),
 (2014, 2, 199, 20, 2, 2, 212),
 (2297, 2, 197, 20, 1, 1, 2249),
 (2295, 2, 196, 20, 1, 1, 2232),
 (2293, 2, 196, 20, 1, 1, 2227),
 (2291, 2, 196, 20, 1, 1, 2220),
 (2289, 2, 196, 20, 1, 1, 2177),
 (2287, 2, 196, 20, 1, 1, 2172),
 (2280, 2, 196, 20, 2, 3, 0),
 (2273, 2, 196, 22, 2, 16, 0),
 (2268, 2, 196, 20, 2, 2, 210),
 (2261, 2, 196, 22, 2, 16, 1),
 (2256, 2, 196, 20, 2, 2, 210),
 (2251, 2, 196, 20, 2, 2, 212),
 (2244, 2, 196, 20, 2, 2, 209),
 (2239, 2, 196, 20, 2, 3, 2),
 (2234, 2, 196, 20, 2, 2, 212),
 (2221, 4, 204, 22, 1, 14, 0),
 (2215, 2, 196, 20, 2, 2, 211),
 (2210, 2, 196, 20, 2, 3, 0),
 (2205, 2, 196, 20, 2, 2, 212),
 (2201, 2, 132, 22, 1, 40, 0),
 (2195, 2, 132, 22, 1, 38, 0),
 (2179, 2, 196, 22, 2, 15, 0),
 (2170, 2, 196, 20, 1, 1, 2287),
 (2155, 2, 196, 20, 2, 2, 209),
 (2149, 2, 196, 22, 2, 16, 0),
 (2142, 2, 196, 22, 2, 16, 1),
 (2128, 2, 196, 22, 2, 16, 0),
 (2114, 2, 196, 22, 2, 16, 0),
 (2105, 2, 196, 20, 2, 3, 0),
 (2100, 2, 196, 20, 2, 3, 0),
 (2093, 2, 196, 22, 2, 16, 0),
 (2088, 2, 196, 20, 2, 3, 0),
 (2083, 2, 196, 20, 2, 2, 212),
 (2079, 2, 196, 20, 1, 1, 1493),
 (2077, 2, 196, 20, 2, 3, 4),
 (2050, 2, 196, 20, 2, 2, 209),
 (2041, 2, 196, 20, 2, 3, 0),
)
TABLE,DESTINATIONS=0x8F7,(0x884,0x889,0x8B4,0x8BB,0x8C0,0x8D1)
def need(v,m):
    if not v:raise ValueError('OP main menu layout: '+str(m))
def verify(root,work,target,candidate):
    containing_layout(work,target,candidate);music=music_layout(root,work,target,candidate)
    image=native_image((work/OBJECT).read_bytes(),FUNCTIONS,FIELDS,EXTERNALS)[2008:2299]
    need(image==target.program_image[START:START+SIZE]==candidate.program_image[START:START+SIZE],'all 291 resolved native bytes, including switch storage')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=list(decoder.disasm(image[:INSTRUCTIONS],START));ins={i.address:i for i in rows}
    need(sum(i.size for i in rows)==INSTRUCTIONS and rows[-1].mnemonic=='ret' and not rows[-1].op_str,'whole 278-byte near no-argument instruction body')
    need(image[INSTRUCTIONS]==0 and struct.unpack('<6H',image[INSTRUCTIONS+1:])==DESTINATIONS,'zero separator and all six ordered native switch WORDs')
    need(all(SEGMENT*16+off in ins for off in DESTINATIONS),'six complete in-function destination boundaries')
    branches=[]
    for i in rows:
        if i.mnemonic.startswith('j'):
            if i.address==0xA17F:
                need(i.mnemonic=='jmp' and i.op_str=='word ptr cs:[bx + 0x8f7]','one reviewed six-way indirect branch')
            else:
                dest=i.operands[0].imm;need(dest in ins,'direct branches stay in complete instructions');branches.append([i.address,dest])
    text=(work/'obj/th03/op.map').read_text()
    need(len(re.findall(r'(?m)^\s*0990:07E0\s+(?:idle\s+)?main_update_and_render\(\)\s*$',text))==2,'both native caller MAP tables')
    pairs=[[SEGMENT,OFFSET+s+2] for s,w,_,fd,*_ in FIELDS if w==4 and fd==0x56]
    for mz in (target,candidate):
        need([[r.segment,r.offset] for r in mz.relocations if START<=r.linear<START+SIZE]==pairs,'complete ordered MZ vector, excluding real same-CS relaxation')
        need(not any(r.linear<START+SIZE and r.linear+2>START and not START<=r.linear<=START+SIZE-2 for r in mz.relocations),'no straddling MZ fields')
    h=hashlib.sha256(image).hexdigest();owner=dict(unit_id='th03-op-decoded-menu-state',name='main',source='src/op/menu/menu_state.inl',object=OBJECT,segment=SEGMENT,offset=0x7E0,start=START,size=SIZE,coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=h,candidate_sha256=h,ordered_relocations=pairs,argument_bytes=0,callee_pop_bytes=0,instruction_bytes=INSTRUCTIONS,inline_non_instruction_bytes=13,private_data_bytes=0,private_bss_bytes=0,abi='near no-argument main menu; BP/SI/DI preserved; real same-CS far Music Room frame')
    return dict(owners=[owner],functions=1,code_bytes=SIZE,instruction_bytes=INSTRUCTIONS,inline_non_instruction_bytes=13,ordered_native_fields=[list(f) for f in FIELDS],ordered_relocations=pairs,switch_table=TABLE,switch_destinations=list(DESTINATIONS),direct_branches=branches,natural_music_call=music,containing_producer_accepted=False,whole_product_accepted=False)
