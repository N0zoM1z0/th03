# MAIN Yumemi charge native CPU runtime checkpoint

On 2026-10-21 the canonical Japanese MAIN target and retained MCY01 candidate
actually passed 2546 independent native-byte semantic cases each. All 583 decoded
instruction positions in ten complete functions were visited: 1613 instruction
bytes plus 32 switch-table bytes in the 1645-byte charge owner. Ten guarded
in-memory semantic mutations per image were rejected after pristine controls
passed. The strict comparison passed, including the complete ordered case and
observation digest vectors, coverage, source closure and package versions.
Only executable SHA and elapsed time differ between runtime receipts; only
executable SHA differs between control receipts. The shared observation digest is
773c807a54a6fc268fdfd3adb50b777c0f6961ff0dc5874606c98757d130f8a8.

This is scoped CPU behavior evidence, not an exactness promotion, complete-game
runtime proof, cold build, or hardware/audio/graphics validation. No ledger
or default build graph is changed by this checkpoint.

## Exact provenance

The actual executed helpers were under
`.analysis/main-yumemi-charge-runtime-model-20261021-v01/`:
`review_charge_runtime.py`, `test_charge_runtime.py`, and
`compare_charge_runtime.py`. The reports are respectively
`target-runtime-v01.json`, `candidate-runtime-v01.json`,
`target-controls-v01.json`, `candidate-controls-v01.json`, and
`comparison-v01.json` in that same directory. Their exact SHA256 bindings,
consumed images and helper closure are preserved in
[historical proof bindings](main-yumemi-charge-runtime-proof.json).

The newly maintained `scripts/review_th03_main_yumemi_charge_runtime.py` combines
the original runtime and controls, resolves the installed script root, and
requires an explicit input SHA rather than restricting candidates to MCY01.
It has NOT inherited execution credit from the ignored-path source. Its
`scripts/compare_th03_main_yumemi_charge_runtime.py` companion requires actual
fresh-image receipts from the installed source closure. Cold integration must
run the installed model and controls anew on the target and each cold image,
then run strict comparison. Historical receipts remain immutable.

## Contract and limits

The scalar oracle covers target acquisition, reset/add/update, collision,
ring rendering, rendering dispatch, gauge state machine and both wrappers.
Inputs include both players, distinct current-player storage fields, signed
coordinate and frame wrap, inclusive collision boundaries, formation selection
and fallback, all rendering phases, all switch cases/default, gauge state/type
and level-wrap branches, IF/DF and near/far stack cleanup.

Actual relocated image instructions execute. POLAR and foreground coordinate
conversion dependencies also execute actual instructions with decoded-boundary
and return-frame checks. Sound, sprite output, hitcircle, palette restoration,
bomb-axis and bullet allocation are explicitly no-side-effect far-call fixtures;
their calls and arguments are checked, not their device/game implementations.
Signed trigonometric table fixtures respect the real overlapping storage, but
are not a historical table-regeneration claim.

Each case checks chronological stores/calls, all physical memory except a
bounded 128-byte local stack scratch window, unchanged caller stack, preserved
registers and IF/DF, and hit return value. Full final register/flag state,
observed events/raw arguments, data and stack hashes feed per-case observation
digests. Source closure, input bytes and package versions are checked before and
after. All 583 instruction positions must execute; complete branch-outcome
coverage is not claimed. In particular, some transformed target range outcomes
are unreachable after input filtering. Enemy/switch/ring loops have finite
bounds 40/8/16, so instruction-budget exhaustion is a failure, not an accepted
nontermination result. The actual maximum was 3661 instructions per case.

## Replaying installed helpers

Run the model with `--exe PATH --expected-sha256 SHA --json REPORT --seconds 170`.
Add `--negative-controls` for the ten mutation controls. Reports must be fresh.
For cold integration this fits the existing 180-second per-command wrapper;
retained target runtime took about 25 seconds, not a guaranteed future budget.

Run the comparator with `--target-runtime REPORT --candidate-runtime REPORT
--target-controls REPORT --candidate-controls REPORT --candidate-exe EXE
--json REPORT`. The target defaults to `.analysis/targets/th03/main.exe` and may
be specified with `--target-exe`. Every input is retained and rechecked; no
memory, trace or register fields are normalized. The source-only unittest
checks the owner partition, full fixture population and guarded mutation set
without invoking the emulator or reading target images.
