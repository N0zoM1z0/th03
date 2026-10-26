"""Current registration ownership; complete native producer with uncredited context.

Resolve all 188 OMF fields, including local DATA and self-relative near calls,
without modifying native objects or executable images. Music and pointer DATA
are required context, not accepted source owners.
"""
import hashlib
import re
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from pathlib import Path
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics
from review_th03_mainl_regist import decode, RANGES
from lib.decoded_mainl_registration_inventory import PUBLICS, PUBLIC_MAP, BINDINGS, FIELDS, DEPENDENCIES

CS, DS, START, SIZE, OWNED, DATA = 0x95F, 0xE3F, 0x189E, 2788, 2720, 0x906
SOURCE, WRAPPER, OBJECT = 'src/mainl/hiscore/regdata.cpp', 'regdata.cpp', 'obj/th03/regdata.obj'


def need(value, message):
    if not value:
        raise ValueError('MAINL registration layout: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def native_image(raw):
    originals = {s:code_bytes(raw,s)[0] for s in (1,2)}
    images = {s:bytearray(b) for s,b in originals.items()}
    for seg, expected in ((1,[(0,1022),(1022,1021),(2043,745)]),(2,[(0,40)])):
        need([(b['offset'],b['size']) for b in code_bytes(raw,seg)[1]]==expected,
             'entire contiguous CODE/DATA LEDATA')
    names, fields, report = [], [], []
    block=None
    for rec in parse_omf(raw):
        if rec.name=='EXTDEF':
            at=0
            while at<len(rec.data):
                n=rec.data[at]
                names.append(rec.data[at+1:at+n+1].decode())
                need(rec.data[at+n+1]==0, 'literal external type index')
                at+=n+2
        if rec.name=='LEDATA':
            block=rec.data[0],int.from_bytes(rec.data[1:3],'little'),len(rec.data)-3
        if rec.name!='FIXUPP':
            continue
        need(block is not None and block[0] in (1,2), 'CODE/DATA fixup block')
        seg,base,length=block
        at=0
        while at<len(rec.data):
            loc,low,method=rec.data[at:at+3];at+=3
            need(method in (0x14,0x16,0x56), 'explicit no-thread field methods')
            frame=rec.data[at] if method in (0x14,0x16) else None
            at+=int(frame is not None)
            index=rec.data[at];at+=1
            site=base+(loc&3)*256+low
            width=4 if loc&0xFC==0xCC else 2
            need(base<=site and site+width<=base+length, 'native field within its LEDATA')
            addend=int.from_bytes(originals[seg][site:site+width],'little')
            fields.append((seg,site,loc,method,frame,index,addend))
            if method==0x14:
                need((seg,site,loc,frame,index,addend)==(1,1402,0xC5,2,2,0), 'local DATA frame/group/segment reference')
                name='_REGIST_PLAYCHARS';value=DATA+addend
            else:
                name,_,segment,offset=BINDINGS[index]
                need(names[index-1]==name, 'literal EXTDEF identity')
                if width==4:
                    need((loc&0xFC,method,frame,addend)==
                         ((0xCC,0x56,None,0) if seg==1 else (0xCC,0x16,2,0)),
                         'far CODE external or DGROUP-framed DATA pointer')
                    need(seg==1 or segment==DS, 'DATA pointers target DGROUP')
                    value=offset|(segment<<16)
                elif loc&0xFC==0x84:
                    need((seg,method,frame,segment,addend)==(1,0x16,1,CS,0), 'self-relative near external same CODE group')
                    value=(offset-(START+site+2))&0xFFFF
                else:
                    need((seg,loc&0xFC,method,frame,segment)==(1,0xC4,0x16,2,DS), 'DGROUP external WORD')
                    value=offset+addend
            images[seg][site:site+width]=value.to_bytes(width,'little')
            report.append(dict(segment_index=seg,offset=site,locat=loc,fixdat=method,frame=frame,target=index,
                               name=name,addend=addend,width=width))
    need(tuple(fields)==FIELDS and len(fields)==188, 'all literal ordered native fields')
    need(names==[v[0] for v in BINDINGS.values()], 'entire seventy-external inventory')
    need([f['offset'] for f in report if f['segment_index']==2]==list(range(36,-1,-4)), 'native descending DATA pointer order')
    return {s:bytes(b) for s,b in images.items()},report


def verify(work,target,candidate,graph,files):
    root=Path(__file__).resolve().parents[2]
    raw=(work/OBJECT).read_bytes();d=describe_omf(raw)
    need(d['record_counts']=={'COMENT':77,'EXTDEF':1,'FIXUPP':4,'GRPDEF':2,'LEDATA':4,
         'LNAMES':1,'MODEND':1,'PUBDEF':16,'SEGDEF':3,'THEADR':1}, 'complete native record inventory')
    lnames=[]
    for rec in parse_omf(raw):
        if rec.name=='LNAMES':
            at=0
            while at<len(rec.data):
                n=rec.data[at];lnames.append(rec.data[at+1:at+1+n].decode());at+=n+1
    need(lnames==['','REGIST_TEXT','CODE','_DATA','DATA','_BSS','BSS','GROUP_01','DGROUP']
         and [list(r.data) for r in parse_omf(raw) if r.name=='GRPDEF']==[[8,255,1],[9,255,2,255,3]],
         'literal CODE group1 and DATA/BSS group2')
    need(d['valid'] and d['module_name']==WRAPPER and d['translator_comments']==['TC86 Borland C++ 4.02']
         and tuple(d['dependency_paths'])==DEPENDENCIES, 'compiler and complete consumed path inventory')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(raw)]==
         [('REGIST_TEXT','CODE',SIZE),('_DATA','DATA',40),('_BSS','BSS',0)], 'complete producer extents')
    need([r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF']==[0x28,0x48,0x48]
         and tuple(code_publics(raw,1))==PUBLICS and code_publics(raw,2)==[(0,'_REGIST_PLAYCHARS')],
         'all native publics and natural alignment')
    row,=[r for r in graph if r['output']==OBJECT]
    need((row['source'],row['wrapper'],row['game'],row['binary'],row['first_binary'])==
         (SOURCE,WRAPPER,3,'L','mainl'), 'actual maintained producer')
    need(files[WRAPPER].replace(b'\r\n',b'\n')==(root/SOURCE).read_bytes().replace(b'\r\n',b'\n'),
         'literal maintained producer transport')
    for name in DEPENDENCIES:
        need(name in files and (work/name).read_bytes()==files[name], 'complete consumed staged input: '+name)
        if name.startswith('src/'):
            need(files[name].replace(b'\r\n',b'\n')==(root/name).read_bytes().replace(b'\r\n',b'\n'),
                 'maintained input: '+name)
    text=(work/'obj/th03/mainl.map').read_text()
    for segment,offset,size,cls,seg,group in (
        (CS,START,SIZE,'CODE','REGIST_TEXT','GROUP_01'),
        (DS,DATA,40,'DATA','_DATA','DGROUP'),(DS,0x27EA,0,'BSS','_BSS','DGROUP')):
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+{size:04X}\s+C={cls}\s+S={seg}\s+G={group}\s+M=regdata.cpp\s+ACBP={(0x28 if cls=="CODE" else 0x48):02X}\s*$',text))==1,
             'complete native MAP allocation')
    for _,symbol,segment,offset in BINDINGS.values():
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,
             'both external MAP tables: '+symbol)
    for (offset,_),symbol in zip(PUBLICS,PUBLIC_MAP):
        need(len(re.findall(rf'(?m)^\s*{CS:04X}:{START+offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,
             'both public MAP tables: '+symbol)
    need(len(re.findall(r'(?m)^\s*0E3F:0906\s+_REGIST_PLAYCHARS\s*$',text))==2,'local DATA public MAP identity')
    images,fields=native_image(raw)
    for seg,start,segment,size in ((1,START,CS,SIZE),(2,DATA,DS,40)):
        begin=segment*16+start
        need(images[seg]==target.program_image[begin:begin+size]==candidate.program_image[begin:begin+size],
             'complete independently resolved producer CODE/DATA equality')
        expected=[(segment,start+f['offset']+2) for f in fields if f['segment_index']==seg and f['width']==4]
        for mz in (target,candidate):
            need([(r.segment,r.offset) for r in mz.relocations if begin<=r.linear<begin+size]==expected,
                 'complete literal ordered producer relocations')
    # Decode the predecessor only as context for the three near external calls.
    allrows=decode(target.program_image)
    need(allrows==decode(candidate.program_image),'complete instruction and branch closure')
    rows=allrows[3:]
    need([(r['offset']-START,r['size']) for r in rows]==
         [(offset,size) for (offset,_),(_,_,size,_) in zip(PUBLICS,RANGES[3:])]
         and sum(r['size'] for r in rows)==OWNED and sum(r['instruction_count'] for r in rows)==988,
         'fourteen complete public procedures /2720 bytes/988 instructions')
    selected=[f for f in fields if f['segment_index']==1 and f['offset']<OWNED]
    need(len(selected)==170 and sum(f['width']==4 for f in selected)==54
         and sum(f['locat']&0xFC==0x84 for f in selected)==3
         and sum(f['fixdat']==0x14 for f in selected)==1
         and sum(f['locat']&0xFC==0xC4 and f['fixdat']==0x16 for f in selected)==112,
         'selected native field partition')
    need(sum(f['segment_index']==1 and f['offset']>=OWNED for f in fields)==8, 'eight music context fields')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    for offset in (0x07EF,0x0959,0x2438):
        call,=list(decoder.disasm(target.program_image[CS*16+offset:CS*16+offset+3],offset))
        need(call.mnemonic=='call' and call.op_str=='0x21e2', 'real near menu caller')
    expected=[(CS,START+f['offset']+2) for f in selected if f['width']==4]
    owners=[]
    for row,(_,public) in zip(rows,PUBLICS):
        start=CS*16+row['offset'];size=row['size']
        owners.append(dict(unit_id='th03-mainl-decoded-registration-'+row['name'].replace('_','-'),
            name=public,source=SOURCE,object=OBJECT,start=start,size=size,segment=CS,offset=row['offset'],
            coordinate_space='decoded-load',canonical_file_offset=None,
            target_sha256=row['sha256'],candidate_sha256=row['sha256'],
            ordered_relocations=[list(r) for r in expected if row['offset']<=r[1]<row['offset']+size],
            argument_bytes=int(row['cleanup'] or 0),callee_pop_bytes=int(row['cleanup'] or 0),
            private_data_bytes=0,private_bss_bytes=0,
            abi='near Pascal arguments/noargs; load returns void; insertion returns signed AX'))
    return dict(owners=owners,functions=14,code_bytes=OWNED,instruction_count=988,
        producer_code_bytes=SIZE,producer_data_bytes=40,private_data_bytes=0,private_bss_bytes=0,
        ordered_native_fields=fields,mz_relocation_count=54,boundaries=rows,
        context_code_bytes=68,context_data_bytes=40,context_credited=False,
        predecessor_context_code_bytes=229,predecessor_context_credited=False,
        native_object_sha256=sha(raw),complete_producer_sha256=sha(images[1]),producer_data_sha256=sha(images[2]),
        selected_code_sha256=sha(images[1][:OWNED]),consumed_paths=list(DEPENDENCIES),
        physical_runtime_or_assets_accepted=False,whole_product_accepted=False)
