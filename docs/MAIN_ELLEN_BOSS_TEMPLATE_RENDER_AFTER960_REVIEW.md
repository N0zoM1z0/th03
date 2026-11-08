# TH03 MAIN Ellen BOSS: template, state transitions and sprite-strip semantics

The complete original nine-function `ba_ellen` physical BOSS remains one
maintained natural C++ source. This source-current pass extends the existing
spread/radial-Extra/pellet/raster reconstruction through its template,
attack transitions and strip render leaves:

- `boss_ellen_template_init()` names the original center, velocity, HP,
  sprite offset and player-two sprite adjustment.
- The four original attack/intro completion paths use the existing named
  `ELLEN_MODE_SELECT` state. The normal render-mode reset has its own
  explicit name.
- Spread and pellet sound-effect IDs and the opposite pellet half-turn
  are named independently.
- `ellen_render_strip()` names the original Y-offset scale, base sprite
  bank, left/top placement. `ellen_render_main()` names the hit-sprite
  delta. `ellen_render_intro()` names the radial sprite bank and half-tile
  placement.

The complete BOSS still contains its eight-shot spread loop, two independent
RNG radial Extra Attack loops, four-by-eight intro sprite loop, three-strip
renderer, update/hitbox controller and the original anonymous renderer-table
references. Signed index wraparound, byte-angle truncation, RNG/far-call
order, integer division, original render table stride and the post-call
sprite/angle updates are unchanged.

## Current-source native verification

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_main_exatt_layout.py --stage af960a --units ba_ellen
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af960a
```

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
**entire 1,675-byte original Ellen BOSS** and linked each object through the
complete normal MAIN response. Both reproduce all **213 literal ordered OMF
FIXUPP fields and nine PUBLIC offsets**, the full original Japanese MAIN
loaded image (**124,642 bytes**) and all **1,553 ordered MZ relocations**.
The other **98 original game objects and original Borland CRT** were reused;
no full cold replay, target patch, original OBJ patch, synthetic byte buffer
or NOP padding.

Protected source-current report:
`.analysis/work/exatt-layout-af960a/report.json`, SHA-256
`448760cfd873930a2e15b3b61fa692fbf5145c9dbca62f20a4d862950f7abc5c`.
The complete BOSS was historically source-covered; this pass improves
current natural C++ semantics and provenance, not distinct original CODE
ownership, vendor raw OMF packet identity or canonical Factory acceptance.
