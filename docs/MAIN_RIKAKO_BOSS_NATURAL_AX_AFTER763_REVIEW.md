# TH03 MAIN Rikako BOSS: natural signed Y shift and offset replace manual AX after763

The complete original 16-bit `ba_rikak` source owns eight public functions:
three attack families, the full BOSS controller/collision state machine,
main ring/sprite rendering and the sixteen-sprite intro renderer. The
original initialized CODE is **1,677 bytes**, with **215 ordered literal
OMF FIXUPP fields and eight PUBLIC locations**. This pass changed the
actual large intro sprite-loop C++, not just a separate tiny leaf.

The historical source manually loaded `top` into `_AX`, shifted AX as
signed 16-bit, performed `_AX += -8` (the original `ADD AX,-8`, rather
than a compound memory subtraction), stored AX back into `top` and
passed `_AX` to `sprite16_put()`. Real TC4 4.02 reproduces the exact
original signed shift and offset from entirely **natural C++**:

    top = static_cast<screen_y_t>((top >> 4) - 8);
    sprite16_put(left, top, sprite_offset);

Both the signed `-8` written as `+ -8` and the natural subtraction form
were independently source-native exact. Original 16-bit radius/angle,
cosine/sine calls, 16 sprite operations, register-local loop order and
palette/clip state remain unchanged. No hand-written original opcode,
binary padding or OMF packet replacement was inserted.

Actual original compiler trials:

- `af763a` — natural signed Y shift followed by `+ -8` matched entire
  original CODE and full original normal MAIN link in both rounds.
- `af763b` — the more readable `(top >> 4) - 8` also matched fully;
  TC4's optimizer emitted the historical signed AX code for the original
  two-step local lifetime.
- `af763c` — passing the computed coordinate inline as a direct
  `sprite16_put(left, expression, ...)` argument changed original CODE.
  This was rejected: the local writeback is compiler-codegen visible.
- `af763d` — final maintained natural-source assignment with explicit
  rationale, freshly recompiled and full-linked in two original TC4
  4.02 rounds. All original byte and OMF fields match.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af763d --units ba_rikak
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af763d

Both genuine native rounds reproduce **all 1,677 original CODE bytes,
215 ordered OMF FIXUPP fields, eight PUBLIC offsets**, original segment
and source COMENT dependencies, complete normal MAIN EXE and MAP,
original Japanese 124,642-byte loaded program and all 1,553 ordered
MZ relocations. Independent ordinary DOS MZ serialization reproduces
all original Japanese 130,882-byte MAIN.EXE bytes. The other 98 project
objects and original CRT reused unchanged; no full cold replay.

Latest proof `.analysis/work/exatt-layout-af763d/report.json`, SHA-256
`c86202442426080c597c976c42cc326691066503a20fbeb2971197d461928a9e`.
The native writer output for the rejected inline-argument trial remains
retained. This is genuine maintainable source recovery for already
owned original CODE, **not** new canonical Factory accepted packed-game
byte credit, original historical vendor OMF raw-packet equality or
whole-game reconstruction acceptance.
