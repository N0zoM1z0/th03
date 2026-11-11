#!/usr/bin/env python3
"""Compose maintained OP IRAND and the natural selection-state producer.

Only the containing assembler TU is rebuilt. The unchanged selected TC4 pair
and the other cold inputs retain their own complete source/native reviews.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import build_th03_op_work as cold
from build_th03_op_selection_work import REPORT as SELECTION_REPORT
from lib.omf import describe_omf, parse_omf
from lib.pc98 import parse_mz
from lib.mainl_owner_migrations import public_offsets
from build_th03_mainl_display_work import literal_fields
from probe_th03_op_irand_source import check_obj

ROOT, WORK = cold.ROOT, cold.WORK
DRIVER = 'scripts/build_th03_op_linked_current.py'
SOURCE = 'src/op/libs/random.asm'
STAGE = 'af1377o'
UNIT = 'th03-op-decoded-score-irand'


def need(value, message):
    if not value:
        raise ValueError('current OP composition: ' + message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(raw):
    return dict(bytes=len(raw), sha256=sha(raw))


def records(raw):
    return [(r.name, r.data) for r in parse_omf(raw) if r.name not in ('THEADR', 'COMENT')]


def context(stage):
    need(re.fullmatch(r'af[0-9]+[a-z]', stage), 'DOS-safe stage')
    files = cold.source_graph()
    need(all((WORK / n).read_bytes() == raw for n, raw in files.items()), 'unchanged cold source graph')
    selected = json.loads((ROOT / SELECTION_REPORT).read_bytes())
    # The acceptance caller validates this selected pair with op_select_storage.
    # Here also bind the actual objects consumed by both complete links.
    pair = [ROOT / row['outputs']['obj']['path'] for row in selected['rounds']]
    need(selected['complete'] and len(pair) == 2 and pair[0].read_bytes() == pair[1].read_bytes(),
         'two unchanged selected TC4 objects')
    base = WORK / 'probe' / stage
    rel = 'probe/' + stage
    anchor = b'include libs/master.lib/random.asm'
    need(files['th03_op.asm'].count(anchor) == 1, 'single original IRAND include')
    body = files['th03_op.asm'].replace(anchor, ('include ' + rel + '/random.asm').encode())
    response = files['obj/th03/op.@l']
    for old, new in ((b'obj\\th03\\op.obj', rel + '/op.obj'),
                     (b'obj\\th03\\seltail.obj', rel + '/seltail.obj'),
                     (b'bin\\th03\\op.exe', rel + '/op.exe'),
                     (b'obj\\th03\\op.map', rel + '/op.map')):
        need(response.count(old) == 1, 'single original link slot: ' + old.decode())
        response = response.replace(old, new.replace('/', '\\').encode())
    inputs = {'th03_op.asm': body, 'random.asm': (ROOT / SOURCE).read_bytes().replace(b'\n', b'\r\n'),
              'op.@l': response, 'seltail.obj': pair[0].read_bytes()}
    prefix = ROOT / '.analysis/toolchain/wineprefix/drive_c'
    for name in ('c0l.obj', 'emu.lib', 'mathl.lib', 'cl.lib'):
        token = name.encode()
        need(response.count(token) == 1, 'one explicit compiler input: ' + name)
        response = response.replace(token, ('C:\\TC4\\LIB\\' + name).encode())
    inputs['op.@l'] = response
    native = [sys.executable, str(ROOT / 'scripts/shared_runtime.py'), 'wine', '--']
    commands = [native + [str(prefix / 'TASM50/bin/TASM32.EXE'), '/m', '/mx', '/kh32768', '/t', '/dGAME=3',
                         (rel + '/th03_op.asm').replace('/', '\\'), (rel + '/op.obj').replace('/', '\\')],
                native + [str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x', 'tlink',
                          '@' + (rel + '/op.@l').replace('/', '\\')]]
    bindings = {n: sha(raw) for n, raw in files.items()}
    bindings.update({DRIVER: sha((ROOT / DRIVER).read_bytes()), SOURCE: sha((ROOT / SOURCE).read_bytes()),
                     SELECTION_REPORT: sha((ROOT / SELECTION_REPORT).read_bytes()),
                     '.analysis/work/op-build.json': sha((ROOT / '.analysis/work/op-build.json').read_bytes())})
    for name in ('obj/th03/op.obj', 'obj/th03/op.map', 'bin/th03/op.exe', 'bin/th03/op.target.exe'):
        bindings[str((WORK / name).relative_to(ROOT))] = sha((WORK / name).read_bytes())
    # Bind every explicit response input, including startup and the library.
    for name in re.findall(rb'[^\s,+]+\.(?:obj|lib)', files['obj/th03/op.@l'], re.I):
        path = Path(name.decode().replace('\\', '/'))
        if re.match(r'^[Cc]:/', str(path)):
            path = prefix / str(path)[3:]
        else:
            path = WORK / path
            if not path.exists() and path.name.lower() in ('c0l.obj', 'emu.lib', 'mathl.lib', 'cl.lib'):
                path = prefix / 'TC4/LIB' / path.name.upper()
        bindings[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    for path in (prefix / 'TASM50/bin/TASM32.EXE', prefix / 'TC4/BIN/TLINK.EXE',
                 ROOT / '_reference/ReC98/bin/msdos.exe', ROOT / 'scripts/shared_runtime.py'):
        bindings[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    return base, inputs, commands, bindings


def review(stage=STAGE):
    base, inputs, commands, bindings = context(stage)
    proof = json.loads((base / 'linked-build.json').read_bytes())
    need(proof['complete'] and proof['stage'] == stage and proof['inputs'] == bindings,
         'current executable/source/input bindings')
    need(proof['staged_inputs'] == {n: pin(raw) for n, raw in inputs.items()} and
         all((base / n).read_bytes() == raw for n, raw in inputs.items()), 'actual consumed snapshots and response')
    need([(p['label'], p['command'], p['cwd'], p['returncode']) for p in proof['native_phases']] ==
         [(f'r{n}-{name}', commands[i], str(WORK), 0) for n in (1, 2)
          for i, name in enumerate(('assemble', 'link'))], 'two actual serial assembler/link rounds')
    for p in proof['native_phases']:
        need(sha((base / (p['label'] + '.log')).read_bytes()) == p['log_sha256'], 'actual writer log')
    need(len(proof['rounds']) == 2 and [r['round'] for r in proof['rounds']] == [1, 2], 'complete round pair')
    target = (WORK / 'bin/th03/op.target.exe').read_bytes()
    parent = (WORK / 'obj/th03/op.obj').read_bytes()
    original_map = (WORK / 'obj/th03/op.map').read_bytes()
    vectors = []
    for row in proof['rounds']:
        need(set(row['outputs']) == {'obj', 'exe', 'map'}, 'all raw outputs')
        outputs = {kind: (base / f"r{row['round']}.{kind}").read_bytes() for kind in row['outputs']}
        need(row['outputs'] == {n: pin(raw) for n, raw in outputs.items()}, 'complete raw output bindings')
        check_obj(parent, outputs['obj'], 'probe/' + stage + '/random.asm')
        need(records(parent) == records(outputs['obj']), 'all literal native program records, including ordered fields')
        need(outputs['exe'] == target == (WORK / 'bin/th03/op.exe').read_bytes(), 'complete decoded Japanese OP')
        need(parse_mz(outputs['exe']).relocations == parse_mz(target).relocations, 'literal ordered MZ relocations')
        module = ('M=probe\\' + stage + '\\th03_op.asm').encode()
        need(outputs['map'].count(module) == 3 and
             outputs['map'].replace(module, b'M=th03_op.asm') == original_map,
             'entire original MAP; only the three containing module filenames differ')
        vectors.append(outputs)
    need(vectors[0] == vectors[1], 'all three raw outputs repeat across independent rounds')
    return proof


def scope(stage=STAGE):
    proof = review(stage)
    base = WORK / 'probe' / stage
    raw = (base / 'r1.obj').read_bytes()
    public = public_offsets(raw)['IRAND']
    need(public == dict(offset=0x1AA0, segment_index=1, group_index=0), 'complete original far IRAND boundary')
    image = parse_mz((base / 'r1.exe').read_bytes())
    body = image.program_image[0x1D12:0x1D12+42]
    fields = [f for f in literal_fields(raw) if f['segment'] == 1 and 0x1AA0 <= f['site'] < 0x1AA0+42]
    relocs = [[r.segment, r.offset] for r in image.relocations if 0x1D12 <= r.linear < 0x1D12+42]
    owner = dict(unit_id=UNIT, name='OP original master.lib far IRAND', source=SOURCE,
        object='obj/th03/op.obj', segment=0, offset=0x1D12, start=0x1D12, size=42, origin='library',
        coordinate_space='decoded-load', canonical_file_offset=None, target_sha256=sha(body), candidate_sha256=sha(body),
        ordered_relocations=relocs, ordered_native_fields=fields, procedure_count=1, procedures=['IRAND'],
        code_bytes=42, initialized_data_bytes=0, private_data_bytes=0, private_bss_bytes=0,
        abi='far Pascal, AX fifteen-bit random result; original CX/DX/FLAGS effects',
        forwarding_chain=['th03_op.asm', SOURCE])
    return dict(owners=[owner], stage=stage, proof=proof)


def build(stage):
    base, inputs, commands, bindings = context(stage)
    need(not base.exists(), 'fresh stage')
    proof = dict(complete=False, stage=stage, inputs=bindings, staged_inputs={n: pin(b) for n, b in inputs.items()},
                 native_phases=[], rounds=[])
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', MSDOS_PATH=r'C:\TC4\BIN')
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        base.mkdir(parents=True)
        for name, raw in inputs.items():
            (base / name).write_bytes(raw)
            os.utime(base / name, (cold.STAMP, cold.STAMP))
        for number in (1, 2):
            for suffix in ('obj', 'exe', 'map'):
                (base / ('op.' + suffix)).unlink(missing_ok=True)
            for index, name in enumerate(('assemble', 'link')):
                label = f'r{number}-{name}'
                run = subprocess.run(commands[index], cwd=WORK, env=env, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, timeout=120)
                (base / (label + '.log')).write_bytes(run.stdout)
                proof['native_phases'].append(dict(label=label, command=commands[index], cwd=str(WORK),
                    returncode=run.returncode, log_sha256=sha(run.stdout)))
                need(run.returncode == 0, 'native failure: ' + label)
            outputs = {}
            for suffix in ('obj', 'exe', 'map'):
                raw = (base / ('op.' + suffix)).read_bytes()
                (base / f'r{number}.{suffix}').write_bytes(raw)
                outputs[suffix] = pin(raw)
            proof['rounds'].append(dict(round=number, outputs=outputs))
            print(f'OP composed round {number} complete', flush=True)
        proof['complete'] = True
        (base / 'linked-build.json').write_text(json.dumps(proof, indent=2) + '\n')
    review(stage)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage', default=STAGE)
    parser.add_argument('--build', action='store_true')
    args = parser.parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    if args.build:
        build(args.stage)
    proof = review(args.stage)
    print(json.dumps(dict(stage=args.stage, raw_repeat_equal=True,
                         outputs_per_round=len(proof['rounds'][0]['outputs'])), indent=2))


if __name__ == '__main__':
    main()
