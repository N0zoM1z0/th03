"""Seven complete snow procedures, one bounded existing ownership extent."""
import hashlib
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes
from lib.decoded_mainl_ending_layout import CS, DS, SOURCE, WRAPPER, OBJECT, verify as enclosing_layout

START,SIZE = 0x2561,464
DATA = dict(flakes=0x22C2,cap=0x22C0,frame=0x27C2,page=0x27C4,slow=0x27C5,adapt=0x27C6,
            vsync=0x144E,active=0x880,seed=0x5B6,sin=0x5BA,cos=0x63A)
PROCEDURES = (('clear',0x2561,21,0,'_mainl_clear_blue'),('reset',0x2576,26,0,'flakes_reset()'),
 ('spawn',0x2590,169,0,'_mainl_snow_spawn'),('update',0x2639,70,0,'_mainl_snow_update'),
 ('render',0x267F,54,0,'_mainl_snow_render'),('gate',0x26B5,48,4,'MAINL_SNOW_GATE'),
 ('tick',0x26E5,76,0,'_mainl_snow_tick'))
ENTRIES = {kind:(offset,size,args) for kind,offset,size,args,_ in PROCEDURES}
BINDINGS = {3:('_vsync_Count1',DS,DATA['vsync']),28:('_page_back',DS,DATA['page']),
 33:('_mainl_dissolve_alpha_requested',DS,DATA['slow']),36:('_mainl_spawn_flakes',DS,DATA['flakes']),
 37:('_mainl_snow_frame',DS,DATA['frame']),38:('_mainl_snow_slot_limit',DS,DATA['cap']),
 39:('IRAND',0,0x1A3E),40:('VECTOR2',0xC7E,0x110),41:('_snd_active',DS,DATA['active']),
 45:('_mainl_snow_auto_adjust',DS,DATA['adapt'])}
FIELDS = ((935,199,22,2,28,0),(932,199,22,2,28,0),(925,199,22,2,28,0),
 (917,199,22,2,3,0),(910,199,22,2,3,0),(905,199,22,2,45,0),(900,199,22,2,38,0),
 (895,199,22,2,33,0),(888,199,22,2,3,0),(881,199,22,2,45,0),(850,199,22,2,37,0),
 (830,199,22,2,37,0),(824,199,22,2,41,0),(807,199,22,2,38,0),(771,199,22,2,36,0),
 (754,198,22,2,38,0),(700,198,22,2,36,0),(681,198,22,2,38,0),(672,206,86,None,40,0),
 (642,206,86,None,39,0),(625,206,86,None,39,0),(608,206,86,None,39,0),
 (594,206,86,None,39,0),(568,206,86,None,39,0),(554,198,22,2,37,0),
 (533,198,22,2,36,0),(505,197,22,2,36,0))


def need(value,message):
    if not value:
        raise ValueError('MAINL snow layout: '+message)


def native_image(raw):
    code,_ = code_bytes(raw,1)
    image,names,fields,report = bytearray(code[479:943]),[],[],[]
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
            if not 479<=site<943:
                continue
            width = 4 if loc&0xFC==0xCC else 2
            need(site+width<=943,'entire native field inside bounded owner')
            addend = int.from_bytes(code[site:site+width],'little')
            fields.append((site,loc,method,frame,index,addend))
            name,segment,offset = BINDINGS[index]
            need(names[index-1]==name and addend==0,'literal external identity and zero addend')
            if width==4:
                need((loc&0xFC,method,frame)==(0xCC,0x56,None) and index in (39,40),'actual native far call')
                value = offset|segment<<16
            else:
                need((loc&0xFC,method,frame,segment)==(0xC4,0x16,2,DS),'WORD DGROUP field')
                value = offset
            image[site-479:site-479+width] = value.to_bytes(width,'little')
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,name=name,addend=addend,width=width))
    need(tuple(fields)==FIELDS,'complete literal ordered native field vector')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    enclosing_layout(work,target,candidate,graph,files)
    image,fields = native_image((work/OBJECT).read_bytes())
    start = CS*16+START
    need(image==target.program_image[start:start+SIZE]==candidate.program_image[start:start+SIZE],
         'complete independently linked native snow cluster')
    text = (work/'obj/th03/mainl.map').read_text()
    for name,segment,offset in BINDINGS.values():
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,
             'both independent external MAP publics: '+name)
    procedures = []
    for kind,offset,size,args,symbol in PROCEDURES:
        body = image[offset-START:offset-START+size]
        ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(body,offset))
        need(sum(i.size for i in ins)==size and (ins[-1].mnemonic,ins[-1].op_str)==('ret',str(args) if args else ''),
             'complete near body and exact argument cleanup')
        need(len(re.findall(rf'(?m)^\s*{CS:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,
             'both procedure MAP publics')
        procedures.append(dict(kind=kind,offset=offset,size=size,argument_bytes=args,callee_pop_bytes=args,sha256=hashlib.sha256(body).hexdigest()))
    expected = [(CS,0x2382+f['offset']+2) for f in fields if f['width']==4]
    for mz in (target,candidate):
        need([(r.segment,r.offset) for r in mz.relocations if start<=r.linear<start+SIZE]==expected,
             'complete literal ordered MZ relocation vector')
    digest = hashlib.sha256(image).hexdigest()
    owner = dict(unit_id='th03-mainl-decoded-snow-cluster',name='seven complete snow procedures',source=SOURCE,object=OBJECT,
        start=start,size=SIZE,segment=CS,offset=START,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=digest,candidate_sha256=digest,ordered_relocations=[list(r) for r in expected],
        procedure_count=7,procedures=procedures,private_data_bytes=0,private_bss_bytes=0,
        abi='seven complete near functions; six cdecl/no arguments and gate Pascal pop4; real nested frames')
    return dict(owners=[owner],extents=1,functions=7,code_bytes=SIZE,procedures=procedures,ordered_native_fields=fields,
                mz_relocation_count=len(expected),enclosing_CODE_bytes=3695,enclosing_initialized_DATA_bytes=224,
                enclosing_BSS_bytes=0,enclosing_procedures=19,enclosing_DATA_or_other_functions_accepted=False,
                library_vector_or_tables_accepted=False,physical_runtime_or_assets_accepted=False,whole_product_accepted=False)
