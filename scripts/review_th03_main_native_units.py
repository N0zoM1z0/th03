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
    "th03-main-player-lose-renderer",
}


CORE_OWNERS = {"th03-main-round-finish", "th03-main-core-entry", "th03-main-round-loop"}
STAGE_OWNERS = {"th03-main-stage-round"}
PALETTE_OWNERS = {"th03-main-stage-palette"}
CHARACTER_OWNERS = {"th03-main-character-setup"}
PLAYER_STATE_OWNERS = {
    "th03-main-player-state-update",
    "th03-main-player-render-knock-bomb",
    "th03-main-stage-shot-sprites",
    "th03-main-round-results",
    "th03-main-player-shots-add",
}
HANDOFF_OWNERS = {"th03-main-executable-chain", "th03-main-demo-transition"}


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


def verify_native_coverage(functions, extent, program):
    """Partition code and compiler tables; validate actual CS jump destinations."""
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_16)
    starts = {}
    ranges = []
    for function in functions:
        start, size = function["offset"], function["size"]
        linear = function["segment"] * 16 + start
        starts[function["name"]] = {
            i.address for i in decoder.disasm(program[linear:linear + size], start)
        }
        ranges.append((start, size))
    data = []
    for item in extent.get("producer_ranges", []):
        start, size = item["offset"], item["size"]
        linear = extent["segment"] * 16 + start
        raw = program[linear:linear + size]
        need(len(raw) == size, "truncated compiler data")
        if item["kind"] == "tc4-natural-zero":
            need(size == 1 and raw == b"\0", "compiler alignment differs")
        elif item["kind"] == "tasm-code-even":
            need(size == 1 and start % 2 == 1 and raw == b"\x90", "native CODE alignment differs")
        else:
            need(item["kind"] == "tc4-switch-table" and size % 2 == 0,
                 "unknown compiler data")
            entries = [int.from_bytes(raw[i:i + 2], "little") for i in range(0, size, 2)]
            need(all(e in starts[item["function"]] for e in entries),
                 "switch destination is not an owned instruction entry")
        data.append(dict(item, raw_hex=raw.hex()))
        ranges.append((start, size))
    cursor = extent["start"]
    for start, size in sorted(ranges):
        need(start == cursor and size > 0, "gap or overlap in reviewed owner coverage")
        cursor += size
    need(cursor == extent["start"] + extent["size"], "complete owner coverage required")
    return data


def producer_ownership(unit, units, functions):
    """A shared native object must exactly cover its declared owners, without gaps."""
    peers = [u for u in units if u["object"] == unit["object"]]
    ranges = sorted(((u["code_extents"][0]["start"], u) for u in peers),
                    key=lambda item: (item[0], item[1]["id"]))
    first = ranges[0][1]["code_extents"][0]
    metadata = (first["segment"], first["map_segment"], first["map_group"], first["map_acbp"])
    cursor, starts = first["start"], []
    native_functions = []
    for start, peer in ranges:
        need(len(peer["code_extents"]) == 1, "native owner must have one extent")
        extent = peer["code_extents"][0]
        need(start == cursor, "native producer owners have a gap or overlap")
        need((extent["segment"], extent["map_segment"], extent["map_group"], extent["map_acbp"])
             == metadata and peer["map_module"] == unit["map_module"], "native producer frames differ")
        cursor += extent["size"]
        starts.append(peer["id"])
        native_functions.extend(peer.get("functions", [f for f in functions if f["object"] == peer["object"]]))
    return dict(extent=dict(first, size=cursor - first["start"]), owners=starts,
                functions=sorted(native_functions, key=lambda f: f["offset"]))


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
        {u["id"] for u in native_units} == LOSE_OWNERS | CORE_OWNERS | STAGE_OWNERS | PALETTE_OWNERS | CHARACTER_OWNERS | HANDOFF_OWNERS | PLAYER_STATE_OWNERS,
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
        entry_loop_producer=comparison["entry_loop_producer"],
        main_flow_producer=comparison["main_flow_producer"],
        shared_producers=comparison["shared_producers"],
        player_producers=comparison["player_producer_layout"],
        character_setup_producer=comparison["character_setup_producer"],
        matching_relocation_prefix=comparison["matching_relocation_prefix"],
        differing_relocation_order_positions=comparison["differing_relocation_order_positions"],
        product_exact=False,
    )
    map_text = (build.WORK / "obj/th03/main.map").read_text().replace(chr(92), "/")
    primitive_path = "obj/th03/roundpr.obj"
    primitive_raw = (build.WORK / primitive_path).read_bytes()
    primitive_segments = [s for s in segment_definitions(primitive_raw) if s["size"]]
    need([(s["name"], s["class"], s["size"]) for s in primitive_segments]
         == [("HITCIRC_TEXT", "CODE", 82)]
         and omf[primitive_path]["translator_comments"] == ["Turbo Assembler  Version 5.0"],
         "round primitive native producer differs")
    need(code_publics(primitive_raw, primitive_segments[0]["index"]) == [
        (0, "@randring_fill$qv"), (18, "@randring1_next16$qv"),
        (36, "@RANDRING1_NEXT16_AND$QUI"), (62, "_collmap_reset")],
        "round primitive entries differ")
    primitive_functions = [f for f in config["functions"]
                           if 0xA3FA <= f.get("segment", config["segment"]) * 16 + f["offset"] < 0xA44C]
    primitive_extent = dict(segment=0x96E, start=0xD1A, size=82, producer_ranges=[
        dict(offset=0xD3D, size=1, kind="tasm-code-even"),
        dict(offset=0xD6B, size=1, kind="tasm-code-even")])
    need(verify_native_coverage(primitive_functions, primitive_extent, target.program_image)
         == verify_native_coverage(primitive_functions, primitive_extent, candidate.program_image),
         "round primitive complete coverage differs")
    need(len(primitive_functions) == 4
         and re.search(r"(?m)^\s*096E:0D1A\s+0052\s+C=CODE\s+S=HITCIRC_TEXT\s+G=MAIN_01\s+M=th03/roundpr\.asm\s+ACBP=48\s*$", map_text),
         "round primitive MAP ownership differs")
    for function in primitive_functions:
        # Public names/offsets are checked against the native OMF above. The
        # linear decoder takes only span/ABI facts, not legacy MAP annotations.
        span = {k: function[k] for k in ("name", "segment", "offset", "size", "abi")}
        proof = verify_owner_linear_span(span, target.program_image, config["segment"])
        need(proof == verify_owner_linear_span(span, candidate.program_image, config["segment"])
             and proof["last_instruction"] == "ret", "round primitive near boundary differs")
    result["round_primitives_context"] = dict(comparison["round_primitives_producer"],
        functions=primitive_functions, native_object=primitive_path, new_authored_credit=0)
    from lib.main_entry_runtime import compare as entry_compare, negative_controls as entry_controls

    result["entry_runtime"] = entry_compare(target, candidate)
    result["entry_controls"] = entry_controls(candidate)
    need(result["entry_runtime"]["cases"] == 1172
         and result["entry_runtime"]["entry_code_bytes_executed"] == 146
         and len(result["entry_controls"]) == 7, "entry contracts are incomplete")
    result["entry_model_sha256"] = sha((ROOT / "scripts/lib/main_entry_runtime.py").read_bytes())
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
    from lib.main_lose_renderer_runtime import compare as renderer_compare, negative_controls as renderer_controls
    result["lose_renderer_runtime"] = renderer_compare(target, candidate)
    result["lose_renderer_controls"] = renderer_controls(candidate)
    need(result["lose_renderer_runtime"]["cases"] == 2068
         and result["lose_renderer_runtime"]["code_bytes_executed"] == 177
         and result["lose_renderer_controls"]["count"] == 8, "loss renderer contracts incomplete")
    result["lose_renderer_model_sha256"] = sha((ROOT / "scripts/lib/main_lose_renderer_runtime.py").read_bytes())
    from lib.main_round_finish_runtime import (
        compare as round_compare,
        negative_controls as round_controls,
    )

    result["round_finish_runtime"] = round_compare(target, candidate)
    result["round_finish_controls"] = round_controls(candidate)
    result["round_finish_model_sha256"] = sha(
        (ROOT / "scripts/lib/main_round_finish_runtime.py").read_bytes()
    )
    from lib.main_round_init_runtime import (
        compare as init_compare,
        negative_controls as init_controls,
    )

    result["stage_round_candidate"] = comparison["stage_round_candidate"]
    result["round_init_runtime"] = init_compare(target, candidate)
    result["round_init_controls"] = init_controls(candidate)
    result["round_init_model_sha256"] = sha(
        (ROOT / "scripts/lib/main_round_init_runtime.py").read_bytes()
    )
    from lib.main_demo_runtime import compare as demo_compare, negative_controls as demo_controls

    result["demo_runtime"] = demo_compare(target, candidate)
    result["demo_controls"] = demo_controls(candidate)
    result["demo_model_sha256"] = sha((ROOT / "scripts/lib/main_demo_runtime.py").read_bytes())
    from lib.main_round_loop_runtime import compare as loop_compare, negative_controls as loop_controls

    result["round_loop_runtime"] = loop_compare(target, candidate)
    result["round_loop_controls"] = loop_controls(candidate)
    need(result["round_loop_runtime"]["code_bytes_executed"] == 862
         and result["round_loop_controls"]["count"] == 8, "round-loop contracts are incomplete")
    result["round_loop_model_sha256"] = sha((ROOT / "scripts/lib/main_round_loop_runtime.py").read_bytes())
    from lib.main_stage_palette_runtime import compare as palette_compare, negative_controls as palette_controls

    result["palette_runtime"] = palette_compare(target, candidate)
    result["palette_controls"] = palette_controls(candidate)
    need(result["palette_runtime"]["cases"] == 1556
         and result["palette_runtime"]["code_bytes_executed"] == 128
         and result["palette_controls"]["count"] == 8, "palette contracts are incomplete")
    result["palette_model_sha256"] = sha((ROOT / "scripts/lib/main_stage_palette_runtime.py").read_bytes())
    from lib.main_character_setup_runtime import compare as character_compare, negative_controls as character_controls, C as character_contract

    need(character_contract["target_sha256"] == result["target_sha256"], "character target contract differs")
    result["character_runtime"] = character_compare(target, candidate)
    result["character_controls"] = character_controls(candidate)
    need(result["character_runtime"]["cases"] == 1020
         and result["character_runtime"]["code_bytes_executed"] == 3888
         and result["character_runtime"]["primitive_code_bytes_executed"] == 80
         and result["character_controls"]["count"] == 16, "character contracts are incomplete")
    result["character_model_sha256"] = sha((ROOT / "scripts/lib/main_character_setup_runtime.py").read_bytes())
    result["character_contract_sha256"] = sha((ROOT / "scripts/lib/main_character_setup_contract.json").read_bytes())
    from lib.main_handoff_runtime import compare as handoff_compare, negative_controls as handoff_controls
    result["handoff_runtime"] = handoff_compare(target, candidate)
    result["handoff_controls"] = handoff_controls(candidate)
    need(result["handoff_runtime"]["cases"] == 1110
         and result["handoff_runtime"]["code_bytes_executed"] == 742
         and result["handoff_controls"]["count"] == 10, "handoff contracts are incomplete")
    result["handoff_model_sha256"] = sha((ROOT / "scripts/lib/main_handoff_runtime.py").read_bytes())
    for unit in (u for u in units if u["id"] in OWNERS | LOSE_OWNERS | CORE_OWNERS | STAGE_OWNERS | PALETTE_OWNERS | CHARACTER_OWNERS | HANDOFF_OWNERS | PLAYER_STATE_OWNERS):
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
        data = verify_native_coverage(functions, extent, target.program_image)
        need(data == verify_native_coverage(functions, extent, candidate.program_image),
             "compiler-local tables differ")
        decoded = []
        for function in functions:
            proof = verify_owner_linear_span(
                function, target.program_image, config["segment"]
            )
            other = verify_owner_linear_span(
                function, candidate.program_image, config["segment"]
            )
            # Distance belongs to the entry ABI, not a far pointer parameter.
            distance = re.match(r"^(near|far)\b", function["abi"], re.I)
            need(distance is not None, "entry distance is missing")
            need(
                proof == other
                and proof["last_instruction"]
                == ("retf" if distance[1].lower() == "far" else "ret"),
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
            decoded.append(
                dict(
                    name=function["name"],
                    offset=function["offset"],
                    bytes=function["size"],
                    **proof,
                )
            )
        obj_path = "obj/th03/" + unit["object"] + ".obj"
        obj_raw = (build.WORK / obj_path).read_bytes()
        if unit["id"] in PLAYER_STATE_OWNERS:
            from lib.main_player_layout import core_ownership
            producer = core_ownership(unit, units)
        else:
            producer = producer_ownership(unit, units, config["functions"])
        producer_extent = producer["extent"]
        segments = [s for s in segment_definitions(obj_raw) if s["size"]]
        need(
            len(segments) == 1
            and segments[0]["class"] == "CODE"
            and segments[0]["name"] == extent["map_segment"]
            and segments[0]["size"] == producer_extent["size"],
            "private storage or wrong CODE extent",
        )
        if unit.get("compiler") == "tasm5":
            need(unit["source"].endswith(".asm")
                 and omf[obj_path]["translator_comments"] == ["Turbo Assembler  Version 5.0"],
                 "native TASM5 producer required")
            need(code_publics(obj_raw, segments[0]["index"])
                 == [(p["offset"], p["name"]) for p in unit["publics"]],
                 "assembler function entries or aliases differ")
        else:
            need(omf[obj_path]["translator_comments"] == ["TC86 Borland C++ 4.02"],
                 "native TC4 producer required")
            need([offset for offset, name in code_publics(obj_raw, segments[0]["index"])]
                 == [f["offset"] - producer_extent["start"] for f in producer["functions"]],
                 "compiler function entries differ")
        pattern = (
            rf"(?m)^\s*{extent['segment']:04X}:{producer_extent['start']:04X}\s+{producer_extent['size']:04X}\s+C=CODE\s+"
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
                "boundary-ownership": True,
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
            compiler_data=data,
            native_producer=dict(object=obj_path, start=producer_extent["start"],
                                 bytes=producer_extent["size"], owners=producer["owners"],
                                 partition=producer.get("partition"),
                                 code_record_sizes=[p["size"] for p in build.code_bytes(obj_raw, segments[0]["index"])[1]]),
            ordered_relocations=len(literal(target)),
            gates=checks,
        )
    need(
        set(result["units"]) == OWNERS | LOSE_OWNERS | CORE_OWNERS | STAGE_OWNERS | PALETTE_OWNERS | CHARACTER_OWNERS | HANDOFF_OWNERS | PLAYER_STATE_OWNERS,
        "all native owners required",
    )
    return result


if __name__ == "__main__":
    try:
        result = review()
        output = ROOT / ".analysis/work/main-unit-review.json"
        output.write_text(json.dumps(result, indent=2) + "\n")
        owners = list(result["units"].values())
        print(f"Native cold unit review: PASS; {len(owners)} owners / "
              f"{sum(len(u['functions']) for u in owners)} functions / "
              f"{sum(u['bytes'] for u in owners)} bytes; product exact remains false")
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print("Native cold unit review: FAIL:", error, file=sys.stderr)
        sys.exit(1)
