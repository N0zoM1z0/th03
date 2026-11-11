#!/usr/bin/env python3
"""Compose the current three project pairs with the rebuilt source CL runtime."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess

import build_th03_package_current as package
import build_th03_runtime_current as runtime
from lib.pc98 import parse_mz

ROOT, DRIVE = package.ROOT, package.DRIVE
STAGE = 'af1397l'
DRIVER = 'scripts/build_th03_runtime_linked_current.py'
need, pin, sha = package.need, package.pin, package.sha


def context(stage, parent=None):
    parent = package.review() if parent is None else parent
    rebuilt = runtime.verify(reviewed=parent)
    base, _, _, inputs, responses, maps = package.context(stage, {})
    inputs[DRIVER] = sha((ROOT / DRIVER).read_bytes())
    inputs[runtime.DRIVER] = sha((ROOT / runtime.DRIVER).read_bytes())
    report = DRIVE / 'TH03RT' / runtime.STAGE / 'runtime-build.json'
    inputs[str(report.relative_to(ROOT))] = sha(report.read_bytes())
    startups = []
    for n in (1, 2):
        library = ROOT / rebuilt['libraries'][n - 1]
        inputs[str(library.relative_to(ROOT))] = sha(library.read_bytes())
        startup = DRIVE / 'TH03PKG' / package.STAGE / f'r{n}/c0l.obj'
        inputs[str(startup.relative_to(ROOT))] = sha(startup.read_bytes())
        startups.append(startup.read_bytes())
        for product in package.PRODUCTS:
            key = f'r{n}/{product}.lnk'; raw = responses[key]
            tokens = re.findall(rb'[^\s,+]+', raw)
            old, = [t for t in tokens if t.lower().endswith((b'\\cl.lib', b'\\linked.lib'))]
            raw = raw.replace(old, package.windows(library).encode())
            unused = [t for t in tokens if t.lower().endswith((b'\\emu.lib', b'\\mathl.lib'))]
            need(len(unused) == 2, 'explicit unused EMU/MATHL response slots')
            for token in unused:
                raw = raw.replace(token, b'')
            responses[key] = raw
    need(startups[0] == startups[1], 'unchanged source C0 pair')
    return base, parent, rebuilt, inputs, responses, maps, startups[0]


def commands(base, number):
    for product, (tree, _) in package.PRODUCTS.items():
        yield product, package.dos() + ['tlink', '@' + package.windows(base / f'r{number}/{product}.lnk')], DRIVE / tree


def expected_map(product, raw):
    # Each change is an observed source-owner effect, checked at its exact
    # address. Keep every other MAP byte, including both PUBLIC tables.
    swaps = {
        'main': [('3215', 'LDIV@', 'F_LDIV@'), ('322C', 'F_LUMOD@', 'LUMOD@')],
        'op': [('33C5', 'LDIV@', 'F_LDIV@')],
        'mainl': [('30B3', 'LDIV@', 'F_LDIV@'), ('30CA', 'F_LUMOD@', 'LUMOD@'),
                  ('3182', 'PADD@', 'F_PADD@')],
    }
    for address, first, second in swaps[product]:
        a = f' 0000:{address} idle  {first}\r\n'.encode()
        z = f' 0000:{address} idle  {second}\r\n'.encode()
        need(raw.count(a + z) == 1, 'unique original same-address runtime alias pair')
        raw = raw.replace(a + z, z + a, 1)
    if product == 'mainl':
        getvect = b' 0E3F:286A 0000 C=BSS    S=_BSS           G=DGROUP  M=getvect    ACBP=48\r\n'
        ioerror = b' 0E3F:286A 0000 C=BSS    S=_BSS           G=DGROUP  M=ioerror    ACBP=48\r\n'
        fbrk = b' 0E3F:2872 0000 C=BSS    S=_BSS           G=DGROUP  M=fbrk       ACBP=48\r\n'
        xx = b' 0E3F:2876 000A C=BSS    S=_BSS           G=DGROUP  M=xx         ACBP=48\r\n'
        setblock = b' 0E3F:2880 0000 C=BSS    S=_BSS           G=DGROUP  M=setblock   ACBP=48\r\n'
        need(all(raw.count(x) == 1 for x in (getvect, fbrk, xx)) and
             ioerror not in raw and setblock not in raw, 'original MAINL empty-segment carrier rows')
        raw = raw.replace(getvect, getvect + ioerror, 1).replace(fbrk, b'', 1).replace(xx, xx + setblock, 1)
    return raw


def review(stage=STAGE, parent=None):
    base, parent, rebuilt, inputs, responses, maps, startup = context(stage, parent)
    report = json.loads((base / 'runtime-linked.json').read_bytes())
    need(report['complete'] and report['stage'] == stage and report['inputs'] == inputs and
         report['parent'] == parent and report['runtime'] == rebuilt, 'complete actual source/runtime/link context')
    need((base / 'startup/c0l.obj').read_bytes() == startup, 'actual consumed source C0 object')
    need(all((base / n).read_bytes() == raw for n, raw in responses.items()), 'all actual ordered linker responses')
    expected = [(f'r{n}-{product}', argv, str(cwd), 0) for n in (1, 2) for product, argv, cwd in commands(base, n)]
    need([(p['label'], p['argv'], p['cwd'], p['returncode']) for p in report['phases']] == expected, 'actual six serialized native links')
    for p in report['phases']:
        need(sha((base / (p['label'] + '.log')).read_bytes()) == p['log_sha256'], 'actual linker log')
    need(len(report['rounds']) == 2 and [r['round'] for r in report['rounds']] == [1, 2], 'both native composition rounds')
    vectors = []
    for n, row in enumerate(report['rounds'], 1):
        rd = base / f'r{n}'
        names = {product + suffix for product in package.PRODUCTS for suffix in ('.exe', '.map')}
        need(set(row['outputs']) == names and row['outputs'] == {name: pin(rd / name) for name in names}, 'all raw native EXE/MAP bytes')
        for product in package.PRODUCTS:
            raw = (rd / (product + '.exe')).read_bytes()
            baseline = DRIVE / 'TH03PKG' / package.STAGE / f'r{n}/{product}.exe'
            need(raw == baseline.read_bytes(), 'complete Japanese linked ' + product)
            a, z = parse_mz(raw), parse_mz(baseline.read_bytes())
            need(a.valid and a.program_image == z.program_image and a.relocations == z.relocations, 'all loaded bytes and ordered MZ relocations: ' + product)
            need((rd / (product + '.map')).read_bytes() == expected_map(product, maps[f'r{n}/{product}.map']), 'entire reviewed source-runtime MAP: ' + product)
        vectors.append({name: (rd / name).read_bytes() for name in names if name != 'main.map'})
    need(vectors[0] == vectors[1], 'all three complete EXEs and two repeatable MAPs repeat')
    return dict(stage=stage, complete_three_current_links_equal=True, native_rounds=2,
                source_CL_contributors=rebuilt['selected_members'], source_startup_reused=True,
                unused_EMU_MATHL_removed=True, exact_MAP_alias_swaps=6, exact_MAP_zero_extent_row_changes=3,
                original_field_order_equal_members=rebuilt['original_field_order_equal_members'],
                remaining_field_order_members=rebuilt['remaining_field_order_members'],
                canonical_source_credit_added=False,
                report=str((base / 'runtime-linked.json').relative_to(ROOT)))


def build(stage):
    base, parent, rebuilt, inputs, responses, maps, startup = context(stage)
    need(not base.exists(), 'unused current runtime link stage')
    report = dict(complete=False, stage=stage, inputs=inputs, parent=parent, runtime=rebuilt, phases=[], rounds=[])
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', MSDOS_PATH=r'C:\TC4\BIN')
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        (base / 'startup').mkdir(parents=True)
        (base / 'startup/c0l.obj').write_bytes(startup)
        for name, raw in responses.items():
            path = base / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
        for n in (1, 2):
            for product, argv, cwd in commands(base, n):
                p = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
                label = f'r{n}-{product}'
                (base / (label + '.log')).write_bytes(p.stdout)
                report['phases'].append(dict(label=label, argv=argv, cwd=str(cwd), returncode=p.returncode, log_sha256=sha(p.stdout)))
                need(p.returncode == 0, 'complete source-runtime native link: ' + label)
            rd = base / f'r{n}'
            names = {product + suffix for product in package.PRODUCTS for suffix in ('.exe', '.map')}
            report['rounds'].append(dict(round=n, outputs={name: pin(rd / name) for name in names}))
            print(f'Source-runtime composition round {n}: all three current project links', flush=True)
        report['complete'] = True
        (base / 'runtime-linked.json').write_text(json.dumps(report, indent=2) + '\n')
    return review(stage, parent)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage', default=STAGE); p.add_argument('--build', action='store_true')
    args = p.parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10: os.nice(10 - os.nice(0))
    print(json.dumps(build(args.stage) if args.build else review(args.stage), indent=2))


if __name__ == '__main__':
    main()
