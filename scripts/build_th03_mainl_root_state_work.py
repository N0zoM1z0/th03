#!/usr/bin/env python3
"""Compile one natural complete root TU and normally link both retained rounds."""
import fcntl
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile

import build_th03_runtime_after548_work as runtime
import build_th03_mainl_work as cold
from review_th03_mainl_sound_work import images
from build_th03_mainl_resources_work import need, sha
from lib.omf import parse_omf
from build_th03_mainl_display_work import payload, literal_fields

ROOT = runtime.ROOT
base = runtime.base
DRIVER = 'scripts/build_th03_mainl_root_state_work.py'
CONFIG = 'config/mainl_work/root_state_after552.json'
PREFIX = '.analysis/work/root-state-after552-'
REPORT = PREFIX + 'build.json'
SCRATCH = base.b.WORK / 'probe/af552h'


def inputs():
    config, digest = base.load(CONFIG)
    expected = ['src/mainl/root/recovered/' + n for n in
                ('complete.cpp', 'cfg_load.inl', 'win.inl', 'state.inl')]
    need(config['schema'] == 'th03-mainl-root-state-after552-v1' and
         config['source'] == expected[0] and config['inputs'] == expected and
         config['original_object'] == 'obj/th03/rootdata.obj' and
         config['parent_report'] == runtime.REPORT and config['native_module'] == 'rootdata.cpp' and
         (config['CODE_bytes'], config['DATA_bytes'], config['BSS_bytes'],
          config['native_ordered_fields'], config['DATA_ordered_fields']) == (2458, 112, 186, 278, 28),
         'complete root code, typed far-pointer DATA and true uninitialized BSS')
    return config, digest


def response(number):
    raw = runtime.link_response('mainl', base.b.WORK, number).replace(b'af548h', b'af552h')
    key = rb'obj\th03\rootdata.obj'
    need(raw.count(key) == 1, 'one original root object binding')
    return raw.replace(key, rb'probe\af552h\rootdata.obj')


def compiler(dos):
    return dos + ['tcc', '-c', r'-I.;..\..', '-O', '-b-', '-3', '-Z', '-d',
                  '-DGAME=3', '-ml', "-DBINARY='L'", '-n.', 'rootdata.cpp']


def program(raw):
    return [(r.name, r.data) for r in parse_omf(raw) if r.name not in ('THEADR', 'COMENT')]


def parent_inputs(config):
    """Reuse immutable source/native evidence without the obsolete live211 gate.

    Native source, producers and tool configuration from the after548 commit
    remain frozen. Reviews/publications/tracking are not compiler inputs. One
    existing source checkout has an explicitly recorded CRLF text transport.
    The current full cold audit separately binds SDK/tools/staged dependencies.
    """
    commit = config['preservation_commit']
    need(commit == '0feb71f8ebc6cd0f708388afff0f3a604024d404', 'fixed after548 source checkpoint')
    recipes = set(cold.recipe_inventory())
    def selected(name):
        if name.startswith(('src/', 'compat/')):
            return True
        if name.startswith('config/'):
            return not (name.endswith(('.csv', '/scoped_acceptance.json', '/publication.json')) or
                        name == 'config/oracles.toml')
        return name in recipes or name.startswith(('scripts/build_th03_', 'scripts/stage_th03_', 'scripts/lib/mainl_'))
    archive = subprocess.check_output(['git', 'archive', commit, 'src', 'compat', 'config', 'scripts'], cwd=ROOT)
    inventory, transports = {}, {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as tree:
        for entry in tree:
            if not entry.isfile() or not selected(entry.name):
                continue
            raw = tree.extractfile(entry).read()
            current = (ROOT / entry.name).read_bytes()
            if current != raw:
                need(entry.name == 'src/main/player/bombs.inl' and b'\r' not in raw and
                     current.replace(b'\r\n', b'\n') == raw, 'unchanged preserved native input ' + entry.name)
                transports[entry.name] = dict(transport='existing CRLF checkout to LF Git text',
                    git_bytes=len(raw), git_sha256=sha(raw), checkout_bytes=len(current), checkout_sha256=sha(current))
            inventory[entry.name] = dict(bytes=len(current), sha256=sha(current))
    parent, digest = base.load(runtime.REPORT)
    need(parent['complete'] and digest == config['parent_report_sha256'] and
         parent['source_sha256'] == sha((ROOT / parent['source']).read_bytes()) and
         parent['driver_sha256'] == sha((ROOT / runtime.DRIVER).read_bytes()), 'actual immutable after548 source/native root')
    vectors = [{k: base.checked(v) for k, v in row['outputs'].items()} for row in parent['rounds']]
    need(len(vectors) == 2 and vectors[0] == vectors[1], 'both actual complete retained runtime vectors')
    return parent, dict(preservation_commit=commit, parent_report_sha256=digest,
        source_inventory=inventory, source_text_transports=transports,
        input_policy='source/compat, native configurations, compiler/linker/staging recipes; no live publication gate',
        actual_parent_raw_pair_equal=True, legacy_live_publication_gate_reexecuted=False)


def main():
    config, config_hash = inputs()
    _, _, _, _, cold_raw, graph, _ = images(ROOT)
    parent, previous = parent_inputs(config)
    parent_hash = previous['parent_report_sha256']
    original = (base.b.WORK / config['original_object']).read_bytes()
    producer, = [g for g in graph if g['output'] == config['original_object']]
    sources = {name: (ROOT / name).read_bytes() for name in config['inputs']}
    record = dict(complete=False, whole_product_accepted=False, source_acceptance=False,
        canonical_credit_changed=False, cold_rebuilt=False, game_objects_recompiled=1,
        retained_project_objects=35, library_rebuilt=False, packing_rebuilt=False,
        source_sha256={n: sha(b) for n, b in sources.items()}, config_sha256=config_hash,
        driver_sha256=sha((ROOT / DRIVER).read_bytes()), cold_report_sha256=sha(cold_raw),
        cold_producer=producer, original_object_sha256=sha(original),
        parent_report_sha256=parent_hash, parent_review=previous, phases=[], rounds=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(record, indent=2) + '\n')
    prefix = ROOT / '.analysis/toolchain/wineprefix'
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', WINEPREFIX=str(prefix),
               MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
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
        need(not SCRATCH.exists(), 'fresh preserved complete-root stage')
        SCRATCH.mkdir()
        for name, raw in sources.items():
            dest = SCRATCH / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
            os.utime(dest, (946684800, 946684800))
        (SCRATCH / 'rootdata.cpp').write_bytes(sources[config['source']])
        os.utime(SCRATCH / 'rootdata.cpp', (946684800, 946684800))
        (SCRATCH / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        (SCRATCH / 'config.json').write_bytes((ROOT / CONFIG).read_bytes())
        vectors = []
        for number in (1, 2):
            old = parent['rounds'][number - 1]['outputs']
            (SCRATCH / 'c0l.obj').write_bytes(base.checked(old['startup']))
            (SCRATCH / f'r{number}.lib').write_bytes(base.checked(old['lib']))
            run(compiler(dos), SCRATCH, f'round{number}-compile')
            native = (SCRATCH / 'rootdata.obj').read_bytes()
            need(payload(native) == payload(original) and literal_fields(native) == literal_fields(original) and
                 program(native) == program(original), 'complete original payload, ordered fields and all non-comment records')
            rsp = response(number)
            (SCRATCH / f'r{number}.lnk').write_bytes(rsp)
            run(dos + ['tlink', f'@probe\\af552h\\r{number}.lnk'], base.b.WORK, f'round{number}-link')
            vector = dict(obj=native, exe=(SCRATCH / f'r{number}.exe').read_bytes(),
                          map=(SCRATCH / f'r{number}.map').read_bytes())
            need(vector['exe'] == base.checked(old['mainl_exe']) and vector['map'] == base.checked(old['mainl_map']),
                 'entire actual target-equal EXE and current native MAP')
            outputs = {}
            for kind, raw in vector.items():
                path = PREFIX + f'round{number}-{kind}.bin'
                (ROOT / path).write_bytes(raw)
                outputs[kind] = dict(path=path, bytes=len(raw), sha256=sha(raw))
            record['rounds'].append(dict(round=number, outputs=outputs, response_sha256=sha(rsp),
                reused_startup=old['startup'], reused_library=old['lib']))
            vectors.append(vector)
            save()
            print('Root state round', number, 'complete: CODE2458 / DATA112 / BSS186; whole EXE/MAP exact', flush=True)
        need(vectors[0] == vectors[1] and all((ROOT / n).read_bytes() == raw for n, raw in sources.items()),
             'entire raw OBJ/EXE/MAP repeat and unchanged actual sources')
    record['complete'] = True
    save()


if __name__ == '__main__':
    main()
