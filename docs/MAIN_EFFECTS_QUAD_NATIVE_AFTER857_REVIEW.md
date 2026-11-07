# TH03 MAIN after857: exact player-effect quad loop and signed raster geometry

The full original **five-function physical `effects` Turbo C++ owner**
contains three BOSS-related explosion/axis spawners, all effect lifecycle
updates and the substantial GRCG circle/quad renderer. Its twelve
physical 10-byte player effect slots are DGROUP globals owned by the
unchanged original storage carrier, not new allocations.

The axis quad's **four-corner vertex traversal** now uses ordinary
typed `while(vertex < PLAYER_EFFECT_QUAD_VERTICES)`, retaining the
original independently advanced signed index and one-byte angle.
The renderer still emits the original **four explicit GRCG line edges**,
not a synthetic polygon; it retains the precise `vertex++; angle +=64`
order, and the original 16-bit `polar` results. Original caller geometry
is now named for the **two different player-field GRCG clip rectangles**
and final 640×200 full-screen clip restoration. The distinct original
circle, center-warning and axis-warning initial radius and signed
radius-delta values are meaningful C++ constants (8/+8, 136/-8,
162/-10), as is the original 16-frame effect expiration gate.

## Genuine original compiler/codegen trials

- `af857a`: four-corner `for` → natural `while` with two post-call
  increments, **full physical original CODE exact** in both TC4/normal
  MAIN TLINK rounds.
- `af857b`: replacing the literal update of the **byte** angle
  `angle += 64` with an enum-valued +64 **changed native CODE**:
  candidate **627** initialized bytes vs original **628**. Literal
  byte update restored; only the vertex count may be safely named.
- `af857c`: native exact with literal +64 and named four-vertex loop
  bound and lifetime expiration threshold.
- `af857d`: challenged `grcg_circle(..., effect->y >> 1, ...)` with
  signed `/2`. It **failed** real native original CODE (candidate
  **631** vs **628** bytes), and negative odd Y values actually have
  different rounding. The original arithmetic shift remains, while
  the polygon's *different* signed `/2` operation is preserved.
- `af857e`: all three original clip rectangles now use named absolute
  player-field geometry and stay native exact.
- `af857f`: named three original signed radius-initialization and
  signed per-frame delta pairs, still **full original CODE exact**.
- Final `af857g`: full current maintained source and all explanatory
  codegen comments recompiled in **two independent original TC4 4.02
  compiler and complete normal MAIN TLINK rounds**, both exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af857g --units effects
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af857g
```

Both original native rounds reproduce **all 628 CODE bytes, 33 literal
ordered native OMF FIXUPP fields, five PUBLIC offsets**, original
segments/ABI/source dependencies, complete normal MAIN EXE/MAP,
**124,642 loaded Japanese program bytes and all 1,553 ordered MZ
relocations**. Independently reviewed standard DOS MZ serialization
reproduces all **130,882 original Japanese MAIN.EXE bytes**. The other
**98 unchanged original project objects and Borland CRT** were reused,
not cold rebuilt; no target-byte patch, inserted NOP, synthetic CODE
array or old source-receipt repin.

Retained protected actual original compiler and linker proof:
`.analysis/work/exatt-layout-af857g/report.json`, SHA-256
`302de7723555257d9705b4508bc252d0d00ab419e3813f125c2c9c2eb38545b3`.
This is **source-native improvement of already historically covered
physical CODE**, not additional unique game byte ownership, raw original
vendor OMF packet identity or canonical Factory packed-file acceptance.
