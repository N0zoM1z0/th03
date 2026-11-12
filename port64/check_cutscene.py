#!/usr/bin/env python3
"""Compare MAINL cutscene parsing and complete interpreter refresh traces."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import tomllib


def original_masks(image, packed):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INSN, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
    from unicorn import x86_const as reg
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        value = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (value + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    u.mem_write(0x1e3f0 + 0x1f0e, struct.pack('<HH', 0, 0x6000))
    for index, segment in enumerate((0xa800, 0xb000, 0xb800, 0xe000)):
        u.mem_write(0x1e3f0 + 0x1c60 + index * 4, struct.pack('<HH', 0, segment))
    u.mem_write(0x60000, packed)
    pixels = bytearray(640 * 400)

    def put_quarter(quarter):
        sx, sy = (quarter & 1) * 320, (quarter >> 1) * 200
        for y in range(200):
            for x in range(320):
                byte = packed[((sy + y) * 640 + sx + x) // 2]
                pixels[(64 + y) * 640 + 160 + x] = byte & 15 if x & 1 else byte >> 4
    put_quarter(0)
    row, latch, mask = bytes(160), 0, 65535

    def returning(count, far=True):
        sp = u.reg_read(reg.UC_X86_REG_SP)
        size = 4 if far else 2
        frame = struct.unpack('<' + 'H' * (size // 2), u.mem_read(0x80000 + sp, size))
        u.reg_write(reg.UC_X86_REG_SP, sp + size + count)
        if far:
            u.reg_write(reg.UC_X86_REG_CS, frame[1])
        u.reg_write(reg.UC_X86_REG_IP, frame[0])

    def code(uc, address, size, unused):
        nonlocal row
        if 0x10724 <= address < 0x10770 and bytes(uc.mem_read(address, 1)) == b'\xcb':
            # Normalize Unicorn's cached CS base at these real far returns.
            returning(0)
        elif address == 0x12c6e:
            sp = uc.reg_read(reg.UC_X86_REG_SP)
            width, offset, segment, top, left = struct.unpack('<5H', uc.mem_read(0x80000 + sp + 4, 10))
            if (width, top, left) != (320, 400, 0):
                raise ValueError('original masked-picture scratch row geometry changed')
            row = bytes(uc.mem_read(segment * 16 + offset, 160))
            returning(10)
        elif address == 0x195f0 + 0xbd7:
            returning(4, False)  # Page copy; both visible pages receive the resulting pixels.

    def output(uc, port, width, value, unused):
        nonlocal mask
        if port == 0x4a8:
            mask = value

    def read(uc, access, address, size, value, unused):
        nonlocal latch
        if 0xafd00 <= address < 0xafd28:
            latch = address - 0xafd00

    def write(uc, access, address, size, value, unused):
        # This helper uses EGC's word latch to copy all four source planes
        # through a single B-plane operand. Model only that device operation.
        if not 0xa8000 <= address < 0xafd00:
            return
        for bit in range(size * 8):
            if mask & (1 << (bit // 8 * 8 + 7 - bit % 8)):
                x = latch * 8 + bit
                byte = row[x // 2]
                pixels[(address - 0xa8000) * 8 + bit] = byte & 15 if x & 1 else byte >> 4

    u.hook_add(UC_HOOK_CODE, code)
    u.hook_add(UC_HOOK_INSN, output, None, 1, 0, reg.UC_X86_INS_OUT)
    u.hook_add(UC_HOOK_MEM_READ, read, begin=0xafd00, end=0xafd27)
    u.hook_add(UC_HOOK_MEM_WRITE, write, begin=0xa8000, end=0xafcff)
    frames = []
    for step in range(4):
        for register, value in ((reg.UC_X86_REG_CS, 0x195f), (reg.UC_X86_REG_DS, 0x1e3f), (reg.UC_X86_REG_SS, 0x8000), (reg.UC_X86_REG_SP, 0xff00)):
            u.reg_write(register, value)
        u.mem_write(0x8ff00, struct.pack('<5H', 0xf000, step, 1, 64, 160))
        u.emu_start(0x195f0 + 0xc4c, 0x195f0 + 0xf000, count=500000)
        if u.reg_read(reg.UC_X86_REG_IP) != 0xf000:
            raise ValueError('original masked picture helper did not return')
        frames.append(bytes(pixels) * 2)
    put_quarter(1)
    frames.append(bytes(pixels) * 2)
    return frames


def original_trace(image, raw, keys):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_CODE, UC_HOOK_INSN
    from unicorn import x86_const as reg
    u = Uc(UC_ARCH_X86, UC_MODE_16)
    u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        value = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (value + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    ds, stack = 0x1e3f0, 0x80000
    u.mem_write(ds + 0x21d6, struct.pack('<HH', 0, 0x6000))
    u.mem_write(0x60000, raw)
    for register, value in ((reg.UC_X86_REG_CS, 0x195f), (reg.UC_X86_REG_DS, 0x1e3f),
                            (reg.UC_X86_REG_SS, 0x8000), (reg.UC_X86_REG_SP, 0xff00)):
        u.reg_write(register, value)
    u.mem_write(stack + 0xff00, struct.pack('<H', 0xf000))
    # Only graphics/storage interfaces are foreign. The actual interpreter,
    # parameter readers, cursor and palette fades execute unchanged.
    models = {0x17d0: ('palette', 0, 0, 4), 0x2064: ('vsync', 0, 0, 4),
              0x1700: ('scroll', 2, 2, 4), 0xf58: ('gaiji', 8, 8, 4),
              0xfec: ('free', 8, 8, 4), 0xe72: ('clear', 0, 0, 4),
              0xeac: ('copy', 2, 2, 4), 0xc36: ('color', 4, 4, 4),
              0xc60: ('off', 0, 0, 4), 0xb9e: ('fill', 8, 8, 4),
              0x3641: ('lower', 2, 0, 4)}
    shared = {0x372: ('delay', 2, 2), 0xdc2: ('input', 0, 0), 0x9b7: ('font', 10, 10),
              0xccb: ('load', 6, 6), 0x52a: ('pi_palette', 2, 2), 0x54f: ('pi', 6, 6),
              0xd11: ('quarter', 8, 8), 0xc1c: ('measure', 4, 4),
              0xc9a: ('ok', 2, 2), 0xc4d: ('ok', 4, 4),
              0xa0: ('music_load', 6, 0), 0x6e2: ('control', 2, 2), 0x66a: ('effect', 2, 2)}
    models.update({0xc7e0 + offset: (name, count, clean, 4) for offset, (name, count, clean) in shared.items()})
    models.update({0x95f0 + offset: (name, count, count, 2) for offset, name, count in
                   ((0xd7b, 'snapshot', 0), (0xe4c, 'free_box', 0), (0xe6b, 'restore', 0),
                    (0xbd7, 'copy_pic', 4), (0xc4c, 'masked_pic', 8))})
    trace = []
    age = shown = tone = scroll = sounds = 0
    halted = False
    sound_events = []

    def get(register):
        return u.reg_read(getattr(reg, 'UC_X86_REG_' + register))

    def state(done=0):
        data = bytes(u.mem_read(ds + 0x21d6, 20))
        word = lambda at: struct.unpack_from('<h', data, at)[0]
        return [struct.unpack_from('<H', data)[0], word(10), word(12), word(14), data[16], data[17] >> 4,
                data[8], shown, tone, scroll, word(18), u.mem_read(0x8fefc, 1)[0], sounds, done]

    def elapse(frames):
        nonlocal age, halted
        for _ in range(frames):
            trace.append(state())
            if age >= len(keys) - 1:
                halted = True
                u.emu_stop()
                return
            age += 1

    def hook(uc, address, size, unused):
        nonlocal tone, scroll, sounds
        relative = address - 0x10000
        if relative not in models:
            return
        name, count, clean, retbytes = models[relative]
        sp = get('SP')
        frame = struct.unpack('<' + 'H' * ((retbytes + count) // 2), uc.mem_read(stack + sp, retbytes + count))
        args = frame[retbytes // 2:]
        if name in ('delay', 'measure'):
            elapse(args[0])
        elif name == 'vsync':
            elapse(1)
        elif name == 'palette':
            tone = struct.unpack('<H', uc.mem_read(ds + 0x578, 2))[0]
        elif name == 'scroll':
            scroll = args[0]
        elif name == 'input':
            uc.mem_write(ds + 0x1d0c, struct.pack('<H', keys[age]))
        elif name == 'ok':
            remaining = args[0]
            while not keys[age] & 0x2020 and remaining:
                elapse(1)
                if halted:
                    return
                remaining -= 1
            uc.mem_write(ds + 0x1d0c, struct.pack('<H', keys[age]))
        elif name in ('music_load', 'control', 'effect'):
            sounds += 1
            if name == 'music_load':
                if args[2] != 0x600:
                    raise ValueError('cutscene requested an unexpected sound-bank load')
                filename = bytes(uc.mem_read(args[1] * 16 + args[0], 16)).split(b'\0')[0].decode('ascii')
                sound_events.append([0, 0, filename])
            else:
                sound_events.append([1 if name == 'control' else 2, args[0], ''])
        elif name == 'lower':
            uc.reg_write(reg.UC_X86_REG_AX, args[0] + 32 if 65 <= args[0] <= 90 else args[0])
        elif name == 'gaiji':
            # The real ADC prefix is covered by the bounded parameter/gaiji
            # comparison; its AND clears CF before the second page call.
            uc.reg_write(reg.UC_X86_REG_EFLAGS, get('EFLAGS') & ~1)
        if halted:
            return
        uc.reg_write(reg.UC_X86_REG_SP, sp + retbytes + clean)
        uc.reg_write(reg.UC_X86_REG_CS, frame[1] if retbytes == 4 else 0x195f)
        uc.reg_write(reg.UC_X86_REG_IP, frame[0])

    def output(uc, port, width, value, unused):
        nonlocal shown
        if width != 1 or port not in (0xa4, 0xa6):
            raise ValueError(f'unexpected interpreter output {port:x}/{width}')
        if port == 0xa4:
            shown = value & 1

    u.hook_add(UC_HOOK_CODE, hook)
    u.hook_add(UC_HOOK_INSN, output, None, 1, 0, reg.UC_X86_INS_OUT)
    u.emu_start(0x195f0 + 0x167e, 0x195f0 + 0xf000, count=5000000)
    if not halted and get('IP') != 0xf000:
        raise ValueError('original interpreter did not return or reach the requested refresh')
    if not halted:
        final = state(1)
        trace.extend([final] * (len(keys) - len(trace)))
    return trace, sound_events


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--native-checks', type=Path, required=True)
    parser.add_argument('--dos-root', type=Path, required=True)
    args = parser.parse_args()
    root = args.dos_root.resolve()
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    from review_th03_mainl_cutscene import parameter_case
    raw = (root / '.analysis/toolchain/wineprefix/drive_c/TH03PKG/af1409l/r1/mainl.exe').read_bytes()
    manifest = tomllib.loads((root / 'config/th03_diet.toml').read_text())
    expected = next(row['decoded_sha256'] for row in manifest['artifacts'] if row['id'] == 'th03-mainl')
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('original MAINL identity changed')
    image = parse_mz(raw)
    executable = str(args.native_checks.resolve())

    def path(file):
        return subprocess.check_output(['wslpath', '-w', str(file)], text=True).strip() if args.native_checks.suffix == '.exe' else str(file)

    def parse_reply(reply):
        trace, sounds = [], []
        for line in reply.splitlines():
            if line.startswith('sound\t'):
                _, kind, value, name = line.split('\t')
                sounds.append([int(kind), int(value), name])
            else:
                trace.append(list(map(int, line.split())))
        return trace, sounds

    for text, second, offset in (('x', False, 0), ('7x', False, 0), ('12x', False, 65534), ('999x', False, 65535), (',12x', True, 65534), ('!x', True, 0)):
        original = parameter_case(image, text, offset, second)
        actual = list(map(int, subprocess.check_output([executable, '--script-parameter', text, str(offset), str(int(second)), '73'], text=True).split()))
        if actual != [original['value'], original['final_offset'], original['carry']]:
            raise ValueError(f'parameter rewind/default/comma/carry differs: {text, second, offset}: {actual} != {original}')
    print('Parameter defaults, eager reads/rewinds, commas, WORD wrap and carry agree with MAINL.', flush=True)
    disk = root / '.analysis/runtime/images/zun.hdi'
    font = root / '.analysis/runtime/fonts/FREECG98.BMP'
    with tempfile.TemporaryDirectory(prefix='th03-cutscene-') as work:
        picture = Path(work) / 'frame.ppm'
        text = Path(work) / 'script.txt'
        packed = Path(work) / 'picture.bin'
        subprocess.run([str(args.native.resolve()), '--hdi', str(disk), '--pi', 'DM1A.PI', '--packed', str(packed)], check=True)
        expected_pixels = original_masks(image, packed.read_bytes())
        text.write_bytes(b'\\p,DM1A.PI \\=0 \\==1,1 \\w999 \\$')
        for step, expected_frame in enumerate(expected_pixels):
            output = Path(work) / 'pages.bin'
            subprocess.check_output([executable, '--cutscene-pixels', path(disk), path(font), path(text), ','.join(['0'] * step), path(output)], text=True)
            if output.read_bytes() != expected_frame:
                raise ValueError(f'complete original masked picture pages differ at step{step}')
        print('All four EGC mask steps and the final picture agree in every pixel of both pages.', flush=True)
        synthetic = [b'\\v2' + 'あ'.encode('cp932') * 5 + b'\\t200\\wi2\\fo1\\$',
                     b'\\c4\\b3\\ga28\\ga29\\g2\\s3\\c\\b\\w4\\k128\\$',
                     b'\\v1' + 'い'.encode('cp932') * 115 + b'\\s-\\n\\n\\n\\n\\$',
                     b'\\p,DM1A.PI \\pp\\==2,2\\p=\\vp1\\@\\=4\\p-\\$',
                     b'\\wk3\\wm4,2\\wmk5,8\\m,DEMO1.M \\fm3\\m$\\m*\\e7\\$']
        profiles = [[0] * 400, [0] + [32] * 399, [0] + [4096] * 399,
                    [0] * 25 + [32] * 4 + [0] * 4 + [32] * 367]
        for index, source in enumerate(synthetic):
            source += bytes(3)  # Actual bytes for the speculative parameter reads.
            text.write_bytes(source)
            for profile, keys in enumerate(profiles):
                expected_trace, expected_sounds = original_trace(image, source, keys)
                reply = subprocess.check_output([executable, '--cutscene-trace', path(disk), path(font), path(text), ','.join(map(str, keys[1:])), path(picture)], text=True)
                actual, sounds = parse_reply(reply)
                if actual != expected_trace or sounds != expected_sounds:
                    mismatch = next(((tick, a, b) for tick, (a, b) in enumerate(zip(actual, expected_trace)) if a != b), (len(actual), len(expected_trace)))
                    raise ValueError(f'interpreter case{index}/input{profile}: {mismatch}')
            print(f'Interpreter state at every refresh agrees: script{index}, four input profiles.', flush=True)
        keys = [0] + [4096] * 1499
        names = [f'@{character:02}{suffix}.TXT' for character in range(9) for suffix in ('DM0', 'DM1', 'ED')] + ['@99ED.TXT']
        for name in names:
            subprocess.run([str(args.native.resolve()), '--hdi', str(disk), '--extract', name, '--output', str(text)], check=True)
            source = text.read_bytes()
            expected_trace, expected_sounds = original_trace(image, source, keys)
            reply = subprocess.check_output([executable, '--cutscene-trace', path(disk), path(font), name, ','.join(map(str, keys[1:])), path(picture)], text=True)
            actual, sounds = parse_reply(reply)
            if actual != expected_trace or sounds != expected_sounds or not actual[-1][-1]:
                mismatch = next(((tick, a, b) for tick, (a, b) in enumerate(zip(actual, expected_trace)) if a != b), 'script did not stop')
                raise ValueError(f'complete original script {name}: {mismatch}')
            print(f'Complete {name} interpreter trace agrees through STOP.', flush=True)
        subprocess.run([executable, '--cutscene-flow', path(disk), path(font)], check=True)


if __name__ == '__main__':
    main()
