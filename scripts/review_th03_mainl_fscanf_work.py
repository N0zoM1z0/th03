#!/usr/bin/env python3
"""Full native BCC fscanf stack-vararg source and 32-owner Japanese MAINL."""
import json
from pathlib import Path

import build_th03_mainl_fscanf_work as producer
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REVIEW='.analysis/work/mainl-fscanf-native-review.json'


def review():
    raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,prior,parenthash=producer.retained()
    original=producer.ORIGINAL.read_bytes()
    goal=producer.original_scope(original)
    source=(ROOT/producer.SOURCE).read_bytes()
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_thirty_one_source_build_sha256']==parenthash and
         r['original_sha256']==sha(original) and r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['compiler_flags']==producer.BCC_FLAGS,
         'current natural fscanf source, original CRT, pinned build and exact31 parent')
    need(goal['CODE_bytes']==40 and goal['public']==[(0,'_fscanf')] and
         goal['externs']==['__Nfgetc','__Nungetc','__scanner'] and
         [(f['site'],f['frame_method'],f['segment_relative'],f['target']) for f in
          goal['native_literal_fields']]==
         [(31,5,False,3),(27,5,True,1),(23,5,True,2)],
         'real variadic 40-byte wrapper and its three descending TARGET-frame OMF fields')
    need(len(r['rounds'])==2 and [entry['round'] for entry in r['rounds']]==[1,2],
         'two independent full BCC/TLIB/TLINK source builds')
    phases=['extract']+[f'round{i}-{name}' for i in (1,2)
                        for name in ('compile','library','link')]
    need([q['label'] for q in r['phases']]==phases and all(
         q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
         q['log_sha256'] for q in r['phases']),
         'original actual Borland build command logs and phase order')
    expected_code=bytes(payload(original)[1,i] for i in range(40))
    vectors=[]
    for index,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'complete native source OBJ/LIB/EXE/MAP vectors')
        out={}
        for kind,q in row['outputs'].items():
            blob=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(blob),sha256=sha(blob)),
                 'real complete native '+kind+' original file')
            out[kind]=blob
        need(producer.original_scope(out['obj'])==goal and
             bytes(payload(out['obj'])[1,i] for i in range(40))==expected_code and
             literal_fields(out['obj'])==literal_fields(original),
             'complete 40 native BCC bytes, all three literal ordered FIXUPPs')
        sources=dict(prior[index],fscanf=out['obj'])
        cmp=compare_members(members,library_members(out['lib']),sources)
        need(cmp==row['library_comparison'] and
             cmp['replaced_members']==sorted(sources) and
             cmp['contextual_members_unchanged']==861,
             '32 original source CRT positions, all 861 other members intact')
        need(out['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete original decoded Japanese MAINL EXE and native MAP raw equal')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'whole original DOS MZ EXE with full relocation vector')
        vectors.append(out)
    need(vectors[0]==vectors[1],
         'all raw original BCC/TLIB/TLINK source outputs reproducible in two rounds')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_fscanf_CODE_bytes=40,source_fscanf_CODE_bytes=40,
                complete_native_CODE_raw_equal=True,
                original_near_callback_imports=['__Nfgetc','__Nungetc','__scanner'],
                original_literal_FIXUPPs=3,all_ordered_fields_raw_equal=True,
                true_far_stack_varargs=True,
                original_CRT_member_count=893,native_source_members=32,
                unchanged_original_member_programs=861,
                cumulative_source_CODE_bytes=19872,
                original_decoded_Japanese_EXE_bytes=67372,
                MZ_relocations=677,full_Japanese_EXE_raw_equal=True,
                whole_original_MAP_raw_equal=True,native_repeated_rounds=2,
                original_source_path=producer.SOURCE,
                build_report_sha256=sha(raw),preceding_native_source_report_sha256=parenthash,
                accepted_publication_unchanged=True)


if __name__=='__main__':
    x=review()
    (ROOT/REVIEW).write_text(json.dumps(x,indent=2)+'\n')
    print(json.dumps(x,indent=2))
