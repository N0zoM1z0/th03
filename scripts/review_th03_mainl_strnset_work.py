#!/usr/bin/env python3
"""Recheck complete native Borland strnset and 16 genuine source CRT members."""
import json
from pathlib import Path

import build_th03_mainl_strnset_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import compare_members,library_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-strnset-native-review.json'


def review():
    raw=(ROOT/producer.REPORT).read_bytes()
    receipt=json.loads(raw)
    base,files,accepted,members,existing,parenthash=producer.retained()
    old=producer.ORIGINAL.read_bytes()
    new_source=(ROOT/producer.SOURCE).read_bytes()
    original=producer.original_scope(old)
    need(receipt['complete'] and not receipt['source_acceptance'] and
         receipt['added_accepted_bytes']==0 and not receipt['original_cold_rebuilt'] and
         receipt['accepted_baseline']==base and
         receipt['accepted_library_sha256']==sha(accepted) and
         receipt['previous_fifteen_source_build_sha256']==parenthash and
         receipt['original_sha256']==sha(old) and
         receipt['source_sha256']==sha(new_source) and
         receipt['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         receipt['compiler_flags']==producer.BCC_FLAGS,
         'current original native BCC source, full parent library and compiler driver')
    need(original['CODE_bytes']==58 and original['externs']==['_strlen','_setmem'] and
         original['pub']==[(0,'_strnset')] and
         [(f['site'],f['target'],f['location_type']) for f in original['native_literal_fields']]==
         [(41,2,3),(12,1,3)],
         'complete native strnset object with two ordered far calls')
    need(len(receipt['rounds'])==2 and
         [q['round'] for q in receipt['rounds']]==[1,2] and
         [q['label'] for q in receipt['phases']]==
         ['extract']+[f'round{n}-{phase}' for n in (1,2)
                      for phase in ('compile','library','link')] and
         all(q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
             q['log_sha256'] for q in receipt['phases']),
         'two complete BCC/TLIB/TLINK source writer rounds and actual phase logs')
    expected=[m.name for m in members if m.name in set(existing[0])|{'strnset'}]
    vectors=[]
    for idx,row in enumerate(receipt['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'complete native OBJ/LIB/EXE/MAP outputs')
        outputs={}
        for kind,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'complete current generated native '+kind)
            outputs[kind]=data
        need(producer.original_scope(outputs['obj'])==original,
             'all 58 CODE bytes, public, import and ordered literal OMF fields exact')
        all_source=dict(existing[idx],strnset=outputs['obj'])
        compared=compare_members(members,library_members(outputs['lib']),all_source)
        need(compared==row['library_comparison'] and
             compared['replaced_members']==expected and
             compared['contextual_members_unchanged']==877,
             '16 natural source CRT members and 877 original untouched member programs')
        need(outputs['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete original Japanese decoded MAINL and native MAP raw exact')
        mz=parse_mz(outputs['exe'])
        need(mz.valid and len(outputs['exe'])==67372 and len(mz.relocations)==677,
             'all original MZ relocation entries and source-linked file size')
        vectors.append(outputs)
    need(vectors[0]==vectors[1],
         'two independent full native raw OBJ/LIB/EXE/MAP vectors match')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                original_and_native_CODE_bytes=[58,58],
                original_public='_strnset',ordered_native_FIXUPPs=2,
                literal_fields_raw_equal=True,original_exports=['_strlen','_setmem'],
                original_library_members=893,reconstructed_source_members=16,
                unchanged_member_program_records=877,
                cumulative_naturally_compiled_CODE_bytes=14114,
                complete_Japanese_EXE_raw_equal=True,whole_MAP_raw_equal=True,
                original_MZ_relocations=677,source_linked_EXE_bytes=67372,
                native_repeated_rounds=2,
                source_path=producer.SOURCE,
                retained_build_report_sha256=sha(raw),
                previous_fifteen_source_receipt_sha256=parenthash,
                accepted_publication_unchanged=True)

if __name__=='__main__':
    result=review()
    (ROOT/REPORT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
