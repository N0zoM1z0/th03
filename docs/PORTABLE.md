# TH03 semantic and 64-bit port

`port/modern-64` contains native C++17 HDI/PF assets, PI/CDG/BFNT graphics,
title/menu/Option state, story/versus character selection and MAINL stage introductions. Linux
uses SDL2; Windows x64 uses Win32/GDI. No DOS executable is executed by this
program. Game data remains external.

The DOS reconstruction stays on `main`. The user's Windows DOSBox session and
its `D:\Entertainment\Game\Touhou\th03-reconstruct\play.hdi` are separate
from this work. Do not replace that disk, send it input, restart its emulator
or publish a portable preview into its directory while the user is playing.

## Build and run

From this branch's checkout, with CMake, Ninja, a C++17 compiler and SDL2:

```sh
cmake -S port64 -B build/linux-x64 -G Ninja -DCMAKE_BUILD_TYPE=Debug
cmake --build build/linux-x64 --target th03-port64 th03-port64-checks --parallel 1
ctest --test-dir build/linux-x64 --output-on-failure
build/linux-x64/th03-port64 --hdi /path/to/original/zun.hdi --scene menu
```

Use one CPU at nice10 for builds and private Xvfb for GUI checks. The active
local checkout is `.analysis/native/port64/` in the DOS worktree. Its own
`build/` directory is ignored. It reads the DOS worktree's original HDI using
an explicit absolute `--hdi` path; mutable Wine/analyzer state is not shared.

Windows cross-build:

```sh
cmake -S port64 -B build/windows-x64 -G Ninja -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_TOOLCHAIN_FILE="$PWD/port64/mingw64-toolchain.cmake"
cmake --build build/windows-x64 --target th03-port64 --parallel 1
```

`th03-port64.exe` links MinGW runtime libraries statically. For background
checks, use `--headless`; this creates no Windows window and takes no keyboard
input. Do not start a portable window on the user's active desktop during DOS
playtesting.

The title starts with hidden labels. A direction opens the menu. Arrows move,
Z/Enter confirms and Escape returns/quits. Option changes rank, sound-mode
state and key-mode state in memory. There is no sound synthesis or save writer
yet. Start enters story selection; VS opens the three original match modes and
then selection. Completion prepares the resident characters, opponent order
and CPU flags, then displays the original MAINL stage introduction before
stopping at the MAIN handoff. Gameplay, Music Room, HiScore and attract
playback remain to be joined. The goal is a
complete playable port; this intermediate build is not a full game preview.

Headless examples:

```sh
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --scene menu --screenshot menu.ppm
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --scene options --inputs 8,0,4096 --screenshot options-return.ppm
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --list
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --pi TL02.PI --packed title.pixels
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --scene story-select --screenshot selection.ppm
```

`--inputs` supplies original hexadecimal or decimal WORD input masks, one per
VBlank; use zero between separate presses. A tuple `SP:P1:P2` supplies the
interface and both independent player words. Selection samples once per three
VBlanks after its initial 30-frame loading wait; held/released samples must
span that cadence. `--frames` advances idle headless frames or limits a window
run. `--archive` can replace `--hdi` for
an extracted original PF. `--extract NAME --output FILE` exports one decoded
resource for focused comparisons. Outputs must stay outside original media
and the user's playable disk.

## Semantic contracts and checks

The FAT/PF reader and PI decoder adapt TH04 `port/modern-64` revision `1ba7107`
(`port64/main.cpp` and `pi_image.*`, MIT). TH03's original CP932 8.3 archive
name and `YUMEZIKU` directory select its own resources. Source contracts are
`src/mainl/archive_io/pfint21.asm`, `src/shared/formats/pfopen.asm` and
`src/mainl/formats/pi_decode.asm`; the 32-byte directory entries, byte-wrapped
directory key, member XOR, equal-byte RLE and logical-length truncation agree
with TH04. PI retains its two history rows and high-nibble-first packed pixels.

`src/op/entry.cpp` and `src/op/menu/menu_state.inl` supply the menu semantics:
520 idle frames remain title; frame 521 requests attract. The title key cannot
also select Start until release. Menu Up and Down are separate ordered tests.
Option wraps rank/key bytes, toggles sound Off/FM, and returns with Option
selected. `src/op/libs/random.asm` supplies the explicit 32-bit LCG recurrence.

Menu rendering uses the original `MIKOFT.BFT` glyphs, `OPWIN.BFT` sprites and
`TL02.PI`. Each overlapping right-edge sprite first restores its full column
from the untouched background, as the original animation does. Simply drawing
overlapping transparent sprites leaves vertical stripes. Original gaiji
centering rounds to 8-pixel columns and uses the per-label shift values.

Observed on 2026-11-11:

- Linux title decoding matches all 128,000 packed pixel bytes produced by the
  original TH03 MAINL PI decoder instructions, with explicit file-I/O replies.
  The existing `DecoderProbe` ran the real decoder and native allocator; it
  did not substitute a host PI decoder.
- The complete initial 640x400 main menu is pixel-identical to the retained
  original DOSBox-X menu capture, including palette conversion and text.
- An SDL2 window on private Xvfb accepted menu navigation, Option rank change,
  return to main and quit. No user desktop input was sent.
- The MinGW Windows x64 executable ran headlessly on Windows and emitted the
  same complete menu PPM as Linux. The Win32 window backend is compiled;
  interactive Windows rendering/input remains to be exercised privately.
- Focused checks cover PF stored/RLE/XOR and malformed lengths, PI history/run
  bounds, menu release/wrap/input order, Option transitions, idle timing and
  the LCG carry/wrap vector. Linux and Windows use explicit fixed-width state.

Private evidence remains in the DOS worktree's `.analysis/work/`:
`port-pi-original.py`, `port-pi-original.log`, `TL02.original-packed`,
`th03-port64-menu.ppm`, `native-window-options.png`, `native-window-menu.png`
and `native-window.log`. The DOS comparison is
`.analysis/runtime/candidates/dos-replay-rebuilt/menu.png`.
These are focused runtime/port checks; canonical exact ledgers are unchanged.

Repeat the original decoder/frame comparison with the DOS checkout's Python:

```sh
PYTHONPATH=/path/to/dos/scripts /path/to/dos/.venv/bin/python port64/check_title.py \
  --native build/linux-x64/th03-port64 --dos-root /path/to/dos \
  --dos-frame /path/to/dos/.analysis/runtime/candidates/dos-replay-rebuilt/menu.png \
  --output /path/to/dos/.analysis/work/new-title-check
```

The check pins the original media and decoded MAINL against the DOS checkout's
existing target configuration. It supplies real PI file bytes to the original
instructions using the existing bounded native probe; no DOS emulator or new
full-game machine model is added.

## Next integration

Character selection now uses original CD2 portraits, BFNT names, gaiji cursors,
ability stars, spell cards and RGB palette. CDG drawing preserves bottom-up
planes, masked clear/OR, no-alpha overwrite and horizontal flip. Curve math
preserves byte-angle and signed-WORD multiplication wraps before division.
The selection locks/curve cycle survive cancellation within the OP process;
normal and alternate Shot/Bomb confirmations are independent ordered tests.

`check_selection.py` compares actual OP instructions against the native helper
for selection state/palette collisions, complete curve rasters and story
opponent generation. It verifies that OP's local LCG does not publish its last
draw into the resident counter used to seed MAIN. Run with the DOS Python:

```sh
/path/to/dos/.venv/bin/python port64/check_selection.py \
  --native-checks build/linux-x64/th03-port64-checks --dos-root /path/to/dos
```

The source is `src/op/menu/character_selection.inl` and the story/VS procedures
in `src/op/entry.cpp`. An SDL window entered story selection from Start,
selected Marisa and completed the handoff. A two-player headless route confirmed
Mima on both sides and resolved their palette collision. Linux and native Windows
selection PPMs agree. Windows state checks also pass. Evidence is in the DOS
worktree's `.analysis/work/port64-selection-*` files. Two-player controls follow
the DOS mappings: P1 uses T/F/H/B with Z/X; P2 uses keypad movement with Left/Right
for Shot/Bomb. Ordinary single-player menus/movement also accept arrows.

Next, join MAIN's resident/round setup
through explicit C++ state. Preserve 16-bit arithmetic, two-player ownership
and random draw order. Add a save directory separate from
both DOS media and the user's DOSBox package before implementing persistence.
Use the original DOS behavior as the comparison baseline, and clarify another
semantic owner when it blocks that integration.

MAINL introductions require `--font-bmp /path/to/FREECG98.BMP`, the external
2048x2048 monochrome Anex86-format PC-98 font also accepted by DOSBox-X. Font
rendering follows TH03's C++ `graph_putsa_fx`, including alternate JIS-row ANK
glyphs and WORD-truncated bold weight. TH04's ASM renderer is different.
`STNX0.PI`, the selected stage background, portraits and optional `ST.CD2`
stage number compose directly from original assets. Fade steps are six tone
units; input cannot dismiss the first 33 introduction VBlanks.

The full Marisa/Rikako Stage 1 frame agrees pixel-for-pixel with the retained
DOS frame, including text and palette. Repeat with:

```sh
python3 port64/check_intro.py --native build/linux-x64/th03-port64 --dos-root /path/to/dos
```

Use `--scene stage-intro --characters 5,13 --frames 20` with the HDI and font
for the same frame. The two IDs are paletted character IDs 1..18; `--stage`
accepts the original zero-based stage. No original disk or font is written.

MAIN round initialization now runs after the introduction, reading
`ENEDAT.DAT` from the second PF. The typed state includes original CPU safety,
rank/round difficulty, player positions/hearts/bombs, gauge state, character
speeds, CPU charge thresholds and formation rings. MAIN's process-local LCG is
seeded anew from the resident counter. The backward random-ring fill retains
its cursor; the WORD getter increments that cursor before reading, so index255
reads the wrapped cursor as its high byte. Stage setup assigns initial versus
gauge levels *after* round preparation; keeping the earlier rank increment
would change the first round.

`round.cpp` also contains ordinary player movement and shot-pair allocation/
update. They are not connected to a running battle yet. Next, implement the
original battle resources/rendering, formation/enemy VM and player state loop,
then the remaining attack families and result/MAINL routes. Audio, persistence
and campaign acceptance still remain.

Run the focused MAIN comparison with:

```sh
/path/to/dos/.venv/bin/python port64/check_round.py \
  --native build/linux-x64/th03-port64 \
  --native-checks build/linux-x64/th03-port64-checks --dos-root /path/to/dos
```

Six normal/versus/later-stage fixtures run the actual MAIN initializer, LCG,
ring fill and formation randomizer instructions. Scalar state, both players'
threshold arrays, the final seed and both complete formation rings agree.
Unrelated object-pool resetters are foreign services in this bounded check.
The first formation randomizer reads an uninitialized stack byte, attested as
`0x5e` from C0's saved InitStart. `Round::prepare` takes that context explicitly;
recover later-round stack context before connecting the round restart path.
The original instruction baseline comes from the pinned Japanese MAIN target,
not the user's no-hit executable.

`--main-assets --list` and `--main-assets --extract NAME --output FILE` inspect
the second PF in the original HDI. Both Linux and Windows x64 build; native
Windows headless state checks pass and its full introduction frame agrees with
Linux. The independent Windows DOSBox session remains untouched.

The enemy VM now runs original ENEDAT movement/spawn/wait/clip opcodes with
signed-WORD arithmetic, byte speed bands and the original independent duration
divisions. Six scripts agree with actual MAIN instructions for 1,237 ticks,
including the vector/movement callees. Run `port64/check_enemy.py` with the
same three arguments as `check_round.py`. The original data does not use its
broken loop instructions; custom loop scripts still need the DOS stack context.

`--scene battle-ready --characters 5,13` renders the initialized battlefield.
The atlas is assembled from MAINL's interlaced PI loads and MAIN's BF2 pose
copies. Drawing preserves SPRITE16's whole-column clipping and physical
200-line graphics; TRAM remains at 400 lines and uses fixed text colors.
The graphics score font comes from the maintained ReC98 score bitmap. Its
digit5 differs by one dot from `NUM8.BF2`, so the fonts are not interchangeable.
`check_battle_graphics.py --native build/linux-x64/th03-port64 --dos-root /path/to/dos`
compares the unchanged DOS borders, P1 gauge, score and TRAM glyph ink. The DOS
capture contains moving objects behind text and additional CPU gauge charge;
those pixels are not initial-state fixtures. This is a rendering checkpoint,
not a complete battle comparison. The running player/combat/intro/background
loop still needs joining before native playtesting.
