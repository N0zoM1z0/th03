#!/usr/bin/env python3
"""Review the complete shared CDG loader against independent OP/MAINL bindings."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
import itertools
import json
from pathlib import Path
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from inventory_rec98_th03 import frozen_files
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from replay_th03_op_score import normalized_contracts
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import Probe, REVISION, sha

ROOT = Path(__file__).resolve().parents[1]
PARENT = '.analysis/th03-op-select/sol-op-select-source-20261006/receipt.json'
PARENT_SHA = '885ecb011fd829c9da2d1272f2f571415f49e0ec71303ec9ec9e4b8d5c06b0b2'
PROVIDERS = ['th03/cdg_load.cpp', 'th03/formats/cdg_load.cpp', 'th03/formats/cdg.h',
             'planar.h', 'pc98.h', 'platform.h', 'x86real.h',
             'libs/master.lib/master.hpp', 'libs/master.lib/func.hpp']
PROFILES = {
    'op': dict(cs=0xbeb, ds=0xd7f, start=0x5da, slots=0x1aa8, flag=0x5f0,
               callbacks=(0x9a8, 0x8f4, 0x9e4, 0x888, 0x24ca, 0x25ce)),
    'mainl': dict(cs=0xc7e, ds=0xe3f, start=0x73e, slots=0x1d0e, flag=0x894,
                  callbacks=(0x966, 0x8b2, 0x9a2, 0x846, 0x21ae, 0x22b2)),
}
FUNCTIONS = [('single', 0, 138, 8), ('single_noalpha', 138, 134, 8),
             ('all', 272, 230, 6), ('all_noalpha', 502, 28, 6), ('free', 530, 63, 2)]
CALLBACKS = [('open', 4), ('read', 6), ('seek', 6), ('close', 0), ('alloc', 2), ('free', 2)]
# Independently inspected call instructions relative to each complete carrier.
CALL_SITES = {'open': [29, 167, 282], 'read': [38, 92, 122, 176, 256, 310, 418, 468],
              'seek': [70, 208, 221, 438], 'alloc': [77, 103, 237, 403, 449],
              'close': [127, 261, 491], 'free': [567]}
INTERNAL = {12: 'free', 150: 'free', 292: 'free', 333: 'free', 518: 'all'}


def u16(value):
    return value & 65535


def signed(value):
    return (value & 32767) - (value & 32768)


def slot_address(profile, slot):
    return u16(profile['slots'] + u16(slot * 16))


def header(size=4, count=1, alpha=0, colors=0):
    return struct.pack('<5H2B2H', size, 32, 2, 80, 1, count, 0x7f, alpha, colors)


def analyze(image, profile):
    cs, start = profile['cs'], profile['start']
    entries = {(cs, start+r): n for n, r, _, _ in FUNCTIONS}
    models = {(0, a): (n, z) for a, (n, z) in zip(profile['callbacks'], CALLBACKS)}
    expected = {start+r: dest for dest, (n, _) in models.items() for r in CALL_SITES[n]}
    expected.update({start+r: next(k for k, v in entries.items() if v == n) for r, n in INTERNAL.items()})
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    bounds, returns, calls, bodies, found = set(), {}, {}, [], set()
    for name, relative, size, cleanup in FUNCTIONS:
        a = start+relative
        body = image[cs*16+a:cs*16+a+size]
        ins = list(decoder.disasm(body, a))
        local = {i.address for i in ins}
        if len(body) != size or not ins or sum(i.size for i in ins) != size or (ins[-1].mnemonic, ins[-1].op_str) != ('retf', str(cleanup)):
            raise ValueError('CDG complete native body/far cleanup differs: '+name)
        bounds.update((cs, i.address) for i in ins)
        edges = []
        for j, i in enumerate(ins):
            if i.mnemonic in ('ret', 'retf'):
                if (i.mnemonic, i.op_str) != ('retf', str(cleanup)):
                    raise ValueError('CDG interior return differs')
                returns[(cs, i.address)] = cleanup
            if i.mnemonic in ('int', 'in', 'out', 'iret'):
                raise ValueError('CDG unexpected device instruction')
            if not (i.mnemonic.startswith(('j', 'loop')) or i.mnemonic in ('call', 'lcall', 'ljmp')):
                continue
            if not i.operands or any(o.type != X86_OP_IMM for o in i.operands):
                raise ValueError('CDG unexpected indirect edge')
            dest = tuple(o.imm for o in i.operands) if i.mnemonic == 'lcall' else (cs, i.operands[0].imm)
            if i.mnemonic in ('call', 'lcall'):
                if expected.get(i.address) != dest or i.mnemonic != ('call' if dest in entries else 'lcall'):
                    raise ValueError('CDG unknown caller/destination')
                if dest in entries and (not j or ins[j-1].bytes != b'\x0e'):
                    raise ValueError('CDG internal near call lacks original PUSH CS bridge')
                found.add(i.address)
                calls[(cs, i.address+i.size)] = dest
            elif i.mnemonic == 'ljmp' or dest[1] not in local:
                raise ValueError('CDG branch enters operand/neighbor')
            edges.append(dict(site=i.address, kind=i.mnemonic, destination=list(dest)))
        bodies.append(dict(name=name, segment=cs, offset=a, size=size, cleanup=cleanup,
                           sha256=sha(body), instructions=len(ins), edges=edges))
    if found != set(expected):
        raise ValueError('CDG complete call set differs')
    return dict(bodies=bodies, bounds=bounds, returns=returns, entries=entries, calls=calls, models=models)


class CDGSpec:
    """Scalar CDG algorithm; flat synthetic file writes and segment replies only."""
    def __init__(self, before, profile, scenario):
        self.memory = bytearray(before)
        self.p, self.s = profile, scenario
        self.data = (0x2000+profile['ds'])*16
        self.events, self.writes, self.external = [], [], []
        self.native = Counter()
        self.reads = self.allocations = 0

    def dg(self, at, width=2):
        a = self.data+u16(at)
        return int.from_bytes(self.memory[a:a+width], 'little')

    def store(self, at, width, value):
        a, value = self.data+u16(at), value & ((1 << (8*width))-1)
        self.memory[a:a+width] = value.to_bytes(width, 'little')
        self.writes.append((a, width, value))

    def call(self, name, args):
        event = dict(name=name, args=args)
        result = self.s['status']
        if name == 'alloc':
            values = self.s['allocations']
            result = values[self.allocations % len(values)]
            self.allocations += 1
            event['reply'] = result
        if name == 'read':
            amount, offset, segment = args
            if self.reads == 0:
                if amount != 16 or segment != self.p['ds']+0x2000:
                    raise ValueError('CDG scalar header pointer/size differs')
                data = bytes.fromhex(self.s['header']) if self.s['header'] is not None else b''
            else:
                data = bytes.fromhex(self.s['payload'])[:amount]
            self.reads += 1
            event['bytes'] = data.hex()
            a = segment*16+offset
            for i, b in enumerate(data):
                self.memory[a+i] = b
                self.external.append((a+i, 1, b))
        self.events.append(event)
        return result

    def invoke(self, name):
        self.native[name] += 1
        slot = self.s['slot']
        if name == 'free':
            self.free_slot(slot)
            return
        if name == 'all_noalpha':
            self.store(self.p['flag'], 1, 1)
            self.invoke('all')
            self.store(self.p['flag'], 1, 0)
            return
        first = slot_address(self.p, slot)
        if name.startswith('single'):
            self.free_slot(slot, native=True)
            self.call('open', [0x1234, 0x5678])
            self.call('read', [16, first, self.p['ds']+0x2000])
            displacement = (signed(u16(self.s['n'])) * u16(self.dg(first)*5)) & 0xffffffff
            self.call('seek', [1, displacement & 65535, displacement >> 16])
            self.planes(first, name == 'single_noalpha', single=True)
        else:
            self.call('open', [0x1234, 0x5678])
            self.free_slot(slot, native=True)
            self.call('read', [16, first, self.p['ds']+0x2000])
            i = 1
            while self.dg(first+10, 1) > i:
                self.free_slot(u16(slot+i), native=True)
                i += 1
            i, at = 0, first
            while self.dg(first+10, 1) > i:
                for field in (0, 2, 4, 6, 8):
                    self.store(at+field, 2, self.dg(first+field))
                self.store(at+10, 1, self.dg(first+10, 1))
                self.store(at+11, 1, 0)
                self.planes(at, bool(self.dg(self.p['flag'], 1)), single=False)
                i, at = i+1, u16(at+16)
        self.call('close', [])

    def free_slot(self, slot, native=False):
        if native:
            self.native['free'] += 1
        at = slot_address(self.p, slot)
        for field in (12, 14):
            value = self.dg(at+field)
            if value:
                self.call('free', [value])
                self.store(at+field, 2, 0)

    def planes(self, at, noalpha, single):
        if noalpha:
            if not single:
                self.store(at+12, 2, 0)
            self.call('seek', [1, self.dg(at), 0])
            if single:
                self.store(at+12, 2, 0)
        else:
            segment = self.call('alloc', [self.dg(at)])
            self.store(at+12, 2, segment)
            self.call('read', [self.dg(at), 0, self.dg(at+12)])
        segment = self.call('alloc', [u16(self.dg(at)*4)])
        self.store(at+14, 2, segment)
        self.call('read', [u16(self.dg(at)*4), 0, self.dg(at+14)])


class CDGProbe(Probe):
    """Unmodified native CODE/returns with complete instruction and frame guards."""
    def __init__(self, mz, profile, scenario):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR
        from unicorn import x86_const as reg
        self.uc, self.reg = Uc(UC_ARCH_X86, UC_MODE_16), reg
        self.uc.mem_map(0, 0x100000)
        image = bytearray(mz.program_image)
        for r in mz.relocations:
            at = r.segment*16+r.offset
            struct.pack_into('<H', image, at, u16(struct.unpack_from('<H', image, at)[0]+0x2000))
        self.uc.mem_write(0x20000, bytes(image))
        self.p, self.s, self.stack = profile, scenario, 0x40000
        self.code, self.data = (0x2000+profile['cs'])*16, (0x2000+profile['ds'])*16
        self.uc.mem_write(self.stack, bytes([0xa5])*65536)
        for i in range(max(1, scenario['count'])):
            at = slot_address(profile, scenario['slot']+i)
            raw = header(count=scenario['count'], alpha=scenario['old'][0], colors=scenario['old'][1])
            # Native metadata addresses wrap their 16-bit effective offsets.
            for field, width in [(a, 2) for a in (0, 2, 4, 6, 8, 12, 14)]+[(10, 1), (11, 1)]:
                self.uc.mem_write(self.data+u16(at+field), raw[field:field+width])
        self.uc.mem_write(self.data+profile['flag'], bytes([scenario['flag']]))
        for key, value in dict(DS=0x2000+profile['ds'], SS=0x4000, ES=0x3333,
                               BP=0x7777, SI=0x1357, DI=0x2468, BX=0xbeef).items():
            self.set(key, value)
        self.set('EFLAGS', 2 | (0x200 if scenario['if'] else 0) | (0x400 if scenario['df'] else 0))
        self.meta = analyze(mz.program_image, profile)
        self.rows = {(r['segment'], r['offset']): r for r in self.meta['bodies']}
        self.events, self.writes, self.external, self.errors, self.frames = [], [], [], [], []
        self.native, self.visited = Counter(), set()
        self.reads = self.allocations = 0
        self.position = None

        def guard(fn):
            def invoke(*args):
                try:
                    return fn(*args)
                except Exception as error:
                    self.errors.append(str(error))
                    self.uc.emu_stop()
            return invoke

        def code(uc, address, size, user):
            seg = self.get('CS')-0x2000
            off = address-self.get('CS')*16
            position = self.position = (seg, off)
            if self.get('SS') != 0x4000:
                raise ValueError('CDG stack segment alias')
            if address == self.code+0xff00:
                f = self.top
                if seg != profile['cs'] or self.get('SP') != f['sp']+4+f['cleanup'] or self.frames or any(self.get(r) != v for r, v in f['saved'].items()):
                    raise ValueError('CDG terminal far frame differs')
                self.stop = True
                uc.emu_stop()
                return
            if self.frames and position == self.frames[-1]['ret']:
                f = self.frames.pop()
                if self.get('SP') != f['sp']+4+f['cleanup'] or any(self.get(r) != v for r, v in f['saved'].items()):
                    raise ValueError('CDG native callback return differs')
            if position in self.meta['bounds']:
                self.visited.add(position)
                if position in self.meta['entries']:
                    row = self.rows[position]
                    self.native[row['name']] += 1
                    if self.entered:
                        sp = self.get('SP')
                        ip, cs = struct.unpack('<HH', uc.mem_read(self.stack+sp, 4))
                        ret = (cs-0x2000, ip)
                        if self.meta['calls'].get(ret) != position:
                            raise ValueError('CDG internal PUSH CS/far caller frame differs')
                        self.frames.append(dict(sp=sp, ret=ret, cleanup=row['cleanup'],
                                                saved={r: self.get(r) for r in ('BP', 'SI', 'DI', 'DS')}))
                    self.entered = True
                if position in self.meta['returns']:
                    f = self.frames[-1] if self.frames else self.top
                    sp = self.get('SP')
                    ip, cs = struct.unpack('<HH', uc.mem_read(self.stack+sp, 4))
                    if sp != f['sp'] or (cs-0x2000, ip) != f['ret'] or any(self.get(r) != v for r, v in f['saved'].items()):
                        raise ValueError('CDG native far return stack differs')
                return
            if position not in self.meta['models']:
                raise ValueError('CDG escape/operand boundary differs: '+str(position))
            name, cleanup = self.meta['models'][position]
            sp = self.get('SP')
            frame = struct.unpack('<'+'H'*(2+cleanup//2), uc.mem_read(self.stack+sp, 4+cleanup))
            if self.meta['calls'].get((frame[1]-0x2000, frame[0])) != position:
                raise ValueError('CDG foreign caller frame differs')
            args = list(frame[2:])
            event, result = dict(name=name, args=args), scenario['status']
            if name == 'alloc':
                values = scenario['allocations']
                result = values[self.allocations % len(values)]
                self.allocations += 1
                event['reply'] = result
            if name == 'read':
                amount, offset, segment = args
                if self.reads == 0:
                    if amount != 16 or segment != profile['ds']+0x2000:
                        raise ValueError('CDG native header pointer/size differs')
                    raw = bytes.fromhex(scenario['header']) if scenario['header'] is not None else b''
                else:
                    raw = bytes.fromhex(scenario['payload'])[:amount]
                self.reads += 1
                event['bytes'] = raw.hex()
                a = segment*16+offset
                if len(raw) > amount or a+len(raw) > 0x100000 or (raw and (a < 0x20000+len(image) and a+len(raw) > 0x20000 and not self.data <= a <= self.data+65536)):
                    raise ValueError('CDG synthetic file injection exceeds request/aliases CODE')
                if raw:
                    uc.mem_write(a, raw)
                    self.external.extend((a+i, 1, b) for i, b in enumerate(raw))
            self.events.append(event)
            self.set('AX', result)
            self.set('DX', 0x55aa)
            self.set('EFLAGS', (self.get('EFLAGS') & ~1) | int(scenario['carry']))
            self.set('SP', sp+4+cleanup)
            self.set('CS', frame[1])
            self.set('IP', frame[0])

        def write(uc, access, address, size, value, user):
            if self.stack <= address and address+size <= self.stack+65536:
                return
            if self.position not in self.meta['bounds'] or not self.data <= address or address+size > self.data+65536 or size not in (1, 2):
                raise ValueError('CDG native physical store span differs')
            self.writes.append((address, size, value & ((1 << (size*8))-1)))

        def intr(*args):
            raise ValueError('CDG unexpected interrupt')

        # RETF runs unchanged. No memory-read hook (known Unicorn regression).
        self.uc.hook_add(UC_HOOK_CODE, guard(code))
        self.uc.hook_add(UC_HOOK_MEM_WRITE, guard(write))
        self.uc.hook_add(UC_HOOK_INTR, guard(intr))

    def run(self, name, budget=250000):
        self.stop = self.entered = False
        self.errors.clear()
        row = next(r for r in self.meta['bodies'] if r['name'] == name)
        args = [u16(self.s['slot'])]
        if name != 'free':
            args = ([u16(self.s['n']), 0x1234, 0x5678, u16(self.s['slot'])]
                    if name.startswith('single') else [0x1234, 0x5678, u16(self.s['slot'])])
        self.set('CS', self.p['cs']+0x2000)
        self.set('SP', 0xffd0)
        self.uc.mem_write(self.stack+0xffd0, struct.pack('<'+'H'*(2+len(args)), 0xff00, self.p['cs']+0x2000, *args))
        self.top = dict(sp=0xffd0, ret=(self.p['cs'], 0xff00), cleanup=row['cleanup'],
                        saved={r: self.get(r) for r in ('BP', 'SI', 'DI', 'DS')})
        self.uc.emu_start(self.code+row['offset'], 0x100000, count=budget)
        if self.errors:
            raise ValueError(self.errors[0])
        if not self.stop:
            raise ValueError('CDG terminal/instruction budget differs')


def scenario(**kw):
    s = dict(slot=0, n=0, count=1, old=[0x8000, 0x9000], header=header().hex(),
             payload='', allocations=[0x5000, 0x7000], flag=0, status=0, carry=False,
             **{'if': True, 'df': False})
    s.update(kw)
    return s


def observe(mz, profile, name, s, follow=True):
    p = CDGProbe(mz, profile, s)
    before = bytes(p.uc.mem_read(0, 0x100000))
    spec = CDGSpec(before, profile, s)
    sequence = [name, 'free'] if follow else [name]
    for function in sequence:
        spec.invoke(function)
        p.run(function)
    for label, actual, expected in [('events', p.events, spec.events), ('writes', p.writes, spec.writes),
                                     ('external', p.external, spec.external), ('native', p.native, spec.native)]:
        if actual != expected:
            raise ValueError('CDG scalar '+label+' differs: '+str((name, s, actual, expected))[:2000])
    actual = bytes(p.uc.mem_read(0, 0x100000))
    if actual[:p.stack] != spec.memory[:p.stack] or actual[p.stack+65536:] != spec.memory[p.stack+65536:]:
        raise ValueError('CDG full physical memory preservation differs')
    if bool(p.get('EFLAGS') & 0x200) != s['if'] or bool(p.get('EFLAGS') & 0x400) != s['df']:
        raise ValueError('CDG IF/DF differs')
    return dict(function=name, scenario=s, sequence=sequence, native_entries=dict(p.native),
                events=p.events, stores=p.writes, external_inputs=p.external,
                visited=[list(a) for a in sorted(p.visited)], memory_before_sha256=sha(before),
                memory_after_sha256=sha(spec.memory), final_flag=spec.dg(profile['flag'], 1))


def cases(profile):
    base = []
    for name in ('single', 'single_noalpha'):
        for size, n in [(4, 0), (4, 2), (13107, 1), (13108, 1), (16384, 32767),
                        (65535, -1), (65535, -32768), (0, -1)]:
            base.append((name, scenario(header=header(size, 0).hex(), n=n)))
        for slot in (31, 32, 65535, ((65535-profile['slots']) & 65535)//16):
            base.append((name, scenario(slot=slot, n=1)))
        for values in ([0, 0x7000], [0x5000, 0], [0, 0], [profile['ds']+0x2000, 0x7000]):
            base.append((name, scenario(allocations=values, status=65535, carry=True, payload='a17e36c4')))
        for raw in (None, '0800'):
            base.append((name, scenario(header=raw, status=65535, carry=True)))
    for name in ('all', 'all_noalpha'):
        for slot, count in [(0, 0), (0, 1), (0, 2), (0, 32), (0, 255), (31, 2), (65535, 3),
                            (((65535-profile['slots']) & 65535)//16, 3),
                            (u16(profile['flag']-profile['slots'])//16, 2)]:
            base.append((name, scenario(slot=slot, count=count, header=header(count=count).hex())))
        base.append((name, scenario(count=2, header=header(count=2).hex(), allocations=[0, 0], status=65535, carry=True, payload='a17e36c4')))
        base.append((name, scenario(count=3, header=None, status=65535, carry=True)))
        base.append((name, scenario(count=0, header=header(count=0, alpha=0xabcd, colors=0xdead).hex())))
        base.append((name, scenario(flag=255, payload='a17e36c4')))
    for slot, old in itertools.product((0, 31, 32, 65535),
                                       ([0, 0], [0x8000, 0], [0, 0x9000], [0x8000, 0x9000], [0x8000, 0x8000])):
        base.append(('free', scenario(slot=slot, old=old, status=65535, carry=True)))
    return [(n, dict(s, **{'if': irq, 'df': df}, flag=s['flag'] or int(df)))
            for n, s in base for irq, df in itertools.product((False, True), repeat=2)]


def matrix(mz, profile):
    rows = []
    for n, s in cases(profile):
        rows.append(observe(mz, profile, n, s))
    return rows


def coverage(meta, rows):
    visited = {tuple(a) for r in rows for a in r['visited']}
    result = dict(instructions=len(meta['bounds']), visited=len(meta['bounds'] & visited),
                  unvisited=[list(a) for a in sorted(meta['bounds']-visited)])
    if result['unvisited']:
        raise ValueError('CDG complete native instruction coverage differs: '+str(result))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = (ROOT/PARENT).read_bytes()
    if sha(raw) != PARENT_SHA:
        raise ValueError('CDG previous OP source proof differs')
    parent = json.loads(raw)
    inputs = dict(parent['inputs'])
    inputs[PARENT] = sha(raw)
    for p in ('scripts/review_th03_shared_cdg_load.py', 'scripts/probe_th03_unicorn_far_return.py',
              '.analysis/sol-op-cdg-initial-ghidra-check-20261006.log',
              '.analysis/sol-shared-cdg-mainl-initial-ghidra-check-20261006.log'):
        inputs[p] = sha((ROOT/p).read_bytes())
    def verify():
        for p, h in inputs.items():
            if sha((ROOT/p).read_bytes()) != h:
                raise ValueError('CDG prerequisite/input changed: '+p)
    verify()
    frozen = frozen_files(REVISION)
    observations = {}
    stored = {}
    for art, profile in PROFILES.items():
        artifact = find_artifact(load_target_manifest(ROOT/'config/targets.toml'), 'th03-'+art)
        stored[art] = read_verified_artifact(ROOT, artifact)
        target_path = f'.analysis/th03-diet/sol-diet-restoration-20261006-b/{art}.exe'
        paths = [target_path]+[f'.analysis/th03-op-select/sol-op-select-source-20261006/round{n}/source/bin/th03/{art}.exe' for n in (1, 2)]
        observations[art] = []
        for number, path in enumerate(paths):
            inputs[path] = sha((ROOT/path).read_bytes())
            mz = parse_mz((ROOT/path).read_bytes())
            if not mz.valid:
                raise ValueError('CDG invalid image')
            meta = analyze(mz.program_image, profile)
            item = dict(path=path, bodies=meta['bodies'])
            if number:
                tree = Path(path).parents[2]
                for p in PROVIDERS:
                    cp = str(tree/p)
                    inputs[cp] = sha((ROOT/cp).read_bytes())
                    if inputs[cp] != sha(frozen[p]):
                        raise ValueError('CDG frozen provider differs: '+p)
                object_path = str(tree/'obj/th03/cdg_load.obj')
                inputs[object_path] = sha((ROOT/object_path).read_bytes())
                obj = describe_omf((ROOT/object_path).read_bytes())
                if not obj['valid'] or obj['dependency_timestamp_normalized_sha256'] != parent['rounds'][number-1]['all_objects']['obj/th03/cdg_load.obj']:
                    raise ValueError('CDG producer OMF differs')
                item['object'] = dict(path=object_path, normalized_sha256=obj['dependency_timestamp_normalized_sha256'], translator_comments=obj['translator_comments'])
                mp = str(tree/f'obj/th03/{art}.map')
                inputs[mp] = sha((ROOT/mp).read_bytes())
                row = next(r for r in code_rows((ROOT/mp).read_text(), len(mz.program_image)) if r['module'] == 'th03/cdg_load.cpp' and r['size'])
                if (row['segment'], row['offset'], row['size']) != (profile['cs'], profile['start'], 593):
                    raise ValueError('CDG current complete MAP contribution differs')
                target = parse_mz((ROOT/target_path).read_bytes())
                item['comparisons'] = {n: extent_observation(target, mz, dict(segment=profile['cs'], offset=profile['start']+a, start=profile['cs']*16+profile['start']+a, size=z)) for n, a, z, _ in FUNCTIONS}
                item['carrier'] = extent_observation(target, mz, row)
                if any(not r['raw_slice_equal'] or not r['ordered_relocations_equal'] for r in [*item['comparisons'].values(), item['carrier']]):
                    raise ValueError('CDG original raw/ordered comparison differs')
                links = {}
                for product in ('op', 'main', 'mainl'):
                    lp = str(tree/f'obj/th03/{product}.@l')
                    inputs[lp] = sha((ROOT/lp).read_bytes())
                    links[product] = 'obj\\th03\\cdg_load.obj' in (ROOT/lp).read_text()
                if links != dict(op=True, main=False, mainl=True):
                    raise ValueError('CDG shared physical-object link ownership differs')
                item['links'] = links
            item['cpu'] = matrix(mz, profile)
            item['coverage'] = coverage(meta, item['cpu'])
            if number and normalized_contracts(item['cpu']) != normalized_contracts(observations[art][0]['cpu']):
                raise ValueError('CDG target/cold scalar contracts differ')
            observations[art].append(item)
            print('PASS CDG', art, path, len(item['cpu']), 'cases', item['coverage'], flush=True)
    verify()
    final = frozen_files(REVISION)
    for p in PROVIDERS:
        if final[p] != frozen[p]:
            raise ValueError('CDG frozen provider changed')
    for art in PROFILES:
        artifact = find_artifact(load_target_manifest(ROOT/'config/targets.toml'), 'th03-'+art)
        if read_verified_artifact(ROOT, artifact) != stored[art]:
            raise ValueError('CDG canonical target changed')
    report = dict(kind='th03-shared-complete-cdg-loading-native-review', observed_utc=datetime.now(timezone.utc).isoformat(), inputs=inputs,
                  observations=observations, tools=dict(capstone=version('capstone'), unicorn=version('unicorn')),
                  diagnostic_checks_pass=True, source_acceptance=False, exact_acceptance=False, new_build=False,
                  notes='Five complete functions593bytes independently bound for OP and MAINL, one frozen SHARED OMF linked to both and absent from MAIN. Original raw slices and ordered relocation rows compared without sorting. Original near PUSH-CS bridges and all RETF/Pascal frames, ordered native stores/callback requests/explicit bounded synthetic input writes and physical1MiB outside64KiBstack checked. No assets/DOS/heap implementation/CRT/header/canonical packed storage/fullproduct/exact credit.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('PASS complete shared CDG loader diagnostics; exact open')


if __name__ == '__main__':
    main()
