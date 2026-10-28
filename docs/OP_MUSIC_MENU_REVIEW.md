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

The current OP publication now accepts all three literal source includes:
state/tracks216, copy30 and animation/menu1998. The newly accepted two extents
add10 complete procedures/2028 CODE; OP totals are36 extents/46 procedures/
6127 CODE+487 initialized DATA at that CODE checkpoint. The subsequent storage
review adds the complete1008 initialized DATA bytes; OP now has37 extents/
46 procedures/6127 CODE+1495 initialized DATA. BSS1060 has separately reviewed
layout and zero file-backed byte credit.
The supporting native receipt itself does not publish ownership; acceptance is
recorded in `config/op_work/scoped_acceptance.json`. Whole-game exactness remains
open.

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

## Complete CODE ownership

`scripts/lib/op_music_ownership.py` checks the ten remaining native public
boundaries and both MAP tables. Each complete procedure decodes through its
actual return: `polygon_build` is near Pascal pop12; `cmt_load` and the combined
comment helper pop2; the menu is far with no argument cleanup. Other functions
return near without callee argument cleanup. The copy and tail extents meet
exactly at native offset246, after the already accepted216-byte prefix.

The generic producer inventory retains its original two-source label. The
actual compiler dependency records and literal three-include wrapper establish
the maintained30-byte copy source independently; the frozen native recipe is
unchanged. No padding, object patch or product-byte substitution is involved.

The acceptance adapter revalidates the unchanged two-round native graph and
all prior owner bytes/ordered relocations. It pins the complete prior scope at
`6cfa85f`, checks every other prior verifier input, and retains its original
runtime observations without extending or rerunning their models. The two
adapted files are the acceptance adapter and progress consumer. Any changed
source graph or native output fails that reuse guard. The current publication
records this distinction explicitly in `prior_acceptance`.

## Initialized DATA and BSS

`scripts/lib/op_music_storage.py` checks the complete1008-byte contribution at
DGROUP05F2. It evaluates the actual staged CP932 title/filename declarations
through their explicit compatibility headers. The natural initializer contains:

| Object | Relative offset | Bytes |
| --- | --- | --- |
| 21 title far pointers | 0 | 84 |
| 19 file far pointers | 84 | 76 |
| Initialization flag / playing BYTE | 160 / 161 | 1 / 1 |
| 21 display strings, each32 CP932 bytes plus NUL | 162 | 693 |
| 19 filenames plus NULs | 855 | 136 |
| `MUSIC.TXT` / `op3.pi` plus NULs | 991 / 1001 | 10 / 7 |

All40 native far fields reference local SEGDEF2 under DGROUP. Their literal
emitted order is reverse pointer order and matches the complete ordered MZ
vector. Segment fields are also checked at load segments1000 and3000. All1008
semantic/native/target/candidate bytes match, including spaces and terminators;
there are no unnamed initializer holes. No source, native recipe or cold output
changed.

BSS starts at DGROUP1F70. Native SEGDEF/MAP, five public symbols and all CODE BSS
addends agree with the source layout: points40, center64, velocity64, angle16,
angle-speed16, selection1, page1, segment-only pointer2, four far pointers16 and
20 comment records840, total1060. `points[10]` reserves40 bytes even when normal
rendering uses fewer entries. There is no BSS initializer record. This establishes
layout without claiming raw file bytes or an initial memory value.

The DATA owner adds zero procedures and no CODE. Three small regressions check
the complete result, identical corrupted DATA images and relocation order with
unchanged membership. The ordinary OP publisher verifies this scope; a direct
native review is available as:

```sh
PYTHONPATH=scripts .venv/bin/python -m lib.op_music_storage
```

The earlier CODE-only and historical runtime receipts keep their original scope
flags. This initialized DATA proof supersedes their storage exclusions only in
the current source publication. BSS still contributes no file-backed bytes.
