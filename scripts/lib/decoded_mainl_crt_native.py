"""Six complete CRT source producers and their actual normal-library contributions."""
import hashlib
import json
import re
import tomllib
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from build_th03_mainl_display_work import literal_fields
from lib.decoded_mainl_display_native import externs
from lib.decoded_mainl_file_native import byte_map
from lib.borland_library import library_members, object_program_records
from lib.omf import parse_omf, describe_omf
from lib.op_asset_native import extent
from lib.op_shared_native import address
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

PREFIX = 'th03-mainl-decoded-crt-'
# Physical bodies are disjoint. Near entry shims synthesize the far return and
# fall through into the shared body; aliases at the far entry add no procedures.
# name, offset, size, return, callee-pop, public
P = lambda n,o,s,r='ret',p=0,v=True: (n,o,s,r,p,v)
SCOPES = (
 ('h_llsh',0x315E,33,0xE8E,0,[P('N_LXLSH@',0,3,'near-to-far'),P('LXLSH@',3,30,'retf')]),
 ('h_padd',0x317F,96,0xE8E,0,[P('N_PADD@',0,3,'near-to-far'),P('PADD@',3,44,'retf'),P('N_PSUB@',47,3,'near-to-far'),P('PSUB@',50,46,'retf')]),
 ('ioerror',0x31DF,82,0xE8E,91,[P('__IOERROR',0,62,p=2),P('__DOSERROR',62,20,p=2)]),
 ('n_pcmp',0x357C,33,0xF02,0,[P('N_PCMP@',0,33)]),
 ('fbrk',0x3E70,352,0x1130,2,[P('grow_break',0,142,p=4,v=False),P('__brk',142,67),P('__sbrk',209,143)]),
 ('setblock',0x8E5A,32,0x1184,0,[P('_setblock',0,32,'retf')]),
)
DATA = {'ioerror': 'dos-error-data', 'fbrk': 'break-granule-data'}
SOURCE_MAP = {PREFIX+name: ('src/mainl/crt/'+name+'.asm','owned/'+name+'.obj') for name, *_ in SCOPES}
SOURCE_MAP.update({PREFIX+unit: ('src/mainl/crt/'+name+'.asm','owned/'+name+'.obj') for name,unit in DATA.items()})
EXTERNALS = {
 'h_llsh': [], 'h_padd': [], 'n_pcmp': [], 'ioerror': ['_errno','__sys_nerr'],
 'fbrk': ['_setblock','N_PCMP@','N_LXLSH@','N_PADD@','__psp','__heapbase','__brklvl','__heaptop'],
 'setblock': ['__IOERROR'],
}
PUBLICS = {
 'h_llsh': [(0,'N_LXLSH@'),(3,'F_LXLSH@'),(3,'LXLSH@')],
 'h_padd': [(0,'N_PADD@'),(3,'F_PADD@'),(3,'PADD@'),(47,'N_PSUB@'),(50,'F_PSUB@'),(50,'PSUB@')],
 'ioerror': [(0,'__IOERROR'),(62,'__DOSERROR')], 'n_pcmp': [(0,'N_PCMP@')],
 'fbrk': [(142,'__brk'),(209,'__sbrk')], 'setblock': [(0,'_setblock')],
}
DS = 0xE3F


def need(v,message):
    if not v:
        raise ValueError('MAINL CRT native: '+str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def resolve(raw,base,data_base,table):
    data=byte_map(raw,1);image=bytearray(data[i] for i in range(len(data)))
    names=externs(raw);details=[];far=[]
    for f in literal_fields(raw):
        need(f['segment']==1 and f['site']+f['width']<=len(image),'complete CODE field')
        site=f['site'];actual=base+site
        if f['target_method']==2:
            symbol=names[f['target']-1];seg,off=address(table,symbol);off+=f['addend']
        else:
            need((f['target_method'],f['target'],f['frame_method'],f['frame'])==(0,2,1,1),'private DGROUP data field')
            symbol='private DATA';seg,off=DS,data_base+f['addend']
        if f['location_type']==3:
            need(f['width']==4 and f['target_method']==2 and f['frame_method']==5 and
                 f['segment_relative'] and seg==0 and f['addend']==0 and
                 image[site-1:site+4]==b'\x9a\0\0\0\0','genuine ordinary external far CALL')
            image[site-1:site+4]=b'\x90\x0e\xe8'+((off-(actual+4))&65535).to_bytes(2,'little')
            far.append(dict(site=actual-1,symbol=symbol,target=off))
        else:
            need(f['location_type']==1 and f['width']==2,'offset-only native WORD')
            if f['segment_relative']:
                need((f['frame_method'],f['frame'],seg)==(1,1,DS),'actual DGROUP offset frame')
                value=off
            else:
                need((f['frame_method'],f['frame'],seg)==(0,1,0),'actual near CODE call frame')
                value=(off-(actual+2))&65535
            image[site:site+2]=value.to_bytes(2,'little')
        details.append(dict(f,symbol=symbol,resolved_target=[seg,off],product_site=actual))
    return bytes(image),details,far


def error_data(root,files):
    config=tomllib.loads((root/'config/toolchain.toml').read_text())
    sdk=root/config['paths']['wine_prefix']/'drive_c/TC4/INCLUDE/ERRNO.H'
    installed=root/'.analysis/toolchain/installed/tc40j/INCLUDE/ERRNO.H'
    raw=sdk.read_bytes();need(raw==installed.read_bytes(),'installed errno ABI header identity')
    defines={n:int(v) for n,v in re.findall(rb'(?m)^#define\s+(E\w+)\s+(\d+)\s',raw)}
    equates={n:int(v) for n,v in re.findall(rb'(?m)^(E\w+) equ (\d+)$',files['owned/crt_errno.inc'])}
    need(equates[b'EZERO']==0 and all(defines[n]==v for n,v in equates.items() if n!=b'EZERO'),'every named errno constant agrees with the installed ABI')
    rows=re.findall(rb'(?m)^\s*db (E\w+) ; DOS (\d+)\s*$',files['owned/dos_error_map.inc'])
    need([int(n) for _,n in rows]==list(range(89)),'complete ordered DOS error domain0..88')
    need(len(re.findall(rb'(?m)^\s*db\b',files['owned/dos_error_map.inc']))==89,'no extra map bytes')
    return b'\0\0'+bytes(equates[n] for n,_ in rows),sha(raw)


def verify(root,work,target,candidate,graph,files):
    import build_th03_mainl_work as build
    report_raw=(root/'.analysis/work/mainl-build.json').read_bytes();report=json.loads(report_raw)
    need(report['complete'] and report['raw_repeat_equal'] and [r['round'] for r in report['rounds']]==[1,2] and
         report['rounds'][0]['outputs']==report['rounds'][1]['outputs'],'unchanged complete cold pair reused')
    need(set(n for n,*_ in SCOPES)==set(build.CRT) and build.CRT==('h_llsh','h_padd','n_pcmp','ioerror','fbrk','setblock'),'the six actual library producers and original assembly schedule')
    source_names=[*[n+'.asm' for n,*_ in SCOPES],'crt_errno.inc','dos_error_map.inc']
    need(all(files['owned/'+n]==(root/'src/mainl/crt'/n).read_bytes()==(work/'owned'/n).read_bytes() and
             report['source_sha256']['owned/'+n]==sha(files['owned/'+n]) for n in source_names),
         'complete source-bound maintained CRT native inputs and literal staging')
    members=library_members((work/'crt.lib').read_bytes());need(len(members)==893,'complete normal library')
    table=(work/'obj/th03/mainl.map').read_text();decoder=Cs(CS_ARCH_X86,CS_MODE_16);decoder.detail=True
    semantic,errno_sha=error_data(root,files);owners=[];modules=[];far_calls=[]
    for name,base,size,data_base,data_size,procs in SCOPES:
        obj='owned/'+name+'.obj';raw=(work/obj).read_bytes();d=describe_omf(raw)
        need(report['rounds'][0]['outputs'][obj]==dict(bytes=len(raw),sha256=sha(raw)),'current complete raw CRT vector')
        need(d['valid'] and d['module_name']==name+'.asm' and d['translator_comments']==['Turbo Assembler  Version 5.0'] and
             d['dependency_paths']==[name+'.asm']+(['crt_errno.inc','dos_error_map.inc'] if name=='ioerror' else []),'actual native producer and complete include closure')
        member,=[m for m in members if m.name==name]
        need(member.program_records==object_program_records(raw),'complete linked library member equals its native source producer')
        rows=[(1,'_TEXT','CODE',size),(2,'_DATA','DATA',data_size)]+([] if name in ('h_llsh','h_padd','n_pcmp') else [(3,'_BSS','BSS',0)])
        need(segment_definitions(raw)==[dict(index=i,name=n,**{'class':c},overlay='',size=s) for i,n,c,s in rows] and
             [r.data[0] for r in parse_omf(raw) if r.name=='SEGDEF']==[0x28]+[0x48]*(len(rows)-1),'complete BYTE CODE,WORD DATA/BSS native geometry')
        group='06ff02' if len(rows)==2 else '08ff03ff02' if name=='fbrk' else '08ff02ff03'
        need([r.data.hex() for r in parse_omf(raw) if r.name=='GRPDEF']==[group],'literal native DGROUP member order')
        for seg,off,sz,cls,sn,grp,attr in [(0,base,size,'CODE','_TEXT','(none)',0x28),(DS,data_base,data_size,'DATA','_DATA','DGROUP',0x48)]:
            need(len(re.findall(rf'(?m)^\s*{seg:04X}:{off:04X}\s+{sz:04X}\s+C={cls}\s+S={sn}\s+G={re.escape(grp)}\s+M={name}\s+ACBP={attr:02X}\s*$',table))==1,'complete actual library MAP contribution')
        need(code_publics(raw,1)==PUBLICS[name] and externs(raw)==EXTERNALS[name],'complete public and external native identities')
        for off,symbol in PUBLICS[name]:need(address(table,symbol)==(0,base+off),'all near/far aliases in both MAP tables')
        need(set(byte_map(raw,1))==set(range(size)) and set(byte_map(raw,2))==set(range(data_size)) and
             (len(rows)==2 or not byte_map(raw,3)),'complete CODE/DATA,empty BSS initializer coverage')
        image,fields,far=resolve(raw,base,data_base,table);extent((target,candidate),image,0,base,[]);far_calls+=far
        ins=list(decoder.disasm(image,base));bounds={i.address for i in ins}
        need(sum(i.size for i in ins)==size,'complete dense CRT instructions')
        for i in ins:
            if i.mnemonic.startswith(('j','loop')):
                need(i.operands[0].type==X86_OP_IMM and i.operands[0].imm in bounds,'all static local branches enter instructions,including shared pointer bodies')
        procedures=[]
        for symbol,off,length,ret,pop,public in procs:
            body=[i for i in ins if base+off<=i.address<base+off+length]
            need(sum(i.size for i in body)==length,'complete disjoint physical body')
            if ret=='near-to-far':
                need([i.mnemonic for i in body]==['pop','push','push'] and body[1].op_str=='cs' and
                     body[0].op_str==body[2].op_str and body[0].op_str in ('bx','es'),'near-entry shim synthesizes far return and falls into shared body')
            else:
                need(body[-1].mnemonic==ret and (int(body[-1].op_str,0) if body[-1].op_str else 0)==pop,'native near/far return and callee cleanup')
            if public:need((off,symbol) in PUBLICS[name],'actual native procedure entry')
            procedures.append(dict(name=symbol,offset=off,size=length,return_kind=ret,callee_pop_bytes=pop,public=public))
        need(sum(p['size'] for p in procedures)==size,'all CRT bytes have physical body ownership without alias double counting')
        owners.append(owner(PREFIX+name,name,obj,0,base,image,len(procedures),procedures))
        native_data=bytes(byte_map(raw,2)[i] for i in range(data_size))
        need(native_data==(semantic if name=='ioerror' else b'\0'*data_size),'complete named error mapping and original zero granule')
        if data_size:
            extent((target,candidate),native_data,DS,data_base,[])
            owners.append(owner(PREFIX+DATA[name],name,obj,DS,data_base,native_data,0,[]))
        expected_data_pubs=[(0,'__doserrno'),(2,'__dosErrorToSV')] if name=='ioerror' else []
        need(code_publics(raw,2)==expected_data_pubs,'complete DATA aliases or genuinely private state')
        for off,symbol in expected_data_pubs:need(address(table,symbol)==(DS,data_base+off),'both DATA public MAP tables')
        modules.append(dict(name=name,object=obj,object_sha256=sha(raw),library_member_index=members.index(member),fields=fields,
                            native_CODE_bytes=size,native_DATA_bytes=data_size,BSS_file_bytes=0,ordered_relocations=[]))
    need(sum(len(m['fields']) for m in modules)==39 and far_calls==[dict(site=0x3EBC,symbol='_setblock',target=0x8E5A)],'complete39-field stream and sole natural far-call relaxation')
    return dict(owners=owners,native_modules=modules,source_CODE_bytes=628,source_initialized_DATA_bytes=93,procedures=13,
        near_to_far_shim_entries=3,distinct_far_body_entries=3,aliases_add_no_procedures=True,natural_far_calls=far_calls,
        source_padding_added=False,uninitialized_file_byte_credit=0,errno_SDK_sha256=errno_sha,DOS_error_map_entries=89,
        unchanged_cold_report_sha256=sha(report_raw),retained_full_raw_outputs=938,reused_cold_rounds=2,
        native_rebuild_required=False,ancestor_runtime_replayed=False,whole_product_accepted=False)


def owner(unit,name,obj,seg,off,image,count,procedures):
    return dict(unit_id=unit,name=unit.removeprefix(PREFIX),source='src/mainl/crt/'+name+'.asm',object=obj,origin='library',
        segment=seg,offset=off,start=seg*16+off,size=len(image),coordinate_space='decoded-load',canonical_file_offset=None,
        target_sha256=sha(image),candidate_sha256=sha(image),ordered_relocations=[],code_bytes=len(image) if seg==0 else 0,
        initialized_data_bytes=len(image) if seg==DS else 0,procedure_count=count,procedures=procedures,
        private_data_bytes=0,private_bss_bytes=0,abi='16-bit CRT register helpers,near callee-pop error helpers and near/far cdecl heap-break chain')


if __name__=='__main__':
    from pathlib import Path
    from lib.decoded_mainl_acceptance import audit
    print(json.dumps(audit(Path(__file__).resolve().parents[2])['scope']['crt_native'],indent=2))
