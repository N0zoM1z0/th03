"""Execute the 177-byte near-this loss renderer against independent ring rules.

The existing particle helper is a bounded near-Pascal ABI stub. This validates
angle calls, clipping state and stack/register ownership, not raster hardware.
"""

from dataclasses import replace
import struct
import capstone
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.x86_const import *

START, SIZE, PARTICLE = 0xC248, 177, 0xC1E6
RADII = sorted(set(range(-512, 512)) | {-32768, -32767, -32766, -4097, -4096,
                                          4095, 4096, 32765, 32766, 32767})
REG = dict(ax=UC_X86_REG_AX, bx=UC_X86_REG_BX, cx=UC_X86_REG_CX, dx=UC_X86_REG_DX,
           si=UC_X86_REG_SI, di=UC_X86_REG_DI, bp=UC_X86_REG_BP, sp=UC_X86_REG_SP,
           cs=UC_X86_REG_CS, ds=UC_X86_REG_DS, ss=UC_X86_REG_SS, es=UC_X86_REG_ES,
           ip=UC_X86_REG_IP)


def need(value, message):
    if not value:
        raise ValueError("lose renderer contract: " + message)


def specification(radius):
    quarter = (-1 if radius < 0 else 1) * (abs(radius) // 4)
    calls = []
    for start, phase in ((quarter, 32), (-quarter, -32), (quarter, 0)):
        for index in range(16):
            angle = (start + index * 16) & 255
            calls.append((angle, (angle + phase) & 255))
    return calls


class Machine:
    def __init__(self, image, load):
        self.base = load * 16
        self.cs, self.ds = load + 0x96E, load + 0x1D56
        self.data = self.ds * 16
        self.u = Uc(UC_ARCH_X86, UC_MODE_16)
        self.u.mem_map(0, 0x100000)
        self.u.mem_write(self.base, image.relocated_program_image(load))
        decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
        self.instructions = {i.address: i.size for i in decoder.disasm(
            image.program_image[START:START + SIZE], START)}
        self.active = False
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_READ, self.read)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def reg(self, name):
        return self.u.reg_read(REG[name]) & 0xFFFF

    def set(self, name, value):
        self.u.reg_write(REG[name], value & 0xFFFF)

    def read(self, uc, access, address, size, value, _):
        if not self.active:
            return
        stack = self.top - 14 <= address and address + size <= self.top + 2
        data = ((self.data + 0x38E2 <= address and address + size <= self.data + 0x38E4)
                or (address == self.data + 0x6590 and size == 1))
        need(stack or data, "unexpected state/this read")

    def write(self, uc, access, address, size, value, _):
        if not self.active:
            return
        stack = self.top - 14 <= address and address + size <= self.top
        clip = self.data + 0x1D84 <= address and address + size <= self.data + 0x1D8B
        need(stack or clip, "write outside private stack and clip state")

    def code(self, uc, address, size, _):
        if address == self.cs * 16 + 0x7000:
            self.returned = True
            uc.emu_stop()
            return
        rva = address - self.base
        if rva == PARTICLE:
            need(self.reg("cs") == self.cs and self.reg("sp") == self.sp - 14,
                 "near helper argument/return width")
            ip, angle_y, angle_x = struct.unpack("<3H", uc.mem_read(self.top - 14, 6))
            event = (angle_x & 255, angle_y & 255)
            need(len(self.calls) < 48 and event == self.expected[len(self.calls)],
                 "ordered particle ring angles differ")
            self.calls.append(event)
            self.raw_calls.append((angle_x, angle_y))
            need(self.cs * 16 + ip - self.base in self.instructions, "helper return boundary")
            for name, value in (("ax", 0xA500), ("bx", 0xB600), ("cx", 0xC700),
                                ("dx", 0xD800), ("es", 0x9000)):
                self.set(name, value + len(self.calls))
            uc.reg_write(UC_X86_REG_EFLAGS, 0x203)
            self.set("sp", self.reg("sp") + 6)
            self.set("ip", ip)
            return
        need(rva in self.instructions, "unexpected instruction or foreign flow")
        self.seen.update(range(rva, rva + self.instructions[rva]))

    def run(self, radius, pid, seed=0):
        self.active = False
        self.expected = specification(radius)
        self.calls, self.raw_calls, self.seen = [], [], set()
        self.returned = False
        self.sp = 0xFE00 if seed & 1 else 0x80
        self.top = 0x70000 + self.sp
        self.u.mem_write(self.data + 0x38E2, struct.pack("<H", radius & 0xFFFF))
        self.u.mem_write(self.data + 0x6590, bytes([pid]))
        self.u.mem_write(self.data + 0x1D84, b"\x92" * 8)
        # This word is deliberately invalid as a player pointer: the method
        # consumes it but never reads it or the addressed object.
        self.u.mem_write(self.top, struct.pack("<2H", 0x7000, 0xFFFF if seed & 2 else 0))
        for name, value in (("ax", 0xA55A), ("bx", 0xB66B), ("cx", 0xC77C),
                            ("dx", 0xD88D), ("si", 0x2468), ("di", 0x369C),
                            ("bp", 0x1357), ("ss", 0x7000), ("ds", self.ds),
                            ("es", 0x9000), ("cs", self.cs), ("sp", self.sp),
                            ("ip", START - 0x96E0)):
            self.set(name, value)
        self.u.reg_write(UC_X86_REG_EFLAGS, 0x202)
        self.active = True
        try:
            self.u.emu_start(self.base + START, 0, count=5000)
        except UcError as error:
            raise ValueError("lose renderer contract: guest execution failed") from error
        finally:
            self.active = False
        need(self.returned and self.calls == self.expected, "incomplete renderer/particle sequence")
        need(self.reg("sp") == self.sp + 4, "near-this RET 2 cleanup differs")
        need(tuple(self.reg(r) for r in ("si", "di", "bp", "ss", "ds"))
             == (0x2468, 0x369C, 0x1357, 0x7000, self.ds), "callee-saved registers differ")
        clip = struct.pack("<HHHB", 0 if pid == 0 else 320, 319 if pid == 0 else 639, 24, 3) + b"\x92"
        actual = bytes(self.u.mem_read(self.data + 0x1D84, 8))
        need(actual == clip, "clip/size state differs")
        return dict(calls=self.calls, raw_word_carriers=self.raw_calls, clip=actual.hex()), self.seen


def compare(target, candidate):
    seen, count = set(), 0
    for load in (0x2000, 0x3000):
        a, b = Machine(target, load), Machine(candidate, load)
        for index, radius in enumerate(RADII):
            pid = (0, 1, 2, 255)[index % 4]
            expected, visited = a.run(radius, pid, index)
            actual, other = b.run(radius, pid, index)
            need(expected == actual and visited == other, "target/candidate disagreement")
            seen.update(visited)
            count += 1
    need(len(seen) == SIZE, "complete renderer instruction-byte coverage")
    return dict(equal=True, cases=count, radius_values=len(RADII), code_bytes_executed=len(seen),
                particle_calls_per_case=48, dos_loads=2, stack_depth_bytes=14,
                scope="signed16 radius, every byte start angle and division remainder, clip PID branches, near-this ABI; foreign particle/raster behavior remains bounded")


def negative_controls(image):
    rejected = []
    for name, old, new, radius, pid in (
        ("radius divisor", "bb0400", "bb0500", 127, 0),
        ("loop length", "83ff10", "83ff0f", 0, 0),
        ("ring phase", "0420", "041f", 0, 0),
        ("clip selector", "750e", "740e", 0, 0),
        ("near-this cleanup", "c20200", "c20400", 0, 0),
        ("callee save", "5f5ec9", "905ec9", 0, 0),
        ("particle helper", "e853ff", "e854ff", 0, 0),
        ("clip write ownership", "c706841d0000", "c706821d0000", 0, 0),
    ):
        before, after = bytes.fromhex(old), bytes.fromhex(new)
        raw = bytearray(image.program_image)
        at = raw.find(before, START, START + SIZE)
        need(at >= START and len(before) == len(after), "mutation site: " + name)
        raw[at:at + len(before)] = after
        try:
            Machine(replace(image, program_image=bytes(raw)), 0x2000).run(radius, pid)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("lose renderer contract: semantic mutation survived: " + name)
    return dict(count=len(rejected), rejected=rejected)
