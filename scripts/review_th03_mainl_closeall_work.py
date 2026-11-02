#!/usr/bin/env python3
"""Exact closeall native CODE/FIXUPP and 34-source product-only MAINL link."""
import json
from pathlib import Path

import build_th03_mainl_closeall_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REVIEW='.analysis/work/mainl-closeall-native-review.json'


def review():
    raw=(ROOT/p.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,prior,parenthash=p.retained()
    original=p.ORIGINAL.read_bytes()
    goal=p.original_scope(original)
    src=(ROOT/p.SOURCE).read_bytes()
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['partial_parent_fopen_OMF_order_open'] is True and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_thirty_three_source_build_sha256']==parenthash and
         r['original_sha256']==sha(original) and r['source_sha256']==sha(src) and
         r['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         r['native_assembler_flags']==p.TASM_FLAGS,
         'real original closeall program/driver, unchanged 33-source product-only parent')
    need(goal['CODE_bytes']==99 and goal['publics']==[(0,'_fcloseall')] and
         goal['imports']==['__streams','__nfile','_fclose'] and
         [(f['site'],f['frame_method'],f['target'],f['addend']) for f in goal['fields']]==
         [(75,1,2,0),(43,5,3,0),(19,1,1,100)],
         'exact original closeall three native fields in descending order')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two full Borland source/normal link rounds')
    phases=['extract']+[f'round{i}-{x}' for i in (1,2)
                        for x in ('assemble','library','link')]
    need([q['label'] for q in r['phases']]==phases and all(
         q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
         q['log_sha256'] for q in r['phases']),
         'complete native TASM/TLIB/TLINK logs')
    expected_code=bytes(payload(original)[1,i] for i in range(99))
    vectors=[]
    for i,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'entire native OBJ/LIB/EXE/MAP files')
        out={}
        for kind,q in row['outputs'].items():
            blob=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(blob),sha256=sha(blob)),
                 'complete real '+kind+' output identity')
            out[kind]=blob
        need(p.original_scope(out['obj'])==goal and
             bytes(payload(out['obj'])[1,j] for j in range(99))==expected_code and
             literal_fields(out['obj'])==literal_fields(original),
             'all original CLOSEALL CODE, ordered OMF FIXUPPs, public/extern/owner exact')
        actual=dict(prior[i],closeall=out['obj'])
        comparison=compare_members(members,library_members(out['lib']),actual)
        need(comparison==row['library_comparison'] and
             comparison['replaced_members']==sorted(actual) and
             comparison['contextual_members_unchanged']==859,
             '34 actual source modules at original positions, other859 vendor programs untouched')
        need(out['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'whole original Japanese decoded MAINL EXE/MAP byte-for-byte')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'entire original DOS MZ relocation-bearing EXE')
        vectors.append(out)
    need(vectors[0]==vectors[1],
         'two full repeated real native source writer vectors')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                newly_recovered_native_CODE_bytes=99,all_native_CODE_bytes_equal=True,
                original_public='_fcloseall',original_ordered_OMF_fields=3,
                ordered_FIXUPPs_raw_equal=True,
                original_imports=['__streams','__nfile','_fclose'],
                original_CRT_members=893,working_source_members=34,
                unchanged_original_member_programs=859,
                cumulative_original_source_CODE_bytes=20527,
                previous_fopen_native_OMF_order_still_open=True,
                whole_original_Japanese_EXE_equal=True,whole_MAP_raw_equal=True,
                real_Japanese_EXE_bytes=67372,original_MZ_relocations=677,
                repeated_native_rounds=2,
                original_source=p.SOURCE,
                build_report_sha256=sha(raw),prior_33_source_report_sha256=parenthash,
                accepted_ledger_unchanged=True)


if __name__=='__main__':
    receipt=review()
    (ROOT/REVIEW).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
