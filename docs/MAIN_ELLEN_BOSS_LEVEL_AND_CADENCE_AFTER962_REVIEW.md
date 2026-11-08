# TH03 MAIN Ellen BOSS: natural level scaling and byte render cadence

The complete original nine-function `ba_ellen` BOSS remains a single
maintained natural C++ physical source. This follow-up extends the previous
template/render pass into the level-parameter setup and two pattern leaves:

- The four level-derived bullet-speed, Extra count, pellet-speed and
  pellet-interval formulas now name their individual divisors and base
  values. The signedness, integer-division order and byte destinations are
  unchanged.
- The spread attack's even-frame cadence and eight-shot volley use named
  values; its `if(!frame%2)` and `if(frame%2)` branches remain distinct.
- The Extra Attack's three-frame render-state advance is now ordinary
  `boss_render_frame = boss_render_frame + ELLEN_EXTRA_RENDER_STEP`, rather
  than the original compound-assignment spelling. A fresh TC4 experiment
  proves this natural assignment reproduces the original byte CODE.
- The sprite-strip height's original integer divisor is named at the leaf.

This is the complete original BOSS, not a helper-only build. Its spread,
two independently randomized radial Extra Attack bursts, pellet pattern,
full update/hitbox controller, strip/main renderer and four-by-eight intro
renderer all compile together. The independent RNG calls, loop ordering,
byte arithmetic, signed renderer-table index and far callback ABI remain
unchanged.

## Original compiler evidence

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_main_exatt_layout.py --stage af962a --units ba_ellen
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af962a
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
`.analysis/work/exatt-layout-af962a/report.json`, SHA-256
`0d4c188c64c0a551c2fa4c43cadf65f2ddfc7f2ae5bda69d6ad0a5cfaa5d7b71`.
The prior `af960a` report is now a historical source snapshot because this
follow-up changes the same maintained `ba_ellen` translation unit. The
BOSS's CODE was already historically source-covered; this advances current
natural C++ semantics and provenance, not distinct original CODE ownership,
vendor raw OMF packet identity or canonical Factory acceptance.
