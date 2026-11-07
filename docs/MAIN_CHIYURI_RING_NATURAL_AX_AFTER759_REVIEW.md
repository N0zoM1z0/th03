# TH03 MAIN Chiyuri BOSS ring renderer: original AX register now natural C++ (after759)

The complete original physical `ba_chiyu` source contains eleven functions
including cardinal/ring/trail/fan attacks, the full BOSS update/collision
state machine, and palette, intro and sixteen-sprite ring renderers.
We challenged its historical hand-coded `_AX` in the **ring-render loop**,
not merely renamed constants.

Previously, after `polar()` computed `top`, the source manually loaded AX,
shifted `static_cast<int16_t>(_AX) >>= 4`, stored AX back to `top`, and
passed `_AX` to `sprite16_put`. The original 16-bit TC4 compiler naturally
emits the exact same instructions from:

    top = static_cast<screen_y_t>(top >> 4);
    sprite16_put(left, top, sprite_offset);

This removes explicit `_AX` dependencies in the original ring BOSS
renderer, retaining the signed subpixel shift and local top lifetime.
The original 16-sprite register `i`, radius/cosine/sine polar sequence,
angle side effects, collision ordering and palette paths remain intact.

Actual original compiler experiments:

- `af759a` compiled this natural signed assignment as the complete
  2,654-byte physical original BOSS object and linked the full normal
  MAIN twice; all source/OMF/EXE/MAP fields matched.
- `af759b` tried an even shorter `top >>= 4` in place of the explicit
  signed assignment; original TC4 CODE changed. That experiment was
  rejected, not reclassified as exact.
- `af759c` restored the native-exact expression and added the rationale.
  Both fresh, independent real Turbo C++ 4.02/full normal TLINK rounds
  again reproduced the entire original module and both complete images.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af759c --units ba_chiyu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af759c

Both rounds match **2,654 complete original CODE bytes, 381 ordered
literal OMF FIXUPP fields, 11 PUBLIC offsets**, source COMENT dependencies,
segment and zero-data declarations, full normal MAIN EXE and normalized
MAP, Japanese **124,642-byte loaded program**, all **1,553 original
MZ relocations** and independently serialized full **130,882-byte
Japanese MAIN.EXE**. Other 98 original project objects and Borland CRT
were reused unchanged. No cold replay or output byte patches.

Current-source receipt: `.analysis/work/exatt-layout-af759c/report.json`
SHA-256 `a6b15e0e5e5acd9917b82ac1eeb5276f67ff0c7f322147dca1cf51ee79c12c18`.
The rejected `af759b` is retained as a native negative control. This is
actual natural source recovery of already owned original bytes,
not additional Factory canonical packed-file acceptance or raw vendor
OMF packet identity.
