#!/usr/bin/env python3
"""Review actual DOS destruction bytes and the integrated, unaccepted xx bank."""
import json
from pathlib import Path
import re
import struct
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from probe_th03_mainl_xx_dispatch import DRIVER,SOURCE,HEADER,FLAGS,LINK,WRAPPER,trap_context,sdk_inventory
from review_th03_mainl_xx_dispatch import review as dispatch_review,ACCEPTED_SHA,negative_constant_filter,CANDIDATE_SIZE
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_resources_work import cold_context,need,sha
from build_th03_mainl_work import WORK
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

REPORT='.analysis/work/mainl-xx-destruction-build.json'
REVIEW='.analysis/work/mainl-xx-destruction-review.json'
DESTROY='src/mainl/crt/xx_destroy.inl'
BASE,SIZE,XX_BASE=0x78D0,2500,0x580D
BODIES=[('destroyOneObject',0x791E,108,'far'),('destroyBases',0x798A,129,'far'),
    ('destroyVariable',0x7A0B,715,'far'),('destroyArray',0x7CD6,258,'far'),
    ('findTrueTypeAndAddr',0x7DD8,177,'far'),('dtorCleanup',0x7E89,1035,'near')]


def source_bodies(listing):
    result=[]
    for name,_,_,kind in BODIES:
        found=re.findall(r'^\s*\d+\s+([0-9A-F]{4})\s+(@'+name+r'\$\S+)\s+proc\s+(far|near)\s*$',listing,re.M)
        need(len(found)==1 and found[0][2]==kind,'actual TASM private procedure: '+name)
        start,symbol,_=found[0]
        end=re.findall(r'^\s*\d+\s+([0-9A-F]{4})\s+'+re.escape(symbol)+r'\s+endp\s*$',listing,re.M)
        need(len(end)==1,'actual TASM private procedure end: '+name)
        result.append(dict(name=name,start=int(start,16),size=int(end[0],16)-int(start,16),return_kind=kind))
    return result


def native_probe(image,entry,kind):
    """Two concrete ABI questions; run real instructions, never helper models."""
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_INTR
    from unicorn.x86_const import UC_X86_REG_CS,UC_X86_REG_IP,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_SP,UC_X86_REG_BP,UC_X86_REG_SI,UC_X86_REG_DI,UC_X86_REG_AX,UC_X86_REG_DX
    u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x80000);u.mem_write(0,image)
    ss,sp,finish=0x7000,0xFF00,0xF100
    def words(at,*values):u.mem_write(at,struct.pack('<'+'H'*len(values),*values))
    registers=[UC_X86_REG_AX,UC_X86_REG_SP,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_BP,UC_X86_REG_SI,UC_X86_REG_DI]
    for reg,value in [(UC_X86_REG_CS,0),(UC_X86_REG_DS,0xE3F),(UC_X86_REG_SS,ss),(UC_X86_REG_SP,sp),(UC_X86_REG_BP,0xAAAA),(UC_X86_REG_SI,0x7777),(UC_X86_REG_DI,0x8888),(UC_X86_REG_AX,0x9999)]:u.reg_write(reg,value)
    if kind=='empty-offset':
        # A nonzero segment makes an offset-only sentinel distinguishable from
        # either a null far pointer or a full FFFFFFFF pointer comparison.
        words(ss*16+sp,finish,0xFFFF,0x1234,0x3456,0x12,0x200,0x400)
        expected=[0,sp+2,0xE3F,ss,0xAAAA,0x7777,0x8888]
    else:
        need(kind=='far-vtable','bounded native probe selection')
        words(ss*16+sp,finish,0,0x300,0x6000,0x1000)
        words(ss*16+0x1000,0x200,0x6000)
        words(0x60206,6,0x1050)  # vptr offset; VTABLE|RTTI|FAR_VPTR
        words(0x60306,0x500,0x6000)
        words(0x604FC,0x20,0x10)
        words(0x604E8,0x400,0x6000)
        expected=[0x2E0,sp+4,0xE3F,ss,0xAAAA,0x7777,0x8888]
    returned=[]
    def stop(uc,site,count,data):
        if site==finish:returned.append(True);uc.emu_stop()
    def interrupt(uc,number,data):raise ValueError('destruction probe reached an unresolved helper/interrupt: '+str(number))
    u.hook_add(UC_HOOK_CODE,stop);u.hook_add(UC_HOOK_INTR,interrupt);u.emu_start(entry,0x80000,count=1000)
    values=[u.reg_read(q) for q in registers]
    need(returned==[True] and values==expected,'actual '+kind+' near/far cdecl return and preserved SS/register frame')
    result=dict(case=kind,return_value=values[0],sp=values[1],ds=values[2],ss=values[3],bp=values[4],si=values[5],di=values[6])
    if kind=='far-vtable':
        result.update(return_segment=u.reg_read(UC_X86_REG_DX),type=list(struct.unpack('<2H',u.mem_read(ss*16+0x1000,4))))
        need((result['return_segment'],result['type'])==(0x6000,[0x400,0x6000]),'far vtable and SS-relative type output')
    return result


def review(root,report=None):
    root=Path(root);old=dispatch_review(root);cold_context(root)
    raw=(root/REPORT).read_bytes();r=json.loads(raw) if report is None else report
    need(r['complete'] and not r['source_acceptance'] and r['accepted_source_bytes']==0 and r['miniature_only'] and not r['whole_product_linked'] and not r['whole_product_cold_rebuilt'],'unaccepted integrated xx bank remains a miniature')
    sources={'xxbank.inl':SOURCE,'xx_abi.h':HEADER,'xxdtor.inl':DESTROY}
    wrapper=WRAPPER.replace(b'int near dtorCleanup',b'static int near dtorCleanup')+b'#include "xxdtor.inl"\n'
    need(r['source_sha256']=={n:sha((root/n).read_bytes()) for n in sources.values()} and r['driver_sha256']==sha((root/DRIVER).read_bytes()),'maintained source/header/shared build driver bindings')
    need(r['compiler']==compiler_context(root) and r['compiler_flags']==FLAGS and r['available_SDK_header_sha256']==sdk_inventory(root),'current scoped compiler/profile/all64 available SDK headers')
    need(r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()) and r['wrapper_sha256']==sha(wrapper),'unchanged cold report and same-TU static cleanup wrapper')
    need((root/'.analysis/work/xx-destruction-wrapper.cpp').read_bytes()==wrapper and (root/'.analysis/work/xx-destruction-mini.lnk').read_bytes()==LINK,'actual native compiler wrapper and mini link response')
    for short,path in sources.items():need((root/('.analysis/work/xx-destruction-source-'+short)).read_bytes()==(root/path).read_bytes(),'actual compiler source transport: '+short)
    config=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/config['paths']['wine_prefix']
    dos=['/usr/bin/wine-stable',str(root/config['paths']['msdos_player']),'-e','-x'];tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t']
    phases=[]
    for number in (1,2):
        for label,command in [('compile',dos+[r'C:\BC45\BCC.EXE',*FLAGS,'xxdisp.cpp']),('assemble',tasm+['/l','xxdisp.asm','xxdisp.obj']),('context',tasm+['xxctx.asm','xxctx.obj']),('mini-link',dos+['tlink','@xxmini.lnk'])]:phases.append((f'round{number}-{label}',command,0))
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'two actual serial native rounds')
    for p in r['native_phases']:
        log=(root/('.analysis/work/xx-destruction-'+p['label']+'.log')).read_bytes();need(sha(log)==p['log_sha256'],'complete actual native phase log')
        if p['label'].endswith('compile'):need(log.startswith(r['compiler']['banner'].encode()+b'\r\n'),'actual BCC banner')
    vectors=[];bodies=[]
    for row in r['rounds']:
        need(set(row['outputs'])=={'asm','obj','context','exe','map','listing'},'five native outputs plus unmodified diagnostic listing')
        v={}
        for key,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'complete raw output identity');v[key]=b
        imports=externs(v['obj']);context=trap_context(imports)
        need(row['unresolved_imports']==imports and row['context_sha256']==sha(context) and (root/'.analysis/work/xx-destruction-context.asm').read_bytes()==context,'complete explicit diagnostic trap context')
        need(len(imports)==17 and not any(n.startswith('@dtorCleanup$') for n in imports),'cleanup resolves in the same TU; remaining17 interfaces remain unresolved')
        need(describe_omf(v['obj'])['valid'] and describe_omf(v['context'])['valid'],'actual whole native OMF structure')
        bodies.append(source_bodies(v['listing'].decode()));vectors.append(v)
    need({k:v for k,v in vectors[0].items() if k!='listing'}=={k:v for k,v in vectors[1].items() if k!='listing'} and bodies[0]==bodies[1],'whole raw ASM/two-OBJ/EXE/MAP repeat; listing page clocks are retained separately')
    v=vectors[0];candidate=parse_mz(v['exe']);target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());need(candidate.valid and target.valid,'real native mini MZ and fixed decoded Japanese target')
    definitions=segment_definitions(v['obj']);size=definitions[0]['size'];pubs=code_publics(v['obj'],1)
    need(definitions[1:]==[dict(index=i,name=n,**{'class':k},overlay='',size=s) for i,n,k,s in [(2,'_DATA','DATA',0),(3,'_BSS','BSS',8)]] and definitions[0]['name']=='_TEXT','no invented storage or separate product TU')
    need(pubs==[(459,'__Local_unwind'),(491,'__Return_unwind'),(673,'__ExceptionHandler')],'static destruction helpers add no public ABI')
    for off,name in pubs:need(address(v['map'].decode(),name)==(0,off),'actual linked public address')
    p=payload(v['obj']);need(len([k for k in p if k[0]==1])==size and not any(k[0] in (2,3) for k in p),'dense actual CODE and no initialized candidate DATA/BSS')
    native=(WORK/'vendor/xx.obj').read_bytes();op=payload(native);fields=[f for f in literal_fields(native) if f['segment']==1 and BASE-XX_BASE<=f['site']<BASE-XX_BASE+SIZE]
    image=bytearray(op[1,BASE-XX_BASE+i] for i in range(SIZE));original_map=(WORK/'obj/th03/mainl.map').read_text();mz=[]
    for f in fields:
        at=f['site']-(BASE-XX_BASE);absolute=BASE+at
        need(at+f['width']<=SIZE and (f['frame_method'],f['frame'])==(5,None),'complete literal original field and CODE frame')
        if f['target_method']==2:
            name=externs(native)[f['target']-1]
            mapped={'@__RefDestructorCount$qv':'__refdestructorcount()',
                '@$bdele$qnv':'operator delete(void far*)',
                '@$bdla$qnv':'operator delete[](void far*)'}.get(name,name)
            seg,off=address(original_map,mapped);need(seg==0 and f['addend']==0,'actual original library interface')
        else:
            need((f['target_method'],f['target'])==(0,1),'original internal CODE reference');seg,off=0,XX_BASE+f['addend']
        if f['location_type']==3:
            need(f['width']==4 and f['segment_relative'],'original FAR field')
            if image[at-1]==0x9A:
                image[at-1:at+4]=b'\x90\x0e\xe8'+((off-absolute-4)&65535).to_bytes(2,'little')
            else:
                image[at:at+4]=struct.pack('<2H',off,seg);mz.append(absolute+2)
        elif f['location_type']==2:
            need(f['width']==2 and f['segment_relative'],'original segment WORD');image[at:at+2]=seg.to_bytes(2,'little');mz.append(absolute)
        else:
            need(f['location_type']==1 and f['width']==2,'original offset/relative WORD')
            value=off if f['segment_relative'] else (off-absolute-2)&65535
            image[at:at+2]=value.to_bytes(2,'little')
    need(len(fields)==19 and bytes(image)==target.program_image[BASE:BASE+SIZE],'all2500 original raw bytes independently resolved with19 literal ordered fields')
    original_mz=[q.linear for q in target.relocations if BASE<=q.linear<BASE+SIZE]
    need(len(mz)==5 and mz==original_mz,'all five real original segment WORD sites in literal order')
    # Decode the two real catch tables and context table; never linear-disassemble
    # their 78 bytes as if they belonged to destroyOneObject's instructions.
    t=target.program_image
    for at,handler in [(0x78D0,0x7963),(0x78E8,0x7973)]:
        need(struct.unpack('<12H',t[at:at+24])==(0,0,handler,0,0,0,0,0,0,0,0,0),'actual catch-all handler descriptor')
    need(struct.unpack('<15H',t[0x7900:0x791E])==(0,0,0xFFE2,0,3,0x78E8,0,0,4,6,3,0x78D0,0,6,4),'actual nested try/catch contexts and BP offset')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;bounds=set();instructions=[];native_rows=[]
    for name,start,count,kind in BODIES:
        ins=list(decoder.disasm(t[start:start+count],start));need(sum(i.size for i in ins)==count and ins[-1].mnemonic==('ret' if kind=='near' else 'retf') and not ins[-1].op_str,'complete actual original body: '+name)
        instructions+=ins;bounds|={i.address for i in ins}
        native_rows.append(dict(name=name,start=start,size=count,return_kind=kind))
    need(BODIES[0][1]==BASE+78 and all(a[1]+a[2]==b[1] for a,b in zip(BODIES,BODIES[1:])) and BODIES[-1][1]+BODIES[-1][2]==BASE+SIZE,'complete nonoverlapping78 DATA plus2422 instruction-byte ownership')
    for i in instructions:
        if i.mnemonic.startswith(('j','loop')) and i.operands[0].type==X86_OP_IMM:need(i.operands[0].imm in bounds,'original direct branch stays on instruction boundaries')
    pairs=[]
    for original,recovered in zip(native_rows,bodies[0]):
        ins=list(decoder.disasm(candidate.program_image[recovered['start']:recovered['start']+recovered['size']],recovered['start']))
        need(sum(i.size for i in ins)==recovered['size'] and ins[-1].mnemonic==('ret' if recovered['return_kind']=='near' else 'retf'),'actual candidate full body: '+recovered['name'])
        pairs.append(dict(name=original['name'],original_bytes=original['size'],candidate_bytes=recovered['size'],complete_raw_equal=t[original['start']:original['start']+original['size']]==candidate.program_image[recovered['start']:recovered['start']+recovered['size']]))
    entries={q['name']:q['start'] for q in bodies[0]}
    need(bodies[0][0]['start']==CANDIDATE_SIZE+78 and all(a['start']+a['size']==b['start'] for a,b in zip(bodies[0],bodies[0][1:])) and bodies[0][-1]['start']+bodies[0][-1]['size']==size,'complete candidate dispatch/EH/destruction bank coverage')
    sentinel=[native_probe(t,0x7E89,'empty-offset'),native_probe(candidate.program_image,entries['dtorCleanup'],'empty-offset')]
    vtable=[native_probe(t,0x7DD8,'far-vtable'),native_probe(candidate.program_image,entries['findTrueTypeAndAddr'],'far-vtable')]
    need(sentinel[0]==sentinel[1] and vtable[0]==vtable[1],'target/source agree on both concrete ABI questions')
    filter_result=negative_constant_filter(candidate.program_image,673)
    need(filter_result==old['negative_constant_filter_target_and_source'][0],'same actual dispatcher branch after same-TU cleanup integration')
    return dict(complete=True,source_acceptance=False,accepted_source_bytes=0,accepted_publication_sha256=ACCEPTED_SHA,
        review_driver_sha256=sha((root/'scripts/review_th03_mainl_xx_destruction.py').read_bytes()),selected_build_report_sha256=sha(raw),source_sha256=r['source_sha256'],
        original_bank_base=BASE,original_bank_size=SIZE,original_instruction_bytes=2422,original_inline_EH_bytes=78,original_bodies=native_rows,
        original_literal_native_fields=fields,original_MZ_sites=original_mz,OMF_segment_field_sites=mz,candidate_literal_native_fields=literal_fields(v['obj']),
        candidate_CODE_segment_bytes=size,candidate_bodies=bodies[0],body_raw_comparison=pairs,
        complete_integrated_bank_raw_equal=candidate.program_image[:size]==t[0x72B3:BASE+SIZE],
        same_TU_cleanup_resolved=True,unresolved_interfaces=externs(v['obj']),two_whole_raw_vectors_repeated=True,
        diagnostic_listing_has_wall_clock_headers=True,empty_offset_target_and_source=sentinel,far_vtable_target_and_source=vtable,
        integrated_negative_constant_filter=filter_result,all_available_SDK_headers_bound=64,whole_product_linked=False,
        original_cold_rebuilt=False,ancestor_runtime_replayed=False,physical_DOS_execution_claimed=False)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];result=review(root);(root/REVIEW).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('original_literal_native_fields','candidate_literal_native_fields','source_sha256')},indent=2))
