"""Independent scalar contract for the complete Music Room polygon pair.

IRAND and polar execute as unowned instruction context. Only the polygon
renderer is a bounded reply. No product ownership is promoted by this module.
"""
import hashlib
import json
import struct

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn import x86_const as x

from lib.op_startup_state import State, REG, GPRS, address, logical, ARITH
from lib.op_cfg_runtime import reply
from lib.op_music_state_layout import CS, DS, START as CARRIER, OBJECT, native_image, verify as carrier_layout
from probe_th03_main_boss_marisa_cpp import code_bytes
from lib.omf import parse_omf
from lib.op_music_state_runtime import Machine as FrameMachine

START, SIZE = CARRIER + 246, 645
BUILD, UPDATE, RANDOM, POLAR, RENDER = START, START + 143, 0x1D12, 0xC005, 0xC6A
CENTER, VELOCITY, ANGLE, SPEED, POINTS, INITIALIZED = 0x1F98, 0x1FD8, 0x2018, 0x2028, 0x1F70, 0x692


class ContractError(ValueError):
    """A guest contract mismatch, distinct from verifier implementation errors."""


def need(value, message):
    if not value:
        raise ContractError('OP Music polygon: ' + str(message))


def signed(value, bits=16):
    value &= (1 << bits) - 1
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def layout(root, work, target, candidate):
    """Resolve native fields, never patching an object or executable."""
    raw = (work / OBJECT).read_bytes()
    carrier_layout(root, work, target, candidate)  # Entire producer MAP/public geometry.
    native_image(raw)  # Complete natural carrier records, segments and publics.
    code, _ = code_bytes(raw, 1)
    image = bytearray(code[246:891])
    names, fields, relocations, block = [], [], [], None
    externals = {5: ('_SinTable8', DS, 0x316), 6: ('_CosTable8', DS, 0x396),
                 7: ('IRAND', 0, RANDOM), 19: ('@polar$qiii', 0xBEB, 0x155),
                 24: ('GRCG_POLYGON_C', 0, RENDER)}
    for record in parse_omf(raw):
        if record.name == 'EXTDEF':
            at = 0
            while at < len(record.data):
                length = record.data[at]
                at += 1
                names.append(record.data[at:at + length].decode())
                at += length
                need(record.data[at] == 0, 'untyped external')
                at += 1
        elif record.name == 'LEDATA':
            block = record.data[0], int.from_bytes(record.data[1:3], 'little')
        elif record.name == 'FIXUPP' and block[0] == 1:
            at = 0
            while at < len(record.data):
                loc, low, method = record.data[at:at + 3]
                at += 3
                frame = None
                need(method in (20, 22, 86), 'native field form')
                if method in (20, 22):
                    frame = record.data[at]
                    at += 1
                index = record.data[at]
                at += 1
                site = block[1] + (loc & 3) * 256 + low
                width = 4 if (loc >> 2 & 15) == 3 else 2
                if not 246 <= site < 891:
                    continue
                need(site + width <= 891, 'complete scoped field')
                addend = int.from_bytes(code[site:site + width], 'little')
                fields.append([site, width, loc, method, frame, index, addend])
                if method == 20:
                    need(frame == 1 and width == 2 and index in (2, 3), 'DGROUP field')
                    value = {2: 0x5F2, 3: 0x1F70}[index] + addend
                else:
                    name, segment, offset = externals[index]
                    need(names[index - 1] == name, 'external identity')
                    if method == 22:
                        need(frame == 1 and width == 2 and index in (5, 6), 'trigonometry DATA field')
                        value = offset + addend
                    else:
                        need(width == 4 and code[site - 1] == 0x9A and index in (7, 19, 24), 'ordinary far CALL')
                        value = (segment << 16) + offset + addend
                        relocations.append([CS, 0xC1E + site + 2])
                image[site - 246:site - 246 + width] = value.to_bytes(width, 'little')
    need(len(fields) == 54 and len(relocations) == 14, 'complete native field/relocation counts')
    need(bytes(image) == target.program_image[START:START + SIZE] == candidate.program_image[START:START + SIZE],
         'complete independently resolved native/target/candidate bytes')
    for mz in (target, candidate):
        need([[r.segment, r.offset] for r in mz.relocations if START <= r.linear < START + SIZE] == relocations,
             'literal ordered MZ relocation vector')
        need(not any(r.linear < START < r.linear + 2 or r.linear < START + SIZE < r.linear + 2 for r in mz.relocations),
             'no straddling relocation')
    instructions = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(image, START))
    need(sum(i.size for i in instructions) == SIZE, 'whole instruction partition')
    return dict(code_bytes=SIZE, procedures=2, native_fields=fields, ordered_relocations=relocations,
                instruction_count=len(instructions), raw_sha256=hashlib.sha256(image).hexdigest(),
                source='src/op/music/animation_and_menu.inl', object=OBJECT,
                source_ownership_promoted=False, whole_product_accepted=False)


class Prediction(State):
    def set32(self, name, value):
        value &= 0xFFFFFFFF
        self.r[name], self.high[name] = value & 65535, value & 0xFFFF0000

    def shift(self, value, count, right=False, bits=16):
        result = (signed(value, bits) >> count if right else value << count) & ((1 << bits) - 1)
        carry = (value >> (count - 1 if right else bits - count)) & 1
        self.flags = (self.flags & 0x600) | 2 | logical(result, bits) | carry
        self.mask = 0xC5  # OF/AF undefined for these multi-bit shifts.
        return result

    def multiply(self, value, signed_operands=False):
        product = (signed(self.r['ax']) * signed(value) if signed_operands else self.r['ax'] * value)
        self.r['ax'], self.r['dx'] = product & 65535, (product >> 16) & 65535
        overflow = product != signed(self.r['ax']) if signed_operands else bool(product >> 16)
        self.flags = (self.flags & 0x600) | 2 | (0x801 if overflow else 0)
        self.mask = 0x801

    def divide(self, divisor):
        # Every scoped IDIV follows CWD. Quotient truncates towards zero.
        numerator, divisor = signed(self.r['ax']), signed(divisor)
        quotient = (abs(numerator) // abs(divisor)) * (-1 if (numerator < 0) != (divisor < 0) else 1)
        self.r['ax'], self.r['dx'] = quotient & 65535, (numerator - quotient * divisor) & 65535
        self.mask = 0

    def increment(self, value):
        carry, defined = self.flags & 1, self.mask & 1
        result = self.op(value, 1)
        self.flags = (self.flags & ~1) | carry
        self.mask = (self.mask & ~1) | defined
        return result

    def rand(self, continuation):
        seed = self.dg(0x312, 4)
        self.frame(continuation, 0)
        self.r['ax'] = 0x4E35
        self.multiply(self.dg(0x314))
        self.r['cx'] = self.r['ax']
        self.r['ax'] = 0x15A
        self.multiply(self.dg(0x312))
        self.r['cx'] = self.op(self.r['cx'], self.r['ax'])
        self.r['ax'] = 0x4E35
        self.multiply(self.dg(0x312))
        self.r['ax'] = self.op(self.r['ax'], 1)
        carry = self.flags & 1
        # ADC has a separate carry input; preserve its full arithmetic result.
        left, right = self.r['dx'], self.r['cx']
        result = (left + right + carry) & 65535
        overflow = (~(left ^ right) & (left ^ result) & 0x8000) != 0
        self.flags = (self.flags & 0x600) | 2 | logical(result) | int(left + right + carry > 65535) | (16 if (left ^ right ^ result) & 16 else 0) | (0x800 if overflow else 0)
        self.mask = ARITH
        self.r['dx'] = result
        self.field(0x312, self.r['ax'])
        self.r['ax'] = self.r['dx']
        self.field(0x314, self.r['ax'])
        need(self.dg(0x312, 4) == (seed * 22695477 + 1) & 0xFFFFFFFF, 'independent DWORD LCG specification')
        self.r['ax'] &= 0x7FFF
        self.logic(self.r['ax'] >> 8, bits=8)
        self.returned()

    def polar(self, continuation):
        self.frame(continuation, 0xBEB)
        self.enter()
        radius = signed(self.word(self.ss, self.r['bp'] + 8))
        ratio = signed(self.word(self.ss, self.r['bp'] + 10))
        self.set32('dx', ratio)
        self.set32('ax', radius * ratio)
        self.set32('ax', self.shift(self.full()['ax'], 8, right=True, bits=32))
        self.r['ax'] = self.op(self.r['ax'], self.word(self.ss, self.r['bp'] + 6))
        self.pop('bp')
        self.returned()

    def build(self):
        self.enter(4)
        self.push(self.r['si'])
        self.push(self.r['di'])
        self.r['di'] = self.word(self.ss, self.r['bp'] + 14)
        at = address(self.ss, self.r['bp'] + 10)
        self.store(at, 2, self.shift(self.word(self.ss, self.r['bp'] + 10), 4, right=True))
        local = self.r['bp'] - 2
        self.store(address(self.ss, local), 2, 0)
        while True:
            self.r['ax'] = self.word(self.ss, local)
            count = self.word(self.ss, self.r['bp'] + 6)
            self.op(self.r['ax'], count, True)
            if signed(self.r['ax']) >= signed(count):
                break
            self.r['ax'] = self.shift(self.r['ax'], 8)
            self.divide(count)
            self.al(self.op(self.r['ax'] & 255, self.word(self.ss, self.r['bp'] + 4, 1), bits=8))
            self.store(address(self.ss, self.r['bp'] - 3), 1, self.r['ax'] & 255)
            for table, origin, continuation in ((0x396, 12, 0xD4D), (0x316, 10, 0xD70)):
                if table == 0x316:
                    self.al(self.word(self.ss, self.r['bp'] - 3, 1))
                self.r['ax'] &= 255
                self.r['ax'] = self.op(self.r['ax'], self.r['ax'])
                self.r['bx'] = self.r['ax']
                self.push(self.dg(table + self.r['bx']))
                self.push(self.word(self.ss, self.r['bp'] + 8))
                self.push(self.word(self.ss, self.r['bp'] + origin))
                self.polar(continuation)
                self.r['sp'] = self.op(self.r['sp'], 6)
                self.r['bx'] = self.shift(self.word(self.ss, local), 2)
                self.field(self.r['di'] + self.r['bx'] + (2 if table == 0x316 else 0), self.r['ax'])
            self.store(address(self.ss, local), 2, self.increment(self.word(self.ss, local)))
        for axis in (0, 2):
            self.r['bx'] = self.shift(self.word(self.ss, local), 2)
            self.r['ax'] = self.dg(self.r['di'] + axis)
            self.field(self.r['di'] + self.r['bx'] + axis, self.r['ax'])
        self.pop('di')
        self.pop('si')
        self.r['sp'] = self.r['bp']
        self.pop('bp')
        self.r['sp'] += 14

    def index(self):
        self.r['bx'] = self.shift(self.r['si'], 2)
        return self.r['bx']

    def init_polygon(self, reset):
        self.rand(0xEF7 if reset else 0xDBA)
        self.r['bx'] = 640
        self.divide(self.r['bx'])
        self.field(CENTER + self.index(), self.r['dx'])
        if reset:
            self.field(CENTER + self.index() + 2, 0xF9C0)
        else:
            self.rand(0xDCE)
            self.r['bx'] = 6400
            self.divide(self.r['bx'])
            self.field(CENTER + self.index() + 2, self.r['dx'])
        self.rand(0xF16 if reset else 0xDE2)
        self.r['ax'] &= 15 if reset else 7
        self.logic(self.r['ax'])
        self.r['dx'] = self.op(8 if reset else 4, self.r['ax'], True)
        self.field(VELOCITY + self.index(), self.r['dx'])
        self.op(self.dg(VELOCITY + self.index()), 0, True)
        if self.dg(VELOCITY + self.r['bx']) == 0:
            self.field(VELOCITY + self.index(), 1)
        self.rand(0xF43 if reset else 0xE0F)
        self.r['ax'] &= 3
        self.logic(self.r['ax'])
        self.r['ax'] = self.op(self.shift(self.r['ax'], 4), 32)
        self.field(VELOCITY + self.index() + 2, self.r['ax'])
        self.rand(0xF5A if reset else 0xE26)
        self.field(ANGLE + self.r['si'], self.r['ax'], 1)
        self.rand(0xF63 if reset else 0xE2F)
        self.al(self.r['ax'] & 7)
        self.logic(self.r['ax'] & 255, bits=8)
        low = self.op(4, self.r['ax'] & 255, True, bits=8)
        self.r['dx'] = (self.r['dx'] & 0xFF00) | low
        self.field(SPEED + self.r['si'], low, 1)
        self.op(self.dg(SPEED + self.r['si'], 1), 0, True, bits=8)
        if self.dg(SPEED + self.r['si'], 1) == 0:
            self.field(SPEED + self.r['si'], 4, 1)

    def render(self):
        self.push(self.ds)
        self.push(POINTS)
        self.r['ax'], self.r['bx'] = self.r['si'], 4
        self.divide(self.r['bx'])
        self.r['ax'] = self.op(self.r['ax'], 3)
        self.push(self.r['ax'])
        self.frame(0xF8E, 0)
        self.calls += 1
        at = address(self.ss, self.r['sp'])
        mask = self.mask | 0x600
        self.events.append(('render', self.full(), bytes(self.memory[at:at + 10]).hex(),
                            bytes(self.memory[address(self.ds, POINTS):address(self.ds, POINTS) + 4 * (self.r['ax'] + 1)]).hex(),
                            self.flags & mask, mask, self.calls))
        self.r, self.flags = reply(self.r, self.calls, self.o['seed'], self.flags, self.o['status'])
        self.mask = ARITH
        self.returned(6)

    def update(self):
        self.enter()
        self.push(self.r['si'])
        self.op(self.dg(INITIALIZED, 1), 0, True, bits=8)
        if not self.dg(INITIALIZED, 1):
            self.r['si'] = 0
            self.logic(0)
            while True:
                self.op(self.r['si'], 16, True)
                if self.r['si'] == 16:
                    break
                self.init_polygon(False)
                self.r['si'] = self.increment(self.r['si'])
            self.field(INITIALIZED, 1, 1)
        self.r['si'] = 0
        self.logic(0)
        while True:
            self.op(self.r['si'], 16, True)
            if self.r['si'] == 16:
                break
            self.push(POINTS)
            self.push(self.dg(CENTER + self.index()))
            self.push(self.dg(CENTER + self.index() + 2))
            self.r['ax'] = self.r['si'] & 3
            self.logic(self.r['ax'])
            self.r['ax'] = self.op(self.shift(self.r['ax'], 4), 64)
            self.push(self.r['ax'])
            self.r['ax'], self.r['bx'] = self.r['si'], 4
            self.divide(4)
            self.r['ax'] = self.op(self.r['ax'], 3)
            self.push(self.r['ax'])
            self.al(self.dg(ANGLE + self.r['si'], 1))
            self.push(self.r['ax'])
            self.push(0xE8C)
            self.build()
            self.r['ax'] = self.dg(VELOCITY + self.index())
            offset = CENTER + self.index()
            self.field(offset, self.op(self.dg(offset), self.r['ax']))
            self.r['ax'] = self.dg(VELOCITY + self.index() + 2)
            offset = CENTER + self.index() + 2
            self.field(offset, self.op(self.dg(offset), self.r['ax']))
            self.al(self.dg(SPEED + self.r['si'], 1))
            self.field(ANGLE + self.r['si'], self.op(self.dg(ANGLE + self.r['si'], 1), self.r['ax'] & 255, bits=8), 1)
            self.op(self.dg(CENTER + self.index()), 0, True)
            bounce = signed(self.dg(CENTER + self.r['bx'])) <= 0
            if not bounce:
                self.op(self.dg(CENTER + self.index()), 639, True)
                bounce = signed(self.dg(CENTER + self.r['bx'])) >= 639
            if bounce:
                self.index()
                self.r['dx'] = 65535
                self.r['ax'] = self.dg(VELOCITY + self.r['bx'])
                self.multiply(self.r['dx'], signed_operands=True)
                self.field(VELOCITY + self.r['bx'], self.r['ax'])
            self.op(self.dg(CENTER + self.index() + 2), 8000, True)
            if signed(self.dg(CENTER + self.r['bx'] + 2)) >= 8000:
                self.init_polygon(True)
            self.render()
            self.r['si'] = self.increment(self.r['si'])
        self.pop('si')
        self.pop('bp')
        self.r['sp'] += 2


class Machine(FrameMachine):
    """Execute all owned and context instructions on one physical Unicorn."""

    def __init__(self, image, load):
        self.image, self.load = image, load
        self.base, self.cs, self.ds = load * 16, load + CS, load + DS
        self.uc = Uc(UC_ARCH_X86, UC_MODE_16)
        self.uc.mem_map(0, 1 << 20)
        memory = bytearray(1 << 20)
        raw = image.relocated_program_image(load)
        memory[self.base:self.base + len(raw)] = raw
        self.initial = bytes(memory)
        self.instructions = {}
        for start, size in ((START, SIZE), (RANDOM, 42), (POLAR, 26)):
            rows = list(Cs(CS_ARCH_X86, CS_MODE_16).disasm(image.program_image[start:start + size], start))
            need(sum(i.size for i in rows) == size, 'complete instruction partition')
            self.instructions.update({i.address: i.size for i in rows})
        self.covered = set()
        self.context = set()
        self.hooks = [self.uc.hook_add(UC_HOOK_CODE, self.code), self.uc.hook_add(UC_HOOK_MEM_WRITE, self.write)]

    def event(self, event):
        need(self.index < len(self.expected.events) and self.expected.events[self.index] == event,
             'event ' + str(self.index) + ': ' + str(event) + ' expected ' + str(self.expected.events[self.index:self.index + 1]))
        self.index += 1

    def write(self, uc, access, at, size, value, user):
        try:
            if self.index < len(self.expected.events) and self.expected.events[self.index][0] == 'far-frame':
                _, dest, ip, cs = self.expected.events[self.index]
                need(size == 2 and (at, value) in ((dest, ip), (dest + 2, cs)), 'actual native far return words')
                return
            self.event(('store', at, size, value))
        except Exception as error:
            self.fail(error)

    def code(self, uc, at, size, user):
        try:
            if at == self.cs * 16 + 0xFFFF:
                self.returned = True
                uc.emu_stop()
                return
            rva = at - self.base
            self.maximum_stack = max(self.maximum_stack, self.stack - self.r('sp'))
            need(self.maximum_stack <= 128, 'bounded full checked stack')
            if rva in (RANDOM, POLAR, RENDER):
                physical = address(self.r('ss'), self.r('sp'))
                ip, cs = struct.unpack('<HH', uc.mem_read(physical, 4))
                self.event(('far-frame', physical, ip, cs))
                if rva == RENDER:
                    mask, count = self.expected.events[self.index][-2:]
                    vertices, pointer, segment = struct.unpack('<3H', uc.mem_read(physical + 4, 6))
                    self.event(('render', self.full(), bytes(uc.mem_read(physical, 10)).hex(),
                                bytes(uc.mem_read(address(segment, pointer), 4 * (vertices + 1))).hex(),
                                uc.reg_read(x.UC_X86_REG_EFLAGS) & mask, mask, count))
                    values, flags = reply({n: self.r(n) for n in (*GPRS, 'cs', 'ds', 'es', 'ss', 'fs', 'gs')},
                                          count, self.o['seed'], uc.reg_read(x.UC_X86_REG_EFLAGS), self.o['status'])
                    for name in ('ax', 'bx', 'cx', 'dx', 'es'):
                        uc.reg_write(REG[name], values[name])
                    uc.reg_write(x.UC_X86_REG_EFLAGS, flags)
                    uc.reg_write(REG['sp'], self.r('sp') + 10)
                    uc.reg_write(REG['cs'], cs)
                    uc.reg_write(REG['ip'], ip)
                    return
            need(self.instructions.get(rva) == size, 'whole allowed instruction at ' + hex(rva))
            destination = self.covered if START <= rva < START + SIZE else self.context
            destination.update(range(rva, rva + size))
        except Exception as error:
            self.fail(error)

    def run(self, kind='update', *, seed=0x1357, flags=0x202, initialized=1,
            count=6, angle=0, radius=112, center_x=320, center_y=3200,
            profile=0, stack=0xF800, status=0xFFFF, reenter=False):
        self.guest_started = False
        need(kind in ('build', 'update') and -1 <= count <= 256, 'bounded entry domain')
        memory = bytearray(self.expected.memory if reenter else self.initial)

        def put(offset, value, width=2):
            at = address(self.ds, offset)
            memory[at:at + width] = (value & ((1 << (width * 8)) - 1)).to_bytes(width, 'little')

        if not reenter:
            put(0x312, seed, 4)
            put(INITIALIZED, initialized, 1)
            for i in range(16):
                # All four post-update X/Y threshold neighborhoods, signed wrap,
                # negative velocity and BYTE angle wrap occur in one frame.
                cx = (0, 1, 638, 639, 640, -1, 32767, -32768)[(i + profile) % 8]
                cy = (7999, 8000, 7998, -1600, 32767, -32768, 0, 7900)[(i + profile) % 8]
                vx = (0, 1, -1, 8, -8, 32767, -32768, 4)[(i + 2 * profile) % 8]
                vy = (0, 1, 2, 32, 80, 32767, -32768, -1)[(i + 2 * profile) % 8]
                put(CENTER + 4 * i, cx)
                put(CENTER + 4 * i + 2, cy)
                put(VELOCITY + 4 * i, vx)
                put(VELOCITY + 4 * i + 2, vy)
                put(ANGLE + i, seed + 37 * i, 1)
                put(SPEED + i, seed - 19 * i, 1)
            for i in range(4 * (max(count, 6) + 1)):
                put(0x3000 + i, seed + i * 29, 1)
        memory[address(0x7000, stack - 128):address(0x7000, stack)] = b'\xD3' * 128
        frame = struct.pack('<7H', 0xFFFF, angle & 65535, count & 65535, radius & 65535,
                            center_y & 65535, center_x & 65535, 0x3000) if kind == 'build' else b'\xFF\xFF'
        at = address(0x7000, stack)
        memory[at:at + len(frame)] = frame
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
        self.o = dict(load=self.load, seed=seed & 65535, status=status)
        self.expected = Prediction(memory, registers, high, flags, self.o)
        getattr(self.expected, kind)()
        self.index, self.error, self.returned = 0, None, False
        self.stack, self.maximum_stack = stack, 0
        self.guest_started = True
        try:
            self.uc.emu_start(self.base + (BUILD if kind == 'build' else UPDATE), 1 << 20, count=200000)
        except UcError as error:
            raise ContractError('Music polygon guest fault') from error
        if self.error is not None:
            raise self.error
        need(self.returned and self.index == len(self.expected.events), 'complete near return and event sequence')
        need(self.full() == self.expected.full(), 'all DWORD registers/six segments ' + str((self.full(), self.expected.full())))
        mask = self.expected.mask | 0x600
        need(self.uc.reg_read(x.UC_X86_REG_EFLAGS) & mask == self.expected.flags & mask, 'all defined flags/IF/DF')
        need(bytes(self.uc.mem_read(0, 1 << 20)) == self.expected.memory, 'full physical memory including every stack byte')
        return dict(kind=kind, registers=self.expected.full(), flags=self.expected.flags & mask, flags_mask=mask,
                    events=self.index, render_calls=self.expected.calls, maximum_stack_depth=self.maximum_stack,
                    trace_sha256=hashlib.sha256(json.dumps(self.expected.events, sort_keys=True).encode()).hexdigest())


def cases():
    for angle in range(256):
        yield 'build', dict(angle=0xA500 | angle, count=3 + angle % 4, radius=64 + 16 * (angle % 4), center_y=(angle * 257) & 65535)
    for count in (-1, 0, 1, 2, 7, 127, 128, 129, 255, 256):
        for radius in (0, -1, -32768, 32767):
            yield 'build', dict(count=count, radius=radius, center_x=-32768, center_y=0xFFFF, angle=0xFFFF)
    for initialized in (0, 1, 128, 255):
        for seed in (0, 1, 4, 8, 0x1357, 0xFFFF, 0x80000000, 0xFFFFFFFF):
            for profile in range(8):
                yield 'update', dict(initialized=initialized, seed=seed, profile=profile)
    for flags in (2, 0x202, 0x402, 0xED7):
        for stack in (0x100, 0xFFF0):
            for kind in ('build', 'update'):
                yield kind, dict(flags=flags, stack=stack, initialized=0, seed=0xFFFFFFFF)


def verify(target, candidate):
    observations = []
    for image in (target, candidate):
        loads = []
        for load in (0x1000, 0x3000):
            machine = Machine(image, load)
            digest, counts, depth = hashlib.sha256(), dict(build=0, update=0), 0
            try:
                for kind, options in cases():
                    try:
                        row = machine.run(kind, **options)
                    except ContractError as error:
                        raise ContractError(str((kind, options, error))) from error
                    digest.update(json.dumps(row, sort_keys=True).encode())
                    counts[kind] += 1
                    depth = max(depth, row['maximum_stack_depth'])
                for i in range(3):
                    row = machine.run('update', initialized=0, reenter=bool(i), flags=0xED7)
                    digest.update(json.dumps(row, sort_keys=True).encode())
                    counts['update'] += 1
                    depth = max(depth, row['maximum_stack_depth'])
                need(machine.covered == set(range(START, START + SIZE)), 'all 645 owned bytes execute')
                need(len(machine.context) == 68, 'all actual IRAND/polar context bytes execute')
                loads.append(dict(load_segment=load, complete_returns=counts, cases=sum(counts.values()),
                                  executed_code_bytes=len(machine.covered), executed_context_bytes=len(machine.context),
                                  consecutive_frames=3, maximum_stack_depth=depth, trace_sha256=digest.hexdigest()))
            finally:
                machine.close()
        observations.append(loads)
    need(observations[0] == observations[1], 'complete target/candidate observations')
    return dict(images=2, observations=observations[0], ignored_stack_bytes=0,
                actual_random_and_polar=True, synthetic_owned_returns=False,
                renderer_is_bounded_reply=True, physical_pixels_or_timing_proved=False,
                source_ownership_promoted=False, whole_product_accepted=False)


def negative_controls(target):
    """Mutate real instructions; verifier defects must propagate as failures."""
    from dataclasses import replace
    controls = (
        ('build-stack-locals', 0xA615, 2, 'build', {}),
        ('center-y-SAR4', 0xA620, 1, 'build', dict(center_y=0x7FFF)),
        ('build-signed-division', 0xA630, 8, 'build', dict(count=129)),
        ('angle-low-BYTE-slot', 0xA634, 1, 'build', dict(angle=0xA501)),
        ('angle-zero-extension', 0xA639, 1, 'build', {}),
        ('cosine-DGROUP-offset', 0xA640, 1, 'build', {}),
        ('actual-polar-entry', 0xA649, 1, 'build', {}),
        ('point-index-times4', 0xA655, 1, 'build', {}),
        ('sine-DGROUP-offset', 0xA663, 1, 'build', {}),
        ('point-y-field', 0xA67B, 1, 'build', {}),
        ('closed-point-x', 0xA68E, 1, 'build', {}),
        ('closed-point-y', 0xA699, 1, 'build', {}),
        ('build-Pascal-pop12', 0xA6A1, 2, 'build', {}),
        ('persistent-initialized-field', 0xA6A9, 1, 'update', {}),
        ('initial-random-entry', 0xA6B6, 1, 'update', dict(initialized=0)),
        ('initial-x-mod640', 0xA6BB, 1, 'update', dict(initialized=0)),
        ('initial-y-mod6400', 0xA6CF, 1, 'update', dict(initialized=0)),
        ('initial-vx-mask7', 0xA6E3, 1, 'update', dict(initialized=0)),
        ('initial-vx-zero-replacement', 0xA708, 1, 'update', dict(initialized=0, seed=1)),
        ('initial-vy-base32', 0xA716, 1, 'update', dict(initialized=0)),
        ('initial-angle-speed4', 0xA732, 1, 'update', dict(initialized=0)),
        ('initial-angle-zero-replacement', 0xA744, 1, 'update', dict(initialized=0, seed=1)),
        ('initial-all16', 0xA748, 1, 'update', dict(initialized=0)),
        ('initialized-persistence', 0xA751, 1, 'update', dict(initialized=0)),
        ('radius64', 0xA775, 1, 'update', {}),
        ('vertex-count3', 0xA782, 1, 'update', {}),
        ('actual-nested-build-entry', 0xA78A, 1, 'update', {}),
        ('x-velocity-field', 0xA793, 1, 'update', {}),
        ('y-velocity-field', 0xA7A5, 1, 'update', {}),
        ('angle-speed-field', 0xA7B2, 1, 'update', {}),
        ('left-reflect-inclusive', 0xA7C2, 1, 'update', {}),
        ('right-boundary639', 0xA7CD, 1, 'update', dict(profile=7)),
        ('reflection-negates-vx', 0xA7D7, 1, 'update', {}),
        ('reset-bound8000', 0xA7EC, 1, 'update', {}),
        ('reset-center-minus1600', 0xA80F, 1, 'update', {}),
        ('reset-vx-mask15', 0xA817, 1, 'update', {}),
        ('reset-vx-zero-replacement', 0xA83C, 1, 'update', dict(seed=10)),
        ('reset-vy-base32', 0xA84A, 1, 'update', {}),
        ('reset-angle-speed4', 0xA866, 1, 'update', {}),
        ('reset-angle-zero-replacement', 0xA878, 1, 'update', dict(seed=10)),
        ('renderer-point-pointer', 0xA87B, 1, 'update', {}),
        ('renderer-vertex-count3', 0xA887, 1, 'update', {}),
        ('all16-updates', 0xA891, 1, 'update', {}),
        ('update-near-return', 0xA898, 8, 'update', {}),
        ('actual-random-multiplier', 0x1D13, 1, 'update', dict(initialized=0)),
        ('actual-polar-shift8', 0xC019, 1, 'build', {}),
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
                    raise  # A scalar/domain defect is not a rejected guest.
                rejected.append(name)
            else:
                raise ValueError('Music polygon mutation survived: ' + name)
        finally:
            machine.close()
    return dict(actual_instruction_mutations=len(controls), rejected=rejected,
                verifier_implementation_exceptions_are_not_rejections=True)
