# TH03 — active handoff (2026-11-09)

Follow the highest-priority workflow in [AGENTS.md](../AGENTS.md). This
page is the current checkout handoff. Earlier chronology is preserved in
[the after927 archive](RE_HANDOFF_ARCHIVE_AFTER927.md) and the
[after1053 continuation archive](RE_HANDOFF_ARCHIVE_AFTER1053.md); use this
page, not archived next-target lists, for current priorities.

## Start here

- Inspect the real persistent worktree with git status -sb. Preserve any
  dirty or untracked work; do not assume another agent is editing concurrently.
- Read [the workflow](RE_WORKFLOW.md), the affected source file and the
  focused review before changing a compiler-sensitive owner.
- Use only the pinned Japanese targets in config/targets.toml
  (candidate-local-attested). Never substitute translated/reference binaries
  or alter original target, OBJ, compiler, CRT or linker inputs.
- Keep the loop scoped: edit, compile the affected original physical TUs,
  compare the complete native objects and normal link, document useful
  findings, then commit as gpt-web: xxx. Do not push unless asked.
- Do not run a full cold replay for an ordinary scoped change.

## Current source-bound MAIN evidence

**Latest integration: af1053k**

Two independent original Turbo C++ 4.02 rounds rebuilt these twelve complete
physical owners together:

- Shared BOSS providers: `ba_sring` and `ba_srest`.
- Nine major BOSS owners: Mima, Reimu, Yumemi, Ellen, Kana, Kotohime,
  Marisa, Rikako and Chiyuri.
- The complete four-function HitCircle owner.

Both normal MAIN links match the original Japanese loaded image and all
ordered MZ relocations. The other 87 original game objects and Borland CRT
were reused; no full cold replay was run.

| Measure | af1053k result |
| --- | ---: |
| Complete physical owners rebuilt | 12 |
| CODE | 18,845 bytes |
| Ordered native fields | 2,570 |
| PUBLICs | 97 |
| Japanese MAIN loaded image | 124,642 bytes |
| Ordered MZ relocations | 1,553 |
| Independent original compiler rounds | 2 |

Protected report:
.analysis/work/exatt-layout-af1053k/report.json

Report SHA-256:
44fdc9bb483c928f4e47d9c916c94a228ecbea4e19c0703c349cd912e6235ea0

The report's twelve source hashes were checked against all twelve maintained
files at that checkpoint. Current scoped source bindings are: `ba_sring` and
`ba_srest` use `af1056c`, `ba_koto` uses `af1068e`, `ba_chiyu` uses `af1058a`,
`ba_mima` uses `af1059a`, `ba_kana` uses `af1060a`, `ba_reimu` uses `af1061b`,
`ba_ellen` uses `af1063a`, `ba_maris` uses `af1065a`, `ba_rikak` uses `af1066a`,
and `hitcirc` uses `af1068s`. Only `ba_yumem` remains bound to `af1053k`.
The `af1067a` ten-owner integration is historical for the later Kotohime
source change; its other nine owner bindings remain unchanged. Local native
probe reports are not Factory Oracle receipts or accepted facts.

Shared BOSS current-source refresh: `.analysis/work/exatt-layout-af1056c/report.json`
SHA-256: `f23dfc1120fdf36091ccc6b890ac6a7382af9790b5b1662c06a830a13aa7dad5`.
It covers 949 CODE bytes, 106 ordered native fields and eight PUBLIC offsets
across both shared physical owners, with the full Japanese MAIN image and
ordered relocations equal in two independent rounds. See the
[updated shared-core review](MAIN_BOSS_SHARED_CORE_NATURAL_CONTROL_AFTER1047_REVIEW.md)
and [pattern-rejection review](MAIN_BOSS_PATTERN_REJECTION_DO_WHILE_AFTER1025_REVIEW.md).

Kotohime's previous current-source refresh was `af1057d`; the newer Radial
Burst source is now bound by `af1068e`. It recompiled the complete 1,840-byte
`ba_koto` owner with 262 ordered native fields and eleven PUBLICs in two
original TC4 rounds, preserving the Japanese MAIN image and ordered
relocations. The update controller retains its direct inactive-player return.
The Radial Burst now has loop-header register indices and per-center scratch
lifetime. See the [current Radial review](MAIN_KOTOHIME_RADIAL_NATURAL_FOR_AND_ARITHMETIC_AFTER1033_REVIEW.md).

Current Kotohime report: `.analysis/work/exatt-layout-af1068e/report.json`
SHA-256: `a51759a9529f0da12dc9dd9cded1492aedf828405599ddafefc354876a25669c`.

HitCircle current-source refresh: `.analysis/work/exatt-layout-af1068s/report.json`
SHA-256: `af14a3b0d2de5b3b25d324d7725caf693c5363b12bd4b9c98be1e565af35e50b`.
It recompiled the complete 445-byte `hitcirc` owner with 30 ordered native
fields and four PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The two spawn paths write `age` and `pid`
directly; the unused `HitCircle::spawn` member is removed. The thirteen-record
update uses a natural `while` loop, and the renderer shares one cel temporary
between enemy and player draws. The `_BX` cel and symbolic monochrome hardware
operations remain because their natural rewrites still change CODE. See the
[current HitCircle lifetime review](MAIN_HITCIRCLE_NATURAL_LIFETIME_AND_RENDER_FOR_AFTER985_REVIEW.md).

Chiyuri current-source refresh: `.analysis/work/exatt-layout-af1058a/report.json`
SHA-256: `dde32e0ba6923503b17958abcc9524f64c30f6e3918c552fc72e30edb384d970`.
It recompiled the complete 2,654-byte `ba_chiyu` owner with 381 ordered native
fields and eleven PUBLICs in two original TC4 rounds, preserving the Japanese
MAIN image and ordered relocations. The 613-byte `gba_boss_update_chiyuri()`
controller now uses the direct inactive-player return before the complete mode
switch and collision/hitbox tail. See the
[current Chiyuri PID-scope review](MAIN_CHIYURI_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Mima current-source refresh: `.analysis/work/exatt-layout-af1059a/report.json`
SHA-256: `397144dec5bda10fd68ba3740c4409cd1adb38073fe30b2605235599d009f0a7`.
It recompiled the complete 1,922-byte `ba_mima` owner with 277 ordered native
fields and nine PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The complete Mima update controller now
uses the direct inactive-player return while retaining its level setup, mode
dispatch and collision/hitbox tail. See the
[current Mima PID-scope review](MAIN_MIMA_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Kana current-source refresh: `.analysis/work/exatt-layout-af1060a/report.json`
SHA-256: `da7b824a76578facb835758886e2ca95e2a6d5788b5548b3b2084cfb59bb3d29`.
It recompiled the complete 1,874-byte `ba_kana` owner with 274 ordered native
fields and nine PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The complete Kana update controller now
uses the direct inactive-player return before its attack-mode dispatch and
collision/hitbox tail. See the
[current Kana PID-scope review](MAIN_KANA_UPDATE_POSITIVE_PID_SCOPE_AFTER1033_REVIEW.md).

Reimu current-source refresh: `.analysis/work/exatt-layout-af1061b/report.json`
SHA-256: `2b36c1dae2ce97a8803cf443bf2f3346e47744a080d07fdc06225e6cca975c4f`.
It recompiled the complete 2,020-byte `ba_reimu` owner with 270 ordered native
fields and nine PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The complete Reimu update controller now
uses the direct inactive-player return before target tracking and frame
advancement, while preserving its INTRO/SELECT logic, four attack families and
collision/hitbox tail. See the
[current Reimu PID-scope review](MAIN_REIMU_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Ellen current-source refresh: `.analysis/work/exatt-layout-af1063a/report.json`
SHA-256: `9965bf3ad20cf6fe5fadb5ec5522529f19e086a6618d6598660629c85ef9c513`.
It recompiled the complete 1,675-byte `ba_ellen` owner with 213 ordered native
fields and nine PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The complete Ellen update controller now
uses the direct inactive-player return before target tracking and frame
advancement, preserving its level setup, attack-mode dispatch and collision/
hitbox tail. See the
[current Ellen PID-scope review](MAIN_ELLEN_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Marisa current-source refresh: `.analysis/work/exatt-layout-af1065a/report.json`
SHA-256: `85c25305bb19ad8683e49d10c616d23de3d91abb57ca97e6c666b4afdb4f75b8`.
It recompiled the complete 1,431-byte `ba_maris` owner with 199 ordered native
fields and nine PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The complete Marisa update controller now
uses the direct inactive-player return before its mode dispatch and collision/
hitbox tail. See the
[current Marisa PID-scope review](MAIN_MARISA_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Rikako current-source refresh: `.analysis/work/exatt-layout-af1066a/report.json`
SHA-256: `17e3ec6f9a147a36d35f77af3f6e73742efbe4605b7b9832f4773b6474fdc1b4`.
It recompiled the complete 1,677-byte `ba_rikak` owner with 215 ordered native
fields and eight PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The complete Rikako update controller now
uses the direct inactive-player return before its mode dispatch, preserving the
signed-byte spin update and collision/hitbox tail. See the
[current Rikako PID-scope review](MAIN_RIKAKO_UPDATE_POSITIVE_PID_SCOPE_AFTER1033_REVIEW.md).

Current-source ten-owner integration: `.analysis/work/exatt-layout-af1067a/report.json`
SHA-256: `857551a78dd400b20c72940c186dc53835c1385fa0bcb69131920e389d47c689`.
This integration rebuilt the current shared pair plus all eight updated
character BOSS owners together in two original TC4 4.02 rounds: 10 complete
physical owners, 16,042 CODE bytes, 2,197 ordered native fields and 83 PUBLICs.
Both normal MAIN links reproduce the original Japanese loaded image and all
ordered relocations. The two unchanged owners, Yumemi and HitCircle, remain
bound to the `af1053k` baseline; no full cold replay was run.

### Evidence interpretation

`af1053k` remains the latest twelve-owner integration checkpoint. Current
source bindings are split by the subsequent scoped refreshes: the shared pair
uses `af1056c`, Kotohime uses `af1057d`, Chiyuri uses `af1058a`, Mima uses
`af1059a`, Kana uses `af1060a`, Reimu uses `af1061b`, Ellen uses `af1063a`,
Marisa uses `af1065a`, Rikako uses `af1066a`, and the other two owners remain
bound to `af1053k`. The earlier
`af1053i`, `af1052g`,
`af1051k` and `af1047l` full-set checkpoints are historical snapshots, not
additional current proof. Older standalone
`af1024*` and `af1021*` reports are also historical for owners changed since
those stages; do not call them current source proofs. The focused reviews and
detailed compiler chronology are preserved in
[the after1053 archive](RE_HANDOFF_ARCHIVE_AFTER1053.md).

## Current source-bound MAINL evidence

The `af1055m` refresh rebuilds the complete Staff/root owners in two original
TC4 rounds. Both complete decoded EXE/MAP pairs and all ordered relocations
match the Japanese target. It preserves and revalidates the unchanged cold pair;
no full cold replay was run. The current decoded publication is restored.

Report: `.analysis/work/mainl-current-af1055m.json`, SHA-256
`79caf379d74222bb546b8d482f5c0e52fce31aeadf0279ca18fdbeabe6ae45d9`.
See the [focused review](MAINL_CURRENT_SOURCE_REFRESH_AFTER1055_REVIEW.md) for
source transport, current native evidence and the next-build commands.

## Latest source recovery and next work

The latest work concentrated on the complete Yumemi BOSS owner rather than
only its small attack leaves:

- `gba_boss_update_yumemi()` (368 B): register PID local, direct mismatch
  return, explicit scheduler result test, natural frame increment and
  base-first origin arithmetic; the full mode dispatch and collision/hitbox
  tail remain in their original order.
- `yumemi_render_main()` (333 B), `yumemi_render_arrival()` (404 B) and its
  83-byte caller: register-qualified locals, natural coordinate expressions,
  constant-first phase/mode tests, and preserved raster/hardware draw order.
- Ring, aimed, chase, cross-ring and rain attacks: natural modulo/phase
  predicates, base-first four-way cross-ring geometry, with RNG and bullet
  calls kept separate and ordered.

The complete `ba_yumem` owner remains 2,358 CODE bytes, 343 ordered native
fields and ten PUBLICs. The latest individual-owner proof is `af1053j`; the
latest twelve-owner integration is `af1053k`. Both use two independent
original TC4 rounds and reproduce the Japanese MAIN image and ordered MZ
relocations. Recent source checkpoints include `a15e7b4b` (arrival geometry),
`0fe02754` (update/main renderer), `e71406d8` (cross-ring geometry) and
`f7b0ef44` (pattern cadence). The final integration checkpoint is `7fe6d95c`.

The shared BOSS scheduler has also been re-naturalized under the current
controller scope. `boss_pattern_next()` now uses a `do-while` rejection loop,
preserving the inclusive recent-pattern window and one RNG draw per candidate.
Stage `af1056c` rebuilt both shared owners (`ba_sring` and `ba_srest`) in two
original TC4 rounds: 949 CODE bytes, 106 ordered native fields and eight
PUBLICs, with both normal MAIN links and ordered relocations exact. The other
ten owners remain source-bound to `af1053k`; see the
[af1056c shared-core review](MAIN_BOSS_SHARED_CORE_NATURAL_CONTROL_AFTER1047_REVIEW.md).

Kotohime's complete 332-byte `gba_boss_update_kotohime()` controller now
uses the direct inactive-player return before target tracking and mode
advancement. This re-applies the natural guard under the current Radial/Pellet
and arithmetic source, and preserves the entire switch plus collision/hitbox
tail. Stage `af1057d` rebuilt `ba_koto` in two original TC4 rounds: 1,840 CODE
bytes, 262 ordered native fields and eleven PUBLICs, with the full Japanese
MAIN image and ordered relocations exact. See the
[af1057d current-source review](MAIN_KOTOHIME_UPDATE_INTRO_GUARD_AFTER1025_REVIEW.md).

Chiyuri's complete 613-byte `gba_boss_update_chiyuri()` controller now uses
the same direct inactive-player return before target tracking and frame
advancement. The current 2,654-byte `ba_chiyu` owner was rebuilt in two original
TC4 rounds: 381 ordered native fields and eleven PUBLICs match, as do both
normal MAIN images and ordered relocations. See the
[af1058a current-source review](MAIN_CHIYURI_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Mima's complete `gba_boss_update_mima()` controller now uses the direct
inactive-player return as well. The current `ba_mima` owner was rebuilt in two
original TC4 rounds: 1,922 CODE bytes, 277 ordered native fields and nine
PUBLICs match, with the full Japanese MAIN image and ordered relocations exact.
The seven level-parameter initializations remain before the guard; the launched
player's mode switch and collision/hitbox tail remain after it. See the
[af1059a current-source review](MAIN_MIMA_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Kana's complete `gba_boss_update_kana()` controller now uses the same direct
inactive-player return. Its seven level parameters remain before the guard;
the full INTRO/SELECT/attack dispatch, render-frame update and collision/hitbox
tail remain in order. Stage `af1060a` rebuilt `ba_kana` in two original TC4
rounds: 1,874 CODE bytes, 274 ordered native fields and nine PUBLICs match,
with both normal MAIN images and ordered relocations exact. See the
[af1060a current-source review](MAIN_KANA_UPDATE_POSITIVE_PID_SCOPE_AFTER1033_REVIEW.md).

Reimu's complete `gba_boss_update_reimu()` controller now uses the direct
inactive-player return before target/frame updates. The current `ba_reimu`
owner was rebuilt in two original TC4 rounds: 2,020 CODE bytes, 270 ordered
native fields and nine PUBLICs match, with both normal MAIN images and ordered
relocations exact. The INTRO/SELECT logic, four attack families and complete
collision/hitbox tail remain in order. See the
[af1061b current-source review](MAIN_REIMU_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Ellen's complete `gba_boss_update_ellen()` controller now uses the direct
inactive-player return before target tracking and frame advancement. The
current `ba_ellen` owner was rebuilt in two original TC4 rounds: 1,675 CODE
bytes, 213 ordered native fields and nine PUBLICs match, with both normal MAIN
images and ordered relocations exact. The level setup, four attack-mode groups
and collision/hitbox tail remain in order. See the
[af1063a current-source review](MAIN_ELLEN_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Marisa's complete `gba_boss_update_marisa()` controller now uses the direct
inactive-player return before target tracking and frame advancement. The
current `ba_maris` owner was rebuilt in two original TC4 rounds: 1,431 CODE
bytes, 199 ordered native fields and nine PUBLICs match, with both normal MAIN
images and ordered relocations exact. The level setup, full attack-mode switch
and collision/hitbox tail remain in order. See the
[af1065a current-source review](MAIN_MARISA_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Rikako's complete `gba_boss_update_rikako()` controller now uses the direct
inactive-player return before target/frame updates. The current `ba_rikak`
owner was rebuilt in two original TC4 rounds: 1,677 CODE bytes, 215 ordered
native fields and eight PUBLICs match, with both normal MAIN images and ordered
relocations exact. The five level parameters remain before the guard; the
Orbit/Entities/Alternating Burst switch, signed-byte spin update and full
collision/hitbox tail remain after it. See the
[af1066a current-source review](MAIN_RIKAKO_UPDATE_POSITIVE_PID_SCOPE_AFTER1033_REVIEW.md).

The current-source integration after these updates combines both Shared
BOSS providers with Kotohime, Chiyuri, Mima, Kana, Reimu, Ellen, Marisa and
Rikako. Stage `af1067a` rebuilt all ten complete physical owners in two
original TC4 rounds: 16,042 CODE bytes, 2,197 ordered native fields and 83
PUBLICs match, as do both complete normal MAIN images and ordered relocations.
Only the unchanged Yumemi and HitCircle owners remain on the prior af1053k
source binding. See the [af1067a ten-owner integration report](#current-source-bound-main-evidence).

The later Kotohime Radial Burst source-only refresh `af1068e` supersedes the
`ba_koto` binding in that ten-owner integration. It revalidates the complete
1,840-byte owner in two original TC4 rounds; the other nine objects were not
changed. No full cold replay was run.
HitCircle's later `af1068s` source-only refresh similarly supersedes its
`af1053k` baseline binding. It revalidates the complete 445-byte `hitcirc`
owner in two original TC4 rounds; no other physical owner was rebuilt.

The current two-owner integration after the Radial and HitCircle updates is
`af1068t`: `ba_koto` and `hitcirc`, 2,285 CODE bytes, 292 ordered native fields
and 15 PUBLICs. Both original TC4 rounds and both normal MAIN links match.
Report: `.analysis/work/exatt-layout-af1068t/report.json`, SHA-256
`527dd1fa061231d33e796217ba7f6b41fdeb505c0a28abe348d5613647d675a2`.

Recommended next work:

1. Continue `HitCircle::cel()` and Kotohime Radial Burst with substantive
   function-level recovery: the spawn paths, thirteen-record update loop and
   renderer lifetime are now naturalized, but the BX cel calculation and
   Radial projectile arithmetic still deserve deeper register/operand-order
   experiments. Compare the complete affected physical owner each time.
2. Expand beyond the already integrated nine character BOSS owners. Use
   `config/units.csv`, `config/evidence.csv`, current source and focused
   reviews to identify genuinely unowned large functions or engine areas.
3. Treat all older next-target recommendations as historical. Recheck current
   source and evidence before selecting work; do not assume an old note or
   decompiler boundary is correct.

For every source change, choose an unused DOS-safe stage, rebuild only affected
physical TUs, compare the complete native extents/ordered fields and normal
link, and preserve both original compiler rounds. Do not run full cold replay
for ordinary scoped changes.

## Factory replay availability

The repository shell and scoped original-TC4 probes are available, but the
Factory-controlled replay queue currently rejects TH03 submissions because
`th03` is not registered with the configured replay worker. The accepted
snapshot therefore has no OracleResults for these imported claims. Do not
promote local probe output, Ghidra output, or Git commits to accepted exactness;
retry canonical replay only after worker registration is restored.

## Current product status and limits

The 2026-11-09 preflight and script audit distinguish these current scopes:

- **MAIN:** 106 units; file-backed authored source 78,737/78,737 bytes;
  main-function ledger 459/459; 335 boundary observations and 335
  function-exact entries. These are scoped source/ledger measures, not
  whole-game acceptance.
- **OP:** current decoded source acceptance 60 extents / 92 procedures /
  14,985 bytes (13,221 CODE + 1,764 initialized DATA). Canonical packed
  unit and whole-product acceptance remain separate.
- **MAINL:** current decoded publication is restored through `af1055m`.
  All tracked extents have source; accepted scopes and their origins are in
  generated progress. Whole-product and canonical Factory acceptance remain open.
- **ZUN:** 77 decoded extents; 2,179 authored, 1,390 original-ASM and
  5,066 library bytes. Whole-product source ownership remains open.

Whole-game completion percentage is unknown. Use generated
[PROGRESS.md](PROGRESS.md) and current preflight rather than old totals.

### Open blockers

- The original BIOS input_s object remains source-native exact at 417 CODE
  bytes but the full MAIN link has a historical one-byte trailing-NOP gap.
  Do not insert a synthetic NOP or claim full-link acceptance.
- MAINL scopes beyond the current decoded publication remain open. Extend
  affected native evidence before claiming additional ownership.
- Vendor OMF packet identity and original raw MZ-header writer identity are
  separate from CODE/FIXUPP/PUBLIC and normal-link image/relocation equality.
  Canonical Factory packed-file acceptance remains open.

## Storage and handoff safety

The [after1024 storage audit](STORAGE_HANDOFF_AFTER1024.md) and
[current policy](STORAGE_HANDOFF_CURRENT.md) remain authoritative. Preserve
all source-bound receipt ancestry, both raw rounds, logs, Japanese targets,
compiler/Wine and analyzer state. No native proof tree was removed in the
script audit. Generic cleanup now refuses receipt pruning and analysis
`--apply`; only `clean_generated.py --caches-only --apply` is supported.

## Script audit and current reporting

`status.py` and generated progress separate ledger, decoded publication and
current native owner checks. All bars count extents; MAIN's function ledger
is separate. The MAINL reviewers support read-only `--check`; the obsolete
145-owner publication fallback and presentation-source verifier gate are retired.
ZUN was republished after removing that presentation dependency; its complete
physical audit is unchanged. OP's publication remains valid.

Default `ci.py` checks changed machine-input syntax and whitespace; `--full`
selects the broad suite. The [script index](../scripts/README.md) records the
1,358-file syntax/dependency audit and broad-test failures rooted in the stale
MAINL cold graph and historical cleanup expectations. Use affected current
checks; the historical all-tests run was not repeated as a completion gate.
The later `af1055m` source refresh restores current MAINL decoded publication.

## Minimal commands

Read-only start and current MAIN review:

    git status -sb
    .venv/bin/python scripts/preflight.py
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1053k

For a changed physical owner, choose a genuinely unused DOS-safe stage and
list only the affected original TUs:

    STAGE=afNNNx
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage "$STAGE" --units ba_koto,hitcirc
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage "$STAGE"

Finish with affected checks and git diff --check. Documentation-only edits
do not require compiler, analyzer, preflight, cold replay or receipt refresh.

## Reference map

- [AGENTS.md](../AGENTS.md) · [Workflow](RE_WORKFLOW.md) ·
  [Architecture](ARCHITECTURE.md) · [Japanese targets](../config/targets.toml)
- [Latest twelve-owner integration](MAIN_TWELVE_OWNER_CURRENT_INTEGRATION_AFTER1053K_REVIEW.md)
- [Yumemi update and renderer](MAIN_YUMEMI_UPDATE_AND_MAIN_RENDER_NATURAL_CPP_AFTER1051_REVIEW.md) ·
  [cross-ring](MAIN_YUMEMI_CROSS_RING_NATURAL_CPP_AFTER1052_REVIEW.md) ·
  [attack cadence](MAIN_YUMEMI_ATTACK_MODULO_AND_PHASE_NATURAL_CPP_AFTER1053_REVIEW.md)
- [Detailed post-af927 chronology](RE_HANDOFF_ARCHIVE_AFTER1053.md)
- [HitCircle cel register and VRAM stride history](MAIN_HITCIRCLE_NATURAL_CEL_REGISTER_AFTER976_REVIEW.md)
- [Current storage policy](STORAGE_HANDOFF_CURRENT.md) ·
  [after1024 applied audit](STORAGE_HANDOFF_AFTER1024.md)
- [Historical handoff archive](RE_HANDOFF_ARCHIVE_AFTER927.md)
- [Generated progress](PROGRESS.md)
