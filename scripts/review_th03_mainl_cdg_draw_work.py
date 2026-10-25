#!/usr/bin/env python3
"""Review the complete MAINL CDG blitters with real SMC and GRCG setup."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_cdg_work as cdg
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_cdg_draw_layout import PRODUCERS, verify as layout
from lib.decoded_mainl_cdg_draw_runtime import Machine, verify as runtime, negative_controls, geometry_proof

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'.analysis/work/mainl-cdg-draw-build.json'
INPUTS = (*cdg.INPUTS,'scripts/review_th03_mainl_cdg_draw_work.py','scripts/lib/decoded_mainl_cdg_draw_layout.py',
          'scripts/lib/decoded_mainl_cdg_draw_runtime.py',*tuple(p[1] for p in PRODUCERS))
COUNTS = dict(alpha=1123,hflip=1903,noalpha=1123)
ZERO = dict(alpha=dict(graph_stores=262144,rows=5,color_planes=4,maximum_inner_iterations=65536,SMC_WORD_writes=5),
            hflip=dict(graph_stores=327680,rows=5,color_planes=4,maximum_inner_iterations=65536,SMC_WORD_writes=6),
            noalpha=dict(graph_stores=0,rows=4,color_planes=4,maximum_inner_iterations=0,SMC_WORD_writes=1))


def need(value,message):
    if not value:
        raise ValueError('MAINL CDG draw review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    r = scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['ignored_stack_bytes'])
         ==(2,3,493,493,8298,0),'complete three-function / physical-memory dimensions')
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['executed_owner_bytes'],o['actual_color_helper_bytes'],
           o['maximum_stack_depth'],o['zero_width_terminal_summaries']) for o in r['observations']]
         ==[(0x1000,4149,COUNTS,493,41,16,ZERO),(0x3000,4149,COUNTS,493,41,16,ZERO)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) and o['flat_graph_stores']>600000 for o in r['observations']),
         'all native helpers / full zero-counter iterations / complete terminal frames')
    p = r['native_geometry_proof']
    need((p['WORD_width_states'],p['WORD_origin_states'],p['WORD_segment_states'],p['row_delta_mod_WORD'],
          p['maximum_rows_per_plane'],p['maximum_color_planes'],p['LOOP_zero_counter_iterations'],p['REP_zero_counter_iterations'])
         ==(65536,65536,65536,0xFFB0,411,26,65536,0) and not p['budget_expiry_used'] and not p['nonterminal_claim'],
         'native row/plane recurrence and finite zero-width LOOP proof')
    need(r['actual_owned_color_helper'] and r['flat_memory_operand_contract']
         and not r['physical_GRCG_or_pixels_emulated'] and not r['external_LUT_owned'],'explicit software/bus versus physical-device boundary')
    l = scope['layout']
    need((l['functions'],l['code_bytes'],l['ordered_native_field_count'],l['mz_relocation_count'],l['self_modifying_WORDs'],l['natural_producer_bytes'])
         ==(3,493,19,2,12,496) and l['excluded_outer_EVEN_bytes']==[0x2A7,0x371,0xFA3]
         and not l['enclosing_alignment_accepted'] and not l['lookup_or_hardware_accepted'] and not l['whole_product_accepted'],
         'whole native producer geometry and separate natural alignment')
    c = scope['negative_controls']
    need(c['count']==len(set(c['rejected']))==59 and (c['owner_instruction_mutations'],c['actual_color_helper_mutations'])==(58,1)
         and c['actual_guest_instruction_mutations'] and not c['alignment_mutations_counted'],'actual blitter/helper instruction controls')


def smoke(target,candidate):
    rows = []
    for image in (target,candidate):
        m = Machine(image,0x3000)
        try:
            rows.append([m.run(k,**p) for k,p in (
                ('alpha',dict(width=3,bottom=160,left=0xFFFF,top=399,flags=0xED7)),
                ('hflip',dict(width=0x4001,lookup='xor',top=1638,ss=0x8000,stack=0x80,flags=0xED7)),
                ('noalpha',dict(width=0,flags=0xED7)))])
        finally:
            m.close()
    need(rows[0]==rows[1],'current independent SMC / bus / flags / actual-helper smoke')
    return dict(images=2,cases_per_image=3,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw = (root/'.analysis/work/mainl-cdg-draw-build.json').read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-cdg-draw-current-review-v1','complete draw report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),'current source / implementation / cold binding')
    need(report['cdg_review_sha256']==sha(cdg.REPORT.read_bytes()),'current prerequisite loader proof')
    scope = report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'current complete native draw ownership')
    need(scope['runtime']['native_geometry_proof']==geometry_proof(target)==geometry_proof(candidate),'current native geometry binding')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate the entire unchanged cold pair; rerun new blitter gates')
    options = parser.parse_args()
    report = dict(schema='th03-mainl-cdg-draw-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
                  provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
                  whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_cdg_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files = sound.images(ROOT)
    cdg.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),cdg_review_sha256=sha(cdg.REPORT.read_bytes()),
                  source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope'] = dict(layout=layout(work,target,candidate,graph,files),runtime=runtime(target,candidate),
                           negative_controls=negative_controls(target))
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'draw inputs changed during execution')
    report['complete'] = True
    save()
    print('MAINL CDG draw: three complete functions / 493 CODE bytes; real SMC, nested GRCG instructions and complete bus contracts pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
