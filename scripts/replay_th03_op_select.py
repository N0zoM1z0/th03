#!/usr/bin/env python3
"""Cold compile the complete character-selection TU with previous OP owners."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib
from lib.omf import describe_omf, normalize_dependency_timestamps
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from replay_th03_main_exact_units import execute
from replay_th03_op_score import normalized_contracts
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import sha
from review_th03_op_title import RANGES as TITLE_RANGES
from review_th03_op_entry import RANGES as ENTRY_RANGES
from review_th03_op_music import RANGES as MUSIC_RANGES
from review_th03_op_select import CS, DS, RANGES, analyze, observe, PROOF as PARENT

ROOT=Path(__file__).resolve().parents[1]
MANIFEST='config/th03_op_select_candidate.toml'
PROOF='.analysis/sol-op-select-review-20261006.json'
PROOF_SHA='7e8d58a346b49abfefe74b976aa86efc5728a509a858dc5096fbd50def39c722'
PUBLICS=['scoredat_load_and_decode','playchars_available_load','select_cdg_load_part1_of_4',
         'select_cdg_load_part2_of_4','select_cdg_load_part3_of_4','select_init_and_load','select_free',
         'vs_sel_pics_put','story_sel_pics_put','stats_put','names_put','extras_put','curve_put',
         'select_curves_update_and_render','cursor_put','select_update_player',
         'select_1p_vs_2p_menu','select_vs_cpu_menu','select_story_menu']


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run-id',required=True);args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',args.run_id):raise ValueError('invalid run id')
    output=ROOT/'.analysis/th03-op-select'/args.run_id;output.mkdir(parents=True,exist_ok=False)
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('OP selection diagnostic proof differs')
    proof=json.loads(raw);inputs=dict(proof['inputs']);inputs[PROOF]=sha(raw)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP selection prerequisite input differs: '+p)
    cfg=tomllib.loads((ROOT/MANIFEST).read_text());manifests={}
    for name in ('score','title','entry','menu','music'):
        p=f'config/th03_op_{name}_candidate.toml';manifests[name]=tomllib.loads((ROOT/p).read_text());inputs[p]=sha((ROOT/p).read_bytes())
    score,title,entry,menu,music=(manifests[n] for n in ('score','title','entry','menu','music'))
    source_files=sorted(set([cfg['source'],*cfg['support_files'],entry['source'],*entry['support_files'],menu['source'],
                            title['source'],*title['support_files'],*score['support_files'],*[u['source'] for u in score['units']],
                            *music['support_files'],*[u['source'] for u in music['units']]]))
    for p in [MANIFEST,'scripts/replay_th03_op_select.py',*source_files]:inputs[p]=sha((ROOT/p).read_bytes())
    snapshot=output/'repository-inputs'
    for p,h in inputs.items():
        if not p.startswith('.analysis/'):
            dest=snapshot/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,dest)
            if sha(dest.read_bytes())!=h:raise ValueError('OP selection input changed while freezing')
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op');stored=read_verified_artifact(ROOT,artifact)
    target=parse_mz((ROOT/proof['observations'][0]['path']).read_bytes())
    if not target.valid or not proof['diagnostic_checks_pass'] or proof['exact_acceptance']:raise ValueError('OP selection diagnostic prerequisite differs')
    subprocess.run([sys.executable,'scripts/attest_toolchain.py'],cwd=ROOT,check=True)
    tool=tomllib.loads((ROOT/'config/toolchain.toml').read_text());attestation=sha((ROOT/'.analysis/toolchain/attestation.json').read_bytes())
    env=os.environ.copy();env.update(DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(ROOT/tool['paths']['wine_prefix']),MSDOS_PATH=r'C:\TC4\BIN')
    archive=output/'reference.tar';subprocess.run(['git','archive','--format=tar',f'--output={archive}',cfg['reference_revision']],cwd=ROOT/'_reference/ReC98',check=True)
    archive_sha=sha(archive.read_bytes());previous=json.loads((ROOT/PARENT).read_bytes());rounds=[]
    for number in (1,2):
        logs=output/f'round{number}';work=logs/'source';work.mkdir(parents=True)
        subprocess.run(['tar','-xf',str(archive),'-C',str(work)],check=True)
        if list(work.rglob('*.obj')) or list((work/'bin').glob('th0[1-5]/*.exe')):raise ValueError('cold selection archive contains game outputs')
        for p in source_files:
            dest=work/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(snapshot/p,dest)
        for unit in score['units']:
            if 'wrapper' in unit:(work/unit['wrapper']).write_text(f'#include "{unit["source"]}"\n')
            else:
                carrier=work/unit['carrier'];text=carrier.read_text()
                if text.count(unit['anchor'])!=1:raise ValueError('prior score include anchor differs')
                carrier.write_text(text.replace(unit['anchor'],f'#include "{unit["source"]}"',1))
        carrier=work/title['carrier'];text=carrier.read_text();split=text.index(title['anchor'])
        if text.count(title['anchor'])!=1 or sha(text[:split].encode())!=title['prefix_sha256']:raise ValueError('prior title prefix differs')
        carrier.write_text(f'#include "{title["source"]}"\n\n'+text[split:])
        wrapper=work/entry['wrapper']
        if sha(wrapper.read_bytes())!=entry['original_source_sha256']:raise ValueError('entry original frozen source differs')
        wrapper.write_text(f'#include "{entry["source"]}"\n')
        wrapper=work/music['wrapper'];carrier=work/music['carrier']
        if sha(wrapper.read_bytes())!=music['original_wrapper_sha256'] or sha(carrier.read_bytes())!=music['original_carrier_sha256']:raise ValueError('prior Music frozen carrier differs')
        text=carrier.read_text();a=text.index(music['unowned_anchor']);b=text.index(music['unowned_end_anchor'],a)
        if text.count(music['unowned_anchor'])!=1 or text.count(music['unowned_end_anchor'])!=1:raise ValueError('prior Music copy-function anchors differ')
        wrapper.write_text(f'#include "{music["units"][0]["source"]}"\n\n'+text[a:b]+f'#include "{music["units"][1]["source"]}"\n')
        wrapper=work/cfg['wrapper'];carrier=work/cfg['carrier']
        if sha(wrapper.read_bytes())!=cfg['original_wrapper_sha256']:raise ValueError('selection frozen wrapper differs')
        frozen_carrier=subprocess.check_output(['git','show',cfg['reference_revision']+':'+cfg['carrier']],cwd=ROOT/'_reference/ReC98')
        if sha(frozen_carrier)!=cfg['original_carrier_sha256'] or carrier.read_bytes()!=frozen_carrier.replace(b'#include "th03/formats/score_ld.cpp"',b'#include "src/op/formats/score_load.inl"'):
            raise ValueError('selection maintained-loader carrier differs')
        text=carrier.read_text();split=text.index(cfg['anchor'])
        if text.count(cfg['anchor'])!=1 or sha(frozen_carrier.split(cfg['anchor'].encode())[0])!=cfg['prefix_sha256']:raise ValueError('selection private prefix differs')
        prefix=text[:split]
        for forwarding in cfg['support_files']:
            original=forwarding.removeprefix('compat/rec98/')
            prefix=prefix.replace(f'#include "{original}"',f'#include "{forwarding}"')
        carrier.write_text(prefix+f'#include "{cfg["source"]}"\n')
        command=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%' r'&&set PROCESSOR_ARCHITECTURE=AMD64&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat']
        result=execute(command,work,env,logs/'cold-build.log')
        obj=describe_omf((work/cfg['object']).read_bytes())
        if not obj['valid'] or 'TC86 Borland C++ 4.02' not in obj['translator_comments']:raise ValueError('selection compiler producer differs')
        object_observation=dict(path=cfg['object'],normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'])
        all_objects={p.relative_to(work).as_posix():sha(normalize_dependency_timestamps(p.read_bytes())) for p in sorted((work/'obj').rglob('*.obj'))}
        game_objects={p:h for p,h in all_objects.items() if any(p.startswith(f'obj/th0{n}/') for n in range(1,6))};products={}
        for item in load_target_manifest(ROOT/'config/targets.toml')['artifacts']:
            p=Path('bin')/item['game']/Path(item['private_path']).name;products[p.as_posix()]=sha((work/p).read_bytes())
        if products!=previous['rounds'][0]['products']:raise ValueError('selection changed previous complete product vector')
        if len(all_objects)!=416 or len(game_objects)!=350 or len(products)!=20:raise ValueError('selection complete cold vector differs')
        candidate=parse_mz((work/'bin/th03/op.exe').read_bytes());meta=analyze(candidate.program_image);comparisons={}
        for name,seg,a,z,c,far in RANGES:
            comp=extent_observation(target,candidate,dict(segment=seg,offset=a,start=seg*16+a,size=z));comparisons[name]=comp
            if not comp['raw_slice_equal'] or comp['ordered_relocations_equal']!=(name not in ('curves','versus')):raise ValueError('selection original raw/ordered observation differs')
        aggregates={}
        for name,off,size in [('carrier',0x19f2,3013),('remaining_owner',0x1a5d,2906)]:
            comp=extent_observation(target,candidate,dict(segment=CS,offset=off,start=CS*16+off,size=size));aggregates[name]=comp
            if not comp['raw_slice_equal'] or comp['ordered_relocations_equal']:raise ValueError('selection aggregate original raw/order result differs')
        data=extent_observation(target,candidate,dict(segment=DS,offset=0xa0e,start=DS*16+0xa0e,size=0xe3))
        if not data['raw_slice_equal'] or not data['ordered_relocations_equal']:raise ValueError('selection original DATA differs')
        prior={}
        for prefix,ranges in [('entry',ENTRY_RANGES),('music',MUSIC_RANGES),('title',[(n,CS,a,z,c,False) for n,a,z,c in TITLE_RANGES])]:
            for name,seg,a,z,c,far in ranges:
                comp=extent_observation(target,candidate,dict(segment=seg,offset=a,start=seg*16+a,size=z));prior[prefix+'-'+name]=comp
                raw_expected=not(prefix=='music' and name=='put') and not(prefix=='title' and name=='column')
                if not comp['ordered_relocations_equal'] or comp['raw_slice_equal']!=raw_expected:raise ValueError('previous OP original raw/ordered result differs')
        if candidate.program_image[DS*16+0xdc:DS*16+0x166]!=target.program_image[DS*16+0xdc:DS*16+0x166]:raise ValueError('menu original labels/statics differ')
        mp=work/'obj/th03/op.map';map_text=mp.read_text();carriers=code_rows(map_text,len(candidate.program_image))
        owner=next(c for c in carriers if c['module']==cfg['wrapper'] and c['size'])
        if (owner['segment'],owner['offset'],owner['size'])!=(CS,0x19f2,3013):raise ValueError('selection original MAP carrier differs')
        for (_,seg,off,size,cleanup,far),public in zip(RANGES[:19],PUBLICS):
            coords={(int(s,16),int(a,16)) for s,a in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(public)+r'\([^\n]*\)\s*$',map_text,re.M)}
            if coords!={(seg,off)}:raise ValueError('selection original public entry differs: '+public)
        # Complete unchanged prior product vector; focus source execution on
        # all Select controls in IF=DF=0 plus every successful public caller.
        baseline=proof['observations'][0]['cpu'];indices=[i for i,r in enumerate(baseline) if not r['scenario']['if'] and not r['scenario']['df'] or r['function'] in ('versus','cpu','story') and len(r['scenario']['inputs'])>10]
        cpu=[observe(candidate,baseline[i]['function'],baseline[i]['scenario'],baseline[i]['args'],baseline[i]['sequence']) for i in indices]
        if normalized_contracts(cpu)!=normalized_contracts([baseline[i] for i in indices]):raise ValueError('maintained selection source-case contracts differ')
        visited={tuple(a) for r in cpu for a in r['visited']};coverage=dict(instructions=len(meta['bounds']),visited=len(meta['bounds']&visited),unvisited=[list(a) for a in sorted(meta['bounds']-visited)])
        if coverage['unvisited']:raise ValueError('maintained selection native coverage incomplete')
        changes=[dict(decoded_linear=i,target=x,candidate=y) for i,(x,y) in enumerate(zip(target.program_image,candidate.program_image)) if x!=y]
        if len(target.program_image)!=len(candidate.program_image) or len(changes)!=6:raise ValueError('known whole OP six-byte inequality differs')
        rounds.append(dict(number=number,build=result,object=object_observation,all_objects=all_objects,game_objects=game_objects,products=products,
                           comparisons=comparisons,aggregates=aggregates,data=data,prior=prior,cpu=cpu,case_indices=indices,coverage=coverage,map_sha256=sha(mp.read_bytes()),
                           whole_decoded=dict(equal=False,changed_bytes=len(changes),changes=changes,original_ordered_relocations_equal=target.relocations==candidate.relocations)))
        print('PASS maintained OP selection cold round',number,flush=True)
    if rounds[0]['products']!=rounds[1]['products'] or rounds[0]['game_objects']!=rounds[1]['game_objects']:raise ValueError('selection cold determinism differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('selection compiler input changed: '+p)
    if sha(archive.read_bytes())!=archive_sha:raise ValueError('selection frozen archive changed')
    for p in source_files:
        if sha((snapshot/p).read_bytes())!=inputs[p]:raise ValueError('selection source snapshot changed: '+p)
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('selection canonical stored target changed')
    report=dict(kind='th03-op-maintained-character-selection-cold-compiler-probes',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,
                reference_archive_sha256=archive_sha,toolchain_receipt_sha256=attestation,rounds=rounds,
                tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),new_maintained_decoded_bytes=2906,total_maintained_decoded_bytes=9523,
                diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,
                notes='Complete3013-byte19-function selection carrier with one bounded18-function maintainedinl, private unowned DATA/BSS prefix through19explicit compatibility imports, and existing107-byte score loader inl. New2906 bytes/18functions only. Other score394/IRAND42/POLAR26 context not credited. Complete native menus, ordered callbacks/ports/stores/external inputs and physical memory rerun with full instruction coverage. Two independent20product350gameobject vectors deterministic/all416OMF recorded; prior complete Music Room product vector identical, previous owner original rawordered results retained without repeating their unchanged matrices. Original curves351/versus407 relocation order remains unequal despite raw equality. Whole OP six raw bytes and original relocation order still fail. Graphics/resources/DOS/clock/ISR/CRT/header/DATA/BSS/canonicalstorage/fullproduct/exact remain open.')
    (output/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS source-present OP character-selection compiler probes; exact open')


if __name__=='__main__':main()
