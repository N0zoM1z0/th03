"""Natural C++ allocation and exception providers, including actual inline EH data."""
import json
import re
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from build_th03_mainl_exception_work import SOURCES,FLAGS,DRIVER,REPORT,TOOLCHAIN,compiler_context,reused_pairs,library_response,link_response
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.omf import describe_omf,parse_omf
from lib.pc98 import parse_mz
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_file_native import byte_map
from lib.op_asset_native import extent
from lib.op_shared_native import address as map_address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

PREFIX='th03-mainl-decoded-crt-'
DS,NEW_DATA,NEW_INIT,NEW_EXIT=0xE3F,0xEEA,0x1318,0x1336
LAYOUT={
 'new':dict(base=0x3273,size=754,instructions=[(28,107),(135,46),(181,81),(262,67),(367,91),(458,39),(621,77)],data=[(0,28),(329,38),(497,58),(555,66),(698,56)]),
 'xalloc':dict(base=0x5251,size=513,instructions=[(0,91),(127,120),(247,67),(380,77)],data=[(91,36),(314,66),(457,56)]),
 'xmsg':dict(base=0x5452,size=955,instructions=[(36,167),(239,171),(410,94),(518,83),(637,185)],data=[(0,36),(203,36),(504,14),(601,36),(822,56),(878,19),(897,58)])}
SOURCE_MAP={PREFIX+n:(p,'vendor/'+n+'.obj') for n,p in SOURCES.items()}
SOURCE_MAP.update({PREFIX+'new-'+n:(SOURCES['new'],'vendor/new.obj') for n in ('data','init','exit')})

MAP_NAMES={
 '@xnew_handler$qv':'xnew_handler()',
 '@set_new_handler$qnqv$v':'set_new_handler(void(far*)())',
 '@$bnew$qui':'operator new(unsigned int)',
 '@$bdele$qnv':'operator delete(void far*)',
 '@__RefDestructorCount$qv':'__refdestructorcount()',
 '@_ThrowException$qnvt1t1t1uiuiuinuc':'_throwexception(void far*,void far*,void far*,void far*,unsigned int,unsigned int,unsigned int,unsigned char far*)',
 '@xalloc@$bctr$qmx6stringui':'xalloc::xalloc(const string far&,unsigned int)',
 '@xalloc@raise$qv':'xalloc::raise()',
 '@xmsg@$bctr$qmx6string':'xmsg::xmsg(const string far&)',
 '@xmsg@$bctr$qmx4xmsg':'xmsg::xmsg(const xmsg far&)',
 '@xmsg@$bdtr$qv':'xmsg::~xmsg()',
 '@xmsg@raise$qv':'xmsg::raise()',
 '@xmsg@$basg$qmx4xmsg':'xmsg::operator =(const xmsg far&)',
 '@string@$bctr$qmx6string':'string::string(const string far&)',
 '@string@$bctr$qnxc':'string::string(const char far*)',
 '@string@$bdtr$qv':'string::~string()'}


def address(table,symbol):
    return map_address(table,MAP_NAMES.get(symbol,symbol))


def selected(root,work,files):
    reused,meta=reused_pairs(root,work,files)
    raw=(root/REPORT).read_bytes();r=json.loads(raw)
    need(r['complete'] and not r['source_acceptance'] and r['accepted_source_bytes']==0 and not r['whole_product_cold_rebuilt'] and r['retained_project_objects']==36,'bounded native build receipt,not self-authorized acceptance')
    need(r['source_sha256']=={p:sha((root/p).read_bytes()) for p in SOURCES.values()} and r['driver_sha256']==sha((root/DRIVER).read_bytes()) and r['compiler_flags']==FLAGS and r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()) and r['reused_sources']==meta,'current maintained C++ source/driver/flags/cold/reused context')
    members=library_members((work/'crt.lib').read_bytes());need(len(members)==893 and r['current_library_sha256']==sha((work/'crt.lib').read_bytes()),'retained normal library identity')
    need(all((root/('.analysis/work/exception-native-source-'+n+'.cpp')).read_bytes()==(root/p).read_bytes() for n,p in SOURCES.items()) and
         (root/'.analysis/work/exception-native-library.rsp').read_bytes()==library_response(members) and (root/'.analysis/work/exception-native-link.lnk').read_bytes()==link_response(files),'actual preserved source and response inputs')
    config=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/config['paths']['wine_prefix'];dos=['/usr/bin/wine-stable',str(root/config['paths']['msdos_player']),'-e','-x'];phases=[]
    for number in (1,2):
        phases += [(f'round{number}-{n}',dos+[r'C:\BC45\BCC.EXE',*FLAGS,n+'.cpp'],0) for n in SOURCES]
        phases += [(f'round{number}-library',dos+['tlib',r'@probe\excnlib.rsp'],0),(f'round{number}-link',dos+['tlink',r'@probe\excnat.lnk'],0)]
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'two actual serial compiler/TLIB/TLINK rounds')
    compiler=compiler_context(root);need(r['compiler']==compiler,'scoped optimizing compiler and runtime identity')
    for phase in r['native_phases']:
        log=(root/('.analysis/work/exception-native-'+phase['label']+'.log')).read_bytes()
        need(sha(log)==phase['log_sha256'],'actual preserved native phase log')
        if phase['label'].endswith(tuple(SOURCES)):
            need(log.startswith(compiler['banner'].encode()+b'\r\n'),'actual optimizing compiler banner')
    vectors=[];headers={}
    for row in r['rounds']:
        need(set(row['outputs'])==set(SOURCES)|{'lib','exe','map'},'complete selected output vector');v={}
        for name,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'whole current native output identity');v[name]=b
        need(row['library']==compare_members(members,library_members(v['lib']),dict(reused,**{n:v[n] for n in SOURCES})) and row['library']['contextual_members_unchanged']==871,'all893 positions and871 other current library members')
        for n in SOURCES:
            d=describe_omf(v[n]);need(d['valid'] and d['module_name']==n+'.cpp' and d['translator_comments']==[compiler['translator']],'real maintained high-level compiler input')
            deps=[]
            for dependency in d['dependency_paths']:
                dep=dependency.replace(chr(92),'/');deps.append(dep)
                if dep.upper().startswith('C:/TC4/INCLUDE/'):
                    filename=dep.rsplit('/',1)[1].upper();h=(prefix/'drive_c/TC4/INCLUDE'/filename).read_bytes()
                    need(h==(root/config['paths']['tc40j_install']/'INCLUDE'/filename).read_bytes(),'consumed active SDK equals pinned installation');headers[dep]=sha(h)
                else:need(dep==n+'.cpp','no undeclared source dependency')
            need(n+'.cpp' in deps,'actual source dependency record')
        vectors.append(v)
    need(vectors[0]==vectors[1] and r['vendor_header_sha256']==headers,'complete raw OBJ/LIB/EXE/MAP repetition and every consumed SDK header')
    need(r['whole_EXE_equal'] and r['whole_MAP_equal'] and all(v['exe']==(work/'bin/th03/mainl.target.exe').read_bytes() and v['map']==(work/'obj/th03/mainl.map').read_bytes() for v in vectors),'whole pinned Japanese decoded EXE and retained MAP equality')
    return vectors[0],r,sha(raw)


def verify(root,work,target,candidate,graph,files):
    v,r,report_sha=selected(root,work,files);table=v['map'].decode();linked=parse_mz(v['exe'])
    need(linked.valid,'complete linked C++ MZ');owners=[];modules={}
    for name,layout in LAYOUT.items():
        raw=v[name];original=(work/('vendor/'+name+'.obj')).read_bytes();base,size=layout['base'],layout['size']
        need(segment_definitions(raw)==segment_definitions(original),'complete original C++ segment definitions')
        for kind in ('SEGDEF','GRPDEF'):
            need([q.data for q in parse_omf(raw) if q.name==kind]==[q.data for q in parse_omf(original) if q.name==kind],'literal original segment packing/group order')
        pubs={i:code_publics(raw,i) for i in range(1,6)}
        need(pubs=={i:code_publics(original,i) for i in range(1,6)} and externs(raw)==externs(original),'every original public/external identity')
        fields=literal_fields(raw)
        need(fields==literal_fields(original) and payload(raw)==payload(original),'complete native initialized payload and literal ordered fields without normalization')
        need(len(fields)=={'new':49,'xalloc':24,'xmsg':49}[name],'complete original C++ field inventory')
        need(len(re.findall(rf'(?m)^\s*0000:{base:04X}\s+{size:04X}\s+C=CODE\s+S=_TEXT\s+G=\(none\)\s+M={name}\s+ACBP=28\s*$',table))==1,'complete normal-library C++ CODE allocation')
        coordinates={1:(0,base,size)}
        if name=='new':
            coordinates.update({2:(DS,NEW_DATA,24),4:(DS,NEW_INIT,6),5:(DS,NEW_EXIT,6)})
            for i,cls,section in ((2,'DATA','_DATA'),(4,'INITDATA','_INIT_'),(5,'EXITDATA','_EXIT_')):
                seg,off,count=coordinates[i]
                need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{count:04X}\s+C={cls}\s+S={section}\s+G=DGROUP\s+M=new\s+ACBP=48\s*$',table))==1,'complete static xalloc/handler/startup/shutdown allocation')
        for i,entries in pubs.items():
            for off,symbol in entries:
                seg,start,_=coordinates[i];need(address(table,symbol)==(seg,start+off),'all actual public addresses in normal-library link')
        classified=[]
        for kind,key in [('CODE','instructions'),('inline-CS-data','data')]:
            classified += [dict(offset=o,size=s,kind=kind) for o,s in layout[key]]
        positions=[i for q in classified for i in range(q['offset'],q['offset']+q['size'])]
        need(len(positions)==size and set(positions)==set(range(size)),'complete nonoverlapping instruction/inline-data ownership')
        code_positions={i for o,s in layout['instructions'] for i in range(o,o+s)}
        buffers={};relocations={i:[] for i in coordinates}
        for i,(seg,off,count) in coordinates.items():
            data=byte_map(raw,i);missing=set(range(count))-set(data)
            need(set(data)<=set(range(count)) and missing==(set(range(6)) if name=='new' and i==2 else set()),'dense initializers except actual six-byte static-object reserve')
            # No bytes are synthesized for the C++ object reserve. Both complete
            # real link rounds have already repeated and matched the target.
            linked_bytes=linked.program_image[seg*16+off:seg*16+off+count]
            buffers[i]=bytearray(data[k] if k in data else linked_bytes[k] for k in range(count))
        need(not byte_map(raw,3),'no BSS initializer/file credit');observed=[];far_calls=[]
        for f in fields:
            i,site=f['segment'],f['site'];need(i in coordinates and site+f['width']<=len(buffers[i]) and f['segment_relative'],'complete segment-relative C++ field')
            image=buffers[i];product_segment,product_base,_=coordinates[i]
            if f['target_method']==2:
                symbol=externs(raw)[f['target']-1];seg,off=address(table,symbol);off+=f['addend']
                need((f['frame_method'],f['frame'])==(5,None),'ordinary external target frame')
            else:
                need(f['target_method']==0 and f['target'] in coordinates,'real source segment target')
                seg,off,_=coordinates[f['target']];off+=f['addend'];symbol='private '+str(f['target'])
                need((f['frame_method'],f['frame'])==((1,1) if f['target']==2 else (5,None)),'original DGROUP or CODE frame')
            if f['location_type']==3:
                need(f['width']==4,'complete far pointer')
                if i==1 and site-1 in code_positions and image[site-1]==0x9A:
                    need(f['target_method']==2 and f['addend']==0 and image[site:site+4]==bytes(4),'real ordinary external far CALL')
                    if seg==product_segment:
                        image[site-1:site+4]=b'\x90\x0e\xe8'+((off-(product_base+site+4))&65535).to_bytes(2,'little')
                    else:
                        image[site:site+4]=off.to_bytes(2,'little')+seg.to_bytes(2,'little');relocations[i].append([product_segment,product_base+site+2])
                    far_calls.append(dict(site=product_base+site-1,symbol=symbol,target=[seg,off],relaxed=seg==product_segment))
                else:
                    image[site:site+4]=off.to_bytes(2,'little')+seg.to_bytes(2,'little');relocations[i].append([product_segment,product_base+site+2])
            else:
                need(f['width']==2 and f['location_type'] in (1,2),'actual offset/segment WORD')
                value=off if f['location_type']==1 else seg
                if f['location_type']==2:
                    need(f['addend']==0,'segment WORD has no hidden offset');relocations[i].append([product_segment,product_base+site])
                image[site:site+2]=value.to_bytes(2,'little')
            observed.append(dict(f,resolved_target=[seg,off],symbol=symbol))
        images={i:bytes(b) for i,b in buffers.items()}
        for i,image in images.items():
            seg,off,_=coordinates[i];need(image==linked.program_image[seg*16+off:seg*16+off+len(image)],'entire independently resolved C++ native image')
            extent((target,candidate),image,seg,off,relocations[i])
        decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;procedures=[];all_instructions=[]
        for off,count in layout['instructions']:
            ins=list(decoder.disasm(images[1][off:off+count],base+off));all_instructions+=ins
            need(sum(i.size for i in ins)==count and (ins[-1].mnemonic,ins[-1].op_str)==('retf',''),'complete original far cdecl body,excluding inline records')
            symbol=next((n for p,n in pubs[1] if p==off),'compiler-generated-'+str(off))
            procedures.append(dict(name=symbol,offset=off,size=count,return_kind='retf',callee_pop_bytes=0,public=any(p==off for p,_ in pubs[1])))
        bounds={i.address for i in all_instructions}
        for ins in all_instructions:
            if ins.mnemonic.startswith(('j','loop')):
                need(ins.operands[0].type==X86_OP_IMM and ins.operands[0].imm in bounds,'all branches enter real instructions,not inline EH records')
        for i,image in images.items():
            seg,off,_=coordinates[i];procs=procedures if i==1 else [];suffix={1:'',2:'-data',4:'-init',5:'-exit'}[i]
            reserved=6 if i==2 else 0;code=sum(n for _,n in layout['instructions']) if i==1 else 0
            owners.append(dict(unit_id=PREFIX+name+suffix,name=name+suffix,source=SOURCES[name],object='vendor/'+name+'.obj',origin='library',segment=seg,offset=off,start=seg*16+off,size=len(image),coordinate_space='decoded-load',canonical_file_offset=None,
                target_sha256=sha(image),candidate_sha256=sha(image),ordered_relocations=relocations[i],code_bytes=code,initialized_data_bytes=len(image)-code-reserved,uninitialized_file_data_bytes=reserved,
                procedure_count=len(procs),procedures=procs,private_data_bytes=0,private_bss_bytes=0,maintained_native_object=r['rounds'][0]['outputs'][name]['path'],abi='large-model16-bit far cdecl; native exception/type metadata and compiler-generated copy/destructor/startup/shutdown bodies'))
        modules[name]=dict(native_fields=observed,original_literal_native_fields=fields,far_calls=far_calls,complete_initialized_payload_equal=True,native_field_order_preserved=True,
            instruction_spans=[list(q) for q in layout['instructions']],inline_CS_data_spans=[list(q) for q in layout['data']],ordered_scope_relocations=relocations[1])
    need(sum(len(m['native_fields']) for m in modules.values())==122,'all122 original fields')
    return dict(owners=owners,modules=modules,source_sha256=r['source_sha256'],consumed_vendor_header_sha256=r['vendor_header_sha256'],compiler=r['compiler'],selected_build_report_sha256=report_sha,
        source_CODE_bytes=1563,source_inline_CS_DATA_bytes=659,source_initialized_DATA_bytes=689,source_uninitialized_file_DATA_bytes=6,procedures=16,
        selected_compiler_library_link_rounds=2,normal_library_members=893,untouched_current_library_members=871,source_CRT_providers_in_selected_library=28,reused_natural_CRT_pairs=19,retained_project_objects=36,
        full_raw_vector_repeated=True,whole_EXE_MAP_equal=True,source_padding_added=False,static_object_reserve_bytes_from_two_actual_links=True,source_initializer_added=False,BSS_file_byte_credit=0,
        original_cold_rebuilt=False,ancestor_runtime_replayed=False,physical_DOS_execution_claimed=False,whole_product_accepted=False)


if __name__=='__main__':
    from pathlib import Path
    from build_th03_mainl_resources_work import cold_context
    from build_th03_mainl_work import WORK
    root=Path(__file__).resolve().parents[2];_,files,graph=cold_context(root)
    target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());candidate=parse_mz((WORK/'bin/th03/mainl.exe').read_bytes())
    result=verify(root,WORK,target,candidate,graph,files)
    (root/'.analysis/work/mainl-exception-native-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('owners','modules','consumed_vendor_header_sha256')},indent=2))
