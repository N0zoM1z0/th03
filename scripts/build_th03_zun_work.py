#!/usr/bin/env python3
"""Build the complete ZUN launcher twice from current producers and vendor inputs.

No historical project object, payload build, composition or stored candidate is
an input. Vendor -1, MASTERS.LIB and Borland startup/runtime stay unowned.
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
from build_th03_op_work import need, sha
from lib.omf import describe_omf
from lib.targets import find_artifact, read_verified_artifact
from lib.toolchain import attest_surface
from lib.zun import compose_launcher, parse_launcher, dispatch_observation
from lib.zun_driver_layout import review as review_driver
from lib.zun_work_source import compose, PROFILE
from verify_th03_zun_init_standalone import verify_outputs as review_init

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / ".analysis/toolchain/wineprefix/drive_c/TH03ZUN"
OUT = ROOT / ".analysis/work"
STAMP = 946684800


def runtime_inventory():
    config = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    surface, = [s for s in config["surfaces"] if s["id"] == "tc40j-lib"]
    consumed = ROOT / config["paths"]["wine_prefix"] / "drive_c/TC4/LIB"
    installed = ROOT / surface["path"]
    result = {}
    for name in ("C0T.OBJ", "EMU.LIB", "MATHS.LIB", "CT.LIB"):
        raw = (consumed / name).read_bytes()
        need(raw == (installed / name).read_bytes(), "consumed tiny runtime differs from pinned installation: " + name)
        result[name] = sha(raw)
    return result


def sdk_inventory():
    config = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    surface, = [s for s in config["surfaces"] if s["id"] == "tc40j-include"]
    consumed = ROOT / config["paths"]["wine_prefix"] / "drive_c/TC4/INCLUDE"
    installed = ROOT / surface["path"]
    result = {}
    for name in ("DOS.H", "_DEFS.H"):
        raw = (consumed / name).read_bytes()
        need(raw == (installed / name).read_bytes(), "consumed resident SDK differs from pinned installation: " + name)
        result[name.lower()] = sha(raw)
    return result


def recipe_inventory():
    paths = ("scripts/build_th03_zun_work.py", "scripts/build_th03_op_work.py",
             "scripts/bootstrap_jwasm.py", "scripts/stage_th03_zun_driver_jwasm.py",
             "scripts/stage_th03_zun_init.py", "scripts/stage_th03_zun_resident.py",
             "scripts/stage_th03_zunsoft.py", "scripts/verify_th03_zun_init_standalone.py",
             "scripts/review_th03_zunsoft.py", "scripts/lib/zun_work_source.py",
             "scripts/lib/zun_driver_layout.py", "scripts/lib/zun_logo_layout.py",
             "scripts/lib/zun_logo_runtime.py", "scripts/lib/zun_resident_layout.py",
             "scripts/lib/zun_resident_runtime.py", "scripts/review_th03_zun_resident.py",
             "scripts/lib/zun_init_layout.py", "scripts/lib/zun_init_runtime.py", "scripts/review_th03_zun_init.py",
             "scripts/lib/zun_driver_scalar_layout.py", "scripts/lib/zun_driver_scalar_runtime.py",
             "scripts/lib/zun_driver_alignment.py",
             "scripts/stage_th03_zun_driver.py", "scripts/verify_th03_zun_driver_hybrid.py",
             "config/th03_zun_init_fixups.json", "config/th03_zun_init_labels.json",
             "scripts/lib/zun.py", "scripts/lib/omf.py",
             "scripts/lib/pc98.py", "scripts/lib/targets.py", "scripts/lib/toolchain.py",
             "scripts/probe_th03_main_bomb_rikako_cpp.py", "scripts/probe_th03_main_boss_marisa_cpp.py",
             "config/th03_zun_work.toml", "config/th03_zun_driver_jwasm.toml",
             "config/zun_resident/source.json", "config/th03_diet.toml",
             "config/toolchain.toml", "config/targets.toml")
    return {name: sha((ROOT / name).read_bytes()) for name in paths}


def runtime_rows(image):
    directory = parse_launcher(image, 223)
    rows = [dispatch_observation(image, directory, "", ""),
            dispatch_observation(image, directory, " -X", "-X")]
    for number in range(1, 6):
        result = dispatch_observation(image, directory, f"  -{number} hello", f"-{number}")
        need(result["tail"] == " hello" and result["sp"] == 0xFFFC
             and result["remaining_count"] == 6 - number and not result["flags"] & 0x400,
             "wrapper dispatch stack/DF/argument ABI drift")
        rows.append(result)
    return rows


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    report_path = OUT / "zun-build.json"
    config = tomllib.loads((ROOT / "config/toolchain.toml").read_text())
    recipe = tomllib.loads((ROOT / PROFILE).read_text())
    prefix = ROOT / config["paths"]["wine_prefix"]
    env = dict(os.environ, DISPLAY="", WAYLAND_DISPLAY="", WINEDEBUG="-all",
               WINEPREFIX=str(prefix), MSDOS_PATH=r"C:\TC4\BIN", TZ="UTC", LANG="C", LC_ALL="C")
    dos = ["/usr/bin/wine-stable", str(ROOT / config["paths"]["msdos_player"]), "-e", "-x"]
    tasm = ["/usr/bin/wine-stable", str(prefix / "drive_c/TASM50/bin/TASM32.EXE"), *recipe["assembler_flags"]]
    report = dict(complete=False, product_exact=False, ownership_acceptance=False,
                  provenance="candidate-local-attested", rounds=[], native_phases=[],
                  retained_project_objects=0, whole_game_percentage=None)
    report["recipe_sha256"] = recipe_inventory()
    save = lambda: report_path.write_text(json.dumps(report, indent=2) + "\n")

    def execute(argv, cwd, label, accepted=(0,), marker=None):
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=90)
        (OUT / "zun-native.log").write_bytes(result.stdout)
        report["native_phases"].append(dict(label=label, argv=argv, cwd=str(cwd.relative_to(ROOT)), returncode=result.returncode,
                                            log_sha256=sha(result.stdout)))
        save()
        need(result.returncode in accepted and (marker is None or marker in result.stdout),
             label + " failed; see .analysis/work/zun-native.log")

    with (ROOT / ".analysis/borland-wine-writer.lock").open("ab") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        save()
        surfaces = [attest_surface(ROOT, s) for s in config["surfaces"] if not s.get("bootstrap_only")]
        need(all(s["pass"] or not s["required"] for s in surfaces), "base toolchain identity drift")
        report["toolchain_surfaces"] = surfaces
        report["consumed_runtime_sha256"] = runtime_inventory()
        report["consumed_sdk_sha256"] = sdk_inventory()
        report["emitter"] = emitter.attest()
        profile = emitter.config()
        diet = tomllib.loads((ROOT / "config/th03_diet.toml").read_text())
        tool = (ROOT / diet["tool"]["path"]).read_bytes()
        need(sha(tool) == diet["tool"]["sha256"] and len(tool) == diet["tool"]["size"], "DIET identity drift")
        previous, first_sources = None, None
        for number in (1, 2):
            files, maintained, source_context = compose(ROOT)
            inventory = {n: sha(b) for n, b in sorted(files.items())}
            if first_sources is None:
                first_sources = inventory
            need(inventory == first_sources, "source/vendor graph drift between cold rounds")
            with TemporaryDirectory(prefix=".ZUN-source-", dir=WORK.parent) as temporary:
                fresh = Path(temporary)
                for name, raw in files.items():
                    path = fresh / name
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(raw)
                    os.utime(path, (STAMP, STAMP))
                for name in ("obj/th01", "obj/th03", "bin/th01", "bin/th03", "product"):
                    (fresh / name).mkdir(parents=True, exist_ok=True)
                need(not WORK.is_symlink(), "working tree must be a real directory")
                if WORK.exists():
                    shutil.rmtree(WORK)
                shutil.copytree(fresh, WORK)
            outputs = {}
            def collect(names):
                for name in names:
                    raw = (WORK / name).read_bytes()
                    if name.endswith(".obj"):
                        need(describe_omf(raw)["valid"], "invalid generated OMF: " + name)
                    outputs[name] = raw
            execute(tasm + [r"src\zun\init.asm,init.obj"], WORK / "init", f"round{number}:init-assemble")
            execute(dos + ["tlink", "@link.rsp"], WORK / "init", f"round{number}:init-link")
            collect(["init/init." + ext for ext in ("obj", "com", "map")])
            for stem, game in (("zunsoft", 1), ("res_yume", 3)):
                execute(dos + ["tcc", *recipe["compiler_flags"], f"-DGAME={game}",
                               f"-nobj/th0{game}/", f"th0{game}/{stem}.cpp"],
                        WORK, f"round{number}:" + stem + "-compile")
                execute(dos + ["tlink", f"@obj\\th0{game}\\{stem}.rsp"],
                        WORK, f"round{number}:" + stem + "-link")
                collect([f"obj/th0{game}/{stem}.obj", f"obj/th0{game}/{stem}.map", f"bin/th0{game}/{stem}.com"])
            execute([str(ROOT / profile["binary_path"]), *profile["assembler_flags"]],
                    WORK / "driver", f"round{number}:driver-assemble")
            execute(dos + ["tlink", "@link.rsp"], WORK / "driver", f"round{number}:driver-link")
            collect(["driver/driver." + ext for ext in ("obj", "com", "map")])
            layout = review_driver(outputs["driver/driver.obj"], outputs["driver/driver.map"])
            payloads = [(WORK / "libs/kaja/ongchk.com").read_bytes(), outputs["init/init.com"],
                        outputs["bin/th01/zunsoft.com"], outputs["driver/driver.com"], outputs["bin/th03/res_yume.com"]]
            payload_bytes = sum(map(len, payloads))
            for alias in ("stub", "call", "helper"):
                flags = [f"/dPAYLOAD_BYTES={payload_bytes}"] if alias == "call" else []
                execute(tasm + flags + [alias + ".asm," + alias + ".obj"],
                        WORK / "wrapper", f"round{number}:wrapper-" + alias)
                execute(dos + ["tlink", "@" + alias + ".rsp"],
                        WORK / "wrapper", f"round{number}:wrapper-" + alias + "-link")
                collect(["wrapper/" + alias + "." + ext for ext in ("obj", "com", "map")])
            candidate = compose_launcher(outputs["wrapper/stub.com"], outputs["wrapper/call.com"],
                                         outputs["wrapper/helper.com"], recipe["options"], payloads)
            (WORK / "product/zun.com").write_bytes(candidate)
            outputs["product/zun.com"] = candidate
            # Give each DOS filename one case-insensitive owner while DIET
            # rewrites its working copy. The linked/composed output stays bound.
            with TemporaryDirectory(prefix=".ZUN-pack-", dir=WORK.parent) as temporary:
                packing = Path(temporary)
                (packing / "DIET.EXE").write_bytes(tool)
                (packing / "ZUN.COM").write_bytes(candidate)
                execute(dos + ["DIET.EXE", *recipe["diet_options"], "ZUN.COM"],
                        packing, f"round{number}:pack", accepted=(1,), marker=b"Success!")
                packed = (packing / "ZUN.COM").read_bytes()
                execute(dos + ["DIET.EXE", "-ra", "ZUN.COM"], packing,
                        f"round{number}:roundtrip", accepted=(1,), marker=b"Success!")
                need((packing / "ZUN.COM").read_bytes() == candidate, "same-tool DIET roundtrip differs")
            outputs["product/zun.packed.com"] = packed
            (WORK / "product/zun.packed.com").write_bytes(packed)
            need(all((WORK / n).read_bytes() == b for n, b in files.items()), "consumed input drift")
            need(all((ROOT / n).read_bytes() == b for n, b in maintained.items()), "maintained source drift")
            report["rounds"].append(dict(round=number, layout=layout,
                directory=parse_launcher(candidate, len(outputs["wrapper/stub.com"])),
                outputs={n: dict(bytes=len(b), sha256=sha(b)) for n, b in sorted(outputs.items())}))
            if previous is not None:
                report["raw_repeat_equal"] = outputs == previous
                need(outputs == previous, "cold raw OBJ/COM/MAP/packed repetition failed")
            previous = outputs
            save()
            print(f"round {number}: {len(outputs)} outputs; decoded {len(candidate)} B; packed {len(packed)} B", flush=True)
        report.update(source_sha256=first_sources, maintained_inputs={n: sha(b) for n, b in sorted(maintained.items())},
                      source_context=source_context)
        targets = tomllib.loads((ROOT / "config/targets.toml").read_text())
        stored = read_verified_artifact(ROOT, find_artifact(targets, "th03-zun"))
        expected = next(a for a in diet["artifacts"] if a["id"] == "th03-zun")
        with TemporaryDirectory(prefix=".ZUN-target-", dir=WORK.parent) as temporary:
            temp = Path(temporary)
            (temp / "DIET.EXE").write_bytes(tool)
            (temp / "ZUN.COM").write_bytes(stored)
            execute(dos + ["DIET.EXE", "-ra", "ZUN.COM"], temp, "restore-target",
                    accepted=(1,), marker=b"Success!")
            decoded = (temp / "ZUN.COM").read_bytes()
            need(len(decoded) == expected["decoded_size"] and sha(decoded) == expected["decoded_sha256"],
                 "canonical decoded target identity drift")
        (WORK / "product/zun.target.com").write_bytes(decoded)
        directory = parse_launcher(decoded, 223)
        reviews = []
        for declaration, payload in zip(directory["payloads"], payloads):
            at, size = declaration["decoded_file_offset"], declaration["size"]
            target = decoded[at:at + size]
            reviews.append(dict(name=declaration["name"], target_bytes=size, candidate_bytes=len(payload),
                                target_sha256=sha(target), candidate_sha256=sha(payload), raw_equal=target == payload))
        report["comparison"] = dict(decoded_equal=candidate == decoded, stored_equal=packed == stored,
                                    decoded_bytes=len(candidate), stored_bytes=len(packed), payloads=reviews,
                                    decoded_sha256=sha(candidate), stored_sha256=sha(packed))
        if reviews[1]["raw_equal"]:
            row = directory["payloads"][1]
            report["init_review"] = review_init(outputs["init/init.obj"], outputs["init/init.com"],
                outputs["init/init.map"], decoded[row["decoded_file_offset"]:row["decoded_file_offset"] + row["size"]])
        actual, reference = runtime_rows(candidate), runtime_rows(decoded)
        need(actual == reference, "bounded wrapper target/candidate trace differs")
        report["wrapper_runtime"] = dict(cases_per_image=7, total_cases=14, rows_equal=True,
                                        candidate=actual, dos_services="bounded stubs; stop before payload execution")
        broken = bytearray(candidate)
        broken[directory["helper_offset"] + 4] = 1
        try:
            dispatch_observation(bytes(broken), directory, " -1 hello", "-1")
        except ValueError as error:
            need("missed the payload entry" in str(error), "unexpected transfer control failure")
        else:
            raise ValueError("incorrect transfer entry escaped the negative control")
        report["wrong_transfer_entry_rejected"] = True
        from lib.zun_logo_layout import verify as logo_layout
        from lib.zun_logo_runtime import verify as logo_runtime, negative_controls
        logo = directory["payloads"][2]
        at, size = logo["decoded_file_offset"], logo["size"]
        target_logo = decoded[at:at + size]
        report["logo_scopes"] = dict(layout=logo_layout(WORK, target_logo, payloads[2], at),
            runtime=logo_runtime(target_logo, payloads[2]), negative_controls=negative_controls(target_logo))
        from lib.zun_resident_layout import verify as resident_layout
        from lib.zun_resident_runtime import verify as resident_runtime, negative_controls as resident_controls
        resident = directory["payloads"][4]
        at, size = resident["decoded_file_offset"], resident["size"]
        target_resident = decoded[at:at + size]
        report["resident_scopes"] = dict(layout=resident_layout(WORK, target_resident, payloads[4], at),
            runtime=resident_runtime(target_resident, payloads[4]), negative_controls=resident_controls(target_resident))
        from lib.zun_init_layout import verify as init_layout
        from lib.zun_init_runtime import verify as init_runtime, negative_controls as init_controls
        init = directory["payloads"][1]
        at, size = init["decoded_file_offset"], init["size"]
        target_init = decoded[at:at + size]
        report["init_scopes"] = dict(layout=init_layout(WORK, target_init, payloads[1], at),
            runtime=init_runtime(target_init, payloads[1]), negative_controls=init_controls(target_init))
        from lib.zun_driver_scalar_layout import verify as scalar_layout
        from lib.zun_driver_scalar_runtime import verify as scalar_runtime, negative_controls as scalar_controls
        driver = directory["payloads"][3]
        at, size = driver["decoded_file_offset"], driver["size"]
        target_driver = decoded[at:at + size]
        report["driver_scalar_scopes"] = dict(layout=scalar_layout(WORK, target_driver, payloads[3], at, files, maintained),
            runtime=scalar_runtime(target_driver, payloads[3]), negative_controls=scalar_controls(target_driver))
        from lib.zun_driver_alignment import run as alignment_controls
        report["driver_alignment_controls"] = alignment_controls(files, WORK.parent,
            [str(ROOT / profile["binary_path"]), *profile["assembler_flags"]], dos + ["tlink", "@link.rsp"], execute, target_driver)
        need(recipe_inventory() == report["recipe_sha256"], "recipe changed during cold build")
        need(runtime_inventory() == report["consumed_runtime_sha256"], "consumed tiny runtime changed during cold build")
        need(sdk_inventory() == report["consumed_sdk_sha256"], "consumed SDK changed during cold build")
        need(report["emitter"] == emitter.attest(), "driver emitter identity drift")
        report.update(complete=True, same_tool_roundtrip=True)
        save()
    print(json.dumps({k: v for k, v in report.items() if k not in
                      {"rounds", "native_phases", "source_sha256", "maintained_inputs", "wrapper_runtime", "toolchain_surfaces"}}, indent=2))
    need(report["comparison"]["decoded_equal"] and report["comparison"]["stored_equal"],
         "complete source product differs from canonical ZUN; inspect payload comparisons")
    return report


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    build()


if __name__ == "__main__":
    main()
