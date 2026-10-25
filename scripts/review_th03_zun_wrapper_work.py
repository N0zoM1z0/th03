#!/usr/bin/env python3
"""Review complete maintained launcher/transfer TUs on the current cold graph."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import review_th03_zun_data_work as data
from review_th03_zun_format_work import images
from lib.zun_wrapper_layout import verify as layout, SOURCES
from lib.zun_wrapper_runtime import Machine, verify as runtime, negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'.analysis/work/zun-wrapper-build.json'
INPUTS = (*data.INPUTS,'scripts/review_th03_zun_wrapper_work.py','scripts/lib/zun_wrapper_layout.py',
          'scripts/lib/zun_wrapper_runtime.py',*SOURCES)


def need(value,message):
    if not value:
        raise ValueError('ZUN wrapper review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {n:sha((root/n).read_bytes()) for n in INPUTS}


def witness(scope):
    r = scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['data_bytes'],r['cases_per_image']) == (2,3,213,21,2310),
         'complete wrapper runtime dimensions')
    need([(o['load_segment'],o['split_stack'],o['cases'],o['covered_owner_bytes'],o['maximum_observed_stack_depth'])
          for o in r['observations']] == [(0x1000,False,1155,213,4),(0x3000,True,1155,213,4)],
         'complete load/SS/coverage/stack witnesses')
    need(all(o['cases_by_entry'] == dict(launcher=1065,call=45,helper=45)
             and re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),
         'all three entry domains and traces')
    need(not r['payload_instructions_executed'] and not r['stack_windows_ignored']
         and r['all_memory_and_ordered_stores_checked'] and r['DOS_AL_reply_policies'] == 3,
         'bounded DOS, complete memory and payload stop boundary')
    c = scope['negative_controls']
    need(c['count'] == len(set(c['rejected'])) == 21 and c['actual_guest_instruction_changes']
         and not c['payload_bytes_mutated'] and not c['directory_mutations_counted_as_instructions'],
         '21 actual wrapper instruction mutations')
    need(not scope['layout']['payloads_owned'] and not scope['layout']['enclosing_product_accepted'],
         'bounded outer wrapper source classification')


def smoke(target,candidate):
    observations = []
    for image in (target,candidate):
        m = Machine(image,0x3000,True)
        try:
            observations.append([
                m.run(reply=1), m.run(count=0),
                m.run(command=b' -X',fcb=b'-X',reply=2),
                m.run(command=b' -3 hello',fcb=b'-3',reply=2,flags=0xED7),
                m.run('call',payload_index=2,size=10096,flags=0x202),
                m.run('helper',payload_index=0,size=0,flags=0x202)])
        finally:
            m.close()
    need(observations[0] == observations[1], 'current complete-state wrapper smoke')
    return dict(cases_per_image=6,images=2,trace_sha256=sha(json.dumps(observations[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,files,maintained,cold):
    raw = REPORT.read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema'] == 'th03-zun-wrapper-current-review-v1', 'complete current report')
    need(report['implementation_sha256'] == inputs(root), 'wrapper implementation/source drift')
    need(report['cold_report_sha256'] == sha(cold)
         and report['data_report_sha256'] == sha(data.REPORT.read_bytes()), 'whole cold/DATA report binding')
    scope = report['scope']
    need(scope['layout'] == layout(work,target,candidate,files,maintained), 'current native whole-TU ownership')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate current complete prerequisites; run new wrapper gates')
    options = parser.parse_args()
    report = dict(schema='th03-zun-wrapper-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
        whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    save = lambda: REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_zun_data_work.py')],cwd=ROOT,check=True)
    work,driver_target,driver_candidate,at,files,maintained,cold = images(ROOT)
    data.current_scope(ROOT,work,driver_target,driver_candidate,at,files,maintained,cold)
    target = (work/'product/zun.target.com').read_bytes()
    candidate = (work/'product/zun.com').read_bytes()
    report['cold_report_sha256'],report['data_report_sha256'] = sha(cold),sha(data.REPORT.read_bytes())
    report['scope'] = dict(layout=layout(work,target,candidate,files,maintained),
                          runtime=runtime(target,candidate),negative_controls=negative_controls(target))
    witness(report['scope'])
    need(report['implementation_sha256'] == inputs(ROOT), 'inputs changed during wrapper review')
    report['complete'] = True
    save()
    print('ZUN wrapper: three whole TUs / 213 CODE + 21 DATA bytes; native, complete-state and 21 mutation gates pass')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
