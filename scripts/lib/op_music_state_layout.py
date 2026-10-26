"""The complete216-byte state/track prefix of the natural OP_MUSIC producer."""
import hashlib
import re
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.omf import parse_omf,describe_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes,code_publics

SOURCE='src/op/music/state_and_tracks.inl'
WRAPPER='th03/op_music.cpp'
OBJECT='obj/th03/op_music.obj'
CS,DS,OFFSET,DATA,BSS=0x990,0xD7F,0xC1E,0x5F2,0x1F70
START,SIZE=CS*16+OFFSET,216
UNIT='th03-op-decoded-music-state-and-tracks'
PROCEDURES=(('track_put_both',0,114,4),('tracklist_put_both',114,39,2),
    ('nopoly_B_snap',153,49,0),('nopoly_B_free',202,14,0))
PUBLICS=((0,'@TRACK_PUT_BOTH$QUCUC'),(114,'@TRACKLIST_PUT_BOTH$QUC'),
    (153,'@nopoly_B_snap$qv'),(202,'@nopoly_B_free$qv'),(216,'@nopoly_B_put$qv'),
    (246,'@POLYGON_BUILD$QP14SCREEN_POINT_TI22SPACE_CHANGING_PIXEL_TIIUC'),
    (389,'@polygons_update_and_render$qv'),(891,'@music_update_render_and_flip$qv'),
    (945,'@cmt_bg_snap$qv'),(1260,'@CMT_LOAD$QI'),(1333,'@cmt_bg_free$qv'),
    (1374,'@cmt_unput$qv'),(1659,'@CMT_LOAD_UNPUT_AND_PUT$QI'),(1768,'@musicroom_menu$qv'))
FIELDS=((210,4,204,86,None,4,0),(207,2,196,20,1,3,202),
    (184,2,196,20,1,3,202),(174,2,196,22,1,2,0),(166,2,196,20,1,3,202),
    (161,4,204,86,None,3,0),(106,4,204,86,None,15,0),(103,2,196,20,1,2,0),
    (64,2,196,20,1,3,201),(56,4,204,86,None,15,0),(53,2,196,20,1,2,0),(8,2,196,20,1,3,201))
EXTERNALS={2:('_VRAM_PLANE_B',DS,0x19FA),3:('HMEM_ALLOCBYTE',0,0x24CA),
    4:('HMEM_FREE',0,0x25CE),15:('@GRAPH_PUTSA_FX$QIIINXUC',0xBEB,0x82B)}


def need(value,message):
    if not value:raise ValueError('OP Music state layout: '+str(message))


def native_image(raw):
    description=describe_omf(raw)
    need(description['valid'] and description['module_name']==WRAPPER and
        description['translator_comments']==['TC86 Borland C++ 4.02'],'actual TC4 producer')
    need(description['record_counts']==dict(COMENT=70,EXTDEF=1,FIXUPP=4,GRPDEF=1,LEDATA=4,LNAMES=1,MODEND=1,PUBDEF=23,SEGDEF=3,THEADR=1),
        'entire containing OMF record geometry')
    need(segment_definitions(raw)==[dict(index=i,name=n,**{'class':c},overlay='',size=s) for i,n,c,s in
        ((1,'OP_MUSIC_TEXT','CODE',2244),(2,'_DATA','DATA',1008),(3,'_BSS','BSS',1060))],
        'complete natural CODE/DATA/BSS contributions')
    need(tuple(code_publics(raw,1))==PUBLICS,'all fourteen containing CODE publics')
    code,blocks=code_bytes(raw,1)
    need([(b['offset'],b['size']) for b in blocks]==[(0,1024),(1024,1017),(2041,203)],'all CODE LEDATA blocks')
    names=[];fields=[];block=None;image=bytearray(code[:SIZE])
    for rec in parse_omf(raw):
        if rec.name=='EXTDEF':
            at=0
            while at<len(rec.data):
                n=rec.data[at];at+=1;names.append(rec.data[at:at+n].decode());at+=n
                need(rec.data[at]==0,'untyped external');at+=1
        elif rec.name=='LEDATA':block=rec.data[0],int.from_bytes(rec.data[1:3],'little')
        elif rec.name=='FIXUPP' and block[0]==1:
            at=0
            while at<len(rec.data):
                loc,low,method=rec.data[at:at+3];at+=3;frame=None
                need(method in (20,22,86),'native field form')
                if method in (20,22):frame=rec.data[at];at+=1
                index=rec.data[at];at+=1
                site=block[1]+(loc&3)*256+low;width=4 if loc>>2&15==3 else 2
                if site>=SIZE:continue
                need(site+width<=SIZE,'whole scoped native field')
                addend=int.from_bytes(code[site:site+width],'little')
                fields.append((site,width,loc,method,frame,index,addend))
                if method==20:
                    need(width==2 and frame==1 and index in (2,3),'DGROUP local DATA/BSS WORD')
                    value={2:DATA,3:BSS}[index]+addend
                elif method==22:
                    need(width==2 and frame==1 and index==2,'external VRAM far-pointer storage WORD')
                    value=EXTERNALS[index][2]+addend
                else:
                    need(width==4 and code[site-1]==0x9A and index in (3,4,15),'actual native far CALL')
                    _,segment,offset=EXTERNALS[index];value=(segment<<16)+offset+addend
                image[site:site+width]=value.to_bytes(width,'little')
    need(tuple(fields)==FIELDS and all(names[i-1]==name for i,(name,_,_) in EXTERNALS.items()),'all twelve literal ordered fields and identities')
    return bytes(image)


def verify(root,work,target,candidate):
    native=(work/OBJECT).read_bytes();image=native_image(native)
    need(image==target.program_image[START:START+SIZE]==candidate.program_image[START:START+SIZE],
        'all216 independently resolved native/target/candidate bytes')
    need((work/WRAPPER).read_text()=='#include "src/op/music/state_and_tracks.inl"\n\n#include "src/op/music/nopoly_blit.inl"\n\n#include "src/op/music/animation_and_menu.inl"\n',
        'literal three-include maintained producer')
    dependencies=describe_omf(native)['dependency_paths']
    need(all(name in dependencies for name in (WRAPPER,SOURCE,'src/op/music/nopoly_blit.inl','src/op/music/animation_and_menu.inl')),
        'all literal maintained includes consumed')
    table=(work/'obj/th03/op.map').read_text()
    for seg,off,size,cls,name,group in ((CS,OFFSET,2244,'CODE','OP_MUSIC_TEXT','GROUP_01'),
        (DS,DATA,1008,'DATA','_DATA','DGROUP'),(DS,BSS,1060,'BSS','_BSS','DGROUP')):
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{size:04X}\s+C={cls}\s+S={name}\s+G={group}\s+M=th03/op_music\.cpp\s+ACBP={(0x28 if cls=="CODE" else 0x48):02X}\s*$',table))==1,
            'complete containing MAP geometry: '+name)
    for offset,name in PUBLICS[:4]:
        symbol={'@TRACK_PUT_BOTH$QUCUC':'track_put_both(unsigned char,unsigned char)',
            '@TRACKLIST_PUT_BOTH$QUC':'tracklist_put_both(unsigned char)',
            '@nopoly_B_snap$qv':'nopoly_b_snap()','@nopoly_B_free$qv':'nopoly_b_free()'}[name]
        need(len(re.findall(rf'(?m)^\s*{CS:04X}:{OFFSET+offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',table))==2,'both owned MAP publics: '+symbol)
    relocations=[[CS,OFFSET+site+2] for site,width,*_ in FIELDS if width==4]
    for mz in (target,candidate):
        need([[r.segment,r.offset] for r in mz.relocations if START<=r.linear<START+SIZE]==relocations,'complete literal ordered MZ vector')
        need(not any(r.linear<START+SIZE and r.linear+2>START and not START<=r.linear<=START+SIZE-2 for r in mz.relocations),'no straddling relocation')
    rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(image,START))
    need(sum(i.size for i in rows)==SIZE and [(i.address,i.op_str) for i in rows if i.mnemonic=='call']==[(0xA5A9,'0xa51e')],
        'all216 instructions and actual internal track CALL')
    digest=hashlib.sha256(image).hexdigest()
    owner=dict(unit_id=UNIT,name='Music Room state and tracks',source=SOURCE,object=OBJECT,segment=CS,offset=OFFSET,start=START,size=SIZE,
        coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=digest,candidate_sha256=digest,ordered_relocations=relocations,
        procedure_count=4,procedures=[dict(name=n,offset=o,size=s,callee_pop_bytes=p) for n,o,s,p in PROCEDURES],
        code_bytes=SIZE,initialized_data_bytes=0,private_data_bytes=0,private_bss_bytes=0,
        abi='four complete near procedures; track Pascal pop4/list pop2; BYTE arguments in WORD slots; snap/free noargs')
    return dict(owners=[owner],functions=4,code_bytes=SIZE,instruction_bytes=SIZE,ordered_native_fields=[list(f) for f in FIELDS],
        ordered_relocations=relocations,containing_CODE_bytes=2244,containing_DATA_bytes=1008,containing_BSS_bytes=1060,
        containing_other_CODE_DATA_BSS_newly_accepted=False,whole_product_accepted=False)
