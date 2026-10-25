#!/usr/bin/env python3
"""Review the complete story caller on the current source-bound OP cold pair."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import review_th03_op_vs_work as vs
from lib.op_story_layout import verify as layout
from lib.op_story_runtime import Machine,verify as runtime,negative_controls

ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/op-story-build.json'
INPUTS=(*vs.INPUTS,'scripts/review_th03_op_story_work.py','scripts/lib/op_story_layout.py','scripts/lib/op_story_runtime.py')
def need(v,m):
    if not v:raise ValueError('OP story review: '+m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}

def witness(scope):
    r=scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['cases_per_image'],r['executed_owner_bytes'],r['executed_nested_bytes'])
         ==(2,1,390,6748,390,206),'complete caller and nested runtime dimensions')
    need([(o['load_segment'],o['cases'],o['ordinary_cases'],o['actual_consecutive_reentry_cases'],
           o['covered_owner_bytes'],o['executed_nested_bytes'],o['maximum_observed_stack_depth']) for o in r['observations']]
         ==[(0x1000,3374,3347,27,390,206,26),(0x3000,3374,3347,27,390,206,26)]
         and all((o['terminal_cases'],o['nonterminal_cases'],o['retry_paths'],o['maximum_actual_random_calls'])==(2832,542,158,66)
                 and re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),
         'two complete returning/retry/closed-loop witnesses and actual reentry')
    need(all(r[k]==256 for k in ('exhaustive_selected_character_BYTE','exhaustive_selection_AL','exhaustive_rank_BYTE',
        'exhaustive_sound_state_BYTE','exhaustive_each_seed_BYTE_lane')) and r['seen_masks']==128
        and r['closed_nonterminal_candidate_domain']==7 and r['maximum_private_stack_window']==48
        and not r['all_32bit_seeds_termination_proved'] and not r['character_selection_implementation_executed']
        and not r['successful_exec_or_physical_hardware_emulated'],'bounded state and device/selection contracts')
    c=scope['negative_controls']
    need(c['count']==len(set(c['rejected']))==40 and c['actual_guest_instruction_mutations']
        and not c['source_or_payload_patched'] and not c['character_selection_code_mutated'],'forty actual instruction controls')
    l=scope['layout']
    need(l['functions']==1 and l['code_bytes']==390 and len(l['ordered_native_fields'])==22
        and len(l['ordered_relocations'])==5 and len(l['blocked_candidate_CFG'])==11
        and l['library_random_dependency_bytes']==42 and l['reviewed_initialized_dependency_bytes']==139
        and not l['library_random_source_credit_added'] and not l['character_selection_procedure_owned']
        and not l['containing_producer_accepted'] and not l['whole_product_accepted'],'complete bounded native ownership')

def smoke(target,candidate):
    observations=[]
    for image in (target,candidate):
        m=Machine(image,0x3000)
        try:observations.append([
            m.run(selected_char=17,rank=255,random_seed=0xFFFF0000,flags=0xED7,stack=0x80),
            m.run(selected_char=17,rank=255,random_seed=0xFFFF0000,reenter=True),
            m.run(selection_ax=0xA580,reenter=True),m.run(selected_char=21,resoff=0xFF80)])
        finally:m.close()
    need(observations[0]==observations[1],'current terminal/nonterminal/reentry/AL ABI smoke')
    return dict(images=2,cases_per_image=4,trace_sha256=sha(json.dumps(observations[0],sort_keys=True).encode()),
        full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)

def current_scope(root,work,target,candidate,cold_raw):
    raw=(root/'.analysis/work/op-story-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-op-story-current-review-v1','complete story review')
    need(r['implementation_sha256']==inputs(root),'complete current source/model bindings')
    need(r['cold_report_sha256']==sha(cold_raw) and r['vs_review_sha256']==sha(vs.REPORT.read_bytes()),'current native/VS prerequisite binding')
    s=r['scope'];need(s['layout']==layout(work,target,candidate),'complete current native caller ownership');witness(s)
    return dict(**s,review_sha256=sha(raw),current_smoke=smoke(target,candidate))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--current-cold',action='store_true',help='revalidate complete source/SDK/recipe/output pair and rerun every new story gate');o=p.parse_args()
    r=dict(schema='th03-op-story-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        provenance='candidate-local-attested',native_pair_built_now=not o.current_cold,canonical_unit_credit_changed=False,whole_product_accepted=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_op_vs_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw=vs.render.helpers.sound.attract.dispatch.cfg.images(ROOT)
    vs.current_scope(ROOT,work,target,candidate,raw)
    r.update(cold_report_sha256=sha(raw),vs_review_sha256=sha(vs.REPORT.read_bytes()),
        source_inventory_sha256=vs.render.helpers.sound.attract.dispatch.digest(cold['source_sha256']))
    r['scope']=dict(layout=layout(work,target,candidate),runtime=runtime(target,candidate),negative_controls=negative_controls(target))
    witness(r['scope']);need(r['implementation_sha256']==inputs(ROOT),'story inputs changed during execution')
    r['complete']=True;save();print('OP story: complete near caller / 390 CODE bytes; native, full-state, reentry and mutation gates pass',flush=True)
    return 0
if __name__=='__main__':raise SystemExit(main())
