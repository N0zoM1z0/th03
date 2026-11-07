#!/usr/bin/env python3
"""After597: narrowly audited retirement of three UNREFERENCED boss probe runs.

This is NOT a native receipt DAG pruner. The active after559 Chiyuri
and after561 eight-boss first-use proof rounds are explicitly protected,
as are after596 MAIN, after587 MAINL, after520 and their stored artifacts.
Only the three exact old exploratory run IDs below are eligible. Before
removing their duplicate expanded source/reference trees, preserve each
original tiny receipt/compiler log and a full path/size/SHA-256 manifest
in the private .analysis/handoff/after597-disposable-proof-trials directory.
No source files, targets, libraries, accepted products, Wine tools,
active native inputs or other .analysis paths may be deleted.

Commands:
  .venv/bin/python scripts/cleanup_after597_handoff_storage.py --preview
  .venv/bin/python scripts/cleanup_after597_handoff_storage.py --apply
  .venv/bin/python scripts/cleanup_after597_handoff_storage.py --verify
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / ".analysis/handoff/after597-disposable-proof-trials"

RETIRED = (
    ".analysis/th03-main-boss-chiyuri-cpp/gptweb-chiyuri-559",
    ".analysis/th03-main-boss-chiyuri-cpp/gptweb-chiyuri-559-native-r1",
    ".analysis/th03-main-boss-marisa-cpp/gptweb-marisa-561-native-test",
)
EXPECTED_FILES = (1779, 1779, 1773)
EXPECTED_ALLOCATED = (26324992, 26324992, 26288128)

# All of these are CURRENT, immutable root receipts and must remain present.
PROTECTED_ROOTS = {
    ".analysis/work/main-chiyuri-after559-native-build.json":
        "7a71a981f5832449198b7c8ba4e79000bcdac2e5b3149ac35a5049e1c5c52d5c",
    ".analysis/work/main-eight-boss-after561-native-build.json":
        "dd895851b5f7a4c76541d1e6f197e7f074a0156093efc182de5ba86ccbd61d0a",
    ".analysis/work/main-yumemi-cpu-after596-native-build.json":
        "bdc70dfa4d48ed66c76cb9cd18ef7c3add5e65a8e6a2183d730cb1621f5dc8c3",
    ".analysis/work/mainl-score-input-pi-after587-native-build.json":
        "439917fca4e1a0d6984ab9f9fe31e3431da74d0bc68a518c2d14c55693724c82",
    ".analysis/work/mainl-after520-fstreambase-virtual-setbuf-ios-state-build.json":
        "f32c534f42d520f2c07a3acce769857d01ef310c04c00b419b585bf650994d8e",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def need(ok: bool, reason: str) -> None:
    if not ok:
        raise ValueError("after597 fail-closed disposable-trial cleanup: " + reason)


def previous_proofs() -> dict:
    out = {}
    for name, expected in PROTECTED_ROOTS.items():
        p = ROOT / name
        need(p.is_file() and sha(p.read_bytes()) == expected,
             "protected source-native proof root changed: " + name)
        out[name] = expected

    chiyuri = json.loads((ROOT / list(PROTECTED_ROOTS)[0]).read_bytes())
    eight = json.loads((ROOT / list(PROTECTED_ROOTS)[1]).read_bytes())
    need(chiyuri["complete"] and eight["complete"],
         "original 559/561 active source proofs must remain complete")
    need([row["probe_run_id"] for row in chiyuri["rounds"]] ==
         ["gptweb-chiyuri-559-proof-r1", "gptweb-chiyuri-559-proof-r2"],
         "exact original Chiyuri native proof source dirs")
    eight_ids = {
        row["original_OMF"][boss]["probe_run_id"]
        for row in eight["rounds"] for boss in row["original_OMF"]
    }
    expected_eight = {
        f"gptweb-561-{boss}-r{n}"
        for boss in ("yumemi", "kana", "mima", "reimu",
                     "kotohime", "ellen", "rikako", "marisa")
        for n in (1, 2)
    }
    need(eight_ids == expected_eight,
         "all 16 retained native BOSS proof materializations")
    for proof_id in (
        "gptweb-chiyuri-559-proof-r1", "gptweb-chiyuri-559-proof-r2",
        *sorted(eight_ids),
    ):
        stem = proof_id.split("-")
        boss = "chiyuri" if "chiyuri" in stem else stem[2]
        path = ROOT / f".analysis/th03-main-boss-{boss}-cpp/{proof_id}"
        need(path.is_dir() and (path / "receipt.json").is_file()
             and (path / "source").is_dir(),
             "all active original native proof directories still present: " + proof_id)
    return out


def reference_files() -> list[Path]:
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    files = []
    skip = {
        "scripts/cleanup_after597_handoff_storage.py",
        "docs/STORAGE_HANDOFF_CURRENT.md",
        "docs/STORAGE_HANDOFF_AFTER597.md",
        "tests/test_after597_cleanup.py",
    }
    for raw in tracked.split(b"\0"):
        if not raw:
            continue
        path = Path(os.fsdecode(raw))
        if path.as_posix() in skip:
            continue
        candidate = ROOT / path
        if candidate.is_file() and not candidate.is_symlink():
            files.append(candidate)
    for folder in (ROOT/".analysis/work", ROOT/".analysis/handoff"):
        if not folder.exists():
            continue
        for candidate in folder.rglob("*"):
            if not candidate.is_file() or candidate.is_symlink():
                continue
            if AUDIT in candidate.parents:
                continue
            if (candidate.suffix.lower() in {
                ".json", ".md", ".txt", ".log", ".py", ".sh", ".toml", ".yaml",
            } and candidate.stat().st_size <= 4_000_000):
                files.append(candidate)
    return files


def references() -> dict[str, list[str]]:
    ids = [Path(p).name for p in RETIRED]
    patterns = {key: re.compile(
        re.escape(key) + rb"(?![a-zA-Z0-9_-])")
        for key in (key.encode("ascii") for key in ids)}
    hits = {name: [] for name in ids}
    for path in reference_files():
        data = path.read_bytes()
        for raw_id, expr in patterns.items():
            if expr.search(data):
                hits[raw_id.decode("ascii")].append(
                    str(path.relative_to(ROOT)))
    return hits


def tree_manifest() -> list[dict]:
    result = []
    for rel, expected_count, expected_alloc in zip(
        RETIRED, EXPECTED_FILES, EXPECTED_ALLOCATED
    ):
        path = ROOT / rel
        need(path.is_dir() and not path.is_symlink()
             and path.resolve().is_relative_to(ROOT.resolve()),
             "only an explicit existing private exploratory run may be retired: " + rel)
        items = []
        for node in sorted(path.rglob("*")):
            need(not node.is_symlink(), "no unexpected symlink: " + str(node))
            if node.is_dir():
                continue
            need(node.is_file(), "unexpected non-file in proof run: " + str(node))
            st = node.stat()
            need(st.st_nlink == 1, "original native artifact has hardlink: " + str(node))
            items.append(dict(path=str(node.relative_to(ROOT)),
                bytes=st.st_size, allocated_bytes=st.st_blocks * 512,
                sha256=sha(node.read_bytes())))
        files = len(items)
        allocated = sum(x["allocated_bytes"] for x in items)
        need(files == expected_count and allocated == expected_alloc,
             "candidate source workspace changed or references unexpectedly added: " + rel)
        for stub in ("receipt.json", "compiler.log", "reference.tar"):
            need((path / stub).is_file(), "missing original source probe evidence: " + rel+"/"+stub)
        report = json.loads((path / "receipt.json").read_bytes())
        need(report.get("source_acceptance") is True and
             report.get("exact_acceptance") is False,
             "old exploratory source probe must not be mistaken for accepted whole-object credit")
        result.append(dict(path=rel,files=files,
            allocated_bytes=allocated,logical_bytes=sum(x["bytes"] for x in items),
            candidate_OMF_sha256=report["object"]["sha256"],entries=items))
    return result


def apply() -> None:
    previous_proofs()
    blocked = references()
    need(not any(blocked.values()), "candidate still externally referenced: " +
         repr({k: v[:3] for k, v in blocked.items() if v}))
    manifest = tree_manifest()
    need(not AUDIT.exists(), "retirement already audited; use --verify, never apply again")
    AUDIT.mkdir(parents=True)
    manifest_raw = (json.dumps(manifest,indent=2,ensure_ascii=True)+"\n").encode()
    (AUDIT/"deleted-tree-manifest.json").write_bytes(manifest_raw)
    archive = AUDIT/"tiny-original-compiler-receipts"
    archive.mkdir()
    for entry in manifest:
        root = ROOT / entry["path"]
        dest = archive / root.name
        dest.mkdir()
        for name in ("receipt.json","compiler.log"):
            shutil.copy2(root/name,dest/name)
    snapshot = {
        "status": "pending-delete",
        "method": "exact allowlisted unreferenced exploratory boss proof directories",
        "current_source_native_DAG_protected": PROTECTED_ROOTS,
        "source_ref_scan": blocked,
        "current_retired_roots": RETIRED,
        "manifest_sha256": sha(manifest_raw),
        "candidate_root_files": sum(x["files"] for x in manifest),
        "candidate_logical_bytes": sum(x["logical_bytes"] for x in manifest),
        "candidate_allocated_bytes": sum(x["allocated_bytes"] for x in manifest),
        "archived": {},
    }
    for entry in manifest:
        name = Path(entry["path"]).name
        snapshots = {}
        for filename in ("receipt.json", "compiler.log"):
            f = archive/name/filename
            snapshots[filename] = dict(
                sha256=sha(f.read_bytes()),bytes=f.stat().st_size)
        snapshot["archived"][name] = snapshots
    report = AUDIT/"report.json"
    report.write_text(json.dumps(snapshot,indent=2)+"\n")
    for entry in manifest:
        path=ROOT/entry["path"]
        need(path.is_dir() and not path.is_symlink(),
             "explicit candidate path changed before deletion")
        shutil.rmtree(path)
        need(not path.exists(), "failed to retire only exact approved path")
    snapshot["status"] = "applied"
    report.write_text(json.dumps(snapshot,indent=2)+"\n")
    verify()
    print("Applied safely: retired",snapshot["candidate_root_files"],
          "unreferenced exploratory files /",
          snapshot["candidate_allocated_bytes"],"allocated bytes; active evidence intact")


def verify() -> None:
    previous_proofs()
    report = json.loads((AUDIT/"report.json").read_text())
    need(report["status"] == "applied" and
         tuple(report["current_retired_roots"]) == RETIRED and
         report["candidate_root_files"] == sum(EXPECTED_FILES) and
         report["candidate_allocated_bytes"] == sum(EXPECTED_ALLOCATED) and
         report["current_source_native_DAG_protected"] == PROTECTED_ROOTS,
         "complete source-root protected cleanup receipt and exact bound")
    manifest_bytes = (AUDIT/"deleted-tree-manifest.json").read_bytes()
    need(sha(manifest_bytes) == report["manifest_sha256"],
         "full original source file SHA-256 retirement inventory preserved")
    manifest = json.loads(manifest_bytes)
    need([m["path"] for m in manifest] == list(RETIRED) and
         [m["files"] for m in manifest] == list(EXPECTED_FILES) and
         [m["allocated_bytes"] for m in manifest] == list(EXPECTED_ALLOCATED),
         "original exact native trial count and size")
    for item in manifest:
        need(not (ROOT/item["path"]).exists(),
             "no partial or superseded run workspace survived")
        name = Path(item["path"]).name
        files = report["archived"][name]
        for filename,info in files.items():
            blob = (AUDIT/"tiny-original-compiler-receipts"/name/filename).read_bytes()
            need(sha(blob)==info["sha256"] and len(blob)==info["bytes"],
                 "original native compiler log/receipt is still archived")
    print("Cleanup review PASS:",
          report["candidate_root_files"],"unreferenced files retired,",
          report["candidate_allocated_bytes"],"allocated bytes recovered; active originals retained")


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    action=parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--preview",action="store_true")
    action.add_argument("--apply",action="store_true")
    action.add_argument("--verify",action="store_true")
    opts=parser.parse_args()
    if opts.verify:
        verify()
    elif opts.apply:
        apply()
    else:
        previous_proofs()
        if AUDIT.exists():
            verify()
            return
        hits=references()
        need(not any(hits.values()),"external source reference to candidate: "+repr(hits))
        rows=tree_manifest()
        print("SAFE PREVIEW ONLY: 3 explicitly unreferenced exploratory roots,",
              sum(x["files"] for x in rows),"files;",
              sum(x["allocated_bytes"] for x in rows),
              "allocated bytes. Active 559/561 BOSS and latest MAIN/MAINL/CRT retained.")


if __name__=="__main__":
    main()
