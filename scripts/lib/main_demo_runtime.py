"""Execute both real demo callbacks against independent memory/ABI contracts."""

from dataclasses import replace
import itertools
import struct

from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import (
    UC_X86_REG_AX, UC_X86_REG_BX, UC_X86_REG_CX, UC_X86_REG_DX,
    UC_X86_REG_SI, UC_X86_REG_DI, UC_X86_REG_BP, UC_X86_REG_SP,
    UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS,
    UC_X86_REG_IP, UC_X86_REG_EFLAGS,
)

START, NONE, END = 0x9AD6, 0x9B0F, 0x9B14
SS, SP = 0x8000, 0xFF00


def need(value, message):
    if not value:
        raise ValueError("demo runtime: " + message)


def execute(image, scenario, load, noop=False, calls=1):
    frame, midpoint, input_sp = scenario
    ds = load + 0x1D56
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from("<H", program, relocation.linear)[0]
        struct.pack_into("<H", program, relocation.linear, (old + load) & 65535)
    u.mem_write(load * 16, bytes(program))
    data = bytearray((i * 37 + 11) & 255 for i in range(65536))
    struct.pack_into("<H", data, 0x1186, frame)
    struct.pack_into("<H", data, 0x2660, 0xABCD)
    struct.pack_into("<H", data, 0x1A9A, input_sp)
    data[0x2663], data[0x65A0] = midpoint, 0xA7
    u.mem_write(ds * 16, bytes(data))
    registers = (
        (UC_X86_REG_AX, 0xA55A), (UC_X86_REG_BX, 0x5AA5),
        (UC_X86_REG_CX, 0x1234), (UC_X86_REG_DX, 0x5678),
        (UC_X86_REG_SI, 0x1357), (UC_X86_REG_DI, 0x2468),
        (UC_X86_REG_BP, 0xBEEF), (UC_X86_REG_CS, load + 0x96E),
        (UC_X86_REG_DS, ds), (UC_X86_REG_ES, 0x4444), (UC_X86_REG_SS, SS),
    )
    for reg, value in registers:
        u.reg_write(reg, value)
    u.reg_write(UC_X86_REG_EFLAGS, 0x202)
    initial = bytes(u.mem_read(0, 0x100000))
    expected = bytearray(initial)
    events, actual_events, visited = [], [], set()

    def write(offset, size, value):
        address = ds * 16 + offset
        expected[address:address + size] = value.to_bytes(size, "little")
        events.append((offset, size, value))

    for _ in range(calls):
        if not noop:
            if frame < 7000:
                frame += 1
                write(0x1186, 2, frame)
            elif frame == 7000:
                write(0x2660, 2, 0x1DC8)
            if midpoint:
                write(0x65A0, 1, 1)
            if input_sp:
                write(0x65A0, 1, 1)

    def hook(uc, address, size, unused):
        relative = address - load * 16
        if relative == 0x97E0:
            uc.emu_stop()
            return
        need((NONE if noop else START) <= relative < (END if noop else NONE),
             "execution left callback")
        visited.update(range(relative, relative + size))

    def store(uc, access, address, size, value, unused):
        if not SS * 16 <= address < (SS + 0x1000) * 16:
            actual_events.append((address - ds * 16, size, value))

    u.hook_add(UC_HOOK_CODE, hook)
    u.hook_add(UC_HOOK_MEM_WRITE, store)
    for _ in range(calls):
        u.mem_write(SS * 16 + SP, struct.pack("<H", 0x100))
        u.reg_write(UC_X86_REG_SP, SP)
        entry = (NONE if noop else START) - 0x96E0
        u.reg_write(UC_X86_REG_IP, entry)
        u.emu_start(load * 16 + (NONE if noop else START), 0, count=100)
        need(u.reg_read(UC_X86_REG_IP) == 0x100, "near return")
        need(u.reg_read(UC_X86_REG_SP) == SP + 2, "near stack cleanup")
        need(all(u.reg_read(reg) == value for reg, value in registers),
             "preserved registers and segments")
    actual = bytes(u.mem_read(0, 0x100000))
    stack_start, stack_end = SS * 16, (SS + 0x1000) * 16
    need(actual[:stack_start] == expected[:stack_start]
         and actual[stack_end:] == expected[stack_end:], "complete non-stack memory")
    need(actual_events == events, "ordered stores")
    return dict(events=events, visited=sorted(visited))


def compare(target, candidate):
    count, visited = 0, set()
    for load in (0x1000, 0x2200):
        scenarios = itertools.product(
            (0, 1, 6998, 6999, 7000, 7001, 65535),
            (0, 1, 255), (0, 1, 0x100, 0x8000, 65535),
        )
        for scenario in scenarios:
            first = execute(target, scenario, load)
            need(first == execute(candidate, scenario, load), "target/candidate")
            visited.update(first["visited"])
            count += 1
        for noop, calls in ((True, 1), (False, 2)):
            first = execute(target, (6999, 255, 0x8000), load, noop, calls)
            need(first == execute(candidate, (6999, 255, 0x8000), load, noop, calls),
                 "no-op and repeated transition")
            visited.update(first["visited"])
            count += 1
    need(visited == set(range(START, END)), "all 62 callback bytes executed")
    return dict(cases=count, code_bytes_executed=len(visited), equal=True,
                scope="real demo/no-op callbacks, unsigned frame boundaries, ordered duplicate exit stores, next-invocation transition, two loads and complete non-stack memory; no foreign stubs")


def negative_controls(image):
    rejected = []
    for name, offset, value, scenario, noop in (
        ("threshold", 0x9ADD, 0x59, (7000, 0, 0), False),
        ("counter direction", 0x9AE2, 0x0E, (1, 0, 0), False),
        ("finish callback", 0x9AF3, 0xC9, (7000, 0, 0), False),
        ("exit value", 0x9B00, 2, (1, 1, 0), False),
        ("input width", 0x9B01, 0x80, (1, 0, 0x100), False),
        ("no-op stack", 0x9B12, 0x90, (1, 0, 0), True),
    ):
        program = bytearray(image.program_image)
        need(program[offset] != value, "control must change a byte")
        program[offset] = value
        try:
            execute(replace(image, program_image=bytes(program)), scenario, 0x1000, noop)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("demo runtime mutation accepted: " + name)
    return dict(count=len(rejected), rejected=rejected)
