"""Whole flake/unput procedures in the natural nineteen-procedure staff TU."""
import hashlib
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes
from lib.decoded_mainl_ending_layout import CS, DS, SOURCE, WRAPPER, OBJECT, verify as enclosing_layout

SPRITE,SLOTS = 0xA62,0x1D0E
ENTRIES = {'flake':(0x249A,76),'unput':(0x24E6,123)}
FIELDS = ((383,197,22,2,31,4),(370,197,22,2,31,2),(317,197,20,2,2,4))


def need(value,message):
    if not value:
        raise ValueError('MAINL staff draw layout: '+message)


def native_image(raw):
    code,_ = code_bytes(raw,1)
    image,names,fields,report = bytearray(code[280:479]),[],[],[]
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
            if not 280<=site<479:
                continue
            need((loc&0xFC,frame)==(0xC4,2) and site+2<=479,'literal DGROUP WORD field')
            addend = int.from_bytes(code[site:site+2],'little')
            fields.append((site,loc,method,frame,index,addend))
            if method==0x14:
                need((index,addend)==(2,4),'actual own DATA sprite addend')
                name,value = '_sFLAKE',SPRITE
            else:
                need(method==0x16 and index==31 and names[index-1]=='_mainl_staff_cdg_slots'
                     and addend in (2,4),'actual external slot field identity and member addend')
                name,value = names[index-1],SLOTS+addend
            image[site-280:site-278] = value.to_bytes(2,'little')
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,name=name,addend=addend,width=2))
    need(tuple(fields)==FIELDS,'complete literal ordered fields')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    enclosing = enclosing_layout(work,target,candidate,graph,files)
    raw = (work/OBJECT).read_bytes()
    image,fields = native_image(raw)
    first = CS*16+ENTRIES['flake'][0]
    need(image==target.program_image[first:first+199]==candidate.program_image[first:first+199],
         'complete independently linked native drawing bodies')
    text = (work/'obj/th03/mainl.map').read_text()
    for symbol,segment,offset in (('flake_put(int,int,int)',CS,0x249A),('CDG_UNPUT_FOR_UPWARDS_MOTION_E_8',CS,0x24E6),
                                  ('_sFLAKE',DS,SPRITE),('_mainl_staff_cdg_slots',DS,SLOTS)):
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,
             'both owner/external MAP publics: '+symbol)
    owners = []
    for kind,(offset,size) in ENTRIES.items():
        start = CS*16+offset
        body = image[start-first:start-first+size]
        ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(body,offset))
        need(sum(i.size for i in ins)==size and (ins[-1].mnemonic,ins[-1].op_str)==('ret','6'),
             'complete near Pascal procedure and callee argument cleanup')
        for mz in (target,candidate):
            need(not [(r.segment,r.offset) for r in mz.relocations if start<=r.linear<start+size],
                 'complete empty ordered MZ field vector')
        digest = hashlib.sha256(body).hexdigest()
        owners.append(dict(unit_id='th03-mainl-decoded-staff-'+kind,name='flake_put' if kind=='flake' else 'CDG_UNPUT_FOR_UPWARDS_MOTION_E_8',
            source=SOURCE,object=OBJECT,start=start,size=size,segment=CS,offset=offset,coordinate_space='decoded-load',
            canonical_file_offset=None,target_sha256=digest,candidate_sha256=digest,ordered_relocations=[],
            argument_bytes=6,callee_pop_bytes=6,private_data_bytes=0,private_bss_bytes=0,
            abi='near Pascal; WORD coordinates/index; all native caller-argument stores and inherited IF/DF'))
    return dict(owners=owners,functions=2,code_bytes=199,ordered_native_fields=fields,mz_relocation_count=0,
                enclosing_CODE_bytes=enclosing['enclosing_CODE_bytes'],enclosing_initialized_DATA_bytes=224,
                enclosing_BSS_bytes=0,enclosing_procedures=19,private_data_bytes=0,private_bss_bytes=0,
                enclosing_DATA_or_other_functions_accepted=False,sprite_assets_or_physical_graphics_accepted=False,
                whole_product_accepted=False)
