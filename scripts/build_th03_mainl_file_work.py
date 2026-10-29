#!/usr/bin/env python3
"""Rebuild MAINL root with maintained file/hook state; reuse unchanged context."""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import tomllib

import build_th03_mainl_work as build
from build_th03_mainl_resources_work import cold_context, need, sha, native_records, public_records
from lib.omf import describe_omf

ROOT = Path(__file__).resolve().parents[1]
WRAPPER, OBJECT = 'th03_mainl.asm', 'obj/th03/mainl.obj'
DRIVER, REPORT = 'scripts/build_th03_mainl_file_work.py', '.analysis/work/mainl-file-build.json'
STATE = (
    ('libs/master.lib/fil[data].asm', 'src/mainl/archive_io/file_initialized.inl'),
    ('libs/master.lib/fil[bss].asm', 'src/mainl/archive_io/file_uninitialized.inl'),
    ('libs/master.lib/pfint21[bss].asm', 'src/mainl/archive_io/hook_uninitialized.inl'),
)


def wrapper(files):
    raw = files[WRAPPER]
    for old, new in STATE:
        marker = ('include ' + old).encode()
        need(raw.count(marker) == 1, 'one state provider at original source position')
        raw = raw.replace(marker, ('include ' + new).encode())
    return raw


def response(files):
    raw = files['obj/th03/mainl.@l']
    for a, b in ((b'obj\\th03\\mainl.obj', b'probe\\fileroot.obj'),
                 (b'bin\\th03\\mainl.exe', b'probe\\fileroot.exe'),
                 (b'obj\\th03\\mainl.map', b'probe\\fileroot.map')):
        need(raw.count(a) == 1, 'one affected root at original link position')
        raw = raw.replace(a, b)
    return raw


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    cold_raw, files, _ = cold_context(ROOT)
    sources = {n: (ROOT / n).read_bytes() for _, n in STATE}
    generated, link = wrapper(files), response(files)
    config = tomllib.loads((ROOT / 'config/toolchain.toml').read_text())
    prefix, work = ROOT / config['paths']['wine_prefix'], build.WORK
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / config['paths']['msdos_player']), '-e', '-x']
    tasm = ['/usr/bin/wine-stable', str(prefix / 'drive_c/TASM50/bin/TASM32.EXE')]
    report = dict(complete=False, source_acceptance=False, whole_product_cold_rebuilt=False, context_project_objects=35,
        driver_sha256=sha((ROOT / DRIVER).read_bytes()), cold_report_sha256=sha(cold_raw),
        source_sha256={n: sha(b) for n, b in sources.items()}, wrapper_sha256=sha(generated), response_sha256=sha(link),
        rounds=[], native_phases=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(report, indent=2) + '\n')
    def execute(argv, label):
        result = subprocess.run(argv, cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        (build.OUT / ('file-' + label + '.log')).write_bytes(result.stdout)
        report['native_phases'].append(dict(label=label, command=argv, returncode=result.returncode, log_sha256=sha(result.stdout)))
        save()
        need(result.returncode == 0, label + ': ' + result.stdout.decode(errors='replace')[-1000:])
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        original, stamp = (work / WRAPPER).read_bytes(), (work / WRAPPER).stat()
        temporary = [work / n for n in (*sources, 'probe/fileroot.obj', 'probe/fileroot.exe', 'probe/fileroot.map', 'probe/fileroot.lnk')]
        need(all(not p.exists() for p in temporary), 'fresh selected temporary paths')
        try:
            (work / 'probe').mkdir(exist_ok=True)
            for name, content in [*sources.items(), (WRAPPER, generated), ('probe/fileroot.lnk', link)]:
                (work / name).write_bytes(content)
                os.utime(work / name, (946684800, 946684800))
            (build.OUT / 'file-root.asm').write_bytes(generated)
            (build.OUT / 'file-root.lnk').write_bytes(link)
            for number in (1, 2):
                for ext in ('obj', 'exe', 'map'):
                    (work / f'probe/fileroot.{ext}').unlink(missing_ok=True)
                execute(tasm + ['/m', '/mx', '/kh32768', '/t', '/dGAME=3', WRAPPER, r'probe\fileroot.obj'], f'round{number}-assemble')
                raw, baseline = (work / 'probe/fileroot.obj').read_bytes(), (work / OBJECT).read_bytes()
                need(describe_omf(raw)['valid'] and native_records(raw) == native_records(baseline) and
                     public_records(raw) == public_records(baseline), 'complete native payload/fixup order/public identity')
                execute(dos + ['tlink', r'@probe\fileroot.lnk'], f'round{number}-link')
                outputs = {}
                for ext in ('obj', 'exe', 'map'):
                    raw = (work / f'probe/fileroot.{ext}').read_bytes()
                    path = f'.analysis/work/file-round{number}.{ext}'
                    (ROOT / path).write_bytes(raw)
                    outputs[ext] = dict(path=path, bytes=len(raw), sha256=sha(raw))
                need((work / 'probe/fileroot.exe').read_bytes() == (work / 'bin/th03/mainl.target.exe').read_bytes() and
                     (work / 'probe/fileroot.map').read_bytes() == (work / 'obj/th03/mainl.map').read_bytes(), 'whole pinned target and retained MAP')
                report['rounds'].append(dict(round=number, outputs=outputs))
                save()
                print(f'file round{number}: maintained state/native root/whole target and MAP PASS', flush=True)
            need({k: v['sha256'] for k, v in report['rounds'][0]['outputs'].items()} ==
                 {k: v['sha256'] for k, v in report['rounds'][1]['outputs'].items()}, 'complete raw selected repeat equality')
        finally:
            (work / WRAPPER).write_bytes(original)
            os.utime(work / WRAPPER, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))
            for p in temporary:
                p.unlink(missing_ok=True)
    cold_context(ROOT)
    report['complete'] = True
    save()


if __name__ == '__main__':
    main()
