#!/usr/bin/env python3
"""Independently review original 916-byte high-address qsort and full MAINL link."""
import json
from pathlib import Path

from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_hqsort_work as producer
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-hqsort-native-review.json'


def whole_CODE(obj):
    p=payload(obj)
    return bytes(p[1,i] for i in range(916))


def review():
    raw=(ROOT/producer.REPORT).read_bytes()
    receipt=json.loads(raw)
    base,files,accepted,members,previous,parenthash=producer.retained()
    original=producer.ORIGINAL.read_bytes()
    expected=producer.original_scope(original)
    inputs={name:(ROOT/name).read_bytes() for name in producer.SOURCES}
    need(receipt['complete'] and not receipt['source_acceptance'] and
         receipt['added_accepted_bytes']==0 and not receipt['original_cold_rebuilt'] and
         receipt['accepted_baseline']==base and
         receipt['accepted_library_sha256']==sha(accepted) and
         receipt['preceding_seventeen_source_build_sha256']==parenthash and
         receipt['original_sha256']==sha(original) and
         receipt['source_sha256']=={n:sha(blob) for n,blob in inputs.items()} and
         receipt['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         receipt['native_assembler_flags']==producer.TASM_FLAGS,
         'original full high-address sorter, source and native original library')
    need(expected['CODE_bytes']==916 and expected['far_public_offset']==872 and
         expected['BSS_bytes']==6 and len(expected['literal_ordered_fields'])==52 and
         expected['imports']==['N_PADD@','N_LXMUL@','N_PADA@','N_PCMP@',
                               'N_PSBA@','N_PSUB@','N_PSBP@','N_LDIV@'],
         'full high-address sort original native symbols/relocations/ABI')
    original_CODE=whole_CODE(original)
    decoder=Cs(CS_ARCH_X86,CS_MODE_16)
    bounds=((0,46),(46,872),(872,916))
    need([sum(i.size for i in decoder.disasm(original_CODE[a:b],a)) for a,b in bounds]==
         [46,826,44],'complete original near swap, high-address recursive core and public far wrapper')
    need(len(receipt['rounds'])==2 and
         [row['round'] for row in receipt['rounds']]==[1,2],
         'two actual independent native high-sort source rounds')
    phases=['extract']+[f'round{i}-{name}' for i in (1,2)
                        for name in ('assemble','library','link')]
    need([q['label'] for q in receipt['phases']]==phases and all(
         q['returncode']==0 and
         sha((ROOT/q['log_path']).read_bytes())==q['log_sha256']
         for q in receipt['phases']),
         'real native TASM/TLIB/TLINK original writer logs')
    vectors=[]
    for index,row in enumerate(receipt['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'complete native output vector types')
        out={}
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'literal real high-sort '+kind+' output')
            out[kind]=blob
        need(producer.original_scope(out['obj'])==expected and
             whole_CODE(out['obj'])==original_CODE and
             literal_fields(out['obj'])==literal_fields(original),
             'all916 original source CODE bytes and all52 native ordered fixups exact')
        source_members=dict(previous[index],hqsort=out['obj'])
        comparison=compare_members(members,library_members(out['lib']),source_members)
        need(comparison==row['library_comparison'] and
             comparison['replaced_members']==sorted(source_members) and
             comparison['contextual_members_unchanged']==875 and
             comparison['ordered_members_equal'],
             '18 original-position compiled CRT modules and875 original context members')
        need(out['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'entire fixed Japanese decoded MAINL exe and native map raw equal')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'all677 original MZ relocations and original file extent')
        vectors.append(out)
    need(vectors[0]==vectors[1],
         'two complete byte-identical native OBJ/LIB/EXE/MAP output vectors')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_highsort_CODE_bytes=916,
                source_highsort_CODE_bytes=916,original_native_CODE_equal=True,
                original_near_swap_bytes=46,
                original_highsort_recursive_core_bytes=826,
                original_far_public_bytes=44,
                original_far_public_offset=872,
                literal_ordered_fixups=52,all52_native_FIXUPPs_equal=True,
                original_BSS_bytes=6,source_BSS_bytes=6,
                external_original_imports=expected['imports'],
                original_CRT_members=893,original_source_members=18,
                untouched_original_member_programs=875,
                cumulative_exact_source_CODE_bytes=15786,
                original_Japanese_decoded_EXE_file_bytes=67372,
                original_MZ_relocations=677,
                whole_original_EXE_raw_equal=True,
                whole_original_MAP_raw_equal=True,
                native_repeated_rounds=2,original_source_paths=list(producer.SOURCES),
                original_build_sha256=sha(raw),
                inherited_seventeen_source_receipt_sha256=parenthash,
                accepted_publication_unchanged=True)


if __name__=='__main__':
    report=review()
    (ROOT/REPORT).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
