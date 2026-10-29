#!/usr/bin/env python3
"""Review actual DOS compatibility rules and the contiguous descriptor bank."""
import json
from pathlib import Path
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
import probe_th03_mainl_xx_dispatch as native
from probe_th03_mainl_xx_types import DRIVER,SOURCE,SUPPORT,REPORT,wrapper
from review_th03_mainl_xx_catch import parsed_bodies,dense,BODIES as CATCH_BODIES,EQUAL,CATCH
from review_th03_mainl_xx_calls import call_bodies,classify,CALLS,DESTROY,ACCEPTED_SHA
from review_th03_mainl_xx_destruction import source_bodies
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_resources_work import cold_context,need,sha
from build_th03_mainl_work import WORK
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_acceptance import proof_inputs
from lib.decoded_mainl_xx_types_probe import run,CASES
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

REVIEW='.analysis/work/mainl-xx-types-review.json'
BASE,SIZE,XX_BASE=0x58DB,1121,0x580D
BODIES=[('findBaseType',0x58DB,339,'near'),('compatibleType',0x5A2E,372,'near'),
    ('allocExceptMem',0x5BA2,92,'far'),('freeExceptMem',0x5BFE,57,'far'),
    ('typeIDcaught',0x5C37,261,'near')]


def baseline(root):
    raw=(root/'.analysis/work/mainl-xx-catch-build.json').read_bytes();r=json.loads(raw)
    reviewed=(root/'.analysis/work/mainl-xx-catch-review.json').read_bytes();p=json.loads(reviewed)
    need(p['complete'] and not p['source_acceptance'] and p['accepted_source_bytes']==0 and p['selected_build_report_sha256']==sha(raw) and p['review_driver_sha256']==sha((root/'scripts/review_th03_mainl_xx_catch.py').read_bytes()),'current reviewed catch baseline receipt')
    need(r['complete'] and r['driver_sha256']==sha((root/native.DRIVER).read_bytes()) and r['compiler_flags']==native.FLAGS and r['compiler']==compiler_context(root),'unchanged current shared native recipe/profile')
    need(p['source_sha256']==r['source_sha256'] and r['source_sha256']=={n:sha((root/n).read_bytes()) for n in r['source_sha256']} and r['probe_support_sha256']=={n:sha((root/n).read_bytes()) for n in r['probe_support_sha256']},'baseline product banks/header and probe bindings')
    vectors=[]
    for row in r['rounds']:
        v={}
        for key,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'retained complete baseline raw native output');v[key]=b
        vectors.append(v)
    need(len(vectors)==2 and {k:v for k,v in vectors[0].items() if k!='listing'}=={k:v for k,v in vectors[1].items() if k!='listing'},'reused whole raw baseline pair; no ancestor runtime replay')
    for phase in r['native_phases']:need(sha((root/('.analysis/work/xx-catch-'+phase['label']+'.log')).read_bytes())==phase['log_sha256'],'retained original baseline phase log')
    return sha(reviewed)


def review(root,report=None):
    root=Path(root);cold_context(root);baseline_sha=baseline(root)
    accepted_raw=(root/'config/mainl_work/scoped_acceptance.json').read_bytes();accepted=json.loads(accepted_raw)
    need(sha(accepted_raw)==ACCEPTED_SHA and accepted['proof_inputs']==proof_inputs(root) and len(accepted['audit']['scope']['owners'])==211 and sum(o['size'] for o in accepted['audit']['scope']['owners'])==36946,'unchanged accepted211-owner publication and verifier inputs')
    raw=(root/REPORT).read_bytes();r=json.loads(raw) if report is None else report
    need(r['complete'] and not r['source_acceptance'] and r['accepted_source_bytes']==0 and r['miniature_only'] and not r['whole_product_linked'] and not r['whole_product_cold_rebuilt'],'unaccepted DOS types miniature,not normal-library exactness')
    sources={'xxbank.inl':native.SOURCE,'xx_abi.h':native.HEADER,'xxdtor.inl':DESTROY,'xxcall.inl':CALLS,'xxeq.inl':EQUAL,'xxcatch.inl':CATCH,'xxtypes.inl':SOURCE}
    base=(native.WRAPPER.replace(b'int near dtorCleanup',b'static int near dtorCleanup')+b'#include "xxdtor.inl"\n').replace(native.CATCH_INTERFACES,b'').replace(b'#include "xxbank.inl"',b'#include "xxeq.inl"\n#include "xxcall.inl"\n#include "xxcatch.inl"\n#include "xxbank.inl"')
    current_wrapper=wrapper(base)
    need(r['source_sha256']=={n:sha((root/n).read_bytes()) for n in sources.values()} and r['driver_sha256']==sha((root/native.DRIVER).read_bytes()) and r['profile_driver_sha256']=={DRIVER:sha((root/DRIVER).read_bytes())} and r['probe_support_sha256']=={SUPPORT:sha((root/SUPPORT).read_bytes())},'maintained banks,common builder,independent profile and focused probe source')
    need(r['compiler']==compiler_context(root) and r['compiler_flags']==native.FLAGS and r['available_SDK_header_sha256']==native.sdk_inventory(root),'current scoped compiler/profile/all64 available SDK headers')
    need(r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()) and r['wrapper_sha256']==sha(current_wrapper),'unchanged cold report and original relative same-TU source order')
    need((root/'.analysis/work/xx-types-wrapper.cpp').read_bytes()==current_wrapper and (root/'.analysis/work/xx-types-mini.lnk').read_bytes()==native.LINK,'actual compiler wrapper and link response')
    for short,path in sources.items():need((root/('.analysis/work/xx-types-source-'+short)).read_bytes()==(root/path).read_bytes(),'actual source transport: '+short)
    cfg=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/cfg['paths']['wine_prefix'];dos=['/usr/bin/wine-stable',str(root/cfg['paths']['msdos_player']),'-e','-x'];tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t'];phases=[]
    for number in (1,2):
        for label,cmd in [('compile',dos+[r'C:\BC45\BCC.EXE',*native.FLAGS,'xxdisp.cpp']),('assemble',tasm+['/l','xxdisp.asm','xxdisp.obj']),('context',tasm+['xxctx.asm','xxctx.obj']),('mini-link',dos+['tlink','@xxmini.lnk'])]:phases.append((f'round{number}-{label}',cmd,0))
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'two actual serial native compiler/assembler/mini-link rounds')
    for p in r['native_phases']:
        log=(root/('.analysis/work/xx-types-'+p['label']+'.log')).read_bytes();need(sha(log)==p['log_sha256'],'whole native phase log')
        if p['label'].endswith('compile'):need(log.startswith(r['compiler']['banner'].encode()+b'\r\n'),'actual scoped BCC banner')
    expected={'@$bdele','@$bdla','@__RefDestructorCount','___InitExceptBlocks','___ExitExceptBlocks','___call_unexpected','__Global_unwind','___JumpToCatch__','_abort','_free','_malloc','_memcpy','_memset','___call_terminate','N_LXMUL@','N_LUDIV@'}
    vectors=[];bodies=[]
    for row in r['rounds']:
        need(set(row['outputs'])=={'asm','obj','context','exe','map','listing'},'five complete raw native outputs plus unmodified listing');v={}
        for key,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'whole actual raw output identity');v[key]=b
        imports=externs(v['obj']);context=native.trap_context(imports)
        need(len(imports)==16 and {n.rsplit('$',1)[0] for n in imports}==expected and not any(n.startswith('@typeIDcaught$') for n in imports),'last private type-match edge resolves; remaining16 library/runtime interfaces are traps')
        need(row['unresolved_imports']==imports and row['context_sha256']==sha(context) and (root/'.analysis/work/xx-types-context.asm').read_bytes()==context,'actual trap-only diagnostic context without helper models')
        need(describe_omf(v['obj'])['valid'] and describe_omf(v['context'])['valid'],'complete actual native OMF structure');bodies.append(parsed_bodies(v['listing'].decode(),BODIES));vectors.append(v)
    need({k:v for k,v in vectors[0].items() if k!='listing'}=={k:v for k,v in vectors[1].items() if k!='listing'} and bodies[0]==bodies[1],'whole raw ASM/two-OBJ/EXE/MAP repeat without output normalization; page clocks kept separately')
    v=vectors[0];candidate=parse_mz(v['exe']);target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());need(candidate.valid and target.valid,'real native mini MZ and fixed Japanese decoded target')
    defs=segment_definitions(v['obj']);size=defs[0]['size'];need(defs[1:]==[dict(index=i,name=n,**{'class':k},overlay='',size=s) for i,n,k,s in [(2,'_DATA','DATA',0),(3,'_BSS','BSS',8)]],'no invented DATA/BSS or emergency-buffer storage owner')
    p=payload(v['obj']);need(len([q for q in p if q[0]==1])==size and not any(q[0] in (2,3) for q in p),'dense actual candidate CODE and no DATA/BSS initializers')
    original=(WORK/'vendor/xx.obj').read_bytes();op=payload(original);fields=[f for f in literal_fields(original) if f['segment']==1 and BASE-XX_BASE<=f['site']<BASE-XX_BASE+SIZE];image=bytearray(op[1,BASE-XX_BASE+i] for i in range(SIZE));original_map=(WORK/'obj/th03/mainl.map').read_text()
    need(len(fields)==3 and [externs(original)[f['target']-1] for f in fields]==['_abort','_malloc','_free'],'three literal original allocator fields in original emission order')
    for f in fields:
        at=f['site']-(BASE-XX_BASE);absolute=BASE+at
        need((f['location_type'],f['width'],f['segment_relative'],f['frame_method'],f['frame'],f['target_method'],f['addend'])==(3,4,True,5,None,2,0) and at+4<=SIZE and image[at-1]==0x9A,'complete real original far call field')
        seg,off=address(original_map,externs(original)[f['target']-1]);need(seg==0,'actual original library CODE frame');image[at-1:at+4]=b'\x90\x0e\xe8'+((off-absolute-4)&65535).to_bytes(2,'little')
    need(bytes(image)==target.program_image[BASE:BASE+SIZE] and not any(BASE<=q.linear<BASE+SIZE for q in target.relocations),'all1121 original bytes independently resolved; no MZ words or hidden data')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;old=[dict(name=n,start=a,size=s,return_kind=k) for n,a,s,k in BODIES];rows=bodies[0]
    dense(target.program_image,old,decoder);dense(candidate.program_image,rows,decoder)
    need(old[0]['start']==BASE and old[-1]['start']+old[-1]['size']==BASE+SIZE and all(a['start']+a['size']==b['start'] for a,b in zip(old,old[1:])),'complete five-procedure original bank with no tables/padding')
    equal=parsed_bodies(v['listing'].decode(),[('sameTypeID',0x583E,157,'far')])[0];call_rows=call_bodies(v['listing'].decode());_,covered=classify(candidate.program_image,call_rows,decoder);catch=parsed_bodies(v['listing'].decode(),CATCH_BODIES);dispatch=catch[-1]['start']+catch[-1]['size'];pubs=code_publics(v['obj'],1)
    need(rows[0]['start']==equal['start']+equal['size'] and all(a['start']+a['size']==b['start'] for a,b in zip(rows,rows[1:])) and rows[-1]['start']+rows[-1]['size']==call_rows[0]['start'] and set(covered)==set(range(call_rows[0]['start'],catch[0]['start']-42)),'natural comparator/types/call/EH adjacency without manufactured gaps')
    need(pubs==[(catch[2]['start'],'@_CatchCleanup$qv')]+[(dispatch+o,n) for o,n in [(459,'__Local_unwind'),(491,'__Return_unwind'),(673,'__ExceptionHandler')]],'original public ABI only; all five new procedures stay private')
    for at,name in pubs:need(address(v['map'].decode(),'_catchcleanup()' if name=='@_CatchCleanup$qv' else name)==(0,at),'actual linked public address')
    destroys=source_bodies(v['listing'].decode());need(destroys[0]['start']==dispatch+1566+78 and destroys[-1]['start']+destroys[-1]['size']==size,'complete same-TU dispatch/destruction tail')
    type_entry=rows[-1]['start'];calls=[]
    for off,count in [(533,132),(673,881)]:
        for i in decoder.disasm(candidate.program_image[dispatch+off:dispatch+off+count],dispatch+off):
            if i.mnemonic=='call' and i.operands[0].type==X86_OP_IMM and i.operands[0].imm==type_entry:calls.append(i.address)
    need(len(calls)==2,'both matcher/dispatcher direct near calls enter the actual private typeIDcaught body')
    probes=[]
    for kind in CASES:
        pair=[run(target.program_image,0x5BFE if kind=='emergency-free' else 0x5C37,0x583E,kind),run(candidate.program_image,rows[3]['start'] if kind=='emergency-free' else type_entry,equal['start'],kind)]
        need(pair[0]==pair[1],'actual original/source type rule and near/far frame: '+kind);probes.append(pair)
    return dict(complete=True,source_acceptance=False,accepted_source_bytes=0,accepted_publication_sha256=ACCEPTED_SHA,reused_baseline_receipt_sha256=baseline_sha,review_driver_sha256=sha((root/'scripts/review_th03_mainl_xx_types.py').read_bytes()),selected_build_report_sha256=sha(raw),source_sha256=r['source_sha256'],profile_driver_sha256=r['profile_driver_sha256'],
        original_bank_base=BASE,original_bank_size=SIZE,original_instruction_bytes=SIZE,original_inline_data_bytes=0,original_bodies=old,original_literal_native_fields=fields,original_MZ_words=0,
        candidate_bank_bytes=rows[-1]['start']+rows[-1]['size']-rows[0]['start'],candidate_CODE_segment_bytes=size,candidate_bodies=rows,candidate_literal_native_fields=literal_fields(v['obj']),complete_bank_raw_equal=candidate.program_image[rows[0]['start']:rows[-1]['start']+rows[-1]['size']]==target.program_image[BASE:BASE+SIZE],
        actual_dispatch_type_calls=calls,same_TU_type_match_edge_resolved=True,unresolved_interfaces=externs(v['obj']),target_and_source_type_probes=probes,two_whole_raw_vectors_repeated=True,all_available_SDK_headers_bound=64,
        whole_product_linked=False,original_cold_rebuilt=False,ancestor_runtime_chain_rebuilt=False,physical_DOS_execution_claimed=False)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];r=review(root);(root/REVIEW).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('source_sha256','original_literal_native_fields','candidate_literal_native_fields')},indent=2))
