"""Complete native DOS command/environment constructors, with their callee-pop ABI."""
import json
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from build_th03_mainl_dosconstruct_work import SOURCES,DRIVER,REPORT,reused_pairs,library_response,link_response
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
SOURCE_MAP={PREFIX+n:(p,'vendor/'+n+'.obj') for n,p in SOURCES.items()}
LAYOUT={'doscmd':(0x895B,311,'__DOSCMD',[227,165,99,66,28]),'dosenv':(0x2DFB,365,'__DOSENV',[319,220,130,100,51])}
EXTERNALS=['_malloc','_strlen','__stpcpy']


def need(value,message):
    if not value:raise ValueError('MAINL DOS constructors native: '+str(message))


def selected(root,work,files):
    raw=(root/REPORT).read_bytes();r=json.loads(raw);reused,meta=reused_pairs(root,work,files)
    need(r['complete'] and not r['source_acceptance'] and not r['whole_product_cold_rebuilt'] and r['retained_project_objects']==36 and
         r['source_sha256']=={p:sha((root/p).read_bytes()) for p in SOURCES.values()} and r['driver_sha256']==sha((root/DRIVER).read_bytes()) and
         r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()) and r['reused_sources']==meta,'constructor source/recipe/cold and reused actual CRT pairs')
    current=(work/'crt.lib').read_bytes();members=library_members(current)
    need(r['current_library_sha256']==sha(current) and len(members)==893,'normal library identity')
    need(all((root/('.analysis/work/dosconstruct-source-'+n+'.asm')).read_bytes()==(root/p).read_bytes() for n,p in SOURCES.items()) and
         (root/'.analysis/work/dosconstruct-library.rsp').read_bytes()==library_response(members) and
         (root/'.analysis/work/dosconstruct-link.lnk').read_bytes()==link_response(files),'actual full source and response inputs')
    config=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/config['paths']['wine_prefix']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t']
    dos=['/usr/bin/wine-stable',str(root/config['paths']['msdos_player']),'-e','-x'];phases=[]
    for n in (1,2):
        phases += [(f'round{n}-{name}',tasm+[name+'.asm',name+'.obj'],0) for name in SOURCES]
        phases += [(f'round{n}-library',dos+['tlib',r'@probe\ctorlib.rsp'],0),(f'round{n}-link',dos+['tlink',r'@probe\dosctor.lnk'],0)]
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'actual serial assembly/library/link rounds')
    vectors=[]
    for row in r['rounds']:
        need(set(row['outputs'])==set(SOURCES)|{'lib','exe','map'},'complete selected output vector');v={}
        for name,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'complete current raw native output');v[name]=b
        review=compare_members(members,library_members(v['lib']),dict(reused,**{n:v[n] for n in SOURCES}))
        need(row['library']==review and review['contextual_members_unchanged']==888,'all893 member positions and888 unchanged current members')
        need(v['exe']==(work/'bin/th03/mainl.target.exe').read_bytes() and v['map']==(work/'obj/th03/mainl.map').read_bytes(),'whole pinned Japanese decoded EXE and retained MAP equality')
        vectors.append(v)
    need(vectors[0]==vectors[1],'whole raw two-OBJ/LIB/EXE/MAP repetition')
    return vectors[0],r,sha(raw)


def verify(root,work,target,candidate,graph,files):
    v,r,report_sha=selected(root,work,files);table=v['map'].decode();linked=parse_mz(v['exe']);need(linked.valid,'native linked MZ')
    owners=[];modules={}
    for name,(base,size,public,old_sites) in LAYOUT.items():
        raw=v[name];original=(work/('vendor/'+name+'.obj')).read_bytes();d=describe_omf(raw)
        need(d['valid'] and d['module_name']==name+'.asm' and d['translator_comments']==['Turbo Assembler  Version 5.0'] and
             d['dependency_paths']==[name+'.asm'],'actual complete maintained constructor TU')
        need(segment_definitions(raw)==[dict(index=i,name=n,**{'class':c},overlay='',size=s) for i,n,c,s in
             [(1,'_TEXT','CODE',size),(2,'_DATA','DATA',0),(3,'_BSS','BSS',0)]] and
             [q.data[0] for q in parse_omf(raw) if q.name=='SEGDEF']==[0x28,0x48,0x48] and
             [q.data.hex() for q in parse_omf(raw) if q.name=='GRPDEF']==['08ff02ff03'],'literal BYTE CODE/WORD empty DATA/BSS and original group order')
        need(code_publics(raw,1)==code_publics(original,1)==[(0,public)] and externs(raw)==externs(original)==EXTERNALS,'complete public/external identities')
        fields,old_fields=literal_fields(raw),literal_fields(original)
        need(payload(raw)==payload(original) and len(fields)==len(old_fields)==5 and [f['site'] for f in old_fields]==old_sites,'complete initialized payload and original literal field order')
        old_by_site={f['site']:f for f in old_fields}
        need(len(old_by_site)==5 and len({f['site'] for f in fields})==5 and all(f==old_by_site[f['site']] for f in fields),'all actual field identities/geometry without reordering either emitted stream')
        line=f'0000:{base:04X} {size:04X} C=CODE   S=_TEXT          G=(none)  M={name:<10} ACBP=28'
        need(table.count(line)==1 and address(table,public)==(0,base),'complete native MAP contribution and both public tables')
        data=byte_map(raw,1);need(set(data)==set(range(size)) and not byte_map(raw,2) and not byte_map(raw,3),'dense complete CODE and no DATA/BSS initializers')
        image=bytearray(data[i] for i in range(size));observed=[];far_calls=[]
        for f in fields:
            site=f['site'];need((f['segment'],f['width'],f['location_type'],f['segment_relative'],f['frame_method'],f['frame'],f['target_method'],f['addend'])==(1,4,3,True,5,None,2,0) and
                 site+4<=size and image[site-1:site+4]==b'\x9a\0\0\0\0','actual ordinary complete far CALL field')
            symbol=EXTERNALS[f['target']-1];seg,off=address(table,symbol);need(seg==0,'same-CODE external callee')
            image[site-1:site+4]=b'\x90\x0e\xe8'+((off-(base+site+4))&65535).to_bytes(2,'little')
            observed.append(dict(f,symbol=symbol,product_site=base+site,resolved_target=[seg,off]));far_calls.append(dict(site=base+site-1,symbol=symbol,target=off))
        image=bytes(image);need(image==linked.program_image[base:base+size],'complete independently resolved linked native code')
        extent((target,candidate),image,0,base,[])
        decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;ins=list(decoder.disasm(image,base));bounds={i.address for i in ins}
        need(sum(i.size for i in ins)==size and ins[-1].mnemonic=='ret' and ins[-1].op_str=='0xc','complete near callee-pop12 constructor')
        for i in ins:
            if i.mnemonic.startswith(('j','loop')):need(i.operands[0].type==X86_OP_IMM and i.operands[0].imm in bounds,'local branch enters a complete instruction')
        procedures=[dict(name=public,offset=0,size=size,return_kind='ret',public=True,callee_pop_bytes=12)]
        owners.append(dict(unit_id=PREFIX+name,name=name,source=SOURCES[name],object='vendor/'+name+'.obj',origin='library',segment=0,offset=base,start=base,
            size=size,coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=sha(image),candidate_sha256=sha(image),ordered_relocations=[],
            code_bytes=size,initialized_data_bytes=0,procedure_count=1,procedures=procedures,private_data_bytes=0,private_bss_bytes=0,
            maintained_native_object=r['rounds'][0]['outputs'][name]['path'],abi='near callee-pop12 with three far pointer arguments'))
        modules[name]=dict(native_fields=observed,original_literal_native_fields=old_fields,far_calls=far_calls,native_field_order_preserved=True,ordered_scope_relocations=[])
    return dict(owners=owners,modules=modules,source_sha256=r['source_sha256'],source_CODE_bytes=676,source_initialized_DATA_bytes=0,procedures=2,
        selected_build_report_sha256=report_sha,selected_assembly_library_link_rounds=2,normal_library_members=893,untouched_current_library_members=888,
        source_CRT_providers_in_selected_library=11,reused_natural_farheap_exec_loadprog=True,retained_project_objects=36,full_raw_vector_repeated=True,whole_EXE_MAP_equal=True,
        source_padding_added=False,BSS_file_byte_credit=0,original_cold_rebuilt=False,ancestor_runtime_replayed=False,physical_DOS_execution_claimed=False,whole_product_accepted=False)


if __name__=='__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['dosconstruct_native'],indent=2))
