"""Complete program resolution/preparation and the combined natural CRT library."""
import hashlib
import json
import re
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from build_th03_mainl_loadprog_work import SOURCE,DRIVER,REPORT,library_response,link_response
from build_th03_mainl_display_work import literal_fields,payload
from lib.decoded_mainl_farheap_native import selected as farheap_pair
from lib.decoded_mainl_exec_native import selected as exec_pair
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
UNIT=PREFIX+'loadprog'
DATA_UNIT=PREFIX+'loadprog-data'
UNITS=(UNIT,DATA_UNIT)
OBJECT='vendor/loadprog.obj'
BASE,DS,DATA_BASE=0x928C,0xE3F,0x12F0
EXTERNALS=['__exitbuf','__DOSCMD','__DOSENV','_free','_getenv','__environ','__searchenv','_errno','__access','_strcat','_strcpy','_strlen','_stricmp','_strrchr','___path_isdbcsleadbyte']


def need(v,message):
    if not v:raise ValueError('MAINL load program native: '+str(message))


def sha(b):return hashlib.sha256(b).hexdigest()


def selected(root,work,files):
    raw=(root/REPORT).read_bytes();r=json.loads(raw);src=(root/SOURCE).read_bytes()
    heap,hp,hsha=farheap_pair(root,work,files);execution,ep,esha=exec_pair(root,work,files)
    need(r['complete'] and not r['source_acceptance'] and not r['whole_product_cold_rebuilt'] and r['retained_project_objects']==36 and
         r['source_sha256']==sha(src) and r['driver_sha256']==sha((root/DRIVER).read_bytes()) and
         r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()),'complete maintained source/recipe/cold context')
    for key,prior,prior_sha,v in [('reused_farheap',hp,hsha,heap),('reused_exec',ep,esha,execution)]:
        need(r[key]==dict(source_sha256=prior['source_sha256'],build_report_sha256=prior_sha,object_sha256=sha(v['obj'])),'actual reused natural CRT input')
    errno=(root/'src/mainl/crt/crt_errno.inc').read_bytes()
    need(errno==files['owned/crt_errno.inc']==(root/'.analysis/work/loadprog-errno.inc').read_bytes() and
         r['errno_header_sha256']==sha(errno),'actual preserved named errno header')
    current=(work/'crt.lib').read_bytes();members=library_members(current)
    need(r['current_library_sha256']==sha(current) and len(members)==893,'normal library identity')
    need((root/'.analysis/work/loadprog-source.asm').read_bytes()==src and
         (root/'.analysis/work/loadprog-library.rsp').read_bytes()==library_response(members) and
         (root/'.analysis/work/loadprog-link.lnk').read_bytes()==link_response(files),'actual full source and response inputs')
    config=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/config['paths']['wine_prefix']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t','loadprog.asm','loadprog.obj']
    dos=['/usr/bin/wine-stable',str(root/config['paths']['msdos_player']),'-e','-x'];phases=[]
    for n in (1,2):phases += [(f'round{n}-assemble',tasm,0),(f'round{n}-library',dos+['tlib',r'@probe\ldplib.rsp'],0),(f'round{n}-link',dos+['tlink',r'@probe\ldprog.lnk'],0)]
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'actual serial assembly/library/link rounds')
    vectors=[]
    for row in r['rounds']:
        need(set(row['outputs'])=={'obj','lib','exe','map'},'complete selected output vector');v={}
        for name,meta in row['outputs'].items():
            b=(root/meta['path']).read_bytes();need(meta==dict(path=meta['path'],bytes=len(b),sha256=sha(b)),'complete current raw native output');v[name]=b
        review=compare_members(members,library_members(v['lib']),{'loadprog':v['obj'],'farheap':heap['obj'],'exec':execution['obj']})
        need(row['library']==review and review['contextual_members_unchanged']==890,'all893 member positions and890 other current members')
        need(v['exe']==(work/'bin/th03/mainl.target.exe').read_bytes() and v['map']==(work/'obj/th03/mainl.map').read_bytes(),'whole pinned Japanese decoded EXE and retained MAP equality')
        vectors.append(v)
    need(vectors[0]==vectors[1],'whole raw OBJ/LIB/EXE/MAP repetition')
    return vectors[0],r,sha(raw)


def verify(root,work,target,candidate,graph,files):
    v,r,report_sha=selected(root,work,files);raw=v['obj'];original=(work/OBJECT).read_bytes();d=describe_omf(raw)
    need(d['valid'] and d['module_name']=='loadprog.asm' and d['translator_comments']==['Turbo Assembler  Version 5.0'] and
         d['dependency_paths']==['loadprog.asm','crt_errno.inc'],'complete actual maintained source/include consumption')
    need(segment_definitions(raw)==[dict(index=i,name=n,**{'class':c},overlay='',size=s) for i,n,c,s in
         [(1,'_TEXT','CODE',871),(2,'_DATA','DATA',40),(3,'_BSS','BSS',0)]] and
         [q.data[0] for q in parse_omf(raw) if q.name=='SEGDEF']==[0x28,0x48,0x48] and
         [q.data.hex() for q in parse_omf(raw) if q.name=='GRPDEF']==['08ff02ff03'],'literal native BYTE CODE/WORD DATA/BSS and original DATA/BSS group order')
    need(code_publics(raw,1)==code_publics(original,1)==[(269,'__LoadProg')] and not code_publics(raw,2) and
         externs(raw)==externs(original)==EXTERNALS,'complete public/external identities')
    fields,old_fields=literal_fields(raw),literal_fields(original)
    need(payload(raw)==payload(original) and len(fields)==len(old_fields)==32,'complete initialized CODE/DATA payload and native field count')
    # Compare geometry by site without changing either emitted stream. The old
    # compiler emits reverse-order fields; TASM's actual stream remains intact.
    by_site={f['site']:f for f in old_fields};need(len(by_site)==32 and len({f['site'] for f in fields})==32,'distinct complete native fields')
    frame_changes=[]
    for f in fields:
        old=by_site[f['site']]
        if f['site'] in (633,754):
            need((old['frame_method'],old['frame'],f['frame_method'],f['frame'])==(5,None,0,1) and
                 f['target_method']==2 and f['target'] in (2,3) and not f['segment_relative'],'equivalent same-CODE frame on the two real near constructors')
            old=dict(old,frame_method=0,frame=1);frame_changes.append(f['site'])
        need(f==old,'complete native field identity/geometry; no masked addend or target')
    need(frame_changes==[633,754],'only the two explicit constructor-frame changes')
    table=v['map'].decode()
    for line in ('0000:928C 0367 C=CODE   S=_TEXT          G=(none)  M=loadprog   ACBP=28',
                 '0E3F:12F0 0028 C=DATA   S=_DATA          G=DGROUP  M=loadprog   ACBP=48'):
        need(table.count(line)==1,'complete actual library MAP contributions')
    need(address(table,'__LoadProg')==(0,BASE+269),'near API in both MAP public tables')
    data=byte_map(raw,1);need(set(data)==set(range(871)) and not byte_map(raw,3),'dense CODE and no BSS file initializer')
    image=bytearray(data[i] for i in range(871));observed=[];far_calls=[]
    for f in fields:
        site=f['site'];need(f['segment']==1 and site+f['width']<=871,'whole actual CODE field')
        if f['target_method']==0:
            need((f['target'],f['frame_method'],f['frame'])==(2,1,1),'actual private DGROUP string field');symbol='private DATA';seg,off=DS,DATA_BASE+f['addend']
        else:
            need(f['target_method']==2,'actual external reference');symbol=EXTERNALS[f['target']-1];seg,off=address(table,symbol);off+=f['addend']
        if f['location_type']==3:
            need(f['width']==4 and f['frame_method']==5 and f['segment_relative'] and seg==0 and f['addend']==0 and
                 image[site-1:site+4]==b'\x9a\0\0\0\0','ordinary actual external far CALL')
            image[site-1:site+4]=b'\x90\x0e\xe8'+((off-(BASE+site+4))&65535).to_bytes(2,'little');far_calls.append(dict(site=BASE+site-1,symbol=symbol,target=off))
        else:
            need(f['location_type']==1 and f['width']==2,'native offset WORD')
            if f['segment_relative']:
                need((f['frame_method'],f['frame'],seg)==(1,1,DS),'actual DGROUP offset');value=off
            else:
                need((f['frame_method'],f['frame'],seg)==(0,1,0) and symbol in ('__DOSCMD','__DOSENV'),'real same-CODE near constructor');value=(off-(BASE+site+2))&65535
            image[site:site+2]=value.to_bytes(2,'little')
        observed.append(dict(f,symbol=symbol,product_site=BASE+site,resolved_target=[seg,off]))
    image=bytes(image);linked=parse_mz(v['exe']);need(linked.valid and image==linked.program_image[BASE:BASE+871] and len(far_calls)==14,'whole independently resolved native code and all14 far-call relaxations')
    extent((target,candidate),image,0,BASE,[])
    semantic=b'PATH\0'+b'/\\\0'+b'\0'+b'.BAT\0.COM\0.EXE\0.BAT\0COMSPEC\0/c\0'
    native_data=byte_map(raw,2);need(set(native_data)==set(range(40)) and bytes(native_data[i] for i in range(40))==semantic,'all40 semantic path/suffix/shell DATA bytes')
    extent((target,candidate),semantic,DS,DATA_BASE,[])
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;ins=list(decoder.disasm(image,BASE));bounds={i.address for i in ins}
    need(sum(i.size for i in ins)==871,'complete dense instructions')
    for i in ins:
        if i.mnemonic.startswith(('j','loop')):need(i.operands[0].type==X86_OP_IMM and i.operands[0].imm in bounds,'all local branches enter complete instructions')
    procedures=[]
    for name,start,size,ret in [('find_path_separator',0,132,'retf'),('probe_program',132,137,'retf'),('__LoadProg',269,602,'ret')]:
        body=[i for i in ins if BASE+start<=i.address<BASE+start+size];need(sum(i.size for i in body)==size and body[-1].mnemonic==ret and not body[-1].op_str,'complete near/far caller-pop body')
        procedures.append(dict(name=name,offset=start,size=size,return_kind=ret,public=name=='__LoadProg',callee_pop_bytes=0))
    callback,=[i for i in ins if i.address==BASE+0x33C];flush,=[i for i in ins if i.address==BASE+0x316]
    need(callback.mnemonic=='call' and callback.size==3 and flush.mnemonic=='lcall' and flush.size==4,'actual near execution callback and far buffer-cleanup callback')
    def owner(unit,segment,offset,body,procs):
        return dict(unit_id=unit,name=unit.removeprefix(PREFIX),source=SOURCE,object=OBJECT,origin='library',segment=segment,offset=offset,start=segment*16+offset,
            size=len(body),coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=sha(body),candidate_sha256=sha(body),ordered_relocations=[],
            code_bytes=len(body) if segment==0 else 0,initialized_data_bytes=len(body) if segment==DS else 0,procedure_count=len(procs),procedures=procs,
            private_data_bytes=0,private_bss_bytes=0,maintained_native_object=r['rounds'][0]['outputs']['obj']['path'],abi='near cdecl loader with two private far cdecl helpers and12-byte near executor callback')
    return dict(owners=[owner(UNIT,0,BASE,image,procedures),owner(DATA_UNIT,DS,DATA_BASE,semantic,[])],source_sha256=sha((root/SOURCE).read_bytes()),
        source_CODE_bytes=871,source_initialized_DATA_bytes=40,procedures=3,native_fields=observed,original_literal_native_fields=old_fields,
        equivalent_near_constructor_frame_sites=frame_changes,far_calls=far_calls,ordered_scope_relocations=[],native_field_order_preserved=True,
        selected_build_report_sha256=report_sha,selected_assembly_library_link_rounds=2,normal_library_members=893,untouched_current_library_members=890,
        source_CRT_providers_in_selected_library=9,reused_natural_farheap_and_exec=True,retained_project_objects=36,full_raw_vector_repeated=True,whole_EXE_MAP_equal=True,
        source_padding_added=False,BSS_file_byte_credit=0,original_cold_rebuilt=False,ancestor_runtime_replayed=False,physical_DOS_execution_claimed=False,whole_product_accepted=False)


if __name__=='__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['loadprog_native'],indent=2))
