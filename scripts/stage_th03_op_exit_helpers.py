#!/usr/bin/env python3
"""Stage three original OP exit/display helper TUs. Source-only; no native tools."""
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CONFIG = 'config/th03_op_exit_helpers_candidate.json'
CONFIG_SHA = 'eb036e2d84c870010d3c139f360cdd9e6f295b1443cf563a3273cbd01cd42dc7'
EXPECTED = (
    ('game_exit_to_dos', 'th02/exit_dos.cpp', 2, 8, 25),
    ('vram_planes_set', 'th01/vplanset.cpp', 1, 33, 41),
    ('game_exit', 'th03/exit.cpp', 3, 274, 67),
)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def need(ok, message):
    if not ok:
        raise ValueError(message)

def regular(path):
    path = Path(path)
    need(not any(p.is_symlink() for p in (path, *path.parents)), 'symlink input')
    need(path.is_file(), 'missing input ' + str(path))
    return path.read_bytes()

def validate_config(config):
    need(config['schema'] == 'th03-op-exit-helpers-source-v1', 'schema')
    need(config['source_acceptance'] is False and config['exact_acceptance'] is False, 'credit inflation')
    units = config['units']
    need(len(units) == 3, 'three physical translation units')
    for unit, expected in zip(units, EXPECTED):
        need(tuple(unit[k] for k in ('name', 'wrapper', 'physical_game_macro', 'offset', 'size')) == expected, 'original producer or extent changed')
        need(unit['compare_size'] == unit['size'] and unit['segment'] == 'decoded:0beb', 'extent identity')
        need(unit['language'] == 'cpp' and unit['compiler'] == 'tcc', 'producer language')
        wrapper = Path(unit['wrapper'])
        command = "bin\\msdos -e -x tcc -c -I. -O -b- -3 -Z -d -DGAME=%d -ml -DBINARY='O' -n%s/ %s" % (unit['physical_game_macro'], wrapper.parent.as_posix().replace('th', 'obj/th', 1), wrapper.as_posix())
        need(unit['original_command'] == command, 'literal original producer command')
        need(unit['object'] == 'obj/' + str(wrapper.with_suffix('.obj')), 'physical object identity')
        for field in ('source', 'original_body', 'wrapper', 'object'):
            p = Path(unit[field])
            need(not p.is_absolute() and '..' not in p.parts, 'unsafe source path')
    need(len({u['source'] for u in units}) == len({u['wrapper'] for u in units}) == len({u['object'] for u in units}) == 3, 'duplicate ownership')
    need(config['physical_translation_units'] == 3 and config['code_bytes'] == sum(u['size'] for u in units) == 133, 'bounded counts')
    spans = sorted((u['offset'], u['size']) for u in units)
    need(all(a + size <= b for (a, size), (b, _) in zip(spans, spans[1:])), 'overlapping owners')
    need(set(config['support_files']) == {p for u in units for p in u['support_files']}, 'support closure')

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
    for unit in config['units']:
        data = regular(root / unit['source'])
        need(sha(data) == unit['source_sha256'], 'maintained source differs ' + unit['source'])
        natural = data.replace(b'compat/rec98/', b'')
        need(sha(natural) == unit['original_body_sha256'], 'literal original body provenance')
        includes = re.findall(rb'^#include "([^"]+)"', data, re.M)
        need([p.decode() for p in includes] == unit['support_files'], 'declared compat includes')
        need(data.startswith(b'#pragma option -zCSHARED\n'), 'original shared segment')
        need(b'#pragma codestring' not in data and b'__emit__' not in data, 'no synthetic byte source')
        result[unit['source']] = data
    return config, result

def payload(root):
    config, result = read_inputs(root)
    for unit in config['units']:
        wrapper, body = unit['wrapper'], unit['original_body']
        if wrapper != body:
            result[wrapper] = ('#include "' + body + '"\n').encode()
        result[body] = ('#include "' + unit['source'] + '"\n').encode()
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
    report = dict(schema='th03-op-exit-helpers-overlay-v1', files={n:dict(sha256=sha(b),bytes=len(b)) for n,b in sorted(data.items())}, code_bytes=133, physical_translation_units=3, compiler_invocations=0, source_acceptance=False, exact_acceptance=False)
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
