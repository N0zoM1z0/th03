#!/usr/bin/env python3
"""Review a bounded xx source candidate without upgrading native gaps to exactness."""
import json
from pathlib import Path
import struct
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from probe_th03_mainl_xx_dispatch import DRIVER,REPORT,SOURCE,HEADER,FLAGS,LINK,WRAPPER,trap_context,sdk_inventory
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_resources_work import cold_context,need,sha
from build_th03_mainl_work import WORK
from build_th03_mainl_display_work import payload,literal_fields
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_acceptance import proof_inputs
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

REVIEW='.analysis/work/mainl-xx-dispatch-review.json'
ACCEPTED_SHA='de7276df0d534f40e8bb1ab84f2d054688fd1960bf8cdf92d4a8108d7b34a551'
BASE,SIZE,XX_BASE=0x72B3,1565,0x580D
BODIES=[('local_unwind',0,447,'ret'),('_Local_unwind',459,32,'retf'),('_Return_unwind',491,42,'retf'),('findMatchingHandler',533,132,'ret'),('_ExceptionHandler',673,880,'retf')]
TABLES=[(447,12),(1553,12)]
TAG=(665,b'**BCCxh1')


def negative_constant_filter(image,entry):
    """One actual native branch; no imported helper or allocation is modeled."""
    from unicorn import Uc,UC_ARCH_X86,UC_MODE_16,UC_HOOK_CODE,UC_HOOK_INTR
    from unicorn.x86_const import UC_X86_REG_CS,UC_X86_REG_IP,UC_X86_REG_DS,UC_X86_REG_SS,UC_X86_REG_SP,UC_X86_REG_BP,UC_X86_REG_SI,UC_X86_REG_DI,UC_X86_REG_AX
    u=Uc(UC_ARCH_X86,UC_MODE_16);u.mem_map(0,0x80000);u.mem_write(0,image)
    ss,sp,record,registration,finish=0x7000,0xFF00,0x300,0x200,0xF100
    def word(at,value):u.mem_write(at,struct.pack('<H',value))
    def dword(at,value):u.mem_write(at,struct.pack('<L',value))
    for register,value in [(UC_X86_REG_CS,0),(UC_X86_REG_DS,0xE3F),(UC_X86_REG_SS,ss),(UC_X86_REG_SP,sp),(UC_X86_REG_BP,0xAAAA),(UC_X86_REG_SI,0x7777),(UC_X86_REG_DI,0x8888)]:u.reg_write(register,value)
    word(ss*16+0x14,registration);dword(ss*16+0x16,0x60000200)
    u.mem_write(0x60200,struct.pack('<L3H',0x60000100,0x3333,0,0))
    word(ss*16+registration,0x111);dword(ss*16+registration+6,0x60000000)
    for off,value in [(10,0xF200),(12,0x10),(14,0x1357),(16,0x2468),(24,0x550)]:word(ss*16+registration+off,value)
    dword(ss*16+record,0xC0000094);dword(ss*16+record+4,1);dword(ss*16+record+24,0x60000100)
    word(0x60000+4,0x20);u.mem_write(0x60010,struct.pack('<3H',6,2,0xFFFF))
    u.mem_write(ss*16+sp,struct.pack('<9H',finish,0,record,ss,registration,0x3456,0x6000,0x100,0x6000))
    returned=[]
    def stop(uc,site,count,data):
        if site==finish:returned.append(True);uc.emu_stop()
    def interrupt(uc,number,data):raise ValueError('dispatch probe unexpectedly called an unresolved helper/trap/interrupt: '+str(number))
    u.hook_add(UC_HOOK_CODE,stop);u.hook_add(UC_HOOK_INTR,interrupt);u.emu_start(entry,0x80000,count=10000)
    need(returned==[True],'negative constant filter returns through the actual far caller frame')
    result=dict(return_value=u.reg_read(UC_X86_REG_AX),sp=u.reg_read(UC_X86_REG_SP),ds=u.reg_read(UC_X86_REG_DS),ss=u.reg_read(UC_X86_REG_SS),bp=u.reg_read(UC_X86_REG_BP),si=u.reg_read(UC_X86_REG_SI),di=u.reg_read(UC_X86_REG_DI),
        context=int.from_bytes(u.mem_read(ss*16+registration+12,2),'little'),exception_code=int.from_bytes(u.mem_read(ss*16+registration+20,4),'little'),exception_info=int.from_bytes(u.mem_read(ss*16+registration+24,2),'little'),
        chain=int.from_bytes(u.mem_read(ss*16+0x14,2),'little'),runtime_saved_ds=int.from_bytes(u.mem_read(0x60206,2),'little'),runtime_saved_si=int.from_bytes(u.mem_read(0x60208,2),'little'))
    need(result==dict(return_value=0,sp=0xFF04,ds=0xE3F,ss=ss,bp=0xAAAA,si=0x7777,di=0x8888,context=6,exception_code=0xC0000094,exception_info=0x550,chain=registration,runtime_saved_ds=0x1357,runtime_saved_si=0x2468),'original noncontinuable negative-filter context,SS fields and far cdecl preservation')
    return result


def review(root,report=None):
    root=Path(root);cold_context(root)
    accepted_raw=(root/'config/mainl_work/scoped_acceptance.json').read_bytes();accepted=json.loads(accepted_raw)
    need(sha(accepted_raw)==ACCEPTED_SHA and accepted['proof_inputs']==proof_inputs(root),'current211-owner accepted publication and verifier inputs unchanged')
    need(len(accepted['audit']['scope']['owners'])==211 and sum(o['size'] for o in accepted['audit']['scope']['owners'])==36946,'no new exact credit for xx candidate')
    raw=(root/REPORT).read_bytes();r=json.loads(raw) if report is None else report
    need(r['complete'] and not r['source_acceptance'] and r['accepted_source_bytes']==0 and r['miniature_only'] and not r['whole_product_linked'] and not r['whole_product_cold_rebuilt'],'unaccepted isolated dispatch bank,not a product or source-exact link')
    need(r['compiler']==compiler_context(root) and r['compiler_flags']==FLAGS and r['source_sha256']=={n:sha((root/n).read_bytes()) for n in (SOURCE,HEADER)} and r['driver_sha256']==sha((root/DRIVER).read_bytes()) and r['cold_report_sha256']==sha((root/'.analysis/work/mainl-build.json').read_bytes()),'current maintained source/header/compiler/profile/driver/cold binding')
    need(r['available_SDK_header_sha256']==sdk_inventory(root),'all64 available SDK headers bound; no consumed-header subset is inferred')
    need(r['wrapper_sha256']==sha(WRAPPER) and (root/'.analysis/work/xx-dispatch-wrapper.cpp').read_bytes()==WRAPPER and (root/'.analysis/work/xx-dispatch-source-xxbank.inl').read_bytes()==(root/SOURCE).read_bytes() and (root/'.analysis/work/xx-dispatch-source-xx_abi.h').read_bytes()==(root/HEADER).read_bytes() and (root/'.analysis/work/xx-dispatch-mini.lnk').read_bytes()==LINK,'actual compiler source/header and native mini-link response')
    c=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/c['paths']['wine_prefix'];dos=['/usr/bin/wine-stable',str(root/c['paths']['msdos_player']),'-e','-x'];tasm=['/usr/bin/wine-stable',str(prefix/'drive_c/TASM50/bin/TASM32.EXE'),'/m','/mx','/kh32768','/t'];phases=[]
    for number in (1,2):
        for label,cmd in [('compile',dos+[r'C:\BC45\BCC.EXE',*FLAGS,'xxdisp.cpp']),('assemble',tasm+['xxdisp.asm','xxdisp.obj']),('context',tasm+['xxctx.asm','xxctx.obj']),('mini-link',dos+['tlink','@xxmini.lnk'])]:phases.append((f'round{number}-{label}',cmd,0))
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'two actual serial compiler/assembler/trap-context/mini-link rounds')
    for p in r['native_phases']:
        log=(root/('.analysis/work/xx-dispatch-'+p['label']+'.log')).read_bytes();need(sha(log)==p['log_sha256'],'preserved actual native phase log')
        if p['label'].endswith('compile'):need(log.startswith(r['compiler']['banner'].encode()+b'\r\n'),'actual scoped BCC banner')
    vectors=[]
    for row in r['rounds']:
        need(set(row['outputs'])=={'asm','obj','context','exe','map'},'complete generated ASM/two-OBJ/mini-EXE/MAP vector');v={}
        for name,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'whole actual native raw output identity');v[name]=b
        imports=externs(v['obj']);context=trap_context(imports)
        need(row['unresolved_imports']==imports and row['context_sha256']==sha(context) and (root/'.analysis/work/xx-dispatch-context.asm').read_bytes()==context,'all seven unresolved interfaces use the declared unreachable trap fixture')
        need(describe_omf(v['obj'])['valid'] and describe_omf(v['context'])['valid'],'complete actual native OMF structure')
        vectors.append(v)
    need(vectors[0]==vectors[1],'whole native raw two-round vectors repeat')
    v=vectors[0];native=parse_mz(v['exe']);target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());need(native.valid and target.valid,'real native mini executable and fixed Japanese decoded target')
    definitions=segment_definitions(v['obj']);size=definitions[0]['size']
    need(definitions==[dict(index=i,name=n,**{'class':k},overlay='',size=s) for i,n,k,s in [(1,'_TEXT','CODE',1566),(2,'_DATA','DATA',0),(3,'_BSS','BSS',8)]],'whole candidate CODE/empty DATA/two actual callback slots in BSS')
    pubs=code_publics(v['obj'],1);need(pubs==[(459,'__Local_unwind'),(491,'__Return_unwind'),(673,'__ExceptionHandler')],'all three native publics and the original bank-relative entry offsets')
    table=v['map'].decode()
    for off,symbol in pubs:need(address(table,symbol)==(0,off),'actual mini native public addresses')
    fields=literal_fields(v['obj']);data_fields=[f for f in fields if f['target_method']==0 and f['target']==3]
    need(len(data_fields)==6 and all((f['frame_method'],f['frame'])==(1,1) for f in data_fields),'both ES indirect callbacks must use DGROUP,including their actual memory operand fields')
    p=payload(v['obj']);code=bytes(p[1,i] for i in range(size));need(code[665:673]==TAG[1] and len([k for k in p if k[0]==1])==size and not any(k[0] in (2,3) for k in p),'semantic eight-byte ABI tag,dense CODE and no invented DATA/BSS initializer')
    original=(WORK/'vendor/xx.obj').read_bytes();op=payload(original);old_fields=literal_fields(original)
    need(segment_definitions(original)==[dict(index=i,name=n,**{'class':k},overlay='',size=s) for i,n,k,s in [(1,'_TEXT','CODE',12622),(2,'_DATA','DATA',18),(3,'_BSS','BSS',10)]],'whole original xx module segment/storage boundaries')
    need(all((BASE-XX_BASE+off,symbol) in code_publics(original,1) for off,symbol in pubs),'complete original bank public identities and offsets')
    original_map=(WORK/'obj/th03/mainl.map').read_text()
    need(original_map.count('0E3F:2876 000A C=BSS    S=_BSS           G=DGROUP  M=xx')==1,'original normal-library BSS allocation,not candidate-owned file bytes')
    image=bytearray(op[1,BASE-XX_BASE+i] for i in range(SIZE));bank_fields=[]
    for f in old_fields:
        if f['segment']!=1 or not BASE-XX_BASE<=f['site']<BASE-XX_BASE+SIZE:continue
        bank_fields.append(f);site=f['site']-(BASE-XX_BASE)
        need(site+f['width']<=SIZE and f['segment_relative'],'complete original field within the bank')
        if f['location_type']==3:
            symbol=externs(original)[f['target']-1];seg,off=address(original_map,symbol)
            need((f['target_method'],symbol,seg,f['addend'],image[site-1])==(2,'___call_unexpected',0,0,0x9A),'sole original far import in this bank')
            image[site-1:site+4]=b'\x90\x0e\xe8'+((off-BASE-site-4)&65535).to_bytes(2,'little')
        else:
            need(f['width']==2 and f['location_type']==1 and f['target_method']==0,'real original offset WORD')
            if f['target']==1:
                need((f['frame_method'],f['frame'])==(5,None),'actual original CODE frame');value=XX_BASE+f['addend']
            else:
                need((f['target'],f['frame_method'],f['frame'])==(3,1,1),'actual original callback DGROUP frame');value=0x2876+f['addend']
            image[site:site+2]=value.to_bytes(2,'little')
    need(bytes(image)==target.program_image[BASE:BASE+SIZE],'entire independently resolved original bank,including actual fields and far-call relaxation')
    # Instruction boundaries are checked against real target bytes,not inferred
    # from public-symbol gaps or linear decoding through inline tables.
    occupied=[i for _,o,n,_ in BODIES for i in range(o,o+n)]+[i for o,n in TABLES for i in range(o,o+n)]+list(range(TAG[0],TAG[0]+len(TAG[1])))
    need(len(occupied)==SIZE and set(occupied)==set(range(SIZE)),'complete nonoverlapping instruction/table/signature classification')
    decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True;bounds=set();instructions=[]
    for name,off,count,ret in BODIES:
        ins=list(decoder.disasm(target.program_image[BASE+off:BASE+off+count],BASE+off));need(sum(i.size for i in ins)==count and (ins[-1].mnemonic,ins[-1].op_str)==(ret,''),'complete original near/far body: '+name);instructions+=ins;bounds|={i.address for i in ins}
    need(sum(n for _,_,n,_ in BODIES)==1533 and target.program_image[BASE+TAG[0]:BASE+TAG[0]+8]==TAG[1],'original instruction count and semantic ABI tag')
    for off,count in TABLES:
        entries=[int.from_bytes(target.program_image[BASE+off+i:BASE+off+i+2],'little') for i in range(0,count,2)]
        need(len(entries)==6 and all(q in bounds for q in entries),'each actual CS switch WORD enters a recovered instruction')
    for ins in instructions:
        if ins.mnemonic.startswith(('j','loop')) and ins.operands[0].type==X86_OP_IMM:need(ins.operands[0].imm in bounds,'direct control flow excludes real switch/tag data')
    need(not [q for q in target.relocations if BASE<=q.linear<BASE+SIZE],'original bank has no MZ segment WORDs')
    results=[negative_constant_filter(target.program_image,BASE+673),negative_constant_filter(native.program_image,673)]
    return dict(review_driver_sha256=sha((root/'scripts/review_th03_mainl_xx_dispatch.py').read_bytes()),complete=True,source_acceptance=False,accepted_source_bytes=0,accepted_publication_sha256=ACCEPTED_SHA,selected_build_report_sha256=sha(raw),source_sha256=r['source_sha256'],
        original_bank_base=BASE,original_bank_size=SIZE,original_instruction_bytes=1533,original_inline_DATA_bytes=32,original_bodies=[dict(name=n,offset=o,size=s,return_kind=k) for n,o,s,k in BODIES],original_switch_tables=[list(q) for q in TABLES],
        candidate_CODE_segment_bytes=size,candidate_publics=[list(q) for q in pubs],candidate_literal_native_fields=fields,original_literal_native_fields=bank_fields,complete_bank_raw_equal=native.program_image[:size]==target.program_image[BASE:BASE+SIZE],
        same_public_entry_offsets=True,unresolved_private_and_runtime_interfaces=r['rounds'][0]['unresolved_imports'],two_whole_raw_vectors_repeated=True,negative_constant_filter_target_and_source=results,
        all_available_SDK_headers_bound=64,whole_product_linked=False,original_cold_rebuilt=False,ancestor_runtime_replayed=False,physical_DOS_execution_claimed=False)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];result=review(root);(root/REVIEW).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('candidate_literal_native_fields','original_literal_native_fields','negative_constant_filter_target_and_source')},indent=2))
