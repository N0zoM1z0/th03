#!/usr/bin/env python3
"""Cold-build the whole maintained -4 driver through pinned JWasm and TLINK.

This is a compatible source producer, not evidence of the original assembler.
The outer launcher, other payloads and stored product remain separate work.
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

import bootstrap_jwasm as emitter
import stage_th03_zun_driver as tasm_stage
import stage_th03_zun_driver_jwasm as stage
from build_th03_op_work import need, sha
from lib.targets import find_artifact, read_verified_artifact
from lib.toolchain import attest_surface
from lib.zun import parse_launcher
from lib.zun_driver_layout import review

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ZSP"
OUT = ROOT / ".analysis/work"
STAMP = 946684800


def materialize(destination, files):
    for name, raw in files.items():
        path = destination / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        os.utime(path, (STAMP, STAMP))


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / "zun-driver-build.json"
    config = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    prefix = ROOT / config["paths"]["wine_prefix"]
    dos = ["/usr/bin/wine-stable", str(ROOT / config["paths"]["msdos_player"]), "-e", "-x"]
    env = dict(os.environ, DISPLAY="", WAYLAND_DISPLAY="", WINEDEBUG="-all",
               WINEPREFIX=str(prefix), MSDOS_PATH=r"C:\TC4\BIN", TZ="UTC", LANG="C", LC_ALL="C")
    report = dict(complete=False, product_exact=False, canonical_unit_credit_changed=False,
                  original_assembler_identified=False, provenance="candidate-local-attested",
                  rounds=[], native_phases=[], stored_product_rebuilt=False)
    save = lambda: report_path.write_text(json.dumps(report, indent=2) + "\n")

    def execute(argv, cwd, label, accepted=(0,), marker=None):
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=90)
        (OUT / "zun-driver-native.log").write_bytes(result.stdout)
        report["native_phases"].append(dict(label=label, argv=argv, returncode=result.returncode,
                                            log_sha256=sha(result.stdout)))
        save()
        need(result.returncode in accepted and (marker is None or marker in result.stdout),
             label + " failed; see .analysis/work/zun-driver-native.log")

    with (ROOT / ".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        save()
        surfaces = [attest_surface(ROOT, s) for s in config["surfaces"] if not s.get("bootstrap_only")]
        need(all(s["pass"] or not s["required"] for s in surfaces), "base toolchain identity drift")
        report["emitter"] = emitter.attest()
        profile = emitter.config()
        previous, first_sources = None, None
        for number in (1, 2):
            files, maintained = stage.payload(ROOT)
            inventory = {n: sha(b) for n, b in sorted(files.items())}
            if first_sources is None:
                first_sources = inventory
            need(inventory == first_sources, "source graph drift between rounds")
            need(all(Path(n).suffix.lower() not in {".obj", ".com", ".exe", ".map", ".lib"}
                     for n in files), "native binary seed in source graph")
            with TemporaryDirectory(prefix=".ZSP-source-", dir=WORK.parent) as temporary:
                fresh = Path(temporary)
                materialize(fresh, files)
                need(not WORK.is_symlink(), "working tree must be a real directory")
                if WORK.exists():
                    shutil.rmtree(WORK)
                shutil.copytree(fresh, WORK)
            execute([str(ROOT / profile["binary_path"]), *profile["assembler_flags"]], WORK,
                    f"round{number}:assemble")
            execute(dos + ["tlink", "@link.rsp"], WORK, f"round{number}:link")
            outputs = {n: (WORK / n).read_bytes() for n in ("driver.obj", "driver.com", "driver.map")}
            layout = review(outputs["driver.obj"], outputs["driver.map"])
            need(all((WORK / n).read_bytes() == b for n, b in files.items()), "consumed source drift")
            need(all((ROOT / n).read_bytes() == b for n, b in maintained.items()), "maintained source drift")
            report["rounds"].append(dict(round=number, layout=layout,
                outputs={n: dict(bytes=len(b), sha256=sha(b)) for n, b in outputs.items()}))
            if previous is not None:
                report["raw_repeat_equal"] = previous == outputs
                need(previous == outputs, "cold raw OMF/COM/MAP repeat failed")
            previous = outputs
            save()
        report["source_sha256"] = first_sources
        report["maintained_inputs"] = {n: sha(b) for n, b in sorted(maintained.items())}
        # The target is read only after the two independent source builds.
        diet = tomllib.loads((ROOT / "config/th03_diet.toml").read_text())
        targets = tomllib.loads((ROOT / "config/targets.toml").read_text())
        stored = read_verified_artifact(ROOT, find_artifact(targets, "th03-zun"))
        expected = next(a for a in diet["artifacts"] if a["id"] == "th03-zun")
        tool = (ROOT / diet["tool"]["path"]).read_bytes()
        need(sha(tool) == diet["tool"]["sha256"] and len(tool) == diet["tool"]["size"], "DIET tool drift")
        with TemporaryDirectory(prefix=".ZSP-compare-", dir=WORK.parent) as temporary:
            temp = Path(temporary)
            (temp / "DIET.EXE").write_bytes(tool)
            (temp / "ZUN.COM").write_bytes(stored)
            execute(dos + ["DIET.EXE", "-ra", "ZUN.COM"], temp, "diet:restore-target",
                    accepted=(1,), marker=b"Success!")
            decoded = (temp / "ZUN.COM").read_bytes()
            need(len(decoded) == expected["decoded_size"] and sha(decoded) == expected["decoded_sha256"],
                 "decoded parent identity drift")
            directory = parse_launcher(decoded, 223)
            selected = [p for p in directory["payloads"] if p["name"] == "-4"]
            need(len(selected) == 1 and selected[0]["size"] == 4224, "driver directory boundary drift")
            at = selected[0]["decoded_file_offset"]
            target = decoded[at:at + selected[0]["size"]]
            (WORK / "target.com").write_bytes(target)
            candidate = outputs["driver.com"]
            report["comparison"] = dict(target_sha256=sha(target), candidate_sha256=sha(candidate),
                                         target_bytes=len(target), candidate_bytes=len(candidate),
                                         raw_equal=candidate == target, decoded_parent_offset=at)
            # A genuine alternate producer is the byte comparator's negative
            # control. Its source algorithms/data and native TLINK are unchanged.
            control = temp / "tasm"
            control.mkdir()
            materialize(control, tasm_stage.prepare(maintained))
            execute(["/usr/bin/wine-stable", str(prefix / "drive_c/TASM50/bin/TASM32.EXE"),
                     "/m", "/mx", "/kh32768", "/t", "/dTHIEF", "driver.asm,driver.obj"],
                    control, "control:tasm")
            execute(dos + ["tlink", "@link.rsp"], control, "control:tasm-link")
            alternate = (control / "driver.com").read_bytes()
            differences = [i for i, (a, b) in enumerate(zip(alternate, target)) if a != b]
            need(len(alternate) == len(target) == 4224 and len(differences) == 10,
                 "expected TASM encoding negative control changed")
            report["negative_control"] = dict(producer="pinned TASM32", byte_exact_rejected=True,
                                              candidate_sha256=sha(alternate), differing_sites=differences)
        need(report["emitter"] == emitter.attest(), "emitter changed during cold builds")
        report["complete"] = True
        save()
    need(report["comparison"]["raw_equal"], "whole driver differs from pinned Japanese target")
    print(json.dumps({k: v for k, v in report.items() if k not in
                      {"rounds", "native_phases", "source_sha256", "maintained_inputs"}}, indent=2))
    return report


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    build()


if __name__ == "__main__":
    main()
