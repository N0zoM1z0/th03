#!/usr/bin/env python3
"""Recheck exact original strstr plus xx/seven CRT native source link."""
import json
from pathlib import Path

import build_th03_mainl_strstr_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-strstr-native-review.json'


def review():
    raw=(ROOT/producer.REPORT).read_bytes()
    record=json.loads(raw)
    baseline,files,accepted,members,objects,priorhash=producer.retained()
    original=producer.ORIGINAL.read_bytes()
    source=(ROOT/producer.SOURCE).read_bytes()
    code=producer.original_scope(original)
    need(record['complete'] and not record['source_acceptance'] and
         record['added_accepted_bytes']==0 and not record['original_cold_rebuilt'] and
         record['accepted_baseline']==baseline and
         record['accepted_library_sha256']==sha(accepted) and
         record['preceding_eight_source_receipt_sha256']==priorhash and
         record['source_sha256']==sha(source) and
         record['original_sha256']==sha(original) and
         record['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()),
         'bound original native source,used library and current driver')
    need(len(record['rounds'])==2 and [r['round'] for r in record['rounds']]==[1,2],
         'two full source rounds')
    labels=['extract']+[f'round{n}-{kind}' for n in (1,2)
                        for kind in ('assemble','library','link')]
    need([q['label'] for q in record['phases']]==labels and all(
         q['returncode']==0 and
         sha((ROOT/q['log_path']).read_bytes())==q['log_sha256']
         for q in record['phases']), 'complete actual TASM/TLIB/TLINK logs')
    expected=[m.name for m in members if m.name in set(objects[0])|{'strstr'}]
    all_vectors=[]
    for i,row in enumerate(record['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'whole source object and link vectors')
        outputs={}
        for kind,q in row['outputs'].items():
            data=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(data),sha256=sha(data)),
                 'complete raw native output '+kind)
            outputs[kind]=data
        need(producer.original_scope(outputs['obj'])==code,
             'all108 native substring opcodes/ownership/publics identical')
        replaced=dict(objects[i],strstr=outputs['obj'])
        compared=compare_members(members,library_members(outputs['lib']),replaced)
        need(row['library_comparison']==compared and
             compared['replaced_members']==expected and
             compared['contextual_members_unchanged']==884,
             '9 native source member originals retained,884 other programs untouched')
        target=(producer.WORK/'bin/th03/mainl.target.exe').read_bytes()
        original_map=(producer.WORK/'obj/th03/mainl.map').read_bytes()
        need(outputs['exe']==target and outputs['map']==original_map,
             'exact complete decoded Japanese MAINL MZ EXE and MAP')
        mz=parse_mz(outputs['exe'])
        need(mz.valid and len(outputs['exe'])==67372 and len(mz.relocations)==677,
             'whole actual Japanese MZ with677 original relocations')
        all_vectors.append(outputs)
    need(all_vectors[0]==all_vectors[1],
         'two full identical raw native source OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,native_source_recovered='strstr',
                source_CODE_bytes=108,original_and_candidate_CODE_equal=True,
                original_and_candidate_literal_fields_equal=True,
                total_source_CODE_bytes=13059,original_library_members=893,
                nine_source_members=expected,unchanged_member_programs=884,
                exact_whole_Japanese_EXE=True,exact_whole_Japanese_MAP=True,
                complete_EXE_bytes=67372,MZ_relocations=677,native_rounds=2,
                original_source_path=producer.SOURCE,
                original_source_sha256=sha(source),
                build_report_sha256=sha(raw),parent_receipt_sha256=priorhash,
                published_ledger_unchanged=True)

if __name__=='__main__':
    receipt=review()
    (ROOT/REPORT).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
