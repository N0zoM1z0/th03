#!/usr/bin/env python3
"""Review all487 initialized OP entry bytes through natural native consumers."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import review_th03_op_startup_work as previous
from lib.op_entry_data_layout import verify as layout
from lib.op_entry_data_runtime import verify as runtime,negative_controls,fixture
from lib.op_startup_cold import verify as cold_graph

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/op-entry-data-build.json'
BASELINE='940260114bad05c0056dd483b8908051fca46a83'
INPUTS=(*previous.INPUTS,'scripts/review_th03_op_entry_data_work.py',
    'scripts/lib/op_entry_data_layout.py','scripts/lib/op_entry_data_runtime.py')


def need(value,message):
    if not value:raise ValueError('OP entry DATA review: '+str(message))


def sha(raw):return hashlib.sha256(raw).hexdigest()


def inputs(root):return {name:sha((root/name).read_bytes()) for name in INPUTS}


def invariance(root):
    raw=subprocess.run(['git','show',BASELINE+':config/op_work/scoped_acceptance.json'],cwd=root,check=True,capture_output=True).stdout
    old=json.loads(raw)['audit']['scope']['startup']
    old={k:v for k,v in old.items() if k not in ('review_sha256','current_smoke')}
    current=json.loads(previous.REPORT.read_bytes())['scope']
    need(old==current,'entire previous startup layout/runtime/controls and inherited observations')
    return dict(baseline_commit=BASELINE,complete_startup_observation_sha256=sha(json.dumps(old,sort_keys=True).encode()),
        complete_equal=True,prior_scopes_changed=False)


def witness(scope):
    l,r,c=scope['layout'],scope['runtime'],scope['negative_controls']
    need((l['functions'],l['code_bytes'],l['initialized_data_bytes'],l['bss_bytes'],len(l['declarations']),len(l['publics']),l['initialized_holes'])
        ==(0,0,487,0,46,27,0),'entire natural semantic DATA initializer')
    need(l['ordered_native_fields']==l['ordered_relocations']==[] and l['owners'][0]['procedure_count']==0,'no relocations or new functions')
    need(not l['BSS_file_backed'] and not l['containing_CODE_or_BSS_newly_accepted'] and not l['whole_product_accepted'],'DATA/CODE/BSS ownership remains separate')
    need((r['images'],r['initialized_data_bytes'],r['cases_per_image'])==(2,487,94),'full two-image/two-load consumer matrix')
    need(r['old_full_state_contracts_preserved'] and r['semantic_numeric_register_transfers'] and r['semantic_CRT_stack_copy'] and
        r['explicit_native_operand_reads'] and r['argument_derived_bounded_library_string_reads'],'independent semantic consumers and prior ABI/memory checks')
    need(r['new_CODE_ownership_bytes']==r['new_BSS_ownership_bytes']==0 and not r['physical_text_pixels_DOS_or_successful_exec_proved'],'bounded model scope')
    for row,load in zip(r['observations'],(0x1000,0x3000),strict=True):
        need((row['load_segment'],row['cases'],row['initialized_bytes_read'],row['static_only_unused_bytes'])==(load,47,472,15),'complete read/storage dimensions')
        need((row['ordinary_returns'],row['closed_story_prefixes'])==(43,4),'ordinary returns stay distinct from closed story aliases')
        need(row['consumers']==dict(render=20,story=14,demo=6,main=1,option=2,startup=4),'all consumer families execute')
    need((c['actual_initializer_bit_mutations'],c['mutated_bytes'])==(3769,472) and
        c['rejected_sha256']=='d01179d92169fcf9b0f2288d38c672a3ed121670034d2f32ca7f81b42fd9fb2b',
        'all claimed semantic data-bit controls')
    need(c['unused_static_bytes']==l['static_only_unused_bytes'] and len(c['unused_static_bytes'])==15 and
        c['boolean_nonzero_equivalent_bits']==[[211,bit] for bit in range(1,8)] and
        not c['raw_extent_equality_or_fixture_rejection_counts'],'unused and behavior-equivalent bits are static only')
    need(scope['prior_observations']['complete_equal'] and not scope['prior_observations']['prior_scopes_changed'],'complete prior scope invariance')


def smoke(target,candidate):
    observations=[]
    for image in (target,candidate):
        observations.append([fixture(image,0x3000,kind,parameters)[0] for kind,parameters in
            (('render',('option',dict(selection=0,rank=3))),('story',17),('demo',255),('main',None),
             ('option','disabled'),('story',('alias',221)),('story',('alias',229)),('startup',{}),('startup',dict(zoom=1)),('startup',dict(assign=1)),('startup','quit'))])
    need(observations[0]==observations[1],'current full-state semantic consumer smoke')
    return dict(images=2,cases_per_image=11,trace_sha256=sha(json.dumps(observations[0],sort_keys=True).encode()),
        full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw):
    raw=REPORT.read_bytes()
    report=json.loads(raw)
    need(report['complete'] and report['schema']=='th03-op-entry-data-current-review-v1','complete DATA report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),'current complete source/model/cold bindings')
    need(report['startup_review_sha256']==sha(previous.REPORT.read_bytes()),'current prerequisite startup review')
    need(report['cold_validation']==cold_graph(root,work,target,candidate,json.loads(cold_raw)),'entire current cold native graph')
    scope=report['scope']
    witness(scope)
    need(scope['layout']==layout(root,work,target,candidate) and scope['prior_observations']==invariance(root),'current complete semantic layout and invariance')
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate the whole unchanged native graph and rerun all DATA gates')
    options=parser.parse_args()
    report=dict(schema='th03-op-entry-data-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_op_startup_work.py')],cwd=ROOT,check=True)
    from review_th03_op_cfg_work import images
    work,target,candidate,cold,cold_raw=images(ROOT)
    report['cold_validation']=cold_graph(ROOT,work,target,candidate,cold)
    previous.current_scope(ROOT,work,target,candidate,cold_raw)
    report.update(cold_report_sha256=sha(cold_raw),startup_review_sha256=sha(previous.REPORT.read_bytes()))
    report['scope']=dict(layout=layout(ROOT,work,target,candidate),runtime=runtime(target,candidate),prior_observations=invariance(ROOT))
    save()
    report['scope']['negative_controls']=negative_controls(target)
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'inputs unchanged during review')
    report['complete']=True
    save()
    print('OP entry DATA: all487 semantic/native bytes,472 consumed bytes,3769 bit controls; BSS remains separate',flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
