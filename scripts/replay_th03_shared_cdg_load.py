#!/usr/bin/env python3
"""Cold replay the shared CDG TU with every preceding OP source overlay."""
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
from review_th03_shared_cdg_load import PROFILES, FUNCTIONS, PARENT, analyze, observe, coverage

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'config/th03_shared_cdg_load_candidate.toml'
PROOF = '.analysis/sol-shared-cdg-load-review-20261006.json'
PROOF_SHA = 'b75857090b1a86d8ceb80a558247609b3bc6a99f2293f905b5df760393de6c9a'
PUBLICS = ['CDG_LOAD_SINGLE', 'CDG_LOAD_SINGLE_NOALPHA', 'CDG_LOAD_ALL', 'CDG_LOAD_ALL_NOALPHA', 'CDG_FREE']


def apply_previous(work, manifests):
    """Preserve the accepted bounded overlays and unowned frozen prefixes."""
    score, title, entry, menu, music, select = (manifests[n] for n in ('score', 'title', 'entry', 'menu', 'music', 'select'))
    for unit in score['units']:
        if 'wrapper' in unit:
            (work/unit['wrapper']).write_text(f'#include "{unit["source"]}"\n')
        else:
            carrier = work/unit['carrier']
            text = carrier.read_text()
            if text.count(unit['anchor']) != 1:
                raise ValueError('previous score include anchor differs')
            carrier.write_text(text.replace(unit['anchor'], f'#include "{unit["source"]}"', 1))
    carrier = work/title['carrier']
    text = carrier.read_text()
    split = text.index(title['anchor'])
    if text.count(title['anchor']) != 1 or sha(text[:split].encode()) != title['prefix_sha256']:
        raise ValueError('previous title prefix differs')
    carrier.write_text(f'#include "{title["source"]}"\n\n'+text[split:])
    wrapper = work/entry['wrapper']
    if sha(wrapper.read_bytes()) != entry['original_source_sha256']:
        raise ValueError('previous entry frozen source differs')
    wrapper.write_text(f'#include "{entry["source"]}"\n')
    wrapper, carrier = work/music['wrapper'], work/music['carrier']
    if sha(wrapper.read_bytes()) != music['original_wrapper_sha256'] or sha(carrier.read_bytes()) != music['original_carrier_sha256']:
        raise ValueError('previous Music frozen carrier differs')
    text = carrier.read_text()
    a, b = text.index(music['unowned_anchor']), text.index(music['unowned_end_anchor'])
    if text.count(music['unowned_anchor']) != 1 or text.count(music['unowned_end_anchor']) != 1:
        raise ValueError('previous Music unowned copy anchors differ')
    wrapper.write_text(f'#include "{music["units"][0]["source"]}"\n\n'+text[a:b]+f'#include "{music["units"][1]["source"]}"\n')
    wrapper, carrier = work/select['wrapper'], work/select['carrier']
    if sha(wrapper.read_bytes()) != select['original_wrapper_sha256']:
        raise ValueError('previous selection frozen wrapper differs')
    original = subprocess.check_output(['git', 'show', select['reference_revision']+':'+select['carrier']], cwd=ROOT/'_reference/ReC98')
    if sha(original) != select['original_carrier_sha256'] or carrier.read_bytes() != original.replace(b'#include "th03/formats/score_ld.cpp"', b'#include "src/op/formats/score_load.inl"'):
        raise ValueError('previous selection loader overlay differs')
    text = carrier.read_text()
    split = text.index(select['anchor'])
    if text.count(select['anchor']) != 1 or sha(original.split(select['anchor'].encode())[0]) != select['prefix_sha256']:
        raise ValueError('previous selection unowned DATA/BSS prefix differs')
    prefix = text[:split]
    for forwarding in select['support_files']:
        original_include = forwarding.removeprefix('compat/rec98/')
        prefix = prefix.replace(f'#include "{original_include}"', f'#include "{forwarding}"')
    carrier.write_text(prefix+f'#include "{select["source"]}"\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', args.run_id):
        raise ValueError('invalid run id')
    output = ROOT/'.analysis/th03-shared-cdg-load'/args.run_id
    output.mkdir(parents=True, exist_ok=False)
    raw = (ROOT/PROOF).read_bytes()
    if sha(raw) != PROOF_SHA:
        raise ValueError('shared CDG diagnostic proof differs')
    proof = json.loads(raw)
    if not proof['diagnostic_checks_pass'] or proof['exact_acceptance']:
        raise ValueError('shared CDG diagnostic acceptance state differs')
    inputs = dict(proof['inputs'])
    inputs[PROOF] = sha(raw)
    for p, h in inputs.items():
        if sha((ROOT/p).read_bytes()) != h:
            raise ValueError('shared CDG prerequisite differs: '+p)
    cfg = tomllib.loads((ROOT/MANIFEST).read_text())
    manifests, source_files = {}, {cfg['source'], *cfg['support_files']}
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
    for p in [MANIFEST, 'scripts/replay_th03_shared_cdg_load.py',
              'tests/test_shared_cdg_load_review.py', '.analysis/sol-shared-cdg-load-controls-20261006.log', *source_files]:
        inputs[p] = sha((ROOT/p).read_bytes())
    snapshot = output/'repository-inputs'
    for p, h in inputs.items():
        if not p.startswith('.analysis/'):
            dest = snapshot/p
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT/p, dest)
            if sha(dest.read_bytes()) != h:
                raise ValueError('shared CDG snapshot changed')
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
        logs = output/f'round{number}'
        work = logs/'source'
        work.mkdir(parents=True)
        subprocess.run(['tar', '-xf', str(archive), '-C', str(work)], check=True)
        if list(work.rglob('*.obj')) or list((work/'bin').glob('th0[1-5]/*.exe')):
            raise ValueError('shared CDG archive is not cold')
        for p in source_files:
            dest = work/p
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(snapshot/p, dest)
        apply_previous(work, manifests)
        wrapper, carrier = work/cfg['wrapper'], work/cfg['carrier']
        if sha(wrapper.read_bytes()) != cfg['original_wrapper_sha256'] or sha(carrier.read_bytes()) != cfg['original_carrier_sha256']:
            raise ValueError('shared CDG original frozen carrier differs')
        wrapper.write_text(f'#include "{cfg["source"]}"\n')
        command = ['wine', 'cmd', '/d', '/c', r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%' r'&&set PROCESSOR_ARCHITECTURE=AMD64&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat']
        result = execute(command, work, env, logs/'cold-build.log')
        obj = describe_omf((work/cfg['object']).read_bytes())
        if not obj['valid'] or 'TC86 Borland C++ 4.02' not in obj['translator_comments']:
            raise ValueError('shared CDG producer differs')
        all_objects = {p.relative_to(work).as_posix(): sha(normalize_dependency_timestamps(p.read_bytes())) for p in sorted((work/'obj').rglob('*.obj'))}
        game_objects = {p: h for p, h in all_objects.items() if any(p.startswith(f'obj/th0{n}/') for n in range(1, 6))}
        products = {}
        for item in load_target_manifest(ROOT/'config/targets.toml')['artifacts']:
            p = Path('bin')/item['game']/Path(item['private_path']).name
            products[p.as_posix()] = sha((work/p).read_bytes())
        if products != previous['rounds'][0]['products'] or len(products) != 20 or len(game_objects) != 350 or len(all_objects) != 416:
            raise ValueError('shared CDG preceding complete product vector differs')
        untouched = {p: h for p, h in game_objects.items() if p != cfg['object']}
        if untouched != {p: h for p, h in previous['rounds'][0]['game_objects'].items() if p != cfg['object']}:
            raise ValueError('shared CDG changed another physical game object')
        # Research benchmark DATA embeds __TIME__. Preserve its differences;
        # it is outside the20product/350game-object vector, not normalized away.
        nongame_changes = {p: dict(previous=previous['rounds'][0]['all_objects'][p], current=h)
                           for p, h in all_objects.items() if p not in game_objects and h != previous['rounds'][0]['all_objects'][p]}
        observations = {}
        for art, profile in PROFILES.items():
            candidate = parse_mz((work/f'bin/th03/{art}.exe').read_bytes())
            meta = analyze(candidate.program_image, profile)
            mp = work/f'obj/th03/{art}.map'
            map_text = mp.read_text()
            owner = next(r for r in code_rows(map_text, len(candidate.program_image)) if r['module'] == cfg['wrapper'] and r['size'])
            if (owner['segment'], owner['offset'], owner['size']) != (profile['cs'], profile['start'], 593):
                raise ValueError('shared CDG original MAP ownership differs')
            comparisons = {}
            for (n, a, z, _), public in zip(FUNCTIONS, PUBLICS):
                off = profile['start']+a
                coords = {(int(s, 16), int(o, 16)) for s, o in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?'+public+r'\s*$', map_text, re.M)}
                if coords != {(profile['cs'], off)}:
                    raise ValueError('shared CDG original public entry differs: '+public)
                comparisons[n] = extent_observation(targets[art], candidate, dict(segment=profile['cs'], offset=off, start=profile['cs']*16+off, size=z))
            carrier_comparison = extent_observation(targets[art], candidate, owner)
            if any(not r['raw_slice_equal'] or not r['ordered_relocations_equal'] for r in [*comparisons.values(), carrier_comparison]):
                raise ValueError('shared CDG original raw/ordered comparison differs')
            baseline = proof['observations'][art][0]['cpu']
            indices = [i for i, r in enumerate(baseline) if not r['scenario']['if'] and not r['scenario']['df']]
            cpu = [observe(candidate, profile, baseline[i]['function'], baseline[i]['scenario']) for i in indices]
            if normalized_contracts(cpu) != normalized_contracts([baseline[i] for i in indices]):
                raise ValueError('shared CDG maintained source scalar contracts differ')
            changes = [dict(decoded_linear=i, target=x, candidate=y) for i, (x, y) in enumerate(zip(targets[art].program_image, candidate.program_image)) if x != y]
            if len(candidate.program_image) != len(targets[art].program_image) or art == 'op' and len(changes) != 6:
                raise ValueError('shared CDG known whole decoded failure differs')
            observations[art] = dict(comparisons=comparisons, carrier=carrier_comparison, cpu=cpu, case_indices=indices,
                                     coverage=coverage(meta, cpu), map_sha256=sha(mp.read_bytes()),
                                     whole_decoded=dict(equal=not changes, changes=changes, original_ordered_relocations_equal=targets[art].relocations == candidate.relocations))
        rounds.append(dict(number=number, build=result, all_objects=all_objects, game_objects=game_objects, products=products, nongame_object_changes=nongame_changes,
                           object=dict(path=cfg['object'], normalized_sha256=obj['dependency_timestamp_normalized_sha256'], translator_comments=obj['translator_comments']), observations=observations))
        print('PASS shared CDG maintained cold round', number, flush=True)
    if rounds[0]['products'] != rounds[1]['products'] or rounds[0]['game_objects'] != rounds[1]['game_objects']:
        raise ValueError('shared CDG cold determinism differs')
    for p, h in inputs.items():
        if sha((ROOT/p).read_bytes()) != h:
            raise ValueError('shared CDG source input changed: '+p)
    if sha(archive.read_bytes()) != archive_sha:
        raise ValueError('shared CDG frozen archive changed')
    for p in source_files:
        if sha((snapshot/p).read_bytes()) != inputs[p]:
            raise ValueError('shared CDG snapshot source changed')
    for art, artifact in artifacts.items():
        if read_verified_artifact(ROOT, artifact) != stored[art]:
            raise ValueError('shared CDG canonical target changed')
    report = dict(kind='th03-shared-cdg-loading-maintained-cold-probes', observed_utc=datetime.now(timezone.utc).isoformat(), inputs=inputs,
                  reference_archive_sha256=archive_sha, toolchain_receipt_sha256=attestation, rounds=rounds,
                  tools=dict(capstone=version('capstone'), unicorn=version('unicorn')), diagnostic_checks_pass=True,
                  source_acceptance=False, exact_acceptance=False,
                  notes='One complete593-byte/5-function shared CPP TU through two explicit compatibility imports; independent OP/MAINL bindings. Two fresh20product350gameobject vectors deterministic/all416OMF recorded; all products identical to preceding selection and all349otherphysical game objects unchanged. Research benchmark object differences retained separately; no416-object determinism claim. Each artifact each round82cases/all219native positions, full1MiB preservation and complete ordered stores/file fixtures/frames rerun. External CDG declarations/global DATA/BSS/root/header/DOS/heap/resources/canonical packing/fullproduct/exact ownership remain open; MAIN exact aggregate is separate.')
    (output/'receipt.json').write_text(json.dumps(report, indent=2)+'\n')
    print('PASS source-present shared CDG loader cold probes; exact open')


if __name__ == '__main__':
    main()
