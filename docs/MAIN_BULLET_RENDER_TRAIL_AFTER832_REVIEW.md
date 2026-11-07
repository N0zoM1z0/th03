# TH03 MAIN after832: complete Bullet engine, native C++ trail traversal

This change is in the **entire 1,080-line original physical Bullet source**,
not an isolated fake leaf. It includes the large `group_velocity_set()`,
`bullets_add()`, `bullets_update()`, and multi-pass `bullets_render()`
controllers, small Bullet lifecycle helpers, as well as the separate 386
GRCG pellet writer `grcg_pellet_put` under its authentic source segment,
original DATA/BSS and native OMF ownership.

## Exact maintained C++ recovery

The 16×16 full-color bullet renderer's **trail history traverser** now uses
a natural typed C++ `for` loop. It starts at the last history slot,
checks `trail_i > 0`, then updates *both* the signed trail index and the
VRAM sprite offset in the correct comma-expression evaluation order.
The original pointer relationship, `TRAIL_POINTS_PER_SPRITE` spacing,
history sprite render calls and later cloud/pellet passes remain unchanged.
The real original compiler independently confirms the `for` form emits
**all original instructions, offsets and OMF fixups** in the complete game.

## Original-native negative controls, not assumed equivalences

- `af832a`: changing the entire original trail `while` to the typed
  `for` with two ordered updates passed the original TC4/normal TLINK
  native comparator in both independent rounds.
- `af832b`: similarly changing the *different* 8×8 pellet `do/while`
  traversal to a `for` changed original CODE (**2,687** initialized CODE
  bytes vs **2,685** target). The code's original bottom test and
  register/pointer update arrangement are preserved, not simplified.
- `af832c`: replacing the hardware `_SI &= ((PRESHIFT * 2) - 1)` with
  natural `_SI %= (PRESHIFT * 2)` changed register/compiler codegen in
  the original 386 GRCG pellet writer (**2,704** initialized CODE bytes).
  The original `SI` mask remains for exact native instruction identity;
  this was a genuine compiled negative control, not a hypothetical test.

The current final `af832d` source adds comments documenting why the two
legitimate physical loops need different forms and recompiles the exact
maintained file from its own freshly rooted, compiler-bound source snapshot.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af832d --units bullet
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af832d
```

Both independent original TC4 4.02 and complete normal MAIN TLINK rounds
reproduce **all 2,685 original CODE bytes** (including both CODE segments),
**196 literal ordered OMF FIXUPP fields, 20 PUBLIC offsets**, source/data/
BSS and segment ABI, the complete normal original MAIN EXE/MAP,
**124,642 Japanese loaded bytes, all 1,553 original MZ relocation words**
and all 130,882 Japanese MAIN.EXE bytes via the independently checked
standard DOS MZ serializer. The **98 other original project objects and
CRT were reused**; this did **not** run a whole cold replay or patch an OBJ.

Protected source-bound native report:
`.analysis/work/exatt-layout-af832d/report.json` SHA-256
`50422145d8d23fa201bfb47d7c4e7815a0caf38a4fcb386cfbd792c14e6134cf`.
The actual two original compiler/TLINK rounds, private writer logs, source
snapshots, objects, complete EXE/MAP and MZ proof are retained unchanged.
This source was historically native-covered already, so these are **not
newly distinct original CODE bytes or canonical Factory packed-file
acceptance**. Raw original vendor OMF metadata and full game ownership
remain separate open questions.
