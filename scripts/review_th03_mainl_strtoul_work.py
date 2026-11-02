#!/usr/bin/env python3
"""Complete native Borland strtoul scanner/helpers and eleven-source linker."""
import json
from pathlib import Path

import build_th03_mainl_strtoul_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-strtoul-native-review.json'


def review():
    raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,ten,priorhash=producer.retained()
    original=producer.ORIGINAL.read_bytes()
    source=(ROOT/producer.SOURCE).read_bytes()
    goal=producer.original_scope(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['preceding_ten_source_build_sha256']==priorhash and
         r['source_sha256']==sha(source) and
         r['original_sha256']==sha(original) and
         r['compiler_flags']==producer.BCC_FLAGS and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()),
         'current actual original native code,accepted CRT and source scope')
    need(goal['CODE_bytes']==231 and goal['public_offset']==56 and
         len(goal['native_literal_fields'])==6 and
         goal['imports']==['_errno','__ctype','__scantol'],
         'complete original two-helper/far-entry scanner interface and fields')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two native object and whole product rounds')
    labels=['extract']+[f'round{n}-{kind}' for n in (1,2) for kind in
                       ('compile','library','link')]
    need([q['label'] for q in r['phases']]==labels and all(
         q['returncode']==0 and sha((ROOT/q['log_path']).read_bytes())==
         q['log_sha256'] for q in r['phases']),
         'actual BCC/TLIB/TLINK command log contents')
    expected=[m.name for m in members if m.name in set(ten[0])|{'strtoul'}]
    vectors=[]
    for index,entry in enumerate(r['rounds']):
        need(set(entry['outputs'])=={'obj','lib','exe','map'},
             'complete source OBJ and native library/exe/map artifacts')
        output={}
        for name,q in entry['outputs'].items():
            b=(ROOT/q['path']).read_bytes()
            need(q==dict(path=q['path'],bytes=len(b),sha256=sha(b)),
                 'unmodified full native source output '+name)
            output[name]=b
        need(producer.original_scope(output['obj'])==goal,
             'all231 native CODE bytes,original imports/public and6 literal fields equal')
        src=dict(ten[index],strtoul=output['obj'])
        comparison=compare_members(members,library_members(output['lib']),src)
        need(comparison==entry['library_comparison'] and
             comparison['replaced_members']==expected and
             comparison['contextual_members_unchanged']==882,
             'eleven real source objects at original slots,882 untouched programs')
        need(output['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete fixed Japanese decoded MAINL exe/map raw equality')
        mz=parse_mz(output['exe'])
        need(mz.valid and len(output['exe'])==67372 and len(mz.relocations)==677,
             'all677 original MZ relocations and original full file')
        vectors.append(output)
    need(vectors[0]==vectors[1],'two complete identical native OBJ/LIB/EXE/MAP output vectors')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                CODE_original_bytes=231,CODE_source_bytes=231,
                all231_CODE_bytes_equal=True,private_near_helpers=2,
                public_strtoul_offset=56,original_and_native_imports=goal['imports'],
                ordered_native_fields=6,literal_fields_exact=True,
                native_DATA_bytes=0,native_BSS_bytes=0,
                original_library_members=893,source_members=11,
                untouched_original_member_programs=882,
                exact_joint_source_CODE_bytes=13493,
                full_Japanese_EXE_bytes=67372,whole_EXE_raw_equal=True,
                whole_MAP_raw_equal=True,MZ_relocations=677,
                native_rounds=2,original_source=producer.SOURCE,
                build_report_sha256=sha(raw),prior_ten_source_receipt_sha256=priorhash,
                published_accepted_source_ledger_unchanged=True)

if __name__=='__main__':
    x=review()
    (ROOT/REPORT).write_text(json.dumps(x,indent=2)+'\n')
    print(json.dumps(x,indent=2))
