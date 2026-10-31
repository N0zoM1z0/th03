#!/usr/bin/env python3
"""Review the actual xx normal-library replacement and whole MAINL carrier."""
import json
from pathlib import Path
import re
import struct
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
import build_th03_mainl_xx_work as producer
import probe_th03_mainl_xx_dispatch as miniature
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_work import WORK
from build_th03_mainl_display_work import literal_fields
from review_th03_mainl_xx_rtti import initialized_payload,destruction_codegen,handler_codegen,catch_storage_codegen
from review_th03_mainl_xx_catch import dense,comparator_codegen
from review_th03_mainl_xx_types import compatible_codegen
from review_th03_mainl_xx_calls import classify
from lib.decoded_mainl_xx_native import native_bodies
from lib.borland_library import library_members,compare_members,object_program_records
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_xx_rtti_probe import run as rtti_run,CASES
from lib.decoded_mainl_xx_throw_probe import run as raise_run,callback
from lib.omf import describe_omf,parse_omf
from lib.pc98 import parse_mz
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

REVIEW='.analysis/work/mainl-xx-product-review.json'


def native_fixup_blocks(obj):
    """Retain literal writer order and explain its dependence on CODE layout."""
    fields=literal_fields(obj);blocks=[];cursor=0;observed=[]
    for record in parse_omf(obj):
        if record.name!='LEDATA' or record.data[0]!=1:continue
        start=int.from_bytes(record.data[1:3],'little');size=len(record.data)-3
        need(start==cursor and 0<size<=1024,'contiguous actual native CODE blocks')
        selected=[f for f in fields if f['segment']==1 and start<=f['site']<start+size]
        need(all(f['site']+f['width']<=start+size for f in selected) and
            all(a['site']>b['site'] for a,b in zip(selected,selected[1:])),
            'complete native fields in literal descending order within each CODE block')
        blocks.append(dict(start=start,size=size,literal_fields=selected))
        observed.extend(selected);cursor+=size
    need(len(fields)==187 and observed==fields and
        all(b['size']==1024 for b in blocks[:-1]),
        'all187 literal fields retain emitted CODE-block order,without sorting')
    return blocks


def native_storage(image,base,rows,size,obj):
    gaps=[];cursor=0
    for row in rows:
        need(row['start']>=cursor,'disjoint native procedures')
        if row['start']>cursor:gaps.append([cursor,row['start']-cursor])
        cursor=row['start']+row['size']
    need(cursor<size,'native RTTI storage follows the last procedure')
    gaps.append([cursor,size-cursor])
    need([n for a,n in gaps[:-1]]==[96,48,102,42,12,8,90],
        'all native switch/EH storage gaps retain their original extents')
    start,count=gaps[-1]
    fields=[f for f in literal_fields(obj) if f['segment']==1 and f['site']==start+48]
    need(len(fields)==1 and fields[0]['target_method']==0 and fields[0]['target']==1,
        'actual native far typeinfo-descriptor reference')
    vt=fields[0]['addend']-12;zero=vt-start-63
    need(zero in (0,1) and count==135+zero,'actual native descriptor/vtable storage extent')
    at=base+start;vtable=base+vt;dtor=base+rows[42]['start'];data=image
    need(struct.unpack('<5H',data[at:at+10])==(1,1,10,0xFFFF,0) and
        data[at+10:at+20]==b'Bad_cast\0\0' and
        struct.unpack('<5H',data[at+20:at+30])==(1,1,10,0xFFFF,0) and
        data[at+30:at+42]==b'Bad_typeid\0\0','complete native exception descriptors')
    need(struct.unpack('<3H',data[at+42:at+48])==(4,0x2010,10) and
        data[at+52:at+63]==b'typeinfo *\0' and all(b==0 for b in data[at+63:vtable]),
        'native pointer descriptor,name and actual optional zero')
    need(struct.unpack('<2H',data[at+48:at+52])==(vtable+12,0) and
        struct.unpack('<2H',data[vtable:vtable+4])==(vtable+12,0) and
        data[vtable+4:vtable+8]==b'\0'*4 and
        struct.unpack('<2H',data[vtable+8:vtable+12])==(dtor,0),
        'all native type/vtable/destructor pointers')
    need(struct.unpack('<19H',data[vtable+12:vtable+50])==
        (8,3,38,0,0x1073,48,52,0,0,0,0,0,0,1,1,dtor,0,5,56) and
        data[vtable+50:vtable+60]==b'typeinfo\0\0' and
        data[vtable+60:vtable+72]==b'\0'*12 and vt+72==size,
        'entire native typeinfo header,name and terminated descriptor lists')
    return dict(gaps=gaps,RTTI_metadata_bytes=count,RTTI_zero_bytes=zero)


def review(root,report=None):
    root=Path(root);baseline,files,library,members,mini=producer.baseline(root)
    old_build=json.loads((root/producer.BASE_BUILD).read_bytes())
    previous_providers=sorted(set(old_build['reused_sources'])|set(producer.build.CRT)|{'new','xalloc','xmsg'})
    need(len(previous_providers)==28 and 'xx' not in previous_providers and next(m.program_records for m in members if m.name=='xx')==object_program_records((WORK/'vendor/xx.obj').read_bytes()),'28 real prior source providers and original vendor xx,without double-counting an existing source owner')
    raw=(root/producer.REPORT).read_bytes();r=json.loads(raw) if report is None else report
    need(r['complete'] and r['whole_product_linked'] and r['diagnostic_candidate'] and not r['source_acceptance'] and r['accepted_source_bytes']==0 and not r['whole_product_cold_rebuilt'] and r['retained_project_objects']==36,'complete unaccepted actual whole MAINL link,without cold rebuild')
    need(r['baseline']==baseline and r['driver_sha256']==sha((root/producer.DRIVER).read_bytes()) and r['support_sha256']=={p:sha((root/p).read_bytes()) for p in producer.SUPPORT},'current normal-library/miniature baselines,producer and scoped support')
    need(r['source_sha256']=={p:sha((root/p).read_bytes()) for p in producer.SOURCES.values()} and r['compiler']==compiler_context(root) and r['compiler_flags']==producer.OBJECT_FLAGS and r['assembly_flags']==producer.ASM_FLAGS and r['native_object_compiler'] and r['available_SDK_header_sha256']==miniature.sdk_inventory(root),'current maintained TU,native BCC object recipe and64 SDK headers')
    need(len(r['retained_binary_inputs_sha256'])==39 and r['retained_binary_inputs_sha256']=={p:sha((root/p).read_bytes()) for p in r['retained_binary_inputs_sha256']},'all36 project objects plus startup and two pinned SDK libraries retained')
    unit=producer.wrapper(b'');need(r['wrapper_sha256']==sha(unit) and (root/'.analysis/work/xx-product-maintained-xx.cpp').read_bytes()==(root/producer.UNIT).read_bytes(),'real module-name source transport and unchanged maintained TU')
    for short,path in producer.SOURCES.items():
        need((root/('.analysis/work/xx-product-source-'+short)).read_bytes()==(unit if short=='xx.cpp' else (root/path).read_bytes()),'actual compiler source input: '+short)
    extract=producer.build.response('base.lib',['*'+m.name for m in members])
    need((root/'.analysis/work/xx-product-extract.rsp').read_bytes()==extract and (root/'.analysis/work/xx-product-library.rsp').read_bytes()==producer.library_response(members) and (root/'.analysis/work/xx-product-link.lnk').read_bytes()==producer.link_response(files),'literal native extract/build/link responses and original member/link order')
    cfg=tomllib.loads((root/'config/toolchain.toml').read_text());dos=['/usr/bin/wine-stable',str(root/cfg['paths']['msdos_player']),'-e','-x']
    phases=[('extract-current-library',dos+['tlib','@extract.rsp'],0)]
    for number in (1,2):
        for label,argv in [('compile-asm',dos+[r'C:\BC45\BCC.EXE',*producer.ASM_FLAGS,'xx.cpp']),('compile-native',dos+[r'C:\BC45\BCC.EXE',*producer.OBJECT_FLAGS,'xx.cpp']),('library',dos+['tlib',r'@probe\xxwhole\library.rsp']),('link',dos+['tlink',r'@probe\xxwhole\link.lnk'])]:phases.append((f'round{number}-{label}',argv,0))
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'one extraction and two actual BCC native-object/TLIB/whole-product TLINK rounds')
    for phase in r['native_phases']:
        log=(root/('.analysis/work/xx-product-'+phase['label']+'.log')).read_bytes()
        need(sha(log)==phase['log_sha256'],'whole actual native phase log')
        if 'compile-' in phase['label']:need(log.startswith(r['compiler']['banner'].encode()+b'\r\n'),'real scoped compiler banner')
    mini_review=json.loads((root/producer.MINI_REVIEW).read_bytes())
    original=(WORK/'vendor/xx.obj').read_bytes()
    transported={n:(root/('.analysis/work/xx-product-source-'+n)).read_bytes() for n in producer.NAMES}
    vectors=[];rows=[]
    for round in r['rounds']:
        need(set(round['outputs'])=={'asm','obj','lib','exe','map'},'five complete raw compiler/native-object/library/link outputs')
        vector={}
        for kind,meta in round['outputs'].items():
            data=(root/meta['path']).read_bytes();need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),'complete actual normal-link output');vector[kind]=data
        observed=compare_members(members,library_members(vector['lib']),{'xx':vector['obj']})
        need(round['library']==observed and observed['contextual_members_unchanged']==892 and observed['replaced_members']==['xx'],'same893 positions,all892 surrounding member program records unchanged,only real source xx replaced')
        need(describe_omf(vector['obj'])['valid'],'valid complete actual native xx OMF')
        need(segment_definitions(vector['obj'])[1:]==segment_definitions(mini['obj'])[1:] and
            [n for at,n in code_publics(vector['obj'],1)]==[n for at,n in code_publics(original,1)] and
            externs(vector['obj'])==externs(original),'native storage and all original public/imported interfaces')
        procedures=native_bodies(vector['obj'],vector['asm'],transported,
            mini_review['original_bodies'],mini_review['candidate_bodies'])
        need(round['native_procedures']==procedures,'recomputed actual native source/LINNUM procedure extents')
        rows.append(procedures);vectors.append(vector)
    need(vectors[0]==vectors[1] and rows[0]==rows[1],'whole raw ASM/native OBJ/LIB/EXE/MAP pair equality,without normalization')
    v=vectors[0];source=parse_mz(v['exe']);target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());need(source.valid and target.valid,'actual full native MAINL MZ and pinned Japanese decoded MZ')
    table=v['map'].decode();coordinates={}
    for segment,offset,size,kind,name in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]{4})\s+C=(CODE|DATA|BSS)\s+S=(_TEXT|_DATA|_BSS)\s+G=\S+\s+M=xx\s+ACBP=\S+\s*$',table,re.M):
        need(kind not in coordinates,'one actual whole-program xx segment owner');coordinates[kind]=(int(segment,16),int(offset,16),int(size,16))
    definitions=segment_definitions(v['obj']);code_size=definitions[0]['size']
    need(set(coordinates)=={'CODE','DATA','BSS'} and coordinates['CODE']==(0,0x580D,code_size) and coordinates['DATA'][1:]==(0x1172,18) and coordinates['BSS'][1:]==(0x2876,10) and coordinates['DATA'][0]==coordinates['BSS'][0],'actual original xx positions and complete native CODE/DATA/BSS extents')
    fields=literal_fields(v['obj']);p,iterated=initialized_payload(v['obj']);base=coordinates['CODE'][1];image=bytearray(p[1,i] for i in range(code_size));mz=[];names=externs(v['obj'])
    need(len(fields)==187 and not iterated,'all187 actual native compiler fields and dense LEDATA ownership')
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
    original_bodies=mini_review['original_bodies'];op,_=initialized_payload(original)
    prefix=procedures[10]['start']+procedures[10]['size']+24
    need(prefix==2822 and bytes(op[1,i] for i in range(prefix))==bytes(p[1,i] for i in range(prefix)),
        'entire original2822-byte object prefix through the complete call bank')
    prefix_fields=[[f for f in literal_fields(obj) if f['segment']==1 and f['site']<prefix]
        for obj in (original,v['obj'])]
    need(prefix_fields[0]==prefix_fields[1] and len(prefix_fields[0])==92,
        'all92 original prefix fields agree literally in emitted order')
    need(source.program_image[base:base+prefix]==target.program_image[base:base+prefix],
        'the complete2822-byte linked prefix also agrees at the original position')
    call_start=procedures[8]['start']
    call_fields=[[f for f in fields if call_start<=f['site']<prefix] for fields in prefix_fields]
    need(call_start==1327 and prefix-call_start==1495 and call_fields[0]==call_fields[1] and
        len(call_fields[0])==88,'complete1495-byte native call bank and88 literal ordered fields')
    forward_calls=[]
    for owner,offset,callee in [(11,630,21),(11,719,21),(11,794,18),
        (19,62,21),(31,102,32),(32,571,33)]:
        pair=[]
        for obj,data,bodies,bias in [(original,op,original_bodies,0x580D),
            (v['obj'],p,procedures,0)]:
            at=bodies[owner]['start']-bias+offset;destination=bodies[callee]['start']-bias
            selected=[f for f in literal_fields(obj) if f['segment']==1 and f['site']==at]
            need(selected==[dict(segment=1,site=at,location_type=3,width=4,
                segment_relative=True,frame_method=5,frame=None,target_method=0,
                target=1,addend=destination)] and data[1,at-1]==0x9A,
                'original five-byte forward FAR CALL and literal native CODE field')
            pair.append(selected[0])
        forward_calls.append(dict(owner=original_bodies[owner]['name'],offset=offset,
            callee=original_bodies[callee]['name'],original_and_candidate_fields=pair))
    need(bytes(op[2,i] for i in range(18))==bytes(p[2,i] for i in range(18)),
        'entire original/current18-byte initialized DATA')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    dense(source.program_image,[dict(q,start=base+q['start']) for q in procedures],decoder)
    storage=native_storage(source.program_image,base,procedures,code_size,v['obj'])
    call_tables,_=classify(source.program_image,[dict(name=original_bodies[i]['name'],
        start=base+procedures[i]['start'],size=procedures[i]['size']) for i in (8,9,10)],decoder)
    comparator=comparator_codegen(original,v['obj'],procedures[2]['start'])
    compatibility=compatible_codegen(original,v['obj'],procedures[4]['start'],
        procedures[2]['start'],procedures[3]['start'])
    destruction=destruction_codegen(original,v['obj'],original_bodies,procedures)
    exception_handler=handler_codegen(original,v['obj'],original_bodies,procedures)
    catch_storage=catch_storage_codegen(original,v['obj'],original_bodies,procedures,native=True)
    fixup_blocks=[native_fixup_blocks(obj) for obj in (original,v['obj'])]
    handler_blocks=[]
    need(original_bodies[29]['name']=='_ExceptionHandler','actual handler procedure identity')
    for blocks,start in zip(fixup_blocks,[original_bodies[29]['start']-0x580D,procedures[29]['start']]):
        handler_blocks.append([dict(block_start=b['start'],relative_sites=[f['site']-start
            for f in b['literal_fields'] if start<=f['site']<start+880]) for b in blocks
            if any(start<=f['site']<start+880 for f in b['literal_fields'])])
    need([q['relative_sites'] for q in handler_blocks[0]]==[[372,294],[724,703,700]] and
        [[site for q in pair for site in q['relative_sites']] for pair in handler_blocks]==
        exception_handler['literal_field_offset_order'],
        'handler literal order follows its actual native CODE-block ownership')
    original_publics=code_publics((WORK/'vendor/xx.obj').read_bytes(),1)
    need(externs(v['obj'])==externs((WORK/'vendor/xx.obj').read_bytes()),
        'normal-library xx retains all18 original EXTDEF names in literal order')
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
    frame_allocations=[int.from_bytes(data[start+14:start+16],'little') for data,start in
        [(target.program_image,original_bodies[18]['start']),
         (source.program_image,base+procedures[18]['start'])]]
    need(frame_allocations==[390,342],'original/current Raise storage gap remains explicit')
    raw_equal=v['exe']==target.raw;map_equal=v['map']==(WORK/'obj/th03/mainl.map').read_bytes()
    need(not raw_equal and not map_equal,'current full product remains a raw-different candidate,not exact acceptance')
    tail_start=base+procedures[36]['start'];tail_size=code_size-procedures[36]['start']
    body_comparisons=[]
    need(len(original_bodies)==len(procedures)==50,'complete original/current function comparison scope')
    for old,new in zip(original_bodies,procedures):
        at=base+new['start']
        body_comparisons.append(dict(name=old['name'],original_bytes=old['size'],candidate_bytes=new['size'],
            size_delta=new['size']-old['size'],raw_equal=source.program_image[at:at+new['size']]==target.program_image[old['start']:old['start']+old['size']]))
    need(body_comparisons[15]==dict(name='dispatchException',original_bytes=140,candidate_bytes=140,size_delta=0,raw_equal=True),'complete140-byte normal-linked dispatcher matches the fixed target without normalization')
    need(body_comparisons[2]==dict(name='sameTypeID',original_bytes=157,candidate_bytes=157,
        size_delta=0,raw_equal=True) and base+procedures[2]['start']==0x583E and
        not any(0x583E<=q.linear<0x58DB for q in source.relocations),
        'complete157-byte normal-linked comparator at the original address,without native fields')
    return dict(complete=True,source_acceptance=False,accepted_source_bytes=0,whole_product_linked=True,whole_product_accepted=False,
        selected_build_report_sha256=sha(raw),review_driver_sha256=sha((root/'scripts/review_th03_mainl_xx_work.py').read_bytes()),source_sha256=r['source_sha256'],baseline=baseline,
        normal_library_members=893,unchanged_surrounding_members=892,source_CRT_providers=29,reused_source_CRT_providers=28,reused_source_provider_names=previous_providers,retained_project_objects=36,retained_binary_inputs=39,
        original_file_bytes=len(target.raw),candidate_file_bytes=len(v['exe']),original_header_bytes=target.header.header_size,candidate_header_bytes=source.header.header_size,
        original_relocation_count=len(target.relocations),candidate_relocation_count=len(source.relocations),original_MZ_relocations=[[q.segment,q.offset] for q in target.relocations],candidate_MZ_relocations=[[q.segment,q.offset] for q in source.relocations],
        whole_EXE_raw_equal=raw_equal,whole_MAP_raw_equal=map_equal,original_xx_CODE_bytes=12622,candidate_xx_CODE_bytes=code_size,native_module_coordinates=coordinates,
        original_RTTI_tail_bytes=1735,candidate_RTTI_tail_bytes=tail_size,RTTI_tail_raw_equal=source.program_image[tail_start:tail_start+tail_size]==target.program_image[0x8294:0x895B],
        raw_function_comparisons=body_comparisons,
        candidate_literal_native_fields=fields,candidate_ordered_xx_MZ_words=mz,candidate_LIDATA_records=iterated,actual22_public_bindings=bindings,all_source_CODE_bytes_resolved=True,all18_interfaces_resolved_to_real_library=True,original_and_candidate_EXTDEF_vectors=[externs((WORK/'vendor/xx.obj').read_bytes()),externs(v['obj'])],literal_EXTDEF_vector_equal=True,
        native_object_compiler=True,native_procedures=procedures,native_storage=storage,
        original_prefix_raw_bytes=prefix,original_and_candidate_prefix_fields=prefix_fields,
        original_call_bank_raw_bytes=prefix-call_start,original_and_candidate_call_bank_fields=call_fields,
        restored_forward_far_calls=forward_calls,RaiseException_stack_allocations=frame_allocations,
        comparator_codegen=comparator,compatibility_codegen=compatibility,destruction_codegen=destruction,
        exception_handler_codegen=exception_handler,catch_storage_codegen=catch_storage,
        original_and_candidate_CODE_fixup_blocks=fixup_blocks,handler_CODE_fixup_blocks=handler_blocks,
        native_call_adapter_tables=call_tables,
        target_and_source_RTTI_probes=probes,target_and_source_real_memcpy_raise_probe=raise_pair,alternate_stack_offset=0xFF10,alternate_stack_real_memcpy_raise_probe=alternate,raw_Raise_argument_copy_bytes=71,actual_native_handler_sha256=sha(handler),two_whole_raw_vectors_repeated=True,all_available_SDK_headers_bound=64,
        original_cold_rebuilt=False,ancestor_runtime_chain_rebuilt=False,physical_DOS_execution_claimed=False)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];r=review(root);(root/REVIEW).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('source_sha256','candidate_literal_native_fields','original_MZ_relocations','candidate_MZ_relocations')},indent=2))
