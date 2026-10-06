#!/usr/bin/env python3
"""Cold compile the bounded maintained OP title include with its original carrier."""
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
from review_th03_op_title import CS, RANGES, analyze, matrix
from review_th03_op_score import RANGES as SCORE_RANGES

ROOT=Path(__file__).resolve().parents[1]
MANIFEST='config/th03_op_title_candidate.toml'
PROOF='.analysis/sol-op-title-review-20261006.json'
PROOF_SHA='97f38ccda4b990f023198c49c9789d493a4365a3392cab41a22f28a0e9bf1205'


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run-id',required=True);args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',args.run_id):raise ValueError('invalid run id')
    output=ROOT/'.analysis/th03-op-title'/args.run_id;output.mkdir(parents=True,exist_ok=False)
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('OP title diagnostic proof differs')
    proof=json.loads(raw);inputs=dict(proof['inputs']);inputs[PROOF]=sha(raw)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP title prerequisite input differs: '+p)
    cfg=tomllib.loads((ROOT/MANIFEST).read_text());score=tomllib.loads((ROOT/'config/th03_op_score_candidate.toml').read_text())
    source_files=sorted(set([cfg['source'],*cfg['support_files'],*score['support_files'],*[u['source'] for u in score['units']]]))
    for p in [MANIFEST,'scripts/replay_th03_op_title.py',*source_files]:inputs[p]=sha((ROOT/p).read_bytes())
    snapshot=output/'repository-inputs'
    for p,h in inputs.items():
        if not p.startswith('.analysis/'):
            dest=snapshot/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,dest)
            if sha(dest.read_bytes())!=h:raise ValueError('OP title input changed while freezing')
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op');stored=read_verified_artifact(ROOT,artifact)
    target_path=proof['observations'][0]['path'];target=parse_mz((ROOT/target_path).read_bytes())
    if not target.valid or not proof['diagnostic_checks_pass'] or proof['exact_acceptance']:raise ValueError('OP title diagnostic prerequisite differs')
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
        carrier=work/cfg['carrier'];text=carrier.read_text()
        if text.count(cfg['anchor'])!=1:raise ValueError('title include anchor differs')
        split=text.index(cfg['anchor'])
        if sha(text[:split].encode())!=cfg['prefix_sha256']:raise ValueError('title original owned prefix differs')
        if (work/cfg['wrapper']).read_text()!=f'#include "{cfg["carrier"]}"\n':raise ValueError('title original wrapper differs')
        carrier.write_text(f'#include "{cfg["source"]}"\n\n'+text[split:])
        command=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%'
                 r'&&set PROCESSOR_ARCHITECTURE=AMD64&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat']
        result=execute(command,work,env,logs/'cold-build.log')
        objects={}
        for name,p in [('title',cfg['object'])]+[(u['id'],u['object']) for u in score['units']]:
            obj=describe_omf((work/p).read_bytes())
            if not obj['valid'] or 'TC86 Borland C++ 4.02' not in obj['translator_comments']:raise ValueError('OP title compiler producer differs')
            objects[name]=dict(path=p,normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'])
        all_objects={p.relative_to(work).as_posix():sha(normalize_dependency_timestamps(p.read_bytes())) for p in sorted((work/'obj').rglob('*.obj'))}
        game_objects={p:h for p,h in all_objects.items() if any(p.startswith(f'obj/th0{n}/') for n in range(1,6))}
        products={}
        for item in load_target_manifest(ROOT/'config/targets.toml')['artifacts']:
            p=Path('bin')/item['game']/Path(item['private_path']).name;products[p.as_posix()]=sha((work/p).read_bytes())
        if len(all_objects)!=416 or len(game_objects)!=350 or len(products)!=20:raise ValueError('OP title complete cold vector differs')
        candidate=parse_mz((work/'bin/th03/op.exe').read_bytes())
        if not candidate.valid:raise ValueError('invalid title compiler OP')
        meta=analyze(candidate.program_image)
        if meta['semantics']!=analyze(target.program_image)['semantics']:raise ValueError('title complete semantic topology differs')
        comparisons={}
        for name,a,z,c in RANGES:
            comp=extent_observation(target,candidate,dict(segment=CS,offset=a,start=CS*16+a,size=z));comparisons[name]=comp
            if not comp['ordered_relocations_equal'] or (name!='column' and not comp['raw_slice_equal']):raise ValueError('maintained title original raw/ordered comparison differs')
            if name=='column' and comp['raw_slice_equal']:raise ValueError('unowned column known raw inequality disappeared')
        prior_score={}
        for name,seg,a,z,c,owner in SCORE_RANGES:
            comp=extent_observation(target,candidate,dict(segment=seg,offset=a,start=seg*16+a,size=z));prior_score[name]=comp
            if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('prior score original raw/ordered comparison differs')
        mp=work/'obj/th03/op.map';map_text=mp.read_text();carriers=code_rows(map_text,len(candidate.program_image))
        title=next(c for c in carriers if c['module']==cfg['wrapper'] and c['size'])
        if title['segment']!=CS or title['offset']!=0x14e2 or title['size']!=902:raise ValueError('title original MAP carrier differs')
        publics=['op_animate()','op_fadein_animate()','box_main_to_submenu_animate()','box_submenu_to_main_animate()','box_column16_unput(unsigned int)']
        for (_,off,size,cleanup),public in zip(RANGES,publics):
            coords={(int(s,16),int(a,16)) for s,a in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(public)+r'\s*$',map_text,re.M)}
            if coords!={(CS,off)}:raise ValueError('title original public MAP entry differs')
        cpu=matrix(candidate)
        if normalized_contracts(cpu)!=normalized_contracts(proof['observations'][0]['cpu']):raise ValueError('maintained title native contracts differ')
        changes=[dict(decoded_linear=i,target=x,candidate=y) for i,(x,y) in enumerate(zip(target.program_image,candidate.program_image)) if x!=y]
        rounds.append(dict(number=number,build=result,objects=objects,all_objects=all_objects,game_objects=game_objects,products=products,
                           comparisons=comparisons,prior_score=prior_score,cpu=cpu,map_sha256=sha(mp.read_bytes()),
                           whole_decoded=dict(equal=not changes,changed_bytes=len(changes),changes=changes,
                                              original_ordered_relocations_equal=target.relocations==candidate.relocations)))
        print('PASS maintained OP title cold round',number,flush=True)
    if rounds[0]['products']!=rounds[1]['products'] or rounds[0]['game_objects']!=rounds[1]['game_objects']:raise ValueError('OP title cold determinism differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP title compiler input changed: '+p)
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('OP title canonical stored target changed')
    report=dict(kind='th03-op-maintained-title-cold-compiler-probes',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,
                reference_archive_sha256=sha(archive.read_bytes()),toolchain_receipt_sha256=attestation,rounds=rounds,
                tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),new_maintained_decoded_bytes=808,
                total_maintained_decoded_bytes=1309,diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,
                notes='Four complete contiguous functions in one maintained title inl replace a frozen compiler carrier prefix. Unowned column94 remains in the original private carrier and retains three raw unequal instruction bytes. Prior501 score source is included; prior543 bytes raw/ordered checked, old1168-call score contract proof retained without rerun/exact inheritance. Two fresh frozen scaffolds20products/350gameobjects deterministic, all416OMF recorded. Flat memory/library/timer fixtures grant no actual VRAM banking/ROM writes/ISR/resource/heap/canonicalstorage/wholeproduct/source/exact acceptance.')
    (output/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS source-present OP title compiler probes; unowned column/exact open')


if __name__=='__main__':main()
