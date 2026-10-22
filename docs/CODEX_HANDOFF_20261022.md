# TH03 handoff to Codex, 2026-10-22

## Resumed work and historical stop state

The owner has resumed development with a 98% authored-byte exact goal across TH03, authorized local tools and regular commits/pushes using `gpt-6.1-sol:`. The PFOPEN repair is now integrated and aggregate CI passes; the OP acceptance proposal remains pending. The complete authored denominator is still unknown.

The earlier pause was requested at 18:12 UTC+8. That checkpoint captured recoverable cleanup and preserved drafts without new native runs, acceptance publication or source integration after the pause. An already-running offline OP preparation completed before closeout. The sections below retain that historical inventory with current verification noted explicitly.

- Live repository: `/home/pentester/coding/codex_ida/th03-reconstruction/th03`, Factory repository ID `th03`, branch `main`.
- At the pause checkpoint all commits were local. The owner has now authorized pushing to `origin/main`; inspect `git branch -vv` for current synchronization. Base before the pause handoff: `d9bb4235697638f645b52054c92e455cff9d6b70`.
- Read `AGENTS.md` first, then this document. `docs/RE_HANDOFF.md` retains the longer history.
- Continue in the existing live workspace: ignored `.analysis/` contains required private proofs and both partial proposals. A fresh Git checkout alone is not a full evidence workspace. Never use `git clean -fdx` or indiscriminate `.analysis/` removal.

## Completed and committed

- `0b07a287`: six OP source/proof packages, updated MAINL acceptance, frozen OP 33-owner publication and progress/SVG integration.
- `1a66d81`: exact missing support.py recovery, a nonexecuted versioned backup and restored OP historical cold/packing replay.
- `8a18afa`: cleanup retention now follows native list inputs and transitive typed guards; includes ancestor-symlink protections and regression tests. It was not used for another broad cleanup.
- `1b9ee86`: exact effects object recovery, 32 archive restorations, correction of the earlier cleanup conclusion and six new recovery tests.
- `d9bb423`: pins the lossless archive of terminal intermediate audit logs before removal.

The support helper is exactly 5,324 bytes, SHA-256 fd19475aea02ec5aa6ae8e4c48f6ab88170f1d73e0f6ee7dbfa7231d50dc8c68. Its recovery copy is `config/recovery/native_support_20261020.py.txt`.

The missing effects.obj was reproduced by one new, bounded native compile in EFRC222: 2,216 bytes, 48 OMF records, SHA-256 d37d84309d2cc4d66ef62e67c2685839ac05c74bc1ea90be60d408cb4272d13a. Cleanup/registry checks passed. Exact data was restored to the old missing path, without recreating old producer receipts, changing old pins, patching bytes or claiming original filesystem mtime. Preserve `.analysis/effects-fresh-reproduction-20261022-v03`, `.analysis/effects-fresh-reproduction-output-20261022-v02` and `.analysis/dependency-recovery-20261022-v01`. The preceding failed staging attempt made zero native calls and remains preserved.

## Verification

- P_SHOT candidate checkpoint on `d9cb49e`: aggregate CI passes 2,293 tests in 374.775 seconds with two existing skips and all remaining identity/database/Oracle gates. CI peak RSS 665,468 KiB under one CPU/nice 10/768 MiB Ghidra heap. Source-only PSRC222 compiles five bodies / 1,497 bytes in one native phase with no private DATA/BSS, no retained objects, clean cleanup/registry and released lock; peak native RSS 108,912 KiB. Lengths, instruction shapes and raw bytes outside declared fixups/possible linker relaxations agree with target. Symbol bindings, actual link and literal order remain open. Evidence: `.analysis/codex-main-shot-20261022-v01/`. PSRC221 is a preserved failed include-composition attempt, not a successful producer.
- Integrated repair verification: aggregate CI passes with 2,293 tests in 363.258 seconds, two existing skips, complete tracking/progress/toolchain checks, all four stored Ghidra database attestations and Oracle smoke controls. Focused PFOPEN/cold-source tests: 146 pass. PFOPEN verbatim replay, 330-file current composition and full historical OP cold replay pass without native invocations. Logs, replay reports and reviewed install manifest: `.analysis/codex-pfopen-binding-20261022-v01/`. Single CPU, nice 10, Ghidra heap cap 768 MiB; full-CI peak RSS 657,944 KiB, zero swaps reported by the resource audit. Original failed receipts remain preserved.
- Codex status check on `cf17a65` (2026-10-22): preflight and generated-progress checks pass. Aggregate CI ran 2,243 tests in 288.125 seconds, with one error, one failure and two skips; both failing cases still stop at PFOPEN's `input drift scripts/clean_generated.py`. CI stopped at the test stage, so later aggregate gates were not run. Log: `.analysis/codex-status-20261022-AG5AK1/ci.log`; exit: `ci.exit` in that directory. Single CPU, nice 10; peak RSS 657,540 KiB (642 MiB), with zero swaps reported by the resource audit in `resources.txt`. No proposal integration or native build was performed.
- Full integrated run at `8a18afa`: 2,237 tests in 273.863 seconds; one error, one failure, two skips. Both failing cases are in `test_op_pfopen_replay`, stopping at the historical cleaner input binding. Log and exit: `.analysis/dependency-recovery-20261022-v01/post-recovery-full-tests.log` and `.exit` with the same basename. Exit is 1.
- Integrated recovery tests: nine pass, including the three existing support tests and six new dependency-recovery tests. Log: `.analysis/dependency-recovery-20261022-v01/integrated-recovery-tests.log`.
- Cleanup: 57 root focused tests pass; the proposal validation also covered 14 closeout tests, 71 total.
- Historical PFOPEN proposal check: 112 focused tests passed before integration. The integrated results above supersede its test status.

Use `.venv/bin/python -B`, not system Python: the venv has the required Unicorn/Capstone versions. After reviewing/integrating the repair, run its focused tests, `.venv/bin/python -B -m unittest discover -s tests`, and the aggregate CI prescribed by `AGENTS.md`. Do not turn failures into skips or rewrite historical expected hashes.

## PFOPEN input-binding repair — integrated

The preserved six-file draft was reviewed against its exact preimages and original Git blobs, then installed. The follow-up `config/op_fullcold_exact/source_bindings_v2.json` separately binds the changed replay and test files while preserving their original install entries and inert snapshots. The original proof, native manifests, verifier bytes and reports are unchanged. Current replay/test bytes and modes remain checked; all other source-dependency guards remain active. See the reviewed install record and current verification above. The following paragraphs describe the original proposal before integration.

Authoritative live draft: `.analysis/pfopen-input-binding-20261022-v01/files/`. Its latest test log is `expanded-tests.log` in the proposal root: 112 tests, 13.387 seconds, OK. `initial-pin-comparison.json` checks all 1,431 retained pins: exactly two live housekeeping files drifted, cleaner and progress; the other 1,429 passed.

This is why the integrated replay is still red. Both files are frozen historical inputs, not current consumed source/import helpers. The draft resolves only those two logical paths to exact, inert snapshots. Original logical modes remain pinned separately from snapshot storage mode 0644. It also versions the current replay SELF binding while retaining the original replay bytes. The original proof, inventory, native verifier and receipts remain unchanged. The loaded historical verifier receives the same narrowly enumerated two-path I/O adaptation; other pins delegate unchanged. Source/helper guards, exact closure checks and verbatim original-report comparison remain enforced. Review this boundary carefully before integration.

Changed/new target files:
- `scripts/replay_th03_op_pfopen_source.py`
- `tests/test_op_pfopen_replay.py`
- `config/op_pfopen_source/replay_binding_v2.json`
- `config/recovery/clean_generated_095e54bc.py.txt`
- `config/recovery/progress_1feecd5c.py.txt`
- `config/recovery/op_pfopen_replay_0b07a287.py.txt`

Exact origins: cleaner commit 095e54bc3d437ca12ea499aeb242d1c6b1e79253 / blob 9d658a86ac7f5c4fe9140c59e04ac5cff0bd9c5c; progress commit 1feecd5c980be16625a4dbf0ba148a98b6a8f3f3 / blob e7ec8096111a2da54de429fc4120bf5430dd8d9e; original replay commit 0b07a287ddeef8904046ef5f8ebdfaa352f332ea / blob d6f0b5a637fdfba70b1e8974b172056f0bfd6b94.

The draft was not finalized as an install package. `prepare.py` and `extend_tests.py` in its root are intermediate builders and must NOT be rerun unchanged: `files/` is the latest implementation. This handoff captures its six changed files as `docs/handoff/20261022/pfopen-input-binding.draft.patch`, with exact preimage/proposal hashes in `DRAFT_MANIFEST.json`. This is preservation, not approval or integration. Review, verify preimages and modes, produce a reviewed install manifest, then apply and test.

## Second next task: current OP product acceptance draft

Preserve `.analysis/op-current-product-acceptance-proposal-20261022-v01/`. It contains a new acceptance library/runner, a fixed 45-owner / 13,221-byte cohort, draft helper bindings and a sealing utility. No old publication was changed. No progress/status/SVG integration or negative tests were written.

The already-started offline prepare completed successfully after the pause request: `.analysis/op-current-product-acceptance-proposal-20261022-v01/review-v01/review.json`, SHA-256 1f9494e81517cbb849890fcbd3ffa0965ceaadd4be7d879973dab5f95b5d1e07. It checked the 62 historical cold phases, five separate packing phases, both actual owner/object/MAP/EXE sets, 330 current composed sources and eleven owner gates. Published=false; native_invocations=0. This is preparation evidence, not human code review or acceptance publication.

The special lineage cases are selection split 48 + 2,858 bytes across selhelp/seltail, and PFOPEN 281 bytes in optail via the th03/formats source alias. Keep both independently checked. The old 33-owner / 9,530-byte publication is a frozen historical cohort and must stay unchanged. IRAND42 stays excluded; do not reclassify vendor code for credit.

Review the code and add negative tests. Re-seal helper bindings only after final helper/tracking integration, and prepare fresh evidence. In particular, `replay_th03_op_fullcold_exact.py::check_current_sources` currently pins every file in source-dependency install manifests, not merely consumed code. Integrating the PFOPEN replay repair may expose its old helper binding here. Inspect the exact failure and make any versioned compatibility change narrowly; do not discard guards or rewrite old manifests.

Preserved draft: `docs/handoff/20261022/op-product-acceptance.draft.patch`. The optional sealing utility is copied as inert text beside it. Package docs, reviewed install manifest, negative tests and UI integration remain unfinished. Suggested final UI files: `scripts/status.py`, `scripts/progress.py`, `scripts/validate_tracking.py`, `resources/progress.svg`, `docs/PROGRESS.md`, `docs/RE_HANDOFF.md`.

Packing provenance must remain precise: two cold decoded EXEs are exact; a separate source-produced byte-identical EXE was packed twice. Those cold outputs were NOT directly packed. Canonical mixed-product equality is not 36,041 newly authored bytes.

## Cleanup and preservation

An earlier cleanup missed list-form indirect dependencies; a missing helper masked downstream failures. All 32 discovered archived dependencies were restored exactly, including mode and nanosecond mtime: 9,370,166 logical / 9,433,088 allocated bytes. Receipts 001–004 live under `.analysis/dependency-recovery-20261022-v01/`. Keep all five original lossless archives and restoration manifests under `.analysis/cleanup-archives-20261022-v01/`.

Final reconciliation: `.analysis/recovery-reference-audit-20261022-v01/reference-restoration-audit-final.json`; independent present-file verification: `present-restored-dependencies-verification.json`, SHA-256 2c276b9fc486d97f3bd1460eb9c1490902b0ea9788ca66fd81a47f506b816d8e. No pending archived restoration or cleanup Git/cache-deletion intersection remains in that audit. There are still 859 historical missing-reference strings and 22 unavailable historical JSONs; this is not proof that every old replay is possible.

For closeout, only three terminal intermediate audit edge logs were losslessly compressed: 136,354,163 bytes to 3,742,512 bytes. The archive is `.analysis/cleanup-archives-20261022-v01/recovery-audit-raw-edges-v01.tar.xz`, SHA-256 d111e0be2ba5a535408c656221932fc642305d85b8231eecbcfdacc0db3828dc. Its `-members.json`, `-verification.json` and `-applied.json` sidecars record exact restoration and removal. All members were round-trip verified before the three redundant originals and their own test-extraction copies were removed. The final raw graph, JSON reports, native receipts, restored dependencies and active drafts remain live. Net allocated saving for these three logs is 132,616,192 bytes excluding the small apply receipt.

At 10:17:20 UTC, `.analysis/` used 16,547,971,072 allocated bytes, versus 21,563,080,704 before cleanup: about 4.67 GiB less, including intervening recovery/proposal work. This is a dated measurement, not a fixed future footprint. See `docs/reconstruction/ANALYSIS_CLEANUP_20261022.md` and `DEPENDENCY_RECOVERY_20261022.md` for the full corrected history. Do not remove toolchain, targets, reference corpus, venv, Ghidra, locks/poison/ownership records, archives or either partial proposal.

## Honest progress and later source work

Current published source acceptance remains OP 33 owners / 9,530 decoded bytes and MAINL 145 scoped owners. OP maintained source inventory is 45/46 extents / 13,221 bytes; the 45-owner new publication is still a draft. MAINL publication is already complete and its canonical authored credit remains zero. Do not interpret canonical packing or mixed-product equality as a whole-game authored percentage. No new source credit or SVG percentage was claimed during closeout.

The current source frontier is the complete 1,497-byte P_SHOT root contribution at E266..E83F, now a compiled candidate under `src/main/player/shotroot.cpp`/`.hpp` and `src/main/round/results.inl`. The existing 185-byte update/render TU remains separate. Follow the current correction/compiler sections of `docs/reconstruction/MAIN_NEXT_FRONTIER_REVIEW.md`; its older v3 intake includes already accepted Marisa and is historical. The candidate's proposed far helpers must bind to `score_bonus_digits_put` in the accepted score ASM and `reimu_hyper_shot_add(Subpixel, Subpixel)` in `src/main/player/reimu_gameplay.hpp`; their old disassembly bodies are no longer present in the current root. A preliminary source-root stager stopped at that identity check without native calls; see `link-preparation/attempt.json` under the current evidence tree. Source/name linkage, actual raw/order/layout and two cold rounds must precede ledger promotion. ZUN driver/ONGCHK remain library-origin material.

The conservative cleanup preview from the previous checkpoint was cancelled after more than thirteen minutes of read-only dependency scanning to prioritize source compilation. Its owned process terminated with exit 143; zero deletions occurred. The original preview log and cancellation are retained in `.analysis/codex-pfopen-binding-20261022-v01/`. Do not treat that attempt as a completed cleanup or a new storage-saving claim.

For native work, retain the established sole-writer lock/poison/ownership protocol, single CPU, nice>=10, headless UTC, 90-second phase plus 15-second owned cleanup, fresh namespaces and complete receipts. Never patch executable/OMF/relocation bytes, invent old producer receipts, run a carrier twice or use global process kills. The owner has authorized regular pushes for this resumed goal.
