# TH03 MAIN after904 — entire Rikako major BOSS, verified native C++

The entire eight-function original `ba_rikak` Turbo C++ 4.02 physical
source was recompiled: BOSS template, signed-division orbit pattern,
entity burst, four-pellet RNG volley, alternating paired shots, full
update/hitbox controller and both multi-sprite renderers. Shared BOSS
state remains in its real external owner.

The four-pellet emitter now uses a natural C++ `while`, preserving four
independent RNG draws and the original mutable +8 bullet-speed step.
Three unsigned 16-bit spin clocks now use natural `if(!(frame %8))`,
and intro flicker uses its named period without changing code. Both
sprite-ring angles can be written naturally as
`angle = angle + RIKAKO_RENDER_*_ANGLE_STEP` with exact TC4 codegen.
Collision geometry (64×48 tile, 32-pixel radius) and all main, orbit
and intro sprite dimensions/offsets now have named compile-time values.

Original compiler trials, not assumed equivalence:

- `af904a`: original four-shot `for` -> `while` passed complete native
  TC4/normal MAIN TLINK twice.
- `af904b`: 3 spin clocks + flicker predicate became natural remainder
  truth tests; complete owner still exact.
- `af904c`: byte frame `boss_render_frame += signed_delta` changed
  original CODE when rewritten as explicit assignment: **1,679** vs
  **1,677** bytes, first difference CODE segment 4 offset 871. Reverted.
- `af904d`: named original hitbox, collision tile and sprite geometry,
  complete original physical owner exact twice.
- `af904e`: dropping the explicit unsigned conversion on signed sprite
  index `%4` produced **1,684** vs **1,677** CODE, first mismatch
  segment 4 offset 1263. The original cast remains.
- `af904f`: *both* byte sprite-angle compound `+=` updates accepted
  natural `angle = angle + named_step`, unlike signed spin-delta update.
- Final `af904g`: complete maintained current source passed two real
  original TC4 4.02 and full normal MAIN TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af904g --units ba_rikak
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af904g
```

Both rounds match **1,677 original CODE bytes, 215 literal ordered
native OMF FIXUPPs, eight PUBLIC offsets**, original source/segment/
16-bit ABI, full normal MAIN EXE and normalized MAP, all **124,642
Japanese loaded bytes and 1,553 ordered MZ relocations**. The reviewed
standard DOS MZ serializer reproduces all 130,882 original Japanese
MAIN.EXE bytes, not vendor header-generation identity. **98 other
project objects and original CRT reused**, no full cold replay,
patching, padding or artificial machine-code buffers.

Protected source-bound native report:
`.analysis/work/exatt-layout-af904g/report.json` SHA-256
`2c9056929d3e0f08aed51eaa1d6aaab9059740dc21f174dcdbcbe74737543cc3`.
Historically source-covered original CODE; no new distinct game CODE
coverage, raw vendor OMF identity or canonical Factory packed credit.
