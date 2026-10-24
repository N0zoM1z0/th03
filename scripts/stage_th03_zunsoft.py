#!/usr/bin/env python3
"""Compose only the maintained logo root overlay; never compile or link.

Merge into fresh pinned ReC98 source context, preserving the original
th01/zunsoft.cpp translation-unit slot and tiny-model link order. Header
forwarders are explicit context, not ownership of master.lib or the whole -3.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REVISION = 'b6ba5b0a529edbb31efdf8c0e939263804f8ee47'
OWNER = 'src/zun/zunsoft.cpp'
SLOT = 'th01/zunsoft.cpp'
FROZEN_SHA = 'a2fd32b9213f89dbf582c36d48390f216666ca533f60cf2b3daa42d3d9984d98'
SOURCE_SHA = 'f1c7efb2a913686278732eb51753471684ce6441fd36bc40f764399f36c47948'
DEPENDENCIES = (
    'libs/master.lib/pc98_gfx.hpp',
    'platform/x86real/pc98/egc.hpp',
    'platform/x86real/pc98/page.hpp',
    'th01/hardware/grcg.hpp',
    'th01/math/polar.hpp',
)
COMPAT = tuple('compat/rec98/' + p for p in DEPENDENCIES)
INPUTS = (OWNER,) + COMPAT
PROCEDURES = (
    ('graph_clear_both', 0x367, 29), ('zunsoft_init', 0x384, 76),
    ('zunsoft_exit', 0x3d0, 20), ('zunsoft_vector2', 0x3e4, 85),
    ('objects_setup', 0x439, 201), ('circles_render_and_update', 0x502, 180),
    ('stars_render_and_update', 0x5b6, 205), ('wait', 0x683, 21),
    ('logo_render_and_update', 0x698, 309), ('main', 0x7cd, 173),
)

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)

def no_symlink(path: Path) -> None:
    require(not any(p.is_symlink() for p in (path, *path.parents)),
            'symlink input/output ancestor: ' + str(path))

def read_inputs(root: Path) -> dict[str, bytes]:
    result = {}
    for name in INPUTS:
        p = root / name
        no_symlink(p)
        raw = p.read_bytes()
        require(raw and b'\r' not in raw and raw.endswith(b'\n'), 'LF text required: ' + name)
        raw.decode('ascii')
        result[name] = raw
    body = result[OWNER]
    require(sha(body) == SOURCE_SHA, 'reviewed maintained root identity differs')
    includes = tuple(x.decode() for x in re.findall(rb'^#include "([^"\n]+)"', body, re.M))
    require(includes == COMPAT, 'ordered root dependency vector differs')
    original = body
    for context, compat in zip(DEPENDENCIES, COMPAT):
        require(result[compat] == ('#include "' + context + '"\n').encode(),
                'compat edge differs: ' + compat)
        original = original.replace(('#include "' + compat + '"').encode(),
                                    ('#include "' + context + '"').encode())
    # Native TC4 word alignment supplies the one-byte gap after wave_amp.
    # The frozen candidate used an unused char instead. Reconstruct that exact
    # candidate only for the statement-lineage check, never for compilation.
    require(b'char wave_padding;' not in original, 'explicit padding variable is not a producer input')
    original = original.replace(b'#pragma option -2 -d- -a2 // ZUN bloat; native word alignment',
                                b'#pragma option -2 -d- // ZUN bloat')
    original = original.replace(b'char wave_amp;\n', b'char wave_amp;\nchar wave_padding;\n')
    require(sha(original) == FROZEN_SHA, 'source statements differ beyond declared include/alignment recovery')
    require(b'#pragma option -2 -d-' in body, 'CPU/duplicate-string pragma missing')
    signatures = re.findall(rb'^void (?:pascal )?(\w+)\(', body, re.M)
    require([p.decode() for p in signatures] == [p[0] for p in PROCEDURES], 'procedure shape/order differs')
    return result

def stage(root: Path, output: Path) -> dict:
    payload = read_inputs(root)
    payload[SLOT] = ('#include "' + OWNER + '"\n').encode()
    no_symlink(output)
    require(not output.exists(), 'exclusive fresh output required')
    require(output.parent.is_dir(), 'output parent must exist')
    output.mkdir()
    for name, body in payload.items():
        p = output / name
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as f:
            f.write(body)
    receipt = dict(
        kind='th03-zunsoft-source-only-overlay', reference_revision=REVISION,
        owner=OWNER, translation_unit=SLOT,
        files={p: dict(size=len(b), sha256=sha(b)) for p, b in sorted(payload.items())},
        source_shape=dict(procedures=[dict(name=n, historical_inner_start=s,
                          historical_size=z) for n, s, z in PROCEDURES],
                          historical_code_size=1299, historical_data_size=15,
                          historical_bss_size=293),
        source_association='Five explicit forwarding includes; native word alignment replaces an unused padding char',
        memory_model='tiny', compilation_game_define=1,
        pragma='-2 -d- -a2', plain_char='signed (default; do not add -K)',
        ABI='near cdecl roots; near Pascal vector with 8-byte cleanup',
        context_ownership='Forwarded headers, master.lib, startup and CRT remain context',
        compiler_invocations=0, compiled=False, linked=False, runtime=False,
        source_acceptance=False, exact_acceptance=False, whole_payload_ownership=False,
    )
    with (output / 'source_inventory.json').open('x') as f:
        json.dump(receipt, f, indent=2, sort_keys=True)
        f.write('\n')
    return receipt

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=ROOT)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    receipt = stage(a.root, a.output)
    print('PASS source-only ZUN -3 root overlay: %d files; no native execution or exact credit' % len(receipt['files']))

if __name__ == '__main__':
    main()
