# TH03 DOS position independence

TH03 has a separate PI build for `OP.EXE`, `MAIN.EXE`, and `MAINL.EXE`. The
default Japanese build uses the original collision routine. Fresh TC4 rounds
at `af1413e` reproduce its complete player-core CODE, ordered OMF fields,
PUBLICs, segment layout and linked MAIN with the original MZ relocations.
The [four-file packing proof](CURRENT_LINKED_BUILD_REVIEW.md) remains the
default build record. PI covers the three game EXEs and keeps the original
ZUN launcher and game data.

## Why this build differs

Demo 1 diverged in the original-collision relinks at gameplay row 1,177.
The 2P horizontal position was 416 subpixels in the original layout and 544
in the 32/16/64 layout. Input, score and the RNG trace still matched there.
The previous 2P position was (480, 3936) subpixels. At the left boundary
`player_hittest(32)` computes a negative starting byte column. An unsigned
byte multiply forms the wrong 16-bit offset, and the branch that skips a
negative column uses the mask shift count for its first column advance.

The linked routine reproduced the failure in a CPU fixture with an empty
collision map. In the original layout it started reading at `DS:104A`
inside `xxv`. The 32/16/64 layout started at `DS:109A` inside `signal`.
Both reported a false collision at different positions. The separate PI
[source fragment](../src/main/player/hittest_columns_pi.inl) sign-extends the
column before multiplying and advances a full column on the skip path.
The original source stays in [stuff.inl](../src/main/player/stuff.inl).
The PI builder stages the fragment only inside its isolated player-core TU.
Both TC4 rounds emit the same complete PI core payload, literal ordered OMF
fields, PUBLICs and segments. They link identical full MAIN images with the
same original relocation count. In every PI layout the CPU fixture reads the
same offsets in the 2P bitmap, misses the empty case and hits the inserted
contact at the same coordinates.

## Linked address checks

Stage `af1416p` uses a complete unchanged-input control relink and the three
TH04 test layouts. The inserted CODE/DATA/BSS contributions are 16/32/48,
32/16/64 and 3/7/11 bytes per eligible segment. The original object order and
hashes are preserved across the control and the three relinks. The table
lists the minimum number of contributions whose offsets changed within
their frames, with the number of relocations and matching far transfers per
layout. An independent rebuild at `af1417p` reproduced all 12 EXE files
byte for byte. The 12 complete MAP files matched after normalizing the
stage path in module names.

| Program | CODE / DATA / BSS moved | Ordered MZ relocations | Far CALL/JMP targets |
| --- | ---: | ---: | ---: |
| MAIN | 164 / 26 / 10 | 1,553 | 1,132 |
| OP | 96 / 30 / 10 | 607 | 402 |
| MAINL | 100 / 30 / 7 | 677 | 464 |

The linked checks also cover 135 far pointers in initialized data, 156
CS-relative writes, the VSYNC, CRT BIOS and archive interrupt installations,
and both MAIN bullet jump tables. OP's `start_demo()` follows the
`_resident` pointer from `0D7F:2464` to `0D8F:24B4`. MAINL follows
the ending template from `0E3F:0B3E` to `0E4D:0B4E`. MAIN moves the
random ring and cursor together and uses both new offsets. The linker test
rejects an unchanged layout, a missing relocation and a stale far target.

The displacement screen flags inline switch data and the PI decoder's
private buffer fields. Its DS is set to the allocated buffer, so fields
such as `bit_buf` at `4112h` do not use DGROUP. The register screen
follows constant MOV/PUSH and arithmetic origins through direct branches.
Reviewed cases include VRAM offsets, the collision-map size added before
its symbolic base, and `1234h` placeholders overwritten by CDG and
collision-map writers. Both MAINL CDG blitters returned through the native
far frame at loads `2000h` and `6000h` in all four layouts. Their
self-modifying word writes stayed at the same instruction fields and the
two-row fixture produced the expected bytes on all four planes.

## DOS replay

The corrected PI control and 32/16/64 layout each completed all four
attract demos. All 28,068 gameplay records and the RNG hook sequence match
byte for byte, including player state, scores, input and relevant resident
fields. The observer verified each complete relocated MAIN image on entry
and observed the fifth launch return to the first pairing. Both runs used
the same DOSBox-X normal core, fixed guest cycle configuration and host
fast-forward setting on private copies of the original HDI. The odd layout
also booted through the public DOS runner and entered attract combat.

The retained raw traces also passed on the byte-identical `af1417p`
executables after tightening the parser's launch order, frame continuity,
field widths and RNG hook checks. Deliberately changing a frame, DGROUP,
RNG hook address, initialized far pointer or CS-relative store target
now fails the corresponding check.

A separate CPU probe compared both players' horizontal scan addresses and
masks with the clipped bitmap geometry at the six gameplay hitbox sizes.
All 384 cases matched across the four layouts. The 42 cases with a
nonnegative starting column also matched the default routine.

The original-collision control and 32/16/64 diagnostic completed the same
four demos with differing gameplay records. Their traces reproduce the
position dependence removed in the separate PI build.

The original and odd MAINL layouts displayed identical ending dialogue at
two stable checkpoints. Both also reached the staff roll with animated
snow. Screenshots taken during animation correspond to different frames.
The seeded score-only visit registered Reimu on Easy at Stage 2 as
`ABBBBBBB`, with displayed score 123,456,783. Both disks produced the
same 824-byte `YUME.NEM`. The four sections pass their checksums and the
other three difficulty sections retain their bytes. These MAINL and OP
executables are byte-identical to the corresponding PI-stage inputs.

## Reproduce

Use an unused DOS-safe stage name. The observer is the pinned read-only
DOSBox-X binary from the local TH04 demo-observer build. It reads TH03's
addresses from each layout's own MAP and checks the complete relocated
MAIN image on every launch.

```sh
DISPLAY= WAYLAND_DISPLAY= .venv/bin/python scripts/audit_th03_dos_pi.py --stage afNNNNp
DISPLAY= WAYLAND_DISPLAY= .venv/bin/python scripts/review_th03_pi_addresses.py \
  --stage afNNNNp --output .analysis/work/th03-pi-addresses.json
DISPLAY= WAYLAND_DISPLAY= .venv/bin/python scripts/capture_th03_pi_demos.py \
  --stage afNNNNp --emulator "$PI_OBSERVER" --unthrottled \
  --output .analysis/runtime/candidates/th03-pi-demos
```

Pass `--original-collision` to the link and address commands to reproduce
the old address dependency with the exact collision routine. Use
[`play_th03_dos.py`](../scripts/play_th03_dos.py) with `--pi-stage afNNNNp`
and optional `--pi-layout odd` to boot a fresh private play disk. The
[MAINL fixture](../scripts/play_th03_pi_mainl.py) uses the same layout
inputs and seeds the installed DOS resident before launching the ending or
score menu. See the [DOS runner](RUNTIME.md) for the private Xvfb command.

The current private evidence is under `TH03PI/af1416p/` in the TH03 Wine
drive, `.analysis/work/th03-pi-addresses-af1416p.json`, and
`.analysis/runtime/candidates/pi-fixed-demos/`. The latter contains the
paired `rows.txt` and `comparison.json` files. The original-collision
negative control is `af1412p`.
