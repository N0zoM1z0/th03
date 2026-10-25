#!/usr/bin/env python3
"""Review complete native ONGCHK ownership and independent instruction contracts."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import review_th03_zun_ongchk_source_work as source
from review_th03_zun_format_work import images
from lib.zun import parse_launcher
from lib.zun_ongchk_layout import verify as layout
from lib.zun_ongchk_runtime import Machine,verify as runtime,negative_controls

ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/zun-ongchk-build.json'
INPUTS=(*source.INPUTS,'scripts/review_th03_zun_ongchk_work.py','scripts/lib/zun_ongchk_layout.py','scripts/lib/zun_ongchk_runtime.py')

def need(v,m):
    if not v:raise ValueError('ONGCHK exact review: '+m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}

def witness(scope):
    r=scope['runtime']
    need((r['images'],r['source_extents'],r['entry_points'],r['code_bytes'],r['data_bytes'],r['bss_bytes'],r['executed_owner_bytes'],r['cases_per_image'])
         ==(2,1,10,892,34,42,892,8134),'complete code/DATA/BSS runtime dimensions')
    need([(o['load_segment'],o['cases'],o['terminal_cases'],o['nonterminal_cases'],o['covered_owner_bytes'],o['maximum_observed_stack_depth'],o['maximum_actual_register_write_calls']) for o in r['observations']]
         ==[(0x1000,4067,3857,210,892,20,60),(0x3000,4067,3857,210,892,20,60)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) and o['maximum_polls']>=10000 for o in r['observations']),
         'complete returning/polling/spin/near-call witnesses')
    need(r['exhaustive_BYTE_domains']==256 and r['maximum_private_stack_window']==48 and r['held_native_polling_cycles']==7
         and r['all_nested_helpers_executed'] and r['spin_iterations_executed'] and not r['physical_timing_or_devices_emulated'],
         'bounded complete-state device contracts')
    c=scope['negative_controls'];need(c['instruction_mutations']==len(set(c['instructions_rejected']))==43
        and c['static_initialized_DATA_mutations_rejected']==34 and c['actual_consumed_DATA_mutations']==33
        and c['consumed_DATA_indices_rejected']==list(range(33)) and not c['static_DATA_controls_have_instruction_credit']
        and not c['result_initializer_is_consumed_before_store'],'separate instruction, consumed-DATA and static initializer controls')
    l=scope['layout'];need((l['source_extents'],l['entry_points'],l['code_bytes'],l['data_bytes'],l['bss_bytes'])==(1,10,892,34,42)
        and len(l['native']['native_fields'])==38 and len(l['polling_cycles'])==7 and l['ordered_relocations']==[]
        and l['all_initialized_DATA_semantically_owned'] and not l['original_source_attested']
        and not l['original_assembler_attested'] and not l['whole_product_accepted'],'complete scoped library ownership and proved polling cycles')

def children(target,candidate):
    row=parse_launcher(target,223)['payloads'][0];at,size=row['decoded_file_offset'],row['size']
    return target[at:at+size],candidate[at:at+size]

def smoke(target,candidate):
    observations=[]
    for image in children(target,candidate):
        m=Machine(image,0x3000)
        try:observations.append([
            m.run(boards=((0x188,3),),busy=1,rom_word=0x2A27,rom_version=6,ss=0x8000,stack=0x80),
            m.run(fallback=0xFE88,override=254,flags=2),
            m.run(boards=((0x88,2),),mismatch_index=0,mismatch_mask=0x80),
            m.run(boards=((0x188,3),),hold='read_ready',seed=0xFFFF,ss=0x8000)])
        finally:m.close()
    need(observations[0]==observations[1],'current full-state hardware/RAM/polling ABI smoke')
    return dict(images=2,cases_per_image=4,trace_sha256=sha(json.dumps(observations[0],sort_keys=True).encode()),
        full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)

def current_scope(root,work,target,candidate,files,maintained,cold_raw):
    raw=(root/'.analysis/work/zun-ongchk-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-zun-ongchk-current-review-v1','complete exact review')
    need(r['implementation_sha256']==inputs(root),'complete current source/model bindings')
    need(r['cold_report_sha256']==sha(cold_raw)
         and r['directory_review_sha256']==sha(source.directory.REPORT.read_bytes())
         and r['source_candidate_review_sha256']==sha(source.REPORT.read_bytes()),'current cold/directory/source-candidate bindings')
    scope=r['scope'];need(scope['layout']==layout(work,target,candidate,files,maintained,json.loads(cold_raw)),'complete current native library source ownership');witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--current-cold',action='store_true',help='revalidate complete source/SDK/recipe/output pair; rerun every new ONGCHK gate');o=p.parse_args()
    r=dict(schema='th03-zun-ongchk-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),provenance='candidate-local-attested',
        native_pair_built_now=not o.current_cold,canonical_unit_credit_changed=False,whole_product_accepted=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_zun_ongchk_source_work.py')],cwd=ROOT,check=True)
    work,_,_,_,files,maintained,cold_raw=images(ROOT);cold=json.loads(cold_raw)
    need(cold['consumed_sdk_sha256']==source.build.sdk_inventory() and cold['consumed_runtime_sha256']==source.build.runtime_inventory(),'current SDK/runtime identities')
    target=(work/'product/zun.target.com').read_bytes();candidate=(work/'product/zun.com').read_bytes()
    source.directory.current_scope(ROOT,work,target,candidate,files,maintained,cold_raw)
    sr=json.loads(source.REPORT.read_bytes());need(sr['complete'] and sr['implementation_sha256']==source.inputs()
        and sr['cold_report_sha256']==sha(cold_raw),'current full source candidate report')
    r.update(cold_report_sha256=sha(cold_raw),directory_review_sha256=sha(source.directory.REPORT.read_bytes()),
        source_candidate_review_sha256=sha(source.REPORT.read_bytes()),source_inventory_sha256=source.behavior.sha(json.dumps(cold['source_sha256'],sort_keys=True).encode()))
    a,b=children(target,candidate)
    r['scope']=dict(layout=layout(work,target,candidate,files,maintained,cold),runtime=runtime(a,b),negative_controls=negative_controls(a))
    witness(r['scope']);need(r['implementation_sha256']==inputs(ROOT),'ONGCHK inputs changed during execution')
    r['complete']=True;save();print('ONGCHK: complete library COM / 892 CODE + 34 DATA + 42 BSS; native, full-state instruction and mutation gates pass',flush=True)
    return 0
if __name__=='__main__':raise SystemExit(main())
