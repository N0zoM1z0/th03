# TH03 handoff

Commit format: `gpt-6.1-sol: xxx`. Use local headless tools; no Factory MCP.
Read `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/RE_WORKFLOW.md` and the local
`th03-re` skill before reconstruction. The full project introduction and setup
remain in [README.md](../README.md).

## Current state

- Reconstruction source baseline: `83b196d` (native character setup accepted).
- MAIN: **440 exact functions / 74,398 bytes / 95 CODE extents**. These are
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
- ZUN's complete -4 sprite16 driver now matches all 4,224 decoded payload bytes.
  Two fresh source builds reproduce raw OMF/COM/MAP; all 55 procedures / 56 public
  addresses, WORD/USE16 segments and DGROUP order pass. A compatible JWasm OMF
  emitter plus the existing TLINK naturally resolves TASM's ten differing bytes.
  Only MODEL/386 declaration order, variadic macro spelling and include separators
  change in staging; instruction/data/procedure includes stay byte-identical.
  The original assembler is unknown. Public JWasm source and executable are
  pinned separately in `config/th03_zun_driver_jwasm.toml`; an independent clean
  source rebuild reproduces its executable digest. The TASM path is a fresh
  ten-byte negative control. Full ZUN storage and formal source acceptance remain
  open. See `config/zun_driver_work/observation.json`.
- All 95 source objects compile in 96 serial phases. Two independent 589-file
  source trees reproduce all 97 raw OBJ/EXE/MAP outputs; all 249 maintained
  inputs match staging. Only vendor startup/libraries are reused as unowned
  inputs. Current native-owner review passes ten owners / 37 functions /
  9,662 bytes and checks all 95 configured extents.
- The first **394 of 1,553 global relocation records** match literally; 947
  ordered positions still differ. Relocation membership and the 124,642-byte
  loaded-image size match. Loaded bytes differ only at `0xEC2D` and `0x1DB05`
  (target `90`, candidate `00`). Header sizes are 6,240 versus 7,680 bytes.
- Last full CI: PASS, 1,735 tests / 284 optional archive skips. Heavy work uses
  one CPU at nice10; latest CI took 2m36s at 395 MiB peak RSS. OP's initial cold
  pair took 2m04s at 44 MiB; MAINL's pair took 2m55s at 63 MiB. The last MAIN
  native review peaked at about 534 MiB. The ZUN driver cold pair plus TASM
  control took 10s at 33 MiB; clean JWasm bootstrap took 13s at 45 MiB.

## Maintained producers

| Scope | Source / native producer | Current result |
| --- | --- | --- |
| Entry, round loop, demo, stage/round setup and round finish | `src/main/core/entry.cpp` plus bounded includes; `entry.obj` | One 3,050-byte PLAYFLD producer, records 1,021/1,018/1,011; all 56 literal sites match. Loop uses `-G`, stage returns to `-G-`. |
| Character resources and nine callback setters | `src/main/player/character_setup.cpp`; `ch_setup.obj` | Twelve functions / 3,888 bytes at loaded `0xA44C..0xB37C`; records 1,017/1,023/1,017/831, all 277 sites match. Independent 1,020-case model covers every instruction byte; 16 mutations fail. |
| Stage palette | `src/main/graphics/stage_palette.asm`; `stg_pal.obj` | Four far functions / 130 bytes; 1,556 runtime cases and eight mutations. Two natural EVEN bytes are checked separately. |
| RNG and collision primitives | `src/main/round/primitives.asm`; `roundpr.obj` | Existing 82 bytes at `0xA3FA..0xA44C`, no new credit. MAIN_04 getters remain in root. Ring index 255 aliases the already-incremented index byte on its word read. |
| Chiyuri / Ellen extra attacks | `src/main/player/exatt_chiyuri.cpp`, `exatt_ellen.cpp` | 978 / 1,129 bytes; Ellen includes its 51-byte slot initializer. Native CODE record order matches without OMF rewriting. |
| Lose update, particles and banners | `src/main/player/lose.cpp` | Three functions / 487 bytes. The separate renderer is still unresolved. |

All listed native scopes pass the configured unit gates. Runtime models execute
the actual target/candidate instructions, with explicit bounded stubs for foreign
services; they do not establish real DOS, graphics, sound or device behavior.
Contracts and negative controls live in `scripts/lib/main_*_runtime.py` and tests.
Producer grouping and historical filenames remain inferences. Source ownership,
ABI and byte credit are recorded separately in the ledgers.

## Resume here

1. Inspect Git and run `.venv/bin/python scripts/preflight.py`.
2. Prioritize the fresh ZUN source build, then OP/MAINL decoded owner acceptance.
   OP and MAINL now have live cold builders; their old native receipts are no
   longer needed for whole-file byte observations. ZUN -4 now has a complete
   byte-matching live source producer. Rebuild wrapper/-2/-3/-5 from their
   maintained sources, keep the -1 vendor payload explicitly unowned, compose all
   actual fresh outputs, then reproduce stored DIET packaging. Old composition
   scripts consume deleted retained carriers and pin the old ten-byte driver
   failure; they are historical diagnostics, not the new builder's backend.
   Keep storage equality, source ownership and accepted ledger credit separate.
3. For MAIN whole-link work, investigate global relocation record **394**
   (zero-based), loaded site `0x185A6`
   in `chiyuri_bomb`. Mapping the canonical vector through the current MAP gives
   `b_chiyu` at records 394–406, `ex_chyu` at 407–429 and `cs_chiyu` at 430–438.
   This is a read-only observation; no early-link experiment has been run.
   `src/main/boss/order.asm` currently predeclares CODE segments only through
   E_EXPL_TEXT. Preserve segment-first-declaration order when moving MAIN_05
   objects; extending genuine segment declarations is an untested hypothesis.
4. Root HITCIRC context is now 958 bytes from loaded `0xB37C`. Moving the entire
   root earlier is known to change PLAYER_M placement. The library prefix/body
   split and all 17 SHARED objects already preserve their physical contributions.
5. Other open issues: renderer emits 175 instead of 177 bytes (target saves SI
   and DI); state/shot relocation interleaving; the two alignment bytes; MZ
   header/order and the complete four-product source graph. Combining state and
   shot into a simple multi-section TU preserved bytes but failed literal order.
   Ordinary TASM, QUIRKS and MASM51 alignment controls still emitted `00`.
   `scripts/probe_th03_main_producers.py` can replay these diagnostic controls.

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
- Current ZUN driver tree: `.analysis/toolchain/wineprefix/drive_c/TH03ZSP`.
  `bootstrap_jwasm.py` materializes the pinned compatible emitter when absent;
  the driver builder checks its source/binary identity before and after use.
  JWasm remains private under `.analysis/toolchain/extra/jwasm`; base Borland
  tool identities and the canonical Japanese targets are unchanged.
- Current reports: `.analysis/work/main-build.json`, `main-unit-review.json`,
  `op-build.json`, `mainl-build.json`, `zun-driver-build.json` and `ci.log`.
- Keep the targets, installed tools, local Wine prefix, runtime image and Ghidra
  databases. `.analysis` is about 1.3 GiB, mostly the Wine runtime itself.
- Old runs, probes, logs and caches are disposable even if historical evidence
  names them. Use fresh source builds for new acceptance. Toolchain execution
  probes now remove their temporary DOS workspaces on success or failure.

See [scripts/README.md](../scripts/README.md) for command roles and
[PROGRESS.md](PROGRESS.md) for ledger-derived counts.
