# TH03 reconstruction: current agent handoff (2026-11-07)

This is the CURRENT, compact handoff. The full previous after596 chronology
is frozen in [RE_HANDOFF_ARCHIVE_AFTER596.md](RE_HANDOFF_ARCHIVE_AFTER596.md).
Old after554/after565 instructions and the 258-stage after520 storage audit
are historical baselines, not the latest native source-link or deletion roots.
Read AGENTS.md and the relevant source review, not every historical note.

## Latest 34-owner current-source native MAIN after657

The new af657a original Turbo C++/TLINK two-round full MAIN
integration compiles **34 actual complete project source TUs**,
including all previous 30 gameplay/BOSS/Extra Attack/CPU/Yumemi
units, plus four original physical sources newly recovered in
after652-655: Ellen charged-shot, Ellen bomb, Chiyuri charged-shot
and Kotohime charged-shot. The current Mima/Rikako BOSS C++
arithmetic changes are also included. The compiler consumed
the real edited source and header paths, attested by emitted
OMF dependency records. Both native rounds preserve **42,352
original CODE bytes, 4,342 ordered literal native fixups,
240 PUBLIC offsets**, complete normal MAIN executable/MAP
and Japanese loaded program/1,553 MZ relocations; independently
serialized standard MZ reproduces the exact original 130,882-byte
Japanese MAIN.EXE. Other 65 original project objects and
startup/CRT libraries were reused without full cold replay.
Read MAIN_THIRTYFOUR_CHARGESHOT_BOMB_AFTER657_NATIVE_REVIEW.md.
The source-owned CODE was already accounted for; do not
double-count as canonical packed-game Factory acceptance.

## Mima and Rikako full BOSS native C++ after656

Mima's large BOSS update now recomputes the opponent bullet PID
directly in natural C++ after the shared helper, preserving
the original order and exact codegen. Rikako's entity/pellet
BOSS attack now uses direct byte-field speed += 8 instead of an
AL load/add/store. A shorter-looking AX -= 8 in Rikako's
sprite renderer changed original CODE and was rejected.
The after656d source-OMF-attested original TC4/TLINK dual rounds
verify both complete BOSS objects together: 3,599 CODE bytes,
492 ordered fixups, 17 PUBLICs, full original MAIN/MAP and
Japanese MZ. See MAIN_MIMA_RIKAKO_CPP_AFTER656_REVIEW.md.
Only these two source objects were recompiled, no full
cold replay or newly accepted canonical game-byte credit.

## Kotohime original nine-function charged-shot source after655

The full cs_koto native original source is now verified from real
changed compiler inputs: nine functions / 690 CODE bytes / 79
ordered FIXUPPs / 9 PUBLICs. Ordinary boolean active and inactive
checks are original-native byte equal. TC4 checks the physical
8-byte projectile, center +02 and velocity +06 offsets and the
four-byte Gauge timing view; original Gauge frames retain their
0/0x80 start/end. Replacing the collision routine's special BX
pointer contract with an ordinary register pointer selected SI
and emitted original-unequal 692-byte CODE (af655b), so that
negative variant was rejected. Two source-bound native rounds
af655e reproduce full original MAIN/MAP/Japanese MZ. Details:
MAIN_KOTOHIME_CHARGESHOT_CPP_AFTER655_REVIEW.md.
Only the affected original project object was recompiled,
without full cold replay or double canonical byte acceptance.

## Chiyuri nine-function charged-shot source after654

The original cs_chiyu full native producer now uses original-code-equal
natural i * 4 + 2 staggered ages and explicitly unsigned % 2 sprite
and Gauge attack parity. Real TC4 checks the six-byte per-projectile
stride and center offset +02. Its update, collision and rendering
traverse slots backwards; the original reset loop mistakenly clears
only the first slot sixteen times, which is intentionally not fixed.
Both after654e current-source/OMF-attested native TC4/TLINK rounds
match all 1,011 CODE bytes, 96 literal ordered fixups, 9 PUBLICs,
complete original MAIN and Japanese MZ relocations. Full details:
MAIN_CHIYURI_CHARGESHOT_CPP_AFTER654_REVIEW.md.
Only this affected object recompiled; no full cold replay or
double-counted canonical packed-file acceptance.

## Ellen bomb actual zero-private-BSS source ABI after653

The full original `b_ellen` three-function TU has 1,023 CODE
bytes and 116 fixups, with **zero private BSS**, unlike the
default source mode. `af653a` proved that compiling with the
private 132-byte bomb storage silently changes 18 code
address/addend bytes even when CODE length and PUBLIC offsets
match. The native v2 wrapper now defines
`TH03_BOMB_EXTERNAL_STORAGE` and compiler-asserts the exact
8-byte particle, 128-byte pool and +04 velocity offset.
Real C++ `static_cast<unsigned int>(frame) % 2` compiles the
original palette/sound tick; real native-unequal `%4` shake and
fallthrough respawn rewrites were rejected. Two original
source/OMF-attested `af653g` TC4/TLINK rounds preserve
**1,023 CODE bytes, 116 literal native fixups, three PUBLICs**,
all segment/BSS definitions, full original MAIN EXE/MAP
and Japanese MZ. Read
[after653 Ellen bomb native ownership](MAIN_ELLEN_BOMB_EXTERNAL_ABI_AFTER653_REVIEW.md).
No full cold replay and no double-counted packed-game
Factory acceptance.

## Ellen full charged-shot/Gauge owner after652

The v2 native compiler overlay now supports the complete original
Ellen `cs_ellen` controller source/TLINK slot in addition to
after650's 30 current owners. Its ten functions (large
homing/clip/collision update, 64-slot pool, sprite renderer and
two-region Gauge volleys) now use natural native-exact
`--ellen_chargeshot_p->state` and direct signed-register C++
instead of a temporary `#define _AX`. Real original TC4
checks the 12-byte projectile's center/velocity offsets and
four-byte Gauge timing record. An attempt to remove the
full updater's `goto active` changed original code and was
rejected (`af652b`). Source-OMF-attested `af652g`
dual original TC4/TLINK rounds prove **1,530 CODE bytes,
169 ordered native fixups, ten PUBLICs**, whole MAIN and
the Japanese loaded program/1,553 original MZ relocations.
See [after652 Ellen native review](MAIN_ELLEN_CHARGESHOT_NATIVE_AFTER652_REVIEW.md).
Only this affected object was recompiled; no full cold replay
or new canonical packed-byte credit.

## Latest complete 30-owner source-native MAIN after650

The v2 explicitly source/header-rooted `af650a` Turbo C++/TLINK
two-round proof now recompiles **30 complete original physical TUs**:
the earlier 28 BOSS/Extra Attack/Bullet/Fireball/Enemy objects
**plus** CPU collision/dodge and Yumemi target/charged-shot/Gauge
(whose full sources changed in after646/647). All selected sources
actually consumed are verified through OMF COMENT dependencies,
including maintained packed BOSS and Extra Attack headers.
Both rounds match **38,098 original CODE bytes, 3,882 literal ordered
native FIXUPPs, 209 PUBLIC offsets, complete normal MAIN EXE/MAP**,
the Japanese loaded program, 1,553 ordered MZ relocations and
separately serialized exact original 130,882-byte Japanese file.
See [after650 thirty native gameplay owners](MAIN_THIRTY_CPU_GAUGE_GAMEPLAY_AFTER650_NATIVE_REVIEW.md).
Other 69 original objects and startup/CRT libraries reused unchanged,
**no full cold replay**, no new canonical packed-byte credit or
historic vendor OMF packet identity claim.

## Chiyuri complete paired Extra Attack beam after649

The genuine Chiyuri four-function Extra Attack owner now explicitly
names its physical **eight pairs / sixteen 32-byte slots**, narrow,
growing, full and shrinking GRCG trapezoid phases, 4/0x10 warning
ticks and endpoint sloped-collmap state boundaries. Original 16-bit
AL/AX/DX choreography and near skip-branch labels are kept: a
natural late-beam subtraction failed the native original-CODE
control `af649a`. Correct v2 changed-source/header-attested
`af649b` two-round TC4/TLINK proof reproduces **978 CODE bytes,
55 ordered FIXUPPs, 4 PUBLICs**, entire original normal MAIN
and Japanese MZ. See
[after649 Chiyuri beam review](MAIN_CHIYURI_PAIR_BEAM_AFTER649_NATIVE_REVIEW.md).
No cold replay or double code-byte credit.

## Yumemi large GRCG Extra Attack beam source after648

The full Yumemi Extra Attack compiler TU (five functions, including the
very large GRCG beam/sprite renderer and dual collision/collmap updater)
now expresses the signed-width beam extent as natural
`static_cast<signed char>(p->duration - 8 - p->frame)`
instead of a cast of `0xF8`, with original bytecode unchanged.
It also names the actual ordinary/special eight-plus-eight 32-byte
entity slot partition and original beam growth/closing frame limits.
Source/header OMF-attested `af648b` native TC4/TLINK dual rounds
prove **1,696 CODE bytes / 87 literal ordered fields / 5 PUBLICs**,
full original normal MAIN and Japanese MZ. See
[after648 Yumemi beam review](MAIN_YUMEMI_EXATT_GRCG_CPP_AFTER648_REVIEW.md).
No whole cold replay or newly accepted packed-file bytes.

## Full Yumemi target/charged-shot and Gauge attack native source after647

The v2 compiler overlay additionally supports the actual
`cs_yume` physical source (ten complete original functions)
outside the older 28-BOSS/gameplay scope. Its large charged-shot
ring renderer and 8-case Gauge barrage timeline use typed, native
C++ frame phase enums and exact unsigned `frame % 2`
flicker. Target acquisition names boss=254, none=255 and
first-formation=0 sentinels. Compiling a superficially equivalent
Gauge `+=` was original-unequal and rejected. Both actual-source
OMF-attested `af647g` native TC4/TLINK rounds verify
**1,645 CODE bytes / 133 ordered literal FIXUPPs / 10 PUBLICs**,
full original normal MAIN and Japanese program/1,553 relocations.
See [after647 Yumemi charged-shot and Gauge review](MAIN_YUMEMI_CHARGESHOT_NATIVE_AFTER647_REVIEW.md).
Only this physical object is recompiled; no cold replay or
double canonical byte credit.

## Native full CPU target/dodge owner after646

The scoped genuine Turbo C++/TLINK v2 source driver can now compile
and OMF-dependency-attest the original `p_cpu` physical object
**outside** the existing 28-owner gameplay overlay. The full CPU
collision/target/approach/dodge state machine now uses natural
`round_or_result_frame % 4` and `randring1_next16() % 4`
with original-binary equality, names the 3x3 dodge lookup and
three retry columns, and preserves the original signed-byte
probe-radius loop after an equal-value enum candidate was
source-unequal. Dual `af646f` native TC4/TLINK rounds reproduce
**1,077 original CODE bytes / 64 literal ordered fields / 4 PUBLICs**,
full original normal MAIN and Japanese image/MZ relocations.
See [after646 CPU native review](MAIN_CPU_DODGE_CPP_AFTER646_NATIVE_REVIEW.md).
No full cold replay, new canonical packed-game Factory credit or
double-counting of previously tracked code bytes.

## Current changed-source 28-owner MAIN integration after645

The latest `af645a` two-round genuine Turbo C++/TLINK source-bound
native pair rebuilt **28 complete original TUs simultaneously**,
including new Kotohime/Mima/Ellen/Rikako Extra Attack semantics,
typed parity/history loops, and natural Chiyuri BOSS cardinal/fan
C++ arithmetic. The v2 read-only reviewer checked actual OMF
source/header dependencies and verified **35,376 previously owned
CODE bytes, 3,685 literal ordered FIXUPPs, 195 PUBLICs**, full
normal MAIN EXE/MAP, Japanese loaded image, 1,553 original MZ
relocations and separately serialized original 130,882-byte EXE
in both rounds. See
[after645 native integration review](MAIN_TWENTYEIGHT_EXATT_BOSS_AFTER645_NATIVE_REVIEW.md).
Only selected 28 physical objects recompiled; other 71 original
objects plus CRT libraries unchanged, no full cold replay or double
Factory packed-game byte credit.

## Chiyuri full BOSS cardinal/fan natural C++ after644

The two major Chiyuri cardinal and fan barrage functions no longer
need explicit AL load/add/store for cardinal +8/-8, three cumulative
quarter-turn shots, four fan +2/-2 speed steps or both mirrored fan
angles. The original-exact mirror form is **binary**
`bullet_template.angle = (0 - bullet_template.angle)`;
the shorter unary negation was native-unequal (`af644f`).
The real modified-source-attested TC4/TLINK proof `af644h`
matches **2,654 CODE bytes, 381 ordered fields and 11 PUBLICs**,
full MAIN and all Japanese relocations in both native rounds. See
[after644 Chiyuri C++ review](MAIN_CHIYURI_BOSS_NATURAL_ARITH_AFTER644_REVIEW.md).
No cold replay or new accepted packed-game CODE bytes.

## Rikako full homing and typed native parity after643

The real Rikako Extra Attack now has named eight ordinary/fourteen total
slots, inclusive 0x40..0x50 homing window, special +0x17
`homing_disabled` semantics and original flying/arrival state
boundaries. Natural `static_cast<unsigned int>(frame) % 2` in
the renderer produces original parity bytes, unlike plain `frame % 2`
(`af643a`). Replacing the signed `angle_delta /= 8` divisor with
an equal-valued enum changed codegen and was rejected (`af643c`).
Correct v2 `af643e` full source/header-bound native TC4/TLINK
pair reproduces **702 CODE bytes, 46 ordered FIXUPPs, five PUBLICs**,
complete original MAIN and Japanese MZ. See
[after643 Rikako Extra Attack review](MAIN_RIKAKO_EXATT_HOMING_AFTER643_NATIVE_REVIEW.md).
No full cold replay or duplicate accepted byte count.

## Ellen seven-sample orbit/trail Extra Attack after642

The six-function Ellen Extra Attack uses 12 original 30-byte physical
slots per player, each a near entity pointer plus two seven-word
history arrays. Native TC4 checks the +02/+10 history offsets and
30-byte stride. The large orbit/history/collision update's descending
history copy and seven-sample flight completion loops, plus the
four-sprite renderer's 6/4/2/0 loop, are now natural C++ for-loops.
The actual source/header-attested `af642c` two-round TC4/TLINK
proof reproduces all **1,129 CODE bytes, 79 ordered fields, six
PUBLICs**, original complete MAIN/MAP/Japanese MZ. Read
[after642 Ellen Extra Attack review](MAIN_ELLEN_EXATT_TRAIL_AFTER642_NATIVE_REVIEW.md).
No full cold replay or new canonical byte credit.

## Mima full Extra Attack signed/unsigned parity after641

The main Mima Extra Attack rebound/collision/update owner now
expresses the original `duration & 1` as typed natural C++:
`static_cast<unsigned int>(duration) % 2`. Ordinary signed
`duration % 2` was real native-unequal (`af641a`). Named
six-slot, flight and 0x10/0x20/0x50 acceleration phases preserve
all original movement and collision semantics. The full v2
`af641c` source/header-attested native TC4/TLINK pair matches
**727 CODE bytes, 44 ordered fields, four PUBLICs**, entire
normal MAIN and Japanese MZ. See
[after641 Mima Extra Attack review](MAIN_MIMA_EXATT_UNSIGNED_PARITY_AFTER641_NATIVE_REVIEW.md).
No full cold replay or double accepted target bytes.

## Kotohime complete Extra Attack event counter after640

The eight-function Kotohime Extra Attack module now names the ten
physical slots (eight ordinary plus two special), both exact shot
counts and the original post-arrival `angle` byte's actual *event
counter* semantics at pulses 4, 8, 12 and 16. The tempting
four-shot signed ternary changed native CODE and was **rejected**.
The real source/header OMF-attested `af640c` two-round
TC4/TLINK proof reproduces all **1,054 CODE bytes, 100 ordered fields
and eight PUBLICs**, full normal MAIN and Japanese relocations.
See [after640 Kotohime Extra Attack review](MAIN_KOTOHIME_EXATT_EVENTS_AFTER640_NATIVE_REVIEW.md).
No full cold replay or double target-byte credit.

## Latest source-rooted 28-unit GAME3 integration after639

The latest `af639a` fresh native Turbo C++/TLINK dual rounds
recompile **28** complete project objects together *after* Chiyuri,
Rikako, Kotohime and Kana natural C++ source recovery. Source/OMF
dependency attestation confirms the compiler consumed the current
changed sources, including both 32-byte BOSS/Extra Attack headers.
Both rounds match **35,376 previously owned CODE bytes, 3,685
literal ordered native FIXUPP fields, 195 PUBLICs**, complete
normal MAIN EXE/MAP and the Japanese target program and 1,553
ordered MZ relocations. The separately generated standard MZ
serialization gives the original 130,882-byte Japanese MAIN.EXE.
Read [after639 native integration](MAIN_TWENTYEIGHT_GAMEPLAY_AFTER639_NATIVE_REVIEW.md).
Only the 28 affected TUs were newly compiled; other 71 project objects
and startup libraries were reused. No full cold replay or double
Factory packed-file acceptance credit.

## Kana staged ring and rotating attack native C++ after638

Kana's full nine-function original BOSS now uses actual-byte-equal
C++ direct `bullet_template.angle += 6`,
`bullet_template.speed.v += 3` and rotating-ring
`boss_frame % 4`. All 18 scheduler IDs and accel/staged/cloud/
rotating phases are named. Same-valued *non-time* numeric literals
were deliberately kept distinct after hand-checking the first
compiled enum pass: PID, render mode, angle and iteration count
must not accidentally acquire frame-limit names. The one-line
signed rotating-direction arithmetic failed native comparison,
so the actual four-branch AL implementation remains. Final
v2 `af638f` dual original Turbo C++/TLINK rounds prove all
**1,874 CODE bytes, 274 ordered fields, nine PUBLICs**, full
normal MAIN and all Japanese relocations. See
[after638 Kana native review](MAIN_KANA_BOSS_NATIVE_AFTER638_REVIEW.md).
No full cold replay or newly accepted packed game bytes.

## Kotohime four full BOSS patterns after637

Kotohime's aimed/radial ring helpers now use exact original C++
`boss_move_phase -= 2` in two locations and its ring renderer uses
natural `boss_frame % 4` flicker. Original native-unequal
direct +2 / -4 angle substitutes were tested and rejected.
The full 18-mode scheduler and ring expansion, release and
pellet phases use named compile-time constants. Actual v2
`af637f` Turbo C++/TLINK pair reproduces all **1,840 original CODE
bytes, 262 ordered FIXUPP fields, 11 PUBLICs**, full normal MAIN
and 1,553 Japanese relocations. See
[after637 Kotohime review](MAIN_KOTOHIME_BOSS_NATIVE_AFTER637_REVIEW.md).
No cold replay or newly accepted packed bytes.

## Rikako native signed spin and BOSS phases after636

Rikako's large update and three attack routines now lower from
natural `boss_frame % 8` in all three spin-clock paths, plus
`boss_spin_delta += ((boss_spin_delta > 2) ? -1 : 1)` in the
alternating burst. The full 18-mode dispatcher and warning, entity,
pellet and four alternating burst phases have typed names. Genuine
v2 Turbo C++/TLINK dual rounds `af636d` prove **all 1,677 original
CODE bytes, 215 ordered native fixups, eight PUBLICs**, complete
normal MAIN EXE/MAP and all Japanese relocations. See
[after636 Rikako review](MAIN_RIKAKO_BOSS_NATIVE_AFTER636_REVIEW.md).
No cold replay or duplicate accepted bytes.

## Chiyuri full BOSS modes and natural modulo after635

The current Chiyuri BOSS includes all 18 character-specific scheduler
modes, typed trail warning/firing and two independent fan timelines,
and true original-equal C++ `% 8` and `% 4` for warning and animation
cadence. Both real source/OMF-bound Turbo C++/TLINK rounds `af635c`
preserve the full **2,654 original CODE bytes, 381 ordered fields,
11 PUBLICs**, normal MAIN and Japanese MZ/1,553 relocations. See
[after635 Chiyuri native review](MAIN_CHIYURI_BOSS_TIMING_AFTER635_NATIVE_REVIEW.md).
No new Factory packed byte credit or full cold replay.

## Current 28-unit GAME3 native source pair after634

The `af634a` actual-source/OMF-dependency-attested Turbo C++/TLINK
pair **recompiled all 28** BOSS, shared BOSS, Extra Attack, Bullet,
Fireball, Explosion and four Enemy TUs together after the current
Mima/Ellen/Reimu/Marisa source changes. It preserves **35,376
original CODE bytes / 3,685 literal ordered FIXUPP fields / 195 PUBLICs**,
complete original normal MAIN EXE/MAP, Japanese program image,
1,553 MZ relocations and the separately serialized exact original
file. Native proof and current caveats are in
[after634 source-bound integration](MAIN_TWENTYEIGHT_GAMEPLAY_AFTER634_NATIVE_REVIEW.md).
Other 71 original objects and libraries were retained; no whole
cold replay or new packed-file Factory byte acceptance was claimed.

## Mima original signed-orbit and attack cadence after633

Original-source-rooted Turbo C++ compiles `boss_frame % 2` for
Mima's orbit and spreading/sound ticks, and `boss_frame % 4`
for random bomb volley firing to the **original exact byte masks**.
The entire large Mima BOSS TU is source-bound and exact in two
`af633b` native compiler/TLINK rounds (1,922 CODE bytes, 277
ordered fields and nine PUBLICs). See
[after633 Mima source review](MAIN_MIMA_CADENCE_NATIVE_AFTER633_REVIEW.md).
No full cold replay or additional accepted packed bytes.

## Marisa full BOSS native pattern recovery after632

The real Marisa source owner now uses natural `boss_frame % 4` and
`boss_frame % 0x20` for the exact original four- and 32-frame firing
periods. Its full 18-mode dispatcher and wide/narrow columns, ring
and spread timelines are now explicit compile-time enums, preserving
the distinct final volley and finish frames. Both genuine native
`af632c` rounds verify **1,431 CODE bytes, 199 ordered fields, nine
PUBLICs**, the entire original MAIN link and all Japanese relocations.
See [after632 Marisa review](MAIN_MARISA_PATTERN_NATIVE_AFTER632_REVIEW.md).
No cold replay or new accepted packed-game bytes.

## Reimu full BOSS dispatch and timelines after631

Reimu's large controller retains its genuine pre-switch intro/pattern
selection, and now names all shared scheduler values plus the four
separate attack phase maps: orbit cloud, paired spread, expanding orbit
Extra Attack and mirrored spread. Natural shortcut `angle = -angle`
was rejected by genuine native codegen. Correct v2 `af631c`
source-bound Turbo C++/TLINK two-round proof is **2,020 CODE bytes /
270 literal ordered fields / nine PUBLICs**, complete MAIN and all
Japanese relocations. See
[after631 Reimu native review](MAIN_REIMU_PATTERN_NATIVE_AFTER631_REVIEW.md).
No full cold replay or new accepted packed CODE credit.

## Ellen original attack scheduler and Extra Attack timing after630

The current Ellen full BOSS TU has original-valued C++ enums for the
18 shared scheduler modes, spread/volley timing and the two distinct
Extra Attack bursts. Actual-source/OMF-dependency-attested `af630f`
dual TC4/TLINK rounds reproduce all **1,675 CODE bytes, 213 ordered
fields, nine PUBLICs**, complete MAIN and all Japanese relocations.
Native-unequal attempts to invert spread control flow and compress the
renderer ring-index wraparound were rejected; no behavior fix was
introduced. See [after630 Ellen source review](MAIN_ELLEN_PATTERN_NATIVE_AFTER630_REVIEW.md).

## Mima full BOSS source recovery after630

The current Mima BOSS now expresses its signed `+7/-7` orbit direction
as genuine original-byte-producing C++ and identifies the 18 attack
scheduler modes and real frame boundaries in typed enums. The
source/OMF-attested `af630c` dual native compiler/TLINK rounds preserve
the complete 1,922 CODE bytes, 277 ordered fields, nine PUBLICs, full
original MAIN and 1,553 Japanese relocations. See
[after630 Mima source review](MAIN_MIMA_PATTERN_NATIVE_AFTER630_REVIEW.md).
An inverted Ellen branch tested in `af630a` was original-unequal and
is not retained. No double byte credit or full cold replay.

## Current bounded 28-owner source-native integration after629

The latest `af629a` original compiler/TLINK pair rebuilt **all nine
large BOSS TUs, two shared BOSS owners, ten Extra Attack units, Bullet,
Fireball, Explosion and four Enemy units** together, after the actual
shared-template and Yumemi source changes: **28 native producer TUs /
35,376 CODE bytes / 3,685 literal ordered native fields / 195 PUBLICs**.
The v2 read-only reviewer checks the exact consumed current sources
including the separately maintained BOSS and Extra Attack 32-byte
headers. Both complete normal MAIN EXE/MAP outputs, Japanese loaded
program bytes, all 1,553 ordered MZ relocations and independent
standard MZ serialization match original. See
[after629 native integration review](MAIN_TWENTYEIGHT_SHARED_TEMPLATE_AFTER629_NATIVE_REVIEW.md).
Only 28 affected objects were built, **not** a whole-project cold
replay; no double source-byte or Factory packed-file acceptance credit.

## Yumemi large BOSS mode dispatch / ring recovery after628

The complete 2,358-byte Yumemi original-source BOSS TU now uses a
natural signed ternary for the rotating-ring `_AL` angular step,
plus named character-specific attack mode and ring phase enums in
the actual large pattern scheduler/renderer. Two independent
OMF-source-attested native TC4/TLINK rounds (`af628f`) match all
2,358 CODE bytes, 343 literal fixups, ten PUBLICs, full normal
MAIN and 1,553 original relocations. The failed single-shift
animation variant `af628b` was rejected, not smuggled into the
accepted code. See
[after628 Yumemi BOSS review](MAIN_YUMEMI_PATTERN_NATIVE_AFTER628_REVIEW.md).

## Eleven complete BOSS native owners share a single ABI after627

All nine character BOSS controller sources plus shared ring and core
(11 physical native objects, **18,400 CODE bytes / 2,540 ordered fields /
93 PUBLICs**) now compile against the one checked **32-byte**
`boss_template_state_t`. In Mima/Marisa, anonymous physical fields
have been renamed to their true initializer semantics without changing
field byte locations or code. Two actual source-and-header-rooted
Turbo C++ / full TLINK rounds `af627b` reproduce original complete
MAIN EXE/MAP, 1,553 ordered Japanese relocations and serialized file.
Read [after627 original BOSS template review](MAIN_ELEVEN_BOSS_PHYSICAL_TEMPLATE_AFTER627_NATIVE_REVIEW.md).
All previously owned bytes remain credited only once.

## BOSS template and core unified through after626

The current `boss_template_state_t` also replaces duplicated
Chiyuri/Ellen/Rikako/Reimu templates and the shared BOSS controller's
32-byte state view. Explicit v2 source/header OMF dependency attestation,
two TC4/TLINK rounds and complete original MAIN/MAP/Japanese MZ matching
passed for **six more physical units: 8,975 CODE bytes, 1,185 ordered
native fixups and 45 PUBLICs**. The original REP MOVSW state copy and
signed per-character byte semantics are preserved. See
[after626 native review](MAIN_BOSS_TEMPLATE_CORE_AFTER626_NATIVE_REVIEW.md).
No new accepted game-byte credit is claimed.

## Latest BOSS physical ABI after625

Kana, Kotohime and Yumemi major BOSS source TUs now include a maintained
single physical 32-byte `boss_template_state_t` instead of three duplicate
structs. Native after625b source-bound two-round TC4/TLINK proof covers
**6,072 CODE bytes / 879 ordered fields / 30 PUBLICs**, original complete
MAIN/1,553 relocations and explicitly verified OMF COMENT dependency on
the new template header. See
[after625 template ABI review](MAIN_BOSS_SHARED_TEMPLATE_AFTER625_NATIVE_REVIEW.md).
Historical receipts are kept unchanged, and no new canonical game bytes
are credited.

## URGENT: v1 source-binding flaw, corrected native proof after614

**DO NOT cite after598–610 overlay reports as proof that changed source
compiled.** Their literal `#include "src/...cpp"` silently loaded old
`TH03WORK/src/...`, even as the overlay copied the modified source to a
separate directory. Original OMF dependency records exposed the problem;
invalid `chains.hitsue` in the new C++ compiled successfully in v1 but was
correctly rejected in explicit-source v2. This invalidates the source-exact
claim of the after606 nineteen-owner v1 receipt and supersedes the claims
in the following chronological sections. Do not delete those experiments.

After614 native v2 **does** prove current 10 Extra Attack TUs from actually
consumed source/header overlays: **8,781 CODE / 563 native fields / 52 PUBLICs**
in two real Turbo C++ / full TLINK rounds, entire MAIN/Japanese target exact.
The 32-byte entity requires local byte packing under original TC4; original
Chiyuri Extra Attack branch/beam instructions have been restored after
negative compiler trials. See
[after614 source-binding audit](MAIN_NATIVE_SOURCE_BINDING_AFTER614_REVIEW.md)
and v2 read-only review `scripts/review_th03_main_source_overlay.py --stage af614a`.
The remaining v1 BOSS, Bullet, Fireball and Enemy source claims need
source-rooted confirmation or correction. Do not treat `progress.py` ledger
counts as proof of newly changed source bytes.

## Critical correction: v2 native source binding

**Do not treat the historical after598–610 scoped overlay results as
proof that the edited source compiled.** Turbo C++ resolved their
`#include "src/..."` to the old TH03WORK tree even though the probe
recorded hashes of copied candidate source files. The v2 compiler
driver/read-only reviewer now force original-source and shared-header
include paths, check the OMF dependency COMENT records, and reject v1
receipts. It caught an intentionally-invalid Explosion member name,
and reanalysis showed actual Bullet register-encoding failures and
Fireball/Enemy control-flow changes. Original baseline programs remain
available and unchanged; no historical receipts were deleted.
`af614a` is a genuine v2 full ten-Extra-Attack proof with correct
byte packing and restored Chiyuri register/branch operations. See
[after615 source-binding review](MAIN_NATIVE_OVERLAY_SOURCE_BINDING_AFTER615_REVIEW.md).
All earlier after598–610 positive statements below are *historical*
and should not be promoted without new v2 compiler evidence.

### New large source-verified collision routine after611

The full 630-byte `explosions_hittest()` collision/score/charge dispatcher
now compiles from the *actual changed* natural C++ source under v2,
verified in four incremental positive controls and two complete real
TC4/TLINK rounds (`af611g`). The code removes alias macros/enum and
radius unions while preserving the original stack frame, 49 ordered
native fields, original MAIN linker and Japanese MZ. See
[after611 actual-source review](MAIN_EXPLOSION_GENUINE_CPP_AFTER611_REVIEW.md).
This is not new accepted byte credit. The old v1 collision reports
are invalid for changed-source attribution.

### Bullet/Fireball/Enemy native source correction after615

The earlier v1 after607–609 source claims have been corrected, not carried
forward. Three Bullet pseudo-register expressions changed x86 opcode bytes;
Fireball direct continues changed jump layout; Enemy script VM early returns
changed near/short branches and pointer allocation. Source was restored to
the actual original-byte-producing forms, with negative compiler controls
and precise reasons in
[after615 native recertification](MAIN_BULLET_ENEMY_FIREBALL_AFTER615_REVALIDATION.md).
The modified large Explosion collision function remains **genuinely exact**.
The corrected v2 `af615a` simultaneously recompiles all seven physical
Bullet/Fireball/Enemy/Explosion TUs from the *actual* modified sources:
8,195 CODE bytes, 582 ordered native fields, 50 PUBLICs plus Fireball DATA
in two complete normal MAIN links and Japanese full-file equality.
No full cold replay, source masking or new Factory packed-byte credit.

## Immediate next-agent start

- Inspect git status --short --branch and git log; do not reset or discard
  dirty/untracked/ignored work. The working HEAD may have advanced past after614; inspect it again.
- Use .venv/bin/python scripts/preflight.py when starting or changing the
  toolchain. Check scripts/validate_tracking.py and scripts/progress.py --check.
- For CURRENT changed MAIN source evidence, run the v2 source-bound
  scripts/review_th03_main_source_overlay.py --stage af614a; the after596
  reader is an older pinned-source historical control.
  For MAINL, run the READ-ONLY
  scripts/review_th03_mainl_score_input_pi_after587_work.py.
  Set DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts and use one allowed CPU
  at nice10. These reviewers do not run full cold replay.
- Wine/Borland writers use .analysis/borland-wine-writer.lock. Preserve the
  candidate-local-attested Japanese targets and existing source inputs.

## What is verified now (different notions of exactness)

| Product | Current verified scope | Formal/remaining boundary |
| --- | --- | --- |
| MAIN | after596 source-native 99-object link; 124,642 program bytes and 1,553 ordered MZ relocations exactly original; standard DOS MZ serializer gives the exact 130,882-byte Japanese file | Direct newer TLINK emits a 132,322-byte MZ with a different header. Source-owned ledger is 459/459 functions and 78,737/78,737 *reviewed authored bytes*, not all program/library bytes or vendor tool identity |
| MAINL (ending) | Historical after587 source-native multi-TU link: entire 67,372-byte Japanese decoded EXE and all 677 ordered relocations exact; targeted historical reviewer still passes | **Current source-bound decoded acceptance pending** after later MAIN source edits invalidate the earlier all-source preservation guard. Historical 220/259 extents / 37,968 bytes (17,717 authored + 20,251 library) are retained *as past reviewed evidence*, not present accepted source credit. Canonical Factory credit 0/250 |
| OP | Retained decoded source publication: 60 extents, 92 procedures, 14,985 reviewed bytes | Canonical packed product/source ownership still open |
| ZUN | Retained decoded publication: 77 extents, 89 procedures/entries and 8,635 reviewed CODE+DATA bytes | Canonical packed product/source ownership still open |

Source-backed whole linked images, raw vendor OMF packet identity, original
historical compiler/linker provenance, physical behavior, source ownership
and canonical packed-file acceptance are DIFFERENT claims. Never upgrade a
reviewed function, normal TLINK equality, or a compact MZ serialization to
formal Factory/whole-product ownership acceptance.

## Retained current native roots — do not delete

- MAIN latest full source graph:
  .analysis/work/main-yumemi-cpu-after596-native-build.json
  and scripts/review_th03_main_yumemi_cpu_after596_work.py.
  The parent chain is after595 results/shots/HUD; after594 entry/round loop;
  after593 player core; after592 nine character callback setup; after591
  collision/386 collmap; after589 large fireball/explosion; after588
  bullet/386 GRCG; after572 four enemy producers; after567 nine BOSSes and
  native held-key input; after568 distinct compact DOS MZ serializer.
- MAINL latest full source graph:
  .analysis/work/mainl-score-input-pi-after587-native-build.json
  and scripts/review_th03_mainl_score_input_pi_after587_work.py.
  Parents: after586 SFX/music/file; after585 input modes/PI raster; after584
  original continue menu segment fix; after583 CG-ROM text; after582 CDG
  loader; after580 root story/stage; after578 score/name-entry; after577
  three 386 CDG blitters; after575 Staff Roll/ending; after573 cutscene;
  after570 natural TASM sound, after569 registration DATA EVEN; earlier
  input/vector/root/CRT and normal C0/linker parents.
- Both independent compiler rounds, consumed scratch source and response
  files, original OMF/EXE/MAP files, logs, JSON receipts, and relevant
  after514/after520 CRT proof chains are live historical evidence.
  Preserve the entire active source-bound DAG, not only last-stage EXEs.

## Historical claims that must not mislead the next agent

- Older docs calling after554/after565 the CURRENT link predate the
  above after587/after596 source stages. The original MAIN full file
  IS now reproducible using the separate standard MZ format stage;
  the direct TLINK compact header is still not a historical match.
- All 22 FAR procedures, 5,598 CODE bytes and 860 logical fixups of
  cplx2 were source-linked in after514. The unchanged pinned
  src/mainl/crt/cplx2.asm header saying "full native link not yet
  established" is STALE; its original OMF frame metadata is still
  different. See docs/MAINL_CPLX2_FULL_SOURCE_LINK_AFTER514_NATIVE_REVIEW.md.
- The unchanged pinned src/mainl/cutscene.cpp comment that three PI call
  operands "remain open" is STALE: after573 independently recompiles
  all 3,195 CODE bytes and 236 ordered OMF fields, full MAINL exact.
  Avoid editing those SHA-bound historical inputs just to fix a comment.
- The old continue menu's CONTINUE_TEXT pragma is wrong for the original
  CUTSCENE_TEXT object. The corrected alternative after584 links exact;
  negative C++ direct-section control had 696 MZ relocations vs 677.
- A proposed TASM EVEN at the original root joystick two zero-byte
  positions generated 90h rather than the original 00h. This was
  rejected; do not silently replace semantic db 0 source with EVEN.
- A natural C++ call to explosions_hittest in MAIN hitbox compiles as
  direct FAR CALL 9Ah, not original NOP/PUSH CS/near CALL 90h 0Eh E8h.
  Three negative compiler controls are retained under TH03WORK/probe/af590h.
- A later CRT historical baseline after520 reached 728/893 working
  source-linked members and 194,292 original CODE bytes. The older
  isteldbl and h_ldiv notes describe scoped evidence/limitations,
  not a reason to re-credit already completed cplx2 or to claim all
  893 vendor library members were independently source-linked.

## Latest scoped source refresh (after598)

After the frozen after596 MAIN proof, the large Yumemi Extra Attack producer
and Mima Extra Attack producer now share `src/main/player/exatt_entity.hpp`
instead of maintaining two redundant 32-byte record definitions. Two native
TC4/TLINK rounds in the `af598v` overlay preserve all 2,423 CODE bytes,
131 ordered native fixup fields, nine PUBLICs, segment definitions, the
complete original normal MAIN EXE/MAP and 1,553 MZ relocations. See
[review](MAIN_EXATT_ENTITY_SHARED_AFTER598_NATIVE_REVIEW.md) and
`scripts/probe_th03_main_exatt_layout.py`. No additional accepted byte
scope is claimed. Historical after596 receipt source pins remain frozen;
validate new source with the scoped overlay, not by repinning that receipt.

### Rikako state after599

The `af599t` native overlay covers five physically distinct Extra Attack TUs:
Yumemi, Mima, Rikako, shared flight/Reimu prefix and Reimu update. The original
32-byte entity now exposes Rikako's byte +0x17 as a character-specific
`homing_disabled` state without imposing that meaning on other characters.
Both TC4/TLINK rounds reproduce all 4,281 CODE bytes, 250 ordered fields,
24 PUBLICs and unchanged full Japanese MAIN image/relocations. See
[scoped native review](MAIN_RIKAKO_EXATT_HOMING_AFTER599_NATIVE_REVIEW.md).
The `af598v` frozen source refresh remains separately retained. No extra
owned bytes or historical OMF provenance are claimed.

### Character-specific +0x11 after600

`af600b` recompiled eight complete Extra Attack owners (7,442 original CODE
bytes / 484 ordered fields / 42 PUBLICs) in two real TC4/TLINK rounds while
preserving the full MAIN program/1,553 relocations and normalized MAP. Ellen's
+0x11 is a **signed spin delta**, Kotohime's is the **unsigned extra mode**;
Chiyuri uses the same 32-byte entity but currently does not read that byte.
The shared struct keeps both alternatives in a one-byte union and retains the
Rikako +0x17 overlay. See
[after600 native review](MAIN_EXATT_CHARACTER_BYTE11_AFTER600_NATIVE_REVIEW.md).
The historical after599 handoff's 262 count was a transcription error: the
live proof records 250 (after600 includes 484). No new accepted bytes.

### Chiyuri's natural C++ branch after601

`exatt_update_chiyuri` now uses ordinary C++ `if`/`continue` to
skip an inactive paired beam instead of the old manual register/CODE
label branch. The **entire 978-byte Chiyuri object**, all 55 ordered
native fields, four PUBLICs and full Japanese MAIN link pass both
real Turbo C++/TLINK rounds; see
[review](MAIN_CHIYURI_NATURAL_BRANCH_AFTER601_NATIVE_REVIEW.md) and
`.analysis/work/exatt-layout-af601n/report.json`. Historical evidence
remains immutable; no additional accepted byte claim.

### Natural Chiyuri control flow after601

The full Chiyuri beam renderer and paired projectile update no longer need
handwritten ASM for their state==0 jump or phase taper. Native TC4 produces
all original 978 CODE bytes (and original ordered native fields/segdefs) from
the maintained C++ source in two independently compiled and full-linked
rounds, latest `af601e`. The beam renderer still uses the observed AX return
register interface at its shared phase-label boundary. Read
[after601 native review](MAIN_CHIYURI_NATURAL_CONTROL_AFTER601_NATIVE_REVIEW.md)
for the exact accepted and rejected variants. This changes expression
recoverability, not the amount of previously owned target CODE.

### Ten complete Extra Attack producers after602

The current `af602a` source overlay compiles/links all **ten** complete
physical Extra Attack owners: 8,781 original CODE bytes, 563 ordered fields
and 52 PUBLICs in two fresh native TC4/TLINK rounds. Source now shares one
32-byte entity view for Marisa/Kana as well as the prior Ellen/Kotohime/
Chiyuri/Yumemi/Mima/Rikako and Reimu/flight producers. It includes the
original-equal natural Chiyuri control and beam expression. See
[after602 review](MAIN_EXATT_ALL_TEN_AFTER602_NATIVE_REVIEW.md) and the
SHA-bound ignored report; do not treat a historical after596 source-hash
reviewer as suitable for these later changed sources. No extra accepted bytes.

### Active MAINL source-bound gate after602 (not a binary mismatch)

The original after587 MAINL native pair and all 677 relocations are still
retained. The **read-only**
`scripts/review_th03_mainl_score_input_pi_after587_work.py` currently passes
its 425-byte three-unit / two-exact-MAINL-link review. However
`scripts/status.py` now correctly reports **pending decoded source
acceptance: 0 currently admissible extents**, instead of previously
reviewed historical 220. The reason is specific: the after552
`scripts/build_th03_mainl_root_state_work.py` parent graph pins an
all-`src/` archive to early commit `0feb71f8`, including unrelated MAIN
Extra Attack sources. Our natural C++ changes to
`src/main/player/exatt_chiyuri.cpp` make the broad source-preservation
check fail (`unchanged preserved native input ...`). This is a
**current evidence/source-binding failure**, not observed changed MAINL
bytes or lost prior archive evidence. Later changed MAIN source files
would also need audited binding; restoring just one pinned hash would
not resolve the integrity question.

`scripts/progress.py` now publishes the current **pending** gate instead
of carrying over stale source credit. Do not regenerate a historical
receipt, amend its checksums, waive the parent input check, or claim
current 220 decoded extents without a source-scoped recertification.
Historical counts remain visible here; the latest MAIN work instead has
its own new source-native multi-unit overlays and full MAIN comparisons.
No full cold replay was run merely to suppress this validator error.

### Chiyuri major BOSS after603

The full **2,654-byte/11-function Chiyuri BOSS** has exact newly source-
compiled C++ renderer improvements: natural signed `top >>= 4` in the
ring loop and `_DX = 0` before the mono interrupt replace both hand-ASM
blocks. The `af603e` scoped original TC4/TLINK proof rebuilds only that
BOSS slot in two rounds, preserves **381 ordered native fixups**, all
PUBLIC/segment metadata, full normal MAIN EXE/MAP and Japanese file equality.
See [after603 native review](MAIN_CHIYURI_BOSS_NATURAL_RENDER_AFTER603_NATIVE_REVIEW.md).
The historical original BOSS sources/receipts are retained; no double credit.

### Five complete BOSS C++ modules after604

The `af604f` native overlay recompiles five whole Chiyuri/Kana/Kotohime/
Ellen/Rikako BOSS TUs after replacing hand-authored AX shifts in their
large renderer loops with natural signed C++ expressions, plus Kana's
cloud-angle `_AL -= 0x10`. Both actual TC4/TLINK rounds preserve the
**9,720 original CODE bytes**, **1,345 ordered native fields**, **48 PUBLICs**,
complete normal MAIN EXE/MAP and Japanese target relocations. See
[after604 native review](MAIN_FIVE_BOSS_RENDER_AFTER604_NATIVE_REVIEW.md).
The old source-bound after596 proof remains frozen and these are not
incremental accepted byte credits.

### All nine large BOSS source TUs after605

The new `af605c` source-compiled native checkpoint relinks **all nine major
BOSS TUs together** (17,451 original CODE bytes, 2,434 ordered fields,
85 complete functions/PUBLICs) in two real Turbo C++/TLINK rounds, preserving
the full original Japanese MAIN program and all 1,553 relocations. Yumemi
arrival rendering now uses native `_DX = 0` instead of hand-ASM; the
Chiyuri/Kana/Kotohime/Ellen/Rikako C++ ring and other recovery from
`af603e`/`af604f` is retained. The unchanged Mima, Reimu and Marisa
source TUs were independently rebuilt and linked at the same time. Read
[after605 nine-BOSS review](MAIN_NINE_BOSSES_AFTER605_NATURAL_CPP_REVIEW.md).
This is not new accepted CODE credit or a canonical Factory completion.

### Current 19-unit BOSS + Extra Attack integration after606

The newest `af606a` source-native **two-round** proof simultaneously
recompiles and relinks all **9 large BOSS + 10 Extra Attack** units, totaling
**26,232 original CODE bytes, 2,997 ordered native fields and 137 PUBLICs**.
The complete normal MAIN EXE/MAP and all 1,553 original Japanese relocations
remain equal; no full cold replay was performed. New read-only
`scripts/review_th03_main_source_overlay.py --stage af602a af605c af606a`
checks all three current source-bound proof receipts, maintained source
snapshots, full original object fields, compiler logs, MAP and whole MZ.
See [after606 review](MAIN_19_GAMEPLAY_OWNERS_AFTER606_NATIVE_REVIEW.md).
Historical after596 source pins are intentionally frozen; no new Factory
byte credit or historical vendor OMF packet identity is claimed.

### Bullet native register recovery after607

The complete physical Bullet source TU (all 2,685 CODE bytes / 196 ordered
fields / 20 PUBLICs, including large bullet update and 386 GRCG pellet
rendering) now emits original register operations from Turbo C++ rather
than three hand-authored `shl ax`, `xor bx`, `xor dx` instructions.
The native `af607g` two-round original TLINK and read-only source-bound
review pass, preserving full Japanese MAIN and all MZ relocations.
See [after607 Bullet native review](MAIN_BULLET_REGISTER_CPP_AFTER607_NATIVE_REVIEW.md).
The scoped overlay/reviewer also support individual Enemy/Fireball/Explosion
producers with CODE/DATA/BSS-aware output accounting. The older historical
after596 receipt and packed-file Factory counts remain unchanged.

### Fireball full-state-machine C++ after608

The actual Fireball 1,555-CODE-byte / 115-native-fixup source owner now
uses natural `if`/`continue` for both the falling Y release and the
player-dependent horizontal transfer completion, replacing
`free_and_continue` and `switch_to_fall` jumps. Two independent
original TC4/TLINK rounds in `af608c` prove all CODE + 1 DATA + 1 BSS,
10 PUBLICs, normalized full MAIN MAP, complete Japanese program and MZ
vector. See [after608 fireball review](MAIN_FIREBALL_TRANSFER_CPP_AFTER608_NATIVE_REVIEW.md).
The `af608b` seven-unit Enemy/Fireball/Explosion/Bullet control also
passed, with unrelated originals reused. No newly accepted bytes.

### Four original Enemy units, script VM and clipping, after609

The maintained `enemy.cpp` now lowers the large `enemy_run()` ENEDAT
script VM using natural early-return/continue C++ for linear, ordinary,
speed, circular and sine movement, both loop kinds, one typed segmented
script-pointer expression and the duration calculation. The
`enemy_move_and_clip()` helper now has explicit early returns and
short-circuit X/Y clipping without hand-goto. Real two-round native
`af609k` proof recompiles all four `eforna/efornb/eupda/eupdb`
original units, **3,325 CODE bytes / 222 ordered fields / 19 PUBLICs**,
and full Japanese MAIN EXE/MAP/relocation match. See
[after609 script VM review](MAIN_ENEMY_SCRIPT_CPP_AFTER609_NATIVE_REVIEW.md).
The game's original broken LOOP displacement/op_size behavior is retained;
no newly accepted byte count or physical behavior claim is added.

### Explosion collision native C++ recertified after615

The full `explosions_hittest()` collision/chain/score/charge function
now uses natural saturating hit-count C++, direct near-pointer accesses,
a single radius/diameter value and a byte mode (no fake returning macros
or extra struct unions). Real v2 native `af611g` source- and OMF-bound
two-round proof reproduces all 630 original CODE bytes, 49 literal
ordered fields, the entire normal MAIN map/link and original Japanese
image/relocations. See
[the reviewed native source](MAIN_EXPLOSION_NATIVE_CPP_AFTER615_REVIEW.md).
The v1 false-positive experiments are not cited as proof.

### Bullet exact instruction encoding recertified after616

The v2 forced-source native compiler disproved three seemingly natural
Bullet register rewrites: `SHL AX,1` became `ADD AX,AX`, while `_BX=0`
and `_DX=0` selected different XOR ModR/M encodings. The three
necessary original-encoding inline assembly sites are restored with
explanatory comments. Current `af612d` v2 native and OMF dependency review
confirms the full 2,685 CODE bytes, 196 ordered fields, 20 PUBLICs and
complete Japanese MAIN link. Historical `af607g` v1 is **not evidence**
that those three rewritten C++ expressions produced exact target bytes.
See [native opcode review](MAIN_BULLET_CODEGEN_ENCODING_AFTER616_REVIEW.md).

### Genuine signed C++ in five complete BOSS renderers (after620)

The **v2**, actually consumed source/OMF-dependency-bound `af620h`
native compiler rounds now prove a natural *signed* register shift:
`static_cast<int16_t>(_AX) >>= 4` emits original SAR AX,4, where
ordinary unsigned AX produces SHR and simplified `top >>=4` changes
local instructions. All five Chiyuri/Kana/Kotohime/Ellen/Rikako BOSS
TUs (9,720 CODE bytes, 1,345 ordered native fields, 48 PUBLICs) and
the complete normal MAIN EXE/MAP/Japanese image/relocations match twice.
Kana's cloud angle retains inline SUB AL,10 because even signed C++
emits original-unequal ADD AL,F0. See
[after620 five-BOSS native review](MAIN_FIVE_BOSS_SIGNED_REGISTER_AFTER620_NATIVE_REVIEW.md).
This replaces, not supplements, the invalid v1 after603/604/605
changed-source verification claims; no duplicate byte credit.

### All nine original BOSS TUs genuinely source-rooted after621

`af621c` now passes two real original 16-bit Turbo C++/TLINK rounds for
**all nine BOSS TUs together** (17,451 CODE bytes, 2,434 ordered fields,
85 PUBLICs, entire normal MAIN and Japanese program/1,553 relocations).
The five signed C++ AX shift improvements are included. Yumemi's prior
`_DX=0` was rejected by v2 (different XOR encoding); original inline
XOR DX,DX is restored with a source comment. See
[after621 native nine-BOSS review](MAIN_NINE_BOSS_SOURCE_ROOTED_AFTER621_NATIVE_REVIEW.md).
The earlier `af605c` v1 result is **not** a valid changed-source proof.

### Current combined 26-owner original native integration (after622)

The latest genuinely **source-rooted v2** compiler/linker receipt is
`af622a`: all **nine major BOSS, ten Extra Attack and seven Bullet/
Enemy/Fireball/Explosion source units simultaneously** rebuilt and
relinked in two Turbo C++/TLINK rounds. It proves **34,427 original
CODE bytes**, **3,579 ordered native fields**, **187 PUBLICs**, correct
segment DATA/BSS ownership and the entire normal MAIN EXE/MAP;
the Japanese MAIN load image and all 1,553 ordered MZ relocations match.
The current compiler OMF dependencies explicitly bind the changed
candidate source and shared header; v1 stages are not promoted. No
full cold replay occurred, and the 73 remaining project objects and
vendor CRT were reused. See
[after622 source-attested integration](MAIN_26_GAMEPLAY_OWNERS_AFTER622_NATIVE_REVIEW.md).
No new canonical Factory byte or historical raw OMF packet credit.

### Shared BOSS ring and seven-function state/scheduler core (after623)

The native v2 source-overlay now covers the two physical
`ba_sring`/`ba_srest` objects from `src/main/boss/shared.cpp`.
Shared bounce/despawn/pattern/reward constants have semantic C++ enum
names; both original rounds prove **949 CODE bytes / 106 ordered fields /
8 PUBLICs**, complete normal MAIN EXE/MAP and Japanese MZ equality
(`af623c`). Simple C++ struct assignment was independently rejected:
Turbo C++ emits a FAR copy call instead of the original REP MOVSW
in `boss_update_start()`. Preserve that original machine interface.
See [after623 shared-BOSS review](MAIN_BOSS_SHARED_NATIVE_AFTER623_REVIEW.md).

### 28 complete MAIN source TUs in one genuine native link (after624)

Latest `af624a` extends the validated source-rooted 26-owner link with
both BOSS shared ring/state core objects. Two independent original
TC4/TLINK rounds now recompile/relink **28 complete original TUs**:
**35,376 original CODE bytes, 3,685 literal ordered native fields,
195 PUBLICs**, original segment/BSS layouts and one Fireball initialized
DATA byte. Both complete normal MAIN EXE/MAP outputs, all 1,553
Japanese ordered MZ relocations and separate full Japanese MAIN
serialization are exact. Source and shared-header OMF dependencies are
explicitly verified; the other 71 project objects and vendor libraries
were reused. This is not a full cold replay. See
[after624 28-owner native proof](MAIN_28_GAMEPLAY_BOSS_OWNERS_AFTER624_NATIVE_REVIEW.md).
No new packed-file Factory credit, historical OMF packet identity or
untested hardware behavior claim is added.

## Remaining priorities for real reconstruction

Prioritize truly unowned byte/OMF/segment scopes or semantics; do not
count historical original functions again because an extra source-forward
TU recompiled them. Check original 16-bit ABI, x87, source-local packing,
segment naming, literal ordered FIXUPPs and target program bytes.
Verify MAINL project ownership and leftover root alignment evidence;
do not equate administrative publication gaps with source-missing bytes.
Clarify actual whole-file/packed-file provenance and original vendor
OMF frames without inventing target opcode arrays or object patches.
Continue OP/ZUN decoded source questions when material. Do not run full
cold replay unless their source/recipe inputs materially changed.

## Storage and historical references

The after520 CRT retention guard covers 258 source stages and 5,760
native files ONLY in its historical prefix. It is not a deletion
authorization for after521–596, MAIN/MAINL source scratch, tools or
pinned targets. See docs/STORAGE_HANDOFF_CURRENT.md and the latest
audited storage addendum. Native after559/after561 BOSS source proof
workspaces are active; do not blanket-prune the .analysis tree.
The after554 maintenance did not delete new native proofs.

History: docs/RE_HANDOFF_ARCHIVE_AFTER596.md;
docs/RE_HANDOFF_ARCHIVE_AFTER554.md; docs/MAINL_WORKING_CRT_RECOVERY_INDEX.md.
Run only affected review and tracking/progress checks, then git diff --check;
commit substantial changes as gpt-web: xxx. Do not push unless asked.
