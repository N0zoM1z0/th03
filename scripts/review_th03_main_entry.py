#!/usr/bin/env python3
"""Review a source-produced MAIN entry and its bounded emulated behavior."""

from pathlib import Path
from dataclasses import replace
from collections import Counter
import argparse
import importlib.util
import json
import re

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from unicorn import UcError
from lib.pc98 import parse_mz
from lib.main_entry_runtime import compare, execute
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact
from probe_th03_main_bomb_rikako_cpp import segment_definitions, code_bytes
from review_th03_cpu_link_order import omf
from review_th03_farcall_groups import audit_native, digest, pinned, call_window
import stage_th03_main_entry as stage

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = ROOT / ".analysis/main-resume-20261023"


def need(ok, message):
    if not ok:
        raise ValueError(message)


def mutated(image, offset, value):
    data = bytearray(image.program_image)
    data[offset] = value
    return replace(image, program_image=bytes(data))


def negative_controls(image):
    normal = dict(resident=True, bgm=1, story=0, outcomes=[1, 0])
    controls = (
        (
            "resident branch",
            0x96F8,
            0x75,
            dict(resident=False, bgm=0, story=0, outcomes=[]),
        ),
        ("palette tone", 0x9728, 101, normal),
        ("continue comparison", 0x9745, 2, normal),
        ("OP filename", 0x975F, 0x54, normal),
        (
            "story decrement",
            0x976A,
            0x4F,
            dict(resident=True, bgm=1, story=0, outcomes=[2]),
        ),
    )
    rejected = []
    for name, offset, value, scenario in controls:
        need(image.program_image[offset] != value, "negative control must change bytes")
        try:
            execute(mutated(image, offset, value), scenario)
        except (ValueError, UcError) as error:
            # Unicorn failures also reject a mutation; no mutated product is written.
            rejected.append(dict(name=name, reason=type(error).__name__))
        else:
            raise ValueError("mutation accepted: " + name)
    return rejected


def publics(raw):
    result = {}
    for line in raw.decode().splitlines():
        m = re.fullmatch(r"\s*([0-9A-Fa-f]{4}):([0-9A-Fa-f]{4})\s+(\S+)\s*", line)
        if m:
            value = (int(m[1], 16), int(m[2], 16))
            need(m[3] not in result or result[m[3]] == value, "ambiguous MAP symbol")
            result[m[3]] = value
    return result


def review(base=DEFAULT_BASE):
    packet = base / "native-entry-link-v02"
    output = base / "native-entry-link-v02-output"
    # The historical aggregate correctly failed literal relocation equality.
    manifest, work = audit_native(packet, output, 6, False)
    done = json.loads((output / "completion.json").read_text())
    need(
        done["errors"] == ["ValueError('static object observation failed')"],
        "unexpected historical failure",
    )
    spec = importlib.util.spec_from_file_location(
        "entry_frozen_verifier", packet / "verify.py"
    )
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    verifier.source_closure(json.loads((packet / "plan.json").read_text()))
    linked = verifier.verify(work, manifest)
    checks = linked["checks"]
    need(
        all(
            v
            for k, v in checks.items()
            if k != "outside_entry_literal_relocations_preserved"
        ),
        "layout/raw regression",
    )
    need(
        checks["outside_entry_literal_relocations_preserved"] is False,
        "historical relocation observation changed",
    )
    source_inputs = {}
    for name in ("src/main/core/entry.cpp", "src/main/core/entry.hpp"):
        raw = pinned(manifest["repeat_inputs"][name])
        need((ROOT / name).read_bytes() == raw, "installed source differs: " + name)
        source_inputs[name] = digest(ROOT / name)
    root = pinned(manifest["repeat_inputs"]["th03_main.asm"])
    response = pinned(manifest["repeat_inputs"]["obj/th03/main.@l"])
    old_plan = json.loads(
        (
            ROOT / ".analysis/codex-main-state-link-20261022-v01/native-v02/plan.json"
        ).read_text()
    )
    need(
        stage.transform_root(pinned(old_plan["sources"]["th03_main.asm"])) == root,
        "maintained root staging differs",
    )
    need(
        stage.transform_response(pinned(old_plan["sources"]["obj/th03/main.@l"]))
        == response,
        "maintained object order differs",
    )
    names = publics((work / "obj/th03/main.map").read_bytes())
    expected = dict(
        _main=(0x96E, 6),
        MAIN_EXEC=(0x96E, 0x1D74),
        _stage_setup=(0x96E, 0x434),
        _round_loop=(0x96E, 0x98),
        _round_start_next=(0x96E, 0xB3F),
        _main_archive_name=(0x1D56, 0x13A),
        _main_gaiji_font=(0x1D56, 0x146),
        _main_op_name=(0x1D56, 0x151),
        _main_ending_name=(0x1D56, 0x154),
        _main_background_init=(0x1D56, 0x39C0),
    )
    need(
        all(names.get(n) == v for n, v in expected.items()),
        "existing code/storage alias address",
    )
    candidate = parse_mz((work / "bin/th03/main.exe").read_bytes())
    prior = parse_mz(
        (
            ROOT / ".analysis/toolchain/wineprefix/drive_c/PSTL245/bin/th03/main.exe"
        ).read_bytes()
    )
    target = parse_mz(
        read_verified_artifact(
            ROOT,
            find_artifact(
                load_target_manifest(ROOT / "config/targets.toml"), "th03-main"
            ),
        )
    )
    obj = work / "obj/th03/entry.obj"
    raw = obj.read_bytes()
    segments = segment_definitions(raw)
    nonempty = [s for s in segments if s["size"]]
    need(
        len(nonempty) == 1
        and nonempty[0]["name"] == "PLAYFLD_TEXT"
        and nonempty[0]["size"] == 146,
        "one 146-byte CODE contribution; no DATA/BSS",
    )
    code, _ = code_bytes(raw, nonempty[0]["index"])
    decoder = Cs(CS_ARCH_X86, CS_MODE_16)
    decoder.detail = True
    ins = list(decoder.disasm(code, 0))
    need(sum(i.size for i in ins) == 146, "complete object decode")
    _, blocks = omf(
        obj,
        [
            dict(module="src/main/core/entry.cpp", segment=s["name"], start=0)
            for s in segments
        ],
    )
    fixups = [f for b in blocks for f in b["fixups"]]
    need(len(fixups) == 23, "complete original OMF fixup set")
    masked = set()
    wanted = target.program_image[0x96E6:0x9778]
    for f in fixups:
        at = f["site"]
        i = next(i for i in ins if i.address <= at < i.address + i.size)
        need(f["kind"] in (1, 3), "reviewed fixup width")
        width = 4 if f["kind"] == 3 else 2
        if width == 4:
            need(i.mnemonic == "lcall" and at == i.address + 1, "far operand fixup")
            if wanted[i.address : i.address + 3] == bytes.fromhex("900ee8"):
                masked.add(i.address)
        else:
            need(
                (at, 2)
                in (
                    (i.address + i.imm_offset, i.imm_size),
                    (i.address + i.disp_offset, i.disp_size),
                ),
                "word fixup must occupy a decoded operand",
            )
        masked.update(range(at, at + width))
    need(
        all(a == b for n, (a, b) in enumerate(zip(code, wanted)) if n not in masked),
        "non-fixup object bytes differ",
    )
    diff = [
        0x96E6 + n
        for n, (a, b) in enumerate(zip(candidate.program_image[0x96E6:0x9778], wanted))
        if a != b
    ]
    need(diff == list(range(0x9770, 0x9775)), "only one five-byte call mismatch")
    a, dest, _ = call_window(candidate, 0x9770)
    b, tdest, _ = call_window(target, 0x9770)
    need(not a and b and dest == tdest == 0xB454, "actual call forms/destination")

    def outside(im):
        return [
            (r.segment, r.offset)
            for r in im.relocations
            if not 0x96E6 <= r.linear < 0x9778
        ]

    need(
        Counter(outside(candidate)) == Counter(outside(prior)),
        "outside relocation membership changed",
    )
    register_manifest, register_work = audit_native(
        base / "native-v09", base / "native-v09-output", 1, True
    )
    register_result = json.loads(
        (base / "native-v09-output/object-verification.json").read_text()
    )
    need(
        register_result["code_bytes"] == 662
        and register_result["functions"][2]["bytes"] == 175,
        "register-disable observation changed",
    )
    register_control = dict(
        compiled_object=digest(register_work / "obj/th03/lose.obj"),
        renderer_bytes=175,
        code_bytes=662,
        exact_acceptance=False,
    )
    runtime = compare(target, candidate)
    need(runtime["entry_code_bytes_executed"] == 146, "complete entry byte coverage")
    return dict(
        schema="th03-main-entry-source-review-v1",
        review_tools=[
            digest(ROOT / n)
            for n in (
                "scripts/review_th03_main_entry.py",
                "scripts/lib/main_entry_runtime.py",
                "scripts/stage_th03_main_entry.py",
            )
        ],
        source_inputs=source_inputs,
        compiled_object=digest(obj),
        linked_executable=digest(work / "bin/th03/main.exe"),
        source_only_native_compile=True,
        native_link_phases=6,
        historical_completion_preserved_false=True,
        layout_checks=checks,
        aliases=expected,
        object_fixups=len(fixups),
        nonfixup_object_bytes_equal=146 - len(masked),
        linked_entry_equal_bytes=141,
        linked_entry_differences=diff,
        outside_relocation_membership_preserved=True,
        outside_literal_order_equal=False,
        register_disable_control=register_control,
        runtime=runtime,
        negative_controls=negative_controls(candidate),
        source_acceptance=False,
        exact_acceptance=False,
        cold_build=False,
        whole_game_percentage=None,
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--base", type=Path, default=DEFAULT_BASE)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    result = review(args.base)
    with args.output.open("x") as out:
        json.dump(result, out, indent=2)
        out.write("\n")
    print(
        json.dumps(
            {
                k: result[k]
                for k in (
                    "schema",
                    "native_link_phases",
                    "object_fixups",
                    "nonfixup_object_bytes_equal",
                    "linked_entry_equal_bytes",
                    "exact_acceptance",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
