#!/usr/bin/env python3
"""Restore real exec LIDATA/frames and prove shared runtime in MAINL and OP."""
import collections
import fcntl
import json
import os
import re
import subprocess
import tomllib
from pathlib import Path

import build_th03_mainl_after536_work as parent
import review_th03_mainl_after536_work as parent_review
import build_th03_op_work as op
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members, compare_members, object_program_records
from lib.targets import find_artifact, read_verified_artifact
from lib.toolchain import attest_surface

ROOT = parent.ROOT
b = parent.b
DRIVER = 'scripts/build_th03_runtime_after537_work.py'
CONFIG = 'config/th03_runtime_after537.json'
PREFIX = '.analysis/work/runtime-after537-'
REPORT = PREFIX + 'build.json'
SCRATCH = b.WORK / 'probe/af537d'
OP_SCRATCH = op.WORK / 'probe/af537d'
MAP_ROW = re.compile(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+([0-9A-F]+) C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(\S+)\s+ACBP=([0-9A-F]{2})\s*$')


def load(path):
    raw = (ROOT / path).read_bytes()
    return json.loads(raw), sha(raw)


def checked(meta):
    raw = (ROOT / meta['path']).read_bytes()
    need(meta == dict(path=meta['path'], bytes=len(raw), sha256=sha(raw)), 'raw retained ' + meta['path'])
    return raw


def op_context():
    record, digest = load('.analysis/work/op-build.json')
    files = op.source_graph()
    need(record['complete'] and record['raw_repeat_equal'] and record['retained_project_objects'] == 0 and
         record['recipe_sha256'] == op.recipe_inventory() and len(files) == 330 and
         record['source_sha256'] == {n: sha(v) for n, v in sorted(files.items())} and
         all((op.WORK / n).read_bytes() == v for n, v in files.items()), 'current OP source-only cold context')
    need(len(record['rounds']) == 2 and [q['round'] for q in record['rounds']] == [1, 2] and
         record['rounds'][0]['outputs'] == record['rounds'][1]['outputs'] and
         set(record['rounds'][0]['outputs']) == {p['output'] for p in op.producers(files)} |
         {'bin/th03/op.exe', 'obj/th03/op.map'}, 'complete retained OP thirty-object pair inventories')
    for name, meta in record['rounds'][0]['outputs'].items():
        raw = (op.WORK / name).read_bytes()
        need(meta == dict(bytes=len(raw), sha256=sha(raw)), 'unchanged OP cold output ' + name)
    tools = tomllib.loads((ROOT / 'config/toolchain.toml').read_text())
    need(record['toolchain_surfaces'] == [attest_surface(ROOT, s) for s in tools['surfaces']
                                        if not s.get('bootstrap_only')], 'same attested OP native tools')
    diet = tomllib.loads((ROOT / 'config/th03_diet.toml').read_text())
    declaration, = [q for q in diet['artifacts'] if q['id'] == 'th03-op']
    decoded = (op.WORK / 'bin/th03/op.target.exe').read_bytes()
    need(len(decoded) == declaration['decoded_size'] and sha(decoded) == declaration['decoded_sha256'] and
         decoded == (op.WORK / 'bin/th03/op.exe').read_bytes(), 'pinned decoded Japanese OP identity')
    targets = tomllib.loads((ROOT / 'config/targets.toml').read_text())
    stored = read_verified_artifact(ROOT, find_artifact(targets, 'th03-op'))
    need((op.WORK / 'bin/th03/op.packed.exe').read_bytes() == stored and
         record['packing']['stored_equal'] and record['packing']['raw_repeat_equal'], 'unchanged packed OP cold bridge')
    return dict(receipt_sha256=digest, recipe_sha256=record['recipe_sha256'],
        source_sha256=record['source_sha256'], outputs=record['rounds'][0]['outputs'],
        source_files=330, retained_game_objects=30, historical_raw_storage='one vector; equal two-round inventories'), files, stored


def exec_scope(original, native, config):
    aa, zz = b.segment_definitions(original), b.segment_definitions(native)
    x, y = b.initialized_payload(original), b.initialized_payload(native)
    fields = b.literal_fields(original)
    need(aa == zz and x == y and len(y) == config['exec_initialized_CODE_bytes'] and
         aa[0]['size'] == config['exec_CODE_extent'] and
         [i for i in range(aa[0]['size']) if (1, i) not in x] == config['exec_uninitialized_sites'] and
         len(fields) == config['exec_literal_fields'] and fields == b.literal_fields(native),
         'complete original initialized storage, true holes and all 21 literal ordered fields')
    records = {}
    for name in ('SEGDEF', 'GRPDEF', 'EXTDEF', 'PUBDEF', 'MODEND'):
        a = [r.data.hex() for r in b.parse_omf(original) if r.name == name]
        z = [r.data.hex() for r in b.parse_omf(native) if r.name == name]
        need(a == z, 'literal original exec ' + name)
        records[name] = a
    return dict(segments=aa, initialized_bytes=len(y), uninitialized_CODE_sites=[356, 357],
        initialized_sha256=sha(bytes(v for _, v in sorted(y.items()))), literal_fields=fields,
        literal_records=records, original_program_identity=object_program_records(original) == object_program_records(native))


def map_rows(raw):
    rows = []
    for line in raw.decode().splitlines():
        m = MAP_ROW.match(line)
        if m:
            seg, off, size, cls, name, group, module, attrs = m.groups()
            rows.append(dict(segment=int(seg, 16), offset=int(off, 16), size=int(size, 16),
                segment_class=cls, name=name, group=group, module=module, attributes=int(attrs, 16)))
    need(rows, 'actual complete detailed MAP rows')
    return rows


def op_map_review(baseline, candidate):
    added = b' 0D7F:2502 0000 C=BSS    S=_BSS           G=DGROUP  M=fbrk       ACBP=48\r\n'
    anchor = b' 0D7F:2502 0004 C=BSS    S=_BSS           G=DGROUP  M=signal     ACBP=48\r\n'
    removed = b' 0D7F:2510 0000 C=BSS    S=_BSS           G=DGROUP  M=setblock   ACBP=48\r\n'
    need(added not in baseline and baseline.count(anchor) == baseline.count(removed) == 1,
         'unique historical OP zero-extent BSS ownership rows')
    expected = baseline.replace(anchor, added + anchor, 1).replace(removed, b'', 1)
    need(candidate == expected and len(candidate) == len(baseline),
         'complete OP MAP has exactly the two explicitly reviewed zero-extent row differences')
    return dict(raw_equal=False, old_sha256=sha(baseline), new_sha256=sha(candidate), bytes=len(candidate),
        added_zero_BSS_owner='fbrk at 0D7F:2502', omitted_zero_BSS_owner='setblock at 0D7F:2510',
        all_material_rows_and_other_bytes_equal=True)


def material_scope(map_blob, original_members, source_members):
    rows = map_rows(map_blob)
    names = {q['module'].casefold() for q in rows}
    profiles, totals, selected = [], collections.Counter(), []
    for slot, (a, z) in enumerate(zip(original_members, source_members)):
        need(a.name == z.name, 'original ordered runtime slots')
        if a.name.casefold() not in names:
            continue
        selected.append(dict(slot=slot, name=a.name))
        original, source = map(b.original_library_member, (a, z))
        ss, tt = b.segment_definitions(original), b.segment_definitions(source)
        x, y = b.initialized_payload(original), b.initialized_payload(source)
        attrs = [r.data[0] for r in b.parse_omf(original) if r.name == 'SEGDEF']
        native_attrs = [r.data[0] for r in b.parse_omf(source) if r.name == 'SEGDEF']
        for s in ss:
            if not s['size']:
                continue
            t, = [q for q in tt if q['name'] == s['name'] and q['class'] == s['class']]
            p = {i: x[s['index'], i] for i in range(s['size']) if (s['index'], i) in x}
            q = {i: y[t['index'], i] for i in range(t['size']) if (t['index'], i) in y}
            need(s['size'] == t['size'] and p == q and attrs[s['index'] - 1] == native_attrs[t['index'] - 1],
                 'all original selected initialized/uninitialized storage and segment flags ' + a.name)
            mapped, = [r for r in rows if r['module'].casefold() == a.name.casefold() and
                       r['name'] == s['name'] and r['segment_class'] == s['class'] and r['size']]
            need(mapped['size'] == s['size'] and mapped['attributes'] == attrs[s['index'] - 1],
                 'complete selected object-to-MAP material ownership')
            totals[s['class'] + '_extent'] += s['size']
            totals[s['class'] + '_initialized'] += len(p)
            totals[s['class'] + '_uninitialized'] += s['size'] - len(p)
            profiles.append(dict(member=a.name, slot=slot, segment=s['name'], segment_class=s['class'],
                bytes=s['size'], initialized_bytes=len(p), initialized_sha256=sha(bytes(p.values())),
                uninitialized_sites=[i for i in range(s['size']) if i not in p], mapping=mapped))
    return dict(selected_members=selected, totals=dict(totals), material_segments=profiles)


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    config, config_hash = load(CONFIG)
    old_review = parent_review.review()
    old, old_hash = load(parent.REPORT)
    startup, startup_hash = load(parent.parent.REPORT)
    op_cold, op_files, stored_op = op_context()
    source = (ROOT / config['source']).read_bytes()
    original_library = (ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    need(sha(original_library) == config['original_compiler_library_sha256'], 'pinned real compiler library')
    original_members = library_members(original_library)
    need(original_members[config['exec_slot']].name == 'exec', 'actual original exec slot')
    original = b.original_library_member(original_members[config['exec_slot']])
    diet = tomllib.loads((ROOT / 'config/th03_diet.toml').read_text())
    diet_blob = (ROOT / diet['tool']['path']).read_bytes()
    need(sha(diet_blob) == diet['tool']['sha256'] and len(diet_blob) == diet['tool']['size'], 'pinned DIET')
    prefix = ROOT / '.analysis/toolchain/wineprefix'
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
        MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    tasm = ['/usr/bin/wine-stable', str(prefix / 'drive_c/TASM50/bin/TASM32.EXE')]
    record = dict(complete=False, source_acceptance=False, new_source_members=0, new_CODE_extent_bytes=0,
        corrected_initialized_CODE_bytes=255, corrected_literal_frames=4, cold_rebuilt=False,
        game_objects_recompiled=0, driver_sha256=sha((ROOT / DRIVER).read_bytes()), config_sha256=config_hash,
        source_sha256=sha(source), parent_build_sha256=old_hash, parent_review=old_review,
        startup_build_sha256=startup_hash, op_cold=op_cold, phases=[], rounds=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(record, indent=2) + '\n')

    def run(argv, cwd, label, accepted=(0,), marker=None):
        p = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        path = PREFIX + label + '.log'
        (ROOT / path).write_bytes(p.stdout)
        record['phases'].append(dict(label=label, argv=argv, returncode=p.returncode,
                                     log_path=path, log_sha256=sha(p.stdout)))
        save()
        need(p.returncode in accepted and (marker is None or marker in p.stdout),
             label + ': ' + p.stdout.decode(errors='replace')[-1500:])

    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(not SCRATCH.exists() and not OP_SCRATCH.exists(), 'fresh shared-runtime native directories')
        SCRATCH.mkdir()
        OP_SCRATCH.mkdir(parents=True)
        for path in (SCRATCH / 'exec.asm',):
            path.write_bytes(source)
            os.utime(path, (946684800, 946684800))
        (SCRATCH / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        (SCRATCH / 'config.json').write_bytes((ROOT / CONFIG).read_bytes())
        base_lib = checked(old['rounds'][0]['outputs']['lib'])
        members = library_members(base_lib)
        (SCRATCH / 'base.lib').write_bytes(base_lib)
        (SCRATCH / 'extract.rsp').write_bytes(b.build.response('base.lib', ['*' + m.name for m in members]))
        run(dos + ['tlib', '@extract.rsp'], SCRATCH, 'extract')
        extracted = {p.stem.casefold(): p for p in SCRATCH.iterdir() if p.suffix.casefold() == '.obj'}
        need(set(extracted) == {m.name.casefold() for m in members}, 'all source-bound parent member inputs')
        for member in members:
            p = extracted[member.name.casefold()]
            if p.name != member.name + '.obj':
                p.rename(SCRATCH / (member.name + '.obj'))
        vectors = []
        for number in (1, 2):
            need(checked(old['rounds'][number - 1]['outputs']['lib']) == base_lib, 'both retained library rounds')
            c0 = checked(startup['rounds'][number - 1]['outputs']['startup'])
            (SCRATCH / 'c0l.obj').write_bytes(c0)
            (OP_SCRATCH / 'c0l.obj').write_bytes(c0)
            run(tasm + config['assembler_flags'] + ['exec.asm,exec.obj'], SCRATCH, f'round{number}-exec')
            obj = (SCRATCH / 'exec.obj').read_bytes()
            scope = exec_scope(original, obj, config)
            rsp = b.build.response(f'probe\\af537d\\r{number}.lib /E',
                ['+probe\\af537d\\' + m.name + '.obj' for m in members])
            (SCRATCH / f'r{number}.rsp').write_bytes(rsp)
            run(dos + ['tlib', f'@probe\\af537d\\r{number}.rsp'], b.WORK, f'round{number}-library')
            library = (SCRATCH / f'r{number}.lib').read_bytes()
            comparison = compare_members(members, library_members(library), {'exec': obj})
            need(comparison['contextual_members_unchanged'] == 892, 'all other source member programs unchanged')
            (OP_SCRATCH / f'r{number}.lib').write_bytes(library)
            vector = dict(exec=obj, lib=library)
            materials, maps = {}, {}
            for product, work, scratch in (('mainl', b.WORK, SCRATCH), ('op', op.WORK, OP_SCRATCH)):
                response = (work / f'obj/th03/{product}.@l').read_bytes()
                for a, z in ((b'c0l.obj', rb'probe\af537d\c0l.obj'),
                             (f'bin\\th03\\{product}.exe'.encode(), f'probe\\af537d\\r{number}.exe'.encode()),
                             (f'obj\\th03\\{product}.map'.encode(), f'probe\\af537d\\r{number}.map'.encode()),
                             (b' crt.lib' if product == 'mainl' else b' cl.lib', f' probe\\af537d\\r{number}.lib'.encode())):
                    need(response.count(a) == 1, 'one explicit source-C0/runtime/output substitution')
                    response = response.replace(a, z)
                (scratch / f'r{number}.lnk').write_bytes(response)
                run(dos + ['tlink', f'@probe\\af537d\\r{number}.lnk'], work, f'round{number}-{product}-link')
                exe, mapping = (scratch / f'r{number}.exe').read_bytes(), (scratch / f'r{number}.map').read_bytes()
                vector[product + '_exe'], vector[product + '_map'] = exe, mapping
                need(exe == (work / f'bin/th03/{product}.target.exe').read_bytes(), 'complete original ' + product + ' EXE')
                if product == 'mainl':
                    need(mapping == checked(old['rounds'][number - 1]['outputs']['map']), 'unchanged reviewed MAINL MAP')
                    maps[product] = dict(raw_equal_to_after536=True, sha256=sha(mapping), bytes=len(mapping))
                else:
                    maps[product] = op_map_review((work / 'obj/th03/op.map').read_bytes(), mapping)
                materials[product] = material_scope(mapping, original_members, library_members(library))
            need(materials['op']['selected_members'] == config['OP_selected_members'] and
                 materials['op']['totals'] == config['OP_material_totals'], 'complete 76-member OP material inventory')
            pack = OP_SCRATCH / f'p{number}'
            pack.mkdir()
            (pack / 'DIET.EXE').write_bytes(diet_blob)
            (pack / 'OP.EXE').write_bytes(vector['op_exe'])
            run(dos + ['DIET.EXE', '-B', 'OP.EXE'], pack, f'round{number}-op-pack', (1,), b'Success!')
            vector['op_packed'] = (pack / 'OP.EXE').read_bytes()
            need(vector['op_packed'] == stored_op, 'complete canonical Japanese packed OP')
            run(dos + ['DIET.EXE', '-ra', 'OP.EXE'], pack, f'round{number}-op-restore', (1,), b'Success!')
            need((pack / 'OP.EXE').read_bytes() == vector['op_exe'], 'actual OP packed/decoded roundtrip')
            outputs = {}
            for kind, raw in vector.items():
                path = PREFIX + f'round{number}-' + kind + '.bin'
                (ROOT / path).write_bytes(raw)
                outputs[kind] = dict(path=path, bytes=len(raw), sha256=sha(raw))
            record['rounds'].append(dict(round=number, outputs=outputs, exec_scope=scope,
                library_comparison=comparison, map_reviews=maps, material_scopes=materials))
            save()
            vectors.append(vector)
            print('Shared runtime round', number, 'MAINL/OP EXE and canonical OP packed exact', flush=True)
        need(vectors[0] == vectors[1], 'complete two-target raw native pair repeat')
    need((ROOT / config['source']).read_bytes() == source and load(CONFIG)[1] == config_hash and
         op_context()[0] == op_cold, 'all live source/OP cold bindings unchanged')
    record['complete'] = True
    save()


if __name__ == '__main__':
    main()
