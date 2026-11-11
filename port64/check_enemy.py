#!/usr/bin/env python3
"""Compare original ENEDAT execution against the portable enemy VM.

Real MAIN instructions execute the script interpreter and its vector/movement
callees. This is an isolated script check; combat collisions are not invoked.
"""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import tomllib


def scripts(file):
    at, out = 4, []
    while True:
        count = struct.unpack_from('<H', file, at)[0]
        at += 2
        if not count:
            return out
        formation = []
        for _ in range(count):
            size = file[at]
            at += 1
            formation.append(file[at:at + size])
            at += size
        out.append(formation)


class Original:
    def __init__(self, image, script, band, mirror, player_y):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
        from unicorn.x86_const import (UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS,
                                      UC_X86_REG_ES, UC_X86_REG_SS, UC_X86_REG_IP)
        self.sp_reg, self.ip_reg = UC_X86_REG_SP, UC_X86_REG_IP
        self.u = u = Uc(UC_ARCH_X86, UC_MODE_16)
        u.mem_map(0, 0x100000)
        program = bytearray(image.program_image)
        for relocation in image.relocations:
            old = struct.unpack_from('<H', program, relocation.linear)[0]
            struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
        u.mem_write(0x10000, bytes(program))
        data = 0x2d560
        u.mem_write(data + 0x4adc, struct.pack('<H', 0x3ed6))
        u.mem_write(data + 0x1fbe, struct.pack('<H', 0x6000))
        u.mem_write(data + 0x1fc0, bytes([band]))
        u.mem_write(data + 0x65a6, struct.pack('<hh', 144 << 4, player_y))
        self.base = data + 0x3ed6
        enemy = bytearray(48)
        enemy[0], enemy[33] = 3, mirror
        u.mem_write(self.base, bytes(enemy))
        u.mem_write(0x60000, script)
        for reg, value in ((UC_X86_REG_CS, 0x239d), (UC_X86_REG_DS, 0x2d56),
                           (UC_X86_REG_ES, 0x2d56), (UC_X86_REG_SS, 0x8000)):
            u.reg_write(reg, value)
        self.stopped = False

        def hook(uc, address, size, unused):
            if address == 0x239d0 + 0x100:
                self.stopped = True
                uc.emu_stop()

        u.hook_add(UC_HOOK_CODE, hook)

    def tick(self):
        u = self.u
        u.mem_write(0x8ff00, struct.pack('<H', 0x100))
        u.reg_write(self.sp_reg, 0xff00)
        u.reg_write(self.ip_reg, 0x55c)
        self.stopped = False
        u.emu_start(0x239d0 + 0x55c, 0, count=10000)
        if not self.stopped:
            raise ValueError('original enemy_run did not return')
        b = bytes(u.mem_read(self.base, 48))
        word = lambda at: struct.unpack_from('<H', b, at)[0]
        signed = lambda at: struct.unpack_from('<h', b, at)[0]
        return [b[0], signed(2), signed(4), b[6], b[7], b[8], b[9], word(10), word(12),
                signed(16), signed(18), word(24), struct.unpack_from('<b', b, 26)[0], b[31], b[33]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True)
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
    cases = [(0, 0, 0, 0, 5376), (1, 0, 1, 128, 5376), (5, 8, 3, 0, 5376),
             (6, 0, 2, 128, 3072), (8, 0, 3, 128, 5376), (10, 0, 1, 0, 5376)]
    total = 0
    with tempfile.TemporaryDirectory(prefix='th03-enemy-') as work:
        enedat = Path(work) / 'ENEDAT.DAT'
        subprocess.run([str(args.native.resolve()), '--hdi', str(root / '.analysis/runtime/images/zun.hdi'),
                        '--main-assets', '--extract', 'ENEDAT.DAT', '--output', str(enedat)], check=True)
        data = scripts(enedat.read_bytes())
        for formation, enemy, band, mirror, player_y in cases:
            ticks = 600
            native = subprocess.check_output([str(args.native_checks.resolve()), '--enemy', str(enedat),
                                              *map(str, (formation, enemy, band, mirror, ticks, player_y))], text=True)
            probe = Original(image, data[formation][enemy], band, mirror, player_y)
            for frame, line in enumerate(native.splitlines()):
                actual = list(map(int, line.split()))
                expected = probe.tick()
                if actual != expected:
                    raise ValueError(f'formation={formation}, enemy={enemy}, frame={frame}: native={actual}, original={expected}')
                total += 1
    print(f'{len(cases)} original enemy scripts agree for {total} ticks, including movement, signed angles and opcode timing.')


if __name__ == '__main__':
    main()
