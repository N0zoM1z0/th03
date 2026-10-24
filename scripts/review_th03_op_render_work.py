#!/usr/bin/env python3
"""Review three complete OP renderers against the current source-only cold pair."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import review_th03_op_helpers_work as helpers
from lib.op_render_layout import verify as layout
from lib.op_render_runtime import Machine,verify as runtime,negative_controls
ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/op-render-build.json'
INPUTS=(*helpers.INPUTS,'scripts/review_th03_op_render_work.py','scripts/lib/op_render_layout.py','scripts/lib/op_render_runtime.py','src/op/menu/menu_state.inl')
def need(v,m):
    if not v:raise ValueError('OP renderer review: '+m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}
def witness(s):
    r=s['runtime'];need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['inline_non_instruction_bytes'],r['cases_per_image'],r['exhaustive_option_BYTE_states'])==(2,3,518,509,9,11622,256),'complete renderer runtime dimensions')
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['executed_owner_bytes'],o['inline_non_instruction_bytes'],o['maximum_observed_stack_depth'],o['maximum_library_calls']) for o in r['observations']]
        ==[(0x1000,5811,{'vs':657,'main':657,'option':4497},509,9,20,3),(0x3000,5811,{'vs':657,'main':657,'option':4497},509,9,20,3)]
        and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'complete renderer path/stack/library witnesses')
    c=s['negative_controls'];need(c['count']==len(set(c['rejected']))==24,'twenty-four actual renderer mutations')
    l=s['layout'];need(l['functions']==3 and l['code_bytes']==518 and l['instruction_bytes']==509 and l['inline_non_instruction_bytes']==9 and len(l['ordered_native_fields'])==39 and len(l['ordered_relocations'])==7 and not l['containing_producer_accepted'] and not l['whole_product_accepted'],'bounded complete native renderer ownership with inline data separate')
def smoke(target,candidate):
    rows=[]
    for image in (target,candidate):
        m=Machine(image,0x3000)
        try:rows.append([
            m.run('vs',selection=0xFFFF,attribute=0xF3A5),m.run('main',selection=0x100),m.run('main',selection=5,flags=0xED7),
            m.run('option',selection=0,rank=3,attribute=0),m.run('option',selection=0,rank=255,resoff=0xFF80,resseg=0x5000),
            m.run('option',selection=1,bgm=255),m.run('option',selection=2,key=2),m.run('option',selection=0xFFFF)])
        finally:m.close()
    need(rows[0]==rows[1],'current renderer WORD/BYTE/request/return smoke')
    return dict(images=2,cases_per_image=8,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)
def current_scope(root,work,target,candidate,cold_raw):
    raw=(root/'.analysis/work/op-render-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-op-render-current-review-v1','complete renderer report')
    need(r['implementation_sha256']==inputs(root),'renderer implementation/source drift')
    need(r['cold_report_sha256']==sha(cold_raw) and r['helpers_review_sha256']==sha(helpers.REPORT.read_bytes()),'current cold/helpers binding')
    s=r['scope'];need(s['layout']==layout(work,target,candidate),'current complete native renderer ownership');witness(s)
    return dict(**s,review_sha256=sha(raw),current_smoke=smoke(target,candidate))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--current-cold',action='store_true',help='revalidate the complete existing source/SDK/recipe/output pair; rerun all renderer gates');o=p.parse_args()
    r=dict(schema='th03-op-render-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),provenance='candidate-local-attested',native_pair_built_now=not o.current_cold,whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_op_helpers_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw=helpers.sound.attract.dispatch.cfg.images(ROOT);helpers.current_scope(ROOT,work,target,candidate,raw)
    r['cold_report_sha256']=sha(raw);r['helpers_review_sha256']=sha(helpers.REPORT.read_bytes());r['source_inventory_sha256']=helpers.sound.attract.dispatch.digest(cold['source_sha256'])
    r['scope']=dict(layout=layout(work,target,candidate),runtime=runtime(target,candidate),negative_controls=negative_controls(target));witness(r['scope'])
    need(r['implementation_sha256']==inputs(ROOT),'renderer inputs changed during review');r['complete']=True;save()
    print('OP renderers: three complete functions / 518 CODE bytes; 509 instruction bytes and nine inline non-instruction bytes; cold/native/runtime gates pass',flush=True);return 0
if __name__=='__main__':raise SystemExit(main())
