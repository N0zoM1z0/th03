#!/usr/bin/env python3
"""Close abort's literal relocation order, retaining its real far-call ABI."""
import fcntl
import json
import os
import subprocess
from pathlib import Path

import build_th03_runtime_after538_work as parent
import review_th03_runtime_after538_work as previous
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members, compare_members

base = parent.base
ROOT = base.ROOT
DRIVER = 'scripts/build_th03_runtime_after539_work.py'
CONFIG = 'config/th03_runtime_after539.json'
PREFIX = '.analysis/work/runtime-after539-'
REPORT = PREFIX + 'build.json'
SCRATCH = base.b.WORK / 'probe/af539i'
OP_SCRATCH = base.op.WORK / 'probe/af539i'


def inputs():
    config, digest = base.load(CONFIG)
    need(config['schema'] == 'th03-shared-abort-literal-order-after539-v1' and
         config['source_paths'] == {'abort': 'src/shared/crt/abort.asm'} and
         config['slots'] == {'abort': 2} and config['literal_fields'] == {'abort': 2} and
         config['literal_order_equal'] == {'abort': True} and
         config['tasm_flags'] == ['/m', '/mx', '/kh32768', '/t'] and
         config['original_assembler_identified'] is False, 'bounded assembly/ABI recipe')
    for name, meta in config['native_tools'].items():
        need(sha((ROOT / meta['path']).read_bytes()) == meta['sha256'], 'pinned native tool ' + name)
    return config, dict(config_sha256=digest, native_tools=config['native_tools'])


def scope(original, native, config):
    result = parent.scope(original, native, 'abort', config)
    need(result['initialized_bytes'] == 20 and result['literal_order_equal'] and
         all(not v for v in result['uninitialized_sites'].values()), 'complete gap-free abort body')
    publics = lambda raw: [r.data.hex() for r in base.b.parse_omf(raw) if r.name == 'PUBDEF']
    need(publics(original) == publics(native), 'literal original PUBLIC payload/order')
    result['literal_PUBLIC_records'] = publics(native)
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
    need(counts == dict(literal_equal=58, order_only=18), 'one existing selected order gap closed')
    return dict(counts=counts, members=rows, diagnostic_only=True, new_source_credit=0)


def link_response(product, work, number):
    response = (work / f'obj/th03/{product}.@l').read_bytes()
    for a, z in ((b'c0l.obj', rb'probe\af539i\c0l.obj'),
                 (f'bin\\th03\\{product}.exe'.encode(), f'probe\\af539i\\r{number}.exe'.encode()),
                 (f'obj\\th03\\{product}.map'.encode(), f'probe\\af539i\\r{number}.map'.encode()),
                 (b' crt.lib' if product == 'mainl' else b' cl.lib',
                  f' probe\\af539i\\r{number}.lib'.encode())):
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
    source = (ROOT / config['source_paths']['abort']).read_bytes()
    original_raw = (ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    need(sha(original_raw) == config['original_compiler_library_sha256'], 'real original CL.LIB identity')
    originals = library_members(original_raw)
    need(len(originals) == 893 and originals[2].name == 'abort', '893 original members / abort slot')
    prefix = ROOT / '.analysis/toolchain/wineprefix'
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    tasm = ['/usr/bin/wine-stable', str(prefix / 'drive_c/TASM50/bin/TASM32.EXE')]
    record = dict(complete=False, source_acceptance=False, new_source_members=0, new_CODE_extent_bytes=0,
        refined_existing_CODE_bytes=20, corrected_literal_order_members=1, cold_rebuilt=False,
        game_objects_recompiled=0, packing_rebuilt=False, driver_sha256=sha((ROOT / DRIVER).read_bytes()),
        parent_build_sha256=old_hash, parent_review=parent_review, startup_build_sha256=startup_hash,
        op_cold=op_cold, emitter_attestation=attestation, source_paths=config['source_paths'],
        source_sha256=sha(source), phases=[], rounds=[])
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
        (SCRATCH / 'abort.asm').write_bytes(source)
        os.utime(SCRATCH / 'abort.asm', (946684800, 946684800))
        (SCRATCH / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        (SCRATCH / 'config.json').write_bytes((ROOT / CONFIG).read_bytes())
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
            run(tasm + config['tasm_flags'] + ['abort.asm,abort.obj'], SCRATCH, f'round{number}-abort')
            obj = (SCRATCH / 'abort.obj').read_bytes()
            body_scope = scope(base.b.original_library_member(originals[2]), obj, config)
            rsp = base.b.build.response(f'probe\\af539i\\r{number}.lib /E',
                ['+probe\\af539i\\' + m.name + '.obj' for m in members])
            (SCRATCH / f'r{number}.rsp').write_bytes(rsp)
            run(dos + ['tlib', f'@probe\\af539i\\r{number}.rsp'], base.b.WORK, f'round{number}-library')
            library = (SCRATCH / f'r{number}.lib').read_bytes()
            comparison = compare_members(members, library_members(library), {'abort': obj})
            need(comparison['contextual_members_unchanged'] == 892, '892 other source programs unchanged')
            (OP_SCRATCH / f'r{number}.lib').write_bytes(library)
            vector, materials, responses = dict(abort=obj, lib=library), {}, {}
            for product, work, scratch in (('mainl', base.b.WORK, SCRATCH), ('op', base.op.WORK, OP_SCRATCH)):
                response = link_response(product, work, number)
                (scratch / f'r{number}.lnk').write_bytes(response)
                responses[product] = sha(response)
                run(dos + ['tlink', f'@probe\\af539i\\r{number}.lnk'], work, f'round{number}-{product}-link')
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
            record['rounds'].append(dict(round=number, outputs=outputs, scope=body_scope,
                library_comparison=comparison, material_scopes=materials, selected_literal_audit=audit,
                response_sha256=responses, library_response_sha256=sha(rsp), reused_packed_op=packed))
            save()
            vectors.append(vector)
            print('abort round', number, 'ordered fields and both original EXEs / full prior MAPs exact', flush=True)
        need(vectors[0] == vectors[1], 'both six-file raw native output vectors repeat')
    need(source == (ROOT / config['source_paths']['abort']).read_bytes() and inputs()[1] == attestation,
         'source and pinned tools unchanged during native production')
    record['complete'] = True
    save()


if __name__ == '__main__':
    main()
