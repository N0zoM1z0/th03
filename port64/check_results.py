#!/usr/bin/env python3
"""Compare result rewards/TRAM and complete playfield transitions with MAIN."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import tomllib


def machine(image):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16
    from unicorn.x86_const import UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_IP
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))

    def call(segment, offset, near=False, arguments=()):
        for reg, value in ((UC_X86_REG_CS, segment + 0x1000), (UC_X86_REG_DS, 0x2d56),
                           (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
            u.reg_write(reg, value)
        stack = struct.pack('<H', 0xf000) if near else struct.pack('<HH', 0xf000, 0x239d)
        u.mem_write(0x8ff00, stack + b''.join(struct.pack('<H', value) for value in reversed(arguments)))
        end = (segment + 0x1000) * 16 + 0xf000 if near else 0x329d0
        u.emu_start((segment + 0x1000) * 16 + offset, end, count=2000000)
        if u.reg_read(UC_X86_REG_IP) != 0xf000:
            raise ValueError(f'original {segment:04x}:{offset:04x} did not return')
    return u, call


def result_original(image, pid, stage, profile, ticks):
    from unicorn import UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_IP
    u, call = machine(image)
    ds = 0x2d560
    u.mem_write(ds + 0x1d90, struct.pack('<HH', 0, 0x6000))
    u.mem_write(0x60033, bytes((stage, 255 if profile == 1 else 2)))
    u.mem_write(ds + 0x38dd, bytes([pid ^ 1]))
    u.mem_write(ds + 0x4b64, bytes(16))
    u.mem_write(ds + 0x4b7c, bytes(1))
    u.mem_write(ds + 0x688a, bytes(16))
    p = ds + 0x65a6 + pid * 128
    for at, value in ((0x72, 42), (0x76, 7), (0x77, 5), (0x78, 3), (0x79, 2)):
        u.mem_write(p + at, bytes([255 if profile == 1 else value]))
    if profile == 2:
        u.mem_write(ds + 0x798, bytes((3 if pid == 1 else 0, 3 if pid == 0 else 0)))
        u.mem_write(ds + 0x393c + (pid ^ 1), bytes([3]))
        u.mem_write(ds + 0x2d56, bytes(2))
    u.mem_write(ds + 0x598, struct.pack('<H', 0xa000))
    u.mem_write(0xa0000, struct.pack('<H', 32) * 2000)
    u.mem_write(0xa2000, struct.pack('<H', 0xe1) * 2000)

    def hook(uc, address, size, unused):
        # Keep the actual text writers and BCD score addition. Only the
        # graphics digit blits are foreign device output in this comparison.
        if address not in (0x196e0 + 0x3f28, 0x196e0 + 0x3f88):
            return
        sp = uc.reg_read(UC_X86_REG_SP)
        ip, cs = struct.unpack('<HH', uc.mem_read(0x80000 + sp, 4))
        uc.reg_write(UC_X86_REG_SP, sp + 12)
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    u.hook_add(UC_HOOK_CODE, hook)
    out = []
    for tick in range(ticks):
        u.mem_write(ds + 0x6596, struct.pack('<H', tick))
        if profile == 2:
            call(0x96e, 0x34a1, arguments=(pid ^ 1,))
        call(0x96e, 0x4d12, near=True)
        b = bytes(u.mem_read(ds, 65536))
        out += list(b[0x6894:0x689a])
        out += list(struct.unpack_from('<HHHi', b, 0x688a))
        out += [b[0x4b7c]] + list(b[0x4b64:0x4b74])
    out += list(struct.unpack('<2000H', u.mem_read(0xa0000, 4000)))
    out += list(struct.unpack('<2000H', u.mem_read(0xa2000, 4000)))
    return out


def transition_original(image, ticks):
    from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
    from unicorn.x86_const import UC_X86_REG_SP, UC_X86_REG_CS, UC_X86_REG_IP
    u, call = machine(image)
    ds = 0x2d560
    for at, value in ((0x2c0, 0xa800), (0x2c4, 200), (0x2c6, 80), (0x2c8, 0), (0x5e8, 65535), (0x2660, 0x1dc8)):
        u.mem_write(ds + at, struct.pack('<H', value))
    u.mem_write(ds + 0x2662, bytes(18))
    pixels = bytearray(640 * 200)
    color = 2

    def hardware(uc, address, size, unused):
        nonlocal color
        if address != 0x10f5c:
            return
        sp = uc.reg_read(UC_X86_REG_SP)
        ip, cs, color = struct.unpack('<HHH', uc.mem_read(0x80000 + sp, 6))
        uc.reg_write(UC_X86_REG_SP, sp + 8)
        uc.reg_write(UC_X86_REG_CS, cs)
        uc.reg_write(UC_X86_REG_IP, ip)

    def write(uc, access, address, size, value, unused):
        for byte in range(size):
            at = address + byte - 0xa8000
            if 0 <= at < 16000:
                mask = (value >> (byte * 8)) & 255
                for bit in range(8):
                    if mask & (128 >> bit):
                        pixels[at * 8 + bit] = color

    u.hook_add(UC_HOOK_CODE, hardware)
    u.hook_add(UC_HOOK_MEM_WRITE, write, begin=0xa8000, end=0xabfff)
    for _ in range(ticks):
        offset = struct.unpack('<H', u.mem_read(ds + 0x2660, 2))[0]
        call(0x96e, offset, near=True)
    offset = struct.unpack('<H', u.mem_read(ds + 0x2660, 2))[0]
    frame, midpoint = u.mem_read(ds + 0x2662, 2)
    phase = 1 if offset == 0x1dc8 else 2 if offset == 0x1f2a else 0
    return [phase, frame, midpoint, *struct.unpack('<8h', u.mem_read(ds + 0x2664, 16))], pixels


def branch_original(image, profile, frame, midpoint):
    from unicorn import UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_SP, UC_X86_REG_BP, UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_IP, UC_X86_REG_AX
    u, _ = machine(image)
    ds = 0x2d560
    winner = 1 if profile in (1, 2, 3) else 0
    u.mem_write(ds + 0x1d90, struct.pack('<HH', 0, 0x6000))
    u.mem_write(0x60017, bytes([winner]))
    u.mem_write(0x60028, bytes([1 if profile >= 2 else 0x81]))
    u.mem_write(0x60033, bytes([8 if profile == 5 else 0, 0 if profile == 3 else 2]))
    u.mem_write(ds + 0x65a6 + winner * 128 + 0x6c, bytes([2 if profile == 1 else 1]))
    u.mem_write(ds + 0x38dc, bytes((2, winner ^ 1)))
    u.mem_write(ds + 0x6596, struct.pack('<H', frame))
    u.mem_write(ds + 0x1188, struct.pack('<H', 460 if profile == 5 else 320))
    u.mem_write(ds + 0x2663, bytes([midpoint]))
    u.mem_write(ds + 0x2660, struct.pack('<H', 0x1f2a if midpoint else 0x1dc3))
    u.mem_write(ds + 0x688a, bytes(16))
    u.mem_write(ds + 0x4b64, bytes((3, 2, 1, 0, 0, 0, 0, 0, 6, 5, 4, 0, 0, 0, 0, 0)))
    hud = False

    def hook(uc, address, size, unused):
        nonlocal hud
        if address == 0x199b1:
            hud = True
            uc.emu_stop()
        elif address == 0x19921:
            uc.reg_write(UC_X86_REG_IP, 0x9924 - 0x96e0)  # Banner graphics is foreign here.
        elif address in (0x196e0 + 0x3f28, 0x196e0 + 0x3f88):
            sp = uc.reg_read(UC_X86_REG_SP)
            ip, cs = struct.unpack('<HH', uc.mem_read(0x80000 + sp, 4))
            uc.reg_write(UC_X86_REG_SP, sp + 12)
            uc.reg_write(UC_X86_REG_CS, cs)
            uc.reg_write(UC_X86_REG_IP, ip)

    u.hook_add(UC_HOOK_CODE, hook)
    for reg, value in ((UC_X86_REG_CS, 0x196e), (UC_X86_REG_DS, 0x2d56),
                       (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00), (UC_X86_REG_BP, 0xff00)):
        u.reg_write(reg, value)
    u.mem_write(0x8ff00, struct.pack('<HH', 0, 0xf000))
    u.emu_start(0x19918, 0x286e0, count=100000)
    if not hud and u.reg_read(UC_X86_REG_IP) != 0xf000:
        raise ValueError('original result branch did not reach HUD or return')
    offset = struct.unpack('<H', u.mem_read(ds + 0x2660, 2))[0]
    phase = 1 if offset == 0x1dc8 else 2 if offset == 0x1f2a else 0
    return [3 if hud else u.reg_read(UC_X86_REG_AX), u.mem_read(0x60034, 1)[0], *u.mem_read(0x60018, 16), phase]


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
    for case in ((0, 0, 0, 220), (1, 0, 0, 220), (0, 8, 0, 220), (1, 8, 1, 480), (0, 0, 2, 32)):
        native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--result', *map(str, case)], text=True).split()))
        expected = result_original(image, *case)
        if native != expected:
            index = next((i for i, pair in enumerate(zip(native, expected)) if pair[0] != pair[1]), min(len(native), len(expected)))
            raise ValueError(f'result {case}, index={index}: native={native[index:index + 10]}, original={expected[index:index + 10]}')
        print(f'Result rewards, complete BCD scores and TRAM characters/attributes agree: {case}', flush=True)
    with tempfile.TemporaryDirectory(prefix='th03-transition-') as work:
        for ticks in (1, 8, 16, 17, 24, 32):
            file = Path(work) / 'pixels.bin'
            output = str(file)
            if args.native_checks.suffix == '.exe':
                output = subprocess.check_output(['wslpath', '-w', output], text=True).strip()
            native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--transition', str(ticks), output], text=True).split()))
            expected, pixels = transition_original(image, ticks)
            if native != expected or file.read_bytes() != pixels:
                raise ValueError(f'transition {ticks}: native={native}, original={expected}; differing pixels={sum(a!=b for a,b in zip(file.read_bytes(),pixels))}')
            print(f'Complete transition state and masked raster agree at frame{ticks}', flush=True)
    disk = str(root / '.analysis/runtime/images/zun.hdi')
    if args.native_checks.suffix == '.exe':
        disk = subprocess.check_output(['wslpath', '-w', disk], text=True).strip()
    for profile in range(6):
        wait = 160 if profile in (0, 2, 3) else 460 if profile == 5 else 320
        for frame, midpoint in ((wait - 1, 0), (wait, 0), (wait + 16, 1)):
            case = profile, frame, midpoint
            native = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--round-end', disk, *map(str, case)], text=True).split()))
            expected = branch_original(image, *case)
            if native != expected:
                raise ValueError(f'result branch {case}: native={native}, original={expected}')
        print(f'Original round/match/story result routing, life debit and score commit agree: profile{profile}', flush=True)
    subprocess.run([str(args.native_checks.resolve()), '--restart-flow', disk], check=True)


if __name__ == '__main__':
    main()
