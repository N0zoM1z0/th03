#!/usr/bin/env python3
"""Independently verify full original stat CODE/DATA/FIXUPPs and 36-source link."""
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_16

import build_th03_mainl_stat_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-stat-native-review.json'


def native_parts(obj):
    x=payload(obj)
    return (bytes(x[1,i] for i in range(556)),
            bytes(x[2,i] for i in range(4)))


def review():
    raw=(ROOT/p.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,prior,parenthash=p.retained()
    original=p.ORIGINAL.read_bytes()
    expected=p.original_scope(original)
    source=(ROOT/p.SOURCE).read_bytes()
    old_code,old_data=native_parts(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['prior_fopen_FIXUPP_order_open'] and
         r['prior_fclose_MKNAME_frame_open'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_thirty_five_source_build_sha256']==parenthash and
         r['original_sha256']==sha(original) and r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         r['native_assembler_flags']==p.TASM_FLAGS,
         'unchanged pinned Japanese original, full semantic source and native parent')
    need(expected['CODE_bytes']==556 and expected['DATA_bytes']==4 and
         expected['original_pub_offset']==132 and
         expected['imports']==p.EXTERNS and
         [f['site'] for f in expected['literal_fields']]==p.FIXUP_SITES and
         old_data==bytes.fromhex('5c2f2e00'),
         'real private path helper, stat DOS FindFirst, 4 initialized bytes and9 OMF records')
    instructions=Cs(CS_ARCH_X86,CS_MODE_16)
    need([sum(ins.size for ins in instructions.disasm(old_code[a:b],a)) for a,b in
          ((0,132),(132,556))]==[132,424],
         'full actual original 132-byte path separator finder and424-byte public stat')
    need(len(r['rounds'])==2 and [row['round'] for row in r['rounds']]==[1,2],
         'two original native independent assemblies/normal links')
    phases=['extract']+[f'round{i}-{phase}' for i in (1,2)
                        for phase in ('assemble','library','link')]
    need([q['label'] for q in r['phases']]==phases and
         all(q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
             q['log_sha256'] for q in r['phases']),
         'actual complete native TASM/TLIB/TLINK writer receipts')
    vectors=[]
    for i,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'raw native object/full source library/executable/MAP all present')
        results={}
        for kind,meta in row['outputs'].items():
            file=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(file),sha256=sha(file)),
                 'actual full '+kind+' output file identity')
            results[kind]=file
        need(p.original_scope(results['obj'])==expected and
             native_parts(results['obj'])==(old_code,old_data) and
             literal_fields(results['obj'])==literal_fields(original),
             'literal all 556 CODE, 4 DATA and nine ordered OMF original fields exact')
        source_members=dict(prior[i],stat=results['obj'])
        comparison=compare_members(members,library_members(results['lib']),source_members)
        need(comparison==row['library_comparison'] and
             comparison['replaced_members']==sorted(source_members) and
             comparison['contextual_members_unchanged']==857,
             '36 exact source library positions and857 untouched original member programs')
        need(results['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             results['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete original Japanese decoded MAINL EXE and MAP byte-for-byte')
        mz=parse_mz(results['exe'])
        need(mz.valid and len(results['exe'])==67372 and len(mz.relocations)==677,
             'whole original DOS MZ with all 677 real relocations')
        vectors.append(results)
    need(vectors[0]==vectors[1],'two full byte-identical original native writer output vectors')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,original_stat_CODE_bytes=556,
                exact_original_stat_CODE_bytes=556,original_stat_DATA_bytes=4,
                exact_original_DATA_bytes=4,
                raw_CODE_equal=True,raw_initialized_DATA_equal=True,
                original_near_helper_bytes=132,original_public_stat_bytes=424,
                original_far_stat_public_offset=132,
                literal_ordered_original_OMF_FIXUPPs=9,literal_fields_raw_equal=True,
                original_imports=p.EXTERNS,
                original_CRT_member_count=893,source_members_in_link=36,
                other_original_member_programs_unchanged=857,
                cumulative_exact_source_CODE_bytes=21275,
                new_original_DATA_bytes=4,
                original_japanese_EXE_bytes=67372,original_MZ_relocations=677,
                full_japanese_EXE_raw_equal=True,whole_original_MAP_raw_equal=True,
                native_repeated_rounds=2,prior_fopen_OMF_order_open=True,
                prior_fclose_near_frame_open=True,
                source_path=p.SOURCE,bound_build_sha256=sha(raw),
                parent_35_source_receipt_sha256=parenthash,
                published_accepted_ledger_unchanged=True)


if __name__=='__main__':
    q=review()
    (ROOT/REPORT).write_text(json.dumps(q,indent=2)+'\n')
    print(json.dumps(q,indent=2))
