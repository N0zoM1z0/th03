"""Complete natural far-heap source, normal member replacement and exact native output."""
import hashlib
import json
import re
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from build_th03_mainl_farheap_work import SOURCE,DRIVER,REPORT,library_response,link_response
from build_th03_mainl_display_work import literal_fields,payload
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_file_native import byte_map
from lib.borland_library import library_members,compare_members
from lib.omf import parse_omf,describe_omf
from lib.pc98 import parse_mz
from lib.op_asset_native import extent
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

UNIT='th03-mainl-decoded-crt-farheap'
OBJECT='vendor/farheap.obj'
BASE=0x3A15
PUBLICS=[(0,'___first'),(2,'___last'),(4,'___rover'),(320,'_farfree'),(320,'_free'),
         (627,'_malloc'),(637,'_farmalloc'),(986,'_realloc'),(993,'_farrealloc')]
# Disjoint physical pieces; free/farfree alias one API, while word/long size
# entries have distinct prologues that enter the same far-return body.
PROCS=(
 ('release_top',12,99,'ret',False),('release_inner',111,113,'fallthrough-unlink',False),
 ('unlink_free',224,41,'ret',False),('insert_free',265,55,'ret',False),('_free',320,41,'retf',True),
 ('start_heap',361,100,'ret',False),('extend_heap',461,131,'ret',False),('take_free_tail',592,35,'ret',False),
 ('_malloc',627,10,'shared-far-body',True),('_farmalloc',637,125,'retf',True),
 ('move_growing_block',762,124,'ret',False),('shrink_block',886,100,'ret',False),
 ('_realloc',986,7,'shared-far-body',True),('_farrealloc',993,122,'retf',True),
)


def need(v,message):
    if not v:raise ValueError('MAINL far heap native: '+str(message))


def sha(b):return hashlib.sha256(b).hexdigest()


def selected(root,work,files):
    report_raw=(root/REPORT).read_bytes();report=json.loads(report_raw);source=(root/SOURCE).read_bytes()
    need(report['complete'] and not report['source_acceptance'] and not report['whole_product_cold_rebuilt'] and
         report['retained_project_objects']==36 and report['source_sha256']==sha(source) and report['driver_sha256']==sha((root/DRIVER).read_bytes()) and
         report['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()),'actual maintained source/recipe/unchanged cold context')
    current=(work/'crt.lib').read_bytes();members=library_members(current)
    need(report['current_library_sha256']==sha(current) and len(members)==893,'complete retained normal library')
    need((root/'.analysis/work/farheap-source.asm').read_bytes()==source and
         (root/'.analysis/work/farheap-library.rsp').read_bytes()==library_response(members) and
         (root/'.analysis/work/farheap-link.lnk').read_bytes()==link_response(files),'preserved exact source and native response inputs')
    config=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/config['paths']['wine_prefix']
    tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t','farheap.asm','farheap.obj']
    dos=['/usr/bin/wine-stable',str(root/config['paths']['msdos_player']),'-e','-x']
    phases=[]
    for n in (1,2):phases += [(f'round{n}-assemble',tasm,0),(f'round{n}-library',dos+['tlib',r'@probe\hpcrt.rsp'],0),(f'round{n}-link',dos+['tlink',r'@probe\hpheap.lnk'],0)]
    need([(p['label'],p['command'],p['returncode']) for p in report['native_phases']]==phases,'actual two-round TASM/TLIB/TLINK schedule')
    need([r['round'] for r in report['rounds']]==[1,2],'two complete independent selected vectors');vectors=[]
    for row in report['rounds']:
        need(set(row['outputs'])=={'obj','lib','exe','map'},'whole native output vector');v={}
        for name,meta in row['outputs'].items():
            b=(root/meta['path']).read_bytes();need(meta==dict(path=meta['path'],bytes=len(b),sha256=sha(b)),'complete current raw selected output');v[name]=b
        review=compare_members(members,library_members(v['lib']),{'farheap':v['obj']})
        need(row['library']==review and review['member_count']==893 and review['contextual_members_unchanged']==892,'literal library member order and all untouched members')
        need(v['exe']==(work/'bin/th03/mainl.target.exe').read_bytes() and v['map']==(work/'obj/th03/mainl.map').read_bytes(),'complete pinned Japanese decoded EXE and retained MAP equality')
        vectors.append(v)
    need(vectors[0]==vectors[1],'complete raw OBJ/LIB/EXE/MAP repetition')
    return vectors[0],report,sha(report_raw)


def verify(root,work,target,candidate,graph,files):
    vector,report,report_sha=selected(root,work,files);raw=vector['obj'];original=(work/OBJECT).read_bytes();d=describe_omf(raw)
    need(d['valid'] and d['module_name']=='farheap.asm' and d['translator_comments']==['Turbo Assembler  Version 5.0'] and
         d['dependency_paths']==['farheap.asm'],'actual complete source consumption and native object integrity')
    need(segment_definitions(raw)==[dict(index=1,name='_TEXT',**{'class':'CODE'},overlay='',size=1115),dict(index=2,name='_DATA',**{'class':'DATA'},overlay='',size=0)] and
         [r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF']==[0x28,0x48] and
         [r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF']==['06ff02'],'complete native BYTE CODE/WORD empty DATA/DGROUP geometry')
    need(code_publics(raw,1)==code_publics(original,1)==PUBLICS and not code_publics(raw,2) and
         externs(raw)==externs(original)==['__brk','__sbrk'],'complete public aliases and actual near external ABI')
    fields=literal_fields(raw)
    need(payload(raw)==payload(original) and fields==literal_fields(original) and len(fields)==49,'complete native initialized payload and literal absolute ordered fields equal original member')
    need(not byte_map(raw,2),'empty DATA has no source byte credit')
    table=vector['map'].decode()
    for line in ('0000:3A15 045B C=CODE   S=_TEXT          G=(none)  M=farheap    ACBP=28',
                 '0E3F:1130 0000 C=DATA   S=_DATA          G=DGROUP  M=farheap    ACBP=48'):
        need(table.count(line)==1,'complete actual library MAP contribution')
    for off,symbol in PUBLICS:need(address(table,symbol)==(0,BASE+off),'all state/API aliases in both MAP public tables')
    native=byte_map(raw,1);holes=set(range(6,12))
    need(set(native)==set(range(1115))-holes and bytes(native[i] for i in range(6))==b'\0'*6,'three real zero state WORDs and exactly three uninitialized scratch WORDs')
    linked=parse_mz(vector['exe']);need(linked.valid,'complete actual selected MZ')
    image=bytearray(native[i] if i in native else linked.program_image[BASE+i] for i in range(1115));observed=[]
    for f in fields:
        site=f['site'];need(f['segment']==1 and f['width']==2 and f['location_type']==1 and not set(range(site,site+2))&holes,'complete emitted offset WORD field')
        if f['segment_relative']:
            need((f['frame_method'],f['frame'],f['target_method'],f['target'])==(5,None,0,1) and f['addend'] in (0,2,4,6,8,10),'genuine CS state/scratch offset,never a segment load')
            value=BASE+f['addend'];symbol=('___first','___last','___rover','saved_dgroup','resize_high','resize_low')[f['addend']//2]
        else:
            need((f['frame_method'],f['frame'],f['target_method'])==(0,1,2) and f['target'] in (1,2) and f['addend']==0,'actual near brk/sbrk call')
            symbol=['__brk','__sbrk'][f['target']-1];seg,off=address(table,symbol);need(seg==0,'same CODE near callee')
            value=(off-(BASE+site+2))&65535
        image[site:site+2]=value.to_bytes(2,'little');observed.append(dict(f,symbol=symbol,product_site=BASE+site,resolved_word=value))
    image=bytes(image);need(image==linked.program_image[BASE:BASE+1115],'independently resolved whole actual native linked bank')
    extent((target,candidate),image,0,BASE,[])
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;ins=list(decoder.disasm(image[12:],BASE+12));bounds={i.address for i in ins}
    need(sum(i.size for i in ins)==1103,'complete instruction/file-DATA partition')
    for i in ins:
        if i.mnemonic.startswith(('j','loop')):need(i.operands[0].type==X86_OP_IMM and i.operands[0].imm in bounds,'every local branch enters a complete instruction')
    procedures=[]
    for name,off,size,ret,pub in PROCS:
        body=[i for i in ins if BASE+off<=i.address<BASE+off+size]
        need(sum(i.size for i in body)==size,'complete disjoint physical body')
        if ret in ('ret','retf'):need(body[-1].mnemonic==ret and not body[-1].op_str,'original caller-pop near/far return')
        elif ret=='shared-far-body':need(body[-1].mnemonic=='jmp' and body[-1].operands[0].imm in (BASE+0x286,BASE+0x3E7),'word-size API enters the actual shared far body')
        else:need(name=='release_inner' and BASE+off+size==BASE+224 and body[-1].mnemonic=='mov','interior free falls into the callable unlink helper')
        if pub:need((off,name) in PUBLICS,'real native API entry')
        procedures.append(dict(name=name,offset=off,size=size,return_kind=ret,public=pub,callee_pop_bytes=0))
    need(sum(p['size'] for p in procedures)==1103 and len(procedures)==14,'complete code ownership without alias double counting')
    source=(root/SOURCE).read_bytes()
    for name in ('saved_dgroup','resize_high','resize_low'):need(re.search((r'(?m)^'+name+r' dw \?$').encode(),source),'source preserves original uninitialized CS scratch')
    need(b'call _farmalloc' in source and b'call _free' in source and b'___first dw 0' in source,'natural same-segment far calls and real zero initial state')
    owner=dict(unit_id=UNIT,name='farheap',source=SOURCE,object=OBJECT,origin='library',segment=0,offset=BASE,start=BASE,size=1115,
        coordinate_space='decoded-load',canonical_file_offset=None,target_sha256=sha(image),candidate_sha256=sha(image),ordered_relocations=[],
        code_bytes=1103,initialized_data_bytes=12,procedure_count=14,procedures=procedures,private_data_bytes=0,private_bss_bytes=0,
        maintained_native_object=report['rounds'][0]['outputs']['obj']['path'],abi='far cdecl word/long allocation APIs,private register-ABI near helpers and shared near exits')
    return dict(owners=[owner],source_sha256=sha(source),native_fields=observed,procedures=14,source_CODE_bytes=1103,file_DATA_bytes=12,
        initialized_CS_state_bytes=6,uninitialized_CS_scratch_file_bytes=6,CS_scratch_initializer_added=False,all_49_ordered_native_fields_equal_original=True,
        selected_build_report_sha256=report_sha,selected_assembly_library_link_rounds=2,normal_library_members=893,untouched_library_members=892,
        retained_project_objects=36,whole_EXE_MAP_equal=True,full_raw_vector_repeated=True,ordered_scope_relocations=[],
        source_padding_added=False,original_cold_rebuilt=False,ancestor_runtime_replayed=False,physical_DOS_execution_claimed=False,whole_product_accepted=False)


if __name__=='__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['farheap_native'],indent=2))
