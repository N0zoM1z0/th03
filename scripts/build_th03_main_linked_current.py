#!/usr/bin/env python3
"""Compose the 97 selected current MAIN objects in the original link order.

Reuse both independently compiled, source-reviewed native rounds. Keep the
deferred historical input_s carrier and original compiler startup/libraries.
"""
import argparse
import fcntl
import json
import os
import re
import subprocess

from status import native_source_reviews
from probe_th03_main_exatt_layout import ROOT, WORK, parent, need, sha
from build_th03_mainl_current import native_command, pin, checked
from lib.main_mz_compact import compact_mz
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

DRIVER = 'scripts/build_th03_main_linked_current.py'


def paths(stage):
    need(re.fullmatch(r'af[0-9]+[a-z]', stage), 'DOS-safe native stage')
    folder = WORK / 'probe' / stage
    return folder, folder / 'linked-build.json'


def composition(stage, n, selected):
    original = parent.response(n)
    tokens = re.findall(rb'[^\s,]+', original)
    prior = json.loads((ROOT / parent.REPORT).read_bytes())
    base_map = parent.read_pin(prior['rounds'][n-1]['outputs']['map']).splitlines(keepends=True)
    replacements, map_changes = {}, {}
    for scope in selected:
        report = json.loads((ROOT / scope['report']).read_bytes())
        row = report['rounds'][n-1]
        location = WORK / 'probe' / scope['stage']
        response = (location / f'r{n}.@l').read_bytes()
        need(sha(response) == row['response_sha256'], 'reviewed native response')
        alternate = re.findall(rb'[^\s,]+', response)
        need(len(tokens) == len(alternate), 'unchanged original link slots')
        objects = []
        for i, (old, new) in enumerate(zip(tokens, alternate)):
            if old == new:
                continue
            if old.lower().endswith(b'.obj'):
                need(i not in replacements and new.lower().endswith(b'.obj'), 'disjoint physical owners')
                replacements[i] = new
                objects.append((WORK / new.decode().replace('\\', '/')).read_bytes())
            else:
                need(old.lower().endswith((b'.exe', b'.map')), 'only native output slots may also change')
        if 'units' in report:
            expected_objects = [checked(row['outputs'][u + '_obj']) for u in report['units']]
            map_raw = checked(row['outputs']['map'])
        else:
            expected_objects = row['objects_sha256'].values()
            need(sorted(sha(o) for o in objects) == sorted(expected_objects), 'reviewed ASM objects')
            expected_objects = objects
            map_raw = (location / f'r{n}.map').read_bytes()
            need(sha(map_raw) == row['normal_map_sha256'], 'reviewed native MAP')
        need(sorted(sha(o) for o in objects) == sorted(sha(o) for o in expected_objects) and
             len(objects) == scope['modules'], 'complete reviewed object selection')
        candidate = map_raw.splitlines(keepends=True)
        need(len(candidate) == len(base_map), 'complete original MAP row inventory')
        for i, (old, new) in enumerate(zip(base_map, candidate)):
            if old != new:
                need(i not in map_changes, 'disjoint reviewed MAP changes')
                map_changes[i] = new
    retained = [t for i, t in enumerate(tokens) if t.lower().endswith(b'.obj') and i not in replacements]
    need(len(replacements) == 97 and retained == [b'c0l.obj', f'probe\\af567c\\r{n}-input_s.obj'.encode()],
         '97 current objects; only original startup and deferred input carrier retained')
    response = original
    for i, new in replacements.items():
        need(response.count(tokens[i]) == 1, 'one original physical input slot')
        response = response.replace(tokens[i], new)
    for ext in ('exe', 'map'):
        response = response.replace(f'probe\\{parent.STAGE}\\r{n}.{ext}'.encode(),
                                    f'probe\\{stage}\\r{n}.{ext}'.encode())
    for name in ('c0l.obj', 'emu.lib', 'mathl.lib', 'cl.lib'):
        need(response.count(name.encode()) == 1, 'one compiler startup/library slot')
        response = response.replace(name.encode(), ('C:\\TC4\\LIB\\' + name).encode())
    inputs = {str((WORK / t.decode().replace('\\', '/')).relative_to(ROOT)):
              sha((WORK / t.decode().replace('\\', '/')).read_bytes())
              for i, t in enumerate(tokens) if t.lower().endswith(b'.obj') and t != b'c0l.obj'
              for t in [replacements.get(i, t)]}
    for name in ('c0l.obj', 'emu.lib', 'mathl.lib', 'cl.lib'):
        path = ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB' / name.upper()
        inputs[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    return response, b''.join(map_changes.get(i, line) for i, line in enumerate(base_map)), inputs


def selection():
    selected = native_source_reviews(ROOT, 'th03-main')
    need(len(selected) == 76 and all(r['verified'] for r in selected), 'all current source-owner reviews pass')
    return selected


def target_bytes():
    return read_verified_artifact(ROOT, find_artifact(load_target_manifest(ROOT / 'config/targets.toml'), 'th03-main'))


def review(stage, selected=None):
    folder, path = paths(stage)
    selected = selection() if selected is None else selected
    record = json.loads(path.read_bytes())
    need(record['complete'] and record['stage'] == stage and record['selection'] == selected and
         record['driver_sha256'] == sha((ROOT / DRIVER).read_bytes()), 'current driver and source evidence')
    target = target_bytes()
    executables = []
    need(len(record['rounds']) == 2, 'two independent source-object rounds')
    for n, row in enumerate(record['rounds'], 1):
        response, expected_map, inputs = composition(stage, n, selected)
        need(row['number'] == n and row['inputs'] == inputs and
             row['response'] == pin(folder / f'r{n}.@l') and checked(row['response']) == response and
             row['argv'] == native_command() + ['tlink', f'@probe\\{stage}\\r{n}.@l'] and
             row['returncode'] == 0, 'actual original-order native inputs and command')
        checked(row['log'])
        exe, table = checked(row['exe']), checked(row['map'])
        need(row['exe'] == pin(folder / f'r{n}.exe') and row['map'] == pin(folder / f'r{n}.map') and
             table == expected_map and compact_mz(exe) == target, 'complete target and composed original MAP')
        mz, reference = parse_mz(exe), parse_mz(target)
        need(mz.program_image == reference.program_image and mz.relocations == reference.relocations,
             'complete loaded image and literal ordered MZ relocations')
        executables.append(exe)
    need(executables[0] == executables[1], 'raw normal MAIN links repeat')
    return dict(stage=stage, current_source_objects=97, native_rounds=2, full_Japanese_MAIN_equal=True,
                full_composed_MAP_equal=True, ordered_MZ_relocations=len(reference.relocations),
                stored_target_bytes=len(target), normal_link_bytes=len(exe),
                input_s='retained historical 418-byte carrier; original 417-byte discrepancy deferred',
                project_recompiled=False, whole_product_source_accepted=False,
                report=str(path.relative_to(ROOT)), report_sha256=sha(path.read_bytes()))


def build(stage):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    folder, path = paths(stage)
    need(not folder.exists(), 'fresh native stage')
    selected = selection()
    record = dict(complete=False, stage=stage, selection=selected,
                  driver_sha256=sha((ROOT / DRIVER).read_bytes()), rounds=[])
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        folder.mkdir()
        for n in (1, 2):
            response, expected_map, inputs = composition(stage, n, selected)
            rsp = folder / f'r{n}.@l'
            rsp.write_bytes(response)
            argv = native_command() + ['tlink', f'@probe\\{stage}\\r{n}.@l']
            run = subprocess.run(argv, cwd=WORK, env=env, capture_output=True, timeout=120)
            log = folder / f'r{n}.log'
            log.write_bytes(run.stdout + run.stderr)
            need(run.returncode == 0, 'native TLINK: ' + log.read_text(errors='replace')[-1800:])
            record['rounds'].append(dict(number=n, inputs=inputs, argv=argv, returncode=run.returncode,
                log=pin(log), response=pin(rsp), exe=pin(folder / f'r{n}.exe'), map=pin(folder / f'r{n}.map')))
            path.write_text(json.dumps(record, indent=2) + '\n')
        record['complete'] = True
        path.write_text(json.dumps(record, indent=2) + '\n')
    return review(stage, selected)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', required=True)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    print(json.dumps(build(args.stage) if args.build else review(args.stage), sort_keys=True))
