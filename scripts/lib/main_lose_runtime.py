"""Bounded native execution of MAIN lose update, particles and defeat banners."""

import struct
from dataclasses import replace
from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import (
    UC_X86_REG_AX,
    UC_X86_REG_BX,
    UC_X86_REG_CX,
    UC_X86_REG_DX,
    UC_X86_REG_SI,
    UC_X86_REG_DI,
    UC_X86_REG_BP,
    UC_X86_REG_SP,
    UC_X86_REG_CS,
    UC_X86_REG_DS,
    UC_X86_REG_ES,
    UC_X86_REG_SS,
    UC_X86_REG_IP,
    UC_X86_REG_EFLAGS,
)

LOAD, DS, SS, RES, SP = 0x1000, 0x2D56, 0x8000, 0x6000, 0xFF00
SCOPES = ((0xC0D8, 0xC248), (0xC2F9, 0xC370))
STUBS = {
    0xA2D0: ("screen_x", 4, 4, True),
    0xEC3A: ("sound", 2, 2, True),
    0x1C7E: ("palette", 0, 0, True),
    0xBA12: ("rounds_won", 2, 2, False),
    0xEA5D: ("polar", 6, 0, True),
    0xF100: ("sprite", 6, 6, True),
    0x26CA: ("super", 6, 6, True),
}


def need(ok, message):
    if not ok:
        raise ValueError("lose runtime: " + message)


def signed(word):
    return (word + 32768) % 65536 - 32768


def word(value):
    return struct.pack("<H", value & 65535)


def execute(image, kind, seed):
    """Foreign graphics/audio/math calls are fixtures, never device emulation."""
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for r in image.relocations:
        struct.pack_into(
            "<H",
            program,
            r.linear,
            (struct.unpack_from("<H", program, r.linear)[0] + LOAD) & 65535,
        )
    u.mem_write(LOAD * 16, bytes(program))
    for reg, value in (
        (UC_X86_REG_AX, 0xA55A),
        (UC_X86_REG_BX, 0x5AA5),
        (UC_X86_REG_CX, 0x1234),
        (UC_X86_REG_DX, 0x5678),
        (UC_X86_REG_SI, 0x1357),
        (UC_X86_REG_DI, 0x2468),
        (UC_X86_REG_BP, 0xBEEF),
        (UC_X86_REG_SP, SP),
        (UC_X86_REG_CS, LOAD + 0x96E),
        (UC_X86_REG_DS, DS),
        (UC_X86_REG_ES, 0x4444),
        (UC_X86_REG_SS, SS),
        (UC_X86_REG_EFLAGS, 0x202),
    ):
        u.reg_write(reg, value)
    pid, n = seed & 1, seed // 2
    time = n & 255
    pose = n + n // 256
    player = 0x65A6 + pid * 128
    other_player = 0x65A6 + (1 - pid) * 128
    data = bytearray(u.mem_read(DS * 16, 65536))
    data[0x65A6:0x66A6] = bytes((i * 37 + 11) & 255 for i in range(256))
    data[0x6590] = pid
    data[0x1D90:0x1D94] = struct.pack("<HH", 0, RES)
    data[0x316:0x596] = b"".join(word(i * 131 - 0x4000) for i in range(320))
    data[player : player + 4] = b"".join(
        word(v)
        for v in (
            (-32768, -1025, -16, -1, 0, 15, 1024, 32767)[pose % 8],
            (32767, -32768, -17, 0)[pose % 4],
        )
    )
    data[player + 0x1F] = n & 255
    data[other_player + 0x6C] = 255 if n & 1 else 2
    for at, value in (
        (0x38DE, -123),
        (0x38E0, 234),
        (0x38E2, (0, 32767, -6, -32768)[n % 4]),
        (0x6596, (n * 1031) & 65535),
        (0x659C, -6),
        (0x659E, 6),
    ):
        data[at : at + 2] = word(value)
    data[0x38DD] = pid
    u.mem_write(DS * 16, bytes(data))
    u.mem_write(RES * 16, bytes([0xA7]) * 256)
    resident = bytearray(u.mem_read(RES * 16, 256))
    start, args = {
        "update": (0xC0D8, (player,)),
        "particle": (0xC1E6, (0xA500 | ((n * 37) & 255), 0x5A00 | (n & 255))),
        "banner": (0xC2F9, ()),
    }[kind]
    u.reg_write(UC_X86_REG_IP, start - 0x96E0)
    u.mem_write(SS * 16 + SP, word(0x200) + b"".join(word(v) for v in args))
    initial = bytes(u.mem_read(0, 0x100000))
    expected = bytearray(data)
    expected_calls = []

    def read(at):
        return struct.unpack_from("<H", data, at)[0]

    def set_word(at, value):
        expected[at : at + 2] = word(value)

    def call(name, *values):
        expected_calls.append((name, tuple(v & 65535 for v in values)))

    def polar(center, radius, component):
        return (signed(center) + ((signed(radius) * signed(component)) >> 8)) & 65535

    if kind == "update":
        if time == 48:
            call("screen_x", pid, read(player))
            left = (
                signed(read(player)) // 16
                + (320 if pid else 0)
                + signed(read(0x659C + pid * 2))
                + 16
            )
            set_word(0x38DE, left - 24)
            set_word(0x38E0, signed(read(player + 2)) // 16 - 8)
            expected[0x38DC] = 1
            call("sound", 14)
            expected[0x658B + 1 - pid] = 1
            set_word(0x38E2, 0)
        else:
            set_word(0x38E2, read(0x38E2) + 9)
        set_word(0x659C + pid * 2, 6 if (n & 3) < 2 else -6)
        expected[0x6599] = 2
        expected[player + 0x1F] = (n - 1) & 255
        if time == 1:
            for at in (0x38DE, 0x38E0, 0x38E2, 0x659C + pid * 2):
                set_word(at, 0)
            expected[player + 0x1F] = 255
            set_word(0x2D4, 100)
            expected[0x38DC] = 2
            expected[other_player + 0x6C] = (data[other_player + 0x6C] + 1) & 255
            resident[0x17] = 1 - pid
            set_word(0x6596, 0)
            call("palette")
            call("rounds_won", 1 - pid)
        else:
            set_word(0x2D4, 100 + (read(0x6596) & 1) * 30)
            call("palette")
    elif kind == "particle":
        ax, ay = args[1] & 255, args[0] & 255
        c1, c2 = read(0x396 + ax * 2), read(0x316 + ay * 2)
        call("polar", read(0x38DE), read(0x38E2), c1)
        call("polar", read(0x38E0), read(0x38E2), c2)
        left = polar(read(0x38DE), read(0x38E2), c1) + signed(read(0x659C + pid * 2))
        top = polar(read(0x38E0), read(0x38E2), c2)
        call("sprite", 0x34B4, top, left)
    else:
        left = pid * 320 + 96
        phase = read(0x6596) & 31
        top = 32 + phase if phase < 16 else 64 - phase
        call("super", 18, 40, left)
        call("super", 19, 40, left + 64)
        call("super", 20, top, (1 - pid) * 320 + 96)
        call("super", 21, top, (1 - pid) * 320 + 160)

    calls, writes, visited = [], [], set()
    stopped = False

    def hook(uc, address, size, unused):
        nonlocal stopped
        if address == (LOAD + 0x96E) * 16 + 0x200:
            stopped = True
            uc.emu_stop()
            return
        at = address - LOAD * 16
        if any(lo <= at < hi for lo, hi in SCOPES):
            visited.update(range(at, at + size))
            return
        need(at in STUBS, "unreviewed execution " + hex(at) + " after " + str(calls))
        name, arg_bytes, pop, far = STUBS[at]
        frame = 4 if far else 2
        sp = uc.reg_read(UC_X86_REG_SP)
        stack = SS * 16 + sp
        values = (
            struct.unpack(
                "<" + "H" * (arg_bytes // 2), uc.mem_read(stack + frame, arg_bytes)
            )
            if arg_bytes
            else ()
        )
        calls.append((name, values))
        result = 0xA55A
        if name == "screen_x":
            p, x = values
            result = (
                signed(x) // 16 + (320 if p else 0) + signed(read(0x659C + 2 * p)) + 16
            )
        elif name == "polar":
            result = polar(*values)
        uc.reg_write(UC_X86_REG_AX, result & 65535)
        for reg, value in (
            (UC_X86_REG_BX, 0xABCD),
            (UC_X86_REG_CX, 0xDCBA),
            (UC_X86_REG_DX, 0x9182),
        ):
            uc.reg_write(reg, value)
        ip = struct.unpack("<H", uc.mem_read(stack, 2))[0]
        cs = (
            struct.unpack("<H", uc.mem_read(stack + 2, 2))[0]
            if far
            else uc.reg_read(UC_X86_REG_CS)
        )
        uc.reg_write(UC_X86_REG_SP, sp + frame + pop)
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    def write(uc, access, address, size, value, unused):
        need(
            (SS * 16 + SP - 128 <= address and address + size <= SS * 16 + SP + 6)
            or (DS * 16 <= address and address + size <= DS * 16 + 65536)
            or (RES * 16 <= address and address + size <= RES * 16 + 256),
            "write bounds",
        )
        if not SS * 16 <= address < (SS + 0x1000) * 16:
            writes.append((address, size, value))

    u.hook_add(UC_HOOK_CODE, hook)
    u.hook_add(UC_HOOK_MEM_WRITE, write)
    u.emu_start(LOAD * 16 + start, 0, count=1000)
    need(stopped, "instruction budget")
    need(calls == expected_calls, "foreign call sequence/arguments")
    for reg, value in (
        (UC_X86_REG_SI, 0x1357),
        (UC_X86_REG_DI, 0x2468),
        (UC_X86_REG_BP, 0xBEEF),
        (UC_X86_REG_SP, SP + 2 + len(args) * 2),
        (UC_X86_REG_DS, DS),
        (UC_X86_REG_SS, SS),
    ):
        need(u.reg_read(reg) == value, "callee-save/stack contract")
    wanted = bytearray(initial)
    wanted[DS * 16 : DS * 16 + 65536] = expected
    wanted[RES * 16 : RES * 16 + 256] = resident
    actual = bytes(u.mem_read(0, 0x100000))
    stack_start, stack_end = SS * 16 + SP - 128, SS * 16 + SP + 6
    need(
        actual[:stack_start] == wanted[:stack_start]
        and actual[stack_end:] == wanted[stack_end:],
        "complete non-stack memory contract",
    )
    return dict(calls=calls, writes=writes), visited


def compare(target, candidate):
    visited = set()
    counts = {}
    for kind, count in (("update", 512), ("particle", 512), ("banner", 128)):
        seeds = list(range(count))
        if kind == "update":
            seeds += [96 + pid + 512 * pose for pose in range(1, 8) for pid in (0, 1)]
        for seed in seeds:
            a, seen = execute(target, kind, seed)
            b, other = execute(candidate, kind, seed)
            need(a == b and seen == other, "target/candidate disagreement")
            visited |= seen
        counts[kind] = len(seeds)
    need(len(visited) == 487, "complete authored instruction-byte coverage")
    return dict(
        cases=sum(counts.values()),
        by_function=counts,
        code_bytes_executed=len(visited),
        equal=True,
        scope="synthetic player states; complete non-stack memory, ordered writes and call/ABI contracts; foreign math/graphics/audio stubs; renderer and devices not executed",
    )


def negative_controls(image):
    rejected = []
    for name, lo, hi, old, new, kind, seed in (
        ("timer increment", 0xC0D8, 0xC1E6, "fe4c1f", "fe441f", "update", 2),
        ("explode flag", 0xC0D8, 0xC1E6, "c606dc3801", "c606dc3802", "update", 96),
        ("particle sprite", 0xC1E6, 0xC248, "68b434", "68b534", "particle", 0),
        ("banner phase mask", 0xC2F9, 0xC370, "251f00", "250f00", "banner", 6),
    ):
        raw = bytearray(image.program_image)
        before, after = bytes.fromhex(old), bytes.fromhex(new)
        need(raw[lo:hi].count(before) == 1, "mutation site: " + name)
        at = raw.index(before, lo, hi)
        raw[at : at + len(before)] = after
        try:
            execute(replace(image, program_image=bytes(raw)), kind, seed)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("lose runtime: semantic mutation survived: " + name)
    return dict(rejected=rejected, count=len(rejected))
