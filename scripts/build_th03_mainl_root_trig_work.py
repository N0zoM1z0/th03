#!/usr/bin/env python3
"""Reassemble MAINL's large formula-derived trig tables, retaining its contextual root.

Two real TASM/TLINK rounds; source is the pure Python math formula, not
extracted binary data. The generated DOS includes are retained with the native
products. All surrounding source, CODE and BSS remain contextual and uncredited.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import struct
import subprocess

import build_th03_mainl_text_banks_work as parent
from build_th03_mainl_resources_work import need, sha
from build_th03_mainl_display_work import payload, literal_fields
from lib.mainl_owner_migrations import public_offsets
from lib.omf import parse_omf

ROOT = parent.ROOT
base = parent.base
DRIVER = 'scripts/build_th03_mainl_root_trig_work.py'
CONFIG = 'config/mainl_work/root_trig_after555.json'
PREFIX = '.analysis/work/root-trig-after555-native-'
REPORT = PREFIX + 'build.json'
STAGE = 'af555t'
WORK = base.b.WORK
SCRATCH = WORK / ('probe/' + STAGE)
TASM = parent.TASM


def inputs():
    cfg, digest = base.load(CONFIG)
    need(cfg['schema'] == 'th03-mainl-root-trig-after555-v1' and
         cfg['parent_report'] == parent.REPORT and
         cfg['source'] == 'src/shared/math/trig_tables.py' and
         [(x['name'], x['data_offset'], x['size'], x['original_include']) for x in cfg['table_extents']] == [
             ('atan', 778, 256, 'libs/master.lib/atan8[data].asm'),
             ('sine', 1192, 640, 'libs/master.lib/sin8[data].asm')],
         'bounded formula-derived tables only')
    return cfg, digest


def generated(cfg):
    source = ROOT / cfg['source']
    parts = runpy.run_path(str(source))['generate']()
    need(set(parts) == {'generated/atan.inl', 'generated/sine.inl'} and
         all(isinstance(x, bytes) and x.isascii() for x in parts.values()),
         'formula-only, readable ASCII assembler declarations')
    return parts


def context(cfg, parts):
    raw = (WORK / 'th03_mainl.asm').read_bytes()
    need(sha(raw) == cfg['original_context_sha256'], 'pinned contextual root wrapper')
    for extent in cfg['table_extents']:
        old = extent['original_include'].encode('ascii')
        replacement = ('probe/' + STAGE + '/generated/' + extent['name'] + '.inl').encode()
        need(raw.count(old) == 1 and all(x < 128 for x in replacement), 'unique table include to replace')
        raw = raw.replace(old, replacement)
    return raw


def link_response(round_number):
    raw = parent.response(round_number)
    need(raw.count(b'af554b') == 8 and raw.count(rb'obj\th03\mainl.obj') == 1,
         'parent normal link, known source replacements')
    return raw.replace(b'af554b', STAGE.encode()).replace(
        rb'obj\th03\mainl.obj', ('probe\\' + STAGE + r'\mainl.obj').encode())


def structure_without_publics(raw):
    return [(r.name, r.data) for r in parse_omf(raw)
            if r.name not in ('THEADR', 'COMENT', 'PUBDEF', 'LEDATA', 'FIXUPP')]


def map_canonical(raw):
    # The symbol name in the map is a diagnostic path, not a size or address.
    needle = ('M=probe\\' + STAGE + r'\th03_mainl.asm').encode()
    need(raw.count(needle) == 9, 'all nine original root contributions preserved')
    return raw.replace(needle, b'M=th03_mainl.asm')


def table_bytes(cfg):
    table = runpy.run_path(str(ROOT / cfg['source']))['values']()
    a, sine = table
    return {'atan': bytes(a), 'sine': b''.join(struct.pack('<h', v) for v in sine)}


def main():
    cfg, cfg_hash = inputs()
    source = (ROOT / cfg['source']).read_bytes()
    parts = generated(cfg)
    asm = context(cfg, parts)
    original = (WORK / 'obj/th03/mainl.obj').read_bytes()
    need(sha(original) == cfg['original_object_sha256'], 'pinned original compiled root object')
    native = payload(original)
    expected = table_bytes(cfg)
    for extent in cfg['table_extents']:
        name, off, size = extent['name'], extent['data_offset'], extent['size']
        need(len(expected[name]) == size and
             bytes(native[2, off + i] for i in range(size)) == expected[name],
             'independent formula agrees with original native DATA ' + name)
    old, parent_hash = base.load(parent.REPORT)
    need(old['complete'] and parent_hash == cfg['parent_report_sha256'], 'retained after554 source parent')
    need(sha(TASM.read_bytes()) == 'ba50fe547863b96242d98cff54cdf95ab268a8682395afad172eedbfc46c5b26',
         'pinned TASM5 emitter')
    report = dict(complete=False, canonical_credit_changed=False, whole_product_accepted=False,
        cold_rebuilt=False, game_objects_recompiled=1, library_rebuilt=False,
        source_acceptance=False, game_source_bytes=0, library_source_DATA_bytes=896,
        source_sha256=sha(source), generated_sha256={k: sha(v) for k,v in parts.items()},
        context_sha256=sha(asm), config_sha256=cfg_hash, driver_sha256=sha((ROOT / DRIVER).read_bytes()),
        original_object_sha256=sha(original), parent_report_sha256=parent_hash,
        phases=[], rounds=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(report, indent=2) + '\n')
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
               WINEPREFIX=str(ROOT / '.analysis/toolchain/wineprefix'), MSDOS_PATH=r'C:\TC4\BIN',
               TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    tasm = ['/usr/bin/wine-stable', str(TASM)]

    def run(cmd, cwd, label):
        p = subprocess.run(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=100)
        log = PREFIX + label + '.log'
        (ROOT / log).write_bytes(p.stdout)
        report['phases'].append(dict(label=label, argv=cmd, returncode=p.returncode,
                                     log=log, log_sha256=sha(p.stdout)))
        save()
        need(p.returncode == 0, label + ': ' + p.stdout.decode(errors='replace')[-1400:])

    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(not SCRATCH.exists(), 'fresh retained trig table native stage')
        SCRATCH.mkdir()
        for name, raw in parts.items():
            path = SCRATCH / name
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(raw.replace(b'\n', b'\r\n'))
            os.utime(path, (946684800,946684800))
        (SCRATCH / 'th03_mainl.asm').write_bytes(asm)
        os.utime(SCRATCH / 'th03_mainl.asm', (946684800,946684800))
        (SCRATCH / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        (SCRATCH / 'config.json').write_bytes((ROOT / CONFIG).read_bytes())
        vectors = []
        for number in (1,2):
            previous = old['rounds'][number-1]
            reused = previous['reused']
            for k,filename in [('startup','c0l.obj'),('library',f'r{number}.lib'),
                               ('root','rootdata.obj'),('pictures','rootpre.obj')]:
                (SCRATCH / filename).write_bytes(base.checked(reused[k]))
            for k,filename in [('registration','regpre.obj'),('ending','regtail.obj')]:
                (SCRATCH / filename).write_bytes(base.checked(previous['outputs'][k]))
            run(tasm + ['/m','/mx','/kh32768','/t','/dGAME=3',
                 f'probe\\{STAGE}\\th03_mainl.asm,probe\\{STAGE}\\mainl.obj'],
                 WORK, f'round{number}-assemble')
            obj = (SCRATCH / 'mainl.obj').read_bytes()
            need(payload(obj) == native and literal_fields(obj) == literal_fields(original) and
                 len(literal_fields(obj)) == 392 and
                 public_offsets(obj) == public_offsets(original) and
                 structure_without_publics(obj) == structure_without_publics(original),
                 'entire root OBJ initializer, ordered fixups, public definitions and other metadata')
            rsp = link_response(number)
            (SCRATCH / f'r{number}.lnk').write_bytes(rsp)
            run(dos + ['tlink', '@probe\\' + STAGE + f'\\r{number}.lnk'], WORK,
                f'round{number}-link')
            vector = dict(obj=obj, exe=(SCRATCH / f'r{number}.exe').read_bytes(),
                          map=(SCRATCH / f'r{number}.map').read_bytes())
            need(vector['exe'] == base.checked(previous['outputs']['exe']) and
                 map_canonical(vector['map']) == base.checked(previous['outputs']['map']),
                 'complete original decoded EXE including relocations, and all MAP rows/locations')
            outputs = {}
            for k,v in vector.items():
                path = PREFIX + f'round{number}-{k}.bin'
                (ROOT / path).write_bytes(v)
                outputs[k] = dict(path=path, bytes=len(v), sha256=sha(v))
            report['rounds'].append(dict(round=number, reused=reused,
                  reused_banks={k: previous['outputs'][k] for k in ('registration','ending')},
                  response_sha256=sha(rsp), outputs=outputs))
            save()
            vectors.append(vector)
            print('Formula trig round', number, 'original 896 DATA; all392 fields; full target EXE exact',flush=True)
        need(vectors[0] == vectors[1] and (ROOT / cfg['source']).read_bytes() == source,
             'both complete OBJ/EXE/MAP native vectors and maintained source repeat')
    report['complete'] = True
    save()

if __name__ == '__main__':
    main()
