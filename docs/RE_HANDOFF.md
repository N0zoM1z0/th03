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
- All 95 source objects compile in 96 serial phases. Two independent 589-file
  source trees reproduce all 97 raw OBJ/EXE/MAP outputs; all 249 maintained
  inputs match staging. Only vendor startup/libraries are reused as unowned
  inputs. Current native-owner review passes ten owners / 37 functions /
  9,662 bytes and checks all 95 configured extents.
- The first **394 of 1,553 global relocation records** match literally; 947
  ordered positions still differ. Relocation membership and the 124,642-byte
  loaded-image size match. Loaded bytes differ only at `0xEC2D` and `0x1DB05`
  (target `90`, candidate `00`). Header sizes are 6,240 versus 7,680 bytes.
- Last full CI: PASS, 1,720 tests / 300 optional archive skips. Heavy work uses
  one CPU at nice10; latest CI took 3m05s at 382 MiB peak RSS. The last native
  review peaked at about 534 MiB.

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
2. Investigate global relocation record **394** (zero-based), loaded site `0x185A6`
   in `chiyuri_bomb`. Mapping the canonical vector through the current MAP gives
   `b_chiyu` at records 394–406, `ex_chyu` at 407–429 and `cs_chiyu` at 430–438.
   This is a read-only observation; no early-link experiment has been run.
   `src/main/boss/order.asm` currently predeclares CODE segments only through
   E_EXPL_TEXT. Preserve segment-first-declaration order when moving MAIN_05
   objects; extending genuine segment declarations is an untested hypothesis.
3. Root HITCIRC context is now 958 bytes from loaded `0xB37C`. Moving the entire
   root earlier is known to change PLAYER_M placement. The library prefix/body
   split and all 17 SHARED objects already preserve their physical contributions.
4. Other open issues: renderer emits 175 instead of 177 bytes (target saves SI
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
.venv/bin/python scripts/status.py
.venv/bin/python scripts/ci.py
git diff --check
```

The replay command rebuilds two independent source trees and reviews the current
cold pair. Keep `DISPLAY` and `WAYLAND_DISPLAY` empty, use an available single
CPU at nice10 and serialize Borland/Wine writers. Ghidra uses a bounded Java heap
as described in [RE_WORKFLOW.md](RE_WORKFLOW.md).

- Current tree: `.analysis/toolchain/wineprefix/drive_c/TH03WORK` (about 4.4 MiB).
- Current reports: `.analysis/work/main-build.json`, `main-unit-review.json`
  and `ci.log`, overwritten by their respective commands.
- Keep the targets, installed tools, local Wine prefix, runtime image and Ghidra
  databases. `.analysis` is about 1.3 GiB, mostly the Wine runtime itself.
- Old runs, probes, logs and caches are disposable even if historical evidence
  names them. Use fresh source builds for new acceptance. Toolchain execution
  probes now remove their temporary DOS workspaces on success or failure.

See [scripts/README.md](../scripts/README.md) for command roles and
[PROGRESS.md](PROGRESS.md) for ledger-derived counts.
