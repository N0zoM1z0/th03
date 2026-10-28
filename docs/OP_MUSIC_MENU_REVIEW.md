# OP Music Room native comparison

2026-10-28: the complete maintained far menu at `0990:1306` matches the pinned
Japanese target: 476 CODE bytes, 160 instructions, 57 OMF fields and 18 literal
ordered MZ relocations. The natural TC4 producer, both MAP publics and complete
far procedure are checked. No product source, native recipe or target changed.

The focused check also covers the entire Music Room carrier: 14 procedures,
2,244 CODE bytes and 50 literal ordered relocations. State/tracks216, copy30,
polygon645, comment/flip877 and menu476 form a complete partition. The complete
current source/tool/SDK/output/packing graph is validated without rebuilding
unchanged native inputs. The native receipt is
`config/op_music_menu_work/observation.json`.

Initialized DATA1008/BSS1060 and source-ownership publication remain separate.
Accepted OP totals are unchanged; this check does not claim whole-game exactness.

## Preserved source details

- The menu frees all 32 CDG slots and loads `op3.pi` before the track list and
  comment backgrounds. Far return and Pascal/cdecl cleanup stay native.
- Selection19 is blank and20 is Quit. Up and Down are independent sequential
  tests; unsigned BYTE wrap and unchecked table access remain unchanged.
- Shot is low-BYTE bit20, OK high-BYTE bit20, Cancel high-BYTE bit10. Release
  loops compare the full input WORD; no input normalization is added.
- Selection stops the old song, loads, plays, updates the playing BYTE, draws
  comments, flips, then draws the second page. The input and sound wrappers
  retain their original calls and ABI.
- Exit frees snapshots/backgrounds and clears the selected pages without
  adding song-stop or reload calls.

## TH04 reference comparison

The authorized local TH04 `src/op/music/room_menu.cpp` and
`musicroom_menu.inl` explain the shared structure. Its GAME4 branch differs:

| Behavior | TH03 target/current source | TH04 reference GAME4 source |
| --- | --- | --- |
| Menu ABI | Far | Near |
| Tracks / blank / Quit | 19 / 19 / 20 | 22 / 22 / 23 |
| Normal / selected text color | 3 / 15 | 5 / 3 |
| Input | Mode-interface wrapper | Reset/sense wrapper |
| Song selection calls | Stop, load, play, update playing, comments | Fade, update playing, comments, load, play |
| Exit song calls | No stop/reload | Fade, load `op`, play |

These are reference-source observations, not additional TH03 target evidence.
TH04 was left unchanged.

## Verification scope

```sh
.venv/bin/python scripts/review_th03_op_music_menu_work.py
.venv/bin/python scripts/review_th03_op_music_menu_work.py --check
```

Use the workflow's one-CPU/nice10/empty-display environment. The two small
`test_op_music_native.py` regressions cover the saved native result and rejection
of identical corrupted linked images against the independently resolved object.

At the user's direction, the large menu runtime matrix was terminated (exit143)
and produced no completed runtime receipt. Its uncommitted emulator model,
held-loop proofs, artificial filename-boundary cases and 55 mutation controls
were removed. Earlier polygon/comment runtime receipts remain historical
observations; their matrices and tests are no longer routine requirements.
