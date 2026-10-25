"""Complete ending entry in the natural STAFFP_TEXT TC4 producer.

The enclosing TU has 18 other procedures and 224 initialized DATA bytes. Their
inventory/layout is checked here; this scope owns only the complete ending body.
"""
import hashlib
import re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

CS, DS, START, SIZE = 0x95F,0xE3F,0x2382,280
SOURCE, WRAPPER, OBJECT = 'src/mainl/staff/data.cpp','staffdat.cpp','obj/th03/staffdat.obj'
DATA = dict(script=0xA5E,resident=0x21EA,tone=0x578,headers=0x1F26,buffers=0x1F0E,bonus=0xB48,op=0xB52)
# Native external identity, linked segment and offset; never obtained from the
# comparison image. Every symbol is independently checked in both MAP sections.
BINDINGS = {1:('_execl',0,0x8E37),4:('GAIJI_RESTORE',0,0xC96),5:('GRAPH_CLEAR',0,0xE72),
 6:('GRAPH_SHOW',0,0x1758),10:('PALETTE_SHOW',0,0x17D0),11:('_PaletteTone',DS,DATA['tone']),
 14:('GRAPH_PI_FREE',0,0xFEC),15:('TEXT_CLEAR',0,0x1F20),16:('_resident',DS,DATA['resident']),
 17:('CDG_FREE',0xC7E,0x950),18:('_pi_headers',DS,DATA['headers']),19:('_pi_buffers',DS,DATA['buffers']),
 20:('@FRAME_DELAY$QI',0xC7E,0x372),21:('@game_exit$qv',0xC7E,0x1B0),
 22:('@CUTSCENE_SCRIPT_LOAD$QNXC',CS,0xB3E),23:('@cutscene_script_free$qv',CS,0xB84),
 24:('@cutscene_animate$qv',CS,0x167E),25:('@regist_menu$qv',CS,0x21E2),
 26:('_mainl_bonus_script',DS,DATA['bonus']),27:('_mainl_op_name',DS,DATA['op'])}
MAP_NAMES = {20:'frame_delay(int)',21:'game_exit()',22:'cutscene_script_load(const char far*)',
             23:'cutscene_script_free()',24:'cutscene_animate()',25:'regist_menu()'}
FIELDS = ((271,205,86,None,1,0),(268,197,22,2,27,0),(264,197,22,2,27,0),
 (255,204,86,None,21,0),(250,204,86,None,4,0),(245,204,86,None,15,0),
 (242,132,22,1,23,0),(239,132,22,1,24,0),(236,132,22,1,22,0),(233,196,22,2,26,0),
 (221,204,86,None,5,0),(210,204,86,None,5,0),(187,196,22,2,16,0),(183,132,22,1,25,0),
 (175,196,22,2,16,0),(168,132,22,1,23,0),(165,132,22,1,24,0),(162,132,22,1,22,0),
 (159,196,20,2,2,0),(152,204,86,None,6,0),(147,204,86,None,5,0),(132,204,86,None,20,0),
 (125,204,86,None,10,0),(120,196,22,2,11,0),(109,196,20,2,2,0),(88,196,20,2,2,0),
 (66,196,20,2,2,0),(41,196,22,2,16,0),(35,204,86,None,14,0),(32,196,22,2,19,0),
 (27,196,22,2,18,0),(21,204,86,None,17,0),(14,204,86,None,17,0),(7,204,86,None,17,0))
PUBLICS = ((0,'_mainl_ending'),(280,'@FLAKE_PUT$QIII'),(356,'CDG_UNPUT_FOR_UPWARDS_MOTION_E_8'),
 (479,'_mainl_clear_blue'),(500,'@flakes_reset$qv'),(526,'_mainl_snow_spawn'),(695,'_mainl_snow_update'),
 (765,'_mainl_snow_render'),(819,'MAINL_SNOW_GATE'),(867,'_mainl_snow_tick'),(943,'CDG_PUT_DISSOLVE_E_8'),
 (1154,'MAINL_STAFF_ENTER'),(1365,'MAINL_STAFF_LEAVE'),(1548,'MAINL_STAFF_GALLERY'),
 (1600,'MAINL_STAFF_SINGLE'),(1829,'MAINL_STAFF_PAIR'),(2187,'MAINL_STAFF_HOLD'),
 (2326,'_mainl_staff_verdict'),(2715,'_mainl_staff_roll'))


def need(value,message):
    if not value:
        raise ValueError('MAINL ending layout: '+message)


def native_image(raw):
    code,_ = code_bytes(raw,1)
    image,names,fields,report = bytearray(code[:SIZE]),[],[],[]
    block = None
    for r in parse_omf(raw):
        if r.name=='EXTDEF':
            at = 0
            while at<len(r.data):
                n = r.data[at]
                names.append(r.data[at+1:at+n+1].decode())
                at += n+2
        if r.name=='LEDATA':
            block = r.data[0],int.from_bytes(r.data[1:3],'little')
        if r.name!='FIXUPP' or block[0]!=1:
            continue
        at = 0
        while at<len(r.data):
            loc,low,method = r.data[at:at+3]
            at += 3
            frame = r.data[at] if method in (0x14,0x16) else None
            at += int(frame is not None)
            index = r.data[at]
            at += 1
            site = block[1]+(loc&3)*256+low
            if site>=SIZE:
                continue
            width = 4 if loc&0xFC==0xCC else 2
            need(site+width<=SIZE,'complete native field within owner')
            addend = int.from_bytes(code[site:site+width],'little')
            fields.append((site,loc,method,frame,index,addend))
            need(addend==0,'no hidden owner addend')
            if method==0x14:
                need((loc&0xFC,frame,index)==(0xC4,2,2),'own initialized DATA reference through DGROUP')
                name,value = '_mainl_ending_script',DATA['script']
            else:
                name,segment,offset = BINDINGS[index]
                need(names[index-1]==name,'literal native external identity')
                if method==0x56:
                    need(loc&0xFC==0xCC,'literal far pointer width')
                    value = offset|(segment<<16)
                elif loc&0xFC==0x84:
                    need((method,frame,segment)==(0x16,1,CS),'same GROUP_01 near reference')
                    value = (offset-(START+site+2))&65535
                else:
                    need((loc&0xFC,method,frame,segment)==(0xC4,0x16,2,DS),'WORD DGROUP external')
                    value = offset
            image[site:site+width] = value.to_bytes(width,'little')
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,name=name,addend=addend,width=width))
    need(len(names)==98 and hashlib.sha256('\0'.join(names).encode()).hexdigest()==
         'f4eb99f0175d8e79a58d74112fdfd15ebd4cd64bf1ca36f8a95ec31cdc54604c','whole producer external inventory')
    need(tuple(fields)==FIELDS,'complete literal ordered owner fields')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    root = Path(__file__).resolve().parents[2]
    raw = (work/OBJECT).read_bytes()
    d = describe_omf(raw)
    need(d['valid'] and d['translator_comments']==['TC86 Borland C++ 4.02'],'native TC4 identity')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(raw)]==
         [('STAFFP_TEXT','CODE',3695),('_DATA','DATA',224),('_BSS','BSS',0)]
         and [r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF']==[0x28,0x48,0x48],
         'natural BYTE CODE / WORD DATA producer inventory')
    need([b['size'] for b in code_bytes(raw,1)[1]]==[1021,1024,1022,628]
         and tuple(code_publics(raw,1))==PUBLICS,'all native records and nineteen procedure boundaries')
    row, = [r for r in graph if r['output']==OBJECT]
    need((row['source'],row['wrapper'],row['game'],row['binary'],row['first_binary'])==(SOURCE,WRAPPER,3,'L','mainl'),
         'actual maintained GAME3/L staff producer')
    need(WRAPPER in d['dependency_paths']
         and files[WRAPPER]==(work/WRAPPER).read_bytes() and files[WRAPPER].replace(b'\r\n',b'\n')==
         (root/SOURCE).read_bytes().replace(b'\r\n',b'\n'),'current source consumption and transport')
    text = (work/'obj/th03/mainl.map').read_text()
    for segment,offset,size,cls,seg,group in ((CS,START,3695,'CODE','STAFFP_TEXT','GROUP_01'),
        (DS,DATA['script'],224,'DATA','_DATA','DGROUP'),(DS,0x27EA,0,'BSS','_BSS','DGROUP')):
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+{size:04X}\s+C={cls}\s+S={seg}\s+G={group}\s+M=staffdat.cpp\s+ACBP={(0x28 if cls=="CODE" else 0x48):02X}\s*$',text))==1,
             'literal enclosing producer MAP allocation')
    for index,(name,segment,offset) in BINDINGS.items():
        symbol = MAP_NAMES.get(index,name)
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,'both external MAP publics: '+symbol)
    for symbol,segment,offset in (('_mainl_ending',CS,START),('_mainl_ending_script',DS,DATA['script']),('_mainl_staff_roll',CS,0x2E1D)):
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{symbol}\s*$',text))==2,'both own MAP publics')
    image,fields = native_image(raw)
    start = CS*16+START
    need(image==target.program_image[start:start+SIZE]==candidate.program_image[start:start+SIZE],
         'complete independently linked native ending bytes')
    instructions = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image,START))
    need(sum(i.size for i in instructions)==SIZE and (instructions[0].mnemonic,instructions[0].op_str)==('enter','2, 0')
         and (instructions[-1].mnemonic,instructions[-1].op_str)==('ret',''),'complete compiler-owned near cdecl procedure')
    expected = [(CS,START+f['offset']+2) for f in fields if f['width']==4]
    for mz in (target,candidate):
        need([(r.segment,r.offset) for r in mz.relocations if start<=r.linear<start+SIZE]==expected,
             'complete literal ordered MZ vector')
    digest = hashlib.sha256(image).hexdigest()
    owner = dict(unit_id='th03-mainl-decoded-staff-ending',name='_mainl_ending',source=SOURCE,object=OBJECT,
        start=start,size=SIZE,segment=CS,offset=START,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=digest,candidate_sha256=digest,ordered_relocations=[list(r) for r in expected],
        argument_bytes=0,callee_pop_bytes=0,private_data_bytes=0,private_bss_bytes=0,
        abi='near cdecl; compiler ENTER 2 / LEAVE / RET; signed BYTE character quotient; far mutable script pointer')
    return dict(owners=[owner],functions=1,code_bytes=SIZE,ordered_native_fields=fields,mz_relocation_count=len(expected),
                near_external_fields=7,own_DATA_fields=4,enclosing_CODE_bytes=3695,enclosing_initialized_DATA_bytes=224,
                enclosing_BSS_bytes=0,enclosing_procedures=19,enclosing_DATA_or_other_functions_accepted=False,
                physical_runtime_or_assets_accepted=False,whole_product_accepted=False)
