"""Complete buffered stream,position,translated write and DOS-interface source ownership."""
import json
import re
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from build_th03_mainl_stdio_work import SOURCES,DRIVER,REPORT,LAYOUT_HEADER,reused_pairs,library_response,link_response
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
DS,BUFFER_DATA,SETUP_INIT=0xE3F,0x116C,0x131E
LAYOUT={
 'fflush':dict(base=0x43fd,size=209,fields=2,group='08ff02ff03',externals=['_flushall', '___write'],procedures=[('_fflush', 0, 209, 'retf', 0, True)]),
 'flushall':dict(base=0x44ce,size=76,fields=3,group='08ff02ff03',externals=['__streams', '__nfile', '_fflush'],procedures=[('_flushall', 0, 76, 'retf', 0, True)]),
 'fseek':dict(base=0x451a,size=492,fields=6,group='08ff02ff03',externals=['_fflush', '_lseek', '__openfd'],procedures=[('buffered_bytes', 0, 137, 'ret', 4, False), ('_fseek', 137, 130, 'retf', 0, True), ('_ftell', 267, 225, 'retf', 0, True)]),
 'setvbuf':dict(base=0x4de9,size=289,fields=13,group='08ff02ff03',externals=['__streams', '_fseek', '_free', '_malloc', '__exitbuf', '__xfflush'],procedures=[('_setvbuf', 0, 289, 'retf', 0, True)]),
 'write':dict(base=0x5051,size=358,fields=9,group='08ff02ff03',externals=['__nfile', '_lseek', '__rtl_write', '__IOERROR', '__openfd'],procedures=[('___write', 0, 358, 'retf', 0, True)]),
 'writea':dict(base=0x51b7,size=91,fields=3,group='08ff03ff02',externals=['__IOERROR', '__openfd'],procedures=[('__rtl_write', 0, 63, 'retf', 0, True), ('__write', 63, 28, 'retf', 0, True)]),
 'xfflush':dict(base=0x5212,size=63,fields=2,group='08ff02ff03',externals=['__streams', '_fflush'],procedures=[('__xfflush', 0, 63, 'retf', 0, True)]),
 'setupio':dict(base=0x359d,size=164,fields=18,group='0aff03ff02',externals=['__streams', '__nfile', '_setvbuf', '_isatty', '__openfd'],procedures=[('__setupio', 0, 164, 'ret', 0, True)]),
 'lseek':dict(base=0x3246,size=45,fields=2,group='08ff03ff02',externals=['__IOERROR', '__openfd'],procedures=[('_lseek', 0, 45, 'retf', 0, True)]),
 'isatty':dict(base=0x3231,size=21,fields=0,group='08ff03ff02',externals=[],procedures=[('_isatty', 0, 21, 'retf', 0, True)]),
}
SOURCE_MAP={PREFIX+n:(p,'vendor/'+n+'.obj') for n,p in SOURCES.items()}
SOURCE_MAP.update({PREFIX+'setvbuf-data':(SOURCES['setvbuf'],'vendor/setvbuf.obj'),PREFIX+'setupio-init':(SOURCES['setupio'],'vendor/setupio.obj')})

def need(value,message):
    if not value:raise ValueError('MAINL buffered I/O native: '+str(message))

def selected(root,work,files):
    raw=(root/REPORT).read_bytes();r=json.loads(raw);reused,meta=reused_pairs(root,work,files)
    need(r['complete'] and not r['source_acceptance'] and not r['whole_product_cold_rebuilt'] and r['retained_project_objects']==36 and
         r['source_sha256']=={p:sha((root/p).read_bytes()) for p in SOURCES.values()} and r['driver_sha256']==sha((root/DRIVER).read_bytes()) and
         r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()) and r['reused_sources']==meta,'stdio source/recipe/cold and reused actual CRT pairs')
    header=(root/LAYOUT_HEADER).read_bytes()
    need(r['layout_header_sha256']==sha(header) and (root/'.analysis/work/stdio-layout.inc').read_bytes()==header,'actual shared FILE-layout include input')
    current=(work/'crt.lib').read_bytes();members=library_members(current)
    need(r['current_library_sha256']==sha(current) and len(members)==893,'normal library identity')
    need(all((root/('.analysis/work/stdio-source-'+n+'.asm')).read_bytes()==(root/p).read_bytes() for n,p in SOURCES.items()) and
         (root/'.analysis/work/stdio-library.rsp').read_bytes()==library_response(members) and
         (root/'.analysis/work/stdio-link.lnk').read_bytes()==link_response(files),'actual full source and response inputs')
    config=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/config['paths']['wine_prefix']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t']
    dos=['/usr/bin/wine-stable',str(root/config['paths']['msdos_player']),'-e','-x'];phases=[]
    for n in (1,2):
        phases += [(f'round{n}-{name}',tasm+[name+'.asm',name+'.obj'],0) for name in SOURCES]
        phases += [(f'round{n}-library',dos+['tlib',r'@probe\stdiolib.rsp'],0),(f'round{n}-link',dos+['tlink',r'@probe\stdioctx.lnk'],0)]
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'actual serial assembly/library/link rounds')
    vectors=[]
    for row in r['rounds']:
        need(set(row['outputs'])==set(SOURCES)|{'lib','exe','map'},'complete selected output vector');v={}
        for name,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'complete current raw native output');v[name]=b
        review=compare_members(members,library_members(v['lib']),dict(reused,**{n:v[n] for n in SOURCES}))
        need(row['library']==review and review['contextual_members_unchanged']==874,'all893 member positions and874 unchanged current members')
        need(v['exe']==(work/'bin/th03/mainl.target.exe').read_bytes() and v['map']==(work/'obj/th03/mainl.map').read_bytes(),'whole pinned Japanese decoded EXE and retained MAP equality')
        vectors.append(v)
    need(vectors[0]==vectors[1],'whole raw ten-OBJ/LIB/EXE/MAP repetition')
    return vectors[0],r,sha(raw)


def verify(root,work,target,candidate,graph,files):
    v,r,report_sha=selected(root,work,files);table=v['map'].decode();linked=parse_mz(v['exe']);need(linked.valid,'complete linked native MZ')
    owners=[];modules={};frame_changes=[]
    for name,layout in LAYOUT.items():
        base,size=layout['base'],layout['size'];raw=v[name];original=(work/('vendor/'+name+'.obj')).read_bytes();d=describe_omf(raw)
        need(d['valid'] and d['module_name']==name+'.asm' and d['translator_comments']==['Turbo Assembler  Version 5.0'] and d['dependency_paths']==[name+'.asm','stdio_layout.inc'],'actual complete source TU and shared layout include consumption')
        defs=[(1,'_TEXT','CODE',size),(2,'_DATA','DATA',4 if name=='setvbuf' else 0),(3,'_BSS','BSS',0)]
        if name=='setupio':defs.append((4,'_INIT_','INITDATA',6))
        need(segment_definitions(raw)==[dict(index=i,name=n,**{'class':c},overlay='',size=s) for i,n,c,s in defs] and
             [q.data[0] for q in parse_omf(raw) if q.name=='SEGDEF']==[0x28]+[0x48]*(len(defs)-1) and
             [q.data.hex() for q in parse_omf(raw) if q.name=='GRPDEF']==[layout['group']],'complete original segment sizes/alignments/group order')
        pubs=[(off,symbol) for symbol,off,_,_,_,public in layout['procedures'] if public]
        need(code_publics(raw,1)==code_publics(original,1)==pubs and externs(raw)==externs(original)==layout['externals'],'complete public/external identities')
        need(all(not code_publics(raw,i) and not code_publics(original,i) for i in range(2,len(defs)+1)),'complete private DATA/INIT public inventory')
        fields,old_fields=literal_fields(raw),literal_fields(original)
        need(payload(raw)==payload(original) and len(fields)==len(old_fields)==layout['fields'],'entire initialized native payload and complete field count')
        old_by_site={(f['segment'],f['site']):f for f in old_fields}
        need(len(old_by_site)==len(fields) and len({(f['segment'],f['site']) for f in fields})==len(fields),'all fields have distinct actual locations')
        for f in fields:
            old=old_by_site[(f['segment'],f['site'])]
            if name=='write' and f['site']==23:
                need((old['frame_method'],old['frame'],f['frame_method'],f['frame'],f['segment_relative'],f['target_method'],f['target'])==(5,None,0,1,False,2,4),'sole equivalent same-CODE near IOERROR call frame')
                old=dict(old,frame_method=0,frame=1);frame_changes.append(dict(module=name,site=23))
            need(f==old,'complete field identity/geometry without sorting either literal emitted stream')
        need(table.count(f'0000:{base:04X} {size:04X} C=CODE   S=_TEXT          G=(none)  M={name:<10} ACBP=28')==1,'complete actual normal-library CODE MAP allocation')
        for off,symbol in pubs:need(address(table,symbol)==(0,base+off),'both actual public MAP tables')
        coordinates={1:(0,base,size)}
        if name=='setvbuf':coordinates[2]=(DS,BUFFER_DATA,4)
        if name=='setupio':coordinates[4]=(DS,SETUP_INIT,6)
        for segment,(seg,off,count) in coordinates.items():
            if segment==1:continue
            cls,section=('DATA','_DATA') if segment==2 else ('INITDATA','_INIT_')
            need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{count:04X}\s+C={cls}\s+S={section}\s+G=DGROUP\s+M={name}\s+ACBP=48\s*$',table))==1,'whole actual private DATA/INIT allocation')
        buffers={};relocations={segment:[] for segment in coordinates}
        for segment,(_,_,count) in coordinates.items():
            data=byte_map(raw,segment);need(set(data)==set(range(count)),'complete dense initialized bytes without holes');buffers[segment]=bytearray(data[i] for i in range(count))
        need(not byte_map(raw,3),'no BSS file initializer');observed=[];far_calls=[];near_calls=[]
        for f in fields:
            segment,site=f['segment'],f['site'];need(segment in coordinates,'field belongs to real initialized source storage');image=buffers[segment];product_segment,product_base,_=coordinates[segment]
            need(site+f['width']<=len(image),'complete actual field within source extent')
            if f['target_method']==2:
                symbol=layout['externals'][f['target']-1];seg,off=address(table,symbol);off+=f['addend']
            else:
                need(f['target_method']==0 and ((name=='setvbuf' and f['target']==2) or (name=='setupio' and f['target']==1)),'only actual private flags or startup callback')
                seg,off,_=coordinates[f['target']];off+=f['addend'];symbol='stdio configured flags' if f['target']==2 else '__setupio'
            if f['location_type']==3:
                need(segment==1 and f['width']==4 and f['segment_relative'] and (f['frame_method'],f['frame'],seg,f['addend'])==(5,None,0,0) and image[site-1:site+4]==b'\x9a\0\0\0\0','ordinary external far CALL')
                image[site-1:site+4]=b'\x90\x0e\xe8'+((off-(base+site+4))&65535).to_bytes(2,'little');far_calls.append(dict(site=base+site-1,symbol=symbol,target=off))
            else:
                need(f['width']==2 and f['location_type'] in (1,2),'actual offset/segment WORD')
                if not f['segment_relative']:
                    need((segment,f['location_type'],f['frame_method'],f['frame'],seg,symbol,f['addend'])==(1,1,0,1,0,'__IOERROR',0) and name in ('write','writea','lseek'),'real near callee-pop2 IOERROR call')
                    need(image[site-1]==0xE8,'real near CALL opcode');value=(off-(base+site+2))&65535;near_calls.append(dict(site=base+site-1,symbol=symbol,target=off,callee_pop_bytes=2))
                elif f['location_type']==2:
                    need((name,segment,site,f['frame_method'],f['frame'],seg,symbol)==('setvbuf',1,190,5,None,0,'__xfflush'),'sole real far exit-buffer callback segment assignment')
                    value=seg;relocations[segment].append([product_segment,product_base+site])
                elif seg==0:
                    need((f['frame_method'],f['frame'])==(5,None) and ((name=='setvbuf' and segment==1 and site==196 and symbol=='__xfflush') or (name=='setupio' and segment==4 and site==2 and symbol=='__setupio')),'real exit/startup callback offset WORD')
                    value=off
                else:
                    need((f['frame_method'],f['frame'],seg)==(1,1,DS),'actual DGROUP offset field');value=off
                image[site:site+2]=value.to_bytes(2,'little')
            observed.append(dict(f,symbol=symbol,product_site=product_base+site,resolved_target=[seg,off]))
        images={segment:bytes(data) for segment,data in buffers.items()}
        if name=='setvbuf':need(images[2]==bytes(4) and relocations[1]==[[0,base+190]],'two real initialized standard-stream flags and exact callback segment relocation')
        if name=='setupio':need(images[4]==bytes((0,2))+base.to_bytes(2,'little')+bytes(2) and not relocations[4],'real type0 priority2 near startup record without invented segment relocation')
        for segment,image in images.items():
            seg,off,_=coordinates[segment];start=seg*16+off;need(image==linked.program_image[start:start+len(image)],'complete independently resolved native linked bytes');extent((target,candidate),image,seg,off,relocations[segment])
        decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;ins=list(decoder.disasm(images[1],base));bounds={i.address for i in ins};need(sum(i.size for i in ins)==size,'complete dense native CODE')
        for i in ins:
            if i.mnemonic.startswith(('j','loop')):need(i.operands[0].type==X86_OP_IMM and i.operands[0].imm in bounds,'every local branch enters a complete instruction')
        procedures=[]
        for symbol,offset,count,ret,pop,public in layout['procedures']:
            body=[i for i in ins if base+offset<=i.address<base+offset+count];need(sum(i.size for i in body)==count and body[-1].mnemonic==ret and body[-1].op_str==(str(pop) if pop else ''),'complete body and real near/far cleanup ABI')
            procedures.append(dict(name=symbol,offset=offset,size=count,return_kind=ret,public=public,callee_pop_bytes=pop))
        for segment,image in images.items():
            seg,off,_=coordinates[segment];procs=procedures if segment==1 else [];suffix='' if segment==1 else '-data' if segment==2 else '-init';unit=PREFIX+name+suffix
            owners.append(dict(unit_id=unit,name=unit.removeprefix(PREFIX),source=SOURCES[name],object='vendor/'+name+'.obj',origin='library',segment=seg,offset=off,start=seg*16+off,size=len(image),coordinate_space='decoded-load',canonical_file_offset=None,
                target_sha256=sha(image),candidate_sha256=sha(image),ordered_relocations=relocations[segment],code_bytes=len(image) if segment==1 else 0,initialized_data_bytes=len(image) if segment!=1 else 0,
                procedure_count=len(procs),procedures=procs,private_data_bytes=0,private_bss_bytes=0,maintained_native_object=r['rounds'][0]['outputs'][name]['path'],abi='far cdecl stream/DOS APIs; near pop4 buffered count,near startup,and near callee-pop2 IOERROR imports'))
        modules[name]=dict(native_fields=observed,original_literal_native_fields=old_fields,far_calls=far_calls,near_calls=near_calls,native_field_order_preserved=True,ordered_scope_relocations=relocations[1])
    need(frame_changes==[dict(module='write',site=23)],'only the reviewed equivalent near IOERROR frame')
    return dict(owners=owners,modules=modules,source_sha256=r['source_sha256'],layout_header_sha256=r['layout_header_sha256'],source_CODE_bytes=1808,source_initialized_DATA_bytes=10,procedures=13,
        equivalent_near_IOERROR_frame_sites=frame_changes,selected_build_report_sha256=report_sha,selected_assembly_library_link_rounds=2,normal_library_members=893,untouched_current_library_members=874,
        source_CRT_providers_in_selected_library=25,reused_nine_natural_CRT_pairs=True,retained_project_objects=36,full_raw_vector_repeated=True,whole_EXE_MAP_equal=True,source_padding_added=False,BSS_file_byte_credit=0,
        original_cold_rebuilt=False,ancestor_runtime_replayed=False,physical_DOS_execution_claimed=False,whole_product_accepted=False)


if __name__=='__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['stdio_native'],indent=2))
