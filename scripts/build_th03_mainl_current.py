#!/usr/bin/env python3
"""Rebuild the changed MAINL Staff/root owners without replacing the cold ancestor."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib

import build_th03_mainl_work as cold
from build_th03_mainl_display_work import payload, literal_fields
from build_th03_mainl_resources_work import need, sha
from lib.mainl_owner_migrations import public_offsets
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, read_verified_artifact
from lib.toolchain import attest_surface
from probe_th03_main_bomb_rikako_cpp import segment_definitions

ROOT = cold.ROOT
DRIVER = 'scripts/build_th03_mainl_current.py'
SOURCES = {'rootdata': 'src/mainl/root/complete_data.cpp', 'staffdat': 'src/mainl/staff/data.cpp'}
STAGER = 'scripts/stage_th03_mainl_fullcold.py'
CURRENT_STAGE = 'af1055m'


def paths(stage):
    need(re.fullmatch(r'af[0-9]+m', stage), 'fresh DOS-safe afNNNm stage')
    return cold.WORK / 'probe' / stage, ROOT / f'.analysis/work/mainl-current-{stage}.json'


def source_graph(current=True):
    if current:
        return cold.sources()
    files, _, _, graph, archive = cold.stage.compose_all(current=False)
    for name in (*[n + '.asm' for n in cold.CRT], 'crt_errno.inc', 'dos_error_map.inc'):
        files['owned/' + name] = (ROOT / 'src/mainl/crt' / name).read_bytes()
    return files, graph, archive


def ancestor():
    """Check the retained cold graph as recorded, including its historical C++."""
    raw = (cold.OUT / 'mainl-build.json').read_bytes()
    record = json.loads(raw)
    need(record['complete'] and record['raw_repeat_equal'] and record['retained_project_objects'] == 0,
         'complete unchanged cold ancestor')
    recipe = cold.recipe_inventory()
    need(set(recipe) == set(record['recipe_sha256']), 'cold recipe inventory')
    for name, digest in record['recipe_sha256'].items():
        content = (subprocess.check_output(['git', 'show', cold.stage.FROZEN_CPP_REV + ':' + name], cwd=ROOT)
                   if name == STAGER else (ROOT / name).read_bytes())
        need(sha(content) == digest, 'unchanged cold recipe input: ' + name)
    old, graph, archive = source_graph(False)
    need(record['archive_sha256'] == archive and
         record['source_sha256'] == {n: sha(b) for n, b in sorted(old.items())},
         'complete historical source graph')
    need(all((cold.WORK / n).read_bytes() == b for n, b in old.items()), 'preserved cold source snapshots')
    need([r['round'] for r in record['rounds']] == [1, 2] and
         record['rounds'][0]['outputs'] == record['rounds'][1]['outputs'] and
         len(record['rounds'][0]['outputs']) == 938, 'complete unchanged raw cold pair')
    for name, meta in record['rounds'][0]['outputs'].items():
        data = (cold.WORK / name).read_bytes()
        need(meta == dict(bytes=len(data), sha256=sha(data)), 'retained cold output: ' + name)
    headers = cold.vendor_header_inventory()
    config = tomllib.loads((ROOT / 'config/toolchain.toml').read_text())
    surfaces = [attest_surface(ROOT, s) for s in config['surfaces'] if not s.get('bootstrap_only')]
    need(headers == record['vendor_header_sha256'] and surfaces == record['toolchain_surfaces'] and
         all(s['pass'] or not s['required'] for s in surfaces), 'unchanged consumed native tools and SDK')
    current, now_graph, now_archive = source_graph()
    need(now_graph == graph and now_archive == archive and set(current) == set(old), 'unchanged project graph')
    changed = {n for n in current if current[n] != old[n]}
    need(changed <= {s + '.cpp' for s in SOURCES}, 'only the two independently rebuilt producers may change')
    for stem, source in SOURCES.items():
        need(current[stem + '.cpp'] == (ROOT / source).read_bytes(), 'literal maintained source: ' + stem)
    return record, sha(raw), old, current, graph


def object_scope(raw, original):
    description = describe_omf(raw)
    need(description['valid'] and payload(raw) == payload(original) and
         literal_fields(raw) == literal_fields(original) and
         public_offsets(raw) == public_offsets(original) and
         segment_definitions(raw) == segment_definitions(original),
         'complete native CODE/DATA, ordered FIXUPP, PUBLICs and segment geometry')
    return dict(CODE_bytes=sum(s == 1 for s, _ in payload(raw)),
                DATA_bytes=sum(s == 2 for s, _ in payload(raw)),
                ordered_fields=len(literal_fields(raw)), publics=len(public_offsets(raw)),
                raw_equal_to_cold=raw == original)


def response(files, stage, number):
    raw = files['obj/th03/mainl.@l']
    for stem in SOURCES:
        old = f'obj\\th03\\{stem}.obj'.encode()
        need(raw.count(old) == 1, 'one original physical object slot: ' + stem)
        raw = raw.replace(old, f'probe\\{stage}\\r{number}\\{stem}.obj'.encode())
    for old, new in ((b'bin\\th03\\mainl.exe', f'probe\\{stage}\\r{number}.exe'.encode()),
                     (b'obj\\th03\\mainl.map', f'probe\\{stage}\\r{number}.map'.encode())):
        need(raw.count(old) == 1, 'one normal native output path')
        raw = raw.replace(old, new)
    return raw


def pin(path):
    data = path.read_bytes()
    return dict(path=str(path.relative_to(ROOT)), bytes=len(data), sha256=sha(data))


def checked(meta):
    path = ROOT / meta['path']
    need(not path.is_symlink() and path.resolve().is_relative_to(ROOT), 'retained native evidence path')
    data = path.read_bytes()
    need(meta == pin(path), 'retained native evidence: ' + meta['path'])
    return data


def native_command():
    config = tomllib.loads((ROOT / 'config/toolchain.toml').read_text())
    return [sys.executable, str(ROOT / 'scripts/shared_runtime.py'), 'wine', '--',
            str(ROOT / config['paths']['msdos_player']), '-e', '-x']


def view_links(scratch, parent, files):
    links = {name: scratch / 'src' / name for name in files}
    links.update({name: cold.WORK / name for name in parent['rounds'][0]['outputs']})
    links.update({f'obj/th03/{stem}.obj': scratch / 'r1' / (stem + '.obj') for stem in SOURCES})
    links.update({'bin/th03/mainl.exe': scratch / 'r1.exe',
                  'bin/th03/mainl.target.exe': cold.WORK / 'bin/th03/mainl.target.exe',
                  'bin/th03/mainl.packed.exe': cold.WORK / 'bin/th03/mainl.packed.exe',
                  'obj/th03/mainl.map': scratch / 'r1.map', 'probe': cold.WORK / 'probe'})
    return links


def build(stage):
    scratch, report_path = paths(stage)
    parent, parent_sha, old, files, graph = ancestor()
    need(not scratch.exists() and not report_path.exists(), 'unused native stage; preserve all earlier evidence')
    config = tomllib.loads((ROOT / 'config/toolchain.toml').read_text())
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
               WINEPREFIX=str(ROOT / config['paths']['wine_prefix']), MSDOS_PATH=r'C:\TC4\BIN',
               TZ='UTC', LANG='C', LC_ALL='C')
    dos = native_command()
    record = dict(complete=False, stage=stage, cold_report_sha256=parent_sha,
                  recipe_sha256=cold.recipe_inventory(), driver_sha256=sha((ROOT / DRIVER).read_bytes()),
                  source_sha256={n: sha(b) for n, b in sorted(files.items())},
                  maintained_source_sha256={n: sha((ROOT / n).read_bytes()) for n in SOURCES.values()},
                  cold_rebuilt=False, objects_rebuilt_per_round=2, retained_project_objects=34,
                  phases=[], rounds=[])
    def save():
        report_path.write_text(json.dumps(record, indent=2) + '\n')
    def run(args, cwd, label):
        result = subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=105)
        log = scratch / (label + '.log')
        log.write_bytes(result.stdout)
        record['phases'].append(dict(label=label, argv=args, cwd=str(cwd.relative_to(ROOT)),
                                     returncode=result.returncode, log=pin(log)))
        save()
        need(result.returncode == 0, label + ': ' + result.stdout.decode(errors='replace')[-1300:])
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        scratch.mkdir()
        snapshot = scratch / 'src'
        snapshot.mkdir()
        for name, data in files.items():
            path = snapshot / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            os.utime(path, ns=(cold.stage.base.STAMP, cold.stage.base.STAMP))
        (scratch / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        save()
        for number in (1, 2):
            folder = scratch / f'r{number}'
            folder.mkdir()
            scopes = {}
            for stem in SOURCES:
                row, = [g for g in graph if g['output'] == f'obj/th03/{stem}.obj']
                flags = [flag for flag in row['flags'] if not flag.startswith('-n')]
                run(dos + ['tcc', *flags, f'-n..\\r{number}\\', row['wrapper']], snapshot,
                    f'round{number}-{stem}-TC4')
                raw = (folder / (stem + '.obj')).read_bytes()
                scopes[stem] = object_scope(raw, (cold.WORK / row['output']).read_bytes())
            link = response(files, stage, number)
            (scratch / f'r{number}.lnk').write_bytes(link)
            run(dos + ['tlink', f'@probe\\{stage}\\r{number}.lnk'], cold.WORK, f'round{number}-TLINK')
            exe, mapped = scratch / f'r{number}.exe', scratch / f'r{number}.map'
            need(exe.read_bytes() == (cold.WORK / 'bin/th03/mainl.target.exe').read_bytes() and
                 mapped.read_bytes() == (cold.WORK / 'obj/th03/mainl.map').read_bytes(),
                 'complete original decoded EXE, ordered relocations and original MAP')
            outputs = {stem: pin(folder / (stem + '.obj')) for stem in SOURCES}
            outputs.update(exe=pin(exe), map=pin(mapped))
            record['rounds'].append(dict(round=number, outputs=outputs, scopes=scopes,
                                         response_sha256=sha(link)))
            save()
            print(f'Current MAINL round {number}: two complete physical owners and original EXE/MAP equal', flush=True)
        # A read-only namespace lets existing layout reviewers inspect the two
        # current objects alongside unchanged ancestors, without replacing any
        # original cold input or output. Compiler inputs live separately in src/.
        view = scratch / 'view'
        view.mkdir()
        for name, target in view_links(scratch, parent, files).items():
            dest = view / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.symlink_to(target)
    record['complete'] = True
    save()
    return review(stage)


def review(stage):
    scratch, report_path = paths(stage)
    parent, parent_sha, old, files, graph = ancestor()
    record = json.loads(report_path.read_bytes())
    need(record['complete'] and record['stage'] == stage and
         record['cold_report_sha256'] == parent_sha and
         record['recipe_sha256'] == cold.recipe_inventory() and
         record['driver_sha256'] == sha((ROOT / DRIVER).read_bytes()) and
         (scratch / 'driver.py').read_bytes() == (ROOT / DRIVER).read_bytes() and
         record['source_sha256'] == {n: sha(b) for n, b in sorted(files.items())} and
         record['maintained_source_sha256'] == {n: sha((ROOT / n).read_bytes()) for n in SOURCES.values()},
         'complete current source-bound native refresh')
    need(all((scratch / 'src' / n).read_bytes() == b for n, b in files.items()), 'complete actual consumed source snapshot')
    for name, target_path in view_links(scratch, parent, files).items():
        link = scratch / 'view' / name
        need(link.is_symlink() and link.readlink() == target_path,
             'read-only current native namespace: ' + name)
    target = (cold.WORK / 'bin/th03/mainl.target.exe').read_bytes()
    diet = tomllib.loads((ROOT / 'config/th03_diet.toml').read_text())
    declaration, = [a for a in diet['artifacts'] if a['id'] == 'th03-mainl']
    stored = read_verified_artifact(ROOT, find_artifact(tomllib.loads((ROOT / 'config/targets.toml').read_text()), 'th03-mainl'))
    need(sha(target) == declaration['decoded_sha256'] and len(target) == declaration['decoded_size'] and
         (cold.WORK / 'bin/th03/mainl.packed.exe').read_bytes() == stored, 'pinned Japanese decoded/stored identities')
    need([p['label'] for p in record['phases']] == [f'round{n}-{step}' for n in (1, 2)
         for step in ('rootdata-TC4', 'staffdat-TC4', 'TLINK')] and
         all(p['returncode'] == 0 and checked(p['log']) is not None for p in record['phases']),
         'six actual original compiler/linker phase logs')
    expected_phases = []
    for number in (1, 2):
        for stem in SOURCES:
            producer, = [g for g in graph if g['output'] == f'obj/th03/{stem}.obj']
            flags = [flag for flag in producer['flags'] if not flag.startswith('-n')]
            expected_phases.append((native_command() + ['tcc', *flags, f'-n..\\r{number}\\', producer['wrapper']],
                                    str((scratch / 'src').relative_to(ROOT))))
        expected_phases.append((native_command() + ['tlink', f'@probe\\{stage}\\r{number}.lnk'],
                                str(cold.WORK.relative_to(ROOT))))
    need([(p['argv'], p['cwd']) for p in record['phases']] == expected_phases,
         'literal original compiler flags, consumed source names, output paths and normal linker commands')
    vectors = []
    for number, row in enumerate(record['rounds'], 1):
        need(row['round'] == number and set(row['outputs']) == set(SOURCES) | {'exe', 'map'} and
             (scratch / f'r{number}.lnk').read_bytes() == response(files, stage, number) and
             row['response_sha256'] == sha(response(files, stage, number)), 'literal original native link order')
        raw = {name: checked(meta) for name, meta in row['outputs'].items()}
        for stem in SOURCES:
            need(raw[stem] == (scratch / f'r{number}' / (stem + '.obj')).read_bytes() and
                 row['scopes'][stem] == object_scope(raw[stem], (cold.WORK / f'obj/th03/{stem}.obj').read_bytes()),
                 'complete source-native physical owner')
            cold.verify_vendor_dependencies(describe_omf(raw[stem]), parent['vendor_header_sha256'])
            for dependency in describe_omf(raw[stem])['dependency_paths']:
                name = dependency.replace(chr(92), '/')
                while '//' in name:
                    name = name.replace('//', '/')
                if name.startswith('C:/TC4/INCLUDE/'):
                    need(name in parent['vendor_header_sha256'], 'complete consumed SDK dependency: ' + name)
                else:
                    need(name in files and (scratch / 'src' / name).read_bytes() == files[name],
                         'complete actual compiler-consumed source/header: ' + name)
        need(raw['exe'] == target and raw['map'] == (cold.WORK / 'obj/th03/mainl.map').read_bytes() and
             parse_mz(raw['exe']).relocations == parse_mz(target).relocations and
             len(parse_mz(target).relocations) == 677, 'complete original MAINL EXE/MAP and 677 ordered MZ entries')
        vectors.append(raw)
    need(len(vectors) == 2 and vectors[0] == vectors[1], 'two complete raw OBJ/EXE/MAP rounds repeat')
    return dict(complete=True, stage=stage, report_sha256=sha(report_path.read_bytes()),
                cold_report_sha256=parent_sha, current_source_inventory_sha256=record['source_sha256'],
                scopes=record['rounds'][0]['scopes'], full_original_EXE_MAP_equal=True,
                current_work=str((scratch / 'view').relative_to(ROOT)), cold_rebuilt=False, rounds=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', required=True)
    parser.add_argument('--build', action='store_true', help='compile two physical owners in a fresh stage')
    args = parser.parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    result = build(args.stage) if args.build else review(args.stage)
    print(json.dumps({k: v for k, v in result.items() if k != 'current_source_inventory_sha256'}, indent=2))


if __name__ == '__main__':
    main()
