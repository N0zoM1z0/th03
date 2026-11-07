# TH03 MAIN after866: Kotohime complete BOSS natural C++ ring and radial control

The **entire eleven-function original physical `ba_koto`** owns Kotohime's
BOSS template, RNG-dependent ring emitter, random/aimed/pellet/radial
attack families, full update and hitbox controller, sprite-ring and intro
renderers. These changes compile that complete original object, not just
isolated per-function stubs.

The ring emitter, both nested radial-barrage loops, and sprite-ring
renderer now use ordinary typed C++ `while` loops with original **signed
16-bit index/polar division**, post-call mutations and byte-angle
truncation. The actual original RNG draws remain conditional and ordered.
The two nested radial divisions (256-step center and 128-step local
spread) are deliberately kept **inside** the same center/projectile
loops. The three ring-effect growth assignments and the five specific
pellet-arc projectile X/Y positions now have meaningful named source
constants instead of unexplained numbers; the separate five `bullets_add`
calls and physical timing still match their original order.

## Genuine original compiler trials

- `af866a`: changed the complete random/aimed ring emitter to `while`;
  original TC4 4.02 and full normal MAIN TLINK were exact in both rounds.
- `af866b`: also changed **both nested center/projectile radial-burst
  loops** to natural `while`, preserving exact 16-bit division and
  byte-angle update; complete original CODE/fixups remained exact.
- `af866c`: also changed the sprite-ring rendering loop to `while`,
  retaining original signed polar and graphics calls. Whole original
  CODE matched exactly in both compiler/linker rounds.
- `af866d`: independently re-tried `boss_move_phase += 2` instead of
  both original AL-mediated phase updates. The real compiler emitted
  **1,834** CODE bytes vs the original **1,840**; restored original
  `_AL` memory load/AL update/store operations, not binary padding.
- `af866e`: independently replaced the radial pattern's original
  byte `_AL += 0xFC` with `boss_move_phase -= 4`. The genuine compiler
  emitted **1,838** CODE bytes, not 1,840; original AL path restored.
- `af866f`: named ring expansion and the five specific pellet origin
  offsets, passing both original compiler/whole-link rounds exactly.
- Final `af866g`: reindented the actual nested radial loop, documented
  original compiler-specific byte carriers and recompiled the complete
  *current maintained source* twice with original TC4/normal MAIN TLINK.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af866g --units ba_koto
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af866g
```

Both independent genuine original TC4 and normal MAIN TLINK rounds match
**all 1,840 original CODE bytes, 262 literal ordered native OMF FIXUPP
fields and 11 PUBLIC offsets**, source/segment/16-bit ABI, complete
normal MAIN EXE/MAP, the entire **124,642-byte original Japanese loaded
program and 1,553 ordered original MZ relocations**. Independently
checked standard DOS MZ serialization reproduces all **130,882 original
Japanese MAIN.EXE bytes**; this does not establish original vendor
linker-header byte construction. The other **98 original game objects
and CRT were reused unchanged**, no full cold replay or target/object
patches.

Protected actual source-bound native report with both compiler/TLINK
writer rounds: `.analysis/work/exatt-layout-af866g/report.json`, SHA-256
`8636fa9b4e682b0e4dd70b3316259be29e391b3675050302087430935650778b`.
This was an already historically source-covered original physical
BOSS; recovery is about exact current C++ code, **not new distinct CODE
coverage, raw vendor packet identity or canonical Factory packed credit**.
