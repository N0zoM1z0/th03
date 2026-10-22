#!/usr/bin/env python3
"""Stage five original OP helper TUs. Source-only; no compiler or native tools."""
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CONFIG = 'config/th03_op_remaining_helpers_candidate.json'
CONFIG_SHA = 'c5042a007a6dfa6f2d9254d12836c060e0afa57a0d4a028423d36666bc569d8c'
EXPECTED = (
    ('snd_determine_mode', 'th02/snd_mode.c', 2, 'c', 0x4a, 29, 30),
    ('snd_pmd_resident', 'th02/snd_pmdr.c', 2, 'c', 0x68, 57, 58),
    ('polar', 'th03/polar.cpp', 3, 'cpp', 0x155, 26, 26),
    ('snd_kaja_interrupt', 'th03/snd_kaja.cpp', 3, 'cpp', 0x553, 30, 30),
    ('game_init_op', 'th03/initop.cpp', 3, 'cpp', 0x571, 105, 105),
)
PRAGMAS = (
    b'#pragma option -WX -zCSHARED -k-\n',
    b'#pragma option -zCSHARED -k-\n',
    b'#pragma option -zCSHARED\n',
    b'#pragma option -zCSHARED\n',
    b'#pragma option -zCSHARED -3\n',
)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def need(ok, message):
    if not ok:
        raise ValueError(message)

def safe_path(name):
    p = Path(name)
    need(not p.is_absolute() and '..' not in p.parts and name == p.as_posix(), 'unsafe source path')
    return p

def regular(path):
    path = Path(path)
    need(not any(p.is_symlink() for p in (path, *path.parents)), 'symlink input')
    need(path.is_file(), 'missing input ' + str(path))
    return path.read_bytes()

def validate_config(config):
    need(config['schema'] == 'th03-op-remaining-helpers-source-v1', 'schema')
    need(config['source_acceptance'] is False and config['exact_acceptance'] is False, 'credit inflation')
    units = config['units']
    need(len(units) == 5, 'five physical translation units')
    for index, (unit, expected) in enumerate(zip(units, EXPECTED)):
        keys = ('name', 'wrapper', 'physical_game_macro', 'language', 'offset', 'size', 'producer_bytes')
        need(tuple(unit[k] for k in keys) == expected, 'original producer or extent changed')
        need(unit['compare_size'] == unit['size'] and unit['segment'] == 'decoded:0beb', 'extent identity')
        need(unit['compiler'] == 'tcc', 'original compiler')
        wrapper = safe_path(unit['wrapper'])
        command = "bin\\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=%d -ml -DBINARY='O' -nobj/%s/ %s" % (unit['physical_game_macro'], wrapper.parent.as_posix(), wrapper.as_posix())
        need(unit['original_command'] == command, 'literal original producer command')
        need(unit['object'] == 'obj/' + str(wrapper.with_suffix('.obj')), 'physical object identity')
        for field in ('source', 'original_body', 'wrapper', 'object'):
            safe_path(unit[field])
        expected_context = []
        if index < 2:
            expected_context = [dict(offset=unit['offset']+unit['size'], size=1, kind='original pragma codestring NOP', value='90', function_code_credit=False)]
        need(unit['original_producer_context'] == expected_context, 'original tail context is not function CODE')
        if index == 2:
            need(unit['excluded_linker_alignment'] == [dict(offset=0x16f, size=1, function_code_credit=False)], 'linker alignment is not function CODE')
        need(unit['calling_convention'] == ('far pascal, RETF 2' if index == 3 else 'far cdecl, RETF'), 'original calling convention')
    need(len({u['source'] for u in units}) == len({u['wrapper'] for u in units}) == len({u['object'] for u in units}) == 5, 'duplicate ownership')
    need(config['physical_translation_units'] == 5 and config['code_bytes'] == sum(u['size'] for u in units) == 247, 'bounded counts')
    need(config['original_producer_context_bytes'] == 2, 'original producer context count')
    spans = sorted((u['offset'], u['size']) for u in units)
    need(all(a + size <= b for (a, size), (b, _) in zip(spans, spans[1:])), 'overlapping owners')
    need(set(config['support_files']) == {p for u in units for p in u['support_files']}, 'support closure')
    for name in config['support_files']:
        safe_path(name)
        need(name.startswith('compat/rec98/'), 'explicit compat prefix')

def read_inputs(root):
    root = Path(root)
    raw = regular(root / CONFIG)
    need(sha(raw) == CONFIG_SHA, 'candidate config differs')
    config = json.loads(raw)
    validate_config(config)
    result = {}
    for name, digest in config['support_files'].items():
        data = regular(root / name)
        need(sha(data) == digest, 'compat source differs ' + name)
        need(data == ('#include "' + name.removeprefix('compat/rec98/') + '"\n').encode(), 'explicit original compat forwarding')
        result[name] = data
    for index, unit in enumerate(config['units']):
        data = regular(root / unit['source'])
        need(sha(data) == unit['source_sha256'], 'maintained source differs ' + unit['source'])
        natural = data.replace(b'compat/rec98/', b'')
        need(sha(natural) == unit['original_body_sha256'], 'literal original body provenance')
        includes = re.findall(rb'^#include "([^"]+)"', data, re.M)
        need([p.decode() for p in includes] == unit['support_files'], 'declared compat includes')
        need(data.startswith(PRAGMAS[index]), 'original producer pragma')
        need(b'__emit__' not in data, 'no synthetic byte source')
        if index < 2:
            need(data.endswith(b'#pragma codestring "\\x90"\n'), 'preserve original sound NOP producer context')
        if index == 3:
            need(data.endswith(b'#if (GAME == 5)\n#pragma codestring "\\x90"\n#endif\n'), 'preserve inactive original GAME5 branch')
        result[unit['source']] = data
    return config, result

def payload(root):
    config, result = read_inputs(root)
    for unit in config['units']:
        result[unit['wrapper']] = ('#include "' + unit['original_body'] + '"\n').encode()
        result[unit['original_body']] = ('#include "' + unit['source'] + '"\n').encode()
    return result

def verify_reference(root, config):
    for unit in config['units']:
        for name, digest in ((unit['wrapper'], unit['original_wrapper_sha256']), (unit['original_body'], unit['original_body_sha256'])):
            need(sha(regular(Path(root) / name)) == digest, 'original reference drift ' + name)

def stage(root, output, reference=None):
    config, _ = read_inputs(root)
    if reference is not None:
        verify_reference(reference, config)
    data = payload(root)
    output = Path(output)
    need(not any(p.is_symlink() for p in (output, *output.parents)), 'symlink output')
    need(not output.exists(), 'fresh output required')
    output.mkdir(parents=True)
    for name, raw in data.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    report = dict(schema='th03-op-remaining-helpers-overlay-v1', files={n:dict(sha256=sha(b),bytes=len(b)) for n,b in sorted(data.items())}, code_bytes=247, original_producer_context_bytes=2, physical_translation_units=5, compiler_invocations=0, source_acceptance=False, exact_acceptance=False)
    (output / 'source_inventory.json').write_text(json.dumps(report, indent=2) + '\n')
    return report

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=ROOT)
    p.add_argument('--reference', type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(stage(args.root, args.output, args.reference), indent=2))

if __name__ == '__main__':
    main()
