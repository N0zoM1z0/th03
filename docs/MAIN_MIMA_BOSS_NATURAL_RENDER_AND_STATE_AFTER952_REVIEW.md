# TH03 MAIN Mima BOSS: named render protocol, template, and attack-state semantics

The complete original nine-function `ba_mima` physical BOSS remains one
maintained natural C++ translation unit. This current-source pass names the
render-mode protocol (normal, particle, expand, flash, trail), the particle
and expanded sprite offsets/sizes/placements, the damaged sprite offset and
placement, and the shared BOSS template's initial center, velocity, HP and
player-two sprite adjustment. It also names the original sound-effect IDs,
spread pellet starting/opposite angles, the signed orbit-angle step and the
first trail phase. Pattern completion now assigns the named
`MIMA_MODE_SELECT` state and normal render mode instead of repeating raw
state bytes.

The existing attack scheduler, all four complete pattern controllers, the
collision path, GRCG split-mask renderer and intro split renderer remain in
the same original physical object. The important code-generation-sensitive
semantics remain untouched: unsigned 16-bit `% period` clocks, the real
six-frame division and byte narrowing in trail, signed compound byte-orbit
steering, the byte render-frame postfix increment, and the mode-5 `goto` into
the shared mode-2 renderer.

## Explored natural alternative and negative control

An actual TC4 trial (`af950a`) replaced the original `goto render_mode_2`
with a `switch` whose trail case fell through to the particle case. It failed
the complete object comparison: the candidate emitted **1,921 initialized
CODE bytes and 279 ordered FIXUPP fields**, not the original 1,922/277.
The maintained source therefore keeps the original `if`/label/goto control
flow. This is a measured compiler constraint, not an assumption based on
older notes.

## Current-source native verification

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_main_exatt_layout.py --stage af952a --units ba_mima
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af952a
```

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
**entire 1,922-byte original Mima BOSS** and linked each object through the
complete normal MAIN response. Both reproduce all **277 literal ordered OMF
FIXUPP fields and nine PUBLIC offsets**, the full original Japanese MAIN
loaded image (**124,642 bytes**) and all **1,553 ordered MZ relocations**.
The other **98 original game objects and original Borland CRT** were reused;
no full cold replay, target patch, original OBJ patch, synthetic byte buffer
or NOP padding.

Protected source-current report:
`.analysis/work/exatt-layout-af952a/report.json`, SHA-256
`d780002d0d8b5daf2756232c0b6e92d461813e045d15a9397b5478b8b7ecee13`.
The full BOSS had historical source coverage already; this pass improves
current natural C++ semantics and native-source provenance, not distinct
original CODE ownership, vendor raw OMF packet identity or canonical Factory
packed-file acceptance.
