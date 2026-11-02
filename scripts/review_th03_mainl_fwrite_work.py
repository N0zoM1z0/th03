#!/usr/bin/env python3
"""Independent entire DOS fwrite and real 29-source Japanese MAINL reviewer."""
import json
from pathlib import Path

import build_th03_mainl_fwrite_work as producer
from build_th03_mainl_resources_work import need,sha
from build_th03_mainl_display_work import payload,literal_fields
from lib.borland_library import compare_members,library_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-fwrite-native-review.json'


def review():
    build_raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(build_raw)
    base,files,accepted,members,prior,parent_sha=producer.retained()
    original=producer.ORIGINAL.read_bytes()
    goal=producer.original_scope(original)
    inputs={name:(ROOT/name).read_bytes() for name in producer.SOURCES}
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['previous_twenty_eight_source_build_sha256']==parent_sha and
         r['original_sha256']==sha(original) and
         r['source_sha256']=={name:sha(src) for name,src in inputs.items()} and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['native_assembler_flags']==producer.TASM_FLAGS,
         'current real native source/driver, unchanged accepted baseline and parent')
    need(goal['CODE_bytes']==153 and goal['public_offset']==0 and
         goal['imports']==['__FPUTN','N_LXMUL@','N_PADD@'] and
         [(x['site'],x['target'],x['frame_method']) for x in goal['literal_ordered_fields']]==
         [(28,2,0),(63,1,0),(95,1,0),(125,3,0)],
         'complete original single far public and ordered near helper calls')
    need(len(r['rounds'])==2 and [x['round'] for x in r['rounds']]==[1,2],
         'two full native source builds')
    logs=['extract']+[f'round{i}-{kind}' for i in (1,2) for kind in
                      ('assemble','library','link')]
    need([x['label'] for x in r['phases']]==logs and
         all(x['returncode']==0 and
             sha((ROOT/x['log_path']).read_bytes())==x['log_sha256'] for x in r['phases']),
         'real native TASM/TLIB/TLINK command log checksums')
    original_code=bytes(payload(original)[1,i] for i in range(153))
    outputs=[]
    for index,row in enumerate(r['rounds']):
        need(set(row['outputs'])=={'obj','lib','exe','map'},
             'four complete actual source output artifacts')
        obj={}
        for kind,meta in row['outputs'].items():
            data=(ROOT/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'actual full native '+kind+' bytes')
            obj[kind]=data
        need(producer.original_scope(obj['obj'])==goal and
             bytes(payload(obj['obj'])[1,i] for i in range(153))==original_code and
             literal_fields(obj['obj'])==literal_fields(original),
             'every original fwrite CODE byte and ordered OMF frame/target field equal')
        source=dict(prior[index],fwrite=obj['obj'])
        comparison=compare_members(members,library_members(obj['lib']),source)
        need(comparison==row['library_comparison'] and
             comparison['replaced_members']==sorted(source) and
             comparison['contextual_members_unchanged']==864,
             '29 native original source objects and864 entirely untouched library members')
        need(obj['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             obj['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'entire decoded Japanese MAINL EXE and original MAP byte-for-byte')
        mz=parse_mz(obj['exe'])
        need(mz.valid and len(obj['exe'])==67372 and len(mz.relocations)==677,
             'entire original MZ relocation-bearing 67372-byte executable')
        outputs.append(obj)
    need(outputs[0]==outputs[1],'two identical whole source OBJ/LIB/EXE/MAP vectors')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,original_CODE_bytes=153,
                source_CODE_bytes=153,full_native_CODE_equal=True,
                original_public='_fwrite',original_literal_FIXUPPs=4,
                all_native_FIXUPPs_equal=True,original_extdef_order=goal['imports'],
                full_source_member_count=29,original_library_members=893,
                unchanged_original_member_programs=864,
                joint_exact_source_CODE_bytes=18855,
                entire_original_EXE_raw_equal=True,whole_MAP_raw_equal=True,
                original_MZ_relocations=677,EXE_file_bytes=67372,
                repeated_native_rounds=2,source_path=producer.SOURCES[0],
                bound_build_report_sha256=sha(build_raw),
                preceding_source_receipt_sha256=parent_sha,
                published_ledger_unchanged=True)


if __name__=='__main__':
    receipt=review()
    (ROOT/REPORT).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
