"""Complete MAINL sound and frame-delay producers, without adjacent padding."""
import hashlib,re
from pathlib import Path
from lib.omf import describe_omf,parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes,code_publics

CS=0xC7E;DS=0xE3F
# object, wrapper, maintained source, first-use GAME/BINARY/parent, load offset,
# complete object bytes, and every public procedure (unit suffix/name/off/size/args/pop).
PRODUCERS=(
 ('obj/th02/snd_load.obj','th02/snd_load.cpp','src/shared/sound/load.cpp',2,'O','op',0xA0,112,
  (('sound-load','_snd_load',0,112,6,0),)),
 ('obj/th02/frmdely1.obj','th02/frmdely1.cpp','src/shared/hardware/frame_delay.cpp',2,'O','op',0x372,21,
  (('linked-tail-delay','@FRAME_DELAY$QI',0,21,2,2),)),
 ('obj/th03/snd_se.obj','th03/snd_se.cpp','src/mainl/linked_game/sound_se.cpp',3,'M','main',0x66A,120,
  (('sound-play','SND_SE_PLAY',0,60,2,2),('sound-update','_snd_se_update',60,60,0,0))),
 ('obj/th03/snd_kaja.obj','th03/snd_kaja.cpp','src/mainl/linked_game/sound_kaja.cpp',3,'O','op',0x6E2,30,
  (('sound-kaja','SND_KAJA_INTERRUPT',0,30,2,2),)),
 ('obj/th03/snd_dlym.obj','th03/snd_dlym.cpp','src/mainl/linked_game/sound_measure.cpp',3,'L','mainl',0xC1C,49,
  (('sound-measure','SND_DELAY_UNTIL_MEASURE',0,49,4,4),)))
MAP_NAMES={'_snd_load':'_snd_load','@FRAME_DELAY$QI':'frame_delay(int)','SND_SE_PLAY':'SND_SE_PLAY',
 'SND_KAJA_INTERRUPT':'SND_KAJA_INTERRUPT','SND_DELAY_UNTIL_MEASURE':'SND_DELAY_UNTIL_MEASURE',
 '_snd_se_update':'_snd_se_update'}
GLOBALS={'_snd_active':0x880,'_snd_se_playing':0x88C,'_snd_se_frame':0x88D,
 '_snd_se_priorities':0x896,'_snd_se_priority_frames':0x8B7,'_vsync_Count1':0x144E,
 '_snd_fm_possible':0x1C70,'_snd_midi_active':0x1C71,'_snd_load_fn':0x1C74}
FIELDS={
 'obj/th02/snd_load.obj':((85,1,0),(66,2,0),(62,2,2),(57,2,1),(52,2,0),(45,2,0),(35,1,0),(20,2,0)),
 'obj/th02/frmdely1.obj':((10,1,0),(5,1,0)),
 'obj/th03/snd_se.obj':((116,1,0),(111,4,0),(105,4,0),(101,3,0),(93,1,0),(90,4,0),(84,1,0),(76,4,0),(69,1,0),(62,5,0),
  (53,4,0),(49,1,0),(43,2,0),(37,2,0),(29,1,0),(22,1,0),(15,1,0),(8,5,0)),
 'obj/th03/snd_kaja.obj':((15,2,0),(5,1,0)),
 'obj/th03/snd_dlym.obj':((26,3,0),(14,1,0),(5,2,0))}
EXTERNALS={
 'obj/th02/snd_load.obj':('_snd_midi_active','_snd_load_fn'),
 'obj/th02/frmdely1.obj':('_vsync_Count1',),
 'obj/th03/snd_se.obj':('_snd_se_playing','_snd_se_priorities','_snd_se_priority_frames','_snd_se_frame','_snd_fm_possible'),
 'obj/th03/snd_kaja.obj':('_snd_active','_snd_midi_active'),
 'obj/th03/snd_dlym.obj':('@FRAME_DELAY$QI','_snd_active','_snd_midi_active')}
DEPENDENCIES=((0x880,1,'6e340b9cffb37a989ca544e6bb780a2c78901d3fb33738768511a30617afa01d'),
 (0x88C,2,'ea5dbf9596d187e9500f23e9a680109475341cf4e81f7e043f7d97152c10772f'),
 (0x896,66,'d09b562db9fa5c13ee1faf576e792014ee88a7f8ec1709e2220a30d2442aabc8'))

def need(v,m):
    if not v:raise ValueError('MAINL sound layout: '+m)
def native_image(raw,obj,offset):
    code,_=code_bytes(raw,1);im=bytearray(code);names=[];block=None;fields=[];report=[]
    for r in parse_omf(raw):
        if r.name=='EXTDEF':
            at=0
            while at<len(r.data):
                n=r.data[at];at+=1;names.append(r.data[at:at+n].decode());at+=n+1
        if r.name=='LEDATA':block=(r.data[0],int.from_bytes(r.data[1:3],'little'))
        if r.name!='FIXUPP':continue
        need(block[0]==1,'all native fields belong to complete CODE');at=0
        while at<len(r.data):
            loc,low,fd=r.data[at:at+3];at+=3;frame=None
            if fd==0x16:frame=r.data[at];at+=1
            need(fd in (0x16,0x56),'literal native fixup form');target=r.data[at];at+=1;s=block[1]+(loc&3)*256+low
            relaxed=obj=='obj/th03/snd_dlym.obj' and s==14;width=4 if relaxed else 2
            need(loc==(0xCC if relaxed else 0xC4) and fd==(0x56 if relaxed else 0x16) and frame==(None if relaxed else 1),'literal width/frame/method')
            need(s+width<=len(code),'whole field');addend=int.from_bytes(code[s:s+width],'little');fields.append((s,target,addend))
            name=names[target-1]
            if relaxed:
                need(name=='@FRAME_DELAY$QI' and code[s-1:s+4]==b'\x9A\0\0\0\0','genuine same-CS far call before relaxation')
                displacement=(0x372-(offset+s+4))&65535
                im[s-1:s+4]=b'\x90\x0E\xE8'+displacement.to_bytes(2,'little')
            else:
                need(name in GLOBALS,'reviewed external DATA name');im[s:s+2]=(GLOBALS[name]+addend).to_bytes(2,'little')
            report.append(dict(offset=s,width=width,locat=loc,fixdat=fd,frame=frame,target=target,name=name,addend=addend,normal_tlink_relaxed_far_call=relaxed))
    need(tuple(names)==EXTERNALS[obj] and tuple(fields)==FIELDS[obj],'complete ordered literal native fields and names')
    return bytes(im),report
def verify(work,target,candidate,graph,files):
    root=Path(__file__).resolve().parents[2];text=(work/'obj/th03/mainl.map').read_text().replace(chr(92),'/');owners=[];native=[]
    for obj,wrapper,source,game,binary,first,offset,size,procedures in PRODUCERS:
        raw=(work/obj).read_bytes();d=describe_omf(raw);need(d['valid'] and d['translator_comments']==['TC86 Borland C++ 4.02'],'native complete TC4 OMF')
        need(segment_definitions(raw)==[dict(index=1,name='SHARED',**{'class':'CODE'},overlay='',size=size),
             dict(index=2,name='_DATA',**{'class':'DATA'},overlay='',size=0),dict(index=3,name='_BSS',**{'class':'BSS'},overlay='',size=0)],'complete CODE, zero private DATA/BSS')
        need([r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF']==[0x28,0x48,0x48],'BYTE/PUBLIC/USE16 CODE and WORD DATA/BSS')
        need([b['size'] for b in code_bytes(raw,1)[1]]==[size] and code_publics(raw,1)==[(a,n) for _,n,a,*_ in procedures],'complete record and public inventory')
        deps=[n.replace(chr(92),'/') for n in d['dependency_paths']];need(wrapper in deps and source in deps,'actual consumed source/wrapper')
        row,=[r for r in graph if r['output']==obj]
        need((row['wrapper'],row['source'],row['game'],row['binary'],row['first_binary'])==(wrapper,source,game,binary,first),'actual first-use producer slot')
        need(files[source]==(work/source).read_bytes() and files[source].replace(b'\r\n',b'\n')==(root/source).read_bytes().replace(b'\r\n',b'\n'),'current maintained source transport')
        need(len(re.findall(rf'(?m)^\s*0C7E:{offset:04X}\s+{size:04X}\s+C=CODE\s+S=SHARED\s+G=\(none\)\s+M={re.escape(wrapper)}\s+ACBP=28\s*$',text))==1,'literal complete MAP allocation')
        im,fields=native_image(raw,obj,offset);need(im==target.program_image[CS*16+offset:CS*16+offset+size]==candidate.program_image[CS*16+offset:CS*16+offset+size],'whole native resolved object equality')
        native.append(dict(object=obj,fields=fields,record_sizes=[size],private_data_bytes=0,private_bss_bytes=0))
        for suffix,name,a,s,args,pop in procedures:
            start=CS*16+offset+a;end=start+s;body=im[a:a+s]
            need(len(re.findall(rf'(?m)^\s*0C7E:{offset+a:04X}\s+{re.escape(MAP_NAMES[name])}\s*$',text))==2,'both literal owner MAP publics: '+name)
            for image in (target,candidate):need(not any(r.linear<end and r.linear+2>start for r in image.relocations),'empty complete ordered MZ relocation vector')
            h=hashlib.sha256(body).hexdigest();owners.append(dict(unit_id='th03-mainl-decoded-'+suffix,name=name,source=source,object=obj,start=start,size=s,
                segment=CS,offset=offset+a,coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=h,candidate_sha256=h,ordered_relocations=[],
                argument_bytes=args,callee_pop_bytes=pop,private_data_bytes=0,private_bss_bytes=0,
                producer_slot=dict(wrapper=wrapper,game=game,binary=binary,first_binary=first),abi='far '+('Pascal' if pop else 'cdecl')+'; WORD arguments; native BYTE sound fields and WORD IRQ counter'))
    for name,offset in GLOBALS.items():need(len(re.findall(rf'(?m)^\s*0E3F:{offset:04X}\s+{re.escape(name)}\s*$',text))==2,'both external DATA MAP tables: '+name)
    for offset,size,h in DEPENDENCIES:
        need(all(hashlib.sha256(im.program_image[DS*16+offset:DS*16+offset+size]).hexdigest()==h for im in (target,candidate)),'complete initialized external sound dependency')
    need(sum(len(n['fields']) for n in native)==33 and sum(o['size'] for o in owners)==332,'complete six-function ownership')
    return dict(owners=owners,functions=6,code_bytes=332,native_objects=native,ordered_relocations=[],normal_tlink_relaxed_calls=1,
        private_data_bytes=0,private_bss_bytes=0,reviewed_initialized_dependency_bytes=69,
        initialized_dependencies=[dict(offset=o,size=s,sha256=h) for o,s,h in DEPENDENCIES],
        external_mutable_storage=dict(filename_buffer_bytes=13,priority_entries=33,duration_entries=33,IRQ_counter_bytes=2),
        adjacent_explicit_padding_accepted=False,whole_product_accepted=False)
