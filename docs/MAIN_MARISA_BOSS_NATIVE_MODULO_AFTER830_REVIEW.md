# TH03 MAIN after830: native original Marisa major BOSS source recovery

The **complete** nine-function original `ba_maris` physical source owns the
Marisa BOSS initializer, four spread/ring/narrow/wide attack families,
whole update/collision, normal renderer, the split-mask sprite renderer and
entrance renderer. This is not a synthetic per-function compile.

Original `boss_frame` and `round_or_result_frame` are unsigned 16-bit frame
clocks. All **three independent bit-mask cadence expressions** in the BOSS
now compile exactly as **natural C++ unsigned remainder**: `%4` for the
spread volley, `%32` for the rotating projectile ring, and `%4` for the
normal renderer's alternating sprite flicker. The physical 16-bit ring
count is still used as the divisor of the ordered `256 / count` angle step.
A width/height/offset-sensitive pair of distinct vertical-column attacks
now uses clear named C++ constants for the four wide and three narrow
release positions, while retaining their distinct original terminal
frames and **16-bit subpixel** Y coordinate (0x1700). The split intro's
200-pixel start distance is also named; neither its original two
monochrome masks nor the signed X offset is rewritten.

The genuine original Turbo C++ codegen experiments were not simply
inferred from arithmetic equivalence:

- `af830a`: all three unsigned `%` expressions passed both complete
  original TC4/TLINK rounds, matching the full physical BOSS CODE.
- `af830b`: replacing `marisa_bullet_angle += 7` with a named integer
  enum **failed** whole CODE equality, producing **1,427** initialized
  CODE bytes against the original **1,431**. Byte-memory/AL lowering
  changed. It is a retained rejected native control, not accepted code.
- `af830c`: restored the literal byte angle step while retaining the
  natural unsigned attack/render clocks and meaningful column/angle/
  split constants. Both original compiler/normal linker rounds pass.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af830c --units ba_maris
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af830c
```

The **entire 1,431 original CODE bytes, 199 literal ordered native
OMF FIXUPP fields, nine PUBLIC offsets**, original source/segment
ownership, both complete normal original MAIN EXE/MAP and the **full
124,642-byte Japanese loaded program with all 1,553 MZ relocations**
match in both independent genuine TC4 4.02/TLINK rounds. The independent
standard MZ serializer recreates the **130,882-byte Japanese MAIN.EXE**.
The other **98 original game objects and Borland CRT were reused**, with
no cold replay or target-byte patching. The protected report is
`.analysis/work/exatt-layout-af830c/report.json`, SHA-256
`32c52ccd3bdceaf17d87b69aa3b6d5949e21810a722f54e832f983c6794458c9`.

The original physical owner was already covered by historical native
proofs: these are **current source-recovery improvements, not new unique
original CODE credit or canonical packed-game Factory acceptance**.
Raw vendor OMF packet identity and original compiler source text remain
separate, unproven claims.
