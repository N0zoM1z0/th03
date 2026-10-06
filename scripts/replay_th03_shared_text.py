#!/usr/bin/env python3
"""Cold compile the complete shared text TU and bounded glyph macros."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib

from lib.omf import describe_omf, normalize_dependency_timestamps, parse_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from replay_th03_main_exact_units import execute
from replay_th03_shared_cdg_load import apply_previous
from replay_th03_shared_cdg_draw import producer_records
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import sha
from review_th03_shared_text import ROOT, PROFILES, PARENT, PARENT_SHA, analyze, matrix, coverage, semantic

MANIFEST='config/th03_shared_text_candidate.toml'
PROOF='.analysis/sol-shared-text-review-20261006.json'
PROOF_SHA='42cd6efc52d9d96620ea26426130f87e3cc222d680d06248959427f8d913a6df'


def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--run-id',required=True); args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',args.run_id): raise ValueError('invalid run id')
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA: raise ValueError('text diagnostic proof differs')
    proof=json.loads(raw); inputs={**proof['inputs'],PROOF:sha(raw)}
    if not proof['diagnostic_checks_pass'] or proof['exact_acceptance']: raise ValueError('text diagnostic scope differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h: raise ValueError('text prerequisite differs: '+p)
    output=ROOT/'.analysis/th03-shared-text'/args.run_id; output.mkdir(parents=True,exist_ok=False)
    cfg=tomllib.loads((ROOT/MANIFEST).read_text()); manifests={}
    source_files={cfg['source'],cfg['glyph_include'],*cfg['support_files']}
    for name in ('score','title','entry','menu','music','select'):
        path=f'config/th03_op_{name}_candidate.toml'; c=manifests[name]=tomllib.loads((ROOT/path).read_text()); inputs[path]=sha((ROOT/path).read_bytes())
        source_files.update(c.get('support_files',[]))
        if 'source' in c: source_files.add(c['source'])
        for u in c.get('units',[]): source_files.add(u['source'])
    load_path='config/th03_shared_cdg_load_candidate.toml'; draw_path='config/th03_shared_cdg_draw_candidate.toml'
    load=tomllib.loads((ROOT/load_path).read_text()); draw=tomllib.loads((ROOT/draw_path).read_text())
    source_files.update([load['source'],*load['support_files'],*draw['support_files'],*[c['source'] for c in draw['carriers']]])
    source_files=sorted(source_files)
    for p in [MANIFEST,load_path,draw_path,'scripts/replay_th03_shared_text.py','tests/test_shared_text_review.py','.analysis/sol-shared-text-controls-20261006.log',*source_files]: inputs[p]=sha((ROOT/p).read_bytes())
    snapshot=output/'repository-inputs'
    for p,h in inputs.items():
        if p.startswith('.analysis/'): continue
        dest=snapshot/p; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(ROOT/p,dest)
        if sha(dest.read_bytes())!=h: raise ValueError('text source snapshot changed')
    previous=json.loads((ROOT/PARENT).read_bytes())
    if sha((ROOT/PARENT).read_bytes())!=PARENT_SHA: raise ValueError('text previous cold proof differs')
    artifacts={a:find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-'+a) for a in PROFILES}
    stored={a:read_verified_artifact(ROOT,x) for a,x in artifacts.items()}
    targets={a:parse_mz((ROOT/proof['observations'][a][0]['path']).read_bytes()) for a in PROFILES}
    subprocess.run([sys.executable,'scripts/attest_toolchain.py'],cwd=ROOT,check=True)
    tool=tomllib.loads((ROOT/'config/toolchain.toml').read_text()); attestation=sha((ROOT/'.analysis/toolchain/attestation.json').read_bytes())
    env=os.environ.copy(); env.update(DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(ROOT/tool['paths']['wine_prefix']),MSDOS_PATH=r'C:\TC4\BIN')
    archive=output/'reference.tar'; subprocess.run(['git','archive','--format=tar',f'--output={archive}',cfg['reference_revision']],cwd=ROOT/'_reference/ReC98',check=True); archive_sha=sha(archive.read_bytes())
    rounds=[]
    for number in (1,2):
        logs=output/f'round{number}'; work=logs/'source'; work.mkdir(parents=True)
        subprocess.run(['tar','-xf',str(archive),'-C',str(work)],check=True)
        if list(work.rglob('*.obj')) or list((work/'bin').glob('th0[1-5]/*.exe')): raise ValueError('text archive is not cold')
        for p in source_files:
            dest=work/p; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(snapshot/p,dest)
            if Path(p).suffix in ('.asm','.inc'): dest.write_bytes(dest.read_bytes().replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'))
        apply_previous(work,manifests)
        if sha((work/load['wrapper']).read_bytes())!=load['original_wrapper_sha256']: raise ValueError('text preceding loader wrapper differs')
        (work/load['wrapper']).write_text(f'#include "{load["source"]}"\n')
        for c in draw['carriers']:
            if sha((work/c['wrapper']).read_bytes())!=c['original_wrapper_sha256']: raise ValueError('text preceding drawing wrapper differs')
            (work/c['wrapper']).write_bytes(('include '+c['source']+'\r\n').encode())
        if sha((work/cfg['wrapper']).read_bytes())!=cfg['original_wrapper_sha256'] or sha((work/cfg['carrier']).read_bytes())!=cfg['original_carrier_sha256'] or sha((work/'th01/hardware/grppsafx.cpp').read_bytes())!=cfg['original_glyph_sha256']: raise ValueError('text original frozen provider differs')
        (work/cfg['wrapper']).write_text(f'#include "{cfg["source"]}"\n')
        command=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%' r'&&set PROCESSOR_ARCHITECTURE=AMD64&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat']
        build=execute(command,work,env,logs/'cold-build.log')
        objects={p.relative_to(work).as_posix():sha(normalize_dependency_timestamps(p.read_bytes())) for p in sorted((work/'obj').rglob('*.obj'))}
        game={p:h for p,h in objects.items() if any(p.startswith(f'obj/th0{n}/') for n in range(1,6))}
        products={}
        for item in load_target_manifest(ROOT/'config/targets.toml')['artifacts']:
            p=Path('bin')/item['game']/Path(item['private_path']).name; products[p.as_posix()]=sha((work/p).read_bytes())
        if products!=previous['rounds'][0]['products'] or len(products)!=20 or len(game)!=350 or len(objects)!=416: raise ValueError('text complete product/object vector differs')
        if {p:h for p,h in game.items() if p!=cfg['object']}!={p:h for p,h in previous['rounds'][0]['game_objects'].items() if p!=cfg['object']}: raise ValueError('text changed another game object')
        nongame={p:dict(previous=previous['rounds'][0]['all_objects'][p],current=h) for p,h in objects.items() if p not in game and h!=previous['rounds'][0]['all_objects'][p]}
        raw=(work/cfg['object']).read_bytes(); obj=describe_omf(raw); old=ROOT/Path(proof['observations']['op'][number]['path']).parents[2]/cfg['object']; inputs[str(old.relative_to(ROOT))]=sha(old.read_bytes())
        if not obj['valid'] or producer_records(raw)!=producer_records(old.read_bytes()): raise ValueError('text original ordered nondependency producer records differ')
        observations={}
        for art,p in PROFILES.items():
            candidate=parse_mz((work/f'bin/th03/{art}.exe').read_bytes()); meta=analyze(candidate.program_image,p); mp=work/f'obj/th03/{art}.map'; map_text=mp.read_text()
            row=next(r for r in code_rows(map_text,len(candidate.program_image)) if r['module']==cfg['wrapper'] and r['size'])
            if (row['segment'],row['offset'],row['size'])!=(cfg[art+'_segment'],cfg[art+'_offset'],cfg['size']): raise ValueError('text complete MAP ownership differs')
            comp=extent_observation(targets[art],candidate,row)
            if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']: raise ValueError('text complete original raw/ordered carrier differs')
            coords={(int(seg,16),int(at,16)) for seg,at in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?graph_putsa_fx\(',map_text,re.M)}
            if coords!={(p['cs'],p['start'])}: raise ValueError('text original public binding differs')
            cpu=matrix(candidate,p)
            if json.loads(json.dumps(semantic(cpu)))!=semantic(proof['observations'][art][0]['cpu']): raise ValueError('text maintained scalar contracts differ')
            changes=[dict(decoded_linear=i,target=x,candidate=y) for i,(x,y) in enumerate(zip(targets[art].program_image,candidate.program_image)) if x!=y]
            if len(candidate.program_image)!=len(targets[art].program_image) or len(changes)!=(6 if art=='op' else 21): raise ValueError('text known whole decoded inequality differs')
            observations[art]=dict(comparison=comp,cpu=cpu,coverage=coverage(meta,cpu),map_sha256=sha(mp.read_bytes()),whole_decoded=dict(equal=False,changes=changes,original_ordered_relocations_equal=targets[art].relocations==candidate.relocations))
        rounds.append(dict(number=number,build=build,all_objects=objects,game_objects=game,products=products,nongame_object_changes=nongame,producer=dict(normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'],records=producer_records(raw),segments=[r.data.hex() for r in parse_omf(raw) if r.name=='SEGDEF'],original_nondependency_records_equal=True),observations=observations))
        print('PASS maintained shared text cold round',number,flush=True)
    if rounds[0]['products']!=rounds[1]['products'] or rounds[0]['game_objects']!=rounds[1]['game_objects']: raise ValueError('text cold determinism differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h: raise ValueError('text source input changed: '+p)
    if sha(archive.read_bytes())!=archive_sha or any(sha((snapshot/p).read_bytes())!=inputs[p] for p in source_files): raise ValueError('text frozen archive/source snapshot changed')
    if any(read_verified_artifact(ROOT,a)!=stored[art] for art,a in artifacts.items()): raise ValueError('text canonical target changed')
    report=dict(kind='th03-shared-text-maintained-cold-probes',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,reference_archive_sha256=archive_sha,toolchain_receipt_sha256=attestation,rounds=rounds,diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,notes='One complete shared613-byte C++ TU and bounded glyph macro include. Independent OP/MAINL bindings, complete raw/original ordered relocations and original nondependency OMF records. Two fresh20product350gameobject vectors; all20products equal preceding drawing and349othergameobjects unchanged. All416OMF recorded; Research changes separate. Native GRCG46context bytes not newly owned. Full scalar chronological ports/converter/stores, stack-outside1MiB, persistent reentry, ABI/register/IFDF and all250instruction positions checked. Synthetic ROM/CRT classifier and converter fixtures grant no physicaldevice/CRT/DATA/BSS/resource/canonicalpacking/fullproduct/exact acceptance.')
    (output/'receipt.json').write_text(json.dumps(report,indent=2)+'\n'); print('PASS source-present shared text cold probes; exact open')


if __name__=='__main__': main()
