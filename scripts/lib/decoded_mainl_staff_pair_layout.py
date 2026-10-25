"""Complete natural near-Pascal two-stage staff pair controller."""
import hashlib
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes
from lib.decoded_mainl_ending_layout import CS, DS, SOURCE, WRAPPER, OBJECT, verify as enclosing_layout

START,SIZE,NATIVE = 0x2AA7,358,1829
DATA = dict(frame=0x27C2,page=0x27C4,speed=0x27CC,secondary_y=0x27D2,height_offset=0x27D4,centers=0x27D8,enabled=0x27D7)
BINDINGS = {7:('GRCG_SETCOLOR',0,0xC36),8:('GRCG_OFF',0,0xC60),9:('GRCG_BYTEBOXFILL_X',0,0xB9E),
            28:('_page_back',DS,DATA['page']),29:('_stf_center_y_on_page',DS,DATA['centers']),
            37:('_mainl_snow_frame',DS,DATA['frame']),46:('_mainl_staff_speed',DS,DATA['speed']),
            49:('_mainl_staff_height_offset',DS,DATA['height_offset']),
            32:('_mainl_dissolve_alpha_enabled',DS,DATA['enabled']),51:('_mainl_staff_secondary_y',DS,DATA['secondary_y'])}
FIELDS = ((2037, 199, 22, 2, 51, 0),
 (2026, 199, 22, 2, 37, 0),
 (2021, 199, 22, 2, 32, 0),
 (2017, 199, 22, 2, 51, 0),
 (2010, 199, 22, 2, 28, 0),
 (1989, 199, 22, 2, 37, 0),
 (1982, 199, 22, 2, 37, 0),
 (1967, 199, 22, 2, 51, 0),
 (1956, 199, 22, 2, 37, 0),
 (1950, 199, 22, 2, 37, 0),
 (1933, 199, 22, 2, 37, 0),
 (1925, 199, 22, 2, 32, 0),
 (1912, 199, 22, 2, 51, 0),
 (1904, 199, 22, 2, 32, 0),
 (1894, 199, 22, 2, 37, 0),
 (1890, 199, 22, 2, 29, 2),
 (1887, 199, 22, 2, 29, 0),
 (1884, 199, 22, 2, 49, 0),
 (1873, 199, 22, 2, 29, 0),
 (1860, 199, 22, 2, 28, 0),
 (1855, 199, 22, 2, 29, 0),
 (1845, 199, 22, 2, 28, 0),
 (1839, 199, 22, 2, 46, 0),
 (2174, 204, 86, None, 8, 0),
 (2169, 204, 86, None, 9, 0),
 (2152, 204, 86, None, 7, 0),
 (2138, 204, 86, None, 8, 0),
 (2133, 204, 86, None, 9, 0),
 (2116, 204, 86, None, 7, 0),
 (2092, 196, 22, 2, 37, 0),
 (2084, 196, 22, 2, 32, 0),
 (2078, 204, 86, None, 8, 0),
 (2073, 204, 86, None, 9, 0),
 (2056, 204, 86, None, 7, 0))
NEAR_CALLS = ((10989, 10244), (11010, 10033), (11018, 9957), (11031, 9909), (11063, 9446), (11067, 10455), (11134, 10033), (11177, 9957), (11190, 9909), (11232, 9957), (11268, 9957))


def need(value,message):
    if not value:
        raise ValueError('MAINL staff pair layout: '+message)


def native_image(raw):
    code,_ = code_bytes(raw,1)
    image,names,fields,report = bytearray(code[NATIVE:NATIVE+SIZE]),[],[],[]
    block = None
    for rec in parse_omf(raw):
        if rec.name=='EXTDEF':
            at = 0
            while at<len(rec.data):
                n = rec.data[at]
                names.append(rec.data[at+1:at+n+1].decode())
                at += n+2
        if rec.name=='LEDATA':
            block = rec.data[0],int.from_bytes(rec.data[1:3],'little')
        if rec.name!='FIXUPP' or block[0]!=1:
            continue
        at = 0
        while at<len(rec.data):
            loc,low,method = rec.data[at:at+3]
            at += 3
            frame = rec.data[at] if method in (0x14,0x16) else None
            at += int(frame is not None)
            index = rec.data[at]
            at += 1
            site = block[1]+(loc&3)*256+low
            if not NATIVE<=site<NATIVE+SIZE:
                continue
            width = 4 if loc&0xFC==0xCC else 2
            need(site+width<=NATIVE+SIZE,'complete native field')
            addend = int.from_bytes(code[site:site+width],'little')
            fields.append((site,loc,method,frame,index,addend))
            name,segment,offset = BINDINGS[index]
            need(names[index-1]==name,'literal external identity')
            if width==4:
                need((loc&0xFC,method,frame,segment,addend)==(0xCC,0x56,None,0,0),'literal far root helper')
            else:
                need((loc&0xFC,method,frame,segment)==(0xC4,0x16,2,DS),'WORD DGROUP field')
            image[site-NATIVE:site-NATIVE+width] = (offset+addend).to_bytes(width,'little')
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,name=name,addend=addend,width=width))
    need(tuple(fields)==FIELDS,'complete literal ordered native fields')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    enclosing_layout(work,target,candidate,graph,files)
    image,fields = native_image((work/OBJECT).read_bytes())
    start = CS*16+START
    need(image==target.program_image[start:start+SIZE]==candidate.program_image[start:start+SIZE],'complete independently linked native staff pair')
    ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image,START))
    need(sum(i.size for i in ins)==SIZE and (ins[-1].mnemonic,ins[-1].op_str)==('ret','6'),'complete near Pascal pop6 body')
    calls = [(i.address,int(i.op_str,16)) for i in ins if i.mnemonic=='call']
    need(tuple(calls)==NEAR_CALLS,'all eleven native internal calls target actual owned helpers')
    text = (work/'obj/th03/mainl.map').read_text()
    for name,segment,offset in (*BINDINGS.values(),('MAINL_STAFF_PAIR',CS,START)):
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+{re.escape(name)}\s*$',text))==2,'both independent MAP publics: '+name)
    expected = [(CS,0x2382+f['offset']+2) for f in fields if f['width']==4]
    for mz in (target,candidate):
        need([(r.segment,r.offset) for r in mz.relocations if start<=r.linear<start+SIZE]==expected,'complete literal ordered MZ vector')
    digest = hashlib.sha256(image).hexdigest()
    owner = dict(unit_id='th03-mainl-decoded-staff-double',name='MAINL_STAFF_PAIR',source=SOURCE,object=OBJECT,
        start=start,size=SIZE,segment=CS,offset=START,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=digest,candidate_sha256=digest,ordered_relocations=[list(r) for r in expected],argument_bytes=6,callee_pop_bytes=6,
        private_data_bytes=0,private_bss_bytes=0,abi='near Pascal; slot/enter/leave WORD arguments; real nested stateful calls and conditional polling prefixes')
    return dict(owners=[owner],functions=1,code_bytes=SIZE,ordered_native_fields=fields,mz_relocation_count=9,
        internal_near_calls=[list(c) for c in calls],enclosing_CODE_bytes=3695,enclosing_initialized_DATA_bytes=224,
        enclosing_BSS_bytes=0,enclosing_procedures=19,enclosing_DATA_or_other_functions_accepted=False,
        bytebox_library_accepted=False,physical_IRQ_driver_assets_or_vector_library_accepted=False,whole_product_accepted=False)
