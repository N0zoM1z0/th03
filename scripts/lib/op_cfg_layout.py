"""Three whole near configuration functions inside the larger OP entry TU.

Surrounding menu CODE, DATA and BSS remain context. Resolution is performed in
comparison buffers only; no native object or executable is rewritten.
"""
import hashlib
import re

from lib.omf import describe_omf,parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes,code_publics

SOURCE='src/op/entry.cpp'
WRAPPER='th03/op_01.cpp'
OBJECT='obj/th03/op_01.obj'
SEGMENT,OFFSET,DATA_SEGMENT,DATA_OFFSET=0x990,8,0xD7F,0x90
FUNCTIONS=(('th03-op-decoded-configuration-cfg_load','cfg_load',0,120),
           ('th03-op-decoded-configuration-cfg_save','cfg_save',120,67),
           ('th03-op-decoded-configuration-cfg_save_exit','cfg_save_exit',187,84))
PUBLICS=((0,'@cfg_load$qv'),(120,'@cfg_save$qv'),(187,'@cfg_save_exit$qv'),(271,'@story_menu$qv'),
 (661,'@VS_CHOICE_PUT$QIUI'),(727,'@vs_menu$qv'),(1092,'@start_demo$qv'),(1294,'@wait_for_input_or_start_demo_the$qv'),
 (1399,'@score_menu$qv'),(1493,'@MAIN_CHOICE_PUT$QIUI'),(1615,'@OPTION_CHOICE_PUT$QIUI'),
 (1945,'@MENU_SEL_UPDATE_AND_RENDER$QCC'),(2008,'@main_update_and_render$qv'),(2299,'@option_update_and_render$qv'),(2831,'_main'))
FIELDS=((265,4,0x56,None,26,0),(260,4,0x56,None,24,0),(229,2,0x16,2,15,0),
 (223,4,0x56,None,25,0),(213,4,0x56,None,23,0),(210,2,0x14,2,2,214),(204,4,0x56,None,47,0),(198,2,0x14,2,2,1),
 (181,4,0x56,None,26,0),(176,4,0x56,None,24,0),(145,2,0x16,2,15,0),(139,4,0x56,None,25,0),
 (129,4,0x56,None,23,0),(126,2,0x14,2,2,214),(102,2,0x16,2,15,0),(97,2,0x16,2,31,0),
 (84,2,0x14,2,2,0),(75,2,0x16,2,15,0),(68,2,0x16,2,31,0),(63,2,0x14,2,2,0),
 (57,4,0x56,None,32,0),(47,2,0x16,2,15,0),(41,2,0x16,2,15,0),(37,2,0x16,2,15,2),
 (26,4,0x56,None,26,0),(21,4,0x56,None,22,0),(9,4,0x56,None,21,0),(6,2,0x14,2,2,214))
EXTERNALS={15:('_resident',DATA_SEGMENT,0x2464),21:('FILE_ROPEN',0,0x9A8),22:('FILE_READ',0,0x8F4),
 23:('FILE_APPEND',0,0x7C8),24:('FILE_WRITE',0,0xA26),25:('FILE_SEEK',0,0x9E4),26:('FILE_CLOSE',0,0x888),
 31:('_snd_active',DATA_SEGMENT,0x5DC),32:('_snd_determine_mode',0xBEB,0x4A),47:('F_SCOPY@',0,0x337E)}


def need(value,message):
    if not value:raise ValueError('OP configuration layout: '+message)


def native_image(raw):
    records=parse_omf(raw);d=describe_omf(raw)
    need(d['valid'] and d['module_name']==WRAPPER and d['translator_comments']==['TC86 Borland C++ 4.02'],'native TC4 containing producer')
    need(d['record_counts']==dict(COMENT=88,EXTDEF=1,FIXUPP=4,GRPDEF=2,LEDATA=5,LNAMES=1,MODEND=1,PUBDEF=46,SEGDEF=3,THEADR=1),'complete containing record closure')
    need(segment_definitions(raw)==[dict(index=1,name='OP_01_TEXT',**{'class':'CODE'},overlay='',size=3094),
     dict(index=2,name='_DATA',**{'class':'DATA'},overlay='',size=487),dict(index=3,name='_BSS',**{'class':'BSS'},overlay='',size=6)],'complete containing CODE/DATA/BSS geometry')
    need([r.data[0] for r in records if r.name=='SEGDEF']==[0x28,0x48,0x48],'BYTE CODE / WORD DATA and BSS / USE16')
    need(code_publics(raw,1)==list(PUBLICS),'all fifteen containing CODE publics')
    code,blocks=code_bytes(raw,1)
    need([(b['offset'],b['size']) for b in blocks]==[(0,1024),(1024,1017),(2041,1023),(3064,30)],'complete native CODE record sequence')
    externals=[];names=[None]
    for rec in records:
        if rec.name not in ('EXTDEF','LNAMES'):continue
        at=0
        while at<len(rec.data):
            size=rec.data[at];at+=1;value=rec.data[at:at+size].decode('ascii');at+=size
            if rec.name=='LNAMES':names.append(value)
            else:externals.append(value);need(rec.data[at]==0,'untyped external');at+=1
    need(len(externals)==47 and all(externals[i-1]==name for i,(name,_,_) in EXTERNALS.items()),'literal scoped symbolic external identities')
    groups=[r.data for r in records if r.name=='GRPDEF']
    need([(names[g[0]],g[1:]) for g in groups]==[('GROUP_01',b'\xff\x01'),('DGROUP',b'\xff\x02\xff\x03')],'both real CODE/DATA group identities')
    image=bytearray(code[:271]);fields=[];block=None;data=None
    for rec in records:
        if rec.name=='LEDATA':
            block=(rec.data[0],int.from_bytes(rec.data[1:3],'little'))
            if block==(2,0):data=rec.data[3:]
        if rec.name!='FIXUPP' or block!=(1,0):continue
        at=0
        while at<len(rec.data):
            loc,low,fd=rec.data[at:at+3];at+=3
            need(fd in (0x14,0x16,0x56),'reviewed containing native fixup form')
            frame=None
            if fd in (0x14,0x16):frame=rec.data[at];at+=1
            target=rec.data[at];at+=1;site=(loc&3)*256+low;width=4 if loc>>2&15==3 else 2
            if site>=271:continue
            need(loc&0xC0==0xC0 and loc>>2&15 in (1,3) and site+width<=271,'whole scoped native field')
            addend=int.from_bytes(code[site:site+width],'little');fields.append((site,width,fd,frame,target,addend))
            if fd==0x14:
                need(width==2 and frame==2 and target==2,'own DATA offset frame');value=DATA_OFFSET+addend
                image[site:site+2]=value.to_bytes(2,'little')
            elif fd==0x16:
                need(width==2 and frame==2 and target in (15,31),'external DATA offset frame')
                image[site:site+2]=(EXTERNALS[target][2]+addend).to_bytes(2,'little')
            else:
                need(width==4 and target in EXTERNALS and code[site-1]==0x9A,'actual far service pointer')
                _,seg,off=EXTERNALS[target];image[site:site+4]=(off+addend).to_bytes(2,'little')+seg.to_bytes(2,'little')
    need(tuple(fields)==FIELDS,'all twenty-eight literal ordered scoped fields')
    need(data is not None and len(data)==487 and data[:9]==bytes(9) and data[214:223]==b'YUME.CFG\0','reviewed boolean, zero template and filename dependencies')
    return bytes(image),data,fields


def verify(work,target,candidate):
    raw=(work/OBJECT).read_bytes();image,data,fields=native_image(raw);deps=[n.replace(chr(92),'/') for n in describe_omf(raw)['dependency_paths']]
    need(SOURCE in deps and WRAPPER in deps and (work/WRAPPER).read_text()=='#include "'+SOURCE+'"\n','actual current maintained containing source')
    text=(work/'obj/th03/op.map').read_text().replace(chr(92),'/')
    for seg,off,size,cls,name,group,attr in ((SEGMENT,OFFSET,3094,'CODE','OP_01_TEXT','GROUP_01',0x28),
        (DATA_SEGMENT,DATA_OFFSET,487,'DATA','_DATA','DGROUP',0x48),(DATA_SEGMENT,0x118A,6,'BSS','_BSS','DGROUP',0x48)):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G={group}\s+M=th03/op_01\.cpp\s+ACBP={attr:02X}\s*$',text))==1,'complete literal containing MAP geometry')
    for name,seg,off in EXTERNALS.values():
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,'both scoped external MAP tables: '+name)
    start=SEGMENT*16+OFFSET;end=start+271;data_start=DATA_SEGMENT*16+DATA_OFFSET
    need(image==target.program_image[start:end]==candidate.program_image[start:end],'all complete CFG instruction bytes')
    need(data==target.program_image[data_start:data_start+487]==candidate.program_image[data_start:data_start+487],'complete containing initialized DATA equality, not ownership credit')
    pairs=[[SEGMENT,OFFSET+site+2] for site,width,_,_,_,_ in FIELDS if width==4]
    for mz in (target,candidate):
        need(not any(r.linear<end and r.linear+2>start and not start<=r.linear<=end-2 for r in mz.relocations),'whole relocation fields')
        need([[r.segment,r.offset] for r in mz.relocations if start<=r.linear<end]==pairs,'all thirteen literal ordered MZ pairs')
    owners=[]
    for unit,name,offset,size in FUNCTIONS:
        need(len(re.findall(rf'(?m)^\s*0990:{OFFSET+offset:04X}\s+(?:idle\s+)?{name}\(\)\s*$',text))==2,'both whole near function MAP publics')
        digest=hashlib.sha256(image[offset:offset+size]).hexdigest();address=start+offset
        owners.append(dict(unit_id=unit,name=name,source=SOURCE,object=OBJECT,segment=SEGMENT,offset=OFFSET+offset,start=address,size=size,
            coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=digest,candidate_sha256=digest,
            ordered_relocations=[pair for pair in pairs if address<=pair[0]*16+pair[1]<address+size],
            abi='near cdecl; no arguments; SS local eight-byte packed cfg; RET',private_data_bytes=0,private_bss_bytes=0))
    return dict(owners=owners,functions=3,code_bytes=271,ordered_native_fields=[dict(offset=s,width=w,fixdat=fd,frame=f,target=t,addend=a) for s,w,fd,f,t,a in fields],
        ordered_relocations=pairs,reviewed_initialized_dependency_bytes=18,
        data_dependencies=dict(disabled_flag=[0x90,1],zero_initializer=[0x91,8],filename=[0x166,9]),
        containing_code_bytes=3094,containing_data_bytes=487,containing_bss_bytes=6,
        containing_producer_accepted=False,whole_product_accepted=False)
