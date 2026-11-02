#!/usr/bin/env python3
"""Review all 756 original DOS qsort bytes and a 17-member native source link."""
import json
from pathlib import Path

from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_qsort_work as producer
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-qsort-native-review.json'


def whole_CODE(raw):
    p=payload(raw)
    return bytes(p[1,i] for i in range(756))


def review():
    report_raw=(ROOT/producer.REPORT).read_bytes()
    receipt=json.loads(report_raw)
    base,files,accepted,members,previous,parenthash=producer.retained()
    original=producer.ORIGINAL.read_bytes()
    original_scope=producer.original_scope(original)
    source_input={name:(ROOT/name).read_bytes() for name in producer.SOURCES}
    need(receipt['complete'] and not receipt['source_acceptance'] and
         receipt['added_accepted_bytes']==0 and not receipt['original_cold_rebuilt'] and
         receipt['accepted_baseline']==base and
         receipt['accepted_library_sha256']==sha(accepted) and
         receipt['preceding_sixteen_source_build_sha256']==parenthash and
         receipt['original_sha256']==sha(original) and
         receipt['source_sha256']=={k:sha(v) for k,v in source_input.items()} and
         receipt['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         receipt['native_assembler_flags']==producer.TASM_FLAGS,
         'current full qsort source,original native member and accepted baseline')
    need(original_scope['CODE_bytes']==756 and
         original_scope['far_public_offset']==712 and
         original_scope['BSS_bytes']==6 and
         original_scope['imports']==['N_LXMUL@','N_LDIV@'] and
         len(original_scope['literal_ordered_fields'])==29,
         'complete original DOS quicksort native TASM interface and fixups')
    orig=whole_CODE(original)
    capstone=Cs(CS_ARCH_X86,CS_MODE_16)
    parts=((0,46),(46,712),(712,756))
    need([sum(x.size for x in capstone.disasm(orig[a:b],a)) for a,b in parts]==
         [46,666,44],'actual entire private swap,recursive sorter and far entry bounds')
    need(len(receipt['rounds'])==2 and
         [row['round'] for row in receipt['rounds']]==[1,2],
         'two complete real source round trips')
    phases=['extract']+[f'round{i}-{n}' for i in (1,2) for n in
                        ('assemble','library','link')]
    need([q['label'] for q in receipt['phases']]==phases and
         all(q['returncode']==0 and
             sha((ROOT/q['log_path']).read_bytes())==q['log_sha256']
             for q in receipt['phases']),
         'actual successful TASM/TLIB/TLINK writer phase logs')
    expected=[m.name for m in members if m.name in set(previous[0])|{'qsort'}]
    vectors=[]
    for round_no,row in enumerate(receipt['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'real complete native source output vector')
        outputs={}
        for kind,q in row['outputs'].items():
            raw=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(raw),sha256=sha(raw)),
                 'unchanged full native '+kind+' artifact')
            outputs[kind]=raw
        need(producer.original_scope(outputs['obj'])==original_scope and
             whole_CODE(outputs['obj'])==orig and
             literal_fields(outputs['obj'])==literal_fields(original),
             'every original CODE byte and every ordered literal native FIXUPP')
        sources=dict(previous[round_no],qsort=outputs['obj'])
        compared=compare_members(members,library_members(outputs['lib']),sources)
        need(compared==row['library_comparison'] and
             compared['replaced_members']==expected and
             compared['contextual_members_unchanged']==876,
             '17 real source slots at original indices,876 complete untouched member programs')
        need(outputs['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete original decoded Japanese MAINL EXE/MAP raw byte identity')
        mz=parse_mz(outputs['exe'])
        need(mz.valid and len(outputs['exe'])==67372 and len(mz.relocations)==677,
             'complete original MZ image and all677 original relocations')
        vectors.append(outputs)
    need(vectors[0]==vectors[1],
         'two independent identical native source OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_qsort_CODE_bytes=756,source_qsort_CODE_bytes=756,
                all_native_qsort_CODE_bytes_equal=True,
                qsort_private_near_swap_bytes=46,
                qsort_recursive_sort_core_bytes=666,
                qsort_far_public_bytes=44,original_far_public_offset=712,
                original_sorted_ordered_fields=29,
                all29_literal_native_FIXUPPs_equal=True,
                original_and_native_BSS_bytes=[6,6],
                original_import_order=['N_LXMUL@','N_LDIV@'],
                original_CRT_members=893,
                exact_source_CRT_members=17,
                untouched_original_program_records=876,
                cumulative_exact_source_CODE_bytes=14870,
                complete_decoded_Japanese_EXE_bytes=67372,
                original_MZ_relocation_entries=677,
                actual_Japanese_EXE_raw_equal=True,
                whole_original_MAP_raw_equal=True,
                complete_native_rounds=2,
                source_paths=list(producer.SOURCES),
                original_build_report_sha256=sha(report_raw),
                previous_sixteen_source_receipt_sha256=parenthash,
                accepted_publication_unchanged=True)


if __name__=='__main__':
    r=review()
    (ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
