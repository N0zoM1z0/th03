#!/usr/bin/env python3
"""Cold-build complete shared/ending PI wrappers with separately bound carrier producers."""
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
from review_th03_shared_pi import ROOT, PROFILES, PARENT, PARENT_SHA, analyze, matrix, coverage, semantic, sha

MANIFEST='config/th03_shared_pi_candidate.toml'
PROOF='.analysis/sol-shared-pi-review-20261006.json'
PROOF_SHA='51324b64b0df4d7b2e865b956b63bf02f347bae0f4af9179d4a85e62325b427b'


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run-id',required=True);args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',args.run_id):raise ValueError('invalid run id')
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('PI wrappers diagnostic proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw)}
    if not proof['diagnostic_checks_pass'] or proof['exact_acceptance']:raise ValueError('PI wrappers diagnostic scope differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('PI wrappers prerequisite differs: '+p)
    output=ROOT/'.analysis/th03-shared-pi'/args.run_id;output.mkdir(parents=True,exist_ok=False)
    cfg=tomllib.loads((ROOT/MANIFEST).read_text());manifests={};source_files={*[c['source'] for c in cfg['carriers']],*cfg['support_files']}
    for name in ('score','title','entry','menu','music','select'):
        path=f'config/th03_op_{name}_candidate.toml';c=manifests[name]=tomllib.loads((ROOT/path).read_text());inputs[path]=sha((ROOT/path).read_bytes());source_files.update(c.get('support_files',[]))
        if 'source' in c:source_files.add(c['source'])
        for u in c.get('units',[]):source_files.add(u['source'])
    shared={}
    for name in ('cdg_load','cdg_draw','text','math','snd_load'):
        path=f'config/th03_shared_{name}_candidate.toml';c=shared[name]=tomllib.loads((ROOT/path).read_text());inputs[path]=sha((ROOT/path).read_bytes());source_files.update(c.get('support_files',[]))
        if 'source' in c:source_files.add(c['source'])
        if 'glyph_include' in c:source_files.add(c['glyph_include'])
        source_files.update(ca['source'] for ca in c.get('carriers',[]))
    source_files=sorted(source_files)
    for p in [MANIFEST,'scripts/replay_th03_shared_pi.py','tests/test_shared_pi_review.py','.analysis/sol-shared-pi-controls-20261006.log',*source_files]:inputs[p]=sha((ROOT/p).read_bytes())
    snapshot=output/'repository-inputs'
    for p,h in inputs.items():
        if p.startswith('.analysis/'):continue
        dest=snapshot/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,dest)
        if sha(dest.read_bytes())!=h:raise ValueError('PI wrappers source snapshot changed')
    previous=json.loads((ROOT/PARENT).read_bytes())
    if sha((ROOT/PARENT).read_bytes())!=PARENT_SHA:raise ValueError('PI wrappers previous cold proof differs')
    artifacts={a:find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-'+a) for a in PROFILES}
    stored={a:read_verified_artifact(ROOT,x) for a,x in artifacts.items()};targets={a:parse_mz((ROOT/proof['observations'][a][0]['path']).read_bytes()) for a in PROFILES}
    subprocess.run([sys.executable,'scripts/attest_toolchain.py'],cwd=ROOT,check=True)
    tool=tomllib.loads((ROOT/'config/toolchain.toml').read_text());attestation=sha((ROOT/'.analysis/toolchain/attestation.json').read_bytes())
    env=os.environ.copy();env.update(DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(ROOT/tool['paths']['wine_prefix']),MSDOS_PATH=r'C:\TC4\BIN')
    archive=output/'reference.tar';subprocess.run(['git','archive','--format=tar',f'--output={archive}',cfg['reference_revision']],cwd=ROOT/'_reference/ReC98',check=True);archive_sha=sha(archive.read_bytes());rounds=[]
    for number in (1,2):
        logs=output/f'round{number}';work=logs/'source';work.mkdir(parents=True);subprocess.run(['tar','-xf',str(archive),'-C',str(work)],check=True)
        if list(work.rglob('*.obj')) or list((work/'bin').glob('th0[1-5]/*.exe')):raise ValueError('PI wrappers archive is not cold')
        for p in source_files:
            dest=work/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(snapshot/p,dest)
            if Path(p).suffix in ('.asm','.inc'):dest.write_bytes(dest.read_bytes().replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'))
        apply_previous(work,manifests)
        for c in [shared['cdg_load'],shared['text'],*shared['snd_load']['carriers'],*cfg['carriers']]:
            if sha((work/c['wrapper']).read_bytes())!=c['original_wrapper_sha256']:raise ValueError('PI wrappers original CPP wrapper differs')
            (work/c['wrapper']).write_text(f'#include "{c["source"]}"\n')
        for c in shared['cdg_draw']['carriers']:
            if sha((work/c['wrapper']).read_bytes())!=c['original_wrapper_sha256']:raise ValueError('PI wrappers preceding drawing wrapper differs')
            (work/c['wrapper']).write_bytes(('include '+c['source']+'\r\n').encode())
        for c in shared['math']['carriers']:
            original=(work/c.get('original_wrapper',c['wrapper'])).read_bytes()
            if c.get('original_wrapper',c['wrapper']).endswith('.asm'):original=original.replace(b'\r\n',b'\n')
            if sha(original)!=c['original_wrapper_sha256']:raise ValueError('PI wrappers preceding ASM producer differs')
            (work/c['wrapper']).write_bytes(('include '+c['source']+'\r\n').encode())
        tup=work/'Tupfile.lua';original=tup.read_bytes()
        if sha(original)!=shared['math']['original_tup_sha256']:raise ValueError('PI wrappers original frozen link graph differs')
        text=original.decode();marker='th03:branch(MODEL_LARGE, { cflags = "-DBINARY=\'L\'" }):link("mainl", {'
        start=text.index(marker);end=text.index('\n})',start)+3;block=text[start:end]
        if block.count('"th03/vector.cpp"')!=1:raise ValueError('PI wrappers preceding MAINL vector position differs')
        tup.write_text(text[:start]+block.replace('"th03/vector.cpp"','"th03/vector_far.asm"')+text[end:])
        if sha(tup.read_bytes())!=previous['rounds'][0]['link_graph']['sha256']:raise ValueError('PI wrappers changed preceding link graph')
        command=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%' r'&&set PROCESSOR_ARCHITECTURE=AMD64&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat']
        build=execute(command,work,env,logs/'cold-build.log')
        log=(logs/'cold-build.log').read_text()
        for c in cfg['carriers']:
            binary='L' if c['artifacts']==['mainl'] else 'O'
            if f"-DGAME=3 -ml -DBINARY='{binary}' -nobj/th03/ {c['wrapper']}" not in log:raise ValueError('PI original GAME3 compiler association differs')
        objects={p.relative_to(work).as_posix():sha(normalize_dependency_timestamps(p.read_bytes())) for p in sorted((work/'obj').rglob('*.obj'))};game={p:h for p,h in objects.items() if any(p.startswith(f'obj/th0{n}/') for n in range(1,6))};products={}
        for item in load_target_manifest(ROOT/'config/targets.toml')['artifacts']:
            p=Path('bin')/item['game']/Path(item['private_path']).name;products[p.as_posix()]=sha((work/p).read_bytes())
        if products!=previous['rounds'][0]['products'] or len(products)!=20 or len(game)!=351 or len(objects)!=417:raise ValueError('PI wrappers complete product/object vector differs')
        owned={c['object'] for c in cfg['carriers']}
        if {p:h for p,h in game.items() if p not in owned}!={p:h for p,h in previous['rounds'][0]['game_objects'].items() if p not in owned}:raise ValueError('PI wrappers changed another original game object')
        nongame={p:dict(previous=previous['rounds'][0]['all_objects'][p],current=h) for p,h in objects.items() if p not in game and h!=previous['rounds'][0]['all_objects'][p]};producers={}
        for c in cfg['carriers']:
            raw=(work/c['object']).read_bytes();obj=describe_omf(raw);old=ROOT/Path(PARENT).parent/f'round{number}/source'/c['object'];inputs[str(old.relative_to(ROOT))]=sha(old.read_bytes())
            if not obj['valid'] or obj['translator_comments']!=['TC86 Borland C++ 4.02'] or producer_records(raw)!=producer_records(old.read_bytes()):raise ValueError('PI wrappers complete original nondependency OMF differs')
            segs=[r.data.hex() for r in parse_omf(raw) if r.name=='SEGDEF']
            if segs!=c['segments']:raise ValueError('PI wrappers original complete CODE/DATA0/BSS0 layout differs')
            producers[c['object']]=dict(normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'],records=producer_records(raw),segments=segs,original_nondependency_records_equal=True,physical_game_macro=3)
        observations={}
        for art,p in PROFILES.items():
            candidate=parse_mz((work/f'bin/th03/{art}.exe').read_bytes());meta=analyze(candidate.program_image,p);mp=work/f'obj/th03/{art}.map';map_text=mp.read_text();maprows=code_rows(map_text,len(candidate.program_image));comparisons={}
            for c in cfg['carriers']:
                if art not in c['artifacts']:continue
                row=next(r for r in maprows if r['module']==c['wrapper'] and r['size'])
                if (row['segment'],row['offset'],row['size'])!=(c[art+'_segment'],c[art+'_offset'],c['size']):raise ValueError('PI wrappers complete source MAP ownership differs')
                comp=extent_observation(targets[art],candidate,row)
                if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('PI wrappers complete original raw/ordered carrier differs')
                comparisons[c['wrapper']]=comp
            bindings=[(public,p['cs'],p[key],True) for key,public in [('palette','pi_palette_apply'),('put','pi_put_8'),('load','pi_load'),('interlace','pi_put_interlace_8'),('quarter','pi_put_quarter_8')] if key in p]
            bindings += [(public,p['ds'],p[key],False) for key,public in [('headers','_pi_headers'),('buffers','_pi_buffers'),('palettes','_Palettes')]]
            for public,seg,start,cpp in bindings:
                label=re.escape(public)+(r'\(.*\)' if cpp else '')
                coords={(int(a,16),int(b,16)) for a,b in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+label+r'\s*$',map_text,re.M)}
                if coords!={(seg,start)}:raise ValueError('PI original public binding differs: '+public)
            cpu=matrix(candidate,p,focused=True)
            if semantic(cpu)!=semantic(matrix(targets[art],p,focused=True)):raise ValueError('PI wrappers maintained scalar contracts differ')
            changes=[dict(decoded_linear=i,target=x,candidate=y) for i,(x,y) in enumerate(zip(targets[art].program_image,candidate.program_image)) if x!=y]
            if len(candidate.program_image)!=len(targets[art].program_image) or len(changes)!=(6 if art=='op' else 21):raise ValueError('PI wrappers known whole decoded inequality differs')
            observations[art]=dict(comparisons=comparisons,cpu=cpu,coverage=coverage(meta,cpu),map_sha256=sha(mp.read_bytes()),whole_decoded=dict(equal=False,changes=changes,original_ordered_relocations_equal=targets[art].relocations==candidate.relocations))
        rounds.append(dict(number=number,build=build,all_objects=objects,game_objects=game,products=products,nongame_object_changes=nongame,producers=producers,link_graph=dict(sha256=sha(tup.read_bytes()),unchanged_from_parent=True),observations=observations));print('PASS maintained PI wrappers cold round',number,flush=True)
    if rounds[0]['products']!=rounds[1]['products'] or rounds[0]['game_objects']!=rounds[1]['game_objects']:raise ValueError('PI wrappers cold determinism differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('PI wrappers source input changed: '+p)
    if sha(archive.read_bytes())!=archive_sha or any(sha((snapshot/p).read_bytes())!=inputs[p] for p in source_files):raise ValueError('PI wrappers frozen archive/source snapshot changed')
    if any(read_verified_artifact(ROOT,a)!=stored[art] for art,a in artifacts.items()):raise ValueError('PI wrappers canonical target changed')
    report=dict(kind='th03-shared-pi-maintained-cold-probes',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,reference_archive_sha256=archive_sha,toolchain_receipt_sha256=attestation,rounds=rounds,diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,notes='Complete four PI CPP carriers555 independently bound: OP243 shared palette/put/load; MAINL555 includes ending interlace/quarter. Original GAME3 large-model TC86/CODE/DATA0/BSS0/nondependency OMF/public/MAP/raw/ordered relocations match; current link graph unchanged. Two20product351gameobject vectors deterministic/all417OMF recorded; all20products equal preceding sound loader,347othergameobjects unchanged. Nine nongame Research timestamp changes separate. All native wrapper/free/memcpy positions, complete physical1MiB outside stack/ordered stores/callback requests/frames/IFDF/overlap/live headers/far normalization/unsigned counter/status and repeated free checked. Graphics/heap/loader callbacks are explicit fixtures; native PI decoder, assets/DGROUP/header ownership/real devices/canonical packing/whole products/exact remain open.')
    (output/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS source-present shared PI wrappers cold probes; exact open')


if __name__=='__main__':main()
