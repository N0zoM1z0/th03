#!/usr/bin/env python3
"""Build/check the current mixed MAIN tree without archived replay dependencies."""

from pathlib import Path, PurePosixPath
from collections import Counter
import argparse
import fcntl
import hashlib
import json
import os
import posixpath
import re
import signal
import shutil
import subprocess
from tempfile import TemporaryDirectory
import time
import tomllib

from lib.pc98 import parse_mz
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact
from probe_th03_main_bomb_rikako_cpp import segment_definitions, code_bytes, omf_index
from lib.omf import parse_omf

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK"
OUT = ROOT / ".analysis/work"
SOURCES = (
    "src/main/player/character_setup.cpp",
    "src/main/core/entry.cpp",
    "src/main/player/state.cpp",
    "src/main/player/shotroot.cpp",
    "src/main/player/lose.cpp",
    "src/main/hud/intro.cpp",
    "src/main/player/exatt_chiyuri.cpp",
    "src/main/player/exatt_ellen.cpp",
)
SOURCE_ALIASES = {
    "src/main/player/character_setup.cpp": "th03/ch_setup.cpp",
    "src/main/player/exatt_chiyuri.cpp": "th03/ex_chyu.cpp",
    "src/main/player/exatt_ellen.cpp": "th03/ex_ellen.cpp",
}
SCOPES = (
    (0x96E6, 0xA2D0),
    (0xDA43, 0xE0F7),
    (0xE266, 0xE83F),
    (0xC0D8, 0xC248),
    (0xC2F9, 0xC370),
    (0x272, 0xB50),  # Unowned library context and its natural inter-object gap.
    (0xB50, 0x2BC4),  # Unowned library body and the next natural word boundary.
    (0xA378, 0xA3FA),  # Native stage palette CODE and function alignment.
    (0xA3FA, 0xA44C),  # Existing round primitives retain their accepted owners.
    (0xA44C, 0xB37C),  # Complete native character resource/callback producer.
    (0xC248, 0xC2F9),  # Native near-this renderer, bounded separately from existing owners.
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def object_path(source):
    return "obj/th03/" + Path(SOURCE_ALIASES.get(source, source)).stem + ".obj"


def linked_objects(path=None):
    path = WORK / "obj/th03/main.@l" if path is None else path
    if not path.is_file():
        path = ROOT / "config/th03_main_link.rsp"
    return [
        name.replace(chr(92), "/")
        for name in path.read_text().split(",")[0].split()
        if name.lower().endswith(".obj")
    ]


def context_producers(names=None):
    """Resolve remaining game objects to maintained source, never cached OMF."""
    from replay_th03_main_exact_units import physical_objects, ordering_objects

    config = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    primary = {object_path(source) for source in SOURCES} | {
        "obj/th03/main.obj",
        "obj/th03/score_hud.obj",
        "c0l.obj",
    }
    producers = {
        "obj/th03/ex_rfly.obj": dict(
            source="src/main/player/exatt_flight_reimu.cpp", staged="th03/ex_rfly.cpp",
            output="obj/th03/ex_rfly.obj", prefix="", origin="authored-source",
        ),
        "obj/th03/gf_ctx.obj": dict(
            source="src/main/graphics/round_fill_context.asm", staged="th03/gf_ctx.asm",
            output="obj/th03/gf_ctx.obj", prefix="", origin="reference-game-context",
        ),
        "obj/th03/execl.obj": dict(
            source="src/main/core/execl.cpp", staged="th03/execl.cpp",
            output="obj/th03/execl.obj", prefix="", origin="authored-source",
        ),
        "obj/th03/tr_ctx.obj": dict(
            source="src/main/round/demo_transition.cpp", staged="th03/tr_ctx.cpp",
            output="obj/th03/tr_ctx.obj", prefix="", origin="authored-source",
        ),
        "obj/th03/roundpr.obj": dict(
            source="src/main/round/primitives.asm", staged="th03/roundpr.asm",
            output="obj/th03/roundpr.obj", prefix="",
        ),
        "obj/th03/stg_pal.obj": dict(
            source="src/main/graphics/stage_palette.asm", staged="th03/stg_pal.asm",
            output="obj/th03/stg_pal.obj", prefix="",
        ),
        "obj/th03/mst_pref.obj": dict(
            source="th03/mst_pref.asm", staged="th03/mst_pref.asm",
            recipe="scripts/lib/main_master_prefix.py",
            output="obj/th03/mst_pref.obj", prefix="", origin="reference-library-context",
        ),
        "obj/th03/mst_body.obj": dict(
            source="th03/mst_body.asm", staged="th03/mst_body.asm",
            recipe="scripts/lib/main_master_body.py",
            output="obj/th03/mst_body.obj", prefix="", origin="reference-library-context",
        ),
    }
    for unit in config["units"]:
        for item in physical_objects(unit) + ordering_objects(unit):
            if Path(item["source"]).suffix not in {".cpp", ".c", ".asm"}:
                continue
            output = item["object_path"]
            if output in primary:
                continue
            staged = item.get(
                "overlay_path", unit.get("overlay_path", item.get("wrapper"))
            )
            if Path(item["source"]).suffix == ".asm":
                staged = str(PurePosixPath(staged).with_suffix(".asm"))
            producer = dict(
                source=item["source"],
                staged=staged,
                output=output,
                prefix=item.get("wrapper_prefix", ""),
            )
            # The DOS compiler emits this literal 8.3 alias. Move the file only.
            if output == "obj/th03/bomb_yumemi.obj":
                producer["emitted"] = "obj/th03/bomb~cxk.obj"
            if output in producers and producers[output] != producer:
                raise ValueError("multiple context producers: " + output)
            producers[output] = producer
    names = linked_objects() if names is None else names
    missing = set(names) - primary - producers.keys()
    if missing:
        raise ValueError(
            "game objects lack a source producer: " + ", ".join(sorted(missing))
        )
    return [producers[name] for name in names if name in producers]


def stage_sources(producers=(), prepared=None, work=None):
    """Copy the complete C++/ASM include closure and whole native TU aliases."""
    prepared = prepared or {}
    work = WORK if work is None else work
    pending = list(SOURCES) + [item["source"] for item in producers] + list(prepared)
    staged = {}
    vendor = ROOT / ".analysis/toolchain/wineprefix/drive_c/TC4/INCLUDE"
    while pending:
        name = pending.pop()
        if PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts:
            raise ValueError("unsafe include path: " + name)
        if name in staged:
            continue
        if name in prepared:
            raw = prepared[name]
        else:
            source = ROOT / name
            if not source.is_file():
                source = ROOT / "_reference/ReC98" / name
            if not source.is_file() or source.is_symlink():
                raise ValueError("source unavailable: " + name)
            raw = source.read_bytes()
        staged[name] = sha(raw)
        dest = work / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        os.utime(dest, (1792656000, 1792656000))
        for line in () if name.endswith(".bmp") else raw.decode("latin1").splitlines():
            match = re.match(r"^\s*#\s*include\s+(.+)", line)
            assembly = re.match(r"^\s*include\s+([^;\s]+)", line, re.I)
            if not match and not assembly:
                continue
            if match:
                token = re.match(r'["<]([^">]+)[">]', match[1])
                if not token:
                    raise ValueError("dynamic include: " + name)
                inc = token[1]
            else:
                inc = assembly[1].strip('"<>')
            inc = inc.replace(chr(92), "/")
            choices = (posixpath.normpath(str(PurePosixPath(name).parent / inc)), inc)
            found = next(
                (
                    n
                    for n in choices
                    if not n.startswith("../")
                    and (
                        n in prepared
                        or (ROOT / n).is_file()
                        or (ROOT / "_reference/ReC98" / n).is_file()
                    )
                ),
                None,
            )
            if found:
                pending.append(found)
            elif not (vendor / inc.upper()).is_file():
                raise ValueError("unresolved include: " + name + ": " + inc)
    for source, alias in SOURCE_ALIASES.items():
        if source in SOURCES:
            dest = work / alias
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((ROOT / source).read_bytes())
            os.utime(dest, (1792656000, 1792656000))
            staged[alias] = sha(dest.read_bytes())
    for item in producers:
        dest = work / item["staged"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        source_raw = prepared.get(item["source"])
        if source_raw is None:
            source_raw = (ROOT / item["source"]).read_bytes()
        raw = item["prefix"].encode("ascii") + source_raw
        dest.write_bytes(raw)
        os.utime(dest, (1792656000, 1792656000))
        staged[item["staged"]] = sha(raw)
    return staged


def code(raw):
    return {
        s["name"]: code_bytes(raw, s["index"])[0]
        for s in segment_definitions(raw)
        if s["class"] == "CODE" and s["size"]
    }


def carrier_code(raw):
    # The ASM carrier has intentional ORG holes in _TEXT. Preserve each actual
    # data record and declared size rather than synthesizing bytes for holes.
    segments = {
        s["index"]: s for s in segment_definitions(raw)
        if s["class"] == "CODE" and s["size"]
    }
    result = {s["name"]: dict(size=s["size"], records=[]) for s in segments.values()}
    for record in parse_omf(raw):
        if record.name not in {"LEDATA", "LIDATA"}:
            continue
        segment, pos = omf_index(record.data)
        if segment in segments:
            result[segments[segment]["name"]]["records"].append((record.name, record.data[pos:]))
    return result


def contributions(raw, omit_replaced=False):
    return [
        line.strip()
        for line in raw.decode().splitlines()
        if re.fullmatch(
            r"\s*[0-9A-Fa-f]{4}:[0-9A-Fa-f]{4}\s+[0-9A-Fa-f]+\s+C=.*ACBP=\S+\s*", line
        )
        and int(line.split()[1], 16)
        and not (
            omit_replaced
            and (
                (
                    "S=PLAYER_M_TEXT" in line
                    and 0x2432 <= int(line.split()[0].split(":")[1], 16) < 0x2C90
                    and line.split()[0].startswith("096E:")
                )
                or (
                    "S=P_EXATT_TEXT" in line
                    and 0xA <= int(line.split()[0].split(":")[1], 16) < 0x845
                    and line.split()[0].startswith("18FE:")
                )
                or (
                    "S=PLAYFLD_TEXT" in line
                    and line.split()[0] in {"096E:0006", "096E:0098", "096E:03F6", "096E:0434", "096E:0B3F"}
                    and any("M=" + module + " " in line for module in
                            ("th03_main.asm", "th03/stg_rnd.cpp", "th03/rnd_loop.cpp",
                             "src/main/core/entry.cpp", "src/main/core/roundfin.cpp"))
                )
                or (
                    "S=HITCIRC_TEXT " in line
                    and line.split()[0] in {"096E:0C98", "096E:0D1A", "096E:0D6C", "096E:1C9C", "096E:1D74", "096E:1DC3"}
                    and any("M=" + module + " " in line.replace(chr(92), "/") for module in
                            ("th03_main.asm", "th03/stg_pal.asm", "th03/roundpr.asm", "th03/ch_setup.cpp", "th03/gf_ctx.asm", "th03/execl.cpp", "th03/tr_ctx.cpp", "th03/tr_ctx.asm"))
                )
                or (
                    "S=_TEXT " in line
                    and line.split()[0] in {"0000:0272", "0000:0B50", "0000:2BC4"}
                    and any("M=" + module + " " in line.replace(chr(92), "/") for module in
                            ("th03_main.asm", "th03/mst_pref.asm", "th03/mst_body.asm"))
                )
                or any("M=th03/" + module + ".cpp " in line.replace(chr(92), "/")
                       for module in ("e_ena", "e_enb", "eforna", "efornb", "eupda", "eupdb", "p_combo", "p_cmbhl"))
                or any("M=th03/" + module + ".cpp " in line.replace(chr(92), "/")
                       for module in ("ex_shfly", "ex_repre", "ex_rfly", "ex_reup"))
            )
        )
    ]


def review(previous=None, cold_build=False):
    target_raw = read_verified_artifact(
        ROOT,
        find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main"),
    )
    candidate_raw = (WORK / "bin/th03/main.exe").read_bytes()
    target, candidate = map(parse_mz, (target_raw, candidate_raw))
    if not candidate.valid:
        raise ValueError("invalid linked MZ")

    def relocations(image, lo, hi):
        return [(r.segment, r.offset) for r in image.relocations if lo <= r.linear < hi]

    def extent(lo, hi):
        return dict(
            start=lo,
            bytes=hi - lo,
            raw_equal=candidate.program_image[lo:hi] == target.program_image[lo:hi],
            ordered_relocations_equal=relocations(candidate, lo, hi)
            == relocations(target, lo, hi),
            differing_bytes=[
                lo + n
                for n, (a, b) in enumerate(
                    zip(candidate.program_image[lo:hi], target.program_image[lo:hi])
                )
                if a != b
            ],
        )

    config_raw = (ROOT / "config/th03_main_exact_units.toml").read_bytes()
    cfg = tomllib.loads(config_raw.decode())
    from lib.main_enemy_layout import verify as verify_enemy_layout
    enemy_layout = verify_enemy_layout(WORK, cfg)
    from lib.main_hitcirc_context import verify as verify_hitcirc_grouping
    hitcirc_grouping = verify_hitcirc_grouping(WORK, target, candidate)
    from lib.main_reimu_layout import verify as verify_reimu_layout
    reimu_layout = verify_reimu_layout(WORK, cfg, target, candidate)
    from lib.main_lose_layout import verify as verify_lose_layout
    lose_layout = verify_lose_layout(WORK, target, candidate)
    from lib.main_combo_layout import verify as verify_combo_layout
    combo_layout = verify_combo_layout(WORK, cfg, target, candidate)
    owned = []
    for unit in cfg["units"] + cfg.get("native_units", []):
        for e in unit.get("code_extents", [unit]):
            lo = e.get("segment", unit.get("segment", cfg["segment"])) * 16 + e["start"]
            owned.append(dict(owner=unit["id"], **extent(lo, lo + e["size"])))
    if not all(r["raw_equal"] and r["ordered_relocations_equal"] for r in owned):
        failed = [
            r for r in owned if not r["raw_equal"] or not r["ordered_relocations_equal"]
        ]
        raise ValueError("tracked scope regressed: " + json.dumps(failed))
    scopes = [extent(lo, hi) for lo, hi in SCOPES]
    if not all(s["raw_equal"] and s["ordered_relocations_equal"] for s in scopes[5:]):
        raise ValueError("native library bytes or literal relocation order differ")
    for name in (Path(object_path(s)).name for s in SOURCES) if previous else ():
        if any(
            s["size"] and s["class"] != "CODE"
            for s in segment_definitions((WORK / "obj/th03" / name).read_bytes())
        ):
            raise ValueError("candidate introduced private DATA/BSS: " + name)
    result = dict(
        target_sha256=sha(target_raw),
        executable_sha256=sha(candidate_raw),
        owned_extent_config_sha256=sha(config_raw),
        new_scopes=scopes,
        checked_owned_extents=len(owned),
        checked_owned_bytes=sum(r["bytes"] for r in owned),
        all_owned_raw_and_ordered_equal=True,
        enemy_producer_layout=enemy_layout,
        executable_chain_candidate=hitcirc_grouping,
        reimu_producer_layout=reimu_layout,
        lose_producer_layout=lose_layout,
        combo_producer_layout=combo_layout,
        character_scopes=[
            r
            for r in owned
            if r["owner"] in {"th03-main-exatt-chiyuri", "th03-main-exatt-ellen"}
        ],
        complete_program_equal=candidate.program_image == target.program_image,
        complete_relocation_membership_equal=Counter(
            (r.segment, r.offset) for r in candidate.relocations
        )
        == Counter((r.segment, r.offset) for r in target.relocations),
        complete_relocation_order_equal=candidate.relocations == target.relocations,
        differing_relocation_order_positions=sum(
            a != b for a, b in zip(candidate.relocations, target.relocations)
        ),
        matching_relocation_prefix=next(
            (i for i, (a, b) in enumerate(zip(candidate.relocations, target.relocations)) if a != b),
            min(len(candidate.relocations), len(target.relocations)),
        ),
        complete_program_differing_bytes=[
            i
            for i, (a, b) in enumerate(
                zip(candidate.program_image, target.program_image)
            )
            if a != b
        ],
        candidate_relocations=len(candidate.relocations),
        target_relocations=len(target.relocations),
        candidate_program_bytes=len(candidate.program_image),
        target_program_bytes=len(target.program_image),
        program_size_equal=len(candidate.program_image) == len(target.program_image),
        file_equal=candidate_raw == target_raw,
        mixed_context=True,
        cold_build=cold_build,
        exact_acceptance=False,
        state_stage_relocation_order={
            name: [r.linear for r in image.relocations if 0xDA43 <= r.linear < 0xE313]
            for name, image in (("target", target), ("candidate", candidate))
        },
        stage_round_candidate=dict(
            **extent(0x9AD6, 0xA21F),
            exact_acceptance=False,
            target_order=[
                r.linear for r in target.relocations if 0x9AD6 <= r.linear < 0xA21F
            ],
            candidate_order=[
                r.linear for r in candidate.relocations if 0x9AD6 <= r.linear < 0xA21F
            ],
        ),
        round_loop_candidate=dict(
            **extent(0x9778, 0x9AD6),
            exact_acceptance=False,
            target_order=relocations(target, 0x9778, 0x9AD6),
            candidate_order=relocations(candidate, 0x9778, 0x9AD6),
        ),
        entry_loop_producer=dict(
            **extent(0x96E6, 0x9AD6),
            target_order=relocations(target, 0x96E6, 0x9AD6),
            candidate_order=relocations(candidate, 0x96E6, 0x9AD6),
        ),
        main_flow_producer=dict(
            **extent(0x96E6, 0xA2D0),
            target_order=relocations(target, 0x96E6, 0xA2D0),
            candidate_order=relocations(candidate, 0x96E6, 0xA2D0),
        ),
        shared_producers=dict(
            **extent(0xE8F8, 0xF1FA),
            target_order=relocations(target, 0xE8F8, 0xF1FA),
            candidate_order=relocations(candidate, 0xE8F8, 0xF1FA),
            exact_acceptance=False,  # EC2D alignment still differs from target.
        ),
        character_setup_producer=extent(0xA44C, 0xB37C),
        round_primitives_producer=extent(0xA3FA, 0xA44C),
    )
    joint = result["entry_loop_producer"]
    if not joint["raw_equal"] or not joint["ordered_relocations_equal"]:
        raise ValueError("entry/loop producer bytes or literal order differ")
    flow = result["main_flow_producer"]
    if not flow["raw_equal"] or not flow["ordered_relocations_equal"]:
        raise ValueError("main flow producer bytes or literal order differ")
    if not result["shared_producers"]["ordered_relocations_equal"]:
        raise ValueError("SHARED native producer relocation order differs")
    if result["matching_relocation_prefix"] < 1072:
        raise ValueError("startup, flow, library, SHARED and loader relocation prefix differs")
    for row in result["character_scopes"]:
        lo, hi = row["start"], row["start"] + row["bytes"]
        row["target_relative_relocation_order"] = [
            seg * 16 + offset - lo for seg, offset in relocations(target, lo, hi)
        ]
        row["candidate_relative_relocation_order"] = [
            seg * 16 + offset - lo for seg, offset in relocations(candidate, lo, hi)
        ]
    sites = [r.linear for r in target.relocations if 0x96E6 <= r.linear < 0xE8F8]
    uniform = sorted(sites, key=lambda p: ((p - 0x96E6) // 1023, -p))
    result["main01_uniform_1023_record_model"] = dict(
        sites=len(sites),
        different_positions=sum(a != b for a, b in zip(sites, uniform)),
        equal=sites == uniform,
    )
    if previous:
        before = parse_mz(previous["exe"])
        old_entry = code(previous["objects"]["entry.obj"])
        new_entry = code((WORK / "obj/th03/entry.obj").read_bytes())
        retired = {n for n in ("stg_rnd.obj", "roundfin.obj") if n in previous["objects"]}
        merge = bool(retired)
        if merge:
            if retired != {"stg_rnd.obj", "roundfin.obj"}:
                raise ValueError("incomplete prior main flow producer set")
            old_stage = code(previous["objects"]["stg_rnd.obj"])
            old_finish = code(previous["objects"]["roundfin.obj"])
            if (set(old_entry) != {"PLAYFLD_TEXT"}
                    or set(old_stage) != {"PLAYFLD_TEXT"}
                    or set(old_finish) != {"PLAYFLD_TEXT"}
                    or set(new_entry) != {"PLAYFLD_TEXT"}
                    or [len(old_entry["PLAYFLD_TEXT"]), len(old_stage["PLAYFLD_TEXT"]),
                        len(old_finish["PLAYFLD_TEXT"]), len(new_entry["PLAYFLD_TEXT"])]
                    != [1008, 1865, 177, 3050]
                    or before.program_image[0x96E6:0xA2D0]
                    != candidate.program_image[0x96E6:0xA2D0]):
                raise ValueError("main flow transfer changed owned bytes or layout")
        from lib.main_enemy_layout import RETIRED
        enemy_retired = {Path(n).name for n in previous.get("game_objects", {})} & RETIRED
        if enemy_retired:
            if enemy_retired != RETIRED or before.program_image != candidate.program_image:
                raise ValueError("enemy producer transfer changed loaded bytes")
            retired.update(enemy_retired)
            result["enemy_producer_transfer"] = dict(
                retired=sorted(enemy_retired), loaded_image_unchanged=True,
                new_layout=enemy_layout,
            )
        reimu_retired = {Path(n).name for n in previous.get("game_objects", {})} & {
            "ex_shfly.obj", "ex_repre.obj"
        }
        if reimu_retired:
            if reimu_retired != {"ex_shfly.obj", "ex_repre.obj"} or before.program_image != candidate.program_image:
                raise ValueError("flight/Reimu transfer changed loaded bytes")
            retired.update(reimu_retired)
            result["reimu_producer_transfer"] = dict(
                retired=sorted(reimu_retired), loaded_image_unchanged=True,
                new_layout=reimu_layout,
            )
        loss_regroup = ("defeat.obj" in previous["objects"] or any(
            Path(n).name == "defeat.obj" for n in previous.get("game_objects", {})))
        if loss_regroup:
            if before.program_image != candidate.program_image:
                raise ValueError("loss producer transfer changed loaded bytes")
            retired.add("defeat.obj")
            result["lose_producer_transfer"] = dict(loaded_image_unchanged=True, new_layout=lose_layout)
        result["retired_objects"] = sorted(retired)
        result["map_contributions_unchanged"] = contributions(
            previous["map"]
        ) == contributions((WORK / "obj/th03/main.map").read_bytes())
        result["map_other_contributions_unchanged"] = contributions(
            previous["map"], omit_replaced=True
        ) == contributions(
            (WORK / "obj/th03/main.map").read_bytes(), omit_replaced=True
        )
        map_text = (WORK / "obj/th03/main.map").read_text().replace(chr(92), "/")
        prefix_pattern = (
            r"(?m)^\s*0000:0272\s+08DD\s+C=CODE\s+S=_TEXT\s+G=\(none\)\s+"
            r"M=th03/mst_pref\.asm\s+ACBP=48\s*$"
        )
        if len(re.findall(prefix_pattern, map_text)) != 1:
            raise ValueError("native library prefix ownership differs")
        for start, size, module in ((0xB50, 8307, "th03/mst_body.asm"),
                                    (0x2BC4, 748, "th03_main.asm")):
            pattern = (
                rf"(?m)^\s*0000:{start:04X}\s+{size:04X}\s+C=CODE\s+S=_TEXT\s+G=\(none\)\s+"
                rf"M={re.escape(module)}\s+ACBP=48\s*$"
            )
            if len(re.findall(pattern, map_text)) != 1:
                raise ValueError("native library body ownership differs: " + module)
        body_raw = (WORK / "obj/th03/mst_body.obj").read_bytes()
        if [(s["name"], s["class"], s["size"]) for s in segment_definitions(body_raw)
                if s["size"]] != [("_TEXT", "CODE", 8307)]:
            raise ValueError("native library body introduced CODE or private DATA/BSS")
        for start, size, module in ((0xD1A, 82, "th03/roundpr.asm"),):
            pattern = (rf"(?m)^\s*096E:{start:04X}\s+{size:04X}\s+C=CODE\s+S=HITCIRC_TEXT\s+G=MAIN_01\s+"
                       rf"M={re.escape(module)}\s+ACBP=48\s*$")
            if len(re.findall(pattern, map_text)) != 1:
                raise ValueError("native HITCIRC ownership differs: " + module)
        primitive_raw = (WORK / "obj/th03/roundpr.obj").read_bytes()
        if [(s["name"], s["class"], s["size"]) for s in segment_definitions(primitive_raw)
                if s["size"]] != [("HITCIRC_TEXT", "CODE", 82)]:
            raise ValueError("native round primitives changed layout or allocated storage")
        for seg, start, size, segment, group, module in (
            (0x96E, 0xD6C, 3888, "HITCIRC_TEXT", "MAIN_01", "th03/ch_setup.cpp"),
            (0x96E, 0x6, 3050, "PLAYFLD_TEXT", "MAIN_01", "src/main/core/entry.cpp"),
            (0x96E, 0x2432, 1478, "PLAYER_M_TEXT", "MAIN_01", "src/main/hud/intro.cpp"),
            (
                0x96E,
                0x29F8,
                664,
                "PLAYER_M_TEXT",
                "MAIN_01",
                "src/main/player/lose.cpp",
            ),
            (0x18FE, 0xA, 978, "P_EXATT_TEXT", "MAIN_06", "th03/ex_chyu.cpp"),
            (0x18FE, 0x3DC, 1129, "P_EXATT_TEXT", "MAIN_06", "th03/ex_ellen.cpp"),
        ):
            pattern = (
                rf"(?m)^\s*{seg:04X}:{start:04X}\s+{size:04X}\s+C=CODE\s+"
                rf"S={segment}\s+G={re.escape(group)}\s+M={re.escape(module)}\s+ACBP=28\s*$"
            )
            if len(re.findall(pattern, map_text)) != 1:
                raise ValueError("source contribution layout differs: " + module)
        result["outside_new_scopes_unchanged"] = len(before.program_image) == len(
            candidate.program_image
        ) and all(
            a == b
            for i, (a, b) in enumerate(
                zip(before.program_image, candidate.program_image)
            )
            if not any(lo <= i < hi for lo, hi in SCOPES)
        )
        result["executable_repeats_previous"] = previous["exe"] == candidate_raw
        result["object_repeats_previous"] = {
            n: raw == (WORK / "obj/th03" / n).read_bytes()
            for n, raw in previous["objects"].items()
            if n not in retired
        }
        if "game_objects" in previous:
            result["game_object_repeats_previous"] = {
                name: raw == (WORK / name).read_bytes()
                for name, raw in previous["game_objects"].items()
                if Path(name).name not in retired
            }
        result["unlinked_CODE_unchanged"] = {
            n: code(raw) == code((WORK / "obj/th03" / n).read_bytes())
            for n, raw in previous["objects"].items()
            if n not in {"ex_chyu.obj", "ex_ellen.obj", "main.obj", "mst_body.obj"}
            and n not in retired and not (merge and n == "entry.obj")
            and not (loss_regroup and n == "lose.obj")
        }
        # Keep native game producers unchanged while the carrier externalizes
        # library references. A cold repeat also checks the complete carrier.
        if "main.obj" in previous["objects"]:
            old_root_raw = previous["objects"]["main.obj"]
            new_root_raw = (WORK / "obj/th03/main.obj").read_bytes()
            old_root = carrier_code(old_root_raw)
            new_root = carrier_code(new_root_raw)
            if "mst_body.obj" in previous["objects"]:
                result["unlinked_CODE_unchanged"]["library_body"] = (
                    carrier_code(previous["objects"]["mst_body.obj"]) == carrier_code(body_raw)
                )
            else:
                result["library_body_transfer"] = (
                    (old_root["_TEXT"]["size"], new_root["_TEXT"]["size"]) == (9056, 748)
                    and before.program_image == candidate.program_image
                )
                if not result["library_body_transfer"]:
                    raise ValueError("library body transfer changed linked bytes or layout")
            old_hitcirc_size = old_root.get("HITCIRC_TEXT", {}).get("size", 0)
            new_hitcirc_size = new_root.get("HITCIRC_TEXT", {}).get("size", 0)
            hitcirc_transfer = old_hitcirc_size != new_hitcirc_size
            lose_transfer = old_root.get("PLAYER_M_TEXT", {}).get("size", 0) != new_root.get("PLAYER_M_TEXT", {}).get("size", 0)
            if lose_transfer:
                result["carrier_lose_transfer"] = (
                    (old_root.get("PLAYER_M_TEXT", {}).get("size", 0), new_root.get("PLAYER_M_TEXT", {}).get("size", 0)) == (177, 0)
                    and {k: v for k, v in old_root.items() if k != "PLAYER_M_TEXT"} == new_root
                    and before.program_image == candidate.program_image)
                if not result["carrier_lose_transfer"]:
                    raise ValueError("loss transfer altered unrelated carrier CODE")
            elif hitcirc_transfer:
                result["carrier_hitcirc_transfer"] = (
                    (old_hitcirc_size, new_hitcirc_size) in {(5058, 4928), (4928, 958), (958, 0)}
                    and {k: v["size"] for k, v in old_root.items() if k != "HITCIRC_TEXT"}
                    == {k: v["size"] for k, v in new_root.items() if k != "HITCIRC_TEXT"}
                    and before.program_image == candidate.program_image
                )
                if not result["carrier_hitcirc_transfer"]:
                    raise ValueError("HITCIRC transfer changed linked bytes or layout")
            elif ("mst_pref.obj" in previous["objects"]
                    and old_root["_TEXT"]["size"] == new_root["_TEXT"]["size"]):
                result["unlinked_CODE_unchanged"]["carrier"] = old_root == new_root
            else:
                # Externalizing library names changes unlinked fixup operands.
                # Enforce unchanged non-library CODE layout and every linked
                # byte outside the declared prefix scope instead.
                result["carrier_library_transfer"] = {
                    k: v["size"] for k, v in old_root.items() if k != "_TEXT"
                } == {k: v["size"] for k, v in new_root.items() if k != "_TEXT"}
                if not result["carrier_library_transfer"]:
                    raise ValueError("library transfer altered game CODE layout")
        pair = ("ex_chyu.obj", "ex_ellen.obj")
        if all(n in previous["objects"] for n in pair):
            result["exatt_combined_CODE_unchanged"] = b"".join(
                code(previous["objects"][n])["P_EXATT_TEXT"] for n in pair
            ) == b"".join(
                code((WORK / "obj/th03" / n).read_bytes())["P_EXATT_TEXT"] for n in pair
            )
        if (
            not result["map_other_contributions_unchanged"]
            or not result["outside_new_scopes_unchanged"]
            or not all(result["unlinked_CODE_unchanged"].values())
            or not result.get("exatt_combined_CODE_unchanged", True)
        ):
            raise ValueError("source replacement altered layout or unrelated bytes")
    return result


def build(rebuild_context=False, cold=False):
    from lib.main_work_stage import stage_carriers, generate_sprites, recipe_hashes

    rebuild_context = rebuild_context or cold
    OUT.mkdir(parents=True, exist_ok=True)
    prefix = ROOT / ".analysis/toolchain/wineprefix"
    env = dict(
        PATH="/usr/bin:/bin",
        HOME="/tmp/home",
        LANG="C",
        LC_ALL="C",
        TZ="UTC",
        DISPLAY="",
        WAYLAND_DISPLAY="",
        WINEDEBUG="-all",
        WINEPREFIX=str(prefix),
        MSDOS_PATH=r"C:\TC4\BIN",
    )
    dos = [
        "/usr/bin/wine-stable",
        str(ROOT / "_reference/ReC98/bin/msdos.exe"),
        "-e",
        "-x",
    ]
    compiler = dos + [
        "tcc",
        "-c",
        "-I.",
        "-O",
        "-b-",
        "-3",
        "-Z",
        "-d",
        "-DGAME=3",
        "-ml",
        "-DBINARY='M'",
        "-nobj/th03/",
    ]
    phases = [
        (compiler + [SOURCE_ALIASES.get(n, n)], [object_path(n)]) for n in SOURCES
    ]
    tasm = [
        "/usr/bin/wine-stable",
        str(prefix / "drive_c/TASM50/bin/TASM32.EXE"),
        "/m",
        "/mx",
        "/kh32768",
        "/t",
        "/dGAME=3",
    ]
    phases += [
        (tasm + ["th03_main.asm", r"obj\th03\main.obj"], ["obj/th03/main.obj"]),
        (
            tasm + [r"src\main\hud\score.asm", r"obj\th03\score_hud.obj"],
            ["obj/th03/score_hud.obj"],
        ),
        (
            dos + ["tlink", r"@obj\th03\main.@l"],
            ["bin/th03/main.exe", "obj/th03/main.map"],
        ),
    ]
    report = dict(
        complete=False,
        native_phases=[],
        mixed_context=True,
        cold_build=cold,
        exact_acceptance=False,
        rebuild_game_context=rebuild_context,
    )
    with (ROOT / ".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        prior_report = None
        prior_report_sha = None
        report_file = OUT / "main-build.json"
        if report_file.is_file():
            prior_raw = report_file.read_bytes()
            prior_report = json.loads(prior_raw)
            prior_report_sha = sha(prior_raw)
        report["recipe_sha256"] = recipe_hashes()
        previous = None
        if (prior_report is None or prior_report.get("complete")) and all(
            (WORK / name).is_file()
            for name in (
                "bin/th03/main.exe",
                "obj/th03/main.map",
            )
        ):
            previous = dict(
                exe=(WORK / "bin/th03/main.exe").read_bytes(),
                map=(WORK / "obj/th03/main.map").read_bytes(),
                objects={
                    n: (WORK / "obj/th03" / n).read_bytes()
                    for n in [*(Path(object_path(s)).name for s in SOURCES), "main.obj", "mst_pref.obj", "mst_body.obj", "stg_pal.obj", "roundpr.obj", "stg_rnd.obj", "roundfin.obj"]
                    if (WORK / "obj/th03" / n).is_file()
                },
            )
            if rebuild_context:
                previous["game_objects"] = {
                    name: (WORK / name).read_bytes()
                    for name in linked_objects()
                    if (WORK / name).is_file()
                }

        if WORK.is_symlink():
            raise ValueError("MAIN working tree must be a real directory")
        WORK.parent.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory(dir=WORK.parent, prefix=".TH03SOURCE-") as fresh:
            destination = Path(fresh) if cold else WORK
            prepared = stage_carriers(destination)
            generated, report["source_generation"] = generate_sprites(destination)
            prepared.update(generated)
            names = linked_objects(destination / "obj/th03/main.@l")
            producers = context_producers(names) if rebuild_context else []
            report["staged_source_sha256"] = stage_sources(
                producers, prepared, work=destination
            )
            if cold:
                if list(destination.rglob("*.obj")) or list(destination.rglob("*.exe")):
                    raise ValueError(
                        "fresh source staging contains cached build outputs"
                    )
                if WORK.exists():
                    shutil.rmtree(WORK)
                destination.rename(WORK)
                report["source_tree_recreated"] = True
                report["initial_cached_game_objects"] = 0
        moves = {
            item["output"]: item["emitted"] for item in producers if "emitted" in item
        }
        if producers:
            context_phases = []
            for item in producers:
                source, output = item["staged"], item["output"]
                (WORK / output).parent.mkdir(parents=True, exist_ok=True)
                argv = (
                    tasm
                    + [
                        source.replace(chr(47), chr(92)),
                        output.replace(chr(47), chr(92)),
                    ]
                    if source.endswith(".asm")
                    else compiler[:-1]
                    + ["-n" + str(PurePosixPath(output).parent) + "/", source]
                )
                context_phases.append((argv, [output]))
            phases = context_phases + phases
        report["builder_sha256"] = sha(Path(__file__).read_bytes())
        produced = {object_path(s) for s in SOURCES} | {
            "obj/th03/main.obj",
            "obj/th03/score_hud.obj",
        }
        produced.update(item["output"] for item in producers)
        report["context_source_producers"] = producers
        context = {}
        for name in linked_objects():
            if name in produced:
                continue
            path = WORK / name
            if not path.is_file():
                path = prefix / "drive_c/TC4/LIB" / name.upper()
            context[name] = sha(path.read_bytes())
        report["retained_context_object_sha256"] = context
        report["tools_sha256"] = {
            str(p.relative_to(ROOT)): sha(p.read_bytes())
            for p in (
                prefix / "drive_c/TC4/BIN/TCC.EXE",
                prefix / "drive_c/TC4/BIN/TLINK.EXE",
                prefix / "drive_c/TASM50/bin/TASM32.EXE",
                ROOT / "_reference/ReC98/bin/msdos.exe",
            )
        }
        with (OUT / "main-build.log").open("wb") as log:
            rollback = (
                previous["game_objects"]
                if cold and previous
                else {
                    name: (WORK / name).read_bytes()
                    for name in produced
                    if (WORK / name).is_file()
                }
                if rebuild_context
                else {}
            )
            try:
                if rebuild_context:
                    for name in produced | set(moves.values()):
                        (WORK / name).unlink(missing_ok=True)
                    report["cached_game_objects_used"] = 0
                for argv, outputs in phases:
                    for n in outputs:
                        (WORK / n).parent.mkdir(parents=True, exist_ok=True)
                        (WORK / n).unlink(missing_ok=True)
                    start = time.monotonic()
                    child = subprocess.Popen(
                        argv,
                        cwd=WORK,
                        env=env,
                        stdout=log,
                        stderr=subprocess.STDOUT,
                        start_new_session=True,
                    )
                    try:
                        status = child.wait(timeout=90)
                    except subprocess.TimeoutExpired:
                        os.killpg(child.pid, signal.SIGTERM)
                        try:
                            child.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            os.killpg(child.pid, signal.SIGKILL)
                            child.wait(timeout=5)
                        raise RuntimeError("native phase timed out")
                    phase = dict(
                        argv=argv,
                        exit_code=status,
                        seconds=round(time.monotonic() - start, 3),
                    )
                    report["native_phases"].append(phase)
                    for output in outputs:
                        if output in moves:
                            origin = WORK / moves[output]
                            if origin.is_file():
                                digest = sha(origin.read_bytes())
                                origin.replace(WORK / output)
                                phase["filename_only_move"] = dict(
                                    emitted=moves[output],
                                    linked=output,
                                    sha256=digest,
                                )
                    if status or not all((WORK / n).is_file() for n in outputs):
                        raise RuntimeError(
                            "native phase failed; see .analysis/work/main-build.log"
                        )
                    phase["output_sha256"] = {
                        n: sha((WORK / n).read_bytes()) for n in outputs
                    }
                report["native_outputs_unchanged"] = all(
                    sha((WORK / n).read_bytes()) == digest
                    for phase in report["native_phases"]
                    for n, digest in phase["output_sha256"].items()
                )
                if not report["native_outputs_unchanged"]:
                    raise ValueError(
                        "native compiler/assembler/linker output was modified"
                    )
                report["staged_sources_unchanged"] = all(
                    sha((WORK / name).read_bytes()) == digest
                    for name, digest in report["staged_source_sha256"].items()
                )
                if not report["staged_sources_unchanged"]:
                    raise ValueError("source input changed during the native build")
                report["character_producers"] = {}
                for name in ("ex_chyu", "ex_ellen"):
                    raw = (WORK / "obj/th03" / (name + ".obj")).read_bytes()
                    segment = next(
                        s
                        for s in segment_definitions(raw)
                        if s["name"] == "P_EXATT_TEXT"
                    )
                    report["character_producers"][name] = dict(
                        code_bytes=segment["size"],
                        code_record_sizes=[
                            r["size"] for r in code_bytes(raw, segment["index"])[1]
                        ],
                    )
                report["comparison"] = review(previous, cold_build=cold)
                for retired in report["comparison"].get("retired_objects", []):
                    (WORK / "obj/th03" / retired).unlink(missing_ok=True)
                eligible = (
                    cold
                    and previous is not None
                    and prior_report is not None
                    and prior_report.get("complete")
                    and prior_report.get("cold_build")
                    and prior_report.get("builder_sha256") == report["builder_sha256"]
                    and prior_report.get("recipe_sha256") == report["recipe_sha256"]
                    and prior_report.get("staged_source_sha256")
                    == report["staged_source_sha256"]
                    and prior_report.get("tools_sha256") == report["tools_sha256"]
                )
                if eligible:
                    prior_outputs = {
                        name: digest
                        for phase in prior_report["native_phases"]
                        for name, digest in phase["output_sha256"].items()
                    }
                    raw_repeat = {
                        name: sha((WORK / name).read_bytes()) == digest
                        for name, digest in prior_outputs.items()
                    }
                    report["cold_reproducibility"] = dict(
                        previous_report_sha256=prior_report_sha,
                        independent_source_trees=True,
                        same_source_inputs=True,
                        raw_output_repeat=raw_repeat,
                        complete=len(raw_repeat) == len(produced) + 2
                        and all(raw_repeat.values()),
                    )
                    if not report["cold_reproducibility"]["complete"]:
                        raise ValueError("independent cold output vector differs")
                report["complete"] = True
            except Exception:
                if rebuild_context:
                    for name, raw in rollback.items():
                        (WORK / name).parent.mkdir(parents=True, exist_ok=True)
                        (WORK / name).write_bytes(raw)
                    if previous:
                        (WORK / "bin/th03").mkdir(parents=True, exist_ok=True)
                        (WORK / "bin/th03/main.exe").write_bytes(previous["exe"])
                        (WORK / "obj/th03/main.map").write_bytes(previous["map"])
                        report["restored_previous_build"] = True
                    else:
                        (WORK / "bin/th03/main.exe").unlink(missing_ok=True)
                        (WORK / "obj/th03/main.map").unlink(missing_ok=True)
                raise
            finally:
                (OUT / "main-build.json").write_text(
                    json.dumps(report, indent=2) + "\n"
                )
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--cold",
        action="store_true",
        help="recreate the entire working tree from source and rebuild all game objects",
    )
    p.add_argument(
        "--rebuild-context",
        action="store_true",
        help="rebuild all game context OBJs from the maintained source recipe",
    )
    p.add_argument(
        "--build",
        action="store_true",
        help="compile maintained candidates, assemble root/score, and relink",
    )
    p.add_argument(
        "--runtime",
        action="store_true",
        help="also compare bounded entry behavior with the target",
    )
    args = p.parse_args()
    if args.rebuild_context and not args.build:
        p.error("--rebuild-context requires --build")
    if args.cold and not args.build:
        p.error("--cold requires --build")
    result = build(args.rebuild_context, args.cold) if args.build else review()
    if args.runtime:
        from lib.main_entry_runtime import compare
        from lib.main_lose_runtime import (
            compare as compare_lose,
            negative_controls as lose_controls,
        )
        from lib.main_entry_runtime import negative_controls

        target = parse_mz(
            read_verified_artifact(
                ROOT,
                find_artifact(
                    load_target_manifest(ROOT / "config/targets.toml"), "th03-main"
                ),
            )
        )
        candidate = parse_mz((WORK / "bin/th03/main.exe").read_bytes())
        result["entry_runtime"] = compare(target, candidate)
        result["entry_negative_controls"] = negative_controls(candidate)
        result["lose_runtime"] = compare_lose(target, candidate)
        result["lose_negative_controls"] = lose_controls(candidate)
        if args.build:
            (OUT / "main-build.json").write_text(json.dumps(result, indent=2) + "\n")
    if not args.build:
        (OUT / "main-check.json").write_text(json.dumps(result, indent=2) + "\n")
    comparison = result["comparison"] if args.build else result
    print(
        json.dumps(
            {
                k: comparison[k]
                for k in (
                    "new_scopes",
                    "checked_owned_extents",
                    "checked_owned_bytes",
                    "complete_program_differing_bytes",
                    "candidate_relocations",
                    "target_relocations",
                    "complete_relocation_order_equal",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
