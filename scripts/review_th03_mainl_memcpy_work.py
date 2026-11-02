#!/usr/bin/env python3
"""Recheck a retained exact native memcpy source-only MAINL pair."""
import json
from pathlib import Path

import build_th03_mainl_memcpy_work as producer
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import compare_members, library_members

ROOT = Path(__file__).resolve().parents[1]
REPORT = '.analysis/work/mainl-memcpy-review.json'


def review(root=ROOT):
    root=Path(root)
    r=json.loads((root/producer.REPORT).read_bytes())
    base, _, library, members, _ = producer.baseline_provider.baseline(root)
    original=producer.TARGET_OBJ.read_bytes()
    source=(root/producer.SOURCE).read_bytes()
    need(r['complete'] and not r['source_acceptance'] and
         r['added_accepted_bytes']==0 and not r['original_cold_rebuilt'] and
         r['reused_accepted_library']==base and r['current_library_sha256']==sha(library) and
         r['source_sha256']==sha(source) and
         r['driver_sha256']==sha((root/producer.DRIVER).read_bytes()) and
         r['original_member_sha256']==sha(original),
         'bound unchanged source, real target member, baseline, and native recipe')
    need(len(r['rounds'])==2 and [q['round'] for q in r['rounds']]==[1,2],
         'two retained native rounds')
    original_code=producer.native_scope(original)
    vectors=[]
    for num,entry in enumerate(r['rounds'],1):
        need(set(entry['outputs'])=={'obj','lib','exe','map'},
             'complete native OBJ/LIB/EXE/MAP outputs')
        outputs={}
        for kind,meta in entry['outputs'].items():
            data=(root/meta['path']).read_bytes()
            need(meta==dict(path=meta['path'],bytes=len(data),sha256=sha(data)),
                 'original retained raw '+kind+' in round '+str(num))
            outputs[kind]=data
        need(producer.native_scope(outputs['obj'])==original_code,
             'all36 native instruction bytes and zero ordered fields')
        compared=compare_members(members,library_members(outputs['lib']),
                                 {'memcpy':outputs['obj']})
        need(entry['library_comparison']==compared and
             compared['contextual_members_unchanged']==892 and
             compared['replaced_members']==['memcpy'],
             'one genuine source replacement in original893-member order')
        need(outputs['exe']==(producer.WORK/'bin/th03/mainl.target.exe').read_bytes() and
             outputs['map']==(producer.WORK/'obj/th03/mainl.map').read_bytes(),
             'complete actual decoded Japanese MAINL EXE and MAP match')
        need(entry['native_code_sha256']==sha(original_code),
             'recompilation retains complete original native memcpy body')
        vectors.append(outputs)
    need(vectors[0]==vectors[1], 'two identical complete raw native output vectors')
    need(len(r['phases'])==7 and [x['label'] for x in r['phases']]==
        ['extract']+[f'round{i}-{kind}' for i in (1,2) for kind in
          ('assemble','library','link')],
         'actual isolated native writer phases')
    for phase in r['phases']:
        log=(root/phase['log_path']).read_bytes()
        need(phase['returncode']==0 and sha(log)==phase['log_sha256'],
             'review actual successful TASM/TLIB/TLINK phase logs')
    return dict(complete=True,source_acceptance=False,added_accepted_bytes=0,
                original_cold_rebuilt=False,original_member_CODE_bytes=36,
                candidate_CODE_bytes=36,literal_ordered_fields=0,
                original_library_members=893,context_members_unchanged=892,
                original_member_index=261,source_origin=producer.SOURCE,
                whole_decoded_EXE_equal=True,whole_MAP_equal=True,
                deterministic_native_rounds=2,
                build_report_sha256=sha((root/producer.REPORT).read_bytes()),
                source_sha256=sha(source),driver_sha256=sha((root/producer.DRIVER).read_bytes()))


if __name__=='__main__':
    r=review()
    (ROOT/REPORT).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
