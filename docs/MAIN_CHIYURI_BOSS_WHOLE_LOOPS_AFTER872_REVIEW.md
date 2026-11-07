# TH03 MAIN after872 — complete Chiyuri BOSS native C++ fan and sprite loops

The **entire** 11-function original `ba_chiyu` physical Turbo C++ 4.02
translation unit is rebuilt here: Chiyuri BOSS template, cardinal/ring/trail
and four-fan attack systems, full update/collision state machine, the
16-sprite ring, main/intro/monochrome renderers and dispatch. These are not
isolated source snippets or recompiled stand-in leaves.

The **four independently timed fan emission loops** now use natural C++
`while` traversals. The horizontal ascending/descending speed passes and
the vertical ascending/descending passes retain the original two bullet
calls per horizontal step, signed 16-bit `(i * span) / fan_count` **before**
subpixel scaling, subsequent signed/byte angle reflection and literal
memory speed changes. The animated **16-sprite orbit renderer** also
uses a natural two-variable `while`: the signed integer index advances
and the byte angle increments *after each* sprite call. Its original
32×16 sprite dimensions, original 0x790 offset and two-bit animation
shift now have named semantic constants. Three different signed 16-bit
intro radii 0x100/0x200/0x300, the original frame shift and the unsigned
16-bit eight-frame trail-warning predicate are expressed more clearly
without modifying the crucial AL-mediated mutable byte phases.

## Independently tested genuine compiler alternatives

- `af872a`: the four full fan loops changed from `for` to `while`;
  **both original TC4/full normal MAIN TLINK rounds** matched entire BOSS.
- `af872b`: added the complete signed-index/byte-angle sprite-ring `while`;
  all original CODE and ordered FIXUPPs still matched twice.
- `af872c`: attempted to name the *live byte* sprite `angle += 0x10` as
  an enum-value +0x10. Original TC4 **rejected** this apparently harmless
  spelling: **2,653** initialized CODE bytes rather than original
  **2,654** (first mismatch CODE segment 4, offset 2049). Restored literal.
- `af872d`: changed the unsigned 16-bit trail warning from `%8 ==0` to
  natural `if(!(boss_frame % period))`; full original BOSS remained exact.
- `af872e`: tried naming both **mutable bullet speed +=2/-=2** updates in
  all four fan passes. The actual native compiler generated **2,642**
  instead of **2,654** CODE bytes. Literal byte-memory operations restored.
- `af872f`: named the original sprite orbit dimensions/offset/shift and
  independent intro radii. Two complete native rounds remained exact.
- Final `af872g`: recompiled all current maintained C++ and source comments
  through the *original* TC4 4.02 and complete normal MAIN TLINK twice.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af872g --units ba_chiyu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af872g
```

Both independent genuine original compiler/full normal linker rounds match
**all 2,654 original CODE bytes, 381 literal ordered native OMF FIXUPP
fields and 11 original PUBLIC names/offsets**, original segment/ABI,
complete normal MAIN EXE and normalized MAP, **124,642 Japanese loaded
program bytes and all 1,553 ordered MZ relocations**. Independently
verified standard DOS MZ serialization reproduces the **130,882-byte
Japanese MAIN.EXE**; it does not prove historical vendor header encoding.
**98 other original game objects and CRT are reused**, no full cold replay,
patching, padding or synthetic original CODE arrays.

Protected real compiler/source/OBJ/EXE/MAP/TLINK evidence:
`.analysis/work/exatt-layout-af872g/report.json`, SHA-256
`5f2a1f413000cf4164440836a770b9712e430bcb908c2667cb8053f92223cdac`.
These 2,654 original bytes were already historically source covered: this
is current C++ improvement and native verification, **not additional
unique target byte credit, raw vendor packet identity or canonical
Factory packed-game acceptance**.
