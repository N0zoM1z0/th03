"""Independent complete-memory contracts for MAIN's four stage palette entries."""

from dataclasses import replace
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import (
    UC_X86_REG_AX, UC_X86_REG_BX, UC_X86_REG_CX, UC_X86_REG_DX,
    UC_X86_REG_SI, UC_X86_REG_DI, UC_X86_REG_BP, UC_X86_REG_SP,
    UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS,
    UC_X86_REG_IP, UC_X86_REG_EFLAGS,
)

# Direct target operands and independently mapped DGROUP, not candidate symbols.
ENTRIES = ((0xA378, 21), (0xA38E, 26), (0xA3A8, 41), (0xA3D2, 40))
PALETTE, SNAPSHOT, CHANGED = 0x11BA, 0x1D94, 0x65A1
PALETTE_SHOW = 0x1C7E
SS, SP, RETURN_CS, RETURN_IP = 0x8000, 0xF000, 0x7000, 0x100
DATA = bytes((i * 37 + 11) & 255 for i in range(65536))


def need(value, message):
    if not value:
        raise ValueError("stage palette runtime: " + message)


def execute(image, which, pid, channel, load, seed=0):
    start, size = ENTRIES[which]
    ds = load + 0x1D56
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for r in image.relocations:
        old = struct.unpack_from("<H", program, r.linear)[0]
        struct.pack_into("<H", program, r.linear, (old + load) & 65535)
    u.mem_write(load * 16, bytes(program))
    data = bytearray(DATA)
    data[PALETTE:PALETTE + 48] = bytes((i * 13 + seed * 67) & 255 for i in range(48))
    data[SNAPSHOT:SNAPSHOT + 48] = bytes((255 - i * 7 - seed * 31) & 255 for i in range(48))
    data[CHANGED] = 0xA7
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
    u.reg_write(UC_X86_REG_EFLAGS, 0x202 | (seed & 1))
    # Deliberately nonzero high bytes prove the arguments are byte views of words.
    args = [pid | ((pid ^ 0xA5) << 8), channel | ((channel ^ 0x5A) << 8)]
    arg_count = (0, 0, 1, 2)[which]
    u.mem_write(SS * 16 + SP, struct.pack("<" + "H" * (2 + arg_count),
                RETURN_IP, RETURN_CS, *args[:arg_count]))
    u.reg_write(UC_X86_REG_SP, SP)
    u.reg_write(UC_X86_REG_IP, start - 0x96E0)
    expected = bytearray(u.mem_read(0, 0x100000))
    events, actual_events, visited = [], [], set()

    def write(offset, raw):
        address = ds * 16 + offset
        expected[address:address + len(raw)] = raw
        events.append((offset, len(raw), int.from_bytes(raw, "little")))

    if which <= 1:
        source, dest = (PALETTE, SNAPSHOT) if which == 0 else (SNAPSHOT, PALETTE)
        for i in range(0, 48, 4):
            write(dest + i, bytes(data[source + i:source + i + 4]))
        if which == 1:
            events.append(("palette-show",))
    else:
        entry = 3 if pid else 0
        if which == 2:
            write(PALETTE + entry, bytes(data[SNAPSHOT + entry:SNAPSHOT + entry + 2]))
            write(PALETTE + entry + 2, bytes(data[SNAPSHOT + entry + 2:SNAPSHOT + entry + 3]))
        else:
            for i in range(3):
                write(PALETTE + entry + i, bytes([channel]))
        write(CHANGED, b"\1")

    def code(uc, address, instruction_size, unused):
        relative = address - load * 16
        if address == RETURN_CS * 16 + RETURN_IP:
            uc.emu_stop()
            return
        if relative == PALETTE_SHOW:
            need(which == 1, "unexpected foreign call")
            need(bytes(uc.mem_read(ds * 16 + PALETTE, 48)) == data[SNAPSHOT:SNAPSHOT + 48],
                 "show must observe the complete restored palette")
            actual_events.append(("palette-show",))
            stack = uc.reg_read(UC_X86_REG_SP)
            ip, cs = struct.unpack("<HH", uc.mem_read(SS * 16 + stack, 4))
            for reg, value in ((UC_X86_REG_AX, 0x1111), (UC_X86_REG_BX, 0x2222),
                               (UC_X86_REG_CX, 0x3333), (UC_X86_REG_DX, 0x4444),
                               (UC_X86_REG_ES, 0x5555)):
                uc.reg_write(reg, value)
            uc.reg_write(UC_X86_REG_SP, stack + 4)
            uc.reg_write(UC_X86_REG_CS, cs)
            uc.reg_write(UC_X86_REG_IP, ip)
            return
        need(start <= relative < start + size, "execution left the owned function")
        visited.update(range(relative, relative + instruction_size))

    def store(uc, access, address, count, value, unused):
        if not SS * 16 <= address < (SS + 0x1000) * 16:
            actual_events.append((address - ds * 16, count, value))

    hooks = [u.hook_add(UC_HOOK_CODE, code), u.hook_add(UC_HOOK_MEM_WRITE, store)]
    try:
        u.emu_start(load * 16 + start, 0, count=200)
        need((u.reg_read(UC_X86_REG_CS), u.reg_read(UC_X86_REG_IP)) == (RETURN_CS, RETURN_IP),
             "far return")
        need(u.reg_read(UC_X86_REG_SP) == SP + 4 + 2 * arg_count, "far Pascal/cdecl cleanup")
        preserved = (UC_X86_REG_SI, UC_X86_REG_DI, UC_X86_REG_BP, UC_X86_REG_DS, UC_X86_REG_SS)
        need(all(u.reg_read(reg) == value for reg, value in registers if reg in preserved),
             "preserved registers and segments")
        expected_es = (ds, 0x5555, ds, 0x4444)[which]
        need(u.reg_read(UC_X86_REG_ES) == expected_es, "ES ownership")
        need(u.reg_read(UC_X86_REG_EFLAGS) & 0x600 == 0x200, "DF0 and interrupt flag")
        actual = bytes(u.mem_read(0, 0x100000))
        stack_lo, stack_hi = SS * 16, (SS + 0x1000) * 16
        need(actual[:stack_lo] == expected[:stack_lo] and actual[stack_hi:] == expected[stack_hi:],
             "complete non-stack memory")
        need(actual_events == events, "ordered copy/stores/call")
        return dict(events=events, visited=sorted(visited))
    finally:
        for hook in hooks:
            u.hook_del(hook)


def compare(target, candidate):
    count, visited = 0, set()
    scenarios = [(which, 0, 0, seed) for which in (0, 1) for seed in (0, 1)]
    scenarios += [(2, pid, 0, pid & 1) for pid in range(256)]
    scenarios += [(3, pid, value, value & 1) for pid in (0, 1) for value in range(256)]
    scenarios += [(3, pid, value, 1) for pid in (2, 255) for value in (0, 127, 255)]
    for load in (0x1000, 0x2200):
        for which, pid, value, seed in scenarios:
            first = execute(target, which, pid, value, load, seed)
            need(first == execute(candidate, which, pid, value, load, seed), "target/candidate")
            visited.update(first["visited"])
            count += 1
    need(visited == {i for start, size in ENTRIES for i in range(start, start + size)},
         "all128 instruction bytes executed")
    return dict(cases=count, code_bytes_executed=len(visited), equal=True,
                scope="four far palette entries; all byte PIDs, all valid-PID channel bytes, dirty word carriers, two loads, complete non-stack memory, ordered stores and call-before-output contract; palette service is a bounded stub; DF0 is a precondition")


def negative_controls(image):
    rejected = []
    for name, offset, value, which, pid, channel in (
        ("short snapshot", 0xA385, 11, 0, 0, 0),
        ("shifted destination", 0xA37F, 0x95, 0, 0, 0),
        ("near return", 0xA38C, 0xC3, 0, 0, 0),
        ("wrong player entry", 0xA3BB, 6, 2, 255, 0),
        ("dirty value", 0xA3CA, 2, 2, 1, 0),
        ("Pascal cleanup", 0xA3CF, 4, 2, 1, 0),
        ("short RGB fill", 0xA3D7, 2, 3, 1, 127),
        ("wrong argument", 0xA3EA, 6, 3, 1, 127),
    ):
        program = bytearray(image.program_image)
        need(program[offset] != value, "control must change a byte")
        program[offset] = value
        try:
            execute(replace(image, program_image=bytes(program)), which, pid, channel, 0x1000)
        except (ValueError, UcError):
            rejected.append(name)
        else:
            raise ValueError("stage palette mutation accepted: " + name)
    return dict(count=len(rejected), rejected=rejected)
