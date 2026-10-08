# TH03 reconstruction handoff — current state (2026-10-08)

Reconstruction resumed after the historical 2026-10-06 closeout. This is a
**scoped, repository-local reconstruction**, not a finished, playable game or
native Factory Truth Kernel acceptance. Original Japanese target provenance is
`candidate-local-attested`; an independently pristine original dump has not
been proved. Source, target and compiler findings must be verified against
TH03 itself, not assumed correct from ReC98, TH04 or old project notes.

## Accepted baseline

| Artifact | Reviewed/source scope | Accepted original CODE |
| --- | --- | --- |
| MAIN | 74 complete reviewed CODE extents; 334 complete functions | **74 exact extents; 334 exact functions; 53,122 bytes** |
| OP | 40 reviewed decoded units; 33 source-present extents / 12,019 bytes | exact0 |
| MAINL | 145 decoded rows; 34 source-present extents / 3,073 bytes | exact0 |
| ZUN | 18 rows; 3 source-present wrapper units / 234 bytes | exact0 |

MAIN's reviewed exact extent comprises **52,199 function bytes** and **923
explicitly classified non-function producer bytes**, across **67 maintained
semantic source owners**. All 334 reviewed functions are exact; the denominator
is **only the currently reviewed CODE**, not the complete MAIN program. The
whole-game owned-code denominator and 505-file intake are unfinished.

Authoritative final default no-candidate replay at this checkpoint:

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-cleanup-maintenance-default-final-20261008

Receipt:
`.analysis/th03-main-exact/gpt-web-cleanup-maintenance-default-final-20261008/receipt.json`.
Two **serial independent cold builds PASS** the immutable original target's
owned CODE bytes, original MAP placements, **ordered MZ relocations**, all
previously accepted owners, maintained DOS behavior probes, **20 product
outputs, 391 game OMF objects and 457 total generated OMF objects**. This
acceptance is bounded to the repository Oracle; it is not native Factory
Truth Kernel replay or whole-game product closure.

Latest tracking snapshot: **277 units, 2,613 evidence rows, 355 knowledge
rows, three hypotheses, 334 authored-function rows** (all values scoped to
their individual artifact/ledger, not additive file counts). Use
`docs/PROGRESS.md`, `config/units.csv`, `config/evidence.csv`,
`config/th03_main_authored_functions.csv`, and
`config/th03_function_boundaries.csv` for the machine-readable current view.

## Accepted large gameplay and shared owners

Do not substitute leaf-only progress for complete source subsystems.
These original modules have all passed their own strict full-link boundaries:

- **MAIN_03_TEXT boss attacks:** complete 18,400-byte segment, shared
  functions and all nine character bosses, including large behavior updates
  and switch-table producer bytes. See
  [boss review](reconstruction/MAIN_BOSS_REVIEW.md).
- **MAIN_05_TEXT character bombs:** 3,113 bytes / seven complete functions
  from multiple natural TC4 producers; all 71 ordered relocation entries
  accepted. See [bombs](reconstruction/MAIN_BOMBS_REVIEW.md).
- **MAIN_07–11 charge-shot/gauge:** all five character owners, 5,802 bytes /
  48 functions. See [charge/gauge](reconstruction/MAIN_CHARGE_GAUGE_REVIEW.md).
- **P_EXATT_TEXT / MAIN_06_TEXT Extra Attacks:** ten complete character/shared
  owners and the adjacent generic 41-byte routine, **8,822 consecutive exact
  CODE bytes**, including 1,150-byte Yumemi, 518-byte Chiyuri and 470-byte
  Ellen functions. See [Extra Attacks](reconstruction/MAIN_EXATT_REVIEW.md).
- **MAIN_010_TEXT Hyper dispatch:** ten complete near Pascal functions /
  **595 bytes**; native TC4 OMF works without any Hyper-specific calibration.
  See [Hyper](reconstruction/MAIN_HYPER_DISPATCH_REVIEW.md).
- **PLAYER_M_TEXT HUD intro/render:** full four-function **1,478-byte**
  source reconstruction, comprising **688-byte update**, **635-byte renderer**
  and two complete symbolic graphics helpers (104 and 51 bytes).
  See [HUD](reconstruction/MAIN_HUD_ROUND_INTRO_REVIEW.md).
- The complete enemy code owner, input/math, movement, shot updates, collision,
  static HUD and other accepted modules retain their original bytes, MAP and
  relocations in the same replay. See the
  [review index](REC98_TH03_REVIEW.md) and [subsystem notes](reconstruction/README.md).

**OMF provenance limitations:** Ellen's natural source needs a narrowly
validated TC4 LEDATA/FIXUPP record-framing calibration. The HUD owner is
regenerated from **two fresh natural TC4 -S sources plus maintained symbolic
TASM**, followed by a fail-closed reversal of 87/57 independently framed
FIXUPP subrecords. Their original CODE, relocation targets and strict
comparators are not patched. The unmodified compiler and calibrated OMF hashes
are retained separately; **historically exact unmodified OMF identity is not
claimed** for those two owners. All historical player/HUD/boss DATA/BSS
allocation remains at original addresses; its physical original compiler
ownership has not been closed.

## Current non-exact gameplay frontier

The [target-first next-frontier review](reconstruction/MAIN_NEXT_FRONTIER_REVIEW.md)
contains **two unaccepted intervals, totaling 2,131 original CODE bytes**:

- **Marisa charge-shot, Hyper, gauge, hitbox and bomb prefix:** 1,958 bytes,
  30 original MZ relocation entries. Ten actual complete logical function
  bodies have been independently reviewed, including **414-, 470- and
  449-byte** functions. The 201-byte update has an **internal early RETF**:
  do not miscount it as two functions. Semantic ABI, shared data and the
  physical producer remain unaccepted. See
  [Marisa gameplay review](reconstruction/MAIN_MARISA_GAMEPLAY_REVIEW.md),
  replayable with `python3 scripts/review_th03_main_marisa_gameplay.py --run-id UNIQUE_ID`.
- **Ordinary shot hardware producer prefix:** 173 bytes, 12 relocation
  entries. Review with its full shooting/graphics dependency chain, not
  just its short entry functions.

Both intervals are *target-boundary research*, **not additional exact
functions or bytes**. Next steps are natural maintained source for whole
owners, complete original near/far ABI and shared tails, DATA/BSS/linker
ownership and two fresh full cold links including all prior exact owners.
OP/MAINL/ZUN additionally need original stored-versus-decoded CODE mapping
and independent exact reconstruction. Full MAIN, resource/heap/IRQ/device
behavior, complete product graph and original provenance are still open.

## Build, CI and private artifact retention

All edits, reads, Python, Ghidra queries, Oracle and builds go through the
TH03 Factory MCP. Work headlessly; **serialize Borland/Wine builds** and
read TH04 references only from `/references/th04`. Preserve existing dirty
changes and their meaningful failure evidence; do not reset away blockers.

    python3 scripts/preflight.py
    python3 scripts/replay_th03_main_exact_units.py --run-id UNIQUE_ID
    python3 scripts/ci.py
    git diff --check

Post-cleanup full CI attempt: **648 tests, 125 errors importing unavailable
host `unicorn`, 167 skipped; full CI FAIL**. This is the documented host
missing-dependency block, not a game-source exact mismatch and not a CI pass.
Log: `.analysis/cleanup-20261008-followup/ci.log`. All independently
runnable post-unittest gates separately **PASS**, including compileall,
target/toolchain/Ghidra attestations, ledger/progress, Oracle and negative
controls; log `.analysis/cleanup-20261008-followup/postgates.log`. The
prior full HUD acceptance is separately documented in the HUD review.

Private replay receipts/referenced proof inputs, original targets,
Ghidra projects, runtime images and Wine/toolchain state are protected.
**2026-10-08 owner-authorized cleanup** reclaimed approximately
**4,492.0 MiB (4.39 GiB)**: two audited guarded passes (275 + 5 paths,
4,487.2 MiB) of unreferenced receipt trees/experimental output, plus
three post-verification Python caches (4.8 MiB). Documented,
ledger-guarded and active proof inputs were preserved. Full receipt runs still referenced by
current evidence retain their entire proof trees. Audits:
`.analysis/cleanup-20261008/receipt.json` and
`.analysis/cleanup-20261008-followup/receipt.json`. See
[retention workflow](RE_WORKFLOW.md) and
[cleanup review](reconstruction/ANALYSIS_CLEANUP.md).

Detailed chronological technical checkpoints (including the 2026-10-06
stopped-state figures) remain in the versioned subsystem reviews and
[historical closeout](CLOSEOUT.md); do **not** mistake those checkpoint
numbers or old CI outcomes for the current accepted baseline above.
