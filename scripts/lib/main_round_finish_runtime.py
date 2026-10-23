"""Execute the complete next-round and score-commit bodies; foreign calls are stubs."""

from dataclasses import replace
import struct

from unicorn import (
    Uc,
    UC_ARCH_X86,
    UC_MODE_16,
    UC_HOOK_CODE,
    UC_HOOK_MEM_WRITE,
    UC_HOOK_INSN,
)
from unicorn.x86_const import (
    UC_X86_INS_OUT,
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

START, SCORE, END = 0xA21F, 0xA289, 0xA2D0
SS, SP, RES = 0x8000, 0xFF00, 0x6000
STUBS = {
    0xF5C: ("setcolor", True, 4),
    0xC40: ("setclip", True, 8),
    0xCD2: ("fill", True, 0),
    0xF86: ("grcg_off", True, 0),
    0x9EBF: ("round_setup", False, 0),
    0xEC2E: ("sound_reset", True, 0),
    0xB8F7: ("hud_wipe", True, 0),
    0xA38E: ("round_objects", True, 0),
    0xBAE0: ("hud_static", True, 0),
}


def need(ok, message):
    if not ok:
        raise ValueError("round finish runtime: " + message)


def execute(image, kind, seed):
    load = 0x1000 if seed & 2 else 0x2200
    ds = load + 0x1D56
    resident_offset = 0x200 if seed & 4 else 0
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from("<H", program, relocation.linear)[0]
        struct.pack_into("<H", program, relocation.linear, (old + load) & 0xFFFF)
    u.mem_write(load * 16, bytes(program))
    for reg, value in (
        (UC_X86_REG_AX, 0xA55A),
        (UC_X86_REG_BX, 0x5AA5),
        (UC_X86_REG_CX, 0x1234),
        (UC_X86_REG_DX, 0x5678),
        (UC_X86_REG_SI, 0x1357),
        (UC_X86_REG_DI, 0x2468),
        (UC_X86_REG_BP, 0xBEEF),
        (UC_X86_REG_SP, SP),
        (UC_X86_REG_CS, load + 0x96E),
        (UC_X86_REG_DS, ds),
        (UC_X86_REG_ES, 0x4444),
        (UC_X86_REG_SS, SS),
        (UC_X86_REG_EFLAGS, 0x202),
    ):
        u.reg_write(reg, value)
    pid, value = seed & 1, seed // 2
    u.mem_write(ds * 16 + 0x1D90, struct.pack("<HH", resident_offset, RES))
    u.mem_write(ds * 16 + 0x39C8, struct.pack("<HH", 0x120, 0x7000))
    u.mem_write(ds * 16 + 0x3283, bytes([seed & 255]))
    digits = bytes((value + i * 31) & 255 for i in range(16))
    u.mem_write(ds * 16 + 0x4B64, digits)
    u.mem_write(RES * 16 + resident_offset, bytes([0xA7]) * 256)
    start = START if kind == "next" else SCORE
    u.reg_write(UC_X86_REG_IP, start - 0x96E0)
    u.mem_write(SS * 16 + SP, struct.pack("<HH", 0x100, pid))
    initial = bytes(u.mem_read(0, 0x100000))
    expected = bytearray(initial)
    writes_expected = []

    def store(address, size, number):
        expected[address : address + size] = number.to_bytes(size, "little")
        writes_expected.append((address, size, number))

    if kind == "next":
        store(ds * 16 + 0x3283, 1, (seed + 1) & 255)
        store(ds * 16 + 0x660A, 2, 0x4110)
        store(ds * 16 + 0x668A, 2, 0x4110)
        expected_trace = [
            ("setcolor", (2, 0xC0)),
            ("setclip", (199, 639, 0, 0)),
            ("out", (0xA6, 1, 1)),
            ("fill", ()),
            ("out", (0xA6, 1, 0)),
            ("fill", ()),
            ("out", (0xA4, 1, 1)),
            ("grcg_off", ()),
            ("round_setup", ()),
            ("background", ()),
            ("sound_reset", ()),
            ("hud_wipe", ()),
            ("round_objects", ()),
            ("hud_static", ()),
        ]
    else:
        for digit in range(8):
            store(
                RES * 16 + resident_offset + 0x18 + pid * 8 + digit,
                1,
                digits[pid * 8 + digit],
            )
            store(RES * 16 + resident_offset + 0x18 + (1 - pid) * 8 + digit, 1, 0)
        expected_trace = []
    trace, writes, visited = [], [], set()
    stopped = False
    stubs = {load * 16 + offset: spec for offset, spec in STUBS.items()}
    stubs[0x70120] = ("background", True, 0)

    def hook(uc, address, size, unused):
        nonlocal stopped
        if address == (load + 0x96E) * 16 + 0x100:
            stopped = True
            uc.emu_stop()
            return
        relative = address - load * 16
        if start <= relative < (SCORE if kind == "next" else END):
            visited.update(range(relative, relative + size))
            return
        need(address in stubs and kind == "next", "foreign control transfer")
        name, far, pop = stubs[address]
        sp = uc.reg_read(UC_X86_REG_SP)
        frame = SS * 16 + sp
        offset = struct.unpack("<H", uc.mem_read(frame, 2))[0]
        segment = (
            struct.unpack("<H", uc.mem_read(frame + 2, 2))[0]
            if far
            else uc.reg_read(UC_X86_REG_CS)
        )
        argument_start = frame + (4 if far else 2)
        arguments = (
            struct.unpack("<" + "H" * (pop // 2), uc.mem_read(argument_start, pop))
            if pop
            else ()
        )
        trace.append((name, arguments))
        # Deliberately clobber volatile registers; no callee implementation or
        # physical graphics/audio behavior is inferred from these interfaces.
        for reg, result in (
            (UC_X86_REG_AX, seed ^ 0x4567),
            (UC_X86_REG_BX, 0x9ABC),
            (UC_X86_REG_CX, 0xDEF0),
            (UC_X86_REG_DX, 0x1357),
        ):
            uc.reg_write(reg, result & 65535)
        uc.reg_write(UC_X86_REG_SP, sp + (4 if far else 2) + pop)
        uc.reg_write(UC_X86_REG_CS, segment)
        uc.reg_write(UC_X86_REG_IP, offset)

    def output(uc, port, size, number, unused):
        trace.append(("out", (port, size, number)))

    def write(uc, access, address, size, number, unused):
        if SS * 16 + SP - 128 <= address and address + size <= SS * 16 + SP + 8:
            return
        need(not SS * 16 <= address < (SS + 0x1000) * 16, "stack write bounds")
        writes.append((address, size, number))

    u.hook_add(UC_HOOK_CODE, hook)
    u.hook_add(UC_HOOK_MEM_WRITE, write)
    u.hook_add(UC_HOOK_INSN, output, None, 1, 0, UC_X86_INS_OUT)
    u.emu_start((load + 0x96E) * 16 + start - 0x96E0, 0, count=2000)
    need(stopped, "return or instruction budget")
    need(trace == expected_trace, "ordered call/port contracts")
    need(writes == writes_expected, "ordered copy/clear/reset stores")
    actual = bytes(u.mem_read(0, 0x100000))
    low, high = SS * 16 + SP - 128, SS * 16 + SP + 8
    need(
        actual[:low] == expected[:low] and actual[high:] == expected[high:],
        "complete memory outside bounded stack window",
    )
    for reg, wanted in (
        (UC_X86_REG_SI, 0x1357),
        (UC_X86_REG_DI, 0x2468),
        (UC_X86_REG_BP, 0xBEEF),
        (UC_X86_REG_DS, ds),
        (UC_X86_REG_SS, SS),
        (UC_X86_REG_SP, SP + (2 if kind == "next" else 4)),
    ):
        need(u.reg_read(reg) == wanted, "near ABI/stack cleanup")
    return dict(
        trace=trace,
        writes=writes,
        visited=sorted(visited),
        final_es=u.reg_read(UC_X86_REG_ES),
    )


def compare(target, candidate):
    visited = set()
    for kind, cases in (("next", 256), ("score", 512)):
        for seed in range(cases):
            first, second = execute(target, kind, seed), execute(candidate, kind, seed)
            need(first == second, "target/candidate observations differ")
            visited.update(first["visited"])
    need(visited == set(range(START, END)), "complete 177-byte execution coverage")
    return dict(
        cases=768,
        by_function={"next": 256, "score": 512},
        code_bytes_executed=len(visited),
        equal=True,
        scope="two load segments, zero/nonzero resident offsets, both valid PIDs, all byte inputs/round wrap; foreign calls and port writes are interface observations",
    )


def negative_controls(image):
    rejected = []
    for name, offset, value, kind in (
        ("round decrement", 0xA25D, 0x0E, "next"),
        ("hyper entry", 0xA26B, 0x11, "next"),
        ("missing score digit", 0xA2C8, 7, "score"),
        ("opponent score not cleared", 0xA2C4, 1, "score"),
        ("Pascal cleanup", 0xA2CE, 4, "score"),
    ):
        program = bytearray(image.program_image)
        need(program[offset] != value, "negative control must change a byte")
        program[offset] = value
        try:
            execute(replace(image, program_image=bytes(program)), kind, 0)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("round finish mutation was accepted: " + name)
    return dict(rejected=rejected, count=len(rejected))
