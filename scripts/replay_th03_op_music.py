#!/usr/bin/env python3
"""Cold compile bounded Music Room owners around the unowned native copy function."""
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
from review_th03_op_music import CS, DS, RANGES, analyze, observe
from review_th03_op_score import RANGES as SCORE_RANGES

ROOT=Path(__file__).resolve().parents[1]
MANIFEST='config/th03_op_music_candidate.toml'
PROOF='.analysis/sol-op-music-review-20261006.json'
PROOF_SHA='22dc12eb9cb250c6bcd1f6febcd98198d651ac4c9f551572324c8e471350f1f2'


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run-id',required=True);args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',args.run_id):raise ValueError('invalid run id')
    output=ROOT/'.analysis/th03-op-music'/args.run_id;output.mkdir(parents=True,exist_ok=False)
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('OP Music Room diagnostic proof differs')
    proof=json.loads(raw);inputs=dict(proof['inputs']);inputs[PROOF]=sha(raw)
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP Music Room prerequisite input differs: '+p)
    cfg=tomllib.loads((ROOT/MANIFEST).read_text());score=tomllib.loads((ROOT/'config/th03_op_score_candidate.toml').read_text())
    title=tomllib.loads((ROOT/'config/th03_op_title_candidate.toml').read_text())
    entry=tomllib.loads((ROOT/'config/th03_op_entry_candidate.toml').read_text())
    menu=tomllib.loads((ROOT/'config/th03_op_menu_candidate.toml').read_text())
    source_files=sorted(set([*[u['source'] for u in cfg['units']],*cfg['support_files'],entry['source'],*entry['support_files'],menu['source'],title['source'],*title['support_files'],*score['support_files'],*[u['source'] for u in score['units']]]))
    for p in [MANIFEST,'scripts/replay_th03_op_music.py',*source_files]:inputs[p]=sha((ROOT/p).read_bytes())
    snapshot=output/'repository-inputs'
    for p,h in inputs.items():
        if not p.startswith('.analysis/'):
            dest=snapshot/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,dest)
            if sha(dest.read_bytes())!=h:raise ValueError('OP Music Room input changed while freezing')
    artifact=find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-op');stored=read_verified_artifact(ROOT,artifact)
    target_path=proof['observations'][0]['path'];target=parse_mz((ROOT/target_path).read_bytes())
    if not target.valid or not proof['diagnostic_checks_pass'] or proof['exact_acceptance']:raise ValueError('OP Music Room diagnostic prerequisite differs')
    subprocess.run([sys.executable,'scripts/attest_toolchain.py'],cwd=ROOT,check=True)
    tool=tomllib.loads((ROOT/'config/toolchain.toml').read_text());attestation=sha((ROOT/'.analysis/toolchain/attestation.json').read_bytes())
    env=os.environ.copy();env.update(DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(ROOT/tool['paths']['wine_prefix']),MSDOS_PATH=r'C:\TC4\BIN')
    archive=output/'reference.tar'
    subprocess.run(['git','archive','--format=tar',f'--output={archive}',cfg['reference_revision']],cwd=ROOT/'_reference/ReC98',check=True)
    archive_sha=sha(archive.read_bytes())
    previous=json.loads((ROOT/'.analysis/th03-op-entry/sol-op-entry-source-20261006/receipt.json').read_bytes())
    rounds=[]
    for number in (1,2):
        logs=output/f'round{number}';work=logs/'source';work.mkdir(parents=True)
        subprocess.run(['tar','-xf',str(archive),'-C',str(work)],check=True)
        if list(work.rglob('*.obj')) or list((work/'bin').glob('th0[1-5]/*.exe')):raise ValueError('cold Music Room archive contains game outputs')
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
        wrapper=work/cfg['wrapper'];carrier=work/cfg['carrier']
        if sha(wrapper.read_bytes())!=cfg['original_wrapper_sha256'] or sha(carrier.read_bytes())!=cfg['original_carrier_sha256']:raise ValueError('Music Room frozen carrier differs')
        text=carrier.read_text();a=text.index(cfg['unowned_anchor']);b=text.index(cfg['unowned_end_anchor'],a)
        if text.count(cfg['unowned_anchor'])!=1 or text.count(cfg['unowned_end_anchor'])!=1:raise ValueError('Music Room copy-function anchors differ')
        unowned=text[a:b]
        wrapper.write_text(f'#include "{cfg["units"][0]["source"]}"\n\n'+unowned+f'#include "{cfg["units"][1]["source"]}"\n')
        command=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%'
                 r'&&set PROCESSOR_ARCHITECTURE=AMD64&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat']
        result=execute(command,work,env,logs/'cold-build.log')
        objects={}
        for name,p in [('music',cfg['object']),('entry',entry['object']),('title',title['object'])]+[(u['id'],u['object']) for u in score['units']]:
            obj=describe_omf((work/p).read_bytes())
            if not obj['valid'] or 'TC86 Borland C++ 4.02' not in obj['translator_comments']:raise ValueError('OP Music Room compiler producer differs')
            objects[name]=dict(path=p,normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'])
        all_objects={p.relative_to(work).as_posix():sha(normalize_dependency_timestamps(p.read_bytes())) for p in sorted((work/'obj').rglob('*.obj'))}
        game_objects={p:h for p,h in all_objects.items() if any(p.startswith(f'obj/th0{n}/') for n in range(1,6))}
        products={}
        for item in load_target_manifest(ROOT/'config/targets.toml')['artifacts']:
            p=Path('bin')/item['game']/Path(item['private_path']).name;products[p.as_posix()]=sha((work/p).read_bytes())
        if products!=previous['rounds'][0]['products']:raise ValueError('Music Room changed previous complete product vector')
        if len(all_objects)!=416 or len(game_objects)!=350 or len(products)!=20:raise ValueError('OP Music Room complete cold vector differs')
        candidate=parse_mz((work/'bin/th03/op.exe').read_bytes())
        if not candidate.valid:raise ValueError('invalid Music Room compiler OP')
        meta=analyze(candidate.program_image)
        comparisons={}
        for name,seg,a,z,c,far in RANGES:
            comp=extent_observation(target,candidate,dict(segment=seg,offset=a,start=seg*16+a,size=z));comparisons[name]=comp
            if not comp['ordered_relocations_equal'] or (name!='put' and not comp['raw_slice_equal']):raise ValueError('Music Room original raw/ordered comparison differs')
            if name=='put' and comp['raw_slice_equal']:raise ValueError('Music Room unowned encoding failure disappeared')
        music_data=extent_observation(target,candidate,dict(segment=DS,offset=0x5f2,start=DS*16+0x5f2,size=0x3f0))
        if not music_data['raw_slice_equal']:raise ValueError('Music Room original data bytes differ')
        prior_score={}
        for name,seg,a,z,c,owner in SCORE_RANGES:
            comp=extent_observation(target,candidate,dict(segment=seg,offset=a,start=seg*16+a,size=z));prior_score[name]=comp
            if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('prior score original raw/ordered comparison differs')
        mp=work/'obj/th03/op.map';map_text=mp.read_text();carriers=code_rows(map_text,len(candidate.program_image))
        owner=next(c for c in carriers if c['module']==cfg['wrapper'] and c['size'])
        if (owner['segment'],owner['offset'],owner['size'])!=(CS,0xc1e,2244):raise ValueError('Music Room original MAP carrier differs')
        entry_owner=next(c for c in carriers if c['module']==entry['wrapper'] and c['size'])
        if (entry_owner['segment'],entry_owner['offset'],entry_owner['size'])!=(CS,8,3094):raise ValueError('prior entry carrier differs')
        prior_entry={}
        for name,seg,a,z,c,far in ENTRY_RANGES:
            comp=extent_observation(target,candidate,dict(segment=seg,offset=a,start=seg*16+a,size=z));prior_entry[name]=comp
            if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('prior entry original raw/ordered differs')
        publics=['track_put_both(unsigned char,unsigned char)','tracklist_put_both(unsigned char)',
                 'nopoly_b_snap()','nopoly_b_free()','nopoly_b_put()',
                 'polygon_build(screen_point_t near*,int,space_changing_pixel_t,int,int,unsigned char)',
                 'polygons_update_and_render()','music_update_render_and_flip()',
                 'cmt_bg_snap()','cmt_load(int)','cmt_bg_free()','cmt_unput()',
                 'cmt_load_unput_and_put(int)','musicroom_menu()']
        for (_,seg,off,size,cleanup,far),public in zip(RANGES[:14],publics):
            coords={(int(s,16),int(a,16)) for s,a in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+re.escape(public)+r'\s*$',map_text,re.M)}
            if coords!={(seg,off)}:raise ValueError('Music Room original public entry differs: '+public)
        prior_title={}
        for name,a,z,c in TITLE_RANGES:
            comp=extent_observation(target,candidate,dict(segment=CS,offset=a,start=CS*16+a,size=z));prior_title[name]=comp
            if not comp['ordered_relocations_equal'] or (name!='column' and not comp['raw_slice_equal']):raise ValueError('prior title raw/ordered differs')
            if name=='column' and comp['raw_slice_equal']:raise ValueError('prior column failure disappeared')

        if candidate.program_image[DS*16+0xdc:DS*16+0x166]!=target.program_image[DS*16+0xdc:DS*16+0x166]:raise ValueError('menu original labels/statics differ')
        # The complete prior product vector is identical; retain old owner
        # raw/ordered comparisons and focus execution on the changed carrier.
        baseline=proof['observations'][0]['cpu'];indices=[]
        for i,row in enumerate(baseline):
            fixture=row['scenario'];name=row['function']
            if not fixture['if'] and not fixture['df']:
                if name=='track' and row['args'][1]!=20:continue
                if name=='load' and (row['args']!=[40] or fixture['read']!=41):continue
                indices.append(i)
            elif not fixture['if'] and fixture['df'] and name in ('put','comment','flip'):indices.append(i)
            elif fixture['if'] and name=='music' and fixture['inputs']==[0,0,0x8000,0,0x1000,0]:indices.append(i)
        cpu=[observe(candidate,baseline[i]['function'],baseline[i]['scenario'],baseline[i]['args'],baseline[i]['sequence']) for i in indices]
        if normalized_contracts(cpu)!=normalized_contracts([baseline[i] for i in indices]):raise ValueError('maintained Music Room source-case contracts differ')
        visited={tuple(a) for row in cpu for a in row['visited']}
        coverage=dict(instructions=len(meta['bounds']),visited=len(meta['bounds']&visited),unvisited=[list(a) for a in sorted(meta['bounds']-visited)])
        if coverage['unvisited']:raise ValueError('maintained Music Room native coverage incomplete: '+str(coverage['unvisited']))
        if len(target.program_image)!=len(candidate.program_image):raise ValueError('whole decoded length differs')
        changes=[dict(decoded_linear=i,target=x,candidate=y) for i,(x,y) in enumerate(zip(target.program_image,candidate.program_image)) if x!=y]
        if len(changes)!=6:raise ValueError('known whole OP six-byte inequality differs')
        rounds.append(dict(number=number,build=result,objects=objects,all_objects=all_objects,game_objects=game_objects,products=products,
                           comparisons=comparisons,music_data=music_data,prior_entry=prior_entry,prior_score=prior_score,prior_title=prior_title,cpu=cpu,case_indices=indices,coverage=coverage,map_sha256=sha(mp.read_bytes()),
                           whole_decoded=dict(equal=not changes,changed_bytes=len(changes),changes=changes,
                                              original_ordered_relocations_equal=target.relocations==candidate.relocations)))
        print('PASS maintained OP Music Room cold round',number,flush=True)
    if rounds[0]['products']!=rounds[1]['products'] or rounds[0]['game_objects']!=rounds[1]['game_objects']:raise ValueError('OP Music Room cold determinism differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('OP Music Room compiler input changed: '+p)
    if sha(archive.read_bytes())!=archive_sha:raise ValueError('Music Room frozen archive changed')
    for p in source_files:
        if sha((snapshot/p).read_bytes())!=inputs[p]:raise ValueError('Music Room source snapshot changed: '+p)
    if read_verified_artifact(ROOT,artifact)!=stored:raise ValueError('OP Music Room canonical stored target changed')
    report=dict(kind='th03-op-maintained-music-room-cold-compiler-probes',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,
                reference_archive_sha256=archive_sha,toolchain_receipt_sha256=attestation,rounds=rounds,
                tools=dict(capstone=version('capstone'),unicorn=version('unicorn')),new_maintained_decoded_bytes=2214,
                total_maintained_decoded_bytes=6617,diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,
                notes='Complete2244-byte Music Room carrier compiled with bounded216/1998-byte maintained includes and14explicit compatibility imports, retaining private unowned30-byte natural copy function between. Native IRAND42/POLAR26 context only; complete ordered calls/ports/stores/bulk operand reads/fullphysical memory in44 selected source cases/all807nativepositions rerun. Complete product vector matches previous maintained entry; previous entry/menu/title and543 score/helper rawordered retained without repeating their old native matrices. Two fresh20product350gameobject vectors deterministic/all416OMF recorded. Original copy30 raw encoding inequalities persist, together with three title bytes and one candidate data alignment byte; original relocation order unequal. Actual graphics/heap/DOS/devices/clock/resources/CRT/headers/DATA/BSS/canonicalstorage/fullproduct/exact remain open.')
    (output/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS source-present OP Music Room compiler probes; unowned copy/column/exact open')


if __name__=='__main__':main()
