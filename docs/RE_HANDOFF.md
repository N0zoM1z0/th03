# TH03 handoff

## Current checkpoint

The latest reconstruction checkpoint is `cb8ae8c1f22ae4477908a7f566c6cbe906b564d5`
(MAINL text ownership). It was saved locally after the already-running CI finished:
2,421 tests, 284 skips, PASS, 9m43s. The tree was clean and main was ahead 12,
behind 0 before this documentation-only cleanup. No native source changed in
that checkpoint. Terminal evidence remains in
`.analysis/work/text-final-ci.log` and `.analysis/work/text-final-ci.exit`.
Historical review notes saying “pending at writing” are snapshots, not current
job status; their original proof records have not been rewritten.

## Verified current source scopes

| Product | Accepted source scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 459 functions / 78,737 CODE bytes / 106 extents | Open |
| OP | 34 extents / 36 procedures / 4,099 CODE + 487 DATA bytes | Open |
| MAINL | 97 extents / 102 procedures / 16,138 CODE + 224 DATA bytes | Open |
| ZUN | 77 extents / 89 procedures or entries / 6,179 CODE bytes | Open |

OP includes 22 separately proved inline compiler bytes. ZUN accepts 8,635
CODE+DATA bytes: authored 2,179, original ASM 1,390, library 5,066. Whole-game
source/function denominators and the completion percentage remain unknown.
Existing source ownership verification is not a claim of newly implemented code.

OP/MAINL/ZUN current source-only cold pairs repeat all outputs and match complete
decoded and canonical DIET `-B` stored targets, but contain unowned reference or
vendor context. MAIN repeats 100 outputs / 98 project objects and all 1,553
literal ordered relocations match. Its remaining differences are CODE alignment
at load EC2D (target 90, candidate 00) and MZ headers 6,240 / 7,680 bytes.
The original VS module is explicitly vendor context, not authored source credit.

Publications: `config/{op_work,mainl_work,zun_work}/scoped_acceptance.json`.
Generated accounting: [PROGRESS.md](PROGRESS.md), `resources/progress.svg`.
Evidence and source presence are separately recorded in `config/evidence.csv`,
`config/knowledge.csv` and `config/units.csv`.

## Review index

Keep detailed ABI, source-transform and ownership findings in their focused
reviews rather than duplicating them here:

- [MAINL text](MAINL_TEXT_REVIEW.md): 613 CODE, first-use GAME3/O; CRT/GRCG
  services and classifier tables remain contextual.
- [MAINL root and continue](MAINL_ROOT_ORCHESTRATION_REVIEW.md): 2,857 CODE;
  switch 18, DATA 112 and BSS 186 stay uncredited; exact continue segment transform.
- [MAINL score data](MAINL_SCOREDAT_REVIEW.md): 229 CODE, first-use GAME3/O;
  checksum boolean is AL only, not normalized AX.
- [MAINL registration](MAINL_REGISTRATION_REVIEW.md): 2,720 CODE; adjacent
  music 68 and pointer DATA 40 remain uncredited.
- [MAINL cutscene](MAINL_CUTSCENE_REVIEW.md): 3,122 instruction bytes;
  72 table bytes and one emitted zero remain uncredited context.
- [MAIN graphics](MAIN_GRAPHICS_FILL_REVIEW.md): 207 instruction bytes;
  nine neighboring bytes and mask DATA remain outside ownership.
- [MAIN player family](MAIN_PLAYER_FAMILY_REVIEW.md) and
  [player state](MAIN_PLAYER_STATE_UPDATE_REVIEW.md): complete native partitions,
  near/far ABI and prior-owner invariance.

The interrupted cutscene ancestor run was not a pass. Original cold and support
reports were recovered only after exact equality with their published hashes;
unchanged guards then passed. Never replace this distinction with a synthetic
complete flag or refreshed hash. Keep its recovery evidence.

## Retained inputs and working state

Preserve fixed Japanese targets/assets (`candidate-local-attested`), the local
Wine prefix, TC4/TASM/JWasm, `.tools/ghidra`, `.tools/jdk`, `.venv`,
`_reference/ReC98` and `ghidra-project/`. Ghidra/JDK attest their complete trees;
do not trim their documentation or archives. Keep one working build per product
under Wine `drive_c/`: `TH03WORK`, `TH03OP`, `TH03ML`, `TH03ZUN`.

Required source input:
`.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar`.
Keep `scripts/lib/zun.py` unchanged because MAIN pins it. OP's builder is a
shared MAINL/ZUN utility; changing it invalidates native graph bindings.
Current proof inputs are `.analysis/work/*-build.json`, `main-unit-review.json`
and all paths actually bound by the current publications. Preserve final CI
receipts and the explicitly retained `.analysis/work/op-music-state-draft/`.

Before any future authorized work, read `AGENTS.md`, [architecture](ARCHITECTURE.md),
[workflow](RE_WORKFLOW.md) and the local
[th03-re skill](../.agents/skills/th03-re/SKILL.md). Use registered TH03 Factory
MCP, pinned headless tools, one CPU at nice10 and serialized Borland/Wine writers.
If native inputs are unchanged, use the selected review's `--current-cold` path
which revalidates the complete graph. Do not restart a large ancestor runtime
chain merely to refresh unchanged supporting reports. Preserve current reports
before any operation that could overwrite them.

## Cleanup boundary

No product implementation, target, ledger, publication or native recipe is part
of this cleanup. Obsolete transient files may be quarantined recoverably with a
manifest; current proof inputs and historically referenced backups stay in place.
Recoverable cleanup records and restore instructions are under
`.analysis/cleanup-quarantine/20261026-cleanup/`. Quarantine moves files out of
active locations; it does not reclaim disk space.
