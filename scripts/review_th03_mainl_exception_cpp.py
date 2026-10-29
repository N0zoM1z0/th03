#!/usr/bin/env python3
"""Review natural C++ candidates honestly; native mismatches give zero exact credit."""
import json
from pathlib import Path
import re
import tomllib
from capstone import Cs,CS_ARCH_X86,CS_MODE_16
from probe_th03_mainl_exception_cpp import SOURCES,FLAGS,DRIVER,REPORT,reused_pairs,library_response,link_response
from build_th03_mainl_resources_work import cold_context,need,sha
from build_th03_mainl_work import WORK
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.decoded_mainl_display_native import externs
from probe_th03_main_boss_marisa_cpp import code_publics
from probe_th03_main_bomb_rikako_cpp import segment_definitions

REVIEW='.analysis/work/mainl-exception-cpp-review.json'
ACCEPTED_PUBLICATION_SHA256='686c32dc99ec87fba8b6de5c2525b42a0a730ef204e6d42985aa7c2c4a98584a'
ORIGINAL={
 'new':dict(base=0x3273,size=754,instructions=[(28,107),(135,46),(181,81),(262,67),(367,91),(458,39),(621,77)],data=[(0,28),(329,38),(497,58),(555,66),(698,56)]),
 'xalloc':dict(base=0x5251,size=513,instructions=[(0,91),(127,120),(247,67),(380,77)],data=[(91,36),(314,66),(457,56)]),
 'xmsg':dict(base=0x5452,size=955,instructions=[(36,167),(239,171),(410,94),(518,83),(637,185)],data=[(0,36),(203,36),(504,14),(601,36),(822,56),(878,19),(897,58)])}


def review(root,report=None):
    root=Path(root);cold,files,_=cold_context(root);reused,meta=reused_pairs(root,WORK,files)
    accepted_raw=(root/'config/mainl_work/scoped_acceptance.json').read_bytes()
    from lib.decoded_mainl_acceptance import proof_inputs
    accepted=json.loads(accepted_raw)
    need(sha(accepted_raw)==ACCEPTED_PUBLICATION_SHA256 and accepted['proof_inputs']==proof_inputs(root),'accepted publication and verifier inputs remain unchanged')
    need(len(accepted['audit']['scope']['owners'])==205 and sum(o['size'] for o in accepted['audit']['scope']['owners'])==34688,'zero accepted-source progress from CPP candidates')
    raw=(root/REPORT).read_bytes();r=json.loads(raw) if report is None else report
    need(r['complete'] and not r['source_acceptance'] and r['accepted_source_bytes']==0 and not r['whole_product_cold_rebuilt'] and r['retained_project_objects']==36,'unaccepted bounded candidate,not source-exact publication')
    need(r['source_sha256']=={p:sha((root/p).read_bytes()) for p in SOURCES.values()} and r['driver_sha256']==sha((root/DRIVER).read_bytes()) and r['compiler_flags']==FLAGS and r['cold_report_sha256']==sha(cold) and r['reused_sources']==meta,'current maintained C++ source/driver/flags/cold/reused context')
    members=library_members((WORK/'crt.lib').read_bytes());need(len(members)==893 and r['current_library_sha256']==sha((WORK/'crt.lib').read_bytes()),'retained normal library identity')
    need(all((root/('.analysis/work/exception-cpp-source-'+n+'.cpp')).read_bytes()==(root/p).read_bytes() for n,p in SOURCES.items()) and
         (root/'.analysis/work/exception-cpp-library.rsp').read_bytes()==library_response(members) and (root/'.analysis/work/exception-cpp-link.lnk').read_bytes()==link_response(files),'actual preserved source and response inputs')
    config=tomllib.loads((root/'config/toolchain.toml').read_text());prefix=root/config['paths']['wine_prefix'];dos=['/usr/bin/wine-stable',str(root/config['paths']['msdos_player']),'-e','-x'];phases=[]
    for number in (1,2):
        phases += [(f'round{number}-{n}',dos+['tcc',*FLAGS,n+'.cpp'],0) for n in SOURCES]
        phases += [(f'round{number}-library',dos+['tlib',r'@probe\excplib.rsp'],0),(f'round{number}-link',dos+['tlink',r'@probe\excpp.lnk'],0)]
    need([(p['label'],p['command'],p['returncode']) for p in r['native_phases']]==phases and [v['round'] for v in r['rounds']]==[1,2],'two actual serial compiler/TLIB/TLINK rounds')
    vectors=[];headers={}
    for row in r['rounds']:
        need(set(row['outputs'])==set(SOURCES)|{'lib','exe','map'},'complete selected output vector');v={}
        for name,m in row['outputs'].items():
            b=(root/m['path']).read_bytes();need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),'whole current native output identity');v[name]=b
        need(row['library']==compare_members(members,library_members(v['lib']),dict(reused,**{n:v[n] for n in SOURCES})) and row['library']['contextual_members_unchanged']==871,'all893 positions and871 other current library members')
        for n in SOURCES:
            d=describe_omf(v[n]);need(d['valid'] and d['module_name']==n+'.cpp' and d['translator_comments']==['TC86 Borland C++ 4.02'],'real maintained high-level compiler input')
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
    v=vectors[0];target=parse_mz((WORK/'bin/th03/mainl.target.exe').read_bytes());candidate=parse_mz(v['exe']);need(target.valid and candidate.valid,'actual complete native executable views')
    equal_exe=v['exe']==(WORK/'bin/th03/mainl.target.exe').read_bytes();equal_map=v['map']==(WORK/'obj/th03/mainl.map').read_bytes()
    need(r['whole_EXE_equal']==equal_exe and r['whole_MAP_equal']==equal_map,'reported whole EXE/MAP comparison is honest')
    modules={};table=v['map'].decode()
    for name,layout in ORIGINAL.items():
        original=(WORK/('vendor/'+name+'.obj')).read_bytes();fresh=v[name];old_defs,new_defs=segment_definitions(original),segment_definitions(fresh)
        need(old_defs[0]['size']==layout['size'],'original reviewed whole module size')
        spans=[dict(offset=o,size=s,kind=kind) for kind,key in [('CODE','instructions'),('inline-CS-data','data')] for o,s in layout[key]]
        occupied=set()
        for span in spans:
            positions=set(range(span['offset'],span['offset']+span['size']));need(not positions&occupied,'nonoverlapping original instruction/table ownership: '+name);occupied|=positions
        need(occupied==set(range(layout['size'])),'complete original module classification without padding credit')
        for off,count in layout['instructions']:
            ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(target.program_image[layout['base']+off:layout['base']+off+count],layout['base']+off))
            need(sum(i.size for i in ins)==count and ins[-1].mnemonic=='retf','whole original far procedure,excluding actual inline data')
        match,=re.findall(rf'(?m)^\s*0000:([0-9A-F]+)\s+([0-9A-F]+)\s+C=CODE\s+S=_TEXT\s+G=\(none\)\s+M={name}\s+ACBP=28\s*$',table)
        base,count=(int(x,16) for x in match);need(count==new_defs[0]['size'],'complete candidate library CODE allocation')
        old_publics,new_publics=code_publics(original,1),code_publics(fresh,1);need([n for _,n in old_publics]==[n for _,n in new_publics] and externs(original)==externs(fresh),'source recovers all original public/external identities')
        original_fields,new_fields=literal_fields(original),literal_fields(fresh);need(len(original_fields)==len(new_fields),'complete native field count preserved,not an equality gate')
        modules[name]=dict(original_segment_definitions=old_defs,candidate_segment_definitions=new_defs,original_publics=[list(p) for p in old_publics],candidate_publics=[list(p) for p in new_publics],
            original_instruction_spans=[dict(offset=o,size=s) for o,s in layout['instructions']],original_inline_data_spans=[dict(offset=o,size=s) for o,s in layout['data']],
            original_CODE_bytes=sum(s for _,s in layout['instructions']),original_inline_CS_DATA_bytes=sum(s for _,s in layout['data']),
            complete_initialized_payload_equal=payload(original)==payload(fresh),original_literal_native_fields=original_fields,candidate_literal_native_fields=new_fields,
            original_literal_ordered_MZ=[[r.segment,r.offset] for r in target.relocations if layout['base']<=r.linear<layout['base']+layout['size']],
            candidate_literal_ordered_MZ=[[r.segment,r.offset] for r in candidate.relocations if base<=r.linear<base+count],candidate_link_offset=base)
    return dict(complete=True,source_acceptance=False,accepted_source_bytes=0,current_accepted_source_progress_changed=False,modules=modules,
        source_sha256=r['source_sha256'],accepted_publication_sha256=ACCEPTED_PUBLICATION_SHA256,selected_build_report_sha256=sha(raw),consumed_vendor_header_sha256=headers,two_raw_vectors_repeated=True,
        normal_library_members=893,untouched_current_library_members=871,reused_natural_providers=19,source_providers_in_candidate_library=28,retained_project_objects=36,
        whole_EXE_equal=equal_exe,whole_MAP_equal=equal_map,original_cold_rebuilt=False,ancestor_runtime_replayed=False,physical_execution_claimed=False)


if __name__=='__main__':
    root=Path(__file__).resolve().parents[1];result=review(root);(root/REVIEW).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('modules','consumed_vendor_header_sha256')},indent=2))
