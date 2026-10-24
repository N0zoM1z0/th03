#!/usr/bin/env python3
"""Complete ZUN cold/formatter review followed by twelve graphics contracts."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import review_th03_zun_format_work as formatter
from lib.zun_driver_graphics_layout import SOURCE,verify as layout
from lib.zun_driver_graphics_runtime import Machine,verify as runtime,negative_controls

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/zun-graphics-build.json'
INPUTS=(*formatter.INPUTS,'scripts/review_th03_zun_graphics_work.py','scripts/lib/zun_driver_graphics_layout.py',
 'scripts/lib/zun_driver_graphics_runtime.py',SOURCE,'src/zun/driver_hardware.inc')
def need(value,message):
    if not value:raise ValueError('ZUN graphics review: '+message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}

def witness(scope):
    r=scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['unreachable_owner_bytes'],r['cases_per_image'],r['video_pages'],r['video_banks'])
        ==(2,12,814,810,4,512,2,4),'complete graphics runtime dimensions')
    need([(o['load_segment'],o['cases'],o['covered_owner_bytes'],o['unreachable_owner_bytes'],o['maximum_observed_stack_depth']) for o in r['observations']]
        ==[(0x1000,256,810,4,48),(0x3000,256,810,4,48)] and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'graphics load/coverage/stack witnesses')
    c=scope['negative_controls'];need(c['count']==len(set(c['rejected']))==26,'twenty-six actual graphics mutations')
    need(not scope['layout']['enclosing_driver_accepted'] and not scope['layout']['reserved_spans_owned'],'bounded graphics library ownership')

def smoke(target,candidate):
    observations=[]
    for image in (target,candidate):
        m=Machine(image,0x3000)
        try:observations.append([
            m.run('egc_begin',flags=2),m.run('egc_end',flags=0xED7),
            m.run('copy_rows',height=1,words=0),m.run('copy_rows',height=2,words=2,skip=0xFFFE,split_stack=True),
            m.run('draw_clipped',x=15,y=-1,height=3),m.run('draw_clipped',y=200),
            m.run('draw_clipped',x=1,y=-1,height=202,mono=1),m.run('blit_egc',overlap=0)])
        finally:m.close()
    need(observations[0]==observations[1],'current independent graphics ABI/port/state smoke')
    return dict(cases_per_image=8,images=2,trace_sha256=sha(json.dumps(observations[0],sort_keys=True).encode()),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)

def current_scope(root,work,target,candidate,at,files,maintained,cold_raw):
    raw=(root/'.analysis/work/zun-graphics-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-zun-graphics-current-review-v1','complete graphics report')
    need(r['implementation_sha256']==inputs(root),'graphics implementation/source drift')
    need(r['cold_report_sha256']==sha(cold_raw) and r['formatter_report_sha256']==sha(formatter.REPORT.read_bytes()),'current cold and formatter bindings')
    scope=r['scope'];need(scope['layout']==layout(work,target,candidate,at,files,maintained),'complete current graphics native ownership');witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--current-cold',action='store_true',help='reuse a current complete cold/formatter pair and rerun graphics gates');options=p.parse_args()
    r=dict(schema='th03-zun-graphics-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not options.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_zun_format_work.py')],cwd=ROOT,check=True)
    work,target,candidate,at,files,maintained,cold=formatter.images(ROOT)
    formatter.current_scope(ROOT,work,target,candidate,at,files,maintained,cold)
    r['cold_report_sha256']=sha(cold);r['formatter_report_sha256']=sha(formatter.REPORT.read_bytes())
    r['source_inventory_sha256']=formatter.digest(json.loads(cold)['source_sha256'])
    r['scope']=dict(layout=layout(work,target,candidate,at,files,maintained),runtime=runtime(target,candidate),negative_controls=negative_controls(target));witness(r['scope'])
    need(r['implementation_sha256']==inputs(ROOT),'graphics inputs changed during execution');r['complete']=True;save()
    print('ZUN graphics: twelve whole procedures / 814 CODE bytes; 810 executed + four CFG-unreachable; all gates pass',flush=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
