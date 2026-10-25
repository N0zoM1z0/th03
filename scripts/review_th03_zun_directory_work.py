#!/usr/bin/env python3
"""Review the native semantic directory and actual wrapper readers."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import review_th03_zun_wrapper_work as wrapper
from review_th03_zun_format_work import images
from lib.zun_directory_layout import SOURCE,verify as layout
from lib.zun_directory_runtime import verify as runtime,negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'.analysis/work/zun-directory-build.json'
INPUTS = (*wrapper.INPUTS,'scripts/review_th03_zun_directory_work.py','scripts/lib/zun_directory_layout.py',
          'scripts/lib/zun_directory_runtime.py','scripts/lib/zun_directory_controls.py','scripts/lib/zun_directory_source.py',SOURCE)


def need(value,message):
    if not value:
        raise ValueError('ZUN directory review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {n:sha((root/n).read_bytes()) for n in INPUTS}


def witness(scope):
    r = scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['data_bytes'],r['cases_per_image']) == (2,0,0,324,42),
         'complete directory DATA dimensions')
    need([(o['load_segment'],o['split_stack'],o['cases'],o['maximum_observed_stack_depth']) for o in r['observations']]
         == [(0x1000,False,21,4),(0x3000,True,21,4)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']), 'both complete reader witnesses')
    c = scope['negative_controls']
    need(c['initial_DATA_byte_mutations_rejected'] == 324 and c['actual_reader_DATA_mutation_count'] == 11
         and c['actual_reader_DATA_mutations_rejected'] == [f'name-{i}' for i in range(5)]+[f'boundary-{i}' for i in range(6)]
         and c['instruction_mutations'] == 0 and not c['static_mutations_have_execution_credit'],
         'separate static and actual-reader DATA controls')
    need(not r['unused_slots_have_execution_credit'] and not r['payload_instructions_executed']
         and not scope['layout']['payloads_owned'] and not scope['layout']['enclosing_product_accepted'],
         'bounded metadata source ownership')
    controls = scope['native_source_controls']
    need(controls['count'] == 2 and controls['source_only'] and not controls['object_patches']
         and [(r['capacity'],r['bytes'],r['byte_exact_rejected']) for r in controls['controls']]
         == [(31,314,True),(33,334,True)], 'both actual native capacity controls')


def current_scope(root,work,target,candidate,files,maintained,cold):
    raw = REPORT.read_bytes();r = json.loads(raw)
    need(r['complete'] and r['schema'] == 'th03-zun-directory-current-review-v1','complete current report')
    need(r['implementation_sha256'] == inputs(root),'directory implementation/source drift')
    need(r['cold_report_sha256'] == sha(cold) and r['wrapper_report_sha256'] == sha(wrapper.REPORT.read_bytes()),
         'current native cold/wrapper bindings')
    scope = r['scope']
    need(scope['layout'] == layout(work,target,candidate,files,maintained,json.loads(cold)),'current native DATA ownership')
    need(scope['native_source_controls'] == json.loads(cold)['directory_source_controls'],'current native controls')
    witness(scope)
    # The outer audit runs the wrapper smoke; this binds the full five-record DATA witnesses.
    return dict(**scope,review_sha256=sha(raw))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--current-cold',action='store_true',help='use fully current cold/wrapper prerequisites; run new metadata gates')
    o = p.parse_args()
    r = dict(schema='th03-zun-directory-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        provenance='candidate-local-attested',native_pair_built_now=not o.current_cold,
        whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    save = lambda: REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_zun_wrapper_work.py')],cwd=ROOT,check=True)
    work,_,_,_,files,maintained,cold = images(ROOT)
    target = (work/'product/zun.target.com').read_bytes();candidate = (work/'product/zun.com').read_bytes()
    wrapper.current_scope(ROOT,work,target,candidate,files,maintained,cold)
    r['cold_report_sha256'],r['wrapper_report_sha256'] = sha(cold),sha(wrapper.REPORT.read_bytes())
    r['scope'] = dict(layout=layout(work,target,candidate,files,maintained,json.loads(cold)),
        runtime=runtime(target,candidate),negative_controls=negative_controls(target),
        native_source_controls=json.loads(cold)['directory_source_controls'])
    witness(r['scope']);need(r['implementation_sha256'] == inputs(ROOT),'inputs changed during review')
    r['complete'] = True;save()
    print('ZUN directory: complete native 324-byte semantic DATA TU; 32-slot ownership, linked boundaries and reader controls pass')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
