#!/usr/bin/env python3
"""Review complete MAINL flake/unput owners and unchecked native bus effects."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_ending_work as ending
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_staff_draw_layout import verify as layout
from lib.decoded_mainl_staff_draw_runtime import Machine, verify as runtime, geometry_proof, negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'.analysis/work/mainl-staff-draw-build.json'
INPUTS = (*ending.INPUTS,'scripts/review_th03_mainl_staff_draw_work.py',
          'scripts/lib/decoded_mainl_staff_draw_layout.py','scripts/lib/decoded_mainl_staff_draw_runtime.py')


def need(value,message):
    if not value:
        raise ValueError('MAINL staff draw review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    r,l,c = scope['runtime'],scope['layout'],scope['negative_controls']
    need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['ignored_stack_bytes'])
         ==(2,2,199,199,25612,0),'complete two-procedure physical-memory dimensions')
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['executed_owner_bytes'],o['maximum_stack_depth_by_function'],
           o['minimum_unput_WORD_stores'],o['maximum_unput_WORD_stores']) for o in r['observations']]
         ==[(load,12806,dict(flake=10051,unput=2755),199,dict(flake=6,unput=10),0,12285) for load in (0x1000,0x3000)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) and o['graph_WORD_stores']>2000000 for o in r['observations']),
         'all native bytes, complete zero/maximal counts and real caller frames')
    p = r['native_geometry_proof']
    need((p['WORD_index_states'],p['distinct_flake_source_offsets'],p['flake_rows'],p['WORD_dimension_states'],
          p['maximum_unput_WORDs_per_row'],p['unput_rows'],p['maximum_unput_WORD_stores'],p['zero_REP_iterations'])
         ==(65536,4096,8,65536,4095,3,12285,0) and p['DF_clear_row_delta']==80
         and p['DF_set_row_delta']=='80 - 4 * (unsigned_width >> 4), modulo WORD'
         and not p['budget_expiry_used'] and not p['nonterminal_claim'],'complete native WORD recurrence proof')
    need(r['caller_argument_stores_checked'] and r['flat_memory_operand_contract'] and r['helper_interfaces']==0
         and not r['sprite_assets_or_physical_graphics_owned'],'whole caller arguments / explicit external DATA and hardware boundary')
    need((l['functions'],l['code_bytes'],len(l['ordered_native_fields']),l['mz_relocation_count'])==(2,199,3,0)
         and (l['enclosing_CODE_bytes'],l['enclosing_initialized_DATA_bytes'],l['enclosing_BSS_bytes'],l['enclosing_procedures'])==(3695,224,0,19)
         and not l['enclosing_DATA_or_other_functions_accepted'] and not l['sprite_assets_or_physical_graphics_accepted']
         and not l['whole_product_accepted'],'complete native owner fields and separate enclosing TU/DATA')
    need(c['count']==len(set(c['rejected']))==37 and (c['flake_instruction_mutations'],c['unput_instruction_mutations'])==(17,20)
         and c['actual_guest_instruction_mutations'] and not c['unowned_data_mutations_counted'],'actual owner instruction controls')


def smoke(target,candidate):
    rows = []
    for image in (target,candidate):
        m = Machine(image,0x3000)
        try:
            rows.append([m.run(kind,**parameters) for kind,parameters in (
                ('flake',dict(left=0xFFFF,index=0xFFFF,source_word=0x8001,flags=0xED7)),
                ('unput',dict(width=0,height=0xFFFF,left=0x8000,flags=0xED7,ss=0x8000,stack=0x80)),
                ('unput',dict(width=0x801,height=0x8001,top=0xFFFF,flags=0xED7)))])
        finally:
            m.close()
    need(rows[0]==rows[1],'current independent near-Pascal / flat-WORD memory smoke')
    return dict(images=2,cases_per_image=3,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw = (root/'.analysis/work/mainl-staff-draw-build.json').read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-staff-draw-current-review-v1','complete staff drawing report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),'current maintained source / implementation / cold binding')
    need(report['ending_review_sha256']==sha(ending.REPORT.read_bytes()),'current enclosing ending/TU proof')
    scope = report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'current complete native owner bytes / fields / layout')
    need(scope['runtime']['native_geometry_proof']==geometry_proof(target)==geometry_proof(candidate),'current native recurrence binding')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate the unchanged entire cold pair; rerun staff drawing gates')
    options = parser.parse_args()
    report = dict(schema='th03-mainl-staff-draw-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
                  provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
                  whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_ending_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files = sound.images(ROOT)
    ending.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),ending_review_sha256=sha(ending.REPORT.read_bytes()),
                  source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope'] = dict(layout=layout(work,target,candidate,graph,files),runtime=runtime(target,candidate),
                           negative_controls=negative_controls(target))
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'staff drawing inputs changed during execution')
    report['complete'] = True
    save()
    print('MAINL staff draw: complete flake76/unput123 CODE bytes; native fields, all caller-frame bytes and independent bus contracts pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
