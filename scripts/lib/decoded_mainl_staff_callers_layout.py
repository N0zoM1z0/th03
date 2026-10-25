"""Three complete native staff callers; no enclosing DATA or alignment credit."""
import hashlib
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes
from lib.decoded_mainl_ending_layout import CS, DS, SOURCE, WRAPPER, OBJECT, verify as enclosing_layout

NATIVE,START,SIZE = 1154,0x2804,446
PROCEDURES = (('enter',0x2804,211,2,'MAINL_STAFF_ENTER','staff-entrance'),
              ('leave',0x28D7,183,2,'MAINL_STAFF_LEAVE','staff-leave'),
              ('gallery',0x298E,52,6,'MAINL_STAFF_GALLERY','staff-gallery'))
ENTRIES = {k:(a,n,args) for k,a,n,args,_,_ in PROCEDURES}
DATA = dict(page=0x27C4,frame=0x27C2,requested=0x27C5,adapt=0x27C6,speed=0x27CC,
            duration=0x27CE,limit=0x27D0,secondary=0x27D6,enabled=0x27D7,centers=0x27D8)
BINDINGS = {7:('GRCG_SETCOLOR',0,0xC36),8:('GRCG_OFF',0,0xC60),9:('GRCG_BYTEBOXFILL_X',0,0xB9E),
            28:('_page_back',DS,DATA['page']),29:('_stf_center_y_on_page',DS,DATA['centers']),
            32:('_mainl_dissolve_alpha_enabled',DS,DATA['enabled']),33:('_mainl_dissolve_alpha_requested',DS,DATA['requested']),
            37:('_mainl_snow_frame',DS,DATA['frame']),46:('_mainl_staff_speed',DS,DATA['speed']),
            47:('_mainl_staff_duration',DS,DATA['duration']),48:('_mainl_staff_center_limit',DS,DATA['limit']),
            50:('_mainl_staff_secondary_slot',DS,DATA['secondary'])}
FIELDS = ((1561,198,22,2,37),(1554,198,22,2,37),(1538,206,86,None,8),(1533,206,86,None,9),
 (1516,205,86,None,7),(1504,197,22,2,32),(1495,197,22,2,29),(1485,197,22,2,28),
 (1478,197,22,2,32),(1467,197,22,2,50),(1455,197,22,2,50),(1448,197,22,2,33),
 (1428,197,22,2,37),(1425,197,22,2,29),(1415,197,22,2,28),(1408,197,22,2,29),
 (1398,197,22,2,28),(1388,197,22,2,37),(1378,197,22,2,37),(1356,197,22,2,32),
 (1347,197,22,2,29),(1337,197,22,2,28),(1330,197,22,2,32),(1319,197,22,2,50),
 (1307,197,22,2,50),(1300,197,22,2,33),(1279,197,22,2,37),(1269,196,22,2,47),
 (1266,196,22,2,29),(1260,196,22,2,48),(1252,196,22,2,28),(1247,196,22,2,48),
 (1243,196,22,2,29),(1233,196,22,2,28),(1230,196,22,2,29),(1224,196,22,2,46),
 (1216,196,22,2,28),(1211,196,22,2,48),(1207,196,22,2,29),(1197,196,22,2,28),
 (1190,196,22,2,29),(1180,196,22,2,28),(1170,196,22,2,47),(1166,196,22,2,37))
NEAR_CALLS = ((0x280C,0x2561),(0x282B,0x24E6),(0x28AF,0x2731),(0x28C9,0x2731),
              (0x28DF,0x2561),(0x2905,0x24E6),(0x2943,0x2731),(0x295D,0x2731),(0x29BA,0x2731))


def need(value,message):
    if not value:
        raise ValueError('MAINL staff callers layout: '+message)


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
            need(site+width<=NATIVE+SIZE and not any(code[site:site+width]),'complete zero-addend native field')
            fields.append((site,loc,method,frame,index))
            name,segment,offset = BINDINGS[index]
            need(names[index-1]==name,'literal external name')
            if width==4:
                need((loc&0xFC,method,frame,segment)==(0xCC,0x56,None,0),'literal far root helper')
                value = offset
            else:
                need((loc&0xFC,method,frame,segment)==(0xC4,0x16,2,DS),'WORD DGROUP field')
                value = offset
            image[site-NATIVE:site-NATIVE+width] = value.to_bytes(width,'little')
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,name=name,addend=0,width=width))
    need(tuple(fields)==FIELDS,'complete literal ordered native fields')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    enclosing_layout(work,target,candidate,graph,files)
    image,fields = native_image((work/OBJECT).read_bytes())
    start = CS*16+START
    need(image==target.program_image[start:start+SIZE]==candidate.program_image[start:start+SIZE],'complete independently linked native staff callers')
    text = (work/'obj/th03/mainl.map').read_text()
    for name,segment,offset in BINDINGS.values():
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+{re.escape(name)}\s*$',text))==2,'both independent external MAP publics: '+name)
    owners,calls = [],[]
    for kind,offset,size,args,symbol,unit in PROCEDURES:
        body = image[offset-START:offset-START+size]
        ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(body,offset))
        need(sum(i.size for i in ins)==size and (ins[-1].mnemonic,ins[-1].op_str)==('ret',str(args)),'complete near Pascal body')
        calls.extend((i.address,int(i.op_str,16)) for i in ins if i.mnemonic=='call')
        need(len(re.findall(rf'(?m)^\s*{CS:04X}:{offset:04X}\s+{symbol}\s*$',text))==2,'both owner MAP publics')
        expected = [(CS,0x2382+f['offset']+2) for f in fields if f['width']==4 and offset<=0x2382+f['offset']<offset+size]
        for mz in (target,candidate):
            need([(r.segment,r.offset) for r in mz.relocations if CS*16+offset<=r.linear<CS*16+offset+size]==expected,'complete literal ordered MZ vector')
        digest = hashlib.sha256(body).hexdigest()
        owners.append(dict(unit_id='th03-mainl-decoded-'+unit,name=symbol,source=SOURCE,object=OBJECT,
            start=CS*16+offset,size=size,segment=CS,offset=offset,coordinate_space='decoded-load',canonical_file_offset=None,
            target_sha256=digest,candidate_sha256=digest,ordered_relocations=[list(r) for r in expected],
            argument_bytes=args,callee_pop_bytes=args,private_data_bytes=0,private_bss_bytes=0,
            abi='near Pascal; live signed WORD state and unchecked BYTE page; real nested frames; native divide faults retained'))
        if kind=='leave':
            owners[-1]['proved_unreachable_ranges'] = [dict(offset=0x2925,size=3,
                reason='signed frame<160 implies trunc(frame/20)<=7; readonly frame until this comparison')]
    need(tuple(calls)==NEAR_CALLS,'all nine native internal near calls target actual owned helpers')
    return dict(owners=owners,functions=3,code_bytes=446,ordered_native_fields=fields,mz_relocation_count=3,
        internal_near_calls=[list(c) for c in calls],enclosing_CODE_bytes=3695,enclosing_initialized_DATA_bytes=224,
        enclosing_BSS_bytes=0,enclosing_procedures=19,enclosing_DATA_or_other_functions_accepted=False,
        bytebox_library_or_physical_graphics_accepted=False,whole_product_accepted=False)
