#!/usr/bin/env python3
"""Whole original xx carrier,front/RTTI bodies and compiler storage ownership."""
import json
from pathlib import Path
import re
import struct
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
import probe_th03_mainl_xx_dispatch as native
from probe_th03_mainl_xx_rtti import DRIVER,SOURCE,FRONT,UNIT,SUPPORT,REPORT,NAMES,wrapper,context
from review_th03_mainl_xx_throw import BODIES as THROW_BODIES
from review_th03_mainl_xx_catch import dense,BODIES as CATCH_BODIES
from review_th03_mainl_xx_types import BODIES as TYPE_BODIES,compatible_codegen
from review_th03_mainl_xx_calls import BODIES as CALL_BODIES,ACCEPTED_SHA
from review_th03_mainl_xx_dispatch import BODIES as DISPATCH_BODIES
from review_th03_mainl_xx_destruction import BODIES as DESTROY_BODIES
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_resources_work import cold_context,need,sha
from build_th03_mainl_work import WORK
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_acceptance import proof_inputs
from lib.decoded_mainl_xx_rtti_probe import run,CASES
from lib.omf import describe_omf,parse_omf
from lib.pc98 import parse_mz
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

REVIEW='.analysis/work/mainl-xx-rtti-review.json'
BASE,SIZE=0x580D,12622
FRONT_BODIES=[('__JumpToCatch__',0x580D,12,'far'),('typeIDname',0x5819,37,'far')]
TAIL_BODIES=[('_CurrExcContext',0x8294,85,'far'),('__ThrowFileName',0x82E9,18,'far'),
    ('__ThrowLineNumber',0x82FB,14,'far'),('__ThrowExceptionName',0x8309,18,'far'),
    ('typeinfo::typeinfo',0x831B,110,'far'),('typeinfo::operator=',0x8389,15,'far'),
    ('typeinfo::~typeinfo',0x8398,52,'far'),('typeinfo::operator==',0x83CC,38,'far'),
    ('typeinfo::operator!=',0x83F2,33,'far'),('typeinfo::before',0x8413,120,'far'),
    ('typeinfo::name',0x848B,26,'far'),('__GetTypeInfo',0x84A5,131,'far'),
    ('searchBaseClass',0x8528,582,'near'),('__DynamicCast',0x876E,357,'far')]


def all_bodies(listing):
    rows=[]
    for at,symbol,kind in re.findall(r'^\s*\d+\s+([0-9A-F]{4})\s+(\S+)\s+proc\s+(far|near)\s*$',listing,re.M):
        ends=re.findall(r'^\s*\d+\s+([0-9A-F]{4})\s+'+re.escape(symbol)+r'\s+endp\s*$',listing,re.M)
        need(len(ends)==1,'actual complete native function '+symbol)
        rows.append(dict(name=symbol,start=int(at,16),size=int(ends[0],16)-int(at,16),return_kind=kind))
    need(len(rows)==50,'all50 original source procedures present,without extra helper definitions')
    return rows


def initialized_payload(raw):
    result=payload(raw);iterated=[]
    for record in parse_omf(raw):
        if record.name!='LIDATA':continue
        data=record.data;segment=data[0];offset=int.from_bytes(data[1:3],'little');cursor=3
        def block():
            nonlocal cursor
            need(cursor+4<=len(data),'complete actual LIDATA block header')
            repeat,count=struct.unpack('<2H',data[cursor:cursor+4]);cursor+=4
            if count:
                value=b''.join(block() for _ in range(count))
            else:
                need(cursor<len(data),'actual LIDATA literal count')
                size=data[cursor];cursor+=1
                need(cursor+size<=len(data),'complete actual LIDATA literal')
                value=data[cursor:cursor+size];cursor+=size
            need(len(value)*repeat<=SIZE,'bounded actual iterated CODE initializer')
            return value*repeat
        value=b''
        while cursor<len(data):value+=block()
        for i,b in enumerate(value):
            need((segment,offset+i) not in result,'disjoint native LEDATA/LIDATA bytes')
            result[segment,offset+i]=b
        iterated.append(dict(segment=segment,offset=offset,size=len(value),record_data_hex=data.hex()))
    return result,iterated


def destruction_codegen(original,candidate,old,rows):
    """Compare real object bytes; explain local CALL operands without erasing them."""
    op,p=payload(original),payload(candidate)
    a,b=old[35],rows[35]
    need(a['name']=='dtorCleanup' and '@dtorCleanup$' in b['name'] and
        a['size']==b['size']==1035,'complete original/current cleanup extents')
    starts=[a['start']-BASE,b['start']]
    raw=[bytes(data[1,start+i] for i in range(1035)) for data,start in zip((op,p),starts)]
    need(raw[0][:8]==raw[1][:8]==bytes.fromhex('558bec83ec205657'),
        'original32-byte cleanup frame,without an induction-pointer local')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    decoded=[list(decoder.disasm(data,start)) for data,start in zip(raw,starts)]
    need([i.size for i in decoded[0]]==[i.size for i in decoded[1]] and
        sum(i.size for i in decoded[0])==1035,'same complete instruction boundaries')
    local_names=('findTrueTypeAndAddr','destroyArray','destroyVariable','callMemberFunc')
    current_targets={}
    for name in local_names:
        selected=[q for q in rows if q['name'].startswith('@'+name+'$')]
        need(len(selected)==1,'actual compiler procedure identity: '+name)
        current_targets[selected[0]['start']]=name
    targets=[{q['start']-BASE:q['name'] for q in old},current_targets]
    calls=[]
    for x,y in zip(*decoded):
        at=x.address-starts[0]
        if x.mnemonic!='call':
            need(x.bytes==y.bytes,'literal cleanup instruction bytes at '+hex(at))
            continue
        need(x.size==y.size==3 and x.bytes[0]==y.bytes[0]==0xE8,
            'real local near CALL encodings')
        dest=[(i.address+3+int.from_bytes(i.bytes[1:],'little',signed=True))&65535
            for i in (x,y)]
        names=[table.get(address) for table,address in zip(targets,dest)]
        need(names[0] is not None and names[0]==names[1],
            'cleanup CALL resolves to the same actual source procedure')
        calls.append(dict(offset=at,target=names[0],original_target=dest[0],
            candidate_target=dest[1],original_hex=x.bytes.hex(),candidate_hex=y.bytes.hex()))
    need([q['target'] for q in calls]==['findTrueTypeAndAddr','findTrueTypeAndAddr',
        'destroyArray','destroyVariable','callMemberFunc'],'all five local cleanup calls')
    fields=[]
    expected={40:'@__RefDestructorCount$qv',932:'@$bdla$qnv',996:'@$bdele$qnv'}
    for obj,start in zip((original,candidate),starts):
        selected=[f for f in literal_fields(obj) if f['segment']==1 and start<=f['site']<start+1035]
        need(len(selected)==3,'all three literal cleanup fields,in native order')
        for f in selected:
            need(f==dict(segment=1,site=f['site'],location_type=3,width=4,
                segment_relative=True,frame_method=5,frame=None,target_method=2,
                target=f['target'],addend=0) and
                externs(obj)[f['target']-1]==expected.get(f['site']-start),
                'actual cleanup runtime interface and original/current field shape')
        fields.append(selected)
    # The declaration precedes member_type,but initialization follows its load.
    # Both the array search and its multiply retain the native BP[-30]/[-34] slots.
    need(rows[32]['name'].startswith('@destroyVariable$'),'actual member-search owner')
    member=[bytes(data[1,start+0x19A+i] for i in range(72)) for data,start in
        [(op,old[32]['start']-BASE),(p,rows[32]['start'])]]
    need(member[0]==member[1],'all72 raw member-search/array-count bytes')
    differences=[dict(offset=i,original=x,candidate=y) for i,(x,y) in
        enumerate(zip(*raw)) if x!=y]
    return dict(original_bytes=1035,candidate_bytes=1035,stack_bytes=32,
        original_raw_sha256=sha(raw[0]),candidate_raw_sha256=sha(raw[1]),
        complete_object_raw_equal=raw[0]==raw[1],raw_byte_differences=differences,
        all1025_bytes_outside_local_call_operands_equal=True,local_calls=calls,
        original_and_candidate_literal_fields=fields,
        literal_field_offset_order=[[f['site']-start for f in ff] for ff,start in zip(fields,starts)],
        destroyVariable_member_search_raw_bytes=72)


def baseline(root):
    raw=(root/'.analysis/work/mainl-xx-throw-build.json').read_bytes();r=json.loads(raw)
    reviewed=(root/'.analysis/work/mainl-xx-throw-review.json').read_bytes();p=json.loads(reviewed)
    need(p['complete'] and not p['source_acceptance'] and p['accepted_source_bytes']==0 and p['selected_build_report_sha256']==sha(raw) and p['review_driver_sha256']==sha((root/'scripts/review_th03_mainl_xx_throw.py').read_bytes()),'current reviewed throw baseline receipt')
    need(r['complete'] and r['driver_sha256']==sha((root/native.DRIVER).read_bytes()) and r['compiler_flags']==native.FLAGS and r['compiler']==compiler_context(root),'unchanged current shared native recipe/profile')
    need(p['source_sha256']==r['source_sha256'] and r['source_sha256']=={n:sha((root/n).read_bytes()) for n in r['source_sha256']} and r['probe_support_sha256']=={n:sha((root/n).read_bytes()) for n in r['probe_support_sha256']},'baseline product banks/header and probe bindings')
    need(r['profile_driver_sha256']=={n:sha((root/n).read_bytes()) for n in r['profile_driver_sha256']},'unchanged independent baseline profile')
    vectors=[]
    for row in r['rounds']:
        v={}
        for key,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'retained complete baseline raw native output');v[key]=b
        vectors.append(v)
    need(len(vectors)==2 and {k:v for k,v in vectors[0].items() if k!='listing'}=={k:v for k,v in vectors[1].items() if k!='listing'},'reused whole raw baseline pair; no ancestor runtime replay')
    for phase in r['native_phases']:need(sha((root/('.analysis/work/xx-throw-'+phase['label']+'.log')).read_bytes())==phase['log_sha256'],'retained original baseline phase log')
    return sha(reviewed)


def review(root,report=None):
    root=Path(root);cold_context(root);baseline_sha=baseline(root)
    accepted_raw=(root/'config/mainl_work/scoped_acceptance.json').read_bytes();accepted=json.loads(accepted_raw)
    need(sha(accepted_raw)==ACCEPTED_SHA and accepted['proof_inputs']==proof_inputs(root) and len(accepted['audit']['scope']['owners'])==211 and sum(o['size'] for o in accepted['audit']['scope']['owners'])==36946,'unchanged accepted211-owner publication and verifier inputs')
    raw=(root/REPORT).read_bytes();r=json.loads(raw) if report is None else report
    need(r['complete'] and not r['source_acceptance'] and r['accepted_source_bytes']==0 and r['miniature_only'] and not r['whole_product_linked'] and not r['whole_product_cold_rebuilt'],'unaccepted whole DOS xx miniature,not normal-library exactness')
    sources=dict(NAMES,**{'xx_abi.h':native.HEADER,'xxunit.cpp':UNIT})
    current_wrapper=wrapper(b'')
    need(r['source_sha256']=={n:sha((root/n).read_bytes()) for n in sources.values()} and r['driver_sha256']==sha((root/native.DRIVER).read_bytes()) and r['profile_driver_sha256']=={DRIVER:sha((root/DRIVER).read_bytes())} and r['probe_support_sha256']=={SUPPORT:sha((root/SUPPORT).read_bytes())},'maintained banks,common builder,independent profile and focused probe source')
    need(r['compiler']==compiler_context(root) and r['compiler_flags']==native.FLAGS and r['available_SDK_header_sha256']==native.sdk_inventory(root),'current scoped compiler/profile/all64 available SDK headers')
    need(r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()) and r['wrapper_sha256']==sha(current_wrapper),'unchanged cold report and original relative same-TU source order')
    need((root/'.analysis/work/xx-rtti-wrapper.cpp').read_bytes()==current_wrapper and (root/'.analysis/work/xx-rtti-mini.lnk').read_bytes()==native.LINK,'actual compiler wrapper and link response')
    for short,path in sources.items():need((root/('.analysis/work/xx-rtti-source-'+short)).read_bytes()==(root/path).read_bytes(),'actual source transport: '+short)
    cfg=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/cfg['paths']['wine_prefix'];dos=['/usr/bin/wine-stable',str(root/cfg['paths']['msdos_player']),'-e','-x'];tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t'];phases=[]
    for number in (1,2):
        for label,cmd in [('compile',dos+[r'C:\BC45\BCC.EXE',*native.FLAGS,'xxdisp.cpp']),('assemble',tasm+['/l','xxdisp.asm','xxdisp.obj']),('context',tasm+['xxctx.asm','xxctx.obj']),('mini-link',dos+['tlink','@xxmini.lnk'])]:phases.append((f'round{number}-{label}',cmd,0))
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'two actual serial native compiler/assembler/mini-link rounds')
    for p in r['native_phases']:
        log=(root/('.analysis/work/xx-rtti-'+p['label']+'.log')).read_bytes();need(sha(log)==p['log_sha256'],'whole native phase log')
        if p['label'].endswith('compile'):need(log.startswith(r['compiler']['banner'].encode()+b'\r\n'),'actual scoped BCC banner')
    expected={'@$bdele','@$bdla','@__RefDestructorCount','___InitExceptBlocks','___ExitExceptBlocks','___call_unexpected','__8086','@$bnew','_memcmp','_strcmp','_abort','_free','_malloc','_memcpy','_memset','___call_terminate','N_LXMUL@','N_LUDIV@'}
    vectors=[];bodies=[]
    for row in r['rounds']:
        need(set(row['outputs'])=={'asm','obj','context','exe','map','listing'},'five complete raw native outputs plus unmodified listing');v={}
        for key,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'whole actual raw output identity');v[key]=b
        imports=externs(v['obj']);ctx=context(imports)
        need(len(imports)==18 and {n.rsplit('$',1)[0] for n in imports}==expected and '__Global_unwind' not in imports and '___JumpToCatch__' not in imports,'all22 original public interfaces resolve;only original18 runtime/library/CPU imports remain')
        need(row['unresolved_imports']==imports and row['context_sha256']==sha(ctx) and (root/'.analysis/work/xx-rtti-context.asm').read_bytes()==ctx,'actual trap-only diagnostic context without helper models')
        need(describe_omf(v['obj'])['valid'] and describe_omf(v['context'])['valid'],'complete actual native OMF structure');bodies.append(all_bodies(v['listing'].decode()));vectors.append(v)
    need({k:v for k,v in vectors[0].items() if k!='listing'}=={k:v for k,v in vectors[1].items() if k!='listing'} and bodies[0]==bodies[1],'whole raw ASM/two-OBJ/EXE/MAP repeat without output normalization; page clocks kept separately')
    v=vectors[0];candidate=parse_mz(v['exe']);target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());need(candidate.valid and target.valid,'real native mini MZ and fixed Japanese decoded target')
    definitions=segment_definitions(v['obj']);size=definitions[0]['size'];p,iterated=initialized_payload(v['obj'])
    need(definitions[1:]==[dict(index=i,name=n,**{'class':k},overlay='',size=s) for i,n,k,s in [(2,'_DATA','DATA',18),(3,'_BSS','BSS',10)]],'natural complete DATA18/BSS10,including packed pair of one-byte exception values')
    need(len([q for q in p if q[0]==1])==size and bytes(p[2,i] for i in range(18))==b'<notype>\0**BCCxh1\0' and not any(q[0]==3 for q in p),'dense actual CODE,all18 DATA bytes and genuinely uninitialized BSS10')
    original=(WORK/'vendor/xx.obj').read_bytes();op=payload(original);fields=literal_fields(original);original_map=(WORK/'obj/th03/mainl.map').read_text();image=bytearray(op[1,i] for i in range(SIZE));mz=[]
    need(segment_definitions(original)==[dict(index=i,name=n,**{'class':k},overlay='',size=s) for i,n,k,s in [(1,'_TEXT','CODE',12622),(2,'_DATA','DATA',18),(3,'_BSS','BSS',10)]] and bytes(op[2,i] for i in range(18))==bytes(p[2,i] for i in range(18)),'actual original three-segment carrier and complete initialized DATA equality')
    for seg,off,length,kind,name in [(0,BASE,SIZE,'CODE','_TEXT'),(0xE3F,0x1172,18,'DATA','_DATA'),(0xE3F,0x2876,10,'BSS','_BSS')]:
        pattern=rf'^\s*{seg:04X}:{off:04X}\s+{length:04X}\s+C={kind}\s+S={name}\s+G=\S+\s+M=xx\s+ACBP=\S+\s*$'
        need(len(re.findall(pattern,original_map,re.M))==1,'real original module segment placement: '+name)
    aliases={'@__RefDestructorCount$qv':'__refdestructorcount()','@$bnew$qui':'operator new(unsigned int)','@$bdele$qnv':'operator delete(void far*)','@$bdla$qnv':'operator delete[](void far*)'}
    for f in fields:
        at=f['site'];absolute=BASE+at
        need(f['segment']==1 and at+f['width']<=SIZE,'all original literal native fields belong to complete CODE')
        if f['target_method']==2:
            name=externs(original)[f['target']-1];seg,off=address(original_map,aliases.get(name,name));off+=f['addend']
        else:
            need(f['target_method']==0 and f['target'] in (1,2,3),'real original CODE/DATA/BSS target')
            seg,base={1:(0,BASE),2:(0xE3F,0x1172),3:(0xE3F,0x2876)}[f['target']];off=base+f['addend']
        if (f['frame_method'],f['frame'])==(1,1):
            need((f['location_type'],f['width'],f['segment_relative'])==(1,2,True) and seg==0xE3F,'original literal DGROUP offset')
            image[at:at+2]=off.to_bytes(2,'little');continue
        need((f['frame_method'],f['frame'])==(5,None) and seg==0,'original CODE frame')
        if f['location_type']==3:
            need(f['width']==4 and f['segment_relative'],'original far field')
            if image[at-1]==0x9A:image[at-1:at+4]=b'\x90\x0e\xe8'+((off-absolute-4)&65535).to_bytes(2,'little')
            else:image[at:at+4]=struct.pack('<2H',off,seg);mz.append(absolute+2)
        elif f['location_type']==2:
            need(f['width']==2 and f['segment_relative'],'original segment WORD');image[at:at+2]=seg.to_bytes(2,'little');mz.append(absolute)
        else:
            need(f['location_type']==1 and f['width']==2,'original offset/displacement WORD')
            image[at:at+2]=(off if f['segment_relative'] else (off-absolute-2)&65535).to_bytes(2,'little')
    need(bytes(op[2,i] for i in range(18))==target.program_image[0xF562:0xF574],'all18 initialized original DATA bytes agree with fixed target')
    need(len(fields)==187 and bytes(image)==target.program_image[BASE:BASE+SIZE] and mz==[q.linear for q in target.relocations if BASE<=q.linear<BASE+SIZE],'entire12622 original CODE bytes and literal ordered187 fields/MZ vector independently reproduced')
    t=target.program_image;decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    old_defs=FRONT_BODIES+[('sameTypeID',0x583E,157,'far')]+TYPE_BODIES+[(n,a,s,'near') for n,a,s,_ in CALL_BODIES]+THROW_BODIES+CATCH_BODIES+[(n,0x72B3+a,s,'near' if k=='ret' else 'far') for n,a,s,k in DISPATCH_BODIES]+DESTROY_BODIES+TAIL_BODIES
    old=[dict(name=n,start=a,size=s,return_kind=k) for n,a,s,k in old_defs];rows=bodies[0]
    need(len(old)==len(rows)==50 and all(a['return_kind']==b['return_kind'] for a,b in zip(old,rows)),'original50 complete procedures and native near/far conventions')
    dense(t,old,decoder);dense(candidate.program_image,rows,decoder)
    destruction=destruction_codegen(original,v['obj'],old,rows)
    need(rows[4]['size']==372 and rows[4]['name'].startswith('@compatibleType$') and
        rows[2]['name'].startswith('@sameTypeID$') and rows[3]['name'].startswith('@findBaseType$'),
        'actual compiler compatibility helper identities and complete extent')
    compatibility=compatible_codegen(original,v['obj'],rows[4]['start'],rows[2]['start'],rows[3]['start'])
    def gaps(procedures,start,end):
        result=[];cursor=start
        for row in procedures:
            need(row['start']>=cursor,'disjoint complete procedure ownership')
            if row['start']>cursor:result.append([cursor,row['start']-cursor])
            cursor=row['start']+row['size']
        need(cursor<=end,'functions fit actual segment')
        if cursor<end:result.append([cursor,end-cursor])
        return result
    old_gaps=gaps(old,BASE,BASE+SIZE);new_gaps=gaps(rows,0,size)
    need([n for a,n in old_gaps]==[96,48,102,42,12,8,90,136] and [n for a,n in new_gaps[:-1]]==[96,48,102,42,12,8,90] and sum(row['size'] for row in old)==12088,'entire original/candidate carrier partitions into50 bodies and534 compiler/semantic storage bytes')
    pubs=code_publics(v['obj'],1);original_pubs=code_publics(original,1)
    need(len(pubs)==22 and [n for a,n in pubs]==[n for a,n in original_pubs] and all(a in {q['start'] for q in rows} for a,n in pubs),'all22 original public mangled interfaces,including real catch register jump')
    candidate_fields=literal_fields(v['obj']);imports=externs(v['obj'])
    need(set(imports)==set(externs(original)) and len(imports)==18,'whole TU has exactly the original18 external interfaces')
    candidate_mz=[]
    for field in candidate_fields:
        if field['segment']!=1:continue
        at=field['site']
        if field['location_type']==2:candidate_mz.append(at)
        elif field['location_type']==3 and p[1,at-1]!=0x9A:candidate_mz.append(at+2)
    need(candidate_mz==[q.linear for q in candidate.relocations] and len(candidate_mz)==20,'literal ordered candidate20 MZ words from actual native fields,not sorted or normalized')
    # Compiler-native RTTI data has a typed20/22/21/12/60 layout plus an
    # optional compiler-emitted byte. TASM relaxation can change final parity;
    # do not infer the emitted initializer from the final label's alignment.
    # Nothing is
    # copied into product source;these are actual labels in generated output.
    labels=['@$xt$8Bad_cast','@$xt$10Bad_typeid','@$xt$n8typeinfo','@typeinfo@4','@$xt$8typeinfo']
    def label(symbol):
        found=re.findall(r'^\s*\d+\s+([0-9A-F]{4})\s+'+re.escape(symbol)+r'\s+label\s+\w+\s*$',v['listing'].decode(),re.M)
        need(len(found)==1,'actual compiler RTTI label: '+symbol);return int(found[0],16)
    positions=[label(n) for n in labels];metadata=new_gaps[-1]
    padding=re.findall(r'^\s*db\s+(\d+) dup \(0\)\s*\n@typeinfo@4\s+label\s+byte\s*$',v['asm'].decode(),re.M)
    need(len(padding)<=1 and all(p=='1' for p in padding),'actual compiler-emitted zero initializer before the vtable')
    padding_bytes=int(padding[0]) if padding else 0
    expected_iterated=([dict(segment=1,offset=positions[3]-1,size=1,record_data_hex='01'+(positions[3]-1).to_bytes(2,'little').hex()+'01000100010000000100')]
        if padding_bytes else [])
    need(iterated==expected_iterated,'only an actually emitted compiler alignment byte has a native LIDATA owner')
    need(positions[:3]==[metadata[0]+o for o in (0,20,42)] and positions[3]==positions[2]+21+padding_bytes and positions[4]==positions[3]+12 and positions[4]+60==size,'all generated RTTI/vtable bytes and actual compiler-emitted initializer have reviewed ownership')
    for data,at,vt,dtor in [(t,0x88D3,0x8913,0x8398),(candidate.program_image,metadata[0],positions[3],rows[42]['start'])]:
        need(struct.unpack('<5H',data[at:at+10])==(1,1,10,0xFFFF,0) and data[at+10:at+20]==b'Bad_cast\0\0','complete Bad_cast descriptor')
        need(struct.unpack('<5H',data[at+20:at+30])==(1,1,10,0xFFFF,0) and data[at+30:at+42]==b'Bad_typeid\0\0','complete Bad_typeid descriptor')
        need(struct.unpack('<3H',data[at+42:at+48])==(4,0x2010,10) and data[at+52:at+63]==b'typeinfo *\0' and all(b==0 for b in data[at+63:vt]),'far pointer descriptor,literal name and actual alignment byte if emitted')
        need(data[vt+4:vt+8]==b'\0'*4 and data[vt+12+38:vt+12+48]==b'typeinfo\0\0' and data[vt+12+48:vt+12+60]==b'\0'*12,'vtable offsets,typeinfo name and three terminated descriptor lists')
        need(struct.unpack('<2H',data[at+48:at+52])==(vt+12,0) and struct.unpack('<2H',data[vt:vt+4])==(vt+12,0) and struct.unpack('<2H',data[vt+8:vt+12])==(dtor,0),'literal generated type/vtable/destructor far pointers')
        need(struct.unpack('<19H',data[vt+12:vt+50])==(8,3,38,0,0x1073,48,52,0,0,0,0,0,0,1,1,dtor,0,5,56),'complete generated typeinfo descriptor header and destructor ABI')
    allocations=[]
    for data,row in [(t,old[18]),(candidate.program_image,rows[18])]:
        need(data[row['start']:row['start']+14]==bytes.fromhex('50515253545556571e068bec81ec'),'unchanged compiler saveregs frame prefix')
        allocations.append(int.from_bytes(data[row['start']+14:row['start']+16],'little'))
    need(allocations==[390,342],'48-byte original/current frame ownership gap remains open;no ancestor runtime replay')
    reused_flags=json.loads((root/'.analysis/work/mainl-xx-throw-review.json').read_bytes())['alternate_saved_eflags_observations']
    old_before=old[45]['start']-BASE;new_before=rows[45]['start']
    need(old[45]['size']==rows[45]['size']==120 and bytes(op[1,old_before+i] for i in range(120))==bytes(p[1,new_before+i] for i in range(120)),'complete unmodified120-byte typeinfo::before object bodies agree before native linking')
    before_fields=[]
    for raw_object,body_start,all_fields in [(original,old_before,fields),(v['obj'],new_before,candidate_fields)]:
        selected=[f for f in all_fields if f['segment']==1 and body_start<=f['site']<body_start+120]
        need(len(selected)==1,'one literal original/current before field')
        f=selected[0]
        need(f==dict(segment=1,site=body_start+96,location_type=3,width=4,segment_relative=True,frame_method=5,frame=None,target_method=2,target=f['target'],addend=0) and externs(raw_object)[f['target']-1]=='_strcmp','actual original/current far strcmp field;literal differing EXTDEF indices retained')
        before_fields.append(selected)
    probes=[]
    for kind in CASES:
        index=49 if kind in CASES[:3] else 47 if kind==CASES[3] else 0
        pair=[run(t,old[index]['start'],kind,0x8528),run(candidate.program_image,rows[index]['start'],kind,rows[48]['start'])]
        need(pair[0]==pair[1],'actual original/source RTTI ABI: '+kind);probes.append(pair)
    raw_equal=candidate.program_image[:size]==t[BASE:BASE+SIZE]
    return dict(complete=True,source_acceptance=False,accepted_source_bytes=0,accepted_publication_sha256=ACCEPTED_SHA,reused_baseline_receipt_sha256=baseline_sha,review_driver_sha256=sha((root/'scripts/review_th03_mainl_xx_rtti.py').read_bytes()),selected_build_report_sha256=sha(raw),source_sha256=r['source_sha256'],profile_driver_sha256=r['profile_driver_sha256'],
        original_CODE_bytes=SIZE,original_instruction_bytes=12088,original_inline_data_bytes=534,original_DATA_bytes=18,original_BSS_bytes=10,original_bodies=old,original_literal_native_fields=fields,original_MZ_words=mz,original_storage_gaps=old_gaps,
        candidate_CODE_segment_bytes=size,candidate_DATA_bytes=18,candidate_BSS_bytes=10,candidate_bodies=rows,candidate_literal_native_fields=candidate_fields,candidate_MZ_words=candidate_mz,candidate_storage_gaps=new_gaps,candidate_LIDATA_records=iterated,complete_CODE_raw_equal=raw_equal,complete_DATA_raw_equal=True,
        all22_original_public_interfaces=True,original18_imports=imports,whole_xx_source_graph_present=True,maintained_translation_unit=UNIT,original_RTTI_metadata_bytes=136,candidate_RTTI_metadata_bytes=metadata[1],candidate_RTTI_compiler_padding_bytes=padding_bytes,all_RTTI_metadata_bytes_owned=True,target_and_source_RTTI_probes=probes,two_whole_raw_vectors_repeated=True,all_available_SDK_headers_bound=64,
        source_exactness_open=True,saved_eflags_gap_remains=reused_flags[0]!=reused_flags[1],reused_alternate_saved_eflags_observations=reused_flags,RaiseException_stack_allocations=allocations,before_object_body_raw_equal=True,original_and_candidate_before_fields=before_fields,destruction_codegen=destruction,compatibility_codegen=compatibility,whole_product_linked=False,original_cold_rebuilt=False,ancestor_runtime_chain_rebuilt=False,physical_DOS_execution_claimed=False)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];r=review(root);(root/REVIEW).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('source_sha256','original_literal_native_fields','candidate_literal_native_fields','original_bodies','candidate_bodies')},indent=2))
