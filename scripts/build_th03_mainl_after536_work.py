#!/usr/bin/env python3
"""Refine baseline OMF ownership without treating a MAP alias tie as layout.

Preserve the entire original/source-bound receipt chain and all raw outputs.
Only the two selected owners are assembled; unchanged C0/game objects recur.
"""
import fcntl
import json
import os
import subprocess
import tomllib
from pathlib import Path

import build_th03_mainl_after535_work as parent
import review_th03_mainl_after535_work as parent_review
import bootstrap_jwasm
from build_th03_mainl_resources_work import need, sha
from lib.borland_library import library_members, compare_members, object_program_records

ROOT = parent.ROOT
b = parent.b
PROFILE = 'config/th03_mainl_baseline_refinements.toml'
DRIVER = 'scripts/build_th03_mainl_after536_work.py'
PREFIX = '.analysis/work/mainl-after536-baseline-refinements-'
RAW_PREFIX = '.analysis/work/af536f-baseline-refinements-'
REPORT = PREFIX + 'build.json'
SCRATCH = b.WORK / 'probe/af536f'
SOURCES = {n: 'src/mainl/crt/' + n + '_link.asm' for n in ('h_padd', 'ioerror')}
INCLUDES = ('src/mainl/crt/crt_errno.inc', 'src/mainl/crt/dos_error_map.inc')
SLOTS = {'h_padd': 72, 'ioerror': 79}


def emitter():
    raw = (ROOT / PROFILE).read_bytes()
    config = tomllib.loads(raw.decode())
    need(config['schema_version'] == 1 and
         config['tool_profile'] == bootstrap_jwasm.PROFILE and
         config['compatible_members'] == ['h_padd'] and
         config['tasm_members'] == ['ioerror'] and
         config['compatible_flags'] == ['-nologo', '-Cp', '-omf'] and
         config['tasm_flags'] == ['/m', '/mx', '/kh32768', '/t'] and
         config['original_assembler_identified'] is False, 'bounded emitter profile')
    return config, dict(profile_sha256=sha(raw),
        attestation_driver_sha256=sha(Path(bootstrap_jwasm.__file__).read_bytes()),
        tool=bootstrap_jwasm.attest())


def originals():
    raw = (ROOT / '.analysis/toolchain/wineprefix/drive_c/TC4/LIB/CL.LIB').read_bytes()
    members = library_members(raw)
    need(len(members) == 893 and all(members[i].name == n for n, i in SLOTS.items()),
         'actual original compiler-library slots')
    return {n: b.original_library_member(members[i]) for n, i in SLOTS.items()}, sha(raw)


def profile(blob):
    need(b.describe_omf(blob)['valid'], 'actual complete native OMF')
    segments = b.segment_definitions(blob)
    data = b.initialized_payload(blob)
    need(set(data) == {(s['index'], i) for s in segments for i in range(s['size'])},
         'complete original initialized coverage')
    records = b.parse_omf(blob)
    return dict(segments=segments,
        attributes=[r.data[0] for r in records if r.name == 'SEGDEF'],
        initialized=[dict(segment=s['index'], bytes=s['size'], sha256=sha(
            bytes(data[s['index'], i] for i in range(s['size'])))) for s in segments],
        imports=b.externs(blob),
        publics={str(s['index']): b.code_publics(blob, s['index']) for s in segments},
        literal_fields=b.literal_fields(blob),
        records={n: [r.data.hex() for r in records if r.name == n]
                 for n in ('SEGDEF', 'GRPDEF', 'PUBDEF', 'EXTDEF', 'ALIAS', 'MODEND')})


def compare(name, original, native):
    a, z = profile(original), profile(native)
    need(all(a[k] == z[k] for k in ('segments', 'attributes', 'initialized', 'imports', 'publics')) and
         all(a['records'][k] == z['records'][k] for k in ('GRPDEF', 'EXTDEF', 'ALIAS', 'MODEND')),
         'complete original bytes, segment/group ownership and external/public identity')
    key = lambda f: (f['segment'], f['site'])
    need(sorted(a['literal_fields'], key=key) == sorted(z['literal_fields'], key=key),
         'every complete literal frame/target/addend at its original position')
    if name == 'h_padd':
        # PUBDEF record packing and LNAMES indices may differ. No PUBLIC is
        # sorted: these are the original/native literal ordered symbol payloads.
        expected = b.parent.ordered_public_payload(original)
        observed = b.parent.ordered_public_payload(native)
        need(expected == observed and sha(expected) ==
             '31883da383c3889f19d039fe47f0fce0619b21ae90fd7fee9f33b79ddce1070e' and
             not a['literal_fields'] and not z['literal_fields'],
             'original six-export chronology and absence of relocation fields')
    else:
        need([f['site'] for f in a['literal_fields']] == [22, 28, 45, 39, 51] and
             [f['site'] for f in z['literal_fields']] == [22, 28, 39, 45, 51],
             'explicit remaining ioerror ordered FIXUPP gap')
    return dict(original=a, native=z,
        literal_ordered_fields_equal=a['literal_fields'] == z['literal_fields'],
        literal_ordered_PUBLIC_payload_equal=(name == 'h_padd'),
        literal_GROUP_equal=True,
        original_program_equal=object_program_records(original) == object_program_records(native))


def map_review(baseline, candidate):
    # Compare the full output with the expected tie exchange and zero-BSS row.
    # Neither input artifact is ever rewritten. Addresses, sizes, idle flags,
    # all other PUBLICs and every other MAP byte must remain unchanged.
    pair = (b' 0000:3182 idle  PADD@\r\n', b' 0000:3182 idle  F_PADD@\r\n')
    need(baseline.count(pair[0] + pair[1]) == 1, 'unique retained same-address alias tie')
    expected = baseline.replace(pair[0] + pair[1], pair[1] + pair[0], 1)
    anchor = b' 0E3F:286A 0000 C=BSS    S=_BSS           G=DGROUP  M=getvect    ACBP=48\r\n'
    zero_owner = b' 0E3F:286A 0000 C=BSS    S=_BSS           G=DGROUP  M=ioerror    ACBP=48\r\n'
    need(baseline.count(anchor) == 1 and zero_owner not in baseline,
         'unique existing BSS position and previously omitted zero-extent owner')
    expected = expected.replace(anchor, anchor + zero_owner, 1)
    need(candidate == expected and candidate != baseline and
         len(candidate) == len(baseline) + len(zero_owner),
         'whole raw MAP has exactly the alias tie exchange and zero-extent BSS owner')
    return dict(raw_equal=False, bytes=len(candidate), baseline_sha256=sha(baseline),
        candidate_sha256=sha(candidate), address='0000:3182',
        prior_alias_order=['PADD@', 'F_PADD@'], original_PUBLIC_alias_order=['F_PADD@', 'PADD@'],
        added_zero_extent_owner=dict(module='ioerror', segment='_BSS', address='0E3F:286A', bytes=0),
        all_other_MAP_bytes_equal=True, all_addresses_sizes_and_flags_equal=True)


def main():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    baseline = parent_review.review()
    old, old_hash = parent.parent.load(parent.REPORT)
    vectors = [{k: parent.parent.retained(v) for k, v in row['outputs'].items()} for row in old['rounds']]
    need(vectors[0] == vectors[1], 'unchanged source-startup/library/native pair')
    original, original_hash = originals()
    config, attestation = emitter()
    source = {n: (ROOT / p).read_bytes() for n, p in SOURCES.items()}
    includes = {p: sha((ROOT / p).read_bytes()) for p in INCLUDES}
    prefix = ROOT / '.analysis/toolchain/wineprefix'
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all',
        WINEPREFIX=str(prefix), MSDOS_PATH=r'C:\TC4\BIN', TZ='UTC', LANG='C', LC_ALL='C')
    dos = ['/usr/bin/wine-stable', str(ROOT / '_reference/ReC98/bin/msdos.exe'), '-e', '-x']
    tasm = ['/usr/bin/wine-stable', str(prefix / 'drive_c/TASM50/bin/TASM32.EXE')]
    jwasm = str(ROOT / '.analysis/toolchain/extra/jwasm/GccUnixR/jwasm')
    record = dict(complete=False, source_acceptance=False, new_source_members=0, new_CODE_bytes=0,
        cold_rebuilt=False, driver_sha256=sha((ROOT / DRIVER).read_bytes()),
        parent_build_sha256=old_hash, parent_review=baseline, emitter_attestation=attestation,
        source_paths=SOURCES, source_sha256={n: sha(v) for n, v in source.items()},
        source_include_sha256=includes, original_compiler_library_sha256=original_hash,
        phases=[], rounds=[])
    save = lambda: (ROOT / REPORT).write_text(json.dumps(record, indent=2) + '\n')

    def run(argv, cwd, label):
        p = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=90)
        path = RAW_PREFIX + label + '.log'
        (ROOT / path).write_bytes(p.stdout)
        record['phases'].append(dict(label=label, argv=argv, returncode=p.returncode,
                                     log_path=path, log_sha256=sha(p.stdout)))
        save()
        need(p.returncode == 0, label + ': ' + p.stdout.decode(errors='replace')[-1200:])

    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        need(not SCRATCH.exists(), 'fresh retained two-owner work directory')
        SCRATCH.mkdir()
        for name, raw in source.items():
            (SCRATCH / (name + '.asm')).write_bytes(raw)
            os.utime(SCRATCH / (name + '.asm'), (946684800, 946684800))
        for p in INCLUDES:
            (SCRATCH / Path(p).name).write_bytes((ROOT / p).read_bytes())
        (SCRATCH / 'driver.py').write_bytes((ROOT / DRIVER).read_bytes())
        (SCRATCH / 'profile.toml').write_bytes((ROOT / PROFILE).read_bytes())
        (SCRATCH / 'base.lib').write_bytes(vectors[0]['lib'])
        (SCRATCH / 'c0l.obj').write_bytes(vectors[0]['startup'])
        members = library_members(vectors[0]['lib'])
        extract = b.build.response('base.lib', ['*' + m.name for m in members])
        (SCRATCH / 'extract.rsp').write_bytes(extract)
        run(dos + ['tlib', '@extract.rsp'], SCRATCH, 'extract')
        extracted = {p.stem.casefold(): p for p in SCRATCH.iterdir()
                     if p.suffix.casefold() == '.obj' and p.stem.casefold() != 'c0l'}
        need(set(extracted) == {m.name.casefold() for m in members},
             'complete source-library extraction')
        for member in members:
            path = extracted[member.name.casefold()]
            destination = SCRATCH / (member.name + '.obj')
            if path != destination:
                path.rename(destination)
        produced = []
        for number in (1, 2):
            run([jwasm, *config['compatible_flags'], '-Foh_padd.obj', 'h_padd.asm'],
                SCRATCH, f'round{number}-h_padd')
            run(tasm + config['tasm_flags'] + ['ioerror.asm,ioerror.obj'],
                SCRATCH, f'round{number}-ioerror')
            fresh = {n: (SCRATCH / (n + '.obj')).read_bytes() for n in SOURCES}
            comparison = {n: compare(n, original[n], fresh[n]) for n in SOURCES}
            rsp = b.build.response(f'probe\\af536f\\r{number}.lib /E',
                ['+probe\\af536f\\' + m.name + '.obj' for m in members])
            (SCRATCH / f'r{number}.rsp').write_bytes(rsp)
            run(dos + ['tlib', f'@probe\\af536f\\r{number}.rsp'], b.WORK,
                f'round{number}-library')
            library = (SCRATCH / f'r{number}.lib').read_bytes()
            library_comparison = compare_members(members, library_members(library), fresh)
            response = (b.WORK / 'obj/th03/mainl.@l').read_bytes()
            for a, z in ((b'c0l.obj', rb'probe\af536f\c0l.obj'),
                         (rb'bin\th03\mainl.exe', f'probe\\af536f\\r{number}.exe'.encode()),
                         (rb'obj\th03\mainl.map', f'probe\\af536f\\r{number}.map'.encode()),
                         (b' crt.lib', f' probe\\af536f\\r{number}.lib'.encode())):
                need(response.count(a) == 1, 'one scoped source-object/library link substitution')
                response = response.replace(a, z)
            (SCRATCH / f'r{number}.lnk').write_bytes(response)
            run(dos + ['tlink', f'@probe\\af536f\\r{number}.lnk'], b.WORK,
                f'round{number}-link')
            vector = dict(fresh, lib=library, exe=(SCRATCH / f'r{number}.exe').read_bytes(),
                          map=(SCRATCH / f'r{number}.map').read_bytes())
            outputs = {}
            for kind, raw in vector.items():
                path = RAW_PREFIX + f'round{number}-' + kind + ('.obj' if kind in SOURCES else '.' + kind)
                (ROOT / path).write_bytes(raw)
                outputs[kind] = dict(path=path, bytes=len(raw), sha256=sha(raw))
            record['rounds'].append(dict(round=number, outputs=outputs,
                comparison=comparison, library_comparison=library_comparison,
                link_response_sha256=sha(response), library_response_sha256=sha(rsp),
                map_review=map_review(vectors[number - 1]['map'], vector['map'])))
            save()
            need(vector['exe'] == vectors[number - 1]['exe'] and
                 library_comparison['contextual_members_unchanged'] == 891,
                 'complete original Japanese EXE and all 891 other source member programs')
            produced.append(vector)
            print('Baseline refinement round', number, 'EXE exact; MAP alias tie reviewed', flush=True)
        need(produced[0] == produced[1], 'two raw native OBJ/LIB/EXE/MAP vectors repeat')
    need(record['source_sha256'] == {n: sha((ROOT / p).read_bytes()) for n, p in SOURCES.items()} and
         record['source_include_sha256'] == {p: sha((ROOT / p).read_bytes()) for p in INCLUDES} and
         record['emitter_attestation'] == emitter()[1], 'source/includes/emitter unchanged')
    record['complete'] = True
    save()


if __name__ == '__main__':
    main()
