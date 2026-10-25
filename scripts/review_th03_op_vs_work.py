#!/usr/bin/env python3
"""Review the complete OP VS caller against a source-bound native cold pair."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import review_th03_op_render_work as render
from lib.op_vs_layout import verify as layout
from lib.op_vs_runtime import Machine,verify as runtime,negative_controls

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/op-vs-build.json'
INPUTS=(*render.INPUTS,'scripts/review_th03_op_vs_work.py','scripts/lib/op_vs_layout.py',
        'scripts/lib/op_vs_runtime.py','src/op/menu/title_animation.inl')

def need(value,message):
    if not value:raise ValueError('OP VS review: '+message)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {name:sha((root/name).read_bytes()) for name in INPUTS}

def witness(scope):
    r=scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],
          r['executed_nested_bytes'],r['cases_per_image'],r['exhaustive_mode_bytes'],
          r['exhaustive_selection_result_bytes'],r['exhaustive_sound_state_bytes'])
         ==(2,1,365,365,331,3778,256,256,256),'complete caller/runtime dimensions')
    need([(o['load_segment'],o['cases'],o['ordinary_menu_cases'],o['post_match_cases'],
           o['covered_owner_bytes'],o['executed_nested_bytes'],o['maximum_observed_stack_depth'],
           o['maximum_polls'],o['maximum_actual_delay_calls']) for o in r['observations']]
         ==[(0x1000,1889,993,896,365,331,28,64,76),(0x3000,1889,993,896,365,331,28,64,76)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),
         'complete ordinary/post-match paths, stack and finite device witnesses')
    need(not r['character_selection_implementations_executed'] and not r['physical_timing_or_pixels_emulated'],
         'bounded character-selection/device interfaces')
    c=scope['negative_controls']
    need(c['count']==len(set(c['rejected']))==31 and c['actual_guest_mutations']
         and not c['character_selection_code_mutated'] and not c['payload_bytes_patched'],
         'thirty-one actual caller/helper instruction mutations')
    l=scope['layout']
    need(l['functions']==1 and l['code_bytes']==365 and len(l['ordered_native_fields'])==23
         and len(l['ordered_relocations'])==7 and l['box_dependency']['size']==44
         and not l['box_dependency']['source_credit_added'] and not l['character_selection_procedures_owned']
         and not l['containing_producer_accepted'] and not l['whole_product_accepted'],
         'complete bounded caller ownership and separate box dependency')

def smoke(target,candidate):
    rows=[]
    for image in (target,candidate):
        m=Machine(image,0x3000)
        try:
            rows.append([m.run(**p) for p in (
                dict(mode=129,samples=(),selection_ax=0x100),
                dict(mode=255,samples=(),selection_ax=0xA580,resoff=0xFF80),
                dict(samples=((0x21,0,0,0),)),
                dict(samples=((0x4000,0,0,0),(0x20,0,0,0),(0,0,0,0),(0x2000,0,0,0)),selection_ax=0),
                dict(samples=((3,0,0,0),(0,0,0,0),(0x20,0,0,0)),selection_ax=0,status=0x8000),
                dict(mode=130,samples=(),selection_ax=0,flags=0xED7,active=255,midi=255,stack=0x80))])
        finally:m.close()
    need(rows[0]==rows[1],'current VS entry/input/AL/cleanup smoke')
    return dict(images=2,cases_per_image=6,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),
                full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)

def current_scope(root,work,target,candidate,cold_raw):
    raw=(root/'.analysis/work/op-vs-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-op-vs-current-review-v1','complete VS report')
    need(r['implementation_sha256']==inputs(root),'VS implementation/source drift')
    need(r['cold_report_sha256']==sha(cold_raw) and r['renderer_review_sha256']==sha(render.REPORT.read_bytes()),
         'current cold/renderer binding')
    s=r['scope'];need(s['layout']==layout(work,target,candidate),'current complete native caller ownership');witness(s)
    return dict(**s,review_sha256=sha(raw),current_smoke=smoke(target,candidate))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--current-cold',action='store_true',help='revalidate existing source/SDK/recipe/output pair; rerun every new VS gate')
    o=p.parse_args()
    r=dict(schema='th03-op-vs-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
           provenance='candidate-local-attested',native_pair_built_now=not o.current_cold,
           whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_op_render_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw=render.helpers.sound.attract.dispatch.cfg.images(ROOT)
    render.current_scope(ROOT,work,target,candidate,raw)
    r['cold_report_sha256']=sha(raw);r['renderer_review_sha256']=sha(render.REPORT.read_bytes())
    r['source_inventory_sha256']=render.helpers.sound.attract.dispatch.digest(cold['source_sha256'])
    r['scope']=dict(layout=layout(work,target,candidate),runtime=runtime(target,candidate),negative_controls=negative_controls(target))
    witness(r['scope']);need(r['implementation_sha256']==inputs(ROOT),'VS inputs changed during review')
    r['complete']=True;save()
    print('OP VS: one complete caller / 365 CODE bytes; native ownership and independent runtime gates pass',flush=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
