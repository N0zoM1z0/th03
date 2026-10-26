"""Current complete cutscene producer: 13 procedures, separate inline-table context.

Resolve every native field independently using literal EXTDEF/MAP bindings.
Only the 3,122 instruction bytes receive ownership; 72 switch-table bytes and
the observed compiler-emitted zero remain required, uncredited context.
"""
import hashlib
import re
from pathlib import Path
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics
from review_th03_mainl_cutscene import decode, RANGES
from lib.decoded_mainl_cutscene_inventory import PUBLICS, PUBLIC_MAP, BINDINGS, FIELDS, DEPENDENCIES

CS, DS, START, SIZE = 0x95F, 0xE3F, 0xB3E, 3195
SOURCE, WRAPPER, OBJECT = 'src/mainl/cutscene.cpp', 'th03/cutscene.cpp', 'obj/th03/cutscene.obj'


def need(value, message):
    if not value:
        raise ValueError('MAINL cutscene layout: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def native_image(raw):
    code, blocks = code_bytes(raw, 1)
    need(len(code)==SIZE and [(b['offset'],b['size']) for b in blocks]==
         [(0,1019),(1019,1019),(2038,1021),(3059,136)], 'entire contiguous compiler LEDATA')
    image=bytearray(code)
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
            block=rec.data[0],int.from_bytes(rec.data[1:3],'little')
            need(block[0]==1, 'no hidden initialized DATA producer')
        if rec.name!='FIXUPP':
            continue
        need(block is not None and block[0]==1, 'all fixups belong to complete CODE')
        at=0
        while at<len(rec.data):
            loc,low,method=rec.data[at:at+3]
            at+=3
            need(method in (0x14,0x16,0x56), 'explicit no-thread native field methods')
            frame=rec.data[at] if method in (0x14,0x16) else None
            at+=int(frame is not None)
            index=rec.data[at]
            at+=1
            site=block[1]+(loc&3)*256+low
            width=4 if loc&0xFC==0xCC else 2
            need(block[1]<=site and site+width<=SIZE, 'complete native field bounds')
            addend=int.from_bytes(code[site:site+width],'little')
            fields.append((site,loc,method,frame,index,addend))
            if method==0x14:
                need((loc&0xFC,frame,index)==(0xC4,1,1), 'same-group own CODE WORD')
                name='CUTSCENE_TEXT'
                value=START+addend
            else:
                name,_,segment,offset=BINDINGS[index]
                need(names[index-1]==name, 'literal EXTDEF identity')
                if width==4:
                    need((loc&0xFC,method,frame,addend)==(0xCC,0x56,None,0), 'far zero-addend field')
                    value=offset|(segment<<16)
                else:
                    need((loc&0xFC,method,frame,segment)==(0xC4,0x16,2,DS), 'DGROUP external WORD')
                    value=offset+addend
            image[site:site+width]=value.to_bytes(width,'little')
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,
                               name=name,addend=addend,width=width))
    need(tuple(fields)==FIELDS and len(fields)==236, 'all literal ordered native fields')
    need(names==[v[0] for v in BINDINGS.values()], 'entire external inventory')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    root=Path(__file__).resolve().parents[2]
    raw=(work/OBJECT).read_bytes()
    d=describe_omf(raw)
    need(d['record_counts']=={'COMENT':60,'EXTDEF':1,'FIXUPP':4,'GRPDEF':2,'LEDATA':4,
         'LNAMES':1,'MODEND':1,'PUBDEF':13,'SEGDEF':3,'THEADR':1}, 'entire native record inventory')
    lnames=[]
    for rec in parse_omf(raw):
        if rec.name=='LNAMES':
            at=0
            while at<len(rec.data):
                n=rec.data[at]
                lnames.append(rec.data[at+1:at+1+n].decode())
                at+=n+1
    need(lnames==['','CUTSCENE_TEXT','CODE','_DATA','DATA','_BSS','BSS','GROUP_01','DGROUP']
         and [list(r.data) for r in parse_omf(raw) if r.name=='GRPDEF']==[[8,255,1],[9,255,2,255,3]],
         'literal OMF group1 CODE and group2 DATA/BSS frame identities')
    need(d['valid'] and d['translator_comments']==['TC86 Borland C++ 4.02']
         and tuple(d['dependency_paths'])==DEPENDENCIES, 'native compiler and complete consumed input inventory')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(raw)]==
         [('CUTSCENE_TEXT','CODE',SIZE),('_DATA','DATA',0),('_BSS','BSS',0)],
         'entire CODE and zero private DATA/BSS')
    need([r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF']==[0x28,0x48,0x48]
         and tuple(code_publics(raw,1))==PUBLICS, 'all thirteen native publics and natural segment alignment')
    row,=[r for r in graph if r['output']==OBJECT]
    need((row['source'],row['wrapper'],row['game'],row['binary'],row['first_binary'])==
         (SOURCE,WRAPPER,3,'L','mainl'), 'actual maintained producer')
    need(files[WRAPPER].replace(b'\r\n',b'\n')==b'#include "src/mainl/cutscene.cpp"\n',
         'literal maintained include wrapper')
    for name in (SOURCE,'src/mainl/cutscene/cutscene.hpp','src/mainl/cutscene/script.inl',
                 'src/mainl/cutscene/egc_start_copy.inl'):
        need(files[name].replace(b'\r\n',b'\n')==(root/name).read_bytes().replace(b'\r\n',b'\n'),
             'actual maintained producer input: '+name)
    text=(work/'obj/th03/mainl.map').read_text()
    for segment,offset,size,cls,seg,group in (
        (CS,START,SIZE,'CODE','CUTSCENE_TEXT','GROUP_01'),
        (DS,0x906,0,'DATA','_DATA','DGROUP'),(DS,0x27EA,0,'BSS','_BSS','DGROUP')):
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+{size:04X}\s+C={cls}\s+S={seg}\s+G={group}\s+M=th03/cutscene.cpp\s+ACBP={(0x28 if cls=="CODE" else 0x48):02X}\s*$',text))==1,
             'complete native MAP allocation')
    for _,symbol,segment,offset in BINDINGS.values():
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,
             'both literal external MAP tables: '+symbol)
    for (offset,_),symbol in zip(PUBLICS,PUBLIC_MAP):
        need(len(re.findall(rf'(?m)^\s*{CS:04X}:{START+offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,
             'both owner MAP tables: '+symbol)
    image,fields=native_image(raw)
    begin=CS*16+START
    need(image==target.program_image[begin:begin+SIZE]==candidate.program_image[begin:begin+SIZE],
         'entire independently resolved object equals both decoded images')
    boundaries=decode(target.program_image)
    need(boundaries==decode(candidate.program_image), 'complete current instruction/branch/table closure')
    need(sum(r['size'] for r in boundaries['functions'])==3122 and
         sum(r['instruction_count'] for r in boundaries['functions'])==1057, 'complete instruction partition')
    need([(r['offset']-START,r['size']) for r in boundaries['functions']]==
         [(offset,size) for (offset,_),(_,_,size,_) in zip(PUBLICS,RANGES)], 'all public procedure boundaries')
    table_sites=set(range(2808,2816,2))|set(range(2848,2880,2))
    need({f['offset'] for f in fields if f['fixdat']==0x14}==table_sites|{1340,1519},
         'twenty destination WORDs and two dispatch table references')
    need(image[2807]==0 and code_bytes(raw,1)[0][2807]==0, 'zero is emitted LEDATA context, not linker tail')
    expected=[(CS,START+f['offset']+2) for f in fields if f['width']==4]
    need(len(expected)==56, 'complete far-field relocation count')
    for mz in (target,candidate):
        need([(r.segment,r.offset) for r in mz.relocations if begin<=r.linear<begin+SIZE]==expected,
             'complete literal ordered MZ relocation vector')
    # The old diagnostic helper called this an alignment byte. Current proof
    # establishes LEDATA provenance only, not an independent causal rationale.
    boundaries['tables']['uncredited_context_start']=boundaries['tables'].pop('alignment_start')
    boundaries['tables']['uncredited_context_size']=boundaries['tables'].pop('alignment_size')
    owners=[]
    for row,(_,public) in zip(boundaries['functions'],PUBLICS):
        start=CS*16+row['offset'];size=row['size']
        owners.append(dict(unit_id='th03-mainl-decoded-cutscene-'+row['name'].replace('_','-'),
            name=public,source=SOURCE,object=OBJECT,start=start,size=size,segment=CS,offset=row['offset'],
            coordinate_space='decoded-load',canonical_file_offset=None,
            target_sha256=row['body_sha256'],candidate_sha256=row['body_sha256'],
            ordered_relocations=[list(r) for r in expected if row['offset']<=r[1]<row['offset']+size],
            argument_bytes=int(row['cleanup'] or 0),callee_pop_bytes=int(row['cleanup'] or 0),
            private_data_bytes=0,private_bss_bytes=0,
            abi='near Pascal arguments/noargs; large-model pointers; BYTE script opcode occupies WORD slot'))
    return dict(owners=owners,functions=13,code_bytes=3122,instruction_count=1057,
        producer_code_bytes=SIZE,private_data_bytes=0,private_bss_bytes=0,
        ordered_native_fields=fields,mz_relocation_count=56,boundaries=boundaries,
        required_inline_table_bytes=72,inline_tables_credited=False,uncredited_compiler_context_bytes=1,
        complete_producer_sha256=sha(image),consumed_paths=list(DEPENDENCIES),
        physical_runtime_or_assets_accepted=False,whole_product_accepted=False)
