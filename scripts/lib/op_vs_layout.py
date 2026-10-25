"""Complete OP VS caller; native title-box code is a separate dependency scope."""
import hashlib
import re

from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.omf import describe_omf,parse_omf
from lib.op_cfg_layout import OBJECT,WRAPPER,SEGMENT,OFFSET,DATA_SEGMENT,DATA_OFFSET,verify as containing_layout
from probe_th03_main_boss_marisa_cpp import code_bytes,code_publics

START,SIZE = SEGMENT*16+0x2DF,365
BOX,BOX_SIZE = SEGMENT*16+0x17AF,44
FIELDS = ((1008,2,199,22,2,15,0),(1000,2,135,22,1,43,0),(991,2,135,22,1,42,0),
 (949,2,199,22,2,15,0),(929,2,199,22,2,15,0),(901,2,199,22,2,15,0),(893,4,207,86,None,13,0),
 (888,2,199,22,2,16,0),(881,2,199,22,2,16,1),(874,2,199,22,2,16,0),(836,2,199,22,2,16,0),
 (798,2,199,22,2,16,0),(788,4,207,86,None,17,0),(753,2,134,22,1,35,0),(748,4,206,86,None,10,0),
 (736,2,198,22,2,15,0),(1080,4,204,86,None,46,0),(1077,2,196,20,2,2,223),
 (1073,2,196,20,2,2,223),(1064,4,204,86,None,12,0),(1059,4,204,86,None,33,0),
 (1051,4,204,86,None,3,0),(1028,2,196,22,2,15,0))
EXTERNALS = {3:('GAIJI_RESTORE',0,0xF1A),10:('TEXT_CLEAR',0,0x21F4),12:('@game_exit$qv',0xBEB,0x112),
 13:('@FRAME_DELAY$QI',0xBEB,0x2EE),15:('_resident',DATA_SEGMENT,0x2464),16:('_input_sp',DATA_SEGMENT,0x1AA6),
 17:('@INPUT_MODE_INTERFACE$QV',0xBEB,0xAD6),33:('SND_KAJA_INTERRUPT',0xBEB,0x553),
 35:('@box_main_to_submenu_animate$qv',SEGMENT,0x17AF),42:('@select_1p_vs_2p_menu$qv',SEGMENT,0x2188),
 43:('@select_vs_cpu_menu$qv',SEGMENT,0x231F),46:('_execl',0,0x9119)}
BOX_FIELDS = ((745,4,206,86,None,1,0),(738,4,206,86,None,8,0))
BOX_EXTERNALS = {1:('@FRAME_DELAY$QI',0xBEB,0x2EE),8:('SUPER_PUT',0,0x28D8)}


def need(v,m):
    if not v:
        raise ValueError('OP VS layout: '+m)


def resolve(raw,start,end,offset,externals):
    code,_ = code_bytes(raw,1)
    image,fields,names = bytearray(code),[],[]
    block = None
    for r in parse_omf(raw):
        if r.name == 'EXTDEF':
            at = 0
            while at < len(r.data):
                size = r.data[at];at += 1
                names.append(r.data[at:at+size].decode());at += size
                need(r.data[at] == 0,'untyped external');at += 1
        elif r.name == 'LEDATA':
            block = (r.data[0],int.from_bytes(r.data[1:3],'little'))
        elif r.name == 'FIXUPP' and block[0] == 1:
            at = 0
            while at < len(r.data):
                loc,lo,fd = r.data[at:at+3];at += 3
                need(fd in (0x14,0x16,0x56),'literal native field form')
                frame = None
                if fd in (0x14,0x16):
                    frame = r.data[at];at += 1
                target = r.data[at];at += 1
                site = block[1]+(loc&3)*256+lo
                width = 4 if loc>>2&15 == 3 else 2
                if not start <= site < end:
                    continue
                need(site+width <= end and loc&0x80,'whole scoped native field')
                addend = int.from_bytes(code[site:site+width],'little')
                fields.append((site,width,loc,fd,frame,target,addend))
                if fd == 0x14:
                    need((width,frame,target) == (2,2,2) and loc&0x40,'actual own DATA WORD')
                    value = DATA_OFFSET+addend
                else:
                    need(target in externals,'scoped symbolic target')
                    _,segment,address = externals[target]
                    if fd == 0x56:
                        need(width == 4 and code[site-1] == 0x9A,'actual far CALL')
                        value = (segment<<16)+address+addend
                    elif loc&0x40:
                        need(width == 2 and frame == 2 and segment == DATA_SEGMENT,'DGROUP external WORD')
                        value = address+addend
                    else:
                        need(width == 2 and frame == 1 and segment == SEGMENT,'same-CODE-group relative near CALL')
                        value = (address+addend-(offset+site+2))&65535
                image[site:site+width] = value.to_bytes(width,'little')
    need(all(names[i-1] == name for i,(name,_,_) in externals.items()),'all scoped external identities')
    return bytes(image[start:end]),fields


def verify(work,target,candidate):
    containing_layout(work,target,candidate)
    raw = (work/OBJECT).read_bytes()
    image,fields = resolve(raw,727,1092,OFFSET,EXTERNALS)
    need(tuple(fields) == FIELDS,'all 23 ordered native WORD/far fields')
    need(image == target.program_image[START:START+SIZE] == candidate.program_image[START:START+SIZE],
         'complete native VS bytes')
    rows = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image,START))
    need(sum(i.size for i in rows) == SIZE and rows[-1].mnemonic == 'ret' and not rows[-1].op_str,
         'whole near no-argument function, no inline storage')
    text = (work/'obj/th03/op.map').read_text()
    need(len(re.findall(r'(?m)^\s*0990:02DF\s+(?:idle\s+)?vs_menu\(\)\s*$',text)) == 2,'both root MAP publics')
    pairs = [[SEGMENT,OFFSET+s+2] for s,w,*_ in FIELDS if w == 4]
    for mz in (target,candidate):
        need([[r.segment,r.offset] for r in mz.relocations if START <= r.linear < START+SIZE] == pairs,
             'all seven ordered MZ relocations')
        need(not any(r.linear < START+SIZE and r.linear+2 > START and not START <= r.linear <= START+SIZE-2 for r in mz.relocations),
             'no straddling relocation')
    # The real title transition executes, but receives no new ownership credit.
    boxraw = (work/'obj/th03/op_main.obj').read_bytes()
    need(describe_omf(boxraw)['valid'] and 'src/op/menu/title_animation.inl' in describe_omf(boxraw)['dependency_paths'],
         'actual maintained title include')
    need(code_publics(boxraw,1) == [(0,'@op_animate$qv'),(550,'@op_fadein_animate$qv'),
        (717,'@box_main_to_submenu_animate$qv'),(761,'@box_submenu_to_main_animate$qv'),(808,'@BOX_COLUMN16_UNPUT$QUI')],
         'complete containing title producer publics')
    box,bfields = resolve(boxraw,717,761,0x14E2,BOX_EXTERNALS)
    need(tuple(bfields) == BOX_FIELDS and box == target.program_image[BOX:BOX+BOX_SIZE]
         == candidate.program_image[BOX:BOX+BOX_SIZE],'native complete 44-byte box dependency')
    bpairs = [[SEGMENT,0x14E2+s+2] for s,w,*_ in BOX_FIELDS]
    for mz in (target,candidate):
        need([[r.segment,r.offset] for r in mz.relocations if BOX <= r.linear < BOX+BOX_SIZE] == bpairs,
             'two ordered box dependency relocations')
    digest = hashlib.sha256(image).hexdigest()
    owner = dict(unit_id='th03-op-decoded-entry-vs-menu',source='src/op/entry.cpp',object=OBJECT,
        name='vs_menu',segment=SEGMENT,offset=0x2DF,start=START,size=SIZE,coordinate_space='decoded-load',
        canonical_file_offset=None,target_sha256=digest,candidate_sha256=digest,ordered_relocations=pairs,
        argument_bytes=0,callee_pop_bytes=0,private_data_bytes=0,private_bss_bytes=0,
        abi='near no-argument entry, AL boolean result; BP/SI/DI preserved; unowned character-selection procedures are bounded interfaces')
    return dict(owners=[owner],functions=1,code_bytes=365,ordered_native_fields=[list(f) for f in FIELDS],
        ordered_relocations=pairs,box_dependency=dict(start=BOX,size=44,source='src/op/menu/title_animation.inl',
        ordered_native_fields=[list(f) for f in BOX_FIELDS],ordered_relocations=bpairs,source_credit_added=False),
        character_selection_procedures_owned=False,containing_producer_accepted=False,whole_product_accepted=False)
