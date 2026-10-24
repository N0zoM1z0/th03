"""Execute MAINL's four lifecycle owners with bounded library replies.

All guest instructions, pointer stores, OUTs, near/far calls and returns execute.
Library bodies, physical hardware and DOS lifetimes remain outside this model.
"""

from dataclasses import replace
import struct

import capstone
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INSN
from unicorn.x86_const import *


ENTRIES = {"planes": (0xC7E2, 41), "exit": (0xC990, 67),
           "init": (0xCEE0, 62), "exit_to_main": (0xD16F, 40)}
SERVICES = {0x213E: ("assign", 2), 0x235A: ("unassign", 0),
            0x1F6E: ("vsync_start", 0), 0x201C: ("vsync_end", 0),
            0x75A: ("egc_start", 0), 0xE24: ("graph_400line", 0),
            0x2AAE: ("js_start", 0), 0x17CA: ("js_end", 0),
            0x2856: ("pfstart", 4), 0x2912: ("pfend", 0),
            0xE72: ("clear", 0), 0x1F20: ("text_clear", 0)}
REGISTERS = {name: globals()["UC_X86_REG_" + name.upper()] for name in
             ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp", "cs", "ds", "es", "ss", "ip")}
POINTERS = struct.pack("<4I", 0xA8000000, 0xB0000000, 0xB8000000, 0xE0000000)
PLANE_OFFSET = 0x1C60


def need(value, message):
    if not value:
        raise ValueError("MAINL lifecycle contract: " + message)


def specification(kind, assign, filename):
    if kind == "planes":
        return [], True
    if kind == "init":
        events = [("assign", 18000)]
        if assign:
            return events, False
        return events + [("vsync_start",), ("egc_start",), ("graph_400line",),
                         ("js_start",), ("pfstart", *filename)], True
    if kind == "exit":
        return [("pfend",), ("out", 0xA6, 1), ("clear",), ("out", 0xA6, 0), ("clear",),
                ("out", 0xA6, 0), ("out", 0xA4, 0), ("vsync_end",), ("unassign",),
                ("text_clear",), ("js_end",), ("egc_start",)], False
    return [("pfend",), ("out", 0xA6, 0), ("out", 0xA4, 0), ("vsync_end",),
            ("unassign",), ("js_end",), ("egc_start",)], False


class Machine:
    def __init__(self, image, load):
        need(image.valid, "valid MZ required")
        self.base = load * 16
        self.ds = load + 0xE3F
        self.data = self.ds * 16
        self.u = Uc(UC_ARCH_X86, UC_MODE_16)
        self.u.mem_map(0, 0x100000)
        self.u.mem_write(self.base, image.relocated_program_image(load))
        self.instructions = {}
        decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
        for start, size in ENTRIES.values():
            insns = list(decoder.disasm(image.program_image[start:start + size], start))
            need(sum(i.size for i in insns) == size, "complete owner decode")
            self.instructions.update({i.address: i.size for i in insns})
        self.covered = set()
        self.active = False
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)
        self.u.hook_add(UC_HOOK_INSN, self.out, None, 1, 0, UC_X86_INS_OUT)

    def reg(self, name):
        return self.u.reg_read(REGISTERS[name]) & 0xFFFF

    def set(self, name, value):
        self.u.reg_write(REGISTERS[name], value & 0xFFFF)

    def write(self, uc, access, address, size, value, _):
        if not self.active:
            return
        stack = self.stack - 10 <= address and address + size <= self.stack
        planes = self.kind in ("planes", "init") and self.data + PLANE_OFFSET <= address and address + size <= self.data + PLANE_OFFSET + 16
        need(stack or planes, "write outside owned stack/plane state")
        if planes:
            self.stores.append((address - self.data, size, value))

    def out(self, uc, port, size, value, _):
        need(self.active and size == 1, "byte OUT required")
        self.events.append(("out", port, value))

    def code(self, uc, address, size, _):
        if address == 0x60000:
            self.returned = True
            uc.emu_stop()
            return
        rva = address - self.base
        if rva in SERVICES:
            role, pop = SERVICES[rva]
            stack = self.reg("ss") * 16 + self.reg("sp")
            ip, cs = struct.unpack("<HH", uc.mem_read(stack, 4))
            caller = cs * 16 + ip - self.base
            need(any(lo < caller <= lo + length for lo, length in ENTRIES.values()), "service return must enter an owner")
            args = struct.unpack("<" + "H" * (pop // 2), uc.mem_read(stack + 4, pop)) if pop else ()
            self.events.append((role, *args))
            for name in ("ax", "cx", "dx", "es"):
                self.set(name, self.seed ^ (0x1234 + len(self.events) * 0x101))
            self.set("ax", self.assign if role == "assign" else self.library_return)
            self.u.reg_write(UC_X86_REG_EFLAGS, (self.u.reg_read(UC_X86_REG_EFLAGS) & ~0xC5) | (0xC5 if self.seed & 1 else 0))
            self.set("sp", self.reg("sp") + 4 + pop)
            self.set("cs", cs)
            self.set("ip", ip)
            return
        allowed = [ENTRIES[self.kind]] + ([ENTRIES["planes"]] if self.kind == "init" else [])
        need(any(lo <= rva < lo + length for lo, length in allowed) and self.instructions.get(rva) == size,
             "execution outside owned instructions/services")
        self.covered.update(range(rva, rva + size))

    def run(self, kind, assign=0, filename=(0xFFFE, 0x4321), library_return=0xACE1,
            seed=0x1357, sp=0x80, flags=0x202):
        self.kind, self.assign, self.seed, self.library_return = kind, assign, seed, library_return
        self.events, self.stores, self.returned = [], [], False
        self.active = False
        self.stack = 0x70000 + sp
        self.u.mem_write(self.stack - 16, b"\xCC" * 32)
        self.u.mem_write(self.stack, struct.pack("<4H", 0, 0x6000, *filename))
        self.u.mem_write(self.data + PLANE_OFFSET - 4, b"\xA5" * 24)
        initial = {n: (seed + i * 0x231) & 0xFFFF for i, n in enumerate(REGISTERS)}
        initial.update(cs=self.base // 16 + 0xC7E, ip=ENTRIES[kind][0] - 0xC7E0,
                       ds=self.ds, ss=0x7000, sp=sp)
        for name, value in initial.items():
            self.set(name, value)
        self.u.reg_write(UC_X86_REG_EFLAGS, flags)
        self.active = True
        try:
            self.u.emu_start(self.base + ENTRIES[kind][0], 0x100000, count=300)
        except UcError as exc:
            raise ValueError("MAINL lifecycle contract: guest fault") from exc
        finally:
            self.active = False
        need(self.returned and self.reg("sp") == sp + (8 if kind == "init" else 4), "far return and Pascal cleanup")
        events, planes_written = specification(kind, assign, filename)
        need(self.events == events, "service/argument/port sequence")
        for name in ("bx", "si", "di", "bp", "ds", "ss"):
            need(self.reg(name) == initial[name], "callee save: " + name)
        need(self.u.reg_read(UC_X86_REG_EFLAGS) & 0x600 == flags & 0x600, "IF/DF preservation")
        need(bytes(self.u.mem_read(self.stack, 8)) == struct.pack("<4H", 0, 0x6000, *filename), "caller return/arguments unchanged")
        expected = POINTERS if planes_written else b"\xA5" * 16
        need(bytes(self.u.mem_read(self.data + PLANE_OFFSET - 4, 24)) == b"\xA5" * 4 + expected + b"\xA5" * 4,
             "four far pointers and neighboring state")
        stores = [(PLANE_OFFSET + i * 4, 4, value) for i, value in
                  enumerate((0xA8000000, 0xB0000000, 0xB8000000, 0xE0000000))] if planes_written else []
        need(self.stores == stores, "ordered dword pointer stores")
        if kind == "init":
            need(self.reg("ax") == (1 if assign else 0), "AX result independent of library returns")
        return tuple(self.events), expected, self.reg("ax") if kind == "init" else None


def verify(target, candidate):
    cases = 0
    for load in (0x1000, 0x3000):
        machines = [Machine(image, load) for image in (target, candidate)]
        for kind in ENTRIES:
            for seed in (0, 1, 0x8000, 0xFFFF):
                for sp in (0x40, 0xFFF0):
                    for flags in (2, 0x202, 0x402, 0x602):
                        for assign in ((0, 1, 0x7FFF, 0x8000, 0xFFFF, 0x1234) if kind == "init" else (0,)):
                            for filename in (((0, 0), (0xFFFF, 0), (0xFFFE, 0xFFFF), (0x1234, 0x4321)) if kind == "init" else ((0, 0),)):
                                for reply in ((0, 1, 0xFFFF) if kind == "init" else (0xACE1,)):
                                    left = machines[0].run(kind, assign, filename, reply, seed, sp, flags)
                                    right = machines[1].run(kind, assign, filename, reply, seed, sp, flags)
                                    need(left == right, "target/candidate observables")
                                    cases += 1
        expected = {i for start, size in ENTRIES.values() for i in range(start, start + size)}
        need(all(m.covered == expected for m in machines), "all 210 owner bytes must execute")
    return dict(cases_per_image=cases, images=2, executed_owner_bytes=210, functions=4,
                load_segments=[0x1000, 0x3000], init_argument_bytes=4, init_callee_pop_bytes=4,
                scope="actual guest code and owned plane setup; foreign library/device/DOS behavior remains bounded")


def negative_controls(image):
    rejected = []
    for name, kind, offset, old, new, assign in (
        ("assign paragraphs", "init", 4, "5046", "4f46", 0),
        ("nonzero failure", "init", 13, "74", "75", 0),
        ("failure AX", "init", 16, "0100", "0000", 1),
        ("failure Pascal pop", "init", 20, "0400", "0200", 1),
        ("success Pascal pop", "init", 60, "0400", "0200", 0),
        ("far filename width", "init", 47, "66", "90", 0),
        ("far filename offset", "init", 50, "06", "08", 0),
        ("plane call target", "init", 25, "e7f8", "e8f8", 0),
        ("plane segment", "planes", 11, "a8", "a0", 0),
        ("plane field ownership", "planes", 6, "601c", "5e1c", 0),
        ("page order", "exit", 12, "01", "00", 0),
        ("cleanup order", "exit", 41, "1c20", "5a23", 0),
        ("return-to-MAIN port", "exit_to_main", 9, "a600", "a400", 0),
        ("return-to-MAIN far return", "exit_to_main", 39, "cb", "c3", 0),
        ("callee save", "exit", 65, "5d", "90", 0),
    ):
        raw = bytearray(image.program_image)
        at = ENTRIES[kind][0] + offset
        before, after = bytes.fromhex(old), bytes.fromhex(new)
        need(raw[at:at + len(before)] == before and len(before) == len(after), "mutation anchor: " + name)
        raw[at:at + len(before)] = after
        try:
            Machine(replace(image, program_image=bytes(raw)), 0x1000).run(kind, assign)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("MAINL lifecycle contract: mutation survived: " + name)
    return dict(count=len(rejected), rejected=rejected)
