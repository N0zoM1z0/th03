#!/usr/bin/env python3
"""Validate the complete original signed strtol BCC object and 12-source link."""
import json
from pathlib import Path

import build_th03_mainl_strtol_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import compare_members,library_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-strtol-native-review.json'


def review():
    raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,eleven,parenthash=producer.retained()
    original=producer.ORIGINAL.read_bytes()
    source=(ROOT/producer.SOURCE).read_bytes()
    native_goal=producer.original_scope(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['preceding_eleven_source_build_sha256']==parenthash and
         r['original_sha256']==sha(original) and
         r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['compiler_flags']==producer.BCC_FLAGS,
         'current original signed source, compiler profile and native parent')
    need(native_goal['CODE_bytes']==290 and native_goal['public_offset']==56 and
         len(native_goal['native_literal_fields'])==7 and
         native_goal['imports']==['_errno','__ctype','__scantol'],
         'original signed scanner size,near callbacks,original fields/imports')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two complete actual native source compiler/link rounds')
    phases=['extract']+[f'round{i}-{kind}' for i in (1,2) for kind in
                       ('compile','library','link')]
    need([q['label'] for q in r['phases']]==phases and all(
         q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
         q['log_sha256'] for q in r['phases']),
         'complete actual BCC/TLIB/TLINK native command logs')
    expected=[m.name for m in members if m.name in set(eleven[0])|{'strtol'}]
    vectors=[]
    for i,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'complete BCC OBJ and whole original Japanese EXE/MAP')
        out={}
        for kind,entry in row['outputs'].items():
            data=(ROOT/entry['path']).read_bytes()
            need(entry==dict(path=entry['path'],bytes=len(data),sha256=sha(data)),
                 'original raw output identity '+kind)
            out[kind]=data
        need(producer.original_scope(out['obj'])==native_goal,
             'all290 original BCC CODE bytes,7 literal OMF fields/public/imports equal')
        replacements=dict(eleven[i],strtol=out['obj'])
        compared=compare_members(members,library_members(out['lib']),replacements)
        need(compared==row['library_comparison'] and
             compared['replaced_members']==expected and
             compared['contextual_members_unchanged']==881,
             'twelve original native source member positions and881 untouched programs')
        need(out['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             out['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete fixed Japanese decoded MAINL EXE/MAP raw identical')
        mz=parse_mz(out['exe'])
        need(mz.valid and len(out['exe'])==67372 and len(mz.relocations)==677,
             'all original Japanese real MZ relocation words')
        vectors.append(out)
    need(vectors[0]==vectors[1],
         'entire raw OBJ/LIB/EXE/MAP repeated without sorting or normalization')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                source_CODE_bytes=290,original_CODE_bytes=290,
                complete_native_CODE_equal=True,source_private_near_callbacks=2,
                original_public_offset=56,original_import_order=native_goal['imports'],
                original_literal_FIXUPPs=7,ordered_native_FIXUPPs_equal=True,
                original_library_members=893,real_source_members=12,
                untouched_original_member_programs=881,
                cumulative_source_CODE_bytes=13783,
                Japanese_EXE_file_bytes=67372,MZ_relocations=677,
                complete_Japanese_EXE_raw_equal=True,complete_MAP_raw_equal=True,
                fully_repeated_native_rounds=2,
                original_source=producer.SOURCE,
                current_build_sha256=sha(raw),
                previous_11_source_sha256=parenthash,
                frozen_accepted_publication=True)

if __name__=='__main__':
    x=review()
    (ROOT/REPORT).write_text(json.dumps(x,indent=2)+'\n')
    print(json.dumps(x,indent=2))
