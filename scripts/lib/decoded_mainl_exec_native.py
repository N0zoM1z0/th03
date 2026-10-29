"""Natural DOS overlay execution source, copied continuation and combined CRT link."""
import hashlib
import json
import re
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from build_th03_mainl_exec_work import SOURCE,DRIVER,REPORT,library_response,link_response
from build_th03_mainl_display_work import literal_fields,payload
from lib.decoded_mainl_farheap_native import selected as farheap_pair
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_file_native import byte_map
from lib.borland_library import library_members,compare_members
from lib.omf import parse_omf,describe_omf
from lib.pc98 import parse_mz
from lib.op_asset_native import extent
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

UNIT='th03-mainl-decoded-crt-exec'
OBJECT='vendor/exec.obj'
BASE=0x8A92
EXTERNALS=['__cexit','__IOERROR','__envseg','DGROUP@','__psp','__version']
DS_FRAME_SITES=(371,397,482,560)


def need(v,message):
    if not v:raise ValueError('MAINL overlay exec native: '+str(message))


def sha(b):return hashlib.sha256(b).hexdigest()


def selected(root,work,files):
    raw=(root/REPORT).read_bytes();r=json.loads(raw);src=(root/SOURCE).read_bytes()
    reused,prior,prior_sha=farheap_pair(root,work,files)
    need(r['complete'] and not r['source_acceptance'] and not r['whole_product_cold_rebuilt'] and r['retained_project_objects']==36 and
         r['source_sha256']==sha(src) and r['driver_sha256']==sha((root/DRIVER).read_bytes()) and
         r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()),'actual source/native recipe/unchanged cold binding')
    need(r['reused_farheap']==dict(source_sha256=prior['source_sha256'],build_report_sha256=prior_sha,object_sha256=sha(reused['obj'])),'actual unchanged natural far-heap producer reused')
    current=(work/'crt.lib').read_bytes();members=library_members(current)
    need(r['current_library_sha256']==sha(current) and len(members)==893,'complete retained normal library identity')
    need((root/'.analysis/work/exec-source.asm').read_bytes()==src and
         (root/'.analysis/work/exec-library.rsp').read_bytes()==library_response(members) and
         (root/'.analysis/work/exec-link.lnk').read_bytes()==link_response(files),'actual preserved source and combined native response inputs')
    config=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/config['paths']['wine_prefix']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t','exec.asm','exec.obj']
    dos=['/usr/bin/wine-stable',str(root/config['paths']['msdos_player']),'-e','-x'];phases=[]
    for n in (1,2):phases += [(f'round{n}-assemble',tasm,0),(f'round{n}-library',dos+['tlib',r'@probe\cexlib.rsp'],0),(f'round{n}-link',dos+['tlink',r'@probe\cexec.lnk'],0)]
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'actual serial two-round schedule')
    vectors=[]
    for row in r['rounds']:
        need(set(row['outputs'])=={'obj','lib','exe','map'},'complete selected output vector');v={}
        for name,meta in row['outputs'].items():
            b=(root/meta['path']).read_bytes();need(meta==dict(path=meta['path'],bytes=len(b),sha256=sha(b)),'whole current raw native output');v[name]=b
        review=compare_members(members,library_members(v['lib']),{'exec':v['obj'],'farheap':reused['obj']})
        need(row['library']==review and review['contextual_members_unchanged']==891,'complete ordered library and both natural source replacements')
        need(v['exe']==(work/'bin/th03/mainl.target.exe').read_bytes() and v['map']==(work/'obj/th03/mainl.map').read_bytes(),'whole pinned Japanese decoded EXE/retained MAP equality')
        vectors.append(v)
    need(vectors[0]==vectors[1],'whole raw OBJ/LIB/EXE/MAP repetition')
    return vectors[0],r,sha(raw)


def verify(root,work,target,candidate,graph,files):
    vector,report,report_sha=selected(root,work,files);raw=vector['obj'];original=(work/OBJECT).read_bytes();d=describe_omf(raw)
    need(d['valid'] and d['module_name']=='exec.asm' and d['translator_comments']==['Turbo Assembler  Version 5.0'] and
         d['dependency_paths']==['exec.asm'],'complete maintained native source consumption')
    need(segment_definitions(raw)==[dict(index=1,name='_TEXT',**{'class':'CODE'},overlay='',size=933),dict(index=2,name='_DATA',**{'class':'DATA'},overlay='',size=0)] and
         [r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF']==[0x28,0x48] and [r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF']==['06ff02'],'native BYTE CODE/WORD empty DATA/DGROUP geometry')
    need(code_publics(raw,1)==code_publics(original,1)==[(359,'__exec')] and not code_publics(raw,2) and
         externs(raw)==externs(original)==EXTERNALS,'complete public/external identities and near public ABI')
    fields=literal_fields(raw);expected=literal_fields(original);frame_changes=[]
    for f in expected:
        if f['site'] in DS_FRAME_SITES:
            need((f['location_type'],f['frame_method'],f['frame'],f['target_method'],f['target']) in
                 ((1,5,None,2,3),(1,5,None,2,5),(1,5,None,2,6)),'original target-framed DOS globals')
            frame_changes.append(dict(site=f['site'],original_frame=[5,None],maintained_frame=[1,1]));f['frame_method']=1;f['frame']=1
    need(fields==expected and len(fields)==21 and [f['site'] for f in frame_changes]==list(DS_FRAME_SITES) and
         payload(raw)==payload(original),'complete initialized payload and literal ordered native fields,with four explicit equivalent DGROUP frames')
    table=vector['map'].decode()
    for line in ('0000:8A92 03A5 C=CODE   S=_TEXT          G=(none)  M=exec       ACBP=28',
                 '0E3F:1184 0000 C=DATA   S=_DATA          G=DGROUP  M=exec       ACBP=48'):
        need(table.count(line)==1,'complete literal actual library MAP contribution')
    need(address(table,'__exec')==(0,BASE+359) and address(table,'DGROUP@')==(0,0x26D),'actual near API and CS startup DGROUP word')
    native=byte_map(raw,1);holes=set(range(255))|{356,357}
    need(set(native)==set(range(933))-holes and not byte_map(raw,2),'exact sparse CS buffer/saved-environment coverage and no DATA initializer')
    need(bytes(native[i] for i in range(352,356))==b'\xff\0\0\0' and native[358]==1,'relative copied-code IP/segment vector and original sticky environment flag')
    linked=parse_mz(vector['exe']);need(linked.valid,'complete actual selected MZ')
    image=bytearray(native[i] if i in native else linked.program_image[BASE+i] for i in range(933));observed=[];far=[]
    for f in fields:
        site=f['site'];need(f['segment']==1 and site+f['width']<=933 and not set(range(site,site+f['width']))&holes,'whole emitted native field')
        symbol='own CS'
        if f['target_method']==0:
            need(f['target']==1 and f['frame_method']==5 and f['segment_relative'],'actual own CS offset field');seg,off=0,BASE+f['addend']
        else:
            need(f['target_method']==2,'actual external field');symbol=EXTERNALS[f['target']-1];seg,off=address(table,symbol);off+=f['addend']
        if f['location_type']==3:
            need(f['width']==4 and f['frame_method']==5 and f['segment_relative'] and symbol=='__cexit' and seg==0 and
                 f['addend']==0 and image[site-1:site+4]==b'\x9a\0\0\0\0','genuine ordinary external far cleanup call')
            image[site-1:site+4]=b'\x90\x0e\xe8'+((off-(BASE+site+4))&65535).to_bytes(2,'little');far.append(dict(site=BASE+site-1,symbol=symbol,target=off))
        else:
            need(f['location_type']==1 and f['width']==2,'offset-only native WORD')
            if not f['segment_relative']:
                need((f['frame_method'],f['frame'],symbol,seg)==(0,1,'__IOERROR',0),'actual near error call');value=(off-(BASE+site+2))&65535
            else:
                if symbol in ('__envseg','__psp','__version'):need((f['frame_method'],f['frame'],seg)==(1,1,0xE3F),'actual DGROUP scalar offset')
                elif symbol=='DGROUP@':need((f['frame_method'],f['frame'],seg)==(0,1,0),'real CS-resident startup word,not segment immediate')
                else:need(symbol=='own CS' and seg==0,'own writable CS state reference')
                value=off
            image[site:site+2]=value.to_bytes(2,'little')
        observed.append(dict(f,symbol=symbol,resolved_target=[seg,off],product_site=BASE+site))
    need(not any(255<=f['site']<352 for f in fields),'copied continuation needs no link-time native fixup')
    image=bytes(image);need(image==linked.program_image[BASE:BASE+933],'independently resolved whole selected bank')
    extent((target,candidate),image,0,BASE,[])
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;procedures=[]
    for name,start,size,kind in [('overlay_load',255,97,'copied-continuation'),('__exec',359,574,'near-cdecl')]:
        ins=list(decoder.disasm(image[start:start+size],BASE+start));bounds={i.address for i in ins}
        need(sum(i.size for i in ins)==size,'complete instruction/CS-DATA partition')
        for i in ins:
            if i.mnemonic.startswith(('j','loop')) and i.operands[0].type==X86_OP_IMM:need(i.operands[0].imm in bounds,'all static local branches enter instructions')
        if kind=='near-cdecl':need(ins[-1].mnemonic=='ret' and not ins[-1].op_str,'original near caller-pop error return')
        else:need(ins[-1].mnemonic=='int' and ins[-1].op_str=='0x21','copied continuation retains DOS termination path')
        procedures.append(dict(name=name,offset=start,size=size,entry_kind=kind,public=kind=='near-cdecl',callee_pop_bytes=0))
    need(far==[dict(site=BASE+0x37B,symbol='__cexit',target=0x304A)],'sole real far cleanup call naturally relaxed')
    source=(root/SOURCE).read_bytes()
    need(b'overlay_stack db 143 dup (?)' in source and b'program_path db 80 dup (?)' in source and b'saved_environment dw ?' in source and
         b'transfer_target dw overlay_load-overlay_area,0' in source and b'mov cx,(overlay_copy_end-overlay_area)/2' in source,'typed real buffer/stack,relative copied-code address and natural copy length')
    owner=dict(unit_id=UNIT,name='exec',source=SOURCE,object=OBJECT,origin='library',segment=0,offset=BASE,start=BASE,size=933,
        coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=sha(image),candidate_sha256=sha(image),ordered_relocations=[],code_bytes=671,
        initialized_data_bytes=262,procedure_count=2,procedures=procedures,private_data_bytes=0,private_bss_bytes=0,
        maintained_native_object=report['rounds'][0]['outputs']['obj']['path'],abi='near cdecl12-byte overlay arguments,error return and copied nonreturning DOS continuation')
    return dict(owners=[owner],source_sha256=sha(source),native_fields=observed,equivalent_DGROUP_frame_changes=frame_changes,procedures=2,
        source_CODE_bytes=671,file_DATA_bytes=262,initialized_CS_bytes=5,uninitialized_CS_file_bytes=257,source_work_buffer_initializer_added=False,
        copied_continuation_bytes=97,copy_region_bytes=352,copy_relative_entry_offset=255,natural_far_cleanup_call=far[0],
        selected_build_report_sha256=report_sha,selected_assembly_library_link_rounds=2,normal_library_members=893,untouched_current_library_members=891,
        source_CRT_providers_in_selected_library=8,reused_natural_farheap=True,retained_project_objects=36,full_raw_vector_repeated=True,whole_EXE_MAP_equal=True,
        source_padding_added=False,original_cold_rebuilt=False,ancestor_runtime_replayed=False,physical_DOS_execution_claimed=False,whole_product_accepted=False)


if __name__=='__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['exec_native'],indent=2))
