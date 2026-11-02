#!/usr/bin/env python3
"""Rebuild one original DOS CRT memcpy member and relink only its MAINL carrier.

The existing decoded cold pair and the accepted 28-provider library are reused;
the full source cold/DIET pipeline is deliberately not replayed here.
"""
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
import tomllib

import build_th03_mainl_work as build
import build_th03_mainl_xx_work as baseline_provider
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import compare_members, library_members, object_program_records
from build_th03_mainl_display_work import payload, literal_fields
from lib.omf import describe_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics
from lib.decoded_mainl_display_native import externs

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'src/mainl/crt/memcpy.asm'
DRIVER = 'scripts/build_th03_mainl_memcpy_work.py'
REPORT = '.analysis/work/mainl-memcpy-build.json'
WORK = build.WORK
SCRATCH = WORK/'probe/mcpctx'
MEMBER = 'memcpy'
TARGET_OBJ = WORK/'vendor/memcpy.obj'
TASM_FLAGS = ['/m', '/mx', '/kh32768', '/t', 'memcpy.asm', 'memcpy.obj']


def native_scope(obj):
    # All 36 instructions are native TASM product output, not an embedded
    # binary constant. Zero-length DATA/BSS are distinct segments.
    segs = segment_definitions(obj)
    need([(s['name'], s['class'], s['size']) for s in segs] ==
         [('_TEXT', 'CODE', 36), ('_DATA', 'DATA', 0), ('_BSS', 'BSS', 0)],
         'one 36-byte CODE owner, plus empty DATA and BSS')
    need(code_publics(obj, 1) == [(0, '_memcpy')] and not externs(obj),
         'one public far memcpy and no external imports')
    need(not literal_fields(obj) and describe_omf(obj)['valid'],
         'valid native OMF with no relocation fields')
    contents = payload(obj)
    return bytes(contents[1, i] for i in range(36))


def link_response(files):
    link = baseline_provider.link_response(files)
    replacements = {
        b'probe\\xxwhole\\xxfull.exe': b'probe\\mcpctx\\linked.exe',
        b'probe\\xxwhole\\xxfull.map': b'probe\\mcpctx\\linked.map',
        b'probe\\xxwhole\\xxcrt.lib': b'probe\\mcpctx\\newcrt.lib',
    }
    for old, new in replacements.items():
        need(link.count(old) == 1, 'one source-only linker output position')
        link = link.replace(old, new)
    return link


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10-os.nice(0))
    base, files, library, members, _ = baseline_provider.baseline(ROOT)
    need(len(members) == 893 and
         [(i, m.name) for i, m in enumerate(members) if m.name == MEMBER] ==
         [(261, MEMBER)], 'original fixed memcpy library membership')
    original = TARGET_OBJ.read_bytes()
    need(object_program_records(original) ==
         next(m.program_records for m in members if m.name == MEMBER),
         'original literal library member records are retained')
    original_code = native_scope(original)
    source = (ROOT/SOURCE).read_bytes()
    config = tomllib.loads((ROOT/'config/toolchain.toml').read_text())
    prefix = ROOT/config['paths']['wine_prefix']
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
               WINEPREFIX=str(prefix), MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC',
               LANG='C', LC_ALL='C')
    tasm = ['/usr/bin/wine-stable', str(prefix/'drive_c/TASM50/bin/TASM32.EXE')]
    dos = ['/usr/bin/wine-stable', str(ROOT/config['paths']['msdos_player']), '-e', '-x']
    report = dict(complete=False, source_acceptance=False, added_accepted_bytes=0,
                  original_cold_rebuilt=False, reused_accepted_library=base,
                  original_member_sha256=sha(original),
                  current_library_sha256=sha(library),
                  source_sha256=sha(source), driver_sha256=sha((ROOT/DRIVER).read_bytes()),
                  phases=[], rounds=[])
    save = lambda: (ROOT/REPORT).write_text(json.dumps(report, indent=2)+'\n')

    def execute(command, cwd, label):
        result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=120)
        log = result.stdout
        output = f'.analysis/work/memcpy-{label}.log'
        (ROOT/output).write_bytes(log)
        report['phases'].append(dict(label=label, command=command,
                                     returncode=result.returncode,
                                     log_path=output, log_sha256=sha(log)))
        save()
        need(result.returncode == 0, label+': '+log.decode(errors='replace')[-1500:])

    with (ROOT/'.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        need(not SCRATCH.exists(), 'fresh isolated TASM/TLIB/TLINK scratch')
        SCRATCH.mkdir()
        try:
            (SCRATCH/'base.lib').write_bytes(library)
            extract = build.response('base.lib', ['*'+m.name for m in members])
            (SCRATCH/'extract.rsp').write_bytes(extract)
            execute(dos+['tlib', '@extract.rsp'], SCRATCH, 'extract')
            actual = {p.stem.casefold(): p for p in SCRATCH.iterdir()
                      if p.suffix.casefold() == '.obj'}
            need(set(actual) == {m.name.casefold() for m in members},
                 '893 original extracted native members')
            for m in members:
                found = actual[m.name.casefold()]
                need(object_program_records(found.read_bytes()) == m.program_records,
                     'unchanged native library member '+m.name)
                destination = SCRATCH/(m.name+'.obj')
                if found != destination:
                    found.rename(destination)
            (SCRATCH/'memcpy.asm').write_bytes(source)
            os.utime(SCRATCH/'memcpy.asm', (946684800, 946684800))
            libinput = build.response(r'probe\mcpctx\newcrt.lib /E',
                ['+probe\\mcpctx\\'+m.name+'.obj' for m in members])
            link = link_response(files)
            (SCRATCH/'library.rsp').write_bytes(libinput)
            (SCRATCH/'link.lnk').write_bytes(link)
            (ROOT/'.analysis/work/memcpy-library.rsp').write_bytes(libinput)
            (ROOT/'.analysis/work/memcpy-link.lnk').write_bytes(link)
            for number in (1, 2):
                for name in ('memcpy.obj', 'newcrt.lib', 'newcrt.bak',
                             'linked.exe', 'linked.map'):
                    (SCRATCH/name).unlink(missing_ok=True)
                execute(tasm+TASM_FLAGS, SCRATCH, f'round{number}-assemble')
                emitted = (SCRATCH/'memcpy.obj').read_bytes()
                need(native_scope(emitted) == original_code,
                     'complete raw36-byte original/native memcpy CODE equality')
                execute(dos+['tlib', r'@probe\mcpctx\library.rsp'],
                        WORK, f'round{number}-library')
                result_lib = (SCRATCH/'newcrt.lib').read_bytes()
                comparison = compare_members(members, library_members(result_lib),
                                             {MEMBER: emitted})
                need(comparison['contextual_members_unchanged'] == 892 and
                     comparison['replaced_members'] == [MEMBER],
                     'one original-position native source member,892 unchanged')
                execute(dos+['tlink', r'@probe\mcpctx\link.lnk'],
                        WORK, f'round{number}-link')
                outputs = {}
                for key, name in [('obj', 'memcpy.obj'), ('lib', 'newcrt.lib'),
                                  ('exe', 'linked.exe'), ('map', 'linked.map')]:
                    data = (SCRATCH/name).read_bytes()
                    where = f'.analysis/work/memcpy-round{number}-{name}'
                    (ROOT/where).write_bytes(data)
                    outputs[key] = dict(path=where, bytes=len(data), sha256=sha(data))
                need((SCRATCH/'linked.exe').read_bytes() ==
                     (WORK/'bin/th03/mainl.target.exe').read_bytes(),
                     'actual full decoded Japanese MAINL EXE raw equality')
                candidate_map = (SCRATCH/'linked.map').read_bytes()
                original_map = (WORK/'obj/th03/mainl.map').read_bytes()
                need(candidate_map == original_map,
                     'actual complete source-replacement MAINL MAP raw equality')
                report['rounds'].append(dict(round=number, outputs=outputs,
                                             library_comparison=comparison,
                                             native_code_sha256=sha(original_code)))
                save()
                print('MAINL memcpy native source/link exact round', number, flush=True)
            need({k:v['sha256'] for k,v in report['rounds'][0]['outputs'].items()} ==
                 {k:v['sha256'] for k,v in report['rounds'][1]['outputs'].items()},
                 'two complete deterministic raw OBJ/LIB/EXE/MAP vectors')
        finally:
            shutil.rmtree(SCRATCH)
    later, _, current_library, current_members, _ = baseline_provider.baseline(ROOT)
    need(later == base and current_library == library and
         [m.program_records for m in members] ==
         [m.program_records for m in current_members] and
         source == (ROOT/SOURCE).read_bytes(), 'accepted native baseline and source unchanged')
    report['complete'] = True
    save()


if __name__ == '__main__':
    main()
