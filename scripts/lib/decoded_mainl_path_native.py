"""Complete DOS fullpath/current-directory/drive/DBCS native source ownership."""
import json
import re
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from build_th03_mainl_path_work import SOURCES,DRIVER,REPORT,reused_pairs,library_response,link_response
from build_th03_mainl_display_work import literal_fields,payload
from lib.decoded_mainl_loadprog_native import sha
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_file_native import byte_map
from lib.borland_library import library_members,compare_members
from lib.omf import parse_omf,describe_omf
from lib.pc98 import parse_mz
from lib.op_asset_native import extent
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

PREFIX='th03-mainl-decoded-crt-'
DS,PATH_DATA,PATH_INIT=0xE3F,0x1158,0x132A
LAYOUT={
 'fullpath':dict(base=0x4706,size=834,fields=18,group='08ff02ff03',externals=['__ctype','_toupper','__getdcwd','__dos_getdrive','_free','_malloc','_realloc','_strcpy','_strlen','___path_isdbcsleadbyte','___path_issbcs'],
   procedures=[('is_separator',0,31,'ret',2,False),('is_sbcs_separator',31,58,'ret',8,False),('__fullpath',89,745,'retf',0,True)]),
 'getdcwd':dict(base=0x4A48,size=157,fields=5,group='08ff03ff02',externals=['_malloc','_errno','_strcpy','_strlen'],procedures=[('__getdcwd',0,157,'retf',0,True)]),
 '_pathops':dict(base=0x430C,size=208,fields=8,group='0aff03ff02',externals=[],procedures=[('path_initialize',0,73,'ret',0,False),('___path_isdbcsleadbyte',73,37,'retf',0,True),('___path_issbcs',110,98,'retf',0,True)]),
 'dosgdriv':dict(base=0x2F68,size=48,fields=0,group='08ff02ff03',externals=[],procedures=[('__dos_getdrive',0,22,'retf',0,True),('__dos_setdrive',22,26,'retf',0,True)])}
SOURCE_MAP={PREFIX+n.removeprefix('_'):(p,'vendor/'+n+'.obj') for n,p in SOURCES.items()}
SOURCE_MAP.update({PREFIX+'pathops-'+kind:(SOURCES['_pathops'],'vendor/_pathops.obj') for kind in ('data','init')})


def need(value,message):
    if not value:raise ValueError('MAINL DOS path native: '+str(message))


def selected(root,work,files):
    raw=(root/REPORT).read_bytes();r=json.loads(raw);reused,meta=reused_pairs(root,work,files)
    need(r['complete'] and not r['source_acceptance'] and not r['whole_product_cold_rebuilt'] and r['retained_project_objects']==36 and
         r['source_sha256']=={p:sha((root/p).read_bytes()) for p in SOURCES.values()} and r['driver_sha256']==sha((root/DRIVER).read_bytes()) and
         r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()) and r['reused_sources']==meta,'path source/recipe/cold and reused actual CRT pairs')
    current=(work/'crt.lib').read_bytes();members=library_members(current)
    need(r['current_library_sha256']==sha(current) and len(members)==893,'normal library identity')
    need(all((root/('.analysis/work/path-source-'+n+'.asm')).read_bytes()==(root/p).read_bytes() for n,p in SOURCES.items()) and
         (root/'.analysis/work/path-library.rsp').read_bytes()==library_response(members) and
         (root/'.analysis/work/path-link.lnk').read_bytes()==link_response(files),'actual full source and response inputs')
    config=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/config['paths']['wine_prefix']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t']
    dos=['/usr/bin/wine-stable',str(root/config['paths']['msdos_player']),'-e','-x'];phases=[]
    for n in (1,2):
        phases += [(f'round{n}-{name}',tasm+[name+'.asm',name+'.obj'],0) for name in SOURCES]
        phases += [(f'round{n}-library',dos+['tlib',r'@probe\pathlib.rsp'],0),(f'round{n}-link',dos+['tlink',r'@probe\pathctx.lnk'],0)]
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'actual serial assembly/library/link rounds')
    vectors=[]
    for row in r['rounds']:
        need(set(row['outputs'])==set(SOURCES)|{'lib','exe','map'},'complete selected output vector');v={}
        for name,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'complete current raw native output');v[name]=b
        review=compare_members(members,library_members(v['lib']),dict(reused,**{n:v[n] for n in SOURCES}))
        need(row['library']==review and review['contextual_members_unchanged']==884,'all893 member positions and884 unchanged current members')
        need(v['exe']==(work/'bin/th03/mainl.target.exe').read_bytes() and v['map']==(work/'obj/th03/mainl.map').read_bytes(),'whole pinned Japanese decoded EXE and retained MAP equality')
        vectors.append(v)
    need(vectors[0]==vectors[1],'whole raw four-OBJ/LIB/EXE/MAP repetition')
    return vectors[0],r,sha(raw)


def verify(root,work,target,candidate,graph,files):
    v,r,report_sha=selected(root,work,files);table=v['map'].decode();linked=parse_mz(v['exe']);need(linked.valid,'complete native linked MZ')
    owners=[];modules={}
    for name,layout in LAYOUT.items():
        base,size=layout['base'],layout['size'];raw=v[name];original=(work/('vendor/'+name+'.obj')).read_bytes();d=describe_omf(raw)
        need(d['valid'] and d['module_name']==name+'.asm' and d['translator_comments']==['Turbo Assembler  Version 5.0'] and d['dependency_paths']==[name+'.asm'],'actual complete maintained path TU')
        pathops=name=='_pathops';defs=[(1,'_TEXT','CODE',size),(2,'_DATA','DATA',16 if pathops else 0),(3,'_BSS','BSS',0)]
        if pathops:defs.append((4,'_INIT_','INITDATA',6))
        need(segment_definitions(raw)==[dict(index=i,name=n,**{'class':c},overlay='',size=s) for i,n,c,s in defs] and
             [q.data[0] for q in parse_omf(raw) if q.name=='SEGDEF']==[0x28]+[0x48]*(len(defs)-1) and
             [q.data.hex() for q in parse_omf(raw) if q.name=='GRPDEF']==[layout['group']],'literal native BYTE CODE/WORD DATA/BSS/INIT and complete group order')
        pubs=[(off,symbol) for symbol,off,_,_,_,public in layout['procedures'] if public]
        need(code_publics(raw,1)==code_publics(original,1)==pubs and externs(raw)==externs(original)==layout['externals'],'complete public/external identities')
        for segment in range(2,len(defs)+1):
            need(code_publics(raw,segment)==code_publics(original,segment)==([(0,'___path_dbcs_vector'),(4,'___path_dbcs_default')] if pathops and segment==2 else []),'complete DATA/BSS/INIT publics')
        fields,old_fields=literal_fields(raw),literal_fields(original)
        need(payload(raw)==payload(original) and len(fields)==len(old_fields)==layout['fields'],'entire initialized payload and actual field inventory')
        old_by_site={(f['segment'],f['site']):f for f in old_fields}
        need(len(old_by_site)==len(fields) and len({(f['segment'],f['site']) for f in fields})==len(fields) and all(f==old_by_site[(f['segment'],f['site'])] for f in fields),'all field identities/geometry without reordering either literal stream')
        need(table.count(f'0000:{base:04X} {size:04X} C=CODE   S=_TEXT          G=(none)  M={name:<10} ACBP=28')==1,'complete real library CODE MAP contribution')
        for off,symbol in pubs:need(address(table,symbol)==(0,base+off),'both native public MAP tables')
        coordinates={1:(0,base,size)}
        if pathops:
            coordinates.update({2:(DS,PATH_DATA,16),4:(DS,PATH_INIT,6)})
            for offset,count,cls,segment in [(PATH_DATA,16,'DATA','_DATA'),(PATH_INIT,6,'INITDATA','_INIT_')]:
                need(len(re.findall(rf'(?m)^\s*{DS:04X}:{offset:04X}\s+{count:04X}\s+C={cls}\s+S={segment}\s+G=DGROUP\s+M=_pathops\s+ACBP=48\s*$',table))==1,'complete actual DBCS DATA/INIT MAP contribution')
            need(address(table,'___path_dbcs_vector')==(DS,PATH_DATA) and address(table,'___path_dbcs_default')==(DS,PATH_DATA+4),'complete real DBCS data public offsets')
        buffers={};relocations={segment:[] for segment in coordinates}
        for segment,(_,_,count) in coordinates.items():
            data=byte_map(raw,segment);need(set(data)==set(range(count)),'all initialized bytes dense with no implicit or invented holes');buffers[segment]=bytearray(data[i] for i in range(count))
        need(not byte_map(raw,3),'no BSS file initializer')
        observed=[];far_calls=[]
        for f in fields:
            segment,site=f['segment'],f['site'];need(segment in coordinates and f['segment_relative'],'complete actual segment-relative native field')
            image=buffers[segment];product_segment,product_base,_=coordinates[segment]
            need(site+f['width']<=len(image),'whole actual native field')
            if f['target_method']==2:
                symbol=layout['externals'][f['target']-1];seg,off=address(table,symbol);off+=f['addend']
            else:
                need(f['target_method']==0 and pathops and f['target'] in (1,2),'only real local CODE/DATA fields')
                seg,off,_=coordinates[f['target']];off+=f['addend'];symbol='path_initialize' if f['target']==1 else 'DBCS DATA'
            if f['location_type']==3:
                need(segment==1 and f['width']==4 and f['frame_method']==5 and f['frame'] is None and seg==0 and f['addend']==0 and image[site-1:site+4]==b'\x9a\0\0\0\0','ordinary native external far CALL')
                image[site-1:site+4]=b'\x90\x0e\xe8'+((off-(base+site+4))&65535).to_bytes(2,'little');far_calls.append(dict(site=base+site-1,symbol=symbol,target=off))
            else:
                need(f['width']==2 and f['location_type'] in (1,2),'real native offset or segment WORD')
                if f['location_type']==2:
                    need((name,segment,site,f['frame_method'],f['frame'],f['target_method'],f['target'],f['addend'])==('_pathops',1,51,1,1,0,2,0),'sole actual DGROUP segment immediate')
                    value=seg;relocations[segment].append([product_segment,product_base+site])
                elif segment==4:
                    need((site,f['frame_method'],f['frame'],f['target_method'],f['target'],f['addend'])==(2,5,None,0,1,0),'real near startup callback offset WORD')
                    value=off
                else:
                    need((f['frame_method'],f['frame'],seg)==(1,1,DS),'actual DGROUP offset field');value=off
                image[site:site+2]=value.to_bytes(2,'little')
            observed.append(dict(f,symbol=symbol,product_site=product_base+site,resolved_target=[seg,off]))
        images={segment:bytes(data) for segment,data in buffers.items()}
        if pathops:
            need(images[2]==bytes(16) and images[4]==bytes((0,15))+base.to_bytes(2,'little')+bytes(2),'complete semantic zero vector/fallback pairs and near priority15 startup record')
            need(relocations[1]==[[0,base+51]] and not relocations[2] and not relocations[4],'only the real CODE segment immediate relocates; INIT offset does not')
        for segment,image in images.items():
            seg,off,_=coordinates[segment];start=seg*16+off
            need(image==linked.program_image[start:start+len(image)],'whole independently resolved linked native scope');extent((target,candidate),image,seg,off,relocations[segment])
        image=images[1];decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;ins=list(decoder.disasm(image,base));bounds={i.address for i in ins}
        need(sum(i.size for i in ins)==size,'complete dense native instructions')
        for i in ins:
            if i.mnemonic.startswith(('j','loop')):need(i.operands[0].type==X86_OP_IMM and i.operands[0].imm in bounds,'all local branches enter complete instructions')
        procedures=[]
        for symbol,offset,count,ret,pop,public in layout['procedures']:
            body=[i for i in ins if base+offset<=i.address<base+offset+count]
            need(sum(i.size for i in body)==count and body[-1].mnemonic==ret and body[-1].op_str==(str(pop) if pop else ''),'complete near/far body and actual caller/callee argument cleanup')
            procedures.append(dict(name=symbol,offset=offset,size=count,return_kind=ret,public=public,callee_pop_bytes=pop))
        for segment,image in images.items():
            seg,off,_=coordinates[segment];procs=procedures if segment==1 else [];suffix='' if segment==1 else '-data' if segment==2 else '-init';unit=PREFIX+name.removeprefix('_')+suffix
            owners.append(dict(unit_id=unit,name=unit.removeprefix(PREFIX),source=SOURCES[name],object='vendor/'+name+'.obj',origin='library',segment=seg,offset=off,start=seg*16+off,
                size=len(image),coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=sha(image),candidate_sha256=sha(image),ordered_relocations=relocations[segment],code_bytes=len(image) if segment==1 else 0,
                initialized_data_bytes=len(image) if segment!=1 else 0,procedure_count=len(procs),procedures=procs,private_data_bytes=0,private_bss_bytes=0,
                maintained_native_object=r['rounds'][0]['outputs'][name]['path'],abi='far cdecl APIs; near pop2/pop8 fullpath helpers and near startup callback'))
        modules[name]=dict(native_fields=observed,original_literal_native_fields=old_fields,far_calls=far_calls,native_field_order_preserved=True,ordered_scope_relocations=relocations[1])
    return dict(owners=owners,modules=modules,source_sha256=r['source_sha256'],source_CODE_bytes=1247,source_initialized_DATA_bytes=22,procedures=9,
        selected_build_report_sha256=report_sha,selected_assembly_library_link_rounds=2,normal_library_members=893,untouched_current_library_members=884,
        source_CRT_providers_in_selected_library=15,reused_natural_farheap_exec_loadprog_dosconstruct=True,retained_project_objects=36,full_raw_vector_repeated=True,whole_EXE_MAP_equal=True,
        source_padding_added=False,BSS_file_byte_credit=0,original_cold_rebuilt=False,ancestor_runtime_replayed=False,physical_DOS_execution_claimed=False,whole_product_accepted=False)


if __name__=='__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['path_native'],indent=2))
