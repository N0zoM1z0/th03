#!/usr/bin/env python3
"""Pack the current source-runtime links and retained ZUN; compare all four targets."""
import argparse
import fcntl
import json
import os
import re
import subprocess
import tomllib

import build_th03_package_current as package
import build_th03_runtime_linked_current as linked

ROOT, DRIVE = package.ROOT, package.DRIVE
DRIVER = 'scripts/package_th03_runtime_current.py'
STAGE = 'af1410p'
FILES = {'main': 'main.exe', 'op': 'op.exe', 'mainl': 'mainl.exe', 'zun': 'zun.com'}
DIET_FILES = ('op.exe', 'mainl.exe', 'zun.com')
need, sha, pin = package.need, package.sha, package.pin


def context(stage, reviewed=None):
    need(re.fullmatch(r'af[0-9]+[a-z]', stage), 'DOS-safe final package stage')
    reviewed = linked.review() if reviewed is None else reviewed
    parent = ROOT / reviewed['report']
    diet = tomllib.loads((ROOT / 'config/th03_diet.toml').read_text())
    tool = ROOT / diet['tool']['path']
    need(pin(tool) == dict(bytes=diet['tool']['size'], sha256=diet['tool']['sha256']), 'pinned DIET executable')
    manifest = package.load_target_manifest(ROOT / 'config/targets.toml')
    targets = {filename: package.read_verified_artifact(ROOT, package.find_artifact(manifest, 'th03-' + name))
               for name, filename in FILES.items()}
    inputs = {p: sha((ROOT / p).read_bytes()) for p in
              (DRIVER, linked.DRIVER, package.DRIVER, 'config/th03_diet.toml', 'config/targets.toml',
               'scripts/shared_runtime.py', 'scripts/lib/main_mz_compact.py', 'scripts/lib/pc98.py',
               'scripts/lib/targets.py', str(parent.relative_to(ROOT)), diet['tool']['path'])}
    sources = {}
    for n in (1, 2):
        for name, filename in FILES.items():
            path = DRIVE / 'TH03ZUN/product/zun.com' if name == 'zun' else parent.parent / f'r{n}' / filename
            sources[f'r{n}/{filename}'] = path.read_bytes()
            inputs[str(path.relative_to(ROOT))] = sha(sources[f'r{n}/{filename}'])
    return DRIVE / 'TH03PKG' / stage, reviewed, inputs, sources, targets, tool


def commands(base, n):
    for filename in DIET_FILES:
        for operation, flags, folder in (('pack', '-B', 'packed'), ('restore', '-ra', 'restore')):
            yield f'r{n}-{filename}-{operation}', package.dos() + ['DIET.EXE', flags, filename], base / f'r{n}/{folder}'


def review(stage=STAGE, reviewed=None):
    base, reviewed, inputs, sources, targets, tool = context(stage, reviewed)
    proof = json.loads((base / 'runtime-package.json').read_bytes())
    need(proof['complete'] and proof['stage'] == stage and proof['inputs'] == inputs and
         proof['linked'] == reviewed, 'complete current source-runtime packing context')
    expected = [(label, argv, str(cwd), 1) for n in (1, 2) for label, argv, cwd in commands(base, n)]
    need([(p['label'], p['argv'], p['cwd'], p['returncode']) for p in proof['phases']] == expected,
         'actual twelve serialized native DIET operations')
    for phase in proof['phases']:
        raw = (base / (phase['label'] + '.log')).read_bytes()
        need(sha(raw) == phase['log_sha256'] and b'Success!' in raw, 'actual successful DIET log')
    names = {'packed/' + f for f in FILES.values()} | {'restore/' + f for f in DIET_FILES}
    need(len(proof['rounds']) == 2 and [r['round'] for r in proof['rounds']] == [1, 2], 'both fresh packing rounds')
    vectors = []
    for n, row in enumerate(proof['rounds'], 1):
        rd = base / f'r{n}'
        need(row['outputs'] == {name: pin(rd / name) for name in names}, 'all actual final output pins')
        for folder in ('packed', 'restore'):
            need((rd / folder / 'DIET.EXE').read_bytes() == tool.read_bytes(), 'actual staged DIET executable')
        vector = {name: (rd / name).read_bytes() for name in names}
        for filename, target in targets.items():
            need(vector['packed/' + filename] == target, 'complete canonical Japanese ' + filename)
        need(package.compact_mz(sources[f'r{n}/main.exe']) == vector['packed/main.exe'], 'current MAIN compact MZ')
        for filename in DIET_FILES:
            need(vector['restore/' + filename] == sources[f'r{n}/{filename}'], 'complete current-input DIET roundtrip: ' + filename)
        vectors.append(vector)
    need(vectors[0] == vectors[1], 'all seven final outputs repeat byte for byte')
    return dict(stage=stage, native_rounds=2, complete_four_file_package_equal=True,
                repeat_identical_outputs_per_round=7, source_startup_original_OBJ_equal=True,
                source_CL_contributors=reviewed['source_CL_contributors'],
                deferred_source_questions=['MAIN input_s link byte', 'ZUN sprite16 terminal nine bytes'],
                files={FILES[name]: len(targets[FILES[name]]) for name in FILES},
                report=str((base / 'runtime-package.json').relative_to(ROOT)))


def build(stage):
    base, reviewed, inputs, sources, _, tool = context(stage)
    need(not base.exists(), 'unused final package stage')
    proof = dict(complete=False, stage=stage, inputs=inputs, linked=reviewed, phases=[], rounds=[])
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', MSDOS_PATH=r'C:\TC4\BIN')
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for n in (1, 2):
            rd = base / f'r{n}'
            for folder in ('packed', 'restore'):
                (rd / folder).mkdir(parents=True)
                (rd / folder / 'DIET.EXE').write_bytes(tool.read_bytes())
            (rd / 'packed/main.exe').write_bytes(package.compact_mz(sources[f'r{n}/main.exe']))
            for label, argv, cwd in commands(base, n):
                filename = argv[-1]
                raw = sources[f'r{n}/{filename}'] if label.endswith('-pack') else (rd / 'packed' / filename).read_bytes()
                (cwd / filename).write_bytes(raw)
                q = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
                (base / (label + '.log')).write_bytes(q.stdout)
                proof['phases'].append(dict(label=label, argv=argv, cwd=str(cwd), returncode=q.returncode, log_sha256=sha(q.stdout)))
                need(q.returncode == 1 and b'Success!' in q.stdout, 'native DIET operation: ' + label)
            names = {'packed/' + f for f in FILES.values()} | {'restore/' + f for f in DIET_FILES}
            proof['rounds'].append(dict(round=n, outputs={name: pin(rd / name) for name in names}))
            print(f'Final package round {n}: current MAIN and three complete DIET roundtrips', flush=True)
        proof['complete'] = True
        (base / 'runtime-package.json').write_text(json.dumps(proof, indent=2) + '\n')
    return review(stage, reviewed)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage', default=STAGE); p.add_argument('--build', action='store_true')
    args = p.parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10: os.nice(10 - os.nice(0))
    print(json.dumps(build(args.stage) if args.build else review(args.stage), indent=2))


if __name__ == '__main__':
    main()
