#!/usr/bin/env python3
"""Cold compile the complete maintained OP entry carrier and prior bounded owners."""
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
from review_th03_op_title import RANGES as TITLE_RANGES, matrix as title_matrix
from review_th03_op_entry import CS, DS, RANGES, analyze, matrix, reentry_failure
from review_th03_op_menu import matrix as menu_matrix
from review_th03_op_score import RANGES as SCORE_RANGES

ROOT=Path(__file__).resolve().parents[1]
MANIFEST='config/th03_op_entry_candidate.toml'
PROOF='.analysis/sol-op-entry-review-20261006.json'
PROOF_SHA='7c39a8f7ca07aa3ac1093aa8207e80410e650aa3d14ab5757a8cb2e59640613c'


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run-id',required=True);args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',args.run_id):raise ValueError('invalid run id')
    output=ROOT/'.analysis/th03-op-entry'/args.run_id;output.mkdir(parents=True,exist_ok=False)
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('OP entry diagnostic proof differs')
    proof=json.loads(raw);inputs=dict(proof['inputs']);inputs[PROOF]=sha(raw)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP entry prerequisite input differs: '+p)
    cfg=tomllib.loads((ROOT/MANIFEST).read_text());score=tomllib.loads((ROOT/'config/th03_op_score_candidate.toml').read_text())
    title=tomllib.loads((ROOT/'config/th03_op_title_candidate.toml').read_text())
    menu=tomllib.loads((ROOT/'config/th03_op_menu_candidate.toml').read_text())
    source_files=sorted(set([cfg['source'],*cfg['support_files'],menu['source'],title['source'],*title['support_files'],*score['support_files'],*[u['source'] for u in score['units']]]))
    for p in [MANIFEST,'scripts/replay_th03_op_entry.py',*source_files]:inputs[p]=sha((ROOT/p).read_bytes())
    snapshot=output/'repository-inputs'
    for p,h in inputs.items():
        if not p.startswith('.analysis/'):
            dest=snapshot/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,dest)
            if sha(dest.read_bytes())!=h:raise ValueError('OP entry input changed while freezing')
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op');stored=read_verified_artifact(ROOT,artifact)
    target_path=proof['observations'][0]['path'];target=parse_mz((ROOT/target_path).read_bytes())
    if not target.valid or not proof['diagnostic_checks_pass'] or proof['exact_acceptance']:raise ValueError('OP entry diagnostic prerequisite differs')
    subprocess.run([sys.executable,'scripts/attest_toolchain.py'],cwd=ROOT,check=True)
    tool=tomllib.loads((ROOT/'config/toolchain.toml').read_text());attestation=sha((ROOT/'.analysis/toolchain/attestation.json').read_bytes())
    env=os.environ.copy();env.update(DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(ROOT/tool['paths']['wine_prefix']),MSDOS_PATH=r'C:\TC4\BIN')
    archive=output/'reference.tar'
    subprocess.run(['git','archive','--format=tar',f'--output={archive}',cfg['reference_revision']],cwd=ROOT/'_reference/ReC98',check=True)
    rounds=[]
    for number in (1,2):
        logs=output/f'round{number}';work=logs/'source';work.mkdir(parents=True)
        subprocess.run(['tar','-xf',str(archive),'-C',str(work)],check=True)
        if list(work.rglob('*.obj')) or list((work/'bin').glob('th0[1-5]/*.exe')):raise ValueError('cold title archive contains game outputs')
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
        wrapper=work/cfg['wrapper']
        if sha(wrapper.read_bytes())!=cfg['original_source_sha256']:raise ValueError('entry original frozen source differs')
        wrapper.write_text(f'#include "{cfg["source"]}"\n')
        command=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%'
                 r'&&set PROCESSOR_ARCHITECTURE=AMD64&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat']
        result=execute(command,work,env,logs/'cold-build.log')
        objects={}
        for name,p in [('menu',cfg['object']),('title',title['object'])]+[(u['id'],u['object']) for u in score['units']]:
            obj=describe_omf((work/p).read_bytes())
            if not obj['valid'] or 'TC86 Borland C++ 4.02' not in obj['translator_comments']:raise ValueError('OP entry compiler producer differs')
            objects[name]=dict(path=p,normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'])
        all_objects={p.relative_to(work).as_posix():sha(normalize_dependency_timestamps(p.read_bytes())) for p in sorted((work/'obj').rglob('*.obj'))}
        game_objects={p:h for p,h in all_objects.items() if any(p.startswith(f'obj/th0{n}/') for n in range(1,6))}
        products={}
        for item in load_target_manifest(ROOT/'config/targets.toml')['artifacts']:
            p=Path('bin')/item['game']/Path(item['private_path']).name;products[p.as_posix()]=sha((work/p).read_bytes())
        if len(all_objects)!=416 or len(game_objects)!=350 or len(products)!=20:raise ValueError('OP entry complete cold vector differs')
        candidate=parse_mz((work/'bin/th03/op.exe').read_bytes())
        if not candidate.valid:raise ValueError('invalid entry compiler OP')
        meta=analyze(candidate.program_image)
        comparisons={}
        for name,seg,a,z,c,far in RANGES:
            comp=extent_observation(target,candidate,dict(segment=seg,offset=a,start=seg*16+a,size=z));comparisons[name]=comp
            if not comp['ordered_relocations_equal'] or not comp['raw_slice_equal']:raise ValueError('maintained title original raw/ordered comparison differs')
        prior_score={}
        for name,seg,a,z,c,owner in SCORE_RANGES:
            comp=extent_observation(target,candidate,dict(segment=seg,offset=a,start=seg*16+a,size=z));prior_score[name]=comp
            if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('prior score original raw/ordered comparison differs')
        mp=work/'obj/th03/op.map';map_text=mp.read_text();carriers=code_rows(map_text,len(candidate.program_image))
        owner=next(c for c in carriers if c['module']==cfg['wrapper'] and c['size'])
        if (owner['segment'],owner['offset'],owner['size'])!=(CS,8,3094):raise ValueError('menu original MAP carrier differs')
        publics=['cfg_load()','cfg_save()','cfg_save_exit()','story_menu()',
                 'vs_choice_put(int,unsigned int)','vs_menu()','start_demo()',
                 'wait_for_input_or_start_demo_the()','score_menu()',
                 'main_choice_put(int,unsigned int)','option_choice_put(int,unsigned int)',
                 'menu_sel_update_and_render(char,char)','main_update_and_render()',
                 'option_update_and_render()','_main']
        for (_,seg,off,size,cleanup,far),public in zip(RANGES[:15],publics):
            coords={(int(s,16),int(a,16)) for s,a in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(public)+r'\s*$',map_text,re.M)}
            if coords!={(seg,off)}:raise ValueError('entry original public MAP entry differs: '+public)
        prior_title={}
        for name,a,z,c in TITLE_RANGES:
            comp=extent_observation(target,candidate,dict(segment=CS,offset=a,start=CS*16+a,size=z));prior_title[name]=comp
            if not comp['ordered_relocations_equal'] or (name!='column' and not comp['raw_slice_equal']):raise ValueError('prior title raw/ordered differs')
            if name=='column' and comp['raw_slice_equal']:raise ValueError('prior column failure disappeared')
        title_cpu=title_matrix(candidate)
        title_baseline=json.loads((ROOT/'.analysis/sol-op-title-review-20261006.json').read_bytes())
        if normalized_contracts(title_cpu)!=normalized_contracts(title_baseline['observations'][0]['cpu']):raise ValueError('prior title native contracts differ')
        if candidate.program_image[DS*16+0xdc:DS*16+0x166]!=target.program_image[DS*16+0xdc:DS*16+0x166]:raise ValueError('menu original labels/statics differ')
        cpu=matrix(candidate)
        if normalized_contracts(cpu)!=normalized_contracts(proof['observations'][0]['cpu']):raise ValueError('maintained entry native contracts differ')
        reentry=reentry_failure(candidate)
        if reentry!=proof['observations'][0]['reentry']:raise ValueError('maintained entry reentry failure differs')
        menu_cpu=menu_matrix(candidate)
        menu_baseline=json.loads((ROOT/'.analysis/sol-op-menu-review-20261006.json').read_bytes())
        if normalized_contracts(menu_cpu)!=normalized_contracts(menu_baseline['observations'][0]['cpu']):raise ValueError('prior menu native contracts differ')
        if len(target.program_image)!=len(candidate.program_image):raise ValueError('whole decoded length differs')
        changes=[dict(decoded_linear=i,target=x,candidate=y) for i,(x,y) in enumerate(zip(target.program_image,candidate.program_image)) if x!=y]
        if len(changes)!=6:raise ValueError('known whole OP six-byte inequality differs')
        rounds.append(dict(number=number,build=result,objects=objects,all_objects=all_objects,game_objects=game_objects,products=products,
                           comparisons=comparisons,prior_score=prior_score,prior_title=prior_title,title_cpu=title_cpu,menu_cpu=menu_cpu,cpu=cpu,reentry=reentry,map_sha256=sha(mp.read_bytes()),
                           whole_decoded=dict(equal=not changes,changed_bytes=len(changes),changes=changes,
                                              original_ordered_relocations_equal=target.relocations==candidate.relocations)))
        print('PASS maintained OP entry cold round',number,flush=True)
    if rounds[0]['products']!=rounds[1]['products'] or rounds[0]['game_objects']!=rounds[1]['game_objects']:raise ValueError('OP entry cold determinism differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP entry compiler input changed: '+p)
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('OP entry canonical stored target changed')
    report=dict(kind='th03-op-maintained-entry-cold-compiler-probes',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,
                reference_archive_sha256=sha(archive.read_bytes()),toolchain_receipt_sha256=attestation,rounds=rounds,
                tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),new_maintained_decoded_bytes=1756,
                total_maintained_decoded_bytes=4403,diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,
                notes='Complete3094-byte original OP entry carrier compiled as maintained entry.cpp with explicit compatibility forwarding and previous1338-byte menu inl owner. New1485 complete screen/startup bytes and previous271 configuration bytes become sourcepresent; no duplicate menu/configuration credit. Real native CFG/IRAND/SCOPY/menu callbacks and2236-case entry model, previous4160-case menu and96-case title models rerun; previous543 score/helper raw-originalordered checked without inheriting actual DOS/devices/heap/resources/clock/canonicalstorage/fullproduct/exact acceptance. Two fresh frozen archives20products350gameobjects deterministic/all416OMF recorded; whole59770-byte OP six raw inequalities and original relocation-order failure retained. Staticseen reentry after returning execl exhausts budget; ordinaryCFG byte3 remains opaque native stack observation.')
    (output/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS source-present OP entry compiler probes; unowned column/exact open')


if __name__=='__main__':main()
