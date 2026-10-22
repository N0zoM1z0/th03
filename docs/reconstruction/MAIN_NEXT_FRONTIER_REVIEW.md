# TH03 MAIN next gameplay owner frontier — target-first intake v3

## Current correction, 2026-10-22

MAIN currently accepts 87 extents / 413 functions / 66,843 reviewed CODE bytes. The Marisa 1,958-byte interval below is already exact; the v3 two-interval description and its replay's overlap failure are historical, not a current work queue.

The retained current-source cold MAP at `.analysis/th03-main-exact/gpt-dots-yumemi-charge-default-cold-v01/round1/main.map` places a 1,497-byte `th03_main.asm` contribution in `P_SHOT_TEXT`, load offsets `0xE266..0xE83F`, immediately before the accepted 185-byte `p_shot` update/render contribution. The retained source corroborates five procedure starts at E266, E313, E35B, E3F2 and E737. This includes result-statistics rendering as well as shot preparation/reset/emission. These are compiler/reference observations, not a proved original physical TU or five accepted target function boundaries. Recover the coherent contribution and its dependencies together while preserving the accepted update/render behavior.

Fresh target evidence for the initial E266..E313 procedure is retained under `.analysis/codex-main-shot-20261022-v01/`: `ghidra-check.log`/`.exit` attest the selected MAIN database, and `target-prefix.json` records the verified immutable-target digest, all 173 decoded bytes, 46 instructions and 12 ordered relocation sites. Its two access-page port writes and twelve far calls agree with the reference hypothesis; the called API's identity still requires independent binding. `retained-root-map.json` records seven retained root CODE contributions totaling 23,459 bytes. That mixed root includes unresolved game/shared/library ownership and is not an authored denominator. No new source or exact credit is granted.

The complete five-procedure C++ candidate is now in `src/main/player/shotroot.cpp`, its declaration header and the bounded `src/main/round/results.inl`. It remains outside the default build and acceptance ledgers. The existing 185-byte update/render TU is unchanged. `target-complete.json` records the fresh target observations for all seven adjacent bodies: candidate sizes 173/72/151/837/264 bytes, with 12/0/3/8/3 ordered MZ sites, followed by the accepted 43/142-byte bodies. Reset uses the 64-entry, 48-byte enemy/fireball/explosion array, independently of the separate player-effect array. Fixup-symbol binding, full linking, behavior, repeat and cold aggregate proof remain required.

## Far-call calibration and physical layout, 2026-10-22

FCAL226 is an original-toolchain control with four text inputs and four fresh native phases: one TC4 caller, two TASM far-return providers and TLINK. Both unlinked calls are genuine five-byte far calls. The same-SEGDEF call becomes `90 0E E8 07 00`; the same-group cross-SEGDEF call remains `9A 10 00 00 00`. Both resolve to their real far-return entries, and only the retained call has a segment relocation. This directly reproduces the distinction relevant to the current score `PLAYER_M_TEXT` / candidate `P_SHOT_TEXT` split; it is not proof of a universal linker rule or the original TH03 producer.

All four native commands exited zero, process/registry cleanup was certain, and the writer lock was released. The original observer then failed to parse MAP's `idle caller()` spelling. Its false completion remains unchanged. A separate exact parser-only correction and postguard audit passed with zero further native calls: `.analysis/codex-main-farcall-20261022-v01/offline-review-v02/review.json`. Preserve that complete evidence tree, including `native-v01/`, `native-v01-output/`, the offline reviewer and `native-v01-resources.txt`. Ten preparation controls passed; the outer run took 23.38 seconds, peak RSS 110,240 KiB, one CPU/nice 10 and zero swaps. This is compiler/linker evidence with no target inputs, runtime, product or authored credit.

`layout-intake-v01.json` and its producing `review-layout-v01.py` bind the retained MAP: MAIN_01 has twenty contributions / 21,010 CODE bytes at load `0x96E6..0xE8F8`. Joining the score and new candidate while preserving addresses has a minimum contiguous placement interval of 4,913 bytes / six contributions; it includes player move 284, hyper 595, a retained root fragment 1,716 and state 367 between the score 454 and candidate 1,497. Merely renaming the two endpoint segments would change intervening layout. This inventory is not a proposed exact acceptance or proof of original ownership.

A same-process-attested local headless query and immutable-target raw intake now cover the intervening 1,716-byte root contribution: provisional source/automatic-database associations are `sub_DA43` 1,106, `_player_render` 131, `sub_DF18` 209, `sub_DFE9` 151 and `player_bomb` 119. Preserve `main010-functions-v01.txt`/`.log`, `main010-target-intake-v01.json`, `main010-call-bindings-v01.json` and their producing scripts in the calibration tree. These are not reviewed authored boundaries. In particular, automatic Ghidra reported zero parameters for `player_bomb`, while raw BP+4 access and `RET 2` agree with the existing near-Pascal near-pointer declaration in `src/main/player/cpu.hpp`; do not adopt the automatic signature. `player-bomb-candidate-v01.inl` in the same evidence tree is a natural, uncompiled body draft using the existing API names; its gauge test is the available gauge at offset 0x1A, and the effect call passes the existing two-word coordinates plus word-sized pid. Header composition, compiler output, source binding and all acceptance gates remain pending.

A separate **open inference** concerns the full physical producer. The stage entry has 19,328 preceding CODE bytes in MAIN_01. Modulo the observed 1,023-byte TC4 LEDATA capacity, this leaves 109 bytes in its first record. That boundary separates the target stage's first seven segment sites from its following five. The remaining target sites also partition within the next two hypothetical records, but within-record enumeration and the original TU remain unproved. The hypothesis and evidence classes are explicit in `config/hypotheses.csv`, `config/evidence.csv` and `config/knowledge.csv`; exact/source counters remain unchanged.

The standard offline MAINL publication refresh rechecked the current source composition and retained native witnesses after the ledger additions. Exactly the three ledger input bindings changed; all 145 owner byte hashes/sizes remain identical. `mainl-refresh-install.json` and `mainl-refresh-v01/` in the calibration evidence tree preserve the refresh and prior sidecars are retained in `mainl-refresh-preimage/`. `mainl-refresh-semantic-diff.json` additionally verifies that the large sidecar diff contains only current-head/observation times and hashes derived from the refreshed identity/ledger proof files; every other field is unchanged. No native build or additional exact credit was performed. The existing OP 33-owner publication was separately re-prepared and published through its maintained CLI after ledger-only review: all owner fields are identical, all 2,297 input names are retained and exactly the same three ledger bindings changed. `op33-refresh-install.json`, `op33-refresh-v01/` and `op33-refresh-preimage/` preserve the comparison, replay and old publication. This restores its current scoped display without adding owners, native invocations or canonical credit. All 79 OP decoded acceptance/progress controls pass after installation.

Next recover the coherent MAIN_01 source/layout composition and measure its natural producer. Preserve the reviewed byte addresses, one-byte field packing, genuine far returns and complete target raw/literal-order gates through that work. A partial segment merge alone cannot establish the original relocation producer. The initial aggregate run after this ledger update found only the OP archival ledger install-binding error; its 2,304-test failure remains in `ci-v01.log`. The narrow repair is documented in [OP replay maintenance](OP_FULLCOLD_EXACT.md#archival-ledger-metadata-maintenance-2026-10-22). Eighteen binding controls, nineteen cold-proof tests, the 330-file current composition and complete historical replay pass with zero new native calls. Final aggregate CI after both publication refreshes passes 2,314 tests in 298.518 seconds with two existing skips and all tracking/progress/toolchain/all-four-database/Oracle gates. `ci-v03.log`, `ci-v03.exit` and `ci-v03-resources.txt` retain the result: outer 7:10.08, peak RSS 665,132 KiB, one CPU/nice 10, 768 MiB Ghidra heap cap and zero swaps. The original failed `ci-v01.log` remains unchanged.

A bounded scripts/tests bytecode inspection found 10,440,704 allocated cache bytes; `cache-inspection-v01.json` records zero deletions and no global proof-dependency sweep. Native receipts, target observations and all retained proof trees remain present. No new storage-saving or authored-byte credit is claimed.

## First actual source link, 2026-10-22

The candidate now uses the maintained `reimu_hyper_shot_add(Subpixel, Subpixel)` API. `scripts/stage_th03_main_shotroot.py` stages the exact five-procedure root removal, caller bindings, seventeen zero-storage DATA aliases and response insertion before `p_shot.obj`. A zero-code public alias binds the score helper at the already maintained `score_bonus_digits_put` entry; its far-Pascal return and eight-byte stack cleanup are preserved. Eleven maintained controls pass. None of these changes modifies the default build or grants source/exact credit.

A fresh four-phase compile/root-assembly/score-assembly/link ran in PSLK225. All native commands exited zero; owned process and registry checks passed, no survivors or poison remained, and the writer lock was released. Inputs were exactly 313 files / 760,420 logical bytes, including 83 explicitly retained context objects. The three changed project objects were freshly generated. The 23.76-second outer run used one CPU/nice 10, peak RSS 110,828 KiB and zero swaps. Its current-source object is 5,957 bytes / 107 OMF records, SHA-256 `b0b33a330a159868dac3cc25429f631b40baea5638c0161ac78b61ba88dae792`, still exactly 1,497 CODE bytes with no private DATA/BSS.

Actual linking did **not** pass the diagnostic gate. All 87 prior extents / 66,843 bytes retain complete raw and literal-order equality. Every MAP allocation/address outside the transferred contribution is preserved; the score alias emits no bytes, and exactly 23 new public names appear. The candidate program nevertheless differs from the retained baseline in 65 bytes, entirely within thirteen five-byte call windows. The target uses `NOP; PUSH CS; CALL near`; TLINK retained `CALL far` for ten dynamic-score calls, one high-digit call and two score-add calls. All thirteen calls resolve to the correct target callee addresses. The header has 1,566 relocations versus 1,553, with exactly thirteen added sites and none missing. After excluding those extra sites for diagnosis, the remaining 26 scoped sites have target membership but unequal literal order. That exclusion is not an acceptance comparison or a byte transformation.

Preserve `.analysis/codex-main-shot-20261022-v01/link-native-v03/` and `link-native-v03-output/`, especially `object-verification.json`, `completion.json`, the four phase receipts and registry transitions. `linked-call-diagnosis-v02.json` and its producing `diagnose-linked-v02.py` bind the raw comparisons and callee-address checks. Original failures remain intact: PSLK223 stopped during directory staging with zero native calls; PSLK224 compiled/assembled three objects, then TLINK rejected the Unix-style response path. PSLK225 used the corrected DOS path, freshly rebuilt all three objects and linked successfully. Thirteen preparation controls, including real source/context materialization, passed before that run. The successful native link is not a successful diagnostic receipt, full cold build, runtime result or exact promotion.

Aggregate CI for the maintained API/stager checkpoint passes 2,304 tests in 419.675 seconds, with two existing skips; tracking/progress/toolchain/all-four-database/Oracle gates pass. `ci-link-v01.log`, `ci-link-v01.exit` and `ci-link-v01-resources.txt` in the evidence tree retain the result. The outer run took 10:19.20 with peak RSS 664,632 KiB, one CPU/nice 10, 768 MiB Ghidra heap cap and zero swaps. This verifies the current repository and preserved proofs; it does not promote the failed new-scope diagnostic.

Next investigate the natural compiler/linker far-call optimization and object framing, then literal relocation order. Do not change executable/object bytes, reorder relocation output, weaken the current raw/order gates or manufacture ABI declarations. Independent cold rounds, behavior and the complete Oracle set remain open.

## Native compiler checkpoint, 2026-10-22

The first PSRC221 attempt exposed duplicate historical shot declarations and a DOS-header ordering conflict. Its one native call failed with certain process/registry cleanup and released lock. Those receipts and frozen source inputs remain unchanged. The candidate header was corrected without modifying shared compatibility headers or accepted source. PSRC222 then compiled successfully with the original TC4J flags: 50 staged source/compatibility files and four vendor headers, 78 literal include edges, no retained object seeds. Eleven focused capsule controls pass for each preparation.

The actual 5,964-byte object has 107 valid OMF records and exactly 1,497 CODE bytes in P_SHOT_TEXT; DATA/BSS are zero. All five public starts, lengths, return forms and instruction shapes agree with the target. The native phase completed in a 6.70-second outer run, peak RSS 108,912 KiB, one CPU/nice 10, no swaps, clean registry/process audit and released writer lock. Receipts: `native-v02-output/completion.json`, `compile_shotroot-finished.json`, `object-verification.json` and registry transition under `.analysis/codex-main-shot-20261022-v01/`. Object SHA-256 is `058169534233ef0655cbecb257c32bfcfe95c23ad41ee6f21158f6073a4403d2`.

`unlinked-fixup-observation.json` records 109 symbolic fixups and thirteen possible same-segment far-call relaxations. Every byte outside those fields/relaxations equals target. The 26 unrelaxed segment-fixup positions have target membership but a different traversal order. This is an unlinked diagnostic, not an actual linked-relocation observation. `retained-root-order.json` separately proves that the old retained linked contribution already has target-equal CODE but unequal literal relocation order; reassembling its old source does not establish target order.

Before linking, resolve the candidate's provisional helper names through the maintained score and Reimu producers. Their old `sub_D668`/`sub_14B0A` bodies were already extracted: the current root calls `score_bonus_digits_put` and `REIMU_HYPER_SHOT_ADD`. The latter's maintained declaration takes two `Subpixel` values; preserve that source/API contract as well as its two-word far-Pascal ABI. `link-preparation/attempt.json` records the failed staging anchor check, with zero native calls and no baseline modification. The remaining root/data aliases and response insertion are still proposals. Actual complete raw/order/layout comparisons, behavior and independent cold rounds remain open; exact credit is zero.

Aggregate CI on the compiled-candidate checkpoint passes 2,293 tests in 374.775 seconds, two existing skips, and completes tracking/progress/toolchain/all-four-database/Oracle gates. Log and resource audit: `ci.log` and `ci-resources.txt` in the evidence tree. Peak CI RSS is 665,468 KiB with one CPU/nice 10 and a 768 MiB Ghidra heap cap. This is verification of the current tree, not a full game cold build.

## Historical v3 intake

Status: **two provisional, non-exact CODE intervals totaling 2131 bytes**.
Neither has a recovered complete original physical owner or accepted
function partition yet. No new exact credit from this intake.
The **334/334 exact functions** apply only to the 74 already
reviewed CODE extents, not the whole game.

## Immutable-target review

    python3 scripts/review_th03_main_next_frontier.py

Current receipt:

    .analysis/th03-main-next-frontier/target-review-v3.json

Pinned Japanese TH03 MAIN.EXE target SHA-256:
f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b.

The review checks full 16-bit bounded decode, original MZ relocation
site containment and order, ending return boundary and disjointness
from all exact CODE spans in the current manifest. These checks do
not prove interior function starts/shared tails or DATA/BSS origins.

| Still-unreviewed subsystem | Target load-image bytes, end exclusive | Size | MZ sites | End |
| --- | --- | ---: | ---: | --- |
| HITBOX Marisa charge/hyper prefix | 0x142D0..0x14A76 | 1958 | 30 | far RETF |
| P_SHOT ordinary-shot producer prefix | 0x0E266..0x0E313 | 173 | 12 | near RET |

The previous v1 five-interval intake (4204 bytes) and v2 four-interval
intake (3609 bytes) are **historical checkpoints**, not a current frontier.
The v2 receipt is retained at
`.analysis/th03-main-next-frontier/target-review-v2.json`; the redundant
unreferenced v1 JSON was removed by the guarded 2026-10-08 cleanup. Its source/commit and
subsequent accepted owner proofs are still versioned. Re-run the current
v3 review command above for the latest boundary checks.
The full ten-function Hyper handler (595 bytes) and the complete four-function
HUD round-intro/renderer (1478 bytes) are **no longer provisional**:
they pass exact raw CODE, physical MAP, ordered MZ relocation and
DOS behavior tests. Their natural/symbolic source and provenance are
recorded in MAIN_HYPER_DISPATCH_REVIEW.md and
MAIN_HUD_ROUND_INTRO_REVIEW.md, respectively.

## Next tasks

1. Review the **entire 1958-byte Marisa charge, hyper, hitbox and
   bomb/gameplay prefix**. It has 30 contained MZ sites, multiple near/far
   entries, character-local globals and shot/gauge dependencies. Corroborate
   original boundaries and shared tails against the immutable target
   before declaring logical or physical owners. Existing charge/boss
   source is a reference, not automatic proof.
The full ten-body target breakdown, including 470-byte gauge and
449-byte bomb functions, is in MAIN_MARISA_GAMEPLAY_REVIEW.md.
No Marisa CODE exact promotion is claimed by that analysis.

2. Bring in the 173-byte P_SHOT hardware producer with its larger ordinary-
   shot dependency graph, rather than spending the session on small
   leaves alone.

For each complete new owner: prove original ABI, DATA/BSS and linker
relationships, recover maintainable source, check exact MAP/raw bytes,
original **ordered** MZ relocations and DOS behavior in two serial cold
builds including every prior exact owner. Preserve negative OMF
calibration drift, and do not weaken acceptance. Whole MAIN and
OP/MAINL/ZUN remain incomplete. No native Factory Truth Kernel
acceptance or independently pristine original provenance is implied.

Negative controls: tests/test_main_next_frontier_review.py.
