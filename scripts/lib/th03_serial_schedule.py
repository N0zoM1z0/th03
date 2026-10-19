#!/usr/bin/env python3
"""Reviewed scheduling adapter for one unchanged two-cold MAIN replay.
Never call this script without the owning durable supervisor.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STATE_ROOT = ROOT / ".analysis/th03-main-serial"
REPLAY = ROOT / "scripts/replay_th03_main_exact_units.py"
PINS = {
    "scripts/replay_th03_main_exact_units.py": "5f48d81ddc3e53c63f4e6bd45511e566245201444657616a1435653e736511d8",
    "config/th03_main_exact_units.toml": "e5130f08cef59426096f2ce40bc31862128c7523005cd3594dfec7240bf42df4",
    "config/toolchain.toml": "abca6f4cca79a1f5be1c683546db05a8420b7ee3c635524d6c1eb9ef48b9d0cd",
}
PINS.update({
    "scripts/lib/__init__.py": "c23b7d19498cba043fa764379b8047fc8aaaddf6fefd54f8aaf131fa4aec0713",
    "scripts/lib/analysis.py": "5f3edcf4b4e3b958976288aa07900a15a91e95276c2305470f6669fdcb95d7bd",
    "scripts/lib/ghidra.py": "7032827832aae949aed20794cb36a292052476d6b0f886c20caea53f353aea85",
    "scripts/lib/hud_tc4_bridge.py": "557188d226089b841475c12d8b94434aff3c8c89b4fa8e20b562f0f7776ebc10",
    "scripts/lib/omf.py": "3fec01c38a13d6a13fc9296292f3b2a7075cdaf3e0897cfc31d1c83b84897030",
    "scripts/lib/pc98.py": "af46d18e4dfbe2c0915c04880031c64bb17133eb8df7ccfba44fbd99b5cb3fcf",
    "scripts/lib/reconstruction.py": "2fb69bd1e2e1eabb30514a7ed205e1b6d028043f05e062b59c3dc67d4298a950",
    "scripts/lib/targets.py": "4756db844953ba748077ff6e75e9df8a80692b8108e0eec3c3fa6dbeeb49ac93",
    "scripts/lib/tc4_omf_bridge.py": "c0143a3de65899e2dafe0f2f9ec77725e1810fcfe8f7e93c6f71e3915b815d24",
    "scripts/lib/toolchain.py": "7c668ef88059f313a2d0fc62d9601324480d210839610c7d02f17ef245dd95b9",
    "scripts/lib/zun.py": "28e7249d90dc0a8a6f9ad6d97ed879a5c05f6a171d4f558add859d5768d2e501"
})
CANDIDATE_PINS = {
    "config/th03_main_marisa_candidate.toml":
        "fd9722b0f16a8bfe305b7782697b729f2ea1ef3d7b13ea1f83ba21af0eaf908d",
    "config/th03_main_reimu_shared_candidate.toml":
        "8294faefad6ca71e8d9cc684070e043e43a65bbd9b3e856c178b0cdce08752d1",
    "config/th03_main_mima_gameplay_candidate.toml":
        "855730e3d9943ef8afa4117c3b5a4ebe0c22ae12de56049f847e69c6182c270d",
}
BUILD_SHA = "400349385d38fcb72d17f14c0e4680d677d8d704c15bcfbabb17725a6f2c9a95"
TUP_SHA = "441f516765ee1fbad1672a5a31e484c979d5fd12f61efe2348c521bdab659cd1"
EMPTY_SHA = hashlib.sha256(b"").hexdigest()
OPTIONS = b"[updater]\nnum_jobs = 1\n"
BEFORE = b":tup\r\nbin\\tup\r\ngoto return_from_tup\r\n"
AFTER = b":tup\r\nbin\\tup -j1\r\ngoto return_from_tup\r\n"
BUILD_ARGV = ["wine", "cmd", "/d", "/c",
              r"set PATH=C:\TASM50\BIN;C:\TC4\BIN;%PATH%"
              r"&&set PROCESSOR_ARCHITECTURE=AMD64"
              r"&&set PROCESSOR_ARCHITEW6432=AMD64&&build.bat"]

def sha(data):
    return hashlib.sha256(data).hexdigest()

def atomic(path, value):
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w") as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)

def check_regular(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError("missing or symlink input: " + str(path))

def check_pins(root, candidate):
    pins = dict(PINS)
    if candidate:
        if candidate not in CANDIDATE_PINS:
            raise ValueError("unreviewed candidate manifest")
        pins[candidate] = CANDIDATE_PINS[candidate]
    for name, expected in pins.items():
        p = root / name
        check_regular(p)
        if sha(p.read_bytes()) != expected:
            raise ValueError("input pin drift: " + name)
    return pins

def verify_options(raw):
    text = raw.decode("utf-8", errors="strict")
    rows = [line.strip() for line in text.splitlines()
            if line.strip().startswith("updater.num_jobs")]
    if len(rows) != 1 or not re.fullmatch(
            r"updater\.num_jobs\s*=\s*'1'\s+from\s+\.tup[/\\]options", rows[0]):
        raise ValueError("effective updater.num_jobs is not uniquely local 1")
    parsed = [line.strip() for line in text.splitlines()
              if re.fullmatch(r"Parsed option file:\s*\.tup[/\\]options", line.strip())]
    if len(parsed) != 1:
        raise ValueError("local Tup options parse marker absent or ambiguous")

class Schedule:
    def __init__(self, original_execute, root, run_id, candidate=False):
        if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", run_id):
            raise ValueError("invalid run id")
        self.original = original_execute
        self.root = root
        self.output = root / ".analysis/th03-main-exact" / run_id
        self.candidate = candidate
        self.rounds = []

    def __call__(self, argv, work, env, log):
        work, log = Path(work), Path(log)
        looks_cold = (argv == BUILD_ARGV or log.name == "cold-build.log"
                      or any("&&build.bat" in str(arg) for arg in argv))
        if not looks_cold:
            return self.original(argv, work, env, log)
        number = len(self.rounds) + 1
        expected = self.output / ("round" + str(number))
        if number > 2 or argv != BUILD_ARGV or work != expected / "source" or log != expected / "cold-build.log":
            raise ValueError("unexpected, duplicate or out-of-order cold build")
        # Reject symlinks in every path component below the canonical root.
        for p in [work, *work.parents]:
            if p == self.root:
                break
            if p.is_symlink():
                raise ValueError("symlink cold workspace")
        if work.resolve() != work or not work.is_dir():
            raise ValueError("noncanonical cold workspace")
        if (work / ".tup").exists() or (work / ".tup").is_symlink():
            raise ValueError("Tup directory must be absent before init")
        build = work / "build.bat"
        tup = work / "bin/tup.exe"
        ini = work / "Tupfile.ini"
        for p in (build, tup, ini):
            check_regular(p)
        build_bytes = build.read_bytes()
        if self.candidate:
            if build_bytes.count(AFTER) != 1 or BEFORE in build_bytes:
                raise ValueError("candidate scheduling carrier is not the reviewed -j1 form")
            original_build = build_bytes.replace(AFTER, BEFORE, 1)
        else:
            original_build = build_bytes
        if sha(original_build) != BUILD_SHA or sha(tup.read_bytes()) != TUP_SHA or sha(ini.read_bytes()) != EMPTY_SHA:
            raise ValueError("cold workspace tool/build pin drift")
        row = dict(round=number, policy="local-tup-num-jobs-1", build_before_sha256=sha(build_bytes),
                   tup_sha256=TUP_SHA, options_sha256=sha(OPTIONS), exact_acceptance=False,
                   phase="initializing", completed=False,
                   original_build_timeout_seconds=180, effective_build_timeout_seconds=300,
                   nonbuild_timeout_seconds=180, outer_supervisor_timeout_seconds=900)
        self.rounds.append(row)  # Repeated attempt cannot enter this round.
        sidecar = expected / "scheduling.json"
        atomic(sidecar, row)
        options = work / ".tup/options"
        try:
            row["init"] = self.original(["wine", "cmd", "/d", "/c", r"bin\tup init"],
                                       work, env, expected / "schedule-init.log")
            db = work / ".tup/db"
            check_regular(db)
            if (work / ".tup").is_symlink():
                raise ValueError("initialized Tup directory is a symlink")
            row["initial_db_sha256"] = sha(db.read_bytes())
            if options.exists() or options.is_symlink():
                raise ValueError("Tup options already exists after init")
            with options.open("xb") as f:
                f.write(OPTIONS)
                f.flush()
                os.fsync(f.fileno())
            row["phase"] = "verifying-options"
            atomic(sidecar, row)
            option_log = expected / "schedule-options.log"
            row["options_probe"] = self.original(["wine", "cmd", "/d", "/c", r"bin\tup options"],
                                                work, env, option_log)
            verify_options(option_log.read_bytes())
            if options.read_bytes() != OPTIONS or build.read_bytes() != build_bytes:
                raise ValueError("scheduling inputs changed before cold build")
            row["phase"] = "building"
            atomic(sidecar, row)
            # Only this fully validated, one-shot cold-build branch receives
            # the larger wall allowance. Other commands retain original execute().
            try:
                completed = subprocess.run(argv, cwd=work, env=env, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT, timeout=300)
            except subprocess.TimeoutExpired as exc:
                # subprocess.run kills/waits its direct child; the unchanged
                # owning supervisor cleans the remaining owned process group.
                partial = exc.output if exc.output is not None else b""
                log.write_bytes(partial)
                row["partial_timeout_log_sha256"] = sha(partial)
                row["partial_timeout_log_bytes"] = len(partial)
                raise
            log.write_bytes(completed.stdout)
            if completed.returncode:
                raise ValueError(f"tool exit {completed.returncode}; see {log.relative_to(self.root)}")
            result = {"argv": argv, "exit_code": completed.returncode,
                      "log_sha256": sha(completed.stdout)}
            row["completed"] = True
            row["phase"] = "finished"
            return result
        except BaseException as exc:
            row["error"] = f"{type(exc).__name__}: {exc}"
            raise
        finally:
            row["build_unchanged"] = build.is_file() and not build.is_symlink() and build.read_bytes() == build_bytes
            row["options_unchanged"] = options.is_file() and not options.is_symlink() and options.read_bytes() == OPTIONS
            atomic(sidecar, row)
            if row["completed"] and not (row["build_unchanged"] and row["options_unchanged"]):
                raise ValueError("scheduling inputs changed during cold build")

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--candidate-manifest", choices=sorted(CANDIDATE_PINS))
    ap.add_argument("--supervisor-state", type=Path, required=True,
                    help="owning durable supervisor status; no standalone launch")
    args = ap.parse_args()
    # Explicit supervisor binding is required; no alternate standalone route.
    expected_state = STATE_ROOT / "runs" / args.run_id / "status.json"
    if args.supervisor_state != expected_state:
        raise ValueError("wrong supervisor state path")
    state = json.loads(expected_state.read_text())
    runner = ROOT / "scripts/replay_th03_main_serial.py"
    if (state.get("run_id") != args.run_id
            or state.get("schedule_adapter_sha256") != sha(Path(__file__).read_bytes())
            or state.get("supervisor_script_sha256") != sha(runner.read_bytes())
            or state.get("original_replay_sha256") != PINS["scripts/replay_th03_main_exact_units.py"]):
        raise ValueError("supervisor has not pinned adapter, supervisor and original replay")
    owner = json.loads((STATE_ROOT / "active.claim/owner.json").read_text())
    if owner.get("run_id") != args.run_id:
        raise ValueError("supervisor claim belongs to another run")
    before = check_pins(ROOT, args.candidate_manifest)
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location("original_th03_replay", REPLAY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    schedule = Schedule(module.execute, ROOT, args.run_id, bool(args.candidate_manifest))
    module.execute = schedule
    argv = [str(REPLAY), "--run-id", args.run_id]
    if args.candidate_manifest:
        argv += ["--candidate-manifest", args.candidate_manifest]
    old_argv = sys.argv
    try:
        sys.argv = argv
        result = module.main()
        if result == 0 and (len(schedule.rounds) != 2 or not all(r["completed"] for r in schedule.rounds)):
            raise ValueError("successful replay did not perform two scheduled cold builds")
        return result
    finally:
        sys.argv = old_argv
        if check_pins(ROOT, args.candidate_manifest) != before:
            raise ValueError("adapter control inputs changed")

if __name__ == "__main__":
    raise SystemExit(main())
