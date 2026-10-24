#!/usr/bin/env python3
"""Cold-build OP under explicit SDK guards, then review the near cfg scope.

The larger containing entry producer and helper alignment remain unaccepted.
Ordinary status binds the full cold/runtime report and runs short cfg cases.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib

from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact,read_verified_artifact
from lib.op_cfg_layout import SOURCE,OBJECT,verify as layout
from lib.op_cfg_runtime import Machine,verify as runtime,negative_controls

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/op-cfg-build.json'
HEADERS=('stddef.h','_defs.h','_null.h','conio.h','process.h')
INPUTS=('scripts/review_th03_op_cfg_work.py','scripts/lib/op_cfg_layout.py','scripts/lib/op_cfg_runtime.py',SOURCE,
 'scripts/build_th03_op_work.py','scripts/lib/pc98.py','scripts/lib/omf.py','scripts/lib/targets.py',
 'scripts/probe_th03_main_bomb_rikako_cpp.py','scripts/probe_th03_main_boss_marisa_cpp.py',
 'config/toolchain.toml','config/targets.toml','config/th03_diet.toml')


def need(value,message):
    if not value:raise ValueError('OP cfg review: '+message)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def digest(value):return sha(json.dumps(value,sort_keys=True).encode())
def inputs(root):return {name:sha((root/name).read_bytes()) for name in INPUTS}


def sdk_inventory(root):
    c=tomllib.loads((root/'config/toolchain.toml').read_text());surface,=[s for s in c['surfaces'] if s['id']=='tc40j-include']
    consumed=root/c['paths']['wine_prefix']/'drive_c/TC4/INCLUDE';installed=root/surface['path'];out={}
    for name in HEADERS:
        a=(consumed/name.upper()).read_bytes();b=(installed/name.upper()).read_bytes()
        need(a==b,'actual consumed SDK header differs from pinned installation: '+name)
        out['C:/TC4/INCLUDE/'+name]=sha(a)
    return out


def images(root):
    import build_th03_op_work as build
    work=build.WORK;raw=(root/'.analysis/work/op-build.json').read_bytes();cold=json.loads(raw)
    need(cold['complete'] and cold['raw_repeat_equal'] and cold['recipe_sha256']==build.recipe_inventory(),'complete current native cold pair/recipe')
    need(cold['rounds'][0]['outputs']==cold['rounds'][1]['outputs'] and len(cold['rounds'][0]['outputs'])==32,'all current cold output records')
    for name in (OBJECT,'bin/th03/op.exe','obj/th03/op.map'):
        data=(work/name).read_bytes();need(cold['rounds'][-1]['outputs'][name]==dict(bytes=len(data),sha256=sha(data)),'current native cfg output: '+name)
    target=(work/'bin/th03/op.target.exe').read_bytes();candidate=(work/'bin/th03/op.exe').read_bytes()
    declaration,=[a for a in tomllib.loads((root/'config/th03_diet.toml').read_text())['artifacts'] if a['id']=='th03-op']
    need(sha(target)==declaration['decoded_sha256'] and len(target)==declaration['decoded_size'] and target==candidate,'complete pinned decoded equality')
    stored=read_verified_artifact(root,find_artifact(tomllib.loads((root/'config/targets.toml').read_text()),'th03-op'))
    need((work/'bin/th03/op.packed.exe').read_bytes()==stored,'complete canonical stored equality')
    deps={p.replace(chr(92),'/') for p in describe_omf((work/OBJECT).read_bytes())['dependency_paths'] if ':' in p}
    need(deps==set(sdk_inventory(root)),'complete consumed SDK dependency set')
    return work,parse_mz(target),parse_mz(candidate),cold,raw


def witness(scope):
    r=scope['runtime'];need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['cases_per_image'],r['exhaustive_byte_domains'],r['read_prefix_lengths'])
         ==(2,3,271,271,4408,256,9),'complete cfg runtime dimensions')
    need([(o['load_segment'],o['cases'],o['covered_owner_bytes'],o['maximum_observed_stack_depth']) for o in r['observations']]
         ==[(0x1000,2204,271,30),(0x3000,2204,271,30)] and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'cfg load/coverage/stack witnesses')
    c=scope['negative_controls'];need(c['count']==len(set(c['rejected']))==21,'all twenty-one actual cfg mutations')
    need(not scope['layout']['containing_producer_accepted'] and not scope['layout']['whole_product_accepted'],'bounded cfg ownership only')


def smoke(target,candidate):
    observations=[]
    for mz in (target,candidate):
        m=Machine(mz,0x3000)
        try:
            observations.append([
                m.run('cfg_load',driver=0xFF,midi=0),m.run('cfg_load',driver=0xFF,midi=0x80),
                m.run('cfg_load',read_bytes=0,trash=0x5A,status=0xFFFF,flags=0xED7),
                m.run('cfg_save',trash=0xA7,status=0x8000,flags=0xED7),
                m.run('cfg_save_exit',trash=0xA7,status=0xFFFF,flags=0xED7)])
        finally:m.close()
    need(observations[0]==observations[1],'current independent cfg transaction smoke')
    return dict(cases_per_image=5,images=2,trace_sha256=digest(observations[0]),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,cold_raw):
    root=Path(root);raw=(root/'.analysis/work/op-cfg-build.json').read_bytes();report=json.loads(raw)
    need(report['complete'] and report['schema']=='th03-op-cfg-current-review-v1','complete current cfg review')
    need(report['implementation_sha256']==inputs(root),'cfg review implementation/source drift')
    need(report['cold_report_sha256']==sha(cold_raw),'cfg review binds current complete cold pair')
    need(report['sdk_before']==report['sdk_after']==sdk_inventory(root),'before/after/current consumed SDK identity')
    scope=report['scope'];need(scope['layout']==layout(work,target,candidate),'current complete cfg native ownership');witness(scope)
    return dict(**scope,review_sha256=sha(raw),sdk_sha256=report['sdk_after'],current_smoke=smoke(target,candidate))


def main():
    import build_th03_op_work as build
    report=dict(schema='th03-op-cfg-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
      sdk_before=sdk_inventory(ROOT),provenance='candidate-local-attested',whole_product_accepted=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(report,indent=2)+'\n');save()
    subprocess.run([sys.executable,str(ROOT/'scripts/build_th03_op_work.py')],cwd=ROOT,check=True)
    report['sdk_after']=sdk_inventory(ROOT);need(report['sdk_before']==report['sdk_after'],'SDK changed during native pair')
    work,target,candidate,cold,raw=images(ROOT);report['cold_report_sha256']=sha(raw)
    report['source_inventory_sha256']=digest(cold['source_sha256'])
    report['scope']=dict(layout=layout(work,target,candidate),runtime=runtime(target,candidate),negative_controls=negative_controls(target));witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'cfg review inputs changed during execution')
    report['complete']=True;save();print('OP cfg: three complete near functions / 271 CODE bytes; SDK, native and guest gates pass',flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
