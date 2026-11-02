#!/usr/bin/env python3
"""Review complete source-linked fopen, distinguishing OBJ FIXUPP order.

Do not claim complete native original OMF: TASM and BCC encode the same
12 logical relocations in a different order. EXE/MAP product raw equality
and all other original library member program records are tested separately.
"""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_fopen_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REVIEW='.analysis/work/mainl-fopen-native-review.json'


def code(raw):
    data=payload(raw)
    return bytes(data[1,i] for i in range(556))


def review():
    report_raw=(ROOT/p.REPORT).read_bytes()
    r=json.loads(report_raw)
    base,files,accepted,members,preceding,parenthash=p.retained()
    orig=p.ORIGINAL.read_bytes()
    goal=p.original_scope(orig)
    source=(ROOT/p.SOURCE).read_bytes()
    ordered=literal_fields(orig)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         not r['complete_native_OMF_equal'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_thirty_two_source_build_sha256']==parenthash and
         r['original_sha256']==sha(orig) and r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         r['native_assembler_flags']==p.TASM_FLAGS,
         'current native fopen source/driver, original accepted and parent closure')
    need(goal['CODE_bytes']==556 and
         goal['public']==[(212,'__OPENFP'),(422,'__GETFP'),(499,'_fopen')] and
         goal['externs']==p.EXTERNS and
         [x['site'] for x in ordered]==p.ORIGINAL_SITES and
         len(ordered)==12,
         'complete original CODE and authentic native twelve field order')
    segments=((0,212),(212,422),(422,499),(499,556))
    need([sum(ins.size for ins in Cs(CS_ARCH_X86,CS_MODE_16).disasm(code(orig)[a:b],a))
          for a,b in segments]==[212,210,77,57],
         'entire original near mode parser/OPENFP/GETFP and far fopen body')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two complete independent actual TASM/TLIB/TLINK runs')
    labels=['extract']+[f'round{n}-{kind}' for n in (1,2) for kind in
                        ('assemble','library','link')]
    need([x['label'] for x in r['phases']]==labels and all(
         x['returncode']==0 and
         sha((ROOT/x['log_path']).read_bytes())==x['log_sha256'] for x in r['phases']),
         'actual original Borland writer logs and full phase order')
    vectors=[]
    for index,entry in enumerate(r['rounds']):
        need(set(entry['outputs'])=={'obj','lib','exe','map'},
             'complete original native OBJ/LIB/EXE/MAP files')
        native={}
        for kind,q in entry['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'full raw native '+kind+' output file')
            native[kind]=data
        need(p.original_scope(native['obj'])==goal and
             code(native['obj'])==code(orig),
             'all556 native CODE bytes, unchanged extern/PUBDEF/group and logical fields')
        fields=literal_fields(native['obj'])
        need(fields!=ordered and
             sorted(fields,key=lambda x:(x['site'],x['location_type']))==
             sorted(ordered,key=lambda x:(x['site'],x['location_type'])) and
             [x['site'] for x in fields]==sorted(p.ORIGINAL_SITES),
             'literal native FIXUPP record ordering OPEN, other properties identical')
        compiled=dict(preceding[index],fopen=native['obj'])
        comparison=compare_members(members,library_members(native['lib']),compiled)
        need(comparison==entry['library_comparison'] and
             comparison['replaced_members']==sorted(compiled) and
             comparison['contextual_members_unchanged']==860,
             '33 original CRT source modules and860 unmodified library program records')
        need(native['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             native['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete Japanese decoded MAINL executable/MAP raw equal')
        mz=parse_mz(native['exe'])
        need(mz.valid and len(native['exe'])==67372 and
             len(mz.relocations)==677,
             'entire original MZ with all real original relocations')
        vectors.append(native)
    need(vectors[0]==vectors[1],
         'two deterministic complete native source OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,original_fopen_CODE_bytes=556,
                full_native_CODE_raw_equal=True,
                original_near_mode_parser_bytes=212,
                original_near_OPENFP_bytes=210,
                original_near_GETFP_bytes=77,
                original_far_fopen_bytes=57,
                real_original_pubdef_offsets=[212,422,499],
                original_imports=p.EXTERNS,
                original_FIXUPP_count=12,logical_FIXUPP_set_raw_equal=True,
                complete_native_OMF_equal=False,ordered_FIXUPPs_raw_equal=False,
                original_fixup_sites=p.ORIGINAL_SITES,
                source_fixup_sites=sorted(p.ORIGINAL_SITES),
                original_CRT_members=893,actual_source_members=33,
                untouched_original_member_programs=860,
                cumulative_source_CODE_bytes=20428,
                real_japanese_decoded_EXE_file_bytes=67372,
                original_MZ_relocations=677,
                entire_original_Japanese_EXE_raw_equal=True,
                entire_original_MAP_raw_equal=True,native_repeated_rounds=2,
                original_source=p.SOURCE,source_sha256=sha(source),
                original_build_report_sha256=sha(report_raw),
                parent_32_source_receipt_sha256=parenthash,
                accepted_publication_unchanged=True)


if __name__=='__main__':
    receipt=review()
    (ROOT/REVIEW).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
