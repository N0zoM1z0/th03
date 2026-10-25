"""Three complete SMC blitters; whole native producers and separate EVEN bytes."""
import hashlib
import re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

CS,DS,SLOTS,LUT,COLOR = 0xC7E,0xE3F,0x1D0E,0x20D6,0xC36
PRODUCERS = (
    ('cdg_put','src/shared/formats/cdg_put.asm',3,0x1F4,382,
     (('alpha','CDG_PUT_8',0,179),('hflip','CDG_PUT_HFLIP_8',180,201))),
    ('cdg_p_na','src/shared/formats/cdg_noalpha.asm',1,0xF32,114,
     (('noalpha','CDG_PUT_NOALPHA_8',0,113),)))
ENTRIES = {kind:(offset+at,size) for _,_,_,offset,_,procedures in PRODUCERS for kind,_,at,size in procedures}
PATCHES = {'alpha':(120,113,99,125,95),'hflip':(129,169,107,151,103,147),'noalpha':(71,)}
WRITERS = {'alpha':(29,44,51,55,65),'hflip':(46,50,54,59,69,73),'noalpha':(29,)}
FIELDS = {
 'cdg_put':((31,196,84,3,120),(46,196,84,3,113),(53,196,84,3,99),(57,196,84,3,125),(67,196,84,3,95),
             (228,196,84,3,309),(232,196,84,3,349),(237,196,84,3,287),(242,196,84,3,331),
             (251,196,84,3,283),(255,196,84,3,327),(12,204,86,3,0),(24,196,86,4,0),
             (192,204,86,3,0),(204,196,86,4,0),(275,197,86,5,0),(319,197,86,4,0)),
 'cdg_p_na':((13,196,86,1,0),(31,196,84,1,71))}
EXTERNALS = {'cdg_put':('_SinTable8','_CosTable8','GRCG_SETCOLOR','_cdg_slots','_hflip_lut'),'cdg_p_na':('_cdg_slots',)}
EXCLUDED = (0x2A7,0x371,0xFA3)


def need(value,message):
    if not value:
        raise ValueError('MAINL CDG draw layout: '+message)


def native_image(raw,leaf,index,offset):
    code,_ = code_bytes(raw,index)
    image,names,fields,report = bytearray(code),[],[],[]
    block = None
    for r in parse_omf(raw):
        if r.name=='EXTDEF':
            at = 0
            while at<len(r.data):
                n = r.data[at]
                names.append(r.data[at+1:at+n+1].decode())
                at += n+2
        if r.name=='LEDATA':
            block = (r.data[0],int.from_bytes(r.data[1:3],'little'))
        if r.name!='FIXUPP':
            continue
        need(block[0]==index,'all fields belong to whole CODE')
        at = 0
        while at<len(r.data):
            loc,low,method,target = r.data[at:at+4]
            at += 4
            site = block[1]+(loc&3)*256+low
            width = 4 if loc&0xFC==0xCC else 2
            need(loc&0xFC in (0xC4,0xCC) and method in (0x54,0x56) and site+width<=len(code),'literal native field grammar')
            addend = int.from_bytes(code[site:site+width],'little')
            fields.append((site,loc,method,target,addend))
            if method==0x54:
                need(target==index and width==2,'real self-CS WORD offset')
                value,name = offset+addend,'SHARED'
            else:
                name = names[target-1]
                need(addend==0 and name in ('GRCG_SETCOLOR','_cdg_slots','_hflip_lut'),'reviewed external binding')
                need(width==(4 if name=='GRCG_SETCOLOR' else 2),'literal far or DATA WORD width')
                value = dict(GRCG_SETCOLOR=COLOR,_cdg_slots=SLOTS,_hflip_lut=LUT)[name]
            image[site:site+width]=value.to_bytes(width,'little')
            report.append(dict(offset=site,locat=loc,fixdat=method,target=target,name=name,addend=addend,width=width))
    need(tuple(names)==EXTERNALS[leaf] and tuple(fields)==FIELDS[leaf],'complete ordered fields and all external identities')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    root = Path(__file__).resolve().parents[2]
    text = (work/'obj/th03/mainl.map').read_text().replace(chr(92),'/')
    owners,native = [],[]
    for leaf,source,index,offset,size,procedures in PRODUCERS:
        obj,wrapper = 'obj/th03/'+leaf+'.obj','th03/'+leaf+'.asm'
        raw = (work/obj).read_bytes()
        d = describe_omf(raw)
        need(d['valid'] and d['translator_comments']==['Turbo Assembler  Version 5.0'],'complete native TASM identity')
        expected = [('CDG_PUT_TEXT','CODE',0),('_DATA','DATA',0),('SHARED','CODE',382)] if index==3 else [('SHARED','CODE',114)]
        need([(s['name'],s['class'],s['size']) for s in segment_definitions(raw)]==expected
             and [r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF']==[0x48]*len(expected),'WORD/PUBLIC/USE16 producers; no private DATA/BSS')
        need([b['size'] for b in code_bytes(raw,index)[1]]==[size]
             and code_publics(raw,index)==[(a,n) for _,n,a,_ in procedures],'one complete CODE record and whole public inventory')
        row, = [r for r in graph if r['output']==obj]
        need((row['source'],row['wrapper'],row['game'],row['binary'],row['first_binary'])==(source,wrapper,3,'O','op'),'actual GAME3/O first-use source slot')
        deps = [n.replace(chr(92),'/') for n in d['dependency_paths']]
        need(source in deps and wrapper in deps and files[source]==(work/source).read_bytes()
             and files[source].replace(b'\r\n',b'\n')==(root/source).read_bytes().replace(b'\r\n',b'\n'),'actual maintained source consumption and transport')
        need(len(re.findall(rf'(?m)^\s*0C7E:{offset:04X}\s+{size:04X}\s+C=CODE\s+S=SHARED\s+G=\(none\)\s+M={re.escape(wrapper)}\s+ACBP=48\s*$',text))==1,'literal whole-producer MAP allocation')
        image,fields = native_image(raw,leaf,index,offset)
        start = CS*16+offset
        need(image==target.program_image[start:start+size]==candidate.program_image[start:start+size],'complete independently resolved native producer bytes')
        need(len(re.findall(rb'(?im)^\s*even\s*$',files[source]))==(4 if index==3 else 2),'ordinary source EVEN directives, including internal loop alignment')
        native.append(dict(object=obj,code_bytes=size,fields=fields,private_data_bytes=0,private_bss_bytes=0))
        for kind,symbol,at,count in procedures:
            body = image[at:at+count]
            instructions = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(body,offset+at))
            by = {i.address:i for i in instructions}
            need(sum(i.size for i in instructions)==count and (instructions[-1].mnemonic,instructions[-1].op_str)==('retf','6'),'complete far Pascal procedure')
            need(len(re.findall(rf'(?m)^\s*0C7E:{offset+at:04X}\s+{symbol}\s*$',text))==2,'both owner MAP publics')
            for writer,patch in zip(WRITERS[kind],PATCHES[kind]):
                i = by[offset+at+writer]
                need(i.mnemonic=='mov' and i.op_str.startswith('word ptr cs:')
                     and f'0x{offset+at+patch:x}' in i.op_str,'every native SMC writer targets its own immediate WORD')
                consumer, = [i for i in instructions if i.address+1==offset+at+patch and i.size==3]
                need(consumer.mnemonic=='mov','entire MOV immediate is the source SMC destination')
            expected_relocs = [(CS,offset+f['offset']+2) for f in fields if f['width']==4 and at<=f['offset']<at+count]
            for mz in (target,candidate):
                need([(r.segment,r.offset) for r in mz.relocations if start+at<=r.linear<start+at+count]==expected_relocs,'complete literal ordered MZ fields')
            digest = hashlib.sha256(body).hexdigest()
            owners.append(dict(unit_id='th03-mainl-decoded-cdg-put-'+kind,name=symbol,source=source,object=obj,
                start=start+at,size=count,segment=CS,offset=offset+at,coordinate_space='decoded-load',canonical_file_offset=None,
                target_sha256=digest,candidate_sha256=digest,ordered_relocations=[list(r) for r in expected_relocs],argument_bytes=6,callee_pop_bytes=6,
                private_data_bytes=0,private_bss_bytes=0,abi='far Pascal; WORD coordinates/slot; real SMC immediate words; flat bus operand contract'))
    for symbol,segment,offset in (('_cdg_slots',DS,SLOTS),('_hflip_lut',DS,LUT),('GRCG_SETCOLOR',0,COLOR)):
        need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+{symbol}\s*$',text))==2,'both external MAP publics')
    for offset in EXCLUDED:
        need(target.program_image[CS*16+offset]==candidate.program_image[CS*16+offset]==0x90,'separate natural outer EVEN byte')
    return dict(owners=owners,functions=3,code_bytes=493,native_objects=native,ordered_native_field_count=19,
                mz_relocation_count=2,self_modifying_WORDs=12,excluded_outer_EVEN_bytes=list(EXCLUDED),
                natural_producer_bytes=496,private_data_bytes=0,private_bss_bytes=0,
                enclosing_alignment_accepted=False,lookup_or_hardware_accepted=False,whole_product_accepted=False)
