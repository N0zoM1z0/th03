#!/usr/bin/env python3
"""Foreground-only, single-shot scheduled replay supervisor. No acceptance claims."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STATE_ROOT = ROOT / ".analysis/th03-main-serial"
CLAIM = STATE_ROOT / "active.claim"
REPLAY = "scripts/replay_th03_main_exact_units.py"
SCHEDULE = ROOT / "scripts/lib/th03_serial_schedule.py"
SCHEDULE_SHA = 'c92312a99220180c674ce0c2fda70836a9c0271ce90fb5abd19f5cbce8610dce'
ORIGINAL_REPLAY_SHA = 'f4df09017064fc3d54c3cd8ff4643e8ceacd77a413e32c13a51844ed9e6a66cf'

def utc():
    return datetime.now(timezone.utc).isoformat()

def atomic(path, value):
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w") as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def pins():
    names = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, timeout=30).split(b"\0")
    result = {}
    for raw in sorted(set(names)):
        if not raw:
            continue
        name = os.fsdecode(raw)
        p = ROOT / name
        if p.is_symlink():
            result[name] = {"symlink": os.readlink(p)}
        elif p.is_file():
            result[name] = digest(p)
        elif not p.exists():
            result[name] = None
        else:
            raise ValueError("unsupported source input: " + name)
    result["@supervisor"] = digest(Path(__file__))
    result["@schedule_adapter"] = digest(SCHEDULE)
    result["@head"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, timeout=30, text=True).strip()
    return result

def process_identity(pid):
    stat = Path(f"/proc/{pid}/stat").read_text()
    tail = stat[stat.rindex(")") + 2:].split()
    name = stat[stat.index("(") + 1:stat.rindex(")")]
    return (pid, int(tail[2]), tail[19], name, tail[0])

def process_ids():
    return [int(p.name) for p in Path("/proc").iterdir() if p.name.isdigit()]

class OwnedGroup:
    """The unreaped child leader reserves its PID/process-group identity."""
    def __init__(self, proc):
        self.proc = proc
        self.leader = process_identity(proc.pid)
        self.reaped = False
        if self.leader[1] != proc.pid:
            raise RuntimeError("child did not acquire its own process group")

    def guard(self):
        if self.reaped or self.proc.returncode is not None:
            raise RuntimeError("refusing operation after leader reap")
        # WNOWAIT both proves child ownership and leaves the leader unreaped.
        os.waitid(os.P_PID, self.proc.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
        now = process_identity(self.proc.pid)
        if now[:3] != self.leader[:3]:
            raise RuntimeError("leader identity drift")

    def members(self):
        self.guard()
        found = []
        for pid in process_ids():
            try:
                item = process_identity(pid)
                if item[1] == self.proc.pid and "wineserver" not in item[3].lower() and item[4] != "Z":
                    found.append(item)
            except (OSError, ValueError, IndexError):
                continue
        return found

    def cleanup(self):
        for sig in (signal.SIGTERM, signal.SIGKILL):
            for expected in self.members():
                fd = None
                try:
                    fd = os.pidfd_open(expected[0], 0)
                    self.guard()
                    current = process_identity(expected[0])
                    if current[:4] != expected[:4] or "wineserver" in current[3].lower():
                        raise RuntimeError("owned member identity drift")
                    # The descriptor binds this signal to the opened process,
                    # even if that numeric PID changes after the /proc check.
                    signal.pidfd_send_signal(fd, sig, None, 0)
                except ProcessLookupError:
                    pass
                finally:
                    if fd is not None:
                        os.close(fd)
            time.sleep(1)
        return self.members()

def finish(proc, stop, timeout=900):
    owner = OwnedGroup(proc)
    result = {"reason": "exited", "cleanup_uncertain": False}
    deadline = time.monotonic() + timeout
    try:
        while True:
            owner.guard()
            if os.waitid(os.P_PID, proc.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT) is not None:
                break
            if stop.exists():
                result["reason"] = "stop_requested"
                break
            if time.monotonic() >= deadline:
                result["reason"] = "wall_timeout"
                break
            time.sleep(0.25)
        result["cleanup_survivors"] = owner.cleanup()
        result["cleanup_uncertain"] = bool(result["cleanup_survivors"])
    except BaseException as exc:
        result["cleanup_uncertain"] = True
        result["cleanup_error"] = f"{type(exc).__name__}: {exc}"
    finally:
        owner.reaped = True
        try:
            result["replay_exit_code"] = proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            result["replay_exit_code"] = None
            result["cleanup_uncertain"] = True
    # Detached descendants/shared wineserver are never claimed or signalled.
    result["cleanup_scope"] = "owned group only; detached descendants and shared wineserver excluded"
    return result

def limits():
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    os.nice(max(0, 10 - os.getpriority(os.PRIO_PROCESS, 0)))

def capture_completion(run, state):
    """Bind immutable per-run tool identity and MAP bytes before claim release."""
    output = ROOT / ".analysis/th03-main-exact" / state["run_id"]
    receipt_path = output / "receipt.json"
    evidence = dict(run_id=state["run_id"], captured_utc=utc(), exact_acceptance=False,
                    scheduled_at_utc=state.get("claimed_utc"),
                    supervisor_started_at_utc=state.get("started_utc"),
                    replay_started_at_utc=state.get("replay_started_utc"),
                    replay_exit_code=state.get("replay_exit_code"),
                    execution_limits=state.get("execution_limits"),
                    supervisor_script_sha256=digest(Path(__file__)),
                    schedule_adapter_sha256=digest(SCHEDULE),
                    original_replay_sha256=digest(ROOT / REPLAY),
                    receipt_present=receipt_path.is_file(), maps={})
    if not receipt_path.exists():
        if state.get("replay_exit_code") == 0:
            raise ValueError("successful replay has no original receipt")
        atomic(run / "completion-evidence.json", evidence)
        return evidence
    if receipt_path.is_symlink():
        raise ValueError("receipt is a symlink")
    raw = receipt_path.read_bytes()
    receipt = json.loads(raw)
    if receipt.get("run_id") != state["run_id"]:
        raise ValueError("receipt run identity differs")
    evidence.update(receipt_path=str(receipt_path.relative_to(ROOT)),
                    receipt_sha256=hashlib.sha256(raw).hexdigest(),
                    receipt_pass=receipt.get("pass"))
    attestation = ROOT / ".analysis/toolchain/attestation.json"
    if attestation.is_symlink():
        raise ValueError("tool attestation is a symlink")
    data = attestation.read_bytes()
    expected = receipt["toolchain_receipt_sha256"]
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError("live tool attestation differs from original receipt")
    frozen = run / "tool-attestation.json"
    with frozen.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if digest(frozen) != expected:
        raise ValueError("archived tool attestation copy differs")
    evidence["tool_attestation"] = dict(path=str(frozen.relative_to(ROOT)), sha256=expected)
    if [r.get("round") for r in receipt["rounds"]] != [1, 2]:
        raise ValueError("receipt does not contain both original rounds")
    for number in (1, 2):
        source = output / ("round" + str(number)) / "source"
        maps = sorted(p for p in source.rglob("*") if p.suffix.lower() == ".map")
        if source / "obj/th03/main.map" not in maps:
            raise ValueError("round MAIN MAP missing")
        for path in maps:
            if path.is_symlink() or not path.is_file():
                raise ValueError("invalid MAP path")
            evidence["maps"][path.relative_to(output).as_posix()] = digest(path)
    evidence["schedule_sidecars"] = {}
    for number in (1, 2):
        p = output / ("round" + str(number)) / "scheduling.json"
        evidence["schedule_sidecars"][p.relative_to(output).as_posix()] = digest(p)
    atomic(run / "completion-evidence.json", evidence)
    return evidence

def supervise(run):
    # Never re-enter a run, even after crash or normal exit. mkdir is atomic.
    # Failure here must not touch status or the exclusive global claim.
    (run / "supervisor.started").mkdir()
    fd = os.open(run, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    status_path = run / "status.json"
    state = json.loads(status_path.read_text())
    proc = None
    try:
        if json.loads((CLAIM / "owner.json").read_text())["run_id"] != state["run_id"]:
            raise RuntimeError("claim owner mismatch")
        limits()
        state.update(state="starting", supervisor_pid=os.getpid(), started_utc=utc(),
                     execution_limits={"cpus": sorted(os.sched_getaffinity(0)),
                                       "nice": os.getpriority(os.PRIO_PROCESS, 0),
                                       "wall_seconds": 900})
        atomic(status_path, state)
        before = json.loads((run / "inputs.before.json").read_text())
        if pins() != before:
            raise RuntimeError("source changed since launch pin")
        if (run / "stop.request").exists():
            state.update(state="stopped_before_launch", replay_invocations=0)
        else:
            env = os.environ.copy()
            env.update(DISPLAY="", WAYLAND_DISPLAY="", PYTHONDONTWRITEBYTECODE="1",
                       OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1")
            with (run / "replay.stdout.log").open("wb", buffering=0) as out, \
                 (run / "replay.stderr.log").open("wb", buffering=0) as err:
                proc = subprocess.Popen(state["argv"], cwd=ROOT, env=env,
                                        stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                                        start_new_session=True)
                state.update(state="running", replay_invocations=1, replay_pid=proc.pid,
                             replay_started_utc=utc())
                atomic(status_path, state)
                state.update(finish(proc, run / "stop.request"))
                proc = None
            state["state"] = "finished"
            evidence = capture_completion(run, state)
            state["completion_evidence_path"] = str(run / "completion-evidence.json")
            state["completion_evidence_sha256"] = digest(run / "completion-evidence.json")
    except BaseException as exc:
        state.update(state="supervisor_error", error=f"{type(exc).__name__}: {exc}")
        if proc is not None:
            state.update(finish(proc, run / "stop.request", timeout=0))
            proc = None
    finally:
        try:
            before = json.loads((run / "inputs.before.json").read_text())
            after = pins()
            atomic(run / "inputs.after.json", after)
            state["source_inputs_unchanged"] = before == after
            state["changed_inputs"] = sorted(k for k in before.keys() | after.keys()
                                            if before.get(k) != after.get(k))
        except BaseException as exc:
            state["source_inputs_unchanged"] = False
            state["pin_error"] = f"{type(exc).__name__}: {exc}"
        evidence_path = run / "completion-evidence.json"
        if evidence_path.exists():
            try:
                evidence = json.loads(evidence_path.read_text())
                evidence.update(source_inputs_unchanged=state.get("source_inputs_unchanged", False),
                                inputs_before_path=str((run / "inputs.before.json").relative_to(ROOT)),
                                inputs_after_path=str((run / "inputs.after.json").relative_to(ROOT)),
                                inputs_before_sha256=digest(run / "inputs.before.json"),
                                inputs_after_sha256=digest(run / "inputs.after.json"))
                evidence["source_input_manifests"] = {
                    evidence["inputs_before_path"]: evidence["inputs_before_sha256"],
                    evidence["inputs_after_path"]: evidence["inputs_after_sha256"],
                }
                atomic(evidence_path, evidence)
                state["completion_evidence_sha256"] = digest(evidence_path)
            except BaseException as exc:
                state.update(state="supervisor_error", evidence_error=f"{type(exc).__name__}: {exc}")
        state.update(finished_utc=utc(), exact_acceptance=False,
                     receipt_path=str(ROOT / ".analysis/th03-main-exact" / state["run_id"] / "receipt.json"))
        # Failure/uncertainty leaves the persistent claim for explicit human review.
        safe = (state.get("state") in ("finished", "stopped_before_launch")
                and not state.get("cleanup_uncertain")
                and not (CLAIM / "launch-error.json").exists())
        state["claim_retained"] = True
        atomic(status_path, state)
        if safe:
            try:
                if json.loads((CLAIM / "owner.json").read_text())["run_id"] != state["run_id"]:
                    raise RuntimeError("claim owner changed before release")
                (CLAIM / "owner.json").unlink()
                CLAIM.rmdir()
                state["claim_retained"] = False
            except BaseException as exc:
                state["claim_release_error"] = f"{type(exc).__name__}: {exc}"
            atomic(status_path, state)

def launch(run_id, candidate=None):
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", run_id):
        raise ValueError("invalid run id")
    if (ROOT / ".analysis/th03-main-exact" / run_id).exists():
        raise ValueError("original replay run ID already exists; never resume")
    if digest(SCHEDULE) != SCHEDULE_SHA or digest(ROOT / REPLAY) != ORIGINAL_REPLAY_SHA:
        raise ValueError("scheduled entrypoint pin drift")
    argv = [sys.executable, str(SCHEDULE), "--run-id", run_id,
            "--supervisor-state", str(STATE_ROOT / "runs" / run_id / "status.json")]
    if candidate:
        p = (ROOT / candidate).resolve(strict=True)
        if not p.is_relative_to(ROOT / "config"):
            raise ValueError("candidate must be in config/")
        argv += ["--candidate-manifest", str(p.relative_to(ROOT))]
    if (STATE_ROOT / "runs" / run_id).exists():
        raise ValueError("supervisor run ID already exists; never resume")
    STATE_ROOT.mkdir(parents=True, exist_ok=True)
    CLAIM.mkdir()  # Fail closed even if an earlier owner appears dead.
    run = STATE_ROOT / "runs" / run_id
    state = dict(run_id=run_id, state="claimed", claimed_utc=utc(), argv=argv,
                 replay_invocations=0, exact_acceptance=False, wall_seconds=900,
                 scheduling_policy="local-tup-num-jobs-1",
                 schedule_adapter_sha256=SCHEDULE_SHA,
                 supervisor_script_sha256=digest(Path(__file__)),
                 original_replay_sha256=ORIGINAL_REPLAY_SHA,
                 original_replay_path=REPLAY)
    run_created = False
    spawn_attempted = False
    supervisor_pid = None
    try:
        atomic(CLAIM / "owner.json", {"run_id": run_id, "claimed_utc": utc()})
        run.mkdir(parents=True, exist_ok=False)
        run_created = True
        atomic(run / "status.json", state)
        atomic(run / "inputs.before.json", pins())
        supervisor_pid = os.getpid()
        result = dict(supervisor_pid=supervisor_pid,
                      supervisor_start_ticks=process_identity(supervisor_pid)[2],
                      launch_utc=utc(), mode="foreground",
                      status_path=str(run / "status.json"),
                      stop_path=str(run / "stop.request"))
        atomic(run / "launch.json", result)
        print(json.dumps(result), flush=True)
        # This marker means supervision was entered, not that a detached child
        # exists. Never overwrite supervisor status on errors after this point.
        spawn_attempted = True
        supervise(run)
        return result
    except BaseException as exc:
        failure = dict(run_id=run_id, state="launch_error", observed_utc=utc(),
                       error=f"{type(exc).__name__}: {exc}",
                       spawn_attempted=spawn_attempted, supervisor_pid=supervisor_pid,
                       launch_ambiguous=spawn_attempted, mode="foreground", claim_retained=True,
                       exact_acceptance=False)
        # A spawn may have succeeded despite a later exception. Never race the
        # supervisor's status writes: use a separate launch-error artifact.
        for path in [CLAIM / "launch-error.json"] + (
                [run / "launch-error.json"] if run_created else []):
            try:
                atomic(path, failure)
            except BaseException:
                pass
        if run_created and not spawn_attempted:
            try:
                atomic(run / "status.json", failure)
            except BaseException:
                pass
        # Retain the claim. An ambiguous spawn is inspected, never retried.
        raise

def main():
    ap = argparse.ArgumentParser(description="Foreground-only owned scheduled replay supervisor")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--candidate-manifest")
    ap.add_argument("--foreground", action="store_true", required=True,
                    help="remain in this Factory command; never launch a detached supervisor")
    args = ap.parse_args()
    result = launch(args.run_id, args.candidate_manifest)
    state = json.loads(Path(result["status_path"]).read_text())
    return 0 if (state.get("state") == "finished"
                 and state.get("replay_exit_code") == 0
                 and state.get("source_inputs_unchanged") is True
                 and not state.get("cleanup_uncertain")) else 1

if __name__ == "__main__":
    raise SystemExit(main())
