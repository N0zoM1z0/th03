#!/usr/bin/env python3
"""Cold-build complete shared input/timing carriers with separately bound carrier producers."""
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
from review_th03_shared_input import ROOT, PROFILES, PARENT, PARENT_SHA, analyze, matrix, coverage, semantic, sha

MANIFEST='config/th03_shared_input_candidate.toml'
PROOF='.analysis/sol-shared-input-review-20261006-b.json'
PROOF_SHA='b745faf78395381ef239d3a0992a2c7d2167b9d372894d2e3930abc1d0e0c97e'


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--run-id',required=True);args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',args.run_id):raise ValueError('invalid run id')
    raw=(ROOT/PROOF).read_bytes()
    if sha(raw)!=PROOF_SHA:raise ValueError('input/timing diagnostic proof differs')
    proof=json.loads(raw);inputs={**proof['inputs'],PROOF:sha(raw)}
    if not proof['diagnostic_checks_pass'] or proof['exact_acceptance']:raise ValueError('input/timing diagnostic scope differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('input/timing prerequisite differs: '+p)
    output=ROOT/'.analysis/th03-shared-input'/args.run_id;output.mkdir(parents=True,exist_ok=False)
    cfg=tomllib.loads((ROOT/MANIFEST).read_text());manifests={};source_files={*[c['source'] for c in cfg['carriers']],*cfg['support_files']}
    for name in ('score','title','entry','menu','music','select'):
        path=f'config/th03_op_{name}_candidate.toml';c=manifests[name]=tomllib.loads((ROOT/path).read_text());inputs[path]=sha((ROOT/path).read_bytes());source_files.update(c.get('support_files',[]))
        if 'source' in c:source_files.add(c['source'])
        for u in c.get('units',[]):source_files.add(u['source'])
    shared={}
    for name in ('cdg_load','cdg_draw','text','math','snd_load','pi'):
        path=f'config/th03_shared_{name}_candidate.toml';c=shared[name]=tomllib.loads((ROOT/path).read_text());inputs[path]=sha((ROOT/path).read_bytes());source_files.update(c.get('support_files',[]))
        if 'source' in c:source_files.add(c['source'])
        if 'glyph_include' in c:source_files.add(c['glyph_include'])
        source_files.update(ca['source'] for ca in c.get('carriers',[]))
    source_files=sorted(source_files)
    for p in [MANIFEST,'scripts/replay_th03_shared_input.py','tests/test_shared_input_review.py','.analysis/sol-shared-input-controls-20261006-b.log',*source_files]:inputs[p]=sha((ROOT/p).read_bytes())
    snapshot=output/'repository-inputs'
    for p,h in inputs.items():
        if p.startswith('.analysis/'):continue
        dest=snapshot/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/p,dest)
        if sha(dest.read_bytes())!=h:raise ValueError('input/timing source snapshot changed')
    previous=json.loads((ROOT/PARENT).read_bytes())
    if sha((ROOT/PARENT).read_bytes())!=PARENT_SHA:raise ValueError('input/timing previous cold proof differs')
    artifacts={a:find_artifact(load_target_manifest(ROOT/'config/targets.toml'),'th03-'+a) for a in PROFILES}
    stored={a:read_verified_artifact(ROOT,x) for a,x in artifacts.items()};targets={a:parse_mz((ROOT/proof['observations'][a][0]['path']).read_bytes()) for a in PROFILES}
    subprocess.run([sys.executable,'scripts/attest_toolchain.py'],cwd=ROOT,check=True)
    tool=tomllib.loads((ROOT/'config/toolchain.toml').read_text());attestation=sha((ROOT/'.analysis/toolchain/attestation.json').read_bytes())
    env=os.environ.copy();env.update(DISPLAY='',WAYLAND_DISPLAY='',WINEDEBUG='-all',WINEPREFIX=str(ROOT/tool['paths']['wine_prefix']),MSDOS_PATH=r'C:\TC4\BIN')
    archive=output/'reference.tar';subprocess.run(['git','archive','--format=tar',f'--output={archive}',cfg['reference_revision']],cwd=ROOT/'_reference/ReC98',check=True);archive_sha=sha(archive.read_bytes());rounds=[]
    for number in (1,2):
        logs=output/f'round{number}';work=logs/'source';work.mkdir(parents=True);subprocess.run(['tar','-xf',str(archive),'-C',str(work)],check=True)
        if list(work.rglob('*.obj')) or list((work/'bin').glob('th0[1-5]/*.exe')):raise ValueError('input/timing archive is not cold')
        for p in source_files:
            dest=work/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(snapshot/p,dest)
            if Path(p).suffix in ('.asm','.inc'):dest.write_bytes(dest.read_bytes().replace(b'\r\n',b'\n').replace(b'\n',b'\r\n'))
        apply_previous(work,manifests)
        for c in [shared['cdg_load'],shared['text'],*shared['snd_load']['carriers'],*shared['pi']['carriers'],*cfg['carriers']]:
            if sha((work/c['wrapper']).read_bytes())!=c['original_wrapper_sha256']:raise ValueError('input/timing original CPP wrapper differs')
            (work/c['wrapper']).write_text(f'#include "{c["source"]}"\n')
        for c in shared['cdg_draw']['carriers']:
            if sha((work/c['wrapper']).read_bytes())!=c['original_wrapper_sha256']:raise ValueError('input/timing preceding drawing wrapper differs')
            (work/c['wrapper']).write_bytes(('include '+c['source']+'\r\n').encode())
        for c in shared['math']['carriers']:
            original=(work/c.get('original_wrapper',c['wrapper'])).read_bytes()
            if c.get('original_wrapper',c['wrapper']).endswith('.asm'):original=original.replace(b'\r\n',b'\n')
            if sha(original)!=c['original_wrapper_sha256']:raise ValueError('input/timing preceding ASM producer differs')
            (work/c['wrapper']).write_bytes(('include '+c['source']+'\r\n').encode())
        tup=work/'Tupfile.lua';original=tup.read_bytes()
        if sha(original)!=shared['math']['original_tup_sha256']:raise ValueError('input/timing original frozen link graph differs')
        text=original.decode();marker='th03:branch(MODEL_LARGE, { cflags = "-DBINARY=\'L\'" }):link("mainl", {'
        start=text.index(marker);end=text.index('\n})',start)+3;block=text[start:end]
        if block.count('"th03/vector.cpp"')!=1:raise ValueError('input/timing preceding MAINL vector position differs')
        tup.write_text(text[:start]+block.replace('"th03/vector.cpp"','"th03/vector_far.asm"')+text[end:])
        if sha(tup.read_bytes())!=previous['rounds'][0]['link_graph']['sha256']:raise ValueError('input/timing changed preceding link graph')
        command=['wine','cmd','/d','/c',r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%' r'&&set PROCESSOR_ARCHITECTURE=AMD64&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat']
        build=execute(command,work,env,logs/'cold-build.log')
        log=(logs/'cold-build.log').read_text()
        for c in cfg['carriers']:
            binary='L' if c['artifacts']==['mainl'] else 'O'
            game=c['physical_game_macro'];directory=Path(c['object']).parent
            if f"-DGAME={game} -ml -DBINARY='{binary}' -n{directory}/ {c['wrapper']}" not in log:raise ValueError('input original compiler association differs')
        objects={p.relative_to(work).as_posix():sha(normalize_dependency_timestamps(p.read_bytes())) for p in sorted((work/'obj').rglob('*.obj'))};game={p:h for p,h in objects.items() if any(p.startswith(f'obj/th0{n}/') for n in range(1,6))};products={}
        for item in load_target_manifest(ROOT/'config/targets.toml')['artifacts']:
            p=Path('bin')/item['game']/Path(item['private_path']).name;products[p.as_posix()]=sha((work/p).read_bytes())
        if products!=previous['rounds'][0]['products'] or len(products)!=20 or len(game)!=351 or len(objects)!=417:raise ValueError('input/timing complete product/object vector differs')
        owned={c['object'] for c in cfg['carriers']}
        if {p:h for p,h in game.items() if p not in owned}!={p:h for p,h in previous['rounds'][0]['game_objects'].items() if p not in owned}:raise ValueError('input/timing changed another original game object')
        nongame={p:dict(previous=previous['rounds'][0]['all_objects'][p],current=h) for p,h in objects.items() if p not in game and h!=previous['rounds'][0]['all_objects'][p]};producers={}
        for c in cfg['carriers']:
            raw=(work/c['object']).read_bytes();obj=describe_omf(raw);old=ROOT/Path(PARENT).parent/f'round{number}/source'/c['object'];inputs[str(old.relative_to(ROOT))]=sha(old.read_bytes())
            if not obj['valid'] or obj['translator_comments']!=['TC86 Borland C++ 4.02'] or producer_records(raw)!=producer_records(old.read_bytes()):raise ValueError('input/timing complete original nondependency OMF differs')
            segs=[r.data.hex() for r in parse_omf(raw) if r.name=='SEGDEF']
            if segs!=c['segments']:raise ValueError('input/timing original complete CODE/DATA0/BSS0 layout differs')
            producers[c['object']]=dict(normalized_sha256=obj['dependency_timestamp_normalized_sha256'],translator_comments=obj['translator_comments'],records=producer_records(raw),segments=segs,original_nondependency_records_equal=True,physical_game_macro=c['physical_game_macro'])
        observations={}
        for art,p in PROFILES.items():
            candidate=parse_mz((work/f'bin/th03/{art}.exe').read_bytes());meta=analyze(candidate.program_image,p);mp=work/f'obj/th03/{art}.map';map_text=mp.read_text();maprows=code_rows(map_text,len(candidate.program_image));comparisons={}
            for c in cfg['carriers']:
                if art not in c['artifacts']:continue
                row=next(r for r in maprows if r['module']==c['wrapper'] and r['size'])
                if (row['segment'],row['offset'],row['size'])!=(c[art+'_segment'],c[art+'_offset'],c['size']):raise ValueError('input/timing complete source MAP ownership differs')
                comp=extent_observation(targets[art],candidate,row)
                if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:raise ValueError('input/timing complete original raw/ordered carrier differs')
                comparisons[c['wrapper']]=comp
            entries={n:a for n,a,_,_ in p['ranges']}
            names={'sense':'input_reset_sense_key_held','interface':'input_mode_interface','key_key':'input_mode_key_vs_key','joy_key':'input_mode_joy_vs_key','key_joy':'input_mode_key_vs_joy','one_cpu':'input_mode_1p_vs_cpu','cpu_one':'input_mode_cpu_vs_1p','cpu_cpu':'input_mode_cpu_vs_cpu','attract':'input_mode_attract','change':'input_wait_for_change','measure_wait':'input_wait_for_ok_or_measure','ok_wait':'input_wait_for_ok','frame_delay':'frame_delay','frame_delay_2':'frame_delay_2'}
            bindings=[(names[key],p['cs'],at,True) for key,at in entries.items()]
            bindings += [(public,p['ds'],p[key],False) for key,public in [('p1','_input_mp_p1'),('p2','_input_mp_p2'),('sp','_input_sp'),('joy','_js_stat'),('present','_js_bexist'),('clock','_vsync_Count1'),('sound','_snd_active'),('midi','_snd_midi_active')]]
            for public,seg,start,cpp in bindings:
                label=re.escape(public)+(r'\(.*\)' if cpp else '')
                coords={(int(a,16),int(b,16)) for a,b in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+label+r'\s*$',map_text,re.M)}
                if coords!={(seg,start)}:raise ValueError('input original public binding differs: '+public)
            cpu=matrix(candidate,p)
            if semantic(cpu)!=semantic(matrix(targets[art],p)):raise ValueError('input/timing maintained scalar contracts differ')
            changes=[dict(decoded_linear=i,target=x,candidate=y) for i,(x,y) in enumerate(zip(targets[art].program_image,candidate.program_image)) if x!=y]
            if len(candidate.program_image)!=len(targets[art].program_image) or len(changes)!=(6 if art=='op' else 21):raise ValueError('input/timing known whole decoded inequality differs')
            observations[art]=dict(comparisons=comparisons,cpu=cpu,coverage=coverage(meta,cpu),map_sha256=sha(mp.read_bytes()),whole_decoded=dict(equal=False,changes=changes,original_ordered_relocations_equal=targets[art].relocations==candidate.relocations))
        rounds.append(dict(number=number,build=build,all_objects=objects,game_objects=game,products=products,nongame_object_changes=nongame,producers=producers,link_graph=dict(sha256=sha(tup.read_bytes()),unchanged_from_parent=True),observations=observations));print('PASS maintained input/timing cold round',number,flush=True)
    if rounds[0]['products']!=rounds[1]['products'] or rounds[0]['game_objects']!=rounds[1]['game_objects']:raise ValueError('input/timing cold determinism differs')
    for p,h in inputs.items():
        if sha((ROOT/p).read_bytes())!=h:raise ValueError('input/timing source input changed: '+p)
    if sha(archive.read_bytes())!=archive_sha or any(sha((snapshot/p).read_bytes())!=inputs[p] for p in source_files):raise ValueError('input/timing frozen archive/source snapshot changed')
    if any(read_verified_artifact(ROOT,a)!=stored[art] for art,a in artifacts.items()):raise ValueError('input/timing canonical target changed')
    report=dict(kind='th03-shared-input-maintained-cold-probes',observed_utc=datetime.now(timezone.utc).isoformat(),inputs=inputs,reference_archive_sha256=archive_sha,toolchain_receipt_sha256=attestation,rounds=rounds,diagnostic_checks_pass=True,source_acceptance=False,exact_acceptance=False,notes='Complete four natural CPP carriers535 independently bound: OP modes367 plus both frame helpers42; MAINL modes367 plus confirmation/measure waits126 plus frame helper21. Original GAME2/GAME3 large TC86 nondependency producer records/CODE/DATA0/BSS0/publics/full raw/original ordered relocations match. Both20product351gameobject vectors deterministic; all417OMF recorded,347othergameobjects unchanged,20products equal parent PI. Research nongame differences separate. All native keyboard/context417 and owned mode/wait/helper positions checked with explicit BIOS/joystick/interrupt/IRQ models, full physical memory outside caller stack, complete DGROUP scalar results, ordered source/target stores and events, terminal ABI/IFDF. Prefixes do not claim completion. Keyboard context/carrier418/trailing NOP is unowned; MAIN owners/manifests unchanged. Header/DGROUP ownership, native joystick/driver/IRQ/hardware clocks, full waits/canonical packing/complete Oracles/exact open.')
    (output/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS source-present shared input/timing cold probes; exact open')


if __name__=='__main__':main()
