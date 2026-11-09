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

The report's twelve source hashes were checked against all twelve current
maintained files. The complete normal link is strong scoped native evidence;
it is not whole-game source ownership or canonical Factory packed-file
acceptance.

### Evidence interpretation

`af1053k` is the latest source-bound integration for all twelve physical
owners. It supersedes the earlier `af1053i`, `af1052g`, `af1051k` and `af1047l`
full-set checkpoints for current source binding. Their reports remain useful
historical snapshots, not additional current proof. Older standalone
`af1024*` and `af1021*` reports are also historical for owners changed since
those stages; do not call them current source proofs. The focused reviews and
detailed compiler chronology are preserved in
[the after1053 archive](RE_HANDOFF_ARCHIVE_AFTER1053.md).

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

Recommended next work:

1. Continue `HitCircle::cel()` and Kotohime Radial Burst with substantive
   function-level recovery: inspect their current sources and focused reviews,
   explore natural C/C++ arithmetic and variable lifetimes, and compare the
   complete affected physical owner. Do not stop at cosmetic leaf rewrites.
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

## Current product status and limits

The last recorded session-start preflight (2026-11-08) reported; this documentation-only handoff refresh did not rerun it:

- **MAIN:** 106 units; file-backed authored source 78,737/78,737 bytes;
  main-function ledger 459/459; 335 boundary observations and 335
  function-exact entries. These are scoped source/ledger measures, not
  whole-game acceptance.
- **OP:** current decoded source acceptance 60 extents / 92 procedures /
  14,985 bytes (13,221 CODE + 1,764 initialized DATA). Canonical packed
  unit and whole-product acceptance remain separate.
- **MAINL:** decoded source acceptance 0/259; Factory acceptance false.
  The after587 native link is historical, not current broad source binding.
  Scoped Staff and root-controller native work is documented separately
  in MAINL_STAFF_NATURAL_CPP_AFTER942_REVIEW.md and
  MAINL_ROOT_CONTROLLER_NATURAL_CPP_AFTER944_REVIEW.md.
- **ZUN:** 77 decoded extents; 2,179 authored, 1,390 original-ASM and
  5,066 library bytes. Whole-product source ownership remains open.

Whole-game completion percentage is unknown. Use generated
[PROGRESS.md](PROGRESS.md) and current preflight rather than old totals.

### Open blockers

- The original BIOS input_s object remains source-native exact at 417 CODE
  bytes but the full MAIN link has a historical one-byte trailing-NOP gap.
  Do not insert a synthetic NOP or claim full-link acceptance.
- MAINL broad decoded publication and source binding need recertification
  against current sources and retained ancestry; current acceptance remains
  0/259.
- Vendor OMF packet identity and original raw MZ-header writer identity are
  separate from CODE/FIXUPP/PUBLIC and normal-link image/relocation equality.
  Canonical Factory packed-file acceptance remains open.

## Storage and handoff safety

The latest applied storage maintenance is
[after1024](STORAGE_HANDOFF_AFTER1024.md), summarized by the
[current storage policy](STORAGE_HANDOFF_CURRENT.md). It removed only
448 regenerable Python bytecode files and repacked Git without pruning.
All 21,319 Git object IDs/types/sizes, refs, reflog files and fsck output
were preserved. No .analysis proof file or native receipt tree was deleted.

Preserve the entire active source-bound receipt DAG, both original compiler
rounds, OBJ/LIB/EXE/MAP outputs, writer logs, Japanese targets, Wine/Borland
prefix and Ghidra/JDK state. Do not use unreferenced-receipt pruning, old
after439/388/319/511 cleanup tools, or generic generated-file previews to
justify native proof deletion. Only the official cache-only cleaner is a
routine deletion route. The 2026-11-09 cache-only preview found 0.0 MiB
eligible, so no files were removed. The 5.6 GiB `.analysis` tree is mainly
protected toolchain/Wine state and native work/proof outputs; no safe
unreferenced native-output set was established. A native proof purge requires
a new full dependency audit and explicit one-time allowlist.

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
