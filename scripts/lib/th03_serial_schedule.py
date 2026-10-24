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
    'scripts/review_th03_cpu_link_order.py': '0b96a855a823aa749cc35ab0b8d4a80b5740bf42a7996a7c934881981df5ba82',
    "scripts/replay_th03_main_exact_units.py": "c30a2fefcc204625c78c531b0439a3f13ab6705d99c9c28225e21bd7c4dc50ea",
    "config/th03_main_exact_units.toml": "164c58b84007f413158f323da8e80b65772b70a0d897fc11baf80da083f8b263",
    "config/toolchain.toml": "c270e15bb809884008d85f1b7b8429ee1795ec65f548dcbbe4b65fd43841e2d7",
}
PINS.update({
    "scripts/lib/th03_yumemi_bomb_candidate.py": "9377b07c365e218cba09fb75215fdb2d5f773185b3167dde41ce32c6161bda6f",
    "scripts/lib/th03_score_candidate.py": "d407cf98a7d5a8b1009e4289563a337b200d23b3f18fadc50257c0f873582434",
    "scripts/lib/__init__.py": "c23b7d19498cba043fa764379b8047fc8aaaddf6fefd54f8aaf131fa4aec0713",
    "scripts/lib/analysis.py": "f643eb39eba10246310d3a418cfdd029c9c4046c8146b5230cedb2cab05aabfa",
    "scripts/lib/ghidra.py": "7032827832aae949aed20794cb36a292052476d6b0f886c20caea53f353aea85",
    "scripts/lib/omf.py": "3fec01c38a13d6a13fc9296292f3b2a7075cdaf3e0897cfc31d1c83b84897030",
    "scripts/lib/pc98.py": "af46d18e4dfbe2c0915c04880031c64bb17133eb8df7ccfba44fbd99b5cb3fcf",
    "scripts/lib/reconstruction.py": "2fb69bd1e2e1eabb30514a7ed205e1b6d028043f05e062b59c3dc67d4298a950",
    "scripts/lib/targets.py": "4756db844953ba748077ff6e75e9df8a80692b8108e0eec3c3fa6dbeeb49ac93",
    "scripts/lib/toolchain.py": "7c668ef88059f313a2d0fc62d9601324480d210839610c7d02f17ef245dd95b9",
    "scripts/lib/zun.py": "28e7249d90dc0a8a6f9ad6d97ed879a5c05f6a171d4f558add859d5768d2e501"
})
PINS.update({
    'scripts/lib/th03_player_tail_candidate.py': '31276ec4694a35aa5ac26ebfe0f39ad64f476945a12e990edcd4dc17c298209e',
    'scripts/lib/th03_tail_compare.py': '9d96fdc4db8eb910233c19fa146e3c2472b28b30c55026408a9c10e8a74078ce',
    'scripts/lib/th03_tail_map.py': 'ce3f8cc70b35a46f5898dab8ca442aa73648ee561a6abb83460eaa2caf17be40',
    'scripts/lib/th03_tail_model.py': '0485b5f3bab8825a0c0d3e10dfe15345d83dda3528ac1979e6b423f9fdaae0f6',
    'scripts/lib/th03_tail_public_display.json': '3219df80ac6d56269c1c83af0d5fd4e43286a304ca93bcea09606496cf1b7cb9',
    'scripts/lib/th03_tail_warning_gate.py': 'ef3a348181ec5887f96582cb052442ee54f50126cb85e49c9d190378b97c922f',
})
PINS.update({'scripts/lib/th03_cpu_gates.py': 'e56f59fc7890db4094e460a18763e846b1d7b960b035a01a221cbfa68ca95709', 'scripts/lib/th03_cpu_map_expectation.json': 'fb4cc0b26827e0c668c1ed2d791df20361307debc1fffd6de0fd95d6648426bc', 'scripts/lib/th03_cpu_map.py': 'fe015bc5deefa26ef273b7967ff75c71bc04a6605d1172187e55c223fa24476d', 'scripts/lib/th03_cpu_display.py': 'f1ca1d9f4f8c258a4fd3ed35ffebfa332ff5587c1e1e5cfe0ae89097498daf15', 'scripts/lib/th03_cpu_expectation.json': 'b1f1bdad5ba163955ec5a1ef4f1578316272c3b766fac342746b5b57af7be34e', 'scripts/lib/th03_cpu_binding.json': '5d683b43ed121a070315d0597dbf1839178982d67875e7c4d10f56767cb813af', 'scripts/lib/th03_cpu_dependencies.json': '0497317cea02dd84d806e1e3aa6faf65df065ff2f996f7ff5507cbedbb4b7152', 'scripts/lib/th03_cpu_baseline_pins.json': '0c5d11db2450fbb8ff1e3623d4d73c2051c87d6882728e14a74e745967812923', 'scripts/lib/th03_cpu_object.py': 'e01420bbebbcb4d44d01cd8e9601d717c92d20b77c996960e11e7d5e5bb019f4', 'scripts/lib/th03_cpu_model.py': '9c4c333474638732a11c7517392e97013587070d50c9b953999d4ffc8b748598', 'scripts/lib/th03_player_cpu_candidate.py': '053edbabe6c9a3dc3a90e1f421e275c5d372490a1d5d5b27a4e5f2427f460fe6'})
PINS.update({'scripts/lib/th03_charge_root.py': 'f3d11020a51ceb35f97e08edc0c7ad211b91691bbdd142352f263cafd1e56bd4', 'scripts/lib/th03_charge_contract.json': '76be5fcde93d6840bcb923b446c93ca6e8a4f193b2c44593961e94d6a4772ccd', 'scripts/lib/th03_charge_verify.py': '1f635f6afd83dce924c24fceb55247ec2d0262b90db6f105d2925423f14d8d32', 'scripts/lib/th03_charge_map.py': '7f547a8a769e35961c9df2f258cb20c599ce74dc5599ea2a1b8bbacbaa470892', 'scripts/lib/th03_yumemi_charge_candidate.py': '57a238aaa5fcedbabe73441ec193b6328e7274908f67bfc5314a33d6145a92c3', 'scripts/lib/th03_charge_map_contract.json': 'd670c354729d27b266218f1cb45c84eefe1a0c1fbf95a7e483aa8e30c9aad95b', 'scripts/lib/th03_charge_root_contract.json': 'b5ac26eacea68a8ba25313dbc894f70bf88d16dd6e9327e72aeb5b17baecad40', 'scripts/review_th03_main_yumemi_charge_runtime.py': 'bf0a1fe18b7436789fc9d5045a5a3ab97fa1102005913dd1676644b9582749f3', 'scripts/compare_th03_main_yumemi_charge_runtime.py': 'a5d378e57f3f9345ad2c35759f462fcdb77586cfd646e6caff4c5459f956f10c'})
CANDIDATE_PINS = {
    "config/th03_main_yumemi_charge_candidate.toml": "738adfd7eed18609c45eee7a95fa100b9d8659f214875b58305da62bd7bcd4bc",
    "config/th03_main_player_cpu_candidate.toml": "2420db4423b3f7269799ac1631f04cffd2ad322c7f3dda687600de27c22400f5",
    "config/th03_main_player_tail_candidate.toml": "a44ab5667b7f3da1cc4bc26efe7fdc48e60d9bcc40802d6fa13f5c8b33ff8ee3",
    "config/th03_main_yumemi_bomb_candidate.toml": "579736dc74c88de408575e0e94f9141c2ebf498f099e783424de3879cc82cad8",
    "config/th03_main_score_candidate.toml": "81aa3026afb3e15c6bff3d1ee79863ee0f95aa113ccf8856171ea8e695b7a347",
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

def candidate_uses_staged_carrier(candidate):
    # Charge adds an owner after the complete accepted-default staging chain.
    # Its original carrier is still serialized by verified local num_jobs=1.
    if candidate is not None and candidate not in CANDIDATE_PINS:
        raise ValueError("unreviewed candidate carrier mode")
    return candidate is not None and candidate != "config/th03_main_yumemi_charge_candidate.toml"

def original_build_carrier(raw, staged):
    if staged:
        if raw.count(AFTER) != 1 or BEFORE in raw:
            raise ValueError("candidate scheduling carrier is not the reviewed -j1 form")
        original = raw.replace(AFTER, BEFORE, 1)
    else:
        original = raw
    if sha(original) != BUILD_SHA:
        raise ValueError("exact original build carrier identity")
    return original

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
        original_build = original_build_carrier(build_bytes, self.candidate)
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
    schedule = Schedule(module.execute, ROOT, args.run_id, candidate_uses_staged_carrier(args.candidate_manifest))
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
