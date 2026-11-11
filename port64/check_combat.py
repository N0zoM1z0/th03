#!/usr/bin/env python3
"""Compare explosion/chain scoring and derived fireballs with original MAIN.

The real explosion, score, gauge, combo, boss/panic and fireball/vector callees
execute together. This check supplies a hitbox and controlled EFE/chain state.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def original(image, fixture, operation="--explosion", run=None, stack_slot=None):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import (UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS,
                                  UC_X86_REG_SS, UC_X86_REG_IP, UC_X86_REG_AX)
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds, pid = 0x2d560, fixture & 1
    put = lambda at, value, size=1: u.mem_write(ds + at, int(value).to_bytes(size, 'little'))
    speeds, against = (0, 0, 96, 64, 127, 32, 0), (0, 1, 1, 2, 3, 1, 1)
    # Explicitly clear the affected BSS, retaining authored initialized tables.
    for at, size in ((0x3ed6, 3072), (0x4ade, 128), (0x393e, 8), (0x65a6, 256), (0x4b64, 16),
                     (0x4ad8, 2), (0x2d54, 2), (0x393c, 2), (0x798, 2),
                     (0x66a6, 448), (0x68de, 20), (0x68f2, 8320), (0x2832, 80)):
        u.mem_write(ds + at, bytes(size))
    put(0x6598, speeds[fixture])
    put(0x6596, 300 if fixture in (3, 4) else 0, 2)
    put(0x4b62, 9)
    put(0x4adb, 0)
    put(0x4ada, against[fixture])
    put(0x63e, pid if fixture == 4 else 255)
    put(0x1e3e, 15 if fixture == 4 else 0)
    put(0x3ed4, 65000 if fixture == 5 else 5120, 2)
    put(0xbec, int(fixture == 4))
    put(0x8df8, 2 if fixture == 4 else 0)
    put(0x1f52, 255)
    u.mem_write(ds + 0x1e52, bytes((i * 13 + 7) & 255 for i in range(256)))
    u.mem_write(ds + 0x659c, bytes(4))
    u.mem_write(ds + 0x856, bytes(2))
    for p in range(2):
        base = 0x65a6 + p * 128
        u.mem_write(ds + base, struct.pack('<hh', *((3600, 4800) if p == 0 else (800, 5200))))
        put(base + 0x1a, 1024, 2)
        put(0x2d56 + p, 15)
        u.mem_write(ds + 0x4b64 + p * 8, bytes([9, 9, 9, 0, 0, 0, 0, 0]))
    if fixture == 2:
        put(0x65a6 + pid * 128 + 0x1e, 1)

    def efe(index, flag, frame, slot):
        at = 0x3ed6 + index * 48
        u.mem_write(ds + at, struct.pack('<BBhhBBBB', flag, frame, 1200, 1800, 2, 0, pid, 32))
        put(at + 28, slot)

    efe(0, 9, 0, 3)
    if fixture in (0, 2):
        efe(1, 10, 4, 4)
    if fixture == 2:
        efe(40, 10, 0, 3)
    if fixture == 3:
        put(0x3ed6 + 40 * 48 + 1, 37)
    put(0x4ade + pid * 16 + 3, 10 if fixture == 3 else 12 if fixture == 4 else 1)
    put(0x4ade + pid * 16 + 4, 1)
    put(0x4afe + pid * 16 + 3, 8 if fixture == 3 else 18 if fixture == 4 else 0)
    put(0x4b1e + pid * 16 + 3, 7 if fixture == 3 else 6 if fixture == 4 else 0)
    put(0x4b3e + pid * 16 + 3, 2)
    if fixture in (4, 5):
        put(0x393e + pid * 4 + 2, 29900 if fixture == 4 else 65530, 2)
    if fixture == 5:
        u.mem_write(ds + 0x4b64 + pid * 8, bytes([9] * 8))
    left, top, right, bottom = (4000, 5000, 4200, 5200) if fixture == 6 else (1100, 1700, 1300, 1900)
    u.mem_write(ds + 0x38ce, struct.pack('<hhhhhhB', left, top, 0, 0, right, bottom, pid))
    extra_events = []
    pipeline = operation == '--combat-pipeline'
    if pipeline:
        u.mem_write(ds + 0x68de, struct.pack('<hhBBBBBBhhHBBBB', 1200, 1800, 16, 64, pid, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0))
        put(0x6590, 40)
    hit_operation = operation in ('--enemy-hit', '--fireball-hit')
    if hit_operation:
        for i in range(64):
            put(0x3ed6 + i * 48, 0)
        put(0x68ef, 1)
        put(0x68f0, 1)
        put(0x658b + pid, int(fixture == 3 and operation == '--enemy-hit'))
        put(0x38dc, int(fixture == 5) * 2)
        put(0x6590, 40)
        put(0x2880, 0)
        put(0x8df6, 0)
        put(0x8df7, 0)
        put(0x4b63, 0)
        put(0x66a6, int(fixture not in (2, 3)))
        u.mem_write(ds + 0x66a8, struct.pack('<hh', 944, -28 if fixture == 4 and operation == '--enemy-hit' else 1672))
        put(0x66a6 + 12, pid)
        for p in range(2):
            u.mem_write(ds + 0x2d3c + p * 4, struct.pack('<HH', 0, 0x7000))
        if operation == '--enemy-hit':
            efe(0, 1, 20, 0)
            put(0x3ed6 + 7, 1 if fixture == 0 else 3 if fixture == 1 else 0)
            put(0x3ed6 + 4, 100 if fixture == 4 else 0 if fixture == 6 else 1800, 2)
            if fixture == 2:
                efe(1, 10, 0, 3)
                put(0x4b3e + pid * 16 + speeds[fixture] // 32, 3)
        else:
            at = 0x3ed6 + 40 * 48
            efe(40, 1, 20, 0)
            put(at + 7, int(fixture == 0))
            put(at + 6, 2)
            put(at + 9, 48)
            put(at + 32, 3 if fixture == 2 else 4 if fixture == 3 else 2 if fixture == 4 else 0)
            if fixture in (2, 3):
                efe(0, 9, 0, 3)
            if fixture == 6:
                u.mem_write(ds + at + 4, struct.pack('<h', -1000))

        if stack_slot is not None:
            put(0x4b7c, 255)

        def hook(uc, address, size, unused):
            sp = uc.reg_read(UC_X86_REG_SP)
            if address == 0x70000 or address == 0x10000 + 0x18fe0 + 0x119e:
                ip, cs = struct.unpack('<HH', uc.mem_read(0x80000 + sp, 4))
                if address == 0x70000:
                    uc.reg_write(UC_X86_REG_AX, int(fixture == 1))
                    put(0x8df6, int(fixture == 1 and operation == '--enemy-hit'))
                    uc.reg_write(UC_X86_REG_SP, sp + 4)
                else:
                    target, y, x = struct.unpack('<Hhh', uc.mem_read(0x80000 + sp + 4, 6))
                    extra_events.extend((x, y, target & 255))
                    uc.reg_write(UC_X86_REG_SP, sp + 10)
                uc.reg_write(UC_X86_REG_CS, cs)
                uc.reg_write(UC_X86_REG_IP, ip)
            elif address == 0x239d0 + 0x47f3:
                # ENTER's [BP-1] retains the previous render-frame context.
                uc.mem_write(0x80000 + sp - 3, bytes([15 if stack_slot is None else stack_slot]))

        u.hook_add(UC_HOOK_CODE, hook)
    for register, value in ((UC_X86_REG_CS, 0x239d), (UC_X86_REG_DS, 0x2d56),
                            (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
        u.reg_write(register, value)
    u.mem_write(0x8ff00, struct.pack('<H', 0xf000) if hit_operation else struct.pack('<HH', 0xf000, 0x239d))
    entry = 0x3d60 if pipeline else 0x2add if operation == '--enemy-hit' else 0x47f3 if operation == '--fireball-hit' else 0x2d3d
    u.emu_start(0x239d0 + entry, 0x239d0 + 0xf000, count=400000)
    if u.reg_read(UC_X86_REG_IP) != 0xf000:
        raise ValueError('original explosion query did not return')
    result = 0 if hit_operation or pipeline else u.reg_read(UC_X86_REG_AX) & 255
    if pipeline:
        u.mem_write(ds + 0x4ba0, bytes(6624))
        for entry in (0x404b, 0x4689):
            u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x239d))
            u.reg_write(UC_X86_REG_SP, 0xff00)
            u.emu_start(0x239d0 + entry, 0x239d0 + 0xf000, count=400000)
            if u.reg_read(UC_X86_REG_IP) != 0xf000:
                raise ValueError('original bullet/explosion/fireball pipeline did not return')
    if run:
        ticks, bomb = run
        for tick in range(ticks):
            u.mem_write(ds + 0x4ba0, bytes(6624))
            u.mem_write(ds + 0x6580, bytes([int(bomb and tick >= 20)] * 2))
            u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x239d))
            u.reg_write(UC_X86_REG_SP, 0xff00)
            u.emu_start(0x239d0 + 0x4689, 0x239d0 + 0xf000, count=100000)
            if u.reg_read(UC_X86_REG_IP) != 0xf000:
                raise ValueError('original fireball update did not return')
    b = bytes(u.mem_read(ds, 65536))
    word = lambda at: struct.unpack_from('<H', b, at)[0]
    signed = lambda at: struct.unpack_from('<h', b, at)[0]
    out = [result, b[0x4b62], b[0x4adb], b[0xbec], b[0x8df8],
           b[0x63e], b[0x1e3e], word(0x3ed4), b[0x1f52]]
    for p in range(2):
        out.extend((b[0x2d54 + p], b[0x393c + p], b[0x798 + p], b[0x4ad8 + p], b[0x2d56 + p]))
    out.extend(b[0x4b64:0x4b74])
    out.extend(b[0x4ade:0x4b5e])
    out.extend(b[0x856:0x858])
    for p in range(2):
        at = 0x393e + p * 4
        out.extend((b[at], b[at + 1], word(at + 2)))
    for p in range(2):
        at = 0x65a6 + p * 128
        out.extend((word(at + 0x1a), b[at + 0x72], word(at + 0x70), *b[at + 0x77:at + 0x7a]))
    for i in range(64):
        at = 0x3ed6 + i * 48
        out.extend((b[at], b[at + 1], signed(at + 2), signed(at + 4), *b[at + 6:at + 10], b[at + 28]))
    for i in range(24):
        at = 0x3ed6 + (40 + i) * 48
        out.extend((signed(at + 16), signed(at + 18), signed(at + 20), signed(at + 22), b[at + 27], b[at + 32]))
    if run or pipeline:
        out.extend(b[0x4ba0:0x6580])
    if hit_operation or pipeline:
        out.extend((b[0x8df6], b[0x4b63], b[0x8df7], b[0x2880]))
        for i in range(13):
            out.extend(struct.unpack_from('<BBhh', b, 0x2832 + i * 6))
        out.extend(b[0x66a6 + i * 14] for i in range(32))
        out.extend((signed(0x68de), signed(0x68e0), *b[0x68e2:0x68e6], b[0x68e7], word(0x68ec), b[0x68ee]))
        for i in range(320):
            at = 0x68f2 + i * 26
            out.extend((b[at], b[at + 1], *struct.unpack_from('<hhhhhh', b, at + 2),
                        *b[at + 14:at + 18], word(at + 18)))
        out.extend((b[0x4b7c], len(extra_events) // 3, *extra_events))
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native-checks', type=Path, required=True)
    parser.add_argument('--dos-root', type=Path, required=True)
    args = parser.parse_args()
    root = args.dos_root.resolve()
    config = tomllib.loads((root / 'config/targets.toml').read_text())
    target = next(row for row in config['artifacts'] if row['id'] == 'th03-main')
    raw = (root / target['private_path']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != target['sha256']:
        raise ValueError('original MAIN identity changed')
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    image = parse_mz(raw)
    for fixture in range(7):
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--explosion', str(fixture)], text=True).split()))
        expected = original(image, fixture)
        if native != expected:
            index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
            raise ValueError(f'explosion fixture={fixture}, index={index}: native={native[index:index + 1]}, original={expected[index:index + 1]}')
    for operation in ('--enemy-hit', '--fireball-hit'):
        for fixture in range(7):
            native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), operation, str(fixture)], text=True).split()))
            expected = original(image, fixture, operation)
            if native != expected:
                index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
                raise ValueError(f'{operation} fixture={fixture}, index={index}: native={native[index:index + 1]}, original={expected[index:index + 1]}')
    for fixture, ticks, bomb in ((2, 20, False), (3, 80, False), (4, 160, False), (3, 100, True)):
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--fireball-run',
                                                       str(fixture), str(ticks), str(int(bomb))], text=True).split()))
        expected = original(image, fixture, run=(ticks, bomb))
        if native != expected:
            index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
            raise ValueError(f'fireball movement fixture={fixture}, ticks={ticks}, index={index}: native={native[index:index + 1]}, original={expected[index:index + 1]}')
    for fixture in (1, 2, 4):
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--combat-pipeline', str(fixture)], text=True).split()))
        expected = original(image, fixture, '--combat-pipeline')
        if native != expected:
            index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
            raise ValueError(f'combat pipeline fixture={fixture}, index={index}: native={native[index:index + 1]}, original={expected[index:index + 1]}')
    for fixture, slot in ((1, 22), (4, 62)):
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--fireball-hit', str(fixture), str(slot)], text=True).split()))
        expected = original(image, fixture, '--fireball-hit', stack_slot=slot)
        if native != expected:
            index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
            raise ValueError(f'fireball stack-slot={slot}, fixture={fixture}, index={index}: native={native[index:index + 1]}, original={expected[index:index + 1]}')
    print('Original fireball stack-slot aliases reproduce score-digit and extends resets with matching Extra Attacks.')
    print('Three real bullet/explosion/fireball pipelines agree, including complete collision maps and all bullet slots.')
    print('Fourteen enemy/fireball hit cases and four full fireball movement/collision snapshots agree with original MAIN.')
    print('Seven original explosion/chain cases agree: score carry, combo/boss/panic, all64 EFE and derived fireballs.')


if __name__ == '__main__':
    main()
