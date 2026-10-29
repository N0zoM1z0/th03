#!/usr/bin/env python3
"""Reassemble one MAINL root with a generated pixel table and relink twice."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tomllib
from collections import Counter

import build_th03_mainl_work as build
from lib.omf import describe_omf, parse_omf
from lib.targets import find_artifact, read_verified_artifact
from lib.toolchain import attest_surface

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'src/mainl/resources/pixel_rotation_table.inl'
OLD = 'src/mainl/resources/rottbl.asm'
WRAPPER, OBJECT = 'th03_mainl.asm', 'obj/th03/mainl.obj'
DRIVER, REPORT = 'scripts/build_th03_mainl_resources_work.py', '.analysis/work/mainl-resources-build.json'
sha = lambda b: hashlib.sha256(b).hexdigest()


def need(value, message):
    if not value:
        raise ValueError('MAINL selected resources: ' + str(message))


def cold_context(root):
    raw = (build.OUT / 'mainl-build.json').read_bytes()
    report = json.loads(raw)
    files, graph, archive = build.sources()
    need(report['complete'] and report['raw_repeat_equal'] and report['retained_project_objects'] == 0 and
         report['recipe_sha256'] == build.recipe_inventory() and report['archive_sha256'] == archive and
         report['vendor_header_sha256'] == build.vendor_header_inventory(), 'complete current cold source/recipe/SDK context')
    need(report['source_sha256'] == {n: sha(b) for n, b in sorted(files.items())} and
         all((build.WORK / n).read_bytes() == b for n, b in files.items()), 'entire source graph and staging')
    need(len(report['rounds']) == 2 and report['rounds'][0]['outputs'] == report['rounds'][1]['outputs'] and
         len(report['rounds'][0]['outputs']) == 938, 'complete raw cold pair')
    for name, info in report['rounds'][0]['outputs'].items():
        content = (build.WORK / name).read_bytes()
        need(info == dict(bytes=len(content), sha256=sha(content)), 'current cold output: ' + name)
    config = tomllib.loads((root / 'config/toolchain.toml').read_text())
    need(report['toolchain_surfaces'] == [attest_surface(root, s) for s in config['surfaces'] if not s.get('bootstrap_only')],
         'current pinned native tools')
    prefix = root / config['paths']['wine_prefix']
    need(sha((prefix / 'drive_c/TC4/LIB/CL.LIB').read_bytes()) == report['vendor_library_sha256'], 'vendor CRT context')
    targets = tomllib.loads((root / 'config/targets.toml').read_text())
    stored = read_verified_artifact(root, find_artifact(targets, 'th03-mainl'))
    declaration, = [a for a in tomllib.loads((root / 'config/th03_diet.toml').read_text())['artifacts'] if a['id'] == 'th03-mainl']
    target = (build.WORK / 'bin/th03/mainl.target.exe').read_bytes()
    need(sha(target) == declaration['decoded_sha256'] and len(target) == declaration['decoded_size'] and
         (build.WORK / 'bin/th03/mainl.exe').read_bytes() == target and
         (build.WORK / 'bin/th03/mainl.packed.exe').read_bytes() == stored, 'pinned Japanese decoded/stored context')
    return raw, files, graph


def wrapper(files):
    marker = ('include ' + OLD).encode()
    need(files[WRAPPER].count(marker) == 1, 'one original table include')
    return files[WRAPPER].replace(marker, ('include ' + SOURCE).encode())


def response(files):
    result = files['obj/th03/mainl.@l']
    for a, b in ((b'obj\\th03\\mainl.obj', b'probe\\resroot.obj'),
                 (b'bin\\th03\\mainl.exe', b'probe\\resroot.exe'),
                 (b'obj\\th03\\mainl.map', b'probe\\resroot.map')):
        need(result.count(a) == 1, 'one affected root in unchanged link order')
        result = result.replace(a, b)
    return result


def native_records(raw):
    # Extra symbolic equates change TASM's public-symbol hash traversal.
    # Preserve every other record literally, including the complete FIXUPP
    # sequence; compare complete PUBDEF records with multiplicity separately.
    return [(r.name, r.data.hex()) for r in parse_omf(raw) if r.name not in ('COMENT', 'PUBDEF')]


def public_records(raw):
    return Counter(r.data for r in parse_omf(raw) if r.name == 'PUBDEF')


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    cold_raw, files, graph = cold_context(ROOT)
    source = (ROOT / SOURCE).read_bytes()
    generated, link = wrapper(files), response(files)
    cfg = tomllib.loads((ROOT / 'config/toolchain.toml').read_text())
    prefix, work = ROOT / cfg['paths']['wine_prefix'], build.WORK
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / cfg['paths']['msdos_player']), '-e', '-x']
    tasm = ['/usr/bin/wine-stable', str(prefix / 'drive_c/TASM50/bin/TASM32.EXE')]
    report = dict(complete=False, source_acceptance=False, whole_product_cold_rebuilt=False, context_project_objects=35,
        driver_sha256=sha((ROOT / DRIVER).read_bytes()), cold_report_sha256=sha(cold_raw),
        source_sha256=sha(source), wrapper_sha256=sha(generated), response_sha256=sha(link), rounds=[], native_phases=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(report, indent=2) + '\n')
    def execute(argv, label):
        result = subprocess.run(argv, cwd=work, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        (build.OUT / ('resources-' + label + '.log')).write_bytes(result.stdout)
        report['native_phases'].append(dict(label=label, command=argv, returncode=result.returncode, log_sha256=sha(result.stdout)))
        save()
        need(result.returncode == 0, label + ': ' + result.stdout.decode(errors='replace')[-1000:])
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        original, stamp = (work / WRAPPER).read_bytes(), (work / WRAPPER).stat()
        names = (SOURCE, 'probe/resroot.obj', 'probe/resroot.exe', 'probe/resroot.map', 'probe/resroot.lnk')
        temporary = [work / n for n in names]
        need(all(not p.exists() for p in temporary), 'fresh scoped temporary paths')
        try:
            (work / 'probe').mkdir(exist_ok=True)
            for name, content in ((SOURCE, source), (WRAPPER, generated), ('probe/resroot.lnk', link)):
                (work / name).write_bytes(content)
                os.utime(work / name, (946684800, 946684800))
            (build.OUT / 'resources-root.asm').write_bytes(generated)
            (build.OUT / 'resources-root.lnk').write_bytes(link)
            for number in (1, 2):
                for p in temporary[1:4]:
                    p.unlink(missing_ok=True)
                execute(tasm + ['/m', '/mx', '/kh32768', '/t', '/dGAME=3', WRAPPER, r'probe\resroot.obj'], f'round{number}-assemble')
                obj = (work / 'probe/resroot.obj').read_bytes()
                (build.OUT / f'resources-round{number}.obj').write_bytes(obj)
                baseline = (work / OBJECT).read_bytes()
                need(describe_omf(obj)['valid'] and native_records(obj) == native_records(baseline) and
                     public_records(obj) == public_records(baseline),
                     'whole native records/literal fixup order and complete public identity')
                execute(dos + ['tlink', r'@probe\resroot.lnk'], f'round{number}-link')
                outputs = {}
                for suffix in ('obj', 'exe', 'map'):
                    raw = (work / f'probe/resroot.{suffix}').read_bytes()
                    dest = f'.analysis/work/resources-round{number}.{suffix}'
                    (ROOT / dest).write_bytes(raw)
                    outputs[suffix] = dict(path=dest, bytes=len(raw), sha256=sha(raw))
                need((work / 'probe/resroot.exe').read_bytes() == (work / 'bin/th03/mainl.target.exe').read_bytes() and
                     (work / 'probe/resroot.map').read_bytes() == (work / 'obj/th03/mainl.map').read_bytes(), 'whole target EXE and retained MAP equality')
                report['rounds'].append(dict(round=number, outputs=outputs))
                save()
                print(f'resources round{number}: natural generated table/full native root/whole linked target PASS', flush=True)
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
