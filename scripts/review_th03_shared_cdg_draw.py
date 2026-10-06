#!/usr/bin/env python3
"""Complete shared CDG blitters: independent bindings, SMC and flat operands."""
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import itertools
import json
from pathlib import Path
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM, X86_OP_MEM
from inventory_rec98_th03 import frozen_files
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from replay_th03_op_score import normalized_contracts
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import Probe, REVISION, sha

ROOT = Path(__file__).resolve().parents[1]
PARENT = '.analysis/th03-shared-cdg-load/sol-shared-cdg-load-source-20261006-c/receipt.json'
PARENT_SHA = '3a299bf3d442ba49e4856f6226ad0ecda5b71ae7760cbf3d6ec6d97ca9a11a99'
PROFILES = {
    'op': dict(cs=0xbeb, ds=0xd7f, slots=0x1aa8, lut=0x1e70, color=0xec6,
               starts=(0x170, 0x224, 0xc46)),
    'mainl': dict(cs=0xc7e, ds=0xe3f, slots=0x1d0e, lut=0x20d6, color=0xc36,
                  starts=(0x1f4, 0x2a8, 0xf32)),
}
FUNCTIONS = [('alpha', 179), ('hflip', 201), ('noalpha', 113)]
# Relative immediate-word destinations in original write order, independently
# read from the three complete bodies. MOV operands retain their original size.
PATCHES = {'alpha': [120, 113, 99, 125, 95],
           'hflip': [129, 169, 107, 151, 103, 147], 'noalpha': [71]}
PATCH_WRITERS = {'alpha': [29, 44, 51, 55, 65],
                 'hflip': [46, 50, 54, 59, 69, 73], 'noalpha': [29]}
PROVIDERS = ['th03/cdg_put.asm', 'th03/formats/cdg_put.asm', 'th03/cdg_p_na.asm',
             'th03/formats/cdg.h', 'th03/formats/cdg.inc', 'th03/formats/cdg[bss].asm',
             'th03/formats/hfliplut.h', 'th03/formats/hfliplut[bss].asm',
             'pc98.inc', 'libs/master.lib/master.inc', 'libs/master.lib/macros.inc']


def u16(value):
    return value & 65535


def signed(value):
    return (value & 32767) - (value & 32768)


def reverse_bits(byte):
    return sum(((byte >> i) & 1) << (7-i) for i in range(8))


def analyze(image, profile):
    d = Cs(CS_ARCH_X86, CS_MODE_16)
    d.detail = True
    cs = profile['cs']
    bodies, bounds, returns, calls, writers = [], set(), set(), {}, {}
    for (name, z), a in zip(FUNCTIONS, profile['starts']):
        body = image[cs*16+a:cs*16+a+z]
        ins = list(d.disasm(body, a))
        local = {i.address for i in ins}
        if len(body) != z or not ins or sum(i.size for i in ins) != z or (ins[-1].mnemonic, ins[-1].op_str) != ('retf', '6'):
            raise ValueError('CDG draw complete body/far cleanup differs')
        bounds.update((cs, i.address) for i in ins)
        edges = []
        seen_writers, seen_calls, slots, lut = set(), set(), 0, 0
        for i in ins:
            if i.mnemonic in ('ret', 'retf'):
                if (i.mnemonic, i.op_str) != ('retf', '6'):
                    raise ValueError('CDG draw interior return differs')
                returns.add((cs, i.address))
            if i.mnemonic in ('int', 'in', 'iret', 'call', 'ljmp'):
                raise ValueError('CDG draw unexpected device/near/indirect edge')
            if i.address-a in PATCH_WRITERS[name]:
                index = PATCH_WRITERS[name].index(i.address-a)
                dest = a+PATCHES[name][index]
                if (i.mnemonic != 'mov' or i.operands[0].type != X86_OP_MEM or i.operands[0].size != 2
                        or i.operands[0].mem.disp != dest or i.operands[0].mem.base or i.operands[0].mem.index
                        or not i.op_str.startswith('word ptr cs:')):
                    raise ValueError('CDG draw SMC writer/destination differs')
                writers[(cs, i.address)] = dest
                seen_writers.add(i.address-a)
            if i.address-a in ([22, 137] if name == 'hflip' else [22] if name == 'alpha' else [11]):
                if len(i.operands) != 2 or i.operands[1].type != X86_OP_IMM or i.operands[1].imm != profile['slots']:
                    raise ValueError('CDG draw slot binding differs')
                slots += 1
            if i.mnemonic == 'mov' and i.op_str.startswith('bx, 0x') and name == 'hflip':
                if i.operands[1].imm != profile['lut']:
                    raise ValueError('CDG draw lookup binding differs')
                lut += 1
            if not (i.mnemonic.startswith(('j', 'loop')) or i.mnemonic == 'lcall'):
                continue
            if not i.operands or any(o.type != X86_OP_IMM for o in i.operands):
                raise ValueError('CDG draw unexpected indirect edge')
            dest = tuple(o.imm for o in i.operands) if i.mnemonic == 'lcall' else (cs, i.operands[0].imm)
            if i.mnemonic == 'lcall':
                if name == 'noalpha' or i.address != a+11 or dest != (0, profile['color']):
                    raise ValueError('CDG draw unknown color caller')
                calls[(cs, i.address+i.size)] = dest
                seen_calls.add(i.address)
            elif dest[1] not in local:
                raise ValueError('CDG draw branch enters operand/neighbor')
            edges.append(dict(site=i.address, kind=i.mnemonic, destination=list(dest)))
        if seen_writers != {a for a in PATCH_WRITERS[name]} or slots != (2 if name == 'hflip' else 1) or lut != int(name == 'hflip') or len(seen_calls) != int(name != 'noalpha'):
            raise ValueError('CDG draw complete writer/binding/call set differs')
        for r in PATCHES[name]:
            patch = a+r
            owners = [i for i in ins if i.address+1 == patch and patch+2 == i.address+i.size]
            if len(owners) != 1 or owners[0].mnemonic != 'mov' or owners[0].operands[1].type != X86_OP_IMM:
                raise ValueError('CDG draw SMC destination is not complete MOV immediate')
        bodies.append(dict(name=name, segment=cs, offset=a, size=z, cleanup=6, sha256=sha(body),
                           instructions=len(ins), edges=edges, patches=[a+r for r in PATCHES[name]]))
    even = [a+z for a, (_, z) in zip(profile['starts'], FUNCTIONS)]
    if any(image[cs*16+a] != 0x90 for a in even):
        raise ValueError('CDG draw observed producer EVEN differs')
    return dict(bodies=bodies, bounds=bounds, returns=returns, calls=calls, writers=writers, even=even)


class DrawSpec:
    """High-level row/plane algorithm over a physical flat memory fixture."""
    def __init__(self, before, profile, initial_fs=0x4444):
        self.memory, self.p = bytearray(before), profile
        self.data = (0x2000+profile['ds'])*16
        self.code = (0x2000+profile['cs'])*16
        self.initial_fs = initial_fs
        self.trace = []
        self.graph_stores = 0
        self.final_es = self.final_fs = None

    def value(self, segment, offset, width):
        at = segment*16+u16(offset)
        return int.from_bytes(self.memory[at:at+width], 'little')

    def store(self, at, width, value, code=False):
        value &= (1 << (8*width))-1
        self.memory[at:at+width] = value.to_bytes(width, 'little')
        self.trace.append(dict(kind='patch' if code else 'store', address=at, width=width, value=value))
        if not code:
            self.graph_stores += 1

    def invoke(self, name, s, prefix_stores=None):
        p = self.p
        first = u16(p['slots']+u16(s['slot']*16))
        dg = lambda off: self.value(p['ds']+0x2000, u16(first+off), 2)
        width, bottom, alpha, colors = dg(8), dg(6), dg(12), dg(14)
        w = u16(width*4)
        origin = u16((signed(u16(s['left'])) >> 3)+bottom)
        last = u16(origin+w-1)
        start = p['starts'][[n for n, _ in FUNCTIONS].index(name)]
        if name != 'noalpha':
            self.trace.append(dict(kind='color', args=[0, 0xc0], reply=s['reply'], carry=s['carry']))
        values = ([colors, origin, width, width, u16(w+80)] if name == 'alpha' else
                  [last, last, w, w, u16(80-w), u16(80-w)] if name == 'hflip' else [width])
        for off, v in zip(PATCHES[name], values):
            self.store(self.code+start+off, 2, v, code=True)
        segment = u16(0xa800+u16(s['top'])*5)
        si = 0

        def rows(source, combine):
            nonlocal si
            di = last if name == 'hflip' else origin
            while True:
                count = (w or 65536) if name == 'hflip' else width if not combine else (width or 65536)
                amount = 1 if name == 'hflip' else 4
                for _ in range(count):
                    at = segment*16+di
                    v = self.value(source, si, amount)
                    if name == 'hflip':
                        v = self.memory[self.data+p['lut']+v]
                    if combine:
                        v |= int.from_bytes(self.memory[at:at+amount], 'little')
                    self.store(at, amount, v)
                    si = u16(si+amount)
                    di = u16(di-1 if name == 'hflip' else di+4)
                    if prefix_stores is not None and self.graph_stores == prefix_stores:
                        return False
                di = u16(di-u16(80-w) if name == 'hflip' else di-u16(w+80))
                if signed(di) < 0:
                    return True

        if name != 'noalpha':
            if not rows(alpha, False):
                return
            self.trace.append(dict(kind='out', port=0x7c, width=1, value=0))
            si = 0
        while True:
            if not rows(colors, name != 'noalpha'):
                return
            segment = u16(segment+0x800)
            if segment < 0xc000:
                continue
            if segment >= 0xc800:
                break
            segment = u16(segment+0x2000)
        self.final_es = segment
        self.final_fs = colors if name == 'hflip' else self.initial_fs


class DrawProbe(Probe):
    """Execute original SMC/REP/LOOP/XLAT/OUT/RETF; replace color setup only."""
    def __init__(self, mz, profile, s):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR, UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc, self.reg = Uc(UC_ARCH_X86, UC_MODE_16), reg
        self.uc.mem_map(0, 0x100000)
        image = bytearray(mz.program_image)
        for r in mz.relocations:
            at = r.segment*16+r.offset
            struct.pack_into('<H', image, at, u16(struct.unpack_from('<H', image, at)[0]+0x2000))
        self.uc.mem_write(0x20000, bytes(image))
        self.p, self.code, self.data, self.stack = profile, (0x2000+profile['cs'])*16, (0x2000+profile['ds'])*16, 0x40000
        self.uc.mem_write(0xa0000, bytes((i*7+0x55)&255 for i in range(0x60000)))
        for segment, factor, seed in [(s['alpha'], 13, 23), (s['colors'], 29, 71)]:
            self.uc.mem_write(segment*16, bytes((i*factor+seed)&255 for i in range(65536)))
        table = bytes(reverse_bits(i) if s['lookup'] == 'reverse' else i if s['lookup'] == 'identity' else i^0x5a for i in range(256))
        self.uc.mem_write(self.data+profile['lut'], table)
        self.uc.mem_write(self.stack, bytes([0xa5])*65536)
        self.metadata(s)
        self.meta = analyze(mz.program_image, profile)
        self.trace, self.errors, self.visited = [], [], set()
        self.position = None
        for key, value in dict(DS=0x2000+profile['ds'], SS=0x4000, ES=0x3333,
                               FS=0x4444, BP=0x7777, SI=0x1357, DI=0x2468, BX=0xbeef).items():
            self.set(key, value)
        self.set('EFLAGS', 2 | (0x200 if s['if'] else 0) | (0x400 if s['df'] else 0))
        def guard(fn, default=None):
            def invoke(*args):
                try:
                    return fn(*args)
                except Exception as error:
                    self.errors.append(str(error))
                    self.uc.emu_stop()
                    return default
            return invoke
        def code(uc, address, size, user):
            seg, off = self.get('CS')-0x2000, address-self.get('CS')*16
            self.position = (seg, off)
            if self.get('SS') != 0x4000:
                raise ValueError('CDG draw SS alias')
            if address == self.code+0xff00:
                if seg != profile['cs'] or self.get('SP') != 0xffda or any(self.get(r) != v for r, v in self.saved.items()):
                    raise ValueError('CDG draw terminal far frame differs')
                self.stop = True
                uc.emu_stop()
                return
            if self.position in self.meta['bounds']:
                self.visited.add(self.position)
                if self.position in self.meta['returns']:
                    ip, cs = struct.unpack('<HH', uc.mem_read(self.stack+self.get('SP'), 4))
                    if self.get('SP') != 0xffd0 or (ip, cs) != (0xff00, profile['cs']+0x2000) or any(self.get(r) != v for r, v in self.saved.items()):
                        raise ValueError('CDG draw native far return frame differs')
                return
            if self.position != (0, profile['color']):
                raise ValueError('CDG draw escape/operand boundary differs: '+str(self.position))
            sp = self.get('SP')
            ip, cs, color, mode = struct.unpack('<4H', uc.mem_read(self.stack+sp, 8))
            if self.meta['calls'].get((cs-0x2000, ip)) != self.position or sp != 0xffc2 or self.get('BP') != 0xffce or self.get('DS') != profile['ds']+0x2000:
                raise ValueError('CDG draw foreign far/Pascal caller frame differs')
            self.trace.append(dict(kind='color', args=[color, mode], reply=self.s['reply'], carry=self.s['carry']))
            for key, value in dict(AX=self.s['reply'], CX=0xbeef, DX=0x55aa).items():
                self.set(key, value)
            self.set('EFLAGS', (self.get('EFLAGS') & ~1) | int(self.s['carry']))
            self.set('SP', sp+8)
            self.set('CS', cs)
            self.set('IP', ip)
        def write(uc, access, address, size, value, user):
            if self.stack <= address and address+size <= self.stack+65536:
                return
            if self.position not in self.meta['bounds']:
                raise ValueError('CDG draw store lacks reviewed native caller')
            kind = 'store'
            if self.code <= address < self.code+0x10000:
                if size != 2 or self.meta['writers'].get(self.position) != address-self.code:
                    raise ValueError('CDG draw unowned SMC destination/width')
                kind = 'patch'
            elif not 0xa0000 <= address or address+size > 0x100000 or size != (1 if self.name == 'hflip' else 4):
                raise ValueError('CDG draw flat physical store span differs')
            self.trace.append(dict(kind=kind, address=address, width=size, value=value & ((1 << (8*size))-1)))
        def output(uc, port, width, value, user):
            expected = self.p['starts'][0]+110 if self.name == 'alpha' else self.p['starts'][1]+126
            if self.position != (profile['cs'], expected) or (port, width, value) != (0x7c, 1, 0):
                raise ValueError('CDG draw native port caller/width/value differs')
            self.trace.append(dict(kind='out', port=port, width=width, value=value))
        def intr(*args):
            raise ValueError('CDG draw unexpected interrupt')
        def inp(*args):
            raise ValueError('CDG draw unexpected input port')
        # No memory-read hook; all self-modifying operands and RETF stay native.
        self.uc.hook_add(UC_HOOK_CODE, guard(code))
        self.uc.hook_add(UC_HOOK_MEM_WRITE, guard(write))
        self.uc.hook_add(UC_HOOK_INTR, guard(intr))
        self.uc.hook_add(UC_HOOK_INSN, guard(output), None, 1, 0, reg.UC_X86_INS_OUT)
        self.uc.hook_add(UC_HOOK_INSN, guard(inp, 0), None, 1, 0, reg.UC_X86_INS_IN)

    def metadata(self, s):
        first = u16(self.p['slots']+u16(s['slot']*16))
        # Independent effective offsets, including wrapped fields.
        for field, value in [(0, 0), (2, 1), (4, 32767), (6, s['bottom']), (8, s['width']),
                             (10, 0), (12, s['alpha']), (14, s['colors'])]:
            self.uc.mem_write(self.data+u16(first+field), struct.pack('<H', u16(value)))

    def run(self, name, s, terminal=True, budget=2000000):
        self.name, self.s, self.stop = name, s, False
        self.errors.clear()
        self.set('CS', self.p['cs']+0x2000)
        self.set('SP', 0xffd0)
        self.saved = {r: self.get(r) for r in ('BP', 'SI', 'DI', 'DS')}
        self.uc.mem_write(self.stack+0xffd0, struct.pack('<5H', 0xff00, self.p['cs']+0x2000, u16(s['slot']), u16(s['top']), u16(s['left'])))
        start = self.p['starts'][[n for n, _ in FUNCTIONS].index(name)]
        self.uc.emu_start(self.code+start, 0x100000, count=budget)
        if self.errors:
            raise ValueError(self.errors[0])
        if self.stop != terminal:
            raise ValueError('CDG draw terminal/instruction budget differs')


def scenario(**kw):
    s = dict(width=1, bottom=0, left=0, top=0, slot=0, alpha=0x5000, colors=0x7000,
             lookup='reverse', reply=0, carry=False, **{'if': True, 'df': False})
    s.update(kw)
    return s


def observe(mz, profile, name, s, sequence=None, prefix=False):
    p = DrawProbe(mz, profile, s)
    rows = []
    for function, case in sequence or [(name, s), (name, dict(s, width=1, bottom=0, left=0, top=0)), (name, s)]:
        p.metadata(case)
        p.trace.clear()
        before = bytes(p.uc.mem_read(0, 0x100000))
        spec = DrawSpec(before, profile, p.get('FS'))
        limit = {'alpha': 391, 'hflip': 327}[function] if prefix else None
        spec.invoke(function, case, limit)
        p.run(function, case, terminal=not prefix, budget=2000 if prefix else 2000000)
        if p.trace != spec.trace:
            i = next((i for i, (a, b) in enumerate(zip(p.trace, spec.trace)) if a != b), min(len(p.trace), len(spec.trace)))
            raise ValueError('CDG draw ordered scalar trace differs: '+str((function, case, i, p.trace[i:i+1], spec.trace[i:i+1], len(p.trace), len(spec.trace))))
        actual = bytes(p.uc.mem_read(0, 0x100000))
        if actual[:p.stack] != spec.memory[:p.stack] or actual[p.stack+65536:] != spec.memory[p.stack+65536:]:
            raise ValueError('CDG draw whole physical preservation differs')
        if not prefix and (p.get('ES') != spec.final_es or p.get('FS') != spec.final_fs):
            raise ValueError('CDG draw final ES/FS differs')
        if bool(p.get('EFLAGS') & 0x200) != case['if'] or bool(p.get('EFLAGS') & 0x400) != (case['df'] if function == 'hflip' else False):
            raise ValueError('CDG draw IF/DF contract differs')
        digest = sha(json.dumps(p.trace, separators=(',', ':')).encode())
        rows.append(dict(function=function, scenario=case, terminal=not prefix, ordered_trace_sha256=digest,
                         trace_events=len(p.trace), graph_stores=spec.graph_stores,
                         patches=[e for e in p.trace if e['kind'] == 'patch'], ports=[e for e in p.trace if e['kind'] == 'out'],
                         memory_before_sha256=sha(before), memory_after_sha256=sha(spec.memory), es=p.get('ES'), fs=p.get('FS')))
    return dict(function=name, scenario=s, sequence=rows, visited=[list(a) for a in sorted(p.visited)])


def matrix(mz, profile):
    parameters = [(1, 0, 0, 0, 0), (2, 80, 7, 5, 31), (3, 160, -1, -1, 32),
                  (2, 240, 641, 399, 65535), (1, 0, -1, 0, 0), (4, 0, 32767, 1023, 0),
                  (3, 80, -32768, 1638, 0), (8, 320, 0, 0, 32)]
    rows = []
    for name, _ in FUNCTIONS:
        for width, bottom, left, top, slot in parameters:
            for irq, df in itertools.product((False, True), repeat=2):
                s = scenario(width=width, bottom=bottom, left=left, top=top, slot=slot, **{'if': irq, 'df': df})
                rows.append(observe(mz, profile, name, s))
        for changes in [dict(alpha=0, colors=0), dict(alpha=0x5000, colors=0x5000),
                        dict(alpha=profile['ds']+0x2000), dict(lookup='identity'), dict(lookup='xor', reply=65535, carry=True)]:
            rows.append(observe(mz, profile, name, scenario(**changes)))
        s = scenario(width=0)
        rows.append(observe(mz, profile, name, s, sequence=[(name, s)], prefix=name != 'noalpha'))
    return rows


def coverage(meta, rows):
    visited = {tuple(a) for r in rows for a in r['visited']}
    result = dict(instructions=len(meta['bounds']), visited=len(meta['bounds'] & visited), unvisited=[list(a) for a in sorted(meta['bounds']-visited)])
    if result['unvisited']:
        raise ValueError('CDG draw complete native coverage differs: '+str(result))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw = (ROOT/PARENT).read_bytes()
    if sha(raw) != PARENT_SHA:
        raise ValueError('CDG draw previous source proof differs')
    parent = json.loads(raw)
    inputs = dict(parent['inputs'])
    inputs[PARENT] = sha(raw)
    for p in ('scripts/review_th03_shared_cdg_draw.py', 'scripts/probe_th03_unicorn_far_return.py',
              '.analysis/sol-shared-cdg-draw-op-ghidra-check-20261006.log', '.analysis/sol-shared-cdg-draw-mainl-ghidra-check-20261006.log'):
        inputs[p] = sha((ROOT/p).read_bytes())
    def verify():
        for p, h in inputs.items():
            if sha((ROOT/p).read_bytes()) != h:
                raise ValueError('CDG draw input changed: '+p)
    verify()
    frozen = frozen_files(REVISION)
    observations, stored = {}, {}
    for art, profile in PROFILES.items():
        artifact = find_artifact(load_target_manifest(ROOT/'config/targets.toml'), 'th03-'+art)
        stored[art] = read_verified_artifact(ROOT, artifact)
        target_path = f'.analysis/th03-diet/sol-diet-restoration-20261006-b/{art}.exe'
        paths = [target_path]+[f'.analysis/th03-shared-cdg-load/sol-shared-cdg-load-source-20261006-c/round{n}/source/bin/th03/{art}.exe' for n in (1, 2)]
        observations[art] = []
        for number, path in enumerate(paths):
            inputs[path] = sha((ROOT/path).read_bytes())
            mz = parse_mz((ROOT/path).read_bytes())
            if not mz.valid:
                raise ValueError('CDG draw invalid MZ')
            meta = analyze(mz.program_image, profile)
            item = dict(path=path, bodies=meta['bodies'], producer_even=meta['even'])
            if number:
                tree = Path(path).parents[2]
                for p in PROVIDERS:
                    cp = str(tree/p)
                    inputs[cp] = sha((ROOT/cp).read_bytes())
                    if (ROOT/cp).read_bytes() != frozen[p]:
                        raise ValueError('CDG draw frozen provider differs: '+p)
                mp = str(tree/f'obj/th03/{art}.map')
                inputs[mp] = sha((ROOT/mp).read_bytes())
                carriers = code_rows((ROOT/mp).read_text(), len(mz.program_image))
                target = parse_mz((ROOT/target_path).read_bytes())
                item['comparisons'] = {}
                for module, a, size in [('th03/cdg_put.asm', profile['starts'][0], 382), ('th03/cdg_p_na.asm', profile['starts'][2], 114)]:
                    row = next(r for r in carriers if r['module'] == module and r['size'])
                    if (row['segment'], row['offset'], row['size']) != (profile['cs'], a, size):
                        raise ValueError('CDG draw complete MAP carrier differs')
                    comp = extent_observation(target, mz, row)
                    if not comp['raw_slice_equal'] or not comp['ordered_relocations_equal']:
                        raise ValueError('CDG draw original carrier raw/ordered rows differ')
                    cp = str(tree/'obj/th03'/Path(module).with_suffix('.obj').name)
                    inputs[cp] = sha((ROOT/cp).read_bytes())
                    obj = describe_omf((ROOT/cp).read_bytes())
                    if not obj['valid'] or obj['dependency_timestamp_normalized_sha256'] != parent['rounds'][number-1]['all_objects']['obj/th03/'+Path(module).with_suffix('.obj').name]:
                        raise ValueError('CDG draw original OMF producer differs')
                    item['comparisons'][module] = comp
                links = {}
                for product in ('op', 'main', 'mainl'):
                    lp = str(tree/f'obj/th03/{product}.@l')
                    inputs[lp] = sha((ROOT/lp).read_bytes())
                    links[product] = [f'obj\\th03\\{obj}.obj' in (ROOT/lp).read_text() for obj in ('cdg_put', 'cdg_p_na')]
                if links != dict(op=[True, True], main=[False, False], mainl=[True, True]):
                    raise ValueError('CDG draw shared physical-object ownership differs')
                item['links'] = links
            item['cpu'] = matrix(mz, profile)
            item['coverage'] = coverage(meta, item['cpu'])
            if number and normalized_contracts(item['cpu']) != normalized_contracts(observations[art][0]['cpu']):
                # Nested sequence memory digests describe whole-image differences.
                def semantic(rows):
                    return json.loads(json.dumps(rows), object_hook=lambda d: {k: v for k, v in d.items() if k not in ('memory_before_sha256', 'memory_after_sha256')})
                if semantic(item['cpu']) != semantic(observations[art][0]['cpu']):
                    raise ValueError('CDG draw target/cold scalar contracts differ')
            observations[art].append(item)
            print('PASS CDG draw', art, path, len(item['cpu']), 'records', item['coverage'], flush=True)
    verify()
    final = frozen_files(REVISION)
    if any(final[p] != frozen[p] for p in PROVIDERS):
        raise ValueError('CDG draw frozen providers changed')
    for art in PROFILES:
        artifact = find_artifact(load_target_manifest(ROOT/'config/targets.toml'), 'th03-'+art)
        if read_verified_artifact(ROOT, artifact) != stored[art]:
            raise ValueError('CDG draw canonical target changed')
    report = dict(kind='th03-shared-complete-cdg-drawing-native-review', observed_utc=datetime.now(timezone.utc).isoformat(), inputs=inputs,
                  observations=observations, tools=dict(capstone=version('capstone'), unicorn=version('unicorn')),
                  diagnostic_checks_pass=True, source_acceptance=False, exact_acceptance=False, new_build=False,
                  notes='Three complete functions493bytes/200positions and three separate natural EVEN bytes in two shared ASM carriers496; independent OP/MAINL bindings. Complete original native SMC/REP/LOOP/XLAT/OUT/RETF and far frames run; one explicit color callback only. Ordered patches/flat operand stores/callback/port trace, full physical1MiB outside64KiBstack, IF/DF and final ES/FS checked. Reentry triples change geometry without resetting VRAM/CODE; zero-width alpha/hflip have independently checked2000-instruction scalar prefixes, no terminal claim. Synthetic flat memory/LUT/buffers grant no physical GRCG/banking/assets/IRQ reentrancy/header/DATA/BSS/CRT/canonicalpacking/fullproduct/exact ownership.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('PASS complete shared CDG drawing diagnostics; exact open')


if __name__ == '__main__':
    main()
