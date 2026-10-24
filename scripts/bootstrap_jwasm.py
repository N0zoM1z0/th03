#!/usr/bin/env python3
"""Materialize/check the bounded ZUN OMF emitter from pinned public source."""

import argparse
import hashlib
import os
from pathlib import Path
import subprocess
import tomllib

ROOT = Path(__file__).resolve().parents[1]
PROFILE = "config/th03_zun_driver_jwasm.toml"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def need(value, message):
    if not value:
        raise ValueError(message)


def config():
    return tomllib.loads((ROOT / PROFILE).read_text())


def attest():
    c = config()
    source = ROOT / c["source_path"]
    binary = ROOT / c["binary_path"]
    need(not source.is_symlink() and not binary.is_symlink(), "JWasm symlink input")
    revision = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"]).decode().strip()
    need(revision == c["revision"], "JWasm source revision drift")
    subprocess.run(["git", "-C", str(source), "diff", "--quiet", "HEAD"], check=True)
    archive = subprocess.check_output(["git", "-C", str(source), "archive", "--format=tar", revision])
    need(sha(archive) == c["archive_sha256"], "JWasm source archive drift")
    raw = binary.read_bytes()
    need(len(raw) == c["binary_bytes"] and sha(raw) == c["binary_sha256"], "JWasm executable drift")
    version = subprocess.run([str(binary), "-?"], capture_output=True, timeout=15)
    need(version.returncode == c["help_exit_code"] and version.stdout.decode().splitlines()[0] == c["version"],
         "JWasm version/execution mismatch")
    return dict(profile=PROFILE, profile_sha256=sha((ROOT / PROFILE).read_bytes()),
                source_revision=revision, source_archive_sha256=sha(archive),
                binary_sha256=sha(raw), version=c["version"], original_assembler_identified=False)


def bootstrap():
    c = config()
    source = ROOT / c["source_path"]
    if not source.exists():
        source.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(source)], check=True)
        subprocess.run(["git", "-C", str(source), "fetch", "--depth=1", c["repository"], c["revision"]], check=True)
        subprocess.run(["git", "-C", str(source), "checkout", "--detach", "FETCH_HEAD"], check=True)
    revision = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"]).decode().strip()
    need(revision == c["revision"], "existing JWasm source has a different revision")
    subprocess.run(["git", "-C", str(source), "diff", "--quiet", "HEAD"], check=True)
    archive = subprocess.check_output(["git", "-C", str(source), "archive", "--format=tar", revision])
    need(sha(archive) == c["archive_sha256"], "JWasm source archive mismatch before build")
    subprocess.run(c["build_command"], cwd=source,
                   env=dict(os.environ, SOURCE_DATE_EPOCH=c["source_date_epoch"]), check=True)
    return attest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    if os.nice(0) < 10:
        os.nice(10 - os.nice(0))
    print(attest() if args.check else bootstrap())


if __name__ == "__main__":
    main()
