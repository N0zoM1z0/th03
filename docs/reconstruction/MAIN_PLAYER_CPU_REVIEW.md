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
content, wrong targets and guard mismatches. Regression of existing producers
is required; the CPU-only native probe is not sufficient evidence for all users.

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
The timeout run is preserved; a fresh reviewed operational recovery remains open.
No regression pass, new exact acceptance or CPU runtime proof is inferred.
These documentation-only result notes were recorded after the successful CI run.
