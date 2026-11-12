#!/usr/bin/env python3
"""Compare YUME.CFG layout with original OP and reload native process saves."""
import argparse
import hashlib
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--native-checks', type=Path, required=True)
    parser.add_argument('--dos-root', type=Path, required=True)
    args = parser.parse_args();root = args.dos_root.resolve()
    sys.path.insert(0, str(root / 'scripts'))
    from lib.pc98 import parse_mz
    from lib.op_cfg_runtime import Machine
    raw = (root / '.analysis/toolchain/wineprefix/drive_c/TH03PKG/af1409l/r1/op.exe').read_bytes()
    manifest = tomllib.loads((root / 'config/th03_diet.toml').read_text())
    expected = next(a['decoded_sha256'] for a in manifest['artifacts'] if a['id'] == 'th03-op')
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('original OP identity changed')
    image = parse_mz(raw);native = str(args.native.resolve());checks = str(args.native_checks.resolve())

    def path(file, exe):
        return subprocess.check_output(['wslpath', '-w', str(file)], text=True).strip() if exe.endswith('.exe') else str(file)

    with tempfile.TemporaryDirectory(prefix='th03-configuration-') as work:
        work = Path(work)
        source = work / 'original.cfg';source.write_bytes(bytes((2, 1, 3, 0xad, 0x57, 0, 0x60, 0xa7)))
        for exiting, values in ((False, (0, 2, 1)), (True, (1, 0, 2))):
            directory = work / str(int(exiting))
            original = Machine(image, 0x1000)
            original.run('cfg_load', cfg=source.read_bytes())
            before = [original.uc.mem_read(0x60000 + offset, 1)[0] for offset in (0x15, 0x16, 0xb)]
            expected = Machine(image, 0x1000).run('cfg_save_exit' if exiting else 'cfg_save', cfg=source.read_bytes(), resident=values, trash=0xad)
            reply = subprocess.check_output([checks, '--configuration', path(source, checks), path(directory, checks), ''.join(map(str, values)), str(int(exiting))], text=True).splitlines()
            if list(map(int, reply[0].split())) != before or bytes(map(int, reply[1].split())) != bytes.fromhex(expected['file_hex']):
                raise ValueError(f'original CFG load/save differs: exit={exiting}')
            saved = (directory / 'YUME.CFG').read_bytes()
            # A subsequent process must prefer the native file over HDI defaults.
            reply = subprocess.check_output([checks, '--configuration', path(source, checks), path(directory, checks), '123', '1'], text=True).splitlines()
            if tuple(map(int, reply[0].split())) != values or saved[:3] != bytes(values):
                raise ValueError('native configuration was not reloaded')
            if (directory / 'YUME.CFG').read_bytes() != bytes((1, 2, 3, 0, 0, 0, 0, 0)):
                raise ValueError('native exit configuration did not replace the old record')
        for name, malformed in [('short', bytes(7)), ('rank', bytes((1, 0, 4, 0, 0, 0, 0, 0)))]:
            directory = work / name;directory.mkdir();(directory / 'YUME.CFG').write_bytes(malformed)
            reply = subprocess.run([checks, '--configuration', path(source, checks), path(directory, checks), '123', '1'], capture_output=True, text=True)
            if reply.returncode == 0 or 'unsupported native YUME.CFG' not in reply.stderr:
                raise ValueError('invalid native configuration was accepted: ' + name)
        disk = root / '.analysis/runtime/images/zun.hdi'
        config = tomllib.loads((root / 'config/targets.toml').read_text())
        if hashlib.sha256(disk.read_bytes()).hexdigest() != config['source']['hdi_sha256']:
            raise ValueError('original HDI identity changed')
        save = work / 'application'
        common = [native, '--hdi', path(disk, native), '--headless', '--save-dir', path(save, native), '--scene', 'options']
        changed = subprocess.check_output(common + ['--inputs', '8,0,2,0,8,0,2,0,8,0'], text=True)
        reloaded = subprocess.check_output(common, text=True)
        fields = lambda output: re.search(r'rank=(\d+) music=(\d+) keys=(\d+)', output).groups()
        if fields(changed) != fields(reloaded):
            raise ValueError('application Option changes did not survive process restart')
        rank, music, keys = map(int, fields(changed))
        if (save / 'YUME.CFG').read_bytes() != bytes((music, keys, rank, 0, 0, 0, 0, 0)):
            raise ValueError('application save order or exit bytes differ')
    print('Original CFG option order/exit bytes and native overwrite, Option save and process reload agree.')


if __name__ == '__main__':
    main()
