#!/usr/bin/env python3
"""SDK-guarded OP cold pair followed by complete demo/score dispatch contracts."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import review_th03_op_cfg_work as cfg
from lib.op_dispatch_layout import SOURCE,verify as layout
from lib.op_dispatch_runtime import Machine,verify as runtime,negative_controls

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/op-dispatch-build.json'
INPUTS=(*cfg.INPUTS,'scripts/review_th03_op_dispatch_work.py','scripts/lib/op_dispatch_layout.py',
 'scripts/lib/op_dispatch_runtime.py','scripts/lib/op_exit_runtime.py')


def need(value,message):
    if not value:raise ValueError('OP dispatch review: '+message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def digest(value):return sha(json.dumps(value,sort_keys=True).encode())
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}


def witness(scope):
    r=scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['cases_per_image'],r['executed_owner_bytes'],
        r['exhaustive_demo_bytes'],r['exhaustive_sound_flag_bytes'])==(2,2,296,2144,296,256,256),'complete dispatch runtime dimensions')
    need([(o['load_segment'],o['cases'],o['covered_owner_bytes'],o['executed_nested_bytes'],o['maximum_observed_stack_depth'])
        for o in r['observations']]==[(0x1000,1072,296,164,26),(0x3000,1072,296,164,26)]
        and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'full dispatch load/coverage/helper/stack witnesses')
    c=scope['negative_controls'];need(c['count']==len(set(c['rejected']))==23,'all twenty-three actual dispatch mutations')
    need(not scope['layout']['containing_producer_accepted'] and not scope['layout']['whole_product_accepted'],'bounded dispatch ownership')


def smoke(target,candidate):
    observations=[]
    for mz in (target,candidate):
        m=Machine(mz,0x3000)
        try:observations.append([m.run('start_demo',demo=v) for v in (0,3,4,254,255)]+[
            m.run('score_menu',active=0,flags=0xED7),m.run('score_menu',midi=1,status=0x8000),
            m.run('score_menu',midi=0x80,resoff=0xFF80,resseg=0x5000,status=0x1234)])
        finally:m.close()
    need(observations[0]==observations[1],'current independent dispatch ABI/byte-wrap smoke')
    return dict(cases_per_image=8,images=2,trace_sha256=digest(observations[0]),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw):
    root=Path(root);raw=(root/'.analysis/work/op-dispatch-build.json').read_bytes();report=json.loads(raw)
    need(report['complete'] and report['schema']=='th03-op-dispatch-current-review-v1','complete current dispatch review')
    need(report['implementation_sha256']==inputs(root),'dispatch implementation/source drift')
    need(report['cold_report_sha256']==sha(cold_raw),'dispatch binds current complete cold pair')
    cfg_raw=(root/'.analysis/work/op-cfg-build.json').read_bytes()
    need(report['cfg_review_sha256']==sha(cfg_raw),'dispatch binds the SDK-guarded cfg cold review')
    cfg.current_scope(root,work,target,candidate,cold_raw)
    scope=report['scope'];need(scope['layout']==layout(work,target,candidate),'current complete dispatch native ownership');witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    report=dict(schema='th03-op-dispatch-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        provenance='candidate-local-attested',whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(report,indent=2)+'\n');save()
    subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_op_cfg_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,cold_raw=cfg.images(ROOT)
    cfg.current_scope(ROOT,work,target,candidate,cold_raw)
    report['cold_report_sha256']=sha(cold_raw);report['cfg_review_sha256']=sha(cfg.REPORT.read_bytes())
    report['source_inventory_sha256']=digest(cold['source_sha256'])
    report['scope']=dict(layout=layout(work,target,candidate),runtime=runtime(target,candidate),negative_controls=negative_controls(target));witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'dispatch inputs changed during execution')
    report['complete']=True;save();print('OP dispatch: two complete near functions / 296 CODE bytes; cold, native, guest and mutation gates pass',flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
