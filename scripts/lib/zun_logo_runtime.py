"""Independent scalar/event contracts for the ten actual -3 logo procedures.

Guest instructions and the two compiler integer helpers execute. Library services,
RNG replies, keyboard and sync ports are explicit bounded interfaces. Block hooks
keep full-flow checks inexpensive; no historical runtime receipt is consumed.
"""

import hashlib
import json
import math
import struct

import capstone
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_BLOCK, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INSN, UC_HOOK_INTR
from unicorn.x86_const import *

from review_th03_zunsoft import RANGES, IMPORTS, MATH


ENTRIES = {name: (start, size) for name, start, size in RANGES}
BSS, BSS_SIZE, PALETTE = 0x2870, 293, 0x2248
RANDOM = (0, 32767, 16384, 640, 400, 31, 32)
SIN = tuple(round(256 * math.sin(i * math.tau / 256)) for i in range(256))
COS = tuple(round(256 * math.cos(i * math.tau / 256)) for i in range(256))
REGISTERS = {n: globals()["UC_X86_REG_" + n.upper()] for n in
             ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp", "cs", "ds", "es", "ss", "ip")}


def need(value, message):
    if not value:
        raise ValueError("ZUN logo contract: " + message)


def w(value):
    return value & 0xFFFF


def s16(value):
    return (value & 0x7FFF) - (value & 0x8000)


def s8(value):
    return (value & 0x7F) - (value & 0x80)


def word(data, offset):
    return struct.unpack_from("<H", data, offset)[0]


def put(data, offset, value):
    struct.pack_into("<H", data, offset, w(value))


def rem(value, divisor):
    value = s16(value)
    return (-1 if value < 0 else 1) * (abs(value) % divisor)


def vector(length, angle):
    return tuple(w((s16(length) * table[angle & 255]) >> 8) for table in (COS, SIN))


def specification(kind, initial, *, rng=RANDOM, length=37, angle=32,
                  key_frame=None, key_group=3, key_value=1, hardware=False,
                  bios=255, palette=100, sync=(32, 0, 0, 32), **_):
    """State/event implementation independent of guest decode and control flow."""
    state = bytearray(initial)
    events = []
    random_index = 0

    def emit(name, *args):
        events.append((name, *(w(a) for a in args)))

    def out(port, value):
        events.append(("OUT", port, 1, value))

    def clear():
        out(0xA6, 1); emit("GRAPH_CLEAR")
        out(0xA6, 0); emit("GRAPH_CLEAR")
        out(0xA4, 0)

    def init():
        nonlocal palette
        for name in ("MEM_ASSIGN_ALL", "GRAPH_START", "KEY_BEEP_OFF", "TEXT_SYSTEMLINE_HIDE", "TEXT_CURSOR_HIDE", "EGC_START"):
            emit(name)
        clear(); emit("TEXT_CLEAR")
        state[0:2] = bytes((0, 1))
        emit("GRC_SETCLIP", 96, 100, 543, 299)
        emit("GRAPH_HIDE"); emit("SUPER_ENTRY_BFNT", 0x21CE)
        emit("PALETTE_SHOW", palette)
        palette = 0
        emit("PALETTE_SHOW", palette); emit("GRAPH_SHOW")

    def exit_():
        emit("SUPER_FREE"); clear()
        for name in ("MEM_UNASSIGN", "TEXT_CLEAR", "EGC_START"):
            emit(name)

    def setup():
        nonlocal random_index
        for i in range(4):
            put(state, 8 + i * 4, 128 * (i + 1)); put(state, 10 + i * 4, 320 - 80 * i)
            put(state, 226 + i * 2, -8); put(state, 234 + i * 2, 8)
        put(state, 224, 0)
        state[2:7] = bytes((0, 0, 23, 0, 0))
        for i in range(50):
            values = []
            for _ in range(3):
                value = rng[random_index % len(rng)]
                random_index += 1
                emit("IRAND", value)
                values.append(value)
            put(state, 24 + i * 4, rem(values[0], 640))
            put(state, 26 + i * 4, rem(values[1], 400))
            state[243 + i] = (rem(values[2], 32) + 6) & 255
        state[242] = 64

    def circles():
        for i in range(3, -1, -1):
            emit("GRCG_SETCOLOR", 0xC0, 4 - i)
            emit("GRCG_CIRCLEFILL", word(state, 8 + i * 4), word(state, 10 + i * 4), 96)
            for position, speed, high in ((8 + i * 4, 226 + i * 2, 607), (10 + i * 4, 234 + i * 2, 367)):
                value = s16(word(state, position) + word(state, speed))
                put(state, position, value)
                if value <= 32 or value > high:
                    put(state, speed, -word(state, speed))
        out(0x7C, 0)

    def stars():
        emit("GRCG_SETCOLOR", 0xC0, 5)
        for i in range(50):
            emit("GRCG_PSET", word(state, 24 + i * 4), word(state, 26 + i * 4))
            delta = vector(state[243 + i], state[242])
            for position, step, limit in ((24 + i * 4, delta[0], 640), (26 + i * 4, delta[1], 400)):
                value = s16(word(state, position) + step)
                if value < 0:
                    value += limit
                elif value >= limit:
                    value -= limit
                put(state, position, value)
        state[242] = (state[242] + 1) & 255
        out(0x7C, 0)

    def wait():
        for value in sync:
            out(0x5F, None)
            events.append(("IN", 0xA0, 1, value))

    def logo():
        frame = s16(word(state, 224))
        if frame < 50 or frame >= 170:
            return
        wave = 90 <= frame < 130
        if frame in (55, 60, 65, 110, 155, 160, 165):
            state[3] = (state[3] + 2) & 255
        for x, offset in ((256, 0), (320, 1)):
            if wave:
                # A char occupies a two-byte argument slot. TC4 transfers the
                # adjacent opaque padding byte as its unspecified high byte.
                emit("SUPER_WAVE_PUT", x, 192, s8(state[3]) + offset, s8(state[4]), word(state, 6), s8(state[5]))
            else:
                emit("SUPER_PUT_8", x, 192, s8(state[3]) + offset)
        if wave:
            state[4] = (state[4] + (-1 if frame < 110 else 1)) & 255
            state[5] = (state[5] + 4) & 255
            state[6] = (state[6] + (4 if frame < 110 else -4)) & 255

    if kind == "main":
        if hardware:
            for value in (7, 0x20, 6):
                out(0x6A, value)
            bios &= 0x7F
        init(); setup()
        while True:
            frame = s16(word(state, 224))
            tone = s8(state[2])
            if frame > 180:
                if tone <= 0:
                    break
                tone -= 2
            elif tone < 100:
                tone += 2
            else:
                tone = None
            if tone is not None:
                state[2] = tone & 255
                palette = s8(state[2])
                emit("PALETTE_SHOW", palette)
            emit("GRCG_SETCOLOR", 0xC0, 0)
            emit("GRCG_BYTEBOXFILL_X", 12, 100, 67, 299)
            stars(); circles(); logo(); wait(); wait()
            state[1] = state[0]; out(0xA4, state[0])
            state[0] ^= 1; out(0xA6, state[0])
            quit_ = 0
            for group in range(8):
                reply = key_value if key_frame == frame and group == key_group else 0
                emit("KEY_SENSE", group, reply)
                quit_ |= reply
            if quit_:
                break
            put(state, 224, frame + 1)
        exit_()
    elif kind == "graph_clear_both": clear()
    elif kind == "zunsoft_init": init()
    elif kind == "zunsoft_exit": exit_()
    elif kind == "objects_setup": setup()
    elif kind == "circles_render_and_update": circles()
    elif kind == "stars_render_and_update": stars()
    elif kind == "wait": wait()
    elif kind == "logo_render_and_update": logo()
    elif kind != "zunsoft_vector2": raise ValueError(kind)
    return bytes(state), events, w(palette), bios


class Machine:
    def __init__(self, image, load=0x2000):
        need(len(image) == 10096, "complete -3 payload")
        self.base = load * 16
        self.u = Uc(UC_ARCH_X86, UC_MODE_16)
        self.u.mem_map(0, 0x100000)
        self.u.mem_write(self.base + 0x100, image)
        need(struct.unpack_from("<256h", image, 0x22E8 - 0x100) == SIN
             and struct.unpack_from("<256h", image, 0x2368 - 0x100) == COS,
             "bounded vendor trig table inputs")
        need(image[0x20CE:0x20DD] == b"touhou.dat\0\4\3\2\1", "owned initialized data")
        self.instructions = {}
        decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
        for start, length in ENTRIES.values():
            insns = list(decoder.disasm(image[start - 0x100:start - 0x100 + length], start))
            need(sum(i.size for i in insns) == length, "complete owned decode")
            self.instructions.update({i.address: i.size for i in insns})
        self.covered, self.blocks = set(), set()
        self.max_depth = 0
        self.active = False
        self.hooks = [
            self.u.hook_add(UC_HOOK_BLOCK, self.block),
            self.u.hook_add(UC_HOOK_CODE, self.service, None, self.base + min(IMPORTS), self.base + max(IMPORTS)),
            self.u.hook_add(UC_HOOK_CODE, self.stop, None, self.base + 0xF000, self.base + 0xF000),
            self.u.hook_add(UC_HOOK_MEM_WRITE, self.write),
            self.u.hook_add(UC_HOOK_INSN, self.out, None, 1, 0, UC_X86_INS_OUT),
            self.u.hook_add(UC_HOOK_INSN, self.input, None, 1, 0, UC_X86_INS_IN),
            self.u.hook_add(UC_HOOK_INTR, self.interrupt),
        ]
        # Unicorn reports zero-sized blocks for some long 16-bit blocks, and a
        # service IP redirect can miss a block notification. Count actual code
        # hooks instead; remove each function's hook once every byte executed.
        self.coverage_hooks = {name: self.u.hook_add(UC_HOOK_CODE, self.cover, name,
            self.base + start, self.base + start + length - 1) for name, (start, length) in ENTRIES.items()}

    def close(self):
        for hook in [*self.hooks, *self.coverage_hooks.values()]:
            self.u.hook_del(hook)
        self.u = None

    def cover(self, uc, address, size, name):
        offset = address - self.base
        need(self.instructions.get(offset) == size, "actual instruction boundary/width")
        self.covered.update(range(offset, offset + size))
        start, length = ENTRIES[name]
        if name in self.coverage_hooks and all(i in self.covered for i in range(start, start + length)):
            self.u.hook_del(self.coverage_hooks.pop(name))

    def reg(self, name):
        return self.u.reg_read(REGISTERS[name]) & 0xFFFF

    def set(self, name, value):
        self.u.reg_write(REGISTERS[name], w(value))

    def block(self, uc, address, size, _):
        offset = address - self.base
        if offset in IMPORTS or offset == 0xF000:
            return
        need(any(a <= offset and offset + size <= b for a, b in self.allowed), "execution outside owned/helper boundary")
        if 0x367 <= offset < 0x87A:
            need(offset in self.instructions, "owned instruction boundary")
            self.blocks.add((offset, size))

    def stop(self, uc, address, size, _):
        self.returned = True
        uc.emu_stop()

    def interrupt(self, uc, number, _):
        raise ValueError("ZUN logo contract: unexpected interrupt")

    def write(self, uc, access, address, size, value, _):
        if not self.active:
            return
        offset = address - self.base
        if self.sp - 64 <= offset and offset + size <= self.sp:
            self.max_depth = max(self.max_depth, self.sp - offset)
            return
        root = BSS <= offset and offset + size <= BSS + BSS_SIZE
        palette = PALETTE <= offset and offset + size <= PALETTE + 2
        scratch = self.kind == "zunsoft_vector2" and any(a <= offset and offset + size <= a + 2 for a in self.refs)
        bios = self.kind == "main" and address == 0x54D and size == 1
        need(root or palette or scratch or bios, "write outside owned state/stack/interface")

    def out(self, uc, port, size, value, _):
        need(self.active and size == 1 and port in (0xA4, 0xA6, 0x7C, 0x5F, 0x6A), "unmodeled output port/width")
        self.emit(("OUT", port, size, None if port == 0x5F else value))

    def emit(self, event):
        index = len(self.events)
        need(index < len(self.expected_events) and event == self.expected_events[index],
             "independent event/argument/port prefix")
        self.events.append(self.expected_events[index])

    def input(self, uc, port, size, _):
        need(port == 0xA0 and size == 1, "unmodeled input port/width")
        value = self.options["sync"][self.input_index % len(self.options["sync"])]
        self.input_index += 1
        self.emit(("IN", port, size, value))
        return value

    def service(self, uc, address, size, _):
        offset = address - self.base
        need(offset in IMPORTS, "foreign service entry")
        name, cleanup = IMPORTS[offset]
        stack = self.base + self.reg("sp")
        words = struct.unpack("<" + "H" * (cleanup // 2 + 1), uc.mem_read(stack, cleanup + 2))
        args = tuple(reversed(words[1:]))
        if name == "IRAND":
            reply = self.options["rng"][self.random_index % len(self.options["rng"])]
            self.random_index += 1
            args = (w(reply),)
        elif name == "KEY_SENSE":
            frame = struct.unpack("<h", uc.mem_read(self.base + BSS + 224, 2))[0]
            reply = self.options["key_value"] if frame == self.options["key_frame"] and args == (self.options["key_group"],) else 0
            args += (w(reply),)
        elif name == "SUPER_ENTRY_BFNT": reply = self.options["asset_error"]
        else: reply = 0xACE1
        if name == "PALETTE_SHOW":
            args = (struct.unpack("<H", uc.mem_read(self.base + PALETTE, 2))[0],)
        self.emit((name, *args))
        self.set("ax", reply)
        self.set("cx", 0xCCCC); self.set("dx", 0xDDDD)
        self.set("sp", self.reg("sp") + 2 + cleanup)
        self.set("ip", words[0])

    def run(self, kind, initial=None, *, seed=0x1357, sp=0xFF00, flags=0x202, refs=(0x3500, 0x3502), **changes):
        options = dict(rng=RANDOM, length=37, angle=32, key_frame=None, key_group=3,
                       key_value=1, hardware=False, bios=255, palette=100, asset_error=0, sync=(32, 0, 0, 32))
        options.update(changes)
        self.options, self.kind, self.sp, self.refs = options, kind, sp, refs
        self.events, self.returned, self.random_index, self.input_index = [], False, 0, 0
        self.active = False
        initial = bytes((seed + i * 37) & 255 for i in range(BSS_SIZE)) if initial is None else bytes(initial)
        expected, self.expected_events, palette, bios = specification(kind, initial, **options)
        self.u.mem_write(self.base + BSS, initial)
        self.u.mem_write(self.base + PALETTE, struct.pack("<H", w(options["palette"])))
        self.u.mem_write(0x45C, bytes((64 if options["hardware"] else 0,)))
        self.u.mem_write(0x54D, bytes((options["bios"],)))
        self.u.mem_write(self.base + 0x3500, b"\xA5" * 16)
        args = [w(options["length"]), w(options["angle"]), refs[1], refs[0]] if kind == "zunsoft_vector2" else []
        caller = struct.pack("<" + "H" * (len(args) + 1), 0xF000, *args)
        self.u.mem_write(self.base + sp - 64, b"\xCC" * (66 + len(args) * 2))
        self.u.mem_write(self.base + sp, caller)
        registers = {n: w(seed + i * 0x231) for i, n in enumerate(REGISTERS)}
        registers.update(cs=self.base // 16, ds=self.base // 16, ss=self.base // 16, sp=sp, ip=ENTRIES[kind][0])
        for name, value in registers.items(): self.set(name, value)
        self.u.reg_write(UC_X86_REG_EFLAGS, flags)
        names = [kind]
        if kind in ("zunsoft_init", "zunsoft_exit"): names += ["graph_clear_both"]
        if kind == "stars_render_and_update": names += ["zunsoft_vector2"]
        if kind == "main": names = list(ENTRIES)
        self.allowed = [(ENTRIES[n][0], sum(ENTRIES[n])) for n in names]
        if "zunsoft_vector2" in names: self.allowed += MATH
        self.active = True
        try:
            self.u.emu_start(self.base + ENTRIES[kind][0], 0x100000, count=4000000)
        except UcError as exc:
            raise ValueError("ZUN logo contract: guest fault") from exc
        finally:
            self.active = False
        need(self.returned and self.reg("sp") == sp + len(caller), "near return/Pascal cleanup")
        for name in ("si", "di", "bp", "ds", "ss"):
            need(self.reg(name) == registers[name], "callee save: " + name)
        need(self.u.reg_read(UC_X86_REG_EFLAGS) & 0x600 == flags & 0x600, "IF/DF preservation")
        need(bytes(self.u.mem_read(self.base + sp, len(caller))) == caller, "caller frame/arguments preserved")
        need(bytes(self.u.mem_read(self.base + BSS, BSS_SIZE)) == expected, "complete root state")
        need(self.events == self.expected_events, "independent event/argument/port sequence")
        need(struct.unpack("<H", self.u.mem_read(self.base + PALETTE, 2))[0] == palette, "palette interface state")
        need(self.u.mem_read(0x54D, 1)[0] == bios, "PC-9821 mode byte")
        scratch = b""
        if kind == "zunsoft_vector2":
            scratch = bytearray(b"\xA5" * 16)
            for address, value in zip(refs, vector(options["length"], options["angle"])):
                struct.pack_into("<H", scratch, address - 0x3500, value)
            need(bytes(self.u.mem_read(self.base + 0x3500, 16)) == bytes(scratch), "signed multiply/shift and near reference outputs")
        return hashlib.sha256(expected + bytes(scratch) + struct.pack("<HB", palette, bios) + json.dumps(self.events).encode()).hexdigest()


def cases():
    for kind in ENTRIES:
        if kind == "main":
            continue
        for seed, flags in ((0, 2), (0xFFFF, 0x602)):
            yield kind, None, dict(seed=seed, flags=flags, sp=0xE800 if seed else 0xFF00)
    for length in (-32768, -37, 0, 37, 32767):
        for angle in range(256):
            yield "zunsoft_vector2", None, dict(length=length, angle=angle)
    for angle in (0, 32, 64, 128, 160, 255):
        for refs in ((0x3501, 0x3503), (0x3504, 0x3504)):
            yield "zunsoft_vector2", None, dict(length=-32768, angle=0xAB00 | angle, refs=refs, flags=0x602)
    for rng in ((0,), (32767,), (-32768, -1, 640, 400, 31, 32, 65535)):
        yield "objects_setup", None, dict(rng=rng)
    for value in (0, 1, 31, 32, 33, 607, 608, 32767, 32768, 65535):
        state = bytearray((i * 37 + 0xA5) & 255 for i in range(BSS_SIZE))
        for i in range(4):
            put(state, 8 + i * 4, value + i); put(state, 10 + i * 4, value - i)
            put(state, 226 + i * 2, (-8, 8, 0, -32768)[i])
            put(state, 234 + i * 2, (8, -8, -32768, 0)[i])
        yield "circles_render_and_update", state, {}
    for angle in (0, 1, 31, 32, 63, 64, 127, 128, 159, 160, 191, 192, 254, 255):
        state = bytearray((i * 29 + angle) & 255 for i in range(BSS_SIZE))
        state[242] = angle
        for i in range(50):
            put(state, 24 + i * 4, (0, 639, 640, -1, 32767, -32768)[i % 6])
            put(state, 26 + i * 4, (0, 399, 400, -1, 32767, -32768)[(i + 3) % 6])
            state[243 + i] = (i * 17 + angle) & 255
        yield "stars_render_and_update", state, {}
    for frame in (-32768, -1, *range(181), 32767):
        state = bytearray((i * 37 + 0xA5) & 255 for i in range(BSS_SIZE))
        put(state, 224, frame)
        state[3:8] = bytes((0xFE, 23, 250, 127, 0xA5))
        yield "logo_render_and_update", state, {}
    for padding in range(256):
        for amplitude in (0, 127, 128, 255):
            state = bytearray(BSS_SIZE)
            put(state, 224, 90 if padding & 1 else 110)
            state[3:8] = bytes((127, 255, 255, amplitude, padding))
            yield "logo_render_and_update", state, {}
    for sync in ((0, 32), (32, 32, 0, 0, 0, 32)):
        yield "wait", None, dict(sync=sync, seed=0xFFFF)
    for group in range(8):
        yield "main", None, dict(key_frame=0, key_group=group, key_value=0x8000,
                                  hardware=bool(group & 1), asset_error=0xFFF3,
                                  bios=(0, 127, 128, 255)[group % 4], flags=0x602 if group & 2 else 2)


def verify(target, candidate):
    observations = []
    total = 0
    for load in (0x1000, 0x3000):
        machines = [Machine(image, load) for image in (target, candidate)]
        transcript = hashlib.sha256()
        count = 0
        try:
            for kind, state, options in cases():
                left = machines[0].run(kind, state, **options)
                need(left == machines[1].run(kind, state, **options), "target/candidate state/event trace")
                transcript.update(left.encode())
                count += 1
            # The long fade executes 231 complete rendered frames. The second
            # load repeats every bounded entry, hardware and keyboard flow;
            # avoiding a duplicate long fade keeps routine verification bounded.
            if load == 0x1000:
                left = machines[0].run("main")
                need(left == machines[1].run("main"), "full 231-frame fade trace")
                transcript.update(left.encode()); count += 1
            expected = set(range(0x367, 0x87A))
            if load == 0x1000:
                need(all(m.covered == expected for m in machines), "owned execution coverage: " +
                     str([sorted(expected - m.covered)[:24] for m in machines]))
            observations.append(dict(load_segment=load, cases_per_image=count,
                trace_sha256=transcript.hexdigest(), covered_owner_bytes=len(machines[0].covered),
                maximum_observed_stack_depth=max(m.max_depth for m in machines)))
            total += count
        finally:
            for machine in machines: machine.close()
    return dict(cases_per_image=total, images=2, functions=10, executed_owner_bytes=1299,
                full_fade_frames=231, data_bytes=15, bss_bytes=293,
                vector_argument_bytes=8, vector_callee_pop_bytes=8,
                opaque_amplitude_high_bytes=256, observations=observations,
                scope="actual root and integer helpers; independent state/event arithmetic; foreign library, asset, RNG, key and device replies bounded")


def negative_controls(image):
    logo = bytearray(BSS_SIZE)
    put(logo, 224, 90)
    logo[3:8] = bytes((6, 23, 250, 127, 0xA5))
    circle = bytearray(BSS_SIZE)
    for i in range(4):
        put(circle, 8 + i * 4, 40); put(circle, 10 + i * 4, 40)
        put(circle, 226 + i * 2, -8); put(circle, 234 + i * 2, -8)
    cases_ = (
        ("clear page", "graph_clear_both", 0x36E, "01", "00", None, {}),
        ("clip boundary", "zunsoft_init", 0x3AE, "1f02", "1e02", None, {}),
        ("page initialization", "zunsoft_init", 0x3A3, "00", "01", None, {}),
        ("filename near pointer", "zunsoft_init", 0x3BA, "ce21", "cf21", None, {}),
        ("vector Pascal cleanup", "zunsoft_vector2", 0x437, "0800", "0600", None, {}),
        ("signed arithmetic shift", "zunsoft_vector2", 0x40B, "08", "07", None, dict(length=37, angle=160)),
        ("near reference output", "zunsoft_vector2", 0x410, "04", "05", None, {}),
        ("setup star count", "objects_setup", 0x4F7, "32", "31", None, {}),
        ("signed RNG modulus", "objects_setup", 0x4C4, "8002", "8102", None, dict(rng=(640,))),
        ("inclusive circle boundary", "circles_render_and_update", 0x55B, "7e", "7c", circle, {}),
        ("star wrap width", "stars_render_and_update", 0x620, "8002", "7f02", None, {}),
        ("sync transition", "wait", 0x68C, "75", "74", None, dict(sync=(0, 32))),
        ("wave phase", "logo_render_and_update", 0x715, "04", "03", logo, {}),
        ("opaque char carrier", "logo_render_and_update", 0x6E4, "ff367628", "687f0090", logo, {}),
        ("PC-9821 mode mask", "main", 0x7EF, "7f", "ff", None, dict(hardware=True, key_frame=0)),
        ("keyboard groups", "main", 0x866, "08", "07", None, dict(key_frame=0)),
        ("page flip", "main", 0x851, "01", "00", None, dict(key_frame=0)),
        ("fade step", "main", 0x817, "02", "01", None, dict(key_frame=0)),
    )
    rejected = []
    for name, kind, address, old, new, state, options in cases_:
        raw = bytearray(image)
        before, after = bytes.fromhex(old), bytes.fromhex(new)
        at = address - 0x100
        need(raw[at:at + len(before)] == before and len(before) == len(after), "mutation anchor: " + name)
        raw[at:at + len(before)] = after
        machine = None
        try:
            machine = Machine(bytes(raw), 0x2000)
            machine.run(kind, state, **options)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("ZUN logo contract: mutation survived: " + name)
        finally:
            if machine is not None: machine.close()
    return dict(count=len(rejected), rejected=rejected)
