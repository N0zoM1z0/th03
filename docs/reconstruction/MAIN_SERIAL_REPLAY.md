# Serial TH03 MAIN replay

The serial entrypoint runs the existing MAIN Oracle with one CPU, niceness of at least 10, and Tup configured for one job. It keeps the original source, target, byte, MAP, relocation, behavior, determinism and completeness gates unchanged. It does not establish whole-game exactness or Factory acceptance.

## Prerequisites

Use the repository Python environment described in [TOOLCHAIN](../TOOLCHAIN.md). Original private targets and the attested game-local Wine/toolchain/reference inputs must be present. Read the reconstruction handoff and run preflight first.

Only one Borland/Wine writer may run at a time. The serial runner's exclusive claim prevents its own overlapping invocations; it cannot coordinate unrelated commands that bypass this runner. Do not edit source/control inputs or clean retained analysis while a replay is active.

The adapter pins the original Oracle, its local Python helpers, the default manifest/toolchain config and the reviewed candidate manifest. A pin mismatch fails closed. Pin updates require reviewing the changed source and rerunning focused tests; never auto-refresh a failed pin merely to make a replay run.

## Commands

Choose a new unique ID for every attempt, including attempts whose outcome is uncertain. Run through the TH03 Factory repository command with a sufficiently long command timeout. The runner remains in the foreground; there is no detached launch route.

Default, no candidate:
    python3 scripts/replay_th03_main_serial.py --foreground --run-id UNIQUE_DEFAULT_ID

Add the reviewed Marisa candidate, retaining every default gate:
    python3 scripts/replay_th03_main_serial.py --foreground --run-id UNIQUE_CANDIDATE_ID --candidate-manifest config/th03_main_marisa_candidate.toml

The adapter is an internal entrypoint; do not invoke scripts/lib/th03_serial_schedule.py directly. It requires the owning supervisor status, claim and script pins.

The supervisor allows 900 seconds for its replay child, followed by bounded owned-process cleanup and final evidence capture. Original per-command limits, including the Oracle's 180-second execute limit, are not extended. A transport timeout does not prove the backend stopped. Never resubmit after uncertainty: inspect the named status and claim instead.

## State and stopping

The runner immediately records and prints its PID, start identity and status path, then stays in the Factory command.

- Shared claim: .analysis/th03-main-serial/active.claim/
- Per-run status, logs and guards: .analysis/th03-main-serial/runs/ID/
- Original complete proof tree: .analysis/th03-main-exact/ID/

To request a cooperative stop, create .analysis/th03-main-serial/runs/ID/stop.request through Factory. Stop and timeout cleanup use the owned unreaped child leader, WNOWAIT and revalidated pidfds. Shared wineserver, unrelated processes and detached descendants are excluded. No broad kill or wineserver shutdown occurs.

Claims remain after ambiguous launch, supervisor failure or cleanup uncertainty. A one-shot supervisor.started marker prevents re-entry even after a crash. Do not remove claims automatically, reuse an ID, or signal a stale numeric PID.

## Scheduling and evidence

At each of the two exact cold-build boundaries, the adapter:
1. Requires the round's .tup directory to be absent.
2. Runs the bundled Tup init using the original execute helper.
3. Creates only .tup/options, setting updater.num_jobs to 1.
4. Checks the bundled Tup options output for the local effective setting.
5. Invokes the unchanged original build command and returns its unchanged result.

It does not rewrite build.bat. The baseline uses local options; the candidate's already-declared -j1 carrier setting agrees with the same policy. The current output parser is bound to the reviewed bundled Tup executable; unexpected output fails before building.

Each round retains scheduling.json, schedule-init.log and schedule-options.log alongside the original cold outputs. The supervisor's completion-evidence.json binds:
- Original receipt path/hash and result
- A byte-identical copy of tool-attestation.json, verified against the receipt before another replay can replace the shared attestation
- Every retained round MAP hash and both scheduling sidecar hashes
- Before/after source-inventory paths and hashes, and source_inputs_unchanged
- Script identities, start/completion timestamps, exit status and actual CPU/niceness settings

MAP and scheduling-sidecar keys are relative to the original replay tree. Tool and source-inventory paths are repository-relative. These records are execution provenance, not substitute Oracle receipts.

For a baseline/candidate preservation experiment, retain both fresh two-round trees (four outputs), both completion records and the separately reviewed technical launch plan. Run the supplemental preservation verifier only after all original Oracle gates have passed. Do not promote reference-owned remainder bytes to authored exactness.

## Portable tests

These tests use only synthetic files and mocked process primitives; they do not require private game inputs or execute Wine/compiler tools:

    python3 -m unittest discover -s tests -p 'test_th03_main_serial.py'
    python3 -m unittest discover -s tests -p 'test_th03_serial_schedule.py'

The tracked-path port was checked with portable mocks. Its logic derives from the separately retained successful foreground experiment; this does not claim that the newly named entrypoint has itself performed another native replay.
