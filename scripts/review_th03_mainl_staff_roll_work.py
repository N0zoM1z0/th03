#!/usr/bin/env python3
"""Review the entire native staff roll and its actual sound/resource/staff/input callees."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_staff_data_work as previous
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_staff_roll_layout import verify as layout
from lib.decoded_mainl_staff_roll_runtime import verify as runtime,negative_controls,Machine
from lib.decoded_mainl_staff_roll_proofs import geometry_proof

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/mainl-staff-roll-build.json'
INPUTS=(*previous.INPUTS,'scripts/review_th03_mainl_staff_roll_work.py',
    'scripts/lib/decoded_mainl_staff_roll_layout.py','scripts/lib/decoded_mainl_staff_roll_services.py',
    'scripts/lib/decoded_mainl_staff_roll_machine.py','scripts/lib/decoded_mainl_staff_roll_runtime.py',
    'scripts/lib/decoded_mainl_staff_roll_proofs.py')


def need(value,message):
    if not value:
        raise ValueError('MAINL roll review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    l,r,c=scope['layout'],scope['runtime'],scope['negative_controls']
    need((l['functions'],l['code_bytes'],len(l['ordered_native_fields']),l['mz_relocation_count'],len(l['internal_near_calls']),len(l['far_calls']))
         ==(1,980,108,34,22,34),'complete native980 and literal ordered fields/calls')
    need(not l['enclosing_DATA_or_other_CODE_newly_accepted'] and not l['whole_product_accepted'],'only complete roll owns new CODE')
    need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['ignored_stack_bytes'],r['complete_returns_per_image'],r['no_input_prefixes_per_image'])
         ==(2,1,980,980,0,6,6),'complete native returns and separate conditional prefixes')
    need(all(o['complete_near_returns']==o['no_input_prefixes']==3 and o['maximum_stack_depth']==78 and o['clear_WORD_callbacks_per_return']==7616000
             and o['executed_owner_bytes']==980 for o in r['observations']),'actual complete matrix and native-frame/WORD-store bounds')
    need(not r['guest_iterations_skipped'] and not r['budget_expiry_used_as_proof'] and not r['physical_IRQ_audio_input_or_pixels_proved'],
         'software contracts retain their explicit device boundaries')
    need((c['count'],c['owner_instruction_mutations'],c['actual_context_mutations'])==(17,15,2)
         and len(set(c['rejected']))==17 and c['actual_guest_instructions_mutated'] and not c['layout_failure_counted'],
         'actual native owner/context controls')


def smoke(target,candidate):
    rows=[]
    for image in (target,candidate):
        machine=Machine(image,0x3000)
        try:
            rows.append([machine.run(prepare_only=True,character=0,credits=255,skill=250,score=(0,0,0,0,0,255,3,0)),
                         machine.run(sample=(0,0,0,0),input_prefix=1)])
        finally:
            machine.close()
    need(rows[0]==rows[1],'current native complete preparation and no-input continuation')
    return dict(images=2,cases_per_image=2,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
        full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw=(root/'.analysis/work/mainl-staff-roll-build.json').read_bytes()
    report=json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-staff-roll-current-review-v1','complete roll report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),'current source/implementation/cold binding')
    need(report['data_review_sha256']==sha(previous.REPORT.read_bytes()),'current prerequisite staff storage proof')
    scope=report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'current entire native byte/field/layout proof')
    need(scope['runtime']['native_geometry_proof']==geometry_proof(target)==geometry_proof(candidate),'current entire native arithmetic/CFG proof')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate entire unchanged native cold pair; rerun all roll gates')
    options=parser.parse_args()
    report=dict(schema='th03-mainl-staff-roll-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
        whole_product_accepted=False,canonical_unit_credit_changed=False)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_staff_data_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files=sound.images(ROOT)
    previous.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),data_review_sha256=sha(previous.REPORT.read_bytes()),
                  source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope']=dict(layout=layout(work,target,candidate,graph,files))
    save()
    report['scope']['runtime']=runtime(target,candidate)
    save()
    report['scope']['negative_controls']=negative_controls(target)
    save()
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'roll implementation changed during execution')
    report['complete']=True
    save()
    print('MAINL roll: complete980 bytes,native call graph,real waits/fade/cleanup and independent full-state gates pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
