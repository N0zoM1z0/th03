# TH03 handoff

Commit format: `gpt-6.1-sol: xxx`. Use local headless tools; no Factory MCP.
Read `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/RE_WORKFLOW.md` and the local
`th03-re` skill before reconstruction. The full project introduction and setup
remain in [README.md](../README.md).

## Current state

- Previous pushed checkpoint: `0e56dae` (native logo alignment and current ZUN source acceptance).
- MAIN: **445 exact functions / 75,317 bytes / 98 CODE extents**. These are
  reviewed source scopes; the full product is not exact. The whole-game source
  denominator is unknown. OP, MAINL and ZUN have no accepted whole-product source exactness.
- OP now has **three accepted decoded source functions / 133 bytes**: exit to
  DOS, VRAM plane setup and game cleanup. The current graph consumes all three
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
  product source ownership. Replay with `publish_th03_op_work_scopes.py`.
- OP now has a live, source-only cold build independent of the deleted historical
  receipts: 330 inputs, all 30 objects rebuilt twice, all 32 raw OBJ/EXE/MAP outputs
  repeat. The complete 63,866-byte decoded EXE, 59,770-byte load image and all
  607 literal relocations match. Two DIET `-B` packs match the complete canonical
  36,041-byte stored target and restore to the actual linked EXE. TH04's `-G`
  selects a larger SFX stub and fails this TH03 target (36,136 bytes).
  Frozen reference source and vendor libraries remain unowned context; this is
  a fresh complete-byte build observation; the three scoped owners above have
  their separate ownership/ABI/runtime acceptance.
  See `config/op_work/observation.json` and `scripts/build_th03_op_work.py`.
- MAINL now has the corresponding live cold build: 1,912 source inputs, 36 project
  objects and six maintained CRT objects per round. Normal TLIB extraction/rebuild
  preserves all 893 vendor member positions, substitutes the six real producers,
  and preserves the other 887 members' program records. All 938 raw outputs repeat.
  The complete 67,372-byte decoded EXE and all 677 ordered relocations match;
  both DIET `-B` packs equal the canonical 37,975-byte stored target. This remains
  a complete-byte build observation with explicit reference/vendor context; the
  four lifecycle owners below have their independent current source acceptance.
  See `config/mainl_work/observation.json`.
- MAINL now has **four accepted decoded source functions / 210 bytes**: plane
  setup, cleanup, initialization and return to MAIN. Their actual first-use
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
- ZUN -4 uses the separately pinned compatible JWasm OMF emitter and normal TLINK.
  Its instruction/data/procedure includes are unchanged; staging only adapts
  model declaration order, variadic macro spelling and include separators. The
  original assembler remains unknown. The standalone producer and its ten-byte
  TASM negative control remain replayable through `build_th03_zun_driver_work.py`.
  The complete builder compiles the driver itself without consuming that tree.
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
- Last full CI: PASS, 1,836 tests / 284 optional archive skips. Heavy work uses
  one CPU at nice10; latest CI took 4m10s at 395 MiB peak RSS, no swap. OP's latest cold
  pair with the current exit/plane models took 2m32s at 68 MiB; MAINL's pair took
  3m10s at 83 MiB with lifecycle/SDK checks. The last MAIN
  cold pair and native review took 5m16s at about 505 MiB. The ZUN driver cold
  pair plus TASM
  control took 10s at 33 MiB; clean JWasm bootstrap took 13s at 45 MiB.
  The complete ZUN cold pair with both logo/resident models took 1m38s at 121 MiB,
  with no swap.

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
   packaging. OP's three exit/plane owners and MAINL's four lifecycle owners now
   pass current decoded source gates; extend these bounded verifiers for further
   reviewed scopes. ZUN's ten logo functions now pass current decoded source gates. All three products
   still have explicit unowned reference/vendor context. Their old
   retained-carrier replay scripts are historical diagnostics, not current build
   inputs. Keep storage equality, ownership and accepted ledger credit separate.
   ZUN resident -5 now also passes current gates. Next scopes are the -2 and -4
   driver units. Bind their current native ownership and
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
.venv/bin/python scripts/build_th03_op_work.py
.venv/bin/python scripts/publish_th03_op_work_scopes.py
.venv/bin/python scripts/build_th03_mainl_work.py
.venv/bin/python scripts/publish_th03_mainl_work_scopes.py
.venv/bin/python scripts/bootstrap_jwasm.py --check
.venv/bin/python scripts/build_th03_zun_driver_work.py
.venv/bin/python scripts/build_th03_zun_work.py
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
  and reruns the exit/plane models.
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
