#!/usr/bin/env python3
"""Stage only the pinned MAINL root/include pair. No compiler or replay is run."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = "src/mainl/memory/heap.inl"
SOURCE_SHA256 = "3960b8f2ff1821475f86d947b82380957a35ce4c7169a518689e857560774432"
ROOT_SHA256 = "d0c9d5b9576c9e1300d48a22449fb6acbc35c796e1071e21a2f5cf330d659713"
REFERENCE_REVISION = "b6ba5b0a529edbb31efdf8c0e939263804f8ee47"
PROVIDERS = (
    "libs/master.lib/hmem_lallocate.asm",
    "libs/master.lib/mem_assign_dos.asm",
    "libs/master.lib/mem_assign.asm",
    "libs/master.lib/memheap.asm",
    "libs/master.lib/mem_unassign.asm",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def replace_slot(root: bytes) -> bytes:
    """Preserve mixed-encoding bytes and every byte outside the frozen slot."""
    newline = b"\r\n" if b"\r\n" in root else b"\n"
    old = b"".join(b"include " + name.encode("ascii") + newline
                   for name in PROVIDERS)
    before = b"include libs/master.lib/palette_white_out.asm" + newline
    after = b"include libs/master.lib/super_free.asm" + newline
    replacement = b"include " + SOURCE_PATH.encode("ascii") + newline
    if replacement in root:
        raise ValueError("root already contains the maintained heap include")
    if any(root.count(b"include " + name.encode("ascii") + newline) != 1
           for name in PROVIDERS):
        raise ValueError("heap providers must each occupy one include slot")
    if root.count(before + old + after) != 1:
        raise ValueError("five consecutive include slots or neighbors differ")
    result = root.replace(before + old + after, before + replacement + after, 1)
    if result.count(replacement) != 1 or result.replace(replacement, old, 1) != root:
        raise ValueError("outside-root preservation failed")
    return result


def stage_root(root: bytes, source: bytes) -> bytes:
    """Reject identity drift before transforming the single reviewed slot."""
    if sha256(root) != ROOT_SHA256:
        raise ValueError("frozen root SHA-256 mismatch")
    if sha256(source) != SOURCE_SHA256:
        raise ValueError("maintained heap source SHA-256 mismatch")
    return replace_slot(root)


def read_regular(path: Path) -> bytes:
    path = path.absolute()
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise ValueError("input path may not traverse symlinks")
    if not path.is_file():
        raise ValueError("input must be a regular file")
    return path.read_bytes()


def stage_files(frozen_root: Path, output_dir: str) -> dict[str, object]:
    # One new leaf beneath .analysis only; never install into the default graph.
    path = PurePosixPath(output_dir)
    if (path.as_posix() != output_dir or len(path.parts) != 2
            or path.parts[0] != ".analysis"
            or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,95}", path.parts[1])):
        raise ValueError("output must be a fresh .analysis/NAME directory")
    root_bytes = read_regular(frozen_root)
    source = read_regular(ROOT / SOURCE_PATH)
    staged = stage_root(root_bytes, source)
    analysis = ROOT / ".analysis"
    if analysis.is_symlink() or (analysis.exists() and not analysis.is_dir()):
        raise ValueError(".analysis must be a real directory")
    analysis.mkdir(exist_ok=True)
    output = ROOT / path
    output.mkdir()  # Exclusive: preserve existing outputs, including partial failures.
    source_output = output / SOURCE_PATH
    source_output.parent.mkdir(parents=True)
    for destination, data in ((output / "th03_mainl.asm", staged),
                              (source_output, source)):
        with destination.open("xb") as handle:
            handle.write(data)
    report = {
        "kind": "mainl-heap-root-staging-only",
        "reference_revision": REFERENCE_REVISION,
        "root_input_sha256": sha256(root_bytes),
        "source_sha256": sha256(source),
        "staged_root_sha256": sha256(staged),
        "replaced_provider_count": len(PROVIDERS),
        "outside_root_preserved": True,
        "native_invocations": 0,
        "cold": False,
        "default_graph_modified": False,
        "exact_acceptance": False,
    }
    with (output / "staging.json").open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frozen-root", required=True, type=Path,
                        help="explicit pinned ReC98 th03_mainl.asm input")
    parser.add_argument("--output-dir", required=True,
                        help="new one-level .analysis/NAME directory")
    args = parser.parse_args()
    try:
        report = stage_files(args.frozen_root, args.output_dir)
    except (OSError, ValueError) as error:
        parser.exit(1, f"staging refused: {error}\n")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
