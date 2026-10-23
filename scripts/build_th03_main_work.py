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
import subprocess
import time
import tomllib

from lib.pc98 import parse_mz
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact
from probe_th03_main_bomb_rikako_cpp import segment_definitions, code_bytes

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03WORK"
OUT = ROOT / ".analysis/work"
SOURCES = (
    "src/main/core/entry.cpp",
    "src/main/player/state.cpp",
    "src/main/player/shotroot.cpp",
    "src/main/player/lose.cpp",
    "src/main/player/defeat.cpp",
)
SCOPES = (
    (0x96E6, 0x9778),
    (0xDA43, 0xE0F7),
    (0xE266, 0xE83F),
    (0xC0D8, 0xC248),
    (0xC2F9, 0xC370),
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def stage_lose():
    """Replace three whole carrier procedures, leaving the unresolved renderer."""
    path = WORK / "th03_main.asm"
    text = path.read_text(encoding="latin1")
    for label, symbol in (
        ("sub_C0D8", "@PLAYER_LOSE_ANIM_UPDATE$QP14PLAYER_STUFF_T"),
        ("sub_C1E6", "@PLAYER_LOSE_PARTICLE_PUT$QUCUC"),
        ("sub_C2F9", "@round_defeat_banners_render$qv"),
    ):
        pattern = rf"(?m)^{label}\s+proc near\n.*?^{label}\s+endp\n"
        text, count = re.subn(pattern, f"extern {symbol}:near\n", text, flags=re.S)
        if count != 1 and f"extern {symbol}:near" not in text:
            raise ValueError("lose carrier procedure unavailable: " + label)
        text = text.replace(f"public {symbol}\n{symbol} label near\n", "")
        text = re.sub(rf"\b{label}\b", lambda _: symbol, text)
    for old, alias in (
        ("word_20E3E", "_player_lose_left"),
        ("word_20E40", "_player_lose_top"),
        ("word_20E42", "_player_lose_radius"),
    ):
        if f"{alias} label word" not in text:
            text, count = re.subn(
                rf"(?m)^({old}\s+dw \?)$",
                f"public {alias}\n{alias} label word\n\\1",
                text,
            )
            if count != 1:
                raise ValueError("lose storage alias unavailable: " + alias)
    path.write_bytes(text.replace("\n", "\r\n").encode("latin1"))
    response = WORK / "obj/th03/main.@l"
    text = response.read_text()
    main = r"obj\th03\main.obj"
    if r"obj\th03\lose.obj" not in text:
        if text.count(main) != 1:
            raise ValueError("MAIN response anchor unavailable")
        text = text.replace(
            main, r"obj\th03\lose.obj " + main + r" obj\th03\defeat.obj"
        )
    response.write_bytes(text.replace("\n", "\r\n").encode())


def stage_sources():
    """Copy just the conservative C++ include closure, leaving root ASM/context intact."""
    pending = list(SOURCES)
    staged = {}
    vendor = ROOT / ".analysis/toolchain/wineprefix/drive_c/TC4/INCLUDE"
    while pending:
        name = pending.pop()
        if PurePosixPath(name).is_absolute() or ".." in PurePosixPath(name).parts:
            raise ValueError("unsafe include path: " + name)
        if name in staged:
            continue
        source = ROOT / name
        if not source.is_file():
            source = ROOT / "_reference/ReC98" / name
        if not source.is_file() or source.is_symlink():
            raise ValueError("source unavailable: " + name)
        raw = source.read_bytes()
        staged[name] = sha(raw)
        dest = WORK / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw)
        os.utime(dest, (1792656000, 1792656000))
        for line in raw.decode("latin1").splitlines():
            match = re.match(r"^\s*#\s*include\s+(.+)", line)
            if not match:
                continue
            token = re.match(r'["<]([^">]+)[">]', match[1])
            if not token:
                raise ValueError("dynamic include: " + name)
            inc = token[1].replace("\\", "/")
            choices = (posixpath.normpath(str(PurePosixPath(name).parent / inc)), inc)
            found = next(
                (
                    n
                    for n in choices
                    if not n.startswith("../")
                    and (
                        (ROOT / n).is_file()
                        or (ROOT / "_reference/ReC98" / n).is_file()
                    )
                ),
                None,
            )
            if found:
                pending.append(found)
            elif not (vendor / inc.upper()).is_file():
                raise ValueError("unresolved include: " + name + ": " + inc)
    return staged


def code(raw):
    return {
        s["name"]: code_bytes(raw, s["index"])[0]
        for s in segment_definitions(raw)
        if s["class"] == "CODE" and s["size"]
    }


def contributions(raw, outside_lose=False):
    return [
        line.strip()
        for line in raw.decode().splitlines()
        if re.fullmatch(
            r"\s*[0-9A-Fa-f]{4}:[0-9A-Fa-f]{4}\s+[0-9A-Fa-f]+\s+C=.*ACBP=\S+\s*", line
        )
        and int(line.split()[1], 16)
        and not (
            outside_lose
            and "S=PLAYER_M_TEXT" in line
            and 0x29F8 <= int(line.split()[0].split(":")[1], 16) < 0x2C90
            and line.split()[0].startswith("096E:")
        )
    ]


def review(previous=None):
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

    cfg = tomllib.loads((ROOT / "config/th03_main_exact_units.toml").read_text())
    accepted = []
    for unit in cfg["units"]:
        for e in unit.get("code_extents", [unit]):
            lo = e.get("segment", unit.get("segment", cfg["segment"])) * 16 + e["start"]
            accepted.append(dict(owner=unit["id"], **extent(lo, lo + e["size"])))
    if not all(r["raw_equal"] and r["ordered_relocations_equal"] for r in accepted):
        raise ValueError("previously accepted scope regressed")
    scopes = [extent(lo, hi) for lo, hi in SCOPES]
    for name in (Path(s).stem + ".obj" for s in SOURCES) if previous else ():
        if any(
            s["size"] and s["class"] != "CODE"
            for s in segment_definitions((WORK / "obj/th03" / name).read_bytes())
        ):
            raise ValueError("candidate introduced private DATA/BSS: " + name)
    result = dict(
        target_sha256=sha(target_raw),
        executable_sha256=sha(candidate_raw),
        new_scopes=scopes,
        checked_accepted_extents=len(accepted),
        checked_accepted_bytes=sum(r["bytes"] for r in accepted),
        all_accepted_raw_and_ordered_equal=True,
        complete_program_equal=candidate.program_image == target.program_image,
        complete_relocation_membership_equal=Counter(
            (r.segment, r.offset) for r in candidate.relocations
        )
        == Counter((r.segment, r.offset) for r in target.relocations),
        complete_relocation_order_equal=candidate.relocations == target.relocations,
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
        cold_build=False,
        exact_acceptance=False,
        state_stage_relocation_order={
            name: [r.linear for r in image.relocations if 0xDA43 <= r.linear < 0xE313]
            for name, image in (("target", target), ("candidate", candidate))
        },
    )
    sites = [r.linear for r in target.relocations if 0x96E6 <= r.linear < 0xE8F8]
    uniform = sorted(sites, key=lambda p: ((p - 0x96E6) // 1023, -p))
    result["main01_uniform_1023_record_model"] = dict(
        sites=len(sites),
        different_positions=sum(a != b for a, b in zip(sites, uniform)),
        equal=sites == uniform,
    )
    if previous:
        before = parse_mz(previous["exe"])
        result["map_contributions_unchanged"] = contributions(
            previous["map"]
        ) == contributions((WORK / "obj/th03/main.map").read_bytes())
        result["map_contributions_outside_lose_unchanged"] = contributions(
            previous["map"], outside_lose=True
        ) == contributions((WORK / "obj/th03/main.map").read_bytes(), outside_lose=True)
        map_text = (WORK / "obj/th03/main.map").read_text()
        for start, size, module in (
            (0x29F8, 368, "src/main/player/lose.cpp"),
            (0x2B68, 177, "th03_main.asm"),
            (0x2C19, 119, "src/main/player/defeat.cpp"),
        ):
            pattern = (
                rf"(?m)^\s*096E:{start:04X}\s+{size:04X}\s+C=CODE\s+"
                rf"S=PLAYER_M_TEXT\s+G=MAIN_01\s+M={re.escape(module)}\s+ACBP=28\s*$"
            )
            if len(re.findall(pattern, map_text)) != 1:
                raise ValueError("lose contribution layout differs: " + module)
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
        }
        result["unlinked_CODE_unchanged"] = {
            n: code(raw) == code((WORK / "obj/th03" / n).read_bytes())
            for n, raw in previous["objects"].items()
        }
        if (
            not result["map_contributions_outside_lose_unchanged"]
            or not result["outside_new_scopes_unchanged"]
            or not all(result["unlinked_CODE_unchanged"].values())
        ):
            raise ValueError("source replacement altered layout or unrelated bytes")
    return result


def build():
    if not (WORK / "th03_main.asm").is_file():
        raise ValueError("current MAIN working tree unavailable")
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
    phases = [(compiler + [n], ["obj/th03/" + Path(n).stem + ".obj"]) for n in SOURCES]
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
        cold_build=False,
        exact_acceptance=False,
    )
    with (ROOT / ".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        previous = None
        if all(
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
                    for n in (Path(s).stem + ".obj" for s in SOURCES)
                    if (WORK / "obj/th03" / n).is_file()
                },
            )

        report["builder_sha256"] = sha(Path(__file__).read_bytes())
        produced = {
            "obj/th03/entry.obj",
            "obj/th03/state.obj",
            "obj/th03/shotroot.obj",
            "obj/th03/lose.obj",
            "obj/th03/defeat.obj",
            "obj/th03/main.obj",
            "obj/th03/score_hud.obj",
        }
        report["staged_source_sha256"] = stage_sources()
        stage_lose()
        for name in ("th03_main.asm", "src/main/hud/score.asm", "obj/th03/main.@l"):
            report["staged_source_sha256"][name] = sha((WORK / name).read_bytes())
        context = {}
        for name in (WORK / "obj/th03/main.@l").read_text().split(",")[0].split():
            name = name.replace("\\", "/")
            if not name.lower().endswith(".obj") or name in produced:
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
            try:
                for argv, outputs in phases:
                    for n in outputs:
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
                    report["native_phases"].append(
                        dict(
                            argv=argv,
                            exit_code=status,
                            seconds=round(time.monotonic() - start, 3),
                        )
                    )
                    if status or not all((WORK / n).is_file() for n in outputs):
                        raise RuntimeError(
                            "native phase failed; see .analysis/work/main-build.log"
                        )
                report["comparison"] = review(previous)
                report["complete"] = True
            finally:
                (OUT / "main-build.json").write_text(
                    json.dumps(report, indent=2) + "\n"
                )
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
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
    result = build() if args.build else review()
    if args.runtime:
        from lib.main_entry_runtime import compare
        from lib.main_lose_runtime import (
            compare as compare_lose,
            negative_controls as lose_controls,
        )
        from review_th03_main_entry import negative_controls

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
                    "checked_accepted_extents",
                    "checked_accepted_bytes",
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
