#!/usr/bin/env python3
"""Complete MAINL PI wrapper chain, decoded ownership and native CPU contracts."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import struct
import subprocess

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import DS, Probe, REVISION, sha
from review_th03_mainl_snow import u16, signed

ROOT = Path(__file__).resolve().parents[1]
CS = 0xc7e
PROOF = '.analysis/sol-mainl-cdg-load-review-20261006.json'
PROOF_SHA256 = 'b6a4f714f8853b415a2f91b3088e8a63c81a5bd00090410e9377961c672f6457'
# Original and cached coordinates are deliberately separate.
RANGES = [('palette', 0x52a, 0x529, 37, 2), ('put', 0x54f, 0x54e, 136, 6),
          ('interlace', 0x5d7, 0x5d6, 135, 6), ('load', 0xccb, 0xccb, 70, 6),
          ('quarter', 0xd11, 0xd11, 177, 8)]
HELPERS = [('graph_free', 0xfec, 76, 8), ('memcpy', 0x4b7d, 36, 0)]
MODELS = {0x17d0: ('palette_show', 0), 0x1632: ('packed_put', 10),
          0x1044: ('load_pack', 12), 0x22b2: ('heap_free', 2)}
MODULES = [('th03/pi_put.cpp', 0x529, 173), ('th03/pi_put_i.cpp', 0x5d6, 135),
           ('th03/pi_load.cpp', 0xccb, 70), ('th03/pi_put_q.cpp', 0xd11, 177)]
PROVIDERS = ['th03/pi_put.cpp', 'th02/formats/pi_put.cpp', 'th03/pi_put_i.cpp',
             'th03/formats/pi_put_i.cpp', 'th03/pi_put_q.cpp', 'th03/formats/pi_put_q.cpp',
             'th03/pi_load.cpp', 'th02/formats/pi_load.cpp', 'th02/formats/pi.h',
             'th03/formats/pi.hpp', 'libs/master.lib/pc98_gfx.hpp', 'defconv.h',
             'platform.h', 'pc98.h', 'planar.h', 'libs/master.lib/func.hpp',
             'libs/master.lib/graph_pi_free.asm', 'libs/master.lib/memheap.asm',
             'th03_mainl.asm']
LOCAL = ['src/main/formats/pi_load.cpp', 'src/main/formats/pi_load.hpp']
BUFFERS, HEADERS, PALETTE = 0x1f0e, 0x1f26, 0x141e


def analyze(image, *, original=True):
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    rows = []
    ranges = [(n, CS, a if original else b, size, cleanup) for n, a, b, size, cleanup in RANGES]
    ranges += [(n, 0, a, size, cleanup) for n, a, size, cleanup in HELPERS]
    for name, segment, start, size, cleanup in ranges:
        body = image[segment*16+start:segment*16+start+size]
        if len(body) != size:
            raise ValueError('PI complete body/far cleanup differs')
        ins = list(decoder.disasm(body, start))
        bounds = {i.address for i in ins}
        wanted = ('retf', str(cleanup) if cleanup else '')
        if sum(i.size for i in ins) != size or not ins or (ins[-1].mnemonic, ins[-1].op_str) != wanted:
            raise ValueError('PI complete body/far cleanup differs')
        edges = []
        for j, i in enumerate(ins):
            if i.mnemonic in ('ret', 'retf') and (i.mnemonic, i.op_str) != wanted:
                raise ValueError('PI interior return differs')
            if not (i.mnemonic.startswith(('j', 'loop')) or i.mnemonic in ('call', 'lcall')):
                continue
            if not i.operands or any(o.type != X86_OP_IMM for o in i.operands):
                raise ValueError('unexpected PI indirect edge')
            dest = tuple(o.imm for o in i.operands) if i.mnemonic == 'lcall' else (segment, i.operands[0].imm)
            if i.mnemonic == 'lcall':
                if dest[0] != 0 or dest[1] not in {*MODELS, *(a for _, a, _, _ in HELPERS)}:
                    raise ValueError('unknown PI far interface/helper')
            elif i.mnemonic == 'call':
                if (name != 'graph_free' or dest != (0, 0x22b2) or
                        not j or ins[j-1].bytes != b'\x0e'):
                    raise ValueError('PI near call lacks PUSH CS/far entry')
            elif dest[1] not in bounds:
                raise ValueError('PI branch enters operand/neighbor')
            edges.append(dict(instruction=i.address, kind=i.mnemonic, destination=dest))
        rows.append(dict(name=name, segment=segment, offset=start, size=size,
                         instructions=len(ins), cleanup=cleanup, sha256=sha(body), edges=edges))
    # These are neighboring observed bytes, not producer-owned source credit.
    neighbor = 0x529 if original else 0x65d
    neighbor_value = 0x90 if original else 0
    if image[CS*16+neighbor] != neighbor_value:
        raise ValueError('PI unowned neighboring byte differs')
    return dict(bodies=rows[:5], helpers=rows[5:], body_bytes=555,
                helper_bytes=112, unowned_neighbor=neighbor, unowned_neighbor_value=neighbor_value)


def header_address(slot):
    return u16(HEADERS+u16(slot*72))


def buffer_address(slot):
    return u16(BUFFERS+u16(slot*4))


def difference_partition(original, candidate):
    """Replayable classification of cached failures; never normalized equality."""
    if len(original) != len(candidate):
        raise ValueError('PI complete image lengths differ')
    differences = {at for at, (a, b) in enumerate(zip(original, candidate)) if a != b}
    scopes = [('shifted_pi', CS*16+0x529, CS*16+0x65e, 300),
              ('root_pi_calls', 0x95f0+0x186, 0x95f0+0xb3e, 10),
              ('cutscene_pi_calls', 0x95f0+0xb3e, 0x95f0+0x17b9, 3),
              ('regist_pi_calls', 0x95f0+0x189e, 0x95f0+0x233e, 6),
              ('native_snow_transitions', 0x95f0+0x24e6, 0x95f0+0x31f1, 20),
              ('unowned_dgroup_0849', DS*16+0x849, DS*16+0x84a, 1)]
    rows, covered = [], set()
    for name, start, end, count in scopes:
        offsets = sorted(at for at in differences if start <= at < end)
        if len(offsets) != count:
            raise ValueError('PI complete cached failure count differs: '+name)
        rows.append(dict(name=name, offsets=offsets, count=count))
        covered.update(offsets)
    if covered != differences:
        raise ValueError('PI cached image has unclassified changed bytes')
    return dict(image_bytes=len(original), different_bytes=len(differences), scopes=rows,
                raw_equal=False, source_acceptance=False, exact_acceptance=False)


def advance(offset, segment, amount):
    offset = u16(offset+amount)
    return offset & 15, u16(segment+(offset >> 4))


def next_top(top):
    top = u16(top+1)
    return u16(top-400) if signed(top) >= 400 else top


class PiProbe(Probe):
    """Real five callers, graph free and memcpy; four declared interfaces only."""
    def __init__(self, mz, scenario, *, original=True):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
        from unicorn import x86_const as reg
        self.uc, self.reg = Uc(UC_ARCH_X86, UC_MODE_16), reg
        self.uc.mem_map(0, 0x100000)
        image = bytearray(mz.program_image)
        for r in mz.relocations:
            at = r.segment*16+r.offset
            struct.pack_into('<H', image, at, u16(struct.unpack_from('<H', image, at)[0]+0x2000))
        self.uc.mem_write(0x20000, bytes(image))
        self.code, self.data, self.stack = 0x2c7e0, 0x2e3f0, 0x40000
        self.original = original
        for key, value in [('CS', 0x2c7e), ('DS', 0x2e3f), ('SS', 0x4000),
                           ('BP', 0x7777), ('SI', 0x1357), ('DI', 0x2468), ('ES', 0x3333),
                           ('EFLAGS', 0x202 | (0x400 if scenario.get('df') else 0))]:
            self.set(key, value)
        self.events, self.writes, self.entries, self.errors = [], [], [], []
        self.stop = False
        self.header = header_address(scenario['slot'])
        def guard(callback):
            def invoke(*args):
                try:
                    return callback(*args)
                except Exception as error:
                    self.errors.append(str(error))
                    self.uc.emu_stop()
            return invoke
        def code(uc, address, size, user):
            if address == self.code+0xff00:
                if self.get('CS') != 0x2c7e:
                    raise ValueError('PI terminal segment alias')
                self.stop = True
                uc.emu_stop()
                return
            if address-0x20000 in MODELS:
                if self.get('CS') != 0x2000:
                    raise ValueError('PI interface segment alias')
                name, cleanup = MODELS[address-0x20000]
                sp = self.get('SP')
                frame = list(struct.unpack('<'+'H'*(2+cleanup//2), uc.mem_read(self.stack+sp, 4+cleanup)))
                if frame[1] not in (0x2000, 0x2c7e):
                    raise ValueError('PI modeled return segment differs')
                self.events.append(dict(name=name, args=frame[2:]))
                if name == 'packed_put' and scenario.get('mutate') and len(self.events) == 1:
                    w, h = scenario['mutate']
                    uc.mem_write(self.data+u16(self.header+20), struct.pack('<2H', w, h))
                elif name == 'load_pack' and scenario.get('replacement'):
                    uc.mem_write(self.data+buffer_address(scenario['slot']), struct.pack('<2H', *scenario['replacement']))
                self.set('AX', scenario.get('status', 0))
                # The frozen HMEM_FREE source preserves BX/CX/ES/DS, including
                # its shared error tail; graph_free relies on that contract.
                self.set('EFLAGS', (self.get('EFLAGS') & ~1) | int(bool(scenario.get('carry'))))
                self.set('SP', sp+4+cleanup)
                self.set('CS', frame[1])
                self.set('IP', frame[0])
                return
            ranges = [(0x2c7e, self.code+(a if original else b), n) for _, a, b, n, _ in RANGES]
            ranges += [(0x2000, 0x20000+a, n) for _, a, n, _ in HELPERS]
            if not any(self.get('CS') == seg and a <= address < a+n for seg, a, n in ranges):
                raise ValueError('CPU escaped reviewed PI callers/helpers')
            if address in (0x20000+0xfec, 0x20000+0x4b7d):
                self.entries.append(address-0x20000)
        def write(uc, access, address, size, value, user):
            if self.data <= address and address+size <= self.data+65536:
                self.writes.append([address-self.data, size, value])
            elif self.stack <= address and address+size <= self.stack+65536:
                return
            else:
                raise ValueError('unexpected PI data write')
        def intr(uc, number, user):
            raise ValueError('unexpected PI interrupt')
        self.uc.hook_add(UC_HOOK_CODE, guard(code))
        self.uc.hook_add(UC_HOOK_MEM_WRITE, guard(write))
        self.uc.hook_add(UC_HOOK_INTR, guard(intr))

    def run(self, name, scenario, *, terminal=True, budget=100000):
        self.stop = False
        self.errors.clear()
        self.set('CS', 0x2c7e)
        self.set('SP', 0xffc0)
        slot = u16(scenario['slot'])
        if name == 'palette':
            args = [slot]
        elif name == 'load':
            args = [0x1234, 0x5678, slot]
        elif name == 'quarter':
            args = [u16(scenario['quarter']), slot, u16(scenario['top']), u16(scenario['left'])]
        else:
            args = [slot, u16(scenario['top']), u16(scenario['left'])]
        self.uc.mem_write(self.stack+0xffc0, struct.pack('<'+'H'*(2+len(args)), 0xff00, 0x2c7e, *args))
        start, cleanup = next((a if self.original else b, c) for n, a, b, _, c in RANGES if n == name)
        self.uc.emu_start(self.code+start, 0x100000, count=budget)
        if self.errors:
            raise ValueError(self.errors[0])
        if self.stop != terminal:
            raise ValueError('PI terminal/budget differs')
        if terminal and (self.get('SP') != 0xffc4+cleanup or self.get('DS') != 0x2e3f or
                         [self.get(r) for r in ('BP', 'SI', 'DI')] != [0x7777, 0x1357, 0x2468]):
            raise ValueError('PI far cleanup/callee-saved differs')


def scalar_rows(name, scenario):
    offset, segment = scenario['pointer']
    width, height = scenario['width'], scenario['height']
    left, top = u16(scenario['left']), u16(scenario['top'])
    if name == 'quarter':
        displacement = {1: 160, 2: 64000, 3: 64160}.get(scenario['quarter'], 0)
        offset, segment = advance(offset, segment, displacement)
    rows, counter = [], 0
    while counter < (200 if name == 'quarter' else height):
        rows.append(dict(name='packed_put', args=[320 if name == 'quarter' else width, offset, segment, top, left]))
        if scenario.get('mutate') and len(rows) == 1:
            width, height = scenario['mutate']
        top = next_top(top)
        stride = 320 if name == 'quarter' else width if name == 'interlace' else width//2
        offset, segment = advance(offset, segment, stride)
        counter = u16(counter+(2 if name == 'interlace' else 1))
        if len(rows) >= 100000:
            raise ValueError('PI scalar unbounded fixture requires explicit budget')
    return rows


def cases():
    result = []
    for name in ('put', 'interlace'):
        for width, height in [(640, 3), (3, 5), (1, 3), (0, 3), (65535, 2), (320, 0)]:
            for pointer in [(0, 0x5000), (0xfffe, 0x5000), (0xfff0, 0xffff)]:
                result.append((name, dict(slot=0, width=width, height=height, pointer=pointer, left=-7, top=399)))
        for slot, top in [(5, 800), (6, -1), (65535, 32767), (0, -32768)]:
            result.append((name, dict(slot=slot, width=8, height=3, pointer=(0xffff, 0x5000), left=641, top=top)))
        result.append((name, dict(slot=0, width=640, height=20, pointer=(3, 0x5000), left=0, top=0, mutate=(3, 3))))
    for quarter in (-1, 0, 1, 2, 3, 4, 255):
        for pointer in [(0, 0x5000), (0xfffe, 0x5000)]:
            result.append(('quarter', dict(slot=0, width=1, height=0, pointer=pointer, left=7, top=800, quarter=quarter)))
    for slot in (5, 6, 65535):
        result.append(('quarter', dict(slot=slot, width=0, height=1, pointer=(0xfff0, 0xffff), left=-8, top=32767, quarter=3)))
    for slot in (0, 5, 6, 65535):
        result.append(('palette', dict(slot=slot)))
        for status in (0, 1, 0x7fff, 0x8000, 0xffff):
            result.append(('load', dict(slot=slot, status=status, carry=bool(status & 1), pointer=(0xabcd, 0x5000))))
    for comment, machine, pointer in [(0, 0, (9, 0)), (0x8000, 0, (0, 0)),
                                      (0, 0x9000, (0, 0x5000)), (0x8000, 0x8000, (7, 0x8000))]:
        result.append(('load', dict(slot=0, comment=comment, machine=machine, pointer=pointer, status=0xffff)))
    result.append(('load', dict(slot=0, pointer=(4, 0x5000), replacement=(7, 0x7000), status=0)))
    return [(n, dict(s, df=df)) for n, s in result for df in (False, True)]


def initialize(p, scenario):
    at = p.header
    header = bytearray((i*11+17) & 255 for i in range(72))
    struct.pack_into('<3H', header, 0, 0x1234, scenario.get('comment', 0x8000), 9)
    struct.pack_into('<3H', header, 14, 8, 0x4321, scenario.get('machine', 0x9000))
    struct.pack_into('<2H', header, 20, scenario.get('width', 640), scenario.get('height', 3))
    p.uc.mem_write(p.data+at, bytes(header))
    p.uc.mem_write(p.data+buffer_address(scenario['slot']), struct.pack('<2H', *scenario.get('pointer', (0, 0x5000))))
    return bytes(p.uc.mem_read(p.data, 65536))


def matrix(mz, *, original=True):
    result = []
    for name, scenario in cases():
        p = PiProbe(mz, scenario, original=original)
        before = initialize(p, scenario)
        expected = bytearray(before)
        p.run(name, scenario)
        if name == 'palette':
            expected[PALETTE:PALETTE+48] = before[p.header+24:p.header+72]
            events = [dict(name='palette_show', args=[])]
            if p.entries != [0x4b7d] or p.get('EFLAGS') & 0x400:
                raise ValueError('PI actual memcpy entry/CLD differs')
        elif name == 'load':
            events = []
            for off, value in [(0, scenario.get('comment', 0x8000)), (14, scenario.get('machine', 0x9000))]:
                if value:
                    events.append(dict(name='heap_free', args=[value]))
                    expected[p.header+off:p.header+off+6] = bytes(6)
            offset, segment = scenario['pointer']
            if segment:
                events.append(dict(name='heap_free', args=[segment]))
            events.append(dict(name='load_pack', args=[buffer_address(scenario['slot']), 0x2e3f,
                p.header, 0x2e3f, 0x1234, 0x5678]))
            if scenario.get('replacement'):
                at = buffer_address(scenario['slot'])
                expected[at:at+4] = struct.pack('<2H', *scenario['replacement'])
            if p.entries != [0xfec] or p.get('AX') != scenario['status']:
                raise ValueError('PI native free/status propagation differs')
        else:
            events = scalar_rows(name, scenario)
            if scenario.get('mutate'):
                expected[p.header+20:p.header+24] = struct.pack('<2H', *scenario['mutate'])
        after = bytes(p.uc.mem_read(p.data, 65536))
        if p.events != events or after != bytes(expected):
            raise ValueError('PI whole DGROUP/ordered request contract differs: '+str((name, scenario)))
        if name != 'palette' and bool(p.get('EFLAGS') & 0x400) != scenario['df']:
            raise ValueError('PI wrapper/free incoming DF differs')
        followup = None
        if name == 'load':
            first_events = list(p.events)
            p.events.clear()
            p.entries.clear()
            p.run(name, scenario)
            offset, segment = scenario.get('replacement', scenario['pointer'])
            followup = ([dict(name='heap_free', args=[segment])] if segment else [])
            followup.append(events[-1])
            if (p.events != followup or p.entries != [0xfec] or p.get('AX') != scenario['status'] or
                    bytes(p.uc.mem_read(p.data, 65536)) != bytes(expected)):
                raise ValueError('PI repeat-load retained pointer/free/status contract differs')
            p.events = first_events
        result.append(dict(name=name, scenario=scenario, events=p.events, entries=p.entries,
                           followup_load=followup,
                           writes=p.writes, ax=p.get('AX') if name == 'load' else None,
                           full_dgroup_checked=True, before_sha256=sha(before), after_sha256=sha(after)))
    # Fixed headers make the ushort/even-counter boundary explicit. No runaway
    # draw is presented as a successful return or physical graphics result.
    for name in ('put', 'interlace'):
        scenario = dict(slot=0, width=3, height=65535, pointer=(0, 0x5000), top=0, left=0)
        p = PiProbe(mz, scenario, original=original)
        before = initialize(p, scenario)
        p.run(name, scenario, terminal=False, budget=2000)
        if bytes(p.uc.mem_read(p.data, 65536)) != before or not p.events:
            raise ValueError('PI high-height budget/unchanged DGROUP differs')
        # Check every observed request prefix independently, without trying
        # to construct an unbounded full interlace specification.
        short = dict(scenario, height=len(p.events)*(2 if name == 'interlace' else 1))
        if p.events != scalar_rows(name, short):
            raise ValueError('PI high-height request prefix differs')
        result.append(dict(name=name, scenario=scenario, budget=2000, terminal=False,
                           requests=len(p.events), full_dgroup_checked=True))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = (ROOT/PROOF).read_bytes()
    if sha(raw) != PROOF_SHA256:
        raise ValueError('PI prior complete CDG load proof differs')
    proof = json.loads(raw)
    inputs = {**proof['inputs'], PROOF: sha(raw), 'scripts/review_th03_mainl_pi.py': sha(Path(__file__).read_bytes())}
    providers = {p: subprocess.check_output(['git', 'show', f'{REVISION}:{p}'], cwd=ROOT/'_reference/ReC98') for p in PROVIDERS}
    local = {p: (ROOT/p).read_bytes() for p in LOCAL}
    inputs.update({p: sha(b) for p, b in local.items()})
    def verify():
        for p, digest in inputs.items():
            if sha((ROOT/p).read_bytes()) != digest:
                raise ValueError('PI input changed: '+p)
    verify()
    artifact = find_artifact(load_target_manifest(ROOT/'config/targets.toml'), 'th03-mainl')
    stored = read_verified_artifact(ROOT, artifact)
    observations = []
    maps = [p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for index, entry in enumerate(proof['observations']):
        path = entry['path']
        mz = parse_mz((ROOT/path).read_bytes())
        if not mz.valid:
            raise ValueError('PI invalid image')
        observed = dict(path=path, analysis=analyze(mz.program_image, original=index == 0),
                        cpu=matrix(mz, original=index == 0))
        if index:
            tree = Path(path).parents[2]
            for p, data in providers.items():
                cp = str(tree/p)
                cached = (ROOT/cp).read_bytes()
                inputs[cp] = sha(cached)
                wanted = (b'#include "src/main/formats/pi_load.cpp"\n' if p == 'th03/pi_load.cpp'
                          else data.replace(b'\n', b'\r\n') if p.endswith('.asm') else data)
                if cached != wanted:
                    raise ValueError('PI frozen/remapped cached provider differs: '+p)
            for p, data in local.items():
                cp = str(tree/p)
                cached = (ROOT/cp).read_bytes()
                inputs[cp] = sha(cached)
                if cached != data:
                    raise ValueError('PI maintained MAIN cached provider differs: '+p)
            rows = code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(), len(mz.program_image))
            target = parse_mz((ROOT/observations[0]['path']).read_bytes())
            observed['complete_cached_failure_partition'] = difference_partition(target.program_image, mz.program_image)
            observed['comparisons'] = {}
            for module, at, size in MODULES:
                row = next(r for r in rows if r['module'] == module and r['size'])
                if (row['segment'], row['offset'], row['size']) != (CS, at, size):
                    raise ValueError('PI complete cached MAP contribution differs')
                observed['comparisons'][module] = extent_observation(target, mz, row)
            observed['body_comparisons'] = []
            for name, original, cached, size, _ in RANGES:
                lhs = target.program_image[CS*16+original:CS*16+original+size]
                rhs = mz.program_image[CS*16+cached:CS*16+cached+size]
                observed['body_comparisons'].append(dict(name=name, original_offset=original,
                    cached_offset=cached, size=size, raw_body_equal=lhs == rhs))
                if lhs != rhs:
                    raise ValueError('PI complete shifted body differs')
            for _, at, size, _ in HELPERS:
                if target.program_image[at:at+size] != mz.program_image[at:at+size]:
                    raise ValueError('PI complete actual helper bytes differ')
            def normalized(cpu):
                return [{k: v for k, v in r.items() if k not in ('before_sha256', 'after_sha256')} for r in cpu]
            if normalized(observed['cpu']) != normalized(observations[0]['cpu']):
                raise ValueError('PI original/cached CPU contracts differ')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError('PI canonical target changed')
    for p, data in providers.items():
        if subprocess.check_output(['git', 'show', f'{REVISION}:{p}'], cwd=ROOT/'_reference/ReC98') != data:
            raise ValueError('PI frozen provider changed')
    result = dict(kind='th03-mainl-complete-pi-wrapper-chain-candidate-review',
                  observed_utc=datetime.now(timezone.utc).isoformat(), inputs=inputs,
                  providers={p: sha(d) for p, d in providers.items()},
                  producer_remap={'th03/pi_load.cpp': 'src/main/formats/pi_load.cpp'},
                  observations=observations, tools=dict(capstone=version('capstone'), unicorn=version('unicorn')),
                  diagnostic_checks_pass=True, fresh_build=False, source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print('PASS complete PI wrappers555/helper112 and explicit CPU contracts:', args.output)


if __name__ == '__main__':
    main()
