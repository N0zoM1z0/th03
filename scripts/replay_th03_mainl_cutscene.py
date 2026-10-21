#!/usr/bin/env python3
"""Check supplied MAINL link products; no native execution or acceptance.

The caller must separately bind fresh compiler/linker invocations to these bytes.
This helper reads no target/source files in verify() and never edits image bytes.
Unicorn's ordinary MZ load relocation is performed only by the existing Probe.
"""
from __future__ import annotations

import argparse
from importlib.metadata import version
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.pc98 import parse_mz
from review_th03_decoded_code import code_rows, extent_observation
from review_th03_mainl_cutscene import CS, decode, runtime_matrix, sha

CACHED_EXE_SHA256 = "ff315af6f9cd197f78292d8c834a90afad7b4d6c9bda0a9f8b09d4bdbc12a1ad"
CACHED_MAP_SHA256 = "f262e1d8e78d353f29e5f2d9a1cd39be91f934d48b0839b5ab55be6d9e033568"
TARGET_EXE_SHA256 = "92600c8858bb407516cac6a9d77538ebdf0c33522c4f6bd9194d569eb927134a"
EXPECTED_DIFFERENCES = [0x140A, 0x1414, 0x144B]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def ordered_relocations(mz):
    return [[item.segment, item.offset] for item in mz.relocations]

def scoped_relocation_words(mz, row):
    start, end = row["start"], row["start"] + row["size"]
    words = []
    for item in mz.relocations:
        if start <= item.linear and item.linear + 2 <= end:
            words.append([item.segment, item.offset,
                          struct.unpack_from("<H", mz.program_image, item.linear)[0]])
    return words

def runtime_summary(observations):
    counts = {
        "parameter_scenarios": len(observations["parameter_cases"]),
        "gaiji_scenarios": len(observations["gaiji_cases"]),
        "loader_scenarios": len(observations["loader_cases"]),
        "companion_parameter_entry_calls": len(observations["gaiji_cases"]),
    }
    counts["scenarios"] = sum(counts[k] for k in
                              ("parameter_scenarios", "gaiji_scenarios", "loader_scenarios"))
    counts["entry_calls"] = counts["scenarios"] + counts["companion_parameter_entry_calls"]
    require(counts["scenarios"] == 53 and counts["entry_calls"] == 65,
            "selected runtime matrix changed its reviewed case count")
    return dict(counts, observations_sha256=sha(
        json.dumps(observations, sort_keys=True, separators=(",", ":")).encode("utf-8")))

def verify(first_exe, second_exe, first_map, second_map,
           cached_exe, cached_map, target_exe):
    """Return diagnostics for seven byte strings, raising on any failed check."""
    inputs = dict(first_exe=first_exe, second_exe=second_exe,
                  first_map=first_map, second_map=second_map,
                  cached_exe=cached_exe, cached_map=cached_map,
                  target_exe=target_exe)
    require(all(isinstance(value, bytes) for value in inputs.values()),
            "verify arguments must be immutable bytes")
    require(sha(cached_exe) == CACHED_EXE_SHA256, "retained carrier EXE pin differs")
    require(sha(cached_map) == CACHED_MAP_SHA256, "retained carrier MAP pin differs")
    require(sha(target_exe) == TARGET_EXE_SHA256, "decoded MAINL target pin differs")
    require(first_exe == second_exe, "first/second raw EXE bytes differ")
    require(first_map == second_map, "first/second raw MAP bytes differ")
    require(first_exe == cached_exe, "linked raw EXE differs from retained carrier")
    require(first_map == cached_map, "linked raw MAP differs from retained carrier")

    images = {name: parse_mz(inputs[name])
              for name in ("first_exe", "second_exe", "cached_exe", "target_exe")}
    for name, mz in images.items():
        require(mz.valid, "invalid MZ: " + name)

    retained_relocations = ordered_relocations(images["cached_exe"])
    rows, extents, analyses, runtimes, summaries = [], [], [], [], []
    target = images["target_exe"]
    for label in ("first", "second"):
        mz = images[label + "_exe"]
        require(ordered_relocations(mz) == retained_relocations,
                label + " full ordered relocation records differ from carrier")
        module_rows = [row for row in code_rows(
            inputs[label + "_map"].decode("ascii"), len(mz.program_image))
            if row["module"] == "th03/cutscene.cpp"]
        require(len(module_rows) == 1, label + " cutscene CODE module is not unique")
        row = module_rows[0]
        require((row["segment"], row["offset"], row["size"], row["name"]) ==
                (CS, 0x0B3E, 3195, "CUTSCENE_TEXT"),
                label + " cutscene CODE coordinates/name differ")
        extent = extent_observation(target, mz, row)
        differences = [
            row["offset"] + index
            for index in range(row["size"])
            if target.program_image[row["start"] + index] !=
               mz.program_image[row["start"] + index]
        ]
        require(differences == EXPECTED_DIFFERENCES,
                label + " target cutscene raw-difference vector differs")
        require(extent["ordered_relocations_equal"] and
                len(extent["candidate_ordered_relocations"]) == 56,
                label + " target cutscene 56 ordered relocation records differ")
        target_words = scoped_relocation_words(target, row)
        candidate_words = scoped_relocation_words(mz, row)
        require(len(target_words) == 56 and target_words == candidate_words,
                label + " target cutscene ordered relocation word values differ")

        # Run both supplied products explicitly, even though raw equality passed.
        analysis = decode(mz.program_image)
        runtime = runtime_matrix(mz)
        summary = runtime_summary(runtime)
        rows.append(row)
        extents.append(dict(extent, raw_difference_offsets= differences,
                            ordered_relocation_words=candidate_words,
                            ordered_relocation_words_equal=True))
        analyses.append(analysis)
        runtimes.append(runtime)
        summaries.append(dict(product=label, **summary))

    require(rows[0] == rows[1] and extents[0] == extents[1],
            "first/second cutscene extent diagnostics differ")
    require(analyses[0] == analyses[1],
            "first/second decoded cutscene observations differ")
    require(runtimes[0] == runtimes[1],
            "first/second selected runtime observations differ")
    return {
        "kind": "th03-mainl-maintained-cutscene-linked-diagnostics",
        "diagnostic_checks_pass": True,
        "inputs_sha256": {name: sha(value) for name, value in inputs.items()},
        "raw_exe_pair_equal": True,
        "raw_map_pair_equal": True,
        "raw_exe_equal_retained_carrier": True,
        "raw_map_equal_retained_carrier": True,
        "all_ordered_relocations_equal_retained_carrier": True,
        "all_ordered_relocation_count": len(retained_relocations),
        "cutscene_extent": extents[0],
        "decoded_analysis": analyses[0],
        "selected_runtime": runtimes[0],
        "runtime_runs": summaries,
        "runtime_observations_equal": True,
        "runtime_scope": "53 selected scenarios / 65 entry calls per supplied image: "
            "loader, numeric parameter readers, gaiji command and cursor advance. "
            "File/heap/ASCII tolower calls and the gaiji suffix/return are models; "
            "the real gaiji ADC/AND prefix executes. Box/picture, remaining full "
            "interpreter branches, physical graphics/input/timing and whole-game "
            "runtime remain open.",
        "native_provenance": "Must be established separately by the caller's "
            "fresh compile/link records; byte verification cannot establish freshness.",
        "cold_reproducible": False,
        "whole_build_closed": False,
        "whole_runtime_proved": False,
        "source_acceptance": False,
        "raw_target_cutscene_equal": False,
        "exact_acceptance": False,
        "tools": {"capstone": version("capstone"), "unicorn": version("unicorn")},
    }

FIRST = '.analysis/mainl-cutscene-native-output-20261021-v01'
LINKED = '.analysis/mainl-cutscene-link-output-20261021-v02'
RETAINED_PINS = {'.analysis/mainl-cutscene-native-output-20261021-v01/manifest.json': '103ade0479e4edaeaa81c09da69a7c909348fb331b12a167f17b2c4861dc8f7e', '.analysis/mainl-cutscene-native-output-20261021-v01/completion.json': '3e5379b150e62e9b7d9fb8cfbf71d438df7dfbe0835a27709fa84064caeaf43c', '.analysis/mainl-cutscene-native-output-20261021-v01/comparison.json': '6afefcdb558848756e97184a063b81d2da57c8f710e50ff2b6d61500d6fc62c2', '.analysis/mainl-cutscene-native-output-20261021-v01/stage.json': '1bc0e20fe815092f3ed1974a52c6a5bbe0aa1dff080965171602b09177598e02', '.analysis/mainl-cutscene-native-output-20261021-v01/maintained-started.json': '5584913d6b5af9829ccc3109d00a8ea09d6ab27391236cad9f8aff2170d4f3f1', '.analysis/mainl-cutscene-native-output-20261021-v01/maintained-finished.json': 'f47e3e4553f5de101354d53300eba27e9f31c6a200ae3a0f0b6d81ea3c0c6307', '.analysis/mainl-cutscene-native-output-20261021-v01/maintained-registry-transition.json': '146d37e0c77ba4ed5332e8a2a8fe19e6afd6cbd38708754bb24cc02bec4e1ff4', '.analysis/mainl-cutscene-link-output-20261021-v02/manifest.json': 'f005dfb0210f4915c62e15706a5e43c8ff1f0d400d9af07df0860843867e5e2d', '.analysis/mainl-cutscene-link-output-20261021-v02/completion.json': 'd308086edc709a3815bf5adbc6304e75ea755998ff8375d36aba6a6de6d25964', '.analysis/mainl-cutscene-link-output-20261021-v02/object-comparison.json': '4e07f6ee5e6702c6bb81129dfd46678f935830794ef84c8f2e77d7107740a761', '.analysis/mainl-cutscene-link-output-20261021-v02/linked-verification.json': 'ed3123cdc3a2ed7ea8e2932def0701d23b28c10dc1eb4a9c18edf9790a547ebd', '.analysis/mainl-cutscene-link-output-20261021-v02/stage.json': '1bc0e20fe815092f3ed1974a52c6a5bbe0aa1dff080965171602b09177598e02', '.analysis/mainl-cutscene-link-output-20261021-v02/compile2-object.json': 'c1394f0dc7ff6bc877ad25cdd3a0159b280428112c0c8f87e619bd491d2dade9', '.analysis/mainl-cutscene-link-output-20261021-v02/source-mtime-declaration.json': '47458c1622bee81d4fc7b076004cb87e7a4da7e21c4179b945f0691c4cc6f8cd', '.analysis/mainl-cutscene-link-output-20261021-v02/link1-started.json': '818732148622d7f0b35c67cf6367562455ca32ed03d1f3afbcd6c6534244e10f', '.analysis/mainl-cutscene-link-output-20261021-v02/link1-finished.json': 'd76717f03e6788150b6c3df36aa8f8e20a65fa341d13f86f5726e693fa92e228', '.analysis/mainl-cutscene-link-output-20261021-v02/link1-registry-transition.json': 'e98cdc3628ead9604d65bf725bfb068722c9b7e1c9cbefd19b8f2605a514c868', '.analysis/mainl-cutscene-link-output-20261021-v02/compile2-started.json': '7cfb2d5ddaf1acb601a9f3c575626c313b8c54e624acb19e2c63769134ad828a', '.analysis/mainl-cutscene-link-output-20261021-v02/compile2-finished.json': 'd5b33b3b6d1dc894533d3611b716fdf9fad390aac91a2f9615ee9f53fde3db8c', '.analysis/mainl-cutscene-link-output-20261021-v02/compile2-registry-transition.json': 'f9445b009910f9d2916e83f412721245705ee563fce57365fb01da4dc4eaddac', '.analysis/mainl-cutscene-link-output-20261021-v02/link2-started.json': 'f500cae81f4e0548d76de2874549d4e0e788a0336de7fc3fe3291402707cba5e', '.analysis/mainl-cutscene-link-output-20261021-v02/link2-finished.json': 'cfc20081838ea0e22ec7d10dee37b7acb018fd5685fce66fe3abf629105087f1', '.analysis/mainl-cutscene-link-output-20261021-v02/link2-registry-transition.json': 'b355d1452e27e03ff8b4bb470aeb9a2dfbf42dbebaa34e492dba7fd86331ca92'}

def read_verified(path, expected):
    name = Path(path)
    require(not name.is_absolute() and ".." not in name.parts, "relative proof path required")
    full = ROOT / name
    require(not any(p.is_symlink() for p in (full, *full.parents)), "proof path cannot traverse symlinks")
    raw = full.read_bytes()
    require(sha(raw) == expected, "retained/source identity differs: " + path)
    return raw

def retained_json(path):
    return json.loads(read_verified(path, RETAINED_PINS[path]))

def native_finished(result):
    require(result.get("exit_code") == 0 and not result.get("timeout")
            and not result.get("cleanup_uncertain") and not result.get("poison")
            and result.get("initial_inventory_complete") is True
            and result.get("inventory_complete") is True
            and result.get("survivors") == [] and result.get("errors") == [],
            "native phase did not finish with certain owned cleanup")

def source_bindings(manifest, reader=read_verified):
    from stage_th03_mainl_cutscene import INPUTS
    for name in (*INPUTS, "scripts/stage_th03_mainl_cutscene.py"):
        reader(name, manifest["sources"][name]["sha256"])

def replay():
    """Recheck retained products and rerun selected CPU models; never compile/link."""
    first = retained_json(FIRST + "/manifest.json")
    links = retained_json(LINKED + "/manifest.json")
    source_bindings(first)
    source_bindings(links)
    initial = retained_json(FIRST + "/completion.json")
    final = retained_json(LINKED + "/completion.json")
    for receipt, count in ((initial, 2), (final, 3)):
        require(receipt["complete"] and not receipt["errors"]
                and receipt["owned_lock_released"] and receipt["native_invocations"] == count,
                "incomplete native provenance")
        require(receipt["exact_acceptance"] is False, "native diagnostic claimed exact acceptance")
    require(final["retained_other_objects"] == 32 and final["cold_whole_program"] is False,
            "hybrid retained-carrier scope differs")
    for directory, phase, argv in (
        (FIRST, "maintained", first["native_argv"]),
        (LINKED, "link1", links["native_argv"]["link"]),
        (LINKED, "compile2", links["native_argv"]["compile"]),
        (LINKED, "link2", links["native_argv"]["link"]),
    ):
        started = retained_json(directory + "/" + phase + "-started.json")
        require(started["argv"] == argv and started["wait_seconds"] == 90
                and started["cleanup_seconds"] == 15, "native command/budget differs")
        native_finished(retained_json(directory + "/" + phase + "-finished.json"))
        require(retained_json(directory + "/" + phase + "-registry-transition.json")["ok"],
                "unaccepted registry transition")
    require(retained_json(FIRST + "/comparison.json")["all_ordered_non_dependency_records_equal"],
            "frozen baseline/maintained code contract differs")
    comparison = retained_json(LINKED + "/object-comparison.json")
    require(comparison["raw_equal"] and comparison["all_ordered_non_dependency_records_equal"],
            "independent maintained objects differ")
    stage1 = retained_json(FIRST + "/stage.json")
    stage2 = retained_json(LINKED + "/stage.json")
    require(stage1 == stage2, "consumed maintained stage differs")
    mtime = retained_json(LINKED + "/source-mtime-declaration.json")
    require(mtime["mtime_ns"] == links["declared_source_mtimes_ns"], "declared source mtimes differ")
    for row in links["carrier_files"].values():
        read_verified(row["path"], row["sha256"])
    first_object = links["first_object"]
    object1 = read_verified(first_object["path"], first_object["sha256"])
    object2_path = ".analysis/toolchain/wineprefix/drive_c/MCL03/R2/obj/th03/cutscene.obj"
    object2 = read_verified(object2_path, retained_json(LINKED + "/compile2-object.json")["sha256"])
    require(object1 == object2 and sha(object1) == comparison["baseline"]["sha256"],
            "retained raw object pair differs")
    work = ".analysis/toolchain/wineprefix/drive_c/MCL03/"
    def product(role, kind, digest):
        return read_verified(work + role + "/" + kind, digest)
    cached_exe = read_verified(links["cached_exe"]["path"], links["cached_exe"]["sha256"])
    cached_map = read_verified(links["cached_map"]["path"], links["cached_map"]["sha256"])
    target = read_verified(links["decoded_target"]["path"], links["decoded_target"]["sha256"])
    result = verify(product("R1", "bin/th03/mainl.exe", sha(cached_exe)),
                    product("R2", "bin/th03/mainl.exe", sha(cached_exe)),
                    product("R1", "obj/th03/mainl.map", sha(cached_map)),
                    product("R2", "obj/th03/mainl.map", sha(cached_map)),
                    cached_exe, cached_map, target)
    require(json.dumps(result, sort_keys=True) == json.dumps(retained_json(LINKED + "/linked-verification.json"), sort_keys=True),
            "fresh verification differs from retained observations")
    return dict(kind="th03-mainl-maintained-cutscene-source-replay", checks_pass=True,
                owner="src/mainl/cutscene.cpp", owner_sha256=first["sources"]["src/mainl/cutscene.cpp"]["sha256"],
                retained_receipts=RETAINED_PINS, compiled_source_materializations=2,
                raw_object_pair_equal=True, retained_other_objects=32,
                source_mtime_basis=mtime["basis"], linked_diagnostics=result,
                native_invocations_this_replay=0, cold_whole_program=False,
                whole_runtime_proved=False, exact_acceptance=False)

def main():
    parser = argparse.ArgumentParser(description="Recheck retained maintained cutscene hybrid proof; no native build")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.is_absolute() and args.output.parts[:1] == (".analysis",)
            and ".." not in args.output.parts, "output must be under .analysis")
    result = replay()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print("PASS maintained MAINL cutscene source: two compiled objects, hybrid links, selected runtime; exact remains open")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
