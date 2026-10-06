#!/usr/bin/env python3
"""Cold compiler probes for maintained OP score candidates, without exact credit."""
import argparse
from datetime import datetime, timezone
import json
from importlib.metadata import version
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
from review_th03_mainl_cutscene import sha, extent_observation
from review_th03_op_score import RANGES, matrix
from review_th03_decoded_code import code_rows

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'config/th03_op_score_candidate.toml'
PROOF = '.analysis/sol-op-score-review-20261006.json'
PROOF_SHA = 'b8d953fec1b3a993aa4f3cf5ee90d9b80884f5da4ebb547094466bcef3e42ec1'


def normalized_contracts(rows):
    """Compare receipt wire types while retaining every semantic observation."""
    values = [{k:v for k,v in row.items() if k not in ('memory_before_sha256', 'memory_after_sha256')}
              for row in rows]
    return json.loads(json.dumps(values))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-id', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', args.run_id):
        raise ValueError('invalid run id')
    output = ROOT / '.analysis/th03-op-score' / args.run_id
    output.mkdir(parents=True, exist_ok=False)
    cfg = tomllib.loads((ROOT / MANIFEST).read_text())
    proof = json.loads((ROOT / PROOF).read_bytes())
    if sha((ROOT / PROOF).read_bytes()) != PROOF_SHA:
        raise ValueError('score diagnostic receipt differs')
    if not proof['diagnostic_checks_pass'] or proof['exact_acceptance']:
        raise ValueError('score diagnostic prerequisite differs')
    inputs = {PROOF: sha((ROOT / PROOF).read_bytes())}
    names = [MANIFEST, 'config/targets.toml', 'config/toolchain.toml',
             'scripts/replay_th03_op_score.py', 'scripts/review_th03_op_score.py',
             'scripts/replay_th03_main_exact_units.py', 'scripts/lib/omf.py',
             'scripts/lib/pc98.py', 'scripts/lib/targets.py',
             'scripts/review_th03_mainl_cutscene.py', 'scripts/attest_toolchain.py',
             'tests/test_op_score_replay.py',
             *cfg['support_files'], *[u['source'] for u in cfg['units']]]
    for p,h in proof['inputs'].items():
        if p.startswith('scripts/') and p.endswith('.py'):
            if sha((ROOT / p).read_bytes()) != h:
                raise ValueError('score diagnostic script input differs: ' + p)
            names.append(p)
    snapshot = output / 'repository-inputs'
    for p in names:
        data = (ROOT / p).read_bytes()
        inputs[p] = sha(data)
        dest = snapshot / p
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    artifact = find_artifact(load_target_manifest(ROOT / 'config/targets.toml'), cfg['artifact'])
    stored = read_verified_artifact(ROOT, artifact)
    path = proof['observations'][0]['path']
    data = (ROOT / path).read_bytes()
    if sha(data) != proof['inputs'][path]:
        raise ValueError('decoded work image differs')
    inputs[path] = sha(data)
    target = parse_mz(data)
    if not target.valid:
        raise ValueError('invalid decoded work image')
    subprocess.run([sys.executable, 'scripts/attest_toolchain.py'], cwd=ROOT, check=True)
    tool = tomllib.loads((ROOT / 'config/toolchain.toml').read_text())
    attestation = sha((ROOT / '.analysis/toolchain/attestation.json').read_bytes())
    env = os.environ.copy()
    env.update(DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
               WINEPREFIX=str(ROOT / tool['paths']['wine_prefix']), MSDOS_PATH=r'C:\TC4\BIN')
    archive = output / 'reference.tar'
    subprocess.run(['git', 'archive', '--format=tar', f'--output={archive}', cfg['reference_revision']],
                   cwd=ROOT / '_reference/ReC98', check=True)
    rounds = []
    for number in (1, 2):
        logs = output / f'round{number}'
        work = logs / 'source'
        work.mkdir(parents=True)
        subprocess.run(['tar', '-xf', str(archive), '-C', str(work)], check=True)
        if list(work.rglob('*.obj')) or list((work / 'bin').glob('th0[1-5]/*.exe')):
            raise ValueError('cold archive contains game outputs')
        for p in cfg['support_files'] + [u['source'] for u in cfg['units']]:
            dest = work / p
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(snapshot / p, dest)
        for unit in cfg['units']:
            if 'wrapper' in unit:
                (work / unit['wrapper']).write_text(f'#include "{unit["source"]}"\n')
            else:
                carrier = work / unit['carrier']
                text = carrier.read_text()
                if text.count(unit['anchor']) != 1:
                    raise ValueError('bounded include carrier anchor differs')
                carrier.write_text(text.replace(unit['anchor'], f'#include "{unit["source"]}"', 1))
        command = ['wine', 'cmd', '/d', '/c',
                   r'set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%'
                   r'&&set PROCESSOR_ARCHITECTURE=AMD64'
                   r'&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat']
        result = execute(command, work, env, logs / 'cold-build.log')
        objects = {}
        for unit in cfg['units']:
            obj = describe_omf((work / unit['object']).read_bytes())
            if not obj['valid'] or 'TC86 Borland C++ 4.02' not in obj['translator_comments']:
                raise ValueError('maintained compiler producer differs')
            objects[unit['id']] = obj
        all_objects = {p.relative_to(work).as_posix(): sha(normalize_dependency_timestamps(p.read_bytes()))
                       for p in sorted((work / 'obj').rglob('*.obj'))}
        products = {}
        for item in load_target_manifest(ROOT / 'config/targets.toml')['artifacts']:
            p = Path('bin') / item['game'] / Path(item['private_path']).name
            products[p.as_posix()] = sha((work / p).read_bytes())
        game_objects = {p:h for p,h in all_objects.items()
                        if any(p.startswith(f'obj/th0{n}/') for n in range(1,6))}
        if len(all_objects) != 416 or len(products) != 20 or len(game_objects) != 350:
            raise ValueError('cold compiler scaffold output vector incomplete')
        candidate = parse_mz((work / 'bin/th03/op.exe').read_bytes())
        if not candidate.valid:
            raise ValueError('invalid compiler probe OP')
        comparisons = {}
        map_text = (work / 'obj/th03/op.map').read_text()
        carriers = code_rows(map_text, len(candidate.program_image))
        for name, seg, off, size, cleanup, owner in RANGES:
            if not any(c['module']==owner and c['segment']==seg and
                       c['offset']<=off and off+size<=c['offset']+c['size'] for c in carriers):
                raise ValueError('score cold MAP carrier differs: ' + name)
            comp = extent_observation(target, candidate, dict(segment=seg, offset=off, start=seg*16+off, size=size))
            if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:
                raise ValueError('maintained score raw/ordered relocation differs: ' + name)
            comparisons[name] = comp
        cpu = matrix(candidate)
        actual = normalized_contracts(cpu)
        expected = normalized_contracts(proof['observations'][0]['cpu'])
        if actual != expected:
            difference = next((dict(index=i, actual=a, expected=b)
                               for i,(a,b) in enumerate(zip(actual, expected)) if a!=b),
                              dict(actual_count=len(actual), expected_count=len(expected)))
            (logs / 'contract-failure.json').write_text(json.dumps(difference, indent=2) + '\n')
            raise ValueError('maintained score native contract differs')
        rounds.append(dict(number=number, build=result, objects=objects, all_objects=all_objects,
                           game_objects=game_objects, products=products, comparisons=comparisons, cpu=cpu,
                           map_sha256=sha(map_text.encode())))
        print('PASS maintained OP score cold round', number, flush=True)
    if rounds[0]['products'] != rounds[1]['products'] or rounds[0]['game_objects'] != rounds[1]['game_objects']:
        raise ValueError('fresh compiler scaffold determinism differs')
    for p,h in inputs.items():
        if sha((ROOT / p).read_bytes()) != h:
            raise ValueError('score compiler input changed: ' + p)
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError('canonical packed target changed')
    report = dict(kind='th03-op-maintained-score-cold-compiler-probes', observed_utc=datetime.now(timezone.utc).isoformat(),
                  inputs=inputs, reference_archive_sha256=sha(archive.read_bytes()),
                  toolchain_receipt_sha256=attestation, rounds=rounds, maintained_decoded_bytes=501,
                  tools=dict(capstone=version('capstone'), unicorn=version('unicorn')),
                  diagnostic_checks_pass=True, source_acceptance=False, exact_acceptance=False,
                  notes='Two maintained CPP TUs and one bounded include built in two fresh frozen reference scaffolds. Twenty products and350gameobjects are deterministic; all416objects recorded, Research date/time objects remain diagnostic. Four MAIN owner wrapper objects from the older aggregate are absent by design. The scaffold and its other products/dependencies remain candidate material. Native IRAND executes as reference context, not maintained source. Decoded byte and modeled runtime equality grant no canonical packed-storage or whole-product/source/exact acceptance.')
    (output / 'receipt.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS source-present score compiler probes; exact open')


if __name__ == '__main__':
    main()
