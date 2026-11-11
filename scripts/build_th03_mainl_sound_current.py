#!/usr/bin/env python3
"""Compose four natural sound ASM providers with the current MAINL project."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import subprocess

import build_th03_mainl_linked_current as linked
from build_th03_mainl_display_work import payload, literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz
from probe_th03_main_bomb_rikako_cpp import segment_definitions

ROOT, need, sha = linked.ROOT, linked.need, linked.sha
DRIVER = 'scripts/build_th03_mainl_sound_current.py'
PARENT = 'af1369m'
STAGE = 'af1375s'
# Source, original compiler wrapper, original allocation, complete function,
# and actual TASM field order (site, original EXTDEF index).
SOUND = {
    'snd_mode': ('mode_detect', 'snd_mode.c', 0x2C, 29, [(13, 3), (20, 2), (24, 1)]),
    'snd_pmdr': ('pmd_resident', 'snd_pmdr.c', 0x4A, 57, [(2, 1), (7, 3), (12, 4), (17, 2)]),
    'snd_dlyv': ('volume_wait', 'snd_dlyv.c', 0x84, 27, [(7, 1)]),
    'snd_se_r': ('se_reset', 'snd_se_r.cpp', 0x65E, 11, [(2, 2), (7, 1)]),
}
FLAGS = ['/m', '/mx', '/kh32768', '/t', '/dGAME=3']


def sources():
    return {stem: (ROOT / f'src/mainl/sound/{row[0]}.asm').read_bytes() for stem, row in SOUND.items()}


def response(stage, n):
    parent = linked.current.cold.WORK / 'probe' / PARENT / f'r{n}'
    data = (parent / 'link.lnk').read_bytes()
    _, graph, _ = linked.current.source_graph()
    for g in graph:
        old = g['output'].replace('/', '\\').encode()
        stem = Path(g['output']).stem
        new = (f'probe\\{stage}\\r{n}\\{stem}.obj' if stem in SOUND else
               f'probe\\{PARENT}\\r{n}\\' + g['output'].replace('/', '\\')).encode()
        need(data.count(old) == 1, 'one complete original project slot')
        data = data.replace(old, new)
    for old, new in [(b' linked.lib', f' probe\\{PARENT}\\r{n}\\linked.lib'.encode()),
                     (br'bin\th03\mainl.exe', f'probe\\{stage}\\r{n}\\mainl.exe'.encode()),
                     (br'obj\th03\mainl.map', f'probe\\{stage}\\r{n}\\mainl.map'.encode())]:
        need(data.count(old) == 1, 'one original library or output slot')
        data = data.replace(old, new)
    return data


def scope(raw, original, stem):
    source, wrapper, offset, size, sites = SOUND[stem]
    need(describe_omf(raw)['module_name'].lower() == stem + '.asm' and
         payload(raw) == payload(original) and len(payload(raw)) == size + 1 and
         segment_definitions(raw) == segment_definitions(original) and
         public_offsets(raw) == public_offsets(original), 'complete native CODE, PUBLIC and segment layout')
    # The cached TC4 objects are reconstructed carriers, not shipped OMF.
    # Keep each emitter's literal stream. All actual TASM fields have a fixed
    # reviewed order, symbol index, DGROUP frame, width and native zero addend.
    fields = [dict(segment=1, site=site, location_type=1, width=2, segment_relative=True,
                   frame_method=1, frame=1, target_method=2, target=target, addend=0)
              for site, target in sites]
    need(literal_fields(raw) == fields, 'entire literal ordered native TASM field stream')
    old = {f['site']: f for f in literal_fields(original)}
    need(len(old) == len(fields) and all(old[f['site']] == f for f in fields),
         'each complete field retains its original symbol/frame identity')
    for kind in ('SEGDEF', 'GRPDEF', 'EXTDEF'):
        need([r.data for r in parse_omf(raw) if r.name == kind] ==
             [r.data for r in parse_omf(original) if r.name == kind],
             'literal original ' + kind + ' metadata; no attribute normalization')
    body = bytes(payload(raw)[1, i] for i in range(size))
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(body, offset))
    need(sum(i.size for i in instructions) == size and instructions[-1].mnemonic == 'retf' and
         payload(raw)[1, size] == 0x90, 'complete far function followed by native EVEN alignment')
    return dict(function_bytes=size, producer_alignment_bytes=1, ordered_native_fields=fields,
                retained_TC4_ordered_fields=literal_fields(original),
                retained_TC4_field_order_equal=fields == literal_fields(original),
                original_segment_group_external_metadata_equal=True)


def map_original(raw):
    for stem, (_, wrapper, _, _, _) in SOUND.items():
        old = ('M=' + stem + '.asm').encode()
        need(raw.count(old) == 3, 'complete sound CODE/DATA/BSS contribution rows')
        raw = raw.replace(old, ('M=th02/' + wrapper).encode())
    return raw


def review(stage=STAGE):
    parent = linked.review(PARENT)
    folder, path = linked.paths(stage)
    record = json.loads(path.read_bytes())
    source = sources()
    need(record['complete'] and record['stage'] == stage and record['parent'] == parent and
         record['driver_sha256'] == sha((ROOT / DRIVER).read_bytes()) and
         record['source_sha256'] == {s: sha(b) for s, b in source.items()} and len(record['rounds']) == 2,
         'current four-source/native composition bindings')
    vectors = []
    for n, row in enumerate(record['rounds'], 1):
        rd = folder / f'r{n}'
        prior = linked.current.cold.WORK / 'probe' / PARENT / f'r{n}'
        need(row['number'] == n and row['response'] == linked.pin(rd / 'link.lnk') and
             linked.current.checked(row['response']) == response(stage, n), 'actual complete ordered link response')
        expected = [(linked.tasm_command() + FLAGS + [s + '.asm', s + '.obj'], rd) for s in SOUND]
        expected += [(linked.current.native_command() + ['tlink', f'@probe\\{stage}\\r{n}\\link.lnk'],
                      linked.current.cold.WORK)]
        need(len(row['phases']) == 5 and
             [(p['argv'], p['cwd']) for p in row['phases']] ==
             [(argv, str(cwd.relative_to(ROOT))) for argv, cwd in expected] and
             all(p['returncode'] == 0 and linked.current.checked(p['log']) is not None for p in row['phases']),
             'all actual serial TASM/TLINK commands and logs')
        need(set(row['outputs']) == {s + '.obj' for s in SOUND} | {'mainl.exe', 'mainl.map'} and
             all(meta == linked.pin(rd / name) for name, meta in row['outputs'].items()), 'complete native output vector')
        vector = {name: linked.current.checked(meta) for name, meta in row['outputs'].items()}
        for stem in SOUND:
            need((rd / (stem + '.asm')).read_bytes() == source[stem].replace(b'\n', b'\r\n'),
                 'actual complete maintained source consumed by TASM')
            original = (prior / f'obj/th02/{stem}.obj').read_bytes()
            need(row['scopes'][stem] == scope(vector[stem + '.obj'], original, stem), 'complete containing ASM producer')
        target = (prior / 'bin/th03/mainl.exe').read_bytes()
        need(vector['mainl.exe'] == target and map_original(vector['mainl.map']) ==
             (prior / 'obj/th03/mainl.map').read_bytes(), 'complete original EXE and exact MAP attributes/layout')
        mz = parse_mz(vector['mainl.exe'])
        need(mz.relocations == parse_mz(target).relocations and len(mz.relocations) == 677,
             'literal ordered complete target MZ relocation vector')
        vectors.append(vector)
    need(vectors[0] == vectors[1], 'all four raw native objects and complete EXE/MAP repeat')
    return dict(stage=stage, parent=parent, native_rounds=2, sound_objects=4,
                function_bytes=124, natural_alignment_bytes=4, complete_EXE_MAP_equal=True,
                ordered_MZ_relocations=677, original_layout_attributes_equal=True,
                native_fields=record['rounds'][0]['scopes'], report_sha256=sha(path.read_bytes()),
                work=str((folder / 'r1').relative_to(ROOT)), whole_product_source_accepted=False)


def build(stage):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    parent = linked.review(PARENT)
    source = sources()
    folder, path = linked.paths(stage)
    need(not folder.exists(), 'fresh natural sound stage')
    record = dict(complete=False, stage=stage, parent=parent, driver_sha256=sha((ROOT / DRIVER).read_bytes()),
                  source_sha256={s: sha(b) for s, b in source.items()}, rounds=[])
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        folder.mkdir()
        for n in (1, 2):
            rd = folder / f'r{n}'
            rd.mkdir()
            prior = linked.current.cold.WORK / 'probe' / PARENT / f'r{n}'
            row = dict(number=n, phases=[], scopes={}, outputs={})

            def run(argv, cwd, label):
                completed = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, timeout=120)
                log = rd / (label + '.log')
                log.write_bytes(completed.stdout + completed.stderr)
                need(completed.returncode == 0, label + ': ' + log.read_text(errors='replace')[-1800:])
                row['phases'].append(dict(argv=argv, cwd=str(cwd.relative_to(ROOT)),
                                          returncode=completed.returncode, log=linked.pin(log)))

            for stem in SOUND:
                p = rd / (stem + '.asm')
                p.write_bytes(source[stem].replace(b'\n', b'\r\n'))
                os.utime(p, (946684800, 946684800))
                run(linked.tasm_command() + FLAGS + [stem + '.asm', stem + '.obj'], rd, stem)
                row['scopes'][stem] = scope((rd / (stem + '.obj')).read_bytes(),
                                            (prior / f'obj/th02/{stem}.obj').read_bytes(), stem)
            (rd / 'link.lnk').write_bytes(response(stage, n))
            row['response'] = linked.pin(rd / 'link.lnk')
            run(linked.current.native_command() + ['tlink', f'@probe\\{stage}\\r{n}\\link.lnk'],
                linked.current.cold.WORK, 'link')
            row['outputs'] = {name: linked.pin(rd / name) for name in
                              [*[s + '.obj' for s in SOUND], 'mainl.exe', 'mainl.map']}
            record['rounds'].append(row)
            path.write_text(json.dumps(record, indent=2) + '\n')
        record['complete'] = True
        path.write_text(json.dumps(record, indent=2) + '\n')
    return review(stage)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', default=STAGE)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    print(json.dumps(build(args.stage) if args.build else review(args.stage), sort_keys=True))
