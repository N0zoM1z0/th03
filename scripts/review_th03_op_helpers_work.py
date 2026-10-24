#!/usr/bin/env python3
"""Review complete OP initializer, KAJA and duplicate delay against a current cold pair."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import review_th03_op_sound_work as sound
from lib.op_helpers_layout import PRODUCERS,verify as layout
from lib.op_helpers_sound_runtime import Machine as SoundMachine,verify as sound_runtime,negative_controls as sound_controls
from lib.op_init_runtime import Machine as InitMachine,verify as init_runtime,negative_controls as init_controls
ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/op-helpers-build.json'
INPUTS=(*sound.INPUTS,'scripts/review_th03_op_helpers_work.py','scripts/lib/op_helpers_layout.py',
 'scripts/lib/op_helpers_sound_runtime.py','scripts/lib/op_init_runtime.py',*tuple(row[2] for row in PRODUCERS))
def need(v,m):
    if not v:raise ValueError('OP helpers review: '+m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}
def witness(s):
    r=s['sound_runtime'];need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['exhaustive_BYTE_states'])==(2,2,51,51,1176,256),'complete helper sound runtime dimensions')
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['covered_owner_bytes'],o['maximum_observed_stack_depth']) for o in r['observations']]
        ==[(0x1000,588,{'frame_delay':28,'kaja':560},51,2),(0x3000,588,{'frame_delay':28,'kaja':560},51,2)],'complete helper sound coverage/state/stack witnesses')
    r=s['init_runtime'];need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'])==(2,1,105,105,1578),'complete init runtime dimensions')
    need([(o['load_segment'],o['cases'],o['allocation_success_cases'],o['allocation_failure_cases'],o['covered_owner_bytes'],o['executed_nested_bytes'],o['maximum_observed_stack_depth']) for o in r['observations']]
        ==[(0x1000,789,229,560,105,41,10),(0x3000,789,229,560,105,41,10)],'complete init success/failure/plane/stack witnesses')
    need(all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for k in ('sound_runtime','init_runtime') for o in s[k]['observations']),'full runtime trace vector')
    for key,count in (('sound_negative_controls',11),('init_negative_controls',13)):
        c=s[key];need(c['count']==len(set(c['rejected']))==count,'complete actual helper mutations')
    l=s['layout'];need(l['functions']==3 and l['code_bytes']==156 and len(l['ordered_relocations'])==11 and l['normal_tlink_relaxed_calls']==1 and not l['whole_product_accepted'],'three complete producers and genuine far-call relaxation')
def smoke(target,candidate):
    rows=[]
    for image in (target,candidate):
        m=SoundMachine(image,0x3000);n=InitMachine(image,0x3000)
        try:rows.append([
            m.run('kaja',active=0,argument=0xFFFF),m.run('kaja',midi=2),m.run('kaja',midi=1),
            m.run('frame_delay',frames=0x8000,ticks=(0x7FFF,0x8000),flags=0xED7),
            n.run(filename=(0xFFFF,0xFFFF),status=0x8000),n.run(assign=0x8000),n.run(assign=0x100,flags=0xED7,stack=0x80)])
        finally:m.close();n.close()
    need(rows[0]==rows[1],'current actual helper ABI and allocation/filename/counter smoke')
    return dict(images=2,cases_per_image=7,trace_sha256=sha(json.dumps(rows[0],sort_keys=True).encode()),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)
def current_scope(root,work,target,candidate,cold_raw):
    raw=(root/'.analysis/work/op-helpers-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-op-helpers-current-review-v1','complete helpers report')
    need(r['implementation_sha256']==inputs(root),'helpers implementation/source drift')
    need(r['cold_report_sha256']==sha(cold_raw) and r['sound_review_sha256']==sha(sound.REPORT.read_bytes()),'current cold/sound binding')
    s=r['scope'];need(s['layout']==layout(work,target,candidate),'current complete native helper ownership');witness(s)
    return dict(**s,review_sha256=sha(raw),current_smoke=smoke(target,candidate))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--current-cold',action='store_true',help='revalidate current complete cold/sound prerequisites; run all new helper gates');o=p.parse_args()
    r=dict(schema='th03-op-helpers-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),provenance='candidate-local-attested',
        native_pair_built_now=not o.current_cold,whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_op_sound_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw=sound.attract.dispatch.cfg.images(ROOT);sound.current_scope(ROOT,work,target,candidate,raw)
    r['cold_report_sha256']=sha(raw);r['sound_review_sha256']=sha(sound.REPORT.read_bytes());r['source_inventory_sha256']=sound.attract.dispatch.digest(cold['source_sha256'])
    r['scope']=dict(layout=layout(work,target,candidate),sound_runtime=sound_runtime(target,candidate),sound_negative_controls=sound_controls(target),init_runtime=init_runtime(target,candidate),init_negative_controls=init_controls(target));witness(r['scope'])
    need(r['implementation_sha256']==inputs(ROOT),'helpers inputs changed during review');r['complete']=True;save()
    print('OP helpers: three complete functions / 156 CODE bytes; 16 native fields / 11 relocations; complete current cold/native/runtime gates pass',flush=True);return 0
if __name__=='__main__':raise SystemExit(main())
