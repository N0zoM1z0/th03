"""Bounded round-loop contracts. Foreign calls and VSYNC delivery are explicit stubs."""

from dataclasses import dataclass, replace
import struct

from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_INSN
from unicorn.x86_const import (
    UC_X86_INS_OUT, UC_X86_REG_AX, UC_X86_REG_BX, UC_X86_REG_CX,
    UC_X86_REG_DX, UC_X86_REG_SI, UC_X86_REG_DI, UC_X86_REG_BP,
    UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES,
    UC_X86_REG_SS, UC_X86_REG_IP, UC_X86_REG_EFLAGS,
)

START, END, SS, SP, RES, STOP = 0x9778, 0x9AD6, 0x8000, 0xFF00, 0x6000, 0xFFF0
# Complete foreign call interfaces observed in the target, not callee bodies.
# The converted NOP/PUSH CS/CALL sequences retain their genuine far return ABI.
DIRECT = {
    0xA438: ("collmap", False, 0), 0x1797F: ("bullet_template", True, 0),
    0xB7E5: ("hitcircles_update", False, 0), 0xE83F: ("shots_update", False, 0),
    0xBB12: ("intro_update", False, 0), 0x13CC7: ("formations", True, 0),
    0x17A1B: ("bullets_update", True, 0), 0x1609E: ("enemies_update", True, 0),
    0x18059: ("fireballs_update", True, 0), 0xCEB2: ("effects_update", True, 0),
    0xDA43: ("player_update", False, 4), 0xEC76: ("sound", True, 0),
    0xC7A5: ("pause", False, 0), 0xCA3C: ("round_CA3C", True, 0),
    0xCB81: ("round_CB81", True, 2), 0x704: ("egc_on", True, 0),
    0xE86A: ("shots_render", False, 0), 0x164DA: ("enemies_render", True, 0),
    0x1837C: ("fireballs_render", True, 0), 0xB80B: ("hitcircles_render", False, 0),
    0xDE95: ("player_render", False, 2), 0x71A: ("egc_off", True, 0),
    0xDF18: ("player_overlay", False, 2), 0xCEE0: ("effects_render", True, 0),
    0x17BD1: ("bullets_render", True, 0), 0xC2F9: ("defeat_banner", False, 0),
    0xE3F2: ("match_result", False, 0), 0xA289: ("score_commit", False, 2),
    0xC830: ("round_C830", False, 0), 0xC8C4: ("round_C8C4", False, 0),
    0xD52E: ("score_hud", False, 0), 0xC9FE: ("round_C9FE", True, 2),
    0xBE5D: ("intro_render", False, 0), 0x15D53: ("combos", True, 0),
    0x1C7E: ("palette", True, 0), 0xF5C: ("grcg_color", True, 4),
    0xB37C: ("clear", False, 0), 0xF86: ("grcg_off", True, 0),
    0xA3FA: ("randring", False, 0), 0xB4A8: ("background_finish", False, 0),
}
CALLBACKS = {
    0x2910: "exatt_update0", 0x291C: "exatt_update1",
    0x1DCE: "boss_update0", 0x1DD2: "boss_update1",
    0x306E: "player_hook0", 0x3072: "player_hook1",
    0x2D2C: "charge_update0", 0x2D30: "charge_update1",
    0x2D44: "pellet0", 0x2D48: "pellet1",
    0x2D4C: "bullet0", 0x2D50: "bullet1",
    0x1182: "input", 0x39C4: "render_hook",
    0x3076: "bomb0", 0x307A: "bomb1",
    0x1DD6: "boss_render0", 0x1DDA: "boss_render1",
    0x2914: "exatt_render0", 0x2920: "exatt_render1",
    0x2D34: "charge_render0", 0x2D38: "charge_render1",
}


@dataclass(frozen=True)
class Scenario:
    frame: int = 1
    total: int = 0x1234FFFF
    flag: int = 0
    timing_after_background: int = -1
    quit: int = 0
    frames: int = 1
    defeat: int = 0
    mode: int = 0
    wins0: int = 0
    wins1: int = 0
    winner: int = 0
    lives: int = 0
    midpoint: int = 0
    result_wait: int = 320
    wait: int = 2
    vsync: int = 0
    speed: int = 126
    damage0: int = 5
    damage1: int = 6
    palette: int = 1
    front: int = 0
    back: int = 1
    input: int = 0x1000


def need(value, message):
    if not value:
        raise ValueError("round loop runtime: " + message)


def initial_data(s, resident_offset):
    data = bytearray((i * 37 + 11) & 255 for i in range(65536))
    for offset, value in {
        0x659A: s.flag, 0x65A0: s.quit, 0x38DC: s.defeat,
        0x2663: s.midpoint, 0x6599: s.wait, 0x6598: s.speed,
        0x65A1: s.palette, 0x658F: s.front, 0x658E: s.back,
        0x6612: s.wins0, 0x6692: s.wins1,
        0x6619: s.damage0, 0x6699: s.damage1,
        0x2928: 0xA4, 0x6590: 0xB5,
    }.items():
        data[offset] = value
    for offset, value in {0x6596: s.frame, 0x1188: s.result_wait,
                          0x11EA: s.vsync, 0x1A9A: s.input,
                          0x1A96: 0x1234, 0x1A98: 0xABCD,
                          0x2660: 0x7000, 0x118A: 0x7020}.items():
        struct.pack_into("<H", data, offset, value)
    struct.pack_into("<I", data, 0x6592, s.total)
    struct.pack_into("<HH", data, 0x1D90, resident_offset, RES)
    for i, offset in enumerate(CALLBACKS):
        struct.pack_into("<HH", data, offset, 0x100 + i * 16, 0x7000)
    return data


def contract(initial, s, ds, resident_offset):
    """Independent state machine: no target decoding or candidate-derived expectations."""
    expected = bytearray(initial)
    stores, trace = [], []
    base, resident = ds * 16, RES * 16 + resident_offset

    def get(offset, size=1):
        return int.from_bytes(expected[base + offset:base + offset + size], "little")

    def put(offset, size, value, cpu=True, absolute=False):
        address = offset if absolute else base + offset
        value &= (1 << (size * 8)) - 1
        expected[address:address + size] = value.to_bytes(size, "little")
        if cpu:
            stores.append((address, size, value))

    def call(name, *args):
        trace.append((name, args, get(0x2928), get(0x6590)))

    def player(pid):
        put(0x2928, 1, pid)
        put(0x6590, 1, pid * 40)

    for frame_index in range(s.frames):
        if get(0x65A0):
            return expected, stores, trace, 0
        call("collmap"); call("bullet_template")
        for pid in (0, 1):
            player(pid)
            for stem in ("exatt_update", "boss_update", "player_hook"):
                call(stem + str(pid))
        call("hitcircles_update"); call("shots_update")
        for pid in (0, 1):
            player(pid); call("charge_update" + str(pid))
        for name in ("intro_update", "formations", "bullets_update", "enemies_update", "fireballs_update"):
            call(name)
        for pid in (0, 1):
            player(pid); call("pellet" + str(pid)); call("bullet" + str(pid))
        call("effects_update"); call("input")
        for pid, input_value in ((0, 0x1234), (1, 0xABCD)):
            put(0x6590, 1, pid); call("player_update", 0x65A6 + pid * 128, input_value)
        call("sound")
        if s.input & 0x1000:
            call("pause")
        call("round_CA3C"); call("round_CB81", 0); call("round_CB81", 1)
        call("render_hook")
        if frame_index + 1 == s.frames:
            put(0x65A0, 1, 1, cpu=False)  # bounded foreign callback requests exit
        frame = get(0x6596, 2)
        if not (get(0x659A) and frame % 2 == 0):
            call("egc_on")
            for stem in ("bomb", "boss_render"):
                for pid in (0, 1):
                    player(pid); call(stem + str(pid))
            for name in ("shots_render", "enemies_render", "fireballs_render", "hitcircles_render"):
                call(name)
            for pid in (0, 1):
                player(pid); call("exatt_render" + str(pid)); call("charge_render" + str(pid))
            for pid in (0, 1):
                put(0x6590, 1, pid); call("player_render", 0x65A6 + pid * 128)
            call("egc_off")
            for pid in (0, 1):
                put(0x6590, 1, pid); call("player_overlay", 0x65A6 + pid * 128)
            call("effects_render"); call("bullets_render")
            if s.defeat == 2:
                call("defeat_banner")
                match = s.mode != 1 and (s.wins0 >= 2 or s.wins1 >= 2)
                match |= s.mode == 1 and s.winner == 0
                if match:
                    call("match_result")
                    if frame == s.result_wait:
                        put(0x2660, 2, 0x1DC8)
                    elif s.midpoint:
                        call("score_commit", s.winner)
                        return expected, stores, trace, 2
                elif frame == 160:
                    put(0x2660, 2, 0x1DC8)
                elif s.midpoint:
                    if s.mode != 1:
                        return expected, stores, trace, 1
                    if s.lives:
                        put(resident + 0x34, 1, s.lives - 1, absolute=True)
                        return expected, stores, trace, 1
                    call("score_commit", 0)
                    return expected, stores, trace, 2
            for name in ("round_C830", "round_C8C4", "score_hud"):
                call(name)
            call("round_C9FE", 0); call("round_C9FE", 1)
            call("intro_render"); call("combos")
            call("background_finish" if get(0x2660, 2) == 0x1DC8 else "background")
            if s.timing_after_background >= 0:
                put(0x659A, 1, s.timing_after_background, cpu=False)
            call("demo")
            wait = get(0x6599)
            if not get(0x659A):
                if wait > get(0x11EA, 2):
                    put(0x11EA, 2, wait, cpu=False)  # modeled IRQ delivery
                put(0x11EA, 2, 0); put(0x6599, 1, 1)
            elif frame % 2 == 0:
                put(0x11EA, 2, 0)
                if wait:
                    put(0x11EA, 2, wait, cpu=False)
                put(0x6599, 1, 2)
            if get(0x65A1):
                call("palette"); put(0x65A1, 1, 0)
            call("out", 0xA6, 1, get(0x658F)); call("out", 0xA4, 1, get(0x658E))
            put(0x658F, 1, get(0x658E)); put(0x658E, 1, get(0x658E) ^ 1)
            call("grcg_color", 0, 0xC0); call("clear", 0x3932)
            call("grcg_color", 1, 0xC0); call("clear", 0x395A); call("grcg_off")
        put(0x6592, 4, get(0x6592, 4) + 1)
        frame = (frame + 1) & 65535
        put(0x6596, 2, frame)
        for offset, mask in ((0x65A5, 15), (0x65A4, 7), (0x65A3, 3), (0x65A2, 1)):
            put(offset, 1, get(0x6592) & mask)
        if frame % 64 == 0:
            if get(0x6598) < 127:
                put(0x6598, 1, get(0x6598) + 1)
            if frame % 1024 == 0:
                call("randring")
                for offset in (0x6619, 0x6699):
                    if get(offset) < 6:
                        put(offset, 1, get(offset) + 1)
            if frame < 2000:
                put(0x661A, 2, 0); put(0x669A, 2, 0)
    return expected, stores, trace, 0


def execute(image, s, load=0x1000, resident_offset=0):
    ds = load + 0x1D56
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for r in image.relocations:
        struct.pack_into("<H", program, r.linear, (struct.unpack_from("<H", program, r.linear)[0] + load) & 65535)
    u.mem_write(load * 16, bytes(program))
    u.mem_write(ds * 16, bytes(initial_data(s, resident_offset)))
    resident = bytearray([0xA7] * 256)
    resident[0x17], resident[0x28], resident[0x34] = s.winner, s.mode, s.lives
    u.mem_write(RES * 16 + resident_offset, bytes(resident))
    registers = ((UC_X86_REG_SI, 0x1357), (UC_X86_REG_DI, 0x2468),
                 (UC_X86_REG_BP, 0xBEEF), (UC_X86_REG_CS, load + 0x96E),
                 (UC_X86_REG_DS, ds), (UC_X86_REG_SS, SS))
    for reg, value in registers + ((UC_X86_REG_AX, 0xA55A), (UC_X86_REG_BX, 0x5AA5),
                                   (UC_X86_REG_CX, 0x1234), (UC_X86_REG_DX, 0x5678),
                                   (UC_X86_REG_ES, 0x4444), (UC_X86_REG_SP, SP),
                                   (UC_X86_REG_IP, START - 0x96E0), (UC_X86_REG_EFLAGS, 0x202)):
        u.reg_write(reg, value)
    u.mem_write(SS * 16 + SP, struct.pack("<H", STOP))
    expected, expected_stores, expected_trace, result = contract(bytes(u.mem_read(0, 0x100000)), s, ds, resident_offset)
    stubs = {load * 16 + address: spec for address, spec in DIRECT.items()}
    for i, name in enumerate(CALLBACKS.values()):
        stubs[0x70100 + i * 16] = (name, True, 0)
    stubs[(load + 0x96E) * 16 + 0x7000] = ("background", False, 0)
    stubs[(load + 0x96E) * 16 + 0x7020] = ("demo", False, 0)
    stores, trace, visited, waits = [], [], set(), {}
    frame_count, stopped = 0, False

    def get(offset, size=1):
        return int.from_bytes(u.mem_read(ds * 16 + offset, size), "little")

    def call(name, args):
        trace.append((name, args, get(0x2928), get(0x6590)))

    def hook(uc, address, size, unused):
        nonlocal frame_count, stopped
        if address == (load + 0x96E) * 16 + STOP:
            stopped = True; uc.emu_stop(); return
        relative = address - load * 16
        if START <= relative < END:
            visited.update(range(relative, relative + size))
            if relative in (0x99DF, 0x9A04):
                key = (frame_count, relative)
                waits[key] = waits.get(key, 0) + 1
                if waits[key] == 2 and get(0x6599) > get(0x11EA, 2):
                    uc.mem_write(ds * 16 + 0x11EA, struct.pack("<H", get(0x6599)))
            return
        need(address in stubs, "foreign control transfer")
        name, far, pop = stubs[address]
        sp = uc.reg_read(UC_X86_REG_SP)
        frame = SS * 16 + sp
        offset = int.from_bytes(uc.mem_read(frame, 2), "little")
        segment = int.from_bytes(uc.mem_read(frame + 2, 2), "little") if far else uc.reg_read(UC_X86_REG_CS)
        args = struct.unpack("<" + "H" * (pop // 2), uc.mem_read(frame + (4 if far else 2), pop)) if pop else ()
        if name == "clear":
            args = (uc.reg_read(UC_X86_REG_BX),)
        call(name, args)
        if name == "render_hook":
            frame_count += 1
            if frame_count == s.frames:
                uc.mem_write(ds * 16 + 0x65A0, b"\x01")
        if name in ("background", "background_finish") and s.timing_after_background >= 0:
            uc.mem_write(ds * 16 + 0x659A, bytes([s.timing_after_background]))
        for reg, value in ((UC_X86_REG_AX, 0xA55A), (UC_X86_REG_BX, 0x5AA5),
                           (UC_X86_REG_CX, 0x1234), (UC_X86_REG_DX, 0x5678),
                           (UC_X86_REG_ES, 0x4444)):
            uc.reg_write(reg, value)
        uc.reg_write(UC_X86_REG_SP, sp + (4 if far else 2) + pop)
        uc.reg_write(UC_X86_REG_CS, segment)
        uc.reg_write(UC_X86_REG_IP, offset)

    def store(uc, access, address, size, value, unused):
        low, high = SS * 16 + SP - 64, SS * 16 + SP + 2
        if low <= address and address + size <= high:
            return
        stores.append((address, size, value))

    def output(uc, port, size, value, unused):
        call("out", (port, size, value))

    hooks = [u.hook_add(UC_HOOK_CODE, hook), u.hook_add(UC_HOOK_MEM_WRITE, store),
             u.hook_add(UC_HOOK_INSN, output, None, 1, 0, UC_X86_INS_OUT)]
    try:
        u.emu_start(load * 16 + START, 0, count=5000)
        need(stopped, "return/instruction budget")
        need(trace == expected_trace, "ordered foreign calls, arguments, player views and ports")
        need(stores == expected_stores, "ordered state stores")
        actual = bytes(u.mem_read(0, 0x100000))
        low, high = SS * 16 + SP - 64, SS * 16 + SP + 2
        need(actual[:low] == expected[:low] and actual[high:] == expected[high:], "complete non-stack memory")
        need(u.reg_read(UC_X86_REG_AX) & 255 == result, "AL result")
        need(u.reg_read(UC_X86_REG_SP) == SP + 2, "near cdecl stack")
        need(all(u.reg_read(reg) == value for reg, value in registers), "preserved registers/segments")
        return dict(visited=sorted(visited), result=result, calls=len(trace), stores=len(stores))
    finally:
        for hook_id in hooks:
            u.hook_del(hook_id)


def scenarios():
    yield Scenario(quit=1)
    for frame in (0, 1, 63, 1023, 1983, 2047, 65535):
        for flag in (0, 1, 255):
            for speed in (126, 127, 255):
                yield Scenario(frame=frame, flag=flag, speed=speed,
                               damage0=5, damage1=255, palette=flag, input=0 if flag else 0xFFFF)
    for wait, vsync in ((0, 0), (1, 1), (2, 0), (255, 65535)):
        for frame in (0, 1):
            for timing in (-1, 0, 1):
                yield Scenario(frame=frame, wait=wait, vsync=vsync, timing_after_background=timing)
    for mode, winner, wins, lives, frame, midpoint in (
        (0, 0, 0, 0, 159, 0), (0, 1, 0, 0, 160, 1), (0, 1, 0, 0, 161, 1),
        (0, 0, 2, 0, 319, 0), (0, 1, 2, 0, 320, 1), (0, 1, 2, 0, 321, 1),
        (1, 0, 0, 0, 320, 1), (1, 0, 0, 0, 321, 1),
        (1, 1, 0, 0, 159, 0), (1, 1, 0, 0, 160, 1),
        (1, 1, 0, 0, 161, 1), (1, 1, 0, 1, 161, 1), (1, 1, 0, 255, 161, 1),
        (255, 255, 255, 0, 321, 255),
    ):
        for player in (0, 1):
            yield Scenario(defeat=2, mode=mode, winner=winner, lives=lives, frame=frame,
                           midpoint=midpoint, wins0=wins if player == 0 else 0,
                           wins1=wins if player == 1 else 0)
    yield Scenario(frame=1023, damage0=6, damage1=5)
    for total in (0, 65535, 0xFFFFFFFF):
        yield Scenario(total=total, frames=2, front=255, back=254, damage0=0, damage1=0)


def compare(target, candidate):
    visited, count = set(), 0
    for load, resident_offset in ((0x1000, 0), (0x2200, 0x200)):
        for s in scenarios():
            first = execute(target, s, load, resident_offset)
            need(first == execute(candidate, s, load, resident_offset), "target/candidate result")
            visited.update(first["visited"])
            count += 1
    need(visited == set(range(START, END)), "complete 862-byte execution coverage: " + str(sorted(set(range(START, END)) - visited)))
    return dict(cases=count, code_bytes_executed=len(visited), equal=True,
                scope="two loads/resident offsets; terminal and repeated frames, result/continue/game-over exits, callback order/player views/arguments, VSYNC schedule, pages/ports, unsigned counters/caps/wrap, complete non-stack memory and near ABI; all foreign services are stubs")


def negative_controls(image):
    rejected = []
    for name, offset, value, s in (
        ("near frame", START, 0x90, Scenario(quit=1)),
        ("quit result", 0x9AD3, 3, Scenario(quit=1)),
        ("player view", 0x978F, 1, Scenario()),
        ("page port", 0x9A26, 0xA4, Scenario()),
        ("speed cap", 0x9A8D, 126, Scenario(frame=63)),
        ("background callback", 0x998A, 0xC9, Scenario(defeat=2, frame=160)),
        ("counter width", 0x9A62, 0x90, Scenario(total=65535)),
        ("unrelated store", 0x9A71, 0xA6, Scenario()),
    ):
        program = bytearray(image.program_image)
        need(program[offset] != value, "mutation must change bytes")
        program[offset] = value
        try:
            execute(replace(image, program_image=bytes(program)), s)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("round loop runtime mutation accepted: " + name)
    return dict(count=len(rejected), rejected=rejected)
