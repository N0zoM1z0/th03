"""Execute the actual linked and canonical MAIN entry with bounded foreign calls."""

import struct
from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import (
    UC_X86_REG_AX,
    UC_X86_REG_BP,
    UC_X86_REG_BX,
    UC_X86_REG_CS,
    UC_X86_REG_CX,
    UC_X86_REG_DI,
    UC_X86_REG_DS,
    UC_X86_REG_DX,
    UC_X86_REG_EFLAGS,
    UC_X86_REG_ES,
    UC_X86_REG_IP,
    UC_X86_REG_SI,
    UC_X86_REG_SP,
    UC_X86_REG_SS,
)

ENTRY, END, LOAD, DS, SS, RES = 0x96E6, 0x9778, 0x1000, 0x2D56, 0x8000, 0x6000
STUBS = {
    0xECD0: ("init", True, 4),
    0xA346: ("cfg", False, 0),
    0xE922: ("sound_mode", True, 0),
    0x11B6: ("gaiji_backup", True, 0),
    0x11F6: ("gaiji_font", True, 4),
    0x9B14: ("stage", False, 0),
    0x1C7E: ("palette", True, 0),
    0x9778: ("round", False, 0),
    0xA21F: ("next_round", False, 0),
    0x13DF9: ("free_formations", True, 0),
    0xECB2: ("sound_stop", True, 2),
    0xB454: ("exec", True, 4),
}
REGS = (
    UC_X86_REG_AX,
    UC_X86_REG_BX,
    UC_X86_REG_CX,
    UC_X86_REG_DX,
    UC_X86_REG_SI,
    UC_X86_REG_DI,
    UC_X86_REG_BP,
    UC_X86_REG_SP,
    UC_X86_REG_DS,
    UC_X86_REG_ES,
    UC_X86_REG_SS,
    UC_X86_REG_CS,
    UC_X86_REG_IP,
    UC_X86_REG_EFLAGS,
)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def execute(image, scenario):
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for r in image.relocations:
        v = struct.unpack_from("<H", program, r.linear)[0]
        struct.pack_into("<H", program, r.linear, (v + LOAD) & 0xFFFF)
    u.mem_write(LOAD * 16, bytes(program))
    for reg, val in zip(
        REGS,
        (
            0xA55A,
            0x5AA5,
            0x1234,
            0x5678,
            0x1357,
            0x2468,
            0xBEEF,
            0xFF00,
            DS,
            0x4444,
            SS,
            LOAD + 0x96E,
            6,
            0x202,
        ),
    ):
        u.reg_write(reg, val)
    u.mem_write(SS * 16 + 0xFF00, struct.pack("<HH", 0x100, 0x7E00))
    u.mem_write(DS * 16 + 0x1D90, struct.pack("<HH", 0, RES))
    u.mem_write(RES * 16 + 0x15, bytes([scenario["bgm"]]))
    u.mem_write(RES * 16 + 0x33, bytes([scenario["story"]]))
    u.mem_write(RES * 16 + 0x10, struct.pack("<I", 0xDEADBEEF))
    u.mem_write(DS * 16 + 0x39C0, struct.pack("<HH", 0x100, 0x7100))
    u.mem_write(DS * 16 + 0x1A0D, b"\x7f")
    regions = ((DS * 16, 65536), (RES * 16, 256), (SS * 16 + 0xFE00, 260))
    initial = [bytes(u.mem_read(a, n)) for a, n in regions]
    trace, writes, visited = [], [], set()
    rounds = 0
    stopped = False
    stubs = {LOAD * 16 + a: spec for a, spec in STUBS.items()}
    stubs[0x71100] = ("background", True, 0)

    def read_word(address):
        return struct.unpack("<H", u.mem_read(address, 2))[0]

    def hook(uc, address, size, unused):
        nonlocal rounds, stopped
        if address == 0x7E100:
            stopped = True
            uc.emu_stop()
            return
        if LOAD * 16 + ENTRY <= address < LOAD * 16 + END:
            visited.update(range(address - LOAD * 16, address - LOAD * 16 + size))
            return
        need(address in stubs, "unreviewed execution " + hex(address))
        name, far, pop = stubs[address]
        sp = uc.reg_read(UC_X86_REG_SP)
        stack = SS * 16 + sp
        frame = 4 if far else 2
        args = bytes(uc.mem_read(stack + frame, pop))
        trace.append((name, args.hex()))
        if name == "round":
            need(rounds < len(scenario["outcomes"]), "unexpected extra round")
            result = scenario["outcomes"][rounds]
            rounds += 1
            uc.mem_write(DS * 16 + 0x6592, struct.pack("<I", 0xA1230000 + rounds))
            uc.reg_write(UC_X86_REG_AX, 0xA500 | result)
        else:
            uc.reg_write(
                UC_X86_REG_AX, RES if name == "cfg" and scenario["resident"] else 0
            )
        uc.reg_write(UC_X86_REG_BX, 0xABCD)
        uc.reg_write(UC_X86_REG_CX, 0xDCBA)
        uc.reg_write(UC_X86_REG_DX, 0x9182)
        ip = read_word(stack)
        cs = read_word(stack + 2) if far else uc.reg_read(UC_X86_REG_CS)
        uc.reg_write(UC_X86_REG_SP, sp + frame + pop)
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    def write(uc, access, address, size, value, unused):
        allowed = (
            (SS * 16 + 0xFE00 <= address and address + size <= SS * 16 + 0xFF04)
            or (RES * 16 <= address and address + size <= RES * 16 + 256)
            or (DS * 16 <= address and address + size <= (DS + 0x1000) * 16)
        )
        need(allowed, "unreviewed write " + hex(address))
        writes.append((address, size, value))

    u.hook_add(UC_HOOK_CODE, hook)
    u.hook_add(UC_HOOK_MEM_WRITE, write)
    u.emu_start(LOAD * 16 + ENTRY, 0, count=2000)
    need(stopped, "entry instruction budget exhausted")
    need(
        rounds == (len(scenario["outcomes"]) if scenario["resident"] else 0),
        "complete round history",
    )
    for reg, val in (
        (UC_X86_REG_SI, 0x1357),
        (UC_X86_REG_DI, 0x2468),
        (UC_X86_REG_BP, 0xBEEF),
        (UC_X86_REG_SP, 0xFF04),
        (UC_X86_REG_DS, DS),
        (UC_X86_REG_SS, SS),
    ):
        need(u.reg_read(reg) == val, "entry callee-save/stack contract")
    expected = [("init", struct.pack("<HH", 0x13A, DS).hex()), ("cfg", "")]
    if scenario["resident"]:
        if scenario["bgm"] != 0:
            expected.append(("sound_mode", ""))
        expected += [
            ("gaiji_backup", ""),
            ("gaiji_font", struct.pack("<HH", 0x146, DS).hex()),
            ("stage", ""),
            ("background", ""),
        ]
        for result in scenario["outcomes"]:
            expected += [("palette", ""), ("round", "")]
            if result == 1:
                expected.append(("next_round", ""))
        expected += [
            ("free_formations", ""),
            ("sound_stop", "0001"),
            (
                "exec",
                struct.pack(
                    "<HH", 0x151 if scenario["outcomes"][-1] == 0 else 0x154, DS
                ).hex(),
            ),
        ]
        need(bytes(u.mem_read(DS * 16 + 0x1A0D, 1)) == b"\x00", "MIDI flag not cleared")
        need(read_word(DS * 16 + 0x2D4) == 100, "palette tone not initialized")
        need(
            bytes(u.mem_read(RES * 16 + 0x10, 4))
            == struct.pack("<I", 0xA1230000 + rounds),
            "resident random seed transfer",
        )
        need(
            bytes(u.mem_read(RES * 16 + 0x33, 1))
            == bytes([(scenario["story"] + (scenario["outcomes"][-1] != 0)) & 255]),
            "story-stage transition",
        )
    need(trace == expected, "foreign call sequence/arguments")
    memory = [bytes(u.mem_read(a, n)) for a, n in regions]
    effects = [
        [(i, y) for i, (x, y) in enumerate(zip(before, after)) if x != y]
        for before, after in zip(initial, memory)
    ]
    return dict(
        trace=trace,
        data_writes=[w for w in writes if not SS * 16 <= w[0] < (SS + 0x1000) * 16],
        registers=[u.reg_read(r) for r in REGS],
        memory_effects=effects,
    ), visited


def compare(target, candidate):
    cases = [dict(resident=False, bgm=b, story=255, outcomes=[]) for b in (0, 1)]
    for terminal in range(256):
        if terminal != 1:
            cases.append(
                dict(
                    resident=True,
                    bgm=terminal & 1,
                    story=255 if terminal & 2 else 0,
                    outcomes=[1] * (terminal % 3) + [terminal],
                )
            )
    for terminal in (0, 2, 255):
        for bgm in (0, 1, 2):
            for story in (0, 255):
                for repeats in (0, 2):
                    cases.append(
                        dict(
                            resident=True,
                            bgm=bgm,
                            story=story,
                            outcomes=[1] * repeats + [terminal],
                        )
                    )
    visited = set()
    for case in cases:
        a, seen = execute(target, case)
        b, other = execute(candidate, case)
        need(a == b, "target/candidate entry behavior differs: " + str(case))
        visited |= seen
        need(seen == other, "entry instruction coverage differs")
    return dict(
        cases=len(cases),
        entry_code_bytes_executed=len(visited),
        visited=sorted(visited),
        all_return_byte_values=True,
        foreign_calls="bounded stubs; actual callees and physical devices not executed",
        memory_scope="changes across complete DGROUP, resident record and entry stack window; ordered non-stack CPU writes, all write bounds and final stack effects; Unicorn far-CALL stack-write hooks differ from PUSH CS/CALL; initial unrelated bytes are not normalized",
        equal=True,
    )
