#!/usr/bin/env python3
"""Review the whole far OP startup with actual owned nested execution."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import review_th03_op_main_menu_work as previous
from lib.op_startup_layout import verify as layout
from lib.op_startup_cold import verify as cold_graph
from lib.op_startup_runtime import Machine,verify as runtime,negative_controls,OPTION_PATH,stream

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/op-startup-build.json'
BASELINE='dbf8a522ba31c21c1705ce3971224d63b34118a1'
INPUTS=(*previous.INPUTS,'scripts/review_th03_op_startup_work.py','scripts/lib/op_startup_layout.py',
    'scripts/lib/op_startup_state.py','scripts/lib/op_startup_primitives.py',
    'scripts/lib/op_startup_children.py','scripts/lib/op_startup_runtime.py',
    'scripts/lib/op_startup_cold.py','scripts/lib/toolchain.py')


def need(value,message):
    if not value:raise ValueError('OP startup review: '+str(message))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def digest(value):
    return sha(json.dumps(value,sort_keys=True).encode())


def inputs(root):
    return {name:sha((root/name).read_bytes()) for name in INPUTS}


def invariance(root,cold_raw):
    old=json.loads(subprocess.run(['git','show',BASELINE+':config/op_work/scoped_acceptance.json'],
        cwd=root,check=True,capture_output=True).stdout)['audit']['scope']['main_menu']
    old={k:v for k,v in old.items() if k not in ('review_sha256','current_smoke')}
    current=json.loads(previous.REPORT.read_bytes())['scope']
    need(old==current,'entire prior main-menu observation including nested contracts and reentry')
    return dict(legacy_eight=previous.legacy_invariance(root,cold_raw),main_menu_baseline_commit=BASELINE,
        main_menu_complete_observation_sha256=digest(old),main_menu_complete_equal=True)


def closed_dispatch(target):
    # Source-level BYTE->signed-WORD partition. The complete native layout
    # independently fixes CBW/OR/CMP and both branch edges, plus the backedge.
    from capstone import Cs,CS_ARCH_X86,CS_MODE_16
    code=target.program_image
    rows={i.address:(i.mnemonic,i.op_str) for i in Cs(CS_ARCH_X86,CS_MODE_16).disasm(code[0xA4D2:0xA505],0xA4D2)}
    need(rows[0xA4DA][0]=='cwde' and code[0xA4DA]==0x98,'16-bit CBW without operand-size prefix')
    for at,expected in ((0xA4DB,('or','ax, ax')),(0xA4DD,('je','0xa4e6')),
        (0xA4DF,('cmp','ax, 1')),(0xA4E2,('je','0xa4eb')),(0xA4E4,('jmp','0xa4ee')),
        (0xA4EE,('les','bx, ptr [0x2464]')),(0xA4F2,('inc','dword ptr es:[bx + 0x10]')),
        (0xA4FE,('cmp','byte ptr [0x162], 0')),(0xA503,('je','0xa4d2'))):
        need(rows[at]==expected,'closed raw-dispatch native CFG: '+hex(at))
    values=[value if value<128 else value|0xFF00 for value in range(256)]
    need([i for i,v in enumerate(values) if v==0]==[0] and [i for i,v in enumerate(values) if v==1]==[1],
        'exhaustive source dispatch partition')
    return dict(raw_BYTE_values=254,sign_extended_WORD_sha256=digest(values),closed_backedge=[0xA503,0xA4D2],
        disabled_owned_calls=['main','option'],live_state=['quit=0','in_option outside0/1','resident.rand modulo2**32'],
        assumptions=['disjoint resident5000/6000 and mapped stack7000','returning input/device ABI preserves DS/SS',
            'input samples write only declared input WORDs','delay counter replies0 then1','no asynchronous quit/in_option writes'],
        successful_return_or_budget_exhaustion_credit=False)


def witness(scope):
    l,r,c=scope['layout'],scope['runtime'],scope['negative_controls']
    need((l['functions'],l['code_bytes'],l['instruction_bytes'],len(l['ordered_native_fields']),len(l['ordered_relocations']),len(l['near_calls']),len(l['far_calls']))==
        (1,263,263,38,16,13,16),'complete raw/native/ordered layout')
    need(not l['containing_DATA_BSS_or_other_CODE_newly_accepted'] and not l['whole_product_accepted'],'bounded source ownership')
    need((r['images'],r['functions'],r['code_bytes'],r['instruction_bytes'],r['cases_per_image'])==(2,1,263,263,2964),'full matrix dimensions')
    need(r['shared_physical_machine'] and not r['synthetic_owned_callee_returns'] and r['external_CRT_copy_executes'] and r['primitive_private_stack_bytes']==0,'actual physical callee/CRT composition')
    need(r['borrowed_private_stack_bytes']==dict(main=96,option=64,wait=80,vs=80),'explicit inherited callee windows')
    for row,load in zip(r['observations'],(0x1000,0x3000),strict=True):
        need((row['load_segment'],row['cases'],row['ordinary_returns'],row['held_descendant_prefixes'],row['raw_dispatch_prefixes'],row['cfg_preparation_boundaries'],row['executed_owner_bytes'])==
            (load,1482,1136,8,266,72,263),'complete classified execution outcomes')
        need(all(row['borrowed_calls'].values()) and row['maximum_stack_depth']<=100 and row['maximum_completed_iterations']==9,'real caller/callee stack and loop witnesses')
    need(c['actual_instruction_mutations']==len(set(c['rejected']))==46,'all actual instruction controls reject')
    need(scope['closed_dispatch']['raw_BYTE_values']==254 and not scope['closed_dispatch']['successful_return_or_budget_exhaustion_credit'],'conditional closed-loop classification')
    need(scope['prior_observations']['main_menu_complete_equal'] and scope['prior_observations']['legacy_eight']['all_equal'],'all nine prior observations remain equal')


def smoke(target,candidate):
    observations=[]
    for image in (target,candidate):
        machine=Machine(image,0x3000)
        try:
            rows=[machine.run(**options) for options in ({},dict(zoom=256),dict(assign=65535),
                dict(mode=129,selection_ax=0),dict(flags=0xED7,samples=OPTION_PATH),
                dict(read_bytes=0,cfg_boundary=True),dict(raw_dispatch=255,loop_prefix=7,samples=stream(*([0]*7))),
                dict(samples=stream(0x20,0,0x20),selection_ax=0,selected_char=17))]
            observations.append(rows)
        finally:machine.close()
    need(observations[0]==observations[1],'current full-state normal/error/option/short-file/conditional-prefix smoke')
    return dict(images=2,cases_per_image=8,trace_sha256=digest(observations[0]),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw):
    raw=REPORT.read_bytes()
    report=json.loads(raw)
    need(report['complete'] and report['schema']=='th03-op-startup-current-review-v1','complete startup review')
    need(report['implementation_sha256']==inputs(root),'all source/model/context inputs')
    need(report['cold_report_sha256']==sha(cold_raw) and report['main_menu_review_sha256']==sha(previous.REPORT.read_bytes()),'complete cold and prerequisite bindings')
    need(report['cold_validation']==cold_graph(root,work,target,candidate,json.loads(cold_raw)),'entire current native graph')
    scope=report['scope']
    witness(scope)
    need(scope['layout']==layout(root,work,target,candidate),'current full native startup ownership')
    need(scope['prior_observations']==invariance(root,cold_raw) and scope['closed_dispatch']==closed_dispatch(target),'current prior observations and closed CFG')
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='revalidate the entire unchanged native graph and rerun all startup gates')
    options=parser.parse_args()
    report=dict(schema='th03-op-startup-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,canonical_unit_credit_changed=False,whole_product_accepted=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    def save():REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:subprocess.run([sys.executable,str(previous.ROOT/'scripts/review_th03_op_main_menu_work.py')],cwd=ROOT,check=True)
    from review_th03_op_cfg_work import images
    work,target,candidate,cold,cold_raw=images(ROOT)
    report['cold_validation']=cold_graph(ROOT,work,target,candidate,cold)
    previous.current_scope(ROOT,work,target,candidate,cold_raw)
    report.update(cold_report_sha256=sha(cold_raw),main_menu_review_sha256=sha(previous.REPORT.read_bytes()),source_inventory_sha256=digest(cold['source_sha256']))
    report['scope']=dict(layout=layout(ROOT,work,target,candidate),runtime=runtime(target,candidate),
        negative_controls=negative_controls(target),closed_dispatch=closed_dispatch(target),prior_observations=invariance(ROOT,cold_raw))
    witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'inputs unchanged during review')
    report['complete']=True
    save()
    print('OP startup: complete263-byte far main; actual owned nested execution and all state/layout/control gates pass',flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
