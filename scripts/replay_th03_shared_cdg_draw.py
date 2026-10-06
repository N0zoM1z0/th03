#!/usr/bin/env python3
"""Cold compile two shared CDG ASM carriers with all preceding source owners."""
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

from lib.omf import describe_omf, normalize_dependency_timestamps, parse_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from replay_th03_main_exact_units import execute
from replay_th03_shared_cdg_load import apply_previous
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import sha
from review_th03_shared_cdg_draw import PROFILES, FUNCTIONS, PARENT, analyze, observe, coverage

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'config/th03_shared_cdg_draw_candidate.toml'
PROOF = '.analysis/sol-shared-cdg-draw-review-20261006.json'
PROOF_SHA = '42623621ef9fee6f4b69cc0cbeabd9c16b7678759963b05fd110bf542ed57ee6'
PUBLICS = ['CDG_PUT_8', 'CDG_PUT_HFLIP_8', 'CDG_PUT_NOALPHA_8']


def semantic(rows):
    """Ignore only whole-image digests; keep every nested semantic observation."""
    return json.loads(json.dumps(rows), object_hook=lambda d: {k: v for k, v in d.items() if k not in ('memory_before_sha256', 'memory_after_sha256')})


def producer_records(raw):
    records = parse_omf(normalize_dependency_timestamps(raw))
    return [(r.name, r.data.hex()) for r in records if not (r.name == 'COMENT' and len(r.data) > 6 and r.data[1] in (0xe8, 0xe9))]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', args.run_id):
        raise ValueError('invalid run id')
    output = ROOT/'.analysis/th03-shared-cdg-draw'/args.run_id
    output.mkdir(parents=True, exist_ok=False)
    raw = (ROOT/PROOF).read_bytes()
    if sha(raw) != PROOF_SHA:
        raise ValueError('CDG draw diagnostic proof differs')
    proof = json.loads(raw)
    if not proof['diagnostic_checks_pass'] or proof['exact_acceptance']:
        raise ValueError('CDG draw diagnostic scope differs')
    inputs = dict(proof['inputs'])
    inputs[PROOF] = sha(raw)
    for p, h in inputs.items():
        if sha((ROOT/p).read_bytes()) != h:
            raise ValueError('CDG draw prerequisite differs: '+p)
    cfg = tomllib.loads((ROOT/MANIFEST).read_text())
    load_path = 'config/th03_shared_cdg_load_candidate.toml'
    load = tomllib.loads((ROOT/load_path).read_text())
    inputs[load_path] = sha((ROOT/load_path).read_bytes())
    manifests = {}
    source_files = {load['source'], *load['support_files'], *cfg['support_files'], *[c['source'] for c in cfg['carriers']]}
    for name in ('score', 'title', 'entry', 'menu', 'music', 'select'):
        p = f'config/th03_op_{name}_candidate.toml'
        c = manifests[name] = tomllib.loads((ROOT/p).read_text())
        inputs[p] = sha((ROOT/p).read_bytes())
        source_files.update(c.get('support_files', []))
        if 'source' in c:
            source_files.add(c['source'])
        for unit in c.get('units', []):
            source_files.add(unit['source'])
    source_files = sorted(source_files)
    for p in [MANIFEST, 'scripts/replay_th03_shared_cdg_draw.py', 'tests/test_shared_cdg_draw_review.py',
              '.analysis/sol-shared-cdg-draw-controls-20261006.log', *source_files]:
        inputs[p] = sha((ROOT/p).read_bytes())
    snapshot = output/'repository-inputs'
    for p, h in inputs.items():
        if not p.startswith('.analysis/'):
            dest = snapshot/p
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT/p, dest)
            if sha(dest.read_bytes()) != h:
                raise ValueError('CDG draw snapshot changed')
    artifacts = {a: find_artifact(load_target_manifest(ROOT/'config/targets.toml'), 'th03-'+a) for a in PROFILES}
    stored = {a: read_verified_artifact(ROOT, x) for a, x in artifacts.items()}
    targets = {a: parse_mz((ROOT/proof['observations'][a][0]['path']).read_bytes()) for a in PROFILES}
    subprocess.run([sys.executable, 'scripts/attest_toolchain.py'], cwd=ROOT, check=True)
    tool = tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    attestation = sha((ROOT/'.analysis/toolchain/attestation.json').read_bytes())
    env = os.environ.copy()
    env.update(DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(ROOT/tool['paths']['wine_prefix']), MSDOS_PATH=r'C:\TC4\BIN')
    archive = output/'reference.tar'
    subprocess.run(['git', 'archive', '--format=tar', f'--output={archive}', cfg['reference_revision']], cwd=ROOT/'_reference/ReC98', check=True)
    archive_sha = sha(archive.read_bytes())
    previous = json.loads((ROOT/PARENT).read_bytes())
    rounds = []
    for number in (1, 2):
        logs, work = output/f'round{number}', output/f'round{number}/source'
        work.mkdir(parents=True)
        subprocess.run(['tar', '-xf', str(archive), '-C', str(work)], check=True)
        if list(work.rglob('*.obj')) or list((work/'bin').glob('th0[1-5]/*.exe')):
            raise ValueError('CDG draw archive is not cold')
        for p in source_files:
            dest = work/p
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(snapshot/p, dest)
            if Path(p).suffix in ('.asm', '.inc'):
                dest.write_bytes(dest.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))
        apply_previous(work, manifests)
        wrapper, carrier = work/load['wrapper'], work/load['carrier']
        if sha(wrapper.read_bytes()) != load['original_wrapper_sha256'] or sha(carrier.read_bytes()) != load['original_carrier_sha256']:
            raise ValueError('previous shared CDG loader frozen carrier differs')
        wrapper.write_text(f'#include "{load["source"]}"\n')
        for c in cfg['carriers']:
            wrapper = work/c['wrapper']
            if sha(wrapper.read_bytes()) != c['original_wrapper_sha256'] or 'carrier' in c and sha((work/c['carrier']).read_bytes()) != c['original_carrier_sha256']:
                raise ValueError('CDG draw original frozen wrapper/carrier differs')
            wrapper.write_bytes(('include '+c['source']+'\r\n').encode())
        command = ['wine', 'cmd', '/d', '/c', r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%' r'&&set PROCESSOR_ARCHITECTURE=AMD64&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat']
        build = execute(command, work, env, logs/'cold-build.log')
        all_objects = {p.relative_to(work).as_posix(): sha(normalize_dependency_timestamps(p.read_bytes())) for p in sorted((work/'obj').rglob('*.obj'))}
        game_objects = {p: h for p, h in all_objects.items() if any(p.startswith(f'obj/th0{n}/') for n in range(1, 6))}
        products = {}
        for item in load_target_manifest(ROOT/'config/targets.toml')['artifacts']:
            p = Path('bin')/item['game']/Path(item['private_path']).name
            products[p.as_posix()] = sha((work/p).read_bytes())
        if products != previous['rounds'][0]['products'] or len(products) != 20 or len(game_objects) != 350 or len(all_objects) != 416:
            raise ValueError('CDG draw preceding complete product vector differs')
        owned = {c['object'] for c in cfg['carriers']}
        if {p: h for p, h in game_objects.items() if p not in owned} != {p: h for p, h in previous['rounds'][0]['game_objects'].items() if p not in owned}:
            raise ValueError('CDG draw changed another physical game object')
        nongame_changes = {p: dict(previous=previous['rounds'][0]['all_objects'][p], current=h) for p, h in all_objects.items() if p not in game_objects and h != previous['rounds'][0]['all_objects'][p]}
        objects = {}
        for c in cfg['carriers']:
            raw = (work/c['object']).read_bytes()
            obj = describe_omf(raw)
            if not obj['valid'] or obj['translator_comments'] != ['Turbo Assembler  Version 5.0']:
                raise ValueError('CDG draw original assembler producer differs')
            old = ROOT/Path(proof['observations']['op'][number]['path']).parents[2]/c['object']
            inputs[str(old.relative_to(ROOT))] = sha(old.read_bytes())
            if producer_records(raw) != producer_records(old.read_bytes()):
                raise ValueError('CDG draw original nondependency OMF records differ')
            segdefs = [r.data.hex() for r in parse_omf(raw) if r.name == 'SEGDEF']
            expected = ['480000020301', '480000040501', '487e01060701'] if c['size'] == 382 else ['487200020301']
            if segdefs != expected:
                raise ValueError('CDG draw physical CODE/DATA ownership differs')
            objects[c['object']] = dict(normalized_sha256=obj['dependency_timestamp_normalized_sha256'], segments=segdefs,
                                        nondependency_producer_records_equal=True, producer_records=producer_records(raw))
        observations = {}
        for art, profile in PROFILES.items():
            candidate = parse_mz((work/f'bin/th03/{art}.exe').read_bytes())
            meta = analyze(candidate.program_image, profile)
            mp = work/f'obj/th03/{art}.map'
            map_text = mp.read_text()
            carriers = code_rows(map_text, len(candidate.program_image))
            comparisons = {}
            for c in cfg['carriers']:
                row = next(r for r in carriers if r['module'] == c['wrapper'] and r['size'])
                if (row['segment'], row['offset'], row['size']) != (c[art+'_segment'], c[art+'_offset'], c['size']):
                    raise ValueError('CDG draw original MAP ownership differs')
                comp = extent_observation(targets[art], candidate, row)
                if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:
                    raise ValueError('CDG draw complete original raw/ordered carrier rows differ')
                comparisons[c['wrapper']] = comp
            for start, public in zip(profile['starts'], PUBLICS):
                coords = {(int(s, 16), int(o, 16)) for s, o in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+public+r'\s*$', map_text, re.M)}
                if coords != {(profile['cs'], start)}:
                    raise ValueError('CDG draw original public entry differs')
            baseline = proof['observations'][art][0]['cpu']
            indices = [i for i, r in enumerate(baseline) if not r['scenario']['if'] and not r['scenario']['df'] or r['scenario']['lookup'] != 'reverse' or r['scenario']['alpha'] != 0x5000 or r['scenario']['colors'] != 0x7000 or not r['scenario']['width']]
            cpu = []
            for i in indices:
                r, s = baseline[i], baseline[i]['scenario']
                cpu.append(observe(candidate, profile, r['function'], s,
                                   sequence=[(r['function'], s)] if not s['width'] else None,
                                   prefix=not s['width'] and r['function'] != 'noalpha'))
            if semantic(cpu) != semantic([baseline[i] for i in indices]):
                raise ValueError('CDG draw maintained source scalar contracts differ')
            changes = [dict(decoded_linear=i, target=x, candidate=y) for i, (x, y) in enumerate(zip(targets[art].program_image, candidate.program_image)) if x != y]
            if len(candidate.program_image) != len(targets[art].program_image) or len(changes) != (6 if art == 'op' else 21):
                raise ValueError('CDG draw known whole decoded inequality differs')
            observations[art] = dict(comparisons=comparisons, cpu=cpu, case_indices=indices,
                                     coverage=coverage(meta, cpu), map_sha256=sha(mp.read_bytes()),
                                     whole_decoded=dict(equal=False, changes=changes, original_ordered_relocations_equal=targets[art].relocations == candidate.relocations))
        rounds.append(dict(number=number, build=build, all_objects=all_objects, game_objects=game_objects, products=products,
                           objects=objects, nongame_object_changes=nongame_changes, observations=observations))
        print('PASS maintained shared CDG draw cold round', number, flush=True)
    if rounds[0]['products'] != rounds[1]['products'] or rounds[0]['game_objects'] != rounds[1]['game_objects']:
        raise ValueError('CDG draw cold determinism differs')
    for p, h in inputs.items():
        if sha((ROOT/p).read_bytes()) != h:
            raise ValueError('CDG draw source input changed: '+p)
    if sha(archive.read_bytes()) != archive_sha or any(sha((snapshot/p).read_bytes()) != inputs[p] for p in source_files):
        raise ValueError('CDG draw frozen archive/source snapshot changed')
    for art, artifact in artifacts.items():
        if read_verified_artifact(ROOT, artifact) != stored[art]:
            raise ValueError('CDG draw canonical target changed')
    report = dict(kind='th03-shared-cdg-drawing-maintained-cold-probes', observed_utc=datetime.now(timezone.utc).isoformat(), inputs=inputs,
                  reference_archive_sha256=archive_sha, toolchain_receipt_sha256=attestation, rounds=rounds,
                  tools=dict(capstone=version('capstone'), unicorn=version('unicorn')), diagnostic_checks_pass=True,
                  source_acceptance=False, exact_acceptance=False,
                  notes='Two full shared ASM carriers496bytes/493body/3naturalEVEN; independent OP/MAINL bindings through three explicit compatibility imports. Two fresh20product350gameobject vectors deterministic/all416OMF recorded. All20products equal preceding sharedload;348othergameobjects unchanged. Complete original-order nondependency OMF records/segment layout match preceding producers. Perartifact/round focused source cases cover all200positions and original carrierbytes/orderedrelocations/MAP publics/SMC/flatstores/ports/wholephysical memory/frames/IFDF/ESFS including zero-width prefixes. Nine Research benchmark differences retained without416objectdeterminism claim. Forwarded declarations/globalDATA/BSS/LUT/GRCG/bankeddevices/assets/IRQ reentrancy/CRT/canonicalpacking/completeproduct/exact remain open; MAIN exact aggregate stays separate.')
    (output/'receipt.json').write_text(json.dumps(report, indent=2)+'\n')
    print('PASS source-present shared CDG drawing cold probes; exact open')


if __name__ == '__main__':
    main()
