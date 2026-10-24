# TH03 handoff

Commit format: `gpt-6.1-sol: xxx`. Use local headless tools; no Factory MCP.
Read `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/RE_WORKFLOW.md` and the local
`th03-re` skill before reconstruction. The full project introduction and setup
remain in [README.md](../README.md).

## Current state

- Previous pushed checkpoint: `30498c1` (ZUN formatter/print source scopes).
- MAIN: **445 exact functions / 75,317 bytes / 98 CODE extents**. These are
  reviewed source scopes; the full product is not exact. The whole-game source
  denominator is unknown. OP, MAINL and ZUN have no accepted whole-product source exactness.
- OP now has **seventeen accepted decoded source functions / 1,067 bytes**. The
  three lifecycle functions / 133 bytes cover exit to DOS, VRAM plane setup and game cleanup. The current graph consumes all three
  maintained sources through their actual GAME2/GAME1/GAME3 physical wrappers.
  Complete native OMF/public/MAP ownership, zero private DATA/BSS and eleven
  literal ordered relocations pass. Both MAP public tables bind the four external
  plane pointer addresses. A fresh 30-object cold pair still repeats all 32 raw
  outputs and matches the complete decoded and canonical DIET `-B` stored target.
  The independent guest model executes every one of the 133 bytes in 288 cases
  per image, across two loads, six register patterns, two stacks and four IF/DF
  states; nine actual instruction mutations fail. Foreign services and hardware
  remain bounded interfaces. `config/op_work/scoped_acceptance.json` revalidates
  all eleven gates against the live source/recipe/output graph; it replaces no
  historical cohort and grants no canonical packed-file unit offsets or whole
  product source ownership. The nine shared input functions below add 367 bytes
  and six relocations; configuration adds thirteen more below. Replay with
  `publish_th03_op_work_scopes.py`.
- OP now has a live, source-only cold build independent of the deleted historical
  receipts: 330 inputs, all 30 objects rebuilt twice, all 32 raw OBJ/EXE/MAP outputs
  repeat. The complete 63,866-byte decoded EXE, 59,770-byte load image and all
  607 literal relocations match. Two DIET `-B` packs match the complete canonical
  36,041-byte stored target and restore to the actual linked EXE. TH04's `-G`
  selects a larger SFX stub and fails this TH03 target (36,136 bytes).
  Frozen reference source and vendor libraries remain unowned context; this is
  a fresh complete-byte build observation; the seventeen scoped owners have
  their separate ownership/ABI/runtime acceptance.
  See `config/op_work/observation.json` and `scripts/build_th03_op_work.py`.
- OP also accepts **three near cfg functions / 271 CODE bytes** inside the
  entry object: full 120/67/84-byte bodies, all 28 ordered native fields and
  thirteen literal MZ relocation pairs pass. Its containing 3,094 CODE / 487
  DATA / six BSS bytes are reviewed context, not enclosing ownership. Eighteen
  initialized dependency bytes bind the selection flag, zero template and
  uppercase YUME.CFG filename; no DATA extents gain canonical credit. A fresh
  SDK-guarded cold pair repeats all 32 outputs and complete decoded/stored OP.
  All five actual SDK headers match the pinned installation before/after use.
  Independent 4,408-case-per-image models at two loads execute all 271 bytes
  and reject twenty-one actual instruction changes. PMD-mode's 29 instruction
  bytes and the 28-byte F_SCOPY helper execute without source credit. Keep the
  mode helper's explicit alignment NOP unaccepted until a natural proof exists.
  All roots use near RET/no arguments; packed cfg resident segment is at byte 5.
  Reads of zero through eight bytes proceed unchecked even with failed status.
  Plain save writes four bytes, including its uninitialized fourth stack byte,
  preserving the remaining file tail. Exit save copies a real eight-byte zero
  initializer then fills three options; its real CRT CLD executes. Keep BYTE
  MIDI values, requested-off versus unavailable selection, DWORD zero seeks,
  SS far buffers and the bounded file-service flags. Full registers/flags,
  frames and memory outside an 80-byte stack pass; peak observed depth is 30.
  File and PMD replies remain bounded interfaces. Lifecycle/shared/cfg models cover fifteen
  functions / 771 CODE bytes, thirty literal relocations, 6,914 model cases
  per image and forty-nine mutants. Whole entry/product acceptance stays open.
  `review_th03_op_cfg_work.py` performs the required fresh cold pair and cfg
  review; follow it with the shared-input review and per-product publication.
- OP's **two demo/score dispatch functions / 296 CODE bytes** now pass native
  ownership and behavior gates: whole 202/94-byte bodies, twenty-five literal
  native fields and ten ordered MZ relocations. Thirty-two initialized dependency
  bytes cover pairing/seed tables, adjacent bytes and lowercase `mainl` filename;
  no DATA credit is added. The fresh SDK-guarded cold pair still repeats all
  outputs and complete decoded/stored files. Independent 2,144-case-per-image
  contracts at two loads execute every owner byte and 164 real nested cfg-save,
  sound-routing and game-exit bytes. Twenty-three actual instruction mutants fail.
  BYTE demo 255 wraps to zero and bypasses the unsigned greater-than-four reset:
  it reads preceding pairing bytes `8F 00` and seed `05090B07` from the pairing
  tail. Keep all four ordinary pairs and DWORD seeds 600/1000/3200/500, sixteen
  individual score-byte clears, unsanitized cfg byte, gaiji-before-stop order,
  score-only SUPER_FREE and the real page/port cleanup sequence. MIDI BYTE exactly
  one selects INT61. Cdecl execl receives two equal far filenames and a DWORD null;
  the caller pops twelve bytes. On exec return score clears only AL, preserving
  AH; demo preserves AX. Register results, DWORD seed effects, flags, IF/DF, near/far
  frames, 26-byte observed stack and memory outside an 80-byte stack pass.
  File/library/driver/exec replies remain bounded interfaces; successful exec and
  physical hardware are open. The former 1,222-byte screen unit is refined into
  821 story/VS/choice-renderer + 202 demo + 105 attract-wait + 94 score bytes;
  total source-present bytes are unchanged and the historical cohort snapshot is
  retained unchanged. Story/VS and attract wait have no current source acceptance.
  OP totals seventeen functions / 1,067 CODE bytes, forty ordered relocations,
  9,058 model cases per image and seventy-two mutants. Run
  `review_th03_op_dispatch_work.py` once for the cold/cfg/dispatch witnesses,
  then the shared-input review and per-product publishers. Whole entry remains open.
- MAINL now has the corresponding live cold build: 1,912 source inputs, 36 project
  objects and six maintained CRT objects per round. Normal TLIB extraction/rebuild
  preserves all 893 vendor member positions, substitutes the six real producers,
  and preserves the other 887 members' program records. All 938 raw outputs repeat.
  The complete 67,372-byte decoded EXE and all 677 ordered relocations match;
  both DIET `-B` packs equal the canonical 37,975-byte stored target. This remains
  a complete-byte build observation with explicit reference/vendor context; the
  fifteen scoped owners below have independent current source acceptance.
  See `config/mainl_work/observation.json`.
- MAINL has **fifteen accepted decoded source functions / 703 bytes**. Its
  four lifecycle owners / 210 bytes are plane setup, cleanup, initialization and return to MAIN. Their actual first-use
  slots remain GAME1/O, GAME3/O, GAME3/M and GAME3/L. Complete native objects,
  both OMF/MAP public tables, zero private DATA/BSS and nineteen literal ordered
  relocations pass. Initialization takes a four-byte far filename; every nonzero
  allocation result returns 1 before further services, while success executes
  the owned plane setup, forwards the pointer unchanged and returns 0 despite
  later service status. Both paths use `RETF 4`. Independent guest execution
  covers all 210 bytes in 4,800 cases per image and rejects fifteen mutations.
  The three consumed SDK headers now match the pinned installation before/after
  each cold round; the plane producer uses explicit `compat/rec98/planar.h`.
  `config/mainl_work/scoped_acceptance.json` replays all eleven gates against
  the current 938-output source/library graph. It grants no canonical packed-file
  unit offsets or whole-product source ownership; library/device/DOS bodies
  remain bounded interfaces. Use `publish_th03_mainl_work_scopes.py` to replay.
- OP and MAINL each accept the same **nine shared input functions / 367 CODE
  bytes**, with zero private DATA/BSS. Both real wrappers retain GAME3/O first
  use; nine complete native publics, both MAP tables and all 58 ordered native
  fields pass. Two high-byte tests have real +1 OMF addends. Ten same-CS far
  calls relax naturally through TLINK; six literal ordered JS call relocations
  differ appropriately between product layouts. Independent 2,218-case models
  per image at two loads cover all 367 bytes and reject nineteen mutations per
  product. Real owned nested interface instructions execute; keyboard, joystick
  and timing services remain bounded interfaces. Full registers/defined flags,
  far Pascal frames, inherited IF/DF, whole memory outside a 40-byte stack and
  exact ordered word stores/services are checked. Preserve lane assignment/OR
  order, WORD joystick presence, OK/CANCEL normalization and attract clearing.
  Release always precedes timeout; negative signed limits skip press waiting.
  Both zero and explicit 9999 reset the counter, tested through 10,003 polls.
  The two complete cold builds remain target-equal. Run
  `review_th03_shared_input_work.py` after new OP/MAINL cold builds and before
  per-product publication. Its bound full witnesses run once; normal status
  executes twelve short cases per image. Lifecycle/shared models total
  OP 2,506 cases / 28 mutants and MAINL 7,018 / 34; configuration and ending
  waits add separate models. No canonical file-backed
  offsets or whole-product source acceptance are inferred.
- MAINL's **two ending input waits / 126 CODE bytes** now have complete native
  ownership, zero private DATA/BSS, eleven literal fixups and three ordinary
  TLINK far-call relaxations. They retain GAME3/L first use and own no MZ
  relocation fields. Both actual input-interface calls and the inactive-music
  fallback execute. Far Pascal returns pop four/two argument bytes respectively;
  frames is at BP+6 and measure at BP+8. Independent 3,378-case models per image
  at two loads cover all 126 bytes and reject eighteen actual mutations.
  Preserve the target's music-wait behavior: input_mode_interface overwrites
  the music query's AX with player-1 keyboard input, which is compared unsigned
  against the signed-looking measure argument. SHOT or OK returns BOOL16 one
  first. MIDI uses INT61/DX=00C0 only for flag BYTE exactly one; other values
  use INT60, both with AH=5. Inactive sound calls the real frame wait; its WORD
  vsync_Count1 resets before a mandatory first poll, even for zero frames, and
  uses an unsigned timeout. IRQ counter wrap, full registers/defined flags,
  inherited IF/DF, a 20-byte observed stack and full physical memory are checked.
  Sound and input/IRQ responses remain bounded interfaces. The normal input
  review now binds these full witnesses and runs five short cases per image.
  MAINL totals 15 functions / 703 CODE bytes, 10,396 model cases per image and
  52 guest mutants; canonical file-backed and whole-product credit stay open.
- ZUN now has a complete live cold build: 110 source inputs plus explicit vendor
  `MASTERS.LIB` and the -1 payload. All 23 raw OBJ/COM/MAP/composition/packed outputs
  repeat. All five payloads and the entire 22,812-byte decoded launcher match;
  both DIET `-B` packs equal the canonical 16,242-byte stored target. Fourteen
  bounded wrapper cases match, and a wrong transfer address is rejected. The
  -2 OMF resolver checks its complete 607 CODE / 783 DATA partition; -4 checks
  all 55 procedures / 56 public addresses and WORD/USE16/DGROUP layout. Vendor
  startup/runtime, MASTERS.LIB, -1 and forwarded headers remain unowned context;
  formal source/behavior acceptance stays separate. See `config/zun_work/observation.json`.
- ZUN -3 now has **ten accepted decoded source functions / 1,299 CODE bytes**.
  The complete native producer also owns 15 initialized DATA bytes and a reviewed
  293-byte BSS layout; these add no canonical packed-file credit. Native TC4
  `-a2` replaces the candidate's unused `wave_padding` variable. All instructions,
  initialized bytes and field addresses remain target-equal, with fourteen BSS
  publics and 48 entries in the two MAP public tables. The implicit alignment byte
  remains opaque: a char amplitude argument transfers it as the unspecified
  high byte of its two-byte slot. All 256 high bytes are tested.
  Independent scalar/event contracts execute actual root and integer-helper
  instructions in 5,111 cases per image and reject eighteen real mutations.
  Every one of the 1,299 owned bytes executes; a 231-frame fade runs at the first
  load, while both loads exercise all entries, signed vector/alias boundaries,
  state/word wrapping, sync, hardware-mode bits and keyboard groups. Native CODE
  records remain 1,017/282 bytes. Four consumed tiny runtime/startup copies match
  the pinned installation before/after execution. The current cold pair repeats
  all 23 raw outputs and the complete decoded/stored targets. Publication in
  `config/zun_work/scoped_acceptance.json` rechecks eleven scoped gates and twenty
  short ABI cases; normal status binds the full current runtime witness rather
  than repeatedly running the long animation. Other payload/source ownership
  remains open, including vendor startup/runtime, MASTERS.LIB and -1.
- ZUN -5 now has **two accepted decoded source functions / 322 CODE bytes**,
  bringing current -3/-5 source acceptance to **twelve functions / 1,621 bytes**.
  Its complete native root owns 307 initialized DATA bytes and zero BSS; both
  OMF publics, one 322-byte CODE record and six entries in the two MAP public
  tables are checked. Near cdecl cfg_init takes a two-byte segment; main takes
  argc/near argv as two words. Only a signed-positive open handle takes the seek
  path; all other handles create with archive attributes and write five default
  option bytes before the unchanged segment word and debug byte. File/service
  failures do not change main's successful return. Option parsing occurs only
  for argc 2, accepts both prefixes/cases and ignores trailing bytes. Initialization
  preserves ten ID characters and their terminator, zeroing offsets 11..255.
  Independent contracts execute all 322 owned bytes in 3,548 cases per image at
  two loads, two stacks/register patterns and four IF/DF states; sixteen actual
  guest mutations fail. The actual N_SCOPY helper executes and clears DF; it
  gains no source credit. Foreign Pascal services explicitly preserve IF/DF
  and callee-saved registers; this makes no real DOS/device flag assertion.
  Consumed DOS.H/_DEFS.H match the pinned SDK before/after the cold pair.
  The publication binds both full models and executes thirty short ABI cases.
  Canonical stored-file offsets and whole-product ownership remain open.
- ZUN -2 now passes complete **original-ASM** decoded source acceptance:
  nine procedures / 607 CODE + 783 initialized DATA bytes, zero BSS. All 1,390
  bytes resolve naturally from native records 1,000/390 and 48 literal ordered
  fixups. Complete OMF/ORG/DGROUP/MAP ownership and the pinned original token
  stream with 59 bijective label changes pass. It adds **zero authored credit**.
  Current -2/-3/-5 acceptance is thirteen extents / 21 procedures / 2,228 CODE
  bytes; authored CODE remains 1,621 bytes. Reviewed producer DATA totals 1,105.
  Independent guest contracts run 70,116 calls per image: 65,536 conversion
  inputs at the first load, 1,536 boundary inputs at the second and 1,522 flow,
  IRQ and draw scenarios at each load. All 607 instruction bytes execute at
  both loads; thirteen actual guest mutants fail. Complete physical memory
  outside a bounded caller stack, exact ordered video/latch/saved-vector stores,
  near/IRET frames and flags are checked. Detection uses fixed ES:023D rather
  than returned BX. Each old vector is saved before publishing its handler;
  install retains 42h paragraphs. Remove restores 59h/6/5 before freeing the
  environment and resident, ignores first-free carry and reports second-free
  carry. Empty text writes 65,536 attribute words; all drawing inherits DF.
  DOS/PC-98 BIOS remain explicit bounded interfaces; wrapper entry supplies
  cleared DF. Out-of-domain unchecked error pointers, real devices and DOS
  lifetime remain unproved. Publication binds all three full witnesses and
  executes 46 short ABI cases; canonical packed-file offsets remain absent.
- ZUN -4 uses the separately pinned compatible JWasm OMF emitter and normal TLINK.
  Staging only adapts model declaration order, variadic macro spelling and
  include separators. Nine native CODE contributions now share DGROUP: root
  WORD plus eight PARA contributions. TLINK generates all eight intergroup gaps
  (71 bytes) without source fillers; native EVEN emits the row-copy boundary
  NOP. DS assumptions consistently describe DGROUP. All 55 procedure addresses
  and the complete 4,224-byte driver remain unchanged. This proves a compatible
  natural layout, not unique original organization. Native WORD and no-EVEN
  controls fail equality (4,156 bytes / 2,716 differences; 4,224 / 33). The
  original assembler remains unknown. The standalone producer and its ten-byte
  TASM negative control remain replayable through `build_th03_zun_driver_work.py`.
  The complete builder compiles the driver itself without consuming that tree.
- ZUN -4 now has **sixteen accepted library procedures / 428 CODE bytes**:
  six register setters, three byte/folding predicates, five numeric parsers and
  two string helpers. Private DATA/BSS ownership is zero; six CS state words
  and ON/OFF strings remain explicit external state. Actual maintained include
  slots, all 56 enclosing publics and both MAP tables pass. Complete native
  image resolution checks 206 fixups (152 absolute, including one DWORD,
  and 54 relative near calls) and eleven initialized records. Coverage is 4,153
  bytes; the 71 linker bytes are absent from initialized OMF. Sixteen scoped
  fixups (eight absolute / eight relative) are checked separately. Moving a
  cross-contribution fixup changes resolved bytes and fails the native-site
  control. Whole-driver ownership remains false.
  Independent actual guest execution passes 8,428 cases per image at two loads,
  covers all 428 bytes and rejects fourteen instruction mutations. All called
  helpers execute; there are no external service stubs. Full registers, near
  frames, CMP/CF and inherited IF/DF, foreign DS/ES, split SS, complete physical
  memory outside a 64-byte stack and ordered field/suffix writes are checked.
  Preserve quoted word order, modulo16 arithmetic, partial direct-parse failures,
  permissive hexadecimal punctuation, temporary H/B suffix writes and the empty
  input read at DS:[SI-1]. LODSB helpers require forward DF; folded comparison
  and decimal do not. The upstream SPRITE16 reference is IDA-generated from a
  TH04 binary, not attested original source. The remaining 3+9 DATA reserved
  bytes and the eight resident procedures / 564 CODE bytes remain unaccepted
  after the command, formatter and graphics scopes below.
  Do not promote that context from complete-byte equality.
- ZUN -4 now also accepts **nine library command procedures / 361 CODE bytes**, zero private DATA/BSS, thirty
  literal OMF fixups (23 absolute / seven relative). Every actual include slot
  and complete physical contribution passes. Independent guest contracts run
  6,678 cases per image at two loads, execute all 361 bytes and reject nineteen
  instruction mutations. All called scalar and print helpers execute; DOS character/
  exit services and eight real option targets remain explicit bounded interfaces.
  Preserve token-start semicolon handling, skipped text after closing quotes,
  the 65th token overwriting the cursor, unconditional dispatch vector read at
  zero count, inverted optional-number branch and callback PUSHA/ES frames.
  Global state requires DS=driver group; dispatch compares through ES=DS. Error
  text is read from SS, including a separately tested foreign stack segment.
  Guest checks bind the WORD vector read, wrapped cursor and defined carry at
  offsets 7FFF/FFFE/FFFF. Lifecycle/scalar/command scopes cover 38 extents /
  46 procedures / 3,017 CODE bytes; formatter scopes add the following acceptance.
- ZUN -4 also accepts **ten library formatter/print procedures / 677 CODE bytes**,
  zero private DATA/BSS. Actual consumed procedure slots and full native driver
  ownership/context pass. Three relative WORD call fields and one absolute DWORD
  digit-table field are checked literally. Sixteen external digit-table bytes
  add no DATA credit. Direct CFG traversal proves four unconditional jumps at
  7A0/7C0/7E0/800 unreachable, totaling eleven bytes. All other 666 owner bytes
  execute in 6,106 cases per image at two loads; twenty-four actual instruction
  mutations fail. Do not claim execution of the dead bytes. Actual formatter,
  reverse, print and accepted strlen instructions execute; only DOS AH=2 replies
  are bounded services. Keep SS four-byte slots and far strings, DWORD numeric
  values/INT32 minimum, minus-before-padding, ignored string zero flag, WORD
  width wrap and signed padding subtraction. Unknown specifiers lose percent;
  double percent emits no literal percent. Character NUL permits later formatting
  but ends printing. PUSHA restores WORDs while numeric ECX/EDX high halves change.
  The 208-byte wrapper stays unchecked: output 208 zeroes saved BP's low byte;
  209 overwrites both bytes. The model stops before output 210 corrupts the caller
  return word. Full WORD/segment results, DWORD effects/ESP, defined flags, IF/DF,
  forward-string preconditions, split SS, near RET/RETN2, ordered external writes,
  a 356-byte observed stack and all memory outside 512 stack bytes pass. The fresh
  complete cold pair repeats all 23 outputs and entire decoded/stored ZUN. After
  correcting the reviewer's digit-field width, the full formatter review reused
  the still-current source/output-bound pair; no extra native build was needed.
  These scopes cover 48 extents / 56 procedures / 3,694 CODE bytes before graphics.
  `review_th03_zun_format_work.py` builds and reviews; its
  `--current-cold` mode validates existing cold bindings before all formatter gates.
- ZUN -4's **twelve graphics procedures / 814 library CODE bytes** now pass native
  ownership and CPU/interface behavior gates, with zero private DATA/BSS. All
  62 literal WORD fixups (53 absolute, nine relative), complete include slots and
  enclosing native/MAP layout pass. Two unreachable clipping jumps account for
  four bytes; all other 810 bytes execute in 512 cases per image at two loads.
  Twenty-six actual instruction mutants fail. Every nested helper executes.
  The explicit two-page/four-bank word-memory fixture checks page switches,
  ordered stores, full memory, and port widths/values/IF/DF; EGC latches, raster
  operations and physical pixel effects are not modeled. Preserve BYTE width,
  unclamped horizontal position, signed top rejection and no second bottom pass
  after negative-Y clipping. Height zero executes 65,536 row iterations (also
  counted independently by a regression hook); zero word count still advances
  offsets. Row helpers preserve SI/DI, and wrapper saves retain original WORD
  registers/segments/high halves. EGC begin/end unconditionally set IF through
  STI; other row/draw helpers inherit IF. Copy-lower leaves access page one;
  prepare restores access/display zero. Full flag results, split SS, near ABI,
  48-byte observed stack and memory outside 64 stack bytes pass. Whole-driver
  and shared DATA/buffer ownership remain open. Current ZUN totals **60 extents /
  68 procedures / 4,508 CODE bytes**: authored 1,621, library 2,280 and original
  ASM 607 CODE + 783 DATA stay separate. Canonical credit remains zero. Seven
  complete runtime witnesses and 150 short ABI cases are bound by publication.
  Use `review_th03_zun_graphics_work.py` for one cold/formatter/graphics chain;
  its `--current-cold` mode validates prerequisites before rerunning graphics.
- All 99 source objects compile in 100 serial phases. Two independent 613-file
  source trees reproduce all 101 raw OBJ/EXE/MAP outputs; all 268 maintained
  inputs match staging. Only vendor startup/libraries are reused as unowned
  inputs. Current native-owner review passes thirteen owners / 42 functions /
  10,581 bytes and checks all 98 configured extents.
- The enemy source now selects two formation/script and two rendering/update
  objects. Keep the 79-byte `enemies_add()` with `enemy_formation_spawn()`:
  an external far declaration loses TC4's native same-group near-call sequence.
  All 3,325 bytes / 19 entries remain unchanged. Six literal MAP contributions,
  all OMF publics, both MAP public tables and zero private DATA/BSS are checked;
  five native OMF/MAP mutation controls pass. The function credit is unchanged.
  See `config/main_work/enemy_layout_observation.json`.
- Executable chaining and the three playfield-transition functions now have
  accepted natural C++ producers: four functions / 742 bytes, all literal
  relocations and eleven native unit gates pass. An independent 1,110-case
  instruction model covers every byte and rejects ten actual guest mutations.
  It checks far filename/NULL widths, cleanup order, signed AX, stack cleanup,
  every frame byte, signed halving/overflow, geometry, callback and midpoint writes.
  Transition clipping ends at 199; incrementing the byte frame separately keeps
  the compiler's original wrap behavior. BYTE alignment retains the odd `1DC3`
  entry. Only the surrounding 216-byte graphics ASM remains unowned in this
  former HITCIRC group. See `config/main_work/handoff_acceptance.json`.
- The first **1,072 of 1,553 global relocation records** match literally; 242
  ordered positions still differ. Relocation membership and the 124,642-byte
  loaded-image size match. Loaded bytes differ only at `0xEC2D` and `0x1DB05`
  (target `90`, candidate `00`). Header sizes are 6,240 versus 7,680 bytes.
- Last full CI: PASS, 1,950 tests / 284 optional archive skips. Heavy work uses
  one CPU at nice10; latest CI took 5m57s at about 501 MiB peak RSS, no swap. OP's latest SDK-guarded cold
  pair plus cfg/dispatch reviews took 2m37s at 116 MiB; MAINL's pair took 2m59s at 84 MiB with lifecycle/SDK
  checks. The separate shared input/ending wait review took 1m48s at about 149 MiB. The last MAIN
  cold pair and native review took 5m16s at about 505 MiB. The ZUN driver cold
  pair plus TASM control took 8s at 33 MiB; clean JWasm bootstrap took 13s
  at 45 MiB. The latest complete ZUN cold/formatter/graphics chain, including
  all seven models and two native alignment controls, took 4m27s at 223 MiB,
  without swap.

## Maintained producers

| Scope | Source / native producer | Current result |
| --- | --- | --- |
| Entry, round loop, demo, stage/round setup and round finish | `src/main/core/entry.cpp` plus bounded includes; `entry.obj` | One 3,050-byte PLAYFLD producer, records 1,021/1,018/1,011; all 56 literal sites match. Loop uses `-G`, stage returns to `-G-`. |
| Character resources and nine callback setters | `src/main/player/character_setup.cpp`; `ch_setup.obj` | Twelve functions / 3,888 bytes at loaded `0xA44C..0xB37C`; records 1,017/1,023/1,017/831, all 277 sites match. Independent 1,020-case model covers every instruction byte; 16 mutations fail. |
| Stage palette | `src/main/graphics/stage_palette.asm`; `stg_pal.obj` | Four far functions / 130 bytes; 1,556 runtime cases and eight mutations. Two natural EVEN bytes are checked separately. |
| RNG and collision primitives | `src/main/round/primitives.asm`; `roundpr.obj` | Existing 82 bytes at `0xA3FA..0xA44C`, no new credit. MAIN_04 getters remain in root. Ring index 255 aliases the already-incremented index byte on its word read. |
| Chiyuri / Ellen extra attacks | `src/main/player/exatt_chiyuri.cpp`, `exatt_ellen.cpp` | 978 / 1,129 bytes; Ellen includes its 51-byte slot initializer. Native CODE record order matches without OMF rewriting. |
| Shared flight and Reimu extra attack | `src/main/player/exatt_flight_reimu.cpp` plus bounded includes; `ex_rfly.obj`, `ex_reup.obj` | Ten existing functions / 1,156 bytes; natural records 825/331, all eighteen literal pairs match. Separate standalone wrappers preserve scoped replay. No new credit. |
| Combo scoring/display and helpers | `src/main/player/combo.cpp` in two compile modes; `p_combo.obj`, `p_cmbhl.obj` | Five existing functions / 978 bytes; four CODE parts, nine literal pairs. Explicit default CODE identity and same-CS far-call locality preserve all load bytes. No new credit. |
| Loss update, particles, renderer and banners | `src/main/player/lose.cpp` plus bounded includes; `lose.obj` | Four functions / 664 bytes; one native record, ten literal pairs. Renderer adds one accepted function / 177 bytes; near-this and 2,068-case model pass. |

All listed native scopes pass the configured unit gates. Runtime models execute
the actual target/candidate instructions, with explicit bounded stubs for foreign
services; they do not establish real DOS, graphics, sound or device behavior.
Contracts and negative controls live in `scripts/lib/main_*_runtime.py` and tests.
Producer grouping and historical filenames remain inferences. Source ownership,
ABI and byte credit are recorded separately in the ledgers.

## Resume here

1. Inspect Git and run `.venv/bin/python scripts/preflight.py`.
2. OP, MAINL and ZUN now have live complete-byte cold builders, including stored
   packaging. OP's three exit/plane owners and MAINL's four lifecycle owners,
   plus nine shared input owners in each product, pass current source gates; extend these bounded verifiers for further
   reviewed scopes. ZUN's ten logo functions now pass current decoded source gates. All three products
   still have explicit unowned reference/vendor context. Their old
   retained-carrier replay scripts are historical diagnostics, not current build
   inputs. Keep storage equality, ownership and accepted ledger credit separate.
   The shared input review is a current, separate witness bound to both cold
   reports. Replay it after new builds. Ending-specific input waits and OP configuration loading/saving also pass.
   OP demo/score dispatch also passes; its source ledger refines the old screen
   span without adding source bytes. Remaining OP story/VS/attract/menu/resource
   and MAINL resource/ending producers are next
   bounded source/behavior questions. The PMD-mode source still has an explicit
   alignment NOP; do not promote that producer before a natural layout proof.
   ZUN resident -5 and complete original-ASM -2 now also pass current gates.
   Sixteen -4 scalar/library functions, nine command, ten formatter and twelve graphics procedures pass current
   gates. The eight
   paragraph gaps now have native source/link proof in one ordinary TU with
   nine CODE contributions; the complete cold pair and both alignment controls
   are bound by current publication. Before whole-driver promotion, resolve the
   remaining 3+9 DATA reserved bytes and eight unaccepted resident procedures. A private
   ON/OFF contribution probe could not change the tiny model's implicit _DATA
   alignment to PARA (assembler A2078); this does not establish natural trailing
   storage. Do not add an empty segment solely to force the target tail. Further
   source scopes are the remaining resident family and maintained
   launcher/transfer units. Formatter dead jumps stay source-owned with separate
   CFG proof, not runtime coverage. Keep unchecked saved-BP overflow behavior.
   Bind their current native ownership and
   affected behavior without reviving deleted historical verification trees.
3. The loss renderer is now accepted: `player_stuff_t::lose_render()` at loaded
   `0xC248`, all 177 bytes. A near-class Pascal member consumes the observed near
   player word with `RET 2`; it never reads this. Explicit signed16 DI iteration
   plus native member preservation gives the original SI/DI saves without dummy
   register uses. Player fields retain their 128-byte layout and root storage.
   The inferred class organization is not a claim of unique original source.
   Update/particle/render/banner bodies form one 664-byte TC4 record, four entries
   and ten exact literal pairs. The independent renderer model executes all 177
   bytes over 2,068 cases and rejects eight actual mutations. It complements the
   existing 487-byte loss model. See `config/main_work/lose_renderer_acceptance.json`.
4. Combo is split into early scoring/display (491 bytes) and late helpers
   (40 / 103 / 344 bytes). Both normal TUs use explicit `-zCP_COMBO_TEXT` and
   MAIN_04: a helper-derived empty segment name changes far-pointer framing.
   `combo_add_raw` keeps its far Pascal ABI; `samecodeseg` gives the helper the
   original native NOP/PUSH CS/near CALL. Five existing functions / 978 bytes,
   four CODE records and nine literal pairs pass full OMF/public/MAP review.
   Effects/chains/enemy updates, combo helpers/explosion/score, Yumemi charge,
   Rikako bomb and hyper now link in the target sequence. No new source credit.
   See `config/main_work/combo_layout_observation.json`.
   The next mismatch is record **1072**, loaded site `0xDC42`, in state /
   MAIN_010_TEXT. Target order is state 1, first-shot-function 7, state 6,
   first-shot-function 5; later shot/result records occur elsewhere. The first
   shot function is only 173 bytes and its twelve far super_put calls split 7/5.
   A diagnostic with real MAIN_010 player_render and P_SHOT player_shots_add
   declarations before the full state/shot definitions preserves all load bytes
   but reaches only record1073. Native records remain 1024/692 and 1023/474;
   this simple combined-TU organization is not the target record grouping.
5. The root has no initialized HITCIRC or PLAYER_M CODE. Its former bodies live
   in ordinary native producers plus the unowned 216-byte graphics ASM context.
   The zero-length HITCIRC declaration remains BYTE/PUBLIC/USE16; the earlier
   real scaffold retains its WORD segment start. Carrier parsing omits empty
   CODE. Root-renderer removal and unrelated carrier records are checked; all
   library prefix/body and seventeen SHARED contributions retain their bytes.
6. Remaining issues: state/shot relocation interleaving,
   two alignment bytes (`0xEC2D`, `0x1DB05`), MZ header/order and the complete
   four-product source graph. A simple state/shot multi-section TU preserves bytes
   but fails literal order. Ordinary TASM, QUIRKS and MASM51 alignment controls emit
   `00` rather than target `90`. `scripts/probe_th03_main_producers.py` retains the
   member/free renderer control and unresolved state/shot/alignment diagnostics.

Japanese targets remain pinned in `config/targets.toml`, with
`candidate-local-attested` provenance. Re-attest a Ghidra database before using
its observations. Exact work must preserve raw bytes, ordered relocations and
real ABI/layout; do not patch objects or insert padding to manufacture equality.

## Commands and local files

```sh
.venv/bin/python scripts/preflight.py
.venv/bin/python scripts/replay_th03_main_native.py
.venv/bin/python scripts/review_th03_op_dispatch_work.py
.venv/bin/python scripts/build_th03_mainl_work.py
.venv/bin/python scripts/review_th03_shared_input_work.py
.venv/bin/python scripts/publish_th03_op_work_scopes.py
.venv/bin/python scripts/publish_th03_mainl_work_scopes.py
.venv/bin/python scripts/bootstrap_jwasm.py --check
.venv/bin/python scripts/build_th03_zun_driver_work.py
.venv/bin/python scripts/review_th03_zun_graphics_work.py
.venv/bin/python scripts/publish_th03_zun_work_scopes.py
.venv/bin/python scripts/status.py
.venv/bin/python scripts/ci.py
git diff --check
```

The replay command rebuilds two independent source trees and reviews the current
cold pair. Keep `DISPLAY` and `WAYLAND_DISPLAY` empty, use an available single
CPU at nice10 and serialize Borland/Wine writers. Ghidra uses a bounded Java heap
as described in [RE_WORKFLOW.md](RE_WORKFLOW.md).

- Current tree: `.analysis/toolchain/wineprefix/drive_c/TH03WORK` (about 4.4 MiB).
- Current OP tree: `.analysis/toolchain/wineprefix/drive_c/TH03OP`; `--review`
  validates its complete source/output/recipe binding, repeats DIET packaging
  and reruns the exit/plane models. The cfg review command guards actual SDK
  headers around a fresh cold pair and runs the full cfg witness.
  Each full invocation recreates the two source trees; no old project objects
  or historical verification receipts are build inputs.
- Current MAINL tree: `.analysis/toolchain/wineprefix/drive_c/TH03ML` (about
  18 MiB). It retains one source/build tree, including the explicitly unowned
  vendor extraction; both cold rounds are recreated from source.
- Current ZUN tree: `.analysis/toolchain/wineprefix/drive_c/TH03ZUN`. The standalone
  -4 command recreates a separate `TH03ZSP` tree when needed; that duplicate is
  disposable after the whole-product cold build verifies the same outputs.
  `bootstrap_jwasm.py` materializes the pinned compatible emitter when absent;
  the driver builder checks its source/binary identity before and after use.
  JWasm remains private under `.analysis/toolchain/extra/jwasm`; base Borland
  tool identities and the canonical Japanese targets are unchanged.
- Current reports: `.analysis/work/main-build.json`, `main-unit-review.json`,
  `op-build.json`, `mainl-build.json`, `zun-build.json`, `zun-driver-build.json` and `ci.log`.
- Keep the targets, installed tools, local Wine prefix, runtime image and Ghidra
  databases. `.analysis` is about 1.3 GiB, mostly the Wine runtime itself.
- Old runs, probes, logs and caches are disposable even if historical evidence
  names them. Use fresh source builds for new acceptance. Toolchain execution
  probes now remove their temporary DOS workspaces on success or failure.

See [scripts/README.md](../scripts/README.md) for command roles and
[PROGRESS.md](PROGRESS.md) for ledger-derived counts.
