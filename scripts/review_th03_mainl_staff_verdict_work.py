#!/usr/bin/env python3
"""Review the complete verdict, far-pointer tables and live text-renderer ABI."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_staff_pair_work as previous
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_staff_verdict_layout import verify as layout,DATA
from lib.decoded_mainl_staff_verdict_runtime import Machine,verify as runtime,geometry_proof,negative_controls

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/mainl-staff-verdict-build.json'
INPUTS=(*previous.INPUTS,'scripts/review_th03_mainl_staff_verdict_work.py',
        'scripts/lib/decoded_mainl_staff_verdict_layout.py','scripts/lib/decoded_mainl_staff_verdict_runtime.py')


def need(value,message):
    if not value:
        raise ValueError('MAINL verdict review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    r,l,c=scope['runtime'],scope['layout'],scope['negative_controls']
    need((r['images'],r['functions'],r['code_bytes'],r['cases_per_image'],r['executed_owner_bytes'],r['actual_context_bytes'],r['ignored_stack_bytes'])
         ==(2,1,389,22288,389,0,0),'whole verdict and explicit zero-credit renderer context')
    need([(o['load_segment'],o['cases'],o['complete_near_returns'],o['executed_owner_bytes'],o['minimum_renderer_calls'],
           o['maximum_renderer_calls'],o['maximum_stack_depth'],o['score_iterations_per_entry']) for o in r['observations']]
         ==[(load,11144,11144,389,6,16,24,8) for load in (0x1000,0x3000)]
         and all(re.fullmatch('[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'complete returning native matrix, callbacks and actual frame bounds')
    p=r['native_geometry_proof']
    need((p['score_iterations'],p['renderer_call_bounds'],p['maximum_stack_depth'],p['score_digit_indices'],p['continues_alias_byte'],
          p['local_stack_bytes'],p['far_string_bytes'],p['renderer_argument_bytes'],p['BYTE_index_range'],p['WORD_table_shift'])
         ==(8,[6,16],24,[8,1],0,4,4,10,[0,255],2),'native fixed score loop and unchecked full far pointers')
    need(p['skill_BYTE_domain']==[0,255] and p['skill_divisors']==[100,10] and p['skill_read_sites']==[0x2D63,0x2D9D,0x2DE3]
         and p['skill_hundreds_range']==[0,2] and p['skill_tens_and_ones_range']==[0,9]
         and p['score_x_range']==[344,472] and p['skill_x_range']==[392,440] and len(p['loop_counter_assumptions'])==2
         and p['loop_termination_proved'] and p['all_DIV_inputs_safe'] and not p['guest_iterations_skipped']
         and not p['budget_expiry_used'] and not p['renderer_code_strings_tables_or_physical_pixels_proved'],'complete arithmetic and conditional software-loop termination proof')
    need(r['immediate_renderer_return_checks'] and r['full_renderer_DWORD_replies'] and r['real_far_frames_checked']
         and not r['guest_iterations_skipped'] and not r['renderer_body_or_table_storage_accepted'] and not r['physical_text_pixels_or_timing_proved'],'complete state and explicit renderer/data/device boundaries')
    need((l['functions'],l['code_bytes'],len(l['ordered_native_fields']),l['mz_relocation_count'],len(l['far_calls']),
          l['local_SEGDEF_fields'],l['external_WORD_fields'],l['far_renderer_fields'],l['local_pointer_bytes'])
         ==(1,389,25,9,9,8,8,9,4) and all(c['argument_bytes']==c['callee_pop_bytes']==10 for c in l['far_calls'])
         and not l['enclosing_DATA_or_other_functions_accepted'] and not l['renderer_code_or_strings_tables_accepted']
         and not l['physical_text_or_pixels_proved'] and not l['whole_product_accepted'],'complete native ownership and distinct SEGDEF/EXTDEF field namespaces')
    need(c['count']==len(set(c['rejected']))==93 and c['owner_instruction_mutations']==93 and c['actual_context_instruction_mutations']==0
         and c['actual_guest_instruction_mutations'] and not c['unowned_renderer_or_DATA_mutations_counted'],'actual owner instruction controls with no unowned renderer/data credit')


def smoke(target,candidate):
    rows=[]
    for image in (target,candidate):
        m=Machine(image,0x3000)
        try:
            rows.append([m.run(**p) for p in ({},dict(score=(0,)*9,skill=0),
                dict(score=(0,)*9,skill=10,foreign_ds=True,ss=0x8000,stack=0x80,flags=0xED7,flag_schedule=(2,0x202,0x402,0xED7)),
                dict(score=(0,)*9,skill=100,writes=((5,DATA['skill'],b'\x09'),(6,DATA['skill'],b'\xFF'))),
                dict(writes=((11,DATA['score'],b'\xFF'),(11,DATA['numbers']+8,bytes.fromhex('ffffcdab')))))])
        finally:
            m.close()
    need(rows[0]==rows[1],'current full-state maximum/minimum and live renderer replies')
    return dict(images=2,cases_per_image=5,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw=(root/'.analysis/work/mainl-staff-verdict-build.json').read_bytes()
    report=json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-staff-verdict-current-review-v1','complete verdict report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),'current source / implementation / cold binding')
    need(report['pair_review_sha256']==sha(previous.REPORT.read_bytes()),'current prerequisite native staff proof')
    scope=report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'current complete raw / ordered native / ownership proof')
    need(scope['runtime']['native_geometry_proof']==geometry_proof(target)==geometry_proof(candidate),'current native fixed-loop and arithmetic proofs')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate entire unchanged source cold pair; rerun full verdict gates')
    options=parser.parse_args()
    report=dict(schema='th03-mainl-staff-verdict-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
                provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
                whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_staff_pair_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files=sound.images(ROOT)
    previous.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),pair_review_sha256=sha(previous.REPORT.read_bytes()),source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope']=dict(layout=layout(work,target,candidate,graph,files),negative_controls=negative_controls(target))
    save()
    report['scope']['runtime']=runtime(target,candidate)
    save()
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'verdict inputs changed during execution')
    report['complete']=True
    save()
    print('MAINL verdict: complete389-byte owner,25 literal fields,nine far calls and full live-state contracts pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
