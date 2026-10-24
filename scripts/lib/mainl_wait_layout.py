"""Whole native ending-wait producer: two far Pascal procedures, 126 bytes."""
import hashlib
import re

from lib.omf import describe_omf,parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes,code_publics

SOURCE='src/mainl/hardware/input_wait.cpp'
WRAPPER='th03/inp_wait.cpp'
OBJECT='obj/th03/inp_wait.obj'
CODE_SEGMENT,DATA_SEGMENT,OFFSET=0xC7E,0xE3F,0xC4D
COUNTER,ACTIVE,MIDI,SINGLE,INTERFACE=0x144E,0x880,0x1C71,0x1D0C,0xDC2
FUNCTIONS=(('th03-mainl-decoded-input-measure-wait','input_wait_for_ok_or_measure',0,77,4),
           ('th03-mainl-decoded-input-ok-wait','input_wait_for_ok',77,49,2))
EXTERNALS=('_vsync_Count1','_input_sp','@INPUT_MODE_INTERFACE$QV','_snd_active','_snd_midi_active')
FIELDS=((113,2,0x16,1,0),(100,2,0x16,2,1),(93,2,0x16,2,0),(87,4,0x56,3,0),
        (82,2,0x16,1,0),(54,2,0x16,2,1),(47,2,0x16,2,0),(41,4,0x56,3,0),
        (26,2,0x16,5,0),(14,4,0x54,1,77),(5,2,0x16,4,0))


def need(value,message):
    if not value:raise ValueError('MAINL wait layout: '+message)


def native_image(raw):
    records=parse_omf(raw);description=describe_omf(raw)
    need(description['valid'] and description['module_name']==WRAPPER
         and description['translator_comments']==['TC86 Borland C++ 4.02'],'native TC4 producer')
    need(description['record_counts']==dict(COMENT=25,EXTDEF=1,FIXUPP=1,GRPDEF=1,LEDATA=1,LNAMES=1,
         MODEND=1,PUBDEF=2,SEGDEF=3,THEADR=1) and records[-1].data==b'\0','complete native record closure')
    need(segment_definitions(raw)==[dict(index=1,name='SHARED',**{'class':'CODE'},overlay='',size=126),
        dict(index=2,name='_DATA',**{'class':'DATA'},overlay='',size=0),
        dict(index=3,name='_BSS',**{'class':'BSS'},overlay='',size=0)],'whole CODE with zero private DATA/BSS')
    need([r.data[0] for r in records if r.name=='SEGDEF']==[0x28,0x48,0x48],'BYTE CODE / WORD DATA and BSS / USE16')
    names=[None];externals=[]
    for rec in records:
        if rec.name not in ('LNAMES','EXTDEF'):continue
        at=0
        while at<len(rec.data):
            n=rec.data[at];at+=1;name=rec.data[at:at+n].decode('ascii');at+=n
            if rec.name=='LNAMES':names.append(name)
            else:
                externals.append(name);need(rec.data[at]==0,'untyped external');at+=1
    need(tuple(externals)==EXTERNALS,'complete symbolic external order')
    group,=[r.data for r in records if r.name=='GRPDEF']
    need(names[group[0]]=='DGROUP' and group[1:]==b'\xff\x02\xff\x03','actual DATA/BSS group')
    need(code_publics(raw,1)==[(0,'@INPUT_WAIT_FOR_OK_OR_MEASURE$QIUI'),(77,'@INPUT_WAIT_FOR_OK$QUI')],'both whole OMF publics')
    body,blocks=code_bytes(raw,1);need(len(body)==126 and [(b['offset'],b['size']) for b in blocks]==[(0,126)],'single full native CODE record')
    image=bytearray(body);fields=[];relaxed=[]
    for rec in records:
        if rec.name!='FIXUPP':continue
        at=0
        while at<len(rec.data):
            loc,lo,fd=rec.data[at:at+3];at+=3
            need(loc&0xC0==0xC0 and loc>>2&15 in (1,3) and fd in (0x16,0x56,0x54),'literal native WORD/far field')
            if fd==0x16:need(rec.data[at]==1,'DGROUP frame');at+=1
            target=rec.data[at];at+=1;site=(loc&3)*256+lo;width=2 if loc>>2&15==1 else 4
            need(site+width<=126,'whole native field');addend=int.from_bytes(body[site:site+width],'little')
            fields.append((site,width,fd,target,addend))
            if width==2:
                need(fd==0x16 and target in (1,2,4,5),'DGROUP external WORD')
                value={1:COUNTER,2:SINGLE,4:ACTIVE,5:MIDI}[target]+addend
                image[site:site+2]=value.to_bytes(2,'little')
            else:
                need(body[site-1]==0x9A and ((fd==0x54 and target==1) or (fd==0x56 and target==3)),'real same-CS far call')
                offset=OFFSET+addend if fd==0x54 else INTERFACE
                image[site-1:site+4]=b'\x90\x0E\xE8'+((offset-(OFFSET+site+4))&65535).to_bytes(2,'little');relaxed.append(site-1)
    need(tuple(fields)==FIELDS,'all eleven ordered fields and their real addends')
    return bytes(image),fields,relaxed


def verify(work,target,candidate):
    raw=(work/OBJECT).read_bytes();image,fields,relaxed=native_image(raw);description=describe_omf(raw)
    deps=[n.replace(chr(92),'/') for n in description['dependency_paths']]
    need(SOURCE in deps and WRAPPER in deps,'actual maintained source dependency')
    need((work/WRAPPER).read_text()=='#include "'+SOURCE+'"\n','actual full wrapper')
    text=(work/'obj/th03/mainl.map').read_text().replace(chr(92),'/')
    for seg,off,size,cls,name,group,attr in ((CODE_SEGMENT,OFFSET,126,'CODE','SHARED',r'\(none\)',0x28),
        (DATA_SEGMENT,0x906,0,'DATA','_DATA','DGROUP',0x48),(DATA_SEGMENT,0x27EA,0,'BSS','_BSS','DGROUP',0x48)):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G={group}\s+M=th03/inp_wait\.cpp\s+ACBP={attr:02X}\s*$',text))==1,'complete literal MAP producer')
    for name,off in (('_vsync_Count1',COUNTER),('_input_sp',SINGLE),('_snd_active',ACTIVE),('_snd_midi_active',MIDI)):
        need(len(re.findall(rf'(?m)^\s*0E3F:{off:04X}\s+(?:idle\s+)?{name}\s*$',text))==2,'both external MAP tables: '+name)
    need(len(re.findall(r'(?m)^\s*0C7E:0DC2\s+input_mode_interface\(\)\s*$',text))==2,'owned nested interface in both MAP tables')
    start=CODE_SEGMENT*16+OFFSET;end=start+126
    need(image==target.program_image[start:end]==candidate.program_image[start:end],'full natural native target equality')
    need(not any(start-1<=r.linear<end for mz in (target,candidate) for r in mz.relocations),'no retained MZ relocation inside or straddling the producer')
    owners=[]
    for unit,name,offset,size,args in FUNCTIONS:
        signature=r'int,unsigned int' if offset==0 else r'unsigned int'
        need(len(re.findall(rf'(?m)^\s*0C7E:{OFFSET+offset:04X}\s+{name}\({signature}\)\s*$',text))==2,'both complete function MAP publics')
        digest=hashlib.sha256(image[offset:offset+size]).hexdigest()
        owners.append(dict(unit_id=unit,name=name,source=SOURCE,object=OBJECT,start=start+offset,size=size,
            coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=digest,candidate_sha256=digest,
            ordered_relocations=[],private_data_bytes=0,private_bss_bytes=0,argument_bytes=args,callee_pop_bytes=args,
            abi='far Pascal; WORD frames at BP+6; '+('WORD measure at BP+8; RETF 4' if offset==0 else 'RETF 2')))
    return dict(owners=owners,functions=2,code_bytes=126,private_data_bytes=0,private_bss_bytes=0,
                ordered_native_fields=[dict(offset=s,width=w,fixdat=fd,target=t,addend=a) for s,w,fd,t,a in fields],
                normal_tlink_relaxed_calls=relaxed,ordered_relocations=[],whole_product_accepted=False)
