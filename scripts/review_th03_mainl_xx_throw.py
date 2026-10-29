#!/usr/bin/env python3
"""Review the complete DOS throw bank,register frame and private unwind edge."""
import json
from pathlib import Path
import re
import struct
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
import probe_th03_mainl_xx_dispatch as native
from probe_th03_mainl_xx_throw import DRIVER,SOURCE,SUPPORT,REPORT,wrapper,context
from review_th03_mainl_xx_catch import parsed_bodies,dense,BODIES as CATCH_BODIES,EQUAL,CATCH
from review_th03_mainl_xx_calls import call_bodies,classify,CALLS,DESTROY,ACCEPTED_SHA
from review_th03_mainl_xx_destruction import source_bodies
from review_th03_mainl_xx_types import BODIES as TYPE_BODIES
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_resources_work import cold_context,need,sha
from build_th03_mainl_work import WORK
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_acceptance import proof_inputs
from lib.decoded_mainl_xx_throw_probe import callback,run,forward
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

REVIEW='.analysis/work/mainl-xx-throw-review.json'
BASE,SIZE,XX_BASE=0x6313,2524,0x580D
BODIES=[('tossAnException',0x6361,815,'far'),('_ThrowException',0x6690,89,'far'),
    ('_ReThrowException',0x66E9,170,'far'),('exceptionChainHook',0x6793,5,'far'),
    ('dispatchException',0x6798,140,'far'),('_Global_unwind',0x6824,71,'far'),
    ('exceptionContextHook',0x686B,5,'far'),('RaiseException',0x6870,1151,'far')]


def throw_bodies(listing):
    rows=parsed_bodies(listing,[b for b in BODIES if b[0] not in ('_Global_unwind','RaiseException')])
    for name in ('_Global_unwind','RaiseException'):
        symbol='_'+name
        start=re.findall(r'^\s*\d+\s+([0-9A-F]{4})\s+'+symbol+r'\s+proc\s+far\s*$',listing,re.M)
        end=re.findall(r'^\s*\d+\s+([0-9A-F]{4})\s+'+symbol+r'\s+endp\s*$',listing,re.M)
        need(len(start)==len(end)==1,'complete original C public '+name)
        rows.append(dict(name=name,start=int(start[0],16),size=int(end[0],16)-int(start[0],16),return_kind='far'))
    return sorted(rows,key=lambda r:r['start'])


def baseline(root):
    raw=(root/'.analysis/work/mainl-xx-types-build.json').read_bytes();r=json.loads(raw)
    reviewed=(root/'.analysis/work/mainl-xx-types-review.json').read_bytes();p=json.loads(reviewed)
    need(p['complete'] and not p['source_acceptance'] and p['accepted_source_bytes']==0 and p['selected_build_report_sha256']==sha(raw) and p['review_driver_sha256']==sha((root/'scripts/review_th03_mainl_xx_types.py').read_bytes()),'current reviewed types baseline receipt')
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
    for phase in r['native_phases']:need(sha((root/('.analysis/work/xx-types-'+phase['label']+'.log')).read_bytes())==phase['log_sha256'],'retained original baseline phase log')
    return sha(reviewed)


def review(root,report=None):
    root=Path(root);cold_context(root);baseline_sha=baseline(root)
    accepted_raw=(root/'config/mainl_work/scoped_acceptance.json').read_bytes();accepted=json.loads(accepted_raw)
    need(sha(accepted_raw)==ACCEPTED_SHA and accepted['proof_inputs']==proof_inputs(root) and len(accepted['audit']['scope']['owners'])==211 and sum(o['size'] for o in accepted['audit']['scope']['owners'])==36946,'unchanged accepted211-owner publication and verifier inputs')
    raw=(root/REPORT).read_bytes();r=json.loads(raw) if report is None else report
    need(r['complete'] and not r['source_acceptance'] and r['accepted_source_bytes']==0 and r['miniature_only'] and not r['whole_product_linked'] and not r['whole_product_cold_rebuilt'],'unaccepted DOS throw miniature,not normal-library exactness')
    sources={'xxbank.inl':native.SOURCE,'xx_abi.h':native.HEADER,'xxdtor.inl':DESTROY,'xxcall.inl':CALLS,'xxeq.inl':EQUAL,'xxcatch.inl':CATCH,'xxtypes.inl':'src/mainl/crt/xx_type_match.inl','xxthrow.inl':SOURCE}
    base=(native.WRAPPER.replace(b'int near dtorCleanup',b'static int near dtorCleanup')+b'#include "xxdtor.inl"\n').replace(native.CATCH_INTERFACES,b'').replace(b'#include "xxbank.inl"',b'#include "xxeq.inl"\n#include "xxcall.inl"\n#include "xxcatch.inl"\n#include "xxbank.inl"')
    current_wrapper=wrapper(base)
    need(r['source_sha256']=={n:sha((root/n).read_bytes()) for n in sources.values()} and r['driver_sha256']==sha((root/native.DRIVER).read_bytes()) and r['profile_driver_sha256']=={DRIVER:sha((root/DRIVER).read_bytes())} and r['probe_support_sha256']=={SUPPORT:sha((root/SUPPORT).read_bytes())},'maintained banks,common builder,independent profile and focused probe source')
    need(r['compiler']==compiler_context(root) and r['compiler_flags']==native.FLAGS and r['available_SDK_header_sha256']==native.sdk_inventory(root),'current scoped compiler/profile/all64 available SDK headers')
    need(r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()) and r['wrapper_sha256']==sha(current_wrapper),'unchanged cold report and original relative same-TU source order')
    need((root/'.analysis/work/xx-throw-wrapper.cpp').read_bytes()==current_wrapper and (root/'.analysis/work/xx-throw-mini.lnk').read_bytes()==native.LINK,'actual compiler wrapper and link response')
    for short,path in sources.items():need((root/('.analysis/work/xx-throw-source-'+short)).read_bytes()==(root/path).read_bytes(),'actual source transport: '+short)
    cfg=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/cfg['paths']['wine_prefix'];dos=['/usr/bin/wine-stable',str(root/cfg['paths']['msdos_player']),'-e','-x'];tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t'];phases=[]
    for number in (1,2):
        for label,cmd in [('compile',dos+[r'C:\BC45\BCC.EXE',*native.FLAGS,'xxdisp.cpp']),('assemble',tasm+['/l','xxdisp.asm','xxdisp.obj']),('context',tasm+['xxctx.asm','xxctx.obj']),('mini-link',dos+['tlink','@xxmini.lnk'])]:phases.append((f'round{number}-{label}',cmd,0))
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'two actual serial native compiler/assembler/mini-link rounds')
    for p in r['native_phases']:
        log=(root/('.analysis/work/xx-throw-'+p['label']+'.log')).read_bytes();need(sha(log)==p['log_sha256'],'whole native phase log')
        if p['label'].endswith('compile'):need(log.startswith(r['compiler']['banner'].encode()+b'\r\n'),'actual scoped BCC banner')
    expected={'@$bdele','@$bdla','@__RefDestructorCount','___InitExceptBlocks','___ExitExceptBlocks','___call_unexpected','__8086','___JumpToCatch__','_abort','_free','_malloc','_memcpy','_memset','___call_terminate','N_LXMUL@','N_LUDIV@'}
    vectors=[];bodies=[]
    for row in r['rounds']:
        need(set(row['outputs'])=={'asm','obj','context','exe','map','listing'},'five complete raw native outputs plus unmodified listing');v={}
        for key,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'whole actual raw output identity');v[key]=b
        imports=externs(v['obj']);ctx=context(imports)
        need(len(imports)==16 and {n.rsplit('$',1)[0] for n in imports}==expected and '__Global_unwind' not in imports,'real Global_unwind resolves internally;15 callable traps and one CPU DATA slot remain')
        need(row['unresolved_imports']==imports and row['context_sha256']==sha(ctx) and (root/'.analysis/work/xx-throw-context.asm').read_bytes()==ctx,'actual trap-only diagnostic context without helper models')
        need(describe_omf(v['obj'])['valid'] and describe_omf(v['context'])['valid'],'complete actual native OMF structure');bodies.append(throw_bodies(v['listing'].decode()));vectors.append(v)
    need({k:v for k,v in vectors[0].items() if k!='listing'}=={k:v for k,v in vectors[1].items() if k!='listing'} and bodies[0]==bodies[1],'whole raw ASM/two-OBJ/EXE/MAP repeat without output normalization; page clocks kept separately')
    v=vectors[0];candidate=parse_mz(v['exe']);target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());need(candidate.valid and target.valid,'real native mini MZ and fixed Japanese decoded target')
    defs=segment_definitions(v['obj']);size=defs[0]['size'];p=payload(v['obj'])
    need(defs[1:]==[dict(index=i,name=n,**{'class':k},overlay='',size=s) for i,n,k,s in [(2,'_DATA','DATA',0),(3,'_BSS','BSS',8)]] and len([q for q in p if q[0]==1])==size and not any(q[0] in (2,3) for q in p),'dense source CODE;original diagnostic BSS8,no new product DATA/BSS owner')
    original=(WORK/'vendor/xx.obj').read_bytes();op=payload(original)
    fields=[f for f in literal_fields(original) if f['segment']==1 and BASE-XX_BASE<=f['site']<BASE-XX_BASE+SIZE]
    image=bytearray(op[1,BASE-XX_BASE+i] for i in range(SIZE));mz=[];original_map=(WORK/'obj/th03/mainl.map').read_text()
    for f in fields:
        at=f['site']-(BASE-XX_BASE);absolute=BASE+at
        need(at+f['width']<=SIZE,'complete original literal field')
        if f['target_method']==2:
            name=externs(original)[f['target']-1];mapped={'@__RefDestructorCount$qv':'__refdestructorcount()'}.get(name,name)
            seg,off=address(original_map,mapped)
            need(f['addend']==0 and (seg==0 or name=='__8086'),'actual original runtime/library symbol')
        else:
            need((f['target_method'],f['target'])==(0,1),'internal original CODE reference');seg,off=0,XX_BASE+f['addend']
        if (f['frame_method'],f['frame'])==(1,1):
            need(name=='__8086' and (f['location_type'],f['width'],f['segment_relative'])==(1,2,True) and (seg,off)==(0xE3F,0x112E),'original CPU discriminator DGROUP frame')
            image[at:at+2]=off.to_bytes(2,'little');continue
        need((f['frame_method'],f['frame'])==(5,None),'original target-relative CODE frame')
        if f['location_type']==3:
            need(f['width']==4 and f['segment_relative'],'complete far original field')
            if image[at-1]==0x9A:image[at-1:at+4]=b'\x90\x0e\xe8'+((off-absolute-4)&65535).to_bytes(2,'little')
            else:image[at:at+4]=struct.pack('<2H',off,seg);mz.append(absolute+2)
        elif f['location_type']==2:
            need(f['width']==2 and f['segment_relative'],'original segment WORD');image[at:at+2]=seg.to_bytes(2,'little');mz.append(absolute)
        else:
            need(f['location_type']==1 and f['width']==2 and f['segment_relative'],'original offset WORD');image[at:at+2]=off.to_bytes(2,'little')
    need(len(fields)==24 and bytes(image)==target.program_image[BASE:BASE+SIZE] and mz==[q.linear for q in target.relocations if BASE<=q.linear<BASE+SIZE],'all2524 original bytes and literal ordered24 fields/MZ words resolved independently')
    t=target.program_image
    eh=(0,0,0x65D1,0,0,0,0,0,0,0,0,0,0,0,0x662A,0,0,0,0,0,0,0,0,0,0,0,0xFFE2,0,3,BASE,0,0,4,0,3,BASE+24,0,0,4)
    need(struct.unpack('<39H',t[BASE:BASE+78])==eh,'all78 original generated two-catch metadata bytes')
    old=[dict(name=n,start=a,size=s,return_kind=k) for n,a,s,k in BODIES];rows=bodies[0]
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    dense(t,old,decoder);dense(candidate.program_image,rows,decoder)
    dispatch=rows[4]
    need(dispatch['size']==140 and candidate.program_image[dispatch['start']:dispatch['start']+140]==t[0x6798:0x6824],'complete unnormalized140-byte dispatcher body matches the fixed original')
    need(sum(r['size'] for r in old)==2446 and old[0]['start']==BASE+78 and old[-1]['start']+old[-1]['size']==BASE+SIZE and all(a['start']+a['size']==b['start'] for a,b in zip(old,old[1:])),'complete eight-procedure original ownership,including two real five-byte hooks')
    types=parsed_bodies(v['listing'].decode(),TYPE_BODIES);calls=call_bodies(v['listing'].decode());_,covered=classify(candidate.program_image,calls,decoder);catches=parsed_bodies(v['listing'].decode(),CATCH_BODIES)
    need(types[-1]['start']+types[-1]['size']==calls[0]['start'] and set(covered)==set(range(calls[0]['start'],rows[0]['start']-78)) and all(a['start']+a['size']==b['start'] for a,b in zip(rows,rows[1:])) and rows[-1]['start']+rows[-1]['size']==catches[0]['start']-42,'natural types/adapters/two-catch EH/throw/single-catch EH adjacency')
    catch_end=catches[-1]['start']+catches[-1]['size'];destroys=source_bodies(v['listing'].decode())
    need(destroys[0]['start']==catch_end+1565+78 and destroys[-1]['start']+destroys[-1]['size']==size,'unchanged same-TU dispatch/destruction tail')
    pubs=code_publics(v['obj'],1)
    expected_publics=[(rows[1]['start'],'@_ThrowException$qnvt1t1t1uiuiuinuc'),(rows[2]['start'],'@_ReThrowException$quinuc'),(rows[5]['start'],'__Global_unwind'),(rows[7]['start'],'_RaiseException'),(catches[2]['start'],'@_CatchCleanup$qv')]+[(catch_end+o,n) for o,n in [(459,'__Local_unwind'),(491,'__Return_unwind'),(673,'__ExceptionHandler')]]
    need(pubs==expected_publics,'all original public C/C++ signatures;private throw dispatcher and hooks stay private')
    # The register-save convention is generated by the compiler attribute.
    # The two destructive stack-resume paths are necessarily explicit assembly.
    for data,body_row in [(t,old[-1]),(candidate.program_image,rows[-1])]:
        body=data[body_row['start']:body_row['start']+body_row['size']]
        need(body[:12]==bytes.fromhex('50515253545556571e068bec') and body[-13:]==bytes.fromhex('8be5071f5f5e5d5b5b5a5958cb'),'compiler saveregs ten-WORD entry and normal RETF fallback')
        ins=list(decoder.disasm(body,body_row['start']));mn=[i.mnemonic for i in ins]
        need(mn.count('pushal')==1 and mn.count('popal')==2 and mn.count('pushfd')==1 and mn.count('popfd')==1 and mn.count('popaw')==1 and mn.count('retf')==3,'guarded386 and16-bit native snapshot/resume instructions')
    actual_unwind_calls=[]
    for i in decoder.disasm(candidate.program_image[catch_end:destroys[0]['start']-78],catch_end):
        if i.mnemonic=='call' and i.operands[0].type==X86_OP_IMM and i.operands[0].imm==rows[5]['start']:actual_unwind_calls.append(i.address)
    need(len(actual_unwind_calls)==1,'actual exception handler calls real far Global_unwind inside same TU')
    cb=callback(v['context']);memcpy_bytes=t[0x4B7D:0x4BA1];mi=list(decoder.disasm(memcpy_bytes,0x4B7D))
    memobj=(WORK/'vendor/memcpy.obj').read_bytes()
    need(sum(i.size for i in mi)==36 and mi[-1].mnemonic=='retf' and not literal_fields(memobj) and bytes(payload(memobj)[1,i] for i in range(36))==memcpy_bytes,'actual entire36-byte original memcpy has no native fields;no helper model')
    probes=[]
    for kind,index in [('raise-386-context',7),('global-unwind-target',5)]:
        pair=[run(t,old[index]['start'],kind,cb,0x112E,0x4B7D),run(candidate.program_image,rows[index]['start'],kind,cb,address(v['map'].decode(),'__8086')[1],address(v['map'].decode(),'_memcpy')[1],memcpy_bytes)]
        if kind=='raise-386-context':
            need(all(pair[0][k]==pair[1][k] for k in pair[0] if k!='context') and pair[0]['context'][:13]==pair[1]['context'][:13] and pair[0]['context'][14:]==pair[1]['context'][14:],'same native register/context/record ABI;retain the observed saved-EFLAGS gap separately')
        else:
            need(pair[0]==pair[1],'actual original/source throw ABI: '+kind)
        probes.append(pair)
    for kind,index in [('throw-forward',1),('rethrow-ss-forward',2)]:
        pair=[forward(t,old[index]['start'],old[0]['start'],kind),forward(candidate.program_image,rows[index]['start'],rows[0]['start'],kind)]
        need(pair[0]==pair[1],'actual original/source wrapper ABI: '+kind);probes.append(pair)
    start,end=rows[0]['start']-78,rows[-1]['start']+rows[-1]['size']
    return dict(complete=True,source_acceptance=False,accepted_source_bytes=0,accepted_publication_sha256=ACCEPTED_SHA,reused_baseline_receipt_sha256=baseline_sha,review_driver_sha256=sha((root/'scripts/review_th03_mainl_xx_throw.py').read_bytes()),selected_build_report_sha256=sha(raw),source_sha256=r['source_sha256'],profile_driver_sha256=r['profile_driver_sha256'],
        original_bank_base=BASE,original_bank_size=SIZE,original_instruction_bytes=2446,original_inline_data_bytes=78,original_bodies=old,original_literal_native_fields=fields,original_MZ_words=mz,
        candidate_bank_bytes=end-start,candidate_CODE_segment_bytes=size,candidate_bodies=rows,candidate_literal_native_fields=literal_fields(v['obj']),complete_bank_raw_equal=candidate.program_image[start:end]==t[BASE:BASE+SIZE],raw_dispatcher_body_equal=True,
        original_covered_contiguous_range=[0x583E,0x8294],original_covered_bytes=10838,actual_dispatch_global_unwind_calls=actual_unwind_calls,same_TU_global_unwind_edge_resolved=True,unresolved_interfaces=externs(v['obj']),target_and_source_throw_probes=probes,actual_memcpy_fixture_sha256=sha(memcpy_bytes),two_whole_raw_vectors_repeated=True,all_available_SDK_headers_bound=64,
        saved_eflags_observations=[p['context'][13] for p in probes[0]],saved_eflags_equal=probes[0][0]['context'][13]==probes[0][1]['context'][13],
        whole_product_linked=False,original_cold_rebuilt=False,ancestor_runtime_chain_rebuilt=False,physical_DOS_execution_claimed=False)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];r=review(root);(root/REVIEW).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('source_sha256','original_literal_native_fields','candidate_literal_native_fields')},indent=2))
