"""Complete natural near-Pascal dissolve owner; enclosing DATA stays unowned."""
import hashlib
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes
from lib.decoded_mainl_ending_layout import CS, DS, SOURCE, WRAPPER, OBJECT, verify as enclosing_layout

START,SIZE,NATIVE = 0x2731,211,943
DATA = dict(slots=0x1D0E,enabled=0x27D7,requested=0x27C5,pattern=0xAA2)
BINDINGS = {31:('_mainl_staff_cdg_slots',DS,DATA['slots']),
            32:('_mainl_dissolve_alpha_enabled',DS,DATA['enabled']),
            33:('_mainl_dissolve_alpha_requested',DS,DATA['requested']),
            34:('CDG_PUT_NOALPHA_8',0xC7E,0xF32),35:('CDG_PUT_8',0xC7E,0x1F4)}
FIELDS = ((1006,199,22,2,33,0),(999,199,22,2,32,0),(970,199,22,2,31,4),
          (957,199,22,2,31,2),(1107,196,20,2,2,68),
          (1037,204,86,None,35,0),(1021,204,86,None,34,0))


def need(value,message):
    if not value:
        raise ValueError('MAINL dissolve layout: '+message)


def native_image(raw):
    code,_ = code_bytes(raw,1)
    image,names,fields,report = bytearray(code[NATIVE:NATIVE+SIZE]),[],[],[]
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
            if not NATIVE<=site<NATIVE+SIZE:
                continue
            width = 4 if loc&0xFC==0xCC else 2
            need(site+width<=NATIVE+SIZE,'entire native field inside owner')
            addend = int.from_bytes(code[site:site+width],'little')
            fields.append((site,loc,method,frame,index,addend))
            if method==0x14:
                need((loc&0xFC,frame,index,addend)==(0xC4,2,2,68),'own DATA contribution plus literal pattern addend')
                name,value = '_mainl_dissolve_pattern',0xA5E+addend
            else:
                name,segment,offset = BINDINGS[index]
                need(names[index-1]==name and (addend in (2,4) if index==31 else addend==0),'literal external name and addend')
                if width==4:
                    need((loc&0xFC,method,frame,segment)==(0xCC,0x56,None,0xC7E),'native far blitter field')
                    value = offset|segment<<16
                else:
                    need((loc&0xFC,method,frame,segment)==(0xC4,0x16,2,DS),'WORD DGROUP field')
                    value = offset+addend
            image[site-NATIVE:site-NATIVE+width] = value.to_bytes(width,'little')
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,name=name,addend=addend,width=width))
    need(tuple(fields)==FIELDS,'complete literal ordered native fields')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    enclosing_layout(work,target,candidate,graph,files)
    image,fields = native_image((work/OBJECT).read_bytes())
    start = CS*16+START
    need(image==target.program_image[start:start+SIZE]==candidate.program_image[start:start+SIZE],
         'complete independently linked native dissolve owner')
    ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image,START))
    need(sum(i.size for i in ins)==SIZE and (ins[-1].mnemonic,ins[-1].op_str)==('ret','8'),
         'complete near Pascal pop8 procedure')
    text = (work/'obj/th03/mainl.map').read_text()
    for name,segment,offset in (*BINDINGS.values(),('_mainl_dissolve_pattern',DS,DATA['pattern']),('CDG_PUT_DISSOLVE_E_8',CS,START)):
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+{re.escape(name)}\s*$',text))==2,'both independent MAP publics: '+name)
    expected = [(CS,0x2382+f['offset']+2) for f in fields if f['width']==4]
    for mz in (target,candidate):
        need([(r.segment,r.offset) for r in mz.relocations if start<=r.linear<start+SIZE]==expected,'complete literal ordered MZ vector')
    digest = hashlib.sha256(image).hexdigest()
    owner = dict(unit_id='th03-mainl-decoded-staff-dissolve',name='CDG_PUT_DISSOLVE_E_8',source=SOURCE,object=OBJECT,
        start=start,size=SIZE,segment=CS,offset=START,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=digest,candidate_sha256=digest,ordered_relocations=[list(r) for r in expected],
        argument_bytes=8,callee_pop_bytes=8,private_data_bytes=0,private_bss_bytes=0,
        abi='near Pascal; real caller coordinate/strength WORDs; nested far Pascal blitters; inherited flags')
    return dict(owners=[owner],functions=1,code_bytes=SIZE,ordered_native_fields=fields,mz_relocation_count=2,
        enclosing_CODE_bytes=3695,enclosing_initialized_DATA_bytes=224,enclosing_BSS_bytes=0,enclosing_procedures=19,
        enclosing_DATA_or_other_functions_accepted=False,external_patterns_slots_or_hardware_accepted=False,whole_product_accepted=False)
