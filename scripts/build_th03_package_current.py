#!/usr/bin/env python3
"""Relink current MAIN/OP/MAINL with source C0 and build the four-file package.

Unchanged game-object pairs and runtime libraries retain their independent
reviews. This verifies the complete artifacts; unresolved source ownership
and MAIN's deferred input carrier remain explicit.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib

from lib.main_mz_compact import compact_mz
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
DRIVE = ROOT / '.analysis/toolchain/wineprefix/drive_c'
DRIVER = 'scripts/build_th03_package_current.py'
STARTUP_CONFIG = 'config/th03_startup_after548.json'
STAGE = 'af1386p'
PRODUCTS = {'main': ('TH03WORK', 'af1373m'), 'op': ('TH03OP', 'af1377o'),
            'mainl': ('TH03ML', 'af1375s')}


def need(value, message):
    if not value:
        raise ValueError('current package: ' + message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path):
    raw = path.read_bytes()
    return dict(bytes=len(raw), sha256=sha(raw))


def windows(path):
    return 'C:\\' + str(path.relative_to(DRIVE)).replace('/', '\\')


def native():
    return [sys.executable, str(ROOT / 'scripts/shared_runtime.py'), 'wine', '--']


def dos():
    return native() + [str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']


def parents():
    import build_th03_main_linked_current as main
    import build_th03_op_linked_current as op
    import build_th03_mainl_sound_current as mainl
    from lib.decoded_zun_acceptance import verify, PUBLICATION
    print('Reviewing the unchanged current source/object pairs', flush=True)
    result = dict(main=main.review(PRODUCTS['main'][1]), op=op.review(PRODUCTS['op'][1]),
                  mainl=mainl.review(PRODUCTS['mainl'][1]))
    result['zun'] = verify(ROOT, json.loads((ROOT / PUBLICATION).read_bytes()))
    return result


def context(stage, reviewed=None):
    need(re.fullmatch(r'af[0-9]+[a-z]', stage), 'DOS-safe stage')
    base = DRIVE / 'TH03PKG' / stage
    config = json.loads((ROOT / STARTUP_CONFIG).read_bytes())
    declarations = [config['original'], *config['supplier_inputs'], *config['native_tools'].values()]
    for declaration in declarations:
        path = ROOT / declaration['path']
        need(sha(path.read_bytes()) == declaration['sha256'], 'pinned startup supplier/tool input')
        if 'bytes' in declaration:
            need(path.stat().st_size == declaration['bytes'], 'pinned supplier input size')
    reviewed = parents() if reviewed is None else reviewed
    inputs = {DRIVER: sha((ROOT / DRIVER).read_bytes()), STARTUP_CONFIG: sha((ROOT / STARTUP_CONFIG).read_bytes()),
              config['source']: sha((ROOT / config['source']).read_bytes())}
    for declaration in declarations:
        inputs[declaration['path']] = declaration['sha256']
    for name in ('config/targets.toml', 'config/th03_diet.toml', 'scripts/shared_runtime.py',
                 'scripts/lib/main_mz_compact.py', 'scripts/build_th03_runtime_after548_work.py'):
        inputs[name] = sha((ROOT / name).read_bytes())
    responses, maps = {}, {}
    for product, (tree, selected) in PRODUCTS.items():
        work = DRIVE / tree
        folder = work / 'probe' / selected
        for number in (1, 2):
            if product == 'main':
                response_path, mapping = folder / f'r{number}.@l', folder / f'r{number}.map'
            elif product == 'op':
                response_path, mapping = folder / 'op.@l', folder / f'r{number}.map'
            else:
                response_path, mapping = folder / f'r{number}/link.lnk', folder / f'r{number}/mainl.map'
            response = response_path.read_bytes()
            # All current responses explicitly bind the original startup slot.
            tokens = re.findall(rb'[^\s,+]+', response)
            startup = [t for t in tokens if t.lower().endswith(b'\\c0l.obj')]
            need(len(startup) == 1, 'one explicit large-model startup slot')
            response = response.replace(startup[0], windows(base / 'startup/c0l.obj').encode())
            for suffix in ('exe', 'map'):
                old, = [t for t in tokens if t.lower().endswith(('.' + suffix).encode())]
                response = response.replace(old, windows(base / f'r{number}/{product}.{suffix}').encode())
            key = f'r{number}/{product}.lnk'
            responses[key] = response
            maps[f'r{number}/{product}.map'] = mapping.read_bytes()
            inputs[str(response_path.relative_to(ROOT))] = sha(response_path.read_bytes())
            inputs[str(mapping.relative_to(ROOT))] = sha(mapping.read_bytes())
            for token in tokens:
                if not token.lower().endswith((b'.obj', b'.lib')):
                    continue
                text = token.decode().replace('\\', '/')
                need(':' not in text or text[:3].lower() == 'c:/', 'local compiler input')
                path = DRIVE / text[3:] if ':' in text else work / text
                if not path.exists() and path.parent == DRIVE / 'TC4/LIB':
                    path = path.with_name(path.name.upper())
                inputs[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    diet = tomllib.loads((ROOT / 'config/th03_diet.toml').read_text())
    tool = ROOT / diet['tool']['path']
    need(pin(tool) == dict(bytes=diet['tool']['size'], sha256=diet['tool']['sha256']), 'pinned DIET tool')
    inputs[diet['tool']['path']] = sha(tool.read_bytes())
    zun = DRIVE / 'TH03ZUN/product/zun.com'
    inputs[str(zun.relative_to(ROOT))] = sha(zun.read_bytes())
    return base, config, reviewed, inputs, responses, maps


def startup_scope(raw, config):
    # Reuse only the complete original-object comparator. No ancestor builder,
    # runtime matrix or historical receipt chain is executed here.
    from build_th03_runtime_after548_work import scope
    return scope((ROOT / config['original']['path']).read_bytes(), raw, config)


def commands(base, config, number):
    yield 'assemble', native() + [str(ROOT / config['native_tools']['tasm']['path']),
                                  *config['native_flags'], 'c0.ASM,c0l.obj'], base / 'startup', 0
    for product, (tree, _) in PRODUCTS.items():
        yield product + '-link', dos() + ['tlink', '@' + windows(base / f'r{number}/{product}.lnk')], DRIVE / tree, 0
    for filename in ('op.exe', 'mainl.exe', 'zun.com'):
        yield filename + '-pack', dos() + ['DIET.EXE', '-B', filename], base / f'r{number}/packed', 1
        yield filename + '-restore', dos() + ['DIET.EXE', '-ra', filename], base / f'r{number}/restore', 1


def review(stage=STAGE, reviewed=None):
    base, config, verified, inputs, responses, maps = context(stage, reviewed)
    proof = json.loads((base / 'package-build.json').read_bytes())
    need(proof['complete'] and proof['stage'] == stage and proof['inputs'] == inputs and
         proof['parents'] == verified, 'complete current source/tool/context binding')
    need((base / 'startup/c0.ASM').read_bytes() == (ROOT / config['source']).read_bytes(), 'actual maintained C0 source')
    need(all((base / name).read_bytes() == raw for name, raw in responses.items()), 'actual complete linker responses')
    expected = [(f'r{n}-{label}', argv, str(cwd), code) for n in (1, 2)
                for label, argv, cwd, code in commands(base, config, n)]
    need([(p['label'], p['argv'], p['cwd'], p['returncode']) for p in proof['phases']] == expected,
         'all actual serial assembly/link/pack/restore commands')
    for phase in proof['phases']:
        need(sha((base / (phase['label'] + '.log')).read_bytes()) == phase['log_sha256'], 'actual writer log')
        if phase['label'].endswith(('-pack', '-restore')):
            need(b'Success!' in (base / (phase['label'] + '.log')).read_bytes(), 'DIET success marker')
    targets = load_target_manifest(ROOT / 'config/targets.toml')
    diet = tomllib.loads((ROOT / 'config/th03_diet.toml').read_text())
    decoded = {a['filename']: a for a in diet['artifacts']}
    vectors = []
    need(len(proof['rounds']) == 2 and [r['round'] for r in proof['rounds']] == [1, 2], 'both native rounds')
    for number, row in enumerate(proof['rounds'], 1):
        rd = base / f'r{number}'
        names = {'c0l.obj', 'main.exe', 'main.map', 'op.exe', 'op.map', 'mainl.exe', 'mainl.map'}
        names |= {'packed/' + n for n in ('main.exe', 'op.exe', 'mainl.exe', 'zun.com')}
        names |= {'restore/' + n for n in ('op.exe', 'mainl.exe', 'zun.com')}
        need(set(row['outputs']) == names, 'entire fourteen-file native/package/roundtrip vector')
        vector = {name: (rd / name).read_bytes() for name in names}
        need(row['outputs'] == {name: pin(rd / name) for name in names}, 'all raw output bytes/hashes')
        need(row['startup'] == startup_scope(vector['c0l.obj'], config), 'complete initialized storage and all ordered C0 fields')
        for product in PRODUCTS:
            filename = product + '.exe'
            raw = vector[filename]
            target = read_verified_artifact(ROOT, find_artifact(targets, 'th03-' + product))
            if product == 'main':
                need(compact_mz(raw) == target == vector['packed/' + filename], 'complete compact Japanese MAIN')
                reference = parse_mz(target)
            else:
                declaration = decoded[filename.upper()]
                need(sha(raw) == declaration['decoded_sha256'] and len(raw) == declaration['decoded_size'],
                     'complete Japanese decoded ' + product)
                reference = parse_mz(vector['restore/' + filename])
            image = parse_mz(raw)
            need(image.valid and image.program_image == reference.program_image and image.relocations == reference.relocations,
                 'entire loaded image and literal ordered MZ vector: ' + product)
            need(vector[product + '.map'] == maps[f'r{number}/{product}.map'], 'entire current native MAP')
        for product, filename in (('op', 'op.exe'), ('mainl', 'mainl.exe'), ('zun', 'zun.com')):
            target = read_verified_artifact(ROOT, find_artifact(targets, 'th03-' + product))
            need(vector['packed/' + filename] == target, 'entire canonical packed ' + product)
            original = vector[filename] if product != 'zun' else (DRIVE / 'TH03ZUN/product/zun.com').read_bytes()
            need(vector['restore/' + filename] == original, 'complete DIET roundtrip: ' + product)
        vectors.append(vector)
    # MAIN retains independently compiled r1/r2 module filenames in its MAP.
    # Each complete MAP was checked verbatim against its corresponding parent.
    # Every other raw output, including the other two MAPs, must repeat.
    need({k: v for k, v in vectors[0].items() if k != 'main.map'} ==
         {k: v for k, v in vectors[1].items() if k != 'main.map'}, 'all thirteen repeatable raw outputs')
    return dict(stage=stage, native_rounds=2, outputs_per_round=14, complete_four_file_package_equal=True,
                repeat_identical_outputs_per_round=13, complete_parent_MAPs_equal=True,
                startup_initialized_bytes=767, startup_ordered_fields=58,
                startup_PUBLIC_packet_order_equal=False, whole_product_source_accepted=False,
                factory_accepted=False, report=str((base / 'package-build.json').relative_to(ROOT)))


def build(stage):
    base, config, verified, inputs, responses, maps = context(stage)
    need(not base.exists(), 'unused package stage')
    proof = dict(complete=False, stage=stage, inputs=inputs, parents=verified, rounds=[], phases=[])
    diet = tomllib.loads((ROOT / 'config/th03_diet.toml').read_text())
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', MSDOS_PATH=r'C:\TC4\BIN')
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        (base / 'startup').mkdir(parents=True)
        source = base / 'startup/c0.ASM'
        source.write_bytes((ROOT / config['source']).read_bytes())
        os.utime(source, (946684800, 946684800))
        for name, raw in responses.items():
            path = base / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
        for number in (1, 2):
            rd = base / f'r{number}'
            for folder in ('packed', 'restore'):
                (rd / folder).mkdir()
                (rd / folder / 'DIET.EXE').write_bytes((ROOT / diet['tool']['path']).read_bytes())
            names = []
            for label, argv, cwd, code in commands(base, config, number):
                if label == 'assemble':
                    (base / 'startup/c0l.obj').unlink(missing_ok=True)
                if label.endswith('-pack'):
                    filename = label.removesuffix('-pack')
                    raw = ((DRIVE / 'TH03ZUN/product/zun.com').read_bytes() if filename == 'zun.com'
                           else (rd / filename).read_bytes())
                    (rd / 'packed' / filename).write_bytes(raw)
                elif label.endswith('-restore'):
                    filename = label.removesuffix('-restore')
                    (rd / 'restore' / filename).write_bytes((rd / 'packed' / filename).read_bytes())
                run = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
                full = f'r{number}-{label}'
                (base / (full + '.log')).write_bytes(run.stdout)
                proof['phases'].append(dict(label=full, argv=argv, cwd=str(cwd), returncode=run.returncode, log_sha256=sha(run.stdout)))
                need(run.returncode == code, 'native phase failed: ' + full)
                if label.endswith(('-pack', '-restore')):
                    need(b'Success!' in run.stdout, 'DIET success marker: ' + full)
            startup = (base / 'startup/c0l.obj').read_bytes()
            (rd / 'c0l.obj').write_bytes(startup)
            (rd / 'packed/main.exe').write_bytes(compact_mz((rd / 'main.exe').read_bytes()))
            names = ['c0l.obj', 'main.exe', 'main.map', 'op.exe', 'op.map', 'mainl.exe', 'mainl.map']
            names += ['packed/' + n for n in ('main.exe', 'op.exe', 'mainl.exe', 'zun.com')]
            names += ['restore/' + n for n in ('op.exe', 'mainl.exe', 'zun.com')]
            proof['rounds'].append(dict(round=number, outputs={n: pin(rd / n) for n in names}, startup=startup_scope(startup, config)))
            print(f'Package round {number}: source C0, three complete links, three DIET pack/restore pairs', flush=True)
        proof['complete'] = True
        (base / 'package-build.json').write_text(json.dumps(proof, indent=2) + '\n')
    return review(stage, verified)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', default=STAGE)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    print(json.dumps(build(args.stage) if args.build else review(args.stage), indent=2))


if __name__ == '__main__':
    main()
