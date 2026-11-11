# Playing the rebuilt DOS game

The actual four packed outputs from `TH03PKG/af1410p/r1/packed/` have been
installed and played in a disposable copy of the pinned Japanese HDI.
Each file is read back and checked against its actual packing output and
the complete Japanese target. See the [build review](CURRENT_LINKED_BUILD_REVIEW.md).

The method follows TH04's `docs/DOS_BUILD.md` and HDI preparation/runtime
probes: boot the original DOS disk, replace the built programs, launch
`GAME.BAT`, send real keyboard input, capture the emulator window and inspect
saved files. `GAME.BAT` installs the ZUN residents and PMD86 driver and removes
them when OP exits. Launching an executable directly skips that setup.

## Reproduce a run

Use the existing local DOSBox-X, Xvfb, xdotool, ImageMagick `import` and mtools.
The runner uses Python 3.11's standard library. The pinned font is
`.analysis/runtime/fonts/FREECG98.BMP`, copied from the existing TH04
DOSBox-X source's `contrib/fonts` directory. Its SHA-256 is
`91d75314ac4f940ab13b3c33fb260ef1713865d025a94f09f6814a72e47dfa87`.
No tool installation or TH04 mutable state is copied.

Run preflight when changing the target or emulator. Choose a new private
output directory:

```sh
DISPLAY= WAYLAND_DISPLAY= nice -n 10 xvfb-run -a \
  -s '-screen 0 1024x768x24 -nolisten tcp' \
  .venv/bin/python -B scripts/play_th03_dos.py \
  --output .analysis/runtime/candidates/my-dos-play --seconds 80 \
  --event down:Left@4 --event up:Left@25 --frame menu@26 \
  --event Down@27 --event Down@28 --event Down@29 --event z@30 \
  --frame high-scores@35 \
  --event down:Left@36 --event up:Left@40 --frame menu-return@42 \
  --event z@44 --frame story-select@46 \
  --event Down@47 --event Down@48 --frame marisa@49 \
  --event z@50 --frame stage-intro@54 \
  --event down:z@55 --event down:Right@56 --event up:Right@57 \
  --event up:z@58 --event Escape@60 \
  --frame pause-a@61 --frame pause-b@63 \
  --event Escape@64 --frame resumed@65 \
  --event Escape@66 --event q@67 \
  --event down:Left@68 --event up:Left@72 --frame returned@74 \
  --event Escape@76 --frame dos-exit@79
```

The runner limits itself and DOSBox-X to one allowed CPU at nice10. Use a
quiet CPU for the outer Xvfb as well if host contention affects input timing.
The profile uses PC-98, normal Pentium core, fixed 24,000 cycles, 16 MiB,
2.5 MHz GDC and the 86c sound board. SDL host audio is dummy; emulated sound
remains enabled. The default executable is `/usr/bin/dosbox-x`, SHA-256
`30a5fdf8fa95abaf7bae1a9e624ccfc9e26e5357a19cc567bf3a2ac659699258`.
The manual session also used TH04's existing observer build read-only, with
TH04 observer variables disabled. Both binary identities are explicitly
allowed and recorded by the runner.

The title initially has no menu labels. Hold Left to reveal them without
selecting Start. Roughly 520 idle frames start an attract demonstration;
distinguish that from manually selected gameplay. Z/Return confirms, arrows
move/select, Escape pauses combat, and Q from pause returns to OP.
Events are timed from emulator launch. Inspect screenshots before interpreting
a run; reaching a capture time does not establish a gameplay result.

`run.json` records actual products, emulator/profile/font, input times,
screenshot hashes and the DOS return marker. The output also retains isolated
before/after CFG and NEM saves. `START` followed by `EXIT` means `GAME.BAT`
returned normally. Ctrl-F9 merely closes the emulator at the time limit.
The original HDI is checked unchanged. `--original` uses the pinned Japanese
files for a baseline run with the same setup and original save data.

## Observed on 2026-11-11

- Fresh original and rebuilt runs displayed identical complete menu pixels and
  returned normally to DOS, using the same emulator/font and initial CFG/NEM
  data. Disk copies differ in FAT write timestamps; frame timing is not
  asserted deterministic.
- The maintained 80-second rebuilt replay opened HiScore through MAINL,
  returned to OP, selected Marisa, displayed the Stage 1 opponent and entered
  combat. Paused frames two seconds apart were pixel-identical; the resumed
  frame changed. Pause/Q returned to OP and Quit unloaded the music driver
  and residents before returning to DOS.
- Ordinary movement and firing in the longer manual session led to a natural
  defeat, MAINL name registration and Continue. Marisa's Stage 1 score of
  18,300 was saved. Choosing No returned to OP; reopening HiScore displayed
  the saved entry, and Start reopened character selection. The original Easy
  setting and unmodified damage were used.
- Music Room displayed Japanese comments and switched tracks 1 and 2.
  A WAV capture contained 21.859 seconds of non-silent stereo 48 kHz PCM.
  This checks sound generation, not listening quality or audio accuracy.
- VS Start's 1P vs 2P mode selected Marisa and Mima independently. P1's
  H/Z/X and P2's keypad 4/Left/Right moved, fired and bombed on their respective
  sides. Both sprites moved to opposite edges, both scores increased, and
  both bomb effects appeared. See `vs-selected.png`, `vs-battle.png`,
  `vs-after-input.png` and `vs-bombs.png` in the manual session directory.

Private evidence is under `.analysis/runtime/candidates/`:
`dos-replay-original/`, `dos-replay-rebuilt/`, `dos-play-replay/` and
`dos-play-20261111/`. The last holds `persisted-score.png`,
`registration-saved.png`, music captures and the manual input log. The first
two execution disks are regenerable; their run records and screenshots
retain the menu comparison.

No game-source change was needed. Full campaign completion, the ending,
Extra and listening-based sound comparison remain to be
played before a semantic or 64-bit port. Runtime play adds no source ownership
credit.
