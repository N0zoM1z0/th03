#!/usr/bin/env python3
"""Review one shared input producer against both complete current cold builds.

Native build receipts and source/behavior acceptance stay separate. This command
runs the long input contracts once; ordinary status revalidates their bindings
and executes short ABI cases. No native object or executable is a write target.
"""
import hashlib
import json
from pathlib import Path
import re
import tomllib

from lib.pc98 import parse_mz
from lib.targets import find_artifact, read_verified_artifact
from lib.shared_input_layout import PROFILES, SOURCE, OBJECT, FUNCTIONS, verify as layout
from lib.shared_input_runtime import Machine, verify as runtime, negative_controls
from lib.mainl_wait_layout import verify as wait_layout, SOURCE as WAIT_SOURCE
from lib.mainl_wait_runtime import Machine as WaitMachine, verify as wait_runtime, negative_controls as wait_controls

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/'.analysis/work/shared-input-build.json'
INPUTS=('scripts/review_th03_shared_input_work.py','scripts/lib/shared_input_layout.py',
        'scripts/lib/shared_input_runtime.py','scripts/lib/pc98.py','scripts/lib/omf.py',
        'scripts/probe_th03_main_bomb_rikako_cpp.py','scripts/probe_th03_main_boss_marisa_cpp.py',
        'config/targets.toml','config/th03_diet.toml',SOURCE,WAIT_SOURCE,
        'scripts/lib/mainl_wait_layout.py','scripts/lib/mainl_wait_runtime.py')


def need(value,message):
    if not value:raise ValueError('shared input review: '+message)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def digest(value):return sha(json.dumps(value,sort_keys=True).encode())
def implementation_inputs(root):return {n:sha((root/n).read_bytes()) for n in INPUTS}


def images(root,profile):
    p=PROFILES[profile];work=root/'.analysis/toolchain/wineprefix/drive_c'/p['folder']
    raw_report=(root/f'.analysis/work/{profile}-build.json').read_bytes();cold=json.loads(raw_report)
    need(cold['complete'] and cold['raw_repeat_equal'] and len(cold['rounds'])==2,'complete current cold pair')
    need(cold['rounds'][0]['outputs']==cold['rounds'][1]['outputs'],'full raw cold output equality')
    objects=cold['rounds'][-1]['outputs'];raw=(work/OBJECT).read_bytes()
    need(objects[OBJECT]==dict(bytes=len(raw),sha256=sha(raw)),'current native input object')
    need(cold['source_sha256'][SOURCE]==sha((work/SOURCE).read_bytes()),'consumed maintained source binding')
    need((work/SOURCE).read_bytes().replace(b'\r\n',b'\n')==(root/SOURCE).read_bytes(),'maintained source and explicit LF/CRLF transport')
    target=(work/f'bin/th03/{profile}.target.exe').read_bytes();candidate=(work/f'bin/th03/{profile}.exe').read_bytes()
    declarations=tomllib.loads((root/'config/th03_diet.toml').read_text())
    pinned,=[r for r in declarations['artifacts'] if r['id']==p['artifact']]
    need(len(target)==pinned['decoded_size'] and sha(target)==pinned['decoded_sha256'] and target==candidate,'complete pinned decoded product')
    stored=read_verified_artifact(root,find_artifact(tomllib.loads((root/'config/targets.toml').read_text()),p['artifact']))
    need((work/f'bin/th03/{profile}.packed.exe').read_bytes()==stored,'complete canonical stored product')
    need(objects[f'bin/th03/{profile}.exe']==dict(bytes=len(candidate),sha256=sha(candidate)),'current complete decoded cold output')
    raw_map=(work/f'obj/th03/{profile}.map').read_bytes()
    need(objects[f'obj/th03/{profile}.map']==dict(bytes=len(raw_map),sha256=sha(raw_map)),'current complete native MAP output')
    return work,parse_mz(target),parse_mz(candidate),cold,raw_report


def witness(scope):
    r=scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['cases_per_image'],r['executed_owner_bytes'],r['exhaustive_high_input_bytes'])
         ==(2,9,367,2218,367,256),'complete two-load shared runtime dimensions')
    need([(o['load_segment'],o['cases'],o['covered_owner_bytes'],o['maximum_observed_stack_depth'],o['maximum_sample_polls'])
          for o in r['observations']]==[(0x1000,1109,367,16,10003),(0x3000,1109,367,16,10003)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'full coverage/wait/stack witnesses')
    controls=scope['negative_controls']
    need(controls['count']==len(set(controls['rejected']))==19,'all nineteen actual input mutations')
    need(scope['layout']['native_ownership_reviewed'] and scope['layout']['acceptance_requires_current_publication']
         and not scope['layout']['whole_product_accepted'],'physical proof separate from publication acceptance')


def wait_witness(scope):
    r=scope['runtime']
    need((r['images'],r['functions'],r['code_bytes'],r['cases_per_image'],r['executed_owner_bytes'],r['exhaustive_sound_flag_bytes'])
         ==(2,2,126,3378,126,256),'complete ending wait runtime dimensions')
    need([(o['load_segment'],o['cases'],o['covered_owner_bytes'],o['maximum_observed_stack_depth']) for o in r['observations']]
         ==[(0x1000,1689,126,20),(0x3000,1689,126,20)]
         and all(re.fullmatch(r'[0-9a-f]{64}',o['trace_sha256']) for o in r['observations']),'full ending wait coverage/stack witnesses')
    controls=scope['negative_controls']
    need(controls['count']==len(set(controls['rejected']))==18,'all eighteen ending wait guest mutations')


def wait_smoke(target,candidate):
    observations=[];zero=(0,0,0,0,0)
    for mz in (target,candidate):
        m=WaitMachine(mz,0x3000)
        try:
            observations.append([
                m.run('input_wait_for_ok',frames=0,samples=[zero]),
                m.run('input_wait_for_ok',frames=0x8000,samples=[(0,0,0,0,0x4000),(0,0,0,0,0x8000)],flags=0xED7),
                m.run('input_wait_for_ok_or_measure',active=0,frames=0,samples=[zero]),
                m.run('input_wait_for_ok_or_measure',midi=1,measure=0x100,samples=[zero,(0,0x100,0,0,0)],replies=[0xFFFF]*2),
                m.run('input_wait_for_ok_or_measure',measure=0,samples=[(0x20,0,0,0,0)],flags=0xED7)])
        finally:m.close()
    need(observations[0]==observations[1],'current independent ending wait ABI/AX smoke')
    return dict(cases_per_image=5,images=2,trace_sha256=digest(observations[0]),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def smoke(target,candidate,profile):
    observations=[];zero=(0,0,0,0)
    for mz in (target,candidate):
        m=Machine(mz,0x3000,profile)
        try:
            rows=[m.run(name) for _,name,_,_ in FUNCTIONS[:-1]]
            rows += [m.run('input_wait_for_change',frames=1,samples=[zero]*2),
                     m.run('input_wait_for_change',frames=0xFFFF,samples=[(1,0,0,0)]*2+[zero],flags=0xED7),
                     m.run('input_wait_for_change',frames=0,samples=[zero,(0x1000,0,0,0)]),
                     m.run('input_mode_cpu_vs_cpu',sample=(0xFFFF,0x1234,0xABCD,0),flags=0xED7)]
            observations.append(rows)
        finally:m.close()
    need(observations[0]==observations[1],'current independent input ABI/state smoke')
    return dict(cases_per_image=12,images=2,trace_sha256=digest(observations[0]),full_runtime_reexecuted_now=False,full_runtime_witness_bound=True)


def current_scope(root,profile,work,target,candidate,cold_report):
    root=Path(root);raw=(root/'.analysis/work/shared-input-build.json').read_bytes();report=json.loads(raw)
    need(report['complete'] and report['schema']=='th03-shared-input-current-review-v1','complete shared review report')
    need(report['implementation_sha256']==implementation_inputs(root),'shared review implementation/source drift')
    scope=report['profiles'][profile]
    need(scope['cold_report_sha256']==sha(cold_report),'shared review must bind the current complete cold pair')
    need(scope['layout']==layout(work,target,candidate,profile),'current full native input ownership')
    need(scope['runtime']['profile']==profile,'runtime product coordinate binding');witness(scope)
    result=dict(**scope,shared_report_sha256=sha(raw),current_smoke=smoke(target,candidate,profile))
    if profile=='mainl':
        wait=scope['ending_wait']
        need(wait['layout']==wait_layout(work,target,candidate),'current complete ending wait ownership')
        wait_witness(wait);result['current_wait_smoke']=wait_smoke(target,candidate)
    return result


def main():
    report=dict(schema='th03-shared-input-current-review-v1',complete=False,implementation_sha256=implementation_inputs(ROOT),
                profiles={},provenance='candidate-local-attested',native_invocations=0,source_acceptance=False,canonical_unit_credit_changed=False)
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    save=lambda:REPORT.write_text(json.dumps(report,indent=2)+'\n')
    save()
    for profile in PROFILES:
        work,target,candidate,cold,raw=images(ROOT,profile)
        result=dict(cold_report_sha256=sha(raw),source_inventory_sha256=digest(cold['source_sha256']),
                    layout=layout(work,target,candidate,profile),runtime=runtime(target,candidate,profile),
                    negative_controls=negative_controls(target,profile))
        witness(result)
        if profile=='mainl':
            result['ending_wait']=dict(layout=wait_layout(work,target,candidate),runtime=wait_runtime(target,candidate),
                                       negative_controls=wait_controls(target))
            wait_witness(result['ending_wait'])
        report['profiles'][profile]=result;save()
        print(profile+': 9 complete functions / 367 CODE bytes; native, guest and mutation checks pass',flush=True)
    need(report['implementation_sha256']==implementation_inputs(ROOT),'review changed during execution')
    report['complete']=True;save();return 0


if __name__=='__main__':raise SystemExit(main())
