#!/usr/bin/env python3
"""Fresh complete ZUN cold pair and bounded ten-procedure formatter review."""
import hashlib
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib

from lib.zun import parse_launcher
from lib.targets import find_artifact,read_verified_artifact
from lib.zun_driver_format_layout import SOURCE,verify as layout
from lib.zun_driver_format_runtime import Machine,ENTRIES,verify as runtime,negative_controls

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/zun-format-build.json'
INPUTS=('scripts/review_th03_zun_format_work.py','scripts/lib/zun_driver_format_layout.py','scripts/lib/zun_driver_format_runtime.py',
 SOURCE,'src/zun/driver_strings.inl','src/zun/driver_data.inl','scripts/build_th03_zun_work.py',
 'scripts/lib/zun_driver_layout.py','scripts/lib/zun.py','scripts/lib/targets.py','scripts/stage_th03_zun_driver.py',
 'scripts/verify_th03_zun_driver_hybrid.py','config/targets.toml','config/th03_diet.toml')


def need(value,message):
    if not value:raise ValueError('ZUN formatter review: '+message)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def digest(value):return sha(json.dumps(value,sort_keys=True).encode())
def inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}


def images(root):
    import build_th03_zun_work as build
    work=build.WORK;raw=(root/'.analysis/work/zun-build.json').read_bytes();cold=json.loads(raw)
    need(cold['complete'] and cold['raw_repeat_equal'] and cold['recipe_sha256']==build.recipe_inventory(),'current complete ZUN cold pair')
    files,maintained,context=build.compose(root)
    need(cold['source_sha256']=={n:sha(b) for n,b in sorted(files.items())} and cold['maintained_inputs']=={n:sha(b) for n,b in sorted(maintained.items())},'current source and maintained bindings')
    need(cold['rounds'][0]['outputs']==cold['rounds'][1]['outputs'] and len(cold['rounds'][0]['outputs'])==29,'all twenty-nine raw outputs repeat')
    for n,r in cold['rounds'][0]['outputs'].items():
        b=(work/n).read_bytes();need(r==dict(bytes=len(b),sha256=sha(b)),'current output: '+n)
    decoded=(work/'product/zun.com').read_bytes()
    pinned,=[a for a in tomllib.loads((root/'config/th03_diet.toml').read_text())['artifacts'] if a['id']=='th03-zun']
    need(len(decoded)==pinned['decoded_size'] and sha(decoded)==pinned['decoded_sha256'],'whole canonical-decoded identity, not a partial payload match')
    target=read_verified_artifact(root,find_artifact(tomllib.loads((root/'config/targets.toml').read_text()),'th03-zun'))
    need((work/'product/zun.packed.com').read_bytes()==target,'whole canonical stored equality')
    child=parse_launcher(decoded,223)['payloads'][3];at,size=child['decoded_file_offset'],child['size']
    return work,decoded[at:at+size],(work/'driver/driver.com').read_bytes(),at,files,maintained,raw


def witness(scope):
    r=scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['executed_owner_bytes'],r['unreachable_owner_bytes'],r['cases_per_image'],r['exhaustive_byte_domains'])
        ==(2,10,677,666,11,6106,256),'complete formatter runtime dimensions')
    need([(o['load_segment'],o['cases'],o['covered_owner_bytes'],o['unreachable_owner_bytes'],o['maximum_observed_stack_depth']) for o in r['observations']]
        ==[(0x1000,3053,666,11,356),(0x3000,3053,666,11,356)]
        and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'complete formatter load/coverage/stack witnesses')
    need((r['wrapper_buffer_bytes'],r['maximum_wrapper_output_bytes'])==(208,209),'unchecked wrapper buffer boundary witness')
    c=scope['negative_controls'];need(c['count']==len(set(c['rejected']))==24,'all twenty-four actual formatter mutations')
    need(not scope['layout']['enclosing_driver_accepted'] and not scope['layout']['reserved_spans_owned'],'bounded library ownership')


def smoke(target,candidate):
    observations=[]
    for image in (target,candidate):
        m=Machine(image,0x3000)
        try:
            observations.append([m.run(n) for n in ENTRIES]+[
                m.run('format_into',text=b'%6d',args=(0xFFFFFFFB,),split_stack=True),
                m.run('format_print',text=b'A'*208,args=()),m.run('format_print',text=b'A'*209,args=(),split_stack=True),
                m.run('format_unsigned',value=0xFFFFFFFF,radix=3,lower=0xFFFF),
                m.run('format_into',text=b'%c!',args=(0,),in_cs=True)])
        finally:m.close()
    need(observations[0]==observations[1],'current formatter independent ABI smoke')
    return dict(cases_per_image=15,images=2,trace_sha256=digest(observations[0]),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,work,target,candidate,payload_offset,files,maintained,cold_raw):
    raw=(root/'.analysis/work/zun-format-build.json').read_bytes();report=json.loads(raw)
    need(report['complete'] and report['schema']=='th03-zun-formatter-current-review-v1','complete current formatter report')
    need(report['implementation_sha256']==inputs(root),'formatter implementation/source drift')
    need(report['cold_report_sha256']==sha(cold_raw),'formatter binds current complete cold pair')
    scope=report['scope'];need(scope['layout']==layout(work,target,candidate,payload_offset,files,maintained),'current complete formatter native ownership');witness(scope)
    return dict(**scope,review_sha256=sha(raw),current_smoke=smoke(target,candidate))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--current-cold',action='store_true',help='reuse a complete current source/output-bound cold pair; rerun all formatter gates')
    options=parser.parse_args()
    report=dict(schema='th03-zun-formatter-current-review-v1',complete=False,implementation_sha256=inputs(ROOT),
        provenance='candidate-local-attested',whole_product_accepted=False,canonical_unit_credit_changed=False,native_pair_built_now=not options.current_cold)
    REPORT.parent.mkdir(parents=True,exist_ok=True);save=lambda:REPORT.write_text(json.dumps(report,indent=2)+'\n');save()
    if not options.current_cold:
        subprocess.run([sys.executable,str(ROOT/'scripts/build_th03_zun_work.py')],cwd=ROOT,check=True)
    work,target,candidate,at,files,maintained,cold_raw=images(ROOT)
    report['cold_report_sha256']=sha(cold_raw);report['source_inventory_sha256']=digest(json.loads(cold_raw)['source_sha256'])
    report['scope']=dict(layout=layout(work,target,candidate,at,files,maintained),runtime=runtime(target,candidate),negative_controls=negative_controls(target));witness(report['scope'])
    need(report['implementation_sha256']==inputs(ROOT),'formatter inputs changed during review')
    report['complete']=True;save();print('ZUN formatter: ten whole procedures / 677 CODE bytes; 666 executed + 11 CFG-unreachable; cold/native/runtime gates pass',flush=True)
    return 0


if __name__=='__main__':raise SystemExit(main())
