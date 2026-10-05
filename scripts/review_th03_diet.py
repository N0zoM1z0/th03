#!/usr/bin/env python3
"""Restore private copies of pinned DIET targets, without accepting source.

The canonical stored images remain immutable. Decoded CODE/layout/relocations
are a separate review namespace; a restoration is not a reconstructed product.
Serialize this console-only Wine writer with every Borland writer.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tomllib

from lib.pc98 import describe_blob, parse_mz
from lib.targets import find_artifact, read_verified_artifact

ROOT = Path(__file__).resolve().parents[1]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check_stored_diet(data: bytes) -> None:
    image = parse_mz(data)
    if (not image.valid or image.header.header_size != 32
        or image.header.number_of_relocations != 0 or data[28:32] != b"diet"):
        raise ValueError("stored target is not the reviewed DIET MZ envelope")


def check_restored(data: bytes, expected: dict) -> dict:
    result = describe_blob(data)
    if (result["size"] != expected["decoded_size"]
        or result["sha256"] != expected["decoded_sha256"]
        or result["format"] != expected["decoded_format"]
        or not result["format_integrity"]["valid"]):
        raise ValueError("decoded format, complete bytes or size differs")
    if expected.get("reference_input_md5") not in (None, result["md5"]):
        raise ValueError("decoded bytes differ from recorded reference input MD5")
    return result


def restore_succeeded(returncode: int, output: bytes) -> bool:
    # The candidate DIET 1.45f tool returns 1 after restoring one file. This
    # observed convention is checked alongside complete output bytes, not
    # treated as sufficient evidence of success by itself.
    return returncode == 1 and b"Success!" in output


def restore(run_id: str, selected: list[str]) -> dict:
    if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", run_id):
        raise ValueError("run-id must use 1-64 ASCII letters, digits, underscores or hyphens")
    config_path = ROOT / "config/th03_diet.toml"
    config_bytes = config_path.read_bytes()
    config = tomllib.loads(config_bytes.decode())
    if config["schema_version"] != 1:
        raise ValueError("unsupported DIET diagnostic schema")
    expected = {a["id"]: a for a in config["artifacts"]}
    ids = selected or list(expected)
    if len(set(ids)) != len(ids) or set(ids) - expected.keys():
        raise ValueError("unknown or duplicate DIET artifact selection")
    frozen = {config_path: config_bytes}
    frozen.update({path: path.read_bytes() for path in (
        ROOT / "config/targets.toml", ROOT / "config/toolchain.toml",
        Path(__file__).resolve(),
    )})
    targets = tomllib.loads(frozen[ROOT / "config/targets.toml"].decode())
    originals = {name: read_verified_artifact(ROOT, find_artifact(targets, name)) for name in ids}
    for data in originals.values():
        check_stored_diet(data)
    tool = ROOT / config["tool"]["path"]
    tool_bytes = tool.read_bytes()
    if len(tool_bytes) != config["tool"]["size"] or sha(tool_bytes) != config["tool"]["sha256"]:
        raise ValueError("DIET tool identity differs")
    # Attest the console runner/toolchain before this additional legacy tool.
    subprocess.run([sys.executable, "scripts/attest_toolchain.py"], cwd=ROOT, check=True)
    toolchain = tomllib.loads(frozen[ROOT / "config/toolchain.toml"].decode())
    prefix = ROOT / toolchain["paths"]["wine_prefix"]
    output = ROOT / ".analysis/th03-diet" / run_id
    output.mkdir(parents=True, exist_ok=False)
    stem = "D" + sha(run_id.encode())[:7].upper()
    work = prefix / "drive_c" / stem
    work.mkdir(exist_ok=False)
    shutil.copy2(tool, work / "DIET.EXE")
    env = os.environ.copy()
    env.update(DISPLAY="", WAYLAND_DISPLAY="", WINEDEBUG="-all", WINEPREFIX=str(prefix),
               MSDOS_PATH=r"C:\TC4\BIN")
    runner = ["wine", str(ROOT / toolchain["paths"]["msdos_player"]), "-e", "-x", "DIET.EXE"]
    commands = []

    def execute(label: str, args: list[str]):
        result = subprocess.run(runner + args, cwd=work, env=env,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
        (output / (label + ".log")).write_bytes(result.stdout)
        commands.append({"argv": runner + args, "returncode": result.returncode,
                         "output_sha256": sha(result.stdout)})
        return result

    check = execute("diet-selfcheck", ["-!"])
    if check.returncode != 0 or b"DIET.EXE is original file!" not in check.stdout:
        raise ValueError("DIET selfcheck did not pass")
    observations = []
    for name in ids:
        declaration = expected[name]
        filename = declaration["filename"]
        if not re.fullmatch(r"[A-Z0-9_]{1,8}\.(EXE|COM)", filename):
            raise ValueError("unsafe DIET working filename")
        destination = work / filename
        destination.write_bytes(originals[name])
        result = execute(name, ["-ra", filename])
        if not restore_succeeded(result.returncode, result.stdout):
            raise ValueError(f"DIET restoration did not report success: {name}")
        decoded = destination.read_bytes()
        description = check_restored(decoded, declaration)
        reference_sha256 = None
        if declaration.get("reference_root"):
            reference = subprocess.check_output(
                ["git", "show", f"{config['reference_revision']}:{declaration['reference_root']}"],
                cwd=ROOT / "_reference/ReC98",
            )
            md5 = re.search(rb"Input\s+MD5\s*:\s*([0-9a-fA-F]{32})", reference)
            if not md5 or md5[1].decode().lower() != declaration["reference_input_md5"]:
                raise ValueError("frozen reference root input MD5 differs")
            reference_sha256 = sha(reference)
        decoded_path = output / filename.lower()
        decoded_path.write_bytes(decoded)
        observations.append({"artifact": name, "stored": describe_blob(originals[name]),
                             "decoded": description,
                             "decoded_path": decoded_path.relative_to(ROOT).as_posix(),
                             "reference_root": declaration.get("reference_root"),
                             "reference_root_sha256": reference_sha256,
                             "reference_input_md5": declaration.get("reference_input_md5")})
    if (any(path.read_bytes() != data for path, data in frozen.items())
        or tool.read_bytes() != tool_bytes or (work / "DIET.EXE").read_bytes() != tool_bytes
        or any(read_verified_artifact(ROOT, find_artifact(targets, name)) != originals[name] for name in ids)):
        raise ValueError("canonical target, DIET tool or decoder configuration changed")
    receipt = {"kind": "th03-private-diet-restoration-diagnostic", "run_id": run_id,
               "scope": config["scope"], "observed_utc": datetime.now(timezone.utc).isoformat(),
               "tool_sha256": sha(tool_bytes), "config_sha256": sha(config_bytes),
               "reference_revision": config["reference_revision"],
               "source_inputs": {path.relative_to(ROOT).as_posix(): sha(data)
                                 for path, data in frozen.items()},
               "commands": commands, "observations": observations,
               "canonical_targets_unchanged": True, "source_acceptance": False,
               "exact_acceptance": False, "restoration_checks_pass": True}
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--artifact", action="append", default=[])
    args = parser.parse_args()
    try:
        result = restore(args.run_id, args.artifact)
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"DIET diagnostic: FAIL: {error}", file=sys.stderr)
        return 1
    print(f"DIET diagnostic: PASS; {len(result['observations'])} private restorations; zero exact/source credit")
    print(f"receipt: .analysis/th03-diet/{args.run_id}/receipt.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
