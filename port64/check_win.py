#!/usr/bin/env python3
"""Compare MAINL winner resources/messages and story dispatch with original code."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import tomllib


def original_message(image, files, p0, p1, winner, stage):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_SP, UC_X86_REG_IP
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds = 0x1e3f0
    u.mem_write(ds + 0x21ea, struct.pack('<HH', 0, 0x6000))
    u.mem_write(ds + 0x13f3, bytes((p0 - 1, p1 - 1)))
    u.mem_write(0x60017, bytes([winner]))
    u.mem_write(0x60033, bytes([stage]))
    file, position, portrait, palette = b'', 0, '', 0
    models = {0x1a68: 4, 0x17d0: 0, 0xc7e0 + 0x934: 6, 0xc7e0 + 0x73e: 8,
              0xc7e0 + 0x7c8: 8, 0x966: 4, 0x9a2: 6, 0x8b2: 6, 0x846: 0}

    def string(offset, segment):
        return bytes(u.mem_read(segment * 16 + offset, 64)).split(b'\0')[0].decode('ascii').upper()

    def hook(uc, address, size, unused):
        nonlocal file, position, portrait, palette
        relative = address - 0x10000
        if relative not in models:
            return
        sp = uc.reg_read(UC_X86_REG_SP)
        frame = list(struct.unpack('<' + 'H' * (2 + models[relative] // 2), uc.mem_read(0x80000 + sp, 4 + models[relative])))
        args = frame[2:]
        if relative == 0xc7e0 + 0x7c8:
            palette, portrait = args[0], string(args[1], args[2])
            if args[3] != 6:
                raise ValueError('original winner picture slot changed')
        elif relative == 0x966:
            file = files[string(*args)]
        elif relative == 0x9a2:
            if args[0]:
                raise ValueError('original winner seek is not absolute')
            position = args[1] | (args[2] << 16)
        elif relative == 0x8b2:
            count, offset, segment = args
            uc.mem_write(segment * 16 + offset, file[position:position + count])
            position += count
        uc.reg_write(UC_X86_REG_SP, sp + 4 + models[relative])
        uc.reg_write(UC_X86_REG_CS, frame[1])
        uc.reg_write(UC_X86_REG_IP, frame[0])

    u.hook_add(UC_HOOK_CODE, hook)
    for reg, value in ((UC_X86_REG_CS, 0x195f), (UC_X86_REG_DS, 0x1e3f), (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
        u.reg_write(reg, value)
    u.mem_write(0x8ff00, struct.pack('<H', 0xf000))
    u.emu_start(0x195f0 + 0x34, 0x195f0 + 0xf000, count=10000)
    if u.reg_read(UC_X86_REG_IP) != 0xf000:
        raise ValueError('original win_load did not return')
    lines = []
    for at in (0x133c, 0x1379, 0x13b6):
        lines += list(u.mem_read(ds + at, 60))
        if u.mem_read(ds + at + 60, 1)[0]:
            raise ValueError('original win_load did not terminate each line')
    return [int(portrait[:2]) // 2, palette, (position - 180) // 180, *lines]


def original_animation(image):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_SS, UC_X86_REG_SP, UC_X86_REG_IP
    from review_th03_mainl_root import FAR
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        old = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (old + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds = 0x1e3f0
    u.mem_write(ds + 0x21ea, struct.pack('<HH', 0, 0x6000))
    u.mem_write(0x60028, b'\x01')
    u.mem_write(0x60029, bytes((1, 3, 5, 7, 9, 11, 13, 15, 17)))
    u.mem_write(0x60033, b'\x01')
    models = {segment * 16 + offset: (name, size, clean, 4)
              for (segment, offset), (name, size, clean) in FAR.items()
              if name not in ('black_in', 'black_out', 'white_in')}
    models.update({0x2064: ('vsync', 0, 0, 4), 0x95f0 + 0x14e: ('text', 0, 0, 2),
                   0x95f0 + 0x31c: ('stage', 0, 0, 2)})
    age, cel, tone, waiting = 0, 0, 0, False
    trace = []

    def wait(frames):
        nonlocal age
        for _ in range(frames):
            trace.append([age, cel, tone, int(waiting), 0])
            age += 1

    def hook(uc, address, size, unused):
        nonlocal cel, tone, waiting
        relative = address - 0x10000
        if relative == 0x57a:
            waiting = False
        if relative not in models:
            return
        name, count, clean, retbytes = models[relative]
        sp = uc.reg_read(UC_X86_REG_SP)
        frame = list(struct.unpack('<' + 'H' * ((retbytes + count) // 2), uc.mem_read(0x80000 + sp, retbytes + count)))
        args = frame[retbytes // 2:]
        if name == 'palette':
            tone = struct.unpack('<H', uc.mem_read(ds + 0x578, 2))[0]
        elif name == 'vsync':
            wait(1)
        elif name in ('delay', 'measure_delay'):
            wait(args[0])  # snd_delay_until_measure's no-BGM branch.
        elif name == 'cdg_put' and args[0] <= 5:
            cel = args[0]
        elif name == 'text':
            waiting = True
        elif name == 'input':
            uc.mem_write(ds + 0x1d0c, struct.pack('<H', 32 if age >= 177 else 0))
        uc.reg_write(UC_X86_REG_SP, sp + retbytes + clean)
        uc.reg_write(UC_X86_REG_CS, frame[1] if retbytes == 4 else 0x195f)
        uc.reg_write(UC_X86_REG_IP, frame[0])

    u.hook_add(UC_HOOK_CODE, hook)
    for reg, value in ((UC_X86_REG_CS, 0x195f), (UC_X86_REG_DS, 0x1e3f), (UC_X86_REG_SS, 0x8000), (UC_X86_REG_SP, 0xff00)):
        u.reg_write(reg, value)
    u.mem_write(0x8ff00, struct.pack('<H', 0xf000))
    u.emu_start(0x195f0 + 0x19d, 0x195f0 + 0xf000, count=100000)
    if u.reg_read(UC_X86_REG_IP) != 0xf000:
        raise ValueError('original win animation did not return')
    trace.append([age, cel, tone, int(waiting), 1])
    return trace


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--native-checks', type=Path, required=True)
    parser.add_argument('--dos-root', type=Path, required=True)
    args = parser.parse_args()
    root = args.dos_root.resolve()
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    from review_th03_mainl_root import RootProbe
    raw = (root / '.analysis/toolchain/wineprefix/drive_c/TH03PKG/af1409l/r1/mainl.exe').read_bytes()
    manifest = tomllib.loads((root / 'config/th03_diet.toml').read_text())
    expected = next(row['decoded_sha256'] for row in manifest['artifacts'] if row['id'] == 'th03-mainl')
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('original MAINL identity changed')
    image = parse_mz(raw)
    disk = str(root / '.analysis/runtime/images/zun.hdi')
    font = str(root / '.analysis/runtime/fonts/FREECG98.BMP')
    files = {}
    with tempfile.TemporaryDirectory(prefix='th03-win-') as work:
        for char in range(9):
            name = f'@{char:02}TX.TXT'
            path = Path(work) / name
            subprocess.run([str(args.native.resolve()), '--hdi', disk, '--extract', name, '--output', str(path)], check=True)
            files[name] = path.read_bytes()
    if args.native_checks.suffix == '.exe':
        disk, font = (subprocess.check_output(['wslpath', '-w', path], text=True).strip() for path in (disk, font))
    cases = []
    for char in range(9):
        for palette in range(2):
            selected, other = char * 2 + palette + 1, 14 if char != 6 else 5
            cases.append((other, selected, 1, 1, 1) if char & 1 else (selected, other, 0, 1, 1))
    cases += [(5, 14, winner, stage, mode) for winner, stage, mode in ((0, 6, 1), (0, 7, 1), (0, 8, 1), (0, 9, 1), (1, 7, 1), (0, 1, 0x81), (1, 1, 0x81))]
    for p0, p1, winner, stage, mode in cases:
        original = original_message(image, files, p0, p1, winner, stage)
        probe = RootProbe(image)
        probe.resident(mode=mode, winner=winner, stage=stage, p1=p0, p2=p1)
        probe.uc.mem_write(0x50029, bytes((1, 3, 5, 7, 9, 11, 13, 15, 17, 42)))
        probe.run(0x297)
        original += [probe.get('AX'), probe.uc.mem_read(0x5000d, 1)[0]]
        actual = list(map(int, subprocess.check_output([str(args.native_checks.resolve()), '--win-message', disk, *map(str, (p0, p1, winner, stage, mode))], text=True).split()))
        if actual != original:
            raise ValueError(f'winner resource/message/route differs: {(p0, p1, winner, stage, mode)}: {actual[:3] + actual[-2:]} != {original[:3] + original[-2:]}')
    print(f'{len(cases)} MAINL winner resource, palette, complete message and story-route cases agree with original instructions.', flush=True)
    expected_clock = original_animation(image)
    actual_clock = [list(map(int, line.split())) for line in subprocess.check_output([str(args.native_checks.resolve()), '--win-clock', disk, font], text=True).splitlines()]
    if actual_clock != expected_clock:
        mismatch = next((pair for pair in zip(actual_clock, expected_clock) if pair[0] != pair[1]), (len(actual_clock), len(expected_clock)))
        raise ValueError(f'original winner animation clock differs: {mismatch}')
    print('Every winner-animation refresh agrees with original logo calls and real palette fade instructions under the no-BGM timing profile.', flush=True)
    subprocess.run([str(args.native_checks.resolve()), '--win-flow', disk, font], check=True)


if __name__ == '__main__':
    main()
