# TH03 handoff

Commit format: `gpt-6.1-sol: xxx`. Use local headless tools; no Factory MCP.
Read `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/RE_WORKFLOW.md` and the local
`th03-re` skill before reconstruction. The full project introduction and setup
remain in [README.md](../README.md).

## Current state

- Previous pushed checkpoint: `db89e6c` (character/HUD literal order restored).
- MAIN: **444 exact functions / 75,140 bytes / 97 CODE extents**. These are
  reviewed source scopes; the full product is not exact. The whole-game source
  denominator is unknown. OP, MAINL and ZUN have no accepted product exactness.
- OP now has a live, source-only cold build independent of the deleted historical
  receipts: 330 inputs, all 30 objects rebuilt twice, all 32 raw OBJ/EXE/MAP outputs
  repeat. The complete 63,866-byte decoded EXE, 59,770-byte load image and all
  607 literal relocations match. Two DIET `-B` packs match the complete canonical
  36,041-byte stored target and restore to the actual linked EXE. TH04's `-G`
  selects a larger SFX stub and fails this TH03 target (36,136 bytes).
  Frozen reference source and vendor libraries remain unowned context; this is
  a fresh complete-byte build observation, not ownership/ABI or runtime acceptance.
  See `config/op_work/observation.json` and `scripts/build_th03_op_work.py`.
- MAINL now has the corresponding live cold build: 1,912 source inputs, 36 project
  objects and six maintained CRT objects per round. Normal TLIB extraction/rebuild
  preserves all 893 vendor member positions, substitutes the six real producers,
  and preserves the other 887 members' program records. All 938 raw outputs repeat.
  The complete 67,372-byte decoded EXE and all 677 ordered relocations match;
  both DIET `-B` packs equal the canonical 37,975-byte stored target. This remains
  a complete-byte build observation with explicit reference/vendor context, not
  new ownership/ABI/runtime acceptance. See `config/mainl_work/observation.json`.
- ZUN now has a complete live cold build: 110 source inputs plus explicit vendor
  `MASTERS.LIB` and the -1 payload. All 23 raw OBJ/COM/MAP/composition/packed outputs
  repeat. All five payloads and the entire 22,812-byte decoded launcher match;
  both DIET `-B` packs equal the canonical 16,242-byte stored target. Fourteen
  bounded wrapper cases match, and a wrong transfer address is rejected. The
  -2 OMF resolver checks its complete 607 CODE / 783 DATA partition; -4 checks
  all 55 procedures / 56 public addresses and WORD/USE16/DGROUP layout. Vendor
  startup/runtime, MASTERS.LIB, -1 and forwarded headers remain unowned context;
  formal source/behavior acceptance stays separate. See `config/zun_work/observation.json`.
- ZUN -4 uses the separately pinned compatible JWasm OMF emitter and normal TLINK.
  Its instruction/data/procedure includes are unchanged; staging only adapts
  model declaration order, variadic macro spelling and include separators. The
  original assembler remains unknown. The standalone producer and its ten-byte
  TASM negative control remain replayable through `build_th03_zun_driver_work.py`.
  The complete builder compiles the driver itself without consuming that tree.
- All 99 source objects compile in 100 serial phases. Two independent 609-file
  source trees reproduce all 101 raw OBJ/EXE/MAP outputs; all 265 maintained
  inputs match staging. Only vendor startup/libraries are reused as unowned
  inputs. Current native-owner review passes twelve owners / 41 functions /
  10,404 bytes and checks all 97 configured extents.
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
- The first **780 of 1,553 global relocation records** match literally; 550
  ordered positions still differ. Relocation membership and the 124,642-byte
  loaded-image size match. Loaded bytes differ only at `0xEC2D` and `0x1DB05`
  (target `90`, candidate `00`). Header sizes are 6,240 versus 7,680 bytes.
- Last full CI: PASS, 1,765 tests / 284 optional archive skips. Heavy work uses
  one CPU at nice10; latest CI took 3m05s at 423 MiB peak RSS. OP's initial cold
  pair took 2m04s at 44 MiB; MAINL's pair took 2m55s at 63 MiB. The last MAIN
  cold pair and native review took 5m03s at about 520 MiB. The ZUN driver cold
  pair plus TASM
  control took 10s at 33 MiB; clean JWasm bootstrap took 13s at 45 MiB.
  The complete ZUN cold pair took 52s at 64 MiB.

## Maintained producers

| Scope | Source / native producer | Current result |
| --- | --- | --- |
| Entry, round loop, demo, stage/round setup and round finish | `src/main/core/entry.cpp` plus bounded includes; `entry.obj` | One 3,050-byte PLAYFLD producer, records 1,021/1,018/1,011; all 56 literal sites match. Loop uses `-G`, stage returns to `-G-`. |
| Character resources and nine callback setters | `src/main/player/character_setup.cpp`; `ch_setup.obj` | Twelve functions / 3,888 bytes at loaded `0xA44C..0xB37C`; records 1,017/1,023/1,017/831, all 277 sites match. Independent 1,020-case model covers every instruction byte; 16 mutations fail. |
| Stage palette | `src/main/graphics/stage_palette.asm`; `stg_pal.obj` | Four far functions / 130 bytes; 1,556 runtime cases and eight mutations. Two natural EVEN bytes are checked separately. |
| RNG and collision primitives | `src/main/round/primitives.asm`; `roundpr.obj` | Existing 82 bytes at `0xA3FA..0xA44C`, no new credit. MAIN_04 getters remain in root. Ring index 255 aliases the already-incremented index byte on its word read. |
| Chiyuri / Ellen extra attacks | `src/main/player/exatt_chiyuri.cpp`, `exatt_ellen.cpp` | 978 / 1,129 bytes; Ellen includes its 51-byte slot initializer. Native CODE record order matches without OMF rewriting. |
| Shared flight and Reimu extra attack | `src/main/player/exatt_flight_reimu.cpp` plus bounded includes; `ex_rfly.obj`, `ex_reup.obj` | Ten existing functions / 1,156 bytes; natural records 825/331, all eighteen literal pairs match. Separate standalone wrappers preserve scoped replay. No new credit. |
| Lose update, particles and banners | `src/main/player/lose.cpp` | Three functions / 487 bytes. The separate renderer is still unresolved. |

All listed native scopes pass the configured unit gates. Runtime models execute
the actual target/candidate instructions, with explicit bounded stubs for foreign
services; they do not establish real DOS, graphics, sound or device behavior.
Contracts and negative controls live in `scripts/lib/main_*_runtime.py` and tests.
Producer grouping and historical filenames remain inferences. Source ownership,
ABI and byte credit are recorded separately in the ledgers.

## Resume here

1. Inspect Git and run `.venv/bin/python scripts/preflight.py`.
2. OP, MAINL and ZUN now have live complete-byte cold builders, including stored
   packaging. Promote decoded/source ownership only through fresh scoped gates;
   all three still have explicit unowned reference/vendor context. Their old
   retained-carrier replay scripts are historical diagnostics, not current build
   inputs. Keep storage equality, ownership and accepted ledger credit separate.
3. MAIN links the Kana/collision/HUD/Marisa/Kotohime sequence after `tr_ctx`,
   then `ex_rfly`, `ex_reup`, Reimu charge/bomb, intro and Mima charge/extra/boss.
   Shared flight (215 bytes) and the Reimu prefix (610 bytes) now compile into one
   natural 825-byte TC4 record. Descending FIXUPP order emits prefix relocations
   before flight relocations; update/render is a separate 331-byte record.
   Ten functions / 1,156 existing bytes, eighteen literal pairs, two MAP allocations
   and twenty public-table entries are checked, with no private DATA/BSS or new
   function credit. All bodies live in bounded includes with one shared entity
   declaration. Standalone scoped replay variants use the same bodies; the live
   response selects only the two grouped producers. See
   `config/main_work/reimu_order_observation.json`.
   The next mismatch is record **780**, loaded site `0x159AA`, in `hitbox` /
   HITBOX_TEXT. Native OMF shows hitbox has one 266-byte HITBOX contribution, while
   the Mima bomb has only 833 BULLET bytes and target records 1296..1308. Try
   early-linking hitbox alone after the Mima boss; keep the bomb late. Earlier
   same-segment conflict reasoning was disproved by these native allocations.
   `state` and `shotroot` also retain interleaved runs.
4. The root has no initialized HITCIRC CODE. Its prior nine procedures / 958 bytes
   live in graphics reference context, accepted executable chaining and accepted
   transitions. The zero-length root declaration is now BYTE/PUBLIC/USE16:
   a trailing WORD declaration rounds up the odd collision-circle end and moves
   later segments. The earlier real scaffold retains the WORD-aligned segment
   start. Native OMF size/attributes and its literal MAP contribution are checked;
   a checksum-valid WORD mutation is rejected. The carrier parser omits empty CODE.
   Moving the whole root can still change PLAYER_M placement. Library prefix/body
   and all 17 SHARED objects retain their physical contributions.
5. Other open issues: renderer emits 175 instead of 177 bytes (target saves SI
   and DI); state/shot relocation interleaving; the two alignment bytes; MZ
   header/order and the complete four-product source graph. Combining state and
   shot into a simple multi-section TU preserved bytes but failed literal order.
   Ordinary TASM, QUIRKS and MASM51 alignment controls still emitted `00`.
   `scripts/probe_th03_main_producers.py` can replay these diagnostic controls.
   The DATA mismatch at `0x1DB05` lies between `vsync_OldMask` and `BYTE_MASK`.

Japanese targets remain pinned in `config/targets.toml`, with
`candidate-local-attested` provenance. Re-attest a Ghidra database before using
its observations. Exact work must preserve raw bytes, ordered relocations and
real ABI/layout; do not patch objects or insert padding to manufacture equality.

## Commands and local files

```sh
.venv/bin/python scripts/preflight.py
.venv/bin/python scripts/replay_th03_main_native.py
.venv/bin/python scripts/build_th03_op_work.py
.venv/bin/python scripts/build_th03_mainl_work.py
.venv/bin/python scripts/bootstrap_jwasm.py --check
.venv/bin/python scripts/build_th03_zun_driver_work.py
.venv/bin/python scripts/build_th03_zun_work.py
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
  validates its complete source/output binding and repeats only DIET packaging.
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
