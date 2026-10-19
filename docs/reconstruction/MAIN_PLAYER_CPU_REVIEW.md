# MAIN CPU player-state source milestone

2026-10-19: **source-present only, no exact promotion**. Four complete natural
C++ functions cover C370..C7A5: **1,036 function bytes + two 20-byte switch tables
+ one real compiler-produced zero = 1,077 CODE bytes**. Accepted MAIN remains
**78 extents / 371 functions / 59,624 bytes**. The broader source-present scope
is now 81 extents / 386 functions / 63,044 bytes; this is not a whole-game denominator.

## Owner and ABI

Maintained `src/main/player/cpu.cpp` and `cpu.hpp` preserve native-v03 body and
layout assertions; localization changes only the include path and provenance
comment. Physical producer p_cpu owns PLAYER_M_TEXT / MAIN_01 at 096E:2C90,
load C370, original file DBD0, length 0435. Names are semantic reconstruction,
not recovered original symbols.

| Function | Load span, end-exclusive | Bytes | Contract |
| --- | --- | ---: | --- |
| player_cpu_direction_for_collision | C370..C433 |195| near Pascal; signed16 dy,x,y at BP+8/+6/+4; AX input_t; RET6 |
| player_cpu_approach_target | C433..C535 |258| near Pascal; near player pointer BP+4; RET2 |
| player_cpu_update | C54A..C568 |30| same pointer; RET2 |
| player_cpu_dodge_and_aim | C568..C791 |553| same pointer; RET2 |

The sole zero is at C535; switch tables are C536..C54A and C791..C7A5.
The dispatcher is called at DB0E from complete player update DA43. Both strategy
functions call the shared far Pascal ELLEN_TARGET_SET at C44F/C5B8, passing byte
pid through a word carrier. Accepted movement, hittest and randring helpers
retain their ABIs; PLAYER_BOMB remains existing carrier code.

The 128-byte player record assertions bind positions 0/2, hit flag 4, CPU strategy 16h,
gauge 18h, safety 6Eh and frame 74h. Coordinates and scan/retry state are signed;
frame/gauge and attempt comparisons are unsigned. Retain the otherwise-unused
random remainder, state restoration after collision and the observed retry branch.
The initial hittest arguments32,48,64,80 are hitbox sizes, not radii.

Existing storage remains carrier-owned: dodge rows DS067E..0756 (216 bytes,
9-word stride, semantic outer bound deliberately unspecified), three retry rows
0756..078C (54 bytes), near table pointer 38EA and shared Ellen target 3ECE/3ED0.
No new DATA/BSS, literal lookup-table recreation or target-byte array is introduced.

## Natural compiler findings

Native-v01 failed on an include diamond: stuff.hpp and move.hpp both reached
unguarded speed/input definitions. Two explicit compatibility guards preserve
the original first definitions under the intended packing. The validator permits
the guarded form only for those two reviewed paths and still rejects extra
content, wrong targets and guard mismatches. The fresh unchanged-default regression below covers existing accepted producers;
the CPU-only native probe does not establish new CPU cold/runtime acceptance.

Native-v02 emitted 1075 bytes. Two signed-byte comparisons shortened by 3 bytes
each; a ternary hit-test argument added 3, followed by an extra natural zero.
Native-v03 uses the existing project int8_t signed8 type and explicit if/else
calls. Accepted plain-char Subpixel8 code already proves MOV AL/CBW under the
same configuration; a zero-storage signedness assertion protects that assumption.
All 1077 native bytes resolve exactly through 64 real symbolic fixups. Both tables
and the sole C535 zero are naturally emitted. No barriers, padding, fake ABI,
volatile forcing or object rewriting is used.

## Retained combined link, separate from historical Yumemi v01

The corrected retained run reused CPU-v03 and Yumemi-v02 objects, assembled the
honest prefix and root carriers once each, then linked once. All three exits 0;
no timeout/surviving child, input drift or worktree change. This is not cold proof
of the newly localized maintained paths.

Passing observations:
- All 81 authored extents / 386 complete functions: target raw bytes and extent-local
  literal relocation order, including all producer ranges.
- The separate new 34-site union matches CPU 2, bomb 20, charge 12 in target order.
- Full outside payload equals the accepted generated baseline; shared storage,
  aliases and generated-baseline allocation/entry/overlay header fields agree.
- All 30 other retained game outputs remain unchanged; they were not freshly built.

Two strict gates remain failed:
1. Outside 1519 literal relocation pairs retain their multiset but 432 positions
   differ. The uncredited prefix 10 moves filtered indices 818..827 to 452..461,
   with 5 internal changes; suffix 89 has 56. The other 1420 retain literal order.
   No sorting, masking, added exclusion, FIXUPP framing edits or ordering padding
   is allowed to turn this into a pass.
2. Accepted score_add's containing root MAP row expects 096E:29F8/15FC; the honest
   suffix is 30C5/0F2F. Actual score_add stays 096E:3ED0 (load D5B0), and all 88 bytes
   remain original-exact. This is a stale carrier-metadata expectation, not a
   misplaced function, but the gate is **not waived** or changed in the accepted manifest.

The historical Yumemi v01 manifest, evidence and original charge-before-bomb
failure remain untouched. The new combined recipe records the later tested
CPU-before-bomb-before-charge order separately. Full strict match, maintained-path
cold replay, runtime and complete Oracle acceptance remain open.

## Translation-unit ordering obstruction (2026-10-19)

Read-only OMF/MAP/MZ analysis explains why another object-order permutation
cannot repair the retained candidate. Each module's relocation entries form one
contiguous run in both images. Baseline root has 532 sites at 452..983; its
prefix 10 lies inside that run at 818..827. Excluding CPU/Yumemi 34 leaves 366
root sites before the prefix and 122 after it. Moving the prefix to p_cpre would
require **main < p_cpre < main** to preserve outside order. Physical BYTE PUBLIC
PLAYER_M_TEXT placement also requires p_cpre < p_cpu < main. These constraints
are contradictory for the current partition and observed TLINK traversal, not a
claim about all future producers or undocumented linker modes.

The internal changes already exist in native OMF. Extraction changes two
PALETTE_SHOW and four SUPER_PUT fixups from same-module _TEXT targets to EXTDEFs,
and the prefix's literal FIXUPP list differs at five positions. These observations
do not prove that the six symbol changes alone caused the scheduling difference.
Removing prefix+CPU also changes native root LEDATA sizes from
1007/1003/1007/1007/1007/597 to 1007/1006/992/882; the unchanged suffix's 56 changes
are present in FIXUPP traversal. TASM's internal ordering rule remains unproved.
TLINK's surviving far-fixup traversal matches the literal MZ lists; no relocation
sorting, record calibration or declaration trick is justified.

Keeping baseline framing in one root TU is insufficient too: C452 belongs to
LEDATA record 930 (C0D8..C4C7), before C5BB in record 932 (C4C7..C8B2), whereas
original CPU order requires **C5BB before C452**. A fixed-framing TC4 -S splice
cannot pass that gate; no native run was made merely to confirm the contradiction.

The next live question is genuine source recovery of the full trailing
C7A5..D6D4 contribution (3,887 bytes), retaining the authentic prefix in root.
The tail has 27 explicit procedures plus the existing 88-byte score_add include;
score_add receives no new credit. Natural tail TUs could follow CPU, with the
original selected union CPU 2 → bomb 20 → tail 89 → charge 12. This removes the
current middle-insertion cycle but does not prove new code or remaining-root
scheduling. Complete boundary/ABI/storage review comes first; copied tail assembly
cannot widen authored exclusions. All current acceptance gates remain unchanged.

The separate candidate-only score_add MAP prototype under
`.analysis/gpt-dots-score-carrier-metadata-v01` explains 92 retained MAP checks;
it remains uninstalled and cannot repair outside order.

### Reproduce this bounded diagnosis

    python3 -B scripts/review_th03_cpu_link_order.py

The read-only script validates all 13 historical input hashes before analysis
and again before reporting. Defaults are checkout-relative, independent of CWD.
`--baseline-root`, `--candidate-root` and `--target` can locate the same retained
files elsewhere; their hashes remain mandatory. The script prints JSON only,
invokes no native tools and changes no acceptance comparator. Missing private
inputs produce a concise failure. A public clone alone does not contain the
retained objects, MAPs, response files, executables or original target.

The readable derivation is
`.analysis/gpt-dots-player-cpu-order-mechanism-v03/DERIVATION.md`.
The full retained report is
`.analysis/gpt-dots-player-cpu-order-mechanism-v03/report.json`,
SHA256 432ecc27b9bbff4839fdf658cf6d98c87e00a68addd804b9939941b9dde714ff.
Independent module-cycle evidence: repository-command:b80757cfb0b549fdb10bf1f78ba4b6bf.

## Compact reproducible integration recipe

`config/th03_main_cpu_yumemi_candidate.toml` is a separate additive diagnostic
candidate. Existing replay machinery applies single-hit source edits and builds:

    h_stitch ... p_cpre p_cpu bm_yume cs_yume main ... player_m

The accepted default manifest is unchanged. p_cpre contains four complete copied
reference assembly functions at C0D8..C370 (664 bytes), explicitly **zero authored
credit**. `cpu_prefix_types.inc` copies only the original declaration spans before
_PLAYCHAR_SPEEDS and _p1/_p2/_players storage instances. Both support sources use
explicit compatibility forwarding includes and repository LF line endings; their
instructions/declaration tokens remain unchanged (empty trailing declaration lines
are omitted). No bulky generated root is committed.
The candidate's CPU edits reproduce the retained root byte-for-byte.

The prefix owns no binary-wide marker: BINARY remains in root, where ReC98.inc
publishes absolute _address_0. The first retained link's duplicate-symbol failure
is preserved; the legitimate one-line ownership fix precedes the corrected run.

For a future authorized cold diagnostic (known MAP gate still fails):

    python3 scripts/replay_th03_main_exact_units.py --candidate-manifest config/th03_main_cpu_yumemi_candidate.toml --run-id UNIQUE_CPU_REVIEW

Do not mistake an unchanged-default regression for this candidate's acceptance.
The full outside-baseline comparator remains an additional required retained/cold
review gate. Reference prefix raw bytes match target; suffix retains 18 pre-existing
encoding differences. Target prefix/suffix relocation order also differs from
baseline, so outside preservation must use the accepted baseline, not target.

## Durable private proof pins

All target evidence uses MAIN SHA256
f41fde47ea36bf4d985ff9127b67fe93d5ecb58cc36e7cffab86959db7f2ce6b.
Reference revision is b6ba5b0a529edbb31efdf8c0e939263804f8ee47, corroboration only.
Independent pristine-dump provenance remains open.

| Proof | Retained path | SHA256 |
| --- | --- | --- |
| Target boundaries/storage | .analysis/gpt-dots-player-cpu-source-v01/audit.json | b26e64b6721699768965e616d0e0da4a3029f8db84057be5c640e31693907c7b |
| Native-v03 receipt | .analysis/gpt-dots-player-cpu-source-v03/probe-v01/compile-first-v01/receipt.json | b447680b9448c597f2f3ac00ab7b48ba88e278fd96390cdacc12335a79c05c21 |
| Native-v03 complete review | .analysis/gpt-dots-player-cpu-source-v03/NATIVE_OBJECT_REVIEW.md | 052cf15b281a4316416d3ab6216360fab0a9645f20d6322239a2086f5688c052 |
| Failed duplicate-symbol receipt | .analysis/gpt-dots-player-cpu-placement-v01/relink-proposal-v02/run-first-v01/receipt.json | a7baac9d9bd6650735b87863349a59a940806040281ad37212fb62e35f3468d2 |
| Corrected retained receipt | .analysis/gpt-dots-player-cpu-placement-v02/relink-proposal-v01/run-first-v01/receipt.json | 38d4e3dab32c1d98f10c45afbad0fa65a20d89aebb77016324d4263852069899 |
| Independent retained review | .analysis/gpt-dots-player-cpu-placement-v02/RETAINED_LINK_REVIEW.md | c9b13e26f2b4188d54166e676ba725a4f35da32a87e996ef448e65a32af5c317 |

Native CPU object 26bcae741b3d4579cd10e14209e46f6de10e214e15f474f5e182d2c59fa1a7d6;
corrected MAIN 9477aae080a2334ede97d43cf52a102780703018adf454b51c4bf43065082a77.
Large reports/objects/targets remain ignored; ledgers record only the bounded CPU
source addition. Post-install full CI passed 783 tests with all 725 inputs
unchanged (13:12:31..13:16:46 UTC); see
`.analysis/gpt-dots-player-cpu-milestone-v01/full-ci/ci.json` and `ci.log`.

The unchanged-default attempt `gpt-dots-cpu-guards-default-cold-v01` started
13:21:07 UTC and exited at 13:25:06 after the first build exceeded its internal
180-second timeout. Research/286 work was still advancing; all 31 fresh game
outputs already matched the accepted first round. This is partial output evidence,
not a completed build or two-cold regression. No round2 or canonical receipt was
produced. Source guards stayed equal, cleanup was clear and the claim was released.
The supervisor completion record is
`.analysis/th03-main-serial/runs/gpt-dots-cpu-guards-default-cold-v01/completion-evidence.json`,
SHA256 58ceeab6047bd0dbba9d1b47740085dfc71d8cd0497667345497bb1f62ab06e2.
Independent partial-output observation: repository-command:1732d9054f2349218357a1b4e1f88308.
The timeout run is preserved and has no regression-pass verdict.
The separate fresh recovery below closes only the unchanged-default regression.
These documentation-only result notes were recorded after the successful CI run.


## Fresh unchanged-default regression after guard installation

At clean HEAD `c58e2b2fe53d64b990ca04abf41e5502ecc1bdae`,
`gpt-dots-cpu-guards-default-cold-v02` ran 13:54:13–14:01:31 UTC on
2026-10-19. Both genuinely cold rounds passed the original replay, with unchanged
source guards and clear cleanup/claim release. The reviewed scheduling adapter
allowed only those two exact cold builds 300 seconds each; other calls retained
180 seconds and outer supervision 900 seconds, one CPU/nice>=10/Tup1. The complete
game/research build graph and original replay SHA5f48 remained unchanged.
Prelaunch full CI passed 798 tests with all 725 input hashes/modes stable.

The supplemental default/default verifier passed at 14:01:47 UTC. Its four
fresh/historical round comparisons cover all 31 game outputs (20 declared plus
11 auxiliary), complete MAIN raw file/payload/header/overlay and literal ordered
MZ relocations, all 43 ordered MAP inventories, and 254 DATA/BSS/STACK allocation
rows including zero-size rows. Both fresh rounds also retain the original target
scope, object, behavior, source/tool and determinism gates. Failed-v01 proof trees
remain byte/mode/file-set guarded.

| Fresh proof | Retained path | SHA256 |
| --- | --- | --- |
| Two-cold canonical receipt | .analysis/th03-main-exact/gpt-dots-cpu-guards-default-cold-v02/receipt.json | 732ac39217a7dd24224412ad22d7f900ba91985b5c2fe8c71612264bfab39af2 |
| Supervisor completion | .analysis/th03-main-serial/runs/gpt-dots-cpu-guards-default-cold-v02/completion-evidence.json | 67233db11f65c5207a8b58f82ba36635d114264c299f300479258903f47dea98 |
| Strict supplemental report | .analysis/gpt-dots-player-cpu-milestone-v01/postrun-default-verifier-v01/report-first-v01.json | 1ad80ee5906c7bda0abc216b3cc9650320d2604e83dab9569c92a2ffe6fa1aa3 |

The frozen launch plan is
`.analysis/gpt-dots-player-cpu-milestone-v01/default-cold-plan-v02/launch-plan-v01.json`
(SHA256 ef8701765a93bda2e183a6a0f8c2455fb3189501a0e965cd9359e2921b2dd319).
Replayable supplemental invocation:

    PYTHONPATH="$PWD/.venv/lib/python3.12/site-packages" python3 -B .analysis/gpt-dots-player-cpu-milestone-v01/postrun-default-verifier-v01/launch.py --report .analysis/NEW_UNUSED_REPORT.json

That verifier intentionally requires the frozen clean HEAD/source identities;
later documentation commits do not retroactively rebind this completed proof.
The two header guards therefore preserve the accepted default **78 extents /
371 functions / 59,624 bytes**. CPU and Yumemi remain source-present only;
combined outside literal-order/MAP blockers, maintained candidate cold/runtime
proof, original provenance and whole-game acceptance remain open.
