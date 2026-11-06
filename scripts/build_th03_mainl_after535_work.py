#!/usr/bin/env python3
"""Replace the prebuilt large-model startup, retaining the source-bound CRT.

Only C0 is assembled and MAINL linked. The original object is an oracle, never
an output template. Native ordered metadata differences remain literal.
"""
import fcntl
import json
import os
import subprocess
import sys
from pathlib import Path

import setuptools

sys.setrecursionlimit(max(sys.getrecursionlimit(), 5000))
import review_th03_mainl_after534_work as parent
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import object_program_records

b = parent.b
ROOT = Path(__file__).resolve().parents[1]
DRIVER = 'scripts/build_th03_mainl_after535_work.py'
CONFIG = 'config/th03_mainl_startup.json'
PREFIX = '.analysis/work/mainl-after535-startup-'
RAW_PREFIX = '.analysis/work/af535e-startup-'
REPORT = PREFIX + 'build.json'
SCRATCH = b.WORK / 'probe/af535e'


def inputs():
    raw = (ROOT / CONFIG).read_bytes()
    config = json.loads(raw)
    need(config['schema'] == 'th03-mainl-large-startup-v1', 'large startup schema')
    for pin in [config['original'], *config['supplier_inputs']]:
        data = (ROOT / pin['path']).read_bytes()
        need(pin == dict(path=pin['path'], bytes=len(data), sha256=sha(data)),
             'pinned original startup/supplier input ' + pin['path'])
    return config, sha(raw)


def profile(blob):
    need(b.describe_omf(blob)['valid'], 'complete actual startup OMF')
    ss = b.segment_definitions(blob)
    data = b.initialized_payload(blob)
    need(set(data) <= {(s['index'], i) for s in ss for i in range(s['size'])},
         'startup initialization within original extents')
    records = b.parse_omf(blob)
    return dict(segments=ss,
        initialized=[dict(segment=s['index'], bytes=sum((s['index'], i) in data for i in range(s['size'])),
            sha256=sha(bytes(data[s['index'], i] for i in range(s['size']) if (s['index'], i) in data)),
            uninitialized=[i for i in range(s['size']) if (s['index'], i) not in data]) for s in ss],
        records={name: [r.data.hex() for r in records if r.name == name]
                 for name in ('THEADR', 'SEGDEF', 'GRPDEF', 'PUBDEF', 'EXTDEF', 'ALIAS', 'MODEND')},
        literal_fields=b.literal_fields(blob))


def compare(original, native, config):
    a, z = profile(original), profile(native)
    need(a['segments'] == z['segments'] and a['initialized'] == z['initialized'],
         'complete original startup initialized/uninitialized CODE/DATA/STACK')
    need(a['segments'][0]['size'] == config['original_CODE_extent'] and
         a['initialized'][0]['bytes'] == config['original_CODE_initialized_bytes'] and
         a['initialized'][0]['uninitialized'] == config['CODE_uninitialized_sites'] and
         a['initialized'][5]['bytes'] == config['original_DATA_bytes'] and
         a['segments'][16]['size'] == config['original_STACK_uninitialized_bytes'],
         'original cache word, model word, runtime DATA and stack reservations')
    need(all(a['records'][n] == z['records'][n]
             for n in ('THEADR', 'SEGDEF', 'GRPDEF', 'EXTDEF', 'ALIAS', 'MODEND')) and
         sorted(a['records']['PUBDEF']) == sorted(z['records']['PUBDEF']),
         'all original segment flags, group, imports, entry and public definitions')
    key = lambda f: (f['segment'], f['site'])
    need(len(a['literal_fields']) == len(z['literal_fields']) == config['literal_relocation_fields'] and
         sorted(a['literal_fields'], key=key) == sorted(z['literal_fields'], key=key) and
         [[f['segment'], f['site']] for f in z['literal_fields']] == config['native_literal_field_order'],
         'every literal frame/target/addend and explicitly pinned emitted order')
    return dict(original=a, native=z,
        literal_ordered_fields_equal=a['literal_fields'] == z['literal_fields'],
        literal_ordered_publics_equal=a['records']['PUBDEF'] == z['records']['PUBDEF'],
        original_member_program_equal=object_program_records(original) == object_program_records(native))


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    config, config_hash = inputs()
    baseline = parent.review()
    latest, latest_hash = parent.load(b.PREFIX + parent.MODE + '-build.json')
    source = (ROOT / config['source']).read_bytes()
    original = (ROOT / config['original']['path']).read_bytes()
    prefix = ROOT / '.analysis/toolchain/wineprefix'
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
        WINEPREFIX=str(prefix), MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    tasm = ['/usr/bin/wine-stable', str(prefix / 'drive_c/TASM50/bin/TASM32.EXE')]
    dos = ['/usr/bin/wine-stable', str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    record = dict(complete=False, source_acceptance=False, authored_game_credit_bytes=0,
        original_cold_rebuilt=False, driver_sha256=sha((ROOT / DRIVER).read_bytes()),
        config_sha256=config_hash, source_sha256=sha(source), baseline_ownership=baseline,
        latest_CRT_build_sha256=latest_hash, assembler_flags=config['assembler_flags'],
        original_startup_sha256=sha(original), phases=[], rounds=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(record, indent=2) + '\n')

    def run(argv, cwd, label):
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=90)
        path = RAW_PREFIX + label + '.log'
        (ROOT / path).write_bytes(result.stdout)
        record['phases'].append(dict(label=label, argv=argv, returncode=result.returncode,
                                     log_path=path, log_sha256=sha(result.stdout)))
        save()
        need(result.returncode == 0, label + ': ' + result.stdout.decode(errors='replace')[-1500:])

    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(not SCRATCH.exists(), 'fresh retained startup work directory')
        SCRATCH.mkdir()
        (SCRATCH / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        (SCRATCH / 'config.json').write_bytes((ROOT / CONFIG).read_bytes())
        (SCRATCH / 'c0.asm').write_bytes(source)
        os.utime(SCRATCH / 'c0.asm', (946684800, 946684800))
        library = parent.retained(latest['rounds'][0]['outputs']['lib'])
        (SCRATCH / 'crt.lib').write_bytes(library)
        response = (b.WORK / 'obj/th03/mainl.@l').read_bytes()
        for old, new in ((b'c0l.obj', rb'probe\af535e\c0l.obj'),
                         (rb'bin\th03\mainl.exe', rb'probe\af535e\mainl.exe'),
                         (rb'obj\th03\mainl.map', rb'probe\af535e\mainl.map'),
                         (b' crt.lib', rb' probe\af535e\crt.lib')):
            need(response.count(old) == 1, 'one scoped link substitution ' + repr(old))
            response = response.replace(old, new)
        (SCRATCH / 'startup.lnk').write_bytes(response)
        record['link_response_sha256'] = sha(response)
        save()
        vectors = []
        for number in (1, 2):
            run(tasm + config['assembler_flags'] + ['c0.ASM,c0l.obj'], SCRATCH,
                f'round{number}-assemble')
            obj = (SCRATCH / 'c0l.obj').read_bytes()
            comparison = compare(original, obj, config)
            run(dos + ['tlink', r'@probe\af535e\startup.lnk'], b.WORK,
                f'round{number}-link')
            vector = dict(startup=obj, exe=(SCRATCH / 'mainl.exe').read_bytes(),
                          map=(SCRATCH / 'mainl.map').read_bytes())
            outputs = {}
            for kind, blob in vector.items():
                path = RAW_PREFIX + f'round{number}.' + ('obj' if kind == 'startup' else kind)
                (ROOT / path).write_bytes(blob)
                outputs[kind] = dict(path=path, bytes=len(blob), sha256=sha(blob))
            # Retain the actual unchanged library pair by reference, rather
            # than representing a copy as fresh TLIB output.
            outputs['lib'] = latest['rounds'][number - 1]['outputs']['lib']
            record['rounds'].append(dict(round=number, outputs=outputs, comparison=comparison))
            save()
            need(vector['exe'] == (b.WORK / 'bin/th03/mainl.target.exe').read_bytes() and
                 vector['map'] == (b.WORK / 'obj/th03/mainl.map').read_bytes(),
                 'complete original decoded Japanese MAINL EXE/MAP equality')
            vectors.append(vector)
            print('Source startup round', number, 'whole EXE/MAP PASS', flush=True)
        need(vectors[0] == vectors[1], 'two byte-identical startup native rounds')
        need(source == (ROOT / config['source']).read_bytes() and
             inputs()[1] == config_hash and library == (SCRATCH / 'crt.lib').read_bytes(),
             'source, original inputs and reused library unchanged during native production')
    record['complete'] = True
    save()


if __name__ == '__main__':
    main()
