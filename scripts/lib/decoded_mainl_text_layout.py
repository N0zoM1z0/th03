"""Complete maintained text renderer, separate from CRT/GRCG services."""
import hashlib
import re
from pathlib import Path
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics
from review_th03_shared_text import analyze, PROFILES

CS, DS, START, SIZE = 0xC7E, 0xE3F, 0x9B7, 613
SOURCE, WRAPPER, OBJECT = 'src/shared/graphics/text.cpp', 'th03/grppsafx.cpp', 'obj/th03/grppsafx.obj'
PUBLIC = '@GRAPH_PUTSA_FX$QIIINXUC'
MAP_PUBLIC = 'graph_putsa_fx(int,int,int,const unsigned char far*)'
BINDINGS = (('__ctype',DS,0xF04),('__mbctype',DS,0x11EE),
            ('__mbcjmstojis',0,0x924C),('GRCG_SETCOLOR',0,0xC36),('GRCG_OFF',0,0xC60))
FIELDS = ((603,206,86,None,5,0),(183,196,22,1,1,1),(154,196,22,1,2,1),
          (128,204,86,None,3,0),(103,196,22,1,2,1),(44,204,86,None,4,0))
DEPENDENCIES = ('th03/grppsafx.cpp','src/shared/graphics/text.cpp',
 'C:\\TC4\\INCLUDE\\mbctype.h','C:\\TC4\\INCLUDE\\ctype.h','C:\\TC4\\INCLUDE\\_defs.h',
 'C:\\TC4\\INCLUDE\\mbstring.h','C:\\TC4\\INCLUDE\\_null.h','compat/rec98/planar.h',
 'planar.h','pc98.h','platform.h','compat/rec98/libs/master.lib/pc98_gfx.hpp',
 'libs/master.lib/pc98_gfx.hpp','libs/master.lib/func.hpp','pc98.h','x86real.h','platform.h',
 'compat/rec98/th01/hardware/grppsafx.h','th01/hardware/grppsafx.h','pc98.h',
 'shiftjis.hpp','decomp.hpp','x86real.h','defconv.h','src/shared/graphics/text_glyph.inl')
STRUCTURE = (('LNAMES','000653484152454404434f4445055f444154410444415441045f42535303425353064447524f5550'),
 ('SEGDEF','286502020301'),('SEGDEF','480000040501'),('SEGDEF','480000060701'),
 ('GRPDEF','08ff02ff03'))


def need(value,message):
    if not value:
        raise ValueError('MAINL current text: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verify(work,target,candidate,graph,files):
    root=Path(__file__).resolve().parents[2];raw=(work/OBJECT).read_bytes()
    d=describe_omf(raw);records=parse_omf(raw)
    need(d['valid'] and d['module_name']==WRAPPER and d['translator_comments']==['TC86 Borland C++ 4.02']
         and tuple(d['dependency_paths'])==DEPENDENCIES, 'complete compiler/dependency identity')
    need(d['record_counts']=={'COMENT':31,'EXTDEF':1,'FIXUPP':1,'GRPDEF':1,'LEDATA':1,
         'LNAMES':1,'MODEND':1,'PUBDEF':1,'SEGDEF':3,'THEADR':1}, 'complete record inventory')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(raw)]==
         [('SHARED','CODE',613),('_DATA','DATA',0),('_BSS','BSS',0)], 'entire producer partition')
    need(tuple((r.name,r.data.hex()) for r in records if r.name in ('LNAMES','SEGDEF','GRPDEF'))==STRUCTURE,
         'literal segment/group/alignment identity')
    need(code_publics(raw,1)==[(0,PUBLIC)] and not code_publics(raw,2) and not code_publics(raw,3),
         'one complete public and no private storage')
    ext,=[r.data for r in records if r.name=='EXTDEF']
    need(ext==b''.join(bytes([len(n)])+n.encode()+b'\0' for n,_,_ in BINDINGS), 'five literal external identities')
    row,=[r for r in graph if r['output']==OBJECT]
    need((row['source'],row['wrapper'],row['game'],row['binary'],row['first_binary'])==
         (SOURCE,WRAPPER,3,'O','op'), 'real GAME3/O first-use producer')
    need(files[WRAPPER].replace(b'\r\n',b'\n')==b'#include "src/shared/graphics/text.cpp"\n', 'exact wrapper')
    for name in DEPENDENCIES:
        if name.startswith('C:\\TC4\\INCLUDE\\'):
            continue  # Complete consumed SDK inventory is bound by sound.images/current audit.
        need(name in files and (work/name).read_bytes()==files[name], 'consumed staged input: '+name)
        if name.startswith('src/'):
            need(files[name].replace(b'\r\n',b'\n')==(root/name).read_bytes().replace(b'\r\n',b'\n'),
                 'literal maintained source/include')
    text=(work/'obj/th03/mainl.map').read_text()
    for seg,off,n,cls,name,group,alignment in ((CS,START,613,'CODE','SHARED','(none)',0x28),
            (DS,0x906,0,'DATA','_DATA','DGROUP',0x48),(DS,0x27EA,0,'BSS','_BSS','DGROUP',0x48)):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{n:04X}\s+C={cls}\s+S={name}\s+G={re.escape(group)}\s+M=th03/grppsafx.cpp\s+ACBP={alignment:02X}\s*$',text))==1,
             'complete native allocation')
    for name,seg,off in (*BINDINGS,(MAP_PUBLIC,CS,START)):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,
             'both native public/external tables: '+name)
    code,blocks=code_bytes(raw,1)
    need([(b['offset'],b['size']) for b in blocks]==[(0,613)], 'one complete LEDATA')
    fixup,=[r.data for r in records if r.name=='FIXUPP'];fields=[];image=bytearray(code);at=0;relocs=[]
    while at<len(fixup):
        loc,low,method=fixup[at:at+3];at+=3
        need(method in (0x16,0x56), 'explicit external fixup only')
        frame=fixup[at] if method==0x16 else None;at+=int(frame is not None)
        index=fixup[at];at+=1;site=(loc&3)*256+low;width=4 if loc&0xFC==0xCC else 2
        addend=int.from_bytes(code[site:site+width],'little');fields.append((site,loc,method,frame,index,addend))
        name,seg,off=BINDINGS[index-1]
        if width==4:
            need((method,frame,seg,addend)==(0x56,None,0,0), 'far external service')
            value=off|(seg<<16);relocs.append((CS,START+site+2))
        else:
            need((loc&0xFC,method,frame,seg,addend)==(0xC4,0x16,1,DS,1), 'DGROUP classifier plus-one')
            value=off+addend
        image[site:site+width]=value.to_bytes(width,'little')
    need(tuple(fields)==FIELDS, 'all six literal ordered fields/addends')
    begin=CS*16+START
    need(bytes(image)==target.program_image[begin:begin+SIZE]==candidate.program_image[begin:begin+SIZE],
         'complete independently resolved raw equality')
    for mz in (target,candidate):
        need([(r.segment,r.offset) for r in mz.relocations if begin<=r.linear<begin+SIZE]==relocs,
             'literal ordered three MZ relocations')
    analysis=analyze(target.program_image,PROFILES['mainl'])
    need(analysis==analyze(candidate.program_image,PROFILES['mainl']), 'complete decoder/ABI/context equality')
    body=analysis['bodies'][0]
    need((body['size'],body['instructions'])==(613,226), 'whole instruction-only RETF10 body')
    owner=dict(unit_id='th03-mainl-decoded-text-renderer',name=PUBLIC,source=SOURCE,object=OBJECT,
        start=begin,size=SIZE,segment=CS,offset=START,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=sha(image),candidate_sha256=sha(image),ordered_relocations=[list(r) for r in relocs],
        argument_bytes=10,callee_pop_bytes=10,private_data_bytes=0,private_bss_bytes=0,
        abi='far Pascal RETF10; signed16 coordinates/effect, far string; CRT converter far cdecl')
    return dict(owners=[owner],functions=1,code_bytes=613,instruction_count=226,
        producer_code_bytes=613,private_data_bytes=0,private_bss_bytes=0,
        ordered_native_fields=fields,mz_relocation_count=3,native_object_sha256=sha(raw),
        complete_producer_sha256=sha(image),consumed_paths=list(DEPENDENCIES),boundaries=analysis,
        contextual_service_bytes=46,context_credited=False,crt_tables_credited=False,
        physical_font_or_device_accepted=False,whole_product_accepted=False)
