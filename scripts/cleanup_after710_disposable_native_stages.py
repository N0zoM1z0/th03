#!/usr/bin/env python3
"""Strict, one-time audit of six unreferenced *failed tool-configuration* stages.

Default is a read-only preview. --apply writes a SHA256 file manifest first,
then removes ONLY the six named, incomplete and externally unreferenced
stage pairs. --verify checks the irreversible audit receipt and absence.
Never operate on successfully reported native stages or any active receipt DAG.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
NATIVE = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK/probe"
WORK = ROOT / ".analysis/work"
AUDIT = ROOT / ".analysis/handoff/after710-linkslot-disposable-trials"
STAGES = ("af694a", "af694b", "af696a", "af699b", "af705a", "af705b")
MANIFEST = AUDIT / "deleted-tree-manifest.json"
REPORT = AUDIT / "report.json"
REASON = {
    "af694a": "ch_setup original TLINK response slot was incorrectly assumed generic",
    "af694b": "p_gauge native MAP segment row count incorrectly assumed four",
    "af696a": "split Combo native MAP segment rows incorrectly assumed four",
    "af699b": "p_exatt native MAP segment row count incorrectly assumed four",
    "af705a": "core original TLINK response slot incorrectly assumed generic",
    "af705b": "lose original MAP module incorrectly normalized to generic th03",
}
# Only these files are permitted to mention retired stage IDs *after* cleanup.
# Other documentation, source, config, and proof receipts prohibit disposal.
INERT_RETIREMENT_TEXT = {
    "scripts/cleanup_after710_disposable_native_stages.py",
    "docs/STORAGE_HANDOFF_CURRENT.md",
    "docs/STORAGE_HANDOFF_AFTER710.md",
}
NATIVE_PARENT_STAGES = ("af686a", "af703a", "af709a")


def require(condition: bool, what: str) -> None:
    if not condition:
        raise RuntimeError(what)


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode()


def paths_for(stage: str) -> tuple[Path, Path]:
    return NATIVE / stage, WORK / f"exatt-layout-{stage}"


def live_guards() -> None:
    require((ROOT / "config/targets.toml").is_file(), "pinned original target manifest")
    for stage in NATIVE_PARENT_STAGES:
        require((WORK / f"exatt-layout-{stage}/report.json").is_file()
                and (NATIVE / stage).is_dir(),
                "active native two-round receipts must stay " + stage)
    require((ROOT / ".analysis/handoff/after597-disposable-proof-trials/report.json").is_file(),
            "prior audited after597 retirement must stay")


def external_references() -> None:
    stages = [s.encode() for s in STAGES]
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).split(b"\x00")
    protected: list[str] = []
    for item in tracked:
        if not item:
            continue
        path = item.decode()
        if path in INERT_RETIREMENT_TEXT:
            continue
        f = ROOT / path
        if not f.is_file() or f.is_symlink():
            continue
        # Tracked text must be unambiguously unreferenced, not just absent
        # from the currently short handoff. Binary files do not pin IDs.
        try:
            raw = f.read_bytes()
        except OSError:
            raise RuntimeError("cannot audit tracked file " + path)
        if b"\x00" not in raw[:4096] and any(s in raw for s in stages):
            protected.append(path)
    require(not protected, "tracked source/document refers to failed stages: " + repr(protected))

    # Scan ALL ignored JSON receipts, not only the latest MAIN report.
    # No successful native source DAG may refer to the removed stage names.
    linked: list[str] = []
    for f in WORK.rglob("*.json"):
        if any(f.is_relative_to(paths_for(s)[1]) for s in STAGES):
            continue
        if f.is_symlink() or not f.is_file():
            continue
        raw = f.read_bytes()
        if any(s in raw for s in stages):
            linked.append(f.relative_to(ROOT).as_posix())
    require(not linked, "an active work JSON references failed stage: " + repr(linked[:20]))


def snapshot() -> dict:
    roots, files = [], []
    total_allocated = 0
    total_size = 0
    for stage in STAGES:
        native, work = paths_for(stage)
        require(native.is_dir() and work.is_dir(), "missing allowed disposable pair " + stage)
        require(not native.is_symlink() and not work.is_symlink(),
                "untrusted symlink in stage roots " + stage)
        require(not (work / "report.json").exists(),
                "successful native receipt: deletion prohibited " + stage)
        require(not (native / "r2").exists(),
                "second native round exists: do not retire " + stage)
        require(not any(p.name == "report.json" for tree in (native,work)
                        for p in tree.rglob("*")),
                "possible proof report inside failed stage: " + stage)
        for tree in (native, work):
            entry_count = 0
            for node in (tree, *tree.rglob("*")):
                require(not node.is_symlink(), "symlink in disposable root: " + str(node))
                require(node.is_dir() or node.is_file(), "unexpected native node " + str(node))
                total_allocated += node.stat().st_blocks * 512
                if node.is_file():
                    raw = node.read_bytes()
                    total_size += len(raw)
                    entry_count += 1
                    files.append({"path": node.relative_to(ROOT).as_posix(),
                                  "size": len(raw), "allocated": node.stat().st_blocks * 512,
                                  "sha256": digest(raw)})
            roots.append({"path": tree.relative_to(ROOT).as_posix(),
                          "stage": stage, "files": entry_count})
    return {"schema": "th03-after710-disposable-failed-config-stages-v1",
            "retired_stages": list(STAGES), "reasons": REASON,
            "roots": roots, "files": sorted(files,key=lambda f:f["path"]),
            "total_files": len(files), "total_regular_bytes": total_size,
            "total_allocated_bytes_including_dirs": total_allocated,
            "excluded_accepted_native_receipts": list(NATIVE_PARENT_STAGES)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--apply", action="store_true", help="audit, manifest, then remove exactly six stage pairs")
    group.add_argument("--verify", action="store_true", help="verify completed retirement, without modifications")
    opt = ap.parse_args()
    live_guards()
    if opt.verify:
        require(REPORT.is_file() and MANIFEST.is_file(), "retirement manifest and receipt missing")
        raw = MANIFEST.read_bytes()
        report = json.loads(REPORT.read_bytes())
        require(digest(raw) == report["manifest_sha256"],
                "manifest SHA drift after retirement")
        manifest = json.loads(raw)
        require(tuple(manifest["retired_stages"]) == STAGES and
                report["total_files"] == manifest["total_files"] and
                report["allocated_bytes_recovered"] ==
                manifest["total_allocated_bytes_including_dirs"],
                "audit stage list or size was changed")
        for stage in STAGES:
            require(all(not path.exists() for path in paths_for(stage)),
                    "audited obsolete stage reappeared: " + stage)
        print("after710 audit VERIFIED:", report["total_files"],
              "files retired,", report["allocated_bytes_recovered"], "allocated bytes; "
              "all active native receipt roots preserved")
        return

    require(not AUDIT.exists(), "refuse to overwrite an existing retirement audit")
    external_references()
    data = snapshot()
    print("DISPOSABLE-ONLY REVIEW:",len(STAGES),"failed configuration stages,",
          len(data["roots"]),"isolated trees,",data["total_files"],"files,",
          data["total_allocated_bytes_including_dirs"],"allocated bytes")
    for stage in STAGES:
        print(" ",stage,":",REASON[stage])
    if not opt.apply:
        print("PREVIEW ONLY: no files deleted, no proof receipts altered")
        return

    # Both manifest and a human-readable summary are durably written before
    # any deletion. Nothing from a completed source-native proof is touched.
    AUDIT.mkdir(parents=True)
    content = json_bytes(data)
    MANIFEST.write_bytes(content)
    report = {
        "schema": "th03-after710-disposable-retirement-receipt-v1",
        "manifest_sha256": digest(content),
        "stage_count": len(STAGES),
        "roots_deleted":len(data["roots"]),
        "total_files": data["total_files"],
        "allocated_bytes_recovered":data["total_allocated_bytes_including_dirs"],
        "retired_stages":list(STAGES),
        "safety": "no native report; no r2; no tracked reference; no other work JSON reference",
    }
    REPORT.write_bytes(json_bytes(report))
    for stage in STAGES:
        for path in paths_for(stage):
            shutil.rmtree(path)
    require(all(not path.exists() for s in STAGES for path in paths_for(s)),
            "some stage directory remained after cleanup")
    print("APPLIED strict manifest-backed cleanup:",data["total_files"],
          "files,",data["total_allocated_bytes_including_dirs"],"allocated bytes")


if __name__ == "__main__":
    main()
