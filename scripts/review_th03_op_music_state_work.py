#!/usr/bin/env python3
"""Review four complete Music Room state/track procedures, without wider credit."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib
import review_th03_op_entry_data_work as previous
from review_th03_op_cfg_work import images
from lib.omf import describe_omf
from lib.op_music_state_layout import SOURCE,OBJECT,WRAPPER,UNIT,verify as layout
from lib.op_music_state_runtime import Machine,verify as runtime,negative_controls
from lib.op_startup_cold import verify as cold_graph

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/op-music-state-build.json'
BASELINE='bcdf24a'
HEADERS=('mem.h','_defs.h','_null.h')
CHAIN=(SOURCE,'src/op/music/nopoly_blit.inl','src/op/music/animation_and_menu.inl')
INPUTS=(*previous.INPUTS,'scripts/review_th03_op_music_state_work.py',
    'scripts/lib/op_music_state_layout.py','scripts/lib/op_music_state_runtime.py',*CHAIN)

def need(value,message):
    if not value:raise ValueError('OP Music state review: '+str(message))

def sha(raw):return hashlib.sha256(raw).hexdigest()
def inputs(root):return {name:sha((root/name).read_bytes()) for name in INPUTS}

def sdk_inventory(root):
    config=tomllib.loads((root/'config/toolchain.toml').read_text())
    surface,=[s for s in config['surfaces'] if s['id']=='tc40j-include']
    consumed=root/config['paths']['wine_prefix']/'drive_c/TC4/INCLUDE'
    installed=root/surface['path'];out={}
    for name in HEADERS:
        a=(consumed/name.upper()).read_bytes();b=(installed/name.upper()).read_bytes()
        need(a==b,'actual consumed Music SDK differs from pinned installation: '+name)
        out['C:/TC4/INCLUDE/'+name]=sha(a)
    return out

def dependencies(root,work,cold):
    import build_th03_op_work as build
    files=build.source_graph()
    producer,=[p for p in build.producers(files) if p['output']==OBJECT]
    need(producer['source']==WRAPPER and producer['ownership']=='maintained-containing' and
        producer['maintained_owner_sources']==[CHAIN[2],SOURCE],'exact two containing source owners')
    need(files[WRAPPER]==('\n\n'.join('#include "'+n+'"' for n in CHAIN)+'\n').encode(),
        'literal complete three-include producer')
    sdk=sdk_inventory(root)
    native=describe_omf((work/OBJECT).read_bytes())
    paths=[re.sub(r'/+','/',p.replace(chr(92),'/')) for p in native['dependency_paths']]
    need({p for p in paths if ':' in p}==set(sdk),'exact consumed Music SDK dependency set')
    for name in paths:
        if ':' not in name:
            need(name in files and sha((work/name).read_bytes())==cold['source_sha256'][name]==sha(files[name]),
                'complete Music native dependency binding: '+name)
    return dict(producer=producer,source_dependencies={n:cold['source_sha256'][n] for n in paths if ':' not in n},sdk_sha256=sdk)

def invariance(root,current=None):
    path='config/op_work/scoped_acceptance.json'
    old=json.loads(subprocess.check_output(['git','show',BASELINE+':'+path],cwd=root))['audit']['scope']
    if current is None:current=json.loads((root/path).read_bytes())['audit']['scope']
    current={k:v for k,v in current.items() if k!='music_state'}
    current['owners']=[o for o in current['owners'] if o['unit_id']!=UNIT]
    need(old==current,'entire prior accepted scope observations remain equal')
    return dict(baseline_commit=BASELINE,complete_prior_scope_sha256=sha(json.dumps(old,sort_keys=True).encode()),
        complete_equal=True,prior_scopes_changed=False)

def witness(scope):
    l,r,c=scope['layout'],scope['runtime'],scope['negative_controls']
    need((l['functions'],l['code_bytes'],l['instruction_bytes'],len(l['owners']))==(4,216,216,1),'complete bounded owner')
    need(len(l['ordered_native_fields'])==12 and len(l['ordered_relocations'])==4,'literal complete native/MZ vectors')
    need(not l['containing_other_CODE_DATA_BSS_newly_accepted'] and not l['whole_product_accepted'],'no wider storage credit')
    need((r['images'],r['functions'],r['code_bytes'],r['cases_per_image'])==(2,4,216,1788),'full two-image/two-load matrix')
    for row,load in zip(r['observations'],(0x1000,0x3000),strict=True):
        need((row['load_segment'],row['cases'],row['executed_owner_bytes'],row['actual_copy_DWORD_callbacks'],
              row['maximum_stack_depth'],row['consecutive_reentry_cases'])==(load,894,216,264000,28,2),'complete load/copy/frame witness')
        need(row['complete_returns']==dict(track_put_both=562,tracklist_put_both=289,nopoly_B_snap=33,nopoly_B_free=10),'all four full procedure returns')
        need(re.fullmatch('[0-9a-f]{64}',row['trace_sha256']),'complete trace digest')
    need(r['actual_nested_track_bodies'] and not r['synthetic_owned_returns'] and r['ignored_stack_bytes']==0,'actual nested calls/full memory')
    need(r['copy_iterations_per_snap']==8000 and r['copy_is_explicit_DWORD_loop'] and not r['DF_changes_copy_direction']
         and r['live_overlapping_source_and_destination'] and r['pointer_offset_WORD_wrap'] and
         r['null_allocation_is_not_checked'] and r['foreign_page_and_table_reloads'],'native unsanitized semantics')
    need(not r['physical_graphics_text_or_heap_proved'] and not r['whole_product_accepted'],'bounded external interfaces only')
    need(c['actual_instruction_mutations']==len(set(c['rejected']))==38,'all38 behavior mutations must reject')
    need(scope['prior_observations']['complete_equal'] and not scope['prior_observations']['prior_scopes_changed'],'prior observations preserved')

def smoke(target,candidate):
    results=[]
    for image in (target,candidate):
        m=Machine(image,0x3000)
        try:results.append([m.run('tracklist_put_both',index=0,page=128,page_after_first=255,pointer_after_first=0xDEADBEEF),
            m.run('nopoly_B_snap',allocated=0,source_offset=65535,flags=0xED7),m.run('nopoly_B_free',reenter=True)])
        finally:m.close()
    need(results[0]==results[1],'complete current nested/list/null-snapshot/free smoke')
    return dict(images=2,cases_per_image=3,trace_sha256=sha(json.dumps(results[0],sort_keys=True).encode()),
        full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)

def current_scope(root,work,target,candidate,cold_raw):
    raw=REPORT.read_bytes();report=json.loads(raw);cold=json.loads(cold_raw)
    previous.current_scope(root,work,target,candidate,cold_raw)
    need(report['complete'] and report['schema']=='th03-op-music-state-current-review-v1','complete Music state report')
    need(report['implementation_sha256']==inputs(root) and report['cold_report_sha256']==sha(cold_raw),'all implementation/cold bindings')
    need(report['entry_data_review_sha256']==sha(previous.REPORT.read_bytes()),'current prerequisite DATA review')
    need(report['cold_validation']==cold_graph(root,work,target,candidate,cold),'entire current native cold graph')
    need(report['dependencies']==dependencies(root,work,cold),'complete current producer/SDK/source bindings')
    need(report['sdk_before']==report['sdk_after']==sdk_inventory(root),'before/after/current SDK identity')
    scope=report['scope'];witness(scope)
    need(scope['layout']==layout(root,work,target,candidate) and scope['prior_observations']==invariance(root),'current layout and complete prior invariance')
    return dict(**scope,review_sha256=sha(raw),sdk_sha256=report['sdk_after'],current_smoke=smoke(target,candidate))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true')
    options=parser.parse_args()
    report=dict(schema='th03-op-music-state-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        sdk_before=sdk_inventory(ROOT),provenance='candidate-local-attested',native_pair_built_now=not options.current_cold,
        whole_product_accepted=False,canonical_unit_credit_changed=False)
    def save():REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    if not options.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/review_th03_op_entry_data_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,cold_raw=images(ROOT)
    report['cold_validation']=cold_graph(ROOT,work,target,candidate,cold)
    previous.current_scope(ROOT,work,target,candidate,cold_raw)
    report.update(cold_report_sha256=sha(cold_raw),entry_data_review_sha256=sha(previous.REPORT.read_bytes()),
        dependencies=dependencies(ROOT,work,cold))
    report['scope']=dict(layout=layout(ROOT,work,target,candidate),runtime=runtime(target,candidate),
        negative_controls=negative_controls(target),prior_observations=invariance(ROOT))
    report['sdk_after']=sdk_inventory(ROOT)
    need(report['sdk_before']==report['sdk_after'],'SDK changed during review')
    witness(report['scope']);need(report['implementation_sha256']==inputs(ROOT),'inputs changed during review')
    report['complete']=True;save()
    print('OP Music state: four complete procedures/216 CODE bytes;1788 cases per image;38 behavior controls',flush=True)
    return 0

if __name__=='__main__':raise SystemExit(main())
