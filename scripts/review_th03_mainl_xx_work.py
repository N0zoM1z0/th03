#!/usr/bin/env python3
"""Review the actual xx normal-library replacement and whole MAINL carrier."""
import json
from pathlib import Path
import re
import struct
import tomllib
import build_th03_mainl_xx_work as producer
import probe_th03_mainl_xx_dispatch as miniature
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_work import WORK
from build_th03_mainl_display_work import literal_fields
from review_th03_mainl_xx_rtti import initialized_payload,all_bodies
from lib.borland_library import library_members,compare_members,object_program_records
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_xx_rtti_probe import run as rtti_run,CASES
from lib.decoded_mainl_xx_throw_probe import run as raise_run,callback
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

REVIEW='.analysis/work/mainl-xx-product-review.json'


def review(root,report=None):
    root=Path(root);baseline,files,library,members,mini=producer.baseline(root)
    old_build=json.loads((root/producer.BASE_BUILD).read_bytes())
    previous_providers=sorted(set(old_build['reused_sources'])|set(producer.build.CRT)|{'new','xalloc','xmsg'})
    need(len(previous_providers)==28 and 'xx' not in previous_providers and next(m.program_records for m in members if m.name=='xx')==object_program_records((WORK/'vendor/xx.obj').read_bytes()),'28 real prior source providers and original vendor xx,without double-counting an existing source owner')
    raw=(root/producer.REPORT).read_bytes();r=json.loads(raw) if report is None else report
    need(r['complete'] and r['whole_product_linked'] and r['diagnostic_candidate'] and not r['source_acceptance'] and r['accepted_source_bytes']==0 and not r['whole_product_cold_rebuilt'] and r['retained_project_objects']==36,'complete unaccepted actual whole MAINL link,without cold rebuild')
    need(r['baseline']==baseline and r['driver_sha256']==sha((root/producer.DRIVER).read_bytes()) and r['support_sha256']=={p:sha((root/p).read_bytes()) for p in producer.SUPPORT},'current normal-library/miniature baselines,producer and scoped support')
    need(r['source_sha256']=={p:sha((root/p).read_bytes()) for p in producer.SOURCES.values()} and r['compiler']==compiler_context(root) and r['compiler_flags']==miniature.FLAGS and r['available_SDK_header_sha256']==miniature.sdk_inventory(root),'current complete maintained TU,scoped compiler and64 SDK headers')
    need(len(r['retained_binary_inputs_sha256'])==39 and r['retained_binary_inputs_sha256']=={p:sha((root/p).read_bytes()) for p in r['retained_binary_inputs_sha256']},'all36 project objects plus startup and two pinned SDK libraries retained')
    unit=producer.wrapper(b'');need(r['wrapper_sha256']==sha(unit) and (root/'.analysis/work/xx-product-maintained-xx.cpp').read_bytes()==(root/producer.UNIT).read_bytes(),'real module-name source transport and unchanged maintained TU')
    for short,path in producer.SOURCES.items():
        need((root/('.analysis/work/xx-product-source-'+short)).read_bytes()==(unit if short=='xx.cpp' else (root/path).read_bytes()),'actual compiler source input: '+short)
    extract=producer.build.response('base.lib',['*'+m.name for m in members])
    need((root/'.analysis/work/xx-product-extract.rsp').read_bytes()==extract and (root/'.analysis/work/xx-product-library.rsp').read_bytes()==producer.library_response(members) and (root/'.analysis/work/xx-product-link.lnk').read_bytes()==producer.link_response(files),'literal native extract/build/link responses and original member/link order')
    cfg=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/cfg['paths']['wine_prefix'];dos=['/usr/bin/wine-stable',str(root/cfg['paths']['msdos_player']),'-e','-x'];tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t']
    phases=[('extract-current-library',dos+['tlib','@extract.rsp'],0)]
    for number in (1,2):
        for label,argv in [('compile',dos+[r'C:\BC45\BCC.EXE',*miniature.FLAGS,'xx.cpp']),('assemble',tasm+['/l','xx.asm','xx.obj']),('library',dos+['tlib',r'@probe\xxwhole\library.rsp']),('link',dos+['tlink',r'@probe\xxwhole\link.lnk'])]:phases.append((f'round{number}-{label}',argv,0))
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'one real native extraction and two actual compiler/TASM/TLIB/whole-product TLINK rounds')
    for phase in r['native_phases']:
        log=(root/('.analysis/work/xx-product-'+phase['label']+'.log')).read_bytes()
        need(sha(log)==phase['log_sha256'],'whole actual native phase log')
        if phase['label'].endswith('compile'):need(log.startswith(r['compiler']['banner'].encode()+b'\r\n'),'real scoped compiler banner')
    vectors=[];rows=[]
    for round in r['rounds']:
        need(set(round['outputs'])=={'asm','obj','listing','lib','exe','map'},'five complete raw outputs plus unmodified clocked listing')
        vector={}
        for kind,meta in round['outputs'].items():
            data=(root/meta['path']).read_bytes();need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),'complete actual normal-link output');vector[kind]=data
        observed=compare_members(members,library_members(vector['lib']),{'xx':vector['obj']})
        need(round['library']==observed and observed['contextual_members_unchanged']==892 and observed['replaced_members']==['xx'],'same893 positions,all892 surrounding member program records unchanged,only real source xx replaced')
        need(describe_omf(vector['obj'])['valid'],'valid complete actual native xx OMF')
        need(initialized_payload(vector['obj'])==initialized_payload(mini['obj']) and literal_fields(vector['obj'])==literal_fields(mini['obj']) and segment_definitions(vector['obj'])==segment_definitions(mini['obj']) and code_publics(vector['obj'],1)==code_publics(mini['obj'],1) and externs(vector['obj'])==externs(mini['obj']),'actual xx module preserves entire current miniature payload,ordered fields,storage and22 public/18 imported interfaces')
        rows.append(all_bodies(vector['listing'].decode()));vectors.append(vector)
    need({k:v for k,v in vectors[0].items() if k!='listing'}=={k:v for k,v in vectors[1].items() if k!='listing'} and rows[0]==rows[1],'whole raw ASM/OBJ/LIB/EXE/MAP pair equality,without any byte normalization')
    v=vectors[0];source=parse_mz(v['exe']);target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());need(source.valid and target.valid,'actual full native MAINL MZ and pinned Japanese decoded MZ')
    table=v['map'].decode();coordinates={}
    for segment,offset,size,kind,name in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=(CODE|DATA|BSS)\s+S=(_TEXT|_DATA|_BSS)\s+G=\S+\s+M=xx\s+ACBP=\S+\s*$',table,re.M):
        need(kind not in coordinates,'one actual whole-program xx segment owner');coordinates[kind]=(int(segment,16),int(offset,16),int(size,16))
    definitions=segment_definitions(v['obj']);code_size=definitions[0]['size']
    need(set(coordinates)=={'CODE','DATA','BSS'} and coordinates['CODE']==(0,0x580D,code_size) and coordinates['DATA'][1:]==(0x1172,18) and coordinates['BSS'][1:]==(0x2876,10) and coordinates['DATA'][0]==coordinates['BSS'][0],'actual original xx positions and complete native CODE/DATA/BSS extents')
    fields=literal_fields(v['obj']);p,iterated=initialized_payload(v['obj']);base=coordinates['CODE'][1];image=bytearray(p[1,i] for i in range(code_size));mz=[];names=externs(v['obj'])
    aliases={'@__RefDestructorCount$qv':'__refdestructorcount()','@$bnew$qui':'operator new(unsigned int)','@$bdele$qnv':'operator delete(void far*)','@$bdla$qnv':'operator delete[](void far*)'}
    for field in fields:
        at=field['site'];absolute=base+at
        need(field['segment']==1 and at+field['width']<=code_size,'complete real source field in native xx carrier')
        if field['target_method']==2:
            name=names[field['target']-1];seg,off=address(table,aliases.get(name,name));off+=field['addend']
        else:
            need(field['target_method']==0 and field['target'] in (1,2,3),'real native xx internal CODE/DATA/BSS target')
            seg,off,_=coordinates[{1:'CODE',2:'DATA',3:'BSS'}[field['target']]];off+=field['addend']
        if (field['frame_method'],field['frame'])==(1,1):
            need((field['location_type'],field['width'],field['segment_relative'])==(1,2,True) and seg==coordinates['DATA'][0],'real whole-product DGROUP field')
            image[at:at+2]=off.to_bytes(2,'little');continue
        frame=(field['frame_method'],field['frame'])
        if frame==(0,1):
            need(field['target_method']==2 and name in ('N_LXMUL@','N_LUDIV@') and (field['location_type'],field['width'],field['segment_relative'])==(1,2,False),'actual explicit CODE-frame near arithmetic helper')
        else:
            need(frame==(5,None),'actual target-relative CODE frame')
        need(seg==0,'real whole-product CODE reference')
        if field['location_type']==3:
            need(field['width']==4 and field['segment_relative'],'real far source field')
            if image[at-1]==0x9A:image[at-1:at+4]=b'\x90\x0e\xe8'+((off-absolute-4)&65535).to_bytes(2,'little')
            else:image[at:at+4]=struct.pack('<2H',off,seg);mz.append(absolute+2)
        elif field['location_type']==2:
            need(field['width']==2 and field['segment_relative'],'source segment WORD');image[at:at+2]=seg.to_bytes(2,'little');mz.append(absolute)
        else:
            need(field['location_type']==1 and field['width']==2,'source offset/displacement WORD')
            image[at:at+2]=(off if field['segment_relative'] else (off-absolute-2)&65535).to_bytes(2,'little')
    need(bytes(image)==source.program_image[base:base+code_size] and mz==[q.linear for q in source.relocations if base<=q.linear<base+code_size] and len(mz)==20,'complete source CODE resolves through actual18 library interfaces and ordered20 MZ words,without miniature traps')
    ds,off,_=coordinates['DATA'];need(source.program_image[ds*16+off:ds*16+off+18]==bytes(p[2,i] for i in range(18)),'all18 DATA bytes bind the actual whole-product DGROUP position')
    original_table=(WORK/'obj/th03/mainl.map').read_text();probes=[];procedures=rows[0]
    original_publics=code_publics((WORK/'vendor/xx.obj').read_bytes(),1)
    source_publics=code_publics(v['obj'],1);bindings=[]
    need(len(source_publics)==len(original_publics)==22,'all original22 public definitions')
    for (old_at,old_name),(new_at,new_name) in zip(original_publics,source_publics):
        names_at={re.sub(r'^idle\s+','',name) for name in re.findall(rf'^\s*0000:{0x580D+old_at:04X}\s+(.+?)\s*$',original_table,re.M) if 'C=CODE' not in name}
        need(old_name==new_name and len(names_at)==1,'same native original public name and unambiguous real MAP interface')
        mapped=names_at.pop();need(address(table,mapped)==(0,base+new_at),'actual whole-program public interface: '+mapped)
        bindings.append(dict(symbol=new_name,MAP_name=mapped,offset=base+new_at))
    for kind in CASES:
        index=49 if kind in CASES[:3] else 47 if kind==CASES[3] else 0
        original_entry=0x876E if index==49 else 0x84A5 if index==47 else 0x580D
        pair=[rtti_run(target.program_image,original_entry,kind,0x8528),rtti_run(source.program_image,base+procedures[index]['start'],kind,base+procedures[48]['start'])]
        need(pair[0]==pair[1],'actual whole-link RTTI/jump ABI: '+kind);probes.append(pair)
    # Reuse the unchanged actual TASM handler,then exercise the real linked
    # memcpy twice. This path has no miniature import redirection or helpers.
    old_throw=json.loads((root/'.analysis/work/mainl-xx-throw-build.json').read_bytes());context_meta=old_throw['rounds'][0]['outputs']['context'];context_raw=(root/context_meta['path']).read_bytes()
    need(sha(context_raw)==context_meta['sha256'] and old_throw['probe_support_sha256']=={'scripts/lib/decoded_mainl_xx_throw_probe.py':sha((root/'scripts/lib/decoded_mainl_xx_throw_probe.py').read_bytes())},'unchanged actual native throw handler fixture')
    handler=callback(context_raw);raise_pair=[]
    for data,mapping in [(target.program_image,original_table),(source.program_image,table)]:
        raise_pair.append(raise_run(data,address(mapping,'_RaiseException')[1],'raise-386-context',handler,address(mapping,'__8086')[1],address(mapping,'_memcpy')[1]))
    need(raise_pair[0]==raise_pair[1],'complete tested real linked386 record/register/context pair agrees at entry SP=FF00')
    alternate=[]
    for data,mapping in [(target.program_image,original_table),(source.program_image,table)]:
        alternate.append(raise_run(data,address(mapping,'_RaiseException')[1],'raise-386-context',handler,address(mapping,'__8086')[1],address(mapping,'_memcpy')[1],stack_offset=0xFF10))
    need(all(alternate[0][k]==alternate[1][k] for k in alternate[0] if k!='context') and alternate[0]['context'][:13]==alternate[1]['context'][:13] and alternate[0]['context'][14:]==alternate[1]['context'][14:] and [q['context'][13] for q in alternate]==[128,132],'one alternate entry SP exposes remaining frame-dependent saved-PF difference without changing flags')
    raise_body=source.program_image[base+procedures[18]['start']:base+procedures[18]['start']+procedures[18]['size']]
    need(raise_body.count(target.program_image[0x6AC0:0x6B07])==1,'complete raw71-byte argument copy block in actual linked product')
    raw_equal=v['exe']==target.raw;map_equal=v['map']==(WORK/'obj/th03/mainl.map').read_bytes()
    need(not raw_equal and not map_equal,'current full product remains a raw-different candidate,not exact acceptance')
    tail_start=base+procedures[36]['start'];tail_size=code_size-procedures[36]['start']
    original_bodies=json.loads((root/producer.MINI_REVIEW).read_bytes())['original_bodies'];body_comparisons=[]
    need(len(original_bodies)==len(procedures)==50,'complete original/current function comparison scope')
    for old,new in zip(original_bodies,procedures):
        at=base+new['start']
        body_comparisons.append(dict(name=old['name'],original_bytes=old['size'],candidate_bytes=new['size'],
            size_delta=new['size']-old['size'],raw_equal=source.program_image[at:at+new['size']]==target.program_image[old['start']:old['start']+old['size']]))
    need(body_comparisons[15]==dict(name='dispatchException',original_bytes=140,candidate_bytes=140,size_delta=0,raw_equal=True),'complete140-byte normal-linked dispatcher matches the fixed target without normalization')
    return dict(complete=True,source_acceptance=False,accepted_source_bytes=0,whole_product_linked=True,whole_product_accepted=False,
        selected_build_report_sha256=sha(raw),review_driver_sha256=sha((root/'scripts/review_th03_mainl_xx_work.py').read_bytes()),source_sha256=r['source_sha256'],baseline=baseline,
        normal_library_members=893,unchanged_surrounding_members=892,source_CRT_providers=29,reused_source_CRT_providers=28,reused_source_provider_names=previous_providers,retained_project_objects=36,retained_binary_inputs=39,
        original_file_bytes=len(target.raw),candidate_file_bytes=len(v['exe']),original_header_bytes=target.header.header_size,candidate_header_bytes=source.header.header_size,
        original_relocation_count=len(target.relocations),candidate_relocation_count=len(source.relocations),original_MZ_relocations=[[q.segment,q.offset] for q in target.relocations],candidate_MZ_relocations=[[q.segment,q.offset] for q in source.relocations],
        whole_EXE_raw_equal=raw_equal,whole_MAP_raw_equal=map_equal,original_xx_CODE_bytes=12622,candidate_xx_CODE_bytes=code_size,native_module_coordinates=coordinates,
        original_RTTI_tail_bytes=1735,candidate_RTTI_tail_bytes=tail_size,RTTI_tail_raw_equal=source.program_image[tail_start:tail_start+tail_size]==target.program_image[0x8294:0x895B],
        raw_function_comparisons=body_comparisons,
        candidate_literal_native_fields=fields,candidate_ordered_xx_MZ_words=mz,candidate_LIDATA_records=iterated,actual22_public_bindings=bindings,all_source_CODE_bytes_resolved=True,all18_interfaces_resolved_to_real_library=True,
        target_and_source_RTTI_probes=probes,target_and_source_real_memcpy_raise_probe=raise_pair,alternate_stack_offset=0xFF10,alternate_stack_real_memcpy_raise_probe=alternate,raw_Raise_argument_copy_bytes=71,actual_native_handler_sha256=sha(handler),two_whole_raw_vectors_repeated=True,all_available_SDK_headers_bound=64,
        original_cold_rebuilt=False,ancestor_runtime_chain_rebuilt=False,physical_DOS_execution_claimed=False)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];r=review(root);(root/REVIEW).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('source_sha256','candidate_literal_native_fields','original_MZ_relocations','candidate_MZ_relocations')},indent=2))
