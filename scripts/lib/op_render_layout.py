"""Three complete near renderers, including the compiler's inline switch table."""
import hashlib,re,struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.omf import describe_omf,parse_omf
from lib.op_cfg_layout import OBJECT,WRAPPER,SEGMENT,OFFSET,DATA_SEGMENT,DATA_OFFSET,verify as containing_layout
from probe_th03_main_boss_marisa_cpp import code_bytes
FUNCTIONS=(('th03-op-decoded-render-vs-choice','vs','src/op/entry.cpp',661,66,66,'vs_choice_put(int,unsigned int)'),
 ('th03-op-decoded-render-main-choice','main','src/op/menu/menu_state.inl',1493,122,122,'main_choice_put(int,unsigned int)'),
 ('th03-op-decoded-render-option-choice','option','src/op/menu/menu_state.inl',1615,330,321,'option_choice_put(int,unsigned int)'))
ENTRIES={kind:(SEGMENT*16+OFFSET+off,size,ins) for _,kind,_,off,size,ins,_ in FUNCTIONS}
FIELDS=((717,4,206,86,None,1,0),(713,2,198,20,2,2,43),(701,2,198,20,2,2,34),(684,2,198,20,2,2,25),
 (1943,2,199,20,1,1,1729),(1941,2,199,20,1,1,1716),(1939,2,199,20,1,1,1703),(1937,2,199,20,1,1,1690),
 (1926,4,207,86,None,1,0),(1922,2,199,20,2,2,106),(1905,2,199,20,2,2,202),(1893,2,199,20,2,2,195),(1881,2,199,20,2,2,188),
 (1849,2,199,22,2,15,0),(1843,4,207,86,None,1,0),(1839,2,199,20,2,2,119),(1822,2,199,20,2,2,165),
 (1810,2,199,20,2,2,157),(1798,2,199,20,2,2,149),(1765,2,198,22,2,15,0),(1759,4,206,86,None,1,0),
 (1755,2,198,20,2,2,114),(1737,2,198,20,2,2,144),(1724,2,198,20,2,2,140),(1711,2,198,20,2,2,135),
 (1698,2,198,20,2,2,131),(1688,2,198,20,1,1,1937),(1666,2,198,22,2,15,0),(1660,4,206,86,None,11,0),
 (1654,2,198,20,2,2,229),(1642,4,206,86,None,1,0),(1638,2,198,20,2,2,110),(1605,4,206,86,None,1,0),
 (1601,2,198,20,2,2,106),(1584,2,198,20,2,2,101),(1567,2,198,20,2,2,95),(1550,2,198,20,2,2,87),
 (1533,2,197,20,2,2,80),(1516,2,197,20,2,2,76))
EXTERNALS={1:('GAIJI_PUTSA',0,0xFCC),11:('TEXT_PUTSA',0,0x2254),15:('_resident',DATA_SEGMENT,0x2464)}
DEPENDENCIES=((0xA9,27,'2722eadfce3d306503ffc58be1a082a2b96ab13ca9329fe3903330d19085b18d'),
 (0xDC,133,'9130c2f10aaa98dce81da55b4e132f3fd6bca8301785f01a113585652e69edd4'),
 (0x175,9,'93d43ba40f1f1a89deff77a93eafeef83233d1569c60a341bd923f3d001b2ad9'))
TABLE=0x799;BRANCHES=(0x6A2,0x6AF,0x6BC,0x6C9)
def need(v,m):
    if not v:raise ValueError('OP renderer layout: '+m)
def native_image(raw):
    code,_=code_bytes(raw,1);im=bytearray(code);fields=[];names=[];block=None;data=None
    for r in parse_omf(raw):
        if r.name=='EXTDEF':
            at=0
            while at<len(r.data):n=r.data[at];at+=1;names.append(r.data[at:at+n].decode());at+=n+1
        elif r.name=='LEDATA':
            block=(r.data[0],int.from_bytes(r.data[1:3],'little'))
            if block==(2,0):data=r.data[3:]
        elif r.name=='FIXUPP' and block[0]==1:
            at=0
            while at<len(r.data):
                loc,lo,fd=r.data[at:at+3];at+=3;frame=None;need(fd in (0x14,0x16,0x56),'known native fixup form')
                if fd in (0x14,0x16):frame=r.data[at];at+=1
                target=r.data[at];at+=1;s=block[1]+(loc&3)*256+lo;w=4 if loc>>2&15==3 else 2
                if not any(off<=s<off+size for _,_,_,off,size,*_ in FUNCTIONS):continue
                need(loc&0xC0==0xC0 and any(off<=s and s+w<=off+size for _,_,_,off,size,*_ in FUNCTIONS),'whole absolute scoped field')
                addend=int.from_bytes(code[s:s+w],'little');fields.append((s,w,loc,fd,frame,target,addend))
                if fd==0x14:
                    need(w==2 and (frame,target) in ((1,1),(2,2)),'real own CODE/DATA group WORD')
                    value=(OFFSET if frame==1 else DATA_OFFSET)+addend
                elif fd==0x16:
                    need((w,frame,target)==(2,2,15),'external resident pointer WORD');value=0x2464+addend
                else:
                    need(w==4 and target in (1,11) and code[s-1]==0x9A,'real far library CALL')
                    _,seg,value=EXTERNALS[target];value=(seg<<16)+value+addend
                im[s:s+w]=value.to_bytes(w,'little')
    need(tuple(fields)==FIELDS and all(names[i-1]==v[0] for i,v in EXTERNALS.items()),'all thirty-nine literal ordered fields and symbolic externals')
    need(data is not None and len(data)==487,'complete native containing DATA')
    return bytes(im),data

def verify(work,target,candidate):
    containing_layout(work,target,candidate);raw=(work/OBJECT).read_bytes();im,data=native_image(raw);text=(work/'obj/th03/op.map').read_text();owners=[]
    deps=describe_omf(raw)['dependency_paths']
    need(all(p in deps for p in (WRAPPER,'src/op/entry.cpp','src/op/menu/menu_state.inl')),'actual compiled containing source and bounded menu include')
    for unit,kind,source,off,size,ins,name in FUNCTIONS:
        start=SEGMENT*16+OFFSET+off;end=start+size;body=im[off:off+size]
        need(body==target.program_image[start:end]==candidate.program_image[start:end],'complete resolved renderer bytes including inline non-instructions')
        rows=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(body[:ins],start));need(sum(i.size for i in rows)==ins and rows[-1].mnemonic=='ret' and rows[-1].op_str=='4','complete instruction bodies and near Pascal RET 4')
        need(len(re.findall(rf'(?m)^\s*0990:{OFFSET+off:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,'both near renderer MAP publics')
        fields=[f for f in FIELDS if off<=f[0]<off+size];pairs=[[SEGMENT,OFFSET+s+2] for s,w,*_ in fields if w==4]
        for image in (target,candidate):
            need([[r.segment,r.offset] for r in image.relocations if start<=r.linear<end]==pairs,'complete ordered renderer relocation vector')
            need(not any(r.linear<end and r.linear+2>start and not start<=r.linear<=end-2 for r in image.relocations),'no straddling MZ field')
        h=hashlib.sha256(body).hexdigest();owners.append(dict(unit_id=unit,name=kind,source=source,object=OBJECT,segment=SEGMENT,offset=OFFSET+off,start=start,size=size,
            coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=h,candidate_sha256=h,ordered_relocations=pairs,argument_bytes=4,callee_pop_bytes=4,
            instruction_bytes=ins,inline_non_instruction_bytes=size-ins,private_data_bytes=0,private_bss_bytes=0,abi='near Pascal; full WORD selection and attribute; BP/SI/DI preserved'))
    for _,seg,off in EXTERNALS.values():
        name=next(v[0] for v in EXTERNALS.values() if (v[1],v[2])==(seg,off))
        need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+(?:idle\s+)?{re.escape(name)}\s*$',text))==2,'both library/global MAP tables')
    for off,size,h in DEPENDENCIES:
        b=data[off-DATA_OFFSET:off-DATA_OFFSET+size];need(hashlib.sha256(b).hexdigest()==h,'complete initialized string dependency')
        for image in (target,candidate):need(image.program_image[DATA_SEGMENT*16+off:DATA_SEGMENT*16+off+size]==b,'native DATA resolves into both current products')
    ordered=[[SEGMENT,OFFSET+s+2] for s,w,*_ in FIELDS if w==4]
    for image in (target,candidate):
        need([[r.segment,r.offset] for r in image.relocations if any(o['start']<=r.linear<o['start']+o['size'] for o in owners)]==ordered,'literal cross-renderer relocation order')
    table=im[TABLE-OFFSET:TABLE-OFFSET+8];need(struct.unpack('<4H',table)==BRANCHES and im[TABLE-OFFSET-1]==0,'zero byte and four complete native switch-table WORDs')
    need(all(0x657<=v<0x798 for v in BRANCHES),'switch table stays in option instructions')
    return dict(owners=owners,functions=3,code_bytes=518,instruction_bytes=509,inline_non_instruction_bytes=9,
        ordered_native_fields=[dict(offset=s,width=w,locat=loc,fixdat=fd,frame=fr,target=t,addend=a) for s,w,loc,fd,fr,t,a in FIELDS],
        ordered_relocations=ordered,switch_table_offset=TABLE,switch_table_targets=list(BRANCHES),
        reviewed_initialized_dependency_bytes=169,private_data_bytes=0,private_bss_bytes=0,containing_producer_accepted=False,whole_product_accepted=False)
