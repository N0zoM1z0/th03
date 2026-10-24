"""Complete demo and score dispatch functions inside the larger OP entry TU."""
import hashlib
import re

from lib.omf import parse_omf,describe_omf
from lib.op_cfg_layout import SOURCE,WRAPPER,OBJECT,SEGMENT,OFFSET,DATA_SEGMENT,DATA_OFFSET,native_image as containing_image
from probe_th03_main_boss_marisa_cpp import code_bytes

FUNCTIONS=(('th03-op-decoded-entry-demo','start_demo',1092,202),
           ('th03-op-decoded-entry-score','score_menu',1399,94))
FIELDS=((1481,4,0x56,None,46,0),(1478,2,0x14,2,2,223),(1474,2,0x14,2,2,223),
 (1465,4,0x56,None,12,0),(1460,4,0x56,None,8,0),(1455,4,0x56,None,33,0),(1447,4,0x56,None,3,0),
 (1428,2,0x16,2,15,0),(1405,2,0x16,2,15,0),
 (1284,4,0x56,None,46,0),(1281,2,0x14,2,2,223),(1277,2,0x14,2,2,223),
 (1268,4,0x56,None,12,0),(1263,4,0x56,None,33,0),(1255,4,0x56,None,3,0),(1247,4,0x56,None,7,0),
 (1229,2,0x16,2,15,0),(1216,2,0x16,2,15,0),(1212,2,0x14,2,2,56),(1192,2,0x16,2,15,0),
 (1181,2,0x14,2,2,50),(1166,2,0x16,2,15,0),(1162,2,0x14,2,2,50),(1128,2,0x16,2,15,0),(1098,2,0x16,2,15,0))
EXTERNALS={3:('GAIJI_RESTORE',0,0xF1A),7:('PALETTE_BLACK_OUT',0,0x536),8:('SUPER_FREE',0,0x269A),
 12:('@game_exit$qv',0xBEB,0x112),15:('_resident',DATA_SEGMENT,0x2464),
 33:('SND_KAJA_INTERRUPT',0xBEB,0x553),46:('_execl',0,0x9119)}


def need(value,message):
    if not value:raise ValueError('OP dispatch layout: '+message)


def native_image(raw):
    containing_image(raw) # Whole containing geometry/publics stay context.
    code,_=code_bytes(raw,1);image=bytearray(code);fields=[];block=None;externals=[]
    for rec in parse_omf(raw):
        if rec.name=='EXTDEF':
            at=0
            while at<len(rec.data):
                size=rec.data[at];at+=1;externals.append(rec.data[at:at+size].decode('ascii'));at+=size+1
        if rec.name=='LEDATA':block=(rec.data[0],int.from_bytes(rec.data[1:3],'little'))
        if rec.name!='FIXUPP' or block[0]!=1:continue
        at=0
        while at<len(rec.data):
            loc,low,fd=rec.data[at:at+3];at+=3;frame=None
            need(fd in (0x14,0x16,0x56),'reviewed containing fixup form')
            if fd in (0x14,0x16):frame=rec.data[at];at+=1
            target=rec.data[at];at+=1;site=block[1]+(loc&3)*256+low;width=4 if loc>>2&15==3 else 2
            if not any(off<=site<off+size for _,_,off,size in FUNCTIONS):continue
            need(loc&0xC0==0xC0 and loc>>2&15 in (1,3) and any(off<=site and site+width<=off+size for _,_,off,size in FUNCTIONS),'whole scoped field')
            addend=int.from_bytes(code[site:site+width],'little');fields.append((site,width,fd,frame,target,addend))
            if fd==0x14:
                need(width==2 and frame==2 and target==2,'own DATA offset frame');value=DATA_OFFSET+addend
                image[site:site+2]=value.to_bytes(2,'little')
            elif fd==0x16:
                need(width==2 and frame==2 and target==15,'external resident DATA frame')
                image[site:site+2]=(EXTERNALS[target][2]+addend).to_bytes(2,'little')
            else:
                need(width==4 and target in EXTERNALS and code[site-1]==0x9A,'real far dispatch call')
                _,seg,off=EXTERNALS[target];image[site:site+4]=(off+addend).to_bytes(2,'little')+seg.to_bytes(2,'little')
    need(tuple(fields)==FIELDS,'all twenty-five ordered literal scoped fields')
    need(all(externals[i-1]==name for i,(name,_,_) in EXTERNALS.items()),'literal scoped symbolic identities')
    return bytes(image)


def verify(work,target,candidate):
    raw=(work/OBJECT).read_bytes();image=native_image(raw)
    from lib.op_cfg_layout import verify as cfg_layout
    cfg_layout(work,target,candidate) # Recheck real containing DATA and MAP geometry.
    text=(work/'obj/th03/op.map').read_text().replace(chr(92),'/')
    for name,seg,off in EXTERNALS.values():
        display='game_exit()' if name=='@game_exit$qv' else name
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+(?:idle\s+)?{re.escape(display)}\s*$',text))==2,'both scoped external MAP tables: '+name)
    owners=[]
    for unit,name,offset,size in FUNCTIONS:
        start=SEGMENT*16+OFFSET+offset;end=start+size
        body=image[offset:offset+size]
        need(body==target.program_image[start:end]==candidate.program_image[start:end],'complete native resolved function bytes')
        need(len(re.findall(rf'(?m)^\s*0990:{OFFSET+offset:04X}\s+(?:idle\s+)?{name}\(\)\s*$',text))==2,'both whole near function MAP publics')
        pairs=[[SEGMENT,OFFSET+s+2] for s,w,*_ in FIELDS if w==4 and offset<=s<offset+size]
        for mz in (target,candidate):
            need(not any(r.linear<end and r.linear+2>start and not start<=r.linear<=end-2 for r in mz.relocations),'whole relocation fields')
            need([[r.segment,r.offset] for r in mz.relocations if start<=r.linear<end]==pairs,'all literal ordered dispatch MZ pairs')
        digest=hashlib.sha256(body).hexdigest()
        owners.append(dict(unit_id=unit,name=name,source=SOURCE,object=OBJECT,segment=SEGMENT,offset=OFFSET+offset,start=start,size=size,
            coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=digest,candidate_sha256=digest,
            ordered_relocations=pairs,abi='near cdecl; no arguments; BP/SI restored; failed execl returns to caller',private_data_bytes=0,private_bss_bytes=0))
    return dict(owners=owners,functions=2,code_bytes=296,ordered_native_fields=[dict(offset=s,width=w,fixdat=f,frame=fr,target=t,addend=a) for s,w,f,fr,t,a in FIELDS],
        ordered_relocations=[p for o in owners for p in o['ordered_relocations']],
        data_dependencies=dict(pairings_and_seed_tables=[0xC4,24],wrapped_zero_preceding_bytes=[0xC2,2],mainl_filename=[0x16F,6]),
        reviewed_initialized_dependency_bytes=32,containing_producer_accepted=False,whole_product_accepted=False)
