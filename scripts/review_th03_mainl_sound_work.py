#!/usr/bin/env python3
"""Fresh MAINL cold pair, then six complete sound and timing source contracts."""
import argparse,hashlib,json,re,subprocess,sys,tomllib
from pathlib import Path
import build_th03_mainl_work as build
from build_th03_op_work import compare_mz
from lib.pc98 import parse_mz
from lib.targets import find_artifact,read_verified_artifact
from lib.decoded_mainl_sound_layout import PRODUCERS,verify as layout
from lib.decoded_mainl_sound_runtime import Machine,verify as runtime,negative_controls
ROOT=Path(__file__).resolve().parents[1];REPORT=ROOT/'.analysis/work/mainl-sound-build.json'
INPUTS=('scripts/review_th03_mainl_sound_work.py','scripts/lib/decoded_mainl_sound_layout.py','scripts/lib/decoded_mainl_sound_runtime.py',
 'scripts/build_th03_mainl_work.py','scripts/build_th03_op_work.py','scripts/lib/pc98.py','scripts/lib/omf.py','scripts/lib/targets.py','scripts/lib/toolchain.py',
 'scripts/probe_th03_main_bomb_rikako_cpp.py','scripts/probe_th03_main_boss_marisa_cpp.py','config/targets.toml','config/th03_diet.toml','config/toolchain.toml',
 *tuple(row[2] for row in PRODUCERS))
COUNTS={'load':691,'frame_delay':28,'play':8885,'update':10628,'kaja':560,'measure':579}
def need(v,m):
    if not v:raise ValueError('MAINL sound review: '+m)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def digest(o):return sha(json.dumps(o,sort_keys=True).encode())
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}
def images(root):
    root=Path(root);need(root.resolve()==build.ROOT,'live repository root');raw=(root/'.analysis/work/mainl-build.json').read_bytes();cold=json.loads(raw);work=build.WORK
    need(cold['complete'] and cold['raw_repeat_equal'] and cold['retained_project_objects']==0,'complete current cold pair')
    need(cold['recipe_sha256']==build.recipe_inventory() and cold['vendor_header_sha256']==build.vendor_header_inventory(),'current native recipe/SDK binding')
    files,graph,archive=build.sources();need(cold['archive_sha256']==archive and cold['source_sha256']=={n:sha(b) for n,b in sorted(files.items())},'complete current source graph')
    need(all((work/n).read_bytes()==b for n,b in files.items()),'complete staged source binding')
    need([r['round'] for r in cold['rounds']]==[1,2] and len(cold['rounds'][0]['outputs'])==938 and cold['rounds'][0]['outputs']==cold['rounds'][1]['outputs'],'complete raw cold output vector')
    for n,row in cold['rounds'][0]['outputs'].items():
        b=(work/n).read_bytes();need(row==dict(bytes=len(b),sha256=sha(b)),'live cold output: '+n)
    targets=tomllib.loads((root/'config/targets.toml').read_text());stored=read_verified_artifact(root,find_artifact(targets,'th03-mainl'))
    declaration,=[a for a in tomllib.loads((root/'config/th03_diet.toml').read_text())['artifacts'] if a['id']=='th03-mainl']
    target=(work/'bin/th03/mainl.target.exe').read_bytes();candidate=(work/'bin/th03/mainl.exe').read_bytes()
    need(len(target)==declaration['decoded_size'] and sha(target)==declaration['decoded_sha256'] and target==candidate,'complete pinned decoded equality')
    need(compare_mz(candidate,target)==cold['comparison'] and (work/'bin/th03/mainl.packed.exe').read_bytes()==stored,'complete format/ordered relocations and canonical stored equality')
    need(cold['packing']['options']==['-B'] and cold['packing']['raw_repeat_equal'] and cold['packing']['stored_equal'] and cold['packing']['same_tool_roundtrip'],'complete pack/restore binding')
    return work,parse_mz(target),parse_mz(candidate),cold,raw,graph,files
def witness(s):
    r=s['runtime'];need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['exhaustive_byte_states'],r['legitimate_SE_entries'],r['filename_copy_bytes'],r['file_read_request_bytes'])
        ==(2,6,332,332,42742,256,33,13,0x5000),'complete sound/timing runtime dimensions')
    need([(o['load_segment'],o['cases'],o['cases_by_function'],o['covered_owner_bytes'],o['maximum_observed_stack_depth'],o['maximum_driver_calls'],o['maximum_counter_updates']) for o in r['observations']]
        ==[(0x1000,21371,COUNTS,332,10,3,3),(0x3000,21371,COUNTS,332,10,3,3)] and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'complete load/state/stack/counter witnesses')
    c=s['negative_controls'];need(c['count']==len(set(c['rejected']))==33,'all thirty-three actual sound mutations')
    need(not s['layout']['adjacent_explicit_padding_accepted'] and not s['layout']['whole_product_accepted'],'bounded natural source classification')
def smoke(target,candidate):
    rows=[]
    for image in (target,candidate):
        m=Machine(image,0x3000)
        try:rows.append([
            m.run('load',midi=2,open_failure=True,open_result=5,read_failure=True),
            m.run('load',midi=1,filename=b'X'*13,suffix_end=32,filename_offset=0xFFFF),
            m.run('play',playing=255,frame=7,argument=0xFFFF),
            m.run('play',playing=1,argument=0x100,frame=7),
            m.run('update',playing=0,frame=255),m.run('update',playing=1,frame=0),
            m.run('kaja',active=0,argument=0xFFFF),m.run('kaja',midi=2),
            m.run('frame_delay',frames=0x8000,ticks=(0x7FFF,0x8000),flags=0xED7),
            m.run('measure',active=0,frames=0xFFFF,ticks=(0xFFFE,0xFFFF)),
            m.run('measure',midi=1,measure=0x8000,measures=(0x7FFF,0x8000))])
        finally:m.close()
    need(rows[0]==rows[1],'current independent sound/file/counter ABI smoke')
    return dict(images=2,cases_per_image=11,trace_sha256=digest(rows[0]),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)
def current_scope(root,work,target,candidate,cold_raw,graph,files):
    raw=(root/'.analysis/work/mainl-sound-build.json').read_bytes();r=json.loads(raw)
    need(r['complete'] and r['schema']=='th03-mainl-sound-current-review-v1','complete sound review')
    need(r['implementation_sha256']==inputs(root) and r['cold_report_sha256']==sha(cold_raw),'current implementation/source/cold binding')
    s=r['scope'];need(s['layout']==layout(work,target,candidate,graph,files),'current full native sound ownership');witness(s)
    return dict(**s,review_sha256=sha(raw),current_smoke=smoke(target,candidate))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--current-cold',action='store_true',help='revalidate complete current source/output pair; rerun all sound gates');o=p.parse_args()
    r=dict(schema='th03-mainl-sound-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),provenance='candidate-local-attested',
        native_pair_built_now=not o.current_cold,whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(r,indent=2)+'\n');save()
    if not o.current_cold:subprocess.run([sys.executable,str(ROOT/'scripts/build_th03_mainl_work.py')],cwd=ROOT,check=True)
    work,target,candidate,cold,raw,graph,files=images(ROOT);r['cold_report_sha256']=sha(raw);r['source_inventory_sha256']=digest(cold['source_sha256'])
    r['scope']=dict(layout=layout(work,target,candidate,graph,files),runtime=runtime(target,candidate),negative_controls=negative_controls(target));witness(r['scope'])
    need(r['implementation_sha256']==inputs(ROOT),'sound review changed during execution');r['complete']=True;save()
    print('MAINL sound/timing: six complete functions / 332 CODE bytes; complete cold/native/runtime gates pass',flush=True);return 0
if __name__=='__main__':raise SystemExit(main())
