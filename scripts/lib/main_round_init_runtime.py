"""Independent bounded contracts for the actual 855-byte round initializer.

Stage setup and the 48 bytes of switch tables are not executed by this model.
Foreign resets, random generation and formation services are explicit fixtures.
"""

from dataclasses import replace
import struct

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

START, END, SS, SP, RES = 0x9EBF, 0xA216, 0x8000, 0xFF00, 0x6000
STUBS = {
    0xE313: ("object_counters", False),
    0xA3FA: ("randring", False),
    0x17384: ("bullets", True),
    0x14A76: ("reimu", True),
    0x153BB: ("mima", True),
    0x142D0: ("marisa", True),
    0x1B653: ("ellen", True),
    0x193BC: ("ellen_slots", True),
    0x1EEC: ("random", True),
    0x13D9C: ("formations", True),
}


def need(value, message):
    if not value:
        raise ValueError("round init runtime: " + message)


def execute(image, scenario, seed):
    rank, mode, round_id, credits = scenario
    stage = (0, 8, 9, 255)[seed % 4]
    load = 0x1000 if seed & 2 else 0x2200
    ds, resident_offset = load + 0x1D56, 0x200 if seed & 4 else 0
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for r in image.relocations:
        old = struct.unpack_from("<H", program, r.linear)[0]
        struct.pack_into("<H", program, r.linear, (old + load) & 65535)
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
        (UC_X86_REG_IP, START - 0x96E0),
        (UC_X86_REG_EFLAGS, 0x202),
    ):
        u.reg_write(reg, value)
    data = bytearray((i * 37 + seed * 11 + 7) & 255 for i in range(65536))
    data[0x1D90:0x1D94] = struct.pack("<HH", resident_offset, RES)
    data[0x3283] = round_id
    data[0x6598] = seed & 255
    data[0x1E3E] = (seed * 19) & 255
    data[0x2D56:0x2D58] = bytes([(seed * 13) & 255, (255 - seed) & 255])
    # The original only clamps the upper bound. Negative indices wrap through
    # 16-bit DGROUP addressing; these fixtures deliberately keep that behavior.
    difficulty = min(round_id - credits + 3, 5)
    table_offset = (0x90 + stage * 12 + difficulty * 2) & 65535
    table_value = (0, 1, 2, 32767, 65535)[seed % 5]
    struct.pack_into("<H", data, table_offset, table_value)
    u.mem_write(ds * 16, bytes(data))
    resident = bytearray((i * 17 + seed) & 255 for i in range(256))
    resident[0xB], resident[0x28], resident[0x33], resident[0x36] = (
        rank,
        mode,
        stage,
        credits,
    )
    u.mem_write(RES * 16 + resident_offset, bytes(resident))
    u.mem_write(SS * 16 + SP, struct.pack("<H", 0x100))
    initial = bytes(u.mem_read(0, 0x100000))
    expected = bytearray(initial)
    events = []

    def write(offset, size, value):
        value &= (1 << (size * 8)) - 1
        address = ds * 16 + offset
        expected[address : address + size] = value.to_bytes(size, "little")
        events.append(("write", address, size, value))

    def call(name):
        events.append(("call", name))

    for offset, size in (
        (0x1DCA, 2),
        (0x1DCC, 2),
        (0x8DF6, 1),
        (0x2662, 1),
        (0x2663, 1),
        (0x1FC0, 1),
    ):
        write(offset, size, 0)
    for name in ("object_counters", "randring", "bullets"):
        call(name)
    for n in range(64):
        write(0x3ED6 + n * 48, 1, 0)
    for n in range(16):
        write(0x292A + n * 32, 1, 0)
        write(0x2B2A + n * 32, 1, 0)
    for n in range(32):
        write(0x66A6 + n * 14, 1, 0)
    for name in ("reimu", "mima", "marisa", "ellen", "ellen_slots"):
        call(name)
    if mode == 1:
        safety = table_value
        if rank == 0:
            safety //= 3
        elif rank == 2:
            safety *= 2
        elif rank == 3:
            safety = safety * 3 + 500
        write(0x6694, 2, min(safety, 65535))
    speed, boss = data[0x6598], data[0x1E3E]
    gauges = [data[0x2D56], data[0x2D57]]
    if rank < 4:
        speed = (
            ((round_id * (16 if rank == 0 else 32) + (32 if rank == 2 else 0)) & 255)
            if rank != 3
            else 96
        )
        write(0x6598, 1, speed)
        write(0x68DC, 1, (0, 0, 8, 24)[rank])
        boss = (
            (stage // 2 if rank == 0 else stage)
            + round_id * (1 if rank == 0 else 2)
            + (0, 0, 2, 8)[rank]
        ) & 255
        write(0x1E3E, 1, boss)
        if mode != 1:
            for n in range(2):
                gauges[n] = (gauges[n] + (1, 2, 2, 4)[rank]) & 255
                write(0x2D56 + n, 1, gauges[n])
    if speed >= 128:
        write(0x6598, 1, 127)
    if boss > 16:
        write(0x1E3E, 1, 16)
    for n in range(2):
        if gauges[n] > 16:
            write(0x2D56 + n, 1, 16)
    for offset, size, value in (
        (0x63E, 1, 255),
        (0x38DC, 1, 0),
        (0x3282, 1, 1),
        (0x3ED4, 2, 5120),
        (0x65A5, 1, 0),
        (0x65A4, 1, 0),
        (0x65A3, 1, 0),
        (0x65A2, 1, 0),
    ):
        write(offset, size, value)
    random_index = 0
    for pid in range(2):
        base = 0x65A6 + pid * 128
        write(0x4AD6 + pid, 1, 0)
        for field, size, value in (
            (8, 1, resident[0xC + pid]),
            (0x15, 1, resident[0xE + pid]),
            (4, 1, 0),
            (5, 1, 0),
            (6, 1, 50),
            (4, 1, 0),
            (0xD, 1, 1),
            (7, 1, 10),
            (0x10, 1, 0),
            (0x11, 1, 0),
            (0x14, 1, 0),
            (0, 2, 0x900),
            (2, 2, 0x1500),
            (0x18, 2, 0),
            (0x22, 1, 1),
            (0x73, 1, 1),
        ):
            write(base + field, size, value)
        for n in range(64):
            call("random")
            number = (seed * 1103 + random_index * 7 + 0xA5A5) & 65535
            random_index += 1
            write(base + 0x24 + n, 1, (number % 4) * 64 + 63)
        for field, size, value in (
            (0x1C, 1, 0),
            (0x1D, 1, 2),
            (0x1F, 1, 0),
            (0x1E, 1, 0),
            (0x74, 2, 0),
            (0x76, 1, 0),
            (0x77, 1, 0),
            (0x78, 1, 0),
            (0x79, 1, 0),
        ):
            write(base + field, size, value)
        for offset, size in (
            (0x2D54 + pid, 1),
            (0x659C + pid * 2, 2),
            (0x658B + pid, 1),
            (0x798 + pid, 1),
        ):
            write(offset, size, 0)
    call("formations")
    actual_events, visited, random_calls = [], set(), 0
    stopped = False

    def hook(uc, address, size, unused):
        nonlocal stopped, random_calls
        if address == (load + 0x96E) * 16 + 0x100:
            stopped = True
            uc.emu_stop()
            return
        relative = address - load * 16
        if START <= relative < END:
            visited.update(range(relative, relative + size))
            return
        need(relative in STUBS, "unexpected foreign transfer")
        name, far = STUBS[relative]
        actual_events.append(("call", name))
        sp = uc.reg_read(UC_X86_REG_SP)
        frame = SS * 16 + sp
        ip = struct.unpack("<H", uc.mem_read(frame, 2))[0]
        cs = (
            struct.unpack("<H", uc.mem_read(frame + 2, 2))[0]
            if far
            else uc.reg_read(UC_X86_REG_CS)
        )
        ax = seed ^ 0x5678
        if name == "random":
            ax = (seed * 1103 + random_calls * 7 + 0xA5A5) & 65535
            random_calls += 1
        for reg, value in (
            (UC_X86_REG_AX, ax),
            (UC_X86_REG_BX, 0xBEEF),
            (UC_X86_REG_CX, 0x1234),
            (UC_X86_REG_DX, 0xABCD),
        ):
            uc.reg_write(reg, value)
        uc.reg_write(UC_X86_REG_SP, sp + (4 if far else 2))
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    def store(uc, access, address, size, value, unused):
        if SS * 16 + SP - 128 <= address and address + size <= SS * 16 + SP + 4:
            return
        need(not SS * 16 <= address < (SS + 0x1000) * 16, "stack write bounds")
        actual_events.append(("write", address, size, value))

    u.hook_add(UC_HOOK_CODE, hook)
    u.hook_add(UC_HOOK_MEM_WRITE, store)
    u.emu_start(load * 16 + START, 0, count=10000)
    need(stopped, "return or instruction budget")
    if actual_events != events:
        index = next(
            (
                n
                for n, pair in enumerate(zip(actual_events, events))
                if pair[0] != pair[1]
            ),
            min(len(actual_events), len(events)),
        )
        need(
            False,
            f"ordered stores/calls at {index}: actual={actual_events[index : index + 1]}, expected={events[index : index + 1]}",
        )
    need(random_calls == 128, "random ring count")
    actual = bytes(u.mem_read(0, 0x100000))
    low, high = SS * 16 + SP - 128, SS * 16 + SP + 4
    need(
        actual[:low] == expected[:low] and actual[high:] == expected[high:],
        "whole non-stack memory",
    )
    for reg, value in (
        (UC_X86_REG_SI, 0x1357),
        (UC_X86_REG_DI, 0x2468),
        (UC_X86_REG_BP, 0xBEEF),
        (UC_X86_REG_DS, ds),
        (UC_X86_REG_SS, SS),
        (UC_X86_REG_SP, SP + 2),
    ):
        need(u.reg_read(reg) == value, "near ABI")
    return dict(events=actual_events, visited=sorted(visited))


def compare(target, candidate):
    visited, count = set(), 0
    for rank in (0, 1, 2, 3, 255):
        for mode in (1, 0x7F, 0x80):
            for round_id in (0, 1, 4, 5, 8, 16, 31, 255):
                for credits in (0, 255):
                    scenario = rank, mode, round_id, credits
                    first, second = (
                        execute(target, scenario, count),
                        execute(candidate, scenario, count),
                    )
                    need(first == second, "target/candidate observations")
                    visited.update(first["visited"])
                    count += 1
    need(visited == set(range(START, END)), "complete initializer instruction coverage")
    return dict(
        cases=count,
        code_bytes_executed=len(visited),
        equal=True,
        scope="855-byte initializer only; two loads/resident offsets, rank/default and byte-wrap/clamp cases; foreign service stubs; stage setup and switch data not executed",
    )


def negative_controls(image):
    rejected = []
    for name, offset, value, scenario in (
        ("boss flag", 0x9EC9, 1, (0, 1, 0, 0)),
        ("effect stride", 0x9EF8, 49, (0, 1, 0, 0)),
        ("shot count", 0x9F33, 31, (0, 1, 0, 0)),
        ("easy divisor", 0x9FB1, 2, (0, 1, 0, 0)),
        ("invincibility", 0xA172, 49, (0, 1, 0, 0)),
        ("random mask", 0xA1AE, 1, (0, 1, 0, 0)),
    ):
        data = bytearray(image.program_image)
        need(data[offset] != value, "control must change a byte")
        data[offset] = value
        try:
            execute(replace(image, program_image=bytes(data)), scenario, 4)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("round init mutation accepted: " + name)
    return dict(rejected=rejected, count=len(rejected))
