#!/usr/bin/env python3
"""Rebuild MAINL and its six maintained CRT providers in two fresh rounds.

Vendor library context is extracted/rebuilt by TLIB, never patched. Reference
source remains explicit context; complete-byte equality does not grant ownership.
"""

import argparse
import fcntl
import json
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
import tomllib

from build_th03_op_work import compare_mz, need, sha
from lib.borland_library import compare_members, library_members
from lib.omf import describe_omf
from lib.targets import find_artifact, read_verified_artifact
from lib.toolchain import attest_surface
import stage_th03_mainl_fullcold as stage

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ML"
OUT = ROOT / ".analysis/work"
CRT = ("h_llsh", "h_padd", "n_pcmp", "ioerror", "fbrk", "setblock")
TLIB_SHA = "2d65d72b8800f7f3d4716218ed508bdd198e73b5f96f4830c1e14d1bb56546e2"
VENDOR_HEADERS = ("stddef.h", "_defs.h", "_null.h", "mem.h", "process.h", "stdlib.h",
                  "mbctype.h", "ctype.h", "mbstring.h")


def vendor_header_inventory():
    config = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    surface, = [s for s in config["surfaces"] if s["id"] == "tc40j-include"]
    compiler_headers = ROOT / config["paths"]["wine_prefix"] / "drive_c/TC4/INCLUDE"
    installed_headers = ROOT / surface["path"]
    result = {}
    for name in VENDOR_HEADERS:
        raw = (compiler_headers / name.upper()).read_bytes()
        need(raw == (installed_headers / name.upper()).read_bytes(), "consumed vendor header differs: " + name)
        result["C:/TC4/INCLUDE/" + name] = sha(raw)
    return result


def verify_vendor_dependencies(description, inventory):
    """Every fresh producer must bind its actual consumed SDK declarations."""
    for path in description["dependency_paths"]:
        path = path.replace(chr(92), "/")
        if path.startswith("C:/TC4/INCLUDE/"):
            need(path in inventory, "undeclared consumed vendor header: " + path)


def recipe_inventory():
    # Pin the current composer/runtime closure separately from generated source.
    paths = {"scripts/build_th03_mainl_work.py", "scripts/build_th03_op_work.py",
             "scripts/stage_th03_mainl_cold.py", "scripts/stage_th03_mainl_fullcold.py",
             "scripts/stage_th03_mainl_cutscene.py", "scripts/stage_th03_mainl_regist.py",
             "scripts/lib/borland_library.py", "scripts/lib/omf.py", "scripts/lib/pc98.py",
             "scripts/lib/targets.py", "scripts/lib/toolchain.py",
             "scripts/probe_th03_main_bomb_rikako_cpp.py", "scripts/probe_th03_main_boss_marisa_cpp.py",
             "config/toolchain.toml", "config/targets.toml", "config/th03_diet.toml",
             "config/th03_mainl_linked_game_source.json"}
    paths.update(str(p.relative_to(ROOT)) for p in (ROOT / "scripts/lib").glob("mainl_*.py"))
    return {n: sha((ROOT / n).read_bytes()) for n in sorted(paths)}


def sources():
    files, _, _, graph, archive_sha = stage.compose_all()
    # Keep genuine short input filenames, with unchanged source bytes.
    for name in (*[n + ".asm" for n in CRT], "crt_errno.inc", "dos_error_map.inc"):
        files["owned/" + name] = (ROOT / "src/mainl/crt" / name).read_bytes()
    need(all(Path(n).suffix.lower() not in {".obj", ".lib", ".exe", ".com", ".map"}
             for n in files), "native binary in source graph")
    need(len(graph) == 36 and len({r["output"] for r in graph}) == 36, "complete project graph")
    return files, graph, archive_sha


def response(library, commands):
    return (library + " &\r\n" + " &\r\n".join(commands) + "\r\n").encode("ascii")


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / "mainl-build.json"
    config = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    prefix = ROOT / config["paths"]["wine_prefix"]
    env = dict(os.environ, DISPLAY="", WAYLAND_DISPLAY="", WINEDEBUG="-all",
               WINEPREFIX=str(prefix), MSDOS_PATH=r"C:\TC4\BIN", TZ="UTC", LANG="C", LC_ALL="C")
    dos = ["/usr/bin/wine-stable", str(ROOT / config["paths"]["msdos_player"]), "-e", "-x"]
    tasm = ["/usr/bin/wine-stable", str(prefix / "drive_c/TASM50/bin/TASM32.EXE")]
    report = dict(complete=False, product_exact=False, ownership_acceptance=False,
                  provenance="candidate-local-attested", rounds=[], native_phases=[])
    report["recipe_sha256"] = recipe_inventory()
    report["vendor_header_sha256"] = vendor_header_inventory()
    save = lambda: report_path.write_text(json.dumps(report, indent=2) + "\n")

    def execute(argv, cwd, label, accepted=(0,), marker=None):
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=90)
        (OUT / "mainl-native.log").write_bytes(result.stdout)
        report["native_phases"].append(dict(label=label, argv=argv, returncode=result.returncode,
                                            log_sha256=sha(result.stdout)))
        save()
        need(result.returncode in accepted and (marker is None or marker in result.stdout),
             label + " failed; see .analysis/work/mainl-native.log")

    with (ROOT / ".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        save()
        surfaces = [attest_surface(ROOT, s) for s in config["surfaces"] if not s.get("bootstrap_only")]
        need(all(s["pass"] or not s["required"] for s in surfaces), "toolchain identity drift")
        tlib = (prefix / "drive_c/TC4/BIN/TLIB.EXE").read_bytes()
        need(sha(tlib) == TLIB_SHA and len(tlib) == 43860, "TLIB identity drift")
        vendor_raw = (prefix / "drive_c/TC4/LIB/CL.LIB").read_bytes()
        original = library_members(vendor_raw)
        need(len(original) == 893, "vendor member coverage")
        report.update(toolchain_surfaces=surfaces, tlib_sha256=TLIB_SHA,
                      vendor_library_sha256=sha(vendor_raw), retained_project_objects=0)
        previous = None
        first_sources = None
        for number in (1, 2):
            files, graph, archive_sha = sources()
            inventory = {n: sha(b) for n, b in sorted(files.items())}
            if first_sources is None:
                first_sources = inventory
            need(inventory == first_sources, "source graph changed between rounds")
            with TemporaryDirectory(prefix=".MAINL-source-", dir=WORK.parent) as temporary:
                fresh = Path(temporary)
                for name, raw in files.items():
                    p = fresh / name
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(raw)
                    os.utime(p, ns=(stage.base.STAMP, stage.base.STAMP))
                for name in ("obj/th01", "obj/th02", "obj/th03", "bin/th03", "vendor"):
                    (fresh / name).mkdir(parents=True, exist_ok=True)
                need(not WORK.is_symlink(), "working tree must be a real directory")
                if WORK.exists():
                    shutil.rmtree(WORK)
                shutil.copytree(fresh, WORK)
            outputs = {}
            for name in CRT:
                execute(tasm + ["/m", "/mx", "/kh32768", "/t", name + ".asm," + name + ".obj"],
                        WORK / "owned", f"round{number}:crt:" + name)
                output = "owned/" + name + ".obj"
                raw = (WORK / output).read_bytes()
                description = describe_omf(raw)
                need(description["valid"], "invalid fresh CRT object " + name)
                verify_vendor_dependencies(description, report["vendor_header_sha256"])
                outputs[output] = raw
            (WORK / "vendor/clbase.lib").write_bytes(vendor_raw)
            (WORK / "vendor/extract.rsp").write_bytes(response("clbase.lib", ["*" + m.name for m in original]))
            execute(dos + ["tlib", "@extract.rsp"], WORK / "vendor", f"round{number}:extract-vendor")
            extracted = {p.stem.casefold(): p for p in (WORK / "vendor").iterdir() if p.suffix.casefold() == ".obj"}
            need(set(extracted) == {m.name.casefold() for m in original}, "vendor extraction membership")
            for member in original:
                path = extracted[member.name.casefold()]
                destination = WORK / "vendor" / (member.name + ".obj")
                if path != destination:
                    path.rename(destination)
                outputs["vendor/" + destination.name] = destination.read_bytes()
            additions = ["+" + ("owned" if m.name in CRT else "vendor") + "\\" + m.name + ".obj"
                         for m in original]
            (WORK / "library.rsp").write_bytes(response("crt.lib /E", additions))
            execute(dos + ["tlib", "@library.rsp"], WORK, f"round{number}:build-crt-library")
            rebuilt = (WORK / "crt.lib").read_bytes()
            replacements = {n: outputs["owned/" + n + ".obj"] for n in CRT}
            library_review = compare_members(original, library_members(rebuilt), replacements)
            outputs["crt.lib"] = rebuilt
            print(f"round {number}: CRT library preserves {len(original)} members", flush=True)
            for row in graph:
                wrapper, output = row["wrapper"], row["output"]
                if row["kind"] == "tasm":
                    argv = tasm + row["flags"] + [wrapper.replace("/", "\\"), output.replace("/", "\\")]
                else:
                    need(row["kind"] == "tcc", "unknown project producer")
                    argv = dos + ["tcc", *row["flags"], wrapper]
                execute(argv, WORK, f"round{number}:" + output)
                raw = (WORK / output).read_bytes()
                description = describe_omf(raw)
                need(description["valid"], "invalid project OMF " + output)
                verify_vendor_dependencies(description, report["vendor_header_sha256"])
                outputs[output] = raw
                print(f"round {number}: {output}", flush=True)
            execute(dos + ["tlink", r"@obj\th03\mainl.@l"], WORK, f"round{number}:link")
            for name in ("bin/th03/mainl.exe", "obj/th03/mainl.map"):
                outputs[name] = (WORK / name).read_bytes()
            need(all((WORK / n).read_bytes() == b for n, b in files.items()), "source changed during build")
            need(vendor_header_inventory() == report["vendor_header_sha256"], "consumed vendor headers changed during build")
            report["rounds"].append(dict(round=number, source_files=len(files), library=library_review,
                outputs={n: dict(bytes=len(b), sha256=sha(b)) for n, b in sorted(outputs.items())}))
            if previous is not None:
                report["raw_repeat_equal"] = outputs == previous
                need(outputs == previous, "cold raw OBJ/LIB/EXE/MAP repetition failed")
            previous = outputs
            save()
        report.update(source_sha256=first_sources, archive_sha256=archive_sha)
        diet = tomllib.loads((ROOT / "config/th03_diet.toml").read_text())
        targets = tomllib.loads((ROOT / "config/targets.toml").read_text())
        stored = read_verified_artifact(ROOT, find_artifact(targets, "th03-mainl"))
        expected = next(a for a in diet["artifacts"] if a["id"] == "th03-mainl")
        tool = (ROOT / diet["tool"]["path"]).read_bytes()
        need(sha(tool) == diet["tool"]["sha256"] and len(tool) == diet["tool"]["size"], "DIET identity drift")
        with TemporaryDirectory(prefix=".MAINL-diet-", dir=WORK.parent) as temporary:
            temp = Path(temporary)
            (temp / "DIET.EXE").write_bytes(tool)
            (temp / "MAINL.EXE").write_bytes(stored)
            execute(dos + ["DIET.EXE", "-!"], temp, "diet:selfcheck", marker=b"original file!")
            execute(dos + ["DIET.EXE", "-ra", "MAINL.EXE"], temp, "diet:restore-target",
                    accepted=(1,), marker=b"Success!")
            decoded = (temp / "MAINL.EXE").read_bytes()
            need(len(decoded) == expected["decoded_size"] and sha(decoded) == expected["decoded_sha256"],
                 "decoded target identity drift")
            (WORK / "bin/th03/mainl.target.exe").write_bytes(decoded)
            candidate = outputs["bin/th03/mainl.exe"]
            report["comparison"] = compare_mz(candidate, decoded)
            packing = []
            packed_outputs = []
            for number in (1, 2):
                (temp / "MAINL.EXE").write_bytes(candidate)
                execute(dos + ["DIET.EXE", "-B", "MAINL.EXE"], temp, f"diet:pack{number}",
                        accepted=(1,), marker=b"Success!")
                packed = (temp / "MAINL.EXE").read_bytes()
                execute(dos + ["DIET.EXE", "-ra", "MAINL.EXE"], temp, f"diet:roundtrip{number}",
                        accepted=(1,), marker=b"Success!")
                restored = (temp / "MAINL.EXE").read_bytes()
                packing.append(dict(round=number, bytes=len(packed), sha256=sha(packed),
                                    stored_equal=packed == stored, roundtrip_equal=restored == candidate))
                packed_outputs.append(packed)
            (WORK / "bin/th03/mainl.packed.exe").write_bytes(packed_outputs[-1])
            report["packing"] = dict(options=["-B"], rounds=packing,
                                      raw_repeat_equal=packed_outputs[0] == packed_outputs[1],
                                      stored_equal=all(b == stored for b in packed_outputs),
                                      same_tool_roundtrip=True)
        from lib.pc98 import parse_mz
        from lib.mainl_lifecycle_layout import verify as layout
        from lib.mainl_lifecycle_runtime import verify as runtime, negative_controls
        t, c = parse_mz(decoded), parse_mz(candidate)
        report["lifecycle_scopes"] = dict(owners=layout(WORK, t, c), runtime=runtime(t, c),
                                         negative_controls=negative_controls(t))
        need(recipe_inventory() == report["recipe_sha256"], "recipe changed during cold build")
        report["complete"] = True
        save()
    print(json.dumps({k: v for k, v in report.items() if k not in
                      {"source_sha256", "rounds", "native_phases", "toolchain_surfaces"}}, indent=2))
    need(all(q["roundtrip_equal"] for q in packing), "DIET roundtrip changed the linked file")
    return report


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    build()


if __name__ == "__main__":
    main()
