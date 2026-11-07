# TH03 — current next-agent handoff (2026-11-07)

**Start here.** This is the active short handoff; detailed per-experiment
history through after709 was moved, unchanged in substance, to
[RE_HANDOFF_ARCHIVE_AFTER709.md](RE_HANDOFF_ARCHIVE_AFTER709.md).
Older roots are [after596](RE_HANDOFF_ARCHIVE_AFTER596.md) and
[after554](RE_HANDOFF_ARCHIVE_AFTER554.md). **Do not treat historical
“latest” paragraphs as current state.** Read [AGENTS.md](../AGENTS.md)
and [the workflow](RE_WORKFLOW.md) before modifying native evidence.

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
  link writer rounds. Earlier nine-object `af823a` remains separately
  current and passes read-only review for **different unchanged TUs**;
  **do not combine them into an invented thirteen-object compile**.
  See [after829 four-source integration](MAIN_FOUR_SOURCE_INTEGRATION_AFTER829_REVIEW.md).
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
  guard weakening. Previous `af823a` nine-object current-source review
  remains separately valid for *different, unchanged* original owners;
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

## Latest after823: nine current original C++ owners with recovered HitCircle loops

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
  `af823a` is now the live source-bound complete nine-TU verification.
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
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af782a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af775a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af772a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af766a
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af765g
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af764d
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af763d
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af762c
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af761c
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af760c
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af759c
.venv/bin/python -m unittest discover -s tests -p test_main_source_overlay_inline_contract.py -q
# Diagnostic success means the input_s full-link failure was detected:
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_input_s_link_gap_after744.py
.venv/bin/python scripts/validate_tracking.py
.venv/bin/python scripts/progress.py --check
git diff --check
```

This list contains **current-source checks that actually pass on this
checkout**. Do not present `af758a`, `af753a`, `af741b`, `af730a`,
`af724a`, `af721a`, `af715a`, `af709a` or `af736a` as current-input
proof after later changed-source revisions: their source hashes
intentionally differ. They remain protected historical native compiler
and full-link evidence, not current live-source acceptance. Never weaken
the independent reviewer to conceal drift.

The latest protected read-only proof root is
`.analysis/work/exatt-layout-af782a/report.json`, with six current
modified complete physical original C++ owners, two independent real
TC4 4.02/TLINK rounds and original Japanese MZ evidence. The previous
still-current eight-source receipt is
`.analysis/work/exatt-layout-af775a/report.json`, with eight current
complete original physical source TUs, both real TC4 4.02 full TLINK
rounds and the independent Japanese MZ comparison. The preceding
protected after766 source-native proof is
`.analysis/work/exatt-layout-af766a/report.json`, with eight
current source-bound original physical objects including both current
Reimu Extra Attack implementation roots, two genuine TC4/TLINK rounds,
and original full MAIN/Japanese MZ comparison. The earlier historical
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
