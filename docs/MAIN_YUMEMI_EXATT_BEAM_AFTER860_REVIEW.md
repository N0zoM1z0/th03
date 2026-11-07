# TH03 MAIN after860: full Yumemi Extra Attack beam renderer and collision

The *entire* original five-function `ex_yume` physical Turbo C++ 4.02
owner is compiled here, including both entity spawn functions, the
large GRCG warning/active-beam renderer, full 16-slot update and render
traversal. Its 8 ordinary and 8 specially spawned 32-byte entity slots
remain allocated in the unchanged original carrier; no new DATA or BSS
ownership is claimed.

## Current natural C++ recovery

The active beam's **four separate vertical/horizontal sprite-edge
traversals** now use natural `while` loops, rather than moving bytecode
or shortening the four original render paths. Both increasing and
decreasing loops retain **signed 16-pixel strides**, exact clip bounds,
per-edge sprite offsets and the original sprite call order. Actual original
TC4 4.02 compiled all four loops byte-identically to the original code.
The beam's 6-unit radius growth/decay, 4-pixel collision cross-section,
8-frame warning/grow behavior, original 0x1200/0x1000 random target
ranges, 0x600 target offset and 0x46 launch speed now use named C++
constants. The radius-to-subpixel shift, active-beam initial radius and
two original player-specific 16-bit GRCG clip rectangles are likewise
explicit. No original 16-bit rounding, integer promotion, RNG ordering,
entity dispatch, hardware calls or memory layout was changed.

## Original-compiler negative controls, not assumed equivalences

- `af860a`: four beam-perimeter `for` loops changed to `while`, complete
  physical object exact in two original compiler/TLINK rounds.
- `af860b`: added named 16-pixel edge step, radius changes and narrow
  hitbox bounds; again exact.
- `af860c`: replacing **two signed-char `extent / 2`** expressions with
  `extent >> 1` generated **1,690** initialized CODE bytes vs the
  original **1,696**; negative odd values also round differently.
- `af860d`: replacing signed `mid_y = top / 2` by arithmetic `>> 1`
  independently failed exact native CODE (also 1,690 bytes).
- `af860e`: changing postincrement `p->frame++` to `++p->frame` in the
  active entity loop emitted **1,701** original-code-byte candidates,
  not the target 1,696; postfix remains.
- `af860f/g`: restored signed division and byte postfix, added the real
  named RNG/geometry and source comments; full maintained source
  compiled exactly, *twice* with genuine original TC4 and normal TLINK.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af860g --units ex_yume
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af860g
```

Both independent real original TC4 4.02 and full normal MAIN TLINK rounds
matched **all 1,696 original CODE bytes, 87 literal ordered native OMF
FIXUPP fields, five PUBLIC offsets**, original source/segment ABI,
complete original normal MAIN EXE/MAP, **all 124,642 Japanese loaded
program bytes and 1,553 ordered original MZ relocations**. Independently
checked standard DOS MZ serialization reproduces all **130,882 bytes**
of the pinned Japanese MAIN.EXE. The **98 unchanged original project
objects and CRT** were reused; no full cold replay, NOP padding, target
byte-array substitution or object patching.

Protected actual original-source-bound report, compiler/writer logs,
OBJ/EXE/MAP and two complete native rounds:
`.analysis/work/exatt-layout-af860g/report.json` SHA-256
`7dfa8037d01d7988d613f539a868c940a25276b7607aae86d3d769e43b75c3fd`.
These original CODE bytes already had historical source coverage:
current C++/native fidelity is improved, but no new distinct CODE credit,
historical raw vendor OMF packet identity, canonical packed-file Factory
acceptance or complete original source text identity is claimed.
