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
from review_th03_mainl_regist import CS, decode, matrix as runtime_matrix, sha

CACHED_EXE_SHA256 = "ff315af6f9cd197f78292d8c834a90afad7b4d6c9bda0a9f8b09d4bdbc12a1ad"
CACHED_MAP_SHA256 = "f262e1d8e78d353f29e5f2d9a1cd39be91f934d48b0839b5ab55be6d9e033568"
TARGET_EXE_SHA256 = "92600c8858bb407516cac6a9d77538ebdf0c33522c4f6bd9194d569eb927134a"
EXPECTED_DIFFERENCES = [0x19E2, 0x19EC, 0x22D8, 0x22E2, 0x230F, 0x2319]

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
    require((observations["top_level_calls_per_image"], observations["terminal_calls_per_image"],
             observations["budget_cases_per_image"]) == (152,151,1), "selected matrix counts changed")
    return dict(entry_calls=152, terminal_calls=151, budget_observations=1,
                observations_sha256=sha(json.dumps(observations,sort_keys=True,separators=(",", ":")).encode()))


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
        module_rows = sorted([row for row in code_rows(
            inputs[label + "_map"].decode("ascii"), len(mz.program_image))
            if row["module"] in ("th03/regist.cpp", "th03/scoredat.cpp") and row["size"]],
            key=lambda row: row["offset"])
        require([(row["segment"],row["offset"],row["size"],row["name"]) for row in module_rows]
                == [(CS,0x17B9,229,"SCOREDAT_TEXT"),(CS,0x189E,2720,"REGIST_TEXT")],
                label + " registration/scoredat CODE coordinates/name differ")
        scope_extents=[]
        for row in module_rows:
            extent=extent_observation(target,mz,row)
            differences=[row["offset"]+index for index in range(row["size"])
                         if target.program_image[row["start"]+index] != mz.program_image[row["start"]+index]]
            expected=[] if row["size"]==229 else EXPECTED_DIFFERENCES
            count=0 if row["size"]==229 else 54
            require(differences==expected,label + " scoped raw differences changed")
            require(extent["ordered_relocations_equal"] and len(extent["candidate_ordered_relocations"])==count,
                    label + " scoped ordered relocations differ")
            target_words=scoped_relocation_words(target,row);candidate_words=scoped_relocation_words(mz,row)
            require(len(target_words)==count and target_words==candidate_words,label + " relocation words differ")
            scope_extents.append(dict(extent,raw_difference_offsets=differences,
                                     ordered_relocation_words=candidate_words,ordered_relocation_words_equal=True))

        # Run both supplied products explicitly, even though raw equality passed.
        analysis = decode(mz.program_image)
        runtime = runtime_matrix(mz)
        summary = runtime_summary(runtime)
        rows.append(module_rows)
        extents.append(scope_extents)
        analyses.append(analysis)
        runtimes.append(runtime)
        summaries.append(dict(product=label, **summary))

    require(rows[0] == rows[1] and extents[0] == extents[1],
            "first/second registration extent diagnostics differ")
    require(analyses[0] == analyses[1],
            "first/second decoded registration observations differ")
    require(runtimes[0] == runtimes[1],
            "first/second selected runtime observations differ")
    target_runtime=runtime_matrix(target)
    require(runtimes[0]==target_runtime,"linked/target selected runtime observations differ")
    summaries.append(dict(product="target",**runtime_summary(target_runtime)))
    return {
        "kind": "th03-mainl-maintained-registration-linked-diagnostics",
        "diagnostic_checks_pass": True,
        "inputs_sha256": {name: sha(value) for name, value in inputs.items()},
        "raw_exe_pair_equal": True,
        "raw_map_pair_equal": True,
        "raw_exe_equal_retained_carrier": True,
        "raw_map_equal_retained_carrier": True,
        "all_ordered_relocations_equal_retained_carrier": True,
        "all_ordered_relocation_count": len(retained_relocations),
        "registration_scoredat_extents": extents[0],
        "decoded_analysis": analyses[0],
        "selected_runtime": runtimes[0],
        "runtime_runs": summaries,
        "runtime_observations_equal": True,
        "runtime_scope": "152 selected entry calls per image, 151 terminal plus one deliberate budget observation. "
            "Registration insertion/name/menu, score load/save/crypto/recreation execute; foreign file, input, rendering, "
            "RNG, timing and sound are models. Physical devices and whole runtime remain open.",
        "native_provenance": "Must be established separately by the caller's "
            "fresh compile/link records; byte verification cannot establish freshness.",
        "cold_reproducible": False,
        "whole_build_closed": False,
        "whole_runtime_proved": False,
        "source_acceptance": False,
        "raw_target_registration_equal": False,
        "raw_target_scoredat_equal": True,
        "exact_acceptance": False,
        "tools": {"capstone": version("capstone"), "unicorn": version("unicorn")},
    }

FIRST = ".analysis/mainl-regist-native-output-20261021-v01"
LINKED = ".analysis/mainl-regist-link-output-20261021-v01"
RETAINED_PINS = {'.analysis/mainl-regist-native-output-20261021-v01/manifest.json': '9f343eeb94a4567af3d6cc50fadf7c632d9c2b72cd21ac5a38ce3c5ce619bef7', '.analysis/mainl-regist-native-output-20261021-v01/completion.json': '18499711b0c72f8acbfe48d978f9e197353bba51b0cd32f43dfa1a0516f320c6', '.analysis/mainl-regist-native-output-20261021-v01/stage.json': '5f33a8a9f84ed5169b7a1ae2843cdc5572b405f86232332c61b53bd31d5faaeb', '.analysis/mainl-regist-native-output-20261021-v01/regist-comparison.json': '9152e9a35eda2d274a7b4ad9e10289a55bc07b0b873028a399815886cf3a480c', '.analysis/mainl-regist-native-output-20261021-v01/scoredat-comparison.json': 'ec53eea85381dffbe2049330c85b71de539ebf6cc4b0c1c5e9778ac2372046db', '.analysis/mainl-regist-native-output-20261021-v01/base-scoredat-started.json': 'b0386cb9d27f788ea881f5549e0583614e7d81199c91336bf0d406b21c0c935c', '.analysis/mainl-regist-native-output-20261021-v01/base-scoredat-finished.json': '69f83a60c7473c4170150570eb68904e82281591c83c58426932dc207bdbaf7c', '.analysis/mainl-regist-native-output-20261021-v01/base-scoredat-registry-transition.json': 'd37fa6788cdca5d9f3650da3519ef6c44073aea948266ee579e4b7cd690e0a85', '.analysis/mainl-regist-native-output-20261021-v01/base-regist-started.json': '215b64151a8c86fc4fd79e506dc9740cc256075fcd8363c17c954672f51b7452', '.analysis/mainl-regist-native-output-20261021-v01/base-regist-finished.json': 'b7b5f2b023b7739f8a35e6f6d80f70659dd7927329abaec538248cff4eaf7992', '.analysis/mainl-regist-native-output-20261021-v01/base-regist-registry-transition.json': 'ea223996aeeff841e9ecd15472cee1d69867666a2c82162db68cf8860fa022d4', '.analysis/mainl-regist-native-output-20261021-v01/own-scoredat-started.json': '250a7e48e3ace6dda1c4bbc571abbcc5f553a2fe0fa8c2655b6d4a2958be711d', '.analysis/mainl-regist-native-output-20261021-v01/own-scoredat-finished.json': 'd18023b10f02cf4391809135a0e4211f261e0a0a34a22f2b6e6479806e39852e', '.analysis/mainl-regist-native-output-20261021-v01/own-scoredat-registry-transition.json': '595b99e515f96b249463658a725f5e9c4a6ef491e2b1255faa086146a53cfc44', '.analysis/mainl-regist-native-output-20261021-v01/own-regist-started.json': '77b8ba17efaf47ef341fabe2246862c04e4b33fab58bcdba8e01c83d941fc70b', '.analysis/mainl-regist-native-output-20261021-v01/own-regist-finished.json': 'afc57270cc8f16f727694a5ce5caf5f168bf08648a49880b8572ac8382a92768', '.analysis/mainl-regist-native-output-20261021-v01/own-regist-registry-transition.json': '7ff77eddd6a7ffd71b66cc61e954317e4f4dc10dcb46596b5e3a5e950f76b677', '.analysis/mainl-regist-link-output-20261021-v01/manifest.json': '60fb7b4df907626a0344dcb04a71a2b1e24d9fbc40dbb2e910ef216fd1daf1da', '.analysis/mainl-regist-link-output-20261021-v01/completion.json': '9370718cf38cf5cffdec8d3e255e4f3a6d3c772de4a35b8d85ebeebff5ef81c2', '.analysis/mainl-regist-link-output-20261021-v01/stage.json': '5f33a8a9f84ed5169b7a1ae2843cdc5572b405f86232332c61b53bd31d5faaeb', '.analysis/mainl-regist-link-output-20261021-v01/source-mtime-declaration.json': '0ad48c273ea4295b32d2781f11024e49122cf08b8e0502a3af85baa1c8d490ad', '.analysis/mainl-regist-link-output-20261021-v01/linked-verification.json': '1c876d1771d65b1dc49ceabc77b0ba05c1eb5cfd870298367c16124ee5b2602a', '.analysis/mainl-regist-link-output-20261021-v01/regist-object-comparison.json': '1a88c6ba093fcd5e727283aa176d069c3a19b099f5915eb590c05afabcfe969e', '.analysis/mainl-regist-link-output-20261021-v01/scoredat-object-comparison.json': 'aa2891d195fcdd2665947e1c325d2e1ac4fc5e2997185773ceaa06fba57b1736', '.analysis/mainl-regist-link-output-20261021-v01/regist2-object.json': '87bc6e613944641646c84e1258461e34f67c2487aa65906f81cadbb3968bcc9e', '.analysis/mainl-regist-link-output-20261021-v01/scoredat2-object.json': '1400de2cb35763f233f59c92aa724d4bbaecf22dc66c3102e39bbd918fd1aa0c', '.analysis/mainl-regist-link-output-20261021-v01/link1-started.json': 'b77c4cc77b1e3b6709768dbe0603ac965958da281d398b0eb667681c2d8fe996', '.analysis/mainl-regist-link-output-20261021-v01/link1-finished.json': '91e80e23009866a63bdf8b2f1b5c09c4531c1b902b2638883a81fac7d4509043', '.analysis/mainl-regist-link-output-20261021-v01/link1-registry-transition.json': '7a30e85d77901e41607425196114feed6c74d7782e6787f7b99a8d1a1e198603', '.analysis/mainl-regist-link-output-20261021-v01/scoredat2-started.json': 'a3c841495a815a1ccc8de80133f76bf356a3c479be29e8259ad286e71d890ba9', '.analysis/mainl-regist-link-output-20261021-v01/scoredat2-finished.json': 'a54b28889ab6987493717e621763d55648a789fa8e5e5d0a6a55e2cebcccdc25', '.analysis/mainl-regist-link-output-20261021-v01/scoredat2-registry-transition.json': '3cb7600b60e39c491d953e0dbef79cf7a8365361cb2cd12f3dda7fd269d688da', '.analysis/mainl-regist-link-output-20261021-v01/regist2-started.json': 'ccc4383b370212fc472c5f8d90405bf2ce5659d40452c2b42da27821997328f5', '.analysis/mainl-regist-link-output-20261021-v01/regist2-finished.json': 'ceca567925dd3075d34506adb26637dff4389ca5f829ca26cfec22c7bb631acd', '.analysis/mainl-regist-link-output-20261021-v01/regist2-registry-transition.json': '2bb1ca56b92c7f7b486fe6c5e5ca977bf6280c2bca116fe9438b98de9ec20cac', '.analysis/mainl-regist-link-output-20261021-v01/link2-started.json': 'e0f73acead965e2d4df4f5fcd235d1e84bf44759aed4b2be9b9bcedb3e35f95f', '.analysis/mainl-regist-link-output-20261021-v01/link2-finished.json': 'f698ddb75b2664fba1ee01962f0d7d6d50a0da25e43b7a7a33d9487aa5b36e5d', '.analysis/mainl-regist-link-output-20261021-v01/link2-registry-transition.json': '8771538111610b6819ed7ec34ba32a8babf2315d64f07276f0538ee544281d09'}

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
    from stage_th03_mainl_regist import INPUTS
    for name in (*INPUTS, "scripts/stage_th03_mainl_regist.py"):
        reader(name, manifest["sources"][name]["sha256"])

def replay():
    """Recheck retained products and rerun selected CPU models; never compile/link."""
    first = retained_json(FIRST + "/manifest.json")
    links = retained_json(LINKED + "/manifest.json")
    source_bindings(first)
    source_bindings(links)
    initial = retained_json(FIRST + "/completion.json")
    final = retained_json(LINKED + "/completion.json")
    for receipt, count in ((initial, 4), (final, 4)):
        require(receipt["complete"] and not receipt["errors"]
                and receipt["owned_lock_released"] and receipt["native_invocations"] == count,
                "incomplete native provenance")
        require(receipt["exact_acceptance"] is False, "native diagnostic claimed exact acceptance")
    require(final["retained_other_objects"] == 31 and final["cold_whole_program"] is False,
            "hybrid retained-carrier scope differs")
    phases = [(FIRST, role + "-" + unit, first["native_argv"][unit])
              for role in ("base", "own") for unit in ("scoredat", "regist")]
    phases += [(LINKED, phase, links["native_argv"][kind]) for phase,kind in
               (("link1","link"),("scoredat2","scoredat"),("regist2","regist"),("link2","link"))]
    for directory, phase, argv in phases:
        started = retained_json(directory + "/" + phase + "-started.json")
        require(started["argv"] == argv and started["wait_seconds"] == 90
                and started["cleanup_seconds"] == 15, "native command/budget differs")
        native_finished(retained_json(directory + "/" + phase + "-finished.json"))
        require(retained_json(directory + "/" + phase + "-registry-transition.json")["ok"],
                "unaccepted registry transition")
    for unit in ("scoredat", "regist"):
        require(retained_json(FIRST + "/" + unit + "-comparison.json")["all_ordered_non_dependency_records_equal"],
                "frozen baseline/maintained code contract differs")
        comparison = retained_json(LINKED + "/" + unit + "-object-comparison.json")
        require(comparison["raw_equal"] and comparison["all_ordered_non_dependency_records_equal"],
                "independent maintained objects differ")
    stage1 = retained_json(FIRST + "/stage.json")
    stage2 = retained_json(LINKED + "/stage.json")
    require(stage1 == stage2, "consumed maintained stage differs")
    mtime = retained_json(LINKED + "/source-mtime-declaration.json")
    require(mtime["mtime_ns"] == links["declared_source_mtimes_ns"], "declared source mtimes differ")
    for row in links["carrier_files"].values():
        read_verified(row["path"], row["sha256"])
    for unit in ("scoredat", "regist"):
        first_object = links["first_objects"][unit]
        object1 = read_verified(first_object["path"], first_object["sha256"])
        object2_path = ".analysis/toolchain/wineprefix/drive_c/MRG02/R2/obj/th03/" + unit + ".obj"
        object2 = read_verified(object2_path, retained_json(LINKED + "/" + unit + "2-object.json")["sha256"])
        comparison = retained_json(LINKED + "/" + unit + "-object-comparison.json")
        require(object1 == object2 and sha(object1) == comparison["baseline"]["sha256"],
                "retained raw object pair differs")
    work = ".analysis/toolchain/wineprefix/drive_c/MRG02/"
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
    return dict(kind="th03-mainl-maintained-regist-source-replay", checks_pass=True,
                owners={unit: first["sources"]["src/mainl/"+unit+".cpp"]["sha256"] for unit in ("scoredat", "regist")},
                retained_receipts=RETAINED_PINS, compiled_source_materializations=2, maintained_compile_invocations=4,
                raw_object_pair_equal=True, retained_other_objects=31,
                source_mtime_basis=mtime["basis"], linked_diagnostics=result,
                native_invocations_this_replay=0, cold_whole_program=False,
                whole_runtime_proved=False, exact_acceptance=False)

def main():
    parser = argparse.ArgumentParser(description="Recheck retained maintained regist hybrid proof; no native build")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.is_absolute() and args.output.parts[:1] == (".analysis",)
            and ".." not in args.output.parts, "output must be under .analysis")
    result = replay()
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x") as stream:
        stream.write(json.dumps(result, indent=2) + "\n")
    print("PASS maintained MAINL regist source: two independently compiled object pairs, hybrid links, selected runtime; exact remains open")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
