# TH03 MAIN next gameplay owner frontier — target-first intake v3

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

The v1 historic five-interval intake of 4204 bytes and v2 four-interval
intake of 3609 bytes remain under the corresponding .analysis receipts.
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
