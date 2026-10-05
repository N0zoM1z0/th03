#!/usr/bin/env python3
"""Factory-native read-only MZ analysis, with same-process database attestation."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid

from ghidra import ROOT, environment, private_export, project_name
from lib.analysis import load_analysis_config
from lib.ghidra import attest_mz_export
from lib.pc98 import parse_mz
from lib.targets import find_artifact, load_target_manifest, read_verified_artifact


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", default="th03-main",
                        choices=("th03-op", "th03-main", "th03-mainl", "th03-zun"))
    parser.add_argument("operation", choices=("check", "decompile", "query"))
    parser.add_argument("arguments", nargs="*")
    args = parser.parse_args()
    config = load_analysis_config(ROOT / "config/analysis_toolchain.toml")
    artifact = find_artifact(load_target_manifest(ROOT / "config/targets.toml"), args.artifact)
    target = read_verified_artifact(ROOT, artifact)
    image = parse_mz(target)
    subprocess.run([sys.executable, "scripts/attest_analysis_toolchain.py"],
                   cwd=ROOT, check=True)
    query = []
    output = None
    if args.operation != "check":
        if len(args.arguments) < 2:
            parser.error("query/decompile requires OUTPUT and query arguments")
        output = private_export(Path(args.arguments[0]))
        output.parent.mkdir(parents=True, exist_ok=True)
        output.unlink(missing_ok=True)
        values = args.arguments[1:]
        if args.operation == "query":
            index = {"list_functions": 3, "search_strings": 2}.get(values[0])
            if index is not None and len(values) > index:
                values[index] = "text:" + values[index]
        script = "DecompileFunctions.java" if args.operation == "decompile" else "QueryProgram.java"
        query = ["-postScript", script, str(output), *values]
    scratch = ROOT / ".analysis/factory-native-ghidra"
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="attest-", dir=scratch) as temporary:
        export = Path(temporary)
        nonce = uuid.uuid4().hex
        command = [str(ROOT / ".tools/ghidra/support/analyzeHeadless"),
                   str(ROOT / "ghidra-project"), project_name(args.artifact),
                   "-process", Path(artifact["private_path"]).name,
                   "-readOnly", "-noanalysis", "-max-cpu", "2",
                   "-postScript", "ExportMzAttestation.java", str(export),
                   str(len(target)), str(image.header.header_size),
                   str(image.header.declared_file_size), nonce,
                   *query, "-scriptPath", str(ROOT / "scripts/ghidra")]
        subprocess.run(command, cwd=ROOT, env=environment(config), check=True)
        report = attest_mz_export(export, target, artifact, config, expected_nonce=nonce)
        if not report["ready"]:
            raise ValueError("same-process MZ database attestation failed")
        if output is not None and not output.is_file():
            raise ValueError("query produced no output")
        # Bind disk bytes once more after the query before releasing semantic output.
        if read_verified_artifact(ROOT, artifact) != target:
            raise ValueError("target changed during analysis")
        load_digest = hashlib.sha256(image.program_image).hexdigest()
        relocated_digest = report["target"]["relocated_load_module_sha256"]
        print("FACTORY_GHIDRA_MZ_ATTESTATION_V1:"
              f"{hashlib.sha256(target).hexdigest()}:"
              f"{hashlib.md5(target, usedforsecurity=False).hexdigest()}:"
              f"{len(target)}:{image.header.header_size}:{len(image.program_image)}:"
              f"{image.header.initial_relative_cs:04x}:{image.header.initial_ip:04x}:"
              f"{len(image.relocations)}:{load_digest}:{relocated_digest}:{len(report['samples'])}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"error: headless MZ analysis failed: {error}", file=sys.stderr)
        sys.exit(1)
