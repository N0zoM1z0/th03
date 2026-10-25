#!/usr/bin/env python3
"""Review natural STAFF initialized DATA and its actual native consumers."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_staff_verdict_work as previous
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_staff_data_layout import verify as layout
from lib.decoded_mainl_staff_data_runtime import verify as runtime, negative_controls, fixture

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/mainl-staff-data-build.json'
INPUTS=(*previous.INPUTS,'scripts/review_th03_mainl_staff_data_work.py',
        'scripts/lib/decoded_mainl_staff_data_layout.py','scripts/lib/decoded_mainl_staff_data_runtime.py')


def need(value,message):
    if not value:
        raise ValueError('MAINL staff DATA review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    l,r,c=scope['layout'],scope['runtime'],scope['negative_controls']
    need((l['functions'],l['code_bytes'],l['initialized_data_bytes'],l['bss_bytes'],l['pointer_bytes'],
          l['sprite_bytes'],l['mask_bytes'],len(l['ordered_native_fields']),l['mz_relocation_count'],l['initialized_holes'])
         ==(0,0,224,0,96,64,64,24,24,0),'complete semantic/native DATA layout')
    need(l['owners'][0]['procedure_count']==0 and not l['enclosing_CODE_or_pointees_accepted']
         and not l['whole_product_accepted'],'DATA adds no procedure or pointee ownership')
    need((r['images'],r['initialized_data_bytes'],r['cases_per_image'],r['ignored_stack_bytes'],r['new_CODE_ownership_bytes'])
         ==(2,224,236,0,0),'complete target/candidate and unchanged full-state consumer contracts')
    need([(o['load_segment'],o['complete_calls'],o['initialized_bytes_read'],o['static_only_bytes']) for o in r['observations']]
         ==[(load,dict(flake=32,mask=28,verdict=46,ending=12),216,8) for load in (0x1000,0x3000)],
         'all reachable initializers read by actual native operand instructions at both loads')
    need(r['existing_full_state_contracts_preserved'] and not r['guest_iterations_skipped']
         and not r['pointee_strings_or_renderer_owned'] and not r['physical_pixels_or_timing_proved'],'bounded storage behavior')
    need(c['count']==len(c['data_bit_mutations'])==len({tuple(m) for m in c['data_bit_mutations']})==1712
         and c['actual_native_consumers'] and c['static_only_mask_bytes']==8
         and not c['script_segment_WORD_behavior_controls'] and not c['CODE_mutations_counted'],'semantic data-bit controls, separate unobserved mask/script-segment lanes')


def smoke(target,candidate):
    rows=[]
    for image in (target,candidate):
        rows.append([fixture(kind,image,0x3000,parameters)[0] for kind,parameters in (
            ('flake',(3,7)),('mask',(7,3)),('verdict',(8,3,9)),('ending',(255,3)))])
    need(rows[0]==rows[1],'current actual relocated DATA consumer replay')
    return dict(images=2,cases_per_image=4,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw=(root/'.analysis/work/mainl-staff-data-build.json').read_bytes()
    report=json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-staff-data-current-review-v1','complete DATA report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),
         'current source / implementation / cold binding')
    need(report['verdict_review_sha256']==sha(previous.REPORT.read_bytes()),'current prerequisite staff proof')
    scope=report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'current entire raw/native/MZ/layout initializer')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate entire unchanged source cold pair; rerun full DATA gates')
    options=parser.parse_args()
    report=dict(schema='th03-mainl-staff-data-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
                provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
                whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_staff_verdict_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files=sound.images(ROOT)
    previous.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),verdict_review_sha256=sha(previous.REPORT.read_bytes()),
                  source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope']=dict(layout=layout(work,target,candidate,graph,files),runtime=runtime(target,candidate))
    save()
    report['scope']['negative_controls']=negative_controls(target)
    save()
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'DATA review inputs changed during execution')
    report['complete']=True
    save()
    print('MAINL staff DATA: all224 bytes,24 literal fields/relocations,216 read bytes and1712 semantic bit controls pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
