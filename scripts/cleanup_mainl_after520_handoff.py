#!/usr/bin/env python3
"""Pinned after520 MAINL cleanup, dry-run by default; deletes only one audited retired mode.

Protect all 258 active source-bound stages and their full two-round native
OBJ/LIB/EXE/MAP writer outputs. Never prune the current source DAG, targets,
toolchain, tests, analysis probes, other products or incomplete experiments.

An independent retired-mode receipt remains as historical JSON metadata;
after pruning, its superseded *raw outputs* cannot be independently replayed
without rebuilding them. This is explicit, not claimed lossless compression.
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
from cleanup_mainl_after439_handoff import verify_active_hashes

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".analysis/work"
BUILDER = ROOT / "scripts/build_th03_mainl_after520_work.py"
CURRENT = ("after520", "fstreambase-virtual-setbuf-ios-state")
CURRENT_SHA256 = "f32c534f42d520f2c07a3acce769857d01ef310c04c00b419b585bf650994d8e"
HISTORICAL_AFTER439_SHA256 = "dd0a1a82695b00e2a3aeaa4e93a609450b50e834e4dd80b228c2eddaef5e8788"
MANIFEST = WORK / "handoff-after520-retired-20261106.json"
RETIRED = ("after506", "ios-iword-usersize-array-slot-boss")
UNRESOLVED = {("after353", "huge-arithmetic"),
              ("after354", "huge-arithmetic"),
              ("after503", "native-32bit-divmod-twelve-entries-boss")}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def guard() -> None:
    if not BUILDER.is_file():
        raise ValueError("after520 source builder missing")
    current = WORK / f"mainl-{CURRENT[0]}-{CURRENT[1]}-build.json"
    if not current.is_file() or digest(current) != CURRENT_SHA256:
        raise ValueError("after520 root source receipt SHA-256 drift: refuse cleanup")
    original = WORK / "mainl-after439-streambuf-base-default-constructor-boss-build.json"
    if not original.is_file() or digest(original) != HISTORICAL_AFTER439_SHA256:
        raise ValueError("historical source-root attestation changed")
    # Any newer actual builder OR receipt invalidates the pinned deletion audit.
    for glob, pattern, base in (
        ("build_th03_mainl_after*_work.py",
         r"build_th03_mainl_after(\d+)_work\.py", ROOT / "scripts"),
        ("mainl-after*-build.json",
         r"mainl-after(\d+)-.+-build\.json", WORK),
    ):
        for path in base.glob(glob):
            match = re.fullmatch(pattern, path.name)
            if match and int(match.group(1)) > 520:
                raise ValueError(f"newer source stage exists: {path}; re-audit first")


def layers() -> list[tuple[str, str]]:
    """Reconstruct the *live*, actual source-parent DAG, not a timestamp guess."""
    guard()
    driver = BUILDER
    recent: list[tuple[str, str]] = []
    seen: set[Path] = set()
    while driver not in seen:
        seen.add(driver)
        tree = ast.parse(driver.read_text())
        declarations = [node for node in tree.body
                        if isinstance(node, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == "MODES"
                                for t in node.targets)]
        if len(declarations) != 1:
            raise ValueError(f"ambiguous MODES in {driver}")
        modes = ast.literal_eval(declarations[0].value)
        if len(modes) != 1:
            raise ValueError(f"ambiguous modes in {driver}")
        match = re.search(r"after\d+", driver.name)
        if match is None:
            raise ValueError(f"unknown builder name: {driver}")
        stage = match.group()
        recent.append((stage, next(iter(modes))))
        if stage == "after317":
            break
        parents = [alias.name for node in tree.body if isinstance(node, ast.Import)
                   for alias in node.names if alias.asname == "parent"
                   and re.fullmatch(r"build_th03_mainl_after\d+_work", alias.name)]
        if len(parents) != 1:
            raise ValueError(f"ambiguous live parent of {driver}")
        driver = driver.parent / (parents[0] + ".py")
        if not driver.is_file():
            raise ValueError(f"missing live parent builder: {driver}")
    else:
        raise ValueError("circular native source DAG")
    original = [node for node in tree.body
                if isinstance(node, ast.FunctionDef) and node.name == "retained"]
    if len(original) != 1:
        raise ValueError("missing base retained() source DAG")
    assignments = [node for node in ast.walk(original[0])
                   if isinstance(node, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "layers"
                           for t in node.targets)]
    if len(assignments) != 1:
        raise ValueError("ambiguous historical layer sequence")
    previous = list(ast.literal_eval(assignments[0].value))
    graph = previous + list(reversed(recent))
    if (len(previous) != 55 or len(graph) != 258
            or len(set(graph)) != 258
            or graph[0] != ("after62", "sprintf-calloc-puts-ctime")
            or graph[-1] != CURRENT
            or ("after439", "streambuf-base-default-constructor-boss") not in graph
            or ("after506", "dos-creat-exitopen-close-callback-boss") not in graph
            or ("after507", "ios-iword-usersize-array-slot-boss") not in graph):
        raise ValueError("active DAG topology differs from audited after520")
    return graph


def protected_paths(graph: list[tuple[str, str]]) -> set[Path]:
    protected = active_inputs(graph)
    if len(protected) != 5760:
        raise ValueError(f"protected receipt/log/output inventory changed: {len(protected)}")
    return protected


def citations() -> str:
    """Tracked code/docs may cite an alternative's specific native outputs."""
    names = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    texts = []
    for name in names:
        if not name or not name.endswith((
                ".py", ".md", ".txt", ".toml", ".csv", ".sh", ".yml", ".yaml")):
            continue
        path = ROOT / name
        if path.is_file() and path.stat().st_size < 2_000_000:
            texts.append(path.read_text(errors="replace"))
    return "\n".join(texts)


def selected_paths(graph: list[tuple[str, str]], protected: set[Path]) -> list[Path]:
    raw, _ = candidates(graph, protected)
    confirmed = set()
    for receipt in WORK.glob("mainl-after*-build.json"):
        match = re.fullmatch(r"mainl-(after\d+)-(.+)-build\.json", receipt.name)
        if match and match.groups() not in UNRESOLVED:
            record = json.loads(receipt.read_text())
            if record.get("complete") and record.get("mode") == match.group(2):
                confirmed.add(match.groups())
    listed = []
    for p in raw:
        if not p.name.startswith(RETIRED[0] + "-" + RETIRED[1] + "-"):
            # Keep every other historical/incomplete/diagnostic mode.
            continue
        if RETIRED not in confirmed:
            raise ValueError("retired mode not independently complete")
        listed.append(p)
    corpus = citations()
    listed = [p for p in listed
              if p.relative_to(ROOT).as_posix() not in corpus and p.name not in corpus]
    if listed and len(listed) != 15:
        raise ValueError(f"unexpected retired mode output count: {len(listed)}")
    for path in listed:
        if (path in protected or not path.is_file() or path.is_symlink()
                or path.stat().st_nlink != 1
                or not path.resolve().is_relative_to(WORK.resolve())):
            raise ValueError(f"unsafe cleanup candidate: {path}")
    return sorted(listed)


def manifest_entries(paths: list[Path]) -> list[dict]:
    return [dict(path=p.relative_to(ROOT).as_posix(),
                 sha256=digest(p),
                 bytes=p.stat().st_size,
                 allocated_bytes=p.stat().st_blocks * 512)
            for p in paths]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="show exact audited candidates")
    parser.add_argument("--apply", action="store_true",
                        help="perform guarded deletion of only audited retired artifacts")
    args = parser.parse_args()
    graph = layers()
    protected = protected_paths(graph)
    paths = selected_paths(graph, protected)
    total = sum(p.stat().st_blocks * 512 for p in paths)
    print(f"ACTIVE: {len(graph)} stages; {len(protected)} protected receipt/log/native paths")
    print(f"CURRENT: {CURRENT[0]}/{CURRENT[1]}, receipt SHA {CURRENT_SHA256}")
    print(f"RETIRED: {RETIRED[0]}/{RETIRED[1]}: {len(paths)} files, {total / 2**20:.2f} MiB allocated")
    if args.list:
        for path in paths:
            print("  " + path.relative_to(ROOT).as_posix())
    if not args.apply:
        print("DRY RUN; no files deleted")
        return
    if not paths:
        print("NOOP: no remaining eligible artifacts, manifest preserved")
        return
    if MANIFEST.exists():
        raise ValueError("original after520 deletion manifest already exists; refusing overwrite")
    # Complete active DAG SHA verification before deletion, including source
    # and driver scripts plus all seven logs and both raw output vectors.
    guard()
    verify_active_hashes(graph)
    entries = manifest_entries(paths)
    if sum(entry["allocated_bytes"] for entry in entries) != total:
        raise ValueError("allocation/manifest drift")
    for path, entry in zip(paths, entries):
        if path in protected or not path.is_file() or digest(path) != entry["sha256"]:
            raise ValueError(f"unsafe or changed selected artifact: {path}")
    # Write the complete pre-deletion byte hashes to an immutable private
    # manifest, then mark it applied only after the exact files are unlinked.
    planned = MANIFEST.with_suffix(".planned.json")
    if planned.exists():
        raise ValueError("previous interrupted deletion plan exists")
    report = dict(schema="th03-after520-native-retired-mode-audit-v1",
                  root_receipt=f".analysis/work/mainl-{CURRENT[0]}-{CURRENT[1]}-build.json",
                  root_sha256=CURRENT_SHA256,
                  graph_stages=len(graph),protected_files=len(protected),
                  retired_mode=list(RETIRED),
                  deleted_files=len(entries),allocated_bytes=total,
                  entries=entries,status="planned")
    planned.write_text(json.dumps(report,indent=2) + "\n")
    for path in paths:
        path.unlink()
    # Verify protected proof integrity remains intact, not just that files exist.
    verify_active_hashes(graph)
    report["status"] = "applied"
    planned.write_text(json.dumps(report,indent=2) + "\n")
    planned.replace(MANIFEST)
    print(f"DELETED: {len(paths)} verified superseded native output/log files; "
          f"{total / 2**20:.2f} MiB allocated")
    print(f"AUDIT: {MANIFEST.relative_to(ROOT)} (SHA-256 inventory of each retired file)")


if __name__ == "__main__":
    main()
