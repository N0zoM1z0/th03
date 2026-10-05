#!/usr/bin/env python3
"""Inventory the frozen ReC98 TH03 intake without granting acceptance credit.

Include traversal is deliberately conservative: all conditional branches are
followed. This is a review queue, not a preprocessed build/dependency graph.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "_reference/ReC98"
INVENTORY = ROOT / "config/rec98_th03_inventory.csv"
REVIEWS = ROOT / "config/rec98_th03_reviews.csv"
SOURCE_SUFFIXES = {".c", ".cpp", ".asm", ".h", ".hpp", ".inc", ".inl"}
FIELDS = ["path", "sha256", "kind", "artifacts", "direct_link_artifacts",
          "unresolved_includes", "reviewed_code_artifacts", "boundary_review_artifacts"]
REVIEWED_REVISION = "b6ba5b0a529edbb31efdf8c0e939263804f8ee47"


def frozen_files(revision: str) -> dict[str, bytes]:
    if revision != REVIEWED_REVISION:
        raise ValueError("review named Lua subgraphs before changing intake revision")
    archive = subprocess.check_output(
        ["git", "archive", revision], cwd=REFERENCE
    )
    with tarfile.open(fileobj=io.BytesIO(archive)) as stream:
        return {member.name: stream.extractfile(member).read()
                for member in stream if member.isfile()}


def link_roots(files: dict[str, bytes]) -> dict[str, set[str]]:
    text = files["Tupfile.lua"].decode()
    section = text.split("-- TH03\n-- ----\n", 1)[1].split("-- TH04\n", 1)[0]
    roots = {}
    for product in ("op", "main", "mainl"):
        block = section.split(f':link("{product}", {{', 1)[1].split("\n})", 1)[0]
        roots[f"th03-{product}"] = set(re.findall(
            r'"([^"\n]+\.(?:cpp|c|asm))"', block
        ))
    # Named Lua subgraphs and the sprite16 table are declared outside TH03's
    # block. Keep these explicit; a changed revision must be reviewed again.
    roots["th03-zun"] = {
        "th02_zuninit.asm", "th01/zunsoft.cpp", "libs/sprite16/sprite16.asm",
        "th03/res_yume.cpp", "Pipeline/zungen.c", "Pipeline/zun_stub.asm",
    }
    if any(path not in files for paths in roots.values() for path in paths):
        raise ValueError("frozen link root missing")
    return roots


def include_paths(path: str, data: bytes) -> list[str]:
    text = data.decode("utf-8", errors="replace")
    if PurePosixPath(path).suffix.lower() in {".asm", ".inc"}:
        return re.findall(r'^\s*include\s+["<]?([^\s;">]+)', text, re.I | re.M)
    # System headers belong to the separately attested Borland toolchain.
    return re.findall(r'^\s*#\s*include\s+"([^"\n]+)"', text, re.M)


def review_rows() -> list[dict[str, str]]:
    with REVIEWS.open(newline="") as stream:
        return list(csv.DictReader(stream))


def inventory(files: dict[str, bytes], reviews: list[dict[str, str]]) -> list[dict]:
    roots = link_roots(files)
    membership: dict[str, set[str]] = {}
    unresolved: dict[str, set[str]] = {}
    # Catalog every dedicated TH03 file, including currently unlinked files
    # and sprite assets. Assets are metadata only and must never be imported.
    dedicated = {p for p in files if p.startswith("th03/") or
                 re.fullmatch(r"th03[^/]*\.(?:asm|inc)", p)}
    pending = [(artifact, path) for artifact, paths in roots.items() for path in paths]
    pending += [("unassigned", path) for path in dedicated]
    seen = set()
    while pending:
        artifact, path = pending.pop()
        if (artifact, path) in seen:
            continue
        seen.add((artifact, path))
        membership.setdefault(path, set()).add(artifact)
        if PurePosixPath(path).suffix.lower() not in SOURCE_SUFFIXES:
            continue
        for include in include_paths(path, files[path]):
            include = include.replace("\\", "/")
            relative = str(PurePosixPath(path).parent / include)
            resolved = next((p for p in (include, relative) if p in files), None)
            if resolved is None:
                unresolved.setdefault(path, set()).add(include)
            else:
                pending.append((artifact, resolved))
    accepted: dict[str, set[str]] = {}
    boundaries: dict[str, set[str]] = {}
    keys = set()
    manifest = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    units = {u["id"]: u for u in manifest["units"]}
    candidate_path = ROOT / "config/th03_main_enemy_candidate.toml"
    if candidate_path.is_file():
        for unit in tomllib.loads(candidate_path.read_text())["units"]:
            if unit["id"] in units:
                raise ValueError("candidate replaces an accepted intake owner")
            units[unit["id"]] = unit
    with (ROOT / "config/units.csv").open(newline="") as stream:
        ledger = {r["id"]: r for r in csv.DictReader(stream)}
    with (ROOT / "config/evidence.csv").open(newline="") as stream:
        evidence = {r["id"]: r for r in csv.DictReader(stream)}
    for row in reviews:
        key = (row["artifact"], row["path"])
        if key in keys or row["path"] not in membership:
            raise ValueError(f"duplicate or out-of-scope review: {key}")
        keys.add(key)
        if row["artifact"] not in membership[row["path"]]:
            raise ValueError(f"artifact outside conservative include closure: {key}")
        if row["state"] not in {"accepted-code-extents", "boundary-reviewed"}:
            raise ValueError(f"unknown review state: {row['state']}")
        if row["artifact"] != manifest["artifact"]:
            raise ValueError(f"review artifact differs from replay manifest: {key}")
        for owner_id in row["owner_ids"].split(";"):
            if owner_id not in units or units[owner_id]["source"] != row["source"]:
                raise ValueError(f"review lacks maintained replay owner: {key}")
            owner = units[owner_id]
            extent_ids = [e["ledger_id"] for e in owner.get(
                "code_extents", [{"ledger_id": owner_id}])]
            if any(ledger[e]["source"] != row["source"] or
                   ledger[e]["boundary_state"] != "reviewed" or
                   (row["state"] == "accepted-code-extents" and ledger[e]["state"] != "exact")
                   for e in extent_ids):
                raise ValueError(f"review owner is not locally accepted: {key}")
        if not row["evidence_ids"] or not row["notes"]:
            raise ValueError(f"review lacks evidence or scope: {key}")
        if any(e not in evidence or evidence[e]["result"] != "pass"
               for e in row["evidence_ids"].split(";")):
            raise ValueError(f"review evidence is missing or failed: {key}")
        boundaries.setdefault(row["path"], set()).add(row["artifact"])
        if row["state"] == "accepted-code-extents":
            accepted.setdefault(row["path"], set()).add(row["artifact"])
    rows = []
    for path, artifacts in sorted(membership.items()):
        if artifacts != {"unassigned"}:
            artifacts.discard("unassigned")
        suffix = PurePosixPath(path).suffix.lower()
        kind = ("translation-unit" if suffix in {".c", ".cpp", ".asm"} else
                "include" if suffix in SOURCE_SUFFIXES else "asset-metadata-only")
        rows.append({
            "path": path, "sha256": hashlib.sha256(files[path]).hexdigest(),
            "kind": kind, "artifacts": ";".join(sorted(artifacts)),
            "direct_link_artifacts": ";".join(sorted(
                a for a, paths in roots.items() if path in paths)),
            "unresolved_includes": ";".join(sorted(unresolved.get(path, set()))),
            "reviewed_code_artifacts": ";".join(sorted(accepted.get(path, set()))),
            "boundary_review_artifacts": ";".join(sorted(boundaries.get(path, set()))),
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    revision = tomllib.loads((ROOT / "config/build.toml").read_text())["reference_revision"]
    rows = inventory(frozen_files(revision), review_rows())
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    if args.check:
        if not INVENTORY.is_file() or INVENTORY.read_text() != output.getvalue():
            raise ValueError("stale TH03 intake inventory; regenerate after review")
    else:
        INVENTORY.write_text(output.getvalue())
    print(f"ReC98 TH03 intake: {len(rows)} files; "
          f"{sum(bool(r['reviewed_code_artifacts']) for r in rows)} with scoped CODE review; "
          "remaining file/artifact review stays open")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
