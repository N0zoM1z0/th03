"""Execute the three OP exit/plane owners with bounded foreign services.

Guest calls, OUT instructions, near/far returns and four far-pointer stores are
real instructions. Library bodies, physical devices and DOS remain outside this
contract. Expected events are independent of the instruction decoder.
"""

from dataclasses import replace
import struct

import capstone
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INSN
from unicorn.x86_const import *


ENTRIES = {"exit_dos": (0xBEB8, 25), "planes": (0xBED1, 41), "exit": (0xBFC2, 67)}
SERVICES = {0x2C1C: "pfend", 0x114C: "graph_clear", 0x2378: "vsync_end",
            0x2676: "mem_unassign", 0x21F4: "text_clear", 0x1A1C: "js_end",
            0x0708: "egc_start", 0x1A2E: "key_beep_on",
            0x2238: "text_systemline_show", 0x222C: "text_cursor_show"}
REGISTERS = {name: globals()["UC_X86_REG_" + name.upper()] for name in
             ("ax", "bx", "cx", "dx", "si", "di", "bp", "sp", "cs", "ds", "es", "ss", "ip")}
PLANE_OFFSET = 0x19FA
PLANE_BYTES = struct.pack("<4I", 0xA8000000, 0xB0000000, 0xB8000000, 0xE0000000)


def need(value, message):
    if not value:
        raise ValueError("OP exit contract: " + message)


def specification(kind):
    if kind == "planes":
        return []
    events = [("pfend",), ("out", 0xA6, 1), ("graph_clear",),
              ("out", 0xA6, 0), ("graph_clear",), ("out", 0xA6, 0),
              ("out", 0xA4, 0), ("vsync_end",), ("mem_unassign",),
              ("text_clear",), ("js_end",), ("egc_start",)]
    if kind == "exit_dos":
        events += [("key_beep_on",), ("text_systemline_show",), ("text_cursor_show",)]
    return events


class Machine:
    def __init__(self, image, load):
        need(image.valid, "valid MZ required")
        self.base = load * 16
        self.ds = load + 0xD7F
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
        self.active = False
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)
        self.u.hook_add(UC_HOOK_INSN, self.out, None, 1, 0, UC_X86_INS_OUT)
        self.covered = set()

    def reg(self, name):
        return self.u.reg_read(REGISTERS[name]) & 0xFFFF

    def set(self, name, value):
        self.u.reg_write(REGISTERS[name], value & 0xFFFF)

    def write(self, uc, access, address, size, value, _):
        if not self.active:
            return
        stack = self.stack - 12 <= address and address + size <= self.stack + 4
        planes = self.kind == "planes" and self.data + PLANE_OFFSET <= address and address + size <= self.data + PLANE_OFFSET + 16
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
            stack = self.reg("ss") * 16 + self.reg("sp")
            ip, cs = struct.unpack("<HH", uc.mem_read(stack, 4))
            caller = (cs * 16 + ip) - self.base
            need(any(lo < caller <= lo + length for lo, length in ENTRIES.values()),
                 "foreign service must return into an owner")
            self.events.append((SERVICES[rva],))
            # Exercise caller-clobbered registers; leave the library's callee
            # saves, IF and DF intact. These replies are explicit model inputs.
            for name in ("ax", "cx", "dx", "es"):
                self.set(name, self.seed ^ (0x1234 + len(self.events) * 0x101))
            self.u.reg_write(UC_X86_REG_EFLAGS, self.u.reg_read(UC_X86_REG_EFLAGS) ^ 0xC5)
            self.set("sp", self.reg("sp") + 4)
            self.set("cs", cs)
            self.set("ip", ip)
            return
        allowed = [ENTRIES[self.kind]]
        if self.kind == "exit_dos":
            allowed.append(ENTRIES["exit"])
        need(any(lo <= rva < lo + length for lo, length in allowed)
             and self.instructions.get(rva) == size, "execution outside owned instructions/services")
        self.covered.update(range(rva, rva + size))

    def run(self, kind, seed=0x1357, sp=0x80, flags=0x202):
        self.kind, self.seed = kind, seed
        self.events, self.stores, self.returned = [], [], False
        self.active = False
        self.u.mem_write(self.data + PLANE_OFFSET - 4, b"\xA5" * 24)
        self.stack = 0x70000 + sp
        self.u.mem_write(self.stack - 16, b"\xCC" * 24)
        self.u.mem_write(self.stack, struct.pack("<HH", 0, 0x6000))
        initial = {n: (seed + i * 0x231) & 0xFFFF for i, n in enumerate(REGISTERS)}
        initial.update(cs=(self.base // 16) + 0xBEB, ds=self.ds, ss=0x7000, sp=sp,
                       ip=ENTRIES[kind][0] - 0xBEB0)
        for name, value in initial.items():
            self.set(name, value)
        self.u.reg_write(UC_X86_REG_EFLAGS, flags)
        self.active = True
        try:
            self.u.emu_start(self.base + ENTRIES[kind][0], 0x100000, count=300)
        except UcError as exc:
            raise ValueError("OP exit contract: guest fault") from exc
        finally:
            self.active = False
        need(self.returned and self.reg("sp") == sp + 4, "far return and stack cleanup")
        need(self.events == specification(kind), "service/port sequence")
        for name in ("bx", "si", "di", "bp", "ds", "ss"):
            need(self.reg(name) == initial[name], "callee save: " + name)
        need(self.u.reg_read(UC_X86_REG_EFLAGS) & 0x600 == flags & 0x600, "IF/DF preservation")
        expected = PLANE_BYTES if kind == "planes" else b"\xA5" * 16
        need(bytes(self.u.mem_read(self.data + PLANE_OFFSET - 4, 24)) == b"\xA5" * 4 + expected + b"\xA5" * 4,
             "four plane pointers and adjacent state")
        expected_stores = [(PLANE_OFFSET + i * 4, 4, value) for i, value in
                           enumerate((0xA8000000, 0xB0000000, 0xB8000000, 0xE0000000))] if kind == "planes" else []
        need(self.stores == expected_stores, "ordered dword stores")
        return tuple(self.events), expected


def verify(target, candidate):
    cases = 0
    for load in (0x1000, 0x3000):
        machines = [Machine(image, load) for image in (target, candidate)]
        for kind in ENTRIES:
            for seed in (0, 1, 0x1357, 0x7FFF, 0x8000, 0xFFFF):
                for sp in (0x40, 0xFFF0):
                    for flags in (2, 0x202, 0x402, 0x602):
                        need(machines[0].run(kind, seed, sp, flags) == machines[1].run(kind, seed, sp, flags),
                             "target/candidate observables")
                        cases += 1
        expected = {i for start, size in ENTRIES.values() for i in range(start, start + size)}
        need(all(m.covered == expected for m in machines), "all 133 owner bytes must execute")
    return dict(cases_per_image=cases, images=2, load_segments=[0x1000, 0x3000],
                executed_owner_bytes=133, functions=3, plane_pointer_bytes=16,
                scope="actual instructions, bounded foreign library replies and OUT trace; physical hardware/DOS not established")


def negative_controls(image):
    rejected = []
    for name, kind, offset, old, new in (
        ("DOS service target", "exit_dos", 9, "2e1a", "2f1a"),
        ("near/far return", "exit_dos", 24, "cb", "c3"),
        ("plane segment", "planes", 11, "a8", "a0"),
        ("plane ownership", "planes", 6, "fa19", "f819"),
        ("plane store width", "planes", 3, "66", "90"),
        ("page order", "exit", 12, "01", "00"),
        ("port address", "exit", 9, "a600", "a400"),
        ("cleanup order", "exit", 41, "7823", "7626"),
        ("callee save", "exit", 65, "5d", "90"),
    ):
        raw = bytearray(image.program_image)
        at = ENTRIES[kind][0] + offset
        before, after = bytes.fromhex(old), bytes.fromhex(new)
        need(raw[at:at + len(before)] == before and len(before) == len(after), "mutation anchor: " + name)
        raw[at:at + len(before)] = after
        try:
            Machine(replace(image, program_image=bytes(raw)), 0x1000).run(kind)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("OP exit contract: mutation survived: " + name)
    return dict(count=len(rejected), rejected=rejected)
