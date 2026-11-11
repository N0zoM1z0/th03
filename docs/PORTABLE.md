# TH03 semantic and 64-bit port

`port/modern-64` builds native C++17 for Linux/SDL2 and Windows x64/Win32-GDI.
Title, menus, character selection and MAINL stage introduction join through
explicit resident state into MAIN round initialization. Enemy scripts, battle
resources/HUD, round-introduction animation, collision primitives and bullets are also
ported and checked separately. The program stops at initialized battle state;
it is not yet a playable full-game port. Player/CPU combat, all attack families,
backgrounds, results/dialogues/endings, Music Room/HiScore, audio and persistence
still need integration and campaign testing.

The DOS reconstruction stays on `main`. The live Windows DOSBox session and
`D:\Entertainment\Game\Touhou\th03-reconstruct\play.hdi` are independent.
Do not replace that disk, send input to its window or restart its emulator.
The native program reads external original data; it executes no DOS code and
writes no saves yet. Add a separate save directory before implementing writes.

## Build and inspect

The local port checkout is `.analysis/native/port64/` inside the DOS checkout.
Use one CPU at nice10 for builds. Its ignored `build/` and runtime state remain
separate from DOS/Wine/analyzer state.

```sh
cmake -S port64 -B build/linux-x64 -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build/linux-x64 --parallel 1
ctest --test-dir build/linux-x64 --output-on-failure
build/linux-x64/th03-port64 --hdi /path/to/original/zun.hdi \
  --font-bmp /path/to/FREECG98.BMP --scene menu
```

The font is an external 2048x2048 monochrome Anex86-format PC-98 BMP, also
accepted by DOSBox-X. MAINL introductions require it; menu/selection do not.
Windows cross-build:

```sh
cmake -S port64 -B build/windows-x64 -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_TOOLCHAIN_FILE="$PWD/port64/mingw64-toolchain.cmake"
cmake --build build/windows-x64 --parallel 1
```

MinGW runtime libraries are linked statically. Use `--headless` for native
Windows background checks; it opens no window and takes no keyboard input.
GUI checks belong on private Xvfb, not the user's active DOS desktop.

Arrows move through single-player menus; Z/Enter confirms and Escape returns.
The original title initially hides menu labels; a direction reveals them.
Two-player P1 uses T/F/H/B with Z/X; P2 uses keypad movement with Left/Right
for Shot/Bomb. Option changes rank, sound-mode and key-mode state in memory.

Useful headless scenes:

```sh
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --scene story-select --screenshot selection.ppm
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --font-bmp /path/to/FREECG98.BMP --scene stage-intro \
  --characters 5,13 --frames 20 --screenshot intro.ppm
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --scene battle-ready --characters 5,13 --screenshot ready.ppm
```

`--characters` supplies two paletted IDs 1..18; `--stage` is zero-based.
`--frames` advances idle headless VBlanks or limits a window run. `--inputs`
accepts comma-separated original WORD masks, or tuples `SP:P1:P2`, one per
VBlank. Use release samples between presses. Selection samples every three
VBlanks after its initial 30-frame wait. `--help` lists supported scenes.

`--list`, `--extract NAME --output FILE` and `--pi NAME --packed FILE` inspect
OP/MAINL resources. `--main-assets --list` or `--main-assets --extract ...`
selects the second PF for resource inspection. `--archive` accepts an extracted
PF instead of the HDI. Keep output files outside original media and the user's
playable disk.

## Comparisons

The FAT/PF reader, PI decoder, font bitmap reader and master.lib motion adapt
TH04 `port/modern-64` revision `1ba7107` (MIT). TH03 owns its CP932 archive names,
resident/OP flow and graphics/gameplay semantics. The original Japanese targets
pinned in `config/targets.toml` remain the baseline. These native checks do not
add source-exact credit to DOS ledgers.

Run the original-instruction checks with the DOS checkout's Python environment
(Unicorn/Capstone). Set `DOS` to that checkout and `NATIVE` to this branch's
`build/linux-x64` directory. Image comparisons also need ImageMagick `convert`.

| Check | Command arguments after the script | Evidence compared |
|---|---|---|
| `check_title.py` | `--native "$NATIVE/th03-port64" --dos-root "$DOS" --dos-frame "$DOS/.analysis/runtime/candidates/dos-replay-rebuilt/menu.png" --output /new/private/output` | All128,000 decoded PI bytes and the complete DOS menu RGB frame |
| `check_selection.py` | `--native-checks "$NATIVE/th03-port64-checks" --dos-root "$DOS"` | OP selection/lock/palette state, complete curve rasters and story opponent/seed policy |
| `check_intro.py` | `--native "$NATIVE/th03-port64" --dos-root "$DOS"` | Complete Marisa/Rikako Stage1 DOS frame, minimum wait and fade handoff |
| `check_round.py` | `--native "$NATIVE/th03-port64" --native-checks "$NATIVE/th03-port64-checks" --dos-root "$DOS"` | Six MAIN initializers, including LCG, backward ring fill, player thresholds and both formation rings |
| `check_enemy.py` | Same arguments as `check_round.py` | Six enemy scripts over 1,237 ticks, including real movement/vector callees |
| `check_battle_graphics.py` | Same arguments as `check_intro.py` | Unchanged DOS borders, P1 gauge/score and TRAM glyph ink |
| `check_hud_intro.py` | Same arguments as `check_selection.py` | 520 story/versus frames: slide/banner state, all128 particles, seed and ring cursor |
| `check_collision.py` | Same arguments as `check_selection.py` | Six complete 6,624-byte bitmaps and their player hit scans |
| `check_bullet.py` | Same arguments as `check_selection.py` | Group vectors, full bullet/trail pools, motion/transfer/cloud/clearing, collision maps and complete pellet rasters |

Linux and native Windows x64 state checks pass; menu, selection and isolated
introduction PPMs agree between platforms. Private SDL window checks exercised
menu/Option/selection on Xvfb. Original captures and local evidence live in the
DOS checkout's `.analysis/work/` and `.analysis/runtime/candidates/`.
`th03-port64-checks --hud-picture HDI 100 FILE.ppm` renders an isolated round
introduction without running the surrounding battle loop.

## Integration findings and next work

Keep the original draw/call order and explicit integer widths. The current
source preserves these consequential details:

- OP's opponent generator uses a local LCG copy; MAIN seeds anew from the
  resident frame counter. Random-ring fill runs backward and retains its
  cursor. Its WORD getter increments the cursor before loading, so index255
  reads the wrapped cursor as its high byte.
- Stage setup assigns initial versus gauge levels after round preparation,
  replacing the preparation's rank increment. The round counter is DWORD;
  the round/result counter is WORD.
- The first formation randomizer reads an uninitialized stack byte, attested
  as `0x5e` from C0's saved InitStart. `Round::prepare` takes that context
  explicitly. Recover later-round stack context before joining restarts.
- TH03's C++ graphics-font renderer uses alternate JIS-row ANK and WORD-truncated
  bold weight. TH04's ASM renderer differs. SPRITE16 uses physical 200-line
  graphics and whole-column clipping; TRAM stays at 400 lines with fixed text
  colors. Graphics score digit5 differs by one dot from `NUM8.BF2`.
- The round-introduction slide destination aliases particle15.x. Collision Y
  reports the scan rectangle's top, not the occupied row; X reports the
  containing eight-tile column. Preserve these coarse values for CPU decisions.

`bullet.cpp` retains the 320-slot pool, shared 48-slot trail ring, byte-wrapped
speed tuning and ascending update order. Derived groups can occupy later slots
and update on that same tick. The pellet explosion query is an explicit foreign
service until the chain owner is joined. Six full spawn pools, nine update
fixtures, sixteen group vectors and five complete pellet rasters agree with
original MAIN instructions. These include the transfer target's pixel rounding,
independent X/Y trail updates and the narrow pellet-write path. The authored
ReC98 pellet bitmap retains the distinct dots in transfer preshifts6/14.
Native Windows x64 transfer/trail states and collision maps agree with Linux.

Continue with backgrounds and the player/CPU combat loop, then join attack
families and result/MAINL routes. Wide CPU scans near the left edge can read
outside the bitmap through wrapped DGROUP addressing. Recover those aliased
DATA owners before joining that path; the isolated collision module currently
reports an unresolved owner instead of treating the memory as empty. The
original ENEDAT does not use its broken loop opcodes; custom loop scripts would
also need the original indeterminate stack context.
