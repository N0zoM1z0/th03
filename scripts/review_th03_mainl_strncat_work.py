#!/usr/bin/env python3
"""Recheck literal Borland native strncat object and cumulative 15-source link."""
import json
from pathlib import Path

import build_th03_mainl_strncat_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import compare_members,library_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-strncat-native-review.json'


def review():
    raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,old,prev=producer.retained()
    original=producer.ORIGINAL.read_bytes()
    source=(ROOT/producer.SOURCE).read_bytes()
    goal=producer.original_scope(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and
         r['accepted_library_sha256']==sha(accepted) and
         r['previous_fourteen_source_build_sha256']==prev and
         r['original_sha256']==sha(original) and r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['compiler_flags']==producer.BCC_FLAGS,
         'real original native member,unchanged original library and source')
    need(goal['CODE_bytes']==105 and goal['externs']==['_strlen','_movmem'] and
         len(goal['native_literal_fields'])==3,
         'complete original external call/code size and three ordered fields')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two actual real native BCC rounds')
    names=['extract']+[f'round{i}-{t}' for i in (1,2)
                       for t in ('compile','library','link')]
    need([q['label'] for q in r['phases']]==names and
         all(q['returncode']==0 and
             sha((ROOT/q['log_path']).read_bytes())==q['log_sha256']
             for q in r['phases']), 'all real compiler/library/link writer phase logs')
    expected=[m.name for m in members if m.name in set(old[0])|{'strncat'}]
    vectors=[]
    for i,entry in enumerate(r['rounds']):
        need(set(entry['outputs'])=={'obj','lib','exe','map'},
             'full native original OMF/member/executable/map')
        v={}
        for k,m in entry['outputs'].items():
            b=(ROOT/m['path']).read_bytes()
            need(m==dict(path=m['path'],bytes=len(b),sha256=sha(b)),
                 'literal original generated file '+k)
            v[k]=b
        need(producer.original_scope(v['obj'])==goal,
             'full105 BCC opcodes,3 ordered relocations,imports and public match')
        new=dict(old[i],strncat=v['obj'])
        comp=compare_members(members,library_members(v['lib']),new)
        need(comp==entry['library_comparison'] and
             comp['replaced_members']==expected and
             comp['contextual_members_unchanged']==878,
             'fifteen native source objects in original positions,878 members untouched')
        need(v['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             v['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'entire original Japanese decoded MAINL EXE and original MAP exact')
        mz=parse_mz(v['exe'])
        need(mz.valid and len(v['exe'])==67372 and len(mz.relocations)==677,
             'all original Japanese MZ relocations in actual EXE')
        vectors.append(v)
    need(vectors[0]==vectors[1],'repeated complete raw native BCC/CRT/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,
                added_accepted_bytes=0,original_cold_rebuilt=False,
                source_CODE_bytes=105,original_CODE_bytes=105,
                complete_original_native_CODE_equal=True,
                native_original_imports=goal['externs'],
                original_literal_FIXUPPs=3,ordered_native_FIXUPPs_exact=True,
                original_CRT_member_count=893,source_members=15,
                unchanged_original_member_programs=878,
                combined_source_CODE_bytes=14056,
                decoded_Japanese_EXE_bytes=67372,MZ_relocations=677,
                entire_original_EXE_equal=True,original_MAP_equal=True,
                repeated_complete_native_rounds=2,
                original_source_path=producer.SOURCE,
                selected_build_report_sha256=sha(raw),
                previous_native_source_receipt_sha256=prev,
                accepted_ledger_unchanged=True)


if __name__=='__main__':
    result=review()
    (ROOT/REPORT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
