#!/usr/bin/env python3
"""Review the complete main caller with real same-machine owned callees."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
import review_th03_op_option_work as option
from lib.op_main_menu_layout import verify as layout
from lib.op_main_menu_runtime import Machine,verify as runtime,negative_controls
ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/op-main-menu-build.json'
BASELINE='d118c463e05bd65fb69dddc34011d0cd8553fd25'
INPUTS=(*option.INPUTS,'scripts/review_th03_op_main_menu_work.py','scripts/lib/op_main_menu_layout.py','scripts/lib/op_main_menu_runtime.py','scripts/lib/op_nested_context.py')
def need(v,m):
    if not v:raise ValueError('OP main menu review: '+str(m))
def sha(raw):return hashlib.sha256(raw).hexdigest()
def digest(v):return sha(json.dumps(v,sort_keys=True).encode())
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}
def legacy_invariance(root,cold_raw):
    raw=subprocess.run(['git','show',BASELINE+':config/op_work/scoped_acceptance.json'],cwd=root,check=True,capture_output=True).stdout
    baseline=json.loads(raw)['audit'];cold=json.loads(cold_raw)
    # Native phase logs can change across fresh cold replays. Compare the
    # complete linked/stored outputs; current source/SDK/recipe/two-round
    # bindings are independently revalidated by cfg.images/current_scope.
    decoded=cold['rounds'][0]['outputs']['bin/th03/op.exe']['sha256']
    stored=cold['packing']['rounds'][0]['packed_sha256']
    need((decoded,stored)==(baseline['decoded_sha256'],baseline['stored_sha256']),'complete decoded/stored artifacts remain equal to baseline')
    rows=[]
    for name,key in (('dispatch','dispatch'),('attract','attract'),('sound','sound'),('helpers','helpers'),('render','renderers'),('vs','vs'),('story','story'),('option','option')):
        old={k:v for k,v in baseline['scope'][key].items() if k not in ('review_sha256','current_smoke')}
        current=json.loads((root/f'.analysis/work/op-{name}-build.json').read_bytes())['scope']
        need(old==current,'every complete original layout/runtime/control observation: '+name)
        rows.append(dict(scope=name,baseline_sha256=digest(old),current_sha256=digest(current),complete_equal=True))
    return dict(baseline_git_commit=BASELINE,baseline_publication_sha256=sha(raw),decoded_sha256=decoded,stored_sha256=stored,cold_report_identity_required=False,complete_scope_observations=rows,all_equal=True)
def witness(s):
    l,r,c=s['layout'],s['runtime'],s['negative_controls']
    need((l['functions'],l['code_bytes'],l['instruction_bytes'],l['inline_non_instruction_bytes'],len(l['ordered_native_fields']),len(l['ordered_relocations']))==(1,291,278,13,42,1),'complete native caller and table storage')
    need(not l['containing_producer_accepted'] and not l['whole_product_accepted'],'bounded caller ownership')
    need((r['images'],r['functions'],r['code_bytes'],r['instruction_bytes'],r['inline_non_instruction_bytes'],r['cases_per_image'])==(2,1,291,278,13,5120),'complete main runtime dimensions')
    need(r['exhaustive_selection_BYTE']==256 and r['shared_physical_machine'] and not r['synthetic_owned_callee_returns'] and r['ignored_private_stack_bytes']==96,'independent BYTE and actual physical callee composition')
    need([(o['load_segment'],o['cases'],o['ordinary_cases'],o['actual_consecutive_reentry_cases'],o['executed_owner_bytes'],o['inline_non_instruction_bytes']) for o in r['observations']]==[(0x1000,2560,2552,8,278,13),(0x3000,2560,2552,8,278,13)] and all(re.fullmatch('[0-9a-f]{64}',o['trace_sha256']) and all(o['nested_calls'].values()) and o['maximum_stack_depth']<=96 and o['nonterminal_cases']>=4 for o in r['observations']),'full two-load caller/callee/reentry witnesses')
    need(all((o['terminal_cases'],o['nonterminal_cases'],o['maximum_stack_depth'])==(2554,6,38) and o['nested_calls']==dict(story=111,vs=105,score=64,wait=275) and o['executed_callee_bytes']==dict(story=390,vs=365,score=94,wait=105) for o in r['observations']),'complete real callee coverage and terminal/nonterminal dimensions')
    need(c['actual_instruction_mutations']==len(set(c['rejected']))==36 and c['consumed_table_WORD_mutations']==6 and c['rejected_table_entries']==list(range(6)) and not c['separator_executed'],'instruction and consumed-table controls stay distinct')
    i=s['legacy_invariance'];need(i['baseline_git_commit']==BASELINE and not i['cold_report_identity_required'] and i['all_equal'] and len(i['complete_scope_observations'])==8 and all(v['complete_equal'] and v['baseline_sha256']==v['current_sha256'] for v in i['complete_scope_observations']),'complete legacy scope invariance')
def smoke(target,candidate):
    rows=[]
    for image in (target,candidate):
        m=Machine(image,0x3000)
        try:rows.append([m.run(initialized=0,input=0),m.run(selection=1,input=0x3020,selection_ax=0,mode=129),m.run(selection=3,input=0x3020),m.run(input=0x20,selection_ax=0,selected_char=17,stack=0x100,flags=0xED7),m.run(input=0,reenter=True),m.run(input=0x20,reenter=True,selection_ax=0,selected_char=17)])
        finally:m.close()
    need(rows[0]==rows[1],'current full-state initialized/callee/static-reentry smoke')
    return dict(images=2,cases_per_image=6,trace_sha256=digest(rows[0]),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)
def current_scope(root,work,target,candidate,cold_raw):
    raw=(root/'.analysis/work/op-main-menu-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-op-main-menu-current-review-v1','complete main caller review')
    need(r['implementation_sha256']==inputs(root),'complete caller/composition/model bindings')
    need(r['cold_report_sha256']==sha(cold_raw) and r['option_review_sha256']==sha(option.REPORT.read_bytes()),'current cold and prerequisite binding')
    s=r['scope'];need(s['layout']==layout(root,work,target,candidate),'complete current native main ownership');witness(s)
    need(s['legacy_invariance']==legacy_invariance(root,cold_raw),'current legacy scope invariance')
    return dict(**s,review_sha256=sha(raw),current_smoke=smoke(target,candidate))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--current-cold',action='store_true',help='revalidate the entire existing source/SDK/recipe/output pair and rerun all new caller gates');o=p.parse_args()
    r=dict(schema='th03-op-main-menu-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),provenance='candidate-local-attested',native_pair_built_now=not o.current_cold,canonical_unit_credit_changed=False,whole_product_accepted=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_op_option_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw=option.story.vs.render.helpers.sound.attract.dispatch.cfg.images(ROOT);option.current_scope(ROOT,work,target,candidate,raw)
    r.update(cold_report_sha256=sha(raw),option_review_sha256=sha(option.REPORT.read_bytes()),source_inventory_sha256=option.story.vs.render.helpers.sound.attract.dispatch.digest(cold['source_sha256']))
    r['scope']=dict(layout=layout(ROOT,work,target,candidate),runtime=runtime(target,candidate),negative_controls=negative_controls(target),legacy_invariance=legacy_invariance(ROOT,raw));witness(r['scope'])
    need(r['implementation_sha256']==inputs(ROOT),'inputs changed during review');r['complete']=True;save();print('OP main: complete 291-byte caller / 278 instruction bytes; actual nested callees, reentry and full-state gates pass',flush=True);return 0
if __name__=='__main__':raise SystemExit(main())
