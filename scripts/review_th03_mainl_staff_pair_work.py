#!/usr/bin/env python3
"""Review the whole staff pair controller and both conditional waiting CFGs."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_staff_single_work as previous
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_staff_pair_layout import verify as layout
from lib.decoded_mainl_staff_pair_runtime import Machine, verify as runtime, geometry_proof, negative_controls, exit_schedule, DATA

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'.analysis/work/mainl-staff-pair-build.json'
INPUTS = (*previous.INPUTS,'scripts/review_th03_mainl_staff_pair_work.py',
          'scripts/lib/decoded_mainl_staff_pair_layout.py','scripts/lib/decoded_mainl_staff_pair_runtime.py')


def need(value,message):
    if not value:
        raise ValueError('MAINL staff pair review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    r,l,c = scope['runtime'],scope['layout'],scope['negative_controls']
    need((r['images'],r['functions'],r['code_bytes'],r['cases_per_image'],r['executed_owner_bytes'],r['actual_context_bytes'],r['unowned_vector_context_bytes'],r['ignored_stack_bytes'])
         ==(2,1,358,12194,358,1688,69,0),'complete owner / actual owned and unowned context dimensions')
    need([(o['load_segment'],o['cases'],o['endings'],o['executed_owner_bytes'],o['actual_context_bytes'],
           o['maximum_stack_depth'],o['maximum_phase_iterations'],o['maximum_ticks'],o['maximum_actual_clear_WORD_callbacks']) for o in r['observations']]
         ==[(load,6097,{'return':5953,'divide-fault':48,'clock-prefix':48,'enter-prefix':48},358,1688,64,[257,257],516,8224000)
             for load in (0x1000,0x3000)] and all(re.fullmatch('[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),
         'actual full loops / parameter lanes / separate returns, faults and both proved-prefix classes')
    p = r['native_geometry_proof']
    need((p['normal_no_music_phase_iterations'],p['normal_no_music_total_ticks'],p['enter_loop_head'],p['enter_loop_tail'],p['leave_loop_head'],p['leave_loop_tail'])
         ==(257,516,0x2AEC,0x2B1C,0x2B24,0x2BBB) and p['conditional_enter_loop_invariant']
         and len(p['conditional_enter_loop_assumptions'])==3 and p['conditional_enter_loop_nontermination_proved']
         and p['readonly_zero_clock_loop_proved'] and p['loop_prefixes_are_not_terminal_calls']
         and p['pair_clamp_frame_WORDs']==[161,32768] and p['pair_IDIV_quotient_range']==[-1638,1638]
         and p['pair_strength_range']==[-1638,7] and p['secondary_y_entrance_invariant']==200 and p['secondary_slot_entrance_invariant']==0
         and p['final_unconditional_ticks']==2 and p['leave_unreachable_bytes']==3
         and p['leave_unreachable_range']==[0x2925,0x2928] and p['leave_unreachable_assumptions']
         and r['proved_unreachable_context_bytes']==3 and not p['guest_iterations_skipped'] and not p['budget_expiry_used'] and not p['physical_driver_IRQ_assets_or_timing_proved'],
         'native two-stage CFG / bounded-returning body invariant / readonly-zero clock proof')
    need(r['capacity_lane_fixture']==dict(capacity_range=[0,255],secondary=0,requested=0,enabled=0,blit_width=0,capacity_clamped=False),'explicit unchecked-capacity alias fixture inside bounded flat graphics interface')
    need(r['immediate_owned_return_checks'] and not r['guest_iterations_skipped']
         and not r['physical_driver_IRQ_assets_or_vector_library_proved'],'explicit ABI and software-interface boundaries')
    need((l['functions'],l['code_bytes'],len(l['ordered_native_fields']),l['mz_relocation_count'],len(l['internal_near_calls']))==(1,358,34,9,11)
         and not l['bytebox_library_accepted'] and not l['enclosing_DATA_or_other_functions_accepted'] and not l['physical_IRQ_driver_assets_or_vector_library_accepted']
         and not l['whole_product_accepted'],'complete natural native body / literal fields / reviewed ownership')
    need(c['count']==len(set(c['rejected']))==89 and c['owner_instruction_mutations']==83 and c['actual_context_instruction_mutations']==6
         and c['actual_guest_instruction_mutations'] and not c['unowned_DATA_or_unreachable_mutations_counted'],'actual owner/context instruction mutations')


def smoke(target,candidate):
    rows = []
    for image in (target,candidate):
        m = Machine(image,0x3000)
        try:
            rows.append([m.run(**p) for p in (dict(cap=1,flags=0xED7),dict(speed=2,page=255,ss=0x8000,stack=0x80),
                dict(duration=0),dict(clock_prefix=3,ticks=None,vsync=0),dict(loop_prefix=3,schedule=((0,(),0x8D5),)),
                dict(schedule=exit_schedule(0x8000),flags=0xED7,ss=0x8000,stack=0x80),
                dict(schedule=exit_schedule(160),box_writes=((DATA['frame'],b'\0\0'),)))])
        finally:
            m.close()
    need(rows[0]==rows[1],'current stateful full / fault / readonly-clock / closed-enter-loop software contracts')
    return dict(images=2,cases_per_image=7,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw = (root/'.analysis/work/mainl-staff-pair-build.json').read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-staff-pair-current-review-v1','complete staff pair report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),'current source / implementation / cold binding')
    need(report['single_review_sha256']==sha(previous.REPORT.read_bytes()),'current prerequisite source / single proof')
    scope = report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'current complete raw / ordered native / ownership proof')
    need(scope['runtime']['native_geometry_proof']==geometry_proof(target)==geometry_proof(candidate),'current native CFG/invariant proofs')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate entire unchanged cold pair; rerun full pair gates')
    options = parser.parse_args()
    report = dict(schema='th03-mainl-staff-pair-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
                  provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
                  whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_staff_single_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files = sound.images(ROOT)
    previous.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),single_review_sha256=sha(previous.REPORT.read_bytes()),source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope'] = dict(layout=layout(work,target,candidate,graph,files),negative_controls=negative_controls(target))
    save()
    report['scope']['runtime'] = runtime(target,candidate)
    save()
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'staff pair inputs changed during execution')
    report['complete'] = True
    save()
    print('MAINL staff pair: complete358-byte owner,1688 executed context bytes +3 proved unreachable and full/two-prefix/fault contracts pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
