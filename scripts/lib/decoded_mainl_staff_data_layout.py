"""Natural 224-byte STAFF initializer; pointees and CODE retain separate owners."""
import hashlib
import re
import struct
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics
from lib.decoded_mainl_ending_layout import CS, DS, SOURCE, WRAPPER, OBJECT, verify as enclosing_layout

START, SIZE = 0xA5E, 224
PUBLICS = ((0,'_mainl_ending_script'),(4,'_sFLAKE'),(68,'_mainl_dissolve_pattern'),
           (132,'_mainl_verdict_playchars'),(168,'_mainl_verdict_ranks'),(184,'_mainl_verdict_numbers'))
NAME_OFFSETS = (0xB55,0xB63,0xB6E,0xB7E,0xB89,0xB94,0xBA5,0xBB4,0xBC4)
RANK_OFFSETS = (0xBD2,0xBDE,0xBEC,0xBF8)
DIGIT_OFFSETS = tuple(0xC07+3*i for i in range(10))
POINTERS = ((0,75,'_mainl_ending_template',0xB3E),) + tuple(
    (base+i*4,index+i,prefix+str(i),offset) for base,index,prefix,offsets in (
        (132,76,'_mainl_vname_',NAME_OFFSETS),(168,85,'_mainl_vrank_',RANK_OFFSETS),
        (184,89,'_mainl_vdigit_',DIGIT_OFFSETS)) for i,offset in enumerate(offsets))
# TC4 emits this single DATA record's fields backwards, including the script last.
FIELDS = tuple((site,0xCC,0x16,2,index,0) for site,index,_,_ in reversed(POINTERS))
SPRITE_ROWS = ('..####.. .######. ######## ######## ######## ######## .######. ..####..',
               '........ ...##... ..####.. .######. .######. ..####.. ...##... ........',
               '........ ........ ...##... ..####.. ..####.. ...##... ........ ........',
               '........ ........ ........ ...##... ...##... ........ ........ ........')
MASK_ROWS = ('FFFF FFFF FFFF FFFF','2222 5555 8888 5555','AAAA 5555 AAAA 5555',
             'EEEE 5555 BBBB 5555','EEEE 7777 BBBB DDDD','FFFF 5555 FFFF 5555',
             'FFFF EEEE FFFF BBBB','FFFF 7777 FFFF FFFF')


def need(value,message):
    if not value:
        raise ValueError('MAINL staff DATA layout: '+str(message))


def sprite_words():
    return tuple(int(row.replace('.','0').replace('#','1'),2) for cel in SPRITE_ROWS for row in cel.split())


def mask_words():
    return tuple(int(word,16) for row in MASK_ROWS for word in row.split())


def semantic_image(load=0):
    data=bytearray(SIZE)
    struct.pack_into('<32H',data,4,*sprite_words())
    struct.pack_into('<32H',data,68,*mask_words())
    for site,_,_,offset in POINTERS:
        struct.pack_into('<HH',data,site,offset,DS+load)
    return bytes(data)


def native_image(raw):
    data,blocks=code_bytes(raw,2)
    need(len(data)==SIZE and [(b['offset'],b['size']) for b in blocks]==[(0,SIZE)],'one complete DATA LEDATA without holes')
    need(tuple(code_publics(raw,2))==PUBLICS,'all six natural DATA public boundaries')
    expected=bytearray(semantic_image())
    for site,_,_,_ in POINTERS:
        expected[site:site+4]=bytes(4)
    need(data==bytes(expected),'complete unlinked semantic initializer, including zero pointer addends')
    names=[]
    fields=[]
    report=[]
    block=None
    resolved=bytearray(data)
    bindings={index:(site,name,offset) for site,index,name,offset in POINTERS}
    for rec in parse_omf(raw):
        if rec.name=='EXTDEF':
            at=0
            while at<len(rec.data):
                n=rec.data[at]
                names.append(rec.data[at+1:at+n+1].decode())
                at+=n+2
        if rec.name=='LEDATA':
            block=rec.data[0],int.from_bytes(rec.data[1:3],'little')
        if rec.name!='FIXUPP' or block[0]!=2:
            continue
        at=0
        while at<len(rec.data):
            need(at+5<=len(rec.data),'complete five-byte DATA FIXUPP field')
            loc,low,method,frame,index=rec.data[at:at+5]
            at+=5
            site=block[1]+(loc&3)*256+low
            addend=int.from_bytes(data[site:site+4],'little')
            fields.append((site,loc,method,frame,index,addend))
            need(index in bindings,'external DATA pointer identity')
            expected_site,name,offset=bindings[index]
            need((loc,method,frame,site,addend)==(0xCC,0x16,2,expected_site,0) and names[index-1]==name,
                 'literal far DATA pointer / DGROUP frame / external identity / zero addend')
            struct.pack_into('<HH',resolved,site,offset,DS)
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,name=name,addend=addend,width=4))
    need(tuple(fields)==FIELDS,'complete literal ordered DATA native fixups')
    need(bytes(resolved)==semantic_image(),'every linked initializer has independently specified semantic value')
    return bytes(resolved),report


def verify(work,target,candidate,graph,files):
    enclosing_layout(work,target,candidate,graph,files)
    data,fields=native_image((work/OBJECT).read_bytes())
    start=DS*16+START
    need(data==target.program_image[start:start+SIZE]==candidate.program_image[start:start+SIZE],
         'complete independently linked raw DATA extent')
    text=(work/'obj/th03/mainl.map').read_text()
    for name,offset in [(name,START+off) for off,name in PUBLICS]+[(name,offset) for _,_,name,offset in POINTERS]:
        need(len(re.findall(rf'(?m)^\s*{DS:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,
             'both MAP public tables: '+name)
    relocations=[(DS,START+site+2) for site,_,_,_,_,_ in FIELDS]
    for mz in (target,candidate):
        need([(r.segment,r.offset) for r in mz.relocations if start<=r.linear<start+SIZE]==relocations,
             'complete literal ordered MZ DATA relocation vector')
        for load in (0x1000,0x3000):
            raw=mz.relocated_program_image(load)
            need(raw[start:start+SIZE]==semantic_image(load),'all offset and relocated segment WORDs at both loads')
    digest=hashlib.sha256(data).hexdigest()
    owner=dict(unit_id='th03-mainl-decoded-staff-data',name='STAFF initialized DATA',source=SOURCE,object=OBJECT,
        start=start,size=SIZE,segment=DS,offset=START,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=digest,candidate_sha256=digest,ordered_relocations=[list(r) for r in relocations],
        procedure_count=0,procedures=[],code_bytes=0,initialized_data_bytes=SIZE,private_data_bytes=SIZE,private_bss_bytes=0,
        abi='WORD-aligned DGROUP DATA; mutable far script pointer, 4x8 WORD sprite, 8x4 WORD masks and 9/4/10 far pointers')
    return dict(owners=[owner],functions=0,code_bytes=0,initialized_data_bytes=SIZE,bss_bytes=0,
        ordered_native_fields=fields,mz_relocation_count=24,publics=[dict(offset=o,name=n) for o,n in PUBLICS],
        pointer_bytes=96,sprite_bytes=64,mask_bytes=64,initialized_holes=0,
        enclosing_CODE_or_pointees_accepted=False,whole_product_accepted=False)
