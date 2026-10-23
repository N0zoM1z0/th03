# TH03 handoff — 2026-10-23

Reconstruction resumed after handoff. The 98% authored-byte exact objective is
**not achieved**: the whole authored denominator is still unknown. Use local
headless tools, no Factory MCP. Commit format: `gpt-6.1-sol: xxx`.

## Start here

Read this file, [architecture](ARCHITECTURE.md), [workflow](RE_WORKFLOW.md) and
`.agents/skills/th03-re/SKILL.md`; inspect Git and run `python3 scripts/preflight.py`.
Use `.venv/bin/python` for CI (host Python lacks the required Unicorn setup).
Re-attest the selected database before target analysis. All Japanese targets
remain `candidate-local-attested`, not independently pristine-dump attested.

Preserve the game-local Wine prefix and one Borland writer at a time. Recent
probes use CPU 19, nice 10 and clear DISPLAY/WAYLAND_DISPLAY; For a 768 MiB Java heap cap use
`_JAVA_OPTIONS="-Xmx768m -XX:ActiveProcessorCount=1"`; the Ghidra wrapper resets
`JAVA_TOOL_OPTIONS`. Do not kill other repositories' jobs.

## Authoritative checkpoint

The resumed entry checkpoint passes full CI: 2,335 tests (two existing skips),
all four database attestations and Oracle/toolchain checks. Wall7:54.19; peak RSS
660,052 KiB, one CPU/nice10, zero swaps. Logs: `.analysis/main-resume-20261023/ci.log`
and `ci-resources.txt`. Its current entry proof is `entry-review-v03.json` there.

`0285623` is the previous product-source checkpoint. The new entry source and
review are described below; all87 accepted extents retain their original scope.
Its complete CI passed 2,329 tests (two existing skips), all four database
attestations and Oracle/toolchain checks. Runtime 8:56.73; peak RSS 665,436 KiB;
zero swaps. Evidence is `.analysis/codex-main-lose-20261022-v01/ci-v01.log`,
`ci-v01.exit` and `ci-v01-resources.txt` within that directory.

| Product | Current bounded result | Completion limit |
|---|---|---|
| MAIN | 87 accepted extents; 413 functions; 66,843 scoped bytes | Reviewed-scope total, not whole authored denominator |
| OP | Source 45/46 units; 13,221 scoped bytes; published 33 owners/9,530 bytes | 45-owner proposal remains unpublished |
| MAINL | Published 145 decoded owners;27,753 authored + 628 library bytes | Canonical exact ledger remains 0; no whole-game percentage |
| ZUN | Source 15/18 units; 1,855 scoped bytes | Canonical exact ledger remains 0; driver/library context separate |

Ledger counts: 296 units, 3,227 evidence rows, 4 hypotheses, 375 knowledge rows,
413 authored-function rows. The latest ledger refresh changed only the evidence
and knowledge bindings in existing OP33/MAINL145 publications; owner scope/hash/size is unchanged.

## MAIN frontier and unresolved questions

The new complete entry candidate at 96E6..9778 compiles to146 bytes and actually
links in MENT266. It preserves all87 accepted scopes and outside program bytes;
141/146 entry bytes match, with one far/relaxed call mismatch and global literal
relocation order still open. 293 bounded entry runtime cases and five mutations
pass. See [entry review](reconstruction/MAIN_ENTRY_REVIEW.md) and replay with
`scripts/review_th03_main_entry.py --output .analysis/NEW_MAIN_ENTRY_REVIEW.json`.

1. State 1,716 bytes and shot 1,497 bytes are compiled and actually linked in
   PSTL245. Existing 87 accepted scopes remain equal. The new ranges still have
   17 unrelaxed far calls/85 differing bytes and relocation-order differences.
   See [actual link](reconstruction/MAIN_PLAYER_STATE_LINK_REVIEW.md).
2. Eight native linker controls show effective group membership and the first
   physical CODE segment predict all 16 control and 20 observed MAIN calls.
   This is bounded native evidence, not a universal TLINK law or proof of the
   original 21,010-byte MAIN_01 physical producer. See
   [group controls](reconstruction/MAIN_FARCALL_GROUP_REVIEW.md).
3. `src/main/player/lose.cpp`/`.hpp` remain the committed PLSE257 candidate:
   four procedures at C0D8..C370, 662 candidate versus 664 target bytes.
   Three bodies 270/98/119 have 362 non-fixup raw bytes equal; renderer 175 versus 177
   remains unresolved. No new exact credit. See
   [defeat review](reconstruction/MAIN_PLAYER_LOSE_REVIEW.md).
4. Subsequent private probes PLSE258..261 **were not installed**. Explicit `_DI`
   uses the correct loop register but only saves DI; target also saves SI.
   O-/Z- do not change CODE. Symbolic ASM initialization changes only the three
   equivalent XOR encodings, not the save pair. Do not repeat the disproved
   assumption that `_DI` alone produces both saves in this toolchain.

Unused probe runs and their temporary carriers were removed during handoff cleanup.
Their conclusions are summarized above; those discarded experiments are no longer
locally replayable. The installed PLSE257 proof remains complete. Verify it with
`review-v04.py --installed --output FRESH.json` under
`.analysis/codex-main-lose-20261022-v01/`.

Next reconstruction work should resolve real producer/layout behavior, then
perform actual links and cold/runtime/ownership gates. Do not add dead variables,
padding, target-byte arrays or false ABI declarations to close the 2-byte gap.
Other MAIN_01 root CODE still totals 8,772 bytes (3,050+5,058+664).

## Cleanup and retention

Removed unused defeat experiments, abandoned cleanup audits and Python caches
(about 123 MiB of file contents). Current source, targets, tools, databases and
installed-source proof remain. Post-cleanup CI passes all 2,329 tests (two skips);
peak RSS 644 MiB, single CPU, zero swaps. See [cleanup record](reconstruction/HANDOFF_CLEANUP_20261022.md).

The long chronological handoff is retained at
[RE_HANDOFF_HISTORY_20261022.md](RE_HANDOFF_HISTORY_20261022.md). Its dated counts,
failures and next steps are historical; this page states the current checkpoint.
