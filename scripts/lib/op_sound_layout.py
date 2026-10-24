"""Complete OP load and frame-delay producers; independent OP link addresses."""
import hashlib,re
from lib.omf import describe_omf,parse_omf
from lib.decoded_mainl_sound_layout import FIELDS
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes,code_publics
CS=0xBEB;DS=0xD7F
FIELDS_GLOBAL={'_snd_midi_active':0x1A0B,'_snd_load_fn':0x1A0E,'_vsync_Count1':0x11E8}
RUNTIME_FIELDS=dict(midi_active=0x1A0B,load_fn=0x1A0E,counter=0x11E8)
PRODUCERS=(('th03-op-decoded-snd-load','load','src/shared/sound/load.cpp','th02/snd_load.cpp','obj/th02/snd_load.obj','_snd_load','_snd_load',0xA2,112,6,0),
 ('th03-op-decoded-input-frame-delay','frame_delay','src/shared/hardware/frame_delay.cpp','th02/frmdely1.cpp','obj/th02/frmdely1.obj','@FRAME_DELAY$QI','frame_delay(int)',0x2EE,21,2,2))
ENTRIES={kind:(CS*16+off,size,args,pop) for _,kind,_,_,_,_,_,off,size,args,pop in PRODUCERS}
def need(v,m):
    if not v:raise ValueError('OP shared sound layout: '+m)
def native_image(raw,obj):
    code,_=code_bytes(raw,1);im=bytearray(code);fields=[];names=[];block=None
    for r in parse_omf(raw):
        if r.name=='EXTDEF':
            at=0
            while at<len(r.data):
                n=r.data[at];at+=1;names.append(r.data[at:at+n].decode());at+=n+1
        if r.name=='LEDATA':block=(r.data[0],int.from_bytes(r.data[1:3],'little'))
        if r.name!='FIXUPP':continue
        need(block[0]==1,'all fields in complete CODE');at=0
        while at<len(r.data):
            loc,low,fd,frame,target=r.data[at:at+5];at+=5;s=block[1]+(loc&3)*256+low
            need((loc,fd,frame)==(0xC4,0x16,1) and s+2<=len(code),'literal WORD/group/external field')
            value=int.from_bytes(code[s:s+2],'little');name=names[target-1];need(name in FIELDS_GLOBAL,'reviewed OP global')
            fields.append((s,target,value));im[s:s+2]=(FIELDS_GLOBAL[name]+value).to_bytes(2,'little')
    need(tuple(fields)==FIELDS[obj] and tuple(names)==(('_snd_midi_active','_snd_load_fn') if 'snd_load' in obj else ('_vsync_Count1',)),'all ten literal ordered fields and external identities')
    return bytes(im),[dict(offset=s,width=2,fixdat=0x16,frame=1,target=t,name=names[t-1],addend=a) for s,t,a in fields]
def verify(work,target,candidate):
    text=(work/'obj/th03/op.map').read_text();owners=[];native=[]
    for unit,kind,source,wrapper,obj,symbol,mapname,off,size,args,pop in PRODUCERS:
        raw=(work/obj).read_bytes();d=describe_omf(raw);need(d['valid'] and d['translator_comments']==['TC86 Borland C++ 4.02'],'native TC4 OMF')
        need(segment_definitions(raw)==[dict(index=1,name='SHARED',**{'class':'CODE'},overlay='',size=size),dict(index=2,name='_DATA',**{'class':'DATA'},overlay='',size=0),dict(index=3,name='_BSS',**{'class':'BSS'},overlay='',size=0)],'complete CODE and zero private DATA/BSS')
        need([r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF']==[0x28,0x48,0x48] and [b['size'] for b in code_bytes(raw,1)[1]]==[size] and code_publics(raw,1)==[(0,symbol)],'native alignment/record/public ownership')
        deps=[n.replace(chr(92),'/') for n in d['dependency_paths']];need(source in deps and wrapper in deps,'actual maintained source consumption')
        need(len(re.findall(rf'(?m)^\s*0BEB:{off:04X}\s+{size:04X}\s+C=CODE\s+S=SHARED\s+G=\(none\)\s+M={re.escape(wrapper)}\s+ACBP=28\s*$',text))==1,'literal complete MAP allocation')
        need(len(re.findall(rf'(?m)^\s*0BEB:{off:04X}\s+(?:idle\s+)?{re.escape(mapname)}\s*$',text))==2,'both complete MAP public tables')
        im,fields=native_image(raw,obj);start=CS*16+off;end=start+size
        need(im==target.program_image[start:end]==candidate.program_image[start:end],'complete independently resolved OP code bytes')
        for image in (target,candidate):need(not any(r.linear<end and r.linear+2>start for r in image.relocations),'empty complete ordered MZ relocation vector')
        h=hashlib.sha256(im).hexdigest();owners.append(dict(unit_id=unit,name=symbol,source=source,object=obj,segment=CS,offset=off,start=start,size=size,
            coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=h,candidate_sha256=h,ordered_relocations=[],argument_bytes=args,callee_pop_bytes=pop,
            private_data_bytes=0,private_bss_bytes=0,abi='far '+('Pascal' if pop else 'cdecl')+'; WORD arguments; DS restore and finite counter-update contract'))
        native.append(dict(object=obj,fields=fields,record_sizes=[size]))
    for name,off in FIELDS_GLOBAL.items():need(len(re.findall(rf'(?m)^\s*0D7F:{off:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,'both OP external DATA MAP tables')
    return dict(owners=owners,functions=2,code_bytes=133,native_objects=native,ordered_relocations=[],private_data_bytes=0,private_bss_bytes=0,whole_product_accepted=False)
