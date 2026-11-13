#!/usr/bin/env python3
"""Compare TH03's resident PMD music/effects and ordered chip writes."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import tomllib
from pmd_driver_probe import Driver

DRIVERS = {
    'pmd': ('PMD.COM', 20379, 'cbbe9bd610aedda586d8bd7f6dd13d21f037a089458a21ddda0b11a53b4b29e4', 0, 0x88),
    'pmd86': ('PMD86.COM', 28783, 'a6c6af4d94981c0029afc730189860bc76d9d6e788657bcd4c82793b577e930c', 2, 0x188),
    'pmdb2': ('PMDB2.COM', 25642, '39e2855df81b73eec90dde753fa838bafaf8139f828078433b00e143cabc938c', 1, 0x88),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--native-checks', type=Path, required=True)
    parser.add_argument('--dos-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--driver', choices=DRIVERS, default='pmd86')
    parser.add_argument('--song')
    parser.add_argument('--ticks', type=int, default=512)
    parser.add_argument('--loops', type=int, default=0)
    parser.add_argument('--all-effects', action='store_true', help='exercise the game effect IDs 0..21')
    args = parser.parse_args();root = args.dos_root.resolve()
    disk = root / '.analysis/runtime/images/zun.hdi'
    config = tomllib.loads((root / 'config/targets.toml').read_text())
    if hashlib.sha256(disk.read_bytes()).hexdigest() != config['source']['hdi_sha256']:
        raise ValueError('original TH03 HDI identity changed')
    out = args.output.resolve();out.mkdir(parents=True, exist_ok=True)
    native, checks = str(args.native.resolve()), str(args.native_checks.resolve())
    def path(file):
        return subprocess.check_output(['wslpath', '-w', str(file)], text=True).strip() if args.native_checks.suffix == '.exe' else str(file)
    filename, size, sha, board, port = DRIVERS[args.driver]
    subprocess.run([checks, '--hdi-file', path(disk), path(out), filename], check=True)
    binary = (out / filename).read_bytes()
    if len(binary) != size or hashlib.sha256(binary).hexdigest() != sha:
        raise ValueError('TH03 driver identity changed')
    subprocess.run([native, '--hdi', str(disk), '--extract', 'YUME.EFC', '--output', str(out / 'YUME.EFC')], check=True)
    names = [line.split()[0] for line in subprocess.check_output([native, '--hdi', str(disk), '--list'], text=True).splitlines() if line.split()[0].endswith('.M')]
    if args.song:
        names = [name for name in names if name == args.song.upper()]
        if not names:
            raise ValueError('requested song is not in the original archive')
    for name in names:
        music = out / name
        subprocess.run([native, '--hdi', str(disk), '--extract', name, '--output', str(music)], check=True)
        d = Driver(binary, filename, ' /M8 /V0 /E2 /K ', 0x2000);d.run()
        if d.exit != 0x3100 or d.service(0x900)['ax'] != 0x4800 + board:
            raise ValueError('TH03 PMD installation/type reply differs')
        d.installed()
        d.service(0x100);d.write_resource(0xb00, (out / 'YUME.EFC').read_bytes());d.write_resource(0x600, music.read_bytes())
        mirror = [d.registers.get((port + bank * 4, address), 0) for bank in range(2) for address in range(256)]
        mirror_path = out / (name + '.mirror');mirror_path.write_text(' '.join(map(str, mirror)))
        ops, rows = [], []
        def operation(op, value):
            d.ports = []
            if op == 'R':
                d.service(0)
            elif op == 'M':
                d.service(0x100)
            elif op == 'P':
                d.service(0xc00 | value)
            elif op == 'S':
                d.service(0xc7f)
            elif op == 'F':
                d.service(0x200 | (value & 255))
            else:
                d.irq(value)
            state = d.snapshot();selected = {};writes = []
            for tick, p, width, v in d.ports:
                if p in (port, port + 4):
                    selected[p] = v
                elif p in (port + 2, port + 6):
                    writes.extend(((p - port - 2) // 4, selected[p - 2], v))
            rows.append([state['measure'], state['volume'] & 255, state['status'], len(writes) // 3, *writes]);ops.append((op, value))
            return state['status'] & 255
        operation('R', 0)
        for tick in range(65536 if args.loops else args.ticks):
            status = operation('I', 3)
            if args.loops and (status == 255 or status >= args.loops):
                break
        else:
            if args.loops:
                raise ValueError('original song did not loop/end in the bounded run')
        for effect in range(22) if args.all_effects else (0, 9, 14, 21):
            operation('P', effect)
            for i in range(24):
                operation('I', (1, 2, 3)[i % 3])
        operation('F', 16)
        for i in range(144):
            operation('I', 3)
        operation('M', 0)
        op_path = out / (name + '.ops');op_path.write_text(''.join(f'{op} {value}\n' for op, value in ops))
        trace = out / (name + '.trace')
        subprocess.run([checks, '--pmd-owner', path(music), path(out / 'YUME.EFC'), str(board), path(mirror_path), path(op_path), path(trace)], check=True)
        actual = [list(map(int, line.split())) for line in trace.read_text().splitlines()]
        if actual != rows:
            (out / (name + ".original.trace")).write_text("".join(" ".join(map(str,row))+"\n" for row in rows))
            index = next((i for i, (a, b) in enumerate(zip(actual, rows)) if a != b), min(len(actual), len(rows)))
            expected_row = rows[index];actual_row = actual[index]
            first = next((i for i, (a, b) in enumerate(zip(actual_row, expected_row)) if a != b), min(len(actual_row), len(expected_row)))
            raise ValueError(f'{args.driver}/{name} operation{index} {ops[index]}, field{first}: native={actual_row[max(0,first-8):first+16]}, original={expected_row[max(0,first-8):first+16]}; row lengths={len(actual_row),len(expected_row)}')
        print(f'{args.driver}/{name}: {len(rows)} original operations and every ordered FM/SSG/rhythm/timer write agree.', flush=True)


if __name__ == '__main__':
    main()
