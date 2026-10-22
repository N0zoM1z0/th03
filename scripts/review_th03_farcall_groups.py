#!/usr/bin/env python3
"""Read-only replay of native far-call group controls and the actual MAIN link."""
from pathlib import Path
import argparse
import hashlib
import json
import re

from lib.pc98 import parse_mz
from lib.omf import parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions, code_bytes
from review_th03_cpu_link_order import omf
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]


def need(value, message):
    if not value:
        raise ValueError(message)


def pinned(row):
    p = ROOT / row['path']
    need(not any(q.is_symlink() for q in (p, *p.parents)), 'input symlink')
    raw = p.read_bytes()
    need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], 'input drift: ' + row['path'])
    if 'mode' in row:
        need(p.stat().st_mode & 0o777 == row['mode'], 'input mode drift')
    return raw


def digest(path):
    raw = path.read_bytes()
    return dict(path=str(path.relative_to(ROOT)), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def contributions(text):
    rows = []
    for line in text.splitlines():
        m = re.fullmatch(r'\s*([0-9A-Fa-f]{4}):([0-9A-Fa-f]{4})\s+([0-9A-Fa-f]+)\s+C=(\S+)\s+S=(\S+)\s+G=(\S+)\s+M=(.*?)\s+ACBP=(\S+)\s*', line)
        if m and int(m[3], 16):
            rows.append(dict(start=int(m[1], 16) * 16 + int(m[2], 16), size=int(m[3], 16),
                             category=m[4], segment=m[5], group=m[6], module=m[7]))
    need(rows, 'no MAP contributions')
    return rows


def frame_observation(rows, caller, callee):
    def owner(address):
        hits = [r for r in rows if r['category'] == 'CODE' and r['start'] <= address < r['start'] + r['size']]
        need(len(hits) == 1, 'unique CODE owner required')
        return hits[0]
    a, b = owner(caller), owner(callee)
    first = a['segment'] if a['group'] == '(none)' else min(
        (r for r in rows if r['category'] == 'CODE' and r['group'] == a['group']), key=lambda r: r['start'])['segment']
    return dict(caller_segment=a['segment'], caller_group=a['group'], effective_first_segment=first,
                callee_segment=b['segment'], predicted_relaxed=b['segment'] == first)


def call_window(image, address):
    window = image.program_image[address:address + 5]
    need(len(window) == 5, 'complete call window')
    if window[0] == 0x9a:
        return False, int.from_bytes(window[3:5], 'little') * 16 + int.from_bytes(window[1:3], 'little'), window.hex()
    need(window[:3] == bytes.fromhex('900ee8'), 'unexpected native call encoding')
    return True, address + 5 + int.from_bytes(window[3:5], 'little', signed=True), window.hex()


def audit_native(packet, output, expected_phases, complete):
    frozen = json.loads((packet / 'freeze-result.json').read_text())
    m = json.loads(pinned(frozen['manifest']))
    for row in m['inputs']:
        pinned(row)
    done = json.loads((output / 'completion.json').read_text())
    need(done['native_invocations'] == expected_phases and done['owned_lock_released'] and done['complete'] is complete, 'terminal native state')
    if complete:
        need(not done['errors'], 'native completion errors')
    work = ROOT / m['work']
    for phase in m['phases']:
        d = json.loads((output / (phase + '-finished.json')).read_text())
        need(d['exit_code'] == 0 and not any(d[k] for k in ('poison', 'timeout', 'cleanup_uncertain', 'survivors', 'errors'))
             and d['inventory_complete'] and d['initial_inventory_complete'], 'native cleanup')
        need(json.loads((output / (phase + '-registry-transition.json')).read_text())['ok'], 'registry audit')
        q = json.loads((output / (phase + '-output.json')).read_text())
        pinned(dict(q, path=str((work / m['native_outputs'][phase]).relative_to(ROOT))))
        extra = output / (phase + '-all-outputs.json')
        if extra.exists():
            for n, q in json.loads(extra.read_text()).items():
                pinned(dict(q, path=str((work / n).relative_to(ROOT))))
    return m, work


def review(base, main_base):
    controls = []
    sources = {}
    for variant in range(1, 9):
        packet, out = base / f'native-v{variant:02d}', base / f'native-v{variant:02d}-output'
        m, work = audit_native(packet, out, 4, True)
        sources[variant] = {n: pinned(q) for n, q in m['repeat_inputs'].items()}
        proof = json.loads((out / 'object-verification.json').read_text())
        image = parse_mz((work / 'cal.exe').read_bytes())
        need(image.valid, 'invalid calibration MZ')
        rows = contributions((work / 'obj/th03/cal.map').read_text())
        obj = work / 'obj/th03/caller.obj'
        raw_object = obj.read_bytes()
        segs = segment_definitions(raw_object)
        segment = next(q for q in segs if q['name'] == 'CAL_A')
        code, _ = code_bytes(raw_object, segment['index'])
        instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(code, 0))
        original_calls = [q for q in instructions if q.mnemonic == 'lcall']
        module = parse_omf(raw_object)[0].data[1:].decode('ascii')
        _, blocks = omf(obj, [dict(module=module, segment=q['name'], start=0) for q in segs])
        fixups = {f['site']: f for block in blocks for f in block['fixups']}
        need([q['callee'] for q in proof['calls']] == ['SAME', 'CROSS'] and len(original_calls) == 2,
             'actual compiler call membership')
        calls = []
        for instruction, q in zip(original_calls, proof['calls']):
            fixup = fixups.get(instruction.address + 1, {})
            need(instruction.size == 5 and instruction.address == q['caller_relative']
                 and fixup.get('kind') == 3 and fixup.get('target') == q['callee'], 'actual external call binding')
            need(q['linked_address'] == proof['publics']['CALLER'] + instruction.address, 'linked caller offset')
            relaxed, dest, raw = call_window(image, q['linked_address'])
            need(dest == q['expected_callee'] and image.program_image[dest] == 0xcb, 'actual far-return provider binding')
            observation = frame_observation(rows, q['linked_address'], dest)
            need(observation['predicted_relaxed'] == relaxed, 'control contradicts frame hypothesis')
            calls.append(dict(callee=q['callee'], address=q['linked_address'], destination=dest,
                              native_relaxed=relaxed, linked_bytes=raw, **observation))
        need(len(calls) == 2 and len(image.relocations) == sum(not c['native_relaxed'] for c in calls), 'control call/relocation count')
        controls.append(dict(variant=variant, manifest=digest(packet / 'manifest.json'), executable=digest(work / 'cal.exe'),
                             publics=proof['publics'], calls=calls))
    deltas = []
    for a, b, expected in [(1, 2, 'cal.@l'), (2, 3, 'same.asm'), (3, 4, 'cross.asm'),
                           (3, 5, 'same.asm'), (5, 6, 'cross.asm'), (6, 7, 'caller.cpp'), (7, 8, 'same.asm')]:
        changed = [n for n in sources[a] if sources[a][n] != sources[b][n]]
        need(changed == [expected], 'uncontrolled source delta')
        deltas.append(dict(before=a, after=b, changed=changed))
    need(controls[6]['publics'] == controls[7]['publics'], 'final membership control moved addresses')
    need([c['native_relaxed'] for c in controls[6]['calls']] == [False, True]
         and [c['native_relaxed'] for c in controls[7]['calls']] == [True, False], 'final membership reversal missing')
    m, work = audit_native(main_base / 'native-v02', main_base / 'native-v02-output', 5, False)
    image = parse_mz((work / 'bin/th03/main.exe').read_bytes())
    need(image.valid, 'invalid MAIN MZ')
    target = parse_mz(read_verified_artifact(ROOT, find_artifact(load_target_manifest(ROOT / 'config/targets.toml'), 'th03-main')))
    rows = contributions((work / 'obj/th03/main.map').read_text())
    prior = json.loads((main_base / 'call-diagnosis-v01.json').read_text())
    need(hashlib.sha256((work / 'bin/th03/main.exe').read_bytes()).hexdigest() == prior['candidate_sha256'], 'MAIN diagnostic binding')
    calls = []
    for q in prior['calls']:
        relaxed, dest, raw = call_window(image, q['address'])
        target_relaxed, expected, _ = call_window(target, q['address'])
        need(target_relaxed and dest == expected, 'MAIN callee mismatch')
        observation = frame_observation(rows, q['address'], dest)
        need(observation['predicted_relaxed'] == relaxed, 'MAIN contradicts frame hypothesis')
        calls.append(dict(address=q['address'], symbol=q['symbol'], destination=dest, native_relaxed=relaxed, **observation))
    need(len(calls) == len({c['address'] for c in calls}) == 20 and sum(c['native_relaxed'] for c in calls) == 3, 'complete MAIN call cohort')
    return dict(schema='th03-farcall-effective-first-segment-review-v1', controls=controls, controlled_source_deltas=deltas,
                main_calls=calls, all36_observed_calls_fit=True, native_invocations=0, new_authored_bytes=0,
                source_acceptance=False, exact_acceptance=False, universal_linker_rule_proved=False,
                original_MAIN_physical_producer_proved=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--controls', type=Path, required=True)
    parser.add_argument('--main-link', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    a = parser.parse_args()
    result = review(a.controls.resolve(), a.main_link.resolve())
    with a.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print('PASS: 16 native control calls and 20 actual MAIN calls; no new native invocation or exact credit')


if __name__ == '__main__':
    main()
