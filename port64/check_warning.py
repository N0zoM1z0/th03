#!/usr/bin/env python3
"""Compare warning portraits, white flash, red fade and active pulses with MAIN.

Run the original controllers and palette restoration; capture text/sound calls
and physical refresh tones at the device boundaries. Compare every game tick,
including simultaneous warnings and the same-call attack activation.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, pid, kind, ticks, pause_case=None):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_IP
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds = 0x2d560
    u.mem_write(ds + 0x798, bytes(2))
    u.mem_write(ds + 0x3938, bytes(6))
    u.mem_write(ds + 0x2d54, bytes((0, 0, 7, 11)))
    u.mem_write(ds + 0x1e3e, bytes([15]))
    palette = bytes((i * 5 + 7) & 255 for i in range(48))
    u.mem_write(ds + 0x11ba, palette)
    u.mem_write(ds + 0x1d94, palette)
    u.mem_write(ds + 0x2d4, struct.pack('<H', 100))
    for p in range(2):
        if pid == 2 or pid == p:
            u.mem_write(ds + 0x798 + p, bytes([1]))
            u.mem_write(ds + 0x393c + p, bytes([kind]))
    tones, sounds = [], []
    pause_inputs = iter((0x1000, 0x20, 0, 0x20, 0x5000) if pause_case == 1 else
                        (0x1000, 0x20, 0, 0x20, 0x1000, 0x1020, 0x20, 0))
    text = [[False, 0, 0, False], [False, 0, 0, False]]
    services = {0x1e8f0 + 0x33e: 0, 0x1e8f0 + 0x34a: 2, 0x1e8f0 + 0x386: 0,
                0x1e8f0 + 0x19c: 0, 0x1e8f0 + 0x187: 2, 0x196e0 + 0x23b1: 2,
                0x1e8f0 + 0x656: 6, 0x11c7e: 0, 0x112d0: 10, 0x1128c: 8, 0x12086: 10, 0x121f2: 0}

    def hook(uc, address, size, unused):
        if address not in services:
            return
        sp = uc.reg_read(UC_X86_REG_SP)
        word = lambda at: struct.unpack('<H', uc.mem_read(0x80000 + sp + at, 2))[0]
        if address == 0x1e8f0 + 0x33e:
            sounds.append(255)
        elif address == 0x1e8f0 + 0x34a:
            sounds.append(word(4))
        elif address == 0x11c7e:
            tones.append(struct.unpack('<H', uc.mem_read(ds + 0x2d4, 2))[0])
        elif address == 0x1e8f0 + 0x19c:
            key = 0 if pause_case is None else next(pause_inputs)
            uc.mem_write(ds + 0x1a9a, struct.pack('<H', key))
        elif address == 0x112d0:
            p = 0 if word(12) >= 44 else 1
            if word(6) == 0x79a:
                text[p][0:2] = [True, word(4)]
            elif word(6) in (0x7d9, 0x7e2):
                text[p][3] = word(6) == 0x7e2
        elif address == 0x1128c:
            p = 0 if word(10) >= 44 else 1
            text[p][2] = word(6) - 0x1f
        elif address == 0x12086:
            text[0 if word(12) >= 44 else 1][0] = False
        ip, cs = word(0), word(2)
        uc.reg_write(UC_X86_REG_SP, sp + 4 + services[address])
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    u.hook_add(UC_HOOK_CODE, hook)

    def call(offset, arguments=(), near=False):
        for reg, value in ((UC_X86_REG_CS, 0x196e), (UC_X86_REG_DS, 0x2d56),
                           (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
            u.reg_write(reg, value)
        u.mem_write(0x8ff00, (struct.pack('<H', 0xf000) if near else struct.pack('<HH', 0xf000, 0x239d)) +
                    b''.join(struct.pack('<H', n) for n in reversed(arguments)))
        u.emu_start(0x196e0 + offset, 0x286e0 if near else 0x329d0, count=100000)
        if u.reg_read(UC_X86_REG_IP) != 0xf000:
            raise ValueError(f'original warning {offset:04x} did not return')

    if pause_case is not None:
        u.mem_write(ds + 0x1d90, struct.pack('<HH', 0, 0x6000))
        u.mem_write(0x6000e, bytes([pause_case == 2, pause_case == 2]))
        u.mem_write(ds + 0x1a9a, struct.pack('<H', 0x1000))
        u.mem_write(ds + 0x65a0, bytes(1))
        u.mem_write(ds + 0x6592, struct.pack('<IH', 12345, 65530))
        call(0x30c5, near=True)
        quit_requested = u.mem_read(ds + 0x65a0, 1)[0]
        frame, result_frame = struct.unpack('<IH', u.mem_read(ds + 0x6592, 6))
        return [quit_requested, frame, result_frame, len(sounds), *sounds, len(tones), *tones]

    for p in range(2):
        call(0x331e, (p,))
    out = list(u.mem_read(ds + 0x798, 2))
    call(0x335c)
    out += tones

    def snapshot():
        b = bytes(u.mem_read(ds, 65536))
        for p in range(2):
            out.extend((b[0x798 + p], b[0x3938 + p], b[0x393a + p], b[0x2d54 + p], text[p][0]))
            if text[p][0]:
                out.extend(text[p][1:])
        out.extend(b[0x11ba:0x11ea])

    snapshot()
    for _ in range(ticks):
        call(0x34a1, (0,))
        call(0x34a1, (1,))
        snapshot()
    return out + [len(sounds)] + sounds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-checks', type=Path, required=True)
    parser.add_argument('--dos-root', type=Path, required=True)
    args = parser.parse_args()
    root = args.dos_root.resolve()
    target = next(row for row in tomllib.loads((root / 'config/targets.toml').read_text())['artifacts'] if row['id'] == 'th03-main')
    raw = (root / target['private_path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != target['sha256']:
        raise ValueError('original MAIN identity changed')
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    image = parse_mz(raw)
    for mode in range(3):
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--pause', str(mode)], text=True).split()))
        expected = original(image, 3, 1, 0, pause_case=mode)
        if native != expected:
            raise ValueError(f'pause {mode}: native={native}, original={expected}')
        print(f'pause {mode}: release/resume or quit outcome, frozen clocks, sounds and fade tones agree', flush=True)
    for pid in (0, 1, 2):
        for kind in (1, 3, 5):
            case = pid, kind, 180
            native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--warning', *map(str, case)], text=True).split()))
            expected = original(image, *case)
            if native != expected:
                index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
                raise ValueError(f'warning {case}, index={index}: native={native[index:index + 10]}, original={expected[index:index + 10]}')
            print(f'warning {case}: all refresh tones, states, text events, palettes and sounds agree', flush=True)


if __name__ == '__main__':
    main()
