#!/usr/bin/env python3
"""Rebuild MAINL root with maintained archive types/state; reuse unchanged context."""
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
DRIVER, REPORT = 'scripts/build_th03_mainl_archive_work.py', '.analysis/work/mainl-archive-build.json'
DATA_SOURCE = 'src/mainl/archive_io/archive_initialized.inl'
TYPES_OLD, TYPES = 'libs/master.lib/pf.inc', 'src/mainl/archive_io/archive_types.inl'
FORWARDER = ('include ' + TYPES + '\r\n').encode()
GETC = 'src/mainl/archive_io/pf_getc.inl'



def wrapper(files):
    return files[WRAPPER]


def response(files):
    raw = files['obj/th03/mainl.@l']
    for a, b in ((b'obj\\th03\\mainl.obj', b'probe\\arcroot.obj'),
                 (b'bin\\th03\\mainl.exe', b'probe\\arcroot.exe'),
                 (b'obj\\th03\\mainl.map', b'probe\\arcroot.map')):
        need(raw.count(a) == 1, 'one affected root at original link position')
        raw = raw.replace(a, b)
    return raw


def mini_wrappers():
    prefix = b'.386\r\n.model use16 large _TEXT\r\ninclude ReC98.inc\r\n_TEXT segment word public \'CODE\' use16\r\nassume cs:_TEXT\r\n'
    suffix = b'\r\n_TEXT ends\r\nend\r\n'
    result = {
        'buffer': prefix.replace(b'include ReC98.inc', b'.stack 32\r\ninclude ReC98.inc') + b'include src/mainl/archive_io/bfill.asm\r\ninclude src/mainl/archive_io/bgetc.asm' + suffix,
        'getc': prefix + b'extrn BGETC:far\r\ninclude ' + GETC.encode() + suffix,
        'read': prefix + b'include src/mainl/archive_io/pfread.asm' + suffix,
    }
    data_prefix = b'.386\r\n.model use16 large _TEXT\r\ninclude ReC98.inc\r\n_DATA segment word public \'DATA\' use16\r\n'
    data_suffix = b'\r\n_DATA ends\r\nend\r\n'
    result['state'] = data_prefix + b'include ' + DATA_SOURCE.encode() + data_suffix
    result['rand'] = data_prefix + b'include libs/master.lib/rand[data].asm' + data_suffix
    return result


def mini_response():
    return b'-c -s probe\\arc-buffer.obj probe\\arc-getc.obj probe\\arc-read.obj probe\\arc-state.obj probe\\arc-rand.obj,probe\\arcmini.exe,probe\\arcmini.map\r\n'


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    cold_raw, files, _ = cold_context(ROOT)
    sources = {n: (ROOT / n).read_bytes() for n in [TYPES, GETC, DATA_SOURCE]}
    need(files[TYPES_OLD].replace(b'\r\n', b'\n').rstrip(b'\n') in sources[TYPES], 'complete original constants and structure')
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
        rounds=[], mini_rounds=[], native_phases=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(report, indent=2) + '\n')
    def execute(argv, label):
        result = subprocess.run(argv, cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        (build.OUT / ('archive-' + label + '.log')).write_bytes(result.stdout)
        report['native_phases'].append(dict(label=label, command=argv, returncode=result.returncode, log_sha256=sha(result.stdout)))
        save()
        need(result.returncode == 0, label + ': ' + result.stdout.decode(errors='replace')[-1000:])
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        original, stamp = (work / WRAPPER).read_bytes(), (work / WRAPPER).stat()
        mini = {f'probe/arc-{n}.asm': b for n,b in mini_wrappers().items()}
        mini['probe/arcmini.lnk'] = mini_response()
        old_types, types_stamp = (work / TYPES_OLD).read_bytes(), (work / TYPES_OLD).stat()
        temporary = [work / n for n in (*sources, 'probe/arcroot.obj', 'probe/arcroot.exe', 'probe/arcroot.map', 'probe/arcroot.lnk')]
        temporary += [work/n for n in mini] + [work/f'probe/arc-{n}.obj' for n in mini_wrappers()] + [work/'probe/arcmini.exe',work/'probe/arcmini.map']
        need(all(not p.exists() for p in temporary), 'fresh selected temporary paths')
        try:
            (work / 'probe').mkdir(exist_ok=True)
            for name, content in [*sources.items(), *mini.items(), (WRAPPER, generated), ('probe/arcroot.lnk', link), (TYPES_OLD, FORWARDER)]:
                (work / name).write_bytes(content)
                os.utime(work / name, (946684800, 946684800))
            (build.OUT / 'archive-root.asm').write_bytes(generated)
            (build.OUT / 'archive-root.lnk').write_bytes(link)
            for number in (1, 2):
                for ext in ('obj', 'exe', 'map'):
                    (work / f'probe/arcroot.{ext}').unlink(missing_ok=True)
                execute(tasm + ['/m', '/mx', '/kh32768', '/t', '/dGAME=3', WRAPPER, r'probe\arcroot.obj'], f'round{number}-assemble')
                raw, baseline = (work / 'probe/arcroot.obj').read_bytes(), (work / OBJECT).read_bytes()
                need(describe_omf(raw)['valid'] and native_records(raw) == native_records(baseline) and
                     public_records(raw) == public_records(baseline), 'complete native payload/fixup order/public identity')
                execute(dos + ['tlink', r'@probe\arcroot.lnk'], f'round{number}-link')
                outputs = {}
                for ext in ('obj', 'exe', 'map'):
                    raw = (work / f'probe/arcroot.{ext}').read_bytes()
                    path = f'.analysis/work/archive-round{number}.{ext}'
                    (ROOT / path).write_bytes(raw)
                    outputs[ext] = dict(path=path, bytes=len(raw), sha256=sha(raw))
                need((work / 'probe/arcroot.exe').read_bytes() == (work / 'bin/th03/mainl.target.exe').read_bytes() and
                     (work / 'probe/arcroot.map').read_bytes() == (work / 'obj/th03/mainl.map').read_bytes(), 'whole pinned target and retained MAP')
                report['rounds'].append(dict(round=number, outputs=outputs))
                mini_outputs = {}
                for name in mini_wrappers():
                    output = f'probe/arc-{name}.obj'
                    (work/output).unlink(missing_ok=True)
                    execute(tasm + ['/m', '/mx', '/kh32768', '/t', '/dGAME=3', rf'probe\arc-{name}.asm', output.replace('/', '\\')], f'round{number}-mini-{name}')
                    raw = (work/output).read_bytes()
                    path = f'.analysis/work/archive-mini-round{number}-{name}.obj'
                    (ROOT/path).write_bytes(raw)
                    mini_outputs[name] = dict(path=path, bytes=len(raw), sha256=sha(raw))
                for ext in ('exe','map'):
                    (work/f'probe/arcmini.{ext}').unlink(missing_ok=True)
                execute(dos + ['tlink', r'@probe\arcmini.lnk'], f'round{number}-mini-link')
                for ext in ('exe','map'):
                    raw = (work/f'probe/arcmini.{ext}').read_bytes()
                    path = f'.analysis/work/archive-mini-round{number}.{ext}'
                    (ROOT/path).write_bytes(raw)
                    mini_outputs[ext] = dict(path=path, bytes=len(raw), sha256=sha(raw))
                report['mini_rounds'].append(dict(round=number,outputs=mini_outputs))

                save()
                print(f'archive round{number}: maintained archive/native root/whole target and MAP PASS', flush=True)
            need({k: v['sha256'] for k, v in report['rounds'][0]['outputs'].items()} ==
                 {k: v['sha256'] for k, v in report['rounds'][1]['outputs'].items()}, 'complete raw selected repeat equality')
            need({k:v['sha256'] for k,v in report['mini_rounds'][0]['outputs'].items()} ==
                 {k:v['sha256'] for k,v in report['mini_rounds'][1]['outputs'].items()}, 'complete raw mini repeat equality')
        finally:
            (work / WRAPPER).write_bytes(original)
            os.utime(work / WRAPPER, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))
            (work / TYPES_OLD).write_bytes(old_types)
            os.utime(work / TYPES_OLD, ns=(types_stamp.st_atime_ns, types_stamp.st_mtime_ns))
            for p in temporary:
                p.unlink(missing_ok=True)
    cold_context(ROOT)
    report['complete'] = True
    save()


if __name__ == '__main__':
    main()
