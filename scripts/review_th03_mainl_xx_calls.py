#!/usr/bin/env python3
"""Bounded native review of the DOS copy/destructor/member call adapters."""
import json
from pathlib import Path
import re
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM,X86_OP_MEM,X86_REG_CS
from probe_th03_mainl_xx_dispatch import DRIVER,SOURCE,HEADER,FLAGS,LINK,WRAPPER,trap_context,sdk_inventory
from review_th03_mainl_xx_destruction import review as destruction_review,source_bodies,DESTROY
from review_th03_mainl_xx_dispatch import ACCEPTED_SHA
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_resources_work import cold_context,need,sha
from build_th03_mainl_work import WORK
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_xx_calls_probe import context,callbacks,run
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

REPORT='.analysis/work/mainl-xx-calls-build.json'
REVIEW='.analysis/work/mainl-xx-calls-review.json'
CALLS='src/mainl/crt/xx_calls.inl'
PROBE='scripts/lib/decoded_mainl_xx_calls_probe.py'
BASE,SIZE,XX_BASE=0x5D3C,1495,0x580D
BODIES=[('callCopyCtor',0x5D3C,750,[(0x602A,24),(0x605A,24)]),
    ('callDestructor',0x608A,392,[(0x6212,24)]),('callMemberFunc',0x6242,185,[(0x62FB,12)])]


def call_bodies(listing):
    rows=[]
    for name,_,_,_ in BODIES:
        begin=re.findall(r'^\s*\d+\s+([0-9A-F]{4})\s+(@'+name+r'\$\S+)\s+proc\s+near\s*$',listing,re.M)
        need(len(begin)==1,'actual TASM call-adapter entry: '+name)
        at,symbol=begin[0];end=re.findall(r'^\s*\d+\s+([0-9A-F]{4})\s+'+re.escape(symbol)+r'\s+endp\s*$',listing,re.M)
        need(len(end)==1,'actual TASM call-adapter end: '+name)
        rows.append(dict(name=name,start=int(at,16),size=int(end[0],16)-int(at,16)))
    return rows


def classify(image,rows,decoder):
    tables=[];bounds=set();occupied=[]
    for row,(_,_,_,expected_tables) in zip(rows,BODIES):
        at,count=row['start'],row['size'];ins=list(decoder.disasm(image[at:at+count],at));local={i.address for i in ins}
        need(sum(i.size for i in ins)==count and (ins[-1].mnemonic,ins[-1].op_str)==('ret',''),'complete near cdecl body: '+row['name'])
        occupied+=list(range(at,at+count));bounds|=local;found=[]
        for i in ins:
            if i.mnemonic.startswith('j') and i.operands[0].type==X86_OP_IMM:need(i.operands[0].imm in local,'call-adapter branch excludes tables and other bodies')
            if i.mnemonic=='jmp' and i.operands[0].type==X86_OP_MEM and i.operands[0].mem.segment==X86_REG_CS:found.append(i.operands[0].mem.disp)
        need(len(found)==len(expected_tables),'actual number of CS switch dispatches')
        # Tables may be emitted in reverse switch order. Their original physical
        # offsets and complete source field streams are retained independently.
        for table,(_,length) in zip(sorted(found),expected_tables):
            values=[int.from_bytes(image[table+j:table+j+2],'little') for j in range(0,length*2,2)]
            need(all(v in local for v in values),'each real switch WORD enters this procedure')
            occupied+=list(range(table,table+2*length));tables.append(dict(start=table,entries=values))
    need(len(occupied)==len(set(occupied)),'nonoverlapping call-adapter instructions and CS tables')
    return tables,occupied


def review(root,report=None):
    root=Path(root);destruction_review(root);cold_context(root)
    raw=(root/REPORT).read_bytes();r=json.loads(raw) if report is None else report
    need(r['complete'] and not r['source_acceptance'] and r['accepted_source_bytes']==0 and r['miniature_only'] and not r['whole_product_linked'] and not r['whole_product_cold_rebuilt'],'unaccepted call-adapter miniature; not whole-product exactness')
    sources={'xxbank.inl':SOURCE,'xx_abi.h':HEADER,'xxdtor.inl':DESTROY,'xxcall.inl':CALLS}
    wrapper=(WRAPPER.replace(b'int near dtorCleanup',b'static int near dtorCleanup')+b'#include "xxdtor.inl"\n').replace(b'#include "xxbank.inl"',b'#include "xxcall.inl"\n#include "xxbank.inl"')
    need(r['source_sha256']=={n:sha((root/n).read_bytes()) for n in sources.values()} and r['driver_sha256']==sha((root/DRIVER).read_bytes()) and r['probe_support_sha256']=={PROBE:sha((root/PROBE).read_bytes())},'current maintained banks,ABI,driver and native callback fixture')
    need(r['compiler']==compiler_context(root) and r['compiler_flags']==FLAGS and r['available_SDK_header_sha256']==sdk_inventory(root),'scoped native compiler/profile/all64 available headers')
    need(r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()) and r['wrapper_sha256']==sha(wrapper),'unchanged cold context and original same-TU source order')
    need((root/'.analysis/work/xx-calls-wrapper.cpp').read_bytes()==wrapper and (root/'.analysis/work/xx-calls-mini.lnk').read_bytes()==LINK,'actual compiler wrapper and miniature response')
    for short,path in sources.items():need((root/('.analysis/work/xx-calls-source-'+short)).read_bytes()==(root/path).read_bytes(),'actual source transport: '+short)
    cfg=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/cfg['paths']['wine_prefix'];dos=['/usr/bin/wine-stable',str(root/cfg['paths']['msdos_player']),'-e','-x'];tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t'];phases=[]
    for number in (1,2):
        for label,cmd in [('compile',dos+[r'C:\BC45\BCC.EXE',*FLAGS,'xxdisp.cpp']),('assemble',tasm+['/l','xxdisp.asm','xxdisp.obj']),('context',tasm+['xxctx.asm','xxctx.obj']),('mini-link',dos+['tlink','@xxmini.lnk'])]:phases.append((f'round{number}-{label}',cmd,0))
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'two actual serial native compiler/assembler/mini-link rounds')
    for phase in r['native_phases']:
        log=(root/('.analysis/work/xx-calls-'+phase['label']+'.log')).read_bytes();need(sha(log)==phase['log_sha256'],'whole actual native phase log')
        if phase['label'].endswith('compile'):need(log.startswith(r['compiler']['banner'].encode()+b'\r\n'),'actual BCC banner')
    vectors=[];bodies=[]
    expected_imports={'@$bdele','@$bdla','@__RefDestructorCount','@_CatchCleanup','___InitExceptBlocks','___ExitExceptBlocks','@typeIDcaught','@exceptionHandled','@initCatchArg','___call_unexpected','__Global_unwind','___JumpToCatch__','___call_terminate','N_LXMUL@','N_LUDIV@'}
    for round in r['rounds']:
        need(set(round['outputs'])=={'asm','obj','context','exe','map','listing'},'five full native outputs plus original diagnostic listing');v={}
        for key,m in round['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'whole native raw output identity');v[key]=b
        imports=externs(v['obj']);fixture=context(trap_context(imports))
        need(len(imports)==15 and {n.rsplit('$',1)[0] for n in imports}==expected_imports,'both destruction call edges now resolve inside xx TU;15 other interfaces remain open')
        need(round['unresolved_imports']==imports and round['context_sha256']==sha(fixture) and (root/'.analysis/work/xx-calls-context.asm').read_bytes()==fixture,'complete actual trap/callback fixture transport')
        need(describe_omf(v['obj'])['valid'] and describe_omf(v['context'])['valid'],'whole real native OMF structure')
        bodies.append(call_bodies(v['listing'].decode()));vectors.append(v)
    need({k:v for k,v in vectors[0].items() if k!='listing'}=={k:v for k,v in vectors[1].items() if k!='listing'} and bodies[0]==bodies[1],'whole raw ASM/two-OBJ/EXE/MAP repeat without byte normalization; retain listing clocks separately')
    v=vectors[0];candidate=parse_mz(v['exe']);target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());need(candidate.valid and target.valid,'real native mini MZ and fixed Japanese decoded target')
    pubs=code_publics(v['obj'],1);definitions=segment_definitions(v['obj']);size=definitions[0]['size'];call_size=pubs[0][0]-459
    need(pubs==[(call_size+o,n) for o,n in [(459,'__Local_unwind'),(491,'__Return_unwind'),(673,'__ExceptionHandler')]],'all original public offsets relative to actual integrated call-bank size')
    for off,name in pubs:need(address(v['map'].decode(),name)==(0,off),'actual native linked public address')
    need(definitions[1:]==[dict(index=i,name=n,**{'class':k},overlay='',size=s) for i,n,k,s in [(2,'_DATA','DATA',0),(3,'_BSS','BSS',8)]],'no invented initialized DATA or BSS credit')
    p=payload(v['obj']);need(len([k for k in p if k[0]==1])==size and not any(k[0] in (2,3) for k in p),'whole dense candidate CODE and actual callback-only BSS')
    native=(WORK/'vendor/xx.obj').read_bytes();op=payload(native);fields=[f for f in literal_fields(native) if f['segment']==1 and BASE-XX_BASE<=f['site']<BASE-XX_BASE+SIZE];original=bytearray(op[1,BASE-XX_BASE+i] for i in range(SIZE))
    for f in fields:
        need((f['width'],f['location_type'],f['segment_relative'],f['frame_method'],f['frame'],f['target_method'],f['target'])==(2,1,True,5,None,0,1),'actual original CODE offset WORD')
        at=f['site']-(BASE-XX_BASE);need(at+2<=SIZE,'complete original native field');original[at:at+2]=(XX_BASE+f['addend']).to_bytes(2,'little')
    need(len(fields)==88 and bytes(original)==target.program_image[BASE:BASE+SIZE] and not any(BASE<=q.linear<BASE+SIZE for q in target.relocations),'all1495 original bytes independently resolved with88 literal ordered fields and no MZ words')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;original_rows=[dict(name=n,start=a,size=s) for n,a,s,_ in BODIES]
    old_tables,covered=classify(target.program_image,original_rows,decoder);new_tables,new_covered=classify(candidate.program_image,bodies[0],decoder)
    need(len(covered)==SIZE and set(covered)==set(range(BASE,BASE+SIZE)) and sum(row['size'] for row in original_rows)==1327,'complete1327 instruction bytes plus168 actual CS table bytes')
    need(len(new_covered)==call_size and set(new_covered)==set(range(call_size)),'complete actual candidate call-bank ownership')
    candidate_fields=literal_fields(v['obj']);call_fields=[f for f in candidate_fields if f['segment']==1 and f['site']<call_size]
    need(len(call_fields)==88 and all((f['width'],f['location_type'],f['segment_relative'],f['frame_method'],f['frame'],f['target_method'],f['target'])==(2,1,True,5,None,0,1) for f in call_fields),'all88 actual candidate CS table fields retained in literal order')
    destroy=source_bodies(v['listing'].decode());need(destroy[-1]['start']+destroy[-1]['size']==size,'integrated destruction tail completes the same native TU')
    cb=callbacks(v['context']);probes=[]
    for (name,a,_,_),kind,symbol in zip(BODIES,['copy-fastcall-virtual','dtor-far-fastthis','member-far-pascal'],['_xx_probe_copy','_xx_probe_dtor','_xx_probe_member']):
        b=next(row['start'] for row in bodies[0] if row['name']==name)
        pair=[run(target.program_image,a,kind,cb[symbol]),run(candidate.program_image,b,kind,cb[symbol])]
        need(pair[0]==pair[1],'actual target/source adapter ABI: '+name);probes.append(pair)
    return dict(complete=True,source_acceptance=False,accepted_source_bytes=0,accepted_publication_sha256=ACCEPTED_SHA,review_driver_sha256=sha((root/'scripts/review_th03_mainl_xx_calls.py').read_bytes()),selected_build_report_sha256=sha(raw),source_sha256=r['source_sha256'],
        original_bank_base=BASE,original_bank_size=SIZE,original_instruction_bytes=1327,original_inline_table_bytes=168,original_bodies=original_rows,original_tables=old_tables,original_literal_native_fields=fields,
        candidate_call_bank_bytes=call_size,candidate_CODE_segment_bytes=size,candidate_bodies=bodies[0],candidate_tables=new_tables,candidate_literal_native_fields=candidate_fields,candidate_call_bank_literal_fields=call_fields,
        complete_call_bank_raw_equal=candidate.program_image[:call_size]==target.program_image[BASE:BASE+SIZE],same_TU_destructor_and_member_edges_resolved=True,unresolved_interfaces=externs(v['obj']),target_and_source_callback_probes=probes,
        two_whole_raw_vectors_repeated=True,diagnostic_listing_has_wall_clock_headers=True,all_available_SDK_headers_bound=64,whole_product_linked=False,original_cold_rebuilt=False,ancestor_runtime_chain_rebuilt=False,physical_DOS_execution_claimed=False)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];r=review(root);(root/REVIEW).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('source_sha256','original_literal_native_fields','candidate_literal_native_fields','candidate_call_bank_literal_fields','original_tables','candidate_tables')},indent=2))
