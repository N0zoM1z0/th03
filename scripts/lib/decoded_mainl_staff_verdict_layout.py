"""Whole native verdict; local SEGDEF fields and far renderer ABI stay distinct."""
import hashlib
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes
from lib.decoded_mainl_ending_layout import CS, DS, SOURCE, WRAPPER, OBJECT, verify as enclosing_layout

START,SIZE,NATIVE = 0x2C98,389,2326
RENDER = (0xC7E,0x9B7)
DATA = dict(score=0x27DC,playchar=0x27E7,rank=0x27E6,skill=0x27E8,unit=0xC25,
            playchars=0xAE2,ranks=0xB06,numbers=0xB16)
BINDINGS = {30:('_score',DS,DATA['score']),52:('@GRAPH_PUTSA_FX$QIIINXUC',*RENDER),
            53:('_mainl_verdict_unit',DS,DATA['unit']),54:('_mainl_verdict_playchar',DS,DATA['playchar']),
            55:('_mainl_verdict_rank',DS,DATA['rank']),56:('_mainl_verdict_skill',DS,DATA['skill'])}
LOCAL_TABLES = {132:('_mainl_verdict_playchars',DATA['playchars'],9),168:('_mainl_verdict_ranks',DATA['ranks'],4),
                184:('_mainl_verdict_numbers',DATA['numbers'],10)}
LOCAL_DATA_BASE = 0xA5E
CALLS = (0x2CB5,0x2CD1,0x2D1E,0x2D47,0x2D5E,0x2D95,0x2DDB,0x2E01,0x2E14)
FIELDS = ((2707, 206, 86, None, 52, 0),
 (2704, 198, 22, 2, 53, 0),
 (2688, 206, 86, None, 52, 0),
 (2685, 198, 20, 2, 2, 184),
 (2658, 198, 22, 2, 56, 0),
 (2650, 206, 86, None, 52, 0),
 (2647, 198, 20, 2, 2, 184),
 (2588, 198, 22, 2, 56, 0),
 (2580, 206, 86, None, 52, 0),
 (2577, 198, 20, 2, 2, 184),
 (2530, 197, 22, 2, 56, 0),
 (2525, 205, 86, None, 52, 0),
 (2522, 197, 20, 2, 2, 184),
 (2502, 205, 86, None, 52, 0),
 (2499, 197, 20, 2, 2, 184),
 (2478, 197, 22, 2, 30, 0),
 (2461, 205, 86, None, 52, 0),
 (2458, 197, 20, 2, 2, 184),
 (2408, 197, 22, 2, 30, 0),
 (2384, 205, 86, None, 52, 0),
 (2381, 197, 20, 2, 2, 168),
 (2369, 197, 22, 2, 55, 0),
 (2356, 205, 86, None, 52, 0),
 (2353, 197, 20, 2, 2, 132),
 (2341, 197, 22, 2, 54, 0))


def need(value,message):
    if not value:
        raise ValueError('MAINL staff verdict layout: '+message)


def native_image(raw):
    code,_ = code_bytes(raw,1)
    need(len(code_bytes(raw,2)[0])==224,'complete native DATA contribution remains separate')
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
            if method==0x14:
                need((loc&0xFC,frame,index,width)==(0xC4,2,2,2),'literal local SEGDEF2/DGROUP field, never EXTDEF2')
                name,offset,_ = LOCAL_TABLES[addend]
                need(offset==LOCAL_DATA_BASE+addend,'native local DATA base plus table offset')
                value,namespace = offset,'SEGDEF'
            else:
                name,segment,offset = BINDINGS[index]
                need(names[index-1]==name and addend==0,'literal zero-addend external identity')
                if width==4:
                    need((loc&0xFC,method,frame,index,segment)==(0xCC,0x56,None,52,RENDER[0]),'literal far renderer field')
                    value = offset|(segment<<16)
                else:
                    need((loc&0xFC,method,frame,segment)==(0xC4,0x16,2,DS),'external WORD DGROUP field')
                    value = offset
                namespace = 'EXTDEF'
            image[site-NATIVE:site-NATIVE+width] = value.to_bytes(width,'little')
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,namespace=namespace,
                               name=name,addend=addend,width=width))
    need(tuple(fields)==FIELDS,'complete literal ordered native fields')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    enclosing_layout(work,target,candidate,graph,files)
    image,fields = native_image((work/OBJECT).read_bytes())
    start = CS*16+START
    need(image==target.program_image[start:start+SIZE]==candidate.program_image[start:start+SIZE],'complete independently linked native verdict')
    ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image,START))
    need(sum(i.size for i in ins)==SIZE and (ins[-1].mnemonic,ins[-1].op_str)==('ret',''),'complete near zero-argument RET body')
    calls = [(i.address,tuple(int(v.strip(),16) for v in i.op_str.split(','))) for i in ins if i.mnemonic=='lcall']
    need(calls==[(at,RENDER) for at in CALLS] and not any(i.mnemonic=='call' for i in ins),'all nine far renderer call sites')
    text = (work/'obj/th03/mainl.map').read_text()
    publics = [(n,s,o) for i,(n,s,o) in BINDINGS.items() if i!=52]
    publics += [(n,DS,o) for n,o,_ in LOCAL_TABLES.values()]
    publics += [('_mainl_staff_verdict',CS,START),('graph_putsa_fx(int,int,int,const unsigned char far*)',*RENDER)]
    for name,segment,offset in publics:
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,'both MAP public tables: '+name)
    expected = [(CS,0x2382+f['offset']+2) for f in fields if f['width']==4]
    for mz in (target,candidate):
        need([(r.segment,r.offset) for r in mz.relocations if start<=r.linear<start+SIZE]==expected,'complete literal ordered MZ vector')
    digest = hashlib.sha256(image).hexdigest()
    owner = dict(unit_id='th03-mainl-decoded-staff-verdict',name='_mainl_staff_verdict',source=SOURCE,object=OBJECT,
        start=start,size=SIZE,segment=CS,offset=START,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=digest,candidate_sha256=digest,ordered_relocations=[list(r) for r in expected],
        argument_bytes=0,callee_pop_bytes=0,private_data_bytes=0,private_bss_bytes=0,
        abi='near zero-argument function; ENTER4 and saved SI/DI; far Pascal renderer pop10 with full DWORD string pointers')
    return dict(owners=[owner],functions=1,code_bytes=SIZE,ordered_native_fields=fields,mz_relocation_count=9,
        far_calls=[dict(offset=at,segment=s,callee=ip,argument_bytes=10,callee_pop_bytes=10) for at,(s,ip) in calls],
        local_SEGDEF_fields=8,external_WORD_fields=8,far_renderer_fields=9,local_pointer_bytes=4,
        enclosing_CODE_bytes=3695,enclosing_initialized_DATA_bytes=224,enclosing_BSS_bytes=0,enclosing_procedures=19,
        enclosing_DATA_or_other_functions_accepted=False,renderer_code_or_strings_tables_accepted=False,
        physical_text_or_pixels_proved=False,whole_product_accepted=False)
