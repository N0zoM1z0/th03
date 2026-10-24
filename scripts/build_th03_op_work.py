#!/usr/bin/env python3
"""Rebuild the current OP source graph; old verification trees are not inputs.

Reference source and vendor libraries remain explicitly unowned context. A raw
product match is a build observation, not an automatic ownership/ABI acceptance.
"""

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import tomllib

from lib.omf import describe_omf
from lib.pc98 import parse_mz
from lib.targets import find_artifact, read_verified_artifact
import stage_th03_op_fullcold as base
import stage_th03_op_nopcall as final_stage

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".analysis/work"
WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03OP"
STAMP = 946684800


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(value, message):
    if not value:
        raise ValueError(message)


def source_graph():
    # Recreate this disposable archive from the pinned local Git object. Its
    # exact digest is still checked by the unchanged historical source stager.
    archive = ROOT / base.ARCHIVE
    if not archive.exists():
        archive.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "-C", str(ROOT / "_reference/ReC98"), "archive",
                        "--format=tar", "--output=" + str(archive), base.REV], check=True)
    return final_stage.payload(ROOT)


def producers(files):
    rows = {p["object"]: dict(p) for p in base.PROJECT_PRODUCERS
            if p["source"] != "th03/op_sel.cpp"}
    for stem, source in (("oplayout", "oplayout.asm"), ("optail", "th03_optail.asm"),
                         ("selhelp", "th03/selhelp.cpp"), ("seltail", "th03/seltail.cpp")):
        rows[f"obj/th03/{stem}.obj"] = dict(source=source, command="-DGAME=3")
    response = files["obj/th03/op.@l"].decode()
    order = [s.replace("\\", "/") for s in re.findall(r"obj\\[^\s,]+\.obj", response)]
    need(len(order) == len(set(order)) == len(rows) == 30, "complete thirty-object graph")
    return [dict(rows[name], output=name) for name in order]


def compare_mz(candidate, target):
    c, t = map(parse_mz, (candidate, target))
    need(c.valid and t.valid, "invalid decoded MZ")
    pairs = lambda m: [(r.segment, r.offset) for r in m.relocations]
    return dict(file_equal=candidate == target,
                header_equal=candidate[:c.header.header_size] == target[:t.header.header_size],
                program_equal=c.program_image == t.program_image,
                ordered_relocations_equal=pairs(c) == pairs(t),
                relocation_membership_equal=sorted(pairs(c)) == sorted(pairs(t)),
                candidate_bytes=len(candidate), target_bytes=len(target),
                candidate_relocations=len(c.relocations), target_relocations=len(t.relocations),
                differing_program_sites=[i for i, (a, b) in
                                         enumerate(zip(c.program_image, t.program_image)) if a != b],
                program_size_equal=len(c.program_image) == len(t.program_image))


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / "op-build.json"
    report = dict(complete=False, product_exact=False, ownership_acceptance=False,
                  provenance="candidate-local-attested", rounds=[], native_phases=[])
    save = lambda: report_path.write_text(json.dumps(report, indent=2) + "\n")
    config = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    prefix = ROOT / config["paths"]["wine_prefix"]
    env = dict(os.environ, DISPLAY="", WAYLAND_DISPLAY="", WINEDEBUG="-all",
               WINEPREFIX=str(prefix), MSDOS_PATH=r"C:\TC4\BIN", TZ="UTC",
               LANG="C", LC_ALL="C")
    dos = ["/usr/bin/wine-stable", str(ROOT / config["paths"]["msdos_player"]), "-e", "-x"]
    tasm = ["/usr/bin/wine-stable", str(prefix / "drive_c/TASM50/bin/TASM32.EXE")]

    def execute(argv, cwd, label, accepted=(0,), marker=None):
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=90)
        (OUT / "op-native.log").write_bytes(result.stdout)
        report["native_phases"].append(dict(label=label, argv=argv,
                                            returncode=result.returncode,
                                            log_sha256=sha(result.stdout)))
        save()
        need(result.returncode in accepted and (marker is None or marker in result.stdout),
             label + " failed; see .analysis/work/op-native.log")

    with (ROOT / ".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        save()
        # Identity checking uses no Wine writers. The normal preflight/CI also
        # executes the pinned tools; this run records their current full surfaces.
        from lib.toolchain import attest_surface
        surfaces = [attest_surface(ROOT, s) for s in config["surfaces"]
                    if not s.get("bootstrap_only")]
        need(all(s["pass"] or not s["required"] for s in surfaces), "toolchain identity drift")
        report["toolchain_surfaces"] = surfaces
        prior = None
        first_sources = None
        for number in (1, 2):
            files = source_graph()
            inventory = {n: sha(b) for n, b in sorted(files.items())}
            need(all(Path(n).suffix.lower() not in {".obj", ".exe", ".lib", ".com", ".map"}
                     for n in files), "binary seed in source graph")
            if first_sources is None:
                first_sources = inventory
            need(inventory == first_sources, "source graph changed between rounds")
            rows = producers(files)
            with TemporaryDirectory(prefix=".OP-source-", dir=WORK.parent) as temporary:
                fresh = Path(temporary)
                for name, raw in files.items():
                    p = fresh / name
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_bytes(raw)
                    os.utime(p, (STAMP, STAMP))
                for directory in ("obj/th01", "obj/th02", "obj/th03", "bin/th03"):
                    (fresh / directory).mkdir(parents=True, exist_ok=True)
                need(not WORK.is_symlink(), "working tree must not be a symlink")
                if WORK.exists():
                    shutil.rmtree(WORK)
                shutil.copytree(fresh, WORK)
            outputs = {}
            for row in rows:
                source, output = row["source"], row["output"]
                game = re.search(r"[/-]dGAME=(\d)", row["command"], re.I)[1]
                if source.endswith(".asm"):
                    argv = tasm + ["/m", "/mx", "/kh32768", "/t", "/dGAME=" + game,
                                   source.replace("/", "\\"), output.replace("/", "\\")]
                else:
                    argv = dos + ["tcc", "-c", "-I.", "-O", "-b-", "-3", "-Z", "-d",
                                  "-DGAME=" + game, "-ml", "-DBINARY='O'",
                                  "-n" + str(Path(output).parent) + "/", source]
                execute(argv, WORK, f"round{number}:" + output)
                raw = (WORK / output).read_bytes()
                need(describe_omf(raw)["valid"], "invalid OMF " + output)
                outputs[output] = raw
                print(f"round {number}: {output}", flush=True)
            execute(dos + ["tlink", r"@obj\th03\op.@l"], WORK, f"round{number}:link")
            for name in ("bin/th03/op.exe", "obj/th03/op.map"):
                outputs[name] = (WORK / name).read_bytes()
            need(all((WORK / n).read_bytes() == b for n, b in files.items()),
                 "source changed during native build")
            report["rounds"].append(dict(round=number, source_files=len(files),
                outputs={n: dict(bytes=len(b), sha256=sha(b)) for n, b in outputs.items()}))
            if prior is not None:
                report["raw_repeat_equal"] = prior == outputs
                need(prior == outputs, "cold raw OBJ/EXE/MAP repeat failed")
            prior = outputs
            save()
        report["source_sha256"] = first_sources
        report["retained_project_objects"] = 0
        # Target bytes enter only the comparison/DIET directory after linking.
        diet = tomllib.loads((ROOT / "config/th03_diet.toml").read_text())
        targets = tomllib.loads((ROOT / "config/targets.toml").read_text())
        stored = read_verified_artifact(ROOT, find_artifact(targets, "th03-op"))
        expected = next(a for a in diet["artifacts"] if a["id"] == "th03-op")
        tool = (ROOT / diet["tool"]["path"]).read_bytes()
        need(sha(tool) == diet["tool"]["sha256"] and len(tool) == diet["tool"]["size"],
             "DIET identity mismatch")
        with TemporaryDirectory(prefix=".OP-diet-", dir=WORK.parent) as temporary:
            temp = Path(temporary)
            (temp / "DIET.EXE").write_bytes(tool)
            (temp / "OP.EXE").write_bytes(stored)
            execute(dos + ["DIET.EXE", "-!"], temp, "diet:selfcheck", marker=b"original file!")
            execute(dos + ["DIET.EXE", "-ra", "OP.EXE"], temp, "diet:restore-target",
                    accepted=(1,), marker=b"Success!")
            decoded = (temp / "OP.EXE").read_bytes()
            need(len(decoded) == expected["decoded_size"] and sha(decoded) == expected["decoded_sha256"],
                 "decoded target identity mismatch")
            (WORK / "bin/th03/op.target.exe").write_bytes(decoded)
            report["comparison"] = compare_mz(outputs["bin/th03/op.exe"], decoded)
        report["complete"] = True
        save()
    print(json.dumps({k: v for k, v in report.items()
                      if k not in {"source_sha256", "rounds", "native_phases", "toolchain_surfaces"}}, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", action="store_true",
                        help="revalidate current cold outputs and repeat DIET packing")
    args = parser.parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    if not args.review:
        build()
    review_packing()


def review_packing():
    with (ROOT / ".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return _review_packing_locked()


def _review_packing_locked():
    report_path = OUT / "op-build.json"
    report = json.loads(report_path.read_text())
    need(report["complete"] and report["raw_repeat_equal"] and len(report["rounds"]) == 2,
         "complete independent cold pair required")
    files = source_graph()
    need({n: sha(b) for n, b in sorted(files.items())} == report["source_sha256"],
         "current source graph differs from cold build")
    need(all((WORK / n).read_bytes() == b for n, b in files.items()), "staged source drift")
    outputs = report["rounds"][1]["outputs"]
    need(len(outputs) == 32 and report["rounds"][0]["outputs"] == outputs, "cold output coverage")
    for name, row in outputs.items():
        raw = (WORK / name).read_bytes()
        need(sha(raw) == row["sha256"] and len(raw) == row["bytes"], "cold output drift: " + name)
    config = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    from lib.toolchain import attest_surface
    need(all(s["pass"] or not s["required"] for s in
             (attest_surface(ROOT, s) for s in config["surfaces"] if not s.get("bootstrap_only"))),
         "toolchain identity drift")
    diet = tomllib.loads((ROOT / "config/th03_diet.toml").read_text())
    targets = tomllib.loads((ROOT / "config/targets.toml").read_text())
    stored = read_verified_artifact(ROOT, find_artifact(targets, "th03-op"))
    expected = next(a for a in diet["artifacts"] if a["id"] == "th03-op")
    decoded = (WORK / "bin/th03/op.target.exe").read_bytes()
    need(len(decoded) == expected["decoded_size"] and sha(decoded) == expected["decoded_sha256"],
         "decoded target drift")
    candidate = (WORK / "bin/th03/op.exe").read_bytes()
    need(compare_mz(candidate, decoded) == report["comparison"], "comparison drift")
    tool = (ROOT / diet["tool"]["path"]).read_bytes()
    need(sha(tool) == diet["tool"]["sha256"] and len(tool) == diet["tool"]["size"], "DIET drift")
    prefix = ROOT / config["paths"]["wine_prefix"]
    env = dict(os.environ, DISPLAY="", WAYLAND_DISPLAY="", WINEDEBUG="-all",
               WINEPREFIX=str(prefix), MSDOS_PATH=r"C:\TC4\BIN", TZ="UTC")
    dos = ["/usr/bin/wine-stable", str(ROOT / config["paths"]["msdos_player"]), "-e", "-x"]
    observations = []
    packed_outputs = []
    with TemporaryDirectory(prefix=".OP-pack-pair-", dir=WORK.parent) as pair:
        for number in (1, 2):
            with TemporaryDirectory(prefix=f"round{number}-", dir=pair) as temporary:
                temp = Path(temporary)
                (temp / "DIET.EXE").write_bytes(tool)
                (temp / "OP.EXE").write_bytes(candidate)
                phases = []
                # TH03 OP uses the compact SFX stub. TH04's -G selects the
                # larger "great SFX" routine and produces a different envelope.
                for options in (["-B", "OP.EXE"], ["-ra", "OP.EXE"]):
                    argv = dos + ["DIET.EXE", *options]
                    result = subprocess.run(argv, cwd=temp, env=env, stdout=subprocess.PIPE,
                                            stderr=subprocess.STDOUT, timeout=90)
                    (OUT / "op-native.log").write_bytes(result.stdout)
                    need(result.returncode == 1 and b"Success!" in result.stdout, "DIET packing/restore failed")
                    phases.append(dict(argv=argv, returncode=result.returncode, log_sha256=sha(result.stdout)))
                    if options[0] == "-B":
                        packed = (temp / "OP.EXE").read_bytes()
                restored = (temp / "OP.EXE").read_bytes()
                packed_outputs.append(packed)
                observations.append(dict(round=number, phases=phases, packed_sha256=sha(packed),
                                         packed_bytes=len(packed), stored_equal=packed == stored,
                                         decoded_roundtrip_equal=restored == candidate))
        report["packing"] = dict(options=["-B"], rounds=observations,
                                  raw_repeat_equal=packed_outputs[0] == packed_outputs[1],
                                  stored_equal=all(b == stored for b in packed_outputs),
                                  same_tool_roundtrip=True)
        (WORK / "bin/th03/op.packed.exe").write_bytes(packed_outputs[-1])
        report_path.write_text(json.dumps(report, indent=2) + "\n")
    need(all(o["decoded_roundtrip_equal"] for o in observations), "DIET roundtrip changed the linked EXE")
    print(json.dumps(report["packing"], indent=2))


if __name__ == "__main__":
    main()
