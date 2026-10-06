#!/usr/bin/env python3
"""Cold-build the maintained ZUN wrapper with explicitly unowned private payloads."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib
import capstone
import unicorn

from capstone import Cs, CS_ARCH_X86, CS_MODE_16
from inventory_rec98_th03 import frozen_files
from lib.omf import describe_omf, normalize_dependency_timestamps
from lib.targets import load_target_manifest, find_artifact, read_verified_artifact
from lib.zun import PSP_SIZE, digest, parse_launcher, dispatch_observation, compose_launcher

ROOT = Path(__file__).resolve().parents[1]


def replay(run_id, cached_run=None):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", run_id):
        raise ValueError("unsafe run ID")
    freeze_paths = ["config/th03_zun_launcher.toml", "config/th03_diet.toml",
                    "config/targets.toml", "config/toolchain.toml", "src/zun/launcher.asm",
                    "src/zun/transfer_call.asm", "src/zun/transfer_helper.asm",
                    "scripts/replay_th03_zun_launcher.py", "scripts/lib/zun.py",
                    "scripts/lib/omf.py", "scripts/lib/targets.py", "scripts/inventory_rec98_th03.py"]
    frozen = {path: (ROOT / path).read_bytes() for path in freeze_paths}
    config = tomllib.loads(frozen[freeze_paths[0]].decode())
    diet = tomllib.loads(frozen["config/th03_diet.toml"].decode())
    targets = load_target_manifest(ROOT / "config/targets.toml")
    stored = read_verified_artifact(ROOT, find_artifact(targets, "th03-zun"))
    def pin(path, expected):
        data = (ROOT / path).read_bytes()
        if digest(data) != expected:
            raise ValueError(f"changed private input: {path}")
        frozen[path] = data
        return data
    cold = json.loads(pin(config["cold_receipt"], config["cold_receipt_sha256"]))
    restoration = json.loads(pin(config["diet_receipt"], config["diet_receipt_sha256"]))
    decoded_pin = next(a for a in diet["artifacts"] if a["id"] == "th03-zun")
    decoded = pin(config["decoded_path"], decoded_pin["decoded_sha256"])
    lineage = next(o for o in restoration["observations"] if o["artifact"] == "th03-zun")
    if not (cold["pass"] and cold["all_products_equal"] and
            restoration["restoration_checks_pass"] and restoration["canonical_targets_unchanged"] and
            cold["reference_revision"] == restoration["reference_revision"] == config["reference_revision"] and
            lineage["stored"]["sha256"] == digest(stored) and
            lineage["decoded"]["sha256"] == digest(decoded)):
        raise ValueError("invalid source/restoration lineage")
    directory = parse_launcher(decoded, config["stub_size"])
    files = frozen_files(config["reference_revision"])
    payloads = {}
    for payload in config["payloads"]:
        if payload["reference_path"] in files:
            data = files[payload["reference_path"]]
            if digest(data) != payload["sha256"]:
                raise ValueError("changed frozen binary payload")
        else:
            rounds = [pin(p, payload["sha256"]) for p in payload["cold_paths"]]
            if rounds[0] != rounds[1]:
                raise ValueError("payload cold rounds differ")
            for round_, data in zip(cold["rounds"], rounds):
                product = round_["products"].get(payload["reference_path"])
                if product is not None and product != digest(data):
                    raise ValueError("payload absent from cold product receipt")
            data = rounds[0]
        payloads[payload["filename"]] = data
    scaffold = pin(config["scaffold_path"], config["scaffold_sha256"])
    second_scaffold = pin(config["second_scaffold_path"], config["scaffold_sha256"])
    if scaffold != second_scaffold or any(
            r["products"]["bin/th03/zun.com"] != digest(scaffold) for r in cold["rounds"]):
        raise ValueError("scaffold composition is not the two recorded cold products")
    scaffold_directory = parse_launcher(scaffold, config["stub_size"])
    if [p["name"] for p in directory["payloads"]] != [p["option"] for p in config["payloads"]]:
        raise ValueError("unexpected target options")
    if any(p["sha256"] != digest(payloads[c["filename"]]) for p, c in zip(
            scaffold_directory["payloads"], config["payloads"])):
        raise ValueError("scaffold payload membership differs")
    output = ROOT / ".analysis/th03-zun-launcher" / run_id
    output.mkdir(parents=True, exist_ok=False)
    if cached_run is not None:
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", cached_run) or cached_run == run_id:
            raise ValueError("unsafe or self-referential cached run")
        cache = ROOT / ".analysis/th03-zun-launcher" / cached_run
        rounds = []
        for number in (1, 2):
            modules, objects = {}, {}
            source_associations = {}
            for module in ("launcher", "transfer_call", "transfer_helper"):
                stem = cache / f"round{number}" / module
                for suffix in ("asm", "com", "obj", "map", "rsp"):
                    path = stem.with_suffix("." + suffix)
                    data = path.read_bytes()
                    frozen[str(path.relative_to(ROOT))] = data
                cached_source = stem.with_suffix(".asm").read_bytes()
                maintained_source = frozen[f"src/zun/{module}.asm"]
                exact_source = cached_source == maintained_source
                if not exact_source:
                    # One explicitly pinned empty line lost two tabs during
                    # whitespace verification; no instruction text was changed.
                    if not (module == "launcher" and
                            digest(cached_source) == config["cached_launcher_before_empty_line_cleanup_sha256"] and
                            cached_source.count(b"\t\t\n") == 1 and
                            cached_source.replace(b"\t\t\n", b"\n", 1) == maintained_source):
                        raise ValueError("cached compiler source differs from maintained source")
                source_associations[module] = dict(exact_text_match=exact_source,
                                                  cached_source_sha256=digest(cached_source),
                                                  maintained_source_sha256=digest(maintained_source),
                                                  pinned_empty_line_cleanup=(not exact_source))
                object_bytes = stem.with_suffix(".obj").read_bytes()
                obj = describe_omf(object_bytes)
                if not obj["valid"] or "Turbo Assembler  Version 5.0" not in obj["translator_comments"]:
                    raise ValueError("invalid cached launcher OMF")
                modules[module] = stem.with_suffix(".com").read_bytes()
                objects[module] = digest(normalize_dependency_timestamps(object_bytes))
            data = compose_launcher(modules["launcher"], modules["transfer_call"], modules["transfer_helper"],
                                    [p["option"] for p in config["payloads"]],
                                    [payloads[p["filename"]] for p in config["payloads"]])
            parent = cache / f"round{number}" / "zun.com"
            parent_bytes = parent.read_bytes()
            frozen[str(parent.relative_to(ROOT))] = parent_bytes
            if data != scaffold or parent_bytes != data:
                raise ValueError("cached composition differs from pinned scaffold")
            rounds.append(dict(round=number, fresh_build=False, directory=parse_launcher(data, config["stub_size"]),
                               com_sha256=digest(data), normalized_omf_sha256=objects,
                               source_associations=source_associations,
                               module_sizes={k: len(v) for k, v in modules.items()}))
    else:
        subprocess.run([sys.executable, "scripts/attest_toolchain.py"], cwd=ROOT, check=True)
        toolchain = tomllib.loads(frozen["config/toolchain.toml"].decode())
        prefix = ROOT / toolchain["paths"]["wine_prefix"]
        env = os.environ.copy()
        env.update(DISPLAY="", WAYLAND_DISPLAY="", WINEDEBUG="-all", WINEPREFIX=str(prefix),
                   MSDOS_PATH=r"C:\TC4\BIN")
        runner = ["wine", str(ROOT / toolchain["paths"]["msdos_player"]), "-e", "-x"]
        rounds = []
        for number in (1, 2):
            work = prefix / "drive_c" / ("Z" + digest(f"{run_id}-{number}".encode())[:7].upper())
            work.mkdir(exist_ok=False)
            dest = output / f"round{number}"
            dest.mkdir()
            commands = []
            modules = {}
            objects = {}
            for module in ("launcher", "transfer_call", "transfer_helper"):
                (work / f"{module}.asm").write_bytes(frozen[f"src/zun/{module}.asm"])
                rsp = f"-c -s -t -3 {module}.obj,{module}.com,{module}.map,\r\n".encode()
                (work / "link.rsp").write_bytes(rsp)
                flags = ["/m", "/mx", "/kh32768", "/t"]
                if module == "transfer_call":
                    flags.append(f"/dPAYLOAD_BYTES={sum(len(p) for p in payloads.values())}")
                for name, args in [
                    ("assemble", ["wine", r"C:\TASM50\BIN\TASM32.EXE"] + flags + [f"{module}.asm,{module}.obj"]),
                    ("link", runner + ["tlink", "@link.rsp"]),
                ]:
                    result = subprocess.run(args, cwd=work, env=env,
                                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
                    (dest / f"{module}-{name}.log").write_bytes(result.stdout)
                    commands.append(dict(argv=args, exit_code=result.returncode,
                                         output_sha256=digest(result.stdout)))
                    if result.returncode:
                        raise ValueError(f"{module} {name} failed; inspect {dest}")
                modules[module] = (work / f"{module}.com").read_bytes()
                object_bytes = (work / f"{module}.obj").read_bytes()
                obj = describe_omf(object_bytes)
                if not obj["valid"] or "Turbo Assembler  Version 5.0" not in obj["translator_comments"]:
                    raise ValueError("invalid maintained launcher OMF")
                objects[module] = digest(normalize_dependency_timestamps(object_bytes))
                for suffix in ("asm", "com", "obj", "map"):
                    shutil.copy2(work / f"{module}.{suffix}", dest / f"{module}.{suffix}")
                (dest / f"{module}.rsp").write_bytes(rsp)
            data = compose_launcher(modules["launcher"], modules["transfer_call"], modules["transfer_helper"],
                                    [p["option"] for p in config["payloads"]],
                                    [payloads[p["filename"]] for p in config["payloads"]])
            (dest / "zun.com").write_bytes(data)
            metadata = parse_launcher(data, config["stub_size"])
            if data != scaffold:
                raise ValueError("maintained launcher differs from pinned scaffold composition")
            rounds.append(dict(round=number, commands=commands, directory=metadata,
                               com_sha256=digest(data), normalized_omf_sha256=objects,
                               module_sizes={k: len(v) for k, v in modules.items()}))
    runtime = []
    for label, data, metadata in [("decoded-target", decoded, directory),
                                   ("maintained-candidate", scaffold, scaffold_directory)]:
        observations = [dispatch_observation(data, metadata, "", ""),
                        dispatch_observation(data, metadata, " -X", "-X")]
        for index in range(1, 6):
            observed = dispatch_observation(data, metadata, f"  -{index} hello", f"-{index}")
            if not (observed["tail"] == " hello" and observed["sp"] == 0xfffc and
                    observed["remaining_count"] == 6 - index and not (observed["flags"] & 0x400)):
                raise ValueError("dispatch stack/DF/argument state differs from reviewed ABI")
            observations.append(observed)
        listing = "\r\n" + "".join(" " + p["name"].ljust(8) + " " for p in metadata["payloads"]) + "\r\n"
        if observations[0]["stdout"] != listing:
            raise ValueError("no-argument procedure listing differs")
        if observations[1]["stdout"] != "No COM-Soft !!!\r\n\n":
            raise ValueError("unknown procedure error output differs")
        runtime.append(dict(image=label, observations=observations))
    mutated = bytearray(decoded)
    mutated[directory["helper_offset"] + 4] = 1  # MOV AX,0101h instead of 0100h.
    try:
        dispatch_observation(bytes(mutated), directory, " -1 hello", "-1")
    except ValueError as error:
        if "missed the payload entry" not in str(error):
            raise
    else:
        raise ValueError("wrong transfer address escaped the runtime negative control")
    differences = [i for i, (a, b) in enumerate(zip(decoded, scaffold)) if a != b]
    encodings = []
    disassembler = Cs(CS_ARCH_X86, CS_MODE_16)
    for offset in config["encoding_difference_offsets"]:
        owner = next(p for p in directory["payloads"]
                     if p["decoded_file_offset"] <= offset < p["decoded_file_offset"] + p["size"])
        address = PSP_SIZE + offset - owner["decoded_file_offset"]
        pairs = [next(disassembler.disasm(data[offset:offset + 15], address)) for data in (decoded, scaffold)]
        if (pairs[0].size != pairs[1].size or
                (pairs[0].mnemonic, pairs[0].op_str) != (pairs[1].mnemonic, pairs[1].op_str)):
            raise ValueError("encoding difference is not the reviewed instruction pair")
        encodings.append(dict(decoded_file_offset=offset, payload=owner["name"],
                              payload_runtime_offset=address, mnemonic=pairs[0].mnemonic,
                              operands=pairs[0].op_str, target_hex=pairs[0].bytes.hex(),
                              candidate_hex=pairs[1].bytes.hex(), size=pairs[0].size))
    if set(differences) != {i for e in encodings for i in range(
            e["decoded_file_offset"], e["decoded_file_offset"] + e["size"]) if decoded[i] != scaffold[i]}:
        raise ValueError("additional raw differences outside reviewed encoding pairs")
    if len(differences) != 10 or any(e["payload"] != "-4" for e in encodings):
        raise ValueError("raw failure vector differs")
    if rounds[0]["com_sha256"] != rounds[1]["com_sha256"] or \
            rounds[0]["normalized_omf_sha256"] != rounds[1]["normalized_omf_sha256"]:
        raise ValueError("maintained launcher cold builds differ")
    for path, original in frozen.items():
        if (ROOT / path).read_bytes() != original:
            raise ValueError(f"input mutated during replay: {path}")
    if read_verified_artifact(ROOT, find_artifact(targets, "th03-zun")) != stored:
        raise ValueError("canonical stored target mutated")
    receipt = dict(kind="th03-zun-maintained-launcher-candidate", run_id=run_id,
                   observed_utc=datetime.now(timezone.utc).isoformat(),
                   source_inputs={p: digest(d) for p, d in frozen.items()},
                   stored_sha256=digest(stored), decoded_sha256=digest(decoded),
                   reference_revision=config["reference_revision"], directory=directory,
                   rounds=rounds, runtime=runtime, encoding_differences=encodings,
                   full_decoded_raw_equal=False, different_bytes=10,
                   wrapper_scoped_raw_equal=all(directory[k] == scaffold_directory[k] for k in [
                       "stub_sha256", "directory_sha256", "helper_sha256"]),
                   cold_wrapper_checks_pass=(cached_run is None), cached_run=cached_run,
                   cached_candidates_checked=(cached_run is not None), payload_source_acceptance=False,
                   wrong_transfer_address_rejected=True,
                   runtime_provider=dict(unicorn_version=unicorn.__version__,
                                         capstone_version=capstone.__version__, python=sys.version,
                                         dos_model="Only stdout and exit services; no payload or hardware execution"),
                   exact_acceptance=False, runtime_scope="Wrapper only; stop before payload entry")
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"PASS maintained wrapper {'cached' if cached_run else 'cold'}/runtime diagnostics; full decoded raw equality FAIL (10 bytes): {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--review-cached-run", help="Read existing source-bound outputs; never grants cold acceptance")
    args = parser.parse_args()
    replay(args.run_id, args.review_cached_run)
