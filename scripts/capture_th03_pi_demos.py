#!/usr/bin/env python3
"""Compare the four TH03 DOS attract demos at MAP-derived game boundaries."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import time
import tomllib
from types import SimpleNamespace

from audit_th03_dos_pi import DRIVE, map_symbols, sha
from lib.pc98 import parse_mz
from play_th03_dos import ROOT, FONT_SHA256, PROFILE, media, need, prepare

OBSERVER_SHA256 = "6e1a6e706d8b62aefa3204e30be5b77125fb4413d6891b5d10bd2701a6616ba1"
FIELDS = (
    ("_demo_frame", 0, 2), ("_round_frame", 0, 4), ("_round_or_result_frame", 0, 2),
    ("_input_mp_p1", 0, 2), ("_input_mp_p2", 0, 2), ("_input_sp", 0, 2),
    ("_score_p1", 0, 16), ("_random_seed", 0, 4), ("_randring", 0, 256),
    ("_randring_p", 0, 2), ("_players", 0, 100), ("_players", 108, 20),
    ("_players", 128, 100), ("_players", 236, 20), ("_resident", 0, 4),
)
HOOKS = (
    (1, "_round_CA3C"), (1, "_stage_demo_uncover"), (3, "IRAND"),
    (4, "randring1_next16()"), (4, "randring1_next16_and(unsigned int)"),
    (4, "randring2_next16()"), (4, "randring2_next16_and(unsigned int)"),
    (4, "randring2_next16_mod(unsigned int)"), (4, "randring_far_next16()"),
    (4, "randring_far_next16_and(unsigned int)"), (4, "randring_far_next16_mod(unsigned int)"),
)


def observer_profile(folder, image):
    main = map_symbols(folder / "main.map")
    code = image.program_image
    need(image.valid and image.header.entry_linear == 0 and code[0] == 0xBA, "expected far-model DOS startup")
    dgroup = int.from_bytes(code[1:3], "little")
    fields = []
    for name, field, width in FIELDS:
        frame, offset = main[name]
        need(frame == dgroup, f"{name} outside DGROUP")
        fields.append((offset + field, width))
    hooks = [(kind, *main[name]) for kind, name in HOOKS]
    return (f"{dgroup:x} {len(code):x}\n{code[:32].hex()}\n{len(hooks)}\n"
            + "".join(f"{kind} {frame:x} {offset:x}\n" for kind, frame, offset in hooks)
            + f"{len(fields)}\n" + "".join(f"{offset:x} {width}\n" for offset, width in fields)), hooks


def install(folder, output, links, layout):
    original, disk, _ = prepare(SimpleNamespace(original=False, package_stage="af1410p"), output)
    record = {}
    for product in ("main", "op", "mainl"):
        name = f"{product}.exe"
        raw = (folder / name).read_bytes()
        row = links[product]
        expected = row["baseline_sha256"] if layout == "control" else row["layouts"][layout]["exe_sha256"]
        map_hash = row["baseline_map_sha256"] if layout == "control" else row["layouts"][layout]["map_sha256"]
        need(sha(raw) == expected and parse_mz(raw).valid, f"{product} layout image")
        need(sha((folder / f"{product}.map").read_bytes()) == map_hash, f"{product} layout MAP")
        destination = "::/YUMEZIKU/" + name.upper()
        media(disk, "mcopy", "-o", str(folder / name), destination)
        need(media(disk, "mtype", destination) == raw, f"{name} disk readback")
        record[product] = expected
    return original, disk, record


def read_demo_rows(trace, rows, image, hooks, process=None, deadline=None):
    counts = {}
    loads = {}
    rng_calls = [0, 0]
    dgroup = int.from_bytes(image.program_image[1:3], "little")
    wrapped = False
    with trace.open() as observed, rows.open("w") as comparable:
        while not wrapped:
            start = observed.tell()
            line = observed.readline()
            if not line.endswith("\n"):
                if process is None or process.poll() is not None or time.monotonic() >= deadline:
                    break
                observed.seek(start)
                time.sleep(0.08)
                continue
            kind, number, *data = line.split()
            number = int(number)
            if kind == "L":
                load = int(data[0], 16)
                need(number == len(loads) + 1 <= 5 and
                     bytes.fromhex(data[-1]) == image.relocated_program_image(load), "complete guest MAIN image")
                loads[number] = load
                rng_calls = [0, 0]
                continue
            need(number in loads and number == len(loads), "record outside its active MAIN launch")
            if kind == "R":
                index, cs, ip, *_ = data
                index = int(index)
                hook = int(cs, 16) - loads[number], int(ip, 16)
                need(2 <= index < len(hooks) and hook == hooks[index][1:], "RNG hook identity")
                rng_calls[int(hooks[index][0] == 4)] += 1
                if number <= 4:
                    comparable.write(f"R {number} {index}\n")
            elif kind == "I":
                cs, ip, ds, lcg, ring, *fields = data
                hook = int(cs, 16) - loads[number], int(ip, 16)
                need(int(ds, 16) == loads[number] + dgroup and [int(lcg), int(ring)] == rng_calls,
                     "gameplay DGROUP or RNG hook count mismatch")
                need(len(fields) == len(FIELDS) + 1 and
                     all(len(bytes.fromhex(raw)) == width for raw, (_, _, width) in zip(fields[:-1], FIELDS, strict=True)),
                     "gameplay field width")
                resident = bytes.fromhex(fields[-1])
                need(resident[:11] == b"YUMEConfig\0" and resident[57] == (number - 1) % 4 + 1,
                     f"demo resident identity on MAIN launch {number}")
                if hook != hooks[0][1:]:
                    need(hook == hooks[1][1:], "unexpected gameplay hook")
                    continue
                frame = int.from_bytes(bytes.fromhex(fields[0]), "little")
                need(frame == min(counts.get(number, 0), 7000), f"unexpected frame in demo launch {number}: {frame}")
                if number == 5:
                    wrapped = True
                    continue
                counts[number] = counts.get(number, 0) + 1
                comparable.write(" ".join(("I", str(number), lcg, ring, *fields[:-2], resident[:58].hex())) + "\n")
            else:
                raise ValueError(f"unknown DOS observer record: {kind}")
    need(wrapped and counts == dict.fromkeys(range(1, 5), 7017), f"four complete attract demos: {counts}")
    return counts, loads


def capture(build, layout, output, emulator, timeout, retained=None, unthrottled=False):
    folder = build / layout
    links = json.loads((build / "layout.json").read_bytes())
    output.mkdir(parents=True)
    image = parse_mz((folder / "main.exe").read_bytes())
    profile, hooks = observer_profile(folder, image)
    profile_path = output / "observer.txt"
    profile_path.write_text(profile)
    rows = output / "rows.txt"
    settings = PROFILE.replace("videodriver=x11", "videodriver=dummy").replace("nosound=false", "nosound=true")
    if unthrottled:
        settings = settings.replace("turbo=false", "turbo=true")
    if retained is not None:
        need((retained / "observer.txt").read_text() == profile, "unchanged observer profile")
        need((retained / "dosbox-x.conf").read_text() == settings, "unchanged DOS emulator configuration")
        need(sha((retained / "FREECG98.BMP").read_bytes()) == FONT_SHA256, "retained font identity")
        trace = retained / "trace.txt"
        disk = retained / "execution.hdi"
        products = {product: links[product]["baseline_sha256"] for product in links}
        counts, loads = read_demo_rows(trace, rows, image, hooks)
    else:
        original, disk, products = install(folder, output, links, layout)
        font = (ROOT / ".analysis/runtime/fonts/FREECG98.BMP").read_bytes()
        need(sha(font) == FONT_SHA256, "font identity")
        (output / "FREECG98.BMP").write_bytes(font)
        config = output / "dosbox-x.conf"
        config.write_text(settings)
        log = output / "boot.log"
        trace = output / "trace.txt"
        env = {k: v for k, v in os.environ.items() if not k.startswith("TH04_")}
        env.update(DISPLAY="", WAYLAND_DISPLAY="", SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy",
                   TH04_DEMO_PROFILE=str(profile_path), TH04_DEMO_TRACE=str(trace),
                   XDG_CACHE_HOME=str(output / "cache"), XDG_CONFIG_HOME=str(output / "config"),
                   XDG_DATA_HOME=str(output / "data"))
        argv = [str(emulator), "-defaultconf", "-defaultmapper", "-conf", str(config), "-fastlaunch",
                "-nogui", "-nomenu", "-exit", "-c", f'imgmount 2 "{disk}" -t hdd -fs none', "-c", "boot -l c"]
        deadline = time.monotonic() + timeout
        with log.open("wb") as stream, subprocess.Popen(
                argv, cwd=output, env=env, stdout=stream, stderr=subprocess.STDOUT) as process:
            try:
                while not trace.exists() and process.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.1)
                counts, loads = read_demo_rows(trace, rows, image, hooks, process, deadline)
            finally:
                if process.poll() is None:
                    process.terminate()
                    process.wait(timeout=10)
        expected = tomllib.loads((ROOT / "config/targets.toml").read_text())["source"]["hdi_sha256"]
        need(sha(original.read_bytes()) == expected, "original HDI unchanged")
    for product, expected in products.items():
        raw = media(disk, "mtype", f"::/YUMEZIKU/{product.upper()}.EXE")
        need(sha(raw) == expected, f"runtime disk {product} identity")
    target_manifest = tomllib.loads((ROOT / "config/targets.toml").read_text())
    zun = next(item for item in target_manifest["artifacts"] if item["id"] == "th03-zun")
    need(sha(media(disk, "mtype", "::/YUMEZIKU/ZUN.COM")) == zun["sha256"], "runtime ZUN identity")
    result = {"layout": layout, "products": products, "complete_demos": counts, "loaded_segments": loads,
              "unthrottled": unthrottled, "emulator_sha256": OBSERVER_SHA256, "rows_sha256": sha(rows.read_bytes())}
    if retained is not None:
        result["retained_trace"] = str(trace)
    (output / "comparison.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"{layout}: four attract demos, {sum(counts.values()):,} gameplay rows", flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--emulator", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--layout", choices=("control", "even", "alt", "odd"), nargs="+", default=("control", "alt"))
    parser.add_argument("--timeout", type=int, default=1400)
    parser.add_argument("--unthrottled", action="store_true", help="remove host throttling in both runs")
    parser.add_argument("--reuse-control", type=Path, help="complete raw capture with unchanged profile and disk")
    args = parser.parse_args()
    if "control" not in args.layout or len(args.layout) < 2 or len(set(args.layout)) != len(args.layout):
        parser.error("compare the control against at least one distinct shifted layout")
    output = args.output.resolve()
    need(output.is_relative_to(ROOT / ".analysis/runtime") and not output.exists(), "fresh private output directory")
    need(re.fullmatch(r"af[0-9]+[a-z]", args.stage), "retained PI stage")
    emulator = args.emulator.resolve()
    need(sha(emulator.read_bytes()) == OBSERVER_SHA256, "pinned read-only DOS observer")
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    build = DRIVE / "TH03PI" / args.stage
    retained = args.reuse_control.resolve() if args.reuse_control else None
    if retained is not None:
        need(retained.is_relative_to(ROOT / ".analysis/runtime"), "private retained capture")
    results = [capture(build, layout, output / layout, emulator, args.timeout,
                       retained if layout == "control" else None, args.unthrottled) for layout in args.layout]
    need(len({row["rows_sha256"] for row in results}) == 1, "DOS attract traces differ")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
