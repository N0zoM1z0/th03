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

The report's twelve source hashes were checked against all twelve maintained
files at that checkpoint. Current scoped source bindings are: `ba_sring` and
`ba_srest` use `af1056c`, `ba_koto` uses `af1084e`, `ba_chiyu` uses `af1083h`,
`ba_yumem` uses `af1083h`, `ba_mima` uses `af1059a`, `ba_kana` uses `af1060a`,
`ba_reimu` uses `af1083h`, `ba_ellen` uses `af1063a`, `ba_maris` uses `af1065a`,
`ba_rikak` uses `af1066a`, `hitcirc` uses `af1085f`, and `bullet` uses
`af1085u`.
The `af1067a` ten-owner integration is historical for the later Kotohime
source change; its other nine owner bindings remain unchanged. Local native
probe reports are not Factory Oracle receipts or accepted facts.

Shared BOSS current-source refresh: `.analysis/work/exatt-layout-af1056c/report.json`
SHA-256: `f23dfc1120fdf36091ccc6b890ac6a7382af9790b5b1662c06a830a13aa7dad5`.
It covers 949 CODE bytes, 106 ordered native fields and eight PUBLIC offsets
across both shared physical owners, with the full Japanese MAIN image and
ordered relocations equal in two independent rounds. See the
[updated shared-core review](MAIN_BOSS_SHARED_CORE_NATURAL_CONTROL_AFTER1047_REVIEW.md)
and [pattern-rejection review](MAIN_BOSS_PATTERN_REJECTION_DO_WHILE_AFTER1025_REVIEW.md).

Kotohime's previous current-source refresh was `af1057d`; the newer Radial
Burst source is now bound by `af1068e`. It recompiled the complete 1,840-byte
`ba_koto` owner with 262 ordered native fields and eleven PUBLICs in two
original TC4 rounds, preserving the Japanese MAIN image and ordered
relocations. The update controller retains its direct inactive-player return.
The Radial Burst now has loop-header register indices and per-center scratch
lifetime. See the [current Radial review](MAIN_KOTOHIME_RADIAL_NATURAL_FOR_AND_ARITHMETIC_AFTER1033_REVIEW.md).

Current Kotohime report: `.analysis/work/exatt-layout-af1068e/report.json`
SHA-256: `a51759a9529f0da12dc9dd9cded1492aedf828405599ddafefc354876a25669c`.
An alternate nested `while` spelling was also verified at `af1068w` against
the same current owner; the maintained source keeps the narrower `for`-header
index lifetimes from `af1068e`. The alternative report is
`.analysis/work/exatt-layout-af1068w/report.json` (SHA-256
`fb0e5d33f26e95e1269447a9bf851eaafd91d2836aa07c11bc54b3906638f1b2`).

HitCircle current-source refresh: `.analysis/work/exatt-layout-af1085e/report.json`
SHA-256: `51120b41a145c2d3222ac49d5c2afd11eb10c2fe6bdbcee3e45b856c9079ada5`.
It recompiled the complete 445-byte `hitcirc` owner with 30 ordered native
fields and four PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The cel calculation uses BX-bound compound
self-division. The thirteen-record update now uses a natural `for` header with
index-first / pointer-second advancement; the renderer scopes its enemy index
and separate enemy/player cel offsets to their actual uses. See the
[current HitCircle for/lifetime review](MAIN_HITCIRCLE_NATURAL_FOR_LOCAL_LIFETIMES_AFTER1085_REVIEW.md)
and [cel allocation review](MAIN_HITCIRCLE_CEL_REGISTER_ALLOCATION_AFTER1029_REVIEW.md).

Chiyuri current-source refresh: `.analysis/work/exatt-layout-af1069u/report.json`
SHA-256: `c4ac3dce799ad355973af2c11a9628b956da5150f0dcd10b5db8c332416152e3`.
It recompiled the complete 2,654-byte `ba_chiyu` owner with 381 ordered native
fields and eleven PUBLICs in two original TC4 rounds, preserving the Japanese
MAIN image and ordered relocations. The 528-byte `chiyuri_pattern_fans()` now
uses a register-qualified opposite-player PID and four natural `while` passes;
each pass preserves emission, byte-speed and index-update order. See the
[current fan-loop review](MAIN_CHIYURI_FANS_NATURAL_WHILE_AFTER1069_REVIEW.md)
and [PID lifetime review](MAIN_CHIYURI_FANS_REGISTER_PID_AFTER1069_REVIEW.md).

Yumemi current-source refresh is now included in the joint
`.analysis/work/exatt-layout-af1070h/report.json` (SHA-256
`878048b4f927d4afa219d30ecf5c8a1660cfa8395fc7b4865bd7b9fceb3a68f4`). It
recompiles the complete 2,358-byte `ba_yumem` owner with 343 ordered native
fields and ten PUBLICs in two original TC4 rounds, preserving the Japanese
MAIN image and ordered relocations. The 368-byte update controller uses natural
update-start/effect-countdown truth tests, initializes its register PID only
after the launched-player guard, and advances the unsigned-word clock with
postfix increment. The 404-byte arrival renderer scopes its byte `phase`
scratch to each of the three branches that use it. The 266-byte Aimed Random
leaf uses a variable-first period-mask firing gate. The Rain leaf has a
loop-local signed index and explicit zero remainder test; Cross Rings and Rain
both use variable-first finish guards. See the [Yumemi update/arrival review](MAIN_YUMEMI_UPDATE_AND_ARRIVAL_LIFETIMES_AFTER1069_REVIEW.md),
[Aimed Random mask review](MAIN_YUMEMI_AIMED_RANDOM_PERIOD_MASK_AFTER1070_REVIEW.md),
[Rain loop review](MAIN_YUMEMI_RAIN_LOCAL_INDEX_AND_MODULO_AFTER1070_REVIEW.md)
and [Cross/Rain guard review](MAIN_YUMEMI_CROSS_RAIN_NATURAL_GUARDS_AFTER1070_REVIEW.md).

Mima current-source refresh: `.analysis/work/exatt-layout-af1059a/report.json`
SHA-256: `397144dec5bda10fd68ba3740c4409cd1adb38073fe30b2605235599d009f0a7`.
It recompiled the complete 1,922-byte `ba_mima` owner with 277 ordered native
fields and nine PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The complete Mima update controller now
uses the direct inactive-player return while retaining its level setup, mode
dispatch and collision/hitbox tail. See the
[current Mima PID-scope review](MAIN_MIMA_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Kana current-source refresh: `.analysis/work/exatt-layout-af1060a/report.json`
SHA-256: `da7b824a76578facb835758886e2ca95e2a6d5788b5548b3b2084cfb59bb3d29`.
It recompiled the complete 1,874-byte `ba_kana` owner with 274 ordered native
fields and nine PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The complete Kana update controller now
uses the direct inactive-player return before its attack-mode dispatch and
collision/hitbox tail. See the
[current Kana PID-scope review](MAIN_KANA_UPDATE_POSITIVE_PID_SCOPE_AFTER1033_REVIEW.md).

Reimu current-source refresh is now included in the five-owner integration
`.analysis/work/exatt-layout-af1077k/report.json` (SHA-256
`ac71f4eff35a78362537d81d8d01b1d306c8a86d4dfa137830c0775de65742b8`). It
recompiles the complete 2,020-byte `ba_reimu` owner with 270 ordered native
fields and nine PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The 443-byte Orbit Burst has three
phase-local signed indices, byte-angle scratches and natural `while` loops;
the 339-byte Orbit Cloud has disjoint byte-angle scopes and natural cadence
tests. The 118-byte spread leaf now has positive cadence guards in both frame
phases, and the 98-byte mirrored spread uses explicit byte casts. The 296-byte
Update controller has a first-use PID local, natural level arithmetic,
compound frame increment and a simplified INTRO return guard. See the [Orbit
Burst review](MAIN_REIMU_ORBIT_BURST_PHASE_LOCAL_WHILE_AFTER1071_REVIEW.md),
[Orbit Cloud review](MAIN_REIMU_ORBIT_CLOUD_PHASE_LOCAL_ANGLE_AFTER1072_REVIEW.md),
[spread-leaf review](MAIN_REIMU_SPREAD_PHASE_GUARDS_NATURAL_CPP_AFTER1077_REVIEW.md),
[Update controller review](MAIN_REIMU_UPDATE_CONTROLLER_NATURAL_CPP_AFTER1074_REVIEW.md)
and [Reimu PID-scope review](MAIN_REIMU_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Ellen current-source refresh: `.analysis/work/exatt-layout-af1063a/report.json`
SHA-256: `9965bf3ad20cf6fe5fadb5ec5522529f19e086a6618d6598660629c85ef9c513`.
It recompiled the complete 1,675-byte `ba_ellen` owner with 213 ordered native
fields and nine PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The complete Ellen update controller now
uses the direct inactive-player return before target tracking and frame
advancement, preserving its level setup, attack-mode dispatch and collision/
hitbox tail. See the
[current Ellen PID-scope review](MAIN_ELLEN_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Marisa current-source refresh: `.analysis/work/exatt-layout-af1065a/report.json`
SHA-256: `85c25305bb19ad8683e49d10c616d23de3d91abb57ca97e6c666b4afdb4f75b8`.
It recompiled the complete 1,431-byte `ba_maris` owner with 199 ordered native
fields and nine PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The complete Marisa update controller now
uses the direct inactive-player return before its mode dispatch and collision/
hitbox tail. See the
[current Marisa PID-scope review](MAIN_MARISA_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Rikako current-source refresh: `.analysis/work/exatt-layout-af1066a/report.json`
SHA-256: `17e3ec6f9a147a36d35f77af3f6e73742efbe4605b7b9832f4773b6474fdc1b4`.
It recompiled the complete 1,677-byte `ba_rikak` owner with 215 ordered native
fields and eight PUBLICs in two original TC4 rounds, preserving the full Japanese
MAIN image and ordered relocations. The complete Rikako update controller now
uses the direct inactive-player return before its mode dispatch, preserving the
signed-byte spin update and collision/hitbox tail. See the
[current Rikako PID-scope review](MAIN_RIKAKO_UPDATE_POSITIVE_PID_SCOPE_AFTER1033_REVIEW.md).

Current-source ten-owner integration: `.analysis/work/exatt-layout-af1067a/report.json`
SHA-256: `857551a78dd400b20c72940c186dc53835c1385fa0bcb69131920e389d47c689`.
This integration rebuilt the current shared pair plus all eight updated
character BOSS owners together in two original TC4 4.02 rounds: 10 complete
physical owners, 16,042 CODE bytes, 2,197 ordered native fields and 83 PUBLICs.
Both normal MAIN links reproduce the original Japanese loaded image and all
ordered relocations. The two unchanged owners, Yumemi and HitCircle, remain
bound to the `af1053k` baseline; no full cold replay was run.

### Evidence interpretation

`af1053k` remains the latest twelve-owner integration checkpoint. Current
source bindings are split by the subsequent scoped refreshes: the shared pair
uses `af1056c`, Kotohime uses `af1057d`, Chiyuri uses `af1058a`, Mima uses
`af1059a`, Kana uses `af1060a`, Reimu uses `af1061b`, Ellen uses `af1063a`,
Marisa uses `af1065a`, Rikako uses `af1066a`, and the other two owners remain
bound to `af1053k`. The earlier
`af1053i`, `af1052g`,
`af1051k` and `af1047l` full-set checkpoints are historical snapshots, not
additional current proof. Older standalone
`af1024*` and `af1021*` reports are also historical for owners changed since
those stages; do not call them current source proofs. The focused reviews and
detailed compiler chronology are preserved in
[the after1053 archive](RE_HANDOFF_ARCHIVE_AFTER1053.md).

## Current source-bound MAINL evidence

The `af1055m` refresh rebuilds the complete Staff/root owners in two original
TC4 rounds. Both complete decoded EXE/MAP pairs and all ordered relocations
match the Japanese target. It preserves and revalidates the unchanged cold pair;
no full cold replay was run. The current decoded publication is restored.

Report: `.analysis/work/mainl-current-af1055m.json`, SHA-256
`79caf379d74222bb546b8d482f5c0e52fce31aeadf0279ca18fdbeabe6ae45d9`.
See the [focused review](MAINL_CURRENT_SOURCE_REFRESH_AFTER1055_REVIEW.md) for
source transport, current native evidence and the next-build commands.

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

The shared BOSS scheduler has also been re-naturalized under the current
controller scope. `boss_pattern_next()` now uses a `do-while` rejection loop,
preserving the inclusive recent-pattern window and one RNG draw per candidate.
Stage `af1056c` rebuilt both shared owners (`ba_sring` and `ba_srest`) in two
original TC4 rounds: 949 CODE bytes, 106 ordered native fields and eight
PUBLICs, with both normal MAIN links and ordered relocations exact. The other
ten owners remain source-bound to `af1053k`; see the
[af1056c shared-core review](MAIN_BOSS_SHARED_CORE_NATURAL_CONTROL_AFTER1047_REVIEW.md).

Kotohime's complete 332-byte `gba_boss_update_kotohime()` controller now
uses the direct inactive-player return before target tracking and mode
advancement. This re-applies the natural guard under the current Radial/Pellet
and arithmetic source, and preserves the entire switch plus collision/hitbox
tail. Stage `af1057d` rebuilt `ba_koto` in two original TC4 rounds: 1,840 CODE
bytes, 262 ordered native fields and eleven PUBLICs, with the full Japanese
MAIN image and ordered relocations exact. See the
[af1057d current-source review](MAIN_KOTOHIME_UPDATE_INTRO_GUARD_AFTER1025_REVIEW.md).

Chiyuri's complete 613-byte `gba_boss_update_chiyuri()` controller now uses
the same direct inactive-player return before target tracking and frame
advancement. The current 2,654-byte `ba_chiyu` owner was rebuilt in two original
TC4 rounds: 381 ordered native fields and eleven PUBLICs match, as do both
normal MAIN images and ordered relocations. See the
[af1058a current-source review](MAIN_CHIYURI_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Mima's complete `gba_boss_update_mima()` controller now uses the direct
inactive-player return as well. The current `ba_mima` owner was rebuilt in two
original TC4 rounds: 1,922 CODE bytes, 277 ordered native fields and nine
PUBLICs match, with the full Japanese MAIN image and ordered relocations exact.
The seven level-parameter initializations remain before the guard; the launched
player's mode switch and collision/hitbox tail remain after it. See the
[af1059a current-source review](MAIN_MIMA_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Kana's complete `gba_boss_update_kana()` controller now uses the same direct
inactive-player return. Its seven level parameters remain before the guard;
the full INTRO/SELECT/attack dispatch, render-frame update and collision/hitbox
tail remain in order. Stage `af1060a` rebuilt `ba_kana` in two original TC4
rounds: 1,874 CODE bytes, 274 ordered native fields and nine PUBLICs match,
with both normal MAIN images and ordered relocations exact. See the
[af1060a current-source review](MAIN_KANA_UPDATE_POSITIVE_PID_SCOPE_AFTER1033_REVIEW.md).

Reimu's complete `gba_boss_update_reimu()` controller has a first-use PID
local, natural level-derived setup arithmetic, compound frame advancement and
a direct INTRO early-return guard. The current `ba_reimu` source is bound by
the five-owner integration `af1077k`: 2,020 CODE bytes, 270 ordered native
fields and nine PUBLICs match in two original TC4 rounds, with both normal MAIN
images and ordered relocations exact. The 443-byte Orbit Burst, 339-byte Orbit
Cloud, 118-byte spreads and 98-byte mirrored spread all have current-source
native matches. See the [Orbit Burst review](MAIN_REIMU_ORBIT_BURST_PHASE_LOCAL_WHILE_AFTER1071_REVIEW.md),
[Orbit Cloud review](MAIN_REIMU_ORBIT_CLOUD_PHASE_LOCAL_ANGLE_AFTER1072_REVIEW.md),
[spread-leaf review](MAIN_REIMU_SPREAD_PHASE_GUARDS_NATURAL_CPP_AFTER1077_REVIEW.md),
[Update controller review](MAIN_REIMU_UPDATE_CONTROLLER_NATURAL_CPP_AFTER1074_REVIEW.md)
and [Reimu PID-scope review](MAIN_REIMU_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Ellen's complete `gba_boss_update_ellen()` controller now uses the direct
inactive-player return before target tracking and frame advancement. The
current `ba_ellen` owner was rebuilt in two original TC4 rounds: 1,675 CODE
bytes, 213 ordered native fields and nine PUBLICs match, with both normal MAIN
images and ordered relocations exact. The level setup, four attack-mode groups
and collision/hitbox tail remain in order. See the
[af1063a current-source review](MAIN_ELLEN_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Marisa's complete `gba_boss_update_marisa()` controller now uses the direct
inactive-player return before target tracking and frame advancement. The
current `ba_maris` owner was rebuilt in two original TC4 rounds: 1,431 CODE
bytes, 199 ordered native fields and nine PUBLICs match, with both normal MAIN
images and ordered relocations exact. The level setup, full attack-mode switch
and collision/hitbox tail remain in order. See the
[af1065a current-source review](MAIN_MARISA_UPDATE_POSITIVE_PID_SCOPE_AFTER1032_REVIEW.md).

Rikako's complete `gba_boss_update_rikako()` controller now uses the direct
inactive-player return before target/frame updates. The current `ba_rikak`
owner was rebuilt in two original TC4 rounds: 1,677 CODE bytes, 215 ordered
native fields and eight PUBLICs match, with both normal MAIN images and ordered
relocations exact. The five level parameters remain before the guard; the
Orbit/Entities/Alternating Burst switch, signed-byte spin update and full
collision/hitbox tail remain after it. See the
[af1066a current-source review](MAIN_RIKAKO_UPDATE_POSITIVE_PID_SCOPE_AFTER1033_REVIEW.md).

The current-source integration after these updates combines both Shared
BOSS providers with Kotohime, Chiyuri, Mima, Kana, Reimu, Ellen, Marisa and
Rikako. Stage `af1067a` rebuilt all ten complete physical owners in two
original TC4 rounds: 16,042 CODE bytes, 2,197 ordered native fields and 83
PUBLICs match, as do both complete normal MAIN images and ordered relocations.
Only the unchanged Yumemi and HitCircle owners remain on the prior af1053k
source binding. See the [af1067a ten-owner integration report](#current-source-bound-main-evidence).

The later Kotohime Radial Burst source-only refresh `af1068e` supersedes the
`ba_koto` binding in that ten-owner integration. It revalidates the complete
1,840-byte owner in two original TC4 rounds; the other nine objects were not
changed. No full cold replay was run.
HitCircle's later `af1068s` source-only refresh similarly supersedes its
`af1053k` baseline binding. It revalidates the complete 445-byte `hitcirc`
owner in two original TC4 rounds; no other physical owner was rebuilt.

The current two-owner integration after the Radial and HitCircle updates is
`af1068t`: `ba_koto` and `hitcirc`, 2,285 CODE bytes, 292 ordered native fields
and 15 PUBLICs. Both original TC4 rounds and both normal MAIN links match.
Report: `.analysis/work/exatt-layout-af1068t/report.json`, SHA-256
`527dd1fa061231d33e796217ba7f6b41fdeb505c0a28abe348d5613647d675a2`.

Kotohime's complete 332-byte `gba_boss_update_kotohime()` controller now
places the opponent PID local after the inactive-player guard and initializes
it at declaration; the boss frame uses prefix increment. Stage `af1084b`
rebuilds the complete 1,840-byte `ba_koto` owner in two original TC4 rounds:
262 ordered native fields and eleven PUBLICs match, with both normal Japanese
MAIN images and ordered relocations exact. See the
[Kotohime update review](MAIN_KOTOHIME_BOSS_UPDATE_NATURAL_CPP_AFTER1084_REVIEW.md).

The current eight-owner Bullet + Kotohime + Reimu + Yumemi + Chiyuri / Reimu
Extra Attack / HitCircle source integration is `af1085v`: `bullet`, `ba_koto`,
`ba_reimu`, `ba_yumem`, `ba_chiyu`, `ex_rfly`, `ex_reup` and `hitcirc`, 13,158
CODE bytes, 1,555 ordered native fields and 75 PUBLICs. Both original TC4
rounds and both normal Japanese MAIN links match. Report:
`.analysis/work/exatt-layout-af1085v/report.json`, SHA-256
`c3d5f5ba9b80eef6462e1c8ac33779c6b588779dd4cd08d4824f0e138d8e0ba3`.
It includes the Bullet group velocity ring increment, Kotohime's current
radial/update source, Reimu's four attack leaves, update controller and both
main/intro renderers, the 205-byte `reimu_exatt_render_one()` recovery, both
physical Reimu Extra Attack owners, Chiyuri's fan source, Yumemi's update/
arrival/Aimed Random/Rain/Cross-Rain changes, and HitCircle's register-bound
cel arithmetic plus narrowed update/render scratch lifetimes.

Reimu's 281-byte `exatt_update_reimu()` is further naturalized in the separate
`ex_reup` physical unit. Stage `af1077d` rebuilt the 331-byte owner in two
original TC4 rounds: 331 CODE bytes, 22 ordered native fields and two PUBLICs
match, with both normal Japanese MAIN images and ordered relocations exact.
The update uses an ordinary entity pointer, a `for`-scope index, variable-first
state tests, and an RNG-initialized byte angle with compound addition. The
current inline source dependency is checked by the source overlay. See the
[Reimu Extra Attack Update review](MAIN_REIMU_EXTRA_ATTACK_UPDATE_NATURAL_CPP_AFTER1077_REVIEW.md).

The 819-byte `group_velocity_set()` dispatcher now uses prefix increment for
the terminal count update in both ordinary and aimed ring fallthrough chains.
The complete 2,685-byte Bullet owner, including its 9,500-byte BSS, matches in
two original TC4 rounds; the eight-owner integration also matches. Several
other tempting local-scope and byte-decrement rewrites changed CODE and were
reverted. See the [Bullet group-velocity review](MAIN_BULLET_GROUP_VELOCITY_RING_INCREMENT_AFTER1085_REVIEW.md).

HitCircle's `HitCircle::cel()` uses the natural compound self-division
`_BX /= HITCIRCLE_FRAMES_PER_CEL` while keeping the intermediate in BX. Its
thirteen-record update and renderer now also use a `for`-header index/pointer
advance and branch-local cel offsets. The current 445-byte owner and seven-owner
integration both match in two original TC4 rounds; see the
[HitCircle for/lifetime review](MAIN_HITCIRCLE_NATURAL_FOR_LOCAL_LIFETIMES_AFTER1085_REVIEW.md),
[cel allocation review](MAIN_HITCIRCLE_CEL_REGISTER_ALLOCATION_AFTER1029_REVIEW.md)
and [compound-division review](MAIN_HITCIRCLE_CEL_COMPOUND_DIVISION_AFTER1084_REVIEW.md).

Kotohime's 302-byte `kotohime_pattern_radial_burst()` now initializes its
per-center angle at declaration while retaining the original signed division
and AL-mediated byte-phase update. The latter remains inline assembly: three
natural C alternatives changed CODE, as did prefix increment of the warning
frame and declaration-initializing the x/y polar scratches. The complete
1,840-byte `ba_koto` owner is exact in two original TC4 rounds; see the
[Kotohime radial review](MAIN_KOTOHIME_RADIAL_CENTER_ANGLE_LIFETIME_AFTER1084_REVIEW.md).

The 118-byte `reimu_pattern_spreads()` and 98-byte
`reimu_pattern_mirrored_spread()` leaves were also rechecked against Ghidra and
the complete `ba_reimu` owner. Positive cadence guards and explicit byte casts
match in two original TC4 rounds; see the
[Reimu spread-leaf review](MAIN_REIMU_SPREAD_PHASE_GUARDS_NATURAL_CPP_AFTER1077_REVIEW.md).
The 205-byte `reimu_exatt_render_one()` in `ex_rfly` now has branch-local
sprite scratch lifetimes, initialized screen coordinates and explicit
`reinterpret_cast` word loads. It was rebuilt with the full 825-byte owner in
two original TC4 rounds; see the
[Reimu Extra Attack renderer review](MAIN_REIMU_EXATT_RENDER_ONE_NATURAL_CPP_AFTER1078_REVIEW.md).
The 259-byte `reimu_render_main()` now has a declaration-initialized PID,
disjoint main/orbit sprite-offset scopes, an orbit-local animation byte, a
loop-local signed index and a positive ORBIT-mode gate. The 259-byte
`reimu_render_intro()` now initializes its PID and sprite offset at declaration
and scopes the X polar scratch to the loop body. The intro animation byte,
signed loop index and Y coordinate remain in their original broader scopes
because isolated lifetime experiments changed CODE. Both renderers are covered
by the current `ba_reimu` source and five-owner integration; see the
[Reimu main-renderer review](MAIN_REIMU_RENDER_MAIN_NATURAL_CPP_AFTER1083_REVIEW.md)
and [Reimu intro-renderer review](MAIN_REIMU_RENDER_INTRO_NATURAL_CPP_AFTER1083_REVIEW.md).

Recommended next work:

1. Continue the Hitbox/collision family and inspect the next large engine/BOSS
   controller. The 819-byte Bullet group dispatcher, HitCircle's 445-byte owner,
   Kotohime's 302-byte Radial Burst and 332-byte BOSS Update, and Reimu's 443-byte
   Orbit Burst, 339-byte Orbit Cloud, 118-byte spreads, 98-byte mirrored spread,
   296-byte BOSS Update, 281-byte Extra Attack Update, 205-byte Extra Attack
   renderer, and both 259-byte main/intro renderers now have current-source
   native matches. Compare the complete affected physical owner each time.
2. Revisit adjacent Reimu Extra Attack creation and remaining rendering
   helpers, then expand into the next large engine/BOSS controller. Recheck
   current source and disassembly rather than inheriting old assumptions.
3. Expand beyond the already integrated nine character BOSS owners. Use
   `config/units.csv`, `config/evidence.csv`, current source and focused
   reviews to identify genuinely unowned large functions or engine areas.
4. Treat all older next-target recommendations as historical. Recheck current
   source and evidence before selecting work; do not assume an old note or
   decompiler boundary is correct.

For every source change, choose an unused DOS-safe stage, rebuild only affected
physical TUs, compare the complete native extents/ordered fields and normal
link, and preserve both original compiler rounds. Do not run full cold replay
for ordinary scoped changes.

## Factory replay availability

The repository shell and scoped original-TC4 probes are available, but the
Factory-controlled replay queue currently rejects TH03 submissions because
`th03` is not registered with the configured replay worker. The accepted
snapshot therefore has no OracleResults for these imported claims. Do not
promote local probe output, Ghidra output, or Git commits to accepted exactness;
retry canonical replay only after worker registration is restored.

## Current product status and limits

The 2026-11-09 preflight and script audit distinguish these current scopes:

- **MAIN:** 106 units; file-backed authored source 78,737/78,737 bytes;
  main-function ledger 459/459; 335 boundary observations and 335
  function-exact entries. These are scoped source/ledger measures, not
  whole-game acceptance.
- **OP:** current decoded source acceptance 60 extents / 92 procedures /
  14,985 bytes (13,221 CODE + 1,764 initialized DATA). Canonical packed
  unit and whole-product acceptance remain separate.
- **MAINL:** current decoded publication is restored through `af1055m`.
  All tracked extents have source; accepted scopes and their origins are in
  generated progress. Whole-product and canonical Factory acceptance remain open.
- **ZUN:** 77 decoded extents; 2,179 authored, 1,390 original-ASM and
  5,066 library bytes. Whole-product source ownership remains open.

Whole-game completion percentage is unknown. Use generated
[PROGRESS.md](PROGRESS.md) and current preflight rather than old totals.

### Open blockers

- The original BIOS input_s object remains source-native exact at 417 CODE
  bytes but the full MAIN link has a historical one-byte trailing-NOP gap.
  Do not insert a synthetic NOP or claim full-link acceptance.
- MAINL scopes beyond the current decoded publication remain open. Extend
  affected native evidence before claiming additional ownership.
- Vendor OMF packet identity and original raw MZ-header writer identity are
  separate from CODE/FIXUPP/PUBLIC and normal-link image/relocation equality.
  Canonical Factory packed-file acceptance remains open.

## Storage and handoff safety

The [after1024 storage audit](STORAGE_HANDOFF_AFTER1024.md) and
[current policy](STORAGE_HANDOFF_CURRENT.md) remain authoritative. Preserve
all source-bound receipt ancestry, both raw rounds, logs, Japanese targets,
compiler/Wine and analyzer state. No native proof tree was removed in the
script audit. Generic cleanup now refuses receipt pruning and analysis
`--apply`; only `clean_generated.py --caches-only --apply` is supported.

## Script audit and current reporting

`status.py` and generated progress separate ledger, decoded publication and
current native owner checks. All bars count extents; MAIN's function ledger
is separate. The MAINL reviewers support read-only `--check`; the obsolete
145-owner publication fallback and presentation-source verifier gate are retired.
ZUN was republished after removing that presentation dependency; its complete
physical audit is unchanged. OP's publication remains valid.

Default `ci.py` checks changed machine-input syntax and whitespace; `--full`
selects the broad suite. The [script index](../scripts/README.md) records the
1,358-file syntax/dependency audit and broad-test failures rooted in the stale
MAINL cold graph and historical cleanup expectations. Use affected current
checks; the historical all-tests run was not repeated as a completion gate.
The later `af1055m` source refresh restores current MAINL decoded publication.

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
