#!/usr/bin/env python3
"""Verify five complete MAINL functions independently of legacy trailer bytes."""
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
from probe_th03_main_bomb_rikako_cpp import segment_definitions

ROOT, need, sha = linked.ROOT, linked.need, linked.sha
DRIVER = 'scripts/build_th03_mainl_function_bodies.py'
PARENT = 'af1369m'
STAGE = 'af1371f'
FUNCTIONS = {
    'sound-mode': ('obj/th02/snd_mode.obj', 0x2C, 29),
    'sound-pmd': ('obj/th02/snd_pmdr.obj', 0x4A, 57),
    'sound-volume': ('obj/th02/snd_dlyv.obj', 0x84, 27),
    'input-sense': ('obj/th03/input_s.obj', 0x388, 417),
    'sound-reset': ('obj/th02/snd_se_r.obj', 0x65E, 11),
}
TRAILER = b'#pragma codestring "\\x90"\n'


def context():
    proof = linked.review(PARENT)
    files, graph, _ = linked.current.source_graph()
    graph = [r for r in graph if r['output'] in {o for o, _, _ in FUNCTIONS.values()}]
    need(len(graph) == 5, 'all five original first-use compiler slots')
    for row in graph:
        source = row['source']
        body = (ROOT / source).read_bytes()
        need(files[source].replace(b'\r\n', b'\n') == body and
             body.endswith(TRAILER) and body.count(TRAILER) == 1,
             'one explicit legacy trailer after the complete maintained function')
        files[source] = body[:-len(TRAILER)].replace(b'\n', b'\r\n')
    return proof, files, graph


def scope(raw, reference, size):
    image, old = payload(raw), payload(reference)
    need(old[1, size] == 0x90 and len(old) == size + 1 and
         image == {k: v for k, v in old.items() if k != (1, size)} and len(image) == size,
         'entire natural function equals the complete original prefix')
    need(literal_fields(raw) == literal_fields(reference) and
         all(f['segment'] == 1 and f['site'] + f['width'] <= size for f in literal_fields(raw)),
         'all literal ordered fields remain wholly inside the function')
    segments = segment_definitions(reference)
    segments[0] = {**segments[0], 'size': size}
    need(segment_definitions(raw) == segments and public_offsets(raw) == public_offsets(reference) and
         list(public_offsets(raw).values()) == [dict(offset=0, segment_index=1, group_index=0)] and
         [r.data for r in parse_omf(raw) if r.name in ('EXTDEF', 'GRPDEF')] ==
         [r.data for r in parse_omf(reference) if r.name in ('EXTDEF', 'GRPDEF')],
         'complete public, external, group and non-owning storage layout')
    from capstone import Cs, CS_ARCH_X86, CS_MODE_16
    instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(bytes(image[1, i] for i in range(size)), 0))
    need(sum(i.size for i in instructions) == size and instructions[-1].mnemonic == 'retf',
         'complete instruction body ends at its genuine far return')
    return dict(CODE_bytes=size, ordered_fields=len(literal_fields(raw)),
                instructions=len(instructions), legacy_trailer_accepted=False)


def review(stage=STAGE):
    proof, files, graph = context()
    folder, path = linked.paths(stage)
    record = json.loads(path.read_bytes())
    need(record['complete'] and record['stage'] == stage and record['parent'] == proof and
         record['driver_sha256'] == sha((ROOT / DRIVER).read_bytes()) and len(record['rounds']) == 2,
         'current natural-function compiler evidence')
    vectors = []
    for n, row in enumerate(record['rounds'], 1):
        rd = folder / f'r{n}'
        need(row['number'] == n and all((rd / name).read_bytes() == data for name, data in files.items()),
             'actual complete compilation snapshots; only explicit trailers omitted')
        need(len(row['phases']) == 5 and set(row['outputs']) == {r['output'] for r in graph},
             'complete five-object native round')
        vector = {}
        for g, phase in zip(graph, row['phases']):
            need(phase['argv'] == linked.project_command(g) and phase['returncode'] == 0 and
                 phase['cwd'] == str(rd.relative_to(ROOT)), 'actual original native compiler flags and cwd')
            linked.current.checked(phase['log'])
            name = g['output']
            need(row['outputs'][name] == linked.pin(rd / name), 'actual native object output')
            raw = linked.current.checked(row['outputs'][name])
            vector[name] = raw
            deps = [p.replace('\\', '/') for p in describe_omf(raw)['dependency_paths']]
            need(g['source'] in deps and g['wrapper'] in deps, 'actual maintained function source consumed')
            _, _, size = next(v for v in FUNCTIONS.values() if v[0] == name)
            expected = (ROOT / proof['work']).parent / f'r{n}' / name
            need(row['scopes'][name] == scope(raw, expected.read_bytes(), size), 'complete owned scope')
        vectors.append(vector)
    need(vectors[0] == vectors[1], 'all five raw native function objects repeat')
    return dict(stage=stage, parent=proof, scopes=record['rounds'][0]['scopes'],
                report_sha256=sha(path.read_bytes()), work=str((folder / 'r1').relative_to(ROOT)),
                function_bytes=sum(v[2] for v in FUNCTIONS.values()), procedures=5,
                legacy_trailers_accepted=False)


def build(stage):
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    proof, files, graph = context()
    folder, path = linked.paths(stage)
    need(not folder.exists(), 'fresh bounded function stage')
    record = dict(complete=False, stage=stage, parent=proof,
                  driver_sha256=sha((ROOT / DRIVER).read_bytes()), rounds=[])
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        folder.mkdir()
        for n in (1, 2):
            rd = folder / f'r{n}'
            rd.mkdir()
            for name, data in files.items():
                p = rd / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(data)
                os.utime(p, ns=(linked.current.cold.stage.base.STAMP, linked.current.cold.stage.base.STAMP))
            for name in ('obj/th02', 'obj/th03'):
                (rd / name).mkdir(parents=True, exist_ok=True)
            row = dict(number=n, phases=[], outputs={}, scopes={})
            for g in graph:
                argv = linked.project_command(g)
                run = subprocess.run(argv, cwd=rd, env=env, capture_output=True, timeout=120)
                log = rd / (Path(g['output']).stem + '.log')
                log.write_bytes(run.stdout + run.stderr)
                need(run.returncode == 0, log.read_text(errors='replace')[-1800:])
                row['phases'].append(dict(argv=argv, cwd=str(rd.relative_to(ROOT)),
                                          returncode=run.returncode, log=linked.pin(log)))
                name = g['output']
                row['outputs'][name] = linked.pin(rd / name)
                _, _, size = next(v for v in FUNCTIONS.values() if v[0] == name)
                row['scopes'][name] = scope((rd / name).read_bytes(),
                    ((ROOT / proof['work']).parent / f'r{n}' / name).read_bytes(), size)
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
