#!/usr/bin/env python3
"""Build all 36 current MAINL project objects with the recovered xx library member.

The unchanged, reviewed 28 source CRT providers and other library members are
reused. The frozen cold worktree and its receipts are never overwritten.
"""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import build_th03_mainl_current as current
from build_th03_mainl_exception_work import compiler_context
from build_th03_mainl_xx_work import (
    ASM_FLAGS, OBJECT_FLAGS, SOURCES, BASE_BUILD, retained_pair,
)
from probe_th03_mainl_xx_rtti import wrapper
from lib.borland_library import library_members, compare_members, object_program_records
from lib.pc98 import parse_mz

ROOT = current.ROOT
DRIVER = 'scripts/build_th03_mainl_linked_current.py'
SUPPORT = (
    'scripts/build_th03_mainl_current.py',
    'scripts/build_th03_mainl_xx_work.py',
    'scripts/probe_th03_mainl_xx_dispatch.py',
    'scripts/probe_th03_mainl_xx_rtti.py',
    'scripts/build_th03_mainl_exception_work.py',
)
need, sha = current.need, current.sha


def paths(stage):
    need(re.fullmatch(r'af[0-9]+[a-z]', stage) is not None, 'fresh DOS-safe stage')
    scratch = current.cold.WORK / 'probe' / stage
    return scratch, scratch / 'linked-build.json'


def context():
    cold, cold_sha, old, files, graph = current.ancestor()
    base, vector, base_sha = retained_pair(ROOT, BASE_BUILD, 'exception-native')
    need(vector['exe'] == (current.cold.WORK / 'bin/th03/mainl.target.exe').read_bytes()
         and vector['map'] == (current.cold.WORK / 'obj/th03/mainl.map').read_bytes(),
         'unchanged target-equal 28-provider library link')
    sources = {name: wrapper(b'') if name == 'xx.cpp' else (ROOT / source).read_bytes()
               for name, source in SOURCES.items()}
    return cold_sha, files, graph, base_sha, vector['lib'], sources


def input_pins(files, sources):
    return dict(project={n: sha(b) for n, b in sorted(files.items())},
                xx={n: sha(b) for n, b in sorted(sources.items())},
                support={n: sha((ROOT / n).read_bytes()) for n in (DRIVER, *SUPPORT)},
                compiler=compiler_context(ROOT), sdk=current.cold.vendor_header_inventory())


def pin(path):
    return current.pin(path)


def tasm_command():
    return [sys.executable, str(ROOT / 'scripts/shared_runtime.py'), 'wine', '--',
            str(ROOT / '.analysis/toolchain/wineprefix/drive_c/TASM50/bin/TASM32.EXE')]


def project_command(row):
    if row['kind'] == 'tasm':
        return tasm_command() + row['flags'] + [row['wrapper'].replace('/', '\\'),
                                               row['output'].replace('/', '\\')]
    need(row['kind'] == 'tcc', 'known native producer')
    return current.native_command() + ['tcc', *row['flags'], row['wrapper']]


def link_response(files):
    link = files['obj/th03/mainl.@l']
    for before, after in [(b' crt.lib', b' linked.lib'), (b'c0l.obj', br'C:\TC4\LIB\C0L.OBJ'),
                          (b'emu.lib', br'C:\TC4\LIB\EMU.LIB'),
                          (b'mathl.lib', br'C:\TC4\LIB\MATHL.LIB')]:
        need(link.count(before) == 1, 'one original library/startup slot')
        link = link.replace(before, after)
    return link


def build(stage):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    scratch, report_path = paths(stage)
    need(not scratch.exists(), 'unused native stage')
    cold_sha, files, graph, base_sha, library, sources = context()
    members = library_members(library)
    need(len(members) == 893, 'complete original library order')
    inputs = input_pins(files, sources)
    original_xx = (current.cold.WORK / 'vendor/xx.obj').read_bytes()
    record = dict(complete=False, stage=stage, inputs=inputs,
                  cold_report_sha256=cold_sha, library_report_sha256=base_sha,
                  retained_library_sha256=sha(library), rounds=[], phases=[])
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
               MSDOS_PATH=r'C:\BC45;C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos = current.native_command()

    def save():
        report_path.write_text(json.dumps(record, indent=2) + '\n')

    def run(argv, cwd, label):
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=120)
        log = scratch / (label + '.log')
        log.write_bytes(result.stdout)
        record['phases'].append(dict(label=label, argv=argv, cwd=str(cwd.relative_to(ROOT)),
                                     returncode=result.returncode, log=pin(log)))
        save()
        need(result.returncode == 0, label + ': ' + result.stdout.decode(errors='replace')[-1800:])

    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scratch.mkdir()
        extracted = scratch / 'members'
        extracted.mkdir()
        (extracted / 'base.lib').write_bytes(library)
        (extracted / 'extract.rsp').write_bytes(current.cold.response(
            'base.lib', ['*' + m.name for m in members]))
        run(dos + ['tlib', '@extract.rsp'], extracted, 'extract-library')
        found = {p.stem.casefold(): p for p in extracted.glob('*') if p.suffix.lower() == '.obj'}
        need(set(found) == {m.name.casefold() for m in members}, 'all native extracted members')
        for m in members:
            path = found[m.name.casefold()]
            need(object_program_records(path.read_bytes()) == m.program_records,
                 'unchanged extracted library member: ' + m.name)
            destination = extracted / (m.name + '.obj')
            if path != destination:
                path.rename(destination)
        save()
        for number in (1, 2):
            folder = scratch / f'r{number}'
            folder.mkdir()
            for name, data in files.items():
                path = folder / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
                os.utime(path, ns=(current.cold.stage.base.STAMP, current.cold.stage.base.STAMP))
            for name in ('obj/th01', 'obj/th02', 'obj/th03', 'bin/th03', 'xx'):
                (folder / name).mkdir(parents=True, exist_ok=True)
            outputs, scopes = {}, {}
            for row in graph:
                output = row['output']
                run(project_command(row), folder, f'r{number}-' + Path(output).stem)
                raw = (folder / output).read_bytes()
                scopes[output] = current.object_scope(raw, (current.cold.WORK / output).read_bytes())
                outputs[output] = pin(folder / output)
            for name, data in sources.items():
                path = folder / 'xx' / name
                path.write_bytes(data)
                os.utime(path, (946684800, 946684800))
            for label, flags in (('xx-asm', ASM_FLAGS), ('xx-object', OBJECT_FLAGS)):
                run(dos + [r'C:\BC45\BCC.EXE', *flags, 'xx.cpp'], folder / 'xx', f'r{number}-' + label)
            scopes['xx'] = current.object_scope((folder / 'xx/xx.obj').read_bytes(), original_xx)
            additions = ['+' + (r'xx\xx.obj' if m.name == 'xx' else '..\\members\\' + m.name + '.obj')
                         for m in members]
            (folder / 'library.rsp').write_bytes(current.cold.response('linked.lib /E', additions))
            run(dos + ['tlib', '@library.rsp'], folder, f'r{number}-library')
            library_review = compare_members(members, library_members((folder / 'linked.lib').read_bytes()),
                                             {'xx': (folder / 'xx/xx.obj').read_bytes()})
            (folder / 'link.lnk').write_bytes(link_response(files))
            run(dos + ['tlink', '@link.lnk'], folder, f'r{number}-link')
            for name in ('xx/xx.asm', 'xx/xx.obj', 'linked.lib', 'bin/th03/mainl.exe', 'obj/th03/mainl.map'):
                outputs[name] = pin(folder / name)
            need((folder / 'bin/th03/mainl.exe').read_bytes() ==
                 (current.cold.WORK / 'bin/th03/mainl.target.exe').read_bytes(), 'complete decoded Japanese target')
            need((folder / 'obj/th03/mainl.map').read_bytes() ==
                 (current.cold.WORK / 'obj/th03/mainl.map').read_bytes(), 'complete original MAINL MAP')
            record['rounds'].append(dict(number=number, outputs=outputs, scopes=scopes,
                                         library=library_review, response=pin(folder / 'link.lnk')))
            save()
            print(f'MAINL round {number}: all 36 current project objects + source xx; complete EXE/MAP equal', flush=True)
        record['complete'] = True
        save()
    return review(stage)


def review(stage):
    scratch, report_path = paths(stage)
    cold_sha, files, graph, base_sha, library, sources = context()
    record = json.loads(report_path.read_bytes())
    need(record['complete'] and record['stage'] == stage and
         record['inputs'] == input_pins(files, sources) and
         record['cold_report_sha256'] == cold_sha and record['library_report_sha256'] == base_sha and
         record['retained_library_sha256'] == sha(library), 'current source/tool/baseline bindings')
    dos = current.native_command()
    expected = [('extract-library', dos + ['tlib', '@extract.rsp'], scratch / 'members')]
    for n in (1, 2):
        folder = scratch / f'r{n}'
        expected += [(f'r{n}-' + Path(g['output']).stem, project_command(g), folder) for g in graph]
        expected += [(f'r{n}-' + label, dos + [r'C:\BC45\BCC.EXE', *flags, 'xx.cpp'], folder / 'xx')
                     for label, flags in [('xx-asm', ASM_FLAGS), ('xx-object', OBJECT_FLAGS)]]
        expected += [(f'r{n}-library', dos + ['tlib', '@library.rsp'], folder),
                     (f'r{n}-link', dos + ['tlink', '@link.lnk'], folder)]
    need([(p['label'], p['argv'], p['cwd']) for p in record['phases']] ==
         [(label, argv, str(cwd.relative_to(ROOT))) for label, argv, cwd in expected] and
         all(p['returncode'] == 0 and current.checked(p['log']) is not None for p in record['phases']),
         'complete successful serial native schedule')
    vectors = []
    for n, row in enumerate(record['rounds'], 1):
        need(row['number'] == n, 'independent native round order')
        folder = scratch / f'r{n}'
        need(all((folder / name).read_bytes() == data for name, data in files.items()) and
             all((folder / 'xx' / name).read_bytes() == data for name, data in sources.items()),
             'actual compiled source snapshots')
        need(all(meta == pin(folder / name) for name, meta in row['outputs'].items()),
             'outputs belong to the recorded native round')
        vector = {name: current.checked(meta) for name, meta in row['outputs'].items()}
        need(set(vector) == {g['output'] for g in graph} |
             {'xx/xx.asm', 'xx/xx.obj', 'linked.lib', 'bin/th03/mainl.exe', 'obj/th03/mainl.map'},
             'complete project/library/link output vector')
        scopes = {g['output']: current.object_scope(vector[g['output']], (current.cold.WORK / g['output']).read_bytes())
                  for g in graph}
        scopes['xx'] = current.object_scope(vector['xx/xx.obj'], (current.cold.WORK / 'vendor/xx.obj').read_bytes())
        need(row['scopes'] == scopes and row['library'] == compare_members(
            library_members(library), library_members(vector['linked.lib']), {'xx': vector['xx/xx.obj']}),
            'entire native owners, literal ordered fields and library order')
        need(row['response'] == pin(folder / 'link.lnk') and
             current.checked(row['response']) == link_response(files), 'original ordered native linker response')
        target = (current.cold.WORK / 'bin/th03/mainl.target.exe').read_bytes()
        need(vector['bin/th03/mainl.exe'] == target and vector['obj/th03/mainl.map'] ==
             (current.cold.WORK / 'obj/th03/mainl.map').read_bytes(), 'complete EXE/MAP and ordered relocations')
        vectors.append(vector)
    need(len(vectors) == 2 and vectors[0] == vectors[1], 'complete raw native output repetition')
    return dict(stage=stage, complete=True, project_objects_per_round=36,
                source_CRT_providers=29, fresh_xx_CODE_bytes=12622,
                fresh_xx_DATA_bytes=18, ordered_xx_fields=187,
                decoded_bytes=len(target), ordered_MZ_relocations=len(parse_mz(target).relocations),
                full_EXE_MAP_equal=True, raw_repeat_equal=True,
                report_sha256=sha(report_path.read_bytes()), work=str((scratch / 'r1').relative_to(ROOT)),
                product_source_accepted=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', required=True)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    print(json.dumps(build(args.stage) if args.build else review(args.stage), sort_keys=True))
