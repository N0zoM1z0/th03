#!/usr/bin/env python3
"""Check unchanged native battle HUD regions against the retained DOS frame."""
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
    with tempfile.TemporaryDirectory(prefix='th03-battle-') as work:
        native, original = Path(work) / 'native.ppm', Path(work) / 'original.ppm'
        subprocess.run([str(args.native.resolve()), '--hdi', str(root / '.analysis/runtime/images/zun.hdi'),
                        '--headless', '--scene', 'battle-ready', '--characters', '5,13',
                        '--screenshot', str(native)], check=True)
        subprocess.run(['convert', str(root / '.analysis/runtime/candidates/dos-play-replay/resumed.png'),
                        '-depth', '8', str(original)], check=True)
        a, b = native.read_bytes(), original.read_bytes()
        header = b'P6\n640 400\n255\n'
        if not a.startswith(header) or not b.startswith(header):
            raise ValueError('unexpected PPM shape')
        a, b = a[len(header):], b[len(header):]
        # These regions have unchanged original state in the captured battle:
        # borders, ten-halfheart HUDs, remaining lives, bombs and P1's initial gauge. The captured CPU
        # has earned additional gauge, so its blue bar is not an initial fixture.
        rectangles = [(0, 0, 640, 16), (0, 0, 16, 400), (304, 0, 336, 400), (624, 0, 640, 400),
                      (16, 384, 304, 400), (336, 384, 352, 400), (608, 384, 624, 400), (288, 16, 296, 32)]
        for left, top, right, bottom in rectangles:
            for y in range(top, bottom):
                lo, hi = (y * 640 + left) * 3, (y * 640 + right) * 3
                if a[lo:hi] != b[lo:hi]:
                    raise ValueError(f'original battle HUD differs in rectangle {(left, top, right, bottom)}, row {y}')
        # Stars and entities can appear behind TRAM. Compare every native
        # glyph's ink against DOS, allowing those changing graphics pixels.
        for left, top, right, bottom in [(120, 16, 200, 32), (440, 16, 520, 32),
                                          (272, 32, 304, 48), (272, 368, 304, 384), (336, 368, 368, 384)]:
            ink = 0
            for y in range(top, bottom):
                for x in range(left, right):
                    at = (y * 640 + x) * 3
                    if a[at:at + 3] == b'\xff\xff\xff':
                        ink += 1
                        if a[at:at + 3] != b[at:at + 3]:
                            raise ValueError(f'TRAM ink differs at {x},{y}')
            if not ink:
                raise ValueError('TRAM fixture did not draw a glyph')
    print('Original DOS borders, hearts, lives, bombs, initial gauge and zero score agree.')


if __name__ == '__main__':
    main()
