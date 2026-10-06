#!/usr/bin/env python3
"""Complete remaining MAINL gaiji/packed drawing and scroll/show candidates."""
import argparse
from collections import Counter
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import re
import struct
import subprocess
from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from capstone.x86_const import X86_OP_IMM
from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import Probe, REVISION, sha
from review_th03_mainl_snow import u16
from review_th03_mainl_heap import cached_provider, BUILD_REMAPS
from review_th03_mainl_super import SuperProbe
from review_th03_mainl_graphics import initial_flags, COLD, COLD_SHA

ROOT = Path(__file__).resolve().parents[1]
PROOF = '.analysis/sol-mainl-screen-review-20261006.json'
PROOF_SHA = 'f773b9b9871b32b98f625efc881c04aecff7749dfd65ea984721fdc5bcee8a86'
OWN_RANGES = [('gaiji', 0xf58, 147, 8), ('clipout', 0x162c, 6, 10), ('pack', 0x1632, 206, 10),
              ('scroll', 0x1700, 88, 2), ('show', 0x1758, 5, 0),
              ('noclipout', 0x2c68, 6, 10), ('noclip', 0x2c6e, 196, 10)]
CONTEXT = [('gdc', 0xc66, 11, 'near')]
RANGES = OWN_RANGES + CONTEXT
ENTRY = {n: a for n, a, _, _ in RANGES if n not in ('clipout', 'noclipout')}
ALIGNMENT = {0xfeb: 0x90, 0x175d: 0x90}
INTERIOR = {0x1683: 0x90, 0x2cb5: 0x90}
NEAR = {a: 0xc66 for a in (0x173a, 0x1743, 0x1748, 0x1751)}
PORTS = {**{a: 0x7c for a in (0xf74, 0xfe4)}, **{a: 0x7e for a in (0xf7b, 0xf81, 0xf87, 0xf8d)},
         0xf91: 0x68, 0xfe0: 0x68, 0xfad: 0xa1, 0xfb1: 0xa3, 0xfbc: 0xa5, 0xfc4: 0xa5,
         0x172a: 0xa2, 0xc66: 0xa0, 0xc6e: 0xa0}
INPUTS = {0xfbe: 0xa9, 0xfc6: 0xa9, 0x1722: 0xa0}
TABLE, TABLE_SIZE = 0x1aaa, 1024
PUBLICS = {'GRAPH_GAIJI_PUTC': 0xf58, 'GRAPH_PACK_PUT_8': 0x1632,
           'GRAPH_PACK_PUT_8_NOCLIP': 0x2c6e, 'GRAPH_SCROLLUP': 0x1700,
           'GRAPH_SHOW': 0x1758, 'gdc_outpw': 0xc66, 'RotTbl': TABLE}
PROVIDERS = ['libs/master.lib/' + n + '.asm' for n in (
    'graph_gaiji_putc', 'graph_pack_put_8', 'graph_pack_put_8_noclip', 'graph_scrollup', 'graph_show',
    'rottbl', 'gdc_outpw', 'grp[data]', 'clip[data]')]
EXTENTS = [('gaiji', 0xf58, 148), ('pack', 0x162c, 212), ('scroll', 0x1700, 88),
           ('show', 0x1758, 6), ('noclip', 0x2c68, 202), ('table', TABLE, TABLE_SIZE)]
SOURCE_IMAGE = bytes((i * 37 + 3) & 255 for i in range(65536))
DRAW_IMAGE = bytes((i * 17 + 5) & 255 for i in range(0x58000))


def table_entry(value):
    """Two packed nibbles contribute one pair of bits to each plane."""
    return bytes(((value >> bit) & 1) | (((value >> (bit + 4)) & 1) << 1) for bit in range(4))


def signed(value):
    value = u16(value)
    return value - 65536 if value & 32768 else value


def return_cleanup(i):
    if i.mnemonic == 'ret' and not i.operands:
        return 'near'
    if i.mnemonic == 'retf':
        return i.operands[0].imm if i.operands else 0
    return None


def analyze(image):
    dec = Cs(CS_ARCH_X86, CS_MODE_16)
    dec.detail = True
    decoded, bounds, returns, rows = [], set(), {}, []
    for name, start, size, cleanup in RANGES:
        body = image[start:start + size]
        if len(body) != size:
            raise ValueError('draw complete body differs')
        instructions = list(dec.disasm(body, start))
        if not instructions or sum(i.size for i in instructions) != size:
            raise ValueError('draw instruction partition differs')
        if return_cleanup(instructions[-1]) != cleanup:
            raise ValueError('draw terminal cleanup differs')
        bounds.update(i.address for i in instructions)
        decoded.append((name, start, size, cleanup, instructions))
    for name, start, size, cleanup, instructions in decoded:
        edges = []
        for i in instructions:
            if i.mnemonic in ('ret', 'retf'):
                if return_cleanup(i) != cleanup:
                    raise ValueError('draw interior cleanup differs')
                returns[i.address] = cleanup
            if i.mnemonic == 'int' and (i.address != 0x175a or i.bytes != b'\xcd\x18'):
                raise ValueError('draw unknown BIOS site')
            if i.mnemonic in ('in', 'out'):
                sites = PORTS if i.mnemonic == 'out' else INPUTS
                expected = hex(sites[i.address]) + ', al' if i.mnemonic == 'out' and i.address in sites else 'al, ' + hex(sites[i.address]) if i.address in sites else None
                if i.op_str != expected:
                    raise ValueError('draw unknown port/site/width')
            if not (i.mnemonic.startswith(('j', 'loop')) or i.mnemonic in ('call', 'lcall', 'ljmp')):
                continue
            if not i.operands or any(o.type != X86_OP_IMM for o in i.operands):
                raise ValueError('draw unknown indirect edge')
            if i.mnemonic in ('lcall', 'ljmp'):
                raise ValueError('draw unknown far edge')
            destination = i.operands[0].imm
            if i.mnemonic == 'call':
                if NEAR.get(i.address) != destination:
                    raise ValueError('draw unknown native call')
            elif destination not in bounds:
                raise ValueError('draw branch enters operand/table/neighbor')
            edges.append(dict(instruction=i.address, kind=i.mnemonic, destination=destination))
        rows.append(dict(name=name, offset=start, size=size, instructions=len(instructions), cleanup=cleanup,
                         sha256=sha(image[start:start + size]), edges=edges))
    if any(image[a:a + 1] != bytes([v]) for a, v in (ALIGNMENT | INTERIOR).items()):
        raise ValueError('draw producer alignment differs')
    table = image[TABLE:TABLE + TABLE_SIZE]
    if table != b''.join(table_entry(value) for value in range(256)):
        raise ValueError('draw packed-pixel table differs')
    return dict(bodies=rows, bounds=sorted(bounds), returns=returns, new_body_bytes=654,
                new_alignment_bytes=2, new_instruction_extent_bytes=656, table_bytes=TABLE_SIZE,
                new_extent_bytes=1680, prior_context_bytes=11, alignment=ALIGNMENT,
                interior_even=INTERIOR, table_sha256=sha(table), table_entries=256,
                polling_prefix_instructions=sum(i.address < 0x1720 for name, _, _, _, instructions in decoded if name == 'scroll' for i in instructions))


class DrawProbe(Probe):
    prepare = SuperProbe.prepare
    enter = SuperProbe.enter
    leave = SuperProbe.leave

    def __init__(self, mz, scenario, meta=None):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INTR, UC_HOOK_INSN
        from unicorn import x86_const as reg
        self.uc, self.reg = Uc(UC_ARCH_X86, UC_MODE_16), reg
        self.uc.mem_map(0, 0x100000)
        image = bytearray(mz.program_image)
        for relocation in mz.relocations:
            at = relocation.segment * 16 + relocation.offset
            struct.pack_into('<H', image, at, u16(struct.unpack_from('<H', image, at)[0] + 0x2000))
        self.uc.mem_write(0x20000, bytes(image))
        self.code, self.data, self.stack = 0x20000, 0x2e3f0, 0x40000
        self.s = scenario
        self.meta = meta or analyze(mz.program_image)
        self.bounds, self.returns = set(self.meta['bounds']), self.meta['returns']
        self.entry_names = {a: n for n, a in ENTRY.items()}
        self.frames, self.pending, self.stop, self.errors = [], None, False, []
        self.native, self.visited, self.ports, self.events, self.writes = Counter(), set(), [], [], []
        self.mode, self.tiles = 0xc0, [17, 34, 51, 68]
        self.cg_mode, self.low, self.high, self.row, self.status_index = 10, 0, 0x56, 0, 0
        self.uc.mem_write(0x50000, SOURCE_IMAGE)
        self.uc.mem_write(0xa8000, DRAW_IMAGE)
        for a, key, default in ((0x528, 'clip_top', 0), (0x52a, 'clip_height', 399), (0x52e, 'clip_seg', 0xa800),
                                (0x564, 'vram_seg', 0xa800), (0x568, 'lines', 400), (0x56c, 'zoom', 0)):
            self.uc.mem_write(self.data + a, struct.pack('<H', scenario.get(key, default)))
        for seg, offset, values in scenario.get('source_values', []):
            for index, value in enumerate(values):
                self.uc.mem_write(seg * 16 + u16(offset + index), bytes([value]))

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
            if address == self.code + 0xff00:
                if self.get('CS') != 0x2000:
                    raise ValueError('draw terminal segment alias')
                if self.frames or self.pending:
                    raise ValueError('draw unfinished native frame')
                self.stop = True
                uc.emu_stop()
                return
            off = address - self.code
            if self.get('CS') != 0x2000 or self.get('SS') != 0x4000:
                raise ValueError('draw CODE/stack segment alias')
            if off not in self.bounds:
                raise ValueError('CPU escaped draw instruction boundaries')
            self.visited.add(off)
            if off in self.entry_names:
                name = self.entry_names[off]
                self.enter(name, next(c for n, _, _, c in RANGES if n == name))
                self.native[name] += 1
            if off in NEAR:
                self.prepare('gdc', self.get('SP') - 2, off + 3, 'near')
            if off in self.returns:
                self.leave(self.returns[off])

        def write(uc, access, address, size, value, user):
            if self.stack <= address and address + size <= self.stack + 65536:
                return
            if not 0xa8000 <= address < address + size <= 0x100000:
                raise ValueError('draw store outside declared synthetic video/overflow span')
            self.writes.append([address, size, value])

        def intr(uc, number, user):
            site = u16(self.get('IP') - 2)
            if number != 0x18 or self.get('CS') != 0x2000 or site != 0x175a or self.get('AH') != 0x40:
                raise ValueError('draw unknown BIOS request/site')
            ax, cf = scenario.get('bios_ax', 0xbeef), scenario.get('bios_cf', 0)
            self.events.append(dict(site=site, name='modeled-int18-show', ax_request=self.get('AX'), ax=ax, cf=cf))
            self.set('AX', ax)
            self.set('EFLAGS', (self.get('EFLAGS') & ~1) | cf)

        def event(site, port, value, direction):
            return dict(site=site, port=port, width=1, value=value, direction=direction,
                        live_if=bool(self.get('EFLAGS') & 512), live_df=bool(self.get('EFLAGS') & 1024))

        def out(uc, port, width, value, user):
            site = self.get('IP')
            if self.get('CS') != 0x2000 or PORTS.get(site) != port or width != 1:
                raise ValueError('draw unknown output port/site/width')
            self.ports.append(event(site, port, value, 'out'))
            if port == 0x7c:
                if value not in (0, 0xc0):
                    raise ValueError('draw unknown GRCG mode')
                self.mode = value
            elif port == 0x7e:
                self.tiles = self.tiles[1:] + [value]
            elif port == 0x68:
                if value not in (10, 11):
                    raise ValueError('draw unknown font mode')
                self.cg_mode = value
            elif port == 0xa1:
                self.low = value
            elif port == 0xa3:
                self.high = value
            elif port == 0xa5:
                self.row = value
            elif port == 0xa2 and value != 0x70:
                raise ValueError('draw unknown GDC command')

        def inp(uc, port, width, user):
            site = self.get('IP')
            if self.get('CS') != 0x2000 or INPUTS.get(site) != port or width != 1:
                raise ValueError('draw unknown input port/site/width')
            if port == 0xa9:
                if self.cg_mode != 11 or self.low >= 128 or self.row & ~0x2f:
                    raise ValueError('draw unknown font latch/mode')
                index = self.high * 128 + self.low
                value = (index * 29 + (self.row & 15) * 7 + (0 if self.row & 32 else 1) * 113 + scenario.get('seed', 11)) & 255
            else:
                values = scenario.get('gdc_status', [4])
                value = values[min(self.status_index, len(values) - 1)]
                self.status_index += 1
            self.ports.append(event(site, port, value, 'in'))
            return value

        self.uc.hook_add(UC_HOOK_CODE, guard(code))
        self.uc.hook_add(UC_HOOK_MEM_WRITE, guard(write))
        self.uc.hook_add(UC_HOOK_INTR, guard(intr))
        self.uc.hook_add(UC_HOOK_INSN, guard(out), None, 1, 0, reg.UC_X86_INS_OUT)
        self.uc.hook_add(UC_HOOK_INSN, guard(inp, 0), None, 1, 0, reg.UC_X86_INS_IN)

    def run(self, name, args=(), budget=500000):
        if name not in ('gaiji', 'pack', 'noclip', 'scroll', 'show'):
            raise ValueError('draw helper requires complete public caller')
        self.stop, self.pending = False, None
        self.errors.clear()
        self.frames.clear()
        cleanup = next(c for n, _, _, c in RANGES if n == name)
        values = dict(CS=0x2000, DS=0x2e3f, SS=0x4000, ES=0x3333, AX=0x1111, BX=0x2222,
                      CX=0x3333, DX=0x4444, BP=0x7777, SI=0x1357, DI=0x2468, SP=0xffc0,
                      EFLAGS=initial_flags(self.s))
        for register, value in values.items():
            self.set(register, value)
        self.uc.mem_write(self.stack + 0xffc0, struct.pack('<' + 'H' * (2 + len(args)), 0xff00, 0x2000, *args))
        self.prepare(name, 0xffc0, 0xff00, cleanup)
        self.uc.emu_start(self.code + ENTRY[name], 0x100000, count=budget)
        if self.errors:
            raise ValueError(self.errors[0])
        if not self.stop:
            raise ValueError('draw terminal/budget differs')
        if self.get('SP') != 0xffc4 + cleanup or any(self.get(r) != values[r] for r in ('BP', 'SI', 'DI', 'DS')):
            raise ValueError('draw cleanup/preserved-register differs')


class Scalar:
    def __init__(self, p):
        self.mem = bytearray(p.uc.mem_read(0, 0x100000))
        self.s, self.data, self.flags = p.s, p.data, initial_flags(p.s)
        self.native, self.ports, self.events, self.writes = Counter(), [], [], []
        self.mode, self.tiles = p.mode, list(p.tiles)
        self.cg_mode, self.low, self.high, self.row, self.status_index = 10, 0, 0x56, 0, 0

    def get(self, offset):
        return int.from_bytes(self.mem[self.data + offset:self.data + offset + 2], 'little')

    def port(self, site, port, value, direction='out', flags=None):
        flags = self.flags if flags is None else flags
        self.ports.append(dict(site=site, port=port, width=1, value=value, direction=direction,
                               live_if=bool(flags & 512), live_df=bool(flags & 1024)))
        if direction == 'in':
            return
        if port == 0x7c:
            self.mode = value
        elif port == 0x7e:
            self.tiles = self.tiles[1:] + [value]
        elif port == 0x68:
            self.cg_mode = value
        elif port == 0xa1:
            self.low = value
        elif port == 0xa3:
            self.high = value
        elif port == 0xa5:
            self.row = value

    def store(self, address, size, value):
        self.mem[address:address + size] = value.to_bytes(size, 'little')
        self.writes.append([address, size, value])

    def gaiji(self, args):
        color, character, y, x = args
        code = u16(character + 0x5680 + int(bool(self.flags & 1))) & 0xff7f
        self.port(0xf74, 0x7c, 0xc0, flags=self.flags & ~512)
        for bit, site in enumerate((0xf7b, 0xf81, 0xf87, 0xf8d)):
            self.port(site, 0x7e, 255 if color & (1 << bit) else 0)
        self.port(0xf91, 0x68, 11)
        self.port(0xfad, 0xa1, code & 255)
        self.port(0xfb1, 0xa3, code >> 8)
        cursor, shift = u16(y * 80 + (x >> 3)), x & 7
        base, direction, index = self.get(0x564) * 16, -2 if self.flags & 1024 else 2, (code >> 8) * 128 + (code & 127)
        for row in range(16):
            left = (index * 29 + row * 7 + self.s.get('seed', 11)) & 255
            right = (left + 113) & 255
            self.port(0xfbc, 0xa5, row | 32)
            self.port(0xfbe, 0xa9, left, 'in')
            self.port(0xfc4, 0xa5, row)
            self.port(0xfc6, 0xa9, right, 'in')
            bits = ((left << 8) | right) >> shift
            word = ((bits & 255) << 8) | (bits >> 8)
            self.store(base + cursor, 2, word)
            cursor = u16(cursor + direction)
            self.store(base + cursor, 1, ((right << 8) >> shift) & 255)
            cursor = u16(cursor + 78)
        self.port(0xfe0, 0x68, 10)
        self.port(0xfe4, 0x7c, 0)
        return None, 0

    def packed(self, name, args):
        length, source, segment, y, x = args
        row = u16(y - self.get(0x528)) if name == 'pack' else y
        if name == 'pack' and row > self.get(0x52a):
            return None, None
        groups, xpos = signed(length) >> 3, signed(x) >> 3
        if groups <= 0:
            return None, None
        if xpos < 0:
            groups += xpos
            if groups <= 0:
                return None, None
            source = u16(source + xpos * 4)
            xpos = 0
        if xpos >= 80:
            return None, None
        groups = min(groups + xpos, 80) - xpos
        cursor, base = u16(row * 80 + xpos), self.get(0x52e)
        self.flags &= ~1024
        for _ in range(groups):
            # Four sequential bytes are fetched before these four plane stores.
            pixels = []
            for _ in range(4):
                value = self.mem[segment * 16 + source]
                pixels.extend((value >> 4, value & 15))
                source = u16(source + 1)
            masks = [sum(((pixel >> bit) & 1) << (7 - index) for index, pixel in enumerate(pixels)) for bit in range(4)]
            for address, value in zip((base * 16 + cursor, base * 16 + u16(cursor + 0x8000),
                                       u16(base + 0x1000) * 16 + cursor, u16(base + 0x3800) * 16 + cursor), masks):
                self.store(address, 1, value)
            cursor = u16(cursor + 1)
        return None, None

    def scroll(self, args):
        lines, line, zoom = self.get(0x568), args[0], self.get(0x56c)
        line = line if line < lines else lines
        shift = (zoom & 255) & 31  # Explicit Unicorn x86 model; physical V30 remains open.
        before = u16(line << shift)
        after = u16(u16(lines - line) << shift)
        statuses = self.s.get('gdc_status', [4])
        while True:
            value = statuses[min(self.status_index, len(statuses) - 1)]
            self.status_index += 1
            self.port(0x1722, 0xa0, value, 'in')
            if value & 4:
                break
        self.port(0x172a, 0xa2, 0x70)
        words = (u16(line * 40), u16(after << 4) | (zoom & 0xff00), 0, u16(before << 4) | (zoom & 0xff00))
        for word in words:
            self.native['gdc'] += 1
            self.port(0xc66, 0xa0, word & 255)
            self.port(0xc6e, 0xa0, word >> 8)
        return (words[-1] & 0xff00) | (words[-1] >> 8), 0

    def run(self, name, args=()):
        self.native[name] += 1
        if name == 'gaiji':
            return self.gaiji(args)
        if name in ('pack', 'noclip'):
            return self.packed(name, args)
        if name == 'scroll':
            return self.scroll(args)
        if name == 'show':
            ax, cf = self.s.get('bios_ax', 0xbeef), self.s.get('bios_cf', 0)
            self.events.append(dict(site=0x175a, name='modeled-int18-show', ax_request=0x4011, ax=ax, cf=cf))
            return ax, cf
        raise ValueError('scalar draw helper requires public caller')


def trace_hash(rows):
    return sha(json.dumps(rows, separators=(',', ':')).encode())


def compare(p, model, ax, cf, label):
    state = lambda x: (x.mode, x.tiles, x.cg_mode, x.low, x.high, x.row, x.status_index)
    if ((ax is not None and p.get('AX') != ax) or (cf is not None and p.get('EFLAGS') & 1 != cf)
            or (p.get('EFLAGS') ^ model.flags) & (512 | 1024) or p.native != model.native
            or p.ports != model.ports or p.events != model.events or p.writes != model.writes or state(p) != state(model)):
        raise ValueError('draw scalar registers/flags/native/interfaces/stores/latches differ: ' + str((label, p.get('AX'), ax, p.get('EFLAGS') & 1, cf, dict(p.native), dict(model.native), len(p.writes), len(model.writes), p.ports[:8], model.ports[:8])))
    actual = bytes(p.uc.mem_read(0, 0x100000))
    if actual[:p.stack] != model.mem[:p.stack] or actual[p.stack + 65536:] != model.mem[p.stack + 65536:]:
        changed = [i for i, (a, b) in enumerate(zip(actual, model.mem)) if a != b and not p.stack <= i < p.stack + 65536]
        raise ValueError('draw full physical memory differs: ' + str((label, changed[:24])))


def matrix(mz):
    meta, rows = analyze(mz.program_image), []
    flags = [dict(df=df, flags=2 | irq) for df in (False, True) for irq in (0, 512)]
    def observe(label, scenario, steps):
        p = DrawProbe(mz, scenario, meta)
        model, results = Scalar(p), []
        before = sha(bytes(model.mem))
        for name, args in steps:
            model.flags = initial_flags(scenario)
            ax, cf = model.run(name, args)
            p.run(name, args)
            compare(p, model, ax, cf, (label, scenario, name, args))
            results.append(dict(function=name, args=args, ax=ax, cf=cf, if_=bool(model.flags & 512), df=bool(model.flags & 1024),
                                registers={r: p.get(r) for r in ('AX', 'BX', 'CX', 'DX', 'BP', 'SI', 'DI', 'DS', 'ES', 'SP')}))
        rows.append(dict(function=label, scenario=scenario, steps=results, top_level_calls=len(steps), native_entries=dict(p.native),
                         events=p.events, port_count=len(p.ports), ports_sha256=trace_hash(p.ports), first_ports=p.ports[:4], last_ports=p.ports[-4:],
                         store_count=len(p.writes), stores_sha256=trace_hash(p.writes), visited=sorted(p.visited),
                         memory_before_sha256=before, memory_after_sha256=sha(bytes(model.mem))))
    for base in flags:
        for carry in (0, 1):
            for character in range(256):
                observe('gaiji-all-characters-carry', dict(base, flags=base['flags'] | carry), [('gaiji', [15, character, 13, 17])])
            for character in (256, 0x7fff, 0x8000, 0xa980, 0xff80, 0xffff):
                observe('gaiji-character-word-aliases', dict(base, flags=base['flags'] | carry), [('gaiji', [0xffff, character, 0, 0])])
        for shift in range(8):
            for color in range(16):
                observe('gaiji-shift-colors', base, [('gaiji', [color, 91, 399, 632 + shift])])
        for x, y in ((0, 0), (7, 0), (8, 0), (639, 399), (640, 400), (0xffff, 0xffff),
                     (0xfff8, 0x8000), (0, 819), (0, 820), (0, 0xcccc)):
            observe('gaiji-coordinate-wrap', dict(base, vram_seg=0xa801), [('gaiji', [0x100, 0, y, x])])
    for name in ('pack', 'noclip'):
        for value in range(256):
            for slot in range(4):
                source = [0] * 4
                source[slot] = value
                observe('packed-byte-plane-basis', dict(flags[value & 3], source_values=[[0x5000, 0x100, source]]), [(name, [8, 0x100, 0x5000, 31, 0])])
        for ix, x in enumerate((-32768, -641, -640, -639, -17, -9, -8, -7, -1, 0, 7, 8, 632, 639, 640, 641, 32767)):
            for il, length in enumerate((-32768, -1, 0, 1, 7, 8, 9, 15, 16, 639, 640, 641, 32760, 32767)):
                observe('packed-horizontal-clipping', flags[(ix + il) & 3], [(name, [u16(length), 0x100, 0x5000, 31, u16(x)])])
        for base in flags:
            for top, height in ((0, 399), (31, 0), (0xffff, 0xffff)):
                for y in (0xffff, 0, 1, 30, 31, 32, 33, 398, 399, 400, 8192, 0xcccc):
                    observe('packed-y-relative-vs-absolute', dict(base, clip_top=top, clip_height=height, clip_seg=0xa801), [(name, [16, 0x100, 0x5000, y, 7])])
            for segment, offset, x, y in ((0x5000, 0xfffd, 0, 0), (0x5000, 1, 0xfff9, 1), (0xa800, 0, 0, 0), (0xa800, 4, 0, 0), (0xb000, 0, 632, 399)):
                observe('packed-source-wrap-aliases', base, [(name, [32, offset, segment, y, x])])
    for zoom in (0, 0x4000):
        for line in list(range(401)) + [0xffff]:
            observe('scroll-all-normal-lines', dict(flags[line & 3], zoom=zoom), [('scroll', [line])])
    for i, lines in enumerate((0, 1, 2, 399, 400, 401, 0xffff)):
        for j, line in enumerate((0, 1, 2, 399, 400, 401, 0xffff)):
            for zoom in (0, 1, 2, 7, 15, 16, 31, 32, 33, 255, 0x4000, 0xffff):
                observe('scroll-zoom-line-boundaries', dict(flags[(i + j + zoom) & 3], lines=lines, zoom=zoom), [('scroll', [line])])
    for value in range(256):
        observe('scroll-status-byte', dict(flags[value & 3], gdc_status=[value, 4]), [('scroll', [17])])
    for base in flags:
        for statuses in ([0, 0, 4], [255], [0, 1, 2, 3, 0x80, 4]):
            observe('scroll-delayed-ready', dict(base, gdc_status=statuses), [('scroll', [399])])
        for cf in (0, 1):
            for ax in (0, 1, 0xffff, 0xbeef):
                observe('show-BIOS-replies', dict(base, bios_cf=cf, bios_ax=ax), [('show', [])])
        observe('connected-remaining-graphics', dict(base, gdc_status=[0, 4]), [('show', []), ('pack', [32, 0x100, 0x5000, 31, 0]),
                ('gaiji', [7, 91, 31, 1]), ('scroll', [399]), ('noclip', [16, 0x100, 0x5000, 31, 632])])
    return rows


def nonterminal(mz):
    meta, rows = analyze(mz.program_image), []
    for df in (False, True):
        for irq in (0, 512):
            for status in (0, 1, 2, 0x80):
                scenario = dict(df=df, flags=2 | irq, gdc_status=[status], zoom=0x4000)
                p, budget = DrawProbe(mz, scenario, meta), 1000
                model = Scalar(p)
                before = sha(bytes(model.mem))
                loops, phase = divmod(budget - meta['polling_prefix_instructions'], 4)
                expected_reads = loops + int(phase >= 2)
                expected_ip = (0x1720, 0x1722, 0x1724, 0x1726)[phase]
                try:
                    p.run('scroll', [17], budget)
                except ValueError as error:
                    if str(error) != 'draw terminal/budget differs':
                        raise
                else:
                    raise ValueError('draw stalled GDC unexpectedly returned')
                model.native['scroll'] += 1
                # Derive the complete polling prefix independently from decoded instruction counts.
                if p.status_index != expected_reads or p.get('IP') != expected_ip:
                    raise ValueError('draw stalled prefix instruction/input phase differs')
                for _ in range(expected_reads):
                    model.port(0x1722, 0xa0, status, 'in')
                    model.status_index += 1
                compare(p, model, None, None, 'stalled GDC prefix')
                if len(p.frames) != 1 or p.pending or p.stop or p.writes or any(e['direction'] == 'out' for e in p.ports):
                    raise ValueError('draw stalled prefix falsely completed or mutated screen')
                rows.append(dict(function='scroll', scenario=scenario, budget=budget, outcome='gdc-not-ready-instruction-budget',
                                 instruction=p.get('IP'), expected_input_count=expected_reads, native_entries=dict(p.native), port_count=len(p.ports), ports_sha256=trace_hash(p.ports),
                                 store_count=0, memory_before_sha256=before, memory_after_sha256=sha(bytes(model.mem))))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw, cold_raw = (ROOT / PROOF).read_bytes(), (ROOT / COLD).read_bytes()
    if sha(raw) != PROOF_SHA or sha(cold_raw) != COLD_SHA:
        raise ValueError('draw prior screen/cold proof differs')
    proof, cold = json.loads(raw), json.loads(cold_raw)
    inputs = {**proof['inputs'], PROOF: sha(raw), 'scripts/review_th03_mainl_draw.py': sha(Path(__file__).read_bytes()),
              'tests/test_mainl_draw_review.py': sha((ROOT / 'tests/test_mainl_draw_review.py').read_bytes())}
    providers = {p: subprocess.check_output(['git', 'show', f'{REVISION}:{p}'], cwd=ROOT / '_reference/ReC98') for p in PROVIDERS}
    def verify():
        for path, digest in inputs.items():
            if sha((ROOT / path).read_bytes()) != digest:
                raise ValueError('draw input changed: ' + path)
    def normalized(rows):
        return [{k: v for k, v in row.items() if k not in ('memory_before_sha256', 'memory_after_sha256')} for row in rows]
    verify()
    artifact = find_artifact(load_target_manifest(ROOT / 'config/targets.toml'), 'th03-mainl')
    stored = read_verified_artifact(ROOT, artifact)
    observations, objects = [], []
    for index, prior in enumerate(proof['observations']):
        path = prior['path']
        mz = parse_mz((ROOT / path).read_bytes())
        if not mz.valid:
            raise ValueError('draw invalid decoded image')
        observed = dict(path=path, analysis=analyze(mz.program_image), cpu=matrix(mz), nonterminal=nonterminal(mz))
        if index:
            if observed['analysis'] != observations[0]['analysis']:
                raise ValueError('draw complete bodies/CFG/table differ')
            tree = Path(path).parents[2]
            for provider, data in providers.items():
                cached = str(tree / provider)
                actual = (ROOT / cached).read_bytes()
                inputs[cached] = sha(actual)
                if actual.replace(b'\r\n', b'\n') != cached_provider(provider, data):
                    raise ValueError('draw frozen cached provider differs: ' + provider)
            object_path = str(tree / 'obj/th03/mainl.obj')
            data = (ROOT / object_path).read_bytes()
            obj = describe_omf(data)
            inputs[object_path] = sha(data)
            if (not obj['valid'] or obj['module_name'] != 'th03_mainl.asm' or obj['translator_comments'] != ['Turbo Assembler  Version 5.0']
                    or obj['dependency_timestamp_normalized_sha256'] != cold['rounds'][index - 1]['all_objects']['obj/th03/mainl.obj']):
                raise ValueError('draw cold root OMF differs')
            observed['object'] = {k: obj[k] for k in ('valid', 'sha256', 'dependency_timestamp_normalized_sha256', 'module_name', 'translator_comments')}
            objects.append(observed['object'])
            if len(objects) > 1 and objects[-1]['dependency_timestamp_normalized_sha256'] != objects[0]['dependency_timestamp_normalized_sha256']:
                raise ValueError('draw OMF differs beyond timestamps')
            map_path = str(tree / 'obj/th03/mainl.map')
            text = (ROOT / map_path).read_text()
            inputs[map_path] = sha((ROOT / map_path).read_bytes())
            carrier = next(row for row in code_rows(text, len(mz.program_image)) if row['module'] == 'th03_mainl.asm' and row['segment'] == 0 and row['size'])
            if not all(carrier['start'] <= a < a + z <= carrier['start'] + carrier['size'] for _, a, z in EXTENTS + [('prior-gdc', 0xc66, 11)]):
                raise ValueError('draw includes outside MAP carrier')
            for name, offset in PUBLICS.items():
                coordinates = {(int(s, 16), int(o, 16)) for s, o in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?' + re.escape(name) + r'\s*$', text, re.MULTILINE)}
                if coordinates != {(0, offset)}:
                    raise ValueError('draw public MAP entry differs')
            observed['carrier'], observed['public_entries'] = carrier, PUBLICS
            target = parse_mz((ROOT / proof['observations'][0]['path']).read_bytes())
            observed['comparisons'] = {n: extent_observation(target, mz, dict(start=a, size=z, segment=0, offset=a)) for n, a, z in EXTENTS + [('prior-gdc', 0xc66, 11)]}
            observed['data_comparisons'] = {n: extent_observation(target, mz, dict(start=0xe3f0 + a, size=z, segment=0xe3f, offset=a)) for n, a, z in [('clip-data', 0x522, 16), ('vram-data', 0x564, 12)]}
            if any(not row['raw_slice_equal'] or not row['ordered_relocations_equal'] for row in list(observed['comparisons'].values()) + list(observed['data_comparisons'].values())):
                raise ValueError('draw raw/ordered relocations differ')
            if normalized(observed['cpu']) != normalized(observations[0]['cpu']) or normalized(observed['nonterminal']) != normalized(observations[0]['nonterminal']):
                raise ValueError('draw target/cold CPU differs')
        observations.append(observed)
        print('Reviewed', path, len(observed['cpu']), 'scenarios', len(observed['nonterminal']), 'budgets', flush=True)
    verify()
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError('draw canonical target changed')
    for provider, data in providers.items():
        if subprocess.check_output(['git', 'show', f'{REVISION}:{provider}'], cwd=ROOT / '_reference/ReC98') != data:
            raise ValueError('draw frozen provider changed')
    result = dict(kind='th03-mainl-complete-draw-scroll-show-candidate-review', observed_utc=datetime.now(timezone.utc).isoformat(),
                  inputs=inputs, providers={p: sha(d) for p, d in providers.items()}, build_scaffold_main_remaps=BUILD_REMAPS,
                  observations=observations, tools=dict(capstone=version('capstone'), unicorn=version('unicorn')),
                  diagnostic_checks_pass=True, new_build=False, source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print('PASS MAINL draw CODE656/table1024/prior GDC11; declared font/GRCG/GDC/BIOS models; exact open:', args.output)


if __name__ == '__main__':
    main()
