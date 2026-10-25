"""Five complete functions in the maintained MAINL root TASM producer.

The enclosing DATA/BSS, three adjacent NOPs and other procedures stay unowned.
Comparison buffers resolve the five real seed WORD references; outputs are intact.
"""
import hashlib
import re
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from lib.omf import parse_omf,describe_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics

OBJECT='obj/th03/mainl.obj'
WRAPPER='th03_mainl.asm'
CODE_BASE,DATA_BASE,DS=0x272,0x112,0xE3F
PROCEDURES=(
 ('root-tail-keyclear','keyclear','DOS_KEYCLEAR',0x6FE,6,'dos_keyclear.asm',0,4),
 ('root-tail-grcg','setcolor','GRCG_SETCOLOR',0xC36,41,'grcg_setcolor.asm',4,4),
 ('root-tail-grcg-off','off','GRCG_OFF',0xC60,5,'grcg_setcolor.asm',0,4),
 ('root-tail-rand','rand','IRAND',0x1A3E,42,'random.asm',0,4),
 ('root-tail-string-compare','compare',None,0x2C30,56,'pf_str_ieq.asm',8,2))
ENTRIES={name:(start,size) for _,name,_,start,size,*_ in PROCEDURES}
PADDING=(0xC5F,0xC65,0x2C2F)
FIELDS=((0x17D1,2,0xC5,0x54,2,0x4A6),(0x17DA,2,0xC5,0x54,2,0x4A4),
        (0x17E3,2,0xC5,0x54,2,0x4A4),(0x17EB,2,0xC5,0x54,2,0x4A4),
        (0x17F0,2,0xC5,0x54,2,0x4A6))

def need(v,m):
    if not v:raise ValueError('MAINL root helper layout: '+m)

def native(raw):
    records=parse_omf(raw);d=describe_omf(raw)
    need(d['valid'] and d['module_name']==WRAPPER and d['translator_comments']==['Turbo Assembler  Version 5.0'],'complete native TASM root identity')
    segments=segment_definitions(raw)
    need([(s['name'],s['class'],s['size']) for s in segments]==[
        ('_TEXT','CODE',10944),('_DATA','DATA',2036),('ROOTPRE_TEXT','CODE',0),
        ('CUTSCENE_TEXT','CODE',0),('SCOREDAT_TEXT','CODE',0),('REGIST_TEXT','CODE',0),
        ('STAFFP_TEXT','CODE',0),('SHARED','CODE',0),('_BSS','BSS',5108)],'complete containing segment geometry')
    need([r.data[0] for r in records if r.name=='SEGDEF']==[0x48,0x48,0x28,0x28,0x28,0x28,0x28,0x48,0x48],
         'native WORD root / BYTE GROUP_01 contributions, PUBLIC USE16')
    intervals=[(s-CODE_BASE,s-CODE_BASE+n) for s,n in ENTRIES.values()]
    image=bytearray(10944);seen=set();fields=[];block=None
    for r in records:
        if r.name=='LEDATA':
            block=(r.data[0],int.from_bytes(r.data[1:3],'little'))
            if block[0]!=1:continue
            for a,b in intervals:
                lo,hi=max(a,block[1]),min(b,block[1]+len(r.data)-3)
                for at in range(lo,hi):
                    need(at not in seen,'nonoverlapping native owner LEDATA');seen.add(at)
                    image[at]=r.data[3+at-block[1]]
        elif r.name=='FIXUPP' and block and block[0]==1:
            at=0
            while at<len(r.data):
                loc,low,fd=r.data[at:at+3];at+=3
                need(loc&0x80 and fd&~3 in (0x04,0x14,0x54) and fd&3<3,
                     f'literal unthreaded native root fields: {block}, {at-3}, {loc:02X}/{fd:02X}')
                if fd&~3 in (0x04,0x14):at+=1 # Explicit frame index, not scoped here.
                target=r.data[at];at+=1
                site=block[1]+(loc&3)*256+low
                width={1:2,2:2,3:4}.get(loc>>2&15)
                if not any(a<=site<b for a,b in intervals):
                    need(width is not None and not any(site<a<site+width for a,_ in intervals),'no straddling native field')
                    continue
                need(width==2 and loc&0x40 and fd==0x54 and target==2,'real own DATA absolute WORD')
                add=int.from_bytes(image[site:site+2],'little')
                fields.append((site,width,loc,fd,target,add))
                image[site:site+2]=(DATA_BASE+add).to_bytes(2,'little')
    need(seen=={p for a,b in intervals for p in range(a,b)},'complete scoped LEDATA coverage, no implicit zeros')
    need(tuple(fields)==FIELDS,'all five ordered native random seed fields')
    return image,d

def verify(work,target,candidate,graph,files):
    raw=(work/OBJECT).read_bytes();image,d=native(raw)
    row,=[r for r in graph if r['output']==OBJECT]
    need((row['wrapper'],row['game'],row['binary'],row['first_binary'])==(WRAPPER,3,'L','mainl'),'actual root GAME3/L producer')
    text=(work/'obj/th03/mainl.map').read_text().replace(chr(92),'/')
    for line in ('0000:0272 2AC0 C=CODE   S=_TEXT          G=(none)  M=th03_mainl.asm ACBP=48',
                 '0E3F:0112 07F4 C=DATA   S=_DATA          G=DGROUP  M=th03_mainl.asm ACBP=48'):
        need(text.count(line)==1,'literal containing root MAP allocation')
    publics=code_publics(raw,1);owners=[]
    from pathlib import Path
    root=Path(__file__).resolve().parents[2]
    for suffix,name,symbol,start,size,leaf,args,frame in PROCEDURES:
        source='src/mainl/root_tail/'+leaf
        need(source in d['dependency_paths'] and 'include '+source in files[WRAPPER].decode('cp932'),
             'actual maintained include and native dependency')
        need(files[source]==(work/source).read_bytes() and files[source].replace(b'\r\n',b'\n')==(root/source).read_bytes().replace(b'\r\n',b'\n'),
             'maintained source transport')
        if symbol:
            need((start-CODE_BASE,symbol) in publics,'native whole procedure public')
            need(len(re.findall(rf'(?m)^\s*0000:{start:04X}\s+(?:idle\s+)?{symbol}\s*$',text))==2,'both MAP procedure publics')
        body=bytes(image[start-CODE_BASE:start-CODE_BASE+size])
        need(body==target.program_image[start:start+size]==candidate.program_image[start:start+size],'whole resolved native helper bytes')
        ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(body,start))
        need(sum(i.size for i in ins)==size and ins[-1].mnemonic==('ret' if name=='compare' else 'retf'),
             'complete instruction-only helper and native near/far return')
        for mz in (target,candidate):need(not any(r.linear<start+size and r.linear+2>start for r in mz.relocations),'empty full ordered MZ relocation vector')
        h=hashlib.sha256(body).hexdigest()
        owners.append(dict(unit_id='th03-mainl-decoded-'+suffix,name=name,source=source,object=OBJECT,
            segment=0,offset=start,start=start,size=size,coordinate_space='decoded-load',canonical_file_offset=None,
            target_sha256=h,candidate_sha256=h,ordered_relocations=[],argument_bytes=args,
            callee_pop_bytes=args,return_address_bytes=frame,private_data_bytes=0,private_bss_bytes=0,
            abi=('near' if frame==2 else 'far')+' Pascal; WORD arguments; original SS frames and full register/flag effects'))
    # STR_IEQ is private. Its real PFOPEN caller identifies the near entry after
    # the separate EVEN byte, without inventing an exported symbol.
    need((work/OBJECT).read_bytes()==raw,'stable root object')
    call=next(r for r in parse_omf(raw) if r.name=='LEDATA' and r.data[0]==1
              and int.from_bytes(r.data[1:3],'little')<=0x2B65-CODE_BASE<int.from_bytes(r.data[1:3],'little')+len(r.data)-3)
    at=0x2B65-CODE_BASE-int.from_bytes(call.data[1:3],'little')+3
    need(call.data[at:at+3]==b'\xE8\xC8\0' and all(m.program_image[0x2B65:0x2B68]==b'\xE8\xC8\0' for m in (target,candidate)),
         'actual private near caller targets 2C30, excluding its prefix alignment')
    for symbol in ('random_seed','_random_seed'):
        need(len(re.findall(rf'(?m)^\s*0E3F:05B6\s+(?:idle\s+)?{symbol}\s*$',text))==2,'both external random seed MAP publics')
    return dict(owners=owners,functions=5,code_bytes=150,ordered_native_fields=[list(f) for f in FIELDS],
        ordered_relocations=[],excluded_adjacent_NOPs=list(PADDING),external_seed_bytes=4,
        private_entry_caller=dict(call=0x2B65,target=0x2C30),containing_producer_accepted=False,
        private_data_bytes=0,private_bss_bytes=0,whole_product_accepted=False)
