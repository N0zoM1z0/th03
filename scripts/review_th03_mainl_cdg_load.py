#!/usr/bin/env python3
"""Complete MAINL CDG loading TU: native CODE over explicit file/heap interfaces."""
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
PROOF = '.analysis/sol-mainl-cdg-put-review-20261006.json'
PROOF_SHA256 = 'bcc4dfc64bb9101360d18b1999f05457e2f637d4373e0257656923da4164968d'
RANGES = [('single', 0x73e, 138, 8), ('single_noalpha', 0x7c8, 134, 8),
          ('all', 0x84e, 230, 6), ('all_noalpha', 0x934, 28, 6),
          ('free', 0x950, 63, 2)]
MODELS = {0x966: ('open', 4), 0x8b2: ('read', 6), 0x9a2: ('seek', 6),
          0x846: ('close', 0), 0x21ae: ('alloc', 2), 0x22b2: ('free', 2)}
PROVIDERS = ['th03/cdg_load.cpp', 'th03/formats/cdg_load.cpp',
             'th03/formats/cdg.h', 'planar.h', 'pc98.h', 'platform.h',
             'libs/master.lib/master.hpp', 'libs/master.lib/func.hpp']
SLOTS, FLAG = 0x1d0e, 0x894


def analyze(image):
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    rows = []
    for name, start, size, cleanup in RANGES:
        body = image[CS * 16 + start:CS * 16 + start + size]
        if len(body) != size:
            raise ValueError('CDG loader complete body/far cleanup differs')
        ins = list(decoder.disasm(body, start))
        bounds = {i.address for i in ins}
        if (sum(i.size for i in ins) != size or not ins or
                (ins[-1].mnemonic, ins[-1].op_str) != ('retf', str(cleanup))):
            raise ValueError('CDG loader complete body/far cleanup differs')
        edges = []
        for j, i in enumerate(ins):
            if i.mnemonic in ('ret', 'retf') and (i.mnemonic, i.op_str) != ('retf', str(cleanup)):
                raise ValueError('CDG loader interior return differs')
            if not (i.mnemonic.startswith(('j', 'loop')) or i.mnemonic in ('call', 'lcall')):
                continue
            if not i.operands or any(o.type != X86_OP_IMM for o in i.operands):
                raise ValueError('unexpected CDG loader indirect edge')
            dest = tuple(o.imm for o in i.operands) if i.mnemonic == 'lcall' else (CS, i.operands[0].imm)
            if i.mnemonic == 'lcall':
                if dest[0] != 0 or dest[1] not in MODELS:
                    raise ValueError('unknown CDG loader far interface')
            elif i.mnemonic == 'call':
                wanted = 0x84e if name == 'all_noalpha' else 0x950
                if dest != (CS, wanted) or not j or ins[j-1].bytes != b'\x0e':
                    raise ValueError('CDG loader near call lacks PUSH CS/far entry')
            elif dest[1] not in bounds:
                raise ValueError('CDG loader branch enters operand/neighbor')
            edges.append(dict(instruction=i.address, kind=i.mnemonic, destination=dest))
        rows.append(dict(name=name, offset=start, size=size, cleanup=cleanup,
                         sha256=sha(body), instructions=len(ins), edges=edges))
    return dict(bodies=rows, contribution_bytes=593, instructions=sum(r['instructions'] for r in rows))


def slot_address(slot):
    return u16(SLOTS + u16(slot * 16))


def header(size=4, count=1, alpha=0, colors=0):
    return struct.pack('<5H2B2H', size, 32, 2, 80, 1, count, 0x7f, alpha, colors)


class Interfaces:
    """No real DOS or heap. Only header bytes are injected; payload reads are requests.

    Repeated allocation return segments deliberately alias synthetic buffers.
    No payload bytes, allocator state, open file, or physical memory outcome is proved.
    """
    def __init__(self, scenario, read, write):
        self.scenario, self.read, self.write = scenario, read, write
        self.events, self.reads, self.allocations = [], 0, 0

    def call(self, name, args):
        self.events.append(dict(name=name, args=args))
        result = self.scenario.get('status', 0)
        if name == 'read':
            amount, offset, segment = args
            if self.reads == 0:
                if amount != 16 or segment != 0x2e3f:
                    raise ValueError('CDG modeled header pointer/size differs')
                data = self.scenario.get('header')
                if data is not None:
                    if len(data) > 16 or offset + len(data) > 65536:
                        raise ValueError('CDG header injection exceeds bounded DGROUP')
                    self.write(offset, data)
            self.reads += 1
        elif name == 'alloc':
            values = self.scenario.get('allocations', [0x5000, 0x7000])
            result = values[self.allocations % len(values)]
            self.allocations += 1
        return result


def scalar(before, name, scenario):
    """Source-level contract with explicit target word promotions; full DGROUP result."""
    data = bytearray(before)
    def read(at, amount):
        return bytes(data[u16(at+i)] for i in range(amount))
    def write(at, values):
        for i, b in enumerate(values):
            data[u16(at+i)] = b
    def word(at):
        return struct.unpack('<H', read(at, 2))[0]
    def store(at, value):
        write(at, struct.pack('<H', u16(value)))
    model = Interfaces(scenario, read, write)
    def free(slot):
        at = slot_address(slot)
        for field in (12, 14):
            value = word(at+field)
            if value:
                model.call('free', [value])
                store(at+field, 0)
    def load_planes(at, noalpha):
        size = word(at)
        if noalpha:
            if not name.startswith('single'):
                store(at+12, 0)
            model.call('seek', [1, size, 0])
            if name.startswith('single'):
                store(at+12, 0)
        else:
            seg = model.call('alloc', [size])
            store(at+12, seg)
            model.call('read', [size, 0, seg])
        size = u16(word(at)*4)
        seg = model.call('alloc', [size])
        store(at+14, seg)
        model.call('read', [u16(word(at)*4), 0, seg])
    slot = scenario['slot']
    first = slot_address(slot)
    if name == 'free':
        free(slot)
    elif name.startswith('single'):
        free(slot)
        model.call('open', [0x1234, 0x5678])
        model.call('read', [16, first, 0x2e3f])
        displacement = (signed(u16(scenario.get('n', 0))) * u16(word(first)*5)) & 0xffffffff
        model.call('seek', [1, displacement & 65535, displacement >> 16])
        load_planes(first, name == 'single_noalpha')
        model.call('close', [])
    else:
        if name == 'all_noalpha':
            data[FLAG] = 1
        model.call('open', [0x1234, 0x5678])
        free(slot)
        model.call('read', [16, first, 0x2e3f])
        i = 1
        while read(first+10, 1)[0] > i:
            free(u16(slot+i))
            i += 1
        i, at = 0, first
        while read(first+10, 1)[0] > i:
            for field in (0, 2, 4, 6, 8):
                store(at+field, word(first+field))
            write(at+10, read(first+10, 1))
            write(at+11, b'\x00')
            load_planes(at, bool(data[FLAG]))
            i, at = i+1, u16(at+16)
        model.call('close', [])
        if name == 'all_noalpha':
            data[FLAG] = 0
    return bytes(data), model.events


class LoadProbe(Probe):
    """Execute all five bodies and native far returns; six external bodies substituted."""
    def __init__(self, mz, scenario):
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
        for key, value in [('CS', 0x2c7e), ('DS', 0x2e3f), ('SS', 0x4000),
                           ('ES', 0x3333), ('BP', 0x7777), ('SI', 0x1357), ('DI', 0x2468),
                           ('EFLAGS', 0x202 | (0x400 if scenario.get('df') else 0))]:
            self.set(key, value)
        self.errors, self.writes, self.native_entries = [], [], []
        self.stop = False
        self.model = Interfaces(scenario, lambda at, n: bytes(self.uc.mem_read(self.data+at, n)),
                                lambda at, b: self.uc.mem_write(self.data+at, b))
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
                    raise ValueError('CDG loader terminal segment alias')
                self.stop = True
                uc.emu_stop()
                return
            if address-0x20000 in MODELS:
                if self.get('CS') != 0x2000:
                    raise ValueError('CDG loader interface segment alias')
                name, cleanup = MODELS[address-0x20000]
                sp = self.get('SP')
                frame = list(struct.unpack('<'+'H'*(2+cleanup//2), uc.mem_read(self.stack+sp, 4+cleanup)))
                if frame[1] != 0x2c7e:
                    raise ValueError('CDG loader modeled return segment differs')
                result = self.model.call(name, frame[2:])
                self.set('AX', result)
                self.set('DX', 0x55aa)
                self.set('EFLAGS', (self.get('EFLAGS') & ~1) | int(bool(scenario.get('carry'))))
                self.set('SP', sp+4+cleanup)
                self.set('CS', frame[1])
                self.set('IP', frame[0])
                return
            off = address-self.code
            if self.get('CS') != 0x2c7e or not any(a <= off < a+n for _, a, n, _ in RANGES):
                raise ValueError('CPU escaped reviewed CDG loader bodies')
            if off in (0x950, 0x84e):
                self.native_entries.append(off)
        def write(uc, access, address, size, value, user):
            if self.data <= address and address+size <= self.data+65536:
                self.writes.append([address-self.data, size, value])
            elif self.stack <= address and address+size <= self.stack+65536:
                return
            else:
                raise ValueError('unexpected CDG loader memory write')
        def intr(uc, number, user):
            raise ValueError('unexpected CDG loader interrupt')
        self.uc.hook_add(UC_HOOK_CODE, guard(code))
        self.uc.hook_add(UC_HOOK_MEM_WRITE, guard(write))
        self.uc.hook_add(UC_HOOK_INTR, guard(intr))

    def run(self, name, scenario, *, terminal=True, budget=100000):
        self.stop = False
        self.errors.clear()
        self.set('CS', 0x2c7e)
        self.set('SP', 0xffd0)
        args = [u16(scenario['slot'])]
        if name != 'free':
            args = ([u16(scenario.get('n', 0)), 0x1234, 0x5678, u16(scenario['slot'])]
                    if name.startswith('single') else [0x1234, 0x5678, u16(scenario['slot'])])
        self.uc.mem_write(self.stack+0xffd0, struct.pack('<'+'H'*(2+len(args)), 0xff00, 0x2c7e, *args))
        start, cleanup = next((a, c) for n, a, _, c in RANGES if n == name)
        self.uc.emu_start(self.code+start, 0x100000, count=budget)
        if self.errors:
            raise ValueError(self.errors[0])
        if self.stop != terminal:
            raise ValueError('CDG loader terminal/budget differs')
        if terminal and (self.get('SP') != 0xffd4+cleanup or self.get('DS') != 0x2e3f or
                         [self.get(r) for r in ('BP', 'SI', 'DI')] != [0x7777, 0x1357, 0x2468]):
            raise ValueError('CDG loader far cleanup/callee-saved differs')


def scenarios():
    cases = []
    for name in ('single', 'single_noalpha'):
        for size, n in [(4, 0), (4, 2), (13107, 1), (13108, 1), (16384, 32767),
                        (65535, -1), (65535, -32768), (0, -1)]:
            cases.append((name, dict(slot=0, header=header(size, 0), n=n)))
        for slot in (31, 32, 65535):
            cases.append((name, dict(slot=slot, header=header(), n=1)))
        for allocations in ([0, 0x7000], [0x5000, 0], [0, 0]):
            cases.append((name, dict(slot=0, header=header(), allocations=allocations, status=65535, carry=True)))
        cases.append((name, dict(slot=0, header=None, status=65535, carry=True)))
        cases.append((name, dict(slot=0, header=struct.pack('<H', 8), status=0)))
    for name in ('all', 'all_noalpha'):
        for slot, count in [(0, 0), (0, 1), (0, 2), (0, 32), (0, 255),
                            (31, 2), (65535, 3), (0xde0, 255), (0xe30, 140)]:
            cases.append((name, dict(slot=slot, header=header(count=count), count=count)))
        cases.append((name, dict(slot=0, header=header(count=2), count=2,
                                allocations=[0, 0], status=65535, carry=True)))
        cases.append((name, dict(slot=0, header=None, count=3, status=65535, carry=True)))
        cases.append((name, dict(slot=0, header=header(count=0, alpha=0xabcd, colors=0xdead), count=0)))
        cases.append((name, dict(slot=0, header=header(count=1), count=1, flag=255)))
    for slot in (0, 31, 32, 65535):
        for old in ((0, 0), (0x8000, 0), (0, 0x9000), (0x8000, 0x9000), (0x8000, 0x8000)):
            cases.append(('free', dict(slot=slot, old=old, status=65535, carry=True)))
    # Both DF states and incoming noalpha states on every base contract.
    return [(n, dict(s, df=df, flag=s.get('flag', int(df)))) for n, s in cases for df in (False, True)]


def matrix(mz):
    rows = []
    for name, scenario in scenarios():
        p = LoadProbe(mz, scenario)
        count = max(1, scenario.get('count', 1))
        for i in range(count):
            at = slot_address(scenario['slot']+i)
            data = header(count=scenario.get('count', 1), alpha=scenario.get('old', (0x8000, 0x9000))[0],
                          colors=scenario.get('old', (0x8000, 0x9000))[1])
            # Populate even wrapped/out-of-table fixtures without importing assets.
            for j, b in enumerate(data):
                p.uc.mem_write(p.data+u16(at+j), bytes([b]))
        p.uc.mem_write(p.data+FLAG, bytes([scenario['flag']]))
        before = bytes(p.uc.mem_read(p.data, 65536))
        expected, events = scalar(before, name, scenario)
        p.run(name, scenario)
        after = bytes(p.uc.mem_read(p.data, 65536))
        if after != expected or p.model.events != events:
            raise ValueError('CDG complete DGROUP/source-level interface contract differs: '+str((name, scenario)))
        if bool(p.get('EFLAGS') & 0x400) != scenario['df']:
            raise ValueError('CDG loader incoming DF differs')
        required_entries = (([0x84e] if name.startswith('all') else []) +
                            [0x950] * (count if name.startswith('all') and scenario.get('header') is not None else 1))
        if name.startswith('all') and scenario.get('header') is None:
            required_entries = [0x84e]+[0x950]*3
        if name.startswith('all') and scenario.get('count') == 0:
            required_entries = [0x84e, 0x950]
        if p.native_entries != required_entries:
            raise ValueError('CDG actual internal free/all entries differ')
        # A subsequent actual free call checks retained pointers and zeroing,
        # including count0 malformed file-header pointer words.
        follow = dict(scenario)
        expected2, events2 = scalar(after, 'free', follow)
        p.model.events.clear()
        p.run('free', follow)
        if bytes(p.uc.mem_read(p.data, 65536)) != expected2 or p.model.events != events2:
            raise ValueError('CDG retained pointer follow-up free differs')
        saved_scenario = dict(scenario)
        if isinstance(saved_scenario.get('header'), bytes):
            saved_scenario['header'] = saved_scenario['header'].hex()
        rows.append(dict(name=name, scenario=saved_scenario, events=events, followup_free=events2,
                         native_entries=required_entries, native_store_count=len(p.writes),
                         final_flag=after[FLAG], full_dgroup_checked=True,
                         before_sha256=sha(before), after_sha256=sha(after)))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = (ROOT/PROOF).read_bytes()
    if sha(raw) != PROOF_SHA256:
        raise ValueError('CDG loader prior native drawing proof differs')
    proof = json.loads(raw)
    inputs = {**proof['inputs'], PROOF: sha(raw),
              'scripts/review_th03_mainl_cdg_load.py': sha(Path(__file__).read_bytes())}
    providers = {p: subprocess.check_output(['git', 'show', f'{REVISION}:{p}'], cwd=ROOT/'_reference/ReC98')
                 for p in PROVIDERS}
    def verify():
        for p, h in inputs.items():
            if sha((ROOT/p).read_bytes()) != h:
                raise ValueError('CDG loader input changed: '+p)
    verify()
    artifact = find_artifact(load_target_manifest(ROOT/'config/targets.toml'), 'th03-mainl')
    stored = read_verified_artifact(ROOT, artifact)
    observations = []
    maps = [p for p in inputs if p.endswith('/obj/th03/mainl.map')]
    for entry in proof['observations']:
        path = entry['path']
        mz = parse_mz((ROOT/path).read_bytes())
        if not mz.valid:
            raise ValueError('CDG loader invalid image')
        observed = dict(path=path, analysis=analyze(mz.program_image), cpu=matrix(mz))
        if observations:
            tree = Path(path).parents[2]
            for p, data in providers.items():
                cp = str(tree/p)
                cached = (ROOT/cp).read_bytes()
                inputs[cp] = sha(cached)
                if cached != data:
                    raise ValueError('CDG loader frozen cached provider association differs')
            rows = code_rows((ROOT/next(p for p in maps if str(tree) in p)).read_text(), len(mz.program_image))
            row = next(r for r in rows if r['module'] == 'th03/cdg_load.cpp' and r['size'])
            if (row['segment'], row['offset'], row['size']) != (CS, 0x73e, 593):
                raise ValueError('CDG loader complete MAP contribution differs')
            target = parse_mz((ROOT/observations[0]['path']).read_bytes())
            observed['comparison'] = extent_observation(target, mz, row)
            observed['raw_difference_offsets'] = [at for at in range(0x73e, 0x98f)
                if target.program_image[CS*16+at] != mz.program_image[CS*16+at]]
            def normalized(cpu):
                return [{k: v for k, v in r.items() if k not in ('before_sha256', 'after_sha256')} for r in cpu]
            if normalized(observed['cpu']) != normalized(observations[0]['cpu']):
                raise ValueError('CDG loader target/cached CPU diagnostics differ')
        observations.append(observed)
    verify()
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError('CDG loader canonical target changed')
    for p, data in providers.items():
        if subprocess.check_output(['git', 'show', f'{REVISION}:{p}'], cwd=ROOT/'_reference/ReC98') != data:
            raise ValueError('CDG loader frozen provider changed')
    result = dict(kind='th03-mainl-complete-cdg-loading-candidate-review',
                  observed_utc=datetime.now(timezone.utc).isoformat(), inputs=inputs,
                  providers={p: sha(d) for p, d in providers.items()}, observations=observations,
                  tools=dict(capstone=version('capstone'), unicorn=version('unicorn')),
                  diagnostic_checks_pass=True, fresh_build=False, source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print('PASS complete CDG loading593 and explicit file/heap CPU contracts:', args.output)


if __name__ == '__main__':
    main()
