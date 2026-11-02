#!/usr/bin/env python3
"""Full native DOS fclose CODE and 35-source product-link, near frame OPEN."""
import json
from pathlib import Path

import build_th03_mainl_fclose_work as p
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REVIEW='.analysis/work/mainl-fclose-native-review.json'


def review():
    raw=(ROOT/p.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,prior,parenthash=p.retained()
    orig=p.ORIGINAL.read_bytes()
    goal=p.original_scope(orig)
    source=(ROOT/p.SOURCE).read_bytes()
    old_fields=literal_fields(orig)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['partial_parent_fopen_OMF_order_open'] is True and
         r['native_fclose_MKNAME_TARGET_frame_open'] is True and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_thirty_four_source_build_sha256']==parenthash and
         r['original_sha256']==sha(orig) and
         r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/p.DRIVER).read_bytes()) and
         r['native_assembler_flags']==p.TASM_FLAGS,
         'genuine original fclose source/driver and 34-source product-only parent')
    need(goal['CODE_bytes']==192 and goal['publics']==[(0,'_fclose')] and
         goal['imports']==['_fflush','_unlink','_free','_close','__MKNAME'] and
         [f['site'] for f in old_fields]==[168,163,112,89,60] and
         all(f['frame_method']==5 for f in old_fields),
         'original complete far fclose code, five fields and native TARGET frames')
    need(len(r['rounds'])==2 and [t['round'] for t in r['rounds']]==[1,2],
         'two independent actual Borland writer rounds')
    labels=['extract']+[f'round{i}-{phase}' for i in (1,2)
                        for phase in ('assemble','library','link')]
    need([x['label'] for x in r['phases']]==labels and all(
         x['returncode']==0 and sha((ROOT/x['log_path']).read_bytes())==
         x['log_sha256'] for x in r['phases']),
         'genuine complete TASM/TLIB/TLINK command logs')
    code=bytes(payload(orig)[1,i] for i in range(192))
    vectors=[]
    for i,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'all complete genuine native source output vectors')
        out={}
        for kind,meta in row['outputs'].items():
            blob=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(blob),sha256=sha(blob)),
                 'complete original source '+kind+' file identity')
            out[kind]=blob
        fields=literal_fields(out['obj'])
        need(p.original_scope(out['obj'])==goal and
             bytes(payload(out['obj'])[1,j] for j in range(192))==code and
             len(fields)==5 and
             all(old==new for n,(old,new) in enumerate(zip(old_fields,fields)) if n!=1) and
             old_fields[1]['frame_method']==5 and fields[1]['frame_method']==0 and
             fields[1]['site']==old_fields[1]['site']==163 and
             fields[1]['target']==old_fields[1]['target']==5,
             'all192 original CODE, four exact fields, one original MKNAME frame gap')
        sources=dict(prior[i],fclose=out['obj'])
        comparison=compare_members(members,library_members(out['lib']),sources)
        need(comparison==row['library_comparison'] and
             comparison['replaced_members']==sorted(sources) and
             comparison['contextual_members_unchanged']==858,
             '35 original member positions, other858 vendor programs remain complete')
        need(out['exe']==(p.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(p.WORK/'obj/th03/mainl.map').read_bytes(),
             'whole fixed original Japanese EXE/MAP byte-for-byte')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'original relocation-bearing 67372-byte DOS Japanese image')
        vectors.append(out)
    need(vectors[0]==vectors[1],'two complete identical raw OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,new_fclose_CODE_bytes=192,
                all_native_CODE_bytes_equal=True,original_public='_fclose',
                original_imports=goal['imports'],original_field_sites=[168,163,112,89,60],
                literal_logical_fields_equal=True,original_literal_fixup_count=5,
                native_original_OMF_equal=False,
                original_MKNAME_frame_method=5,source_MKNAME_frame_method=0,
                parent_fopen_original_OMF_order_still_open=True,
                original_CRT_members=893,source_modules_in_working_library=35,
                untouched_original_CRT_programs=858,
                cumulative_source_CODE_bytes=20719,
                original_EXE_bytes=67372,original_MZ_relocations=677,
                whole_decoded_Japanese_EXE_raw_equal=True,
                whole_original_MAP_raw_equal=True,
                independent_native_rounds=2,
                source_path=p.SOURCE,build_report_sha256=sha(raw),
                parent_34_source_receipt_sha256=parenthash,
                published_accepted_ledger_unchanged=True)


if __name__=='__main__':
    rec=review()
    (ROOT/REVIEW).write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec,indent=2))
