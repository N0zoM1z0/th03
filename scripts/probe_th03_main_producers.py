#!/usr/bin/env python3
"""Replay unresolved renderer/record questions with native tools; no acceptance."""

import fcntl
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

import build_th03_main_work as build
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact
from probe_th03_main_bomb_rikako_cpp import segment_definitions, code_bytes
from probe_th03_main_boss_marisa_cpp import code_publics

ROOT, WORK = build.ROOT, build.WORK


def run():
    names = ("src/main/player/losedraw.cpp", "src/main/player/lose.cpp",
             "src/main/player/state.cpp", "src/main/player/shotroot.cpp")
    sources = {name: (ROOT / name).read_text() for name in names}
    renderer = sources[names[0]]
    register_arg = renderer.replace("(player_stuff_t near *unused_player)",
                                    "(register player_stuff_t near *unused_player)")
    reference_arg = renderer.replace("(player_stuff_t near *unused_player)",
                                     "(player_stuff_t near &unused_player)")
    argsused = lambda text: text.replace("void near pascal player_lose_anim_render",
                                         "#pragma argsused\nvoid near pascal player_lose_anim_render")
    variants = dict(plain=renderer, regarg=register_arg, refarg=reference_arg, argsused=argsused(renderer),
                    regused=argsused(register_arg),
                    regangle=renderer.replace("unsigned char angle;", "register unsigned char angle;"),
                    adjacent=sources[names[1]] + "\n" + renderer)
    target_raw = read_verified_artifact(
        ROOT, find_artifact(load_target_manifest(ROOT / "config/targets.toml"), "th03-main"))
    target = parse_mz(target_raw)
    result = dict(exact_acceptance=False, target_sha256=hashlib.sha256(target_raw).hexdigest(),
                  probe_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), source_sha256={
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names
    }, renderer=[], state_shot={})
    checked = [WORK / n for n in ("bin/th03/main.exe", "obj/th03/main.map",
                                  "obj/th03/state.obj", "obj/th03/shotroot.obj")]
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in checked}
    result["native_context_sha256"] = {str(p.relative_to(ROOT)): h for p, h in before.items()}
    env = dict(os.environ, DISPLAY="", WAYLAND_DISPLAY="", WINEDEBUG="-all",
               WINEPREFIX=str(WORK.parent.parent), MSDOS_PATH=r"C:\TC4\BIN")
    dos = ["/usr/bin/wine-stable", str(ROOT / "_reference/ReC98/bin/msdos.exe"), "-e", "-x"]
    with (ROOT / ".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        short = WORK / "prnative"
        short.mkdir(exist_ok=False)
        try:
            compiler = dos + ["tcc", "-c", "-I.", "-O", "-b-", "-3", "-Z", "-d",
                              "-DGAME=3", "-ml", "-DBINARY='M'", "-nprnative/"]
            with (ROOT / ".analysis/work/producer-probe.log").open("w") as log:
                def compile_source(name, text):
                    (short / (name + ".cpp")).write_text(text)
                    subprocess.run(compiler + ["prnative/" + name + ".cpp"], cwd=WORK,
                                   env=env, stdout=log, stderr=subprocess.STDOUT,
                                   check=True, timeout=90)
                    return (short / (name + ".obj")).read_bytes()

                for name, text in variants.items():
                    raw = compile_source(name, text)
                    segment, = [s for s in segment_definitions(raw) if s["size"]]
                    code, _ = code_bytes(raw, segment["index"])
                    start, = [offset for offset, symbol in code_publics(raw, segment["index"])
                              if "PLAYER_LOSE_ANIM_RENDER" in symbol]
                    result["renderer"].append(dict(variant=name, bytes=len(code) - start,
                                                   prefix_hex=code[start:start + 6].hex()))
                # First declarations bind native section ownership. Keep the
                # shot API in P_SHOT_TEXT even when state.hpp is read first.
                group = ("#pragma codeseg P_SHOT_TEXT main_01\n"
                         "void near player_shots_add(void);\n" + sources[names[2]]
                         + "\n#pragma option -G-\n" + sources[names[3]])
                raw = compile_source("group", group)
                result["state_shot"]["segments"] = [dict(
                    name=s["name"], bytes=s["size"],
                    records=[p["size"] for p in code_bytes(raw, s["index"])[1]])
                    for s in segment_definitions(raw) if s["size"]]
                response = (WORK / "obj/th03/main.@l").read_text()
                for old, new in ((r"obj\th03\state.obj", r"prnative\group.obj"),
                                 (r"obj\th03\shotroot.obj", ""),
                                 (r"bin\th03\main.exe", r"prnative\probe.exe"),
                                 (r"obj\th03\main.map", r"prnative\probe.map")):
                    if response.count(old) != 1:
                        raise ValueError("native link input differs: " + old)
                    response = response.replace(old, new)
                (short / "probe.rsp").write_text(response)
                subprocess.run(dos + ["tlink", r"@prnative\probe.rsp"], cwd=WORK, env=env,
                               stdout=log, stderr=subprocess.STDOUT, check=True, timeout=90)
                candidate = parse_mz((short / "probe.exe").read_bytes())
                result["state_shot"]["scopes"] = []
                for lo, hi in ((0xDA43, 0xE0F7), (0xE266, 0xE83F), (0xDA43, 0xE313)):
                    vectors = [[(r.segment, r.offset) for r in image.relocations
                                if lo <= r.linear < hi] for image in (target, candidate)]
                    result["state_shot"]["scopes"].append(dict(
                        start=lo, bytes=hi - lo,
                        raw_equal=target.program_image[lo:hi] == candidate.program_image[lo:hi],
                        literal_order_equal=vectors[0] == vectors[1], vectors=vectors))
                result["state_shot"]["whole_image_differences"] = [
                    i for i, (a, b) in enumerate(zip(target.program_image, candidate.program_image)) if a != b]
        finally:
            shutil.rmtree(short)
    if before != {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in checked}:
        raise ValueError("producer probe changed working native outputs")
    result["working_outputs_unchanged"] = True
    return result


if __name__ == "__main__":
    output = ROOT / ".analysis/work/producer-review.json"
    result = run()
    output.write_text(json.dumps(result, indent=2) + "\n")
    print("Native producer probes complete; diagnostic only; temporary products removed")
