# TH03 — current next-agent handoff (2026-11-07)

**Start here.** This is the active short handoff; detailed per-experiment
history through after709 was moved, unchanged in substance, to
[RE_HANDOFF_ARCHIVE_AFTER709.md](RE_HANDOFF_ARCHIVE_AFTER709.md).
Older roots are [after596](RE_HANDOFF_ARCHIVE_AFTER596.md) and
[after554](RE_HANDOFF_ARCHIVE_AFTER554.md). **Do not treat historical
“latest” paragraphs as current state.** Read [AGENTS.md](../AGENTS.md)
and [the workflow](RE_WORKFLOW.md) before modifying native evidence.

## After882: original resident CFG loader leaf and external filename ABI

- The original 49-CODE-byte `cfg_lres` resident config loader now uses
  a natural **file-scope extern `const char CFG_FN[]`**, keeping the
  true external CFG filename and original function-level `cfg_t` scratch.
  Original segmented return pointer, direct call/return and stack ABI
  are native-exact.
- Real original TC4 counterexamples: an explicit local near-result
  pointer declaration was rejected by the old parser (`af882b`);
  a valid extra result local generated **53 vs original 49 CODE**
  (`af882c`); `cfg_t cfg={0}` generated **74** (`af882d`). Reverted
  both. Final `af882e` passes two independent original TC4/full normal
  TLINK rounds: **49 CODE bytes, 6 ordered FIXUPPs, 1 PUBLIC**, full
  Japanese MAIN and all 1,553 relocations; 98 other project objects/
  CRT reused, no cold replay. See
  [after882 original CFG leaf review](MAIN_CFG_RESIDENT_NATIVE_SCOPE_AFTER882_REVIEW.md).
  Existing source ownership, not new Factory/canonical CODE credit.

## After881: full Marisa BOSS and genuinely natural native byte assignment

- The complete nine-function `ba_maris` **major BOSS** now has natural
  unsigned frame `%4/%32` truth gates, named collision and three masked
  intro render planes. A crucial fresh TC4 discovery: while mutable
  `marisa_bullet_angle += ENUM_7` previously failed native codegen,
  **`marisa_bullet_angle = marisa_bullet_angle + ENUM_7` passes** with
  every original instruction, independently repeated with a byte cast.
- Original integer ring division `256 / byte_count` **must not be
  explicitly widened to unsigned** (`af881h`, CODE changed at offset
  394). Final `af881i` passes two original TC4 4.02/normal full TLINK
  rounds: **1,431 CODE bytes, 199 ordered native FIXUPPs, 9 PUBLICs**,
  full original Japanese MAIN and 1,553 MZ relocations exact. 98 other
  project objects/CRT reused; no cold replay. See
  [after881 complete Marisa BOSS review](MAIN_MARISA_BOSS_NATURAL_ANGLE_AFTER881_REVIEW.md).
  Historical source-owned CODE, not new unique Factory packed credit.

## After880: shared Chain 1/Chain 2 original periodic state machine

- The *actual shared* current `background/phase.inl` now gives all eleven
  original phase cutoffs/tick/wave values native-exact C++ names and
  removes a redundant cast on an already unsigned global `%4096`.
  Natural `if(!unsigned_frame %8)`/`%4` truth checks are proven exact,
  while explicit unsigned promotion of the **signed local** remains.
- Fresh genuine negative TC4 controls: signed-local `%8` without cast
  grew Chain 1 **702 vs original 695** CODE (`af880b`), changing
  original `&127` to `%128` altered CODE (`af880e`), and simplifying
  to `!(frame&64)` emitted **690** bytes (`af880g`). The uninitialized
  `changed` byte on 416 original paths is preserved, not 'fixed'.
  Final `af880h` **genuinely recompiles both complete `chain1` and
  `chain2` original physical objects together**, two original TC4 4.02/
  full normal TLINK rounds: **1,245 CODE bytes, 86 literal ordered
  fixups, 9 PUBLICs**, complete Japanese MAIN and 1,553 MZ relocations;
  97 other project objects/CRT reused, no cold replay. See
  [after880 shared phase review](MAIN_BACKGROUND_PHASE_NATIVE_AFTER880_REVIEW.md).
  Existing native source ownership, not new unique/Factory packed credit.

## After879: complete Chain 2 particle initialization and native transition

- The original three-function `chain2` owner now expresses its full
  50-particle initializer as natural C++ `while`, preserves the
  original 40/10 sprite-store distinction, and names both sprites
  and the exact unsigned long 144-frame transition. Original ES:DI
  acceleration/periodic controllers and shared live `phase.inl` remain.
- Genuine TC4 negatives: replacing the two sprite branches with a
  ternary emitted **549 vs original 550 CODE bytes** (`af879c`);
  rewriting `round_frame >144UL` as `>=145UL` changed original CODE
  (`af879d`). Both restored. Final `af879e` passes two original
  TC4/full normal TLINK rounds: **550 CODE bytes, 43 ordered FIXUPPs,
  3 PUBLICs**, complete Japanese MAIN/1,553 MZ relocations exact;
  98 other project objects/CRT reused, no cold replay. See
  [after879 complete Chain 2 review](MAIN_CHAIN2_NATIVE_INIT_AFTER879_REVIEW.md).
  Previously source-owned bytes, no new distinct/Factory credit.

## After878: complete Chain 1 background initialization and acceleration control

- Full original six-function `chain1` owner now uses natural `while` in
  **80-particle vector reset and 48-particle randomized initialization**,
  true signed C++ subpixel X/Y RNG bounds, named initial sprite states
  and typed unsigned-long 128-frame acceleration exit. Both large
  register-contract background animation controllers remain physically
  original-exact, with actual shared phase inclusion.
- Original TC4 negative trials: dropping unsigned RNG parity promotion
  grew CODE to **701 vs original 695** (`af878e`); rewriting 32-bit
  `>128UL` as `>=129UL` changed CODE (`af878f`). Final `af878h` passes
  both genuine compiler/full normal TLINK rounds: **695 CODE bytes, 43
  literal ordered native FIXUPPs, six PUBLICs**, complete Japanese MAIN
  and all 1,553 MZ relocations, 98 other game objects/CRT reused. See
  [after878 full Chain 1 review](MAIN_CHAIN1_NATIVE_INIT_AFTER878_REVIEW.md).
  Existing source-covered CODE, not new distinct/Factory packed credit.

## Latest after877: five changed original physical sources in one exact MAIN link

- `af877a` **actually recompiled five current modified original physical
  sources simultaneously in both original Turbo C++ 4.02 and complete
  normal MAIN TLINK rounds**: full **Chiyuri major BOSS**, full Ellen
  and Rikako Extra Attacks, full Chiyuri Chargeshot/Gauge and original
  PC-98 shutdown leaf. Both native rounds exactly reproduce **5,563 CODE
  bytes, 610 literal ordered original OMF FIXUPPs, 32 PUBLICs**, original
  segment/source ABI, the normal MAIN EXE/MAP, **124,642 Japanese loaded
  bytes and all 1,553 ordered MZ relocations**. Independent standard DOS
  MZ serialization also reproduces all 130,882 Japanese EXE bytes.
  **94 other game project objects and CRT reused**, no cold replay. See
  [after877 five-source integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER877_REVIEW.md).
- Earlier native `af871a`, `af865a`, `af859a`, `af853a`, `af847a`,
  `af842a`, `af835a` represent **separate original compiler experiments**,
  not one invented all-object replay. Preserve historical snapshot proof;
  neither count previously source-owned CODE as new distinct bytes nor
  claim canonical packed-game Factory acceptance from native matching.

## After876: original PC-98 VRAM shutdown leaf and repeated OUT semantics

- Original 67-byte `exit` far-`__cdecl` SHARED physical TU now names
  the two page values for **four actual PC-98 OUTs**, with genuine
  16-bit port and byte page compile-time ABI checks. Port 0xA6
  display page and 0xA4 access page operations, original double
  page-zero selection, and cleanup order remain intact.
- Fresh real original TC4 negative controls: removing 'redundant'
  third display-page DX/AL writes generated **62** vs original **67**
  CODE (`af876b`); routing page one via a `const unsigned char`
  local generated **72** (`af876c`). Both rejected. Final `af876d`
  passes two independent original TC4/full normal MAIN TLINK rounds:
  **67 CODE bytes, 8 ordered native FIXUPPs, 1 PUBLIC**, full original
  Japanese MAIN/1,553 MZ relocations. 98 other project objects/CRT
  reused, no cold replay. See
  [after876 exact PC-98 VRAM exit review](MAIN_EXIT_VRAM_NATIVE_AFTER876_REVIEW.md).
  Existing source-covered original CODE; no new unique/Factory credit.

## After875: complete Chiyuri Chargeshot/Gauge native state and reset

- The complete nine-function `cs_chiyu` source now uses natural
  `while` for all five original projectile loops, including the
  staggered update's clip `continue` and the collision tester's
  **five separate `continue` index/pointer paths**. Original eight
  6-byte projectiles per player, signed stagger ages, clipping and
  hitbox margins remain source-native exact.
- Genuine original TC4 negative controls: sprite byte `anim &1` cannot
  be replaced by `%2` (**1,020** vs original **1,011** CODE, `af875d`);
  and the reset REALLY clears the *same first slot 16 times* — inserting
  a pointer advance changes original CODE to **1,014** (`af875g`).
  Original behavior preserved. Gauge `%16` natural truth spelling passes.
  Final `af875h` compiles/links all nine original functions twice:
  **1,011 CODE bytes, 96 ordered native FIXUPPs, 9 PUBLICs**, exact
  Japanese MAIN/1,553 relocations; 98 other game objects/CRT reused.
  See [after875 Chiyuri Chargeshot review](MAIN_CHIYURI_CHARGESHOT_NATIVE_STATE_AFTER875_REVIEW.md).
  Existing source-covered CODE; no new distinct/Factory credit.

## After874: Rikako complete Extra Attack homing and fourteen-slot control

- Complete five-function `ex_rika` has **natural `while` across all four
  entity allocator/update/renderer loops**, including two original
  `continue` exits of its substantial homing/collision control. All
  original 14-slot scan order, 8 normal launch slots, original character-
  specific +0x17 homing-disable byte and 0x40..0x50 steering window
  are retained with newly named target/hitbox/sprite geometry.
- Independent genuine original TC4 negative controls: replacing signed
  byte `angle_delta /=8` with arithmetic `>>3` emitted **699** vs
  original **702** CODE bytes (`af874d`); changing mutable `p->speed++`
  to prefix emitted **710** (`af874f`). Original forms restored. Final
  `af874g` compiles/links the complete original unit twice: **702 CODE
  bytes, 46 ordered native FIXUPPs, 5 PUBLICs**, full Japanese MAIN
  and 1,553 MZ relocations exact; 98 other project objects/CRT reused,
  no cold replay. See
  [after874 full Rikako Extra Attack review](MAIN_RIKAKO_EXATT_NATIVE_HOMING_AFTER874_REVIEW.md).
  Existing source-owned original bytes, not new unique/Factory credit.

## After873: full Ellen Extra Attack history and spiral native C++

- The full six-function `ex_ellen` source now uses native-exact natural
  `while` for twelve paired slot initialization, the four-sample spiral
  renderer, reverse history shift, seven-point landing history fill
  and complete twelve-slot render dispatcher. Original 30-byte history
  storage, signed 16-bit RNG target/clip/hit geometry are preserved.
- Fresh genuine TC4 negatives: converting both allocator `continue`
  loops to `while` gave **1,133** instead of original **1,129** CODE
  bytes (`af873b`), while byte frame prefix increment gave **1,134**
  (`af873f`). Both original expressions restored. Final `af873g`
  compiles the entire original source twice through TC4 4.02 and
  complete normal MAIN TLINK: **1,129 CODE bytes, 79 ordered native
  FIXUPPs, 6 PUBLICs**, original Japanese MAIN and all 1,553 MZ
  relocations exact. 98 other project objects/CRT reused, no cold replay.
  See [after873 complete Ellen Extra Attack review](MAIN_ELLEN_EXATT_NATIVE_HISTORY_AFTER873_REVIEW.md).
  Already source covered; no additional unique CODE/Factory credit.

## After872: complete Chiyuri BOSS four fan loops and sixteen-sprite ring

- Whole original **11-function `ba_chiyu` major BOSS** now uses native-exact
  natural `while` loops in *all four* signed horizontal/vertical fan
  passes and the two-variable **16-sprite orbit renderer**. The 16-bit
  frame `%8` warning condition has a natural truth predicate; sprite
  geometry and three independent signed intro radii are named.
- Fresh negative original TC4 compiler controls: enum-valued *live
  byte* `angle +=0x10` produced **2,653** vs original **2,654** CODE
  bytes (`af872c`); naming byte-memory fan speed `+=2/-=2` produced
  **2,642** (`af872e`). Original memory forms retained. Final `af872g`
  passes two genuine TC4 4.02/complete normal MAIN TLINK rounds with
  **2,654 CODE bytes, 381 ordered OMF FIXUPPs and 11 PUBLICs**, full
  original Japanese MAIN/1,553 MZ relocations exact; 98 other game
  objects and CRT reused, no cold replay. See
  [after872 full Chiyuri BOSS review](MAIN_CHIYURI_BOSS_WHOLE_LOOPS_AFTER872_REVIEW.md).
  Previously source-owned CODE; not new unique/Factory packed-unit credit.

## Latest after871: five session-edited original MAIN physical sources together

- `af871a` **actually recompiles all five full original physical C++
  sources changed in this session in one two-round native experiment**:
  complete **Kotohime major BOSS**, full Chiyuri Extra Attack, complete
  Marisa Chargeshot/Gauge, the 30-byte PMD/MIDI leaf and Kotohime Bomb.
  Both independent original TC4 4.02 and complete normal MAIN TLINK
  rounds match **all 4,885 original CODE bytes, 521 literal ordered
  native OMF FIXUPPs and 26 PUBLICs**, current-source/segment/ABI
  dependencies, complete normal original MAIN EXE/MAP, all **124,642
  Japanese loaded bytes and 1,553 ordered MZ relocations**. Independent
  standard MZ serialization matches all 130,882 original Japanese file
  bytes. **94 unchanged game objects/CRT reused**, no cold replay. See
  [after871 five-source native integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER871_REVIEW.md).
- Other independent source-current read-only reviews `af865a`, `af859a`,
  `af853a`, `af847a`, `af842a`, `af835a` still pass. Freshly rechecked
  old `af821e`, `af779b`, `af769a`, `af735a`, `af684f` now **fail
  current-source hash binding** and remain genuine *historical* native
  receipts only. Do not repin old compiler snapshots, add already
  covered original CODE again to distinct ownership or claim that these
  separate native experiments were one fabricated all-object rebuild.

## After870: complete Kotohime Bomb phases and native dead-index codegen

- The whole original **`b_koto` 528-byte Bomb controller** now uses a
  natural `while` four-explosion row with real 96-pixel stride, named
  first/second palette phases and both native-exact `if(!(frame %8))`
  triggers, restoring exact X/Y sweep and 0x2E0 downward decay.
- Fresh real original TC4 negatives: replacing the *byte shake* `&3`
  with `%4` compiled **531** vs original **528** CODE bytes (`af870b`),
  and removing the **apparently unused signed `i`** with its frame-based
  initialization and loop increment shortened original CODE to
  **505** bytes (`af870e`). Both original expressions preserved; the
  final uninitialized `color` stack read remains historical target
  behavior, not patched. Final `af870f` passes two genuine original
  TC4/full normal MAIN TLINK rounds: **528 CODE bytes, 50 ordered native
  FIXUPPs, 1 PUBLIC**, all original Japanese loaded MAIN and 1,553
  MZ relocations. 98 other project objects/CRT reused, no cold replay.
  See [after870 Kotohime Bomb review](MAIN_KOTOHIME_BOMB_NATIVE_AFTER870_REVIEW.md).
  Existing original source owner; no new distinct/Factory packed credit.

## After869: exact PMD/MIDI hardware interrupt leaf and original AX return

- Original 30-CODE-byte `snd_kaja` hardware/PMD service now uses a
  natural active-only branch with one common `return _AX`, preserving
  original inactive unchanged AX, strict MIDI flag `==1`, PMD-first
  `INT 60h` and MIDI `INT 61h` selection and the real 16-bit Pascal ABI.
  Old TC4-compatible compile-time guards verify 16-bit short and 8-bit
  flags without adding program data.
- Fresh original compiler negative: reversing the MIDI/PMD branch
  produced different original CODE at byte 18 (`af869a`). The restored
  source with natural active-only branch (`af869c`) passed both original
  compiler/link rounds; final `af869d` passes **30 CODE bytes, 2 literal
  ordered native FIXUPPs, 1 PUBLIC**, whole Japanese MAIN/1,553 MZ
  relocations in two independent TC4 4.02/normal TLINK rounds. 98 other
  original objects/CRT reused. See
  [after869 original PMD/MIDI leaf review](MAIN_KAJA_SOUND_NATIVE_BRANCH_AFTER869_REVIEW.md).
  Previously covered original CODE, no new unique/canonical Factory credit.

## After868: all nine source loops of complete Marisa Chargeshot/Gauge

- The complete `cs_mari` original nine-function Marisa Chargeshot/Gauge
  now expresses all **nine original beam/GRCG/Gauge loops** as natural
  C++ `while`: two 12-point initializers, descending 11-to-1 history
  shift, sparse hit samples 0/4/8, three different GRCG tile bands
  and two five-shot Gauge emitters. Original signed Y `>>5`, 24-subpixel
  trail drop, 16-pixel beam offsets and VRAM clips are named/retained.
- Fresh TC4 codegen negatives: naming the two byte-memory Gauge
  `speed.v -=6` operations emitted **1,503** vs original **1,509**
  CODE bytes (`af868f`); converting byte frame postfix to prefix
  emitted **1,514** (`af868g`). Both original byte updates restored.
  Final `af868i` proves **1,509 CODE bytes, 152 ordered native FIXUPPs,
  9 PUBLICs**, full Japanese MAIN and all 1,553 relocations exact
  in two genuine original TC4 4.02/full normal TLINK rounds. 98 other
  game objects/CRT reused, no cold replay. See
  [after868 Marisa Chargeshot review](MAIN_MARISA_CHARGESHOT_WHOLE_LOOPS_AFTER868_REVIEW.md).
  Already historically covered original CODE, no new unique/Factory credit.

## After867: complete Chiyuri Extra Attack paired-entity and beam loops

- Full four-function `ex_chyu` (~518-byte GRCG beam renderer, ~298-byte
  update) now uses natural `while` for **all three physical 2-entity
  spawn, update/arrival/collision and render traversals**, preserving
  original `goto/continue` two-hop pointer lifetime and byte frame order.
- Genuine original compiler experiment `af867c` caught a mistaken source
  assumption: Chiyuri's second entity **spawns toward Y=0x1780, but
  snaps to Y=0x1700** on arrival, used by the beam warning; mixing those
  changed original CODE at offset 877. Restored both distinct physical
  positions. Signed `/4` → `>>2` in the beam renderer also **failed**
  (`af867f`: **975** vs original **978** CODE bytes); signed division
  remains. Final `af867g` proves **978 CODE bytes, 55 ordered native
  FIXUPPs, 4 PUBLICs**, full Japanese MAIN and 1,553 relocations
  in two actual TC4/normal TLINK rounds, 98 other objects/CRT reused.
  See [after867 Chiyuri Extra Attack review](MAIN_CHIYURI_EXATT_PAIRED_WHILE_AFTER867_REVIEW.md).
  Historical source-owned CODE, not new unique/canonical Factory credit.

## After866: complete Kotohime BOSS natural nested radial and ring control

- Full 11-function Kotohime **major BOSS** (`ba_koto`) now uses
  natural C++ `while` loops for the random/aimed ring emitter,
  **both nested radial-burst loops** and the sprite-ring renderer,
  preserving original signed 16-bit divisions, RNG consumption and
  8-/N-sprite calls. The five original pellet-arc positions and
  three radius growth operations have named source constants.
- Fresh genuine TC4 negative controls: converting the two original
  AL-mediated byte phase updates to `boss_move_phase +=2` generated
  **1,834** vs original **1,840** CODE bytes (`af866d`), and
  replacing the radial `_AL +=0xFC` with `boss_move_phase -=4` generated
  **1,838** (`af866e`). Both byte carrier forms remain. Final `af866g`
  passes two genuine original TC4 4.02/full normal MAIN TLINK rounds:
  **1,840 CODE bytes, 262 literal ordered native FIXUPPs, 11 PUBLICs**,
  original Japanese loaded MAIN and all 1,553 ordered MZ relocations.
  98 other project objects/CRT reused, no cold replay. See
  [after866 Kotohime BOSS review](MAIN_KOTOHIME_BOSS_WHILE_AFTER866_REVIEW.md).
  Already source-covered original CODE, not new unique/Factory accepted bytes.

## Latest after865: five session-modified original sources built together

- `af865a` **actually recompiles all five complete original physical
  TUs changed in this session simultaneously**, through two independent
  original TC4 4.02 and complete normal MAIN TLINK rounds: full Yumemi
  and Kotohime **Extra Attack** controllers, the full **Rikako major
  BOSS**, complete Rikako Chargeshot/Gauge and the shared far-Pascal
  volatile-VSYNC frame-delay leaf. Every **5,728 original CODE byte,
  541 ordered native OMF FIXUPPs and 33 PUBLICs**, complete source/
  ABI/segment dependencies, normal MAIN EXE/MAP, all **124,642 Japanese
  loaded program bytes and 1,553 original MZ relocations** match in
  both rounds. Independent standard DOS MZ serialization matches all
  130,882 original Japanese MAIN.EXE bytes. The **94 other unchanged
  game project objects and CRT were reused**, no cold replay. See
  [after865 five-source integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER865_REVIEW.md).
- `af859a`, `af853a`, `af847a`, `af842a`, `af835a` remain separately
  current-source-bound read-only passes for their own other original
  physical owners. Earlier `af825d` (Rikako BOSS), `af750d`
  (Kotohime Extra Attack) and `af740c` (VSYNC leaf) were real original
  native proofs but are now *historical source snapshots*; preserve
  old receipts and require current hashes. Never claim a fabricated
  multi-scope cold build or count historically covered CODE as new
  distinct Factory packed-game acceptance.

## After864: original TH02/TH03 shared volatile VSYNC wait leaf

- Small original **`frmdely1` 21-byte** far-Pascal VSYNC leaf now uses
  an ordinary C++ `while` poll of the real **volatile unsigned 16-bit**
  interrupt-updated counter against the signed `int` duration, with
  authentic old-TC4-compatible compile-time word-width checks.
- Fresh genuine native negatives: swapping comparison operand order
  emitted **22** instead of original **21** CODE bytes (`af864b`),
  and forcing the counter to signed emitted different 21-byte CODE
  (`af864c`). Final `af864d` passes **two independent original
  TC4/full normal MAIN TLINK rounds**, 21 CODE bytes, two ordered
  fixups, one PUBLIC, original loaded Japanese MAIN and all **1,553
  MZ relocations**; 98 other project objects/CRT reused. See
  [after864 native VSYNC wait review](MAIN_FRAME_DELAY_NATIVE_WHILE_AFTER864_REVIEW.md).
  Historical shared source owner; no new distinct/Factory byte credit.

## After863: complete Rikako Chargeshot/Gauge native four-orbit controller

- The complete 11-function `cs_rika` owner now uses natural C++ `while`
  for **four-shot allocation, signed polar orbit update, and rendering**,
  with physically named initial angle/radius, signed ±8 rotation, hit
  margin and 32×32 sprites. The core signed-index parity can become
  natural `%2` only **after explicit unsigned promotion** (native
  `af863e`); signed `%2` fails (`af863d`: **1,287** vs **1,280** CODE).
- Fresh TC4 negative `af863g` showed a prefix byte frame increment
  generated **1,294** CODE bytes instead of original 1,280; postfix
  remains. Final `af863h` compiles/links all original 11 functions in
  two independent original TC4 4.02/full normal TLINK rounds: **1,280
  CODE bytes, 137 ordered OMF FIXUPPs, 11 PUBLICs**, full original
  Japanese MAIN/1,553 relocations exact; 98 other project objects/CRT
  reused, no cold replay. See
  [after863 full Rikako Chargeshot review](MAIN_RIKAKO_CHARGESHOT_LOOPS_AFTER863_REVIEW.md).
  Existing historical owner; no added unique CODE/Factory packed credit.

## After862: complete Rikako BOSS native emitter and renderer loops

- The full eight-function **Rikako major BOSS** (`ba_rikak`) now uses
  natural C++ `while` loops for **both attack ring emitters, eight-sprite
  main and sixteen-sprite intro renderers**, preserving original
  signed 256-angle division, RNG consumption and call ordering.
  Byte +0x20/+0x10 sprite angles, real subpixel orbit radius, four
  pellet volleys/speed increase and opposite half-turn are native-exact
  named C++ values.
- Fresh TC4 negative controls independently confirmed that replacing
  binary zero-minus `angle=(0-angle)` with unary negation produces
  **1,674** vs original **1,677** CODE (`af862d`), and plain signed
  `i %4` in place of explicit `(unsigned int)i %4` produces **1,684**
  (`af862f`). Both original compiler-sensitive semantics remain.
  Final `af862g` passes **two independent actual TC4/complete normal
  MAIN TLINK rounds** with **1,677 CODE bytes, 215 ordered native
  FIXUPPs, 8 PUBLICs**, full Japanese MAIN/1,553 MZ relocations exact.
  98 other project objects/CRT reused, no cold replay. See
  [after862 full Rikako BOSS review](MAIN_RIKAKO_BOSS_NATIVE_LOOPS_AFTER862_REVIEW.md).
  Already covered original owner; no duplicate unique CODE/Factory credit.

## After861: complete Kotohime Extra Attack emitter and render traversals

- The eight-function original `ex_koto` source now uses natural `while`
  loops for **both four- and ten-shot ring emitters** and the ten-entity
  renderer, keeping the exact bullet/byte-angle/postcall ordering.
  Named target RNG ranges, ordinary/special flight speeds, signed
  ±12/±7 ring angles, 12-pixel stripe, collision radius and 2-subpixel
  speed rise are all native exact in actual TC4.
- `af861e` genuinely **failed** original byte CODE when replacing
  mutable event counter `p->angle++` with prefix (1,059 vs original
  **1,054**); `af861f` likewise rejected replacing `p->y += radius`
  with explicit assignment (1,057). Final `af861g` recompiles the
  complete original source in **two genuine TC4 4.02/normal full MAIN
  TLINK rounds**: **1,054 CODE bytes, 100 ordered original FIXUPPs,
  8 PUBLICs**, exact Japanese MAIN/1,553 relocations; 98 unchanged
  original game objects/CRT reused. See
  [after861 Kotohime Extra Attack review](MAIN_KOTOHIME_EXATT_NATIVE_LOOPS_AFTER861_REVIEW.md).
  Historically covered physical CODE; no new unique/Factory accepted credit.

## After860: full Yumemi Extra Attack active beam and four raster loops

- The **entire five-function `ex_yume` original physical owner** now
  renders the active beam's four signed-step sprite perimeter strips
  through normal `while` loops; original 8+8 entity slots, distinct
  16-bit clip rectangles, radius/hitbox phase, RNG target offsets and
  launch speed are source-native exact.
- Genuine original TC4 rejected signed-char `extent /2` → `>>1`
  (`af860c`: **1,690** instead of original **1,696** CODE bytes),
  signed `top /2` → `>>1` (`af860d`: also 1,690), and byte
  `p->frame++` → `++p->frame` (`af860e`: 1,701). Original arithmetic
  and postfix remain. Final `af860g` passes two genuine original
  TC4 4.02/complete normal TLINK rounds: **1,696 CODE bytes, 87
  ordered native OMF FIXUPPs, five PUBLICs**, complete original Japanese
  MAIN and all 1,553 MZ relocations. 98 other project objects/CRT
  reused, no cold replay. See
  [after860 Yumemi Extra Attack review](MAIN_YUMEMI_EXATT_BEAM_AFTER860_REVIEW.md).
  Previously source-covered CODE; no duplicate unique byte/Factory credit.

## Latest after859: five session-edited full original physical sources together

- Actual original `af859a` **recompiles the five complete original
  physical C++ TUs changed in this session together**, in two independent
  genuine TC4 4.02 and complete normal MAIN TLINK rounds: 10-function
  Ellen Chargeshot/Gauge, nine-function **Mima major BOSS**, 10-function
  Yumemi Chargeshot/target/Gauge, five-function player effects renderer
  and the small native Extra Attack callback leaf.
- Both native compiler/normal TLINK rounds match **all 5,766 original
  CODE bytes, 614 literal ordered native FIXUPP fields, 35 PUBLICs**,
  original source dependency/segment ABI, complete normal MAIN EXE/MAP,
  **124,642 Japanese loaded bytes and 1,553 ordered MZ relocations**.
  Independent standard MZ serialization matches the full 130,882-byte
  original Japanese file. **94 unchanged original game project objects
  and CRT reused**, no full cold replay. See
  [after859 five-original-source integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER859_REVIEW.md).
- Read-only reviews of **separate**, unchanged physical source scopes
  `af853a`, `af847a`, `af842a`, `af835a` still pass current checkout.
  Freshly rechecked `af782a`, `af775a`, `af766a`, `af829a`, `af823a`
  **fail present source-hash binding** and are *historical original native
  evidence*, not current-source passing receipts. Do not weaken guards,
  pretend these were built simultaneously, double-count old CODE or
  advertise canonical Factory packed-game acceptance. The `input_s`
  single-NOP historical parent linker gap remains separately open.

## After858: original Extra Attack callback leaf and signed 16-bit ABI

- Small original `p_exatt` owner now uses two immutable `const subpixel_t`
  local copies from its original Subpixel wrapper arguments, a natural
  `if(pid == 0)` character callback selection, and TC4-compatible
  typedef checks for signed 16-bit coordinates and byte player IDs.
- Independent original TC4 negatives: direct wrapper-field callback
  arguments emitted **50** vs **41** original CODE bytes (`af858c`);
  reversing the player branches changed original CODE at equal size
  (`af858d`). Retained two 16-bit locals and original far Pascal
  callback order. Final `af858e` passes two actual original TC4/normal
  MAIN TLINK rounds: **41 CODE bytes, 2 literal ordered FIXUPPs, 1
  PUBLIC**, complete original Japanese MAIN and 1,553 ordered MZ
  relocations; 98 other objects and CRT reused. See
  [after858 Extra Attack leaf review](MAIN_EXATT_ABI_LEAF_AFTER858_REVIEW.md).
  Existing source owner; not new unique CODE or Factory packed credit.

## After857: exact quad player-effects renderer and physical clip/radius geometry

- Complete five-function `effects` original source now renders its
  four-vertex BOSS explosion axis from a natural typed `while` loop,
  preserves four explicit GRCG lines and original post-call byte angle
  advancement. Named two player clip rectangles, full-screen clip and
  signed circle/center/axis radius-delta pairs are native exact.
- Fresh TC4 rejects enum-valued live byte `angle +=64` (**627** vs 628
  CODE bytes, `af857b`), and signed circle Y `/2` instead of original
  arithmetic `>>1` (**631** vs 628, `af857d`). Both originals restored.
  Final `af857g` passes two original TC4/full normal MAIN TLINK rounds:
  **628 CODE bytes, 33 literal ordered FIXUPPs, 5 PUBLICs**, original
  Japanese loaded MAIN and 1,553 ordered MZ relocations. 98 other game
  objects/CRT reused. See
  [after857 player effects review](MAIN_EFFECTS_QUAD_NATIVE_AFTER857_REVIEW.md).
  Historical source-owned CODE, not new unique/Factory accepted credit.

## After856: complete Yumemi Chargeshot/target and sixteen-sprite rings

- Full ten-function `cs_yume` source now expresses the sixteen-sprite
  ring's dual byte-angle/index traversal as a natural **C++ `while`**,
  names actual signed target fallback/formation biases, narrow versus
  56-pixel blooming hitboxes, flight speed, center offset and the byte
  Gauge's original `%8` cadence. The natural `if(!(byte_frame % 8))`
  expression passed genuine original TC4 with the full gauge jump table.
- Genuine failed compiler forms: naming a live `angle += 16` byte
  increment changed original CODE at offset 615 (`af856b`); replacing
  renderer `frame &1` with byte `%2` emitted **1,651** vs **1,645**
  CODE bytes (`af856d`). Both original byte forms remain. Final
  `af856h` passes two original TC4/full normal MAIN TLINK rounds:
  **1,645 CODE bytes, 133 literal ordered native FIXUPPs, 10 PUBLICs**,
  whole original Japanese MAIN and all 1,553 ordered MZ relocations;
  98 other project objects/CRT reused, no cold replay. See
  [after856 Yumemi Chargeshot review](MAIN_YUMEMI_CHARGESHOT_RING_AFTER856_REVIEW.md).
  Historical source owner reverified, no additional unique CODE or
  canonical Factory packed credit.

## After855: entire Mima major BOSS signed/unsigned native angles

- Full nine-function `ba_mima` major BOSS uses natural unsigned `if(!(boss_frame
  %2))` for three attack clocks, named side-bomb/center geometry,
  mirrored intro mask/split radius, and real 16-bit sprite keyframes.
  Crucially, **Mima's byte-angle +9, +3 and +0x80 updates do accept named
  native-exact C++ values**, unlike some other character BOSS cases.
- Genuine original TC4 negative controls: merging mode-5 `goto` into
  mode-2 C++ branch made **1,924 vs original 1,922 CODE bytes** (`af855b`);
  widening the **byte** trail modulo local made 1,900 (`af855d`). Both
  original compiler-sensitive behaviors retained. Final `af855i` proves
  entire **1,922 CODE bytes, 277 ordered native FIXUPPs, 9 PUBLICs**,
  complete original Japanese MAIN and 1,553 ordered MZ relocations in
  **two independent original TC4/full normal TLINK rounds**; 98 other
  objects and CRT reused. See
  [after855 Mima BOSS review](MAIN_MIMA_BOSS_NATIVE_ANGLE_AFTER855_REVIEW.md).
  Historical source owner reverified, not new distinct CODE/Factory credit.

## After854: complete Ellen Chargeshot/Gauge byte-state reconstruction

- Full ten-function `cs_ellen` module (64 physical 12-byte records) now
  has explicit native -110-subpixel homing target offset, -8 clip
  margin, original 0x10 sprite angle bias, separately evaluated 5/1
  cel shifts and naturally true-valued Gauge entrypoint checks.
- Genuinely failed original TC4 alternatives: collapsed byte cel shifts
  produced 1,528 vs original 1,530 CODE (`af854a`); replacing the
  original `goto active` scan with `break` grew to 1,534 (`af854b`);
  splitting byte predecrement gave 1,527 (`af854c`); inverted sprite
  loop gave 1,526 (`af854f`). All original codegen-sensitive layouts
  were restored, not patched. Final `af854g` passes both original
  TC4/full normal MAIN TLINK rounds: **1,530 CODE bytes, 169 ordered
  native FIXUPPs, 10 PUBLICs**, original Japanese loaded MAIN and all
  1,553 ordered MZ relocations. 98 other original game objects/CRT
  reused, no cold replay. See
  [after854 Ellen Chargeshot review](MAIN_ELLEN_CHARGESHOT_CODEGEN_AFTER854_REVIEW.md).
  Historical source-owned bytes, not new unique CODE or Factory credit.

## Latest after853: six modified original MAIN physical owners rebuilt together

- Genuine original `af853a` **simultaneously recompiles all six physical
  source owners changed in this session** in two independent TC4 4.02
  plus full normal MAIN TLINK rounds: full Yumemi **major BOSS**, both
  Combo HUD/BOSS helper slots, complete seven-function Warning, original
  55-byte Gauge saturation leaf and full six-entity Mima Extra Attack.
  Five current maintained C++ sources map to six real linker objects.
- All **5,678 original CODE bytes, 570 literal ordered native FIXUPPs,
  27 PUBLICs**, original segment and current-source OMF dependencies,
  full normal MAIN EXE/MAP, **124,642 Japanese loaded bytes and 1,553
  ordered MZ relocations** match in both real compiler/linker rounds.
  Independent standard MZ serialization matches all 130,882 Japanese
  file bytes. **93 other unchanged original project objects and CRT
  reused**, no full cold replay. See
  [after853 six-source integration](MAIN_SIX_SOURCE_INTEGRATION_AFTER853_REVIEW.md).
- Checked source provenance now: separate `af847a`, `af842a`, `af835a`
  read-only reviews still **pass** current source. Older `af829a` and
  `af827a` now **fail current-source hash checks** after the Yumemi
  BOSS edit (and `af823a` was already historical after Reimu changed).
  Preserve their genuine historical receipts; never weaken source guards,
  claim one invented all-object compile, double-count original CODE
  as new unique bytes or grant canonical Factory acceptance.

## After852: full Mima Extra Attack native unsigned parity recovery

- The complete four-function original `ex_mima` Extra Attack now uses
  a **real natural unsigned `%2`** on the explicitly promoted signed
  16-bit elapsed-duration local. This preserves TC4's original low-bit
  acceleration/8-bit speed mutation; signed `%2` is **not** equivalent
  native CODE and compiled 725 vs original 727 bytes (`af852b`).
- Original 0x1200 random target range, initial speed, hitbox and bounce
  geometry are now named, with compile-time 32-byte entity stride
  proof. `af852d` also rejects `0 - velocity_x` in place of native
  unary negation. Final `af852e` passes two actual original TC4/complete
  MAIN TLINK rounds: **727 CODE bytes, 44 literal ordered FIXUPPs,
  4 PUBLICs**, full Japanese MAIN and all 1,553 MZ relocations exact.
  98 other original objects/CRT reused, no cold replay. See
  [after852 Mima Extra Attack review](MAIN_MIMA_EXATT_UNSIGNED_MODULO_AFTER852_REVIEW.md).
  Previously covered original physical CODE, no new distinct/Factory credit.

## After851: original 55-byte Gauge saturation leaf

- The complete `p_gauge` Gauge charge leaf merges the native original
  Hyper/full-gauge early return into natural C++ `||` and now has
  historical TC4-compatible file-scope typedef checks for **16-bit
  Gauge, 8-bit charge and 0xFF0 saturation**. The original compound
  memory `+=` and strictly `>GAUGE_MAX` clipping are left exact.
- Genuine original TC4 negative controls: explicit `= old+charge`
  generated 58 rather than original 55 CODE (`af851b`); mathematical
  `>=MAX+1` changed CODE (`af851c`); global `static_assert` was not
  accepted by the old compiler (`af851d`). Final `af851e` passes two
  real TC4/complete MAIN TLINK rounds: **55 CODE bytes, one ordered
  native FIXUPP, one PUBLIC**, full Japanese loaded MAIN and 1,553
  MZ relocations; 98 other objects and CRT reused, no cold replay.
  See [after851 Gauge ABI review](MAIN_GAUGE_NATIVE_SATURATION_AFTER851_REVIEW.md).
  Previously covered source owner; no new unique CODE/Factory credit.

## After850: full warning/Gauge/portrait and palette controls

- The full seven-function original `warning` owner now omits redundant
  unsigned casts on four **16-bit word-frame `%2`** checks, uses two
  natural C++ `for` key-release polling loops and a zero-truth Gauge
  brightness test, with original named 27-frame flash/row/tones.
- Fresh original TC4 negatives: removing unsigned promotion from a
  **byte** warning flag `%2` grew the original CODE to **1,569** vs
  **1,560** (`af850d`); naming four live byte brightness `+=/-=`
  constants generated **1,521** bytes (`af850f`). Restored exact
  byte operations. Final `af850h` passes two original TC4/full normal
  MAIN TLINK rounds: **1,560 CODE bytes, 125 ordered native FIXUPPs,
  7 PUBLICs**, original Japanese MAIN and all 1,553 relocations exact.
  98 other objects/CRT reused, no cold replay. See
  [after850 full warning/Gauge review](MAIN_WARNING_GAUGE_NATIVE_AFTER850_REVIEW.md).
  Existing source owner; no additional unique CODE or canonical credit.

## After849: complete Combo HUD and BOSS/Panic helper source

- The two complete original physical Combo objects (`p_combo`,
  `p_cmbhl`) now use **natural unsigned 16-bit `%4`** for the four-frame
  HUD blink and a shared decimal-radix constant for two-digit rendering.
  The original bitwise `&` between independent blink predicates,
  32-bit bonus saturation/rounding, near-segment Fireball call and
  16-bit BOSS/Panic ABI stay intact.
- Fresh genuine TC4 negative controls: `af849c` 32-bit bonus ternary
  generated 493 vs original 491 CODE bytes; `af849d` moving pointer
  initialization changed CODE; `af849f` direct Fireball C++ call
  emitted far `9A` instead of target `90 0E E8`. All rejected.
  Final `af849g` passes two original TC4/full normal MAIN TLINK rounds:
  **978 CODE bytes, 57 ordered FIXUPPs, 5 PUBLICs**, original Japanese
  MAIN and all 1,553 MZ relocations exact. 97 other objects/CRT reused,
  no cold replay. See [after849 Combo review](MAIN_COMBO_HUD_NATIVE_AFTER849_REVIEW.md).
  Existing source owner; no additional unique CODE or canonical credit.

## After848: full Yumemi BOSS native four-stage raster control

- The complete `ba_yumem` BOSS now expresses **all four original entrance
  raster loops** as natural signed-step `while` sweeps and the main render
  no-effect condition as `!(effect || frame)`; original signed chase
  boundaries and four independent cross-ring offsets are named.
- Actual negative TC4 trial `af848d` proved an equivalent inverted
  chase-X early exit changes original CODE. `af848a/b/c` successively
  proved natural loops/condition; final `af848e` passes two original
  TC4/full normal TLINK rounds: **2,358 CODE bytes, 343 ordered native
  FIXUPPs and 10 PUBLICs**, full original Japanese loaded MAIN and
  all 1,553 ordered MZ relocations exact. 98 unchanged original
  project objects/CRT reused, no cold replay. See
  [after848 full Yumemi BOSS review](MAIN_YUMEMI_BOSS_RASTER_CONTROL_AFTER848_REVIEW.md).
  Historically covered source, not new unique CODE/canonical credit.

## Latest after847: seven current original physical Enemy/Fireball/Reimu/Explosion sources

- `af847a` genuinely **recompiled seven current changed physical
  original TUs together**, not an arithmetic union: four original
  Enemy source partitions (formation, full ENEDAT VM, update and
  collision), full Fireball, full **Reimu major BOSS** and original
  explosion-chain collision/bonus. Two independent original TC4 4.02
  / complete normal MAIN TLINK rounds match **7,530 CODE bytes,
  656 literal ordered native FIXUPPs, 39 PUBLICs**, original source
  and segment ABI, full normal MAIN EXE/MAP, **124,642 Japanese loaded
  bytes and all 1,553 ordered MZ relocations**. Independent standard
  MZ serialization reproduces all 130,882 bytes. **92 unchanged game
  objects and CRT reused, no full cold replay**. See
  [after847 seven-original-object integration](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER847_REVIEW.md).
- Later current-checkout boundary: `af842a` and `af835a` still pass
  live-source review; `af829a` is historical after the Yumemi edit,
  while old `af823a` is also **historical source
  evidence only** after the current `ba_reimu` source change: its
  read-only source hash check now **fails**, as expected. The new
  `af847a` proves the *current* Reimu source. Do not alter old receipts,
  claim a fictitious combined all-object replay, double-count previously
  owned CODE or promote canonical Factory packed-game acceptance.

## After846: full explosion collision/chain/bonus original source

- Complete 630-byte `e_expl` collision owner now names original signed
  bonus, enemy/pellet/red-blue score, 255-saturating 8-bit hit count,
  and exact four-region 2/5/2/2 progressive chain charge values.
  These are current C++ semantics, not a replacement for the original
  multi-stage signed bonus arithmetic.
- Actual original TC4 negative controls: byte `%4` replacing the hit
  clock mask failed (**639** vs 630 original CODE, `af846a`), and
  `hits !=0xFF` replacing `hits <255` also changed original CODE
  (`af846b`). Both originals stay. Final `af846e` fully compiles/links
  in two original TC4/normal MAIN TLINK rounds with **630 CODE bytes,
  49 ordered native FIXUPPs, one PUBLIC, full Japanese original MAIN
  and 1,553 ordered relocations** exact. 98 other project objects and
  CRT reused; no cold replay. See
  [after846 explosion-chain review](MAIN_EXPLOSION_CHAIN_NATIVE_AFTER846_REVIEW.md).
  Previously covered owner, not additional unique byte or Factory credit.

## After845: full Reimu major BOSS native word clocks and byte sprite masks

- The complete `ba_reimu` BOSS now uses natural unsigned-16-bit
  `boss_frame % 2` cloud acceleration and `%16` mirrored barrage clocks;
  named physical ring angles/radii, four-frame renderer divisor and
  original intro scale are source-bound. The four separate **byte**
  `anim &3` checks cannot use `%4`: fresh `af845b` candidate grew
  from original **2,020 to 2,044 CODE bytes**, so all masks were restored.
- Final `af845d` genuinely compiles/links the entire full BOSS twice
  with original TC4 4.02/normal TLINK and matches **2,020 CODE bytes,
  270 ordered FIXUPPs, 9 PUBLICs**, full Japanese MAIN and all
  1,553 MZ relocations. 98 other game objects/CRT reused, no cold
  replay. See [after845 full Reimu BOSS review](MAIN_REIMU_BOSS_FRAME_NATURAL_AFTER845_REVIEW.md).
  Existing source owner, no additional unique CODE or Factory credit.

## After844: complete original Fireball controller native timing

- The full 576-line `e_fireb` owner now uses **natural unsigned `%512`**
  for its 16-bit global targeting cycle and named 12/14/32/36-frame
  sprite/hit/fade/expiry phases, while retaining the original **byte**
  `&7` animation cycle and the two-step falling coordinates.
- Genuine original TC4 counterexamples: byte `%8` in place of the
  sprite mask (`af844b`), rewriting `<=3` as `<4` (`af844c`), and
  coalescing `next=x; next+=vx` (`af844e`) all changed CODE and were
  reverted. Final `af844f` passes two original TC4/normal TLINK
  rounds with **1,555 CODE bytes, 115 ordered native FIXUPPs,
  ten PUBLICs**, full Japanese MAIN and all 1,553 ordered relocations.
  98 other original project objects and CRT reused, no cold replay.
  See [after844 full Fireball review](MAIN_FIREBALL_NATIVE_TIMING_AFTER844_REVIEW.md).
  Already covered physical source, no extra distinct byte credit.

## After843: full 1,049-line Enemy formation and VM current-source recovery

- All **four original physical Enemy TUs** (`eforna`, `efornb`, `eupda`,
  `eupdb`) were genuinely compiled together from maintained `enemy.cpp`.
  Its ENEDAT loader now uses a natural `for(;;)` and `!enemy_count`
  sentinel; the formation-spawn loop has original dual byte/word
  post-call increments expressed naturally as C++ `for`.
- New original-compiler negative controls confirm that flattening the
  VM's `EO_MOVE` branch (`af843c`), converting RNG `do/while` to
  `for/break` (`af843d`) and duplicating the `clip` early return
  (`af843f`) do **not** reproduce original TC4 instructions, so the
  originals remain. Final `af843g` proves **3,325 CODE bytes, 222 literal
  ordered OMF FIXUPPs, 19 PUBLICs**, full Japanese MAIN and all 1,553
  relocations exact in **two independent TC4/full normal TLINK rounds**.
  95 other objects/CRT reused, no cold replay. See
  [after843 full Enemy review](MAIN_ENEMY_FORMATION_NATIVE_AFTER843_REVIEW.md).
  This is previously source-owned CODE, not additional unique credit.

## Latest after842: six modified original physical sources in one exact normal MAIN link

- `af842a` **simultaneously compiles all six changed original physical
  objects** in two independent original Turbo C++ 4.02 and complete
  normal TLINK rounds: full Kana major BOSS, both shared BOSS carriers,
  the whole CPU AI, complete input modes and full Kana Chargeshot/Gauge.
  Five current modified maintained C++ files map onto six original
  physical project TUs; no fake sum of individual passes is substituted.
- Every **5,558 original CODE bytes, 619 literal ordered native FIXUPPs,
  39 PUBLICs**, original source/segment ABI, full original MAIN EXE/MAP,
  all **124,642 Japanese loaded bytes and 1,553 ordered MZ relocations**
  match in both real native rounds. Independent standard MZ serialization
  matches all 130,882 original Japanese file bytes. **93 unchanged game
  objects and CRT reused**, no whole cold replay. Protected report:
  [after842 six-object native integration](MAIN_SIX_SOURCE_INTEGRATION_AFTER842_REVIEW.md).
- `af840a` and `af835a` still pass current source checks; `af829a`
  is now historical after the Yumemi source edit, and `af823a` was
  already historical after the Reimu BOSS edit.
  **Do not claim** they were all rebuilt together or add covered bytes
  again to unique CODE ownership. Canonical packed-file Factory
  acceptance and the BIOS `input_s` single-NOP link gap remain open.

## After841: complete Kana Chargeshot/Gauge native geometry

- The full nine-function `cs_kana` owner now names its four true
  reverse-initialized 13-point beam trajectories, four-sample collision
  step, sprite cel stride and original signed subpixel hit margin.
  A fresh native experiment `af841c` tested byte `%64` against widened
  `unsigned int &63` and **failed** (1,288 vs original 1,291 CODE bytes);
  the original modulo remains. Final `af841e` passes two original
  TC4/TLINK rounds: **1,291 CODE bytes, 117 literal ordered fixups,
  9 PUBLICs**, whole Japanese MAIN and all 1,553 relocations. 98
  other objects/CRT reused, no cold replay. See
  [after841 Kana Chargeshot review](MAIN_KANA_CHARGESHOT_GEOMETRY_AFTER841_REVIEW.md).
  Previously covered native owner, not new unique CODE or Factory credit.

## Latest after840: five edited original physical objects in one native MAIN link

- `af840a` **actually recompiles the five complete original physical
  objects edited in after836–839 simultaneously**, across two independent
  original TC4 4.02 and complete normal TLINK rounds: full Kana BOSS,
  two shared BOSS carrier objects, complete CPU AI and all input modes.
  Four maintained source files map to five historical physical objects.
- All **4,267 CODE bytes, 502 literal ordered OMF FIXUPPs and 30 PUBLICs**,
  source/compiler dependencies and segment geometry, complete original
  MAIN EXE/MAP, **124,642 Japanese loaded bytes and 1,553 MZ relocations**
  match in both rounds. Independent standard DOS MZ serialization matches
  all 130,882 Japanese file bytes. **94 unchanged original game objects
  and CRT reused**, no cold replay. See
  [after840 five-object integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER840_REVIEW.md).
- Independent `af835a` remains current source-bound; `af829a` is
  historical after the Yumemi edit, while `af823a` was current at its
  earlier checkpoint but is historical after `ba_reimu` changed. No fictitious combined replay. No overlap
  double-counted as new distinct CODE or canonical Factory acceptance.

## After839: complete input modes and native press/release wait

- The nine-function original `inp_m_w` input-mode physical owner now
  expresses press-phase `input_wait_for_change` as natural C++ `for`,
  keeping release phase, signed timeouts, joystick reads and 9999 sentinel.
- Actual compiler negative controls `af839b` (combined Cancel/OK mask
  360 vs original 367 CODE bytes) and `af839c` (inline `input_t&`
  joystick helper 375 bytes) were reverted. The exact macro expansion
  and short-circuit tests remain. Final `af839d` passes two original
  TC4/full normal MAIN TLINK rounds: **367 CODE bytes, 58 ordered OMF
  fixups, 9 PUBLICs**, full Japanese loaded image and 1,553 relocations;
  98 other objects/CRT reused. See
  [after839 input mode review](MAIN_INPUT_MODES_NATIVE_WAIT_AFTER839_REVIEW.md).
  Existing owner; no new distinct byte or canonical Factory credit.

## After838: complete CPU collision avoidance and pursuit controller

- The full four-function `p_cpu` AI object now uses natural `for(;;)`
  collision/retry control and explicitly named original 16-bit collision
  bands, four-frame scan, floor escape and three-column strategy stride.
  `af838b` ternary hit-test (1,081 vs original 1,077 CODE bytes) and
  `af838d` ternary direction bit flag (1,073 vs 1,077) were genuine
  negative compiler trials, both restored. Final `af838e` passes two
  original TC4/TLINK rounds: **1,077 CODE bytes, 64 ordered FIXUPPs,
  4 PUBLICs**, full Japanese MAIN and 1,553 relocations exact. 98 other
  objects/CRT reused, no cold replay. See
  [after838 complete CPU AI review](MAIN_CPU_RETRY_NATIVE_CONTROL_AFTER838_REVIEW.md).
  Historical source owner reverified, not additional unique CODE.

## After837: full shared BOSS movement, template and pattern selector

- The original shared BOSS source's **two physical owners** (`ba_sring`
  and `ba_srest`) now use natural `if/else if` horizontal turns and
  `for(;;)` random-pattern rejection with explicit `break`, both proven
  exact in real TC4 and complete normal TLINK. The 24-sprite ring,
  32-byte template ABI and RNG order are unchanged; original sprite,
  score, radius and target offsets are named semantic constants.
- Fresh negatives: `length=length*8` changed ring CODE (`af837c`);
  direct C++ 32-byte struct copy changed original 601-byte `ba_srest`
  to 597 bytes (`af837d`). Both are rejected. Final `af837e` passes
  **949 original CODE bytes, 106 ordered FIXUPPs, 8 PUBLICs**, complete
  Japanese MAIN and all 1,553 relocations in two original TC4/TLINK
  rounds; 97 other objects and CRT reused, no cold replay. See
  [after837 BOSS shared review](MAIN_BOSS_SHARED_NATURAL_CONTROL_AFTER837_REVIEW.md).
  Existing owners, no new unique CODE or canonical Factory credit.

## After836: complete Kana major BOSS natural C++ clocks

- The complete `ba_kana` BOSS now expresses both its unsigned-16-bit rotating
  volley tick and intro animation index as natural `%4`, while naming the
  accelerated ring's four separate angles, rotating ring count and intro
  radius. `af836c`'s natural cloud-angle subtraction failed original CODE,
  so exact native `SUB AL,10h` remains. Final `af836d` passed two actual
  original TC4/TLINK rounds: **1,874 CODE bytes, 274 ordered native
  FIXUPPs, 9 PUBLICs**, complete Japanese MAIN and 1,553 relocations.
  98 other objects/CRT reused, no cold replay. See
  [after836 Kana BOSS review](MAIN_KANA_BOSS_NATIVE_MODULO_AFTER836_REVIEW.md).
  Existing native source owner; no new unique CODE credit.

## Latest after835: five full modified physical source owners built together

- `af835a` **actually compiled all five original physical TUs modified
  this session in each of two independent original TC4 4.02 rounds**:
  full Marisa/Ellen **major BOSSes**, full Bullet simulation/render/
  GRCG engine, the exact signed-Q8 `polar` leaf and direct PMD `snd_se`
  source. Both complete normal MAIN TLINK rounds matched **all 5,937
  CODE bytes, 626 literal ordered native FIXUPPs, 41 PUBLICs**, original
  BSS/segment/source dependencies, full normal MAIN EXE/MAP, all
  **124,642 Japanese loaded bytes and 1,553 ordered MZ relocations**.
  Independently serialized original Japanese MZ also matches all
  **130,882 bytes**; 94 other original project objects and CRT reused,
  **no full cold replay**. See
  [after835 five-original-source integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER835_REVIEW.md).
- Earlier simultaneous `af829a` (four original TUs) had an authentic
  compiler proof then, but has a historical Yumemi source snapshot now;
  `af823a` (nine TUs) has a historical Reimu source snapshot. **Do not combine these into a
  claimed simultaneous eighteen-object build.** Historical exact covered
  bytes from these scopes cannot be counted again as unique ownership or
  canonical packed-file Factory acceptance. The original `input_s` one-NOP
  historical parent blocker remains unresolved.

## After834: direct original PMD sound-effect service leaf

- Complete original two-function `snd_se` owner now issues the original
  `AH=PMD_SE_PLAY`, `AL=current effect`, fixed `INT 0x60` **directly**
  from natural `snd_se_update`, removing an unnecessary unsigned-byte
  reference helper. The original 8-bit priority/preemption/expiration
  ordering and byte-frame postfix mutation are preserved.
- Real TC4 `af834a` proves the direct hardware call; `af834b` **rejects**
  reversed but semantically equivalent priority operands (121 candidate
  vs 120 original CODE bytes). Final `af834d` proves the exact current
  source: **120 CODE bytes, 18 ordered fixups, two PUBLICs**, entire
  original MAIN and all 1,553 ordered MZ relocations in two native
  original TC4/TLINK rounds. 98 other objects/CRT reused, no cold replay.
  See [after834 PMD SE review](MAIN_SOUND_PMD_DIRECT_AFTER834_REVIEW.md).
  Existing source owner, not extra unique CODE or Factory packed credit.

## After833: signed-Q8 original polar leaf exact ABI

- The 26-CODE-byte original far-`__cdecl` signed `polar` leaf now explicitly
  casts its **16-bit returned coordinate**, retaining the signed 32-bit
  multiply and genuine TC4 **arithmetic Q8 shift**. Two original native
  positive source trials passed (`af833a/b`).
- A real TC4 trial `af833c` replaced `>>8` with signed `/256` and **failed**
  (33 vs original 26 CODE bytes); negative products round differently.
  The divide was rejected. `af833d` recompiles the final current source
  in two original TC4/normal full MAIN TLINK rounds: 26 CODE bytes,
  zero native OMF fixups, one PUBLIC, original Japanese image and all
  1,553 MZ relocations exact, 98 other project objects/CRT reused.
  See [after833 signed-Q8 polar review](MAIN_POLAR_SIGNED_Q8_AFTER833_REVIEW.md).
  Existing CODE owner reverified, no unique-byte or canonical credit.

## After832: complete Bullet engine source-native trail loop

- `bullet` is an original **1,080-line full physical TC4 TU** with the
  large projectile spawn/update/render controllers and original 386 GRCG
  pellet writer. Its **16×16 trail history `while`** now uses natural
  typed `for(; trail_i>0; (trail_i-=step, so-=cel))` with original sprite
  ordering. Genuine original compiler codegen matches all original bytes.
- `af832b` tested the separate 8×8 pellet `do/while` as a `for` and
  **failed** complete original CODE (2,687 vs 2,685); `af832c`
  challenged GRCG source `_SI &= mask` with `%` and also **failed**
  (2,704). Both original forms remain; final `af832d` passes two
  original TC4/whole normal TLINK rounds on the complete TU: **2,685
  CODE bytes, 196 ordered FIXUPPs, 20 PUBLICs**, full original Japanese
  MAIN and all 1,553 original relocations. 98 other objects and CRT
  reused, no cold replay. See
  [after832 complete Bullet renderer review](MAIN_BULLET_RENDER_TRAIL_AFTER832_REVIEW.md).
  Existing original CODE owner, no new unique byte credit.

## After831: complete Ellen BOSS radial/strip source

- Full nine-function `ba_ellen` major BOSS uses named 256-unit signed-
  division Extra Attack radial emission, original opposite byte Pascal
  mode arguments, nine-entry sprite-strip cycle and four-frame renderer,
  without merging the three original drawing calls or signed table math.
- Three actual native rejected experiments: `af831a` combined `--i`/
  test and generated **1,667** vs original **1,675** CODE bytes;
  `af831b` shifted a signed table height instead of dividing (1,672);
  `af831c` replaced byte-angle `+=0x20` with enum-valued 0x20 (1,671).
  The exact original formulations remain. `af831d` recompiles the
  entire final source **twice with original TC4 + full normal TLINK**:
  1,675 CODE bytes, 213 ordered fixups, nine PUBLICs, whole Japanese
  game and all 1,553 MZ relocations exact. No cold replay, no new
  unique CODE credit. See
  [after831 Ellen BOSS review](MAIN_ELLEN_BOSS_CYCLE_AFTER831_REVIEW.md).

## After830: full Marisa BOSS original native unsigned C++ clocks

- Complete `ba_maris` nine-function major BOSS now uses natural `%4`
  spread period, `%32` rotating-ring period and unsigned `%4` render
  flicker, with named wide/narrow 16-bit columns and split entrance
  geometry, preserving distinct release times, RNG and mask sprite I/O.
- `af830b` genuinely **failed** original TC4 CODE comparison when a
  literal byte `marisa_bullet_angle += 7` was replaced by a named enum:
  1,427 candidate vs original 1,431 CODE bytes. The literal was restored.
- Final `af830c` passed **two independent original TC4 4.02 / full normal
  MAIN TLINK rounds**: 1,431 CODE bytes, 199 ordered FIXUPPs, nine
  PUBLICs, complete Japanese original loaded MAIN and all 1,553 MZ
  relocations matched; 98 other objects and CRT reused, no cold replay.
  See [after830 Marisa BOSS review](MAIN_MARISA_BOSS_NATIVE_MODULO_AFTER830_REVIEW.md).
  Existing native source owner reverified, **not new unique CODE credit**.

## Latest after829: four session-modified complete original physical owners together

- Actual original **TC4 4.02 + full normal MAIN TLINK** stage `af829a`
  recompiles **four complete current modified physical TUs simultaneously**
  in two independent rounds: entire Yumemi, Rikako and Chiyuri **major
  BOSSes** and Reimu's **ten-function Chargeshot/Gauge**. Every **8,137
  original initialized CODE byte, 1,077 ordered native FIXUPPs and
  39 PUBLICs**, full normal MAIN EXE/MAP, all 124,642 Japanese loaded
  bytes and all 1,553 MZ relocations match in both rounds. Independent
  standard MZ serialization reproduces the 130,882-byte Japanese file.
- **95 other original game objects and CRT are reused** without a full
  cold replay; complete original compiler source dependencies are
  checked, and the preserved report has both original OBJ and full
  link writer rounds. Earlier nine-object `af823a` was source-current
  then, but its Reimu input has since changed; it is now historical;
  **do not combine them into an invented thirteen-object compile**.
  See [after829 four-source integration](MAIN_FOUR_SOURCE_INTEGRATION_AFTER829_REVIEW.md),
  retained as historical source evidence after the newer Yumemi edit.
- The named and native-exact C++ fixes include whole-BOSS unsigned
  clocks, signed/unsigned rendering arithmetic, Reimu's 24-slot byte
  lifecycle and Chiyuri's four signed-angle fan loops. Rejected AL/
  byte-memory and `%4` compiler-unequal forms remain **rejected**. These
  original physical owners already had prior exact source coverage;
  **no new distinct CODE byte or canonical packed-file Factory credit**.

## After828: complete Chiyuri BOSS natural warning/render clocks and fan geometry

- The entire `ba_chiyu` eleven-function **major BOSS** now uses
  natural 16-bit unsigned `%8` trail warnings and `%4` global-frame
  renderer cadence, plus named **four separate horizontal/vertical fan
  loops** with signed angle/position division before scaling. The mutable
  **byte** `boss_render_frame &=3` remains exact; no invalid assumption
  from the distinct word-sized clocks was made.
- `af828d` freshly challenged intro byte-phase `_AL` arithmetic with a
  `register unsigned char` C++ temporary and **failed** the genuine
  original compiler CODE comparison (2,674 vs 2,654 bytes). The
  original three-instruction byte update was restored. Final `af828e`
  independently passed **two original TC4 4.02/full normal TLINK rounds**:
  2,654 CODE bytes, 381 literal ordered native FIXUPPs, 11 PUBLICs,
  all 124,642 Japanese loaded bytes and 1,553 MZ relocations match.
  No cold replay or unique byte-credit double count. See
  [after828 complete Chiyuri BOSS review](MAIN_CHIYURI_BOSS_FANS_MODULO_AFTER828_REVIEW.md).

## Latest after827: three newly changed complete original physical sources together

- `af827a` is a genuine **simultaneous two-round original Turbo C++ 4.02
  and complete normal TLINK** rebuild of this session's **three edited
  entire physical TUs**: full Yumemi and Rikako major BOSSes plus the
  complete ten-function Reimu Chargeshot/Gauge owner. All **5,483 original
  CODE bytes, 696 ordered native FIXUPPs and 28 PUBLICs**, full normal
  MAIN EXE/MAP, 124,642 Japanese loaded bytes and all **1,553 ordered
  original MZ relocations** match in both rounds. Independent serializer
  reproduces the complete Japanese 130,882-byte MAIN.EXE.
- The original **96 other project objects and CRT were reused**; no
  cold replay, old receipt overwriting, byte-padding or source-bound
  guard weakening. Previous `af823a` nine-object source proof was
  current at that checkpoint; its Reimu source hash is historical now;
  **do not describe these as a simultaneously built 12-object scope**.
  Existing source owner CODE must not be added as new unique coverage.
  See [after827 scoped three-source integration](MAIN_THREE_SOURCE_INTEGRATION_AFTER827_REVIEW.md).

## After826: complete Reimu Chargeshot/Gauge lifecycle source

- All ten functions of `cs_reimu` now use named byte-valued inactive,
  braking and homing/Hyper states across 24 physical entity slots. The
  authentic **12-per-player update/render vs six-slot hit-test** quirk
  remains unchanged. The 32-frame Gauge period and 16-frame phase,
  and the natural already-unsigned alternate hit-frame clock are now
  source-native C++ names/expressions.
- `af826a/b` tested signed/unsigned `%4` replacements for the animated
  `phase &=3` and both **failed actual TC4 byte equality**. `af826c`
  showed a named enum `angle += 0x20` changes AL/memory codegen; the
  exact original literal increment remains. `af826d/e` then passed;
  final `af826e` has **1,448 CODE bytes, 138 ordered native FIXUPPs,
  10 PUBLICs**, complete original loaded Japanese MAIN and all 1,553
  relocations in both native TC4/TLINK rounds. No cold replay or new
  unique covered bytes. See
  [after826 Reimu Chargeshot review](MAIN_REIMU_CHARGESHOT_STATES_AFTER826_REVIEW.md).

## After825: complete Rikako BOSS signed/unsigned native modulo recovery

- The whole `ba_rikak` major BOSS now uses natural unsigned `%2` for
  entrance flicker and explicit **unsigned** `%4` in both orbital
  renderer sprite-index expressions. A real native `af825b` signed
  `i %4` experiment **failed** (1,684 vs original 1,677 CODE bytes),
  while `af825c` proved `(unsigned int)i %4` native exact.
- Final `af825d` names the complete orbit's signed 256-unit angle
  division and render geometry, with **two independent original TC4 4.02
  / full normal TLINK rounds** matching 1,677 CODE bytes, 215 original
  ordered FIXUPPs, eight PUBLICs, whole original loaded Japanese MAIN
  and all 1,553 MZ relocations. No full cold replay. See
  [after825 Rikako BOSS review](MAIN_RIKAKO_BOSS_SIGNED_MODULO_AFTER825_REVIEW.md).
  Existing source owner reverified; **no duplicate unique CODE credit**.

## After824 complete Yumemi major BOSS native modulo/arrival recovery

- The **entire 10-function `ba_yumem` physical BOSS** now uses natural
  unsigned `%4` ring firing and aimed warning, `%2` aimed shots, and `%16`
  chase-beam release at the same original frame phases; the named
  introduction cues and 8-pixel four-phase 112-pixel entrance raster
  retain original timing, signed shifts and call/RNG order.
- Independent genuine TC4 4.02 + full normal MAIN TLINK stages `af824a`,
  `af824b`, `af824c` all passed; the final full object has **2,358 CODE
  bytes, 343 literal ordered FIXUPPs and 10 PUBLICs**, full Japanese
  124,642-byte program and all 1,553 original MZ relocations exact in
  **both** rounds. Reused 98 unchanged project objects/CRT, no cold replay.
  See [after824 Yumemi BOSS review](MAIN_YUMEMI_BOSS_NATURAL_CLOCKS_AFTER824_REVIEW.md).
  This is **revalidation of an already-covered original owner**, not
  2,358 new unique bytes or canonical packed-game acceptance.

## After821: complete Kotohime BOSS signed orbit and radial C++

- The **entire 538-line `ba_koto`** major BOSS now names 256-unit full
  orbit, 128-unit burst arc, per-projectile angular offset and speed
  scaling, and natural unsigned `%4` ring-sprite flicker, with the original
  signed 16-bit division and byte-angle truncation kept in order.
- Fresh original TC4/TLINK negative trials `af821a`, `af821b/c`,
  `af821f` independently reject natural `+=2` / `-=4` replacements for
  the remaining AL-mediated byte-phase instructions. They stay intact.
- `af821e` passes two original TC4/TLINK whole-MAIN rounds: **1,840
  CODE bytes, 262 ordered FIXUPPs, 11 PUBLICs, 1,553 Japanese MZ
  relocations** and all 124,642 Japanese loaded bytes exact. This is
  existing BOSS source verified again, not incremental unique ownership.
  See [after791/821 Kotohime source review](MAIN_KOTOHIME_BOSS_FLICKER_AFTER791_REVIEW.md).

## Historical after823: nine original C++ owners before the after845 Reimu edit

- `af823a` recompiled **nine complete original physical TUs together** in
  two independent original Turbo C++ 4.02 / complete normal TLINK rounds:
  full Reimu, Mima, Kotohime **major BOSSes**, entire main 200+-line
  frame/stage scheduler, Kana Bomb, full hitbox, HitCircle, shots and
  match-result controllers. Current `results` (natural `%8`, 32-bit bonus),
  Kotohime (signed radial geometry, `%4` flicker) and **both complete
  HitCircle update/render `for` loops** are all compiler-source-bound in
  the same normal MAIN link. Eight nested implementation `.inl` files
  across main/shot/results are pinned to actual TC4 OMF dependencies.
- All **11,578 original CODE bytes, 1,464 literal ordered FIXUPPs and
  49 PUBLICs**, full normal MAIN EXE/MAP, all **124,642 Japanese loaded
  bytes and 1,553 MZ relocations** match, with independent complete
  130,882-byte Japanese MZ serialization. **90 unchanged original
  project objects and original CRT reused; no full cold replay**.
- Previous `af792b` still proves its older physical source snapshots but
  is *historical*, not live-source-current after the HitCircle loops;
  `af823a` was live source-bound at that earlier checkpoint, but its
  Reimu BOSS snapshot is historical after the current after845 edit.
  All these original owners were previously covered: **do not count their
  overlapping CODE again** or claim canonical packed-game acceptance.
  See [after823 nine-source integration](MAIN_NINE_SOURCE_INTEGRATION_AFTER823_REVIEW.md)
  and [HitCircle native loop recovery](MAIN_HITCIRCLE_NATURAL_LOOPS_AFTER822_REVIEW.md).

## Earlier after792 nine-original source integration (source snapshot historical)

- `af792b` genuinely rebuilt **nine complete original TC4 C++ physical
  owners together** in **two independent original compiler + full normal
  MAIN TLINK rounds**: full Reimu, Mima and Kotohime **major BOSSes**,
  entire entry/frame/stage/score scheduler, Kana Bomb, HitBox, HitCircle,
  and whole shot and result renderers. Eight current implementation
  `.inl` files across entry/shots/results have real compiler OMF source
  dependency checks in each round.
- **All 11,578 original CODE bytes, 1,464 literal ordered FIXUPPs, 49
  PUBLICs**, full normal original MAIN and MAP, 124,642 Japanese loaded
  program bytes, 1,553 ordered relocations and independent standard
  MZ serialization of all 130,882 original Japanese MAIN.EXE bytes match.
  **90 unchanged original project objects and CRT reused, no cold replay.**
- An attempted natural `_DX &= 1` in HitCircle (`af792a`) genuinely failed:
  TC4 generated `83 E2 01` rather than original 16-bit immediate
  `81 E2 01 00`; the exact original inline assembler was preserved.
  `af792b` then passed native/independent source review; old `af788c`
  must be treated as *historical* after the current `results` edit.
  These are reverified **previously owned** original CODE bytes, **not
  extra distinct coverage or canonical packed-unit Factory acceptance**.
  See [after792 nine-source integration](MAIN_NINE_SOURCE_INTEGRATION_AFTER792_REVIEW.md).

## After791 Kotohime major BOSS natural native sprite-flicker clock

- The complete Kotohime 1,840-CODE-byte BOSS physical owner now uses
  natural unsigned `% KOTOHIME_RENDER_FLICKER_PERIOD` in the four-frame
  ring sprite flicker; original TC4 produces exactly the former mask.
- `af791a` (`boss_move_phase += 2`) and `af791b` (volatile near ref)
  genuinely failed full-object equality: the original extra AL load
  could not be removed. Those byte increments retain original `_AL`.
- `af791c` proves natural flicker. Final `af791e` additionally gives the
  original signed-angle 256/128-unit orbit divisions and 0x40/0x30/0x10
  burst angle/speed constants semantic C++ names. It passes **two original
  TC4/full normal MAIN TLINK rounds**:
  1,840 CODE bytes, 262 ordered FIXUPPs, 11 PUBLICs, full Japanese loaded
  MAIN and all 1,553 relocations. Recovered existing owner, not new
  distinct byte credit or canonical packed-game acceptance. See
  [after791 Kotohime BOSS review](MAIN_KOTOHIME_BOSS_FLICKER_AFTER791_REVIEW.md).

## After789 round result / scoreboard natural C++ recovery

- The complete original 1,060-byte `results` owner now uses natural
  unsigned `%8` scoreboard cadence, named five-category scoring
  multipliers, the original 192-frame bonus payout, decimal 10/100/10000
  divisions and two natural Boolean predicates. All original signed
  32-bit bonus arithmetic, uint16 cap, main HUD calls and story-clear
  conditions remain intact. The current `results.cpp` plus two live
  `.inl` implementations are forced into the compiler, not stale copies.
- `af789a`/`b`/`c`/`d` are four successful incremental native experiments;
  final `af789d` passes two original TC4 and full normal MAIN TLINK
  rounds: 1,060 CODE bytes, 89 ordered FIXUPPs, three PUBLICs, original
  Japanese loaded game and all 1,553 relocations. No cold replay or
  canonical packed-game Factory acceptance. See
  [after789 natural scoreboard review](MAIN_RESULTS_SCOREBOARD_NATURAL_AFTER789_REVIEW.md).

## Earlier after788: eight original physical MAIN owners (historical after results edit)

- `af788c` **simultaneously rebuilt eight complete original physical
  TUs** in **two independent original TC4 4.02 and full normal TLINK
  rounds**: changed Reimu/Mima **major BOSSes**, the complete `entry`
  frame scheduler, Kana Bomb, plus complete hitbox damage, HitCircle
  renderer, shot create/update/draw and result/statistics renderer.
  The latter four were historically compiled after591/595, but are
  **newly covered by strict live-source root/OMF dependency checks**;
  the full `entry` (four), `shots` (two) and `results` (two) current
  `.inl` implementations are explicitly included in both original
  native compiler rounds, not silently reused from stale Wine copies.
- All **9,738 original CODE bytes, 1,202 ordered native FIXUPPs and
  38 PUBLICs**, full original MAIN EXE/MAP, 124,642 Japanese loaded bytes
  and 1,553 MZ relocations match; the independent serializer reproduces
  the 130,882-byte Japanese MZ. **91 other original objects and CRT
  reused, no cold replay**. Stage's independent read-only source review
  and 9 targeted inline/source-contract tests pass. Both round proofs
  are protected under `.analysis/work/exatt-layout-af788c/`.
- This is a simultaneous fresh current-source validation for eight
  **previously historically covered physical owners**. Do **not** add
  9,738 bytes to the unique ownership union or claim canonical packed-
  file Factory acceptance. `input_s` one-NOP parent-link issue remains.
  See [after788 original eight-source integration](MAIN_EIGHT_SOURCE_INTEGRATION_AFTER788_REVIEW.md).

## Earlier after787 simultaneous complete original-source integration

- `af787a` genuinely rebuilt **four modified original physical TUs at once**,
  not a union inferred from separate trials: complete Reimu and Mima major
  **BOSSes**, the entire main `entry`/200+-line frame/stage/score scheduler
  (four current implementation `.inl` bodies), and complete Kana Bomb.
  Two separate original TC4 4.02 / complete normal TLINK rounds reproduce
  **7,518 CODE bytes, 1,033 ordered original OMF FIXUPPs, 27 PUBLICs**,
  complete original MAIN EXE and MAP, all **124,642 Japanese loaded bytes**
  and **1,553 relocations**, plus the original **130,882-byte Japanese MZ**
  through the separately checked standard serializer. Original native
  compiler source/header/include dependencies are checked for both rounds.
- **95 unchanged original game objects and CRT reused**, no cold replay,
  target-byte padding or overwritten historical receipts. This is a new
  combined current-source proof for already covered physical owners;
  **do not add its 7,518 bytes again** to source-ownership coverage or claim
  canonical Factory packed-unit acceptance. See the
  [after787 four-source integration](MAIN_FOUR_SOURCE_INTEGRATION_AFTER787_REVIEW.md).

## After786 major Mima BOSS naturally recovered unsigned clocks

- Four bit-mask scheduler expressions across **three substantial Mima BOSS
  attack functions** are now actual source-level unsigned `%2`/`%4`
  C++ clocks; genuine original TC4 matches every original instruction.
  Their shared `boss_frame` is unsigned 16-bit. The unrelated six-frame
  volley retains `%6`, and no byte-clock inference is made.
- Complete random attack warning/launch/ring phases now have explicit
  0x20/0x24/0x28, 0x30 and 0x40 symbols, preserving the original three
  discrete warning emissions. `af786a` and `af786b` are successful
  incremental native variants; final `af786c` proves the whole maintained
  source with two independent TC4 / full MAIN TLINK rounds:
  **1,922 CODE bytes, 277 ordered FIXUPPs, 9 PUBLICs, full Japanese loaded
  image and 1,553 relocations**. Existing owner, no double-counted new
  coverage or canonical Factory packed-file acceptance. See
  [after786 Mima BOSS review](MAIN_MIMA_BOSS_NATURAL_CLOCKS_AFTER786_REVIEW.md).

## After785 entire MAIN entry/round scheduler, dual-player selection

- The complete 3,050-CODE-byte `entry` physical owner (main, 200+-line
  `round_loop`, stage and score) now explicitly names left/right player
  indices and the original independent 0/40 sprite source offsets at all
  repeated scheduling sites. It preserves the two different current PID
  storage views and every original update/render call boundary.
- Natural `page_front = page_back` is **not** target CODE exact: `af785b`
  emits an extra two-byte `MOV AL,[page_back]` following the native
  hardware `OUT`, so the original AL reuse remains essential.
- Final `af785c` passes two original TC4/TLINK full-MAIN rounds with 3,050
  CODE bytes, 433 ordered FIXUPPs, 8 PUBLICs, the full Japanese game
  image and 1,553 relocations. Five maintained source/.inl inputs are
  explicitly bound. This is a reverified owner, **not additional distinct
  source bytes or canonical Factory acceptance**. See
  [after785 entry scheduler review](MAIN_ROUND_SCHEDULER_IDENTITY_AFTER785_REVIEW.md).

## After784 Kana Bomb byte-timeline and original MRS ABI (newer than after783)

- The complete `b_kana` Bomb owner now uses named phase boundaries,
  distinct 8/4-frame firing clocks, signed circular geometry and explicit
  byte-wrapping palette fade; byte-sized angle storage is asserted.
- `af784a`/`b`/`c` tested natural C++ for the MRS byte formal's stack
  carrier, but produced a **different** TC4 `PUSH word ptr` sequence;
  the original `_AX`-carrier form stays. `af784d` proved that even
  changing the literal `kana_bomb_angle += 0x10` to a named enum changes
  original AL codegen; it too was reverted.
- Final `af784f` passes two actual original TC4/TLINK rounds on this
  complete physical object: 526 CODE bytes, 53 ordered FIXUPPs,
  one PUBLIC, full MAIN image and 1,553 relocations. No cold replay,
  extra unique-byte coverage or packed-file credit. See
  [after784 Kana Bomb review](MAIN_KANA_BOMB_TIMING_AFTER784_REVIEW.md).

## After783 Reimu BOSS signed-angle experiment (newer than after782)

- The **complete** original `ba_reimu` BOSS owner now uses semantic 256-unit
  turn / 8-unit rotation names in all three signed orbit-division phases.
  Original `angle = (0 - angle)` must **not** be simplified to unary `-angle`:
  the native `af783a` negative comparison failed; it was reverted.
- `af783b` independently passes two original TC4 / full MAIN TLINK rounds:
  2,020 CODE bytes, 270 ordered FIXUPPs, 9 PUBLICs, full Japanese MAIN loaded
  image and 1,553 relocations. This rechecks an existing owner, not new
  distinct exact ownership or packed-file Factory acceptance. See
  [after783 Reimu BOSS review](MAIN_REIMU_BOSS_ORBIT_AFTER783_REVIEW.md).

## Earlier major checkpoints (through after782) — limits and provenance

- **Latest affected complete original-source native proof: `af782a`.**
  Two independently compiled Turbo C++ 4.02/complete normal TLINK rounds
  **simultaneously rebuilt six complete modified physical original TUs**:
  full Yumemi Chargeshot/target selector, Rikako homing Extra Attack,
  full Mima 30-projectile Chargeshot/Gauge, Chiyuri paired-beam Extra
  Attack, **complete major Yumemi BOSS**, and Kana 8-slot Extra Attack.
  All **7,684 original CODE bytes, 771 ordered literal OMF FIXUPP fields,
  44 PUBLICs**, original segment/source dependencies, full normal MAIN
  EXE/MAP, Japanese 124,642-byte loaded game and all 1,553 relocations
  match both rounds. Independent MZ serialization reproduces every byte
  of original 130,882-byte Japanese MAIN.EXE. **93 other project objects
  and CRT reused**, not cold-replayed. No byte padding or target patches.
- **Natural C++ register recovery:** Chiyuri's large two-entity beam
  update now uses `if(!exatt_entity_p->state) goto chiyuri_first_done;`
  instead of a handwritten BX load/memory byte comparison/branch. Real
  original TC4 emits the exact BX/memory/Jcc instructions naturally
  in the full source. The *different* late-beam AX/DX stack arithmetic
  still needs its original register form. Yumemi's major BOSS entrance
  uses native exact **two separate C++ shifts** for four large sprite
  phases; combining them into one shift changes CODE.
- **Other full source progress with native negative controls:** Yumemi's
  ten-function target search/Chargeshot/ring, Rikako's 14-slot homing,
  Mima's 30-slot Chargeshot, and Kana's 8-slot Extra Attack all have
  natural signed loops, state names and exact original byte expressions.
  In separate genuine original TC4 trials, several byte `%2/%4/%8/%16`
  clocks, signed division, byte-memory prefix increments and combined
  shifts changed machine CODE; those forms were **rejected and restored**.
- **Current and historical provenance:** read-only source review passes
  `af782a`, its six individual final stages `af776e`..`af781f`, and
  unaffected previous `af775a` and `af766a` integration receipts.
  Source hashes of older `af758a`/`af741b` snapshots correctly drift
  after later edits; these remain protected historical compiler receipts,
  not current checkout passing evidence. The separate BIOS `input_s`
  original-object-exact but single-NOP full-link gap remains **open**.
- **Previous eight-source still-current proof:
  `af775a`.** Two independent original compiler/full-link rounds rebuilt
  **eight complete genuinely modified physical TUs together**: nine-function
  Kotohime Chargeshot, both large shared-BOSS explosion/controller owners,
  complete Marisa Chargeshot/GRCG, Mima Extra Attack, Chiyuri Chargeshot,
  Kana Chargeshot and fourteen-slot Marisa Extra Attack. **6,853 complete
  original CODE bytes, 629 literal ordered OMF FIXUPP fields, 53 PUBLIC
  offsets**, original segments/current-source dependencies, full normal
  MAIN EXE/MAP, original 124,642-byte Japanese loaded game and all
  1,553 ordered relocations match. The independent standard serializer
  reproduces all original **130,882 Japanese MAIN.EXE bytes**. **91 other
  original project objects and Borland CRT reused**, no full cold replay.
- **Deep source experiments and exactness limits:** Kotohime's real
  near-BX hit pointer and the shared BOSS 32-byte `REP MOVSW` were
  challenged with multiple natural pointer/aggregate-C++ forms; genuine
  TC4 native CODE did **not** match, so the original compiler-specific
  operations remain. Marisa's full GRCG/Charge and dual Gauge controller,
  Mima's six-slot bouncing Extra Attack, Chiyuri/Kana's complete
  Chargeshot/Gauge and Marisa's 14-slot beam Extra Attack now have
  source-native natural local loops, states, typed fields and bounded
  parity/shift operations. `%16`/`%64` byte clock encodings, signed
  division, mutable byte-memory postincrements and GRCG DX zeroing
  were separately challenged and **not** falsely accepted when unequal.
- **Current provenance:** read-only review passes `af775a`, preceding
  current `af772a` six-owner integration and unaffected `af766a`
  eight-owner integration. Earlier receipts such as `af758a` remain
  protected genuine historical compiler snapshot evidence, but their
  live-source input hashes reflect earlier modified source. No old
  receipts were altered or their source-binding checks weakened.
  The original keyboard `input_s` single-NOP full-link blocker remains
  explicitly unresolved and is **not** counted in successful scopes.
- **Previous eight-source current proof: `af766a`.**
  Two separate genuine Turbo C++ 4.02/TLINK rounds concurrently rebuilt
  **eight modified original physical TUs**: Chiyuri, Ellen, Kana,
  Kotohime and Rikako **complete major BOSSes**, Rikako's full
  11-function Chargeshot/Gauge owner, and both original Reimu shared
  flight/Extra Attack update source objects. All **12,156 original
  CODE bytes, 1,555 ordered literal OMF FIXUPP fields, 69 PUBLICs**,
  original segment/source dependencies, the complete normal MAIN/MAP,
  Japanese 124,642-byte loaded program and 1,553 MZ relocations match.
  Standard MZ serialization reproduces all 130,882 Japanese original
  MAIN.EXE bytes. **91 other original game objects and CRT reused**;
  no complete cold replay, binary padding or source/target substitution.
- **Substantial natural C++ register recovery:** five big BOSS orbit and
  entrance sprite renderers now compile the original signed AX shifts
  from natural typed `top` assignments, with no explicit `_AX` register
  writes; Rikako's original ADD AX,-8 is also generated naturally.
  The full Rikako Chargeshot now uses natural signed `register int i`
  to generate the original CX/CL four-projectile loop/angle, rather
  than manually writing `_CX` and `_CL`. These were independently
  source-native tested, with rejected compound-shift/inline-expression
  negative experiments preserved, not accepted.
- **Live Reimu Extra Attack `.inl` source provenance:** the `ex_rfly`
  and `ex_reup` original physical owners now force the current
  `exatt_flight.inl`, `exatt_reimu_prefix.inl` and
  `exatt_reimu_update.inl`, and actual native compiler OMF COMENT
  source dependencies are checked. Original earlier receipts had a
  narrower source-binding scope; the after765+ contract is strict and
  historically versioned. Seven targeted source guard tests pass.
- **Historical source drift audited, not concealed:** the read-only
  reviewer currently passes `af766a` and all seven individual current
  source stages from after759..765; it correctly rejects old `af758a`,
  `af753a`, `af741b` and `af730a` because their source hashes reflect
  older BOSS/Chargeshot versions. Preserve those historical genuine
  compiler receipts as snapshots, not live checkout passing claims.
  The separate original keyboard `input_s` single-NOP link blocker
  remains unresolved and is not included as accepted native full link.
- **Previous twelve-source historical proof: `af758a`.** Two
  independent original TC4 4.02 and complete normal MAIN TLINK rounds
  simultaneously rebuilt **12 complete original physical TUs**, covering
  Chiyuri/Marisa/Mima **large BOSSes**, full Fireball/Explosion engines,
  Ellen/Kotohime Extra Attacks, both Combo scoring/BOSS-panic partitions,
  complete Ellen Chargeshot and the two Extra Attack/Gauge leaf owners.
  All **12,979 initialized original CODE bytes, 1,429 literal ordered OMF
  FIXUPPs, 71 PUBLICs**, complete segment/current-source dependency
  metadata, full normal MAIN/MAP, Japanese 124,642-byte loaded game and
  **all 1,553 original MZ relocations** match. Independent standard MZ
  serialization reproduces the **130,882-byte original Japanese MAIN.EXE**.
  **87 other project objects and CRT reused**, no full cold replay.
- **New original-native C++ register recovery:** Ellen's 10-function
  Chargeshot module `cs_ellen` now uses **normal typed C++ `register`
  SI/DI sprite-coordinate locals** in place of manual `_SI`/`_DI`/`_AX`
  writes. Actual TC4 emits original code with the restored declaration
  order; reversing the locals failed native codegen. Its full deceleration,
  tracking, collision and Gauge emitters are compiled as one object.
  Kotohime's complete eight-function Extra Attack, both Combo source
  partitions and both leaf objects also have actual codegen-verified
  natural C++ recovery and retained negative-control trials.
- **Keyboard `input_s` remains blocked** (not part of `af758a`): its
  current C++ matches the true original 417-byte physical OBJ, but the
  frozen after596 parent linker used an extra trailing 0x90 NOP in a
  418-byte experimental OBJ, so full MAIN link exactness fails by one
  byte. Never count this as accepted original full-link reconstruction.
- **Previous ten-source checkpoint: `af753a`.** Two real
  independent original Turbo C++ 4.02/full TLINK rounds simultaneously
  rebuilt **ten complete modified original physical TUs**: Chiyuri,
  Marisa and Mima **major BOSSes**, Fireball, Ellen/Kotohime Extra
  Attacks, explosion-chain collision, **both** separately linked Combo
  scoring/BOSS panic source partitions, and full Ellen charged-shot
  targeting/Hyper/Gauge. All **12,883 CODE bytes, 1,426 literal
  ordered original OMF FIXUPP fields and 69 PUBLICs**, real native
  source dependencies, segment and DATA/BSS ABI, complete normal
  MAIN EXE/MAP, Japanese 124,642-byte loaded program and all 1,553
  ordered relocations match. Independently serialized original Japanese
  **130,882-byte MAIN.EXE** also matches both rounds. **89 other
  original project objects and CRT reused**, no full cold replay.
- **Additional dirty C++ source fully recovered:** complete Ellen charged-
  shot's 10-function original `cs_ellen` owner now uses natural register
  SI/DI allocation in its sprite leaf, along with native-exact 32-slot
  scan/update/hit/render C++ loops. Its final `af752e` codegen proof
  matches **1,530 original CODE bytes, 169 fixups and 10 PUBLICs**;
  reversing the register declaration order failed native CODE, so the
  original ordering is preserved. This owner joins all preceding nine
  changed source objects in the current ten-source `af753a` proof.
- **Previous nine-modified-TU current-source checkpoint: `af752a`.** Two
  genuinely independent original Turbo C++ 4.02/full TLINK rounds
  **compiled nine complete original physical TUs simultaneously**:
  Chiyuri/Marisa/Mima **major BOSSes**, full Fireball, Ellen/Kotohime
  Extra Attacks, large explosion collision and the two **distinct**
  physical Combo score/HUD and BOSS/panic producers from one current
  `combo.cpp`. All **11,353 original initialized CODE bytes, 1,257
  literal ordered OMF FIXUPP fields and 59 PUBLICs**, original
  DATA/BSS/segment/source dependencies, complete normal MAIN/MAP,
  Japanese 124,642-byte loaded program and all 1,553 relocations
  matched. Independent standard MZ serialization matches the original
  **130,882-byte Japanese MAIN.EXE** in both rounds. **90 other project
  objects and original CRT reused**, no cold replay or byte patch.
- **No dirty changed owners abandoned:** Mima's whole BOSS `af749d`,
  Kotohime's eight-function Extra Attack `af750d`, and **both original
  Combo physical partitions together** `af751d` were resumed, byte-
  checked and saved separately as `gpt-web:` commits, then **all three
  added to the joint after752 proof**. The older after748 five-TU
  receipt remains protected and still live-source reviewable.
- **Previous original-source affected-scope checkpoint: `af751a`.** Two
  independent real original Turbo C++ 4.02/full TLINK rounds rebuilt
  **seven complete modified physical original TUs together**: Chiyuri,
  Marisa and Mima **major BOSSes**, complete Fireball, Ellen and Kotohime
  Extra Attack controllers and the large explosion/chain collision
  function. All **10,375 original CODE bytes, 1,200 ordered OMF FIXUPP
  fields and 54 PUBLICs**, original DATA/BSS/segment contracts and actual
  compiler source dependencies, full normal MAIN EXE/normalized MAP,
  Japanese 124,642-byte loaded program and all 1,553 MZ relocations
  matched both rounds. Independent normal MZ serialization matched the
  complete **130,882-byte original Japanese MAIN.EXE**. **92 other project
  objects and original CRT were reused**, with no cold replay.
- **Dirty worktree owner recovery included:** Mima's full BOSS natural
  attack-phase/renderer edits were preserved and independently source-
  verified (`af749d`; 1,922 CODE / 277 fixups / 9 PUBLICs). The modified
  Kotohime Extra Attack 8-function state/volley owner was likewise
  continued and independently verified (`af750d`; 1,054 CODE / 100
  fixups / 8 PUBLICs). Rejected Mima opponent-ID register reuse and
  Kotohime byte `%4` mask / event-byte prefix remain native negative
  controls, **not** accepted source. Both are included in `af751a`.
- **Previous affected current-source original MAIN proof: `af748a`.** Two
  independent genuine Turbo C++ 4.02/full TLINK rounds **simultaneously
  rebuilt five complete changed original physical TUs**: full Chiyuri
  and Marisa major BOSSes, complete Fireball engine (including its one
  initialized DATA byte), six-function Ellen Extra Attack with original
  seven-point trail, and the large explosion collision/chain controller.
  All **7,399 original CODE bytes, 823 ordered OMF FIXUPP fields, 37
  PUBLICs**, segments/source dependencies, normal full MAIN EXE/MAP,
  Japanese 124,642-byte loaded image and all 1,553 MZ relocations matched.
  Independent standard MZ serialization matched all **130,882 original
  Japanese MAIN.EXE bytes**. **94 other project objects and original CRT
  reused**, no complete cold replay or object patching.
- **New exact-object but blocked-full-link native keyboard finding:**
  `input_s` now naturally expresses its two-pass BIOS/port-delay polling
  in current `src/main/hardware/input_sense.cpp`. Real TC4 compiles match
  the original **417 CODE bytes, 42 ordered original FIXUPPs and one
  PUBLIC**, but the frozen parent MAIN link used an older **418-byte**
  object with an additional trailing **0x90 NOP** (at CODE offset 417).
  Switching to the true 417-byte object changes **only raw EXE file byte
  68,141 from 90 to 00**, so **full MAIN exactness fails** for that unit.
  No padding/byte patch was added. Read
  [the explicit blocked-input proof](MAIN_INPUT_S_LINK_GAP_AFTER744_REVIEW.md)
  and the read-only `scripts/review_th03_input_s_link_gap_after744.py`
  diagnostic; it deliberately returns `normal_MAIN_exact=false`.
- **Current source-drift audit:** the read-only current reviewer passes
  `af748a`, unaffected `af741b` and unaffected `af730a`. It **rejects**
  older `af724a`, `af721a`, `af715a` current-input hashes after this
  turn's Marisa/Chiyuri changes; these remain intact historical native
  source/OBJ/linker snapshots, not live-current-source passes. The
  previously source-drifted `af736a` and `af709a` also remain historical.
- **Previous affected current-source proof: `af741b`.** Two original
  TC4 4.02/TLINK rounds **simultaneously rebuilt eight complete
  original physical TUs**: large Kana BOSS, large Yumemi Extra Attack,
  all four physical `enemy.cpp` formation/script/hittest/update objects,
  and original `frmdely1` VSYNC delay and MAIN `execl` handoff.
  All **6,995 original CODE bytes, 596 literal ordered OMF FIXUPPs,
  35 PUBLICs**, segments and compiler-consumed source dependencies
  match. The entire normal MAIN/MAP, Japanese 124,642-byte loaded
  program, all 1,553 relocations and separately serialized original
  130,882-byte Japanese MAIN.EXE match both rounds. **91 other original
  objects and CRT reused**, no full cold replay or object byte patch.
- **Newly current-source-bound owners:** the original `frmdely1` shared
  object lives at `obj/th02/frmdely1.obj` and occupies 21 CODE bytes in
  TH03; the original TH03 `execl` occupies 79 CODE bytes, including the
  genuine 16-bit far/near vararg handoff. Both now have actual current
  C++ source dependencies, whole-object native OMF fields and complete
  linked MAIN acceptance in this scoped proof. The source-native
  `enemy.cpp` also now passes **all four current compiled partitions**
  after the changed enemy hit/chain controller, not only `eupdb`.
- **Source-codegen negative controls:** direct Kana signed-AL expression,
  simplified Yumemi clip-side selection, enemy parity-expression
  negation, and modern far/near `execl` pointer casts failed actual
  compiler/code comparisons and were **restored**, not credited.
- **Previous affected source-native proof: `af736a`.** Two independent original
  TC4 4.02 / TLINK rounds compiled **seven complete original physical
  current-source TUs together**: Kotohime/Yumemi **large BOSSes**, the
  large ENEDAT enemy script interpreter `efornb`, and original input
  modes, PI loader, KAJA driver and PC-98 exit owners. All **5,796 original
  CODE bytes, 716 literal ordered OMF FIXUPPs, 37 PUBLICs** and complete
  segment/source dependencies match; the complete normal MAIN/MAP,
  Japanese 124,642-byte loaded program, 1,553 relocations and separately
  serialized 130,882-byte original MAIN.EXE match in both rounds.
  **92 other project objects and CRT reused**, no full cold replay.
- **New original-source routes:** the scoped compiler now directly
  validates `inp_m_w` (nine input/CPU/joystick/wait routines), `pi_load`
  (original PI load/unload), `snd_kaja` (PMD/MIDI interrupt) and `exit`
  (PC-98 display/access page registers) as four distinct original physical
  source TUs. Input release/press polling has natural signed-loop/Boolean
  C++ while preserving the original 9999-frame sentinel. Kotohime/Yumemi
  fixed power-of-two phase masks and the full enemy script VM now have
  fresh current-source native codegen proof. Rejected AL-byte, coordinate
  local, Spawn flag, PI return and input-bit rewrites remain protected
  negative-control evidence, **not accepted source**.
- **Previous affected-scope, current-live-source MAIN proof: `af730a`.** Two
  independent original TC4 4.02/full normal TLINK rounds compiled **six
  complete original physical TUs together**: full player `core` and its
  nested state machine, Rikako/Reimu **major BOSSes**, PMD sound effect
  manager, signed Q8 `polar` math, and original CFG resident loader.
  This covered **7,027 complete original CODE bytes, 769 literal ordered
  OMF FIXUPP fields, 42 PUBLICs**, full original segment/BSS contracts,
  the complete normal MAIN/MAP, Japanese loaded program and all 1,553 MZ
  relocations. Original Japanese 130,882-byte MZ bytes matched after
  independent standard serialization; 93 other original game objects
  and CRT were **reused, not recompiled**. No cold replay.
- **Deeper current source guards:** after725 the `core` original TU now
  force-binds all **ten** maintained direct/nested implementation `.inl`
  bodies (including the large `player_state_update`), not merely Hyper.
  A regression in reading historical source evidence was discovered
  and fixed: prior-to-725 receipts like `af709a` are reviewed against
  their **original hyper-only** compiler input contract; post-725 proofs
  require all ten current source paths and compiler-emitted dependencies.
  The original after730 review of `af709a`, `af725d` and `af730a`
  passed with those appropriate contracts. After new Kana/enemy source
  changes, the **current-live-source reviewer correctly rejects** older
  `af709a` / `af736a` receipts due to changed source hashes. This does
  not invalidate their immutable original snapshot proofs; they are
  **historical**, not current checkout validation, and are not repinned.
- **Original additional physical sources now directly proved:** `snd_se`
  (120 original CODE), `polar` (26 CODE), and `cfg_lres` (49 CODE), including
  exact original OMF segment/fixup metadata. Natural C++ changes to the
  BOSS renderer masks, CPU charge/target cadence, sound priority lookups
  and Q8 polar expression were tested in actual native outputs, with
  negative controls retained and source-unequal forms rejected.
- **Prior seven-source affected-scope MAIN proof: `af724a`.** Two
  independent original TC4 4.02 / TLINK rounds **simultaneously rebuilt
  seven complete current original physical TUs**: three large Marisa/Mima/
  Ellen BOSSes, complete `intro` HUD, Bullet engine, newly directly
  source-proved original `initmain` and `hud_stat`. All **9,792 initialized
  CODE bytes, 1,055 ordered native FIXUPPs and 59 PUBLIC offsets**,
  original segment/group ABI and native source dependencies, full normal
  MAIN EXE/MAP, Japanese loaded image and all 1,553 ordered relocations
  matched. 92 other original project objects and CRT were reused. The
  independent standard MZ serializer reproduced the complete original
  130,882-byte Japanese MAIN.EXE. No full cold replay.
- **Earlier `af721a` five-source integration remains separately retained.**
  Two independent original TC4/TLINK rounds rebuilt
  **five genuinely modified complete original physical TUs**: Marisa,
  Mima and Ellen **large BOSSes**, full `intro` HUD particle/animation
  and the complete Bullet/trail engine. All **9,191 CODE bytes, 1,030
  ordered literal native FIXUPPs and 51 PUBLIC offsets**, original
  source and intro `.inl` dependencies, full normal MAIN/MAP, Japanese
  loaded programs and all 1,553 MZ relocations matched. 94 other original
  project objects and original CRT were reused, **not recompiled**.
  Independent standard MZ serialization reproduced the complete original
  130,882-byte Japanese MAIN.EXE.
- **Earlier four-source checkpoint retained separately:** `af715a`
  compiled four complete modified TUs together: Yumemi/Chiyuri **BOSSes**,
  main `entry`/stage/frame scheduler and full CPU movement/dodge logic.
  That retained scope matched 9,139 original CODE bytes, 1,221 ordered
  fixups and 33 PUBLICs. It was not rebuilt again in after721/724/730/748. This is
  **not** an additional disjoint byte-ownership count.
- **New source-binding routes:** the scoped native compiler now accepts
  both the full `entry` physical TU with its four current included `.inl`
  implementations **and** the full `intro` physical TU with its three
  current HUD particle/renderer `.inl` implementations. Borland OMF
  dependencies are forced and independently reviewed, rather than trusting
  stale historical include copies. Marisa/Mima hardware-masked BOSS
  renderers now naturally allocate the historical SI local; Ellen's
  large radial/three-strip controllers, Bullet loops and HUD particle
  state machine have newly source-verified natural C++ operations. The
  register-specific hardware instructions that could not compile exactly
  from C++ are intentionally retained; see negative stages. The current
  compiler additionally binds original `initmain` and `hud_stat` source
  owners, whose direct original compiler segment/BSS and fixup contracts
  were newly source-verified. `hud_stat` cannot declare an extra C++
  `main_01` group without changing its original OMF relocation frames.
- **Previous after709 proof remains separately retained:** `af709a`
  rebuilt five original Kana/split-shared-BOSS/core/lose TUs (6,622 CODE,
  701 ordered FIXUPPs and 42 PUBLICs) in two rounds, with original MAIN/MAP
  and loaded-image checks. The **historical after709 accumulated union**
  covered **58 original physical source TUs, 66,407 CODE bytes, 7,303
  fixups and 367 PUBLICs**. These are a historical deduplicated union of
  separate native proofs, **not** a simultaneous 58-object compiler run or
  an independently recomputed after730 coverage figure. Entry had already
  been source-proved historically in after594; no duplicate distinct-owner
  count is claimed here.
- **Frozen parent/full MAIN:** ordinary after596 original 99-object source-
  native TLINK is still the unchanged parent. The direct TLINK DOS header
  differs from the original Japanese executable; the separately normalized
  MZ serializer matches the file. Neither step proves historical raw
  vendor OMF record identity, whole-product source ownership or canonical
  packed-file Factory acceptance.
- **MAINL remains distinct:** the historical after587 decoded ending EXE,
  MAP and 677 relocations remain retained, but current source-bound decoded
  publication is **PENDING** after later source changes invalidated an old
  input guard. Do not advertise that historical proof as current
  acceptance. OP/ZUN have their own retained decoded evidence and
  outstanding canonical packed-file/whole-product claims.

Read [the latest after782 six-source integration](MAIN_SIX_SOURCE_INTEGRATION_AFTER782_REVIEW.md),
[the earlier after775 eight-source integration](MAIN_EIGHT_SOURCE_INTEGRATION_AFTER775_REVIEW.md),
[the preceding after766 eight-source integration](MAIN_EIGHT_SOURCE_INTEGRATION_AFTER766_REVIEW.md),
[the historical after758 twelve-source integration](MAIN_TWELVE_SOURCE_INTEGRATION_AFTER758_REVIEW.md),
[the preceding after753 ten-source integration](MAIN_TEN_SOURCE_INTEGRATION_AFTER753_REVIEW.md),
[the previous after752 nine-source integration](MAIN_NINE_SOURCE_INTEGRATION_AFTER752_REVIEW.md),
[the prior after751 seven-source integration](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER751_REVIEW.md),
[the previous after748 five-source integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER748_REVIEW.md),
[the previous after741 eight-source review](MAIN_EIGHT_SOURCE_INTEGRATION_AFTER741_REVIEW.md),
[the prior after736 seven-source review](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER736_REVIEW.md),
[the earlier after730 six-source review](MAIN_SIX_SOURCE_INTEGRATION_AFTER730_REVIEW.md),
[the earlier after724 seven-source review](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER724_REVIEW.md),
[the earlier after721 five-source review](MAIN_FIVE_SOURCE_INTEGRATION_AFTER721_REVIEW.md),
[the previous after715 four-source review](MAIN_FOUR_SOURCE_INTEGRATION_AFTER715_REVIEW.md)
and [the historical after709 union](MAIN_FIFTYEIGHT_SCOPED_SOURCE_AFTER709_REVIEW.md)
for exact scopes, controls, provenance and replay limitations.

### Fast, non-rebuilding verification

From the repository root (keep the original Japanese pinned targets):

```sh
git status -sb
.venv/bin/python scripts/preflight.py
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af871a af865a af859a af853a af847a af842a af835a
.venv/bin/python -m unittest discover -s tests -p test_main_source_overlay_inline_contract.py -q
# Diagnostic success means the known input_s full-link failure was detected:
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_input_s_link_gap_after744.py
.venv/bin/python scripts/validate_tracking.py
.venv/bin/python scripts/progress.py --check
git diff --check
```

These are **current-checkout source-bound review stages independently
confirmed after859**. Earlier `af782a`, `af775a` and `af766a` no longer
pass the current-source hash check: preserve their original genuine
compiler/TLINK receipts as **historical snapshots** instead. Do not present `af758a`, `af753a`, `af741b`, `af730a`,
`af724a`, `af721a`, `af715a`, `af709a` or `af736a` as current-input
proof after later changed-source revisions: their source hashes
intentionally differ. They remain protected historical native compiler
and full-link evidence, not current live-source acceptance. Never weaken
the independent reviewer to conceal drift.

The **latest current** protected original-source-bound read-only proof
is `.analysis/work/exatt-layout-af871a/report.json`: five genuinely
edited original physical source owners and both actual original
TC4/TLINK rounds. Earlier `af865a` and `af859a` remain separate
source-current independent five-owner compiler/linker experiments. The older `af782a`, `af775a`, and `af766a` complete real
compiler/TLINK receipts remain protected **historical** source-input
snapshots (the source hashes have subsequently changed); do not call them
current-checkout exact proofs without a new source-bound review. The earlier historical
after758 source snapshot is
`.analysis/work/exatt-layout-af758a/report.json`, with twelve former-current
complete source-native original objects, both genuine full compiler and
TLINK rounds. The previous ten-source root is
`.analysis/work/exatt-layout-af753a/report.json`, with all ten
modified original physical sources, both Combo partitions, Ellen
charged-shot and both independent real compiler/full linker rounds.
The previous after752 proof is
`.analysis/work/exatt-layout-af752a/report.json`, with all nine
current original physical source owners, both Combo partitions and full
independent TC4/TLINK writer evidence. The previous after751 root is
`.analysis/work/exatt-layout-af751a/report.json`, with all seven
modified original physical source owners and both real TC4/TLINK rounds.
The earlier after748 proof `.analysis/work/exatt-layout-af748a/report.json`
retains two actual native
compiler/TLINK rounds for five current modified physical originals. The
previous after741 root is `.analysis/work/exatt-layout-af741b/report.json`,
which still reviews successfully with its eight unaffected sources.
The **historical** after736 root is
`.analysis/work/exatt-layout-af736a/report.json`, preserving its seven
source-snapshot original native object rounds and full TLINK receipts.
Its live-source hash check now **correctly fails** after `enemy.cpp`
changes. Historical `af709a` (Kana), `af715a` (Chiyuri), and `af724a` /
`af721a` (Marisa) must likewise **not** be advertised as current-source
passes. Retain their original snapshots and never weaken the source-bound
reviewer to conceal input drift.
The earlier six-TU root is
`.analysis/work/exatt-layout-af730a/report.json`, including all ten nested
`core` source snapshots and both actual six-unit compiler/linker rounds.
The earlier protected seven-TU integration root is
`.analysis/work/exatt-layout-af724a/report.json`, including both actual
rounds, the two newly bound physical owners and all three HUD `.inl`
dependency snapshots. The earlier five-source `af721a` proof is retained.
Earlier protected proof `.analysis/work/exatt-layout-af715a/report.json`
remains source-bound and unchanged.
Evidence roots (ignored but **protected**) also include
`.analysis/work/exatt-layout-af709a/report.json` plus its actual
two-round OBJ, EXE, MAP, writer logs, source/header snapshots and
the `TH03WORK/probe/af709a` compiler worktree. Other relevant
receipts: `af703a` (7 edited TUs), `af693a` (6 edited TUs),
`af686a` (47 selected TUs) and frozen after596 MAIN.
Review the [latest after782 six-source report](MAIN_SIX_SOURCE_INTEGRATION_AFTER782_REVIEW.md),
[after775 previous eight-source report](MAIN_EIGHT_SOURCE_INTEGRATION_AFTER775_REVIEW.md),
[after766 earlier eight-source report](MAIN_EIGHT_SOURCE_INTEGRATION_AFTER766_REVIEW.md),
[historical after758 twelve-source report](MAIN_TWELVE_SOURCE_INTEGRATION_AFTER758_REVIEW.md),
[after753 previous ten-source report](MAIN_TEN_SOURCE_INTEGRATION_AFTER753_REVIEW.md),
[after752 preceding nine-source report](MAIN_NINE_SOURCE_INTEGRATION_AFTER752_REVIEW.md),
[after751 preceding seven-source report](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER751_REVIEW.md),
[after748 prior five-source report](MAIN_FIVE_SOURCE_INTEGRATION_AFTER748_REVIEW.md),
[after741 preceding eight-source report](MAIN_EIGHT_SOURCE_INTEGRATION_AFTER741_REVIEW.md),
[after736 previous seven-source report](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER736_REVIEW.md),
[after730 prior six-source report](MAIN_SIX_SOURCE_INTEGRATION_AFTER730_REVIEW.md),
[after724 seven-source integration](MAIN_SEVEN_SOURCE_INTEGRATION_AFTER724_REVIEW.md),
[after721 prior five-source integration](MAIN_FIVE_SOURCE_INTEGRATION_AFTER721_REVIEW.md),
[after715 prior integration](MAIN_FOUR_SOURCE_INTEGRATION_AFTER715_REVIEW.md)
and [after709 cumulative report](MAIN_FIFTYEIGHT_SCOPED_SOURCE_AFTER709_REVIEW.md)
for numbers, limits and exact commands. A new rebuild needs a **fresh
DOS-safe stage ID**; do not overwrite prior receipts.

## Do the next actual reconstruction work

1. Prioritize **unproved physical owner/ABI scopes and substantial
   BOSS/player functions**, with the small leaves that feed them;
   don't spend a turn re-counting already source-owned CODE.
   The 58-TU native proof union is **not** all 99 project TUs.
2. Challenge old source comments and v1 results. Original-byte
   exactness requires current maintained compiler-consumed source
   (emitted Borland OMF COMENT dependency), complete CODE and
   initialized DATA, literal ordered FIXUPPs, PUBLICs,
   segment/BSS ownership, real TLINK response and full MAIN/MAP.
   Equivalent math may produce different TC4 bytes; preserve
   signedness, operation order, 16-bit widths, register and
   near/far/Pascal ABI, RNG consumption and original bugs.
3. Use `scripts/probe_th03_main_exatt_layout.py --stage NEW --units a,b`
   to rebuild **only affected original TUs**, and
   `scripts/review_th03_main_source_overlay.py --stage NEW`
   for independent review. Reuse unchanged source-native
   objects and libraries in the original 99-object TLINK.
   Do not run another whole cold replay for routine source edits.
4. Consider the **MAINL current publication gate** separately:
   the after587 source/native evidence is historical, not a
   current signed-off decoded acceptance. Diagnose its exact source
   guard and re-review only affected dependency inputs rather than
   repinning original receipt hashes.
5. Commit each substantive verified improvement `gpt-web: xxx`,
   preserve rejected experiments and both original compiler rounds.
   Don't push without a request.

### Known physical-source traps

- `core` uses original link slot `probe/af593p/rN/core.obj`;
  `ch_setup` uses `probe/af592p/rN/ch_setup.obj`.
  `chain1/chain2` originals are in `obj/`, **not**
  `obj/th03/`. Yumemi Bomb's compiler shortname is
  `bomb~cxk` despite its original linker slot's long filename.
- `combo.cpp` physically emits two original TUs:
  `p_combo` (score/HUD) and `p_cmbhl` (fireball/BOSS/
  panic helpers). The original BOSS `shared.cpp` also emits
  two TUs (`ba_sring`/`ba_srest`). Compiler flags and
  original MAP module row counts are not interchangeable.
- Certain character Bomb `CODE` producers have **zero private BSS**:
  storage is owned by external frozen carriers. Recompiling with
  duplicate BSS changes relocation fields even when CODE sizes match.
- The active scoped compiler binds current `hyper.inl` and
  all four loss/defeat `.inl` bodies with explicit source
  snapshots and OMF dependency checks. It does **not**
  claim every other nested `.inl` in the core is newly
  modified or independently source-bound.
- Do not simplify an original `& 3` to `% 4`,
  prefix/postfix byte mutation or an original
  AL/AX/BX intermediate **without a full native comparison**.
  Multiple exact negative controls are documented.

## Storage and handoff discipline

The ignored `.analysis` contains the source-native receipt DAG,
both round outputs, original private toolchains and Japanese
targets. Do **not** delete by age or run
`clean_generated.py --prune-unreferenced-receipts`.
The current restricted policy and measured audits are in
[STORAGE_HANDOFF_CURRENT.md](STORAGE_HANDOFF_CURRENT.md).
Only verified disposable stage outputs and regenerable caches
may be removed; preserve an audit manifest with hashes before
deleting any bounded failed scratch stage.

For historical details and **negative codegen experiments**, use
[the archived chronology](RE_HANDOFF_ARCHIVE_AFTER709.md)
and the relevant `docs/MAIN_*_AFTER*_REVIEW.md`.
Avoid re-expanding this live handoff into a one-section-per-commit log.
