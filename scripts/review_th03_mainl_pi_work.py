#!/usr/bin/env python3
"""Review five complete MAINL PI callers with real nested native context."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import review_th03_mainl_pi_free_work as free
import review_th03_mainl_sound_work as sound
from lib.decoded_mainl_pi_layout import PRODUCERS, verify as layout
from lib.decoded_mainl_pi_runtime import Machine, verify as runtime, negative_controls, closed_prefix_proof

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / '.analysis/work/mainl-pi-build.json'
INPUTS = (*free.INPUTS, 'scripts/review_th03_mainl_pi_work.py', 'scripts/lib/decoded_mainl_pi_layout.py',
          'scripts/lib/decoded_mainl_pi_runtime.py', *tuple(p[1] for p in PRODUCERS))
COUNTS = dict(palette=585,put=761,interlace=833,load=675,quarter=112)


def need(value,message):
    if not value:
        raise ValueError('MAINL PI review: '+message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def witness(scope):
    r = scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['ignored_stack_bytes'])
         ==(2,5,555,555,5932,0), 'complete five-procedure / full-memory dimensions')
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['nonterminal_prefixes'],o['executed_owner_bytes'],
           o['nested_release_bytes'],o['library_context_bytes'],o['maximum_stack_depth']) for o in r['observations']]
         ==[(0x1000,2966,COUNTS,72,555,76,35,26),(0x3000,2966,COUNTS,72,555,76,35,26)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) and o['checked_far_frames']>20000 for o in r['observations']),
         'native paths / real nested release / CRT / exact far frames')
    p = r['closed_interlace_prefix']
    need(p['native_CFG_proved'] and not p['budget_expiry_used'] and p['only_exit_guard_always_taken']
         and (p['guard'],p['backedge'],p['counter_step'],p['invariant_counter_states'],p['readonly_height'])
         ==(0x64A,0x656,2,32768,65535) and len(p['assumptions'])==3 and len(p['live_invariant'])==4,
         'inductive live-state / closed native CFG prefix proof')
    need(r['far_return_words_checked_at_entry'] and not r['heap_decoder_or_pixels_executed']
         and not r['library_context_accepted'], 'explicit library / heap / decoder / graphics boundaries')
    c = scope['negative_controls']
    need(c['count']==len(set(c['rejected']))==49 and (c['owner_instruction_mutations'],c['nested_release_mutations'],c['library_context_mutations'])
         ==(46,1,2) and c['actual_guest_instruction_mutations'], 'actual owner and contextual instruction controls')
    l = scope['layout']
    need((l['functions'],l['code_bytes'],l['ordered_native_fields'],l['mz_relocation_count'])==(5,555,25,7)
         and not l['library_context_accepted'] and not l['whole_product_accepted'], 'complete raw owners and literal ordered fields')


def smoke(target,candidate):
    rows = []
    for image in (target,candidate):
        machine = Machine(image,0x3000)
        try:
            rows.append([machine.run(k,**p) for k,p in (
                ('palette',dict(slot=0xFFFF,flags=0xED7)),('load',dict(segments=(0,0),pointer=(0xFFFF,0),status=7)),
                ('put',dict(pointer=(0xFFFF,0xFFFF),width=0xFFFF,height=3,ss=0x8000,stack=0x80)),
                ('interlace',dict(height=0xFFFF,prefix=4,clear_df=True)),('quarter',dict(quarter=3,top=0x7FFF)))])
        finally:
            machine.close()
    for row in rows:
        for result in row:
            result.pop('far_return_WORD_write_hooks')
    need(rows[0]==rows[1],'current independent PI / nested frame / live-prefix smoke')
    return dict(images=2,cases_per_image=5,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw = (root/'.analysis/work/mainl-pi-build.json').read_bytes()
    report = json.loads(raw)
    need(report['complete'] and report['schema']=='th03-mainl-pi-current-review-v1','complete PI report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw), 'live implementation / source / cold binding')
    need(report['pi_free_review_sha256']==sha(free.REPORT.read_bytes()),'current prerequisite release proof')
    scope = report['scope']
    need(scope['layout']==layout(work,target,candidate,graph,files),'current complete native ownership')
    need(scope['runtime']['closed_interlace_prefix']==closed_prefix_proof(target)==closed_prefix_proof(candidate),'current literal CFG proof')
    witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate the entire unchanged cold pair; rerun all PI contracts')
    options = parser.parse_args()
    report = dict(schema='th03-mainl-pi-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
                  provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
                  whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():
        REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_mainl_pi_free_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files = sound.images(ROOT)
    free.current_scope(ROOT,work,target,candidate,raw,graph,files)
    report.update(cold_report_sha256=sha(raw),pi_free_review_sha256=sha(free.REPORT.read_bytes()),
                  source_inventory_sha256=sound.digest(cold['source_sha256']))
    report['scope'] = dict(layout=layout(work,target,candidate,graph,files),runtime=runtime(target,candidate),
                           negative_controls=negative_controls(target))
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'PI inputs changed during execution')
    report['complete'] = True
    save()
    print('MAINL PI: five complete functions / 555 CODE bytes; cold/native/full-state contracts pass')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
