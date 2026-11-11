#!/usr/bin/env python3
"""Rebuild the CL runtime contributors used by the current three MZ products."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tomllib

import build_th03_package_current as package
from build_th03_mainl_after329_work import original_library_member
from build_th03_mainl_after533_work import initialized_payload
from build_th03_mainl_display_work import literal_fields
from build_th03_mainl_work import response
from build_th03_runtime_after541_work import ordered_publics
from lib.borland_library import library_members, compare_members, object_program_records
from lib.decoded_mainl_display_native import externs
from lib.omf import parse_omf
from probe_th03_main_bomb_rikako_cpp import segment_definitions

ROOT, DRIVE = package.ROOT, package.DRIVE
STAGE = 'af1405r'
DRIVER = 'scripts/build_th03_runtime_current.py'
BCC_CONFIG = 'config/mainl_work/exception_toolchain.toml'
HEADERS = ('STDIO.H', 'STDLIB.H', '_DEFS.H', '_NFILE.H', '_NULL.H')
BCC_FLAGS = ('-a-', '-c', '-k-', '-O1', '-2-', '-Vs', '-w', '-w-asm', '-X',
             '-zC_TEXT', '-zR_DATA', '-zTDATA', r'-IC:\TC4\INCLUDE', '-ml')
SUPPORT = ('scripts/build_th03_mainl_after329_work.py',
           'scripts/build_th03_mainl_after533_work.py',
           'scripts/build_th03_mainl_display_work.py',
           'scripts/build_th03_mainl_work.py',
           'scripts/build_th03_runtime_after541_work.py',
           'scripts/lib/borland_library.py', 'scripts/lib/decoded_mainl_display_native.py',
           'scripts/lib/omf.py', 'scripts/probe_th03_main_bomb_rikako_cpp.py')
need, sha, pin = package.need, package.sha, package.pin


def context(stage, reviewed=None):
    need(re.fullmatch(r'af[0-9]+[a-z]', stage), 'DOS-safe runtime stage')
    reviewed = package.review() if reviewed is None else reviewed
    parent, _, _, parent_inputs, _, maps = package.context(package.STAGE, {})
    original = DRIVE / 'TC4/LIB/CL.LIB'
    members = library_members(original.read_bytes())
    names = {m.name for m in members}
    selected = {product: sorted({n.decode() for n in re.findall(rb'\bM=(\S+)', raw)} & names)
                for product, raw in maps.items()}
    union = set().union(*map(set, selected.values()))
    recipe = {n: dict(source=f'src/mainl/crt/{n}.asm', emitter='tasm') for n in union if n != 'xx'}
    recipe['h_padd'] = dict(source='src/mainl/crt/h_padd_link.asm', emitter='jwasm')
    recipe['exec'] = dict(source='src/shared/crt/dos_exec.asm', emitter='tasm')
    configs = ['config/th03_runtime_after537.json', 'config/th03_mainl_baseline_refinements.toml']
    for number in range(538, 548):
        name = f'config/th03_runtime_after{number}.json'; configs.append(name)
        q = json.loads((ROOT / name).read_bytes())
        compatible = q.get('compatible_members', list(q['source_paths'])
                           if 'tasm' not in q.get('native_tools', {'tasm': {}}) else [])
        for n, path in q['source_paths'].items():
            if n in union:
                recipe[n] = dict(source=path, emitter='jwasm' if n in compatible else 'tasm')
    config = json.loads((ROOT / configs[0]).read_bytes())
    need(sha(original.read_bytes()) == config['original_compiler_library_sha256'], 'original CL supplier identity')
    need(set(recipe) | {'xx'} == union, 'source for every current MAP runtime contributor')
    recipe['setvbuf'] = dict(source='src/shared/crt/stdio_buffer.c', emitter='bcc45')
    sources = {n + Path(row['source']).suffix: (ROOT / row['source']).read_bytes() for n, row in recipe.items()}
    includes = {}
    def include(path):
        for token in re.findall(rb'(?im)^\s*include\s+([^\s;]+)', path.read_bytes()):
            name = token.decode(); dependency = ROOT / 'src/mainl/crt' / name
            need(Path(name).name == name, 'local bounded CRT include')
            if name not in includes:
                includes[name] = dependency.read_bytes(); include(dependency)
    for row in recipe.values():
        include(ROOT / row['source'])
    sources.update(includes)
    xx = [DRIVE / f'TH03ML/probe/af1369m/r{n}/xx/xx.obj' for n in (1, 2)]
    need(xx[0].read_bytes() == xx[1].read_bytes(), 'independently compiled current xx pair')
    tools = json.loads((ROOT / 'config/th03_runtime_after547.json').read_bytes())['native_tools']
    tools['tasm'] = json.loads((ROOT / package.STARTUP_CONFIG).read_bytes())['native_tools']['tasm']
    bcc = tomllib.loads((ROOT / BCC_CONFIG).read_text())
    for declaration in bcc['surfaces']:
        tools[declaration['name']] = dict(path=declaration['active'], sha256=declaration['sha256'])
    for name, declaration in tools.items():
        need(sha((ROOT / declaration['path']).read_bytes()) == declaration['sha256'], 'pinned runtime tool: ' + name)
    inputs = {n: sha((ROOT / n).read_bytes()) for n in (DRIVER, *SUPPORT, *configs, package.DRIVER, BCC_CONFIG)}
    for name in HEADERS:
        path = DRIVE / 'TC4/INCLUDE' / name
        inputs[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    inputs.update({row['source']: sha((ROOT / row['source']).read_bytes()) for row in recipe.values()})
    inputs.update({'src/mainl/crt/' + n: sha(raw) for n, raw in includes.items()})
    for path in (original, *xx):
        inputs[str(path.relative_to(ROOT))] = sha(path.read_bytes())
    inputs.update({d['path']: d['sha256'] for d in tools.values()})
    inputs.update(parent_inputs)
    return DRIVE / 'TH03RT' / stage, reviewed, inputs, selected, recipe, sources, members, tools, xx


def scope(original, native, name):
    a, z = segment_definitions(original), segment_definitions(native)
    x, y = initialized_payload(original), initialized_payload(native)
    records = lambda raw, kind: [q.data.hex() for q in parse_omf(raw) if q.name == kind]
    need(a == z and x == y, 'complete original storage, initialized bytes and true holes: ' + name)
    need([q.data[0] for q in parse_omf(original) if q.name == 'SEGDEF'] ==
         [q.data[0] for q in parse_omf(native) if q.name == 'SEGDEF'], 'native segment attributes: ' + name)
    need(externs(original) == externs(native), 'complete literal import order: ' + name)
    key = lambda p: (p['name'], p['segment'], p['offset'])
    ap, zp = ordered_publics(original), ordered_publics(native)
    need(sorted(ap, key=key) == sorted(zp, key=key), 'complete public ownership/group/frame: ' + name)
    for kind in ('GRPDEF', 'ALIAS', 'MODEND'):
        need(records(original, kind) == records(native, kind), 'literal native ' + kind + ': ' + name)
    aa, zz = literal_fields(original), literal_fields(native)
    need(aa == zz, 'entire literal ordered field stream: ' + name)
    return dict(segments=a, initialized_bytes=len(y),
                initialized_sha256=sha(bytes(v for _, v in sorted(y.items()))),
                uninitialized={str(s['index']): [i for i in range(s['size']) if (s['index'], i) not in y] for s in z},
                original_fields=aa, native_fields=zz, literal_ordered_fields_equal=aa == zz,
                original_publics=ap, native_publics=zp, PUBLIC_order_equal=ap == zp,
                original_imports=externs(original), fresh_initialized_storage_equal=True,
                original_field_scope_accepted=aa == zz)


def commands(base, recipe, tools, number):
    for name, row in sorted(recipe.items()):
        if row['emitter'] == 'tasm':
            argv = package.native() + [str(ROOT / tools['tasm']['path']), '/m', '/mx', '/kh32768', '/t',
                                      f'{name}.asm,{name}.obj']
        elif row['emitter'] == 'jwasm':
            argv = [str(ROOT / tools['jwasm']['path']), '-nologo', '-Cp', '-omf', '-Fo' + name + '.obj', name + '.asm']
        else:
            need(name == 'setvbuf' and row['emitter'] == 'bcc45', 'bounded source C provider')
            argv = package.dos() + [package.windows(ROOT / tools['bcc']['path']), *BCC_FLAGS, name + '.c']
        yield name, argv, base
    yield 'library', package.dos() + ['tlib', '@' + package.windows(base / f'r{number}/library.rsp')], base


def archive_response(base, members, recipe, number):
    def path(name):
        return base / (name + '.obj') if name in recipe or name == 'xx' else base / 'vendor' / (name + '.obj')
    return response(package.windows(base / f'r{number}/linked.lib') + ' /E',
                    ['+' + package.windows(path(m.name)) for m in members])


def verify(stage=STAGE, reviewed=None):
    base, parent, inputs, selected, recipe, sources, originals, tools, xx = context(stage, reviewed)
    report = json.loads((base / 'runtime-build.json').read_bytes())
    need(report['complete'] and report['stage'] == stage and report['inputs'] == inputs and
         report['parent'] == parent and report['selected'] == selected and report['recipe'] == recipe,
         'complete current runtime context and actual selected contributors')
    need(all((base / name).read_bytes() == raw for name, raw in sources.items()), 'all actual source snapshots')
    extract = response('original.lib', ['*' + m.name for m in originals])
    need((base / 'vendor/original.lib').read_bytes() == (DRIVE / 'TC4/LIB/CL.LIB').read_bytes() and
         (base / 'vendor/extract.rsp').read_bytes() == extract, 'actual original native TLIB extraction inputs')
    expected = [('extract', package.dos() + ['tlib', '@extract.rsp'], str(base / 'vendor'), 0)]
    expected += [(f'r{n}-{label}', argv, str(cwd), 0) for n in (1, 2)
                 for label, argv, cwd in commands(base, recipe, tools, n)]
    need([(p['label'], p['argv'], p['cwd'], p['returncode']) for p in report['phases']] == expected, 'all actual native runtime commands')
    for phase in report['phases']:
        need(sha((base / (phase['label'] + '.log')).read_bytes()) == phase['log_sha256'], 'actual runtime writer log')
    for m in originals:
        need((base / 'vendor' / (m.name + '.obj')).is_file(), 'retained actual extraction input: ' + m.name)
        need(object_program_records((base / 'vendor' / (m.name + '.obj')).read_bytes()) == m.program_records,
             'complete original native extraction: ' + m.name)
    vectors = []
    need(len(report['rounds']) == 2 and [r['round'] for r in report['rounds']] == [1, 2], 'two native runtime rounds')
    for number, row in enumerate(report['rounds'], 1):
        rd = base / f'r{number}'
        need((rd / 'library.rsp').read_bytes() == archive_response(base, originals, recipe, number), 'complete ordered native archive response')
        names = {n + '.obj' for n in recipe} | {'xx.obj', 'linked.lib'}
        need(set(row['outputs']) == names and row['outputs'] == {n: pin(rd / n) for n in names}, 'all runtime output bytes')
        fresh = {n: (rd / (n + '.obj')).read_bytes() for n in (*recipe, 'xx')}
        need(fresh['xx'] == xx[number - 1].read_bytes(), 'current independently compiled xx output')
        scopes = {m.name: scope(original_library_member(m), fresh[m.name], m.name) for m in originals if m.name in fresh}
        need(row['scopes'] == scopes, 'all complete original-object physical scopes')
        compare_members(originals, library_members((rd / 'linked.lib').read_bytes()), fresh)
        vectors.append({n: (rd / n).read_bytes() for n in names})
    need(vectors[0] == vectors[1], 'all raw runtime objects and native library repeat')
    remaining = sorted(n for n, s in report['rounds'][0]['scopes'].items() if not s['literal_ordered_fields_equal'])
    return dict(stage=stage, selected_members=len(recipe) + 1, fresh_ASM_providers=len(recipe) - 1,
                fresh_C_providers=1,
                reused_independent_CPP_providers=1, native_rounds=2, raw_repeat_equal=True,
                original_field_order_equal_members=sum(s['literal_ordered_fields_equal'] for s in report['rounds'][0]['scopes'].values()),
                remaining_field_order_members=remaining, canonical_source_credit_added=False,
                libraries=[str((base / f'r{n}/linked.lib').relative_to(ROOT)) for n in (1, 2)])


def build(stage):
    base, parent, inputs, selected, recipe, sources, originals, tools, xx = context(stage)
    need(not base.exists(), 'unused runtime stage')
    report = dict(complete=False, stage=stage, inputs=inputs, parent=parent,
                  selected=selected, recipe=recipe, phases=[], rounds=[])
    env = dict(os.environ, DISPLAY='', WAYLAND_DISPLAY='', WINEDEBUG='-all', MSDOS_PATH=r'C:\TC4\BIN')
    def run(label, argv, cwd):
        p = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        (base / (label + '.log')).write_bytes(p.stdout)
        report['phases'].append(dict(label=label, argv=argv, cwd=str(cwd), returncode=p.returncode, log_sha256=sha(p.stdout)))
        need(p.returncode == 0, 'runtime native phase: ' + label)
    with (ROOT / '.analysis/borland-wine-writer.lock').open('ab') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        (base / 'vendor').mkdir(parents=True)
        for name, raw in sources.items():
            p = base / name; p.write_bytes(raw); os.utime(p, (946684800, 946684800))
        (base / 'vendor/original.lib').write_bytes((DRIVE / 'TC4/LIB/CL.LIB').read_bytes())
        (base / 'vendor/extract.rsp').write_bytes(response('original.lib', ['*' + m.name for m in originals]))
        run('extract', package.dos() + ['tlib', '@extract.rsp'], base / 'vendor')
        # Native TLIB lowercases extracted filenames on this DOS host.
        for m in originals:
            old = next(p for p in (base / 'vendor').iterdir() if p.name.casefold() == (m.name + '.obj').casefold())
            if old.name != m.name + '.obj':
                old.rename(old.with_name(m.name + '.obj'))
        for number in (1, 2):
            rd = base / f'r{number}'; rd.mkdir()
            (base / 'xx.obj').write_bytes(xx[number - 1].read_bytes())
            (rd / 'library.rsp').write_bytes(archive_response(base, originals, recipe, number))
            for label, argv, cwd in commands(base, recipe, tools, number):
                if label != 'library':
                    (base / (label + '.obj')).unlink(missing_ok=True)
                run(f'r{number}-{label}', argv, cwd)
                if label != 'library':
                    out = next(p for p in base.iterdir() if p.name.casefold() == (label + '.obj').casefold())
                    if out.name != label + '.obj': out.rename(base / (label + '.obj'))
            fresh = {n: (base / (n + '.obj')).read_bytes() for n in (*recipe, 'xx')}
            scopes = {m.name: scope(original_library_member(m), fresh[m.name], m.name) for m in originals if m.name in fresh}
            compare_members(originals, library_members((rd / 'linked.lib').read_bytes()), fresh)
            for name, raw in fresh.items(): (rd / (name + '.obj')).write_bytes(raw)
            names = {n + '.obj' for n in fresh} | {'linked.lib'}
            report['rounds'].append(dict(round=number, scopes=scopes, outputs={n: pin(rd / n) for n in names}))
            print(f'Runtime round {number}: {len(recipe) - 1} fresh ASM providers, natural C setvbuf and current source xx; complete original storage/fields checked', flush=True)
        report['complete'] = True
        (base / 'runtime-build.json').write_text(json.dumps(report, indent=2) + '\n')
    return verify(stage, parent)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stage', default=STAGE); p.add_argument('--build', action='store_true')
    args = p.parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10: os.nice(10 - os.nice(0))
    print(json.dumps(build(args.stage) if args.build else verify(args.stage), indent=2))


if __name__ == '__main__':
    main()
