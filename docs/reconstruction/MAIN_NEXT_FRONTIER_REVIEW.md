# TH03 MAIN next gameplay owner frontier — target-first intake v3

## Current correction, 2026-10-22

MAIN currently accepts 87 extents / 413 functions / 66,843 reviewed CODE bytes. The Marisa 1,958-byte interval below is already exact; the v3 two-interval description and its replay's overlap failure are historical, not a current work queue.

The retained current-source cold MAP at `.analysis/th03-main-exact/gpt-dots-yumemi-charge-default-cold-v01/round1/main.map` places a 1,497-byte `th03_main.asm` contribution in `P_SHOT_TEXT`, load offsets `0xE266..0xE83F`, immediately before the accepted 185-byte `p_shot` update/render contribution. The retained source corroborates five procedure starts at E266, E313, E35B, E3F2 and E737. This includes result-statistics rendering as well as shot preparation/reset/emission. These are compiler/reference observations, not a proved original physical TU or five accepted target function boundaries. Recover the coherent contribution and its dependencies together while preserving the accepted update/render behavior.

Fresh target evidence for the initial E266..E313 procedure is retained under `.analysis/codex-main-shot-20261022-v01/`: `ghidra-check.log`/`.exit` attest the selected MAIN database, and `target-prefix.json` records the verified immutable-target digest, all 173 decoded bytes, 46 instructions and 12 ordered relocation sites. Its two access-page port writes and twelve far calls agree with the reference hypothesis; the called API's identity still requires independent binding. `retained-root-map.json` records seven retained root CODE contributions totaling 23,459 bytes. That mixed root includes unresolved game/shared/library ownership and is not an authored denominator. No new source or exact credit is granted.

The complete five-procedure C++ candidate is now in `src/main/player/shotroot.cpp`, its declaration header and the bounded `src/main/round/results.inl`. It remains outside the default build and acceptance ledgers. The existing 185-byte update/render TU is unchanged. `target-complete.json` records the fresh target observations for all seven adjacent bodies: candidate sizes 173/72/151/837/264 bytes, with 12/0/3/8/3 ordered MZ sites, followed by the accepted 43/142-byte bodies. Reset uses the 64-entry, 48-byte enemy/fireball/explosion array, independently of the separate player-effect array. Native compiler, fixup-symbol binding, full linking, behavior, repeat and cold aggregate proof remain required.

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
