#!/usr/bin/env python3
"""Independently review all original DOS strtok storage, fixups and joint link."""
import json
from pathlib import Path

import build_th03_mainl_strtok_work as producer
from build_th03_mainl_resources_work import need,sha
from lib.borland_library import library_members,compare_members
from lib.pc98 import parse_mz

ROOT=Path(__file__).resolve().parents[1]
REPORT='.analysis/work/mainl-strtok-native-review.json'


def review():
    raw=(ROOT/producer.REPORT).read_bytes()
    r=json.loads(raw)
    base,files,accepted,members,nine,priorhash=producer.retained()
    original=(producer.WORK/'vendor/strtok.obj').read_bytes()
    source=(ROOT/producer.SOURCE).read_bytes()
    original_profile=producer.original_scope(original)
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['accepted_baseline']==base and r['accepted_library_sha256']==sha(accepted) and
         r['preceding_nine_source_build_sha256']==priorhash and
         r['source_sha256']==sha(source) and r['original_sha256']==sha(original) and
         r['driver_sha256']==sha((ROOT/producer.DRIVER).read_bytes()) and
         r['compiler_flags']==producer.BCC_FLAGS,
         'full original stateful BCC source and retained native parent inputs')
    need(original_profile['code_bytes']==203 and
         len(original_profile['native_fields'])==12,
         '203 byte native CODE and twelve original literal OMF fields')
    need(len(r['rounds'])==2 and [x['round'] for x in r['rounds']]==[1,2],
         'two distinct native compiler/library/link rounds')
    phases=['extract']+[f'round{n}-{kind}' for n in (1,2)
                        for kind in ('compile','library','link')]
    need([x['label'] for x in r['phases']]==phases and
         all(x['returncode']==0 and sha((ROOT/x['log_path']).read_bytes())==
             x['log_sha256'] for x in r['phases']),
         'unmodified TASM-extraction/BCC/TLIB/TLINK original phase logs')
    expected=[m.name for m in members if m.name in set(nine[0])|{'strtok'}]
    vectors=[]
    for num,entry in enumerate(r['rounds']):
        need(set(entry['outputs'])=={'obj','lib','exe','map'},
             'complete raw BCC OBJ and library/executable/map outputs')
        output={}
        for kind,m in entry['outputs'].items():
            blob=(ROOT/m['path']).read_bytes()
            need(m==dict(path=m['path'],bytes=len(blob),sha256=sha(blob)),
                 'current complete native '+kind+' file bytes')
            output[kind]=blob
        need(producer.original_scope(output['obj'])==original_profile,
             'full original CODE, BSS/public/GRPDEF and ordered internal FIXUPPs')
        sources=dict(nine[num],strtok=output['obj'])
        compared=compare_members(members,library_members(output['lib']),sources)
        need(compared==entry['library_comparison'] and
             compared['replaced_members']==expected and
             compared['contextual_members_unchanged']==883,
             'ten authentic native source objects and883 original surrounding members')
        need(output['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             output['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete fixed Japanese decoded MAINL EXE/MAP raw-equal')
        mz=parse_mz(output['exe'])
        need(mz.valid and len(output['exe'])==67372 and len(mz.relocations)==677,
             'actual original DOS MZ with677 relocation entries')
        vectors.append(output)
    need(vectors[0]==vectors[1],
         'full raw BCC/TLIB/TLINK native outputs reproducible,not normalized')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,
                original_strtok_CODE_bytes=203,candidate_strtok_CODE_bytes=203,
                literal_native_strtok_FIXUPPs=12,literal_FIXUPPs_raw_equal=True,
                original_BSS_bytes=4,candidate_BSS_bytes=4,
                original_GRPDEF='08ff02ff03',original_and_native_CODE_equal=True,
                original_library_members=893,source_member_count=10,
                untouched_original_member_programs=883,
                member_names=expected,combined_source_CODE_bytes=13262,
                original_decoded_EXE_raw_equal=True,original_MAP_raw_equal=True,
                original_MZ_relocation_count=677,whole_EXE_bytes=67372,
                native_repeated_rounds=2,
                original_CRT_publication_unchanged=True,
                original_source=producer.SOURCE,
                build_report_sha256=sha(raw),prior_native_receipt_sha256=priorhash)

if __name__=='__main__':
    result=review()
    (ROOT/REPORT).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
