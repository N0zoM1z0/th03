#!/usr/bin/env python3
"""Restore ordered startup fields while retaining original entry and storage."""
import fcntl
import json
import os
import subprocess
from pathlib import Path

import build_th03_runtime_after547_work as parent
import review_th03_runtime_after547_work as previous
import build_th03_mainl_after535_work as startup_baseline
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members, object_program_records

base = parent.base
ROOT = base.ROOT
DRIVER = 'scripts/build_th03_runtime_after548_work.py'
CONFIG = 'config/th03_startup_after548.json'
PREFIX = '.analysis/work/runtime-after548-'
REPORT = PREFIX + 'build.json'
SCRATCH = base.b.WORK / 'probe/af548h'
OP_SCRATCH = base.op.WORK / 'probe/af548h'


def inputs():
    config, digest = base.load(CONFIG)
    baseline, _ = startup_baseline.inputs()
    need(config['schema'] == 'th03-shared-large-startup-order-after548-v1' and
         config['source'] == 'src/shared/crt/startup_large.asm' and
         config['original'] == baseline['original'] and config['supplier_inputs'] == baseline['supplier_inputs'] and
         config['native_flags'] == ['/m', '/mx', '/kh32768', '/t'] and config['literal_fields'] == 58 and
         config['literal_ordered_PUBLIC_entries_equal'] is False and
         config['literal_ordered_PUBLIC_records_equal'] is False and
         set(config['native_tools']) == {'tasm', 'tlink', 'wine', 'msdos'}, 'bounded supplier startup recipe')
    for name, pin in config['native_tools'].items():
        need(sha((ROOT / pin['path']).read_bytes()) == pin['sha256'], 'pinned native tool ' + name)
    return config, dict(config_sha256=digest, native_tools=config['native_tools'],
        original_startup=config['original'], supplier_inputs=config['supplier_inputs'], original_tool_identity_claimed=False)


def scope(original, native, config):
    a, z = startup_baseline.profile(original), startup_baseline.profile(native)
    need(a['segments'] == z['segments'] and a['initialized'] == z['initialized'] and
         len(a['segments']) == 17 and a['segments'][0]['size'] == 625 and
         a['initialized'][0]['bytes'] == 623 and a['initialized'][0]['uninitialized'] == [621, 622] and
         a['initialized'][5]['bytes'] == 144 and a['segments'][16]['size'] == 128 and
         a['initialized'][16]['uninitialized'] == list(range(128)) and
         a['initialized'][16]['bytes'] == 0, 'all original storage, true cache holes and reserved stack')
    records = lambda raw, kind: [r.data.hex() for r in base.b.parse_omf(raw) if r.name == kind]
    for kind in ('THEADR', 'LNAMES', 'SEGDEF', 'GRPDEF', 'EXTDEF', 'ALIAS', 'MODEND'):
        need(records(original, kind) == records(native, kind), 'literal original startup ' + kind)
    need(len(a['literal_fields']) == len(z['literal_fields']) == 58 and
         a['literal_fields'] == z['literal_fields'], 'all 58 literal ordered startup fields')
    ap, zp = parent.ordered_publics(original), parent.ordered_publics(native)
    aa, zz = records(original, 'PUBDEF'), records(native, 'PUBDEF')
    key = lambda p: p['name']
    need(len(ap) == len(zp) == len(aa) == len(zz) == 32 and
         sorted(ap, key=key) == sorted(zp, key=key) and sorted(aa) == sorted(zz) and
         (ap == zp) == config['literal_ordered_PUBLIC_entries_equal'] and
         (aa == zz) == config['literal_ordered_PUBLIC_records_equal'],
         'complete original PUBLIC packet set; emitted PUBLIC order remains explicitly different')
    # Reuse the established recursive LIDATA decoder on actual raw records.
    # Header/trailer form a read-only parser envelope; no product object is changed.
    parsed = base.b.parse_omf(native)
    record_bytes = lambda r: native[r.offset:r.offset + 3 + r.length]
    header = record_bytes(parsed[0])
    trailer = record_bytes(parsed[-1])
    sites, spans = [], []
    for record in parsed:
        if record.name not in ('LEDATA', 'LIDATA'):
            continue
        initialized = base.b.initialized_payload(header + record_bytes(record) + trailer)
        sites.extend(initialized)
        spans.append(dict(record=record.name, segment=record.data[0],
                          offset=int.from_bytes(record.data[1:3], 'little'), bytes=len(initialized)))
    need(len(sites) == len(set(sites)) == 767 and set(sites) == set(base.b.initialized_payload(native)),
         'every original initialized byte written once; no cache/stack initialization')
    return dict(original=a, native=z, original_PUBLIC_entries=ap, native_PUBLIC_entries=zp,
        original_PUBLIC_records=aa, native_PUBLIC_records=zz, PUBLIC_packet_multiset_equal=True,
        literal_ordered_fields_equal=True, literal_ordered_PUBLIC_entries_equal=ap == zp,
        literal_ordered_PUBLIC_records_equal=aa == zz, native_initialized_record_spans=spans,
        every_initialized_byte_written_once=True, original_OMF_program_equal=object_program_records(original) == object_program_records(native))


def link_response(product, work, number):
    response = (work / f'obj/th03/{product}.@l').read_bytes()
    for a, z in ((b'c0l.obj', rb'probe\af548h\c0l.obj'),
                 (f'bin\\th03\\{product}.exe'.encode(), f'probe\\af548h\\r{number}.exe'.encode()),
                 (f'obj\\th03\\{product}.map'.encode(), f'probe\\af548h\\r{number}.map'.encode()),
                 (b' crt.lib' if product == 'mainl' else b' cl.lib', f' probe\\af548h\\r{number}.lib'.encode())):
        need(response.count(a) == 1, 'one actual startup/runtime/output path')
        response = response.replace(a, z)
    return response


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    config, attestation = inputs()
    parent_review = previous.review()
    old, old_hash = base.load(parent.REPORT)
    baseline, baseline_hash = base.load(startup_baseline.REPORT)
    op_cold, _, packed_target = base.op_context()
    source = (ROOT / config['source']).read_bytes()
    original = (ROOT / config['original']['path']).read_bytes()
    original_library = (ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    need(sha(original_library) == config['original_compiler_library_sha256'], 'real original compiler library')
    originals = library_members(original_library)
    prefix = ROOT / '.analysis/toolchain/wineprefix'
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    tasm = ['/usr/bin/wine-stable', str(ROOT / config['native_tools']['tasm']['path'])]
    record = dict(complete=False, source_acceptance=False, authored_game_credit_bytes=0, new_source_members=0,
        new_CODE_extent_bytes=0, cold_rebuilt=False, game_objects_recompiled=0, packing_rebuilt=False,
        library_rebuilt=False, fresh_native_outputs_per_round=5, reused_library_outputs_per_round=1,
        CODE_extent=625, initialized_CODE_bytes=623, DATA_bytes=144, uninitialized_CODE_bytes=2,
        uninitialized_STACK_bytes=128, ordered_fields_equal=58, ordered_PUBLIC_entries_equal=False,
        driver_sha256=sha((ROOT / DRIVER).read_bytes()), parent_build_sha256=old_hash, parent_review=parent_review,
        startup_baseline_build_sha256=baseline_hash, op_cold=op_cold, emitter_attestation=attestation,
        source=config['source'], source_sha256=sha(source), phases=[], rounds=[])
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
        need(not SCRATCH.exists() and not OP_SCRATCH.exists(), 'fresh retained startup directories')
        SCRATCH.mkdir()
        OP_SCRATCH.mkdir()
        (SCRATCH / 'c0.asm').write_bytes(source)
        os.utime(SCRATCH / 'c0.asm', (946684800, 946684800))
        (SCRATCH / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        (SCRATCH / 'config.json').write_bytes((ROOT / CONFIG).read_bytes())
        vectors = []
        for number in (1, 2):
            library = base.checked(old['rounds'][number - 1]['outputs']['lib'])
            for scratch in (SCRATCH, OP_SCRATCH):
                (scratch / f'r{number}.lib').write_bytes(library)
            run(tasm + config['native_flags'] + ['c0.ASM,c0l.obj'], SCRATCH, f'round{number}-assemble')
            obj = (SCRATCH / 'c0l.obj').read_bytes()
            comparison = scope(original, obj, config)
            (OP_SCRATCH / 'c0l.obj').write_bytes(obj)
            vector, responses, materials = dict(startup=obj), {}, {}
            for product, work, scratch in (('mainl', base.b.WORK, SCRATCH), ('op', base.op.WORK, OP_SCRATCH)):
                response = link_response(product, work, number)
                (scratch / f'r{number}.lnk').write_bytes(response)
                responses[product] = sha(response)
                run(dos + ['tlink', f'@probe\\af548h\\r{number}.lnk'], work, f'round{number}-{product}-link')
                exe, mapping = (scratch / f'r{number}.exe').read_bytes(), (scratch / f'r{number}.map').read_bytes()
                need(exe == base.checked(old['rounds'][number - 1]['outputs'][product + '_exe']) ==
                     (work / f'bin/th03/{product}.target.exe').read_bytes(), 'complete original ' + product + ' EXE')
                need(mapping == base.checked(old['rounds'][number - 1]['outputs'][product + '_map']),
                     'complete unchanged ' + product + ' MAP')
                vector[product + '_exe'], vector[product + '_map'] = exe, mapping
                materials[product] = base.material_scope(mapping, originals, library_members(library))
            packed = old['rounds'][number - 1]['reused_packed_op']
            need(base.checked(packed) == packed_target, 'retained actual packed OP proof')
            outputs = {}
            for kind, raw in vector.items():
                path = PREFIX + f'round{number}-' + kind + '.bin'
                (ROOT / path).write_bytes(raw)
                outputs[kind] = dict(path=path, bytes=len(raw), sha256=sha(raw))
            outputs['lib'] = old['rounds'][number - 1]['outputs']['lib']
            record['rounds'].append(dict(round=number, outputs=outputs, comparison=comparison,
                response_sha256=responses, material_scopes=materials, reused_packed_op=packed))
            save()
            vectors.append(vector)
            print('Startup round', number, '58 ordered fields and both original EXEs / full prior MAPs exact', flush=True)
        need(vectors[0] == vectors[1], 'both complete five-file fresh native vectors repeat')
    need(source == (ROOT / config['source']).read_bytes() and inputs()[1] == attestation,
         'source and pinned tools unchanged during native production')
    record['complete'] = True
    save()


if __name__ == '__main__':
    main()
