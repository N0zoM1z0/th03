#!/usr/bin/env python3
"""Prune disposable reconstruction output while preserving required local state."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shlex
import shutil
import subprocess
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
    ROOT / ".cache",
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
            raw = row.get("location", "")
            lexical = Path(raw)
            if raw and not lexical.is_absolute() and ".." not in lexical.parts:
                lexical = ROOT / lexical
                if is_under(lexical, ANALYSIS):
                    preserved.add(lexical)
            path = normalized_local_path(raw)
            if path is None:
                continue
            try:
                path.relative_to(ANALYSIS)
            except ValueError:
                continue
            preserved.add(path)
    return preserved


def documented_analysis_paths() -> set[Path]:
    """Return concrete .analysis files named by tracked text.

    Generic directory mentions do not pin every descendant forever. Only paths
    that resolve to files (plus an explicitly named receipt.json) participate
    in the aggressive receipt-pruning keep set.
    """
    preserved: set[Path] = set()
    try:
        tracked = subprocess.check_output(
            ["git", "ls-files", "-z"],
            cwd=ROOT,
            stderr=subprocess.DEVNULL,
        ).decode().split("\0")
    except (OSError, subprocess.CalledProcessError, UnicodeDecodeError):
        return preserved

    for name in tracked:
        if not name:
            continue
        path = ROOT / name
        if not path.is_file() or path.is_symlink():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            continue
        for raw in re.findall(r"\.analysis/[A-Za-z0-9_./-]+", text):
            raw = raw.rstrip(".,;:)")
            candidate = normalized_local_path(raw)
            if candidate is None:
                continue
            try:
                candidate.relative_to(ANALYSIS)
            except ValueError:
                continue
            if candidate.is_file() or candidate.name == "receipt.json":
                preserved.add(candidate)
    return preserved


def referenced_analysis_closure(extra: set[Path] | None = None) -> set[Path]:
    """Follow retained JSON input guards from current ledger/document references."""
    ledger_files = ledger_preserved_paths()
    text_queries = ledger_text_query_paths()
    retained = ledger_files | documented_analysis_paths() | text_queries
    retained |= PRESERVED_ANALYSIS_FILES
    if extra:
        retained |= extra

    visited: set[Path] = set()
    queue = list(retained)
    while queue:
        path = queue.pop()
        if path in visited:
            continue
        visited.add(path)
        retained.add(path)
        if not path.is_file() or path.suffix.lower() != ".json":
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError, OSError):
            # Factory function queries are intentionally plain text even when a
            # historical caller chose a .json output name.
            if path.name != "receipt.json" and path in text_queries:
                continue
            # A retained receipt or other ledger JSON must remain inspectable.
            if path.name == "receipt.json" or path in ledger_files:
                raise ValueError(
                    f"cannot inspect retained proof: {path.relative_to(ROOT)}"
                )
            continue

        stack = [value]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                guards = node.get("inputs")
                if isinstance(guards, dict):
                    for raw in guards:
                        if not isinstance(raw, str) or not raw:
                            continue
                        lexical = Path(raw)
                        if lexical.is_absolute() or ".." in lexical.parts:
                            continue
                        lexical = ROOT / lexical
                        try:
                            lexical.relative_to(ANALYSIS)
                        except ValueError:
                            pass
                        else:
                            if lexical not in retained:
                                retained.add(lexical)
                                queue.append(lexical)
                        resolved = normalized_local_path(raw)
                        if resolved is not None and is_under(resolved, ANALYSIS):
                            if resolved not in retained:
                                retained.add(resolved)
                                queue.append(resolved)
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    return retained


def prune_unreferenced_receipts(
    dry_run: bool,
    extra_preserved: set[Path] | None = None,
) -> int:
    """Optionally remove cold receipt runs unreachable from current proof refs."""
    if not ANALYSIS.exists():
        return 0

    retained = referenced_analysis_closure(extra_preserved)
    receipt_roots: set[Path] = set()
    for receipt in ANALYSIS.rglob("receipt.json"):
        if receipt.is_symlink():
            continue
        root = receipt.parent
        if any(is_under(root, protected) for protected in PRESERVED_ANALYSIS_ROOTS):
            continue
        receipt_roots.add(root)

    candidates = [
        root
        for root in receipt_roots
        if not any(is_under(path, root) for path in retained)
    ]

    # A parent receipt run subsumes nested receipt runs.
    top_level: list[Path] = []
    for root in sorted(candidates, key=lambda x: len(x.parts)):
        if any(is_under(root, parent) for parent in top_level):
            continue
        top_level.append(root)

    return sum(remove_path(root, dry_run) for root in top_level)


def proof_preserved_paths() -> tuple[set[Path], set[Path]]:
    """Keep retained JSON input guards and complete cold receipt directories.

    Receipts also describe outputs and frozen archives outside their input
    dictionaries. Preserve the entire receipt directory, rather than guessing
    which producer files will be needed for the next ownership question.
    """
    files: set[Path] = set()
    roots: set[Path] = set()
    if not ANALYSIS.exists():
        return files, roots
    ledger_files = ledger_preserved_paths()
    text_queries = ledger_text_query_paths()
    for path in ANALYSIS.rglob("*.json"):
        # Never follow a private-state or external symlink to discover proofs.
        if path.is_symlink() or any(is_under(path, root) for root in PRESERVED_ANALYSIS_ROOTS):
            continue
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError, OSError):
            if path.name != "receipt.json" and path in text_queries:
                # Factory function queries intentionally emit plain text, even
                # when a historical caller chose a .json output name.
                files.add(path)
                continue
            if path.name == "receipt.json" or path in ledger_files:
                raise ValueError(f"cannot inspect retained proof: {path.relative_to(ROOT)}")
            continue
        if path.name == "receipt.json":
            roots.add(path.parent)

        def visit(node):
            if isinstance(node, dict):
                guards = node.get("inputs")
                if isinstance(guards, dict):
                    files.add(path)
                    for raw in guards:
                        if not isinstance(raw, str) or not raw:
                            continue
                        lexical = Path(raw)
                        if lexical.is_absolute() or ".." in lexical.parts:
                            continue
                        lexical = ROOT / lexical
                        files.add(lexical)
                        resolved = normalized_local_path(raw)
                        if resolved is not None:
                            files.add(resolved)
                for child in node.values():
                    visit(child)
            elif isinstance(node, list):
                for child in node:
                    visit(child)

        visit(value)
    return files, roots


def ledger_text_query_paths() -> set[Path]:
    """Recognize unchanged, explicitly recorded Factory text query outputs."""
    outputs: set[Path] = set()
    if not EVIDENCE.is_file():
        return outputs
    with EVIDENCE.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("tool") != "Factory-native-same-process-attested-headless-Ghidra-query":
                continue
            try:
                command = shlex.split(row.get("command", ""))
                query = command.index("query")
            except ValueError:
                continue
            location = row.get("location", "")
            if "scripts/factory_ghidra.py" not in command[:query] or command[query+1:query+3] != [location, "function"]:
                continue
            path = normalized_local_path(location)
            if path is None or path.name == "receipt.json" or not path.is_file():
                continue
            if hashlib.sha256(path.read_bytes()).hexdigest() == row.get("output_sha256"):
                outputs.add(path)
    return outputs


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

    proof_files, proof_roots = proof_preserved_paths()
    protected_files = ledger_preserved_paths() | PRESERVED_ANALYSIS_FILES | proof_files
    protected_roots = PRESERVED_ANALYSIS_ROOTS | proof_roots

    def protected_below(path: Path) -> bool:
        return any(is_under(protected, path) for protected in protected_files) or any(
            is_under(root, path) for root in protected_roots
        )

    def prune(path: Path) -> int:
        if any(is_under(path, root) for root in protected_roots):
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
    proof_files, proof_roots = proof_preserved_paths()
    protected = proof_files | proof_roots | ledger_preserved_paths()

    def guarded(path: Path) -> bool:
        return any(is_under(p, path) or is_under(path, p) for p in protected)

    for path in CACHE_ROOTS:
        if not guarded(path):
            removed += remove_path(path, dry_run)

    for base in (ROOT / "scripts", ROOT / "tests"):
        if not base.exists():
            continue
        for path in sorted(base.rglob("__pycache__")):
            if not guarded(path):
                removed += remove_path(path, dry_run)
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Prune disposable local build/replay/cache output while preserving "
            "required private state, guarded proof inputs and receipt trees."
        )
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="perform deletions; without this flag only report what would be removed",
    )
    parser.add_argument(
        "--prune-unreferenced-receipts",
        action="store_true",
        help=(
            "also remove receipt runs that are unreachable from current evidence, "
            "tracked concrete .analysis references and retained JSON input guards"
        ),
    )
    parser.add_argument(
        "--keep-analysis",
        action="append",
        default=[],
        metavar="PATH",
        help=(
            "extra repository-relative .analysis path to preserve during aggressive "
            "receipt pruning; repeat for multiple active runs"
        ),
    )
    args = parser.parse_args()

    extra_preserved: set[Path] = set()
    for raw in args.keep_analysis:
        path = normalized_local_path(raw)
        if path is None or not is_under(path, ANALYSIS):
            parser.error(f"--keep-analysis must stay under .analysis/: {raw}")
        extra_preserved.add(path)

    dry_run = not args.apply
    removed = 0
    if args.prune_unreferenced_receipts:
        removed += prune_unreferenced_receipts(dry_run, extra_preserved)
    removed += clean_analysis(dry_run) + clean_caches(dry_run)
    verb = "would remove" if dry_run else "removed"
    print(f"{verb} approximately {removed / (1024 * 1024):.1f} MiB")
    print(
        "preserved .analysis/toolchain, .analysis/targets, .analysis/runtime, "
        ".analysis/ghidra, target-import.json, ledger evidence and guarded inputs; "
        + (
            "unreferenced receipt trees were eligible because aggressive pruning was requested"
            if args.prune_unreferenced_receipts
            else "all cold receipt trees were preserved"
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
