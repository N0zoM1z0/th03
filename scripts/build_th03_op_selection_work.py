#!/usr/bin/env python3
"""Rebuild the selection tail and relink twice against unchanged cold context."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tomllib

import build_th03_op_work as build
from lib.omf import describe_omf, parse_omf
from lib.op_startup_cold import verify as cold_graph
from review_th03_op_cfg_work import images

ROOT = Path(__file__).resolve().parents[1]
STATE = 'src/op/menu/selection_state.inl'
WRAPPER = 'th03/seltail.cpp'
OBJECT = 'obj/th03/seltail.obj'
REPORT = '.analysis/work/selection-build.json'
DRIVER = 'scripts/build_th03_op_selection_work.py'
sha = lambda raw: hashlib.sha256(raw).hexdigest()


def wrapper():
    return ('#pragma option -zCOP_SEL_TEXT\n#include "' + STATE + '"\n'
            'unsigned char near playchars_available_load(void);\n'
            '#include "probe/select155_tail.inl"\n').encode()


def native_records(raw):
    """Discard only dependency/translator comments; retain every native record."""
    return [(r.name, r.data.hex()) for r in parse_omf(raw) if r.name not in ('COMENT',)]


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    work, target, candidate, cold, cold_raw = images(ROOT)
    cold_graph(ROOT, work, target, candidate, cold)
    files = build.source_graph()
    cfg = tomllib.loads((ROOT / 'config/toolchain.toml').read_text())
    prefix = ROOT / cfg['paths']['wine_prefix']
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / cfg['paths']['msdos_player']), '-e', '-x']
    state = (ROOT / STATE).read_bytes()
    generated = wrapper()
    response = files['obj/th03/op.@l']
    for old, new in ((b'obj\\th03\\seltail.obj', b'probe\\selstate.obj'),
                     (b'bin\\th03\\op.exe', b'probe\\selstate.exe'),
                     (b'obj\\th03\\op.map', b'probe\\selstate.map')):
        assert response.count(old) == 1
        response = response.replace(old, new)
    inputs = {STATE: state, 'src/op/menu/character_selection.inl': files['src/op/menu/character_selection.inl']}
    report = dict(complete=False, source_acceptance=False, whole_product_cold_rebuilt=False,
        driver_sha256=sha((ROOT / DRIVER).read_bytes()), cold_report_sha256=sha(cold_raw),
        source_sha256={n: sha(b) for n, b in inputs.items()}, wrapper_sha256=sha(generated),
        response_sha256=sha(response), context_objects=29, rounds=[], native_phases=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(report, indent=2) + '\n')
    def run(arguments, label):
        result = subprocess.run(dos + arguments, cwd=work, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=90)
        log = ROOT / f'.analysis/work/selection-{label}.log'
        log.write_bytes(result.stdout)
        report['native_phases'].append(dict(label=label, command=dos + arguments,
            returncode=result.returncode, log_sha256=sha(result.stdout)))
        save()
        assert result.returncode == 0, result.stdout
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        original = (work / WRAPPER).read_bytes()
        stamp = (work / WRAPPER).stat()
        temporary = [work / n for n in (STATE, 'probe/selstate.obj', 'probe/selstate.exe',
                                        'probe/selstate.map', 'probe/selstate.lnk')]
        assert all(not p.exists() for p in temporary)
        try:
            (work / STATE).write_bytes(state)
            (work / WRAPPER).write_bytes(generated)
            (work / 'probe/selstate.lnk').write_bytes(response)
            for name in (STATE, WRAPPER, 'probe/selstate.lnk'):
                os.utime(work / name, (build.STAMP, build.STAMP))
            (ROOT / '.analysis/work/selection-tail.cpp').write_bytes(generated)
            (ROOT / '.analysis/work/selection-tail.lnk').write_bytes(response)
            for number in (1, 2):
                for p in temporary[1:4]:
                    p.unlink(missing_ok=True)
                run(['tcc', '-c', '-I.', '-O', '-b-', '-3', '-Z', '-d', '-DGAME=3', '-ml',
                     "-DBINARY='O'", '-oprobe/selstate.obj', WRAPPER], f'round{number}-compile')
                raw = (work / 'probe/selstate.obj').read_bytes()
                assert describe_omf(raw)['valid']
                assert native_records(raw) == native_records((work / OBJECT).read_bytes())
                run(['tlink', r'@probe\selstate.lnk'], f'round{number}-link')
                outputs = {}
                for suffix in ('obj', 'exe', 'map'):
                    raw = (work / f'probe/selstate.{suffix}').read_bytes()
                    name = f'.analysis/work/selection-round{number}.{suffix}'
                    (ROOT / name).write_bytes(raw)
                    outputs[suffix] = dict(path=name, bytes=len(raw), sha256=sha(raw))
                    if suffix == 'exe':
                        assert raw == (work / 'bin/th03/op.target.exe').read_bytes()
                report['rounds'].append(dict(round=number, outputs=outputs))
                save()
                print(f'selection round{number}: actual maintained prefix/native records/whole linked target PASS', flush=True)
            assert {k: v['sha256'] for k, v in report['rounds'][0]['outputs'].items()} == {
                k: v['sha256'] for k, v in report['rounds'][1]['outputs'].items()}
        finally:
            (work / WRAPPER).write_bytes(original)
            os.utime(work / WRAPPER, ns=(stamp.st_atime_ns, stamp.st_mtime_ns))
            for p in temporary:
                p.unlink(missing_ok=True)
    cold_graph(ROOT, work, target, candidate, cold)
    report['complete'] = True
    save()


if __name__ == '__main__':
    main()
