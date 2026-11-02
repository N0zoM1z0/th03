#!/usr/bin/env python3
"""True native DOS tempnam 395 CODE/6 DATA and product-exact 53-source CRT.

The one near __MKNAME fixup is BCC TARGET-framed and TASM CODE-framed.
All other original OMF fields, CODE, DATA and full linked EXE/MAP match.
"""
import json
from pathlib import Path

import build_th03_mainl_tempnam_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-tempnam-native-review.json'


def review():
    build_raw=(ROOT/p.REPORT).read_bytes()
    r=json.loads(build_raw)
    base,files,accepted,members,parents,parenthash=p.retained()
    original=p.ORIGINAL.read_bytes()
    goal=p.original_scope(original)
    source=(ROOT/p.SOURCE).read_bytes()
    original_fix=literal_fields(original)
    original_code,original_data=p.native_parts(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['native_tempnam_near_MKNAME_TARGET_frame_open'] and
         r['prior_strftime_near_UTOA_TARGET_frame_open'] and
         r['prior_timecvt_near_frame_open'] and
         r['prior_fopen_OMF_order_open'] and r['prior_fclose_near_frame_open'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_fifty_two_source_build_sha256']==parenthash and
         r['original_sha256']==sha(original) and r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         r['native_assembler_flags']==p.TASM_FLAGS,
         'exact current source, original accepted library and parent52')
    need(goal['CODE_bytes']==395 and goal['DATA_bytes']==6 and
         original_data==bytes.fromhex("544d50000000") and goal['public']==[(0,"_tempnam")] and
         goal['imports']==p.EXTERNS and len(original_fix)==14 and
         [q['site'] for q in original_fix]==p.ORIGINAL_SITES and
         original_fix[2]['site']==309 and original_fix[2]['frame_method']==5,
         'complete original 395 CODE/6 DATA and14 descending native fields')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two complete native compiler and linker rounds')
    phases=['extract']+[f'round{i}-{name}' for i in (1,2)
                        for name in ('assemble','library','link')]
    need([q['label'] for q in r['phases']]==phases and
         all(q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
             q['log_sha256'] for q in r['phases']),
         'authentic TASM/TLIB/TLINK command and phase log identities')
    vectors=[]
    for i,row in enumerate(r['rounds']):
        out={}
        need(set(row['outputs'])=={'obj','lib','exe','map'},'full native outputs')
        for kind,q in row['outputs'].items():
            b=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(b),sha256=sha(b)),
                 'complete native '+kind+' artifact')
            out[kind]=b
        native_fix=literal_fields(out['obj'])
        need(p.original_scope(out['obj'])==goal and
             p.native_parts(out['obj'])==(original_code,original_data) and
             len(native_fix)==14 and
             sum(a!=b for a,b in zip(original_fix,native_fix))==1 and
             all(a==b for a,b in zip(original_fix,native_fix)
                 if a['site']!=309) and
             original_fix[2]['target']==native_fix[2]['target']==1 and
             original_fix[2]['target_method']==native_fix[2]['target_method']==2 and
             original_fix[2]['frame_method']==5 and
             native_fix[2]['frame_method']==0,
             'original complete CODE/DATA, 13 literal original fixups, 1 frame gap')
        sources=dict(parents[i],tempnam=out['obj'])
        cmp=compare_members(members,library_members(out['lib']),sources)
        need(cmp==row['library_comparison'] and
             cmp['replaced_members']==sorted(sources) and
             cmp['contextual_members_unchanged']==840,
             '53 real CRT source programs and840 others wholly unchanged')
        need(out['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'entire original Japanese decoded EXE and MAP raw-equal')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'original entire MZ size and677 actual relocation entries')
        vectors.append(out)
    need(vectors[0]==vectors[1],'two identical full native OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                original_CODE_bytes=395,source_CODE_bytes=395,
                original_initialized_DATA_bytes=6,source_DATA_bytes=6,
                native_CODE_raw_equal=True,native_DATA_raw_equal=True,
                ordered_original_FIXUPP_fields=14,logical_fields_equal=True,
                other_13_literal_fields_equal=True,original_native_OMF_equal=False,
                only_native_frame_gap_at=309,original_near_frame=5,source_near_frame=0,
                original_893_member_CRT=893,simultaneous_source_members=53,
                untouched_original_member_programs=840,
                cumulative_original_source_CODE_bytes=27366,
                whole_Japanese_EXE_raw_equal=True,whole_MAP_raw_equal=True,
                original_EXE_bytes=67372,original_MZ_relocations=677,
                native_repeated_rounds=2,
                prior_strftime_OMF_gap=True,prior_timecvt_OMF_gap=True,
                prior_fopen_OMF_gap=True,prior_fclose_OMF_gap=True,
                source_path=p.SOURCE,build_report_sha256=sha(build_raw),
                parent_52_receipt_sha256=parenthash,accepted_ledger_unchanged=True)


if __name__=='__main__':
    q=review()
    (ROOT/REPORT).write_text(json.dumps(q,indent=2)+'\n')
    print(json.dumps(q,indent=2))
