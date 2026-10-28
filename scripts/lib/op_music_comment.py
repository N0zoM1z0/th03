"""Complete physical Music Room comment/copy/flip dependencies for the menu.

Actual polygon/random/polar and owned frame-delay bodies execute as context.
Heap, text, file and device replies are explicitly bounded external surfaces.
"""
import hashlib
import json
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import UC_HOOK_INSN
from unicorn import UcError
from unicorn import x86_const as x

from lib.op_music_polygon import Prediction as PolygonPrediction, Machine as PolygonMachine
from lib.op_music_polygon import ContractError, signed, layout as polygon_layout
from lib.op_music_state_layout import CS, DS, START as CARRIER, OBJECT, native_image
from lib.op_startup_state import address, ARITH, REG, GPRS
from lib.op_cfg_runtime import reply
from lib.omf import parse_omf
from probe_th03_main_boss_marisa_cpp import code_bytes

RANGES = ((CARRIER + 216, 30), (CARRIER + 891, 877))
PROCEDURES = (('put', CARRIER + 216, 30, 0), ('flip', CARRIER + 891, 54, 0),
    ('bg_snap', CARRIER + 945, 315, 0), ('load', CARRIER + 1260, 73, 2),
    ('bg_free', CARRIER + 1333, 41, 0), ('unput', CARRIER + 1374, 285, 0),
    ('comment', CARRIER + 1659, 109, 2))
ENTRIES = {n: (start, size, pop) for n, start, size, pop in PROCEDURES}
DELAY = 0xCB86
SERVICES = {0x24CA: ('alloc', 2), 0x25CE: ('free', 2), 0xC6DB: ('text', 10),
    0x9A8: ('open', 4), 0x9E4: ('seek', 6), 0x8F4: ('read', 6), 0x888: ('close', 0),
    0xEC6: ('grcg-color', 4), 0xEF0: ('grcg-off', 0)}
HEAP, BG, CMT, PLANE, PAGE = 0x203A, 0x203C, 0x204C, 0x19FA, 0x2039


def need(value, message):
    if not value:
        raise ContractError('OP Music comments: ' + str(message))


def layout(root, work, target, candidate):
    raw = (work / OBJECT).read_bytes()
    native_image(raw)
    polygon_layout(root, work, target, candidate)  # Whole containing MAP and context geometry.
    code, _ = code_bytes(raw, 1)
    image = bytearray(code)
    names, fields, relocs, block = [], [], [], None
    externals = {1: ('_VRAM_PLANE', DS, PLANE), 2: ('_VRAM_PLANE_B', DS, PLANE), 3: ('HMEM_ALLOCBYTE', 0, 0x24CA),
        4: ('HMEM_FREE', 0, 0x25CE), 8: ('FILE_ROPEN', 0, 0x9A8), 9: ('FILE_READ', 0, 0x8F4),
        10: ('FILE_SEEK', 0, 0x9E4), 11: ('FILE_CLOSE', 0, 0x888),
        12: ('@FRAME_DELAY_2$QI', 0xBEB, 0xCD6), 15: ('@GRAPH_PUTSA_FX$QIIINXUC', 0xBEB, 0x82B),
        22: ('GRCG_SETCOLOR', 0, 0xEC6), 23: ('GRCG_OFF', 0, 0xEF0)}
    def owned(site):
        return any(start - CARRIER <= site < start - CARRIER + size for start, size in RANGES)
    for rec in parse_omf(raw):
        if rec.name == 'EXTDEF':
            at = 0
            while at < len(rec.data):
                length = rec.data[at]
                at += 1
                names.append(rec.data[at:at + length].decode())
                at += length
                need(rec.data[at] == 0, 'untyped external')
                at += 1
        elif rec.name == 'LEDATA':
            block = rec.data[0], int.from_bytes(rec.data[1:3], 'little')
        elif rec.name == 'FIXUPP' and block[0] == 1:
            at = 0
            while at < len(rec.data):
                loc, low, method = rec.data[at:at + 3]
                at += 3
                frame = None
                need(method in (20, 22, 86), 'native field form')
                if method in (20, 22):
                    frame = rec.data[at]
                    at += 1
                index = rec.data[at]
                at += 1
                site = block[1] + (loc & 3) * 256 + low
                width = 4 if loc >> 2 & 15 == 3 else 2
                if not owned(site):
                    continue
                need(owned(site + width - 1), 'whole scoped field')
                addend = int.from_bytes(code[site:site + width], 'little')
                fields.append([site, width, loc, method, frame, index, addend])
                if method == 20:
                    need(frame == 1 and width == 2 and index in (2, 3), 'DGROUP local field')
                    value = {2: 0x5F2, 3: 0x1F70}[index] + addend
                else:
                    name, segment, offset = externals[index]
                    need(names[index - 1] == name, 'exact external identity')
                    if method == 22:
                        need(frame == 1 and width == 2 and index in (1, 2), 'VRAM far-pointer storage field')
                        value = offset + addend
                    else:
                        need(width == 4 and code[site - 1] == 0x9A, 'ordinary far CALL')
                        value = (segment << 16) + offset + addend
                        relocs.append([CS, 0xC1E + site + 2])
                image[site:site + width] = value.to_bytes(width, 'little')
    instructions, digest = [], hashlib.sha256()
    for start, size in RANGES:
        body = bytes(image[start - CARRIER:start - CARRIER + size])
        need(body == target.program_image[start:start + size] == candidate.program_image[start:start + size], 'complete native/target/candidate bytes')
        rows = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(body, start))
        need(sum(i.size for i in rows) == size, 'whole instruction partition')
        instructions.extend(rows)
        digest.update(body)
    for mz in (target, candidate):
        need([[r.segment, r.offset] for r in mz.relocations if owned(r.linear - CARRIER)] == relocs, 'literal ordered MZ relocations')
        need(not any(owned(r.linear - CARRIER) != owned(r.linear + 1 - CARRIER) for r in mz.relocations), 'no straddling relocation')
    need((len(fields), len(relocs), len(instructions)) == (63, 14, 315), 'complete native field/instruction counts')
    return dict(code_bytes=907, procedures=7, native_fields=fields, ordered_relocations=relocs,
        instruction_count=len(instructions), raw_sha256=digest.hexdigest(), ranges=[list(r) for r in RANGES],
        source='src/op/music/animation_and_menu.inl;src/op/music/nopoly_blit.inl', object=OBJECT,
        source_ownership_promoted=False, whole_product_accepted=False)


class Prediction(PolygonPrediction):
    def __init__(self, *args):
        super().__init__(*args)
        self.allocations = self.texts = self.frees = self.seek = 0

    def port(self):
        self.events.append(('out', self.r['dx'], 1, self.r['ax'] & 255, self.full(), self.flags & 0x600))

    def service(self, name, continuation, cleanup):
        self.frame(continuation, 0xBEB if name == 'text' else 0)
        self.calls += 1
        mask = self.mask | 0x600
        at = address(self.ss, self.r['sp'])
        self.events.append(('service', name, self.full(), bytes(self.memory[at:at + 4 + cleanup]).hex(), self.flags & mask, mask, self.calls))
        status = self.o['status']
        if name == 'alloc':
            status = self.o['allocated'][self.allocations]
            self.allocations += 1
        elif name == 'seek':
            self.seek = signed(self.word(self.ss, self.r['sp'] + 6, 4), 32)
        elif name == 'read':
            amount = self.word(self.ss, self.r['sp'] + 4)
            offset = self.word(self.ss, self.r['sp'] + 6)
            segment = self.word(self.ss, self.r['sp'] + 8)
            raw = bytes(((self.seek + i) * 13 + 71) % 255 + 1 for i in range(min(amount, self.o['read_bytes'])))
            dest = address(segment, offset)
            self.events.append(('external-bytes', dest, raw.hex()))
            self.memory[dest:dest + len(raw)] = raw
        elif name == 'text':
            self.texts += 1
            if self.texts == 1 and self.o['text_effects']:
                dest = address(self.dg(PLANE + 2), self.dg(PLANE))
                self.events.append(('external-bytes', dest, 'e7a95c31'))
                self.memory[dest:dest + 4] = bytes.fromhex('e7a95c31')
        elif name == 'free':
            self.frees += 1
            if self.frees == 1 and self.o['free_reload']:
                dest = address(self.ds, BG + 6)
                self.events.append(('external-bytes', dest, 'efbe'))
                self.memory[dest:dest + 2] = bytes.fromhex('efbe')
        self.r, self.flags = reply(self.r, self.calls, self.o['seed'], self.flags, status)
        self.mask = ARITH
        self.returned(cleanup)

    def near(self, name, continuation):
        self.push(continuation)
        getattr(self, name)()

    def put(self):
        self.enter()
        for name in ('si', 'di', 'ds'):
            self.push(self.r[name])
        self.r['ax'] = self.r['es'] = 0xA800
        self.r['ax'] = self.dg(HEAP)
        self.r['ds'] = self.r['ax']
        self.r['di'] = self.r['si'] = 0
        self.logic(0)
        self.r['cx'] = 16000
        step = -2 if self.flags & 0x400 else 2
        for _ in range(16000):
            self.store(address(self.r['es'], self.r['di']), 2, self.word(self.r['ds'], self.r['si']))
            self.r['si'] = (self.r['si'] + step) & 65535
            self.r['di'] = (self.r['di'] + step) & 65535
        self.r['cx'] = 0
        for name in ('ds', 'di', 'si', 'bp'):
            self.pop(name)
        self.r['sp'] += 2

    def delay(self):
        self.frame(0xFCD, 0xBEB)
        self.enter()
        self.field(0x11E8, 0)
        for value in self.o['ticks']:
            self.events.append(('tick', value))
            dest = address(self.ds, 0x11E8)
            self.memory[dest:dest + 2] = value.to_bytes(2, 'little')
            self.r['ax'] = value
            self.op(value, self.word(self.ss, self.r['bp'] + 6), True)
            if value >= self.word(self.ss, self.r['bp'] + 6):
                break
        else:
            raise ValueError('finite delay fixture never reaches requested count')
        self.pop('bp')
        self.returned(2)

    def flip(self):
        self.enter()
        self.near('put', 0xF9F)
        self.push(0xCE000F, 4)
        self.service('grcg-color', 0xFAA, 4)
        self.push(0xFAD)
        self.update()
        self.service('grcg-off', 0xFB2, 0)
        self.r['dx'] = 0xA4
        self.al(self.dg(PAGE, 1))
        self.port()
        self.al(self.op(1, self.dg(PAGE, 1), True, bits=8))
        self.field(PAGE, self.r['ax'], 1)
        self.r['dx'] = 0xA6
        self.port()
        self.push(1)
        self.delay()
        self.pop('bp')
        self.r['sp'] += 2

    def pointer(self, offset):
        value = self.dg(offset, 4)
        self.r['bx'], self.r['es'] = value & 65535, value >> 16

    def blit(self, restore):
        """Two distinct native loops retain a continuous 12800-byte cursor."""
        cursor, row, column = ('cx', 'si', 'di') if restore else ('si', 'di', None)
        self.r[cursor] = 0
        self.logic(0)
        for first, bottom in ((64, 80), (80, 384)):
            self.r[row] = first
            while True:
                self.op(self.r[row], bottom, True)
                if self.r[row] >= bottom:
                    break
                if restore:
                    self.r[column] = 304
                else:
                    self.store(address(self.ss, self.r['bp'] - 2), 2, 304)
                while True:
                    col = self.r[column] if restore else self.word(self.ss, self.r['bp'] - 2)
                    self.op(col, 624, True)
                    if col >= 624:
                        break
                    self.r['ax'] = self.shift(col, 3, right=True)
                    self.r['dx'] = self.shift(self.r[row], 6)
                    self.r['ax'] = self.op(self.r['ax'], self.r['dx'])
                    self.r['dx'] = self.shift(self.r[row], 4)
                    self.r['ax'] = self.op(self.r['ax'], self.r['dx'])
                    local = self.r['bp'] - (2 if restore else 4)
                    self.store(address(self.ss, local), 2, self.r['ax'])
                    for plane in range(4):
                        source, dest = (BG, PLANE) if restore else (PLANE, BG)
                        self.pointer(source + 4 * plane)
                        self.r['bx'] = self.op(self.r['bx'], self.r[cursor] if restore else self.word(self.ss, local))
                        self.set32('ax', self.word(self.r['es'], self.r['bx'], 4))
                        self.pointer(dest + 4 * plane)
                        if restore:
                            self.r['bx'] = self.op(self.r['bx'], self.word(self.ss, local))
                            offset = self.r['bx']
                        else:
                            offset = self.r['bx'] + self.r[cursor]
                        self.store(address(self.r['es'], offset), 4, self.full()['ax'])
                    self.r[cursor] = self.op(self.r[cursor], 4)
                    if restore:
                        self.r[column] = self.op(self.r[column], 32)
                    else:
                        self.store(address(self.ss, self.r['bp'] - 2), 2, self.op(col, 32))
                self.r[row] = self.increment(self.r[row])
        if self.r[cursor] != 12800 or self.r[row] != 384:
            raise AssertionError('independent 320 rows / 10 DWORDs / 12800-byte plane geometry')

    def bg_snap(self):
        self.enter(6)
        self.push(self.r['si'])
        self.push(self.r['di'])
        at = address(self.ss, self.r['bp'] - 6)
        self.store(at, 2, 0)
        for i in range(4):
            self.op(i, 4, True)
            self.push(12800)
            self.service('alloc', 0xFE4, 2)
            self.r['bx'] = self.shift(self.word(self.ss, self.r['bp'] - 6), 2)
            self.field(BG + self.r['bx'] + 2, self.r['ax'])
            self.field(BG + self.r['bx'], 0)
            self.store(at, 2, self.increment(self.word(self.ss, self.r['bp'] - 6)))
        self.op(4, 4, True)
        self.blit(False)
        self.pop('di')
        self.pop('si')
        self.r['sp'] = self.r['bp']
        self.pop('bp')
        self.r['sp'] += 2

    def load(self):
        self.enter()
        self.push(self.r['si'])
        self.push(self.ds)
        self.push(0x9D1)
        self.service('open', 0x1117, 4)
        product = signed(self.word(self.ss, self.r['bp'] + 4)) * 840
        self.set32('ax', signed(product))  # IMUL truncates WORD; CWDE sign-extends it.
        overflow = product != signed(product)
        self.flags = (self.flags & 0x600) | 2 | (0x801 if overflow else 0)
        self.mask = 0x801
        self.push(self.full()['ax'], 4)
        self.push(0)
        self.service('seek', 0x1129, 6)
        self.push(self.ds)
        self.push(CMT)
        self.push(840)
        self.service('read', 0x1135, 6)
        self.service('close', 0x113A, 0)
        self.r['si'] = 0
        self.logic(0)
        for i in range(20):
            self.op(self.r['si'], 20, True)
            self.r['bx'] = self.r['si'] * 42
            self.flags = (self.flags & 0x600) | 2
            self.mask = 0x801
            self.field(CMT + self.r['bx'] + 40, 0, 1)
            self.r['si'] = self.increment(self.r['si'])
        self.op(self.r['si'], 20, True)
        self.pop('si')
        self.pop('bp')
        self.r['sp'] += 4

    def bg_free(self):
        self.enter()
        for i, ret in enumerate((0x115F, 0x1168, 0x1171, 0x117A)):
            self.push(self.dg(BG + 4 * i + 2))
            self.service('free', ret, 2)
        self.pop('bp')
        self.r['sp'] += 2

    def unput(self):
        self.enter(2)
        self.push(self.r['si'])
        self.push(self.r['di'])
        self.blit(True)
        self.pop('di')
        self.pop('si')
        self.r['sp'] = self.r['bp']
        self.pop('bp')
        self.r['sp'] += 2

    def comment(self):
        self.enter()
        self.push(self.r['si'])
        self.push(self.r['di'])
        self.push(self.word(self.ss, self.r['bp'] + 4))
        self.near('load', 0x12A4)
        self.near('put', 0x12A7)
        self.near('unput', 0x12AA)
        self.push(0x1300040, 4)
        self.push(31)
        self.push(self.ds)
        self.push(CMT)
        self.service('text', 0x12BB, 10)
        self.r['di'] = 1
        while True:
            self.op(self.r['di'], 20, True)
            if self.r['di'] == 20:
                break
            self.push(304)
            self.r['ax'] = (self.r['di'] + 4) & 65535
            self.r['ax'] = self.shift(self.r['ax'], 4)
            self.push(self.r['ax'])
            self.push(29)
            self.push(self.ds)
            self.r['ax'] = self.r['di'] * 42
            self.flags = (self.flags & 0x600) | 2
            self.mask = 0x801
            self.r['ax'] = self.op(self.r['ax'], CMT)
            self.push(self.r['ax'])
            self.service('text', 0x12DB, 10)
            self.r['di'] = self.increment(self.r['di'])
        self.r['si'] = 0
        self.logic(0)
        while True:
            self.op(self.r['si'], 32000, True)
            if self.r['si'] == 32000:
                break
            self.pointer(PLANE)
            self.r['bx'] = self.op(self.r['bx'], self.r['si'])
            self.set32('ax', self.word(self.r['es'], self.r['bx'], 4))
            self.r['es'] = self.dg(HEAP)
            self.store(address(self.r['es'], self.r['si']), 4, self.full()['ax'])
            self.r['si'] = self.op(self.r['si'], 4)
        self.pop('di')
        self.pop('si')
        self.pop('bp')
        self.r['sp'] += 4


class Machine(PolygonMachine):
    def __init__(self, image, load):
        super().__init__(image, load)
        memory = bytearray((i * 73 + (i >> 8) * 19 + (i >> 16) * 67) & 255 for i in range(1 << 20))
        raw = image.relocated_program_image(load)
        memory[self.base:self.base + len(raw)] = raw
        self.initial = bytes(memory)
        for start, size in (*RANGES, (DELAY, 21)):
            rows = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(image.program_image[start:start + size], start))
            need(sum(i.size for i in rows) == size, 'whole helper/delay instructions')
            self.instructions.update({i.address: i.size for i in rows})
        self.helper_covered = set()
        self.hooks.append(self.uc.hook_add(UC_HOOK_INSN, self.out, None, 1, 0, x.UC_X86_INS_OUT))

    def code(self, uc, at, size, user):
        try:
            rva = at - self.base
            self.maximum_stack = max(self.maximum_stack, self.stack - self.r('sp'))
            need(self.maximum_stack <= 128, 'bounded complete checked stack')
            if rva in SERVICES:
                physical = address(self.r('ss'), self.r('sp'))
                ip, cs = struct.unpack('<HH', uc.mem_read(physical, 4))
                self.event(('far-frame', physical, ip, cs))
                name, cleanup = SERVICES[rva]
                mask, count = self.expected.events[self.index][-2:]
                self.event(('service', name, self.full(), bytes(uc.mem_read(physical, 4 + cleanup)).hex(),
                            uc.reg_read(x.UC_X86_REG_EFLAGS) & mask, mask, count))
                while self.index < len(self.expected.events) and self.expected.events[self.index][0] == 'external-bytes':
                    _, dest, raw = self.expected.events[self.index]
                    self.event(('external-bytes', dest, raw))
                    uc.mem_write(dest, bytes.fromhex(raw))
                status = self.o['status']
                if name == 'alloc':
                    status = self.o['allocated'][self.allocations]
                    self.allocations += 1
                values, flags = reply({n: self.r(n) for n in (*GPRS, 'cs', 'ds', 'es', 'ss', 'fs', 'gs')},
                                      count, self.o['seed'], uc.reg_read(x.UC_X86_REG_EFLAGS), status)
                for name in ('ax', 'bx', 'cx', 'dx', 'es'):
                    uc.reg_write(REG[name], values[name])
                uc.reg_write(x.UC_X86_REG_EFLAGS, flags)
                uc.reg_write(REG['sp'], self.r('sp') + 4 + cleanup)
                uc.reg_write(REG['cs'], cs)
                uc.reg_write(REG['ip'], ip)
                return
            if rva == DELAY:
                physical = address(self.r('ss'), self.r('sp'))
                ip, cs = struct.unpack('<HH', uc.mem_read(physical, 4))
                self.event(('far-frame', physical, ip, cs))
            if rva == DELAY + 9:
                need(self.ticks < len(self.o['ticks']), 'guest requested an unavailable finite counter reply')
                value = self.o['ticks'][self.ticks]
                self.ticks += 1
                self.event(('tick', value))
                uc.mem_write(address(self.ds, 0x11E8), value.to_bytes(2, 'little'))
            if any(start <= rva < start + length for start, length in RANGES):
                self.helper_covered.update(range(rva, rva + size))
        except Exception as error:
            self.fail(error)
            return
        super().code(uc, at, size, user)

    def out(self, uc, port, size, value, user):
        try:
            self.event(('out', port, size, value, self.full(), uc.reg_read(x.UC_X86_REG_EFLAGS) & 0x600))
        except Exception as error:
            self.fail(error)

    def run(self, kind, *, track=0, read_bytes=840, seed=0x1357, flags=0x202, stack=0xF800,
            allocated=(0x5000, 0x5400, 0x5800, 0x5C00), heap=0x9000, source_offset=0,
            bg_offset=0, initialized=1, page=1, status=0xFFFF, ticks=(0, 1),
            text_effects=True, free_reload=False, reenter=False):
        self.guest_started = False
        need(kind in ENTRIES and 0 <= track <= 65535 and 0 <= read_bytes <= 840, 'bounded entry/file domain')
        need(len(allocated) == 4 and all(s in (0, 0x5000, 0x5400, 0x5800, 0x5C00, 0x9000, 0xA800, 0xA801) for s in allocated), 'mapped allocator fixture')
        need(heap in (0, 0x5000, 0x9000, 0xA800, 0xA801) and 0 <= source_offset <= 65535 and 0 <= bg_offset <= 65535, 'mapped live pointer fixture')
        need(0x100 <= stack <= 0xFFF0 and 0 <= page < 256, 'mapped WORD caller stack/BYTE page')
        need(ticks and all(0 <= value <= 65535 for value in ticks), 'finite WORD counter fixture')
        memory = bytearray(self.expected.memory if reenter else self.initial)
        def put(offset, value, width=2):
            dest = address(self.ds, offset)
            memory[dest:dest + width] = (value & ((1 << (width * 8)) - 1)).to_bytes(width, 'little')
        if not reenter:
            put(0x312, seed, 4)
            put(HEAP, heap)
            put(PAGE, page, 1)
            put(0x692, initialized, 1)
            for i, seg in enumerate((0xA800, 0xB000, 0xB800, 0xE000)):
                put(PLANE + 4 * i, (seg << 16) | source_offset, 4)
                put(BG + 4 * i, (allocated[i] << 16) | bg_offset, 4)
            for i in range(16):
                put(0x1F98 + 4 * i, (i * 41) % 640)
                put(0x1F9A + 4 * i, 7999 if i % 3 == 0 else 3200)
                put(0x1FD8 + 4 * i, (1, -1, 0, 8)[i % 4])
                put(0x1FDA + 4 * i, 32)
                put(0x2018 + i, i * 17, 1)
                put(0x2028 + i, i - 4, 1)
            for i in range(20):
                put(CMT + 42 * i, ord(';'), 1)
        memory[address(0x7000, stack - 128):address(0x7000, stack)] = b'\xD3' * 128
        frame = struct.pack('<2H', 0xFFFF, track) if ENTRIES[kind][2] else b'\xFF\xFF'
        dest = address(0x7000, stack)
        memory[dest:dest + len(frame)] = frame
        self.uc.mem_write(0, bytes(memory))
        registers = {n: (seed + i * 0x231) & 65535 for i, n in enumerate(GPRS)}
        registers.update(sp=stack, cs=self.cs, ds=self.ds, es=seed & 65535, ss=0x7000,
                         fs=(seed ^ 0xA55A) & 65535, gs=(seed ^ 0x5AA5) & 65535)
        high = {n: ((seed ^ 0x5AA5) & 65535) << 16 for n in GPRS}
        for name, register in GPRS.items():
            self.uc.reg_write(register, high[name] | registers[name])
        for name in ('cs', 'ds', 'es', 'ss', 'fs', 'gs'):
            self.uc.reg_write(REG[name], registers[name])
        self.uc.reg_write(x.UC_X86_REG_EFLAGS, flags)
        self.o = dict(load=self.load, seed=seed & 65535, status=status, allocated=tuple(allocated),
                      read_bytes=read_bytes, text_effects=text_effects, free_reload=free_reload, ticks=tuple(ticks))
        self.expected = Prediction(memory, registers, high, flags, self.o)
        getattr(self.expected, kind)()
        self.index, self.error, self.returned = 0, None, False
        self.stack, self.maximum_stack, self.allocations, self.ticks = stack, 0, 0, 0
        self.guest_started = True
        try:
            self.uc.emu_start(self.base + ENTRIES[kind][0], 1 << 20, count=1500000)
        except UcError as error:
            raise ContractError('Music comment guest fault') from error
        if self.error is not None:
            raise self.error
        need(self.returned and self.index == len(self.expected.events), 'complete actual return/event plan')
        need(self.full() == self.expected.full(), 'all DWORD registers and six segments ' + str((self.full(), self.expected.full())))
        mask = self.expected.mask | 0x600
        need(self.uc.reg_read(x.UC_X86_REG_EFLAGS) & mask == self.expected.flags & mask, 'all defined flags/IF/DF')
        need(bytes(self.uc.mem_read(0, 1 << 20)) == self.expected.memory, 'all physical memory including every stack byte')
        return dict(kind=kind, registers=self.expected.full(), flags=self.expected.flags & mask, flags_mask=mask,
                    events=self.index, text_calls=self.expected.texts, allocator_calls=self.expected.allocations,
                    free_calls=self.expected.frees, signed_seek_offset=self.expected.seek,
                    maximum_stack_depth=self.maximum_stack,
                    trace_sha256=hashlib.sha256(json.dumps(self.expected.events, sort_keys=True).encode()).hexdigest())


def cases():
    for kind in ENTRIES:
        for flags in (2, 0x202, 0x402, 0xED7):
            for stack in (0x100, 0xFFF0):
                yield kind, dict(flags=flags, stack=stack, seed=0xFFFF, source_offset=65535,
                                 bg_offset=65535, track=0xFFFF, read_bytes=0, free_reload=True)
    for track in range(256):
        yield 'load', dict(track=track)
    for track in (0x100, 0x7FFF, 0x8000, 0xFF00, 0xFFFF):
        for amount in (0, 1, 39, 40, 41, 839, 840):
            yield 'load', dict(track=track, read_bytes=amount)
    for kind in ('bg_snap', 'unput', 'comment'):
        for allocated in ((0, 0, 0, 0), (0xA800,) * 4, (0xA801, 0xA800, 0, 0x9000)):
            for offset in (0, 1, 65535):
                yield kind, dict(allocated=allocated, source_offset=offset, bg_offset=offset,
                                 flags=0xED7, heap=0xA801, track=40, read_bytes=41)
    for heap in (0, 0x5000, 0x9000, 0xA800, 0xA801):
        for flags in (0x202, 0xED7):
            yield 'put', dict(heap=heap, flags=flags)
    for page in (0, 1, 2, 127, 128, 255):
        for initialized in (0, 1, 255):
            yield 'flip', dict(page=page, initialized=initialized, ticks=(0, 0, 65535), seed=1)
    for amount in (0, 1, 39, 40, 41, 839, 840):
        for effects in (False, True):
            yield 'comment', dict(read_bytes=amount, text_effects=effects, track=39)


def verify(target, candidate):
    observations = []
    for image in (target, candidate):
        loads = []
        for load in (0x1000, 0x3000):
            machine = Machine(image, load)
            counts = {kind: 0 for kind in ENTRIES}
            trace, depth = hashlib.sha256(), 0
            def record(kind, options):
                nonlocal depth
                try:
                    row = machine.run(kind, **options)
                except ContractError as error:
                    raise ContractError(str((kind, options, error))) from error
                trace.update(json.dumps(row, sort_keys=True).encode())
                depth = max(depth, row['maximum_stack_depth'])
                counts[kind] += 1
            try:
                for kind, options in cases():
                    record(kind, options)
                # Retain all heap pointers, loaded comments, animation state and
                # VRAM across the real dependency chain on the same physical UC.
                for kind, options in (('bg_snap', {}), ('comment', dict(reenter=True, track=0xFFFF, read_bytes=39)),
                                      ('flip', dict(reenter=True)), ('comment', dict(reenter=True, read_bytes=0)),
                                      ('bg_free', dict(reenter=True, free_reload=True))):
                    record(kind, options)
                owned = {at for start, size in RANGES for at in range(start, start + size)}
                need(machine.helper_covered == owned, 'all 907 helper bytes execute')
                need(set(range(DELAY, DELAY + 21)) <= machine.context, 'actual owned delay body executes completely')
                loads.append(dict(load_segment=load, cases=sum(counts.values()), complete_returns=counts,
                    helper_bytes=len(machine.helper_covered), polygon_context_bytes=len(machine.covered),
                    other_context_bytes=len(machine.context - owned), maximum_stack_depth=depth,
                    consecutive_dependency_calls=5, trace_sha256=trace.hexdigest()))
            finally:
                machine.close()
        observations.append(loads)
    need(observations[0] == observations[1], 'independent target/candidate complete observations')
    return dict(images=2, procedures=7, code_bytes=907, observations=observations[0], ignored_stack_bytes=0,
        actual_nested_helpers_and_delay=True, synthetic_owned_returns=False,
        explicit_copy_DWORDs_per_plane=3200, explicit_recapture_DWORDs=8000, REP_copy_WORDs=16000,
        unchecked_allocation_failure=True, live_aliasing=True, WORD_pointer_wrap=True,
        physical_pixels_files_heap_or_frame_time_proved=False, source_ownership_promoted=False, whole_product_accepted=False)


def negative_controls(target):
    from dataclasses import replace
    controls = (
        ('put-saved-DS', 0xA5FB, 1, 'put', {}),
        ('put-plane-B-segment', 0xA5FE, 1, 'put', {}),
        ('put-saved-heap', 0xA602, 1, 'put', {}),
        ('put-all16000-WORDs', 0xA60B, 1, 'put', {}),
        ('put-WORD-width', 0xA60E, 1, 'put', {}),
        ('put-restore-DS', 0xA60F, 0x8F, 'put', {}),
        ('flip-actual-put', 0xA89D, 1, 'flip', {}),
        ('flip-B-plane-GRCG-mask', 0xA8A3, 1, 'flip', {}),
        ('flip-actual-polygons', 0xA8AB, 1, 'flip', {}),
        ('flip-GRCG-off-entry', 0xA8AE, 1, 'flip', {}),
        ('flip-show-port-A4', 0xA8B3, 1, 'flip', {}),
        ('flip-live-page', 0xA8B6, 1, 'flip', dict(page=255)),
        ('flip-page-BYTE-subtraction', 0xA8BA, 1, 'flip', dict(page=255)),
        ('flip-access-port-A6', 0xA8C3, 1, 'flip', {}),
        ('flip-frame-argument-one', 0xA8C7, 1, 'flip', {}),
        ('flip-actual-delay-entry', 0xA8C9, 1, 'flip', {}),
        ('snap-allocation12800', 0xA8DD, 1, 'bg_snap', {}),
        ('snap-segment-field', 0xA8EC, 1, 'bg_snap', {}),
        ('snap-reset-offset-zero', 0xA8F2, 1, 'bg_snap', dict(bg_offset=65535)),
        ('snap-all-four-planes', 0xA8FA, 1, 'bg_snap', {}),
        ('snap-title-row64', 0xA900, 1, 'bg_snap', {}),
        ('snap-title-left304', 0xA907, 8, 'bg_snap', {}),
        ('snap-column-byte-shift3', 0xA910, 1, 'bg_snap', {}),
        ('snap-B-source-plane', 0xA924, 1, 'bg_snap', {}),
        ('snap-R-source-plane', 0xA937, 1, 'bg_snap', {}),
        ('snap-G-source-plane', 0xA94A, 1, 'bg_snap', {}),
        ('snap-E-source-plane', 0xA95D, 1, 'bg_snap', {}),
        ('snap-continuous-cursor-step4', 0xA970, 1, 'bg_snap', {}),
        ('snap-column-step32', 0xA974, 1, 'bg_snap', {}),
        ('snap-title-bottom80', 0xA97F, 1, 'bg_snap', {}),
        ('snap-comment-bottom384', 0xAA02, 1, 'bg_snap', {}),
        ('load-MUSIC-TXT-pointer', 0xAA10, 1, 'load', {}),
        ('load-truncated-WORD-times840', 0xAA1C, 1, 'load', dict(track=40)),
        ('load-sign-extend-CWDE', 0xAA1F, 8, 'load', dict(track=40)),
        ('load-SEEK-SET', 0xAA23, 1, 'load', dict(track=40)),
        ('load-request840', 0xAA2E, 1, 'load', {}),
        ('load-null-at-column40', 0xAA45, 1, 'load', {}),
        ('load-all20-rows', 0xAA4B, 1, 'load', {}),
        ('load-Pascal-pop2', 0xAA51, 2, 'load', {}),
        ('free-first-segment', 0xAA58, 1, 'bg_free', {}),
        ('free-reload-second-segment', 0xAA61, 1, 'bg_free', dict(free_reload=True)),
        ('free-fourth-segment', 0xAA73, 1, 'bg_free', {}),
        ('unput-title-row64', 0xAA85, 1, 'unput', {}),
        ('unput-title-left304', 0xAA8A, 8, 'unput', {}),
        ('unput-B-buffer', 0xAAA6, 1, 'unput', {}),
        ('unput-R-buffer', 0xAABB, 1, 'unput', {}),
        ('unput-G-buffer', 0xAAD0, 1, 'unput', {}),
        ('unput-E-buffer', 0xAAE5, 1, 'unput', {}),
        ('unput-continuous-cursor-step4', 0xAAFA, 1, 'unput', {}),
        ('unput-comment-bottom384', 0xAB8F, 1, 'unput', {}),
        ('comment-actual-load', 0xABA2, 1, 'comment', {}),
        ('comment-actual-put', 0xABA5, 1, 'comment', {}),
        ('comment-actual-unput', 0xABA8, 1, 'comment', {}),
        ('comment-title-color31', 0xABB1, 1, 'comment', {}),
        ('comment-row-origin4', 0xABC5, 1, 'comment', {}),
        ('comment-body-color29', 0xABCB, 1, 'comment', {}),
        ('comment-line-stride42', 0xABD1, 1, 'comment', {}),
        ('comment-all20-lines', 0xABDE, 1, 'comment', dict(read_bytes=0)),
        ('comment-recapture-source', 0xABE7, 1, 'comment', {}),
        ('comment-recapture-heap', 0xABF1, 1, 'comment', {}),
        ('comment-recapture-DWORD-width', 0xABF5, 1, 'comment', {}),
        ('comment-recapture-all32000', 0xABFC, 1, 'comment', {}),
        ('comment-Pascal-pop2', 0xAC04, 2, 'comment', {}),
        ('delay-counter-storage', 0xCB8B, 1, 'flip', {}),
        ('delay-unsigned-comparison', 0xCB95, 14, 'flip', dict(ticks=(0, 0x8000, 65535))),
    )
    rejected = []
    for name, site, mask, kind, options in controls:
        raw = bytearray(target.program_image)
        raw[site] ^= mask
        machine = Machine(replace(target, program_image=bytes(raw)), 0x3000)
        try:
            try:
                machine.run(kind, **options)
            except ContractError:
                if not machine.guest_started:
                    raise
                rejected.append(name)
            else:
                raise ValueError('Music comment mutation survived: ' + name)
        finally:
            machine.close()
    return dict(actual_instruction_mutations=len(controls), rejected=rejected,
                prediction_constructor_and_unexpected_hook_exceptions_are_fatal=True)
