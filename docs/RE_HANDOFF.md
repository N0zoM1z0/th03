# TH03 — active handoff (2026-11-08)

Follow the highest-priority workflow in [AGENTS.md](../AGENTS.md). This
page is the current checkout handoff; historical source/compiler chronology
is preserved in [the after927 archive](RE_HANDOFF_ARCHIVE_AFTER927.md)
and the focused experiment reviews linked below.

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

**Latest integration: af1024e**

Two independent original Turbo C++ 4.02 rounds rebuilt these twelve complete
physical owners together:

- Nine major BOSS owners: Mima, Reimu, Yumemi, Ellen, Kana, Kotohime,
  Marisa, Rikako and Chiyuri.
- Collision/effect owners: Hitbox, HitCircle and the explosion chain.

Both normal MAIN links match the original Japanese loaded image and all
ordered MZ relocations. The other 87 original game objects and Borland CRT
were reused; no full cold replay was run.

| Measure | af1024e result |
| --- | ---: |
| Complete physical owners rebuilt | 12 |
| CODE | 18,792 bytes |
| Ordered OMF FIXUPPs | 2,546 |
| PUBLICs | 91 |
| Japanese MAIN loaded image | 124,642 bytes |
| Ordered MZ relocations | 1,553 |
| Independent original compiler rounds | 2 |

Protected report:
.analysis/work/exatt-layout-af1024e/report.json

Report SHA-256:
a37060b2d80d066ab2058774a606f522ecf6f43d726e0bc2983fdbda2416cc7c

The report's twelve source hashes were checked against all twelve current
maintained files. The complete normal link is strong scoped native evidence;
it is not whole-game source ownership or canonical Factory packed-file
acceptance.

### Current component proofs

| Stage | Complete owner(s) | CODE | Ordered FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| af1024d | Mima, Kotohime, Chiyuri, HitCircle | 6,861 | 950 | 35 |
| af1024c | Kotohime | 1,840 | 262 | 11 |
| af1024b | HitCircle | 445 | 30 | 4 |
| af1021b | Mima | 1,922 | 277 | 9 |
| af1021a | Chiyuri | 2,654 | 381 | 11 |

All five component reports are source-current. The af1024e report is the
current simultaneous integration for the full twelve-owner set.

### Subsequent scoped BOSS continuation

The shared BOSS pattern selector's `while(1)`/`break` rejection loop is now a
natural `do-while` in `src/main/boss/shared.cpp`. Stage af1025a rebuilt the
complete `ba_srest` object in two independent original TC4 rounds: 601 CODE
bytes, 84 ordered native fields and seven PUBLICs, with both normal MAIN links
and ordered relocations exact. Its current-source review passed. See
[the focused after1025 review](MAIN_BOSS_PATTERN_REJECTION_DO_WHILE_AFTER1025_REVIEW.md).

The larger Kotohime update controller also now uses a direct intro-completion
guard in `gba_boss_update_kotohime()` rather than a nested `if/else`. Stage
af1025c rebuilt the complete `ba_koto` object in two independent original TC4
rounds: 1,840 CODE bytes, 262 ordered native fields and eleven PUBLICs, with
both normal MAIN links and ordered relocations exact. The attempted shared
`level / 2` local changed CODE and was reverted. See
[the focused Kotohime update review](MAIN_KOTOHIME_UPDATE_INTRO_GUARD_AFTER1025_REVIEW.md).

The same large Kotohime controller now exits immediately when the current PID
is not the launched boss PID, replacing the outer `if(equal) ... else return`
with a direct guard. Stage af1026a independently rebuilt the complete 1,840-
byte `ba_koto` owner in two original TC4 rounds, with 262 ordered native fields,
eleven PUBLICs and the complete Japanese MAIN image/relocations exact. See the
[after1026 Kotohime controller review](MAIN_KOTOHIME_UPDATE_INTRO_GUARD_AFTER1025_REVIEW.md).

Mima's orbit leaf now spells its inclusive finish test as the constant-first
`MIMA_ORBIT_FINISH_FRAME <= boss_frame`. Stage af1026d rebuilt the complete
`ba_mima` owner in two original TC4 rounds: 1,922 CODE bytes, 277 ordered native
fields and nine PUBLICs, with the full Japanese MAIN image and relocations
exact. See the [after1026 Mima orbit review](MAIN_MIMA_ORBIT_FINISH_COMPARE_AFTER1026_REVIEW.md).

Mima's 305-byte `mima_render_main()` now uses independent early-return guards
for hit, Particle, Expand, Flash and Trail phases. The shared Particle/Trail
label and byte-frame postincrement remain intact. Stage af1029g rebuilt the
complete `ba_mima` owner in two original TC4 rounds: 1,922 CODE bytes, 277
ordered native fields and nine PUBLICs, with the complete Japanese MAIN image
and relocations exact. See the
[after1029 Mima renderer review](MAIN_MIMA_RENDER_MAIN_INDEPENDENT_PHASE_GUARDS_AFTER1029_REVIEW.md).

The 298-byte Mima update controller now spells the INTRO completion path as a
positive equality branch with an explicit `else return`. Stage af1030f rebuilt
the complete `ba_mima` owner in two original TC4 rounds: 1,922 CODE bytes,
277 ordered native fields and nine PUBLICs, with the full Japanese MAIN image
and relocations exact. See the
[after1030 Mima INTRO branch review](MAIN_MIMA_UPDATE_INTRO_SUCCESS_BRANCH_AFTER1030_REVIEW.md).

A `switch(boss_render_mode)` alternative with the same cases and Trail goto
was rejected at af1029i because it changed complete `ba_mima` CODE. Keep the
independent guards; see the
[after1029 Mima switch experiment](MAIN_MIMA_RENDER_SWITCH_DISPATCH_AFTER1029_REVIEW.md).

Mima's Trail leaf now uses the same constant-first form for its inclusive end
frame, after the byte-narrowed modulo phases and optional shot. Stage af1026g
rebuilt the complete `ba_mima` owner in two original TC4 rounds with all 1,922
CODE bytes, 277 ordered native fields, nine PUBLICs and the complete Japanese
MAIN image/relocations exact. See the
[after1026 Mima Trail review](MAIN_MIMA_TRAIL_FINISH_COMPARE_AFTER1026_REVIEW.md).

Two natural alternatives for the register-sensitive Mima split-render distance
were also tested and reverted: parameter-qualified `register int distance`
(af1028a) moved the parameter into DI and displaced the left-coordinate
register; an ordinary `int split_distance` local (af1028b) changed complete
CODE as well. Keep the existing SI distance local and DI left local. See the
[after1028 Mima split allocation review](MAIN_MIMA_RENDER_SPLIT_REGISTER_ALLOCATION_AFTER1028_REVIEW.md).

Chiyuri's intro controller now expresses its two mutually exclusive frame
phases as an `if`/`else if` chain, retaining the four cross-effect spawn order
and the common update tail. Stage af1026h rebuilt the complete `ba_chiyu`
owner in two original TC4 rounds: 2,654 CODE bytes, 381 ordered native fields
and eleven PUBLICs, with the full Japanese MAIN image and relocations exact.
See the [after1026 Chiyuri intro review](MAIN_CHIYURI_INTRO_EXCLUSIVE_PHASES_AFTER1026_REVIEW.md).

The 613-byte Chiyuri update controller's INTRO case now puts the default
animation/return path in an explicit final `else`, completing the mutually
exclusive done/cross/default frame chain. Stage af1027h rebuilt the complete
`ba_chiyu` owner in two original TC4 rounds: 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLICs, with the full Japanese MAIN image and
relocations exact. See the
[after1027 Chiyuri intro-default review](MAIN_CHIYURI_INTRO_DEFAULT_ELSE_AFTER1027_REVIEW.md).

The same update controller now declares its SELECT center-array index as
`register unsigned char random_i`. Stage af1028f rebuilt the complete
`ba_chiyu` owner in two original TC4 rounds: 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLICs, with the full Japanese MAIN image and
relocations exact. See the
[after1028 Chiyuri selector review](MAIN_CHIYURI_UPDATE_REGISTER_SELECTOR_AFTER1028_REVIEW.md).

The same 613-byte controller now spells its four-frame render cadence as an
unsigned-clock low-bit test instead of `% 4 == 0`. Stage af1030c rebuilt the
complete `ba_chiyu` owner in two original TC4 rounds: 2,654 CODE bytes, 381
ordered native fields and eleven PUBLICs, with the full Japanese MAIN image
and relocations exact. See the
[after1030 Chiyuri cadence review](MAIN_CHIYURI_UPDATE_RENDER_CADENCE_MASK_AFTER1030_REVIEW.md).

The same controller now uses `if(boss_render_mode)` for its zero-valued normal
mode test while retaining the postfix byte decrement. Stage af1030d rebuilt
the complete `ba_chiyu` owner in two original TC4 rounds: 2,654 CODE bytes,
381 ordered native fields and eleven PUBLICs, with the full Japanese MAIN
image and relocations exact. See the
[after1030 render-mode guard review](MAIN_CHIYURI_UPDATE_NONZERO_RENDER_MODE_AFTER1030_REVIEW.md).

The palette countdown's two byte-zero comparisons are now direct truth tests,
while retaining the nested checks and postfix phase decrement. Stage af1030e
rebuilt the complete `ba_chiyu` owner in two original TC4 rounds: 2,654 CODE
bytes, 381 ordered native fields and eleven PUBLICs, with the full Japanese
MAIN image and relocations exact. See the
[after1030 phase truth-test review](MAIN_CHIYURI_UPDATE_PHASE_TRUTH_TESTS_AFTER1030_REVIEW.md).

The 528-byte Chiyuri fan generator now declares its shared four-pass loop index
as `register int`, matching the original SI allocation. Stage af1027a rebuilt
the complete `ba_chiyu` owner in two original TC4 rounds: 2,654 CODE bytes,
381 ordered native fields and eleven PUBLICs, with the full Japanese MAIN
image and relocations exact. A horizontal two-pass factoring trial at af1027b
changed complete CODE and was reverted. See the
[after1027 Chiyuri fan review](MAIN_CHIYURI_FAN_REGISTER_INDEX_AFTER1027_REVIEW.md).

The same four fan loops now use postfix `i++` in their natural for-headers.
Stage af1029j rebuilt the complete `ba_chiyu` owner in two original TC4
rounds: 2,654 CODE bytes, 381 ordered native fields and eleven PUBLICs, with
the full Japanese MAIN image and relocations exact. See the
[after1029 Chiyuri fan-loop review](MAIN_CHIYURI_FAN_POSTINCREMENT_LOOPS_AFTER1029_REVIEW.md).

The 352-byte Cardinal leaf now scopes its complete attack body under the
positive `(boss_frame % chiyuri_cardinal_interval) == 1` firing condition
instead of returning early on the inverse. Stage af1030h rebuilt the complete
`ba_chiyu` owner in two original TC4 rounds: 2,654 CODE bytes, 381 ordered
native fields and eleven PUBLICs, with the full Japanese MAIN image and
relocations exact. See the
[after1030 Cardinal cadence review](MAIN_CHIYURI_CARDINAL_POSITIVE_CADENCE_GUARD_AFTER1030_REVIEW.md).

The 208-byte Rings leaf now uses the same positive cadence-scope form. Stage
af1030i rebuilt the complete `ba_chiyu` owner in two original TC4 rounds:
2,654 CODE bytes, 381 ordered native fields and eleven PUBLICs, with the full
Japanese MAIN image and relocations exact. See the
[after1030 Rings cadence review](MAIN_CHIYURI_RINGS_POSITIVE_CADENCE_GUARD_AFTER1030_REVIEW.md).

The 115-byte Trail leaf now scopes its one-time release sequence under the
positive fire-frame condition, while its periodic warning bombs remain
independent and earlier. Stage af1030j rebuilt the complete `ba_chiyu` owner
in two original TC4 rounds: 2,654 CODE bytes, 381 ordered native fields and
eleven PUBLICs, with the full Japanese MAIN image and relocations exact. See
the [after1030 Trail fire review](MAIN_CHIYURI_TRAIL_POSITIVE_FIRE_GUARD_AFTER1030_REVIEW.md).

Kotohime's radial burst now declares the outer center index and inner bullet
index as `register int`, matching the original DI/SI loop-index allocation.
Stage af1026i rebuilt the complete `ba_koto` owner in two original TC4 rounds:
1,840 CODE bytes, 262 ordered native fields and eleven PUBLICs, with the full
Japanese MAIN image and relocations exact. See the
[after1026 Kotohime radial-index review](MAIN_KOTOHIME_RADIAL_REGISTER_INDICES_AFTER1026_REVIEW.md).

The same radial function now declares `center_i` before `bullet_i`, matching
the natural outer-to-inner traversal order while retaining DI/SI allocation.
Stage af1029l rebuilt the complete `ba_koto` owner in two original TC4 rounds:
1,840 CODE bytes, 262 ordered native fields and eleven PUBLICs, with the full
Japanese MAIN image and relocations exact. See the
[after1029 Kotohime index-order review](MAIN_KOTOHIME_RADIAL_INDEX_DECLARATION_ORDER_AFTER1029_REVIEW.md).

The same radial review records four rejected complete-owner experiments:
af1026b/c (early-return and inverted expansion/release branches) and
af1026e/f (local `PlayfieldPoint` aggregate/field copies). All changed the
complete `ba_koto` CODE and were reverted. Do not repeat those forms without a
new disassembly-led hypothesis; the detailed results are in the
[after1026 radial-index review](MAIN_KOTOHIME_RADIAL_REGISTER_INDICES_AFTER1026_REVIEW.md).

The HitCircle age walk also now uses a direct positive `p->age` guard in
`hitcircles_update()` instead of a zero-age `continue`. Stage af1025d rebuilt
the complete `hitcirc` object in two independent original TC4 rounds: 445 CODE
bytes, 30 ordered native fields and four PUBLICs, with both normal MAIN links
and ordered relocations exact. See
[the focused HitCircle update review](MAIN_HITCIRCLE_UPDATE_NESTED_GUARD_AFTER1025_REVIEW.md).

The same 38-byte HitCircle update leaf now declares both its record cursor
and signed counter as register locals (`register HitCircle near* p` and
`register int i`), matching the original SI/AX allocations. Stages af1027f and
af1027g each rebuilt the complete `hitcirc` owner in two original TC4 rounds:
445 CODE bytes, 30 ordered native fields and four PUBLICs, with the full
Japanese MAIN image and relocations exact. Three unsigned-local rewrites of
the inline `HitCircle::cel()` leaf (af1027c/d/e) changed CODE and were
reverted. See the
[after1027 HitCircle register review](MAIN_HITCIRCLE_UPDATE_REGISTER_POINTER_AFTER1027_REVIEW.md).

The 236-byte HitCircle renderer now likewise declares its SI record cursor
and DI enemy-slot counter as register locals. Stage af1028c rebuilt the
complete `hitcirc` owner in two original TC4 rounds: 445 CODE bytes, 30
ordered native fields and four PUBLICs, with the full Japanese MAIN image and
relocations exact. See the
[after1028 HitCircle renderer review](MAIN_HITCIRCLE_RENDER_REGISTER_LOCALS_AFTER1028_REVIEW.md).

Further `HitCircle::cel()` rewrites using signed/unsigned locals, moving the
calculation into the renderer, or replacing unsigned division with a shift
were tested in af1029a-d/e/f/h and all changed complete CODE. The target's
SI/DI/BX allocation still requires the existing `_BX` source form; see the
[after1029 HitCircle cel allocation review](MAIN_HITCIRCLE_CEL_REGISTER_ALLOCATION_AFTER1029_REVIEW.md).

The same renderer now uses a positive `p->age` guard for each of the twelve
enemy slots instead of a zero-age `continue`. Stage af1028d again rebuilt the
complete `hitcirc` owner in two original TC4 rounds with all 445 CODE bytes,
30 ordered native fields, four PUBLICs and the full Japanese MAIN image and
relocations exact. See the
[after1028 HitCircle active-guard review](MAIN_HITCIRCLE_RENDER_ACTIVE_GUARD_AFTER1028_REVIEW.md).


Current report locations and SHA-256 identities:

- af1024e: .analysis/work/exatt-layout-af1024e/report.json
  (a37060b2d80d066ab2058774a606f522ecf6f43d726e0bc2983fdbda2416cc7c)
- af1024d: .analysis/work/exatt-layout-af1024d/report.json
  (85a09bd39ea4f01f7f0a730951e223d50ae9b65e79b1917faec62f2b96532b64)
- af1024c: .analysis/work/exatt-layout-af1024c/report.json
  (6f0ea0a0ca95731e8ebdf90a6b4c6c7f601288ee4d902faad3713a363fadde82)
- af1024b: .analysis/work/exatt-layout-af1024b/report.json
  (62b731c48a1910f261b2b16e00baf2186fc6557b8002de3029c3c3ce0ad8d750)
- af1021b: .analysis/work/exatt-layout-af1021b/report.json
  (4c0d0961e91bee8e81c2125b9ce5c9bea18198a46bfecdbb3515924883b3e16c)
- af1021a: .analysis/work/exatt-layout-af1021a/report.json
  (2b9cd91524f458397fd628b52afacd756fed2747a94e9eb80c3a05300a110f41)

### Corrected historical stage bindings

- af927a is **not** a current whole-stage source review: its ba_chiyu
  source hash differs from maintained src/main/boss/chiyuri.cpp.
  Its entry, effects, cs_chiyu and b_chiyu source hashes still match, but
  the stage-wide reviewer correctly rejects the stale BOSS member.
- af935a is historical for ba_maris; the current Marisa owner is included
  in af1024e.
- af1021d and earlier twelve-owner integrations are historical snapshots
  superseded by af1024e. Their original reports and review notes remain
  useful history; do not describe them as current source bindings.

Do not use a composite historical stage as a current proof merely because
most of its source hashes still match. The current reviewer checks every
owner in the stage.

## Latest source recovery and next work

The latest source work includes the shared BOSS pattern selector's natural
rejection loop (af1025a), two large Kotohime update-controller guards
(af1025c/af1026a), Mima's orbit/Trail finish phases (af1026d/af1026g) and independent render
phase guards and update INTRO branch (af1029g/af1030f),
Chiyuri's intro phase chain/default path (af1026h/af1027h), fan-loop SI index/postfix increments and Cardinal/Rings positive cadence
scopes plus Trail positive fire guard (af1027a/af1029j/af1030h/af1030i/af1030j), and update
SELECT register byte/render cadence/phase truth tests (af1028f/af1030c/af1030d/af1030e), Kotohime's
explicit radial register indices/order (af1026i/af1029l), and
HitCircle's age-update/render register locals and active guard
(af1025d/af1027f/af1027g/af1028c/af1028d). The three current
BOSS owners were then rebuilt together at af1026j: 6,416 CODE bytes, 920
ordered native fields and 31 PUBLICs, with both original TC4 rounds and the
complete Japanese MAIN image/relocations exact. See the
[after1026 three-owner integration review](MAIN_BOSS_THREE_OWNER_INTEGRATION_AFTER1026_REVIEW.md).

The latest Chiyuri and HitCircle source changes were then rebuilt together at
af1027i: two complete owners, 3,099 CODE bytes, 411 ordered native fields and
15 PUBLICs, with both original TC4 rounds and the complete Japanese MAIN
image/relocations exact. See the
[after1027 Chiyuri/HitCircle integration review](MAIN_CHIYURI_HITCIRCLE_INTEGRATION_AFTER1027_REVIEW.md).

After the additional HitCircle render and Chiyuri SELECT-local changes, the
same two owners were rebuilt together again at af1028g: 3,099 CODE bytes, 411
ordered native fields and 15 PUBLICs, with both original TC4 rounds and the
complete Japanese MAIN image/relocations exact. See the
[after1028 Chiyuri/HitCircle integration review](MAIN_CHIYURI_HITCIRCLE_INTEGRATION_AFTER1028_REVIEW.md).

After the Mima render-phase and Chiyuri fan-loop changes, both complete BOSS
owners were rebuilt together at af1029k: 4,576 CODE bytes, 658 ordered native
fields and 20 PUBLICs, with two original TC4 rounds and the complete Japanese
MAIN image/relocations exact. See the
[after1029 Mima/Chiyuri integration review](MAIN_BOSS_MIMA_CHIYURI_INTEGRATION_AFTER1029_REVIEW.md).

After the Kotohime radial-index declaration-order change, all three BOSS
owners were rebuilt together at af1029m: 6,416 CODE bytes, 920 ordered native
fields and 31 PUBLICs, with two original TC4 rounds and the complete Japanese
MAIN image/relocations exact. See the
[after1029 three-owner integration review](MAIN_BOSS_THREE_OWNER_INTEGRATION_AFTER1029_REVIEW.md).

After the Mima INTRO and Chiyuri update/leaf changes, the two complete owners
were rebuilt together at af1030k: 4,576 CODE bytes, 658 ordered native fields
and 20 PUBLICs, with two original TC4 rounds and the complete Japanese MAIN
image/relocations exact. See the
[after1030 Mima/Chiyuri integration review](MAIN_BOSS_MIMA_CHIYURI_INTEGRATION_AFTER1030_REVIEW.md).

See
[the after1026 Kotohime radial-index review](MAIN_KOTOHIME_RADIAL_REGISTER_INDICES_AFTER1026_REVIEW.md),
[the after1026 Chiyuri intro review](MAIN_CHIYURI_INTRO_EXCLUSIVE_PHASES_AFTER1026_REVIEW.md),
[the after1026 Mima Trail review](MAIN_MIMA_TRAIL_FINISH_COMPARE_AFTER1026_REVIEW.md),
[the after1026 Mima orbit review](MAIN_MIMA_ORBIT_FINISH_COMPARE_AFTER1026_REVIEW.md),
[the after1025 HitCircle update review](MAIN_HITCIRCLE_UPDATE_NESTED_GUARD_AFTER1025_REVIEW.md),
[the after1025 Kotohime update review](MAIN_KOTOHIME_UPDATE_INTRO_GUARD_AFTER1025_REVIEW.md),
[the after1025 BOSS review](MAIN_BOSS_PATTERN_REJECTION_DO_WHILE_AFTER1025_REVIEW.md),
[the after1024 source review](MAIN_KOTOHIME_RADIAL_AND_HITCIRCLE_ENUMS_AFTER1024_REVIEW.md)
and [the after1021 BOSS review](MAIN_BOSS_NATURAL_PHASE_TESTS_AFTER1021_REVIEW.md).

- **Kotohime Radial Burst:** the complete nested generator now has one
  release-branch scratch scope for x, y, center_angle, bullet_i and
  center_i. Both natural loops use postfix index increments and
  constant-first count comparisons. The original signed 16-bit
  multiply/divide order, byte-angle truncation, polar calls and bullet
  emission order remain. Replacing either loop bound with != changed CODE.
- **HitCircle:** layout/animation and capacity constants are grouped into
  named enums; the enemy ring-wrap guard uses the named count first.
  Preserve the BX/AX cel sequence and its three final BX additions.
  Replacing those additions with a multiplication changed complete CODE.
- **Mima:** the hit-render path chains into the Particle renderer with
  else-if; named render-mode comparisons are constant-first. Keep the
  original Trail-to-Particle label/goto and nested Particle thresholds.
- **Chiyuri:** Cardinal, ring, fan and trail clocks have natural named
  thresholds and state tests. Preserve compiler-sensitive operand order
  and the original bullet-call ordering.

Recommended next targets:

1. Continue the HitCircle::cel() leaf. Explore natural C++ forms without
   disturbing the observed BX/AX register sequence. The af1025e signed
   `register int` and af1025f ordinary signed `int` sequential-local variants
   both changed the complete `hitcirc` CODE and were reverted; see the
   [after1025 HitCircle review](MAIN_HITCIRCLE_UPDATE_NESTED_GUARD_AFTER1025_REVIEW.md).
2. Continue Kotohime Radial Burst's actual center/angle/speed arithmetic and
   variable lifetimes, not just more cosmetic predicate rewrites.
3. Continue Mima's shared Trail/Particle renderer and Chiyuri's four fan
   passes, preserving draw and bullet ordering.
4. Pursue genuinely unowned original source and larger BOSS/engine functions
   alongside the small leaves. Do not count refactors as new source ownership.

## Current product status and limits

The latest session-start preflight (2026-11-08) reported:

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
routine deletion route. A native proof purge requires a new full dependency
audit and explicit one-time allowlist.

## Minimal commands

Read-only start and current MAIN review:

    git status -sb
    .venv/bin/python scripts/preflight.py
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1024e

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
- [Current twelve-owner integration and radial/HitCircle recovery](MAIN_KOTOHIME_RADIAL_AND_HITCIRCLE_ENUMS_AFTER1024_REVIEW.md)
- [Earlier Mima/Chiyuri/Kotohime phase and renderer recovery](MAIN_BOSS_NATURAL_PHASE_TESTS_AFTER1021_REVIEW.md)
- [HitCircle cel register and VRAM stride history](MAIN_HITCIRCLE_NATURAL_CEL_REGISTER_AFTER976_REVIEW.md)
- [Current storage policy](STORAGE_HANDOFF_CURRENT.md) ·
  [after1024 applied audit](STORAGE_HANDOFF_AFTER1024.md)
- [Historical handoff archive](RE_HANDOFF_ARCHIVE_AFTER927.md)
- [Generated progress](PROGRESS.md)
