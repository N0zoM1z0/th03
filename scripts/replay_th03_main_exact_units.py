#!/usr/bin/env python3
"""Replay maintained TH03 MAIN exact owners using the TH04 cold-build method.

Two isolated git archives receive frozen maintained sources. Every scaffold
object is rebuilt, and each full owned extent is checked independently. This
local Oracle does not publish Factory Truth Kernel acceptance.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib

from lib.omf import describe_omf, normalize_dependency_timestamps
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "_reference/ReC98"
FLAGS = ["-c", "-I.", "-O", "-b-", "-3", "-Z", "-d", "-DGAME=3", "-ml"]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compare_extent(target: bytes, candidate: bytes, start: int, size: int) -> dict:
    """Compare an entire payload extent and its relocation multiplicities."""
    left, right = parse_mz(target), parse_mz(candidate)
    if not left.valid or not right.valid or start < 0 or size <= 0:
        raise ValueError("invalid MZ or extent")
    end = start + size
    if end > len(left.program_image) or end > len(right.program_image):
        raise ValueError("extent exceeds a load module")
    # Reject a relocation word straddling either ownership edge.
    for image in (left, right):
        for relocation in image.relocations:
            if relocation.linear < end and relocation.linear + 2 > start:
                if not start <= relocation.linear <= end - 2:
                    raise ValueError("relocation crosses extent boundary")
    a, b = left.program_image[start:end], right.program_image[start:end]
    sites_a = Counter(r.linear - start for r in left.relocations if start <= r.linear < end)
    sites_b = Counter(r.linear - start for r in right.relocations if start <= r.linear < end)
    ordered_a = [r.linear - start for r in left.relocations if start <= r.linear < end]
    ordered_b = [r.linear - start for r in right.relocations if start <= r.linear < end]
    return {
        "payload_offset": start, "size": size,
        "target_file_offset": left.header.header_size + start,
        "candidate_file_offset": right.header.header_size + start,
        "target_sha256": sha(a), "candidate_sha256": sha(b),
        "differing_bytes": sum(x != y for x, y in zip(a, b)),
        "raw_equal": a == b,
        "target_relocation_sites": sorted(sites_a.elements()),
        "candidate_relocation_sites": sorted(sites_b.elements()),
        "relocations_equal": sites_a == sites_b and ordered_a == ordered_b,
        "ordered_relocations_equal": ordered_a == ordered_b,
    }


def execute(argv: list[str], work: Path, env: dict, log: Path) -> dict:
    result = subprocess.run(argv, cwd=work, env=env, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=180)
    log.write_bytes(result.stdout)
    if result.returncode:
        raise ValueError(f"tool exit {result.returncode}; see {log.relative_to(ROOT)}")
    return {"argv": argv, "exit_code": result.returncode,
            "log_sha256": sha(result.stdout)}


def replay(run_id: str, selected_units: list[str]) -> dict:
    config = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", run_id):
        raise ValueError("run-id must use 1-64 ASCII letters, digits, underscores or hyphens")
    output = ROOT / ".analysis/th03-main-exact" / run_id
    output.mkdir(parents=True, exist_ok=False)
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), config["artifact"])
    target = read_verified_artifact(ROOT, artifact)
    if sha(target) != config["target_sha256"]:
        raise ValueError("exact owner target binding differs")
    revision = subprocess.check_output(["git", "rev-parse", config["reference_revision"]],
                                       cwd=REFERENCE, text=True).strip()
    if revision != config["reference_revision"]:
        raise ValueError("reference revision differs")
    owner_ids = {unit["id"] for unit in config["units"]}
    if set(selected_units) - owner_ids:
        raise ValueError("unknown exact owner selection")
    with (ROOT / "config/units.csv").open(newline="") as stream:
        unit_rows = list(csv.DictReader(stream))
    accepted = {row["id"] for row in unit_rows
                if row["artifact"] == config["artifact"] and row["state"] == "exact"}
    if accepted - owner_ids:
        raise ValueError("aggregate omits an accepted owner")
    image = parse_mz(target)
    for unit in config["units"]:
        rows = [row for row in unit_rows if row["id"] == unit["id"]]
        if rows:
            row = rows[0]
            expected_offset = config["segment"] * 16 + unit["start"] + image.header.header_size
            if (row["artifact"] != config["artifact"] or row["source"] != unit["source"]
                or int(row["file_offset"], 0) != expected_offset
                or int(row["size"], 0) != unit["size"]
                or int(row["compare_size"], 0) != unit["size"]):
                raise ValueError(f"ledger/manifest owner mismatch: {unit['id']}")
    for script in ("scripts/validate_tracking.py", "scripts/progress.py"):
        argv = [sys.executable, script] + (["--check"] if script.endswith("progress.py") else [])
        subprocess.run(argv, cwd=ROOT, stdout=subprocess.DEVNULL, check=True)
    # Attest tools before execution. The caller serializes Borland writers.
    with (output / "tool-attestation.log").open("w") as log:
        subprocess.run([sys.executable, "scripts/attest_toolchain.py"],
                       cwd=ROOT, stdout=log, check=True)
    tool = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    prefix = ROOT / tool["paths"]["wine_prefix"]
    env = os.environ.copy()
    env.update(DISPLAY="", WAYLAND_DISPLAY="", WINEDEBUG="-all", WINEPREFIX=str(prefix),
               MSDOS_PATH=r"C:\TC4\BIN")
    dos = ["wine", str(ROOT / tool["paths"]["msdos_player"]), "-e", "-x"]
    inputs = {}
    for module in config["units"]:
        for key in ("source", "header"):
            path = ROOT / module[key]
            inputs[module[key]] = sha(path.read_bytes())
    inputs["probes/main/input_math_behavior.cpp"] = sha((ROOT / "probes/main/input_math_behavior.cpp").read_bytes())
    inputs["config/th03_main_exact_units.toml"] = sha((ROOT / "config/th03_main_exact_units.toml").read_bytes())
    inputs["scripts/replay_th03_main_exact_units.py"] = sha(Path(__file__).read_bytes())
    for name in ("config/targets.toml", "config/toolchain.toml", "config/oracles.toml",
                 "scripts/attest_toolchain.py", "scripts/validate_tracking.py",
                 "scripts/progress.py", "tests/test_main_exact_oracle.py"):
        inputs[name] = sha((ROOT / name).read_bytes())
    for path in (ROOT / "scripts/lib").glob("*.py"):
        inputs[path.relative_to(ROOT).as_posix()] = sha(path.read_bytes())
    snapshot = output / "repository-inputs"
    for name, digest in inputs.items():
        destination = snapshot / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, destination)
        if sha(destination.read_bytes()) != digest:
            raise ValueError("source changed while freezing inputs")
    archive = output / "reference.tar"
    subprocess.run(["git", "archive", "--format=tar", f"--output={archive}", revision],
                   cwd=REFERENCE, check=True)
    report = {"kind": "th03-main-owned-extent-cold-replay", "scope": config["scope"],
              "run_id": run_id, "target_sha256": sha(target),
              "reference_revision": config["reference_revision"],
              "reference_archive_sha256": sha(archive.read_bytes()), "source_inputs": inputs,
              "selected_units": selected_units or sorted(owner_ids),
              "aggregate_units": sorted(owner_ids), "compiler_flags": FLAGS,
              "accepted_units_at_start": sorted(accepted),
              "determinism_object_roots": config["determinism_object_roots"],
              "toolchain_receipt_sha256": sha((ROOT / ".analysis/toolchain/attestation.json").read_bytes()),
              "environment": {key: env[key] for key in ("DISPLAY", "WAYLAND_DISPLAY", "WINEDEBUG", "MSDOS_PATH")},
              "rounds": []}
    stem = "P" + sha(run_id.encode())[:5].upper()
    for number in (1, 2):
        logs = output / f"round{number}"
        logs.mkdir()
        work = logs / "source"
        work.mkdir()
        subprocess.run(["tar", "-xf", str(archive), "-C", str(work)], check=True)
        if list(work.rglob("*.obj")) or list((work / "bin").glob("th0[1-5]/*.exe")):
            raise ValueError("cold scaffold contains cached game objects or products")
        for module in config["units"]:
            for key in ("source", "header"):
                destination = work / module[key]
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(snapshot / module[key], destination)
            (work / f"th03/{module['object']}.cpp").write_text(f'#include "{module["source"]}"\n')
        build_command = ["wine", "cmd", "/d", "/c",
                         r"set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%"
                         r"&&set PROCESSOR_ARCHITECTURE=AMD64"
                         r"&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat"]
        compile_result = execute(build_command, work, env, logs / "cold-build.log")
        objects = {m["object"]: describe_omf((work / f"obj/th03/{m['object']}.obj").read_bytes())
                   for m in config["units"]}
        all_objects = {p.relative_to(work).as_posix(): sha(normalize_dependency_timestamps(p.read_bytes()))
                       for p in sorted((work / "obj").rglob("*.obj"))}
        products = {}
        for target_artifact in load_target_manifest(ROOT / "config/targets.toml")["artifacts"]:
            relative = Path("bin") / target_artifact["game"] / Path(target_artifact["private_path"]).name
            products[relative.as_posix()] = sha((work / relative).read_bytes())
        game_objects = {name: digest for name, digest in all_objects.items()
                        if any(name.startswith(directory + "/") for directory in config["determinism_object_roots"])}
        if (len(products) != 20 or len(all_objects) != config["generated_object_count"]
            or len(game_objects) != config["determinism_object_count"]):
            raise ValueError("cold build output/object vector incomplete")
        for obj in objects.values():
            if "TC86 Borland C++ 4.02" not in obj["translator_comments"]:
                raise ValueError("owned object producer differs")
        candidate = (work / "bin/th03/main.exe").read_bytes()
        # Confirm link-map publics cover exactly the reviewed starts and ends.
        map_text = (work / "obj/th03/main.map").read_text(errors="replace")
        contributions = []
        for unit in config["units"]:
            pattern = (rf"^\s*{config['segment']:04X}:{unit['start']:04X}\s+{unit['size']:04X}"
                       rf"\s+C=CODE\s+S=SHARED\s+G=\(none\)\s+M=th03/{unit['object']}\.cpp\s+ACBP=28\s*$")
            found = re.findall(pattern, map_text, re.MULTILINE)
            if len(found) != 1:
                raise ValueError(f"map ownership, size, segment or alignment moved: {unit['id']}")
            contributions.append({"id": unit["id"], "map": found[0].strip()})
        functions = []
        for function in config["functions"]:
            spelling = ("polar(int,int,int)" if function["name"] == "polar" else
                        function["name"] + ("(int)" if function["name"] == "input_wait_for_change" else "()"))
            pattern = rf"^\s*{config['segment']:04X}:{function['offset']:04X}\s+(?:idle\s+)?{re.escape(spelling)}\s*$"
            if not re.search(pattern, map_text, re.MULTILINE):
                raise ValueError(f"link-map public moved: {spelling}")
            result = compare_extent(target, candidate, config["segment"] * 16 + function["offset"], function["size"])
            functions.append({"name": function["name"], "abi": function["abi"], **result})
        modules = [{"id": m["id"], **compare_extent(target, candidate, config["segment"] * 16 + m["start"], m["size"])}
                   for m in config["units"]]
        probe = prefix / "drive_c" / f"{stem}{number}"
        probe.mkdir(exist_ok=False)
        shutil.copy2(snapshot / "probes/main/input_math_behavior.cpp", probe / "behavior.cpp")
        for module in config["units"]:
            shutil.copy2(snapshot / module["header"], probe / Path(module["header"]).name)
            shutil.copy2(work / f"obj/th03/{module['object']}.obj", probe / f"{module['object']}.obj")
        behavior_compile = execute(dos + ["tcc", *FLAGS, "-n.", "behavior.cpp"], probe, env, logs / "behavior-compile.log")
        (probe / "probe.rsp").write_bytes(b"-c c0l.obj behavior.obj polar.obj inp_m_w.obj, probe.exe, probe.map, emu.lib mathl.lib cl.lib\r\n")
        behavior_link = execute(dos + ["tlink", "@probe.rsp"], probe, env, logs / "behavior-link.log")
        behavior_run = execute(dos + ["probe.exe"], probe, env, logs / "behavior-run.log")
        if b"TH03 input/math behavior PASS" not in (logs / "behavior-run.log").read_bytes():
            raise ValueError("behavior probe did not report PASS")
        shutil.copyfile(work / "bin/th03/main.exe", logs / "main.exe")
        shutil.copyfile(work / "obj/th03/main.map", logs / "main.map")
        report["rounds"].append({"round": number, "fresh_owned_objects": True,
            "commands": [compile_result, behavior_compile, behavior_link, behavior_run],
            "objects": objects, "all_objects": all_objects, "game_objects": game_objects,
            "products": products,
            "map_contributions": contributions, "functions": functions, "units": modules,
            "link_response_sha256": sha((work / "obj/th03/main.@l").read_bytes()),
            "candidate_sha256": sha(candidate), "behavior_pass": True})
    first, second = report["rounds"]
    report["objects_metadata_normalized_equal"] = all(
        first["objects"][name]["dependency_timestamp_normalized_sha256"] ==
        second["objects"][name]["dependency_timestamp_normalized_sha256"] for name in objects)
    report["candidate_equal"] = first["candidate_sha256"] == second["candidate_sha256"]
    report["all_products_equal"] = first["products"] == second["products"]
    report["all_objects_metadata_normalized_equal"] = first["all_objects"] == second["all_objects"]
    report["game_objects_metadata_normalized_equal"] = first["game_objects"] == second["game_objects"]
    report["diagnostic_object_drift"] = sorted(name for name, digest in first["all_objects"].items()
                                              if digest != second["all_objects"].get(name))
    report["full_function_bytes"] = sum(f["size"] for f in config["functions"])
    report["pass"] = (report["objects_metadata_normalized_equal"] and report["candidate_equal"]
                      and report["all_products_equal"] and report["game_objects_metadata_normalized_equal"]
                      and all(f["raw_equal"] and f["relocations_equal"] for r in report["rounds"]
                              for f in r["functions"] + r["units"]))
    # Guard against source and target mutation during the replay.
    if any(sha((ROOT / name).read_bytes()) != digest for name, digest in inputs.items()):
        raise ValueError("source changed during replay")
    if read_verified_artifact(ROOT, artifact) != target:
        raise ValueError("target changed during replay")
    report["observed_utc"] = datetime.now(timezone.utc).isoformat()
    (output / "receipt.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default=datetime.now(timezone.utc).strftime("exact-%Y%m%dT%H%M%S"))
    parser.add_argument("--unit", action="append", default=[])
    args = parser.parse_args()
    try:
        report = replay(args.run_id, args.unit)
        print(f"th03-main-exact: {'PASS' if report['pass'] else 'FAIL'}; 10 functions, "
              f"{report['full_function_bytes']} bytes; two fresh compilations/links and DOS behavior probes")
        print(f"receipt: .analysis/th03-main-exact/{args.run_id}/receipt.json")
        return 0 if report["pass"] else 1
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f"th03-main-exact: FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
