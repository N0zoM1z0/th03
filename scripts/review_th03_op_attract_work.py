#!/usr/bin/env python3
"""Fresh OP cold/cfg/dispatch chain and complete attract wait contracts."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import review_th03_op_dispatch_work as dispatch
from lib.op_attract_layout import verify as layout
from lib.op_attract_runtime import Machine,verify as runtime,negative_controls
ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/op-attract-build.json'
INPUTS=(*dispatch.INPUTS,'scripts/review_th03_op_attract_work.py','scripts/lib/op_attract_layout.py',
 'scripts/lib/op_attract_runtime.py','scripts/lib/shared_input_layout.py','scripts/lib/shared_input_runtime.py')
def need(v,m):
    if not v:raise ValueError('OP attract review: '+m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}
def witness(scope):
    r=scope['runtime'];need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['exhaustive_demo_bytes'])
        ==(2,1,105,105,1230,256),'complete attract runtime dimensions')
    need([(o['load_segment'],o['cases'],o['ordinary_entry_cases'],o['loop_continuation_cases'],o['covered_owner_bytes'],o['executed_nested_bytes'],o['maximum_observed_stack_depth'],o['maximum_sample_polls']) for o in r['observations']]
        ==[(0x1000,615,298,317,105,402,32,523),(0x3000,615,298,317,105,402,32,523)]
        and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'ordinary/continuation, load, nested coverage and stack witnesses')
    c=scope['negative_controls'];need(c['count']==len(set(c['rejected']))==21,'twenty-one actual attract mutations')
    need(not scope['layout']['containing_producer_accepted'] and not scope['layout']['whole_product_accepted'],'bounded attract ownership')
def smoke(target,candidate):
    rows=[]
    for mz in (target,candidate):
        m=Machine(mz,0x3000)
        try:rows.append([m.run(random=0xFFFFFFFF),m.run(present=1,samples=[(0,0,1,0),(0,0,0,4)]),
            m.run(continuation=520,demo=255),m.run(continuation=0x7FFF,flags=0xED7),m.run(continuation=0xFFFF,flags=2)])
        finally:m.close()
    need(rows[0]==rows[1],'current complete attract ABI / helper / counter smoke')
    return dict(cases_per_image=5,images=2,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)
def current_scope(root,work,target,candidate,cold_raw):
    raw=(root/'.analysis/work/op-attract-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-op-attract-current-review-v1','complete attract report')
    need(r['implementation_sha256']==inputs(root),'attract implementation/source drift')
    need(r['cold_report_sha256']==sha(cold_raw) and r['dispatch_review_sha256']==sha(dispatch.REPORT.read_bytes()),'current cold/dispatch binding')
    s=r['scope'];need(s['layout']==layout(work,target,candidate),'current complete native attract ownership');witness(s)
    return dict(**s,review_sha256=sha(raw),current_smoke=smoke(target,candidate))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--current-cold',action='store_true',help='revalidate current cold/cfg/dispatch prerequisites; rerun attract gates');o=p.parse_args()
    r=dict(schema='th03-op-attract-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),provenance='candidate-local-attested',
        native_pair_built_now=not o.current_cold,whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_op_dispatch_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,cold_raw=dispatch.cfg.images(ROOT);dispatch.current_scope(ROOT,work,target,candidate,cold_raw)
    r['cold_report_sha256']=sha(cold_raw);r['dispatch_review_sha256']=sha(dispatch.REPORT.read_bytes());r['source_inventory_sha256']=dispatch.digest(cold['source_sha256'])
    r['scope']=dict(layout=layout(work,target,candidate),runtime=runtime(target,candidate),negative_controls=negative_controls(target));witness(r['scope'])
    need(r['implementation_sha256']==inputs(ROOT),'attract inputs changed during review');r['complete']=True;save()
    print('OP attract: one whole near function / 105 CODE bytes; 402 actual nested bytes; cold/native/runtime gates pass',flush=True);return 0
if __name__=='__main__':raise SystemExit(main())
