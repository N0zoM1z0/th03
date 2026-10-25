"""Complete natural near-Pascal two-stage staff hold controller."""
import hashlib
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes
from lib.decoded_mainl_ending_layout import CS, DS, SOURCE, WRAPPER, OBJECT, verify as enclosing_layout

START,SIZE,NATIVE = 0x2C0D,139,2187
DATA = dict(frame=0x27C2,page=0x27C4,speed=0x27CC,secondary_y=0x27D2,height_offset=0x27D4,centers=0x27D8)
BINDINGS = {28:('_page_back',DS,DATA['page']),29:('_stf_center_y_on_page',DS,DATA['centers']),
            37:('_mainl_snow_frame',DS,DATA['frame']),46:('_mainl_staff_speed',DS,DATA['speed']),
            49:('_mainl_staff_height_offset',DS,DATA['height_offset']),51:('_mainl_staff_secondary_y',DS,DATA['secondary_y'])}
FIELDS = ((2320,197,22,2,51,0),(2317,197,22,2,29,0),(2307,197,22,2,28,0),
          (2291,196,22,2,37,0),(2279,196,22,2,37,0),(2262,196,22,2,37,0),
          (2247,196,22,2,37,0),(2243,196,22,2,29,2),(2240,196,22,2,29,0),
          (2237,196,22,2,49,0),(2226,196,22,2,29,0),(2213,196,22,2,28,0),
          (2208,196,22,2,29,0),(2198,196,22,2,28,0),(2192,196,22,2,46,0))
NEAR_CALLS = ((0x2C50,0x2804),(0x2C53,0x26E5),(0x2C60,0x26B5),
              (0x2C6D,0x2561),(0x2C70,0x26E5),(0x2C7D,0x26B5))


def need(value,message):
    if not value:
        raise ValueError('MAINL staff hold layout: '+message)


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
            need((loc&0xFC,method,frame)==(0xC4,0x16,2) and site+2<=NATIVE+SIZE,'literal WORD DGROUP field')
            addend = int.from_bytes(code[site:site+2],'little')
            fields.append((site,loc,method,frame,index,addend))
            name,segment,offset = BINDINGS[index]
            need(names[index-1]==name and segment==DS,'literal external identity')
            image[site-NATIVE:site-NATIVE+2] = (offset+addend).to_bytes(2,'little')
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,name=name,addend=addend,width=2))
    need(tuple(fields)==FIELDS,'complete literal ordered native fields')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    enclosing_layout(work,target,candidate,graph,files)
    image,fields = native_image((work/OBJECT).read_bytes())
    start = CS*16+START
    need(image==target.program_image[start:start+SIZE]==candidate.program_image[start:start+SIZE],'complete independently linked native staff hold')
    ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image,START))
    need(sum(i.size for i in ins)==SIZE and (ins[-1].mnemonic,ins[-1].op_str)==('ret','6'),'complete near Pascal pop6 body')
    calls = [(i.address,int(i.op_str,16)) for i in ins if i.mnemonic=='call']
    need(tuple(calls)==NEAR_CALLS,'all six native internal calls target actual owned helpers')
    text = (work/'obj/th03/mainl.map').read_text()
    for name,segment,offset in (*BINDINGS.values(),('MAINL_STAFF_HOLD',CS,START)):
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+{re.escape(name)}\s*$',text))==2,'both independent MAP publics: '+name)
    for mz in (target,candidate):
        need(not any(start<=r.linear<start+SIZE for r in mz.relocations),'complete empty ordered MZ vector')
    digest = hashlib.sha256(image).hexdigest()
    owner = dict(unit_id='th03-mainl-decoded-staff-hold',name='MAINL_STAFF_HOLD',source=SOURCE,object=OBJECT,
        start=start,size=SIZE,segment=CS,offset=START,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=digest,candidate_sha256=digest,ordered_relocations=[],argument_bytes=6,callee_pop_bytes=6,
        private_data_bytes=0,private_bss_bytes=0,abi='near Pascal; slot/enter/hold WORD arguments; real nested stateful calls and conditional polling prefixes')
    return dict(owners=[owner],functions=1,code_bytes=SIZE,ordered_native_fields=fields,mz_relocation_count=0,
        internal_near_calls=[list(c) for c in calls],enclosing_CODE_bytes=3695,enclosing_initialized_DATA_bytes=224,
        enclosing_BSS_bytes=0,enclosing_procedures=19,enclosing_DATA_or_other_functions_accepted=False,
        physical_IRQ_driver_assets_or_vector_library_accepted=False,whole_product_accepted=False)
