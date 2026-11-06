#!/usr/bin/env python3
"""Recover environment/write order; preserve the explicit setvbuf operand-order gap."""
import fcntl
import json
import os
import subprocess
from pathlib import Path

import build_th03_runtime_after543_work as parent
import review_th03_runtime_after543_work as previous
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members, compare_members
from build_th03_runtime_after538_work import scope as original_member_scope
from build_th03_runtime_after541_work import ordered_publics, omf_index
import bootstrap_jwasm

base = parent.base
ROOT = base.ROOT
DRIVER = 'scripts/build_th03_runtime_after544_work.py'
CONFIG = 'config/th03_runtime_after544.json'
PREFIX = '.analysis/work/runtime-after544-'
REPORT = PREFIX + 'build.json'
SCRATCH = base.b.WORK / 'probe/af544o'
OP_SCRATCH = base.op.WORK / 'probe/af544o'


def inputs():
    config, digest = base.load(CONFIG)
    need(config['schema'] == 'th03-shared-environment-stdio-order-after544-v1' and
         config['source_paths'] == {'dosenv': 'src/shared/crt/dos_environment.asm', 'write': 'src/shared/crt/write_stream.asm', 'setvbuf': 'src/shared/crt/stdio_buffer.asm'} and
         config['slots'] == {'dosenv': 25, 'write': 331, 'setvbuf': 285} and
         config['literal_fields'] == {'dosenv': 5, 'write': 9, 'setvbuf': 13} and
         config['literal_order_equal'] == {'dosenv': True, 'write': True, 'setvbuf': False} and
         config['includes'] == ['src/mainl/crt/stdio_layout.inc'] and
         set(config['native_tools']) == {'jwasm', 'tlib', 'tlink', 'msdos', 'wine'} and
         config['compatible_profile'] == bootstrap_jwasm.PROFILE and
         config['compatible_flags'] == ['-nologo', '-Cp', '-omf'] and
         config['PUBLIC_record_packing_equal'] == {'dosenv': True, 'write': True, 'setvbuf': True} and
         config['original_assembler_identified'] is False, 'bounded assembly/ABI recipe')
    for name, meta in config['native_tools'].items():
        need(sha((ROOT / meta['path']).read_bytes()) == meta['sha256'], 'pinned native tool ' + name)
    return config, dict(config_sha256=digest, native_tools=config['native_tools'],
        compatible_tool=bootstrap_jwasm.attest(),
        attestation_driver_sha256=sha(Path(bootstrap_jwasm.__file__).read_bytes()))


def scope(original, native, name, config):
    result = original_member_scope(original, native, name, config)
    code, data, bss = {'dosenv': (365, 0, 0), 'write': (358, 0, 0), 'setvbuf': (289, 4, 0)}[name]
    need(result['initialized_bytes'] == code + data and
         result['literal_order_equal'] == (name != 'setvbuf') and
         result['uninitialized_sites'] == {'1': [], '2': [], '3': list(range(bss))},
         'complete initialized storage and true BSS ' + name)
    a, z = ordered_publics(original), ordered_publics(native)
    packets = lambda raw: [r.data.hex() for r in base.b.parse_omf(raw) if r.name == 'PUBDEF']
    aa, zz = packets(original), packets(native)
    need(a == z and (aa == zz) == config['PUBLIC_record_packing_equal'][name],
         'literal cross-segment PUBLIC entries and explicit packet-packing status')
    if name == 'setvbuf':
        need([f['site'] for f in result['original_fields']] ==
             [210,196,194,190,188,129,103,77,71,63,55,49,41] and
             [f['site'] for f in result['native_fields']] ==
             [210,194,196,188,190,129,103,77,71,63,55,49,41],
             'explicit remaining two intra-instruction operand-pair orders; not ordered-exact')
        result['remaining_operand_order_pairs'] = [[196,194], [190,188]]
    spans, sites = [], []
    for record in base.b.parse_omf(native):
        need(record.name != 'LIDATA', 'bounded native sources emit initialized storage as LEDATA')
        if record.name != 'LEDATA':
            continue
        segment, pos = omf_index(record.data)
        offset = int.from_bytes(record.data[pos:pos + 2], 'little')
        length = len(record.data) - pos - 2
        spans.append(dict(segment=segment, offset=offset, bytes=length))
        sites.extend((segment, i) for i in range(offset, offset + length))
    need(len(sites) == len(set(sites)) == code + data and
         set(sites) == set(base.b.initialized_payload(native)),
         'every initialized byte emitted once, without overlaps or BSS initialization ' + name)
    result.update(original_PUBLIC_entries=a, native_PUBLIC_entries=z,
                  original_PUBLIC_records=aa, native_PUBLIC_records=zz,
                  PUBLIC_record_packing_equal=aa == zz,
                  native_initialized_record_spans=spans, every_initialized_byte_written_once=True,
                  CODE_bytes=code, DATA_bytes=data, BSS_bytes=bss)
    return result


def selected_literal_audit(selected, original_members, native_members):
    rows, counts = [], dict(literal_equal=0, order_only=0)
    for member in selected:
        slot, name = member['slot'], member['name']
        need(original_members[slot].name == native_members[slot].name == name, 'selected original slot')
        a = base.b.original_library_member(original_members[slot])
        z = base.b.original_library_member(native_members[slot])
        aa, zz = base.b.literal_fields(a), base.b.literal_fields(z)
        key = lambda f: (f['segment'], f['site'])
        need(base.b.externs(a) == base.b.externs(z) and sorted(aa, key=key) == sorted(zz, key=key),
             'full per-site attributes and literal import order ' + name)
        kind = 'literal_equal' if aa == zz else 'order_only'
        counts[kind] += 1
        rows.append(dict(name=name, slot=slot, kind=kind, original_imports=base.b.externs(a),
                         native_imports=base.b.externs(z), original_fields=aa, native_fields=zz))
    need(counts == dict(literal_equal=69, order_only=7), 'two selected order gaps closed; setvbuf remains order-only')
    return dict(counts=counts, members=rows, diagnostic_only=True, new_source_credit=0)


def link_response(product, work, number):
    response = (work / f'obj/th03/{product}.@l').read_bytes()
    for a, z in ((b'c0l.obj', rb'probe\af544o\c0l.obj'),
                 (f'bin\\th03\\{product}.exe'.encode(), f'probe\\af544o\\r{number}.exe'.encode()),
                 (f'obj\\th03\\{product}.map'.encode(), f'probe\\af544o\\r{number}.map'.encode()),
                 (b' crt.lib' if product == 'mainl' else b' cl.lib',
                  f' probe\\af544o\\r{number}.lib'.encode())):
        need(response.count(a) == 1, 'one source startup/runtime/output path')
        response = response.replace(a, z)
    return response


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    config, attestation = inputs()
    parent_review = previous.review()
    old, old_hash = base.load(parent.REPORT)
    startup, startup_hash = base.load(base.parent.parent.REPORT)
    op_cold, _, packed_target = base.op_context()
    source = {n: (ROOT / p).read_bytes() for n, p in config['source_paths'].items()}
    includes = {p: (ROOT / p).read_bytes() for p in config['includes']}
    original_raw = (ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    need(sha(original_raw) == config['original_compiler_library_sha256'], 'real original CL.LIB identity')
    originals = library_members(original_raw)
    need(len(originals) == 893 and all(originals[i].name == n for n, i in config['slots'].items()),
         '893 original members / both selected slots')
    prefix = ROOT / '.analysis/toolchain/wineprefix'
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    jwasm = str(ROOT / config['native_tools']['jwasm']['path'])
    record = dict(complete=False, source_acceptance=False, new_source_members=0, new_CODE_extent_bytes=0,
        refined_existing_CODE_bytes=1012, refined_existing_DATA_bytes=4, preserved_existing_BSS_bytes=0,
        corrected_literal_order_members=2, partially_refined_literal_order_members=1, cold_rebuilt=False,
        game_objects_recompiled=0, packing_rebuilt=False, driver_sha256=sha((ROOT / DRIVER).read_bytes()),
        parent_build_sha256=old_hash, parent_review=parent_review, startup_build_sha256=startup_hash,
        op_cold=op_cold, emitter_attestation=attestation, source_paths=config['source_paths'],
        source_sha256={n: sha(v) for n, v in source.items()},
        include_sha256={p: sha(v) for p, v in includes.items()}, phases=[], rounds=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(record, indent=2) + '\n')

    def run(argv, cwd, label):
        p = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        path = PREFIX + label + '.log'
        (ROOT / path).write_bytes(p.stdout)
        record['phases'].append(dict(label=label, argv=argv, returncode=p.returncode,
                                     log_path=path, log_sha256=sha(p.stdout)))
        save()
        need(p.returncode == 0, label + ': ' + p.stdout.decode(errors='replace')[-1500:])

    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(not SCRATCH.exists() and not OP_SCRATCH.exists(), 'fresh retained native directories')
        SCRATCH.mkdir()
        OP_SCRATCH.mkdir()
        for name, raw in source.items():
            (SCRATCH / (name + '.asm')).write_bytes(raw)
            os.utime(SCRATCH / (name + '.asm'), (946684800, 946684800))
        for p, raw in includes.items():
            (SCRATCH / Path(p).name).write_bytes(raw)
        (SCRATCH / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        (SCRATCH / 'config.json').write_bytes((ROOT / CONFIG).read_bytes())
        (SCRATCH / 'profile.toml').write_bytes((ROOT / config['compatible_profile']).read_bytes())
        old_lib = base.checked(old['rounds'][0]['outputs']['lib'])
        members = library_members(old_lib)
        (SCRATCH / 'base.lib').write_bytes(old_lib)
        (SCRATCH / 'extract.rsp').write_bytes(base.b.build.response('base.lib', ['*' + m.name for m in members]))
        run(dos + ['tlib', '@extract.rsp'], SCRATCH, 'extract')
        extracted = {p.stem.casefold(): p for p in SCRATCH.iterdir() if p.suffix.casefold() == '.obj'}
        need(set(extracted) == {m.name.casefold() for m in members}, 'all parent member objects extracted')
        for m in members:
            p = extracted[m.name.casefold()]
            if p.name != m.name + '.obj':
                p.rename(SCRATCH / (m.name + '.obj'))
        vectors = []
        for number in (1, 2):
            need(base.checked(old['rounds'][number - 1]['outputs']['lib']) == old_lib, 'both unchanged parent library rounds')
            c0 = base.checked(startup['rounds'][number - 1]['outputs']['startup'])
            for scratch in (SCRATCH, OP_SCRATCH):
                (scratch / 'c0l.obj').write_bytes(c0)
            for name in source:
                run([jwasm, *config['compatible_flags'], '-Fo' + name + '.obj', name + '.asm'], SCRATCH, f'round{number}-{name}')
            fresh = {n: (SCRATCH / (n + '.obj')).read_bytes() for n in source}
            scopes = {n: scope(base.b.original_library_member(originals[config['slots'][n]]), raw, n, config)
                      for n, raw in fresh.items()}
            rsp = base.b.build.response(f'probe\\af544o\\r{number}.lib /E',
                ['+probe\\af544o\\' + m.name + '.obj' for m in members])
            (SCRATCH / f'r{number}.rsp').write_bytes(rsp)
            run(dos + ['tlib', f'@probe\\af544o\\r{number}.rsp'], base.b.WORK, f'round{number}-library')
            library = (SCRATCH / f'r{number}.lib').read_bytes()
            comparison = compare_members(members, library_members(library), fresh)
            need(comparison['contextual_members_unchanged'] == 890, '890 other source programs unchanged')
            (OP_SCRATCH / f'r{number}.lib').write_bytes(library)
            vector, materials, responses = dict(fresh, lib=library), {}, {}
            for product, work, scratch in (('mainl', base.b.WORK, SCRATCH), ('op', base.op.WORK, OP_SCRATCH)):
                response = link_response(product, work, number)
                (scratch / f'r{number}.lnk').write_bytes(response)
                responses[product] = sha(response)
                run(dos + ['tlink', f'@probe\\af544o\\r{number}.lnk'], work, f'round{number}-{product}-link')
                exe, mapping = (scratch / f'r{number}.exe').read_bytes(), (scratch / f'r{number}.map').read_bytes()
                vector[product + '_exe'], vector[product + '_map'] = exe, mapping
                need(exe == base.checked(old['rounds'][number - 1]['outputs'][product + '_exe']) ==
                     (work / f'bin/th03/{product}.target.exe').read_bytes(), 'complete original ' + product + ' EXE')
                need(mapping == base.checked(old['rounds'][number - 1]['outputs'][product + '_map']),
                     'complete unchanged native ' + product + ' MAP')
                materials[product] = base.material_scope(mapping, originals, library_members(library))
            audit = selected_literal_audit(materials['op']['selected_members'], originals, library_members(library))
            packed = old['rounds'][number - 1]['reused_packed_op']
            need(base.checked(packed) == packed_target, 'actual retained original packed OP proof')
            outputs = {}
            for kind, raw in vector.items():
                path = PREFIX + f'round{number}-' + kind + '.bin'
                (ROOT / path).write_bytes(raw)
                outputs[kind] = dict(path=path, bytes=len(raw), sha256=sha(raw))
            record['rounds'].append(dict(round=number, outputs=outputs, scopes=scopes,
                library_comparison=comparison, material_scopes=materials, selected_literal_audit=audit,
                response_sha256=responses, library_response_sha256=sha(rsp), reused_packed_op=packed))
            save()
            vectors.append(vector)
            print('Environment/stdio round', number, 'ordered fields and both original EXEs / full prior MAPs exact', flush=True)
        need(vectors[0] == vectors[1], 'both eight-file raw native output vectors repeat')
    need(source == {n: (ROOT / p).read_bytes() for n, p in config['source_paths'].items()} and
         includes == {p: (ROOT / p).read_bytes() for p in config['includes']} and inputs()[1] == attestation,
         'source and pinned tools unchanged during native production')
    record['complete'] = True
    save()


if __name__ == '__main__':
    main()
