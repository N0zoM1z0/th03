#!/usr/bin/env python3
"""Review four-entry DOS getc and its true original 30-source MAINL link."""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_getc_work as producer
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-getc-native-review.json'


def whole_CODE(blob):
    p=payload(blob)
    return bytes(p[1,i] for i in range(485))


def review():
    build_raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(build_raw)
    base,files,accepted,members,prior29,previous_sha=producer.retained()
    original=producer.ORIGINAL.read_bytes()
    source={n:(ROOT/n).read_bytes() for n in producer.SOURCES}
    goal=producer.original_scope(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_twenty_nine_source_build_sha256']==previous_sha and
         r['original_sha256']==sha(original) and
         r['source_sha256']=={n:sha(data) for n,data in source.items()} and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['native_assembler_flags']==producer.TASM_FLAGS,
         'actual original multi-public getc native source and original library')
    pubs=[(192,'__fgetc'),(217,'__Nfgetc'),
          (220,'_fgetc'),(469,'_fgetchar')]
    f=goal['literal_ordered_fields']
    need(goal['CODE_bytes']==485 and goal['original_BSS_bytes']==1 and
         goal['native_publics']==pubs and goal['imports']==
         ['__streams','_fflush','_eof','___read'] and
         [x['site'] for x in f]==[359,437,461,19,43,119,372,393,473],
         'all485 CODE, four true public entries, one BSS and9 literal original fields')
    code=whole_CODE(original)
    ins=list(Cs(CS_ARCH_X86,CS_MODE_16).disasm(code,0))
    need(sum(x.size for x in ins)==485 and len(ins)==193 and
         code[68]==0xc3 and code[189:192]==bytes.fromhex('c20400') and code[192]==0x55 and
         code[216]==0xcb and code[217:220]==bytes.fromhex('580e50') and
         code[468]==0xcb and code[484]==0xcb,
         'genuine private near/far getc return and near-stack bridge ABI')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two actual independent BCC-native TASM/TLIB/TLINK rounds')
    phases=['extract']+[f'round{i}-{n}' for i in (1,2) for n in
                        ('assemble','library','link')]
    need([q['label'] for q in r['phases']]==phases and
         all(q['returncode']==0 and
             sha((ROOT/q['log_path']).read_bytes())==q['log_sha256']
             for q in r['phases']),
         'actual original Borland compiler writer logs and return values')
    vectors=[]
    for idx,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'complete native source output categories')
        output={}
        for name,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'complete byte-identical native original '+name+' output')
            output[name]=data
        need(producer.original_scope(output['obj'])==goal and
             whole_CODE(output['obj'])==code and
             literal_fields(output['obj'])==f,
             'every native CODE byte and every unusual chronological original OMF field')
        sources=dict(prior29[idx],getc=output['obj'])
        compared=compare_members(members,library_members(output['lib']),sources)
        need(compared==row['library_comparison'] and
             compared['replaced_members']==sorted(sources) and
             compared['contextual_members_unchanged']==863,
             '30 original source CRT slots and 863 remaining program records unchanged')
        need(output['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete original Japanese decoded MAINL EXE and MAP byte-equal')
        mz=parse_mz(output['exe'])
        need(mz.valid and len(output['exe'])==67372 and len(mz.relocations)==677,
             'whole original Japanese DOS MZ with677 original relocation words')
        vectors.append(output)
    need(vectors[0]==vectors[1],'two identical whole native OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_getc_CODE_bytes=485,source_getc_CODE_bytes=485,
                all_native_CODE_bytes_equal=True,original_8086_instruction_count=193,
                original_native_BSS_bytes=1,source_native_BSS_bytes=1,
                original_public_entries=pubs,original_external_imports=goal['imports'],
                original_literal_OMF_FIXUPPs=9,
                all_nine_original_ordered_FIXUPPs_equal=True,
                near_to_far_public_bridge='580e50',near_and_far_ABI_preserved=True,
                original_CRT_members=893,source_CRT_members=30,
                untouched_original_programs=863,
                total_joint_source_CODE_bytes=19340,
                original_Japanese_EXE_bytes=67372,MZ_relocation_count=677,
                full_original_EXE_raw_equal=True,original_MAP_raw_equal=True,
                native_repeated_rounds=2,
                source_paths=list(producer.SOURCES),
                build_receipt_sha256=sha(build_raw),
                previous_29_source_receipt_sha256=previous_sha,
                accepted_publication_unchanged=True)


if __name__=='__main__':
    result=review()
    (ROOT/REPORT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
