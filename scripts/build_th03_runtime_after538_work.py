#!/usr/bin/env python3
"""Restore selected near-call frames through native, unpatched OMF emitters."""
import fcntl
import json
import os
import subprocess
from pathlib import Path

import build_th03_runtime_after537_work as base
import review_th03_runtime_after537_work as previous
import bootstrap_jwasm
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members, compare_members, object_program_records

ROOT = base.ROOT
DRIVER = 'scripts/build_th03_runtime_after538_work.py'
CONFIG = 'config/th03_runtime_after538.json'
PREFIX = '.analysis/work/runtime-after538-'
REPORT = PREFIX + 'build.json'
SCRATCH = base.b.WORK / 'probe/af538l'
OP_SCRATCH = base.op.WORK / 'probe/af538l'


def inputs():
    config, digest = base.load(CONFIG)
    need(config['schema'] == 'th03-shared-near-frames-after538-v1' and
         config['compatible_profile'] == bootstrap_jwasm.PROFILE and
         config['compatible_flags'] == ['-nologo', '-Cp', '-omf'] and
         config['tasm_flags'] == ['/m', '/mx', '/kh32768', '/t'] and
         config['original_assembler_identified'] is False, 'explicit bounded emitter scope')
    return config, dict(config_sha256=digest, tool=bootstrap_jwasm.attest(),
        attestation_driver_sha256=sha(Path(bootstrap_jwasm.__file__).read_bytes()))


def scope(original, native, name, config):
    b = base.b
    ss, tt = b.segment_definitions(original), b.segment_definitions(native)
    x, y = b.initialized_payload(original), b.initialized_payload(native)
    aa = [r.data[0] for r in b.parse_omf(original) if r.name == 'SEGDEF']
    zz = [r.data[0] for r in b.parse_omf(native) if r.name == 'SEGDEF']
    pubs = lambda raw, segments: {str(s['index']): b.code_publics(raw, s['index']) for s in segments}
    need(b.describe_omf(native)['valid'] and ss == tt and aa == zz and x == y and
         pubs(original, ss) == pubs(native, tt) and b.externs(original) == b.externs(native),
         'all original code/storage, widths, public ownership and literal import order ' + name)
    records = {}
    for kind in ('GRPDEF', 'ALIAS', 'MODEND'):
        a = [r.data.hex() for r in b.parse_omf(original) if r.name == kind]
        z = [r.data.hex() for r in b.parse_omf(native) if r.name == kind]
        need(a == z, 'literal original group/entry semantics ' + name)
        records[kind] = a
    a, z = b.literal_fields(original), b.literal_fields(native)
    key = lambda f: (f['segment'], f['site'])
    need(len(a) == len(z) == config['literal_fields'][name] and
         sorted(a, key=key) == sorted(z, key=key) and
         (a == z) == config['literal_order_equal'][name],
         'all full literal attributes match at their sites; exact remaining order status ' + name)
    # Both actual lists remain intact. Sorting above checks site attributes,
    # and never supplies an ordered-equality claim or changes a native object.
    return dict(segments=ss, attributes=aa, initialized_bytes=len(y),
        initialized_sha256=sha(bytes(v for _, v in sorted(y.items()))),
        uninitialized_sites={str(s['index']): [i for i in range(s['size']) if (s['index'], i) not in y] for s in ss},
        publics=pubs(native, tt), imports=b.externs(native), literal_records=records,
        original_fields=a, native_fields=z, literal_order_equal=a == z,
        original_program_identity=object_program_records(original) == object_program_records(native))


def mainl_map_review(old, new):
    removed = b' 0E3F:2872 0000 C=BSS    S=_BSS           G=DGROUP  M=fbrk       ACBP=48\r\n'
    anchor = b' 0E3F:2876 000A C=BSS    S=_BSS           G=DGROUP  M=xx         ACBP=48\r\n'
    added = b' 0E3F:2880 0000 C=BSS    S=_BSS           G=DGROUP  M=setblock   ACBP=48\r\n'
    need(old.count(removed) == old.count(anchor) == 1 and added not in old, 'explicit prior MAINL empty-segment rows')
    expected = old.replace(removed, b'', 1).replace(anchor, anchor + added, 1)
    need(new == expected, 'entire MAINL MAP differs only in the two reviewed zero-BSS rows')
    return dict(raw_equal=False, old_sha256=sha(old), new_sha256=sha(new), bytes=len(new),
        removed_zero_owner='fbrk at 0E3F:2872', added_zero_owner='setblock at 0E3F:2880',
        all_material_rows_addresses_flags_and_other_bytes_equal=True)


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    config, attestation = inputs()
    parent_review = previous.review()
    parent, parent_hash = base.load(base.REPORT)
    startup, startup_hash = base.load(base.parent.parent.REPORT)
    op_cold, _, packed_target = base.op_context()
    source = {n: (ROOT / p).read_bytes() for n, p in config['source_paths'].items()}
    original_raw = (ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    need(sha(original_raw) == config['original_compiler_library_sha256'], 'independently pinned real CL.LIB')
    originals = library_members(original_raw)
    need(len(originals) == 893 and all(originals[i].name == n for n, i in config['slots'].items()), 'five original slots')
    prefix = ROOT / '.analysis/toolchain/wineprefix'
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    tasm = ['/usr/bin/wine-stable', str(prefix / 'drive_c/TASM50/bin/TASM32.EXE')]
    jwasm = str(ROOT / '.analysis/toolchain/extra/jwasm/GccUnixR/jwasm')
    record = dict(complete=False, source_acceptance=False, new_source_members=0, new_CODE_extent_bytes=0,
        corrected_near_frames=10, corrected_group_memberships=1, cold_rebuilt=False, game_objects_recompiled=0,
        driver_sha256=sha((ROOT / DRIVER).read_bytes()), parent_build_sha256=parent_hash,
        parent_review=parent_review, startup_build_sha256=startup_hash, op_cold=op_cold,
        emitter_attestation=attestation, source_paths=config['source_paths'],
        source_sha256={n: sha(v) for n, v in source.items()},
        include_sha256={p: sha((ROOT / p).read_bytes()) for p in config['includes']},
        packing_rebuilt=False, packing_bridge='Unchanged decoded input, pinned tools and actual retained two-round packed OP proof',
        phases=[], rounds=[])
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
        need(not SCRATCH.exists() and not OP_SCRATCH.exists(), 'fresh retained five-owner native directories')
        SCRATCH.mkdir()
        OP_SCRATCH.mkdir()
        for n, raw in source.items():
            p = SCRATCH / (n + '.asm')
            p.write_bytes(raw)
            os.utime(p, (946684800, 946684800))
        for p in config['includes']:
            (SCRATCH / Path(p).name).write_bytes((ROOT / p).read_bytes())
        (SCRATCH / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        (SCRATCH / 'config.json').write_bytes((ROOT / CONFIG).read_bytes())
        old_lib = base.checked(parent['rounds'][0]['outputs']['lib'])
        members = library_members(old_lib)
        (SCRATCH / 'base.lib').write_bytes(old_lib)
        (SCRATCH / 'extract.rsp').write_bytes(base.b.build.response('base.lib', ['*' + m.name for m in members]))
        run(dos + ['tlib', '@extract.rsp'], SCRATCH, 'extract')
        extracted = {p.stem.casefold(): p for p in SCRATCH.iterdir() if p.suffix.casefold() == '.obj'}
        need(set(extracted) == {m.name.casefold() for m in members}, 'complete source-parent object extraction')
        for m in members:
            p = extracted[m.name.casefold()]
            if p.name != m.name + '.obj':
                p.rename(SCRATCH / (m.name + '.obj'))
        vectors = []
        for number in (1, 2):
            need(base.checked(parent['rounds'][number - 1]['outputs']['lib']) == old_lib, 'both inherited library rounds')
            c0 = base.checked(startup['rounds'][number - 1]['outputs']['startup'])
            for scratch in (SCRATCH, OP_SCRATCH):
                (scratch / 'c0l.obj').write_bytes(c0)
            for name in config['compatible_members']:
                run([jwasm, *config['compatible_flags'], '-Fo' + name + '.obj', name + '.asm'], SCRATCH,
                    f'round{number}-{name}')
            run(tasm + config['tasm_flags'] + ['setblock.asm,setblock.obj'], SCRATCH, f'round{number}-setblock')
            fresh = {n: (SCRATCH / (n + '.obj')).read_bytes() for n in source}
            scopes = {n: scope(base.b.original_library_member(originals[config['slots'][n]]), raw, n, config)
                      for n, raw in fresh.items()}
            rsp = base.b.build.response(f'probe\\af538l\\r{number}.lib /E',
                ['+probe\\af538l\\' + m.name + '.obj' for m in members])
            (SCRATCH / f'r{number}.rsp').write_bytes(rsp)
            run(dos + ['tlib', f'@probe\\af538l\\r{number}.rsp'], base.b.WORK, f'round{number}-library')
            library = (SCRATCH / f'r{number}.lib').read_bytes()
            comparison = compare_members(members, library_members(library), fresh)
            need(comparison['contextual_members_unchanged'] == 888, 'all other 888 source member programs unchanged')
            (OP_SCRATCH / f'r{number}.lib').write_bytes(library)
            vector, materials, maps, responses = dict(fresh, lib=library), {}, {}, {}
            for product, work, scratch in (('mainl', base.b.WORK, SCRATCH), ('op', base.op.WORK, OP_SCRATCH)):
                response = (work / f'obj/th03/{product}.@l').read_bytes()
                for a, z in ((b'c0l.obj', rb'probe\af538l\c0l.obj'),
                             (f'bin\\th03\\{product}.exe'.encode(), f'probe\\af538l\\r{number}.exe'.encode()),
                             (f'obj\\th03\\{product}.map'.encode(), f'probe\\af538l\\r{number}.map'.encode()),
                             (b' crt.lib' if product == 'mainl' else b' cl.lib', f' probe\\af538l\\r{number}.lib'.encode())):
                    need(response.count(a) == 1, 'one explicit source startup/runtime/output path')
                    response = response.replace(a, z)
                (scratch / f'r{number}.lnk').write_bytes(response)
                responses[product] = sha(response)
                run(dos + ['tlink', f'@probe\\af538l\\r{number}.lnk'], work, f'round{number}-{product}-link')
                exe, mapping = (scratch / f'r{number}.exe').read_bytes(), (scratch / f'r{number}.map').read_bytes()
                vector[product + '_exe'], vector[product + '_map'] = exe, mapping
                need(exe == base.checked(parent['rounds'][number - 1]['outputs'][product + '_exe']) ==
                     (work / f'bin/th03/{product}.target.exe').read_bytes(), 'complete original ' + product + ' EXE')
                if product == 'mainl':
                    maps[product] = mainl_map_review(base.checked(parent['rounds'][number - 1]['outputs']['mainl_map']), mapping)
                else:
                    need(mapping == (work / 'obj/th03/op.map').read_bytes(), 'complete historical OP MAP restored')
                    maps[product] = dict(raw_equal_to_cold=True, sha256=sha(mapping), bytes=len(mapping))
                materials[product] = base.material_scope(mapping, originals, library_members(library))
            packed = parent['rounds'][number - 1]['outputs']['op_packed']
            need(base.checked(packed) == packed_target, 'retained original packed OP bridge')
            outputs = {}
            for kind, raw in vector.items():
                path = PREFIX + f'round{number}-' + kind + '.bin'
                (ROOT / path).write_bytes(raw)
                outputs[kind] = dict(path=path, bytes=len(raw), sha256=sha(raw))
            record['rounds'].append(dict(round=number, outputs=outputs, scopes=scopes,
                library_comparison=comparison, material_scopes=materials, map_reviews=maps,
                response_sha256=responses, library_response_sha256=sha(rsp), reused_packed_op=packed))
            save()
            vectors.append(vector)
            print('Near-frame round', number, 'both original EXEs and complete OP MAP exact', flush=True)
        need(vectors[0] == vectors[1], 'complete nine-file raw native vectors repeat')
    need(source == {n: (ROOT / p).read_bytes() for n, p in config['source_paths'].items()} and
         record['include_sha256'] == {p: sha((ROOT / p).read_bytes()) for p in config['includes']} and
         inputs()[1] == attestation, 'source/includes/emitter unchanged during native production')
    record['complete'] = True
    save()


if __name__ == '__main__':
    main()
