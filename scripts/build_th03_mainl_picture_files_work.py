#!/usr/bin/env python3
"""Replace generated PIC pointer context with a typed natural C source TU."""
import fcntl
import json
import os
import re
import subprocess

import build_th03_mainl_root_state_work as parent
from review_th03_mainl_sound_work import images
from build_th03_mainl_resources_work import need, sha

ROOT = parent.ROOT
base = parent.base
DRIVER = 'scripts/build_th03_mainl_picture_files_work.py'
CONFIG = 'config/mainl_work/picture_files_after553.json'
PREFIX = '.analysis/work/picture-files-after553-'
REPORT = PREFIX + 'build.json'
SCRATCH = base.b.WORK / 'probe/af553h'


def inputs():
    config, digest = base.load(CONFIG)
    need(config['schema'] == 'th03-mainl-picture-files-after553-v1' and
         config['source'] == 'src/mainl/root/picture_files.c' and
         config['original_object'] == 'obj/th03/rootpre.obj' and config['source_module'] == 'rootpre.c' and
         config['parent_report'] == parent.REPORT and
         (config['DATA_bytes'], config['pointer_bytes'], config['pointer_count'], config['native_fields']) == (18, 2, 9, 9),
         'complete typed nine-entry near filename table')
    return config, digest


def response(number):
    raw = parent.response(number).replace(b'af552h', b'af553h')
    key = rb'obj\th03\rootpre.obj'
    need(raw.count(key) == 1, 'one original generated picture table object')
    return raw.replace(key, rb'probe\af553h\rootpre.obj')


def compiler(dos):
    return dos + ['tcc', '-c', '-I.', '-O', '-b-', '-3', '-Z', '-d',
                  '-DGAME=3', '-ml', "-DBINARY='L'", '-n.', 'rootpre.c']


def map_partition(raw, module):
    pattern = rb'^\s*[0-9A-F]{4}:[0-9A-F]{4}\s+[0-9A-F]{4}\s+C=\S+\s+S=\S+\s+G=\S+\s+M=' + re.escape(module.encode()) + rb'\s+ACBP=[0-9A-F]+\s*$'
    selected, remaining = [], []
    for line in raw.splitlines(keepends=True):
        (selected if re.fullmatch(pattern, line, re.I) else remaining).append(line)
    need(selected, 'actual detailed contribution rows for ' + module)
    return b''.join(remaining), [line.decode().strip() for line in selected]


def main():
    config, config_hash = inputs()
    work, _, _, _, cold_raw, graph, _ = images(ROOT)
    parent_config, _ = parent.inputs()
    _, preservation = parent.parent_inputs(parent_config)
    prior, prior_hash = base.load(parent.REPORT)
    need(prior['complete'] and prior_hash == config['parent_report_sha256'] and
         prior['source_sha256'] == {n: sha((ROOT / n).read_bytes()) for n in parent_config['inputs']}, 'actual current source root parent')
    source = (ROOT / config['source']).read_bytes()
    producer, = [g for g in graph if g['output'] == config['original_object']]
    record = dict(complete=False, source_acceptance=False, whole_product_accepted=False,
        canonical_credit_changed=False, cold_rebuilt=False, game_objects_recompiled=1,
        source_root_recompiled=False, cold_game_objects_retained=34, source_root_reused=True,
        library_rebuilt=False, packing_rebuilt=False, driver_sha256=sha((ROOT / DRIVER).read_bytes()),
        source_sha256=sha(source), config_sha256=config_hash, parent_report_sha256=prior_hash,
        parent_preservation=preservation, cold_report_sha256=sha(cold_raw), cold_producer=producer,
        original_object_sha256=sha((work / config['original_object']).read_bytes()), phases=[], rounds=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(record, indent=2) + '\n')
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
        WINEPREFIX=str(ROOT / '.analysis/toolchain/wineprefix'), MSDOS_PATH=r'C:\TC4\BIN',
        TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']

    def run(argv, cwd, label):
        p = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=90)
        path = PREFIX + label + '.log'
        (ROOT / path).write_bytes(p.stdout)
        record['phases'].append(dict(label=label, argv=argv, cwd=str(cwd.relative_to(ROOT)),
            returncode=p.returncode, log_path=path, log_sha256=sha(p.stdout)))
        save()
        need(p.returncode == 0, label + ': ' + p.stdout.decode(errors='replace')[-1500:])

    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(not SCRATCH.exists(), 'fresh preserved picture filename stage')
        SCRATCH.mkdir()
        (SCRATCH / 'rootpre.c').write_bytes(source)
        os.utime(SCRATCH / 'rootpre.c', (946684800, 946684800))
        (SCRATCH / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        (SCRATCH / 'config.json').write_bytes((ROOT / CONFIG).read_bytes())
        vectors = []
        for number in (1, 2):
            old = prior['rounds'][number - 1]
            (SCRATCH / 'c0l.obj').write_bytes(base.checked(old['reused_startup']))
            (SCRATCH / f'r{number}.lib').write_bytes(base.checked(old['reused_library']))
            (SCRATCH / 'rootdata.obj').write_bytes(base.checked(old['outputs']['obj']))
            run(compiler(dos), SCRATCH, f'round{number}-compile')
            rsp = response(number)
            (SCRATCH / f'r{number}.lnk').write_bytes(rsp)
            run(dos + ['tlink', f'@probe\\af553h\\r{number}.lnk'], work, f'round{number}-link')
            vector = dict(obj=(SCRATCH / 'rootpre.obj').read_bytes(), exe=(SCRATCH / f'r{number}.exe').read_bytes(),
                          map=(SCRATCH / f'r{number}.map').read_bytes())
            need(vector['exe'] == base.checked(old['outputs']['exe']), 'entire pinned target decoded EXE remains raw-exact')
            before, original_rows = map_partition(base.checked(old['outputs']['map']), 'rootpre.asm')
            after, native_rows = map_partition(vector['map'], 'rootpre.c')
            need(before == after, 'every MAP byte outside the explicit picture contributor rows agrees')
            outputs = {}
            for kind, raw in vector.items():
                path = PREFIX + f'round{number}-{kind}.bin'
                (ROOT / path).write_bytes(raw)
                outputs[kind] = dict(path=path, bytes=len(raw), sha256=sha(raw))
            record['rounds'].append(dict(round=number, outputs=outputs, response_sha256=sha(rsp),
                reused_startup=old['reused_startup'], reused_library=old['reused_library'],
                reused_root=old['outputs']['obj'], original_MAP_rows=original_rows, native_MAP_rows=native_rows))
            save()
            vectors.append(vector)
            print('PIC filename round', number, 'complete: typed near DATA18; whole original EXE raw-exact', flush=True)
        need(vectors[0] == vectors[1] and (ROOT / config['source']).read_bytes() == source,
             'whole raw OBJ/EXE/MAP repeat and unchanged source')
    record['complete'] = True
    save()


if __name__ == '__main__':
    main()
