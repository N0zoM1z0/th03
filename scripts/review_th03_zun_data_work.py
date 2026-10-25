#!/usr/bin/env python3
"""Review four bounded driver header/DATA scopes on a complete current cold pair."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import review_th03_zun_lifecycle_work as lifecycle
from review_th03_zun_format_work import images
from lib.zun_driver_data_layout import verify as layout
from lib.zun_driver_data_runtime import Machine, MESSAGES, specification, verify as runtime, negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / '.analysis/work/zun-data-build.json'
INPUTS = (*lifecycle.INPUTS, 'scripts/review_th03_zun_data_work.py',
          'scripts/lib/zun_driver_data_layout.py', 'scripts/lib/zun_driver_data_runtime.py',
          'src/zun/driver.asm', 'src/zun/driver_services.inl', 'src/zun/driver_numbers.inl')


def need(value,message):
    if not value:
        raise ValueError('ZUN DATA review: ' + message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {n:sha((root/n).read_bytes()) for n in INPUTS}


def witness(scope):
    r = scope['runtime']
    need((r['images'],r['code_bytes'],r['data_bytes'],r['functions'],r['cases_per_image']) == (2,2,1294,0,284),
         'complete fresh-image DATA runtime dimensions')
    need([(o['load_segment'],o['cases'],o['initial_data_bytes'],o['header_executed_bytes']) for o in r['observations']]
         == [(0x1000,142,1294,2),(0x3000,142,1294,2)], 'both load/coverage witnesses')
    need(all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) and o['raw_data_preserved_on_load']
             and not o['callback_bodies_executed'] for o in r['observations']),
         'raw initial DATA and bounded callback trace witnesses')
    c = scope['negative_controls']
    need(c['data_byte_mutations_rejected'] == 1294
         and c['runtime_mutation_addresses'] == [0x101,0xC80,0x8E6,0x101E,0x1044,0xF7A,0x1170]
         and c['header_instruction_mutations'] == 1 and c['consumed_data_mutations'] == 6,
         'separate initial-DATA and actual-consumer negative controls')
    need(not r['default_state_replaced'] and r['callbacks_are_selection_boundaries']
         and not scope['layout']['reserved_spans_owned'] and not scope['layout']['enclosing_driver_accepted'],
         'bounded DATA source classification')


def smoke(target,candidate):
    observations = []
    for image in (target,candidate):
        specification(image)
        machine = Machine(image,0x3000)
        try:
            machine.reset(stop=0x10C)
            machine.run(0x100)
            machine.reset()
            machine.run(0x100)
            expected = (MESSAGES[10][1]+MESSAGES[11][1]).encode('shift_jis')
            need(machine.output == expected and machine.terminal == 0x4C01, 'fresh default startup smoke')
            observations.append(machine.traces)
        finally:
            machine.close()
    need(observations[0] == observations[1], 'current fresh-image DATA smoke')
    return dict(cases_per_image=2,images=2,trace_sha256=sha(json.dumps(observations[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,at,files,maintained,cold):
    raw = REPORT.read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema'] == 'th03-zun-data-current-review-v1', 'complete current report')
    need(report['implementation_sha256'] == inputs(root), 'DATA implementation/source drift')
    need(report['cold_report_sha256'] == sha(cold)
         and report['lifecycle_report_sha256'] == sha(lifecycle.REPORT.read_bytes()), 'cold/lifecycle binding')
    scope = report['scope']
    need(scope['layout'] == layout(work,target,candidate,at,files,maintained), 'current native source ownership')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate current complete prerequisites; run new DATA gates')
    options = parser.parse_args()
    report = dict(schema='th03-zun-data-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
        whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    save = lambda: REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_zun_lifecycle_work.py')],cwd=ROOT,check=True)
    work,target,candidate,at,files,maintained,cold = images(ROOT)
    lifecycle.current_scope(ROOT,work,target,candidate,at,files,maintained,cold)
    report['cold_report_sha256'] = sha(cold)
    report['lifecycle_report_sha256'] = sha(lifecycle.REPORT.read_bytes())
    report['scope'] = dict(layout=layout(work,target,candidate,at,files,maintained),
                          runtime=runtime(target,candidate),negative_controls=negative_controls(target))
    witness(report['scope'])
    need(report['implementation_sha256'] == inputs(ROOT), 'inputs changed during DATA review')
    report['complete'] = True
    save()
    print('ZUN header/DATA: four extents / 2 CODE + 1294 DATA bytes; 25 native WORD fields; fresh-image contracts pass')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
