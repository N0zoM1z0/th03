#!/usr/bin/env python3
"""Validate and stage a source-only ZUN -5 overlay. Never compile or link."""
import argparse
import hashlib
import json
from pathlib import Path

# This proposal manifest is reviewed source identity, not compiler evidence.
MANIFEST_SHA = '0027f92e13048315b5c391bea7151f2ac379cfdbfdb81e52f0c44013858001cb'

def sha(b):
    return hashlib.sha256(b).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def no_symlink(path):
    require(not any(p.is_symlink() for p in (path, *path.parents)), 'symlink input/output ancestor')

def read_inputs(root, manifest):
    no_symlink(manifest)
    raw = manifest.read_bytes()
    require(sha(raw) == MANIFEST_SHA, 'proposal manifest identity differs')
    plan = json.loads(raw)
    payload = {}
    for name, identity in plan['files'].items():
        p = root / name
        no_symlink(p)
        b = p.read_bytes()
        require(sha(b) == identity['sha256'] and len(b) == identity['size'], 'source identity differs: ' + name)
        require(b'\r' not in b and b.endswith(b'\n'), 'LF source required')
        b.decode('cp932')
        payload[name] = b
    for frozen, owner in plan['source_map'].items():
        original = payload[owner]
        for old, new in plan['include_rewrites'].items():
            original = original.replace(('#include "' + new + '"').encode(), ('#include "' + old + '"').encode())
        require(sha(original) == plan['frozen_source_sha256'][frozen], 'non-include source change')
    for old, new in plan['include_rewrites'].items():
        if new.startswith('compat/'):
            require(payload[new] == ('#include "' + old + '"\n').encode(), 'non-forwarding compat edge')
    require(b'#pragma option -2' in payload['src/zun/cfg_init.inl'], 'CPU pragma missing')
    return plan, payload

def stage(root, manifest, output):
    plan, payload = read_inputs(root, manifest)
    payload['th03/res_yume.cpp'] = b'#include "src/zun/res_yume.cpp"\n'
    no_symlink(output)
    require(not output.exists(), 'exclusive fresh output required')
    require(output.parent.is_dir(), 'output parent must exist')
    output.mkdir()
    for name, body in payload.items():
        p = output / name
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as f:
            f.write(body)
    report = dict(kind='th03-zun-resident-source-only-overlay', reference_revision=plan['reference_revision'],
                  proposal_sha256=MANIFEST_SHA, files={n:dict(size=len(b),sha256=sha(b)) for n,b in payload.items()},
                  compiled=False, linked=False, runtime=False, source_acceptance=False, exact_acceptance=False,
                  context_ownership=plan['context'])
    with (output/'source_inventory.json').open('x') as f:
        json.dump(report,f,indent=2); f.write('\n')
    return report

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--manifest',type=Path,default=None)
    parser.add_argument('--output',type=Path,required=True)
    a=parser.parse_args()
    result=stage(a.root,a.manifest or a.root/'config/zun_resident/source.json',a.output)
    print('PASS source-only -5 overlay: %d files; zero native execution / exact credit' % len(result['files']))
