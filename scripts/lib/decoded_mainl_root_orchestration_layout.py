"""Complete current root/continue producers with distinct uncredited table/storage."""
import hashlib
import re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf, parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_bytes, code_publics
from review_th03_mainl_root import analyze, TABLE, TABLE_WORDS
from lib.decoded_mainl_root_orchestration_inventory import ROOTDATA, CONTMENU

CS, DS = 0x95F, 0xE3F
PRODUCERS = (
    ('rootdata', 'src/mainl/root/complete_data.cpp', 3, 'ROOTPRE_TEXT', 2458, 0xA2, 112, 0x133C, 186, ROOTDATA),
    ('contmenu', 'src/mainl/root/continue.cpp', 0x99D, 'CUTSCENE_TEXT', 417, 0x906, 0, 0x27EA, 0, CONTMENU),
)
PREFIX = (('cfg_resident', 3, 49), ('win_load', 0x34, 282), ('win_text', 0x14E, 56))


def need(value, message):
    if not value:
        raise ValueError('MAINL root orchestration: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def transport(source, raw):
    raw=raw.replace(b'\r\n', b'\n')
    if source=='src/mainl/root/continue.cpp':
        need(raw.count(b'-zCCONTINUE_TEXT')==1, 'single declared continue segment transformation')
        raw=raw.replace(b'-zCCONTINUE_TEXT', b'-zCCUTSCENE_TEXT')
    return raw


def native(raw, inv, start, data, bss):
    originals={s:code_bytes(raw,s)[0] for s in (1,2) if any(b[0]==s for b in inv['blocks'])}
    images={s:bytearray(v) for s,v in originals.items()}
    names=[];fields=[];observations=[];block=None;blocks=[]
    for rec in parse_omf(raw):
        if rec.name=='EXTDEF':
            at=0
            while at<len(rec.data):
                n=rec.data[at];names.append(rec.data[at+1:at+n+1].decode())
                need(rec.data[at+n+1]==0, 'external type index');at+=n+2
        if rec.name=='LEDATA':
            block=(rec.data[0],int.from_bytes(rec.data[1:3],'little'),len(rec.data)-3)
            blocks.append(list(block))
        if rec.name!='FIXUPP':
            continue
        need(block is not None and block[0] in images, 'field in complete initialized segment')
        seg,base,length=block;at=0
        while at<len(rec.data):
            loc,low,method=rec.data[at:at+3];at+=3
            need(method in (0x14,0x16,0x56), 'explicit no-thread native fixup')
            frame=rec.data[at] if method in (0x14,0x16) else None
            at+=int(frame is not None);index=rec.data[at];at+=1
            site=base+(loc&3)*256+low;width=4 if loc&0xFC==0xCC else 2
            need(base<=site and site+width<=base+length, 'whole native field in LEDATA')
            addend=int.from_bytes(originals[seg][site:site+width],'little')
            fields.append([seg,site,loc,method,frame,index,addend])
            if method==0x14:
                need(seg==1 and loc&0xFC==0xC4 and index in (1,2,3)
                     and frame==(1 if index==1 else 2), 'local CODE/DATA/BSS group identity')
                value={1:start,2:data,3:bss}[index]+addend
                name={1:'local CODE',2:'local DATA',3:'local BSS'}[index]
            else:
                name,segment,offset,_=inv['bindings'][index-1]
                need(names[index-1]==name, 'literal external identity')
                if width==4:
                    need((loc&0xFC,method,frame,addend)==
                         ((0xCC,0x56,None,0) if seg==1 else (0xCC,0x16,2,0)),
                         'far CODE call or DGROUP-framed DATA pointer')
                    need(seg==1 or segment==DS, 'DATA pointers remain in DGROUP')
                    value=offset|(segment<<16)
                elif loc&0xFC==0x84:
                    need((seg,method,frame,segment,addend)==(1,0x16,1,CS,0), 'near external same CODE group')
                    value=(offset-(start+site+2))&0xFFFF
                else:
                    need((seg,loc&0xFC,method,frame,segment)==(1,0xC4,0x16,2,DS), 'DGROUP external WORD')
                    value=offset+addend
            images[seg][site:site+width]=value.to_bytes(width,'little')
            observations.append(dict(segment_index=seg,offset=site,locat=loc,fixdat=method,frame=frame,
                                     target=index,addend=addend,width=width,name=name))
    need(fields==inv['fields'] and blocks==inv['blocks'], 'complete ordered native fields/LEDATA')
    need(names==[v[0] for v in inv['bindings']], 'complete ordered external inventory')
    return {s:bytes(b) for s,b in images.items()},observations


def prefix_decode(image):
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;rows=[]
    far={(s,o) for _,s,o,_ in ROOTDATA['bindings'] if s!=DS}
    for name,offset,size in PREFIX:
        body=image[CS*16+offset:CS*16+offset+size]
        instructions=list(decoder.disasm(body,offset));bounds={i.address for i in instructions}
        need(instructions and sum(i.size for i in instructions)==size
             and (instructions[-1].mnemonic,instructions[-1].op_str)==('ret',''), 'complete prefix nearRET0 body')
        edges=[]
        for i in instructions:
            if i.mnemonic in ('ret','retf'):
                need((i.mnemonic,i.op_str)==('ret',''), 'prefix return convention')
            if not (i.mnemonic.startswith(('j','loop')) or i.mnemonic in ('call','lcall')):
                continue
            need(i.operands and all(o.type==X86_OP_IMM for o in i.operands), 'prefix direct edge')
            if i.mnemonic=='lcall':
                dest=tuple(o.imm for o in i.operands);need(dest in far,'prefix declared far external')
            else:
                need(i.mnemonic!='call' and i.operands[0].imm in bounds, 'prefix internal branch boundary')
                dest=(CS,i.operands[0].imm)
            edges.append(dict(instruction=i.address,kind=i.mnemonic,destination=dest))
        rows.append(dict(name=name,offset=offset,size=size,sha256=sha(body),instructions=len(instructions),
                         return_kind='ret',cleanup='',edges=edges))
    return rows


def verify(work,target,candidate,graph,files):
    root=Path(__file__).resolve().parents[2];text=(work/'obj/th03/mainl.map').read_text()
    observations=[];relocations=[];consumed=[]
    for obj,source,start,code_name,size,data,data_size,bss,bss_size,inv in PRODUCERS:
        path=f'obj/th03/{obj}.obj';wrapper=obj+'.cpp';raw=(work/path).read_bytes();d=describe_omf(raw)
        need(d['valid'] and d['module_name']==wrapper and d['translator_comments']==['TC86 Borland C++ 4.02']
             and d['dependency_paths']==inv['dependencies'] and d['record_counts']==inv['record_counts'],
             'complete compiler/dependency/record identity')
        need([(s['name'],s['class'],s['size']) for s in segment_definitions(raw)]==
             [(code_name,'CODE',size),('_DATA','DATA',data_size),('_BSS','BSS',bss_size)], 'complete producer partition')
        need([[r.name,list(r.data)] for r in parse_omf(raw) if r.name in ('LNAMES','GRPDEF','SEGDEF')]==inv['structural'],
             'literal segment/group identities and alignment')
        need([[list(p) for p in code_publics(raw,s)] for s in (1,2,3)]==inv['publics'], 'all CODE/DATA/BSS publics')
        row,=[r for r in graph if r['output']==path]
        need((row['source'],row['wrapper'],row['game'],row['binary'],row['first_binary'])==
             (source,wrapper,3,'L','mainl'), 'actual GAME3/L maintained producer')
        need(files[wrapper].replace(b'\r\n',b'\n')==transport(source,(root/source).read_bytes()),
             'exact maintained source and declared composer transformation')
        for name in inv['dependencies']:
            if name.startswith('C:\\TC4\\INCLUDE\\'):
                continue  # SDK inventory is independently bound by the complete cold-source audit.
            need(name in files and (work/name).read_bytes()==files[name], 'complete consumed staged input: '+name)
            if name.startswith('src/'):
                need(files[name].replace(b'\r\n',b'\n')==(root/name).read_bytes().replace(b'\r\n',b'\n'),
                     'literal maintained consumed source: '+name)
        for segment,offset,n,cls,seg,group in ((CS,start,size,'CODE',code_name,'GROUP_01'),
                (DS,data,data_size,'DATA','_DATA','DGROUP'),(DS,bss,bss_size,'BSS','_BSS','DGROUP')):
            need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+{n:04X}\s+C={cls}\s+S={seg}\s+G={group}\s+M={obj}.cpp\s+ACBP={(0x28 if cls=="CODE" else 0x48):02X}\s*$',text))==1,
                 'complete native allocation')
        for _,segment,offset,symbol in inv['bindings']:
            need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,
                 'both literal external MAP tables: '+symbol)
        for _,_,_,segment,offset,symbol in inv['public_map']:
            need(len(re.findall(rf'(?m)^\s*{segment:04X}:{offset:04X}\s+(?:idle\s+)?{re.escape(symbol)}\s*$',text))==2,
                 'both literal public MAP tables: '+symbol)
        images,fields=native(raw,inv,start,data,bss)
        for s,offset,segment,n in ((1,start,CS,size),(2,data,DS,data_size)):
            if not n:
                continue
            begin=segment*16+offset
            need(images[s]==target.program_image[begin:begin+n]==candidate.program_image[begin:begin+n],
                 'complete independently resolved CODE/DATA equality')
            expected=[(segment,offset+f['offset']+2) for f in fields if f['segment_index']==s and f['width']==4]
            for mz in (target,candidate):
                need([(r.segment,r.offset) for r in mz.relocations if begin<=r.linear<begin+n]==expected,
                     'literal ordered complete producer relocation vector')
            if s==1:
                relocations+=expected
        observations.append(dict(object=path,source=source,object_sha256=sha(raw),code_sha256=sha(images[1]),
            data_sha256=sha(images[2]) if data_size else None,fields=fields))
        consumed+=inv['dependencies']
    original=analyze(target.program_image)
    need(original==analyze(candidate.program_image),'existing nine complete root bodies and switch closure')
    prefix=prefix_decode(target.program_image)
    need(prefix==prefix_decode(candidate.program_image),'three complete cfg/win prefix bodies')
    rows=prefix+original['bodies']
    need(sum(r['size'] for r in rows)==2857 and sum(r['instructions'] for r in rows)==944,
         'twelve complete bodies /2857 instruction bytes/944 instructions')
    need(original['table']['offset']==TABLE==0x6AF and original['table']['words']==TABLE_WORDS,
         'distinct eighteen-byte switch context')
    need([f['offset'] for f in observations[0]['fields'] if f['segment_index']==1 and f['fixdat']==0x14 and f['frame']==1]
         ==[1724,1722,1720,1718,1716,1714,1712,1710,1708,1442], 'all nine switch destinations and dispatch field')
    owners=[]
    for row in rows:
        is_continue=row['name']=='continue_menu';inv=CONTMENU if is_continue else ROOTDATA
        obj,source,start,_,_,_,_,_,_,_=PRODUCERS[int(is_continue)]
        public,=[name for offset,name in inv['publics'][0] if start+offset==row['offset']]
        owners.append(dict(unit_id='th03-mainl-decoded-root-orchestration-'+row['name'].replace('_','-'),
            name=public,source=source,object=f'obj/th03/{obj}.obj',start=CS*16+row['offset'],size=row['size'],
            segment=CS,offset=row['offset'],coordinate_space='decoded-load',canonical_file_offset=None,
            target_sha256=row['sha256'],candidate_sha256=row['sha256'],
            ordered_relocations=[list(r) for r in relocations if row['offset']<=r[1]<row['offset']+row['size']],
            argument_bytes=int(row['cleanup'] or 0),callee_pop_bytes=int(row['cleanup'] or 0),
            private_data_bytes=0,private_bss_bytes=0,
            abi=('far cdecl noargs' if row['return_kind']=='retf' else 'near Pascal arguments/noargs')))
    need(len(relocations)==131 and sum(len(o['ordered_relocations']) for o in owners)==131,
         'complete selected relocation partition')
    return dict(owners=owners,functions=12,code_bytes=2857,instruction_count=944,boundaries=rows,
        producers=observations,ordered_native_field_count=313,mz_relocation_count=131,
        context_table=original['table'],context_code_bytes=18,context_data_bytes=112,context_bss_bytes=186,
        context_credited=False,consumed_paths=consumed,private_data_bytes=0,private_bss_bytes=0,
        physical_runtime_or_file_success_accepted=False,whole_product_accepted=False)
