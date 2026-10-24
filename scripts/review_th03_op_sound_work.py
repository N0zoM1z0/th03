#!/usr/bin/env python3
"""Fresh OP cold/dispatch/attract chain and complete shared load/delay contracts."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import review_th03_op_attract_work as attract
from lib.op_sound_layout import PRODUCERS,verify as layout
from lib.op_sound_runtime import Machine,verify as runtime,negative_controls
ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/op-sound-build.json'
INPUTS=(*attract.INPUTS,'scripts/review_th03_op_sound_work.py','scripts/lib/op_sound_runtime.py',
 'scripts/lib/decoded_mainl_sound_runtime.py',*tuple(row[2] for row in PRODUCERS))
COUNTS={'load':691,'frame_delay':28}
def need(v,m):
    if not v:raise ValueError('OP sound review: '+m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}
def witness(s):
    r=s['runtime'];need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['exhaustive_MIDI_bytes'],r['filename_copy_bytes'],r['file_read_request_bytes'])
        ==(2,2,133,133,1438,256,13,0x5000),'complete OP sound/timing runtime dimensions')
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['covered_owner_bytes'],o['maximum_observed_stack_depth']) for o in r['observations']]
        ==[(0x1000,719,COUNTS,133,6),(0x3000,719,COUNTS,133,6)] and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'complete load/state/stack witnesses')
    c=s['negative_controls'];need(c['count']==len(set(c['rejected']))==14,'fourteen actual OP sound mutations')
    need(not s['layout']['whole_product_accepted'] and s['layout']['ordered_relocations']==[],'bounded two-producer ownership')
def smoke(target,candidate):
    rows=[]
    for mz in (target,candidate):
        m=Machine(mz,0x3000)
        try:rows.append([
            m.run('load',midi=2,open_failure=True,open_result=5,read_failure=True),
            m.run('load',midi=1,filename=b'X'*13,suffix_end=32,filename_offset=0xFFFF),
            m.run('load',midi=255,function=0xB00),
            m.run('frame_delay',frames=0,ticks=(0,)),
            m.run('frame_delay',frames=0x8000,ticks=(0x7FFF,0x8000),flags=0xED7),
            m.run('frame_delay',frames=0xFFFF,ticks=(0xFFFE,0xFFFF))])
        finally:m.close()
    need(rows[0]==rows[1],'current OP sound/file/WORD-counter ABI smoke')
    return dict(images=2,cases_per_image=6,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)
def current_scope(root,work,target,candidate,cold_raw):
    raw=(root/'.analysis/work/op-sound-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-op-sound-current-review-v1','complete OP sound report')
    need(r['implementation_sha256']==inputs(root),'sound implementation/source drift')
    need(r['cold_report_sha256']==sha(cold_raw) and r['attract_review_sha256']==sha(attract.REPORT.read_bytes()),'current cold/attract binding')
    s=r['scope'];need(s['layout']==layout(work,target,candidate),'current complete native OP sound ownership');witness(s)
    return dict(**s,review_sha256=sha(raw),current_smoke=smoke(target,candidate))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--current-cold',action='store_true',help='revalidate current cold/dispatch/attract prerequisites; rerun sound gates');o=p.parse_args()
    r=dict(schema='th03-op-sound-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),provenance='candidate-local-attested',
        native_pair_built_now=not o.current_cold,whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_op_attract_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,cold_raw=attract.dispatch.cfg.images(ROOT);attract.current_scope(ROOT,work,target,candidate,cold_raw)
    r['cold_report_sha256']=sha(cold_raw);r['attract_review_sha256']=sha(attract.REPORT.read_bytes());r['source_inventory_sha256']=attract.dispatch.digest(cold['source_sha256'])
    r['scope']=dict(layout=layout(work,target,candidate),runtime=runtime(target,candidate),negative_controls=negative_controls(target));witness(r['scope'])
    need(r['implementation_sha256']==inputs(ROOT),'OP sound inputs changed during review');r['complete']=True;save()
    print('OP sound/timing: two complete functions / 133 CODE bytes; cold/native/runtime gates pass',flush=True);return 0
if __name__=='__main__':raise SystemExit(main())
