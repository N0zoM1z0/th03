"""Complete current score-data producer; no reference/body byte patches."""
import hashlib
import re
from pathlib import Path
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics
from review_th03_mainl_regist import decode

CS, DS, START, SIZE = 0x95F, 0xE3F, 0x17B9, 229
SOURCE, WRAPPER, OBJECT = 'src/mainl/scoredat.cpp', 'th03/scoredat.cpp', 'obj/th03/scoredat.obj'
PUBLICS = ((0, '@scoredat_decode$qv'), (60, '@scoredat_recreate$qv'), (187, '@scoredat_sum_invalid$qv'))
PUBLIC_MAP = ('scoredat_decode()', 'scoredat_recreate()', 'scoredat_sum_invalid()')
# Native FIXUPP order, including explicit group and external indices/addends.
FIELDS = ((216,196,22,2,1,0),(194,196,22,2,1,2),(172,132,22,1,2,0),
          (163,196,22,2,1,82),(150,196,22,2,1,87),(132,196,22,2,1,88),
          (121,196,22,2,1,194),(116,196,22,2,1,184),(105,196,22,2,1,84),
          (85,196,22,2,1,2),(51,196,22,2,1,205),(47,196,22,2,1,204),
          (29,196,22,2,1,204),(19,196,22,2,1,205),(6,196,22,2,1,0))
DEPENDENCIES = ('th03/scoredat.cpp','src/mainl/scoredat.cpp','C:\\TC4\\INCLUDE\\stddef.h',
 'C:\\TC4\\INCLUDE\\_defs.h','C:\\TC4\\INCLUDE\\_null.h','compat/rec98/th03/common.h','th03/common.h',
 'platform.h','src/mainl/hiscore/scoredat.hpp','src/mainl/hiscore/regi.h','compat/rec98/th03/score.hpp',
 'th03/score.hpp','th03/common.h','platform.h','th02/score.h','platform.h',
 'compat/rec98/th03/playchar.hpp','th03/playchar.hpp','platform.h','compat/rec98/th01/rank.h',
 'th01/rank.h','src/mainl/hiscore/scorecry.hpp')


def need(value, message):
    if not value:
        raise ValueError('MAINL scoredat layout: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verify(work,target,candidate,graph,files):
    root=Path(__file__).resolve().parents[2]
    raw=(work/OBJECT).read_bytes();d=describe_omf(raw);records=parse_omf(raw)
    need(d['valid'] and d['module_name']==WRAPPER and d['translator_comments']==['TC86 Borland C++ 4.02']
         and tuple(d['dependency_paths'])==DEPENDENCIES, 'complete compiler/dependency identity')
    need(d['record_counts']=={'COMENT':28,'EXTDEF':1,'FIXUPP':1,'GRPDEF':2,'LEDATA':1,
         'LNAMES':1,'MODEND':1,'PUBDEF':3,'SEGDEF':3,'THEADR':1}, 'complete record inventory')
    need([(s['name'],s['class'],s['size']) for s in segment_definitions(raw)]==
         [('SCOREDAT_TEXT','CODE',229),('_DATA','DATA',0),('_BSS','BSS',0)], 'complete producer partition')
    need([r.data[0] for r in records if r.name=='SEGDEF']==[0x28,0x48,0x48]
         and tuple(code_publics(raw,1))==PUBLICS
         and not code_publics(raw,2) and not code_publics(raw,3), 'native alignment and complete publics')
    need([r.data for r in records if r.name=='LNAMES']==
         [b'\x00\x0dSCOREDAT_TEXT\x04CODE\x05_DATA\x04DATA\x04_BSS\x03BSS\x08GROUP_01\x06DGROUP']
         and [list(r.data) for r in records if r.name=='GRPDEF']==[[8,255,1],[9,255,2,255,3]],
         'literal CODE and DATA group identities')
    need([r.data for r in records if r.name=='EXTDEF']==
         [b'\x03_hi\x00\x22@SCOREDAT_ENCODE_AND_SAVE$Q6RANK_T\x00'], 'two literal native externals')
    row,=[r for r in graph if r['output']==OBJECT]
    need((row['source'],row['wrapper'],row['game'],row['binary'],row['first_binary'])==
         (SOURCE,WRAPPER,3,'O','op'), 'real GAME3/O first-use producer, not invented MAINL mode')
    need(files[WRAPPER].replace(b'\r\n',b'\n')==b'#include "src/mainl/scoredat.cpp"\n', 'exact include wrapper')
    for name in DEPENDENCIES:
        if name.startswith('C:\\TC4\\INCLUDE\\'):
            continue  # Complete SDK inventory is independently checked by sound.images/audit.
        need(name in files and (work/name).read_bytes()==files[name], 'consumed staged input: '+name)
        if name.startswith('src/'):
            need(files[name].replace(b'\r\n',b'\n')==(root/name).read_bytes().replace(b'\r\n',b'\n'),
                 'literal maintained source/header')
    text=(work/'obj/th03/mainl.map').read_text()
    for segment,offset,size,cls,seg,group in (
        (CS,START,229,'CODE','SCOREDAT_TEXT','GROUP_01'),
        (DS,0x906,0,'DATA','_DATA','DGROUP'),(DS,0x27EA,0,'BSS','_BSS','DGROUP')):
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+{size:04X}\s+C={cls}\s+S={seg}\s+G={group}\s+M=th03/scoredat.cpp\s+ACBP={(0x28 if cls=="CODE" else 0x48):02X}\s*$',text))==1,
             'complete native MAP allocation')
    for segment,offset,symbol in [(CS,START+o,n) for (o,_),n in zip(PUBLICS,PUBLIC_MAP)]+[
            (DS,0x21EE,'_hi'),(CS,0x1900,'scoredat_encode_and_save(rank_t)')]:
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,
             'both literal public/external MAP tables: '+symbol)
    code,blocks=code_bytes(raw,1)
    need([(b['offset'],b['size']) for b in blocks]==[(0,229)], 'one entire contiguous CODE LEDATA')
    fixup,=[r.data for r in records if r.name=='FIXUPP'];fields=[];image=bytearray(code)
    need(len(fixup)==75,'fifteen explicit no-thread WORD fields')
    for at in range(0,len(fixup),5):
        loc,low,method,frame,index=fixup[at:at+5];site=(loc&3)*256+low
        need(site+2<=SIZE,'field within complete CODE')
        addend=int.from_bytes(code[site:site+2],'little')
        fields.append((site,loc,method,frame,index,addend))
        if (loc,method,frame,index)==(0xC4,0x16,2,1):
            value=0x21EE+addend
        else:
            need((site,loc,method,frame,index,addend)==(172,0x84,0x16,1,2,0),
                 'only self-relative near encode/save external')
            value=(0x1900-(START+site+2))&0xFFFF
        image[site:site+2]=value.to_bytes(2,'little')
    need(tuple(fields)==FIELDS,'all fifteen literal ordered fixups/addends')
    begin=CS*16+START
    need(bytes(image)==target.program_image[begin:begin+SIZE]==candidate.program_image[begin:begin+SIZE],
         'complete independently resolved producer equality')
    for mz in (target,candidate):
        need(not [r for r in mz.relocations if begin<=r.linear<begin+SIZE], 'literal empty MZ relocation vector')
    allrows=decode(target.program_image)
    need(allrows==decode(candidate.program_image),'complete near call and branch closure')
    rows=allrows[:3]
    need([(r['offset']-START,r['size'],r['cleanup']) for r in rows]==[(0,60,''),(60,127,''),(187,42,'')]
         and sum(r['instruction_count'] for r in rows)==98, 'three complete near noargs procedures /98 instructions')
    owners=[]
    for row,(_,public) in zip(rows,PUBLICS):
        owners.append(dict(unit_id='th03-mainl-decoded-scoredat-'+row['name'].replace('_','-'),
            name=public,source=SOURCE,object=OBJECT,start=CS*16+row['offset'],size=row['size'],segment=CS,offset=row['offset'],
            coordinate_space='decoded-load',canonical_file_offset=None,
            target_sha256=row['sha256'],candidate_sha256=row['sha256'],ordered_relocations=[],
            argument_bytes=0,callee_pop_bytes=0,private_data_bytes=0,private_bss_bytes=0,
            abi='near noargs; decode/recreate void; checksum mismatch bool in AL'))
    return dict(owners=owners,functions=3,code_bytes=229,instruction_count=98,producer_code_bytes=229,
        private_data_bytes=0,private_bss_bytes=0,ordered_native_fields=fields,mz_relocation_count=0,boundaries=rows,
        native_object_sha256=sha(raw),complete_producer_sha256=sha(image),consumed_paths=list(DEPENDENCIES),
        external_hi_bytes=206,external_hi_credited=False,encode_save_callee_credited=False,
        physical_runtime_or_file_success_accepted=False,whole_product_accepted=False)
