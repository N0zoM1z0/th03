#!/usr/bin/env python3
"""Prune disposable reconstruction output while preserving required local state."""

from __future__ import annotations

import argparse
import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / ".analysis"
EVIDENCE = ROOT / "config" / "evidence.csv"

PRESERVED_ANALYSIS_ROOTS = {
    ANALYSIS / "toolchain",
    ANALYSIS / "targets",
    ANALYSIS / "runtime",
    ANALYSIS / "ghidra",
}
PRESERVED_ANALYSIS_FILES = {
    ANALYSIS / "target-import.json",
}
CACHE_ROOTS = [
    ROOT / "build",
    ROOT / "dist",
    ROOT / "out",
    ROOT / ".pytest_cache",
    ROOT / ".mypy_cache",
]


def normalized_local_path(raw: str) -> Path | None:
    if not raw:
        return None
    candidate = Path(raw)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    resolved = (ROOT / candidate).resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        return None
    return resolved


def ledger_preserved_paths() -> set[Path]:
    preserved: set[Path] = set()
    if not EVIDENCE.is_file():
        return preserved
    with EVIDENCE.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            path = normalized_local_path(row.get("location", ""))
            if path is None:
                continue
            try:
                path.relative_to(ANALYSIS)
            except ValueError:
                continue
            preserved.add(path)
    return preserved


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def tree_size(path: Path) -> int:
    if path.is_symlink() or path.is_file():
        return path.lstat().st_size
    return sum(
        entry.lstat().st_size
        for entry in path.rglob("*")
        if entry.is_file() or entry.is_symlink()
    )


def remove_path(path: Path, dry_run: bool) -> int:
    if not path.exists() and not path.is_symlink():
        return 0
    size = tree_size(path)
    kind = "tree" if path.is_dir() and not path.is_symlink() else "file"
    print(f"{'would remove' if dry_run else 'remove'} {kind} {path.relative_to(ROOT)}")
    if not dry_run:
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink()
    return size


def clean_analysis(dry_run: bool) -> int:
    if not ANALYSIS.exists():
        return 0

    protected_files = ledger_preserved_paths() | PRESERVED_ANALYSIS_FILES

    def protected_below(path: Path) -> bool:
        return any(is_under(protected, path) for protected in protected_files) or any(
            is_under(root, path) for root in PRESERVED_ANALYSIS_ROOTS
        )

    def prune(path: Path) -> int:
        if any(is_under(path, root) for root in PRESERVED_ANALYSIS_ROOTS):
            return 0
        if path in protected_files:
            return 0
        if not protected_below(path):
            return remove_path(path, dry_run)
        if not path.is_dir() or path.is_symlink():
            return 0

        removed = 0
        for child in sorted(path.iterdir(), key=lambda item: item.name):
            removed += prune(child)
        if not dry_run:
            try:
                path.rmdir()
                print(f"remove empty dir {path.relative_to(ROOT)}")
            except OSError:
                pass
        return removed

    removed = 0
    for child in sorted(ANALYSIS.iterdir(), key=lambda item: item.name):
        removed += prune(child)
    return removed


def clean_caches(dry_run: bool) -> int:
    removed = 0
    for path in CACHE_ROOTS:
        removed += remove_path(path, dry_run)

    for base in (ROOT / "scripts", ROOT / "tests"):
        if not base.exists():
            continue
        for path in sorted(base.rglob("__pycache__")):
            removed += remove_path(path, dry_run)
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prune disposable local build/replay/cache output while preserving "
            "required private state and ledger-referenced evidence."
        )
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="perform deletions; without this flag only report what would be removed",
    )
    args = parser.parse_args()

    dry_run = not args.apply
    removed = clean_analysis(dry_run) + clean_caches(dry_run)
    verb = "would remove" if dry_run else "removed"
    print(f"{verb} approximately {removed / (1024 * 1024):.1f} MiB")
    print(
        "preserved .analysis/toolchain, .analysis/targets, .analysis/runtime, "
        ".analysis/ghidra, target-import.json, and ledger-referenced evidence"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
