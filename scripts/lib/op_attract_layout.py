"""The complete 105-byte near attract wait in the larger OP entry producer."""
import hashlib,re
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.omf import parse_omf
from lib.op_cfg_layout import SOURCE,OBJECT,SEGMENT,OFFSET,DATA_SEGMENT,verify as containing_layout
from probe_th03_main_boss_marisa_cpp import code_bytes

START=0x9E16;SIZE=105;NATIVE_OFFSET=0x50E
FIELDS=((1383,4,0xCD,0x56,None,13,0),(1376,4,0xCD,0x56,None,9,0),
 (1366,2,0x85,0x16,1,34,0),(1355,4,0xCD,0x56,None,9,0),(1341,2,0xC5,0x16,2,16,0),
 (1335,4,0xCD,0x56,None,13,0),(1315,2,0xC5,0x16,2,15,0),(1309,4,0xCD,0x56,None,17,0),
 (1300,2,0xC5,0x16,2,16,0))
EXTERNALS={9:('SUPER_PUT',0,0x28D8,'SUPER_PUT'),13:('@FRAME_DELAY$QI',0xBEB,0x2EE,'frame_delay(int)'),
 15:('_resident',DATA_SEGMENT,0x2464,'_resident'),16:('_input_sp',DATA_SEGMENT,0x1AA6,'_input_sp'),
 17:('@INPUT_MODE_INTERFACE$QV',0xBEB,0xAD6,'input_mode_interface()'),
 34:('@BOX_COLUMN16_UNPUT$QUI',SEGMENT,0x180A,'box_column16_unput(unsigned int)')}
def need(v,m):
    if not v:raise ValueError('OP attract layout: '+m)
def native_image(raw):
    code,_=code_bytes(raw,1);im=bytearray(code);block=None;fields=[];names=[]
    for r in parse_omf(raw):
        if r.name=='EXTDEF':
            at=0
            while at<len(r.data):
                n=r.data[at];at+=1;names.append(r.data[at:at+n].decode());at+=n+1
        if r.name=='LEDATA':block=(r.data[0],int.from_bytes(r.data[1:3],'little'))
        if r.name!='FIXUPP' or block[0]!=1:continue
        at=0
        while at<len(r.data):
            loc,lo,fd=r.data[at:at+3];at+=3;frame=None
            need(fd in (0x14,0x16,0x56),'reviewed containing fixup forms')
            if fd in (0x14,0x16):frame=r.data[at];at+=1
            target=r.data[at];at+=1;s=block[1]+(loc&3)*256+lo;w=4 if loc>>2&15==3 else 2
            if not NATIVE_OFFSET<=s<NATIVE_OFFSET+SIZE:continue
            addend=int.from_bytes(code[s:s+w],'little');fields.append((s,w,loc,fd,frame,target,addend))
            need(target in EXTERNALS and s+w<=NATIVE_OFFSET+SIZE,'complete scoped native fields')
            _,seg,off,_=EXTERNALS[target]
            if loc&0x40:
                value=(off+addend)|(seg<<16) if w==4 else off+addend
            else:
                need(target==34 and w==2 and fd==0x16 and frame==1,'near external self-relative call')
                value=(seg*16+off+addend-(SEGMENT*16+OFFSET+s+2))&65535
            im[s:s+w]=value.to_bytes(w,'little')
    need(tuple(fields)==FIELDS,'nine literal ordered fields including one relative WORD')
    need(all(names[i-1]==name for i,(name,*_) in EXTERNALS.items()),'native symbolic identities')
    return bytes(im)
def verify(work,target,candidate):
    containing_layout(work,target,candidate)
    raw=(work/OBJECT).read_bytes();im=native_image(raw);body=im[NATIVE_OFFSET:NATIVE_OFFSET+SIZE]
    need(body==target.program_image[START:START+SIZE]==candidate.program_image[START:START+SIZE],'complete resolved raw body')
    ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(body,START))
    need(sum(i.size for i in ins)==SIZE and ins[0].mnemonic=='push' and ins[-1].mnemonic=='ret','complete near instruction boundaries')
    text=(work/'obj/th03/op.map').read_text()
    for _,seg,off,name in EXTERNALS.values():
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,'both external MAP tables: '+name)
    need(len(re.findall(r'(?m)^\s*0990:0516\s+(?:idle\s+)?wait_for_input_or_start_demo_the\(\)\s*$',text))==2,'both near owner MAP publics')
    pairs=[[SEGMENT,OFFSET+s+2] for s,w,*_ in FIELDS if w==4]
    for mz in (target,candidate):
        need([[r.segment,r.offset] for r in mz.relocations if START<=r.linear<START+SIZE]==pairs,'five literal ordered far call relocations')
        need(not any(r.linear<START+SIZE and r.linear+2>START and not START<=r.linear<=START+SIZE-2 for r in mz.relocations),'whole relocation fields')
    digest=hashlib.sha256(body).hexdigest()
    owner=dict(unit_id='th03-op-decoded-entry-attract-wait',name='wait_for_input_or_start_demo_then_box_to_main_animate',
        source=SOURCE,object=OBJECT,segment=SEGMENT,offset=0x516,start=START,size=SIZE,coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=digest,candidate_sha256=digest,ordered_relocations=pairs,abi='near cdecl; no arguments; BP/SI preserved; real input/demo helpers; bounded graphics/timing and failed exec',private_data_bytes=0,private_bss_bytes=0)
    return dict(owners=[owner],functions=1,code_bytes=SIZE,ordered_native_fields=[dict(offset=s,width=w,locat=loc,fixdat=fd,frame=fr,target=t,addend=a) for s,w,loc,fd,fr,t,a in FIELDS],
        ordered_relocations=pairs,private_data_bytes=0,private_bss_bytes=0,reviewed_external_data_bytes=6,containing_producer_accepted=False,whole_product_accepted=False)
