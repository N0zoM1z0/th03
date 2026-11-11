#!/usr/bin/env python3
"""Compare the native MAINL introduction with the retained original DOS frame."""
import argparse
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--dos-root', type=Path, required=True)
    args = parser.parse_args()
    root = args.dos_root.resolve()
    command = [str(args.native.resolve()), '--hdi', str(root / '.analysis/runtime/images/zun.hdi'),
               '--font-bmp', str(root / '.analysis/runtime/fonts/FREECG98.BMP'),
               '--headless', '--scene', 'stage-intro', '--characters', '5,13']
    with tempfile.TemporaryDirectory(prefix='th03-intro-') as work:
        native, original = Path(work) / 'native.ppm', Path(work) / 'original.ppm'
        subprocess.run(command + ['--frames', '20', '--screenshot', str(native)], check=True)
        subprocess.run(['convert', str(root / '.analysis/runtime/candidates/dos-play-replay/battle.png'),
                        '-depth', '8', str(original)], check=True)
        if native.read_bytes() != original.read_bytes():
            raise ValueError('complete stage introduction differs from original DOS frame')
        # A held key must not skip the original minimum introduction wait.
        early = subprocess.check_output(command + ['--inputs', ','.join(['32'] * 49)], text=True)
        late = subprocess.check_output(command + ['--inputs', ','.join(['32'] * 85)], text=True)
        if 'phase=5 ' not in early or 'phase=3 ' not in late:
            raise ValueError('introduction minimum wait/fade handoff differs')
    print('Complete 640x400 stage introduction agrees with DOS; minimum wait and fade handoff pass.')


if __name__ == '__main__':
    main()
