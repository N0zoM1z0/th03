#!/usr/bin/env python3
"""Assemble maintained semantic text/state banks and link with current source objects."""
import fcntl
import json
import os
import subprocess

import build_th03_mainl_picture_files_work as parent
from review_th03_mainl_sound_work import images
from build_th03_mainl_resources_work import need, sha

ROOT = parent.ROOT
base = parent.base
DRIVER = 'scripts/build_th03_mainl_text_banks_work.py'
CONFIG = 'config/mainl_work/text_banks_after554.json'
PREFIX = '.analysis/work/text-banks-after554-native-'
REPORT = PREFIX + 'build.json'
SCRATCH = base.b.WORK / 'probe/af554b'
TASM = ROOT / '.analysis/toolchain/wineprefix/drive_c/TASM50/bin/TASM32.EXE'


def inputs():
    config, digest = base.load(CONFIG)
    need(config['schema'] == 'th03-mainl-text-banks-after554-v1' and
         config['parent_report'] == parent.REPORT and config['encoding'] == 'cp932' and
         [(u['name'], u['module'], u['DATA_bytes'], u['context_DATA_bytes'], u['fields']) for u in config['units']] ==
         [('registration', 'regpre.asm', 303, 304, 2), ('ending', 'regtail.asm', 360, 360, 0)], 'complete bounded source banks')
    return config, digest


def transport(raw):
    return raw.decode('utf-8').encode('cp932').replace(b'\n', b'\r\n')


def response(number):
    raw = parent.response(number).replace(b'af553h', b'af554b')
    for name in ('regpre', 'regtail'):
        key = ('obj\\th03\\' + name + '.obj').encode()
        need(raw.count(key) == 1, 'one source bank replacement ' + name)
        raw = raw.replace(key, ('probe\\af554b\\' + name + '.obj').encode())
    return raw


def assembler(dos, module):
    return dos[:1] + [str(TASM), '/m', '/mx', '/kh32768', '/t', '/dGAME=3', module + ',' + module.replace('.asm', '.obj')]


def main():
    config, config_hash = inputs()
    need(sha(TASM.read_bytes()) == 'ba50fe547863b96242d98cff54cdf95ab268a8682395afad172eedbfc46c5b26', 'pinned native TASM5 emitter')
    work, _, _, _, cold_raw, graph, _ = images(ROOT)
    prior, prior_hash = base.load(parent.REPORT)
    need(prior['complete'] and prior_hash == config['parent_report_sha256'], 'actual current picture/root source parent')
    sources = {n: (ROOT / n).read_bytes() for n in config['inputs']}
    producers = [g for g in graph if g['output'] in {u['object'] for u in config['units']}]
    need(len(producers) == 2, 'two complete original bank context producers')
    record = dict(complete=False, source_acceptance=False, whole_product_accepted=False,
        canonical_credit_changed=False, cold_rebuilt=False, game_objects_recompiled=2,
        cold_game_objects_retained=32, source_root_recompiled=False, source_picture_recompiled=False,
        library_rebuilt=False, packing_rebuilt=False, driver_sha256=sha((ROOT / DRIVER).read_bytes()),
        config_sha256=config_hash, assembler_sha256=sha(TASM.read_bytes()), source_sha256={n: sha(v) for n, v in sources.items()},
        transported_sha256={n: sha(transport(v)) for n, v in sources.items()},
        parent_report_sha256=prior_hash, cold_report_sha256=sha(cold_raw), cold_producers=producers,
        original_objects_sha256={u['object']: sha((work / u['object']).read_bytes()) for u in config['units']},
        phases=[], rounds=[])
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
        need(p.returncode == 0, label + ': ' + p.stdout.decode(errors='replace')[-1600:])

    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(not SCRATCH.exists(), 'fresh preserved semantic text bank stage')
        SCRATCH.mkdir()
        for name, raw in sources.items():
            path = SCRATCH / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(transport(raw))
            os.utime(path, (946684800, 946684800))
        for unit in config['units']:
            path = SCRATCH / unit['module']
            path.write_bytes(transport(sources[unit['source']]))
            os.utime(path, (946684800, 946684800))
        (SCRATCH / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        (SCRATCH / 'config.json').write_bytes((ROOT / CONFIG).read_bytes())
        vectors = []
        for number in (1, 2):
            old = prior['rounds'][number - 1]
            reused = dict(startup=old['reused_startup'], library=old['reused_library'],
                          root=old['reused_root'], pictures=old['outputs']['obj'])
            for key, filename in [('startup', 'c0l.obj'), ('library', f'r{number}.lib'),
                                  ('root', 'rootdata.obj'), ('pictures', 'rootpre.obj')]:
                (SCRATCH / filename).write_bytes(base.checked(reused[key]))
            for unit in config['units']:
                run(assembler(dos, unit['module']), SCRATCH, f"round{number}-{unit['name']}-assemble")
            rsp = response(number)
            (SCRATCH / f'r{number}.lnk').write_bytes(rsp)
            run(dos + ['tlink', f'@probe\\af554b\\r{number}.lnk'], work, f'round{number}-link')
            vector = {u['name']: (SCRATCH / u['module'].replace('.asm', '.obj')).read_bytes() for u in config['units']}
            vector.update(exe=(SCRATCH / f'r{number}.exe').read_bytes(), map=(SCRATCH / f'r{number}.map').read_bytes())
            outputs = {}
            for kind, raw in vector.items():
                path = PREFIX + f'round{number}-{kind}.bin'
                (ROOT / path).write_bytes(raw)
                outputs[kind] = dict(path=path, bytes=len(raw), sha256=sha(raw))
            record['rounds'].append(dict(round=number, outputs=outputs, response_sha256=sha(rsp), reused=reused))
            save()  # Preserve complete raw outputs even if an acceptance comparison fails.
            need(vector['exe'] == base.checked(old['outputs']['exe']), 'entire original decoded EXE remains raw-exact')
            before, old_rows = parent.map_partition(base.checked(old['outputs']['map']), 'regpre.asm')
            after, new_rows = parent.map_partition(vector['map'], 'regpre.asm')
            need(before == after, 'only explicit registration DATA extent may differ in MAP')
            record['rounds'][-1].update(original_MAP_rows=old_rows, native_MAP_rows=new_rows)
            save()
            vectors.append(vector)
            print('Text bank round', number, 'complete: DATA303+360; whole original EXE raw-exact', flush=True)
        need(vectors[0] == vectors[1] and all((ROOT / n).read_bytes() == raw for n, raw in sources.items()),
             'both whole raw vectors repeat with unchanged sources')
    record['complete'] = True
    save()


if __name__ == '__main__':
    main()
