# TH03 semantic and 64-bit port

`port/modern-64` contains the first native C++17 slice: read-only HDI/PF assets,
PI decoding, title/menu rendering, input release gates and Option state. Linux
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
yet. Start, VS, Music Room, HiScore and idle attract return their named request
at the original handoff boundary; the corresponding scenes are not implemented.
This is a title/menu milestone, not a playable game preview.

Headless examples:

```sh
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --scene menu --screenshot menu.ppm
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --headless \
  --scene options --inputs 8,0,4096 --screenshot options-return.ppm
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --list
build/linux-x64/th03-port64 --hdi /path/to/zun.hdi --pi TL02.PI --packed title.pixels
```

`--inputs` supplies original hexadecimal or decimal WORD input masks, one per
tick; use zero between separate presses. `--archive` can replace `--hdi` for
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

Port the character-selection CD2 images and selection state, then join the
MAIN resident/round setup through explicit C++ state. Preserve 16-bit arithmetic,
two-player ownership and random draw order. Add a save directory separate from
both DOS media and the user's DOSBox package before implementing persistence.
Use the original DOS behavior as the comparison baseline, and clarify another
semantic owner when it blocks that integration.
