#!/usr/bin/env python3
"""Fresh ZUN cold/formatter/graphics chain and eight driver lifecycle contracts."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import review_th03_zun_graphics_work as graphics
from review_th03_zun_format_work import images
from lib.zun_driver_lifecycle_layout import SOURCE,verify as layout
from lib.zun_driver_lifecycle_runtime import Machine,verify as runtime,negative_controls
ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/zun-lifecycle-build.json'
INPUTS=(*graphics.INPUTS,'scripts/review_th03_zun_lifecycle_work.py','scripts/lib/zun_driver_lifecycle_layout.py',
 'scripts/lib/zun_driver_lifecycle_runtime.py',SOURCE,'scripts/lib/zun_driver_command_runtime.py','scripts/lib/zun_driver_scalar_runtime.py','scripts/lib/zun_driver_scalar_layout.py')
def need(v,m):
    if not v:raise ValueError('ZUN lifecycle review: '+m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}
def witness(scope):
    r=scope['runtime'];need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['terminal_unreachable_owner_bytes'],r['cases_per_image'],r['exhaustive_vector_bytes'])
        ==(2,8,564,549,15,1826,256),'complete lifecycle runtime dimensions')
    need([(o['load_segment'],o['cases'],o['covered_owner_bytes'],o['terminal_unreachable_owner_bytes'],o['maximum_observed_stack_depth']) for o in r['observations']]
        ==[(0x1000,913,549,15,384),(0x3000,913,549,15,384)] and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'lifecycle load/coverage/stack witnesses')
    c=scope['negative_controls'];need(c['count']==len(set(c['rejected']))==25,'twenty-five actual lifecycle mutations')
    need(not scope['layout']['enclosing_driver_accepted'] and not scope['layout']['reserved_spans_owned'],'bounded lifecycle source classification')
def smoke(target,candidate):
    observations=[]
    for im in (target,candidate):
        m=Machine(im,0x3000)
        try:observations.append([
            m.run('allocate_buffers',paragraphs=0xFFFF),m.run('allocate_buffers',allocation_failure=1),
            m.run('set_interrupt_argument',arguments=(b'511',)),m.run('install',present=True),m.run('install',vector=0x80),
            m.run('uninstall',present=True,free_failures=15,split_stack=True),
            m.run('interrupt_dispatch',service=9,flags=0x402),m.run('entry',tail=b'-v 511\r',flags=0xED7)])
        finally:m.close()
    need(observations[0]==observations[1],'current independent lifecycle ABI/interface smoke')
    return dict(cases_per_image=8,images=2,trace_sha256=sha(json.dumps(observations[0],sort_keys=True).encode()),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)
def current_scope(root,work,target,candidate,at,files,maintained,cold):
    raw=REPORT.read_bytes();r=json.loads(raw);need(r['complete'] and r['schema']=='th03-zun-lifecycle-current-review-v1','complete lifecycle report')
    need(r['implementation_sha256']==inputs(root),'lifecycle implementation/source drift')
    need(r['cold_report_sha256']==sha(cold) and r['graphics_report_sha256']==sha(graphics.REPORT.read_bytes()),'current cold/graphics binding')
    s=r['scope'];need(s['layout']==layout(work,target,candidate,at,files,maintained),'current complete lifecycle native ownership');witness(s)
    return dict(**s,review_sha256=sha(raw),current_smoke=smoke(target,candidate))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--current-cold',action='store_true',help='reuse verified cold/formatter/graphics prerequisites; rerun lifecycle gates');o=p.parse_args()
    r=dict(schema='th03-zun-lifecycle-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),provenance='candidate-local-attested',native_pair_built_now=not o.current_cold,whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_zun_graphics_work.py')],cwd=ROOT,check=True)
    work,target,candidate,at,files,maintained,cold=images(ROOT);graphics.current_scope(ROOT,work,target,candidate,at,files,maintained,cold)
    r['cold_report_sha256']=sha(cold);r['graphics_report_sha256']=sha(graphics.REPORT.read_bytes());r['source_inventory_sha256']=graphics.formatter.digest(json.loads(cold)['source_sha256'])
    r['scope']=dict(layout=layout(work,target,candidate,at,files,maintained),runtime=runtime(target,candidate),negative_controls=negative_controls(target));witness(r['scope'])
    need(r['implementation_sha256']==inputs(ROOT),'lifecycle inputs changed during execution');r['complete']=True;save()
    print('ZUN lifecycle: eight whole procedures / 564 CODE bytes; 549 executed + fifteen DOS-terminal-unreachable; all gates pass',flush=True);return 0
if __name__=='__main__':raise SystemExit(main())
