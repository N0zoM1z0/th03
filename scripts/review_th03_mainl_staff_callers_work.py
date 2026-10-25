#!/usr/bin/env python3
"""Review three whole staff callers, native INT0 and proved unreachable bytes."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_dissolve_work as dissolve
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_staff_callers_layout import verify as layout
from lib.decoded_mainl_staff_callers_runtime import Machine, verify as runtime, geometry_proof, negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'.analysis/work/mainl-staff-callers-build.json'
INPUTS = (*dissolve.INPUTS,'scripts/review_th03_mainl_staff_callers_work.py',
          'scripts/lib/decoded_mainl_staff_callers_layout.py','scripts/lib/decoded_mainl_staff_callers_runtime.py')


def need(value,message):
    if not value:
        raise ValueError('MAINL staff callers review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    r,l,c = scope['runtime'],scope['layout'],scope['negative_controls']
    need((r['images'],r['functions'],r['code_bytes'],r['cases_per_image'],r['executed_owner_bytes'],r['proved_unreachable_bytes'],r['actual_owned_context_bytes'],r['ignored_stack_bytes'])
         ==(2,3,446,16716,443,3,693,0),'complete raw / executed / proved unreachable ownership dimensions')
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['divide_faults_by_function'],o['returned_calls'],
           o['native_divide_faults'],o['complete_raw_owner_bytes'],o['executed_owner_bytes'],o['proved_unreachable_bytes'],
           o['actual_context_bytes'],o['maximum_stack_depth_by_function'],o['maximum_actual_calls'],o['actual_clear_WORD_callbacks']) for o in r['observations']]
         ==[(load,8358,dict(enter=3688,leave=2088,gallery=2582),dict(enter=78,leave=0,gallery=0),8280,78,446,443,3,693,
              dict(enter=54,leave=54,gallery=52),dict(clear=1,unput=1,dissolve=2,off=1,alpha=2,noalpha=1,box=1,color=2),92416000)
             for load in (0x1000,0x3000)]
         and all(re.fullmatch('[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),
         'actual nested frames / every REP callback / full parameter lanes / separate returns and native faults')
    p = r['native_geometry_proof']
    need((p['frame_WORD_states'],p['duration_WORD_states'],p['page_BYTE_states'],p['divide_fault_site'])==(65536,65536,256,0x2885)
         and p['zero_divisor_duration_WORDs']==list(range(8))+list(range(0xFFF9,0x10000))
         and p['overflow_duration_WORDs']==list(range(0xFFF1,0xFFF9)) and p['overflow_frame_WORD']==0x8000
         and p['proved_unreachable_ranges']==[dict(segment=0x95F,offset=0x2925,size=3)]
         and (p['complete_raw_owner_bytes'],p['executed_owner_bytes'],p['proved_unreachable_bytes'])==(446,443,3)
         and p['actual_clear_WORDs_per_call']==16000 and p['rep_log_compacted'] and p['every_actual_clear_WORD_checked']
         and not p['guest_iterations_skipped'] and not p['budget_expiry_used'] and p['assumptions']
         and not p['bytebox_body_or_INT0_handler_or_physical_graphics_proved'],'native complete fault classes / unreachable proof / real clear iterations')
    need(r['fresh_CPU_after_stopped_divide_exception'] and r['immediate_owned_return_checks'] and not r['guest_iterations_skipped']
         and not r['bytebox_body_or_INT0_handler_or_physical_graphics_proved'],'explicit exception-dispatch and unowned bytebox/device boundaries')
    need((l['functions'],l['code_bytes'],len(l['ordered_native_fields']),l['mz_relocation_count'],len(l['internal_near_calls']))==(3,446,44,3,9)
         and l['owners'][1]['proved_unreachable_ranges']==[dict(offset=0x2925,size=3,
             reason='signed frame<160 implies trunc(frame/20)<=7; readonly frame until this comparison')]
         and not l['enclosing_DATA_or_other_functions_accepted'] and not l['bytebox_library_or_physical_graphics_accepted']
         and not l['whole_product_accepted'],'complete natural native bodies / literal fields / reviewed ownership')
    need(c['count']==len(set(c['rejected']))==56 and c['owner_instruction_mutations']==51
         and c['by_function']==dict(enter=24,leave=18,gallery=9) and c['actual_context_instruction_mutations']==5
         and c['actual_guest_instruction_mutations'] and not c['unreachable_bytes_counted_as_executed_controls']
         and not c['unowned_DATA_mutations_counted'],'actual owner/context mutations, excluding unreachable and unowned DATA')


def smoke(target,candidate):
    rows = []
    for image in (target,candidate):
        m = Machine(image,0x3000)
        try:
            rows.append([m.run(kind,**p) for kind,p in (
                ('enter',dict(page=255,flags=0xED7)),('enter',dict(frame=0,duration=7)),
                ('enter',dict(frame=0x8000,duration=0xFFF8)),('leave',dict(frame=160,box_seed=0xFF00,flags=0xED7,ss=0x8000,stack=0x80)),
                ('gallery',dict(frame=160,enabled=255)))])
        finally:
            m.close()
    need(rows[0]==rows[1],'current complete ordinary/fault/foreign-stack live software contracts')
    return dict(images=2,cases_per_image=5,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw = (root/'.analysis/work/mainl-staff-callers-build.json').read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-staff-callers-current-review-v1','complete staff callers report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),'current source / implementation / cold binding')
    need(report['dissolve_review_sha256']==sha(dissolve.REPORT.read_bytes()),'current prerequisite source and native-context chain')
    scope = report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'current complete raw / ordered native / ownership proof')
    need(scope['runtime']['native_geometry_proof']==geometry_proof(target)==geometry_proof(candidate),'current native divide / unreachable / clear proof')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate entire unchanged cold pair; rerun complete staff caller gates')
    options = parser.parse_args()
    report = dict(schema='th03-mainl-staff-callers-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
                  provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
                  whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_dissolve_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files = sound.images(ROOT)
    dissolve.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),dissolve_review_sha256=sha(dissolve.REPORT.read_bytes()),source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope'] = dict(layout=layout(work,target,candidate,graph,files),negative_controls=negative_controls(target))
    save()
    report['scope']['runtime'] = runtime(target,candidate)
    save()
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'staff caller inputs changed during execution')
    report['complete'] = True
    save()
    print('MAINL staff callers:446 complete native bytes;443 executed/3 proved unreachable;693 real context bytes and native INT0 contracts pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
