# TH03 MAIN after831 — complete Ellen BOSS radial and nine-entry sprite cycle

This reconstructs the **entire nine-function physical `ba_ellen` Turbo C++
4.02 source**: BOSS template, multi-branch spread controller, both timed
Extra Attack 2D radial bursts, repeated pellet wave, full BOSS update/
collision, each nine-entry strip renderer, four-phase/radial introduction
and render dispatcher. No auxiliary code/TU was substituted for the original.

## Source recovery

- The two true Extra Attack burst loops now express the **256-angle-unit
  full rotation** and **opposite `+2` / `-2` mode arguments** as meaningful
  C++ enumerators. Their byte-valued `angle` is advanced **after** each
  original far call, preserving the signed 16-bit division by the actual
  level-derived count, RNG consumption and original BYTE Pascal argument.
- The main and intro sprite renderers now share named **nine-entry strip
  cycle** and original **four-frame** animation period. The three independent
  physical strip drawing calls, signed `--i` then comparison/8-index wrap,
  separate width/height lookup table reads, and main/intro speaker timing
  are kept exactly as compiled, not merged into a new loop. The intro
  explicitly names its four radial families and eight sprites per family,
  original flicker and finishing boundaries and 200-pixel starting radius.

## Fresh real native counterexamples (not accepted)

The compiler results were challenged instead of trusting historical notes:

- `af831a` combined each pair of signed decrement and comparison into the
  superficially natural `if (--i < 0)`. Four such replacements produce
  **1,667 CODE bytes**, not the original **1,675**; this independently
  reproduces the older compiler-codegen concern, so all four are restored.
- `af831b` changed `ellen_render_heights[i] / 2` into `>> 1` on a **signed
  16-bit table element**. That version generated **1,672 CODE bytes**,
  and it is not in general equivalent for negative values. The division
  remains exact to the original, not silently replaced by arithmetic shift.
- `af831c` used a named `0x20` enumerator in the intro's mutable byte
  `angle += 0x20`. The genuine compiler emitted a different AL/byte
  update, with **1,671** initialized CODE bytes; the literal is restored.

Final stage **`af831d`** keeps all proved natural C++ improvement but
rejects these unequal variants. It independently compiled the complete
current source twice through the original original-TC4 4.02 and full normal
MAIN TLINK response:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af831d --units ba_ellen
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af831d
```

Both rounds match all **1,675 original CODE bytes, 213 literal ordered
OMF FIXUPP fields, nine PUBLIC offsets**, source and storage ownership,
the complete normal MAIN EXE/MAP, the entire **124,642-byte Japanese
loaded program** and **all 1,553 ordered original MZ relocations**.
The independent standard DOS MZ serializer reproduces all **130,882 bytes
of the original Japanese MAIN.EXE**. The 98 unchanged project objects and
Borland CRT were reused, **no all-object cold replay** or target-byte
patching. The complete protected real compiler/linker receipt DAG is
`.analysis/work/exatt-layout-af831d/report.json` (SHA-256
`5181f21fb15d02d3d34fc84d23a2681dbcb798fca8ffae2904958815c169c35c`).

This is fresh native source-bound proof for an **already historically
source-owned original physical TU**. Do not add its bytes again to unique
coverage or claim exact vendor raw OMF packets, canonical packed-game
Factory credit or complete original-project source identity.
