# TH03 reconstruction handoff — current state (2026-10-19)

The owner's requested worktree review is complete. CI/dependency maintenance
and proof-retention fixes are recorded in `ed653cb` and `095e54b`; this
documentation checkpoint reconciles the remaining maintenance changes.
The CPU source-present milestone extends the prior Yumemi commit `30f1564`;
accepted gameplay CODE remains the scope recorded in `38a6248`. The 2026-10-06 closeout and 2026-10-08 maintenance pass
are historical checkpoints. This is a
**scoped, repository-local reconstruction**, not a finished, playable game or
native Factory Truth Kernel acceptance. Original Japanese target provenance is
`candidate-local-attested`; an independently pristine original dump has not
been proved. Source, target and compiler findings must be verified against
TH03 itself, not assumed correct from ReC98, TH04 or old project notes.

## Accepted baseline

| Artifact | Reviewed/source scope | Accepted original CODE |
| --- | --- | --- |
| MAIN | 81 source-present reviewed CODE extents; 386 complete functions | **78 exact extents; 371 exact functions; 59,624 bytes** |
| OP | 40 reviewed decoded units; 33 source-present extents / 12,019 bytes | exact0 |
| MAINL | 145 decoded rows; 34 source-present extents / 3,073 bytes | exact0 |
| ZUN | 18 rows; 3 source-present wrapper units / 234 bytes | exact0 |

MAIN's reviewed exact extent comprises **58,701 function bytes** and **923
explicitly classified non-function producer bytes**, across **70 maintained
semantic source owners**. The reviewed source-present scope totals **63,044
CODE bytes**; Yumemi and CPU add **15 functions / 3,420 bytes** that are not exact.
These denominators cover **only the currently reviewed CODE**, not the complete
MAIN program. The whole-game owned-code denominator and 505-file intake are unfinished.

The latest accepted default no-candidate replay is
`.analysis/th03-main-exact/gpt-dots-gameplay-promoted-default-cold-v01/receipt.json`
(observed 2026-10-19). Both serial cold rounds passed. The
[gameplay acceptance record](reconstruction/MAIN_GAMEPLAY_ACCEPTANCE_PROPOSAL.md)
retains the frozen proof and strict supplemental comparison: complete MAIN,
ordered relocations, MAP/storage layout, all 20 declared products and 31 total
executable outputs. Nine Research-only object metadata drifts remain outside
the accepted game vector. Later metadata and Yumemi source installation do not
rebind that historical proof or grant additional acceptance.

Historical 2026-10-08 default no-candidate replay (74 extents / 334 functions /
53,122 CODE bytes):

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-cleanup-maintenance-default-final-20261008

Receipt:
`.analysis/th03-main-exact/gpt-web-cleanup-maintenance-default-final-20261008/receipt.json`.
At that checkpoint, two **serial independent cold builds passed** the immutable
original target's owned CODE bytes, original MAP placements, **ordered MZ
relocations**, all previously accepted owners, maintained DOS behavior probes,
**20 product outputs, 391 game OMF objects and 457 total generated OMF objects**.
Both checkpoints are bounded to the repository Oracle; neither is native
Factory Truth Kernel replay or whole-game product closure.

Latest tracking snapshot: **284 units, 2,728 evidence rows, 361 knowledge
rows, three hypotheses, 386 authored-function rows** (all values scoped to
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
- **Marisa, Reimu/shared and Mima gameplay:** **6,502 bytes / 37 functions**
  accepted across four extents. See the
  [gameplay acceptance record](reconstruction/MAIN_GAMEPLAY_ACCEPTANCE_PROPOSAL.md).
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

The [Yumemi gameplay review](reconstruction/MAIN_YUMEMI_GAMEPLAY_REVIEW.md)
records two source-present extents / **11 functions / 2,343 CODE bytes**.
Retained linking matched their bytes, extent-local relocation lists and MAP,
but **combined-owner relocation order and outside-owner relocation order fail**.
Localized maintained sources have not received a fresh cold acceptance replay.
Preserve those failures and all existing comparators; no exact promotion is made.

The older [target-first frontier review](reconstruction/MAIN_NEXT_FRONTIER_REVIEW.md)
remains a historical 2,131-byte intake. Its 1,958-byte Marisa owner is now
accepted; the 173-byte ordinary-shot hardware prefix remains unaccepted and
needs review with its complete shooting/graphics dependency chain.

The [CPU-state milestone](reconstruction/MAIN_PLAYER_CPU_REVIEW.md) adds four
complete source-present functions / **1,077 bytes**, including two switch tables
and a natural zero. A separate corrected retained CPU/Yumemi link matches all
81 authored extents and the new 34-site CPU/bomb/charge order. Full outside payload,
storage and generated-baseline header fields pass, but outside literal relocation
order and score_add containing-carrier MAP metadata remain failed gates. The
actual score_add address and 88 bytes still match target. Historical Yumemi v01
evidence and accepted metadata remain unchanged. The 664-byte copied prefix is
uncredited reference support. Maintained-path cold and runtime acceptance remain
open. Existing stage/round and round-loop blockers also remain outside acceptance.

Post-install full CI passed **783 tests**. The unchanged-default regression
`gpt-dots-cpu-guards-default-cold-v01` stopped in its first round at the existing
180-second build timeout while reference Research/286 objects were still compiling.
All 31 fresh game outputs matched the accepted default first round, but no second
round or canonical receipt exists: **the two-cold regression has not passed**.
Source guards and cleanup passed. This operational limitation is separate from
the CPU candidate's known strict blockers. A retry needs a fresh reviewed plan;
historical controls and failed runs are never rebound or overwritten.

OP/MAINL/ZUN still need original stored-versus-decoded CODE mapping and
independent exact reconstruction. Full MAIN, resource/heap/IRQ/device behavior,
DATA/BSS physical ownership, complete product graph and original provenance
remain open.

## Build, CI and private artifact retention

All edits, reads, Python, Ghidra queries, Oracle and builds go through the
TH03 Factory MCP. Work headlessly; **serialize Borland/Wine builds** and
read TH04 references only from `/references/th04`. Preserve existing dirty
changes and their meaningful failure evidence; do not reset away blockers.

    python3 scripts/preflight.py
    python3 scripts/replay_th03_main_exact_units.py --run-id UNIQUE_ID
    python3 scripts/ci.py
    git diff --check

Latest completed full CI: **PASS, 783 tests, zero errors/failures/skips**,
followed by all available target/toolchain/Ghidra identity, ledger/progress
and Oracle negative gates. It ran on 2026-10-19 13:12–13:16 UTC for the CPU
source-present milestone (85.551 seconds for the test suite). All 725 tracked
and proposed input hashes/modes stayed unchanged. Log and result:
`.analysis/gpt-dots-player-cpu-milestone-v01/full-ci/ci.log` and `ci.json`.
This result/status note was added afterward; source and validation inputs were
unchanged, and final documentation links and whitespace were checked separately.
The earlier clean-worktree 776-test CI remains retained under
`.analysis/gpt-dots-dirty-worktree-closeout-v01/final-ci/`.
The previous source-milestone CI remains retained under
`.analysis/gpt-dots-yumemi-gameplay-milestone-v01/final-ci/`.

Historical 2026-10-08 full CI passed **656 tests, zero errors/failures/skips**;
log: `.analysis/closeout/sol-maintenance-20261008/ci.log`.
The clean public-checkout reproduction at that checkpoint passed **656 tests
with 131 private-input-dependent skips**; log:
`.analysis/closeout/sol-maintenance-20261008/portable-ci.log`.
This historical portable run is not a current-checkout or remote GitHub result.
Use the activated `.venv` described in [the toolchain guide](TOOLCHAIN.md).
`requirements-ci.txt` now pins the verified decoder/emulator dependencies;
GitHub Actions installs them before verification. Missing dependencies fail
once with setup instructions, before tests or private tools execute.
The earlier 648-test missing-Unicorn failure and separate post-gates logs
under `.analysis/cleanup-20261008-followup/` remain historical records.

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

The historical follow-up maintenance audit is
`.analysis/closeout/sol-maintenance-20261008/receipt.json`.
It preserved targets, complete proof trees and the evidence at that checkpoint.
Cleanup protects MAIN `source_inputs`, nested retained receipts/reports,
documented symlink aliases and explicit active-run pins in every cleanup phase.
That audit found **278 product/compatibility/ownership/ledger inputs unchanged**
and **235 source/input guards matching** the then-current MAIN cold receipt;
these are historical guard observations, not claims about the later worktree.
Game source and exact scope were unchanged by that maintenance pass.

Detailed chronological technical checkpoints (including the 2026-10-06
stopped-state figures) remain in the versioned subsystem reviews and
[historical closeout](CLOSEOUT.md); do **not** mistake those checkpoint
numbers or old CI outcomes for the current accepted baseline above.
