#!/usr/bin/env python3
"""Review native character and lose CODE owners against a fresh MAIN cold pair."""

from pathlib import Path
import csv
import hashlib
import json
import re
import subprocess
import sys
import tomllib
import capstone

from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from lib.toolchain import tree_identity
from lib.main_work_stage import recipe_hashes
from probe_th03_main_bomb_rikako_cpp import segment_definitions
from probe_th03_main_boss_marisa_cpp import code_publics
from replay_th03_main_exact_units import verify_owner_linear_span
import build_th03_main_work as build

ROOT = Path(__file__).resolve().parents[1]
OWNERS = {"th03-main-exatt-chiyuri", "th03-main-exatt-ellen"}
LOSE_OWNERS = {
    "th03-main-player-lose-update-particle",
    "th03-main-player-defeat-banner",
}


CORE_OWNERS = {"th03-main-round-finish"}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(value, message):
    if not value:
        raise ValueError(message)


def verify_maintained_sources(staged):
    """A current source claim cannot borrow a build of older maintained files."""
    from stage_th03_main_shotroot import transform_score

    checked = 0
    for name, expected in staged.items():
        path = ROOT / name
        need(
            not name.startswith(("src/", "compat/")) or path.is_file(),
            "maintained source missing: " + name,
        )
        if not path.is_file():
            continue
        raw = path.read_bytes()
        if name == "src/main/hud/score.asm":
            raw = transform_score(raw)
        need(sha(raw) == expected, "maintained source drift: " + name)
        checked += 1
    return checked


def review(report=None):
    report_path = ROOT / ".analysis/work/main-build.json"
    report = json.loads(report_path.read_text()) if report is None else report
    need(
        report.get("complete")
        and report.get("cold_build")
        and report.get("source_tree_recreated"),
        "two cold source materializations are required",
    )
    expected = set(build.linked_objects()) - {"c0l.obj"}
    expected.update({"bin/th03/main.exe", "obj/th03/main.map"})
    pair = report.get("cold_reproducibility", {})
    need(
        pair.get("complete")
        and pair.get("independent_source_trees")
        and pair.get("same_source_inputs"),
        "two cold source materializations are required",
    )
    need(
        set(pair.get("raw_output_repeat", {})) == expected
        and all(pair["raw_output_repeat"].values()),
        "complete cold output vector required",
    )
    need(
        report["builder_sha256"]
        == sha((ROOT / "scripts/build_th03_main_work.py").read_bytes())
        and report["recipe_sha256"] == recipe_hashes(),
        "source recipe changed after cold replay",
    )
    need(
        report["native_outputs_unchanged"]
        and report["staged_sources_unchanged"]
        and len(report["native_phases"]) == len(expected) - 1
        and all(p["exit_code"] == 0 for p in report["native_phases"]),
        "native cold lifecycle failed",
    )
    outputs = {
        n: h for p in report["native_phases"] for n, h in p["output_sha256"].items()
    }
    need(
        set(outputs) == expected == set(pair["raw_output_repeat"]),
        "complete cold output inventory differs",
    )
    need(
        all(sha((build.WORK / n).read_bytes()) == h for n, h in outputs.items()),
        "native output drift",
    )
    need(
        all(
            sha((build.WORK / n).read_bytes()) == h
            for n, h in report["staged_source_sha256"].items()
        ),
        "staged source drift",
    )
    maintained_inputs = verify_maintained_sources(report["staged_source_sha256"])
    need(
        all(
            sha((ROOT / n).read_bytes()) == h for n, h in report["tools_sha256"].items()
        ),
        "native tool drift",
    )

    tool_config = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    attestation = json.loads(
        (ROOT / ".analysis/toolchain/attestation.json").read_text()
    )
    need(
        attestation["ready"]
        and attestation["manifest_sha256"]
        == sha((ROOT / "config/toolchain.toml").read_bytes())
        and all(s["pass"] or not s["required"] for s in attestation["surfaces"]),
        "toolchain identity failed",
    )
    prefix = ROOT / tool_config["paths"]["wine_prefix"] / "drive_c/TC4"
    for surface_id, folder in (("tc40j-include", "INCLUDE"), ("tc40j-lib", "LIB")):
        surface = next(s for s in tool_config["surfaces"] if s["id"] == surface_id)
        need(
            tree_identity(prefix / folder).sha256 == surface["sha256"],
            "active compiler input tree differs: " + folder,
        )

    omf = {}
    for name in outputs:
        if name.endswith(".obj"):
            obj = describe_omf((build.WORK / name).read_bytes())
            need(
                obj["valid"]
                and obj["record_counts"].get("THEADR") == 1
                and obj["record_counts"].get("MODEND") == 1,
                "invalid native OMF: " + name,
            )
            omf[name] = obj
    need(len(omf) == len(expected) - 2, "complete fresh game object set required")
    artifact = find_artifact(
        load_target_manifest(ROOT / "config/targets.toml"), "th03-main"
    )
    target_raw = read_verified_artifact(ROOT, artifact)
    candidate_raw = (build.WORK / "bin/th03/main.exe").read_bytes()
    target, candidate = parse_mz(target_raw), parse_mz(candidate_raw)
    need(target.valid and candidate.valid, "MZ format integrity failed")
    config = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    native_units = config.get("native_units", [])
    need(
        {u["id"] for u in native_units} == LOSE_OWNERS | CORE_OWNERS,
        "lose owners are incomplete",
    )
    units = config["units"] + native_units
    comparison = build.review()
    need(comparison["all_owned_raw_and_ordered_equal"], "accepted cohort regressed")
    with (ROOT / "config/units.csv").open() as stream:
        ledgers = {r["id"]: r for r in csv.DictReader(stream)}
    covered = {
        e.get("ledger_id", u["id"]) for u in units for e in u.get("code_extents", [u])
    }
    need(
        {
            r["id"]
            for r in ledgers.values()
            if r["artifact"] == "th03-main" and r["state"] == "exact"
        }
        <= covered,
        "accepted owner missing from cold replay",
    )
    subprocess.run(
        [sys.executable, "scripts/validate_tracking.py"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    required = set(
        tomllib.loads((ROOT / "config/oracles.toml").read_text())["policy"][
            "exact_requires"
        ]
    )
    result = dict(
        cold_report_sha256=sha(report_path.read_bytes()),
        auditor_sha256=sha(Path(__file__).read_bytes()),
        target_sha256=sha(target_raw),
        executable_sha256=sha(candidate_raw),
        raw_cold_outputs=len(outputs),
        valid_native_objects=len(omf),
        maintained_inputs_checked=maintained_inputs,
        replayed_owned_extents=comparison["checked_owned_extents"],
        replayed_owned_bytes=comparison["checked_owned_bytes"],
        units={},
        product_exact=False,
    )
    map_text = (build.WORK / "obj/th03/main.map").read_text()
    from lib.main_lose_runtime import compare, negative_controls

    runtime = compare(target, candidate)
    controls = negative_controls(candidate)
    need(
        runtime["equal"]
        and runtime["code_bytes_executed"] == 487
        and controls["count"] == 4,
        "lose runtime contracts failed",
    )
    result["lose_runtime"] = runtime
    result["lose_negative_controls"] = controls
    result["runtime_model_sha256"] = sha(
        (ROOT / "scripts/lib/main_lose_runtime.py").read_bytes()
    )
    from lib.main_round_finish_runtime import (
        compare as round_compare,
        negative_controls as round_controls,
    )

    result["round_finish_runtime"] = round_compare(target, candidate)
    result["round_finish_controls"] = round_controls(candidate)
    result["round_finish_model_sha256"] = sha(
        (ROOT / "scripts/lib/main_round_finish_runtime.py").read_bytes()
    )
    for unit in (u for u in units if u["id"] in OWNERS | LOSE_OWNERS | CORE_OWNERS):
        (extent,) = unit["code_extents"]
        row = ledgers[unit["id"]]
        lo = extent["segment"] * 16 + extent["start"]
        hi = lo + extent["size"]
        need(
            row["boundary_state"] == "reviewed"
            and row["origin"] == "authored"
            and row["source"] == unit["source"]
            and int(row["file_offset"], 0) == target.header.header_size + lo
            and int(row["size"], 0) == extent["size"] == int(row["compare_size"], 0),
            "reviewed ownership differs",
        )
        functions = sorted(
            unit.get(
                "functions",
                [f for f in config["functions"] if f["object"] == unit["object"]],
            ),
            key=lambda f: f["offset"],
        )
        cursor = extent["start"]
        decoded = []
        for function in functions:
            need(
                function["offset"] == cursor,
                "gap or overlap in reviewed function coverage",
            )
            proof = verify_owner_linear_span(
                function, target.program_image, config["segment"]
            )
            other = verify_owner_linear_span(
                function, candidate.program_image, config["segment"]
            )
            need(
                proof == other
                and proof["last_instruction"]
                == ("retf" if "far" in function["abi"] else "ret"),
                "near/far function boundary differs",
            )
            if "return_pop" in function:
                start = function["segment"] * 16 + function["offset"]
                decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
                last = list(
                    decoder.disasm(
                        target.program_image[start : start + function["size"]], 0
                    )
                )[-1]
                need(
                    int(last.op_str or "0", 0) == function["return_pop"],
                    "Pascal/cdecl stack cleanup differs",
                )
            cursor += function["size"]
            decoded.append(
                dict(
                    name=function["name"],
                    offset=function["offset"],
                    bytes=function["size"],
                    **proof,
                )
            )
        need(
            cursor == extent["start"] + extent["size"],
            "complete owner coverage required",
        )
        obj_path = "obj/th03/" + unit["object"] + ".obj"
        obj_raw = (build.WORK / obj_path).read_bytes()
        segments = [s for s in segment_definitions(obj_raw) if s["size"]]
        need(
            len(segments) == 1
            and segments[0]["class"] == "CODE"
            and segments[0]["name"] == extent["map_segment"]
            and segments[0]["size"] == extent["size"],
            "private storage or wrong CODE extent",
        )
        need(
            omf[obj_path]["translator_comments"] == ["TC86 Borland C++ 4.02"],
            "native TC4 producer required",
        )
        need(
            [offset for offset, name in code_publics(obj_raw, segments[0]["index"])]
            == [f["offset"] - extent["start"] for f in functions],
            "compiler function entries differ",
        )
        pattern = (
            rf"(?m)^\s*{extent['segment']:04X}:{extent['start']:04X}\s+{extent['size']:04X}\s+C=CODE\s+"
            rf"S={re.escape(extent['map_segment'])}\s+G={re.escape(extent['map_group'])}\s+"
            rf"M={re.escape(unit['map_module'])}\s+ACBP={extent['map_acbp']}\s*$"
        )
        need(len(re.findall(pattern, map_text)) == 1, "native MAP ownership differs")
        literal = lambda image: [
            (r.segment, r.offset) for r in image.relocations if lo <= r.linear < hi
        ]
        raw_equal = candidate.program_image[lo:hi] == target.program_image[lo:hi]
        order_equal = literal(candidate) == literal(target)
        checks = dict(
            **{
                "target-identity": True,
                "format-integrity": target.valid and candidate.valid,
                "boundary-ownership": cursor == extent["start"] + extent["size"],
                "toolchain-identity": attestation["ready"],
                "toolchain-replay": report["native_outputs_unchanged"],
                "object-format-integrity": omf[obj_path]["valid"],
                "cold-build-determinism": pair["complete"],
                "layout-relocations": order_equal,
                "raw-bytes": raw_equal,
                "ledger-consistency": True,
                "cold-aggregate-replay": comparison["all_owned_raw_and_ordered_equal"],
            }
        )
        need(
            set(checks) == required and all(checks.values()),
            "complete exact Oracle set did not pass",
        )
        result["units"][unit["id"]] = dict(
            bytes=extent["size"],
            file_offset=int(row["file_offset"], 0),
            functions=decoded,
            ordered_relocations=len(literal(target)),
            gates=checks,
        )
    need(
        set(result["units"]) == OWNERS | LOSE_OWNERS | CORE_OWNERS,
        "all native owners required",
    )
    return result


if __name__ == "__main__":
    try:
        result = review()
        output = ROOT / ".analysis/work/main-unit-review.json"
        output.write_text(json.dumps(result, indent=2) + "\n")
        print(
            "Native cold unit review: PASS; 5 owners / 15 functions / 2771 bytes; product exact remains false"
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print("Native cold unit review: FAIL:", error, file=sys.stderr)
        sys.exit(1)
