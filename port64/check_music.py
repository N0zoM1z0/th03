#!/usr/bin/env python3
"""Compare native Music Room with original OP control, storage and polygons."""
import argparse
import hashlib
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import tomllib


def machine(image, cs=0x1990):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_16
    from unicorn import x86_const as reg
    u = Uc(UC_ARCH_X86, UC_MODE_16);u.mem_map(0, 0x100000)
    program = bytearray(image.program_image)
    for relocation in image.relocations:
        value = struct.unpack_from('<H', program, relocation.linear)[0]
        struct.pack_into('<H', program, relocation.linear, (value + 0x1000) & 65535)
    u.mem_write(0x10000, bytes(program))
    for name, value in (('CS', cs), ('DS', 0x1d7f), ('SS', 0x8000), ('SP', 0xff00)):
        u.reg_write(getattr(reg, 'UC_X86_REG_' + name), value)
    u.mem_write(0x8ff00, struct.pack('<HH', 0xf000, cs))
    return u


class PolygonRaster:
    """Original GRCG_POLYGON_C plus its actual edge/trapezoid helpers."""
    def __init__(self, image):
        from unicorn import UC_HOOK_MEM_WRITE
        from unicorn import x86_const as reg
        self.u = machine(image, 0x1000);self.reg = reg
        self.u.mem_write(0x1d7f0 + 0x27e, struct.pack('<8H', 0, 639, 639, 0, 399, 399, 0xa800, 31920))
        self.u.mem_write(0x1d7f0 + 0x2c0, struct.pack('<5H', 0xa800, 40, 400, 80, 0))
        self.mask = bytearray(32000)

        def write(uc, access, address, size, value, unused):
            for i in range(size):
                at = address + i - 0xa8000
                if 0 <= at < 32000:
                    self.mask[at] |= (value >> (i * 8)) & 255
        self.u.hook_add(UC_HOOK_MEM_WRITE, write, begin=0xa8000, end=0xafcff)

    def draw(self, points, count):
        u, reg = self.u, self.reg
        self.mask = bytearray(32000)
        u.mem_write(0xa8000, bytes(32000));u.mem_write(0x60000, points)
        for name, value in (('CS', 0x1000), ('DS', 0x1d7f), ('SS', 0x8000), ('SP', 0xff00)):
            u.reg_write(getattr(reg, 'UC_X86_REG_' + name), value)
        u.mem_write(0x8ff00, struct.pack('<5H', 0xf000, 0x1000, count, 0, 0x6000))
        u.emu_start(0x10c6a, 0x1f000, count=1000000)
        if u.reg_read(reg.UC_X86_REG_IP) != 0xf000:
            raise ValueError('original polygon raster did not return')
        return bytes(self.mask)


class FontDevice:
    """Previously checked TH03 C++ font renderer used as a foreign device."""
    def __init__(self, executable, font):
        self.process = subprocess.Popen([executable, '--font-service', font], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.cache = {}

    def draw(self, x, y, fx, text):
        key = x, y, fx >> 4, text
        if key not in self.cache:
            self.process.stdin.write(struct.pack('<4H', x, y, fx >> 4, len(text)) + text)
            self.process.stdin.flush()
            mask = self.process.stdout.read(32000)
            if len(mask) != 32000:
                raise ValueError('native font device closed early')
            self.cache[key] = mask
        return self.cache[key]

    def close(self):
        self.process.stdin.close()
        if self.process.wait() != 0:
            raise ValueError('native font device failed')
        self.process.stdout.close()


def original(image, packed, comments, keys, expected, font, output):
    from unicorn import UC_HOOK_CODE, UC_HOOK_INSN
    from unicorn import x86_const as reg
    u = machine(image);raster = PolygonRaster(image)
    ds, stack = 0x1d7f0, 0x80000
    planes = (0xa8000, 0xb0000, 0xb8000, 0xe0000)
    pages = [[bytes(32000) for _ in planes] for _ in range(2)]
    at = frames = accessed = shown = file_position = allocations = 0
    stopped = False
    trace, sounds = [], []
    snapshots = {int(p.name[len(output.name) + 6:-7]): p for p in output.parent.glob(output.name + '.frame*.pixels')}
    raster_frames = set()
    for target in [*snapshots, len(expected) - 1]:
        raster_frames.update(range(max(0, target - 3), target + 1))

    def compare_picture(path):
        store_page();pixels = bytearray(512000)
        for page in range(2):
            for plane in range(4):
                for i, byte in enumerate(pages[page][plane]):
                    if not byte:
                        continue
                    for bit in range(8):
                        if byte & (128 >> bit):
                            pixels[page * 256000 + i * 8 + bit] |= 1 << plane
        actual = path.read_bytes()
        if actual != pixels:
            where = next(i for i, (a, b) in enumerate(zip(actual, pixels)) if a != b)
            raise ValueError(f'Music {path.name} pixels differ: page{where // 256000}, x{where % 640}, y{where // 640 % 400}: native={actual[where]}, original={pixels[where]}')

    def get(name):
        return u.reg_read(getattr(reg, 'UC_X86_REG_' + name))

    def args(n):
        return struct.unpack('<' + 'H' * n, u.mem_read(stack + get('SP') + 4, n * 2))

    def returning(clean=0):
        sp = get('SP');ip, cs = struct.unpack('<HH', u.mem_read(stack + sp, 4))
        u.reg_write(reg.UC_X86_REG_SP, sp + clean + 4);u.reg_write(reg.UC_X86_REG_CS, cs);u.reg_write(reg.UC_X86_REG_IP, ip)

    def text(segment, offset):
        return bytes(u.mem_read(segment * 16 + offset, 128)).split(b'\0')[0]

    def store_page():
        for i, address in enumerate(planes):
            pages[accessed][i] = bytes(u.mem_read(address, 32000))

    def state(done=0):
        selected, page = u.mem_read(ds + 0x2038, 2)
        initialized, playing = u.mem_read(ds + 0x692, 2)
        seed = struct.unpack('<I', u.mem_read(ds + 0x312, 4))[0]
        row = [selected, playing, page, accessed, shown, initialized, seed, frames, done]
        for i in range(16):
            row += list(struct.unpack('<2h', u.mem_read(ds + 0x1f98 + i * 4, 4)))
            row += list(struct.unpack('<2h', u.mem_read(ds + 0x1fd8 + i * 4, 4)))
            row += [u.mem_read(ds + 0x2018 + i, 1)[0], u.mem_read(ds + 0x2028 + i, 1)[0]]
        index = len(trace)
        if index >= len(expected) or row != expected[index]:
            raise ValueError(f'Music frame{index}: original={row[:10]}, native={expected[index][:10] if index < len(expected) else None}; first fields={[i for i, (a, b) in enumerate(zip(row, expected[index])) if a != b][:12] if index < len(expected) else []}')
        if index in snapshots:
            compare_picture(snapshots[index])
        trace.append(row)

    def code(uc, address, size, unused):
        nonlocal at, frames, file_position, allocations, stopped
        if address == 0x1beb0 + 0xcd6:
            frames += 1;state()
            if at + 1 >= len(keys):
                stopped = True;uc.emu_stop();return
            at += 1;returning(2)
        elif address == 0x1beb0 + 0xad6:
            uc.mem_write(ds + 0x1aa6, struct.pack('<H', keys[at]));returning()
        elif address == 0x10000 + 0xc6a:
            count, offset, segment = args(3)
            # Polygons only write B, which is restored in full before each
            # frame and each comment. Render the four frames preceding each
            # requested snapshot to cover both pages at that observation.
            if at in raster_frames:
                points = bytes(uc.mem_read(segment * 16 + offset, (count + 1) * 4))
                mask = raster.draw(points, count)
                before = int.from_bytes(uc.mem_read(planes[0], 32000), 'little')
                uc.mem_write(planes[0], (before | int.from_bytes(mask, 'little')).to_bytes(32000, 'little'))
            returning(6)
        elif address == 0x1beb0 + 0x82b:
            offset, segment, fx, y, x = args(5)
            mask = int.from_bytes(font.draw(x, y, fx, text(segment, offset)), 'little')
            for plane, address in enumerate(planes):
                before = int.from_bytes(uc.mem_read(address, 32000), 'little')
                uc.mem_write(address, ((before & ~mask) | (mask if fx & (1 << plane) else 0)).to_bytes(32000, 'little'))
            returning(10)
        elif address == 0x10000 + 0x24ca:
            allocation = (0x5000, 0x6000, 0x6400, 0x6800, 0x6c00)[allocations]
            allocations += 1;u.reg_write(reg.UC_X86_REG_AX, allocation);returning(2)
        elif address == 0x10000 + 0x9e4:
            origin, low, high = args(3);file_position = low + (high << 16);returning(6)
        elif address == 0x10000 + 0x8f4:
            count, offset, segment = args(3)
            uc.mem_write(segment * 16 + offset, comments[file_position:file_position + count]);returning(6)
        elif address == 0x10000 + 0x114c:
            for address in planes:
                uc.mem_write(address, bytes(32000))
            returning()
        elif address == 0x10000 + 0x1186:
            store_page();dest = args(1)[0];pages[dest] = list(pages[accessed]);returning(2)
        elif address == 0x1beb0 + 0x4cb:
            for plane, address in enumerate(planes):
                data = bytearray(32000)
                for i, byte in enumerate(packed):
                    first, second = byte >> 4, byte & 15
                    if first & (1 << plane):
                        data[i // 4] |= 128 >> (i % 4 * 2)
                    if second & (1 << plane):
                        data[i // 4] |= 64 >> (i % 4 * 2)
                uc.mem_write(address, bytes(data))
            returning(6)
        elif address == 0x1beb0 + 0x553:
            sounds.append([1, args(1)[0], '']);returning(2)
        elif address == 0x1beb0 + 0xa2:
            offset, segment, kind = args(3);sounds.append([0, 0, text(segment, offset).decode()]);returning()
        else:
            clean = services.get(address)
            if clean is None:
                raise ValueError(f'unknown Music service {address:x}')
            returning(clean)

    def output_port(uc, port, width, value, unused):
        nonlocal accessed, shown
        if port == 0xa6:
            store_page();accessed = value & 1
            for i, address in enumerate(planes):
                uc.mem_write(address, pages[accessed][i])
        elif port == 0xa4:
            shown = value & 1
        else:
            raise ValueError(f'unexpected Music port {port:x}')

    services = {0x10000 + offset: clean for offset, clean in ((0x25ce, 2), (0xec6, 4), (0xef0, 0), (0x9a8, 4), (0x888, 0), (0x269a, 0), (0x21f4, 0), (0x1aa4, 0), (0x12dc, 8))}
    services.update({0x1beb0 + offset: clean for offset, clean in ((0x7ec, 2), (0xa90, 6), (0x4a6, 2))})
    addresses = [0x1beb0 + n for n in (0xcd6, 0xad6, 0x82b, 0x4cb, 0x553, 0xa2)]
    addresses += [0x10000 + n for n in (0xc6a, 0x24ca, 0x9e4, 0x8f4, 0x114c, 0x1186)]
    for address in addresses + list(services):
        u.hook_add(UC_HOOK_CODE, code, begin=address, end=address)
    u.hook_add(UC_HOOK_INSN, output_port, None, 1, 0, reg.UC_X86_INS_OUT)
    for i, address in enumerate(planes):
        u.mem_write(ds + 0x19fa + i * 4, struct.pack('<HH', 0, address // 16))
    u.emu_start(0x19900 + 0x1306, 0x28900, count=100000000)
    if not stopped:
        if get('IP') != 0xf000:
            raise ValueError('original Music Room did not return')
        state(1)
    if len(trace) != len(expected):
        raise ValueError(f'Music trace lengths differ: original={len(trace)}, native={len(expected)}')
    compare_picture(output)
    return sounds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--native-checks', type=Path, required=True)
    parser.add_argument('--dos-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args();root = args.dos_root.resolve()
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    raw = (root / '.analysis/toolchain/wineprefix/drive_c/TH03PKG/af1409l/r1/op.exe').read_bytes()
    manifest = tomllib.loads((root / 'config/th03_diet.toml').read_text())
    expected = next(a['decoded_sha256'] for a in manifest['artifacts'] if a['id'] == 'th03-op')
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('original OP identity changed')
    disk = root / '.analysis/runtime/images/zun.hdi';font = root / '.analysis/runtime/fonts/FREECG98.BMP'
    config = tomllib.loads((root / 'config/targets.toml').read_text())
    if hashlib.sha256(disk.read_bytes()).hexdigest() != config['source']['hdi_sha256']:
        raise ValueError('original HDI identity changed')
    out = args.output.resolve();out.mkdir(parents=True, exist_ok=True)
    native, checks = str(args.native.resolve()), str(args.native_checks.resolve())

    def path(file):
        return subprocess.check_output(['wslpath', '-w', str(file)], text=True).strip() if args.native_checks.suffix == '.exe' else str(file)

    packed, comments = out / 'background.bin', out / 'comments.txt'
    subprocess.run([native, '--hdi', str(disk), '--pi', 'OP3.PI', '--packed', str(packed)], check=True)
    subprocess.run([native, '--hdi', str(disk), '--extract', 'MUSIC.TXT', '--output', str(comments)], check=True)
    profiles = [('idle-resets', [0] * 650), ('last-song', [32, 32, 0, 1, 1, 0, 1, 0, 32, 32, 0, 0]),
                ('all-songs-exit', [0, 32, 32, 0] + [mask for _ in range(18) for mask in (2, 0, 32, 32, 0)] + [4096, 4096, 0]),
                ('quit-entry', [0, 1, 0, 32, 32, 0]), ('simultaneous', [0, 3, 3, 0, 4, 0, 2, 0, 4128, 4128, 0])]
    malformed = subprocess.run([checks, '--font-service', path(font)], input=struct.pack('<4H', 0, 0, 2, 4) + b'x', capture_output=True)
    if malformed.returncode == 0 or b'font service request truncated' not in malformed.stderr:
        raise ValueError('font service accepted a truncated text request')
    device = FontDevice(checks, path(font))
    try:
        for name, keys in profiles:
            picture = out / (name + '.pixels')
            reply = subprocess.check_output([checks, '--music-run', path(disk), path(font), ','.join(map(str, keys)), path(picture)], text=True)
            trace, sounds = [], []
            for line in reply.splitlines():
                if line.startswith('sound\t'):
                    _, kind, value, song = line.split('\t');sounds.append([int(kind), int(value), song])
                else:
                    trace.append(list(map(int, line.split())))
            expected_sounds = original(parse_mz(raw), packed.read_bytes(), comments.read_bytes(), keys, trace, device, picture)
            if expected_sounds != sounds:
                raise ValueError(f'Music sound requests differ: {name}: {expected_sounds} != {sounds}')
            (out / (name + '.trace')).write_text(reply)
            print(f'{name}: {len(trace)} complete original Music states, song requests and both graphics pages agree.', flush=True)
    finally:
        device.close()
    with tempfile.TemporaryDirectory(prefix='th03-music-flow-') as work:
        subprocess.run([checks, '--music-flow', path(disk), path(font), path(work)], check=True)


if __name__ == '__main__':
    main()
