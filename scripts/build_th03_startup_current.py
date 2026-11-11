#!/usr/bin/env python3
"""Rebuild the entire original large-model startup from supplier source."""
import argparse
import fcntl
import json
import os
import re
import subprocess

import build_th03_package_current as package
from lib.omf import parse_omf

ROOT, DRIVE = package.ROOT, package.DRIVE
DRIVER = 'scripts/build_th03_startup_current.py'
STAGE = 'af1408s'
SOURCES = {'c0.ASM': 'src/shared/crt/startup/c0.asm',
           'RULES.ASI': 'src/shared/crt/startup/rules.asi'}
TASM = dict(path='.analysis/toolchain/wineprefix/drive_c/TASM41/TASM.EXE',
            bytes=136018, sha256='cafc42bbd1df39ab36e775be74ccb82c0a80da7d2a6dff4dcc2f16ba0e220f95')
FLAGS = ('/m', '/mx', '/q', '/t', '/d__LARGE__')
need, sha, pin = package.need, package.sha, package.pin


def context(stage):
    need(re.fullmatch(r'af[0-9]+[a-z]', stage), 'DOS-safe startup stage')
    config = json.loads((ROOT / package.STARTUP_CONFIG).read_bytes())
    declarations = [config['original'], TASM,
                    config['native_tools']['msdos'], config['native_tools']['wine']]
    for row in declarations:
        raw = (ROOT / row['path']).read_bytes()
        need(sha(raw) == row['sha256'] and ('bytes' not in row or len(raw) == row['bytes']),
             'pinned original startup or native tool: ' + row['path'])
    sources = {name: (ROOT / path).read_bytes().replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
               for name, path in SOURCES.items()}
    inputs = {p: sha((ROOT / p).read_bytes()) for p in
              (DRIVER, package.DRIVER, package.STARTUP_CONFIG, 'scripts/shared_runtime.py',
               'scripts/lib/omf.py', *SOURCES.values())}
    inputs.update({row['path']: row['sha256'] for row in declarations})
    return DRIVE / 'TH03CRT' / stage, inputs, sources, (ROOT / config['original']['path']).read_bytes()


def command():
    # BUILD-C0.BAT's original DOS large-model invocation; retain c0.ASM's THEADR.
    return package.dos() + [package.windows(ROOT / TASM['path']), *FLAGS, 'c0,c0l.obj']


def review(stage=STAGE):
    base, inputs, sources, original = context(stage)
    report = json.loads((base / 'startup-build.json').read_bytes())
    need(report['complete'] and report['stage'] == stage and report['inputs'] == inputs,
         'complete current natural startup context')
    need(all((base / name).read_bytes() == raw for name, raw in sources.items()),
         'actual supplier source snapshots')
    need(len(report['rounds']) == 2 and [r['round'] for r in report['rounds']] == [1, 2],
         'two independent native startup rounds')
    for n, row in enumerate(report['rounds'], 1):
        need(row['argv'] == command() and row['cwd'] == str(base) and row['returncode'] == 0,
             'actual original-recipe DOS assembler command')
        need(sha((base / f'r{n}.log').read_bytes()) == row['log_sha256'], 'actual startup assembler log')
        output = base / f'r{n}/c0l.obj'
        need(row['output'] == pin(output) and output.read_bytes() == original,
             'entire original C0 OBJ, including literal record and PUBLIC order')
        parse_omf(output.read_bytes())
    need((base / 'c0l.obj').read_bytes() == original, 'actual final native startup output')
    return dict(stage=stage, native_rounds=2, complete_original_raw_OBJ_equal=True,
                original_OBJ_bytes=len(original), literal_ordered_fields_equal=True,
                literal_ordered_PUBLIC_records_equal=True,
                objects=[str((base / f'r{n}/c0l.obj').relative_to(ROOT)) for n in (1, 2)],
                report=str((base / 'startup-build.json').relative_to(ROOT)))


def build(stage):
    base, inputs, sources, original = context(stage)
    need(not base.exists(), 'unused natural startup stage')
    report = dict(complete=False, stage=stage, inputs=inputs, rounds=[])
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', MSDOS_PATH=r'C:\TC4\BIN')
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        base.mkdir(parents=True)
        for name, raw in sources.items():
            (base / name).write_bytes(raw)
        for n in (1, 2):
            (base / 'c0l.obj').unlink(missing_ok=True)
            argv = command()
            q = subprocess.run(argv, cwd=base, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
            (base / f'r{n}.log').write_bytes(q.stdout)
            need(q.returncode == 0, 'native supplier startup assembly')
            raw = (base / 'c0l.obj').read_bytes()
            need(raw == original, 'complete native C0 OBJ equals original')
            rd = base / f'r{n}'; rd.mkdir()
            (rd / 'c0l.obj').write_bytes(raw)
            report['rounds'].append(dict(round=n, argv=argv, cwd=str(base), returncode=q.returncode,
                                         log_sha256=sha(q.stdout), output=pin(rd / 'c0l.obj')))
        report['complete'] = True
        (base / 'startup-build.json').write_text(json.dumps(report, indent=2) + '\n')
    return review(stage)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage', default=STAGE); p.add_argument('--build', action='store_true')
    args = p.parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10: os.nice(10 - os.nice(0))
    print(json.dumps(build(args.stage) if args.build else review(args.stage), indent=2))


if __name__ == '__main__':
    main()
