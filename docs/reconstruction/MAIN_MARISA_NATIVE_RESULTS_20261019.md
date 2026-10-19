# TH03 Marisa: native reconstruction result

Current bounded CODE acceptance checkpoint (2026-10-19): the complete Marisa/Reimu/Mima source owners passed the fresh default two-cold replay and strict comparison against both historical combined rounds. The acceptance metadata records 78 extents / 371 complete functions / 59,624 reviewed CODE bytes overall, including the 6,502-byte /37-function gameplay addition. See [the acceptance note](MAIN_GAMEPLAY_ACCEPTANCE_PROPOSAL.md). Existing DATA/BSS physical ownership, whole-game completion and Factory acceptance remain open; configured behavior tests cover input/math only. The earlier checkpoint narrative below is retained as history, including superseded source-present statements and failed experiments.

Checkpoint: `5b9511a3645d2dd915970f0f58f32fc72d4bb91c` (source-present checkpoint, not Factory acceptance).

Two fresh candidate cold builds pass the original gates: 344 complete functions, 54,157 function bytes, and 55,080 owned bytes. Marisa contributes ten complete functions / 1,958 bytes, emitted naturally as charge/gauge 1,509 plus bomb 449. All Marisa bytes, both MAP contributions, and all 30 original ordered MZ entries match. New DATA/BSS allocation is zero. Both configured behavior runs pass.

Two fresh default builds also pass: prior 334 functions / 53,122 owned bytes. Across all four outputs, every load-payload byte outside the Marisa prefix, the original ordered relocation subsequence, and DATA/BSS metadata/file-backed contents are preserved. BSS has allocation metadata, not invented file bytes.

The unowned HITBOX remainder still differs from the immutable target (one XOR encoding and relocation order); this existing mismatch is retained as a failed target comparison. Baseline preservation grants it zero authored credit. No whole-product byte-exactness or completion percentage is asserted.

All produced game binaries and normalized game objects agree between rounds within each replay. Across baseline versus candidate, only bin/th03/main.exe changes; the other 19 products agree. Candidate MAIN SHA256 is be31d4ecb803f17a56c69059701bed85fd1a1cac36f81d456521b417719a809d. Nine non-game `obj/Research/{086,286,386}/{if_shift,wide,xfade}.obj` files show metadata drift; consequently the all-object equality field remains false. This diagnostic is disclosed rather than hidden or normalized further.

The candidate remains source-present. The accepted manifest and ledgers remain 74 extents / 334 functions / 53,122 owned bytes. Factory durable submission is not configured for TH03, so there are no newly Factory-accepted facts. The separate portable suite passed all 656 tests (Factory command `6097ae976d7a48268b048138f5b671db`). Original 19 dirty tracked files and their original untracked test remain preserved.

## Actual commands and reproducibility

```sh
.venv/bin/python -B .analysis/gpt-dots-marisa-source-v01/durable-runner/runner_schedule.py --foreground --run-id gpt-dots-marisa-default-cold-v01
```

```sh
.venv/bin/python -B .analysis/gpt-dots-marisa-source-v01/durable-runner/runner_schedule.py --foreground --run-id gpt-dots-marisa-split-cold-v01 --candidate-manifest config/th03_main_marisa_candidate.toml
```

These IDs are consumed; use fresh IDs for a future run. The launch wrapper additionally pinned HEAD, scripts, and scheduling plan SHA256 `f0d6f90d5f05bcd967763e9b6c226d89a1df2a71f15c1fe8901de3be3d359a54` before exec. Both use `durable-runner/schedule_once.py` and the original `scripts/replay_th03_main_exact_units.py` gates. The candidate manifest changes only its fresh copied build.bat to `bin\tup -j1`; the wrapper also establishes and checks local `.tup/options` num_jobs 1 for both default and candidate, avoiding global configuration changes. One CPU / nice10 and sequential rounds are retained.

Direct candidate engine syntax is `python3 scripts/replay_th03_main_exact_units.py --candidate-manifest config/th03_main_marisa_candidate.toml --run-id NEW_ID`; for this resource-constrained environment use the reviewed foreground wrapper above, especially for the default run's local scheduling guard. Do not launch archived detached runner variants. Launch/status/completion sidecars are retained under `durable-runner/runs/RUN_ID/`. Transport responses were lost; backend completion was verified separately. No original Factory launch command ID is invented.

The bounded read-only preservation verifier is `verify_four_output_preservation.py`, with explicit default/candidate receipt and completion paths, pinned launch plan, UTC freshness lower bound, and report path. Its actual Factory command ID is 085bf3c32fba4f309851eae3733febe6; the complete CLI is retained in [MAIN_MARISA_NATIVE_RESULTS_20261019.json](MAIN_MARISA_NATIVE_RESULTS_20261019.json). Tracked reproduction entrypoints are `scripts/replay_th03_main_serial.py` and `scripts/verify_th03_main_preservation.py`, with pure helper `scripts/lib/th03_preservation_layout.py`. They are portable-tested, but are not the entrypoints used for the historical native runs above. The recorded historical commands remain unchanged.

## Receipt pins

- candidate: `.analysis/th03-main-exact/gpt-dots-marisa-split-cold-v01/receipt.json`
  SHA256 `a33083180015439eb05e381614ce69af557dcce17da11b94dfe2997982772d19`
- baseline: `.analysis/th03-main-exact/gpt-dots-marisa-default-cold-v01/receipt.json`
  SHA256 `bedd69d1933b51e37c44005d958a127feb8a70bee3ad382dc7b6d168bb3552b7`
- preservation: `.analysis/gpt-dots-marisa-source-v01/four-output-preservation-v01.json`
  SHA256 `93332f6c42d6b102cdb131c2867f980b5cdb5eb83b335e1d695812e0c36479fe`

## Final export validation

The tracked reproduction scripts and tests passed all 709 portable tests on
2026-10-19 (Factory command 7803ce5c41a9495e807075a03f2417c8). Both CLI help
checks, tracking validation, progress validation and whitespace checks passed.
This does not relabel the historical native runs as executions of the exported
entrypoints.

Target provenance remains candidate-local-attested: these results are relative
to the pinned repository target extracted from the user-provided Japanese disk
image. Independent pristine-dump provenance remains unconfirmed.
