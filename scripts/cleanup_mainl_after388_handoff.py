#!/usr/bin/env python3
"""Guarded, source-DAG-aware cleanup for TH03's verified after388 checkout.

Dry-run by default. Only obsolete *alternative* native mode artifacts and
unreferenced regenerable disassembly scratch are eligible for deletion.
Never prune active receipt/log/native OBJ/LIB/EXE/MAP pairs, fixed targets,
Wine/toolchains, the older cold/provenance pairs, or experimental source.

This script intentionally FAILS CLOSED for a new MAINL source checkpoint.
Re-audit the live builder/receipt DAG before adapting it for the next agent.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

from cleanup_mainl_handoff_artifacts import active_inputs, candidates

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.analysis/work'
BUILDER = ROOT / 'scripts/build_th03_mainl_after388_work.py'
CURRENT = ('after388', 'string-default-constructor-boss')
RECEIPT_SHA256 = 'd0baf1d6ab2d1019c97d59021b2038f40bbfe434fd0ae77b6136fdf3068d23b9'
MANIFEST = WORK / 'handoff-after388-retired-20261105.txt'
# Diagnostic of a still-open h_ldiv alias/MAP discrepancy; not disposable.
UNRESOLVED = {('after353', 'huge-arithmetic'), ('after354', 'huge-arithmetic')}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def guard() -> None:
    if not BUILDER.is_file():
        raise ValueError('pinned current MAINL builder unavailable')
    receipt = WORK / f'mainl-{CURRENT[0]}-{CURRENT[1]}-build.json'
    if not receipt.is_file() or digest(receipt) != RECEIPT_SHA256:
        raise ValueError('after388 receipt changed; re-audit before pruning')
    for glob, pattern in (
        ('build_th03_mainl_after*_work.py', r'build_th03_mainl_after(\d+)_work\.py'),
        ('mainl-after*-build.json', r'mainl-after(\d+)-.+-build\.json'),
    ):
        root = ROOT / 'scripts' if glob.startswith('build_') else WORK
        for path in root.glob(glob):
            match = re.fullmatch(pattern, path.name)
            if match and int(match.group(1)) > 388:
                raise ValueError(f'newer source layer exists: {path}; re-audit')


def layers() -> list[tuple[str, str]]:
    """Walk the actual literal parent imports; append the 55 fixed base DAG."""
    guard()
    current = BUILDER
    recent: list[tuple[str, str]] = []
    seen: set[Path] = set()
    while current not in seen:
        seen.add(current)
        tree = ast.parse(current.read_text())
        settings = [node for node in tree.body if isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'MODES'
                            for t in node.targets)]
        if len(settings) != 1:
            raise ValueError(f'cannot inspect sole mode declaration: {current}')
        modes = ast.literal_eval(settings[0].value)
        if len(modes) != 1:
            raise ValueError(f'ambiguous source parent mode: {current}')
        stage = re.search(r'after\d+', current.name)
        if not stage:
            raise ValueError(f'bad source stage: {current}')
        recent.append((stage.group(), next(iter(modes))))
        if stage.group() == 'after317':
            break
        imports = [node for node in tree.body if isinstance(node, ast.Import)
                   for alias in node.names if alias.asname == 'parent'
                   and re.fullmatch(r'build_th03_mainl_after\d+_work', alias.name)]
        if len(imports) != 1:
            raise ValueError(f'cannot trace one original source parent: {current}')
        parent = current.parent / f'{imports[0].names[0].name}.py'
        if not parent.is_file():
            raise ValueError(f'missing original source-bound parent: {parent}')
        current = parent
    else:
        raise ValueError('cycle in source-bound CRT DAG')
    # The historical after317 driver owns the first 55 active source layers.
    methods = [node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == 'retained']
    if len(methods) != 1:
        raise ValueError('cannot inspect first source DAG')
    decls = [node for node in ast.walk(methods[0]) if isinstance(node, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == 'layers'
                     for t in node.targets)]
    if len(decls) != 1:
        raise ValueError('cannot inspect static source DAG')
    prior = list(ast.literal_eval(decls[0].value))
    result = prior + list(reversed(recent))
    if (len(prior) != 55 or len(result) != 126
            or result[0] != ('after62', 'sprintf-calloc-puts-ctime')
            or result[-1] != CURRENT or len(set(result)) != len(result)):
        raise ValueError('live source-bound parent topology changed')
    return result


def verify_active_hashes(graph: list[tuple[str, str]]) -> None:
    """Verify every live source/driver/log/raw output identity before applying."""
    for stage, mode in graph:
        receipt = WORK / f'mainl-{stage}-{mode}-build.json'
        value = json.loads(receipt.read_text())
        driver = ROOT / f'scripts/build_th03_mainl_{stage}_work.py'
        if not driver.is_file() or digest(driver) != value['driver_sha256']:
            raise ValueError(f'current builder hash drift: {stage}')
        for name, raw in value['source_paths'].items():
            source = ROOT / raw
            if not source.is_file() or digest(source) != value['source_sha256'][name]:
                raise ValueError(f'original CRT source hash drift: {stage}/{name}')
        for phase in value['phases']:
            path = ROOT / phase['log_path']
            if not path.is_file() or digest(path) != phase['log_sha256']:
                raise ValueError(f'native phase log hash drift: {stage}')
        for rd in value['rounds']:
            for meta in rd['outputs'].values():
                path = ROOT / meta['path']
                if (not path.is_file() or path.stat().st_size != meta['bytes']
                        or digest(path) != meta['sha256']):
                    raise ValueError(f'raw source-linked output hash drift: {stage}')


def scratch_candidates(protected: set[Path]) -> list[Path]:
    """Only regenerated text disassembly, if never cited in tracked source."""
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    tracked_text = []
    for name in names:
        if not name or not name.endswith(('.py', '.md', '.txt', '.toml', '.csv', '.sh', '.yml', '.yaml')):
            continue
        path = ROOT / name
        try:
            if path.is_file() and path.stat().st_size < 2_000_000:
                tracked_text.append(path.read_text(errors='replace'))
        except OSError:
            pass
    content = '\n'.join(tracked_text)
    proposed = set(WORK.glob('*.ndis')) | set(WORK.glob('*.dis'))
    return sorted(p for p in proposed if p.is_file() and not p.is_symlink()
                  and p not in protected and p.name not in content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='execute verified deletion')
    parser.add_argument('--list', action='store_true', help='display each audited candidate path')
    args = parser.parse_args()
    graph = layers()
    protected = active_inputs(graph)
    alternate, modes = candidates(graph, protected)
    # No deletion of incomplete/failed modes or open unresolved diagnostics.
    confirmed = set()
    for path in WORK.glob('mainl-after*-build.json'):
        match = re.fullmatch(r'mainl-(after\d+)-(.+)-build\.json', path.name)
        if match and tuple(match.groups()) not in UNRESOLVED:
            record = json.loads(path.read_text())
            if record.get('complete') and record.get('mode') == match.group(2):
                confirmed.add(tuple(match.groups()))
    eligible = [p for p in alternate if
                (m := re.match(r'^(after\d+)-(.+)-(?:round\d+-|extract|round\d+-)', p.name))
                and any(p.name.startswith(st + '-' + mode + '-') for st, mode in confirmed)
                and p not in protected]
    # Candidate paths are enumerated from a completed, archived build JSON,
    # and validated again just before deletion below.
    all_selected = sorted(set(eligible) | set(scratch_candidates(protected)))
    total = sum(p.stat().st_blocks * 512 for p in all_selected)
    print(f'ACTIVE: {len(graph)} source-bound stages; {len(protected)} receipts/logs/native files protected')
    print(f'ALTERNATE: {len(eligible)} retired-mode files, {len(modes)} old modes scanned')
    print(f'SCRATCH: {len(all_selected)-len(eligible)} uncited regenerable disassemblies')
    print(f'ELIGIBLE: {len(all_selected)} files, {total / 2**20:.2f} MiB allocated')
    for p in all_selected:
        if (p in protected or not p.is_file() or p.is_symlink()
                or not p.resolve().is_relative_to(WORK.resolve())
                or p.stat().st_nlink != 1):
            raise ValueError(f'unsafe prune candidate: {p}')
    if args.list:
        for p in all_selected:
            print('  ' + p.relative_to(ROOT).as_posix())
    if not args.apply:
        print('DRY RUN ONLY; use --list to inspect paths, then --apply after source review')
        return
    if not all_selected:
        print('NOOP: all eligible output already retired; existing manifest preserved')
        return
    if MANIFEST.exists():
        raise ValueError('previous handoff deletion manifest exists; refusing to overwrite audit history')
    guard()  # fail closed if a new layer appeared during the dry-run/review
    verify_active_hashes(graph)
    records = [(p, digest(p)) for p in all_selected]
    for p, expected in records:
        if digest(p) != expected:
            raise ValueError(f'candidate changed during audit: {p}')
    for p, _ in records:
        p.unlink()
    MANIFEST.write_text('\n'.join(p.relative_to(ROOT).as_posix() for p, _ in records)+'\n')
    print(f'DELETED: {len(records)} eligible files; manifest {MANIFEST.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
