"""Execute MAIN's cleanup and wipe producers against bounded service contracts.

The guest instructions, stack and memory writes are real. Foreign graphics and
DOS services are ABI stubs; this does not establish raster or device behavior.
"""

from dataclasses import replace
import struct
import capstone
from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UcError
from unicorn.x86_const import *

ENTRIES = {"exec": (0xB454, 79), "none": (0xB4A3, 5),
           "cover": (0xB4A8, 354), "uncover": (0xB60A, 304)}
SERVICES = {0x1596: ("pi_free", 8), 0x248C: ("super_free", 0),
            0x1590: ("hide", 0), 0x1FDA: ("text_clear", 0), 0x11DA: ("gaiji", 0),
            0xE8F0 + 0x62C: ("mrs_free", 2), 0xE8F0 + 0x12A: ("game_exit", 0),
            0x8F69: ("execl", 0), 0xC40: ("clip", 8), 0xF5C: ("color", 4),
            0xFAC: ("triangle", 12), 0xF86: ("off", 0), 0xB39E: ("bomb", 0)}
REGISTERS = {"ax": UC_X86_REG_AX, "bx": UC_X86_REG_BX, "cx": UC_X86_REG_CX,
             "dx": UC_X86_REG_DX, "si": UC_X86_REG_SI, "di": UC_X86_REG_DI,
             "bp": UC_X86_REG_BP, "sp": UC_X86_REG_SP, "cs": UC_X86_REG_CS,
             "ds": UC_X86_REG_DS, "ss": UC_X86_REG_SS, "es": UC_X86_REG_ES,
             "ip": UC_X86_REG_IP}


def need(value, message):
    if not value:
        raise ValueError("handoff contract: " + message)


def w(value):
    return value & 0xFFFF


def signed(value):
    value = w(value)
    return value - 0x10000 if value & 0x8000 else value


def half(value):
    value = signed(value)
    return w((-1 if value < 0 else 1) * (abs(value) // 2))


def state(frame=0, vertices=None, **changes):
    result = dict(frame=frame, midpoint=0x79, callback=0x4567, hmask=0x1234,
                  vertices=tuple(w(x) for x in (vertices or range(8))),
                  filename=(0xFE01, 0x4123), image=(0xFFFE, 0x4567), status=0xFFFF,
                  success=False, sp=0x80)
    result.update(changes)
    return result


def specification(kind, initial, ds):
    """Observable command/state contract, independent of instruction decoding."""
    output = dict(initial)
    events = []
    if kind == "none":
        return events, output
    if kind == "exec":
        events = [("pi_free", initial["image"] + (0x1AB4, ds)),
                  ("super_free", ()), ("hide", ()), ("text_clear", ()), ("gaiji", ()),
                  ("mrs_free", (0,)), ("mrs_free", (1,)), ("game_exit", ()),
                  ("execl", initial["filename"] * 2 + (0, 0))]
        return events, output
    points = list(initial["vertices"])
    closing = kind == "cover"
    if initial["frame"] == 0:
        points = list((303, 382, 16, 382, 16, 16, 303, 16) if closing
                      else (303, 16, 303, 382, 16, 382, 16, 16))
    deltas = ((0, -18), (3, -23), (4, 18), (7, 23)) if closing else (
        (1, 23), (2, -18), (5, -23), (6, 18))
    for index, delta in deltas:
        points[index] = w(points[index] + delta)
    events.extend([("clip", (191, 623, 0, 8 if closing else 16)), ("color", (2, 0xC0))])
    # Each player receives the same half-height geometry, translated by320.
    groups = [([(303, 8, 303, 191, 0), (16, 8, 16, 191, 2)], 0x5555),
              ([(16, 191, 303, 191, 1), (16, 8, 303, 8, 3)], 0xAAAA)] if closing else [
        ([(16, 191, 303, 191, 0), (16, 8, 16, 191, 1),
          (16, 8, 303, 8, 2), (303, 8, 303, 191, 3)], initial["hmask"])]
    for anchors, mask in groups:
        for translation in (0, 320):
            for x1, y1, x2, y2, vertex in anchors:
                x3 = w(points[vertex * 2] + translation)
                y3 = half(points[vertex * 2 + 1])
                events.append(("triangle", tuple(w(x) for x in
                    (y3, x3, y2, x2 + translation, y1, x1 + translation)), mask))
    output["vertices"] = tuple(points)
    output["frame"] = (initial["frame"] + 1) & 255
    if output["frame"] >= 16:
        output["frame"] = 0
        output["callback"] = 0x1F2A if closing else 0x1DC3
        if closing:
            events.extend([("bomb", (0x3932,)), ("bomb", (0x395A,))])
            output["midpoint"] = 1
    if closing:
        output["hmask"] = 0xFFFF
    events.extend([("off", ()), ("clip", (199, 639, 0, 0))])
    return events, output


class Machine:
    def __init__(self, image, load_segment):
        self.load = load_segment
        self.base = load_segment * 16
        self.ds = load_segment + 0x1D56
        self.data = self.ds * 16
        self.u = Uc(UC_ARCH_X86, UC_MODE_16)
        self.u.mem_map(0, 0x100000)
        self.u.mem_write(self.base, image.relocated_program_image(load_segment))
        self.instructions = {}
        decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
        for start, size in ENTRIES.values():
            for instruction in decoder.disasm(image.program_image[start:start + size], start):
                self.instructions[instruction.address] = instruction.size
        self.active = False
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def reg(self, name):
        return self.u.reg_read(REGISTERS[name]) & 0xFFFF

    def set(self, name, value):
        self.u.reg_write(REGISTERS[name], w(value))

    def words(self, address, count):
        return struct.unpack("<" + "H" * count, self.u.mem_read(address, count * 2))

    def write(self, uc, access, address, size, value, _):
        if not self.active:
            return
        depth = 18 if self.kind == "exec" else 2 if self.kind == "none" else 20
        stack_top = 0x70000 + self.initial["sp"]
        stack = stack_top - depth <= address and address + size <= stack_top
        own_data = self.kind in {"cover", "uncover"} and (
            self.data + 0x2660 <= address and address + size <= self.data + 0x2674
            or self.data + 0x5E8 <= address and address + size <= self.data + 0x5EA)
        need(stack or own_data, "write outside owned state/stack")

    def code(self, uc, address, size, _):
        if address == self.return_address:
            self.returned = True
            uc.emu_stop()
            return
        rva = address - self.base
        if rva in SERVICES:
            role, pop = SERVICES[rva]
            sp = self.reg("sp")
            stack = self.reg("ss") * 16 + sp
            ip, cs = self.words(stack, 2)
            args = self.words(stack + 4, pop // 2)
            if role == "execl":
                args = self.words(stack + 4, 6)
            event = (role, (self.reg("bx"),) if role == "bomb" else args)
            if role == "triangle":
                event += (self.words(self.data + 0x5E8, 1)[0],)
            need(len(self.events) < len(self.expected)
                 and event == self.expected[len(self.events)], "service order, geometry or arguments differ")
            self.events.append(event)
            if role == "execl" and self.initial["success"]:
                self.replaced = True
                uc.emu_stop()
                return
            for register, value in (("ax", 0x9100), ("bx", 0xA200), ("cx", 0xB300),
                                    ("dx", 0xC400), ("es", 0xD000)):
                self.set(register, value + len(self.events))
            if role == "execl":
                self.set("ax", self.initial["status"])
            uc.reg_write(UC_X86_REG_EFLAGS, 0x203)
            self.set("sp", sp + 4 + pop)
            self.set("cs", cs)
            self.set("ip", ip)
            return
        need(rva in self.instructions, "unexpected foreign flow or instruction boundary")
        self.seen.update(range(rva, rva + self.instructions[rva]))

    def run(self, kind, initial):
        self.active = False
        self.kind, self.initial = kind, initial
        self.events, self.seen = [], set()
        self.returned = self.replaced = False
        self.expected, expected_state = specification(kind, initial, self.ds)
        self.u.mem_write(self.data + 0x2660, struct.pack("<HBB8H", initial["callback"],
            initial["frame"], initial["midpoint"], *initial["vertices"]))
        self.u.mem_write(self.data + 0x5E8, struct.pack("<H", initial["hmask"]))
        self.u.mem_write(self.data + 0x1A9C, struct.pack("<2H", *initial["image"]))
        cs = self.load + 0x96E
        for register, value in (("ax", 0xA55A), ("bx", 0xB66B), ("cx", 0xC77C),
                                ("dx", 0xD88D), ("bp", 0x1357), ("si", 0x2468),
                                ("di", 0x369C), ("es", 0x9000), ("ss", 0x7000),
                                ("ds", self.ds), ("cs", cs), ("sp", initial["sp"])):
            self.set(register, value)
        self.u.reg_write(UC_X86_REG_EFLAGS, 0x202)
        if kind == "exec":
            self.return_address = 0x60030
            stack = (0x30, 0x6000) + initial["filename"]
        else:
            self.return_address = cs * 16 + 0x7000
            stack = (0x7000,)
        self.u.mem_write(0x70000 + initial["sp"], struct.pack("<" + "H" * len(stack), *stack))
        start = ENTRIES[kind][0]
        self.set("ip", start - 0x96E0)
        self.active = True
        try:
            self.u.emu_start(self.base + start, 0, count=20000)
        except UcError as error:
            raise ValueError("handoff contract: guest execution failed") from error
        finally:
            self.active = False
        need(self.returned or self.replaced, "bounded execution did not finish")
        need(self.events == self.expected, "incomplete service sequence")
        should_replace = kind == "exec" and initial["success"]
        need(self.replaced == should_replace and self.returned != should_replace, "DOS return/replacement path differs")
        if self.returned:
            need(self.reg("sp") == w(initial["sp"] + (8 if kind == "exec" else 2)), "return stack cleanup differs")
            need((self.reg("bp"), self.reg("si"), self.reg("di"), self.reg("ds"), self.reg("ss"))
                 == (0x1357, 0x2468, 0x369C, self.ds, 0x7000), "callee-saved state differs")
        callback, frame, midpoint, *vertices = self.words_state()
        actual_state = dict(callback=callback, frame=frame, midpoint=midpoint,
                            vertices=tuple(vertices), hmask=self.words(self.data + 0x5E8, 1)[0])
        need(actual_state == {k: expected_state[k] for k in actual_state}, "transition state/callback differs")
        if kind == "exec" and self.returned:
            need(self.reg("ax") == w(initial["status"]), "signed AX result is not propagated")
        return dict(events=self.events, state=actual_state, replaced=self.replaced,
                    ax=signed(self.reg("ax")) if kind == "exec" and self.returned else None), self.seen

    def words_state(self):
        return struct.unpack("<HBB8H", self.u.mem_read(self.data + 0x2660, 20))


PATTERNS = ((303, 382, 16, 382, 16, 16, 303, 16),
            (32767, -3, -32768, -32767, 0, 32767, -1, -1),
            (-1, -32768, 32767, -1, -32768, 1, 32000, -32767))


def cases():
    yield "none", state()
    for kind in ("cover", "uncover"):
        for frame in range(256):
            yield kind, state(frame, PATTERNS[frame % 3], sp=0x200 if frame & 1 else 0xFFE0)
        for frame in (1, 15, 255):
            for vertices in PATTERNS:
                yield kind, state(frame, vertices)
    for success in (False, True):
        for status in (0xFFFF, 0x8001):
            for filename in ((0xFE01, 0x4123), (0, 0x3000), (0xFFFE, 0xF000)):
                for image in ((0, 0), (0xFFFE, 0x4567)):
                    yield "exec", state(filename=filename, image=image, status=status, success=success)


def compare(target, candidate):
    coverage = {kind: set() for kind in ENTRIES}
    counts = {kind: 0 for kind in ENTRIES}
    for load in (0x2000, 0x3000):
        machines = [Machine(image, load) for image in (target, candidate)]
        for kind, initial in cases():
            first, seen = machines[0].run(kind, initial)
            other, other_seen = machines[1].run(kind, initial)
            need(first == other and seen == other_seen, "target/candidate observations differ")
            coverage[kind].update(seen)
            counts[kind] += 1
    for kind, (start, size) in ENTRIES.items():
        need(coverage[kind] == set(range(start, start + size)), "complete instruction-byte coverage required")
    return dict(equal=True, cases=sum(counts.values()), cases_by_entry=counts,
                code_bytes_executed=sum(len(v) for v in coverage.values()),
                bytes_by_entry={k: len(v) for k, v in coverage.items()},
                services="bounded ABI stubs; real DOS/raster/device behavior remains unverified")


def negative_controls(image):
    controls = []
    program = image.program_image
    first_half = program.index(b"\xd1\xf8", 0xB4A8, 0xB60A) + 1
    threshold = program.index(b"\x80\x3e\x62\x26\x10", 0xB4A8, 0xB60A) + 4
    edits = [("signed-half", first_half, b"\xe8", "cover", state(1, PATTERNS[1])),
             ("frame-threshold", threshold, b"\x0f", "cover", state(14)),
             ("near-return", 0xB4A7, b"\xcb", "none", state()),
             ("far-return-pop", 0xB4A1, b"\x02", "exec", state()),
             ("far-null-width", 0xB48C, b"\x90", "exec", state()),
             ("mrs-slot", 0xB47A, b"\x02", "exec", state()),
             ("pi-header", 0xB459, b"\xb6", "exec", state()),
             ("exec-cleanup-order", 0xB488, struct.pack("<HH", 0x1590, 0), "exec", state()),
             ("callback", 0xB5EC, b"\x2b", "cover", state(15)),
             ("midpoint", 0xB5E2, b"\x00", "cover", state(15))]
    for name, at, value, kind, initial in edits:
        changed = bytearray(program)
        need(changed[at:at + len(value)] != value, "mutation must change guest bytes")
        changed[at:at + len(value)] = value
        try:
            Machine(replace(image, program_image=bytes(changed)), 0x2000).run(kind, initial)
        except ValueError:
            controls.append(name)
        else:
            raise ValueError("handoff contract: negative control survived: " + name)
    return dict(count=len(controls), rejected=controls)
