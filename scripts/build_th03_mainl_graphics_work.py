#!/usr/bin/env python3
"""Rebuild MAINL root with maintained clip geometry/generated masks; reuse unchanged context."""
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
DRIVER, REPORT = 'scripts/build_th03_mainl_graphics_work.py', '.analysis/work/mainl-graphics-build.json'
STATE = (
    ('libs/master.lib/clip[data].asm', 'src/mainl/display_hardware/clip_initialized.inl'),
    ('libs/master.lib/edges[data].asm', 'src/mainl/display_hardware/edge_masks.inl'),
    ('libs/master.lib/wordmask[data].asm', 'src/mainl/display_hardware/byte_masks.inl'),
    ('libs/master.lib/mem[data].asm', 'src/mainl/memory/heap_initialized.inl'),
    ('libs/master.lib/mem[bss].asm', 'src/mainl/memory/heap_uninitialized.inl'),
)
COPY = 'src/mainl/display_hardware/page_copy.inl'


def wrapper(files):
    raw = files[WRAPPER]
    for old, new in STATE:
        marker = ('include ' + old).encode()
        need(raw.count(marker) == 1, 'one state provider at original source position')
        raw = raw.replace(marker, ('include ' + new).encode())
    return raw


def response(files):
    raw = files['obj/th03/mainl.@l']
    for a, b in ((b'obj\\th03\\mainl.obj', b'probe\\gfxroot.obj'),
                 (b'bin\\th03\\mainl.exe', b'probe\\gfxroot.exe'),
                 (b'obj\\th03\\mainl.map', b'probe\\gfxroot.map')):
        need(raw.count(a) == 1, 'one affected root at original link position')
        raw = raw.replace(a, b)
    return raw


def mini_wrappers():
    prefix = b'.386\r\n.model use16 large _TEXT\r\n'
    suffix = b'\r\nend\r\n'
    memory = prefix + b'.stack 32\r\ninclude ReC98.inc\r\n_TEXT segment word public \'CODE\' use16\r\nassume cs:_TEXT,ds:DGROUP\r\n'
    memory += b'include src/mainl/memory/heap.inl\r\ninclude src/mainl/resources/smem_release.asm\r\ninclude src/mainl/resources/smem_wget.asm\r\n_TEXT ends\r\n'
    memory += b'_DATA segment word public \'DATA\' use16\r\ninclude src/mainl/memory/heap_initialized.inl\r\ninclude libs/master.lib/grp[data].asm\r\n_DATA ends\r\n'
    memory += b'_BSS segment word public \'BSS\' use16\r\ninclude src/mainl/memory/heap_uninitialized.inl\r\n_BSS ends\r\nDGROUP group _DATA,_BSS'
    copy = prefix + b'include ReC98.inc\r\n_DATA segment word public \'DATA\' use16\r\nextrn graph_VramWords:word\r\n_DATA ends\r\n'
    copy += b'extrn SMEM_WGET:far,SMEM_RELEASE:far\r\n_TEXT segment word public \'CODE\' use16\r\nassume cs:_TEXT,ds:DGROUP\r\ninclude ' + COPY.encode() + b'\r\n_TEXT ends'
    return {'memory':memory+suffix, 'copy':copy+suffix}


def mini_response():
    return b'-c -s probe\\gfx-memory.obj probe\\gfx-copy.obj,probe\\gfxmini.exe,probe\\gfxmini.map\r\n'


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    cold_raw, files, _ = cold_context(ROOT)
    sources = {n: (ROOT / n).read_bytes() for n in [COPY]+[n for _, n in STATE]}
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
        (build.OUT / ('graphics-' + label + '.log')).write_bytes(result.stdout)
        report['native_phases'].append(dict(label=label, command=argv, returncode=result.returncode, log_sha256=sha(result.stdout)))
        save()
        need(result.returncode == 0, label + ': ' + result.stdout.decode(errors='replace')[-1000:])
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        original, stamp = (work / WRAPPER).read_bytes(), (work / WRAPPER).stat()
        mini = {f'probe/gfx-{n}.asm':b for n,b in mini_wrappers().items()}
        mini['probe/gfxmini.lnk'] = mini_response()
        temporary = [work / n for n in (*sources, 'probe/gfxroot.obj', 'probe/gfxroot.exe', 'probe/gfxroot.map', 'probe/gfxroot.lnk')]
        temporary += [work/n for n in mini] + [work/f'probe/gfx-{n}.obj' for n in mini_wrappers()] + [work/'probe/gfxmini.exe',work/'probe/gfxmini.map']
        need(all(not p.exists() for p in temporary), 'fresh selected temporary paths')
        try:
            (work / 'probe').mkdir(exist_ok=True)
            for name, content in [*sources.items(), *mini.items(), (WRAPPER, generated), ('probe/gfxroot.lnk', link)]:
                (work / name).write_bytes(content)
                os.utime(work / name, (946684800, 946684800))
            (build.OUT / 'graphics-root.asm').write_bytes(generated)
            (build.OUT / 'graphics-root.lnk').write_bytes(link)
            for name,content in mini_wrappers().items():
                (build.OUT/f'graphics-mini-{name}.asm').write_bytes(content)
            (build.OUT/'graphics-mini.lnk').write_bytes(mini_response())
            for number in (1, 2):
                for ext in ('obj', 'exe', 'map'):
                    (work / f'probe/gfxroot.{ext}').unlink(missing_ok=True)
                execute(tasm + ['/m', '/mx', '/kh32768', '/t', '/dGAME=3', WRAPPER, r'probe\gfxroot.obj'], f'round{number}-assemble')
                raw, baseline = (work / 'probe/gfxroot.obj').read_bytes(), (work / OBJECT).read_bytes()
                need(describe_omf(raw)['valid'] and native_records(raw) == native_records(baseline) and
                     public_records(raw) == public_records(baseline), 'complete native payload/fixup order/public identity')
                execute(dos + ['tlink', r'@probe\gfxroot.lnk'], f'round{number}-link')
                outputs = {}
                for ext in ('obj', 'exe', 'map'):
                    raw = (work / f'probe/gfxroot.{ext}').read_bytes()
                    path = f'.analysis/work/graphics-round{number}.{ext}'
                    (ROOT / path).write_bytes(raw)
                    outputs[ext] = dict(path=path, bytes=len(raw), sha256=sha(raw))
                need((work / 'probe/gfxroot.exe').read_bytes() == (work / 'bin/th03/mainl.target.exe').read_bytes() and
                     (work / 'probe/gfxroot.map').read_bytes() == (work / 'obj/th03/mainl.map').read_bytes(), 'whole pinned target and retained MAP')
                report['rounds'].append(dict(round=number, outputs=outputs))
                mini_outputs = {}
                for name in mini_wrappers():
                    output = rf'probe\gfx-{name}.obj'
                    (work/output.replace('\\','/')).unlink(missing_ok=True)
                    execute(tasm + ['/m','/mx','/kh32768','/t','/dGAME=3',rf'probe\gfx-{name}.asm',output],f'round{number}-mini-{name}')
                    raw = (work/output.replace('\\','/')).read_bytes()
                    path = f'.analysis/work/graphics-mini-round{number}-{name}.obj'
                    (ROOT/path).write_bytes(raw)
                    mini_outputs[name] = dict(path=path,bytes=len(raw),sha256=sha(raw))
                for ext in ('exe','map'):
                    (work/f'probe/gfxmini.{ext}').unlink(missing_ok=True)
                execute(dos+['tlink',r'@probe\gfxmini.lnk'],f'round{number}-mini-link')
                for ext in ('exe','map'):
                    raw = (work/f'probe/gfxmini.{ext}').read_bytes()
                    path = f'.analysis/work/graphics-mini-round{number}.{ext}'
                    (ROOT/path).write_bytes(raw)
                    mini_outputs[ext] = dict(path=path,bytes=len(raw),sha256=sha(raw))
                report['mini_rounds'].append(dict(round=number,outputs=mini_outputs))

                save()
                print(f'graphics round{number}: maintained state/native root/whole target and MAP PASS', flush=True)
            need({k: v['sha256'] for k, v in report['rounds'][0]['outputs'].items()} ==
                 {k: v['sha256'] for k, v in report['rounds'][1]['outputs'].items()}, 'complete raw selected repeat equality')
            need({k:v['sha256'] for k,v in report['mini_rounds'][0]['outputs'].items()} ==
                 {k:v['sha256'] for k,v in report['mini_rounds'][1]['outputs'].items()},'complete raw native far-call mini repeat equality')
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
