#!/usr/bin/env python3
"""Review the original DOS catch bank and its private far type comparator."""
import json
from pathlib import Path
import re
import struct
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from probe_th03_mainl_xx_dispatch import DRIVER,SOURCE,HEADER,FLAGS,LINK,WRAPPER,CATCH_INTERFACES,trap_context,sdk_inventory
from review_th03_mainl_xx_calls import call_bodies,classify,ACCEPTED_SHA,CALLS,DESTROY
from review_th03_mainl_xx_destruction import source_bodies
from review_th03_mainl_xx_dispatch import CANDIDATE_SIZE
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_resources_work import cold_context,need,sha
from build_th03_mainl_work import WORK
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_acceptance import proof_inputs
from lib.decoded_mainl_xx_catch_probe import context,callbacks,run
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

REPORT='.analysis/work/mainl-xx-catch-build.json'
REVIEW='.analysis/work/mainl-xx-catch-review.json'
CATCH='src/mainl/crt/xx_catch.inl'
EQUAL='src/mainl/crt/xx_type_equal.inl'
PROBE='scripts/lib/decoded_mainl_xx_catch_probe.py'
BASE,SIZE,XX_BASE=0x6CEF,1476,0x580D
BODIES=[('destThrownValue',0x6D19,80,'near'),('exceptionHandled',0x6D69,216,'near'),
    ('_CatchCleanup',0x6E41,125,'far'),('findBaseAddress',0x6EBE,204,'near'),
    ('adjustClassAddress',0x6F8A,131,'far'),('initCatchArg',0x700D,678,'near')]


def parsed_bodies(listing,definitions):
    rows=[]
    for name,_,_,kind in definitions:
        found=re.findall(r'^\s*\d+\s+([0-9A-F]{4})\s+(@'+name+r'\$\S+)\s+proc\s+(far|near)\s*$',listing,re.M)
        need(len(found)==1 and found[0][2]==kind,'actual native entry: '+name)
        at,symbol,_=found[0];end=re.findall(r'^\s*\d+\s+([0-9A-F]{4})\s+'+re.escape(symbol)+r'\s+endp\s*$',listing,re.M)
        need(len(end)==1,'actual native end: '+name);rows.append(dict(name=name,start=int(at,16),size=int(end[0],16)-int(at,16),return_kind=kind))
    return rows


def dense(image,rows,decoder):
    for row in rows:
        at,count=row['start'],row['size'];ins=list(decoder.disasm(image[at:at+count],at));bounds={i.address for i in ins}
        need(sum(i.size for i in ins)==count and (ins[-1].mnemonic,ins[-1].op_str)==('ret' if row['return_kind']=='near' else 'retf',''),'complete original/source instruction body: '+row['name'])
        for i in ins:
            if i.mnemonic.startswith('j') and i.operands[0].type==X86_OP_IMM:need(i.operands[0].imm in bounds,'direct catch branch stays in this instruction body')


def previous_receipt(root):
    # Reuse the affected earlier miniature's current review and whole raw pair.
    # Do not re-run its ancestor runtime observations for every catch review.
    report=json.loads((root/'.analysis/work/mainl-xx-calls-build.json').read_bytes())
    receipt=json.loads((root/'.analysis/work/mainl-xx-calls-review.json').read_bytes())
    need(receipt['complete'] and not receipt['source_acceptance'] and receipt['accepted_source_bytes']==0 and receipt['review_driver_sha256']==sha((root/'scripts/review_th03_mainl_xx_calls.py').read_bytes()) and receipt['selected_build_report_sha256']==sha((root/'.analysis/work/mainl-xx-calls-build.json').read_bytes()),'current reviewed calls miniature receipt')
    need(report['complete'] and report['driver_sha256']==sha((root/DRIVER).read_bytes()) and report['compiler_flags']==FLAGS and report['compiler']==compiler_context(root),'affected baseline was rebuilt with current driver/profile')
    need(receipt['source_sha256']==report['source_sha256'] and report['source_sha256']=={n:sha((root/n).read_bytes()) for n in report['source_sha256']},'unchanged baseline source/header bindings')
    vectors=[]
    for row in report['rounds']:
        v={}
        for key,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'retained whole baseline native output');v[key]=b
        vectors.append(v)
    need(len(vectors)==2 and {k:v for k,v in vectors[0].items() if k!='listing'}=={k:v for k,v in vectors[1].items() if k!='listing'},'unchanged whole baseline pair; keep page clocks separate')
    return sha((root/'.analysis/work/mainl-xx-calls-review.json').read_bytes())


def review(root,report=None):
    root=Path(root);cold_context(root);baseline_sha=previous_receipt(root)
    publication_raw=(root/'config/mainl_work/scoped_acceptance.json').read_bytes();publication=json.loads(publication_raw)
    need(sha(publication_raw)==ACCEPTED_SHA and publication['proof_inputs']==proof_inputs(root) and len(publication['audit']['scope']['owners'])==211,'unchanged211-owner accepted publication and verifier inputs')
    raw=(root/REPORT).read_bytes();r=json.loads(raw) if report is None else report
    need(r['complete'] and not r['source_acceptance'] and r['accepted_source_bytes']==0 and r['miniature_only'] and not r['whole_product_linked'] and not r['whole_product_cold_rebuilt'],'unaccepted catch/type miniature,not a whole-TU replacement')
    sources={'xxbank.inl':SOURCE,'xx_abi.h':HEADER,'xxdtor.inl':DESTROY,'xxcall.inl':CALLS,'xxeq.inl':EQUAL,'xxcatch.inl':CATCH}
    wrapper=(WRAPPER.replace(b'int near dtorCleanup',b'static int near dtorCleanup')+b'#include "xxdtor.inl"\n').replace(CATCH_INTERFACES,b'').replace(b'#include "xxbank.inl"',b'#include "xxeq.inl"\n#include "xxcall.inl"\n#include "xxcatch.inl"\n#include "xxbank.inl"')
    need(r['source_sha256']=={n:sha((root/n).read_bytes()) for n in sources.values()} and r['driver_sha256']==sha((root/DRIVER).read_bytes()) and r['probe_support_sha256']=={PROBE:sha((root/PROBE).read_bytes())},'current product banks,ABI,driver and actual native callback fixture')
    need(r['compiler']==compiler_context(root) and r['compiler_flags']==FLAGS and r['available_SDK_header_sha256']==sdk_inventory(root),'current scoped compiler/profile/all64 available headers')
    need(r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()) and r['wrapper_sha256']==sha(wrapper),'unchanged cold report and correct static same-TU include order')
    need((root/'.analysis/work/xx-catch-wrapper.cpp').read_bytes()==wrapper and (root/'.analysis/work/xx-catch-mini.lnk').read_bytes()==LINK,'actual compiler wrapper and miniature link response')
    for short,path in sources.items():need((root/('.analysis/work/xx-catch-source-'+short)).read_bytes()==(root/path).read_bytes(),'actual compiler source transport: '+short)
    cfg=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/cfg['paths']['wine_prefix'];dos=['/usr/bin/wine-stable',str(root/cfg['paths']['msdos_player']),'-e','-x'];tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t'];phases=[]
    for number in (1,2):
        for label,cmd in [('compile',dos+[r'C:\BC45\BCC.EXE',*FLAGS,'xxdisp.cpp']),('assemble',tasm+['/l','xxdisp.asm','xxdisp.obj']),('context',tasm+['xxctx.asm','xxctx.obj']),('mini-link',dos+['tlink','@xxmini.lnk'])]:phases.append((f'round{number}-{label}',cmd,0))
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'two actual serial native rounds')
    for p in r['native_phases']:
        log=(root/('.analysis/work/xx-catch-'+p['label']+'.log')).read_bytes();need(sha(log)==p['log_sha256'],'whole actual native phase log')
        if p['label'].endswith('compile'):need(log.startswith(r['compiler']['banner'].encode()+b'\r\n'),'actual scoped BCC banner')
    vectors=[];bodies=[];equal=[]
    expected={'@$bdele','@$bdla','@__RefDestructorCount','___InitExceptBlocks','___ExitExceptBlocks','___call_unexpected','__Global_unwind','___JumpToCatch__','@typeIDcaught','_memcpy','_memset','___call_terminate','N_LXMUL@','N_LUDIV@'}
    for row in r['rounds']:
        need(set(row['outputs'])=={'asm','obj','context','exe','map','listing'},'five native outputs plus unmodified timestamped listing');v={}
        for key,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'complete raw native output identity');v[key]=b
        imports=externs(v['obj']);fixture=context(trap_context(imports))
        need(len(imports)==14 and {n.rsplit('$',1)[0] for n in imports}==expected,'real catch/copy edges resolve; memcpy/memset remain actual library calls')
        need(row['unresolved_imports']==imports and row['context_sha256']==sha(fixture) and (root/'.analysis/work/xx-catch-context.asm').read_bytes()==fixture,'actual unchanged TASM callback/trap source')
        need(describe_omf(v['obj'])['valid'] and describe_omf(v['context'])['valid'],'actual whole native OMF structure')
        text=v['listing'].decode();bodies.append(parsed_bodies(text,BODIES));equal.append(parsed_bodies(text,[('sameTypeID',0x583E,157,'far')])[0]);vectors.append(v)
    need({k:v for k,v in vectors[0].items() if k!='listing'}=={k:v for k,v in vectors[1].items() if k!='listing'} and bodies[0]==bodies[1] and equal[0]==equal[1],'whole raw ASM/two-OBJ/EXE/MAP repeat; listing clocks remain separate')
    v=vectors[0];candidate=parse_mz(v['exe']);target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());need(candidate.valid and target.valid,'actual mini MZ and fixed Japanese decoded target')
    definitions=segment_definitions(v['obj']);size=definitions[0]['size'];need(definitions[1:]==[dict(index=i,name=n,**{'class':k},overlay='',size=s) for i,n,k,s in [(2,'_DATA','DATA',0),(3,'_BSS','BSS',8)]] ,'no invented DATA or BSS file bytes')
    p=payload(v['obj']);need(len([k for k in p if k[0]==1])==size and not any(k[0] in (2,3) for k in p),'complete dense candidate CODE and no DATA/BSS initializers')
    rows=bodies[0];dispatch=rows[-1]['start']+rows[-1]['size'];pubs=code_publics(v['obj'],1)
    need(pubs==[(rows[2]['start'],'@_CatchCleanup$qv')]+[(dispatch+o,n) for o,n in [(459,'__Local_unwind'),(491,'__Return_unwind'),(673,'__ExceptionHandler')]],'one original C++ cleanup public plus original three dispatcher publics; other helpers stay private')
    for at,name in pubs:need(address(v['map'].decode(),'_catchcleanup()' if name=='@_CatchCleanup$qv' else name)==(0,at),'actual native linked public address')
    original=(WORK/'vendor/xx.obj').read_bytes();op=payload(original);fields=[f for f in literal_fields(original) if f['segment']==1 and BASE-XX_BASE<=f['site']<BASE-XX_BASE+SIZE];image=bytearray(op[1,BASE-XX_BASE+i] for i in range(SIZE));mz=[];original_map=(WORK/'obj/th03/mainl.map').read_text()
    for f in fields:
        at=f['site']-(BASE-XX_BASE);absolute=BASE+at;need(at+f['width']<=SIZE and (f['frame_method'],f['frame'])==(5,None),'complete original literal CODE field')
        if f['target_method']==2:
            name=externs(original)[f['target']-1];mapped={'@__RefDestructorCount$qv':'__refdestructorcount()'}.get(name,name);seg,off=address(original_map,mapped);need(seg==0 and f['addend']==0,'actual original runtime/library reference')
        else:
            need((f['target_method'],f['target'])==(0,1),'actual internal original CODE reference');seg,off=0,XX_BASE+f['addend']
        if f['location_type']==3:
            need(f['width']==4 and f['segment_relative'],'actual original far field')
            if image[at-1]==0x9A:image[at-1:at+4]=b'\x90\x0e\xe8'+((off-absolute-4)&65535).to_bytes(2,'little')
            else:image[at:at+4]=struct.pack('<2H',off,seg);mz.append(absolute+2)
        elif f['location_type']==2:
            need(f['width']==2 and f['segment_relative'],'actual original segment WORD');image[at:at+2]=seg.to_bytes(2,'little');mz.append(absolute)
        else:
            need(f['location_type']==1 and f['width']==2 and f['segment_relative'],'actual original offset WORD');image[at:at+2]=off.to_bytes(2,'little')
    need(len(fields)==13 and bytes(image)==target.program_image[BASE:BASE+SIZE] and mz==[q.linear for q in target.relocations if BASE<=q.linear<BASE+SIZE] and len(mz)==3,'all1476 original bytes independently resolved with13 literal ordered fields and three ordered MZ words')
    t=target.program_image;need(struct.unpack('<12H',t[BASE:BASE+24])==(0,0,0x6D51,0,0,0,0,0,0,0,0,0) and struct.unpack('<9H',t[0x6D07:0x6D19])==(0,0,0xFFE2,0,3,BASE,0,0,4),'complete42-byte original single try/catch metadata')
    old_rows=[dict(name=n,start=a,size=s,return_kind=k) for n,a,s,k in BODIES];old_equal=dict(name='sameTypeID',start=0x583E,size=157,return_kind='far');decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    dense(t,old_rows+[old_equal],decoder);dense(candidate.program_image,rows+[equal[0]],decoder)
    need(all(a['start']+a['size']==b['start'] for a,b in zip(old_rows,old_rows[1:])) and old_rows[-1]['start']+old_rows[-1]['size']==BASE+SIZE,'complete1434 original instruction-byte ownership after42 EH bytes')
    need(bytes(op[1,0x583E-XX_BASE+i] for i in range(157))==t[0x583E:0x58DB] and not [f for f in literal_fields(original) if f['segment']==1 and 0x583E-XX_BASE<=f['site']<0x58DB-XX_BASE] and not any(0x583E<=q.linear<0x58DB for q in target.relocations),'complete original comparator has157 instructions and no native fields')
    call_rows=call_bodies(v['listing'].decode());_,covered=classify(candidate.program_image,call_rows,decoder);catch_base=rows[0]['start']-42
    candidate_fields=literal_fields(v['obj']);imports=externs(v['obj'])
    memory_fields=[f for f in candidate_fields if f['segment']==1 and rows[-1]['start']<=f['site']<dispatch and f['target_method']==2 and imports[f['target']-1] in ('_memcpy','_memset')]
    need([imports[f['target']-1] for f in memory_fields].count('_memcpy')==2 and [imports[f['target']-1] for f in memory_fields].count('_memset')==1 and all(f['location_type']==3 and f['width']==4 for f in memory_fields),'actual source has the original two memcpy sites and one memset site,not intrinsic expansion')
    need(not [f for f in candidate_fields if f['segment']==1 and f['site']<equal[0]['size']],'candidate comparator has no native fields')
    need(equal[0]['start']==0 and set(covered)==set(range(equal[0]['size'],catch_base)) and len(covered)==catch_base-equal[0]['size'],'same-TU type comparator,call adapters and generated catch EH prefix abut naturally')
    need(all(a['start']+a['size']==b['start'] for a,b in zip(rows,rows[1:])) and source_bodies(v['listing'].decode())[0]['start']==dispatch+CANDIDATE_SIZE+78 and source_bodies(v['listing'].decode())[-1]['start']+source_bodies(v['listing'].decode())[-1]['size']==size,'full contiguous candidate catch/dispatch/destruction TU tail')
    cb=callbacks(v['context']);probes=[]
    for name,at,kind,symbol in [('initCatchArg',0x700D,'class-copy','_xx_probe_catch_ctor'),('_CatchCleanup',0x6E41,'catch-free','_xx_probe_catch_free'),('adjustClassAddress',0x6F8A,'virtual-base',None)]:
        source_at=next(row['start'] for row in rows if row['name']==name);pair=[run(t,at,kind,cb[symbol] if symbol else None),run(candidate.program_image,source_at,kind,cb[symbol] if symbol else None)];need(pair[0]==pair[1],'actual target/source catch traffic: '+kind);probes.append(pair)
    return dict(complete=True,source_acceptance=False,accepted_source_bytes=0,accepted_publication_sha256=ACCEPTED_SHA,reused_baseline_receipt_sha256=baseline_sha,review_driver_sha256=sha((root/'scripts/review_th03_mainl_xx_catch.py').read_bytes()),selected_build_report_sha256=sha(raw),source_sha256=r['source_sha256'],
        original_bank_base=BASE,original_bank_size=SIZE,original_instruction_bytes=1434,original_inline_EH_bytes=42,original_bodies=old_rows,original_comparator=old_equal,original_literal_native_fields=fields,original_MZ_sites=mz,
        candidate_CODE_segment_bytes=size,candidate_catch_bank_bytes=dispatch-catch_base,candidate_bodies=rows,candidate_comparator=equal[0],candidate_literal_native_fields=candidate_fields,candidate_memory_call_fields=memory_fields,
        complete_catch_bank_raw_equal=candidate.program_image[catch_base:dispatch]==t[BASE:BASE+SIZE],complete_comparator_raw_equal=candidate.program_image[:equal[0]['size']]==t[0x583E:0x58DB],same_TU_catch_copy_edges_resolved=True,
        unresolved_interfaces=externs(v['obj']),target_and_source_catch_probes=probes,two_whole_raw_vectors_repeated=True,all_available_SDK_headers_bound=64,diagnostic_listing_has_wall_clock_headers=True,
        whole_product_linked=False,original_cold_rebuilt=False,ancestor_runtime_chain_rebuilt=False,physical_DOS_execution_claimed=False)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];r=review(root);(root/REVIEW).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('source_sha256','original_literal_native_fields','candidate_literal_native_fields','candidate_memory_call_fields')},indent=2))
