#!/usr/bin/env python3
"""Compare collision bitmap primitives and ordinary player hit scans with MAIN."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tomllib


def console_startup(u, image):
    """Run original C0, stdio, far malloc and environment INIT before MAIN."""
    from unicorn import UC_HOOK_INTR
    from unicorn.x86_const import (UC_X86_REG_AX, UC_X86_REG_BX, UC_X86_REG_CS, UC_X86_REG_DS,
                                  UC_X86_REG_DX, UC_X86_REG_ES, UC_X86_REG_IP, UC_X86_REG_SI,
                                  UC_X86_REG_SS, UC_X86_REG_SP, UC_X86_REG_EFLAGS)
    u.mem_write(0xff02, struct.pack('<H', 0x9fff));u.mem_write(0xff2c, struct.pack('<H', 0x900))
    u.mem_write(0xff80, b'\x00\r')
    u.mem_write(0x9000, b'COMSPEC=C:\\COMMAND.COM\0PATH=C:\\DOS\0\0\x01\0C:\\YUMEZIKU\\MAIN.EXE\0')

    def dos(uc, number, unused):
        ax = uc.reg_read(UC_X86_REG_AX);ah = ax >> 8
        if number != 0x21:
            raise ValueError(f'unsupported startup interrupt {number:02x}')
        uc.reg_write(UC_X86_REG_EFLAGS, uc.reg_read(UC_X86_REG_EFLAGS) & ~1)
        if ah == 0x30:
            uc.reg_write(UC_X86_REG_AX, 5);uc.reg_write(UC_X86_REG_BX, 0)
        elif ah == 0x35:
            ip, cs = struct.unpack('<HH', uc.mem_read((ax & 255) * 4, 4))
            uc.reg_write(UC_X86_REG_BX, ip);uc.reg_write(UC_X86_REG_ES, cs)
        elif ah == 0x25:
            uc.mem_write((ax & 255) * 4, struct.pack('<HH', uc.reg_read(UC_X86_REG_DX), uc.reg_read(UC_X86_REG_DS)))
        elif ah == 0x4a:
            pass  # The declared DOS allocation has room for each growth.
        elif ax == 0x4400:
            uc.reg_write(UC_X86_REG_DX, 0x83)  # Character console, stdin/stdout.
        elif ax == 0x6300:
            uc.mem_write(0x9100, bytes([0x81, 0x9f, 0xe0, 0xfc, 0, 0]))
            uc.reg_write(UC_X86_REG_DS, 0x910);uc.reg_write(UC_X86_REG_SI, 0);uc.reg_write(UC_X86_REG_AX, 0)
        else:
            raise ValueError(f'unsupported startup DOS service {ax:04x}')
    hook = u.hook_add(UC_HOOK_INTR, dos)
    h = image.header
    for reg, value in ((UC_X86_REG_CS, 0x1000 + h.initial_relative_cs), (UC_X86_REG_IP, h.initial_ip),
                       (UC_X86_REG_SS, 0x1000 + h.initial_relative_ss), (UC_X86_REG_SP, h.initial_sp),
                       (UC_X86_REG_DS, 0xff0), (UC_X86_REG_ES, 0xff0)):
        u.reg_write(reg, value)
    u.emu_start(0x10000 + h.entry_linear, 0x1013b, count=1000000)
    u.hook_del(hook)
    if u.reg_read(UC_X86_REG_CS) != 0x1000 or u.reg_read(UC_X86_REG_IP) != 0x13b:
        raise ValueError('original console startup did not reach MAIN')
    return bytes(u.mem_read(0x2d560 + 0x2b2, 2)) + bytes(u.mem_read(0x2d560 + 0x10ba, 124))


def original(image, kind, pid, x, y, width, height, right, hit):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16
    from unicorn.x86_const import (UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS,
                                  UC_X86_REG_SS, UC_X86_REG_IP)
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    if kind in ('edge', 'startup'):
        startup = console_startup(u, image)
        if kind == 'startup':
            return startup
    ds = 0x2d560
    u.mem_write(ds + 0x4ba0, bytes(6624))
    u.mem_write(ds + 0x4b8e, struct.pack('<hhhhhhB', x, y, width, height, right, 0, pid))
    for register, value in ((UC_X86_REG_CS, 0x239d), (UC_X86_REG_DS, 0x2d56),
                            (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
        u.reg_write(register, value)
    u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, 0x239d))
    if kind == 'edge':
        u.mem_write(ds + 0x2d4, struct.pack('<H', right))
        u.mem_write(ds + 0x1076, struct.pack('<H', 4))  # Original 486 startup profile.
    else:
        entry = dict(rectangle=0x9e, vertical=0x172, slope=0x1ca)[kind]
        u.emu_start(0x239d0 + entry, 0x239d0 + 0xf000, count=10000)
        if u.reg_read(UC_X86_REG_IP) != 0xf000:
            raise ValueError('original collision writer did not return')
    bitmap = bytes(u.mem_read(ds + 0x4ba0, 6624))
    if not hit:
        return bitmap
    player = bytearray(128)
    struct.pack_into('<hh', player, 0, x, y)
    offset = 0x65a6 + pid * 128
    u.mem_write(ds + offset, bytes(player))
    u.mem_write(ds + 0x6588, struct.pack('<H', offset))
    u.mem_write(ds + 0x6590, bytes([pid]))
    u.mem_write(ds + 0x38e4, bytes(4))
    u.reg_write(UC_X86_REG_CS, 0x196e)
    u.reg_write(UC_X86_REG_SP, 0xff00)
    u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, width if kind == 'edge' else 4))
    u.emu_start(0x196e0 + 0x4a17, 0x196e0 + 0xf000, count=10000)
    if u.reg_read(UC_X86_REG_IP) != 0xf000:
        raise ValueError('original player hit scan did not return')
    flag = bytes(u.mem_read(ds + offset + 4, 1))[0]
    point = struct.unpack('<hh', u.mem_read(ds + 0x38e4, 4))
    return [flag, *point]


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
    native_startup = subprocess.check_output([str(args.native_checks.resolve()), '--startup-crt'])
    if native_startup != original(image, 'startup', 0, 0, 0, 0, 0, 0, False):
        raise ValueError('native startup aliases differ from original C0/stdio/heap/environment startup')
    cases = [('rectangle', 0, 2304, 512, 24, 24, 0), ('rectangle', 1, 64, 64, 12, 12, 0),
             ('vertical', 1, 4496, 5856, 1, 8, 0), ('vertical', 0, 2304, 512, 1, 0, 0),
             ('slope', 0, 64, 0, 3, 0, 4000), ('slope', 1, 4000, 0, 7, 0, 64)]
    for case in cases:
        command = [str(args.native_checks.resolve()), '--collmap', *map(str, case)]
        native = subprocess.check_output(command + ['bitmap'])
        if native != original(image, *case, False):
            raise ValueError(f'complete collision bitmap differs: {case}')
        native = list(map(int, subprocess.check_output(command + ['hit'], text=True).split()))
        if native != original(image, *case, True):
            raise ValueError(f'player scan differs: {case}, native={native}, original={original(image, *case, True)}')
    print('Six complete collision bitmaps and player hit scans agree with original MAIN instructions.')
    for case in ((0, 8, 336, 32, 100), (0, 8, 336, 32, 0), (0, 16, 336, 32, 100),
                 (0, 32, 336, 48, 100), (0, 48, 336, 64, 100), (0, 64, 336, 80, 100),
                 (1, 8, 336, 32, 100), (1, 16, 336, 32, 100),
                 (1, 67, 203, 80, 100), (1, 67, 197, 80, 100), (0, 8, 276, 32, 100)):
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--collision-edge', *map(str, case)], text=True).split()))
        pid, x, y, size, tone = case
        expected = original(image, 'edge', pid, x * 16, y * 16, size, 0, tone, True)
        if native != expected:
            raise ValueError(f'CPU edge scan {case}: native={native}, original={expected}')
    print('Wide CPU edge scans retain palette, sine-table and CRT aliases, including the original allocated environ pointer.')


if __name__ == '__main__':
    main()
