#!/usr/bin/env python3
"""Review the complete native MAINL dissolve procedure and actual owned blitters."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_snow_work as snow
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_dissolve_layout import verify as layout
from lib.decoded_mainl_dissolve_runtime import Machine, verify as runtime, geometry_proof, negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'.analysis/work/mainl-dissolve-build.json'
INPUTS = (*snow.INPUTS,'scripts/review_th03_mainl_dissolve_work.py','scripts/lib/decoded_mainl_dissolve_layout.py',
          'scripts/lib/decoded_mainl_dissolve_runtime.py')


def need(value,message):
    if not value:
        raise ValueError('MAINL dissolve review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    r,l,c = scope['runtime'],scope['layout'],scope['negative_controls']
    need((r['images'],r['functions'],r['code_bytes'],r['cases_per_image'],r['executed_owner_bytes'],r['actual_owned_context_bytes'],r['ignored_stack_bytes'])
         ==(2,1,211,36314,211,333,0),'complete procedure / full physical memory dimensions')
    need([(o['load_segment'],o['cases'],o['calls_by_blitter'],o['executed_owner_bytes'],o['actual_context_bytes'],
           o['maximum_stack_depth'],o['maximum_rows'],o['maximum_inner_iterations'],o['maximum_WORD_stores']) for o in r['observations']]
         ==[(load,18157,dict(alpha=656,noalpha=17501),211,333,38,65536,65536,65536) for load in (0x1000,0x3000)]
         and all(re.fullmatch('[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),
         'all real blitters / BYTE lanes / pattern WORDs / separately executed maximal loops')
    p = r['native_geometry_proof']
    need((p['width_WORD_states'],p['strength_WORD_states'],p['maximum_inner_iterations'],p['maximum_rows'],p['maximum_combined_WORD_stores'])
         ==(65536,65536,65536,65536,1<<32) and p['row_count_formula'] and p['assumptions']
         and not p['maximum_combined_case_executed'] and not p['budget_expiry_used'] and not p['guest_iterations_skipped']
         and not p['physical_planar_pixels_or_timing_proved'],'complete native finite recurrence, without claiming maximal Cartesian execution')
    need(not r['external_patterns_or_slots_owned'] and not r['physical_planar_pixels_or_timing_proved'],'external assets / physical graphics boundary')
    need((l['functions'],l['code_bytes'],len(l['ordered_native_fields']),l['mz_relocation_count'])==(1,211,7,2)
         and not l['enclosing_DATA_or_other_functions_accepted'] and not l['external_patterns_slots_or_hardware_accepted']
         and not l['whole_product_accepted'],'complete native body / ordered fields / reviewed ownership')
    need(c['count']==len(set(c['rejected']))==40 and c['owner_instruction_mutations']==37 and c['actual_context_instruction_mutations']==3
         and c['actual_guest_instruction_mutations'] and not c['unowned_DATA_mutations_counted'],'actual owner/context instruction controls')


def smoke(target,candidate):
    rows = []
    for image in (target,candidate):
        m = Machine(image,0x3000)
        try:
            rows.append([m.run(**p) for p in (dict(enabled=255,requested=128,flags=0xED7),
                dict(strength=0x8000,width=0x8001,blit_width=0,ss=0x8000,stack=0x80),
                dict(width=16,height=3,top=0xFFFF,blit_width=0),dict(enabled=1,persistent=True))])
        finally:
            m.close()
    need(rows[0]==rows[1],'current complete native-call / caller-WORD / unsigned-row smoke')
    return dict(images=2,cases_per_image=4,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw = (root/'.analysis/work/mainl-dissolve-build.json').read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-dissolve-current-review-v1','complete dissolve report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),'current source / implementation / cold binding')
    need(report['snow_review_sha256']==sha(snow.REPORT.read_bytes()),'current prerequisite owner and source chain')
    scope = report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'current full raw / ordered native / ownership proof')
    need(scope['runtime']['native_geometry_proof']==geometry_proof(target)==geometry_proof(candidate),'current native finite-loop binding')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate the entire unchanged cold pair; rerun complete dissolve gates')
    options = parser.parse_args()
    report = dict(schema='th03-mainl-dissolve-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
                  provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
                  whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_snow_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files = sound.images(ROOT)
    snow.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),snow_review_sha256=sha(snow.REPORT.read_bytes()),
                  source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope'] = dict(layout=layout(work,target,candidate,graph,files),runtime=runtime(target,candidate),
                           negative_controls=negative_controls(target))
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'dissolve inputs changed during execution')
    report['complete'] = True
    save()
    print('MAINL dissolve: complete211-byte procedure,333 actual owned context bytes and full physical-state contracts pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
