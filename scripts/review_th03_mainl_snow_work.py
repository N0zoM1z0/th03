#!/usr/bin/env python3
"""Review all seven complete MAINL snow procedures and real nested contexts."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_staff_draw_work as staff
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_snow_layout import verify as layout
from lib.decoded_mainl_snow_runtime import Machine, verify as runtime, geometry_proof, negative_controls

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT/'.analysis/work/mainl-snow-build.json'
INPUTS = (*staff.INPUTS,'scripts/review_th03_mainl_snow_work.py','scripts/lib/decoded_mainl_snow_layout.py',
          'scripts/lib/decoded_mainl_snow_runtime.py')
COUNTS = dict(clear=32,reset=272,spawn=35934,update=2909,render=2397,gate=4117,tick=1904)
CONTROLS = dict(clear=5,reset=5,spawn=21,update=12,render=6,gate=8,tick=12)


def need(value,message):
    if not value:
        raise ValueError('MAINL snow review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    r,l,c = scope['runtime'],scope['layout'],scope['negative_controls']
    need((r['images'],r['extents'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['ignored_stack_bytes'])
         ==(2,1,7,464,464,95130,0),'complete one-extent / seven-procedure dimensions')
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['executed_owner_bytes'],o['actual_context_bytes'],
           o['maximum_stack_depth'],o['nonterminal_prefix_cases'],o['terminal_cases'],o['maximum_actual_calls'],o['actual_vector_pairs'])
          for o in r['observations']]==[(load,47565,COUNTS,464,187,32,18,47547,dict(rand=1020,vector=255,flake=255),2048)
                                      for load in (0x1000,0x3000)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),
         'all real helpers / full seed-output and angle-length matrices / checked terminal and prefix cases')
    p = r['native_geometry_proof']
    need((p['BYTE_capacity_states'],p['maximum_loop_iterations'],p['clear_WORD_stores'],p['reset_alive_BYTES'],
          p['masked_random_output_states'],p['maximum_rand_calls_per_spawn'],p['maximum_vector_calls_per_spawn'],
          p['maximum_flake_calls_per_render'],p['maximum_render_WORD_stores'])==(256,255,16000,80,32768,1020,255,255,2040)
         and (p['closed_poll']['segment'],p['closed_poll']['offset'],p['closed_poll']['bytes'],p['closed_poll']['counter_value'])
         ==(0x95F,0x270E,7,0) and len(p['closed_poll']['cfg_instructions'])==2 and p['closed_poll']['assumptions']
         and not p['budget_expiry_used'] and not p['guest_iterations_skipped'] and not p['physical_IRQ_or_timing_proved'],
         'native finite bounds and conditional immutable-zero closed CFG')
    need(r['actual_owned_RNG_and_flake'] and r['actual_vector_context'] and r['actual_context_bytes']==187
         and not r['vector_library_or_tables_owned'] and not r['physical_IRQ_audio_pixels_or_timing_proved'],
         'explicit vector/table/PMD/counter/device boundary')
    need((l['extents'],l['functions'],l['code_bytes'],len(l['procedures']),len(l['ordered_native_fields']),l['mz_relocation_count'])
         ==(1,7,464,7,27,6) and l['owners'][0]['procedure_count']==7
         and not l['enclosing_DATA_or_other_functions_accepted'] and not l['library_vector_or_tables_accepted']
         and not l['physical_runtime_or_assets_accepted'] and not l['whole_product_accepted'],'complete native bodies / literal fields / reviewed ownership')
    need(c['count']==len(set(c['rejected']))==72 and c['owner_instruction_mutations']==69 and c['by_function']==CONTROLS
         and c['actual_context_instruction_mutations']==3 and c['actual_guest_instruction_mutations']
         and not c['unowned_DATA_mutations_counted'],'actual snow/context instruction controls')


def smoke(target,candidate):
    rows = []
    for image in (target,candidate):
        m = Machine(image,0x3000)
        try:
            rows.append([m.run(kind,**parameters) for kind,parameters in (
                ('spawn',dict(cap=2,frame=8,alive='none',table='signed',flags=0xED7)),
                ('gate',dict(active=255,pmd_measure=0xFFFF,pmd_writes=((0x27C2,b'\xC1\0'),))),
                ('tick',dict(cap=81,frame=640,alive='none',vsync=2,ticks=(0,1),ss=0x8000,stack=0x80)),
                ('tick',dict(cap=0,vsync=0,ticks=None,prefix=3,flags=0xED7)))])
        finally:
            m.close()
    need(rows[0]==rows[1],'current full-state nested / live-alias / closed-cycle smoke')
    return dict(images=2,cases_per_image=4,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw = (root/'.analysis/work/mainl-snow-build.json').read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-snow-current-review-v1','complete snow report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),'current maintained source / implementation / cold binding')
    need(report['staff_review_sha256']==sha(staff.REPORT.read_bytes()),'current owned flake / enclosing staff producer proof')
    scope = report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'current complete raw / ordered native / ownership proof')
    need(scope['runtime']['native_geometry_proof']==geometry_proof(target)==geometry_proof(candidate),'current native loop / closed-cycle binding')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate the entire unchanged cold pair; rerun complete snow gates')
    options = parser.parse_args()
    report = dict(schema='th03-mainl-snow-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
                  provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
                  whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_staff_draw_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files = sound.images(ROOT)
    staff.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),staff_review_sha256=sha(staff.REPORT.read_bytes()),
                  source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope'] = dict(layout=layout(work,target,candidate,graph,files),runtime=runtime(target,candidate),
                           negative_controls=negative_controls(target))
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'snow inputs changed during execution')
    report['complete'] = True
    save()
    print('MAINL snow: seven complete functions / one464-byte extent; actual187 context bytes and full-state terminal/closed-cycle contracts pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
