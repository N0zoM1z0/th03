#!/usr/bin/env python3
"""Compile only two OP sound bodies twice, without their explicit trailers."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tomllib

import build_th03_op_work as build
from lib.op_leaf_native import LEAVES, TRAILER
from lib.op_startup_cold import verify as cold_graph
from probe_th03_main_boss_marisa_cpp import code_bytes
from review_th03_op_cfg_work import images

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.analysis/work'
sha = lambda b: hashlib.sha256(b).hexdigest()


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    work, target, candidate, cold, cold_raw = images(ROOT)
    cold_graph(ROOT, work, target, candidate, cold)
    cfg = tomllib.loads((ROOT / 'config/toolchain.toml').read_text())
    prefix = ROOT / cfg['paths']['wine_prefix']
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    report = dict(complete=False, driver_sha256=sha(Path(__file__).read_bytes()),
                  cold_report_sha256=sha(cold_raw), rounds=2, source_acceptance=False,
                  whole_product_rebuilt=False, objects=[])
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for index, row in enumerate(LEAVES[:2]):
            _, source, _, _, obj, _, _, _, size, _, _ = row
            raw = (ROOT / source).read_bytes()
            assert raw.endswith(TRAILER) and raw.count(TRAILER) == 1
            stripped = raw[:-len(TRAILER)]
            native_source = f'probe/lbody{index}.c'
            scratch, output = work / native_source, work / f'probe/lbody{index}.obj'
            assert not scratch.exists() and not output.exists()
            saved_source = f'.analysis/work/sound-body{index}.c'
            (ROOT / saved_source).write_bytes(stripped)
            entry = dict(source=source, source_sha256=sha(raw), current_object_sha256=sha((work / obj).read_bytes()),
                         stripped_source=saved_source, stripped_source_sha256=sha(stripped),
                         native_source=native_source, outputs=[])
            try:
                scratch.write_bytes(stripped)
                os.utime(scratch, (build.STAMP, build.STAMP))
                for round_no in (1, 2):
                    output.unlink(missing_ok=True)
                    command = ['/usr/bin/wine-stable', str(ROOT / cfg['paths']['msdos_player']), '-e', '-x',
                               'tcc', '-c', '-I.', '-O', '-b-', '-3', '-Z', '-d', '-DGAME=2', '-ml',
                               "-DBINARY='O'", '-nprobe/', native_source]
                    run = subprocess.run(command, cwd=work, env=env, stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT, timeout=90)
                    log = OUT / f'sound-body{index}-round{round_no}.log'
                    log.write_bytes(run.stdout)
                    assert run.returncode == 0, run.stdout
                    compiled = output.read_bytes()
                    body, _ = code_bytes(compiled, 1)
                    current, _ = code_bytes((work / obj).read_bytes(), 1)
                    assert len(body) == size and body == current[:size]
                    dest = f'.analysis/work/sound-body{index}-round{round_no}.obj'
                    (ROOT / dest).write_bytes(compiled)
                    entry['outputs'].append(dict(path=dest, sha256=sha(compiled), returncode=run.returncode,
                                                  command=command, log_sha256=sha(run.stdout)))
                    print(f'sound body {index}, round {round_no}: {size} native bytes PASS', flush=True)
                assert entry['outputs'][0]['sha256'] == entry['outputs'][1]['sha256']
                report['objects'].append(entry)
            finally:
                scratch.unlink(missing_ok=True)
                output.unlink(missing_ok=True)
    cold_graph(ROOT, work, target, candidate, cold)
    report['complete'] = True
    (OUT / 'sound-bodies.json').write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
