#!/usr/bin/env python3
"""Review menu movement and the option caller on a source-bound OP cold pair."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import review_th03_op_story_work as story
from lib.op_option_layout import verify as layout
from lib.op_option_runtime import Machine,verify as runtime,negative_controls
ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/op-option-build.json'
INPUTS=(*story.INPUTS,'scripts/review_th03_op_option_work.py','scripts/lib/op_option_layout.py','scripts/lib/op_option_runtime.py')
def need(v,m):
    if not v:raise ValueError('OP option review: '+str(m))
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}
def witness(s):
    l,r,c=s['layout'],s['runtime'],s['negative_controls']
    need((l['functions'],l['code_bytes'],l['instruction_bytes'],len(l['ordered_native_fields']),len(l['ordered_relocations']))==(2,595,595,65,9),'complete native ownership and literal field vectors')
    need(not any(l[k] for k in ('containing_producer_accepted','main_caller_accepted','whole_product_accepted')),'bounded disjoint source scope')
    need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['ignored_private_stack_bytes'])==(2,2,595,595,16570,64),'complete runtime dimensions')
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['executed_owner_bytes'],o['executed_nested_bytes']) for o in r['observations']]==[(0x1000,8285,{'move':4145,'option':4140},595,567),(0x3000,8285,{'move':4145,'option':4140},595,567)] and all(re.fullmatch('[0-9a-f]{64}',o['trace_sha256']) and o['maximum_stack_depth']<=64 for o in r['observations']),'two full owner/nested coverage and bounded stack witnesses')
    need(r['exhaustive_BYTE_lanes']==['selection','maximum','direction','rank','bgm','key'] and r['real_nested_helpers'] and not r['main_caller_accepted'] and not r['whole_product_accepted'],'separate exhaustive BYTE lanes and actual nested execution')
    need(c['count']==c['actual_instruction_mutations']==len(set(c['rejected']))==35 and not c['data_mutations'],'35 actual instruction controls')
def smoke(target,candidate):
    rows=[]
    for image in (target,candidate):
        m=Machine(image,0x3000)
        try:rows.append([m.run('move',selection=127,direction=0x5A01,maximum=0xA503),m.run('move',selection=128,direction=0,maximum=0xA580,callback='main'),m.run('option',initialized=0,flags=0xED7,stack=0x80),m.run('option',input=0x302F,selection=2),m.run('option',input=12,selection=1,driver_ax=0x12FF,midi=2),m.run('option',input=8,selection=1,disabled=255)])
        finally:m.close()
    need(rows[0]==rows[1],'current BYTE/padding/input/driver/full-state smoke')
    return dict(images=2,cases_per_image=6,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)
def current_scope(root,work,target,candidate,cold_raw):
    raw=(root/'.analysis/work/op-option-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-op-option-current-review-v1','complete option review')
    need(r['implementation_sha256']==inputs(root),'current source/model drift')
    need(r['cold_report_sha256']==sha(cold_raw) and r['story_review_sha256']==sha(story.REPORT.read_bytes()),'current native/prerequisite binding')
    s=r['scope'];need(s['layout']==layout(work,target,candidate),'current complete native menu ownership');witness(s)
    return dict(**s,review_sha256=sha(raw),current_smoke=smoke(target,candidate))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--current-cold',action='store_true',help='revalidate the entire existing source/SDK/recipe/output pair; rerun all new gates');o=p.parse_args()
    r=dict(schema='th03-op-option-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),provenance='candidate-local-attested',native_pair_built_now=not o.current_cold,canonical_unit_credit_changed=False,whole_product_accepted=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_op_story_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw=story.vs.render.helpers.sound.attract.dispatch.cfg.images(ROOT);story.current_scope(ROOT,work,target,candidate,raw)
    r.update(cold_report_sha256=sha(raw),story_review_sha256=sha(story.REPORT.read_bytes()),source_inventory_sha256=story.vs.render.helpers.sound.attract.dispatch.digest(cold['source_sha256']))
    r['scope']=dict(layout=layout(work,target,candidate),runtime=runtime(target,candidate),negative_controls=negative_controls(target));witness(r['scope'])
    need(r['implementation_sha256']==inputs(ROOT),'inputs changed during review');r['complete']=True;save();print('OP option: two complete functions / 595 CODE bytes; native, full-state and mutation gates pass',flush=True);return 0
if __name__=='__main__':raise SystemExit(main())
