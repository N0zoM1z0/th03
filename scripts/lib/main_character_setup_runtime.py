"""Independent memory, argument and callback contracts for MAIN character setup."""

from pathlib import Path
from dataclasses import replace
import hashlib
import json
import struct

from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import (
    UC_X86_REG_AX, UC_X86_REG_BX, UC_X86_REG_CX, UC_X86_REG_DX,
    UC_X86_REG_SI, UC_X86_REG_DI, UC_X86_REG_BP, UC_X86_REG_SP,
    UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS,
    UC_X86_REG_IP, UC_X86_REG_EFLAGS,
)

CONTRACT_PATH = Path(__file__).with_name("main_character_setup_contract.json")
C = json.loads(CONTRACT_PATH.read_text())
START, END = 0xA44C, 0xB37C
PRIMITIVES = ((0xA3FA, 18), (0xA40C, 17), (0xA41E, 26), (0xA438, 19))
SS, SP, RETURN_IP = 0x8000, 0xF000, 0x100
PALETTE, SNAPSHOT, TEMPLATE = 0x11BA, 0x1D94, 0x640
DATA = bytes((i * 37 + 11) & 255 for i in range(65536))


def need(value, message):
    if not value:
        raise ValueError("character setup runtime: " + message)


def execute(image, case, load):
    kind = case["kind"]
    pid, seed = case.get("pid", 0), case.get("seed", 0)
    char = C["characters"][case.get("character", 0)]
    ds = load + 0x1D56
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for r in image.relocations:
        word = struct.unpack_from("<H", program, r.linear)[0]
        struct.pack_into("<H", program, r.linear, (word + load) & 65535)
    u.mem_write(load * 16, bytes(program))
    data = bytearray(DATA)
    data[TEMPLATE:TEMPLATE + 12] = b"00xy.bf2\0ABC"
    for p in (0, 1):
        data[C["players"] + p * 128 + 8] = case.get("paletted", 1) if p == pid else 0xA6
    data[PALETTE:PALETTE + 48] = bytes((i * 19 + seed * 71) & 255 for i in range(48))
    data[SNAPSHOT:SNAPSHOT + 48] = bytes((255 - i * 3 - seed) & 255 for i in range(48))
    data[C["primitives"]["randring_p"]] = case.get("index", 255)
    u.mem_write(ds * 16, bytes(data))
    fnseg, fnoff = SS, SP - (24 if kind == "callback" else 14)
    if kind == "pair":
        fnseg, fnoff = 0x6000 + seed * 0x100, case.get("offset", 0x200)
        u.mem_write(fnseg * 16 + fnoff, b"13xy.bf2\0XYZ")
    if kind == "callback":
        entry, pop, args = 0xA524 + case["character"] * 408, 2, [pid]
    elif kind == "resources":
        entry, pop, args = 0xA4C3, 4, [case["resource"] & 65535, pid]
    elif kind == "pair":
        entry, pop, args = START, 6, [fnoff, fnseg, case["slot"] & 65535]
    elif kind == "finalize":
        entry, pop, args = 0xA4A1, 0, []
    elif kind in ("fill", "get", "mask", "reset"):
        entry = PRIMITIVES[("fill", "get", "mask", "reset").index(kind)][0]
        pop, args = (2, [case["mask"]]) if kind == "mask" else (0, [])
    else:
        raise ValueError("unknown character runtime case")
    registers = ((UC_X86_REG_SI, 0x1357), (UC_X86_REG_DI, 0x2468),
                 (UC_X86_REG_BP, 0xBEEF), (UC_X86_REG_DS, ds), (UC_X86_REG_SS, SS))
    for reg, value in registers + ((UC_X86_REG_AX, 0xA55A), (UC_X86_REG_BX, 0x5AA5),
                                  (UC_X86_REG_CX, 0x1234), (UC_X86_REG_DX, 0x5678),
                                  (UC_X86_REG_ES, 0x4444), (UC_X86_REG_CS, load + 0x96E)):
        u.reg_write(reg, value)
    u.reg_write(UC_X86_REG_EFLAGS, 0x202 | (seed & 1))
    u.mem_write(SS * 16 + SP, struct.pack("<" + "H" * (1 + len(args)), RETURN_IP, *args))
    u.reg_write(UC_X86_REG_SP, SP)
    u.reg_write(UC_X86_REG_IP, entry - 0x96E0)
    expected = bytearray(u.mem_read(0, 0x100000))
    events, actual_events, visited, primitive_visited = [], [], set(), set()
    random_calls, expected_ax = 0, None
    loaded_palette = bytes((i * 29 + 101 + seed * 41) & 255 for i in range(48))

    def write_abs(address, raw):
        expected[address:address + len(raw)] = raw
        if not SS * 16 <= address < 0x90000:
            events.append(("store", address, len(raw), int.from_bytes(raw, "little")))

    def write(offset, size, value):
        write_abs(ds * 16 + offset, (value & ((1 << (size * 8)) - 1)).to_bytes(size, "little"))

    def far_pointer(offset, pair):
        segment, address = pair
        # Native pointer stores publish SEG before OFFSET; preserve that literal order.
        write(offset + 2, 2, (segment + load) & 65535)
        write(offset, 2, address)

    def resource_name(resource):
        value = ((resource - (case.get("paletted", 1) & 1) + 32768) & 65535) - 32768
        fn = bytearray(data[TEMPLATE:TEMPLATE + 12])
        if value >= 10:
            fn[0] = (fn[0] + value // 10) & 255
            value %= 10
        fn[1] = (fn[1] + value) & 255
        return fn

    def pair_plan(slot, filename):
        fn = bytearray(filename)
        events.append(("bfnt", fnseg, fnoff, bytes(fn)))
        for i, v in ((2, ord('e')), (3, ord('x')), (5, ord('m')), (6, ord('r')), (7, ord('s'))):
            fn[i] = v
            write_abs(fnseg * 16 + fnoff + i, bytes([v]))
        events.append(("mrs", slot & 65535, fnseg, fnoff, bytes(fn)))
        for i, v in ((2, ord('b')), (3, ord('m'))):
            fn[i] = v
            write_abs(fnseg * 16 + fnoff + i, bytes([v]))
        events.append(("mrs", (slot + 2) & 65535, fnseg, fnoff, bytes(fn)))

    def finalize_plan():
        events.extend((("flip", 1), ("flip", 3), ("respal",), ("palette",)))
        expected[ds * 16 + PALETTE:ds * 16 + PALETTE + 48] = loaded_palette
        for i in range(0, 48, 4):
            write_abs(ds * 16 + SNAPSHOT + i, loaded_palette[i:i + 4])

    if kind in ("callback", "resources"):
        pair_plan(pid, resource_name(char["resource"] if kind == "callback" else case["resource"]))
    elif kind == "pair":
        pair_plan(case["slot"], b"13xy.bf2\0XYZ")
    if kind == "callback":
        for role, (offset, stride) in C["fields"].items():
            far_pointer(offset + pid * stride, char["functions"][role])
        player = C["players"] + pid * 128
        write(player + 0x66, 2, char["functions"]["hyper"][1])
        write(player + 0x64, 2, C["standby"][1])
        if pid:
            finalize_plan()
        for offset, function in zip(C["background_fields"], C["background_functions"][str(char["chain"])]):
            far_pointer(offset, function)
        events.append(("boss", char["name"], pid))
    elif kind == "finalize":
        finalize_plan()
    elif kind == "fill":
        for i in range(256):
            events.append(("random", i))
            write(C["primitives"]["randring"] + 255 - i, 1, (i * 113 + seed * 77) & 255)
    elif kind in ("get", "mask"):
        index = data[C["primitives"]["randring_p"]]
        write(C["primitives"]["randring_p"], 1, (index + 1) & 255)
        address = ds * 16 + C["primitives"]["randring"] + index
        # At index255 the high byte aliases the already incremented index itself.
        expected_ax = int.from_bytes(expected[address:address + 2], "little")
        if kind == "mask":
            expected_ax &= case["mask"]
    elif kind == "reset":
        for i in range(1656):
            write(C["primitives"]["collmap"] + i * 4, 4, 0)
        expected_ax = 0

    services = {s * 16 + o: (name, s, o) for name, (s, o) in C["services"].items()}
    for character in C["characters"]:
        s, o = character["functions"]["boss_init"]
        services[s * 16 + o] = ("boss:" + character["name"], s, o)

    def code(uc, address, size, unused):
        nonlocal random_calls
        relative = address - load * 16
        if relative == 0x96E0 + RETURN_IP:
            uc.emu_stop()
            return
        if relative in services:
            name, segment, offset = services[relative]
            need((uc.reg_read(UC_X86_REG_CS), uc.reg_read(UC_X86_REG_IP)) == (load + segment, offset),
                 "real foreign far frame")
            stack = uc.reg_read(UC_X86_REG_SP)
            ip, cs = struct.unpack("<HH", uc.mem_read(SS * 16 + stack, 4))
            word = lambda off: int.from_bytes(uc.mem_read(SS * 16 + stack + off, 2), "little")
            count = 0
            if name in ("bfnt", "mrs"):
                off, seg = word(4), word(6)
                fn = bytes(uc.mem_read(seg * 16 + off, 12))
                if name == "bfnt":
                    actual_events.append((name, seg, off, fn)); count = 4
                else:
                    actual_events.append((name, word(8), seg, off, fn)); count = 6
            elif name == "flip":
                actual_events.append((name, word(4))); count = 2
            elif name.startswith("boss:"):
                actual_events.append(("boss", name.split(":")[1], word(4))); count = 2
            elif name == "respal":
                actual_events.append((name,))
                uc.mem_write(ds * 16 + PALETTE, loaded_palette)
            elif name == "palette":
                actual_events.append((name,))
                need(bytes(uc.mem_read(ds * 16 + PALETTE, 48)) == loaded_palette,
                     "palette output must follow resident palette load")
            elif name == "random":
                actual_events.append((name, random_calls))
                random_calls += 1
            for reg, value in ((UC_X86_REG_AX, 0xBEEF), (UC_X86_REG_BX, 0x9234),
                               (UC_X86_REG_CX, 0x5678), (UC_X86_REG_DX, 0x9ABC), (UC_X86_REG_ES, 0x5555)):
                uc.reg_write(reg, value)
            if name == "random":
                uc.reg_write(UC_X86_REG_AX, ((random_calls - 1) * 113 + seed * 77) & 65535)
            uc.reg_write(UC_X86_REG_SP, stack + 4 + count)
            uc.reg_write(UC_X86_REG_CS, cs)
            uc.reg_write(UC_X86_REG_IP, ip)
            return
        if START <= relative < END:
            visited.update(range(relative, relative + size))
        elif any(start <= relative < start + span for start, span in PRIMITIVES):
            primitive_visited.update(range(relative, relative + size))
        else:
            need(0xA378 <= relative < 0xA38D, "execution left bounded owned entries")

    def store(uc, access, address, count, value, unused):
        if not SS * 16 <= address < 0x90000:
            actual_events.append(("store", address, count, value))

    hooks = [u.hook_add(UC_HOOK_CODE, code), u.hook_add(UC_HOOK_MEM_WRITE, store)]
    try:
        u.emu_start(load * 16 + entry, 0, count=10000)
        need((u.reg_read(UC_X86_REG_CS), u.reg_read(UC_X86_REG_IP)) == (load + 0x96E, RETURN_IP), "near return")
        need(u.reg_read(UC_X86_REG_SP) == SP + 2 + pop, "Pascal/cdecl stack cleanup")
        need(all(u.reg_read(reg) == value for reg, value in registers), "preserved SI/DI/BP/DS/SS")
        if expected_ax is not None:
            need(u.reg_read(UC_X86_REG_AX) == expected_ax, "unsigned word result")
        if kind == "reset":
            need(u.reg_read(UC_X86_REG_CX) == 0 and u.reg_read(UC_X86_REG_ES) == ds, "collision reset registers")
        need(u.reg_read(UC_X86_REG_EFLAGS) & 0x600 == 0x200, "DF0 and IF")
        actual = bytes(u.mem_read(0, 0x100000))
        need(actual[:SS * 16] == expected[:SS * 16] and actual[0x90000:] == expected[0x90000:],
             "complete non-stack memory")
        need(actual_events == events, "ordered arguments, filenames, callback stores and calls")
        return dict(visited=sorted(visited), primitives=sorted(primitive_visited), events=events)
    finally:
        for hook in hooks:
            u.hook_del(hook)


def compare(target, candidate):
    need(hashlib.sha256(target.program_image).hexdigest() == C["target_program_sha256"], "canonical target identity")
    cases = []
    for character in range(9):
        for pid in (0, 1):
            for palette in (0, 1, 2, 3, 128, 255):
                cases.append(dict(kind="callback", character=character, pid=pid, paletted=palette, seed=palette & 1))
    for pid in (0, 1):
        for resource in (-32768, -11, -1, 0, 1, 9, 10, 11, 17, 18, 99, 100, 32767):
            for palette in (0, 1, 2, 255):
                cases.append(dict(kind="resources", pid=pid, resource=resource, paletted=palette, seed=palette & 1))
    for slot in (0, 1, 2, 3, 7, 65535):
        for offset in (0x200, 0x440):
            cases.append(dict(kind="pair", slot=slot, offset=offset, seed=slot & 1))
    cases += [dict(kind="finalize", seed=s) for s in (0, 1)]
    cases += [dict(kind="fill", seed=s, index=i) for s, i in ((0, 0), (1, 255))]
    cases += [dict(kind="get", index=i) for i in range(256)]
    cases += [dict(kind="mask", index=i, mask=m) for i in (0, 1, 2, 127, 254, 255) for m in (0, 1, 0x1234, 65535)]
    cases += [dict(kind="reset", seed=s) for s in (0, 1)]
    visited, primitives = set(), set()
    for load in (0x1000, 0x2200):
        for case in cases:
            first = execute(target, case, load)
            need(first == execute(candidate, case, load), "target/candidate")
            visited.update(first["visited"]); primitives.update(first["primitives"])
    need(visited == set(range(START, END)), "all3888 character setup bytes executed")
    need(primitives == {i for start, size in PRIMITIVES for i in range(start, start + size)}, "all80 primitive instruction bytes executed")
    return dict(cases=len(cases) * 2, code_bytes_executed=len(visited), primitive_code_bytes_executed=len(primitives), equal=True,
                scope="all nine character selections, both valid PIDs and palette parities, signed resource boundaries/wrap, far mutable filenames and ordered file/palette/boss services; full non-stack memory and near ABI; existing RNG tail alias and collision reset; foreign services are bounded stubs, DF0 required")


def negative_controls(image):
    callback = dict(kind="callback", character=0, pid=0, paletted=1)
    resource = dict(kind="resources", pid=0, resource=17, paletted=3)
    pair = dict(kind="pair", slot=1, offset=0x200)
    rejected = []
    for name, offset, value, case in (
        ("short filename copy", 0xA4DA, 11, resource),
        ("palette parity", 0xA4E9, 2, resource),
        ("decimal divisor", 0xA4F8, 9, resource),
        ("image extension", 0xA463, 0x62, pair),
        ("second image slot", 0xA491, 1, pair),
        ("flip slot", 0xA4A5, 0, dict(kind="finalize")),
        ("far filename segment", 0xA495, 4, pair),
        ("player branch", 0xA534, 0x84, callback),
        ("callback segment", 0xA53B, 0xFF, callback),
        ("near hyper pointer", 0xA5D7, 0x2A, callback),
        ("background segment", 0xA691, 0x6F, callback),
        ("boss argument", 0xA6B1, 0x50, callback),
        ("Pascal cleanup", 0xA6BA, 4, callback),
        ("short random fill", 0xA3FC, 0xFE, dict(kind="fill", index=255)),
        ("index direction", 0xA417, 0x0E, dict(kind="get", index=255)),
        ("short collision clear", 0xA441, 0x77, dict(kind="reset")),
    ):
        program = bytearray(image.program_image)
        need(program[offset] != value, "control must change a byte: " + name)
        program[offset] = value
        try:
            execute(replace(image, program_image=bytes(program)), case, 0x1000)
        except (ValueError, UcError):
            rejected.append(name)
        else:
            raise ValueError("character setup mutation accepted: " + name)
    return dict(count=len(rejected), rejected=rejected)
