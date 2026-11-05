#!/usr/bin/env python3
"""Scope-guarded cleanup of superseded MAINL trial outputs (dry-run default).

This is frozen to the validated 319-source / 2026-11-05 receipt checkpoint.
It intentionally DOES NOT replace the general cleanup script or infer proof
from filename age. Never delete the active 55-layer DAG or the two current
raw native output rounds. Re-check the next source checkpoint before reuse.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.analysis/work'
BUILDER = ROOT / 'scripts/build_th03_mainl_after317_work.py'
CURRENT = ('after317', 'nec-delay-mbyte')
EXPECTED_RECEIPT_SHA256 = 'cef375198c75b6495405305208c0f7d752670be029f14b7167a732cd00512a2c'


def checked_path(raw: str) -> Path:
    """Fail closed for symlinks, traversal, missing proof and non-work paths."""
    candidate = Path(raw)
    if candidate.is_absolute() or '..' in candidate.parts:
        raise ValueError(f'unsafe generated proof path: {raw}')
    path = ROOT / candidate
    if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(WORK.resolve()):
        raise ValueError(f'missing or unsafe proof file: {raw}')
    return path


def current_layers() -> list[tuple[str, str]]:
    if not BUILDER.is_file():
        raise ValueError('current builder is missing')
    # New source layers invalidate this checkpoint-specific cleanup policy.
    newer = [p for p in (ROOT/'scripts').glob('build_th03_mainl_after*_work.py')
             if (m := re.fullmatch(r'build_th03_mainl_after(\d+)_work.py', p.name))
             and int(m.group(1)) > 317]
    newer += [p for p in WORK.glob('mainl-after*-build.json')
              if (m := re.match(r'mainl-after(\d+)-', p.name))
              and int(m.group(1)) > 317]
    if newer:
        raise ValueError(f'newer source checkpoint exists; update guard first: {newer[:3]}')
    latest = WORK / f'mainl-{CURRENT[0]}-{CURRENT[1]}-build.json'
    if hashlib.sha256(latest.read_bytes()).hexdigest() != EXPECTED_RECEIPT_SHA256:
        raise ValueError('current native receipt hash changed; refusing cleanup')
    tree = ast.parse(BUILDER.read_text())
    methods = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'retained']
    if len(methods) != 1:
        raise ValueError('cannot identify one source-bound retained() DAG')
    nodes = [n for n in ast.walk(methods[0]) if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == 'layers' for t in n.targets)]
    if len(nodes) != 1:
        raise ValueError('cannot locate one static source-bound layer sequence')
    layers = list(ast.literal_eval(nodes[0].value))
    if len(layers) != 55 or layers[0] != ('after62', 'sprintf-calloc-puts-ctime') or layers[-1] != ('after307', 'jis-copy-case'):
        raise ValueError('the known 55-layer DAG changed')
    return layers + [CURRENT]


def active_inputs(layers: list[tuple[str, str]]) -> set[Path]:
    needed: set[Path] = set()
    for stage, mode in layers:
        receipt = checked_path(f'.analysis/work/mainl-{stage}-{mode}-build.json')
        record = json.loads(receipt.read_text())
        if not record.get('complete') or record.get('mode') != mode or len(record.get('rounds', [])) != 2:
            raise ValueError(f'incomplete current source receipt: {stage}/{mode}')
        needed.add(receipt)
        for phase in record['phases']:
            needed.add(checked_path(phase['log_path']))
        for rd in record['rounds']:
            for item in rd['outputs'].values():
                p = checked_path(item['path'])
                if p.stat().st_size != item['bytes']:
                    raise ValueError(f'changed original proof length: {p}')
                needed.add(p)
    return needed


def candidates(layers: list[tuple[str, str]], protected: set[Path]) -> tuple[list[Path], dict[str, int]]:
    live_modes = set(layers)
    live_stages = {stage for stage, mode in layers}
    selected: set[Path] = set()
    groups: defaultdict[str, int] = defaultdict(int)
    # Prune only the raw outputs/logs of completed, superseded alternate
    # modes at a stage still represented by a protected active receipt.
    # Keep their small JSON reports as archived historical metadata.
    for receipt in sorted(WORK.glob('mainl-after*-build.json')):
        match = re.fullmatch(r'mainl-(after\d+)-(.+)-build\.json', receipt.name)
        if not match:
            continue
        stage, mode = match.groups()
        if stage not in live_stages or (stage, mode) in live_modes:
            continue
        record = json.loads(receipt.read_text())
        if record.get('mode') != mode:
            raise ValueError(f'bad alternative-mode receipt: {receipt}')
        refs = [phase['log_path'] for phase in record.get('phases', [])]
        refs += [item['path'] for rd in record.get('rounds', [])
                 for item in rd.get('outputs', {}).values()]
        for ref in refs:
            path = ROOT / ref
            # Historical incomplete trials may have no corresponding output.
            if not path.exists():
                continue
            path = checked_path(ref)
            if path in protected:
                continue
            if not path.name.startswith(stage + '-'):
                raise ValueError(f'unexpected alternate mode output name: {path}')
            selected.add(path)
            groups[f'{stage}/{mode}'] += 1
    return sorted(selected), dict(groups)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='delete only audited obsolete alternate-mode raw vectors')
    args = parser.parse_args()
    layers = current_layers()
    protected = active_inputs(layers)
    old, groups = candidates(layers, protected)
    allocated = sum(p.stat().st_blocks * 512 for p in old)
    print(f'current proof: {len(layers)} native layers, {len(protected)} retained files; NONE targeted')
    print(f'superseded modes: {len(groups)}, {len(old)} raw files, {allocated / 2**20:.2f} MiB allocated')
    for group, n in sorted(groups.items()):
        print(f'  {group}: {n} raw files')
    if not args.apply:
        print('DRY RUN ONLY; inspect and rerun with --apply for these superseded vectors')
        return
    for path in old:
        if path in protected or not path.is_file() or path.is_symlink():
            raise ValueError(f'refusing unsafe deletion: {path}')
        path.unlink()
    # A compact inventory gives the next agent the exact retired paths.
    manifest = WORK / 'handoff-2026-11-05-retired-variants.txt'
    manifest.write_text('\n'.join(p.relative_to(ROOT).as_posix() for p in old)+'\n')
    print(f'DELETED {len(old)} superseded raw files; manifest: {manifest.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
