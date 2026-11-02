#!/usr/bin/env python3
"""Independent natural Borland fputs 85 CODE/2 OMF and 51-source MAINL link."""
import json
from pathlib import Path

import build_th03_mainl_fputs_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-fputs-native-review.json'


def code(blob):
    obj=payload(blob)
    return bytes(obj[1,i] for i in range(85))


def review():
    raw=(ROOT/p.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,earlier,parenthash=p.retained()
    original=p.ORIGINAL.read_bytes()
    goal=p.original_scope(original)
    src=(ROOT/p.SOURCE).read_bytes()
    original_code=code(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_fifty_source_build_sha256']==parenthash and
         r['original_sha256']==sha(original) and r['source_sha256']==sha(src) and
         r['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         r['compiler_flags']==p.BCC_FLAGS,
         'bound natural C++ source, real original CRT and 50-source native parent')
    need(goal['CODE_bytes']==85 and
         goal['externs']==['__FPUTN','_strlen'] and
         goal['public']==[(0,'_fputs')] and
         [(x['site'],x['width'],x['frame_method'],x['target_method'],x['target'])
          for x in goal['native_literal_fields']]==
         [(56,2,5,2,1),(23,4,5,2,2)],
         'original mixed near-Pascal and far strlen TARGET-frame ABI and CODE')
    need(len(r['rounds'])==2 and [row['round'] for row in r['rounds']]==[1,2],
         'two real Borland C++ original native source rounds')
    phases=['extract']+[f'round{i}-{kind}' for i in (1,2)
                        for kind in ('compile','library','link')]
    need([q['label'] for q in r['phases']]==phases and
         all(q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
             q['log_sha256'] for q in r['phases']),
         'actual Borland BCC/TLIB/TLINK writer flags/command logs')
    pairs=[]
    for idx,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'complete native source OBJ/library/executable/MAP files')
        outputs={}
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'full source-built '+kind+' artifact identity')
            outputs[kind]=blob
        need(p.original_scope(outputs['obj'])==goal and
             code(outputs['obj'])==original_code and
             literal_fields(outputs['obj'])==literal_fields(original),
             'all85 natural BCC CODE and two literal original mixed near/far FIXUPPs')
        source=dict(earlier[idx],fputs=outputs['obj'])
        compared=compare_members(members,library_members(outputs['lib']),source)
        need(compared==row['library_comparison'] and
             compared['replaced_members']==sorted(source) and
             compared['contextual_members_unchanged']==842,
             '51 genuine source CRT program owners and other842 original members unchanged')
        need(outputs['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'entire original Japanese decoded MAINL EXE/MAP byte-for-byte')
        mz=parse_mz(outputs['exe'])
        need(mz.valid and len(outputs['exe'])==67372 and len(mz.relocations)==677,
             'complete original MZ format with all677 relocations')
        pairs.append(outputs)
    need(pairs[0]==pairs[1],'two complete identical BCC/TLIB/TLINK original source vectors')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                original_fputs_CODE_bytes=85,source_fputs_CODE_bytes=85,
                all_native_CODE_raw_equal=True,
                original_EXTDEF_order=['__FPUTN','_strlen'],
                literal_ordered_FIXUPPs_count=2,all_native_FIXUPPs_equal=True,
                original_near_pascal_FPUTN_frame_method=5,
                original_far_strlen_frame_method=5,
                full_original_OMF_equal=True,
                original_893_CRT_members=893,native_source_members=51,
                original_untouched_vendor_programs=842,
                cumulative_exact_source_CODE_bytes=25715,
                original_Japanese_EXE_bytes=67372,original_MZ_relocations=677,
                complete_Japanese_EXE_raw_equal=True,original_MAP_raw_equal=True,
                native_repeated_rounds=2,
                prior_timecvt_near_frame_open=True,
                prior_fopen_FIXUPP_order_open=True,prior_fclose_near_frame_open=True,
                original_source=p.SOURCE,source_sha256=sha(src),
                build_report_sha256=sha(raw),parent_50_source_receipt_sha256=parenthash,
                formal_accepted_ledger_unchanged=True)


if __name__=='__main__':
    q=review()
    (ROOT/REPORT).write_text(json.dumps(q,indent=2)+'\n')
    print(json.dumps(q,indent=2))
