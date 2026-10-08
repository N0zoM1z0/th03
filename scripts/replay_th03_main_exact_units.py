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

import capstone

from lib.omf import describe_omf, normalize_dependency_timestamps
from lib.tc4_omf_bridge import reframe_ellen_tc4_fixupp, validate_ellen_omf_recipe
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / "_reference/ReC98"
FLAGS = ["-c", "-I.", "-O", "-b-", "-3", "-Z", "-d", "-DGAME=3", "-ml"]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def physical_objects(unit: dict) -> list[dict]:
    """Return the physical OMF producers backing one semantic source owner."""
    declared = unit.get("physical_objects")
    if declared is None:
        item = {
            "object": unit["object"],
            "object_path": unit.get("object_path", f"obj/th03/{unit['object']}.obj"),
            "wrapper": unit.get("wrapper", f"th03/{unit['object']}.cpp"),
            "wrapper_prefix": "",
            "translator_comment": unit.get("translator_comment", "TC86 Borland C++ 4.02"),
        }
        if "source" in unit:
            item["source"] = unit["source"]
        return [item]
    if not declared or "overlay_path" in unit:
        raise ValueError(f"invalid physical object split: {unit['id']}")
    result = []
    names = set()
    paths = set()
    for raw in declared:
        item = dict(raw)
        name = item.get("object")
        if not name or name in names:
            raise ValueError(f"duplicate physical object: {unit['id']}")
        item.setdefault("object_path", f"obj/th03/{name}.obj")
        item.setdefault("wrapper", f"th03/{name}.cpp")
        item.setdefault("wrapper_prefix", "")
        if "source" in unit:
            item.setdefault("source", unit["source"])
        item.setdefault(
            "translator_comment", unit.get("translator_comment", "TC86 Borland C++ 4.02")
        )
        if (
            item["object_path"] in paths
            or not isinstance(item["wrapper_prefix"], str)
            or ("source" in item and (
                not isinstance(item["source"], str) or not item["source"]
            ))
        ):
            raise ValueError(f"invalid physical object declaration: {unit['id']}")
        names.add(name)
        paths.add(item["object_path"])
        result.append(item)
    return result


def ordering_objects(unit: dict) -> list[dict]:
    """Return zero-owned-byte OMF scaffolds used only to preserve link order."""
    declared = unit.get("ordering_objects", [])
    if not isinstance(declared, list):
        raise ValueError(f"invalid ordering object list: {unit['id']}")
    result = []
    names = {item["object"] for item in physical_objects(unit)}
    paths = {item["object_path"] for item in physical_objects(unit)}
    overlays = set()
    for raw in declared:
        if not isinstance(raw, dict):
            raise ValueError(f"invalid ordering object declaration: {unit['id']}")
        allowed = {"object", "source", "overlay_path", "object_path", "translator_comment"}
        if set(raw) - allowed or not {"object", "source", "overlay_path"} <= set(raw):
            raise ValueError(f"invalid ordering object declaration: {unit['id']}")
        item = dict(raw)
        name = item["object"]
        item.setdefault("object_path", f"obj/th03/{name}.obj")
        item.setdefault("translator_comment", "Turbo Assembler  Version 5.0")
        if (
            not isinstance(name, str) or not name
            or name in names
            or not isinstance(item["source"], str) or not item["source"]
            or not isinstance(item["overlay_path"], str) or not item["overlay_path"]
            or item["object_path"] in paths
            or item["overlay_path"] in overlays
        ):
            raise ValueError(f"invalid ordering object declaration: {unit['id']}")
        names.add(name)
        paths.add(item["object_path"])
        overlays.add(item["overlay_path"])
        result.append(item)
    return result


def physical_object_for(unit: dict, name: str) -> dict:
    matches = [item for item in physical_objects(unit) if item["object"] == name]
    if len(matches) != 1:
        raise ValueError(f"unknown physical object {name}: {unit['id']}")
    return matches[0]


def unit_source_paths(unit: dict) -> list[str]:
    """Return every repository source/support input required by one owner."""
    names = [unit["source"], unit["header"], *unit.get("support_files", [])]
    names.extend(
        producer["source"]
        for producer in physical_objects(unit)
        if producer.get("source")
    )
    names.extend(item["source"] for item in ordering_objects(unit))
    return list(dict.fromkeys(names))


def physical_object_count_delta(unit: dict) -> int:
    """Count generated producer/scaffold objects added by one owner model."""
    ordering_count = len(ordering_objects(unit))
    if "physical_objects" not in unit:
        return ordering_count
    count = len(physical_objects(unit))
    additive = unit.get("physical_objects_additive", False)
    if not isinstance(additive, bool):
        raise ValueError(f"invalid physical object count mode: {unit['id']}")
    return (count if additive else count - 1) + ordering_count

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


def normalized_code_extents(unit: dict, default_segment: int) -> list[dict]:
    """Return one or more discontiguous CODE contributions for one source owner."""
    raw_extents = unit.get("code_extents")
    if raw_extents is None:
        raw_extents = [{
            "name": "code",
            "ledger_id": unit["id"],
            "segment": unit.get("segment", default_segment),
            "start": unit["start"],
            "size": unit["size"],
            "map_size": unit.get("map_size", unit["size"]),
            "map_start": unit.get("map_start", unit["start"]),
            "map_module": unit.get(
                "map_module", unit.get("wrapper", f"th03/{unit['object']}.cpp")
            ),
            "map_acbp": unit.get("map_acbp", 28),
            "map_segment": unit.get("map_segment", "SHARED"),
            "map_group": unit.get("map_group", "(none)"),
            "producer_ranges": [
                {"relative": relative, "size": size, "kind": "padding"}
                for relative, size in unit.get("padding_ranges", [])
            ],
        }]
    elif "start" in unit or "size" in unit:
        raise ValueError(f"split owner also declares legacy start/size: {unit['id']}")

    result = []
    names = set()
    ledger_ids = set()
    for index, raw in enumerate(raw_extents):
        extent = dict(raw)
        extent.setdefault("name", f"code-{index + 1}")
        extent.setdefault("ledger_id", unit["id"])
        extent.setdefault("segment", unit.get("segment", default_segment))
        extent.setdefault(
            "map_module",
            unit.get("map_module", unit.get("wrapper", f"th03/{unit['object']}.cpp")),
        )
        extent.setdefault("map_acbp", unit.get("map_acbp", 28))
        extent.setdefault("map_segment", unit.get("map_segment", "SHARED"))
        extent.setdefault("map_group", unit.get("map_group", "(none)"))
        extent.setdefault("map_size", extent["size"])
        extent.setdefault("map_start", extent["start"])
        extent.setdefault("producer_ranges", [])
        if extent["name"] in names or extent["ledger_id"] in ledger_ids:
            raise ValueError(f"duplicate split owner extent identity: {unit['id']}")
        names.add(extent["name"])
        ledger_ids.add(extent["ledger_id"])
        if extent["start"] < 0 or extent["size"] <= 0:
            raise ValueError(f"invalid CODE extent: {unit['id']}:{extent['name']}")

        raw_parts = extent.get("map_parts")
        if raw_parts is None:
            default_physical = physical_objects(unit)[0]
            extent["map_parts"] = [{
                "object": default_physical["object"],
                "start": extent["map_start"],
                "size": extent["map_size"],
                "map_module": extent["map_module"],
                "map_acbp": extent["map_acbp"],
                "map_segment": extent["map_segment"],
                "map_group": extent["map_group"],
            }]
            if not (0 <= extent["map_start"] <= extent["start"]
                    and extent["start"] + extent["size"]
                    <= extent["map_start"] + extent["map_size"]):
                raise ValueError(f"CODE extent escapes MAP contribution: {unit['id']}")
        else:
            if unit.get("ownership") == "bounded-include" or not raw_parts:
                raise ValueError(f"invalid multi-contribution owner: {unit['id']}")
            parts = []
            for raw_part in raw_parts:
                part = dict(raw_part)
                producer = physical_object_for(unit, part["object"])
                part.setdefault("map_module", producer["wrapper"])
                part.setdefault("map_acbp", extent["map_acbp"])
                part.setdefault("map_segment", extent["map_segment"])
                part.setdefault("map_group", extent["map_group"])
                if part["start"] < 0 or part["size"] <= 0:
                    raise ValueError(f"invalid MAP part: {unit['id']}:{extent['name']}")
                parts.append(part)
            parts.sort(key=lambda part: part["start"])
            cursor = extent["start"]
            for part in parts:
                if part["start"] != cursor:
                    raise ValueError(
                        f"MAP parts do not exactly cover owner: {unit['id']}:{extent['name']}"
                    )
                cursor += part["size"]
            if cursor != extent["start"] + extent["size"]:
                raise ValueError(
                    f"MAP parts do not exactly cover owner: {unit['id']}:{extent['name']}"
                )
            extent["map_parts"] = parts

        if unit.get("ownership") == "bounded-include":
            if (Path(unit["source"]).suffix != ".inl"
                or not all(unit.get(key) for key in
                           ("carrier_path", "carrier_sha256", "overlay_path", "object_path"))):
                raise ValueError(f"invalid bounded include: {unit['id']}")
        elif unit.get("ownership") == "carved-producers":
            if (
                not all(unit.get(key) for key in ("carrier_path", "carrier_sha256"))
                or "overlay_path" in unit
                or "physical_objects" not in unit
                or not unit.get("carrier_edits")
                or not unit.get("physical_objects_additive")
            ):
                raise ValueError(f"invalid carved producer owner: {unit['id']}")
        elif raw_parts is None and extent["map_start"] != extent["start"]:
            raise ValueError(f"interior CODE requires a bounded include: {unit['id']}")
        result.append(extent)
    return result


def apply_carrier_edits(unit: dict, work: Path) -> None:
    """Apply declarative, single-hit edits to a frozen reference carrier.

    These edits change source organization only. Exact credit remains limited
    to the declared owner extent, which is compared against the immutable target
    after linking.
    """
    for index, edit in enumerate(unit.get("carrier_edits", []), 1):
        allowed = {
            "replace-once": {"kind", "path", "before", "after"},
            "replace-exact-count": {"kind", "path", "before", "after", "count"},
            "remove-between": {
                "kind", "path", "start_marker", "end_marker", "replacement"
            },
        }
        kind = edit.get("kind")
        if kind not in allowed or set(edit) != allowed[kind]:
            raise ValueError(f"invalid carrier edit {unit['id']}:{index}")
        path = work / edit["path"]
        data = path.read_bytes()

        if kind in {"replace-once", "replace-exact-count"}:
            before = edit["before"].encode("ascii")
            after = edit["after"].encode("ascii")
            expected = 1 if kind == "replace-once" else edit["count"]
            if (
                not before
                or not isinstance(expected, int)
                or expected <= 0
                or data.count(before) != expected
            ):
                raise ValueError(
                    f"carrier replacement anchor drifted: {unit['id']}:{index}"
                )
            data = data.replace(before, after, expected)
        else:
            start_marker = edit["start_marker"].encode("ascii")
            end_marker = edit["end_marker"].encode("ascii")
            replacement = edit["replacement"].encode("ascii")
            if (not start_marker or not end_marker
                or data.count(start_marker) != 1 or data.count(end_marker) != 1):
                raise ValueError(
                    f"carrier removal anchor drifted: {unit['id']}:{index}"
                )
            start = data.index(start_marker)
            end = data.index(end_marker, start) + len(end_marker)
            if end <= start:
                raise ValueError(f"invalid carrier removal range: {unit['id']}:{index}")
            data = data[:start] + replacement + data[end:]

        path.write_bytes(data)


def verify_include_carrier(
    unit: dict, work: Path, *, require_include: bool = True, verify_hash: bool = True
) -> None:
    """Bind a maintained owner to a frozen generated carrier."""
    ownership = unit.get("ownership")
    if ownership not in {"bounded-include", "carved-producers"}:
        return
    child = unit.get("overlay_path")
    carriers = [{"path": unit["carrier_path"], "sha256": unit["carrier_sha256"]},
                *unit.get("parent_carriers", [])]
    seen = {child} if child else set()
    for declaration in carriers:
        path = declaration["path"]
        if path in seen:
            raise ValueError(f"bounded include carrier cycle: {unit['id']}")
        seen.add(path)
        carrier = work / path
        data = carrier.read_bytes()
        if verify_hash and sha(data) != declaration["sha256"]:
            raise ValueError(f"bounded include carrier drifted: {unit['id']}")
        if ownership == "bounded-include" and require_include:
            pattern = rf"^\s*include\s+{re.escape(child)}\s*$"
            text = data.decode("ascii", errors="surrogateescape")
            if len(re.findall(pattern, text, re.MULTILINE | re.IGNORECASE)) != 1:
                raise ValueError(f"bounded include must occur once in carrier: {unit['id']}")
        child = path
    if (
        ownership == "bounded-include"
        and child.replace("\\", "/") != unit["map_module"].replace("\\", "/")
    ):
        raise ValueError(f"bounded include chain does not reach MAP module: {unit['id']}")

def verify_disjoint_ownership(extents_by_owner: dict[str, list[dict]]) -> None:
    """Containing MAP ranges may overlap; credited CODE extents must not."""
    ranges = sorted((e["segment"], e["start"], e["start"] + e["size"], owner)
                    for owner, extents in extents_by_owner.items() for e in extents)
    for previous, current in zip(ranges, ranges[1:]):
        if previous[0] == current[0] and previous[2] > current[1]:
            raise ValueError(f"overlapping CODE ownership: {previous[3]} / {current[3]}")


def verify_private_calls(function: dict, functions: list[dict], payload: bytes,
                         default_segment: int) -> list[dict]:
    """Prove a private near entry through calls from complete owned callers."""
    if function.get("map_public") or not function.get("private_callers"):
        raise ValueError(f"private function requires call-based ownership: {function['name']}")
    segment = function.get("segment", default_segment)
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    decoder.detail = True
    result = []
    seen = set()
    for declaration in function["private_callers"]:
        name, expected = declaration["name"], declaration["count"]
        callers = [f for f in functions if f["name"] == name
                   and f["object"] == function["object"]
                   and f.get("segment", default_segment) == segment
                   and f.get("map_public")]
        if len(callers) != 1 or name in seen or expected <= 0:
            raise ValueError(f"invalid private caller declaration: {function['name']}")
        seen.add(name)
        caller = callers[0]
        start = segment * 16 + caller["offset"]
        instructions = list(decoder.disasm(payload[start:start + caller["size"]], caller["offset"]))
        if (sum(i.size for i in instructions) != caller["size"] or not instructions
            or instructions[-1].mnemonic not in {"ret", "retf"}):
            raise ValueError(f"incomplete private caller decode: {name}")
        sites = [i.address for i in instructions
                 if i.mnemonic == "call" and len(i.operands) == 1
                 and i.operands[0].type == capstone.x86.X86_OP_IMM
                 and i.operands[0].imm == function["offset"]]
        if len(sites) != expected:
            raise ValueError(f"private entry call count moved: {function['name']}")
        result.append({"caller": name, "direct_near_call_sites": sites})
    return result


def verify_owner_linear_span(
    function: dict, payload: bytes, default_segment: int
) -> dict:
    """Validate one function boundary inside a complete owned CODE extent.

    This mode is for monolithic assembly functions that were not PUBDEF/MAP
    publics in the original object. It does not invent symbol visibility:
    the declared span must decode linearly without gaps and end at a real
    near/far return in the immutable target and in every replayed candidate.
    """
    if function.get("map_public") or function.get("private_callers"):
        raise ValueError(
            f"owner-linear-span forbids public/private-call metadata: {function['name']}"
        )
    segment = function.get("segment", default_segment)
    start = segment * 16 + function["offset"]
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    instructions = list(
        decoder.disasm(payload[start:start + function["size"]], function["offset"])
    )
    if (
        not instructions
        or sum(instruction.size for instruction in instructions) != function["size"]
        or instructions[-1].address + instructions[-1].size
            != function["offset"] + function["size"]
        or instructions[-1].mnemonic not in {"ret", "retf"}
    ):
        raise ValueError(f"incomplete owner-linear function span: {function['name']}")
    return {
        "instruction_count": len(instructions),
        "last_instruction": instructions[-1].mnemonic,
        "last_instruction_address": instructions[-1].address,
    }


def add_candidate_owners(config: dict, candidate: dict) -> dict:
    """Add reviewed candidates without replacing acceptance inputs or owners."""
    if set(candidate) != {"schema_version", "units", "functions"} or candidate["schema_version"] != 1:
        raise ValueError("candidate manifest may only add units and functions")
    for key, identity in (("units", "id"), ("units", "object"), ("functions", "name")):
        existing = {item[identity] for item in config[key]}
        additions = [item[identity] for item in candidate[key]]
        if len(set(additions)) != len(additions) or existing.intersection(additions):
            raise ValueError(f"candidate repeats existing {key} {identity}")
    return {**config, "units": config["units"] + candidate["units"],
            "functions": config["functions"] + candidate["functions"]}


def replay(run_id: str, selected_units: list[str], candidate_manifest: Path | None = None) -> dict:
    config = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    if candidate_manifest is not None:
        candidate_manifest = candidate_manifest.resolve()
        if not candidate_manifest.is_relative_to(ROOT / "config"):
            raise ValueError("candidate manifest must be inside repository config/")
        config = add_candidate_owners(config, tomllib.loads(candidate_manifest.read_text()))
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
    extents_by_owner = {
        unit["id"]: normalized_code_extents(unit, config["segment"])
        for unit in config["units"]
    }
    verify_disjoint_ownership(extents_by_owner)
    extent_count = sum(len(extents) for extents in extents_by_owner.values())
    ledger_ids = {
        extent["ledger_id"]
        for extents in extents_by_owner.values()
        for extent in extents
    }
    if len(ledger_ids) != extent_count:
        raise ValueError("duplicate ledger identity across CODE extents")
    with (ROOT / "config/units.csv").open(newline="") as stream:
        unit_rows = list(csv.DictReader(stream))
    accepted = {row["id"] for row in unit_rows
                if row["artifact"] == config["artifact"] and row["state"] == "exact"}
    if accepted - ledger_ids:
        raise ValueError("aggregate omits an accepted owner extent")
    image = parse_mz(target)

    # Every owned CODE byte must be classified exactly once as a reviewed
    # function body or as an explicit producer-owned non-function range.
    # Split owners such as th03/bullet.cpp may contribute multiple CODE
    # segments without claiming the unrelated bytes between them.
    for unit in config["units"]:
        extents = extents_by_owner[unit["id"]]
        coverage = {
            extent["name"]: [None] * extent["size"]
            for extent in extents
        }
        for function in config["functions"]:
            if function["object"] != unit["object"]:
                continue
            function_segment = function.get("segment", config["segment"])
            matches = [
                extent for extent in extents
                if extent["segment"] == function_segment
                and extent["start"] <= function["offset"]
                and function["offset"] + function["size"]
                    <= extent["start"] + extent["size"]
            ]
            if len(matches) != 1:
                raise ValueError(f"function does not map to exactly one owner extent: {function['name']}")
            extent = matches[0]
            relative = function["offset"] - extent["start"]
            for index in range(relative, relative + function["size"]):
                if coverage[extent["name"]][index] is not None:
                    raise ValueError(f"overlapping owner coverage: {unit['id']}")
                coverage[extent["name"]][index] = f"function:{function['name']}"
        for extent in extents:
            for producer_range in extent["producer_ranges"]:
                relative = producer_range["relative"]
                size = producer_range["size"]
                kind = producer_range["kind"]
                if relative < 0 or size <= 0 or relative + size > extent["size"]:
                    raise ValueError(
                        f"invalid producer range: {unit['id']}:{extent['name']}:{kind}"
                    )
                for index in range(relative, relative + size):
                    if coverage[extent["name"]][index] is not None:
                        raise ValueError(
                            f"producer range overlaps reviewed bytes: {unit['id']}"
                        )
                    coverage[extent["name"]][index] = f"producer:{kind}"
            holes = [
                index for index, owner in enumerate(coverage[extent["name"]])
                if owner is None
            ]
            if holes:
                raise ValueError(
                    f"unclassified owner bytes in {unit['id']}:{extent['name']}: "
                    f"{holes[:8]}"
                )

    for unit in config["units"]:
        for extent in extents_by_owner[unit["id"]]:
            rows = [row for row in unit_rows if row["id"] == extent["ledger_id"]]
            if len(rows) != 1:
                raise ValueError(
                    f"ledger row missing or duplicated: {unit['id']}:{extent['name']}"
                )
            row = rows[0]
            expected_offset = (
                extent["segment"] * 16 + extent["start"] + image.header.header_size
            )
            if (row["artifact"] != config["artifact"] or row["source"] != unit["source"]
                or int(row["file_offset"], 0) != expected_offset
                or int(row["size"], 0) != extent["size"]
                or int(row["compare_size"], 0) != extent["size"]):
                raise ValueError(
                    f"ledger/manifest owner mismatch: {unit['id']}:{extent['name']}"
                )
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
        for name in unit_source_paths(module):
            path = ROOT / name
            inputs[name] = sha(path.read_bytes())
    inputs["probes/main/input_math_behavior.cpp"] = sha((ROOT / "probes/main/input_math_behavior.cpp").read_bytes())
    inputs["config/th03_main_exact_units.toml"] = sha((ROOT / "config/th03_main_exact_units.toml").read_bytes())
    inputs["scripts/replay_th03_main_exact_units.py"] = sha(Path(__file__).read_bytes())
    if candidate_manifest is not None:
        name = candidate_manifest.relative_to(ROOT).as_posix()
        inputs[name] = sha(candidate_manifest.read_bytes())
    # Freeze every ledger/control input consulted by the pre-replay acceptance
    # checks. Otherwise an exact-state or evidence edit during a long cold build
    # could escape the end-of-replay mutation guard.
    for name in (
        "config/targets.toml",
        "config/toolchain.toml",
        "config/oracles.toml",
        "config/units.csv",
        "config/evidence.csv",
        "config/th03_main_authored_functions.csv",
        "config/th03_function_boundaries.csv",
        "docs/PROGRESS.md",
        "resources/progress.svg",
        "scripts/attest_toolchain.py",
        "scripts/validate_tracking.py",
        "scripts/progress.py",
        "tests/test_main_exact_oracle.py",
    ):
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
    report["candidate_manifest"] = (
        candidate_manifest.relative_to(ROOT).as_posix() if candidate_manifest else None
    )
    stem = "P" + sha(run_id.encode())[:5].upper()
    for number in (1, 2):
        logs = output / f"round{number}"
        logs.mkdir()
        work = logs / "source"
        work.mkdir()
        subprocess.run(["tar", "-xf", str(archive), "-C", str(work)], check=True)
        if list(work.rglob("*.obj")) or list((work / "bin").glob("th0[1-5]/*.exe")):
            raise ValueError("cold scaffold contains cached game objects or products")
        # Freeze-check every shared carrier before any owner is allowed to
        # reorganize it. A carved owner gains its include only in the next
        # phase, and then its include chain is checked without reusing the old
        # whole-carrier digest.
        for module in config["units"]:
            verify_include_carrier(
                module, work, require_include=not bool(module.get("carrier_edits"))
            )
        for module in config["units"]:
            apply_carrier_edits(module, work)
        for module in config["units"]:
            if module.get("carrier_edits"):
                verify_include_carrier(module, work, verify_hash=False)

        for module in config["units"]:
            for name in unit_source_paths(module):
                destination = work / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(snapshot / name, destination)
            if "overlay_path" in module:
                overlay = work / module["overlay_path"]
                overlay.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(snapshot / module["source"], overlay)
            else:
                for producer in physical_objects(module):
                    wrapper = work / producer["wrapper"]
                    wrapper.parent.mkdir(parents=True, exist_ok=True)
                    wrapper.write_text(
                        producer["wrapper_prefix"] + f'#include "{producer["source"]}"\n'
                    )
        for module in config["units"]:
            for ordering in ordering_objects(module):
                overlay = work / ordering["overlay_path"]
                overlay.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(snapshot / ordering["source"], overlay)
        for module in config["units"]:
            if "build_file" not in module:
                continue
            build_path = work / module["build_file"]
            build_text = build_path.read_text()
            anchor = module["build_anchor"]
            replacement = module["build_replacement"]
            if build_text.count(anchor) != 1:
                raise ValueError(f"build replacement anchor drifted: {module['id']}")
            build_path.write_text(build_text.replace(anchor, replacement, 1))
        # Calibrate only the observed TC4 Ellen OMF LEDATA/FIXUPP record
        # boundary at CODE offset 1000. The emitted CODE section, symbol
        # targets, fixup *set*, and every raw-byte/MZ-order oracle remain
        # immutable. A precompiled object is supplied as an explicit .obj
        # input to the maintained build graph; Tup must not overwrite it.
        reframed_omf_objects = []
        for module in config["units"]:
            for producer in physical_objects(module):
                if "tc4_omf_reframe" not in producer:
                    continue
                wrapper = validate_ellen_omf_recipe(producer)
                output_obj = work / producer["object_path"]
                output_obj.parent.mkdir(parents=True, exist_ok=True)
                if output_obj.exists():
                    raise ValueError("TC4 OMF record calibration would reuse a stale object")
                command = [
                    "wine", "cmd", "/d", "/c",
                    (r"set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%"
                     r"&&bin\msdos -e -x tcc -c -I. -O -b- -3 -Z -d"
                     r" -DGAME=3 -ml -a2 -nobj/th03/ "
                     + wrapper.replace("/", "\\"))
                ]
                tc4 = execute(command, work, env,
                              logs / f"{producer['object']}-direct-tc4.log")
                original_omf = output_obj.read_bytes()
                before = describe_omf(original_omf)
                if (
                    not before["valid"]
                    or "TC86 Borland C++ 4.02" not in before["translator_comments"]
                ):
                    raise ValueError("unexpected compiler for Ellen original OMF record")
                calibrated = reframe_ellen_tc4_fixupp(original_omf)
                output_obj.write_bytes(calibrated)
                after = describe_omf(output_obj.read_bytes())
                if not after["valid"] or after["translator_comments"] != before["translator_comments"]:
                    raise ValueError("calibrated OMF identity was modified")
                reframed_omf_objects.append({
                    "owner": module["id"], "object": producer["object"],
                    "semantic_source": producer["source"],
                    "unmodified_tc4_omf_sha256": sha(original_omf),
                    "record_framed_omf_sha256": sha(calibrated),
                    "raw_module_bytes_unchanged": False,
                    "code_and_symbol_target_edits": 0,
                    "record_framing": "two LEDATA/FIXUPP pairs split at CODE offset 1000",
                    "TC4_compile_command": tc4,
                })
        build_command = ["wine", "cmd", "/d", "/c",
                         r"set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%"
                         r"&&set PROCESSOR_ARCHITECTURE=AMD64"
                         r"&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat"]
        compile_result = execute(build_command, work, env, logs / "cold-build.log")
        objects = {}
        for module in config["units"]:
            for producer in [*physical_objects(module), *ordering_objects(module)]:
                if producer["object"] in objects:
                    continue
                objects[producer["object"]] = describe_omf(
                    (work / producer["object_path"]).read_bytes()
                )
        all_objects = {p.relative_to(work).as_posix(): sha(normalize_dependency_timestamps(p.read_bytes()))
                       for p in sorted((work / "obj").rglob("*.obj"))}
        products = {}
        for target_artifact in load_target_manifest(ROOT / "config/targets.toml")["artifacts"]:
            relative = Path("bin") / target_artifact["game"] / Path(target_artifact["private_path"]).name
            products[relative.as_posix()] = sha((work / relative).read_bytes())
        game_objects = {name: digest for name, digest in all_objects.items()
                        if any(name.startswith(directory + "/") for directory in config["determinism_object_roots"])}
        object_count_delta = sum(
            physical_object_count_delta(module) for module in config["units"]
        )
        if (len(products) != 20
            or len(all_objects) != config["generated_object_count"] + object_count_delta
            or len(game_objects) != config["determinism_object_count"] + object_count_delta):
            raise ValueError("cold build output/object vector incomplete")
        for module in config["units"]:
            for producer in [*physical_objects(module), *ordering_objects(module)]:
                obj = objects[producer["object"]]
                if producer["translator_comment"] not in obj["translator_comments"]:
                    raise ValueError(f"owned/scaffold object producer differs: {module['id']}")
        candidate = (work / "bin/th03/main.exe").read_bytes()
        # Confirm link-map publics cover exactly the reviewed starts and ends.
        map_text = (work / "obj/th03/main.map").read_text(errors="replace")
        contributions = []
        for unit in config["units"]:
            for extent in extents_by_owner[unit["id"]]:
                for part_index, part in enumerate(extent["map_parts"], 1):
                    pattern = (
                        rf"^\s*{extent['segment']:04X}:{part['start']:04X}"
                        rf"\s+{part['size']:04X}"
                        rf"\s+C=CODE\s+S={re.escape(part['map_segment'])}"
                        rf"\s+G={re.escape(part['map_group'])}"
                        rf"\s+M={re.escape(part['map_module'])}"
                        rf"\s+ACBP={part['map_acbp']}\s*$"
                    )
                    found = re.findall(pattern, map_text, re.MULTILINE)
                    if len(found) != 1:
                        raise ValueError(
                            f"map ownership, size, segment or alignment moved: "
                            f"{unit['id']}:{extent['name']}:part-{part_index}"
                        )
                    producer = physical_object_for(unit, part["object"])
                    contributions.append({
                        "id": unit["id"],
                        "extent": extent["name"],
                        "part": part_index,
                        "ledger_id": extent["ledger_id"],
                        "ownership": unit.get("ownership", "translation-unit"),
                        "object": producer["object"],
                        "object_path": producer["object_path"],
                        "owned_start": part["start"],
                        "owned_size": part["size"],
                        "map": found[0].strip(),
                    })
        auxiliary_contributions = []
        for unit in config["units"]:
            for aux in unit.get("aux_map", []):
                map_module = aux.get("map_module", unit.get(
                    "map_module", unit.get("wrapper", f"th03/{unit['object']}.cpp")
                ))
                map_acbp = aux.get("map_acbp", 48)
                pattern = (
                    rf"^\s*{aux['segment']:04X}:{aux['start']:04X}\s+{aux['size']:04X}"
                    rf"\s+C={re.escape(aux['class'])}\s+S={re.escape(aux['map_segment'])}"
                    rf"\s+G={re.escape(aux['map_group'])}\s+M={re.escape(map_module)}"
                    rf"\s+ACBP={map_acbp}\s*$"
                )
                found = re.findall(pattern, map_text, re.MULTILINE)
                if len(found) != 1:
                    raise ValueError(
                        f"auxiliary MAP contribution moved: {unit['id']} "
                        f"{aux['class']}:{aux['start']:04X}"
                    )
                item = {
                    "id": unit["id"], "class": aux["class"],
                    "map": found[0].strip(), "raw_compare": aux.get("raw_compare", False),
                }
                if item["raw_compare"]:
                    item.update(compare_extent(
                        target, candidate,
                        aux["segment"] * 16 + aux["start"], aux["size"]
                    ))
                auxiliary_contributions.append(item)
        functions = []
        for function in config["functions"]:
            private_calls = None
            spelling = function.get("map_public") or (
                "polar(int,int,int)" if function["name"] == "polar" else
                function["name"] + (
                    "(int)" if function["name"] == "input_wait_for_change" else "()"
                )
            )
            function_segment = function.get("segment", config["segment"])
            pattern = rf"^\s*{function_segment:04X}:{function['offset']:04X}\s+(?:idle\s+)?{re.escape(spelling)}\s*$"
            span_check = None
            if function.get("boundary") == "private-near-calls":
                private_calls = verify_private_calls(
                    function, config["functions"], parse_mz(candidate).program_image, config["segment"]
                )
                if private_calls != verify_private_calls(
                    function, config["functions"], image.program_image, config["segment"]
                ):
                    raise ValueError(f"private call sites moved: {function['name']}")
            elif function.get("boundary") == "owner-linear-span":
                target_span = verify_owner_linear_span(
                    function, image.program_image, config["segment"]
                )
                span_check = verify_owner_linear_span(
                    function, parse_mz(candidate).program_image, config["segment"]
                )
                if span_check != target_span:
                    raise ValueError(f"owner-linear function span moved: {function['name']}")
            elif not re.search(pattern, map_text, re.MULTILINE):
                raise ValueError(f"link-map public moved: {spelling}")
            result = compare_extent(
                target, candidate,
                function_segment * 16 + function["offset"], function["size"]
            )
            functions.append({
                "name": function["name"], "abi": function["abi"],
                "private_calls": private_calls, "span_check": span_check, **result
            })
        modules = []
        producer_ranges = []
        padding = []
        for unit in config["units"]:
            for extent in extents_by_owner[unit["id"]]:
                modules.append({
                    "id": unit["id"],
                    "extent": extent["name"],
                    "ledger_id": extent["ledger_id"],
                    **compare_extent(
                        target, candidate,
                        extent["segment"] * 16 + extent["start"], extent["size"]
                    ),
                })
                for producer_range in extent["producer_ranges"]:
                    relative = producer_range["relative"]
                    size = producer_range["size"]
                    result = {
                        "id": unit["id"],
                        "extent": extent["name"],
                        "kind": producer_range["kind"],
                        "relative": relative,
                        **compare_extent(
                            target, candidate,
                            extent["segment"] * 16 + extent["start"] + relative,
                            size,
                        ),
                    }
                    producer_ranges.append(result)
                    if producer_range["kind"] == "padding":
                        padding.append(result)
        probe = prefix / "drive_c" / f"{stem}{number}"
        probe.mkdir(exist_ok=False)
        shutil.copy2(snapshot / "probes/main/input_math_behavior.cpp", probe / "behavior.cpp")
        for module in config["units"]:
            shutil.copy2(snapshot / module["header"], probe / Path(module["header"]).name)
            for producer in physical_objects(module):
                object_path = work / producer["object_path"]
                shutil.copy2(object_path, probe / f"{producer['object']}.obj")
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
            "tc4_reframed_omf": reframed_omf_objects,
            "objects": objects, "all_objects": all_objects, "game_objects": game_objects,
            "products": products,
            "map_contributions": contributions,
            "auxiliary_map_contributions": auxiliary_contributions,
            "functions": functions, "units": modules,
            "producer_ranges": producer_ranges,
            "padding_ranges": padding,
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
    report["declared_producer_bytes"] = sum(
        producer_range["size"]
        for unit in config["units"]
        for extent in extents_by_owner[unit["id"]]
        for producer_range in extent["producer_ranges"]
    )
    report["declared_padding_bytes"] = sum(
        producer_range["size"]
        for unit in config["units"]
        for extent in extents_by_owner[unit["id"]]
        for producer_range in extent["producer_ranges"]
        if producer_range["kind"] == "padding"
    )
    report["owned_extent_bytes"] = sum(
        extent["size"]
        for unit in config["units"]
        for extent in extents_by_owner[unit["id"]]
    )
    report["pass"] = (report["objects_metadata_normalized_equal"] and report["candidate_equal"]
                      and report["all_products_equal"] and report["game_objects_metadata_normalized_equal"]
                      and all(f["raw_equal"] and f["relocations_equal"] for r in report["rounds"]
                              for f in r["functions"] + r["units"] + r["producer_ranges"])
                      and all(
                          (not aux["raw_compare"]) or (
                              aux["raw_equal"] and aux["relocations_equal"]
                          )
                          for r in report["rounds"]
                          for aux in r["auxiliary_map_contributions"]
                      ))
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
    parser.add_argument("--candidate-manifest", type=Path,
                        help="add candidates to the complete accepted-owner replay; gates stay unchanged")
    args = parser.parse_args()
    try:
        report = replay(args.run_id, args.unit, args.candidate_manifest)
        print(
            f"th03-main-exact: {'PASS' if report['pass'] else 'FAIL'}; "
            f"{len(report['rounds'][0]['functions'])} functions, "
            f"{report['full_function_bytes']} function bytes / "
            f"{report['owned_extent_bytes']} owned bytes "
            f"(including {report['declared_producer_bytes']} producer-owned "
            f"non-function bytes, {report['declared_padding_bytes']} padding); "
            "two fresh compilations/links and DOS behavior probes"
        )
        print(f"receipt: .analysis/th03-main-exact/{args.run_id}/receipt.json")
        return 0 if report["pass"] else 1
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f"th03-main-exact: FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
