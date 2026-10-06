#!/usr/bin/env python3
"""Complete root MAINL PI decoder with native allocation and explicit DOS bytes."""
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
from review_th03_mainl_super import SuperProbe
from review_th03_mainl_draw import return_cleanup, trace_hash
from review_th03_mainl_graphics import initial_flags, COLD, COLD_SHA
import review_th03_mainl_heap as heap
import review_th03_mainl_smem as smem
from review_th03_mainl_heap import TOP, OWN, ID, RESERVE, OUT, HEAP, HOLE, END, cached_provider, BUILD_REMAPS

ROOT = Path(__file__).resolve().parents[1]
PROOF = '.analysis/sol-mainl-draw-review-20261006.json'
PROOF_SHA = 'e5cf07b16edd05e7c0883c8283fe8707c257f5c0b70bb080c0061237297a2608'
OWN_RANGES = [('graph_free', 0xfec, 76, 8), ('error', 0x1038, 11, 12), ('load', 0x1044, 1211, 12),
              ('read_color', 0x1500, 238, 'near'), ('read_byte', 0x15ee, 44, 'near'), ('refill', 0x161a, 18, 'near')]
CONTEXT = heap.RANGES + smem.OWN_RANGES + [('dos_open', 0xaae, 26, 4)]
RANGES = OWN_RANGES + CONTEXT
ENTRY = {name: start for name, start, _, _ in RANGES if name != 'error'}
ENTRY['get'] = 0x1ec0
ALIGNMENT = {0x1043: 0x90, 0x14ff: 0x90}
FAR = {**heap.CALLS, 0x1ebb: 0x2186, 0xfff: 0x22b2, 0x1018: 0x22b2, 0x1031: 0x22b2,
       0x1052: 0xaae, 0x105e: 0x1ec0, 0x112b: 0x210a, 0x1184: 0x210a, 0x14f2: 0x1eaa}
NEAR = {**{a: 0x15ee for a in (0x10a1, 0x10a9, 0x10ba, 0x10c3, 0x10ca, 0x10d3, 0x10d8, 0x10e8,
                               0x10f6, 0x10fb, 0x1101, 0x1106, 0x110c, 0x1111, 0x1138, 0x1144, 0x1149, 0x1154, 0x1159, 0x11ba)},
        **{a: 0x1500 for a in (0x11c6, 0x11d0, 0x127a, 0x1284)},
        **{a: 0x161a for a in (0x11ff, 0x1241, 0x12b0, 0x12f0, 0x1325, 0x1375, 0x151b, 0x153c, 0x1560, 0x159d, 0x15f9)}}
DOS = {**heap.DOS, 0xaba: 0x3d, 0x107e: 0x3f, 0x1626: 0x3f, 0x14e8: 0x3e}
PUBLICS = {'GRAPH_PI_FREE': 0xfec, 'GRAPH_PI_LOAD_PACK': 0x1044}
PROVIDERS = list(dict.fromkeys(smem.PROVIDERS + ['libs/master.lib/graph_pi_free.asm',
    'libs/master.lib/graph_pi_load_pack.asm', 'libs/master.lib/dos_ropen.asm', 'libs/master.lib/dos_ropen[data].asm']))
PATTERN = bytes((i * 37 + 3) & 255 for i in range(0x50001))


def color_bits(rank):
    if not 0 <= rank < 16:
        raise ValueError('synthetic color rank outside grammar')
    if rank < 2:
        return '1' + str(rank)
    if rank < 4:
        return '00' + str(rank - 2)
    if rank < 8:
        return '010' + format(rank - 4, '02b')
    return '011' + format(rank - 8, '03b')


def position_bits(position):
    if not 0 <= position <= 4:
        raise ValueError('synthetic position outside grammar')
    return format(position, '02b') if position < 3 else '11' + str(position - 3)


def length_bits(length):
    if not 1 <= length < 1 << 32:
        raise ValueError('synthetic length outside bounded grammar')
    bits = format(length, 'b')
    return '1' * (len(bits) - 1) + '0' + bits[1:]


def copy_bits(position, length):
    return position_bits(position) + length_bits(length)


class PrefixStop(Exception):
    """Harness stop before the next private byte call; never a synthetic return."""


def analyze(image):
    context = smem.analyze(image)
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    decoded, bounds, returns, rows = [], set(), {}, []
    for name, start, size, cleanup in RANGES:
        body = image[start:start + size]
        instructions = list(decoder.disasm(body, start))
        if len(body) != size or not instructions or sum(i.size for i in instructions) != size:
            raise ValueError('PI decoder complete instruction partition differs')
        if name != 'byte' and return_cleanup(instructions[-1]) != cleanup:
            raise ValueError('PI decoder terminal cleanup differs')
        bounds.update(i.address for i in instructions)
        decoded.append((name, start, size, cleanup, instructions))
    for name, start, size, cleanup, instructions in decoded:
        edges = []
        for index, i in enumerate(instructions):
            if i.mnemonic in ('ret', 'retf'):
                if return_cleanup(i) != cleanup:
                    raise ValueError('PI decoder interior cleanup differs')
                returns[i.address] = cleanup
            if i.mnemonic in ('in', 'out'):
                raise ValueError('PI decoder unexpected port')
            if i.mnemonic == 'int' and (i.address not in DOS or i.bytes != b'\xcd\x21'):
                raise ValueError('PI decoder unknown DOS site')
            if not (i.mnemonic.startswith(('j', 'loop')) or i.mnemonic in ('call', 'lcall', 'ljmp')):
                continue
            if not i.operands or any(o.type != X86_OP_IMM for o in i.operands):
                raise ValueError('PI decoder unknown indirect edge')
            if i.mnemonic in ('lcall', 'ljmp'):
                raise ValueError('PI decoder unknown far edge')
            destination = i.operands[0].imm
            if i.mnemonic == 'call':
                if NEAR.get(i.address) != destination:
                    if FAR.get(i.address) != destination:
                        raise ValueError('PI decoder unknown native call')
                    if not index or instructions[index - 1].bytes != b'\x0e':
                        raise ValueError('PI decoder far call lacks PUSH CS')
            elif destination not in bounds:
                raise ValueError('PI decoder branch enters operand/neighbor')
            edges.append(dict(instruction=i.address, kind=i.mnemonic, destination=destination))
        rows.append(dict(name=name, offset=start, size=size, instructions=len(instructions), cleanup=cleanup,
                         sha256=sha(image[start:start + size]), edges=edges))
    if any(image[a:a + 1] != bytes([v]) for a, v in (ALIGNMENT | heap.ALIGNMENT | smem.ALIGNMENT).items()):
        raise ValueError('PI decoder producer alignment differs')
    return dict(bodies=rows, bounds=sorted(bounds), returns=returns, new_body_bytes=1598,
                new_alignment_bytes=2, new_extent_bytes=1600, prior_context_bytes=730,
                alignment=ALIGNMENT, heap_stack=context)


def stream_data(s):
    if 'file_hex' in s:
        return bytes.fromhex(s['file_hex'])
    width, height, mode = s.get('width', 2), s.get('height', 1), s.get('mode', 0)
    bits = s.get('bits', '1010' + '00' + '0')
    packed = bytes(int((bits + '0' * ((-len(bits)) % 8))[i:i + 8], 2) for i in range(0, len(bits), 8))
    machine = bytes(s.get('machine', [65, 66, 67, 68]))
    extension = bytes(s.get('extension', []))
    return (bytes(s.get('magic', [80, 105])) + bytes(s.get('comment', [])) + b'\x1a' + bytes(s.get('dummy', [])) + b'\0'
            + bytes([mode]) + struct.pack('>H', s.get('aspect', 0)) + bytes([s.get('planes', 4)]) + machine
            + struct.pack('>H', s.get('extension_length', len(extension))) + extension + struct.pack('>HH', width, height)
            + (b'' if mode & 128 else bytes((i * 13 + 7) & 255 for i in range(48))) + packed)


class DecoderProbe(Probe):
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
        self.s, self.meta = scenario, meta or analyze(mz.program_image)
        self.bounds, self.returns = set(self.meta['bounds']), self.meta['returns']
        self.entry_names = {a: n for n, a in ENTRY.items()}
        self.calls = FAR | NEAR
        self.pending, self.frames, self.stop, self.errors = None, [], False, []
        self.paused, self.pause_kind, self.zero_chunks = False, None, 0
        self.native, self.events, self.writes, self.visited = Counter(), [], [], set()
        self.temp, self.file_pos, self.read_index, self.dos_index = None, 0, 0, 0
        self.file = stream_data(scenario)
        self.uc.mem_write(0x50000, PATTERN)
        self.uc.mem_write(0x50100, b'synthetic.pi\0')
        for offset, key, default in ((TOP, 'top', 0x6000), (OWN, 'own', 0), (ID, 'id', 0xbeef),
                                     (RESERVE, 'reserve', 256), (OUT, 'out', 0x9000), (HEAP, 'heap', 0x9000),
                                     (HOLE, 'hole', 0), (END, 'end', 0x6000), (0x558, 'sharing', 0xa500)):
            self.uc.mem_write(self.data + offset, struct.pack('<H', scenario.get(key, default)))
        for segment, using, next_segment, identifier in scenario.get('blocks', []):
            self.uc.mem_write(segment * 16, struct.pack('<3H', using, next_segment, identifier))
        for segment, offset, values in scenario.get('initial_values', []):
            for index, value in enumerate(values):
                self.uc.mem_write(segment * 16 + u16(offset + index), bytes([value]))

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
                    raise ValueError('PI decoder terminal segment alias')
                if self.frames or self.pending:
                    raise ValueError('PI decoder unfinished native frame')
                self.stop = True
                uc.emu_stop()
                return
            off = address - self.code
            if self.get('CS') != 0x2000 or self.get('SS') != 0x4000:
                raise ValueError('PI decoder CODE/stack segment alias')
            if off not in self.bounds:
                raise ValueError('CPU escaped PI decoder instruction boundaries')
            if off == ENTRY['read_byte'] and self.native['read_byte'] == scenario.get('pause_after_bytes'):
                self.paused, self.pause_kind = True, 'byte'
                uc.emu_stop()
                return
            if off == 0x13ee and self.get('SI') == self.get('DI') == 0 and 'pause_zero_copy_after' in scenario:
                self.zero_chunks += 1
                if self.zero_chunks == scenario['pause_zero_copy_after']:
                    self.paused, self.pause_kind = True, 'zero-copy'
                    uc.emu_stop()
                    return
            self.visited.add(off)
            name = self.entry_names.get(off)
            if name and not (name == 'get' and self.pending is None and self.frames and self.frames[-1]['name'] == 'get'):
                self.enter(name, next(c for n, _, _, c in RANGES if n == name))
                self.native[name] += 1
            if off in self.calls:
                name = self.entry_names[self.calls[off]]
                self.prepare(name, self.get('SP') - 2, off + 3, 'near' if off in NEAR else next(c for n, _, _, c in RANGES if n == name))
            if off in self.returns:
                if self.frames and self.frames[-1]['name'] == 'get' and not self.get('EFLAGS') & 1:
                    self.temp = self.get('AX') * 16
                self.leave(self.returns[off])

        def write(uc, access, address, size, value, user):
            if self.stack <= address and address + size <= self.stack + 65536:
                return
            if not (self.data <= address and address + size <= self.data + 65537 or 0x50000 <= address and address + size <= 0xa0001):
                raise ValueError('PI decoder store outside declared state/buffer/heap span')
            if 0xfec <= self.get('IP') < 0x162c and not (self.temp is not None and self.temp + 0x4000 <= address and address + size <= self.temp + 0x4114):
                self.writes.append([address, size, value])

        def intr(uc, number, user):
            site, ah = u16(self.get('IP') - 2), self.get('AH')
            if number != 0x21 or self.get('CS') != 0x2000 or DOS.get(site) != ah:
                raise ValueError('PI decoder unknown DOS request/site')
            if ah == 0x3d:
                ax, cf = scenario.get('open_ax', 0x1234), scenario.get('open_cf', 0)
                event = dict(site=site, name='dos_open', mode=self.get('AL'), filename=[self.get('DX'), self.get('DS')], ax=ax, cf=cf)
            elif ah == 0x3e:
                ax, cf = scenario.get('close_ax', 7), scenario.get('close_cf', 0)
                event = dict(site=site, name='dos_close', handle=self.get('BX'), ax=ax, cf=cf)
            elif ah == 0x3f:
                items = scenario.get('reads', [])
                item = items[self.read_index] if self.read_index < len(items) else {}
                self.read_index += 1
                count, offset, segment = self.get('CX'), self.get('DX'), self.get('DS')
                if count != 16384 or offset or self.temp is None or segment * 16 != self.temp:
                    raise ValueError('PI decoder DOS buffer/count differs')
                payload = bytes.fromhex(item['payload_hex']) if 'payload_hex' in item else self.file[self.file_pos:self.file_pos + min(count, item.get('limit', count))]
                payload = payload[:count]
                ax, cf = item.get('ax', len(payload)), item.get('cf', 0)
                if cf and not item.get('inject_on_failure'):
                    payload = b''
                self.file_pos += len(payload)
                if payload:
                    uc.mem_write(segment * 16 + offset, payload)
                event = dict(site=site, name='dos_read', handle=self.get('BX'), destination=[offset, segment], count=count,
                             payload_size=len(payload), payload_sha256=sha(payload), ax=ax, cf=cf)
            elif ah == 0x48:
                items = scenario.get('dos_allocs', [])
                item = items[self.dos_index] if self.dos_index < len(items) else {}
                self.dos_index += 1
                query, size = site == 0x218c, self.get('BX')
                ax, cf = item.get('ax', 8 if query else 0x6000), item.get('cf', 1 if query else 0)
                bx = item.get('bx', scenario.get('largest', 0x3000) if query else size)
                self.set('BX', bx)
                event = dict(site=site, name='dos_allocate', size=size, ax=ax, bx=bx, cf=cf)
            else:
                ax, cf = scenario.get('dos_free_ax', 7), scenario.get('dos_free_cf', 1)
                event = dict(site=site, name='dos_free', segment=self.get('ES'), ax=ax, cf=cf)
            self.events.append(event)
            self.set('AX', ax)
            self.set('EFLAGS', (self.get('EFLAGS') & ~1) | cf)

        def out(*args):
            raise ValueError('PI decoder unexpected output port')
        def inp(*args):
            raise ValueError('PI decoder unexpected input port')
        self.uc.hook_add(UC_HOOK_CODE, guard(code))
        self.uc.hook_add(UC_HOOK_MEM_WRITE, guard(write))
        self.uc.hook_add(UC_HOOK_INTR, guard(intr))
        self.uc.hook_add(UC_HOOK_INSN, guard(out), None, 1, 0, reg.UC_X86_INS_OUT)
        self.uc.hook_add(UC_HOOK_INSN, guard(inp, 0), None, 1, 0, reg.UC_X86_INS_IN)

    def run(self, name, args=(), budget=3000000):
        if name not in ('load', 'graph_free'):
            raise ValueError('PI decoder private helper requires complete public caller')
        self.stop, self.pending, self.paused = False, None, False
        self.frames.clear()
        self.errors.clear()
        cleanup = next(c for n, _, _, c in RANGES if n == name)
        values = dict(CS=0x2000, DS=0x2e3f, SS=0x4000, ES=0x3333, AX=0x1111, BX=0x2222,
                      CX=0x3333, DX=0x4444, BP=0x7777, SI=0x1357, DI=0x2468, SP=0xffc0, EFLAGS=initial_flags(self.s))
        for register, value in values.items():
            self.set(register, value)
        self.uc.mem_write(self.stack + 0xffc0, struct.pack('<' + 'H' * (2 + len(args)), 0xff00, 0x2000, *args))
        self.prepare(name, 0xffc0, 0xff00, cleanup)
        self.uc.emu_start(self.code + ENTRY[name], 0x100000, count=budget)
        if self.errors:
            raise ValueError(self.errors[0])
        if self.paused:
            if (self.stop or len(self.frames) != 1 or self.frames[0]['name'] != 'load'
                    or self.pause_kind == 'byte' and (not self.pending or self.pending['name'] != 'read_byte')
                    or self.pause_kind == 'zero-copy' and self.pending):
                raise ValueError('PI decoder semantic prefix native frame differs')
            return
        if not self.stop:
            raise ValueError('PI decoder terminal/budget differs')
        if self.get('SP') != 0xffc4 + cleanup or any(self.get(r) != values[r] for r in ('BP', 'SI', 'DI', 'DS')):
            raise ValueError('PI decoder cleanup/preserved-register differs')


class Scalar(smem.Scalar):
    def __init__(self, p):
        super().__init__(p)
        self.flags, self.file, self.file_pos, self.read_index = initial_flags(p.s), bytes(p.file), 0, 0
        self.temp, self.writes, self.decode_steps = None, [], []

    def own_write(self, address, size, value):
        self.mem[address:address + size] = value.to_bytes(size, 'little')
        if not (self.temp is not None and self.temp + 0x4000 <= address and address + size <= self.temp + 0x4114):
            self.writes.append([address, size, value])

    def tword(self, offset, value):
        self.w(self.temp + offset, value)

    def read(self, site, handle, segment):
        items = self.s.get('reads', [])
        item = items[self.read_index] if self.read_index < len(items) else {}
        self.read_index += 1
        payload = bytes.fromhex(item['payload_hex']) if 'payload_hex' in item else self.file[self.file_pos:self.file_pos + min(16384, item.get('limit', 16384))]
        payload = payload[:16384]
        ax, cf = item.get('ax', len(payload)), item.get('cf', 0)
        if cf and not item.get('inject_on_failure'):
            payload = b''
        self.file_pos += len(payload)
        self.mem[segment * 16:segment * 16 + len(payload)] = payload
        self.events.append(dict(site=site, name='dos_read', handle=handle, destination=[0, segment], count=16384,
                                payload_size=len(payload), payload_sha256=sha(payload), ax=ax, cf=cf))

    def next_byte(self):
        pointer = self.word(self.temp + 0x4110)
        if pointer == 16384:
            self.native['refill'] += 1
            self.read(0x1626, self.word(self.temp + 0x410e), self.temp >> 4)
            pointer = 0
        value = self.mem[self.temp + pointer]
        self.tword(0x4110, pointer + 1)
        return value

    def bits(self, count):
        value = 0
        for _ in range(count):
            length = self.mem[self.temp + 0x4113]
            if not length:
                self.mem[self.temp + 0x4112] = self.next_byte()
                length = 8
            buffer = self.mem[self.temp + 0x4112]
            value = (value << 1) | (buffer >> 7)
            self.mem[self.temp + 0x4112] = (buffer << 1) & 255
            self.mem[self.temp + 0x4113] = length - 1
        return value

    def byte(self):
        if self.native['read_byte'] == self.s.get('pause_after_bytes'):
            raise PrefixStop()
        self.native['read_byte'] += 1
        return self.bits(8)

    def color(self, previous):
        self.native['read_color'] += 1
        if self.bits(1):
            rank = self.bits(1)
        elif not self.bits(1):
            rank = 2 + self.bits(1)
        elif not self.bits(1):
            rank = 4 + self.bits(2)
        else:
            rank = 8 + self.bits(3)
        index, row = rank ^ 15, self.temp + 0x400c + (previous & 255) * 16
        value = self.mem[row + index]
        if index != 15:
            for i in range(index, 15):
                self.mem[row + i] = self.mem[row + i + 1]
            self.mem[row + 15] = value
        return value

    def graph_free(self, args):
        image_offset, image_segment, header_offset, header_segment = args
        for field in (0, 16):
            segment = self.word(header_segment * 16 + u16(header_offset + field + 2))
            if segment:
                self.run('free', [segment])
                for offset in ((4, 2, 0) if not field else (14, 18, 16)):
                    self.own_write(header_segment * 16 + u16(header_offset + offset), 2, 0)
        if image_segment:
            self.run('free', [image_segment])
        return None, None

    def load(self, args):
        output_offset, output_segment, header_offset, header_segment, file_offset, file_segment = args
        self.flags &= ~1024
        handle, carry = self.run('dos_open', [file_offset, file_segment])
        if carry:
            return 65534, 1
        temporary, carry = self.run('get', [16660])
        if carry:
            return temporary, 1
        self.temp = temporary * 16
        self.tword(0x410e, handle)
        self.mem[self.temp + 0x4112:self.temp + 0x4114] = b'\0\0'
        self.tword(0x4110, 0)
        self.read(0x107e, handle, temporary)
        for previous in range(16):
            self.mem[self.temp + 0x400c + previous * 16:self.temp + 0x401c + previous * 16] = bytes((previous + 1 + index) & 15 for index in range(16))
        if self.byte() != 80 or self.byte() != 105:
            return 65523, 1
        cursor = header_offset
        def header(value, size=2):
            nonlocal cursor
            self.own_write(header_segment * 16 + cursor, size, value)
            cursor = u16(cursor + size)
        header(0)
        header(0)
        comment = 0
        for _ in range(100000):
            if self.byte() == 26:
                break
            comment = u16(comment + 1)
        else:
            raise ValueError('scalar PI comment budget')
        header(comment)
        for _ in range(100000):
            if not self.byte():
                break
        else:
            raise ValueError('scalar PI dummy budget')
        mode = self.byte()
        header(mode, 1)
        self.mem[self.temp + 0x410c] = mode
        aspect = (self.byte() << 8) | self.byte()
        header(aspect)
        if aspect:
            return 65523, 1
        planes = self.byte()
        if planes != 4:
            return 65523, 1
        header(planes, 1)
        for _ in range(2):
            low, high = self.byte(), self.byte()
            header(low | (high << 8))
        extension = (self.byte() << 8) | self.byte()
        header(extension)
        header(0)
        self.own_write(self.data + ID, 2, 10)
        machine, carry = self.run('long', [extension, 0])
        header(machine)
        if not carry:
            for index in range(extension):
                self.own_write(machine * 16 + index, 1, self.byte())
        width = (self.byte() << 8) | self.byte()
        header(width)
        self.tword(0x4000, width)
        height = (self.byte() << 8) | self.byte()
        header(height)
        self.tword(0x4002, height)
        allocation = (width * u16(height + 2)) >> 1
        end_offset, end_delta = allocation & 65535, u16((allocation >> 16) << 12)
        self.tword(0x4008, end_offset)
        self.tword(0x400a, end_delta)
        self.own_write(self.data + ID, 2, 10)
        image, carry = self.run('long', [allocation & 65535, allocation >> 16])
        if carry:
            return 65528, 1
        self.tword(0x4004, 0)
        self.tword(0x4006, image)
        self.tword(0x400a, image + end_delta)
        self.own_write(output_segment * 16 + output_offset, 2, width)
        self.own_write(output_segment * 16 + u16(output_offset + 2), 2, image)
        self.mem[self.temp + 0x410c] = (mode << 1) & 255
        if not mode & 128:
            for _ in range(48):
                header(self.byte(), 1)
        left = self.color(0)
        right = self.color(left)
        fill = (left << 4) | right
        for i in range(width):
            self.own_write(image * 16 + i, 1, fill)
        destination, offset, previous_position = image, width, 255
        def store(value):
            nonlocal destination, offset
            self.own_write(destination * 16 + offset, 1, value)
            offset = u16(offset + 1)
            if not offset:
                destination = u16(destination + 0x1000)
        def back(distance):
            segment = u16(destination - (0x1000 if offset < distance else 0))
            return self.mem[segment * 16 + u16(offset - distance)]
        for _ in range(200000):
            position = self.bits(2)
            if position == 3:
                position += self.bits(1)
            if position == previous_position:
                previous = back(1) & 15
                while True:
                    left = self.color(previous)
                    right = self.color(left)
                    previous = right
                    store((left << 4) | right)
                    if not self.bits(1):
                        break
                previous_position = 255
                self.decode_steps.append(dict(kind='literal', position=position, segment=destination, offset=offset))
            else:
                length_bits = 0
                while self.bits(1):
                    length_bits += 1
                    if length_bits > 31:
                        raise ValueError('scalar PI length budget')
                length = (1 << length_bits) | self.bits(length_bits)
                low, high = length & 65535, length >> 16
                if not position:
                    last = back(1)
                    values = [last] if last == ((last >> 4) | ((last & 15) << 4)) else [back(2), last]
                    # LOOP starts at zero for an empty low word, then the high-word
                    # SUB/CF test schedules one additional full 65536-byte cycle.
                    copies = length + (65536 if not low else 0)
                    for index in range(copies):
                        store(values[index % len(values)])
                else:
                    distance = width * 2 if position == 2 else width if position == 1 else u16(width - 1) if position == 3 else u16(width + 1)
                    half = distance & 1
                    amount = (distance >> 1) + half
                    source = u16(offset - amount)
                    source_segment = u16(destination - (0x1000 if offset < amount else 0))
                    if half:
                        for _ in range(low or 65536):
                            value = self.mem[source_segment * 16 + source]
                            source = u16(source + 1)
                            if not source:
                                source_segment = u16(source_segment + 0x1000)
                            value = ((value & 15) << 4) | (self.mem[source_segment * 16 + source] >> 4)
                            store(value)
                    else:
                        remaining, zero_chunks = low, 0
                        for _ in range(10000):
                            if source == offset == 0 and 'pause_zero_copy_after' in self.s:
                                zero_chunks += 1
                                if zero_chunks == self.s['pause_zero_copy_after']:
                                    self.prefix = dict(source_segment=source_segment, destination_segment=destination,
                                                       source=source, destination=offset, remaining=remaining, zero_chunks=zero_chunks)
                                    raise PrefixStop()
                            # REP chunks end at whichever 16-bit pointer wraps first.
                            capacity = u16(-max(source, offset))
                            count = min(remaining, capacity) if remaining else capacity
                            remaining = u16(remaining - count)
                            for _ in range(count):
                                value = self.mem[source_segment * 16 + source]
                                source = u16(source + 1)
                                if not source:
                                    source_segment = u16(source_segment + 0x1000)
                                store(value)
                            if not count:
                                if not source:
                                    source_segment = u16(source_segment + 0x1000)
                                if not offset:
                                    destination = u16(destination + 0x1000)
                            if not remaining:
                                break
                        else:
                            raise ValueError('scalar PI zero-progress aligned copy budget')
                previous_position = position
                self.decode_steps.append(dict(kind='copy', position=position, length=length, segment=destination, offset=offset))
            if offset >= end_offset and destination >= u16(image + end_delta):
                break
        else:
            raise ValueError('scalar PI decode budget')
        self.events.append(dict(site=0x14e8, name='dos_close', handle=handle, ax=self.s.get('close_ax', 7), cf=self.s.get('close_cf', 0)))
        self.run('release', [temporary])
        return 0, 0

    def run(self, name, args=()):
        if name not in ('load', 'graph_free', 'dos_open'):
            return super().run(name, args)
        self.native[name] += 1
        if name == 'graph_free':
            return self.graph_free(args)
        if name == 'load':
            return self.load(args)
        ax, carry = self.s.get('open_ax', 0x1234), self.s.get('open_cf', 0)
        self.events.append(dict(site=0xaba, name='dos_open', mode=self.get(0x558) & 255, filename=list(args), ax=ax, cf=carry))
        return (65534 if carry else ax), carry


def compare(p, model, ax, carry, label):
    if ((ax is not None and p.get('AX') != ax) or (carry is not None and p.get('EFLAGS') & 1 != carry)
            or (p.get('EFLAGS') ^ model.flags) & (512 | 1024) or p.native != model.native or p.events != model.events
            or p.writes != model.writes or (p.file_pos, p.read_index, p.temp) != (model.file_pos, model.read_index, model.temp)):
        raise ValueError('PI decoder scalar registers/flags/native/DOS/output stores differ: ' + str((label, p.get('AX'), ax, p.get('EFLAGS') & 1, carry, dict(p.native), dict(model.native), p.events, model.events, len(p.writes), len(model.writes), p.writes[:16], model.writes[:16])))
    actual = bytes(p.uc.mem_read(0, 0x100000))
    if actual[:p.stack] != model.mem[:p.stack] or actual[p.stack + 65536:] != model.mem[p.stack + 65536:]:
        changed = [i for i, (a, b) in enumerate(zip(actual, model.mem)) if a != b and not p.stack <= i < p.stack + 65536]
        raise ValueError('PI decoder full physical memory differs: ' + str((label, changed[:24], [(i, actual[i], model.mem[i]) for i in changed[:12]])))


EXTENTS = [('complete-pi', 0xfec, 1600), ('prior-heap', 0x210a, 628),
           ('prior-stack', 0x1eaa, 76), ('prior-dos-open', 0xaae, 26)]
LOAD_ARGS = [0x300, 0x5000, 0x200, 0x5000, 0x100, 0x5000]


def matrix(mz):
    meta, rows = analyze(mz.program_image), []
    flags = [dict(df=df, flags=2 | irq, initial_cf=cf) for df, irq, cf in
             ((False, 0, 0), (True, 0, 1), (False, 512, 1), (True, 512, 0))]
    def observe(label, scenario, free=False, args=None):
        p = DecoderProbe(mz, scenario, meta)
        model = Scalar(p)
        before = sha(bytes(model.mem))
        results = []
        model.flags = initial_flags(scenario)
        ax, cf = model.run('load', args or LOAD_ARGS)
        p.run('load', args or LOAD_ARGS)
        compare(p, model, ax, cf, label)
        results.append(dict(function='load', args=args or LOAD_ARGS, ax=ax, cf=cf))
        if free and not cf:
            header_offset, header_segment = (args or LOAD_ARGS)[2:4]
            output_offset, output_segment = (args or LOAD_ARGS)[:2]
            free_args = [model.word(output_segment * 16 + output_offset), model.word(output_segment * 16 + u16(output_offset + 2)), header_offset, header_segment]
            for _ in range(2):
                model.flags = initial_flags(scenario)
                ax, cf = model.run('graph_free', free_args)
                p.run('graph_free', free_args)
                compare(p, model, ax, cf, label + '/free')
                results.append(dict(function='graph_free', args=free_args, ax=ax, cf=cf))
        rows.append(dict(label=label, scenario=scenario, steps=results, top_level_calls=len(results),
                         file_sha256=sha(p.file), file_bytes=len(p.file), events=p.events, native_entries=dict(p.native),
                         visited=sorted(p.visited), decode_steps=model.decode_steps, store_count=len(p.writes), stores_sha256=trace_hash(p.writes),
                         memory_before_sha256=before, memory_after_sha256=sha(bytes(model.mem))))
    for base in flags:
        for scenario in ({}, {'mode':128}, {'mode':255}, {'height':0}, {'width':0}, {'height':65534},
                         {'open_cf':1}, {'magic':[0,105]}, {'magic':[80,0]}, {'aspect':1}, {'aspect':65535}, {'planes':0}, {'planes':8},
                         {'heap':0x6412,'out':0x6412}, {'heap':0x6413,'out':0x6413},
                         {'extension':[1,2,3,4,5]}, {'extension_length':100,'extension':[], 'heap':0x6416,'out':0x6416},
                         {'reads':[{'cf':1}]}, {'reads':[{'cf':1,'inject_on_failure':True,'ax':0}]},
                         {'reads':[{'ax':0}]}, {'reads':[{'ax':65535}]}, {'reads':[{'limit':0}]},
                         {'close_cf':1,'close_ax':65535}, {'top':0,'largest':0x3000},
                         {'top':0,'largest':0x3000,'dos_allocs':[{}, {'cf':1}]}):
            observe('header-allocation-DOS-flags', dict(base, **scenario), free=True)
    for left in range(16):
        for right in range(16):
            observe('color-MTF-all-contexts', dict(flags[(left+right)&3], bits=color_bits(left)+color_bits(right)+copy_bits(0,1)))
    for sharing in range(256):
        observe('DOS-sharing-byte', dict(flags[sharing&3], sharing=0xa500|sharing, open_cf=1))
    for position in range(5):
        for width in (1,2,3,7,8):
            for length in (1,2,3,7,8,127,128,255,256,257):
                observe('all-copy-positions-geometry-length', dict(flags[(position+width+length)&3], width=width, height=0,
                        bits='1011'+copy_bits(position,length)))
        for length in (1023,32767,65535,65536,65537):
            # The zero-position branch honors the full length. Other positions use only its low word.
            observe('length-word-and-segment-boundaries', dict(width=2, height=0, heap=0x8000, out=0x8000,
                    bits='1010'+copy_bits(position,length)))
        if position:
            observe('length-high-word-ignored', dict(bits='1010'+copy_bits(position,16777217)))
        literal = ''.join(color_bits((i*7)&15)+color_bits((i*11+3)&15)+('1' if i<7 else '0') for i in range(8))
        for base in flags:
            observe('literal-continuation-and-position-reset', dict(base, width=2, height=12,
                    bits='1011'+copy_bits(position,1)+position_bits(position)+literal+copy_bits(position,8)), free=True)
        for width in (60000,60001):
            observe('source-destination-segment-crossing', dict(width=width, height=1, heap=0x8000,out=0x8000,
                    bits='1011'+copy_bits(position,65535)))
    for comment in (16312,16313,16314,16315,16316,16317,16318,16319):
        literal = ''.join(color_bits(i&15)+color_bits((i+7)&15)+('1' if i<63 else '0') for i in range(64))
        observe('compressed-bit-refill-boundaries', dict(comment=[65]*comment,width=2,height=63,
                bits='1011'+copy_bits(0,1)+position_bits(0)+literal))
    for comment,bits in ((16317,'000000'+copy_bits(4,1)), (16317,'1010'+copy_bits(3,8)),
                         (16316,'1010'+copy_bits(0,256)), (16316,'1010'+copy_bits(0,128))):
        observe('private-position-unary-byte-context-refill', dict(comment=[65]*comment,bits=bits))
    for position in (0,1,2,3,4):
        observe('post-wrap-reference-borrow', dict(width=60000,height=2,heap=0x8000,out=0x8000,
                bits='1011'+copy_bits(2,5536)+copy_bits(position,60000)))
    for width,first in ((60000,5536),(65534,1)):
        literal=''.join(color_bits(i&15)+color_bits((i+7)&15)+('1' if i<7 else '0') for i in range(8))
        observe('literal-back-reference-and-output-wrap', dict(width=width,height=1,heap=0x8000,out=0x8000,
                bits='1011'+copy_bits(2,first)+position_bits(2)+literal+copy_bits(0,40000)))
    for comment in (16384,32768,65536):
        observe('comment-buffer-refill-and-word-wrap', dict(comment=[65]*comment), free=True)
    for dummy in (1,255,16384):
        observe('dummy-buffer-refill', dict(dummy=[66]*dummy))
    for count in (1,255,16384):
        observe('machine-extension-refill', dict(extension=[(i*19+7)&255 for i in range(count)]), free=True)
    for base in flags:
        observe('far-header-output-pointer-wrap', base, free=True, args=[0xffff,0x5000,0xfffe,0x5000,0x100,0x5000])
    for base in flags:
        for mask in range(8):
            header = bytearray(22)
            struct.pack_into('<3H', header,0,0xabcd,0x6001 if mask&1 else 0,17)
            struct.pack_into('<3H', header,14,23,0xdcba,0x6011 if mask&2 else 0)
            scenario = dict(base, out=0x6100, heap=0x6000, blocks=[[0x6000,1,0x6010,1],[0x6010,1,0x6020,2],[0x6020,1,0x6100,3]],
                            initial_values=[[0x5000,0x200,list(header)]])
            p = DecoderProbe(mz,scenario,meta);model=Scalar(p);before=sha(bytes(model.mem));args=[0xbeef,0x6021 if mask&4 else 0,0x200,0x5000]
            ax,cf=model.run('graph_free',args);p.run('graph_free',args);compare(p,model,ax,cf,'all-free-presence')
            rows.append(dict(label='all-free-presence',scenario=scenario,steps=[dict(function='graph_free',args=args,ax=ax,cf=cf)],top_level_calls=1,
                             events=p.events,native_entries=dict(p.native),visited=sorted(p.visited),store_count=len(p.writes),stores_sha256=trace_hash(p.writes),
                             memory_before_sha256=before,memory_after_sha256=sha(bytes(model.mem))))
    return rows


def nonterminal(mz):
    meta, rows = analyze(mz.program_image), []
    for df in (False,True):
        for irq in (0,512):
            for kind in ('comment','dummy'):
                for count in (200,16390):
                    data=b'Pi'+(b'\x1a' if kind=='dummy' else b'')+b'A'*33000
                    scenario=dict(df=df,flags=2|irq,file_hex=data.hex(),pause_after_bytes=count)
                    p=DecoderProbe(mz,scenario,meta);model=Scalar(p);before=sha(bytes(model.mem))
                    try:model.run('load',LOAD_ARGS)
                    except PrefixStop:pass
                    else:raise ValueError('PI decoder scalar semantic prefix unexpectedly returned')
                    p.run('load',LOAD_ARGS)
                    compare(p,model,None,None,'unterminated '+kind)
                    if not p.paused or p.stop or p.get('IP')!=ENTRY['read_byte'] or p.native['read_byte']!=count:
                        raise ValueError('PI decoder private byte prefix falsely completed')
                    rows.append(dict(function='load',scenario=scenario,outcome='unterminated-'+kind+'-semantic-prefix',instruction=p.get('IP'),
                                     native_entries=dict(p.native),events=p.events,pending=p.pending,frames=p.frames,visited=sorted(p.visited),store_count=len(p.writes),stores_sha256=trace_hash(p.writes),
                                     memory_before_sha256=before,memory_after_sha256=sha(bytes(model.mem))))
    for df in (False,True):
        for irq in (0,512):
            scenario=dict(df=df,flags=2|irq,width=1,height=0,heap=0x8000,out=0x8000,
                          bits='1011'+copy_bits(3,65536),pause_zero_copy_after=4)
            p=DecoderProbe(mz,scenario,meta);model=Scalar(p);before=sha(bytes(model.mem))
            try:model.run('load',LOAD_ARGS)
            except PrefixStop:pass
            else:raise ValueError('PI decoder scalar zero-copy prefix unexpectedly returned')
            p.run('load',LOAD_ARGS)
            compare(p,model,None,None,'zero-progress aligned copy')
            state=model.prefix
            if (not p.paused or p.pause_kind!='zero-copy' or p.stop or p.get('IP')!=0x13ee
                    or (p.get('DS'),p.get('ES'),p.get('SI'),p.get('DI'),p.get('AX'),p.zero_chunks)
                    != tuple(state[k] for k in ('source_segment','destination_segment','source','destination','remaining','zero_chunks'))):
                raise ValueError('PI decoder zero-copy prefix phase differs')
            rows.append(dict(function='load',scenario=scenario,outcome='zero-progress-aligned-copy-semantic-prefix',instruction=p.get('IP'),
                             prefix=state,native_entries=dict(p.native),events=p.events,pending=p.pending,frames=p.frames,visited=sorted(p.visited),
                             store_count=len(p.writes),stores_sha256=trace_hash(p.writes),memory_before_sha256=before,memory_after_sha256=sha(bytes(model.mem))))
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    raw, cold_raw = (ROOT / PROOF).read_bytes(), (ROOT / COLD).read_bytes()
    if sha(raw) != PROOF_SHA or sha(cold_raw) != COLD_SHA:
        raise ValueError('PI decoder prior drawing/cold proof differs')
    proof, cold = json.loads(raw), json.loads(cold_raw)
    inputs = {**proof['inputs'], PROOF: sha(raw), 'scripts/review_th03_mainl_pi_decoder.py': sha(Path(__file__).read_bytes()),
              'tests/test_mainl_pi_decoder_review.py': sha((ROOT / 'tests/test_mainl_pi_decoder_review.py').read_bytes())}
    providers = {p: subprocess.check_output(['git', 'show', f'{REVISION}:{p}'], cwd=ROOT / '_reference/ReC98') for p in PROVIDERS}
    def verify():
        for path, digest in inputs.items():
            if sha((ROOT / path).read_bytes()) != digest:
                raise ValueError('PI decoder input changed: ' + path)
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
            raise ValueError('PI decoder invalid decoded image')
        observed = dict(path=path, analysis=analyze(mz.program_image))
        if index:
            if observed['analysis'] != observations[0]['analysis']:
                raise ValueError('PI decoder complete bodies/CFG/table differ')
            tree = Path(path).parents[2]
            for provider, data in providers.items():
                cached = str(tree / provider)
                actual = (ROOT / cached).read_bytes()
                inputs[cached] = sha(actual)
                if actual.replace(b'\r\n', b'\n') != cached_provider(provider, data):
                    raise ValueError('PI decoder frozen cached provider differs: ' + provider)
            object_path = str(tree / 'obj/th03/mainl.obj')
            data = (ROOT / object_path).read_bytes()
            obj = describe_omf(data)
            inputs[object_path] = sha(data)
            if (not obj['valid'] or obj['module_name'] != 'th03_mainl.asm' or obj['translator_comments'] != ['Turbo Assembler  Version 5.0']
                    or obj['dependency_timestamp_normalized_sha256'] != cold['rounds'][index - 1]['all_objects']['obj/th03/mainl.obj']):
                raise ValueError('PI decoder cold root OMF differs')
            observed['object'] = {k: obj[k] for k in ('valid', 'sha256', 'dependency_timestamp_normalized_sha256', 'module_name', 'translator_comments')}
            objects.append(observed['object'])
            if len(objects) > 1 and objects[-1]['dependency_timestamp_normalized_sha256'] != objects[0]['dependency_timestamp_normalized_sha256']:
                raise ValueError('PI decoder OMF differs beyond timestamps')
            map_path = str(tree / 'obj/th03/mainl.map')
            text = (ROOT / map_path).read_text()
            inputs[map_path] = sha((ROOT / map_path).read_bytes())
            carrier = next(row for row in code_rows(text, len(mz.program_image)) if row['module'] == 'th03_mainl.asm' and row['segment'] == 0 and row['size'])
            if not all(carrier['start'] <= a < a + z <= carrier['start'] + carrier['size'] for _, a, z in EXTENTS):
                raise ValueError('PI decoder includes outside MAP carrier')
            for name, offset in PUBLICS.items():
                coordinates = {(int(s, 16), int(o, 16)) for s, o in re.findall(r'^\s*([0-9A-F]{4}):([0-9A-F]{4})\s+(?:idle\s+)?' + re.escape(name) + r'\s*$', text, re.MULTILINE)}
                if coordinates != {(0, offset)}:
                    raise ValueError('PI decoder public MAP entry differs')
            observed['carrier'], observed['public_entries'] = carrier, PUBLICS
            target = parse_mz((ROOT / proof['observations'][0]['path']).read_bytes())
            observed['comparisons'] = {n: extent_observation(target, mz, dict(start=a, size=z, segment=0, offset=a)) for n, a, z in EXTENTS}
            observed['data_comparisons'] = {n: extent_observation(target, mz, dict(start=0xe3f0 + a, size=z, segment=0xe3f, offset=a)) for n, a, z in [('sharing', 0x558, 2), ('heap-data', TOP, 8)]}
            if any(not row['raw_slice_equal'] or not row['ordered_relocations_equal'] for row in list(observed['comparisons'].values()) + list(observed['data_comparisons'].values())):
                raise ValueError('PI decoder raw/ordered relocations differ')
        observed['cpu'], observed['nonterminal'] = matrix(mz), nonterminal(mz)
        own = {i.address for _,start,size,_ in OWN_RANGES for i in Cs(CS_ARCH_X86,CS_MODE_16).disasm(mz.program_image[start:start+size],start)}
        visited = {a for row in observed['cpu'] + observed['nonterminal'] for a in row['visited']}
        observed['instruction_coverage'] = dict(new_instructions=len(own),visited=len(own & visited),unvisited=sorted(own-visited))
        if index:
            if normalized(observed['cpu']) != normalized(observations[0]['cpu']) or normalized(observed['nonterminal']) != normalized(observations[0]['nonterminal']):
                raise ValueError('PI decoder target/cold CPU differs')
        observations.append(observed)
        print('Reviewed', path, len(observed['cpu']), 'scenarios', len(observed['nonterminal']), 'budgets', flush=True)
    verify()
    if read_verified_artifact(ROOT, artifact) != stored:
        raise ValueError('PI decoder canonical target changed')
    for provider, data in providers.items():
        if subprocess.check_output(['git', 'show', f'{REVISION}:{provider}'], cwd=ROOT / '_reference/ReC98') != data:
            raise ValueError('PI decoder frozen provider changed')
    result = dict(kind='th03-mainl-complete-pi-decoder-candidate-review', observed_utc=datetime.now(timezone.utc).isoformat(),
                  inputs=inputs, providers={p: sha(d) for p, d in providers.items()}, build_scaffold_main_remaps=BUILD_REMAPS,
                  observations=observations, tools=dict(capstone=version('capstone'), unicorn=version('unicorn')),
                  diagnostic_checks_pass=True, new_build=False, source_acceptance=False, exact_acceptance=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print('PASS MAINL PI decoder1600/prior heap-stack-open730; explicit DOS models; exact open:', args.output)


if __name__ == '__main__':
    main()
