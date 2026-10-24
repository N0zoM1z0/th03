"""Three complete OP helper producers, with their own native link fields."""
import hashlib,re
from lib.omf import describe_omf,parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes,code_publics
CS=0xBEB;DS=0xD7F
PRODUCERS=(
 ('th03-op-decoded-input-frame-delay-2','frame_delay','src/op/hardware/frame_delay_2.cpp','th02/frmdely2.cpp','obj/th02/frmdely2.obj','@FRAME_DELAY_2$QI','frame_delay_2(int)',0xCD6,21,2,2),
 ('th03-op-decoded-snd-kaja-interrupt','kaja','src/op/snd/kaja_interrupt.cpp','th03/snd_kaja.cpp','obj/th03/snd_kaja.obj','SND_KAJA_INTERRUPT','SND_KAJA_INTERRUPT',0x553,30,2,2),
 ('th03-op-decoded-configuration-init','init','src/op/core/initop.cpp','th03/initop.cpp','obj/th03/initop.obj','@game_init_op$qnxuc','game_init_op(const unsigned char far*)',0x571,105,4,0))
SOUND_ENTRIES={kind:(CS*16+off,size,args,pop) for _,kind,_,_,_,_,_,off,size,args,pop in PRODUCERS if kind!='init'}
SOUND_FIELDS=dict(active=0x5DC,midi_active=0x1A0B,counter=0x11E8)
FORWARDING={
 'obj/th03/snd_kaja.obj':('th03/snd_kaja.cpp','th02/snd/kajaint.cpp','src/op/snd/kaja_interrupt.cpp'),
 'obj/th03/initop.obj':('th03/initop.cpp','th03/core/initop.cpp','src/op/core/initop.cpp')}
# EXTDEF order is checked separately from both independently ordered MAP tables.
EXTERNALS={
 'frame_delay':(('_vsync_Count1',DS,0x11E8,'_vsync_Count1'),),
 'kaja':(('_snd_active',DS,0x5DC,'_snd_active'),('_snd_midi_active',DS,0x1A0B,'_snd_midi_active')),
 'init':(('JS_START',0,0x2DB8,'JS_START'),('KEY_BEEP_OFF',0,0x1A22,'KEY_BEEP_OFF'),
 ('MEM_ASSIGN_DOS',0,0x245A,'MEM_ASSIGN_DOS'),('PFSTART',0,0x2B60,'PFSTART'),
 ('VSYNC_START',0,0x22CA,'VSYNC_START'),('EGC_START',0,0x708,'EGC_START'),
 ('GRAPH_CLEAR',0,0x114C,'GRAPH_CLEAR'),('GRAPH_START',0,0x19F6,'GRAPH_START'),
 ('TEXT_CURSOR_HIDE',0,0x2226,'TEXT_CURSOR_HIDE'),('TEXT_SYSTEMLINE_HIDE',0,0x2232,'TEXT_SYSTEMLINE_HIDE'),
 ('@vram_planes_set$qv',CS,0x21,'vram_planes_set()'))}
FIELDS={'frame_delay':((10,1,0),(5,1,0)),'kaja':((15,2,0),(5,1,0)),
 'init':((97,4,0),(88,1,0),(83,6,0),(78,9,0),(73,10,0),(68,2,0),(63,5,0),(48,7,0),(37,7,0),(26,8,0),(21,11,0),(7,3,0))}
def need(v,m):
    if not v:raise ValueError('OP helper layout: '+m)
def native_image(raw,kind,off):
    code,_=code_bytes(raw,1);im=bytearray(code);names=[];block=None;fields=[];report=[]
    for r in parse_omf(raw):
        if r.name=='EXTDEF':
            at=0
            while at<len(r.data):
                n=r.data[at];at+=1;names.append(r.data[at:at+n].decode());at+=n+1
        elif r.name=='LEDATA':block=(r.data[0],int.from_bytes(r.data[1:3],'little'))
        elif r.name=='FIXUPP':
            need(block[0]==1,'complete CODE fields');at=0
            while at<len(r.data):
                loc,low,fd=r.data[at:at+3];at+=3;s=block[1]+(loc&3)*256+low
                if kind=='init':
                    target=r.data[at];at+=1;need((loc,fd)==(0xCC,0x56),'literal absolute far-pointer field');width=4;frame=None
                else:
                    frame,target=r.data[at:at+2];at+=2;need((loc,fd,frame)==(0xC4,0x16,1),'literal DGROUP WORD field');width=2
                addend=int.from_bytes(code[s:s+width],'little');fields.append((s,target,addend));name,seg,value,_=EXTERNALS[kind][target-1]
                need(names[target-1]==name,'literal external identity')
                relaxed=kind=='init' and target==11
                if relaxed:
                    need(code[s-1]==0x9A,'original far CALL for genuine TLINK relaxation')
                    im[s-1:s+4]=b'\x90\x0E\xE8'+((value-(off+s+4))&65535).to_bytes(2,'little')
                else:im[s:s+width]=(value if width==2 else seg*65536+value).to_bytes(width,'little')
                report.append(dict(offset=s,locat=loc,fixdat=fd,frame=frame,target=target,name=name,addend=addend,width=width,normal_tlink_relaxation=relaxed))
    need(tuple(names)==tuple(e[0] for e in EXTERNALS[kind]) and tuple(fields)==FIELDS[kind],'all sixteen ordered native fields and external names')
    return bytes(im),report

def verify(work,target,candidate):
    text=(work/'obj/th03/op.map').read_text();owners=[];native=[]
    for unit,kind,source,wrapper,obj,symbol,mapname,off,size,args,pop in PRODUCERS:
        raw=(work/obj).read_bytes();d=describe_omf(raw);need(d['valid'] and d['translator_comments']==['TC86 Borland C++ 4.02'],'native TC4 producer')
        need(segment_definitions(raw)==[dict(index=1,name='SHARED',**{'class':'CODE'},overlay='',size=size),dict(index=2,name='_DATA',**{'class':'DATA'},overlay='',size=0),dict(index=3,name='_BSS',**{'class':'BSS'},overlay='',size=0)],'whole natural CODE and zero private DATA/BSS')
        need([r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF']==[0x28,0x48,0x48] and [b['size'] for b in code_bytes(raw,1)[1]]==[size] and code_publics(raw,1)==[(0,symbol)],'BYTE/PUBLIC/USE16 CODE, one complete record and public')
        deps=[n.replace(chr(92),'/') for n in d['dependency_paths']];need(source in deps and wrapper in deps,'actual source and wrapper consumption')
        chain=FORWARDING.get(obj,(wrapper,source))
        need(all(n in deps for n in chain),'every actual source forwarding layer in native dependencies')
        for parent,child in zip(chain,chain[1:]):
            need((work/parent).read_bytes()==('#include \"'+child+'\"\n').encode(),'literal maintained forwarding layer: '+parent)
        need(len(re.findall(rf'(?m)^\s*0BEB:{off:04X}\s+{size:04X}\s+C=CODE\s+S=SHARED\s+G=\(none\)\s+M={re.escape(wrapper)}\s+ACBP=28\s*$',text))==1,'literal MAP allocation')
        for seg,value,name in ((CS,off,mapname),*((e[1],e[2],e[3]) for e in EXTERNALS[kind])):
            need(len(re.findall(rf'(?m)^\s*{seg:04X}:{value:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,'both MAP public tables: '+name)
        im,fields=native_image(raw,kind,off);start=CS*16+off;end=start+size
        need(im==target.program_image[start:end]==candidate.program_image[start:end],'complete independently resolved native bytes')
        ordered=[[CS,off+s+2] for s,t,_ in FIELDS[kind] if kind=='init' and t!=11]
        for image in (target,candidate):
            need(not any(r.linear<end and r.linear+2>start and not start<=r.linear<=end-2 for r in image.relocations),'no straddling relocation')
            need([[r.segment,r.offset] for r in image.relocations if start<=r.linear<end]==ordered,'complete literal ordered relocation vector')
        h=hashlib.sha256(im).hexdigest();owners.append(dict(unit_id=unit,name=symbol,source=source,object=obj,segment=CS,offset=off,start=start,size=size,
            coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=h,candidate_sha256=h,ordered_relocations=ordered,forwarding_chain=list(chain),
            argument_bytes=args,callee_pop_bytes=pop,private_data_bytes=0,private_bss_bytes=0,abi='far '+('Pascal' if pop else 'cdecl')+('; far filename pointer' if kind=='init' else '; WORD argument and external BYTE/WORD state')))
        native.append(dict(object=obj,ordered_fields=fields,record_sizes=[size]))
    return dict(owners=owners,functions=3,code_bytes=156,native_objects=native,normal_tlink_relaxed_calls=1,ordered_relocations=[r for o in owners for r in o['ordered_relocations']],private_data_bytes=0,private_bss_bytes=0,whole_product_accepted=False)
