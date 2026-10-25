"""The complete five-procedure CDG TU and its natural TC4/TLINK call bridges."""
import hashlib
import re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics

CS, DS, START, SIZE = 0xC7E, 0xE3F, 0x73E, 593
SOURCE, WRAPPER, OBJECT = 'src/shared/formats/cdg_load.cpp', 'th03/cdg_load.cpp', 'obj/th03/cdg_load.obj'
SLOTS, FLAG = 0x1D0E, 0x894
PROCEDURES = (('single',0,138,8,'CDG_LOAD_SINGLE'),('single_noalpha',138,134,8,'CDG_LOAD_SINGLE_NOALPHA'),
              ('all',272,230,6,'CDG_LOAD_ALL'),('all_noalpha',502,28,6,'CDG_LOAD_ALL_NOALPHA'),('free',530,63,2,'CDG_FREE'))
ENTRIES = {name:(START+at,size,args) for name,at,size,args,_ in PROCEDURES}
EXTERNALS = ('HMEM_ALLOCBYTE','HMEM_FREE','FILE_ROPEN','FILE_READ','FILE_SEEK','FILE_CLOSE','_cdg_slots','_cdg_noalpha')
CALLS = {'alloc':0x21AE,'free':0x22B2,'open':0x966,'read':0x8B2,'seek':0x9A2,'close':0x846}
FIELDS = ((568,206,86,None,2,0),(542,198,22,1,7,0),(523,198,22,1,8,0),(507,197,22,1,8,0),
 (492,205,86,None,6,0),(469,205,86,None,4,0),(450,205,86,None,1,0),(439,205,86,None,5,0),
 (419,205,86,None,4,0),(404,205,86,None,1,0),(396,197,22,1,8,0),(332,205,84,None,1,530),
 (311,205,86,None,4,0),(302,197,22,1,7,0),(291,205,84,None,1,530),(283,205,86,None,3,0),
 (262,205,86,None,6,0),(257,205,86,None,4,0),(238,204,86,None,1,0),(222,204,86,None,5,0),
 (209,204,86,None,5,0),(177,204,86,None,4,0),(168,204,86,None,3,0),(159,196,22,1,7,0),
 (149,204,84,None,1,530),(128,204,86,None,6,0),(123,204,86,None,4,0),(104,204,86,None,1,0),
 (93,204,86,None,4,0),(78,204,86,None,1,0),(71,204,86,None,5,0),(39,204,86,None,4,0),
 (30,204,86,None,3,0),(21,196,22,1,7,0),(11,204,84,None,1,530))


def need(value,message):
    if not value:
        raise ValueError('MAINL CDG layout: '+message)


def native_image(raw):
    code,_ = code_bytes(raw,1)
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
        need(block[0]==1,'all native fields in CODE')
        at = 0
        while at<len(r.data):
            loc,low,method = r.data[at:at+3]
            at += 3
            frame = r.data[at] if method==0x16 else None
            at += int(frame is not None)
            index = r.data[at]
            at += 1
            site = block[1]+(loc&3)*256+low
            width = 2 if method==0x16 else 4
            need((loc&0xFC,method,frame) in ((0xC4,0x16,1),(0xCC,0x56,None),(0xCC,0x54,None))
                 and site+width<=len(code),'literal native width/frame/method')
            addend = int.from_bytes(code[site:site+width],'little')
            fields.append((site,loc,method,frame,index,addend))
            if method==0x16:
                need(index in (7,8) and addend==0,'literal external DATA field')
                image[site:site+2]=(SLOTS if index==7 else FLAG).to_bytes(2,'little')
                name = EXTERNALS[index-1]
            elif method==0x56:
                need(1<=index<=6 and addend==0,'literal external root far field')
                value = tuple(CALLS.values())[index-1]
                image[site:site+4]=value.to_bytes(4,'little')
                name = EXTERNALS[index-1]
            else:
                need(index==1 and addend==530 and code[site-1:site+4]==b'\x9a\x12\x02\0\0','real symbolic forward CDG_FREE far field')
                displacement = (START+530-(START+site+4))&65535
                image[site-1:site+4]=b'\x90\x0e\xe8'+displacement.to_bytes(2,'little')
                name = 'CDG_FREE'
            report.append(dict(offset=site,locat=loc,fixdat=method,frame=frame,target=index,name=name,addend=addend,
                               width=width,normal_tlink_relaxed_call=method==0x54))
    need(tuple(names)==EXTERNALS and tuple(fields)==FIELDS,'complete ordered literal field and external identity vectors')
    # TC4 already knows the earlier-defined all-loader here. Its ordinary C++
    # call emits PUSH CS / near CALL without an OMF field or a separator NOP.
    need(code[517:521]==b'\x0e\xe8\x07\xff','natural backward same-TU call')
    return bytes(image),report


def verify(work,target,candidate,graph,files):
    root = Path(__file__).resolve().parents[2]
    raw = (work/OBJECT).read_bytes()
    d = describe_omf(raw)
    need(d['valid'] and d['translator_comments']==['TC86 Borland C++ 4.02'],'native TC4 identity')
    need(segment_definitions(raw)==[dict(index=1,name='SHARED',**{'class':'CODE'},overlay='',size=593),
        dict(index=2,name='_DATA',**{'class':'DATA'},overlay='',size=0),dict(index=3,name='_BSS',**{'class':'BSS'},overlay='',size=0)],
        'whole CODE and zero private DATA/BSS')
    need([r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF']==[0x28,0x48,0x48]
         and [b['size'] for b in code_bytes(raw,1)[1]]==[593]
         and code_publics(raw,1)==[(a,symbol) for _,a,_,_,symbol in PROCEDURES],'native BYTE alignment, one complete record and all publics')
    row, = [r for r in graph if r['output']==OBJECT]
    need((row['source'],row['wrapper'],row['game'],row['binary'],row['first_binary'])==(SOURCE,WRAPPER,3,'O','op'),'actual GAME3/O first-use producer')
    need(SOURCE in d['dependency_paths'] and WRAPPER in d['dependency_paths']
         and files[SOURCE]==(work/SOURCE).read_bytes()
         and files[SOURCE].replace(b'\r\n',b'\n')==(root/SOURCE).read_bytes().replace(b'\r\n',b'\n'),'maintained source consumption and transport')
    text = (work/'obj/th03/mainl.map').read_text()
    need(len(re.findall(r'(?m)^\s*0C7E:073E\s+0251\s+C=CODE\s+S=SHARED\s+G=\(none\)\s+M=th03/cdg_load.cpp\s+ACBP=28\s*$',text))==1,'literal whole producer MAP allocation')
    image,fields = native_image(raw)
    start = CS*16+START
    need(image==target.program_image[start:start+SIZE]==candidate.program_image[start:start+SIZE],'complete independently linked native bytes')
    owners = []
    for name,at,count,args,symbol in PROCEDURES:
        need(len(re.findall(rf'(?m)^\s*0C7E:{START+at:04X}\s+{symbol}\s*$',text))==2,'both complete owner MAP publics')
        body = image[at:at+count]
        ins = list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(body,START+at))
        need(sum(i.size for i in ins)==count and (ins[-1].mnemonic,ins[-1].op_str)==('retf',str(args)), 'complete far Pascal procedure')
        expected = [(CS,START+f['offset']+2) for f in fields if f['fixdat']==0x56 and at<=f['offset']<at+count]
        for mz in (target,candidate):
            observed = [(r.segment,r.offset) for r in mz.relocations if start+at<=r.linear<start+at+count]
            need(observed==expected,'literal complete ordered MZ relocation vector')
        h = hashlib.sha256(body).hexdigest()
        owners.append(dict(unit_id='th03-mainl-decoded-cdg-load-'+name.replace('_','-'),name=symbol,source=SOURCE,object=OBJECT,
            start=start+at,size=count,segment=CS,offset=START+at,coordinate_space='decoded-load',canonical_file_offset=None,
            target_sha256=h,candidate_sha256=h,ordered_relocations=[list(r) for r in expected],argument_bytes=args,callee_pop_bytes=args,
            private_data_bytes=0,private_bss_bytes=0,abi='far Pascal; WORD slot and signed index; BYTE image count and flag; real nested calls'))
    for symbol,offset in (('_cdg_slots',SLOTS),('_cdg_noalpha',FLAG)):
        need(len(re.findall(rf'(?m)^\s*0E3F:{offset:04X}\s+{symbol}\s*$',text))==2,'both external DATA MAP publics')
    for symbol,offset in zip(EXTERNALS,tuple(CALLS.values())):
        need(len(re.findall(rf'(?m)^\s*0000:{offset:04X}\s+{symbol}\s*$',text))==2,'both external root MAP publics')
    return dict(owners=owners,functions=5,code_bytes=593,ordered_native_fields=fields,mz_relocation_count=24,
                normal_tlink_relaxed_calls=4,compiler_backward_bridge_calls=1,private_data_bytes=0,private_bss_bytes=0,
                enclosing_DATA_or_interfaces_accepted=False,whole_product_accepted=False)
