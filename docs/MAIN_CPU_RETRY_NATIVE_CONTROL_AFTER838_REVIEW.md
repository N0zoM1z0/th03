# TH03 MAIN after838: complete CPU AI retry state and collision semantics

The complete original `p_cpu` physical TC4 source owns four original
functions: 3x3 collision-direction selection, target approach, careful
mode selector and the large dodge-and-aim/retry controller. It uses
original 16-bit subpixel geometry and signed 8-bit probe/retry storage.

The careful-mode collision retry control is now a **natural `for(;;)`**
loop with the original break points. The 4-frame collision scan cadence,
three signed left/center/right collision regions, floor escape X and the
three-region dodge strategy row stride now have semantic C++ constants.
The original **discarded but really executed RNG draw**, collision
safeguards, attempt ordering, `INPUT` bitmask flags and the distinction
between the first wide and subsequent narrow hit tests are preserved.

Genuine original TC4 compiler/normal MAIN TLINK experiments:

- `af838a`: actual `while(true)` -> natural `for(;;)`, both original
  independent compiler/link rounds exact.
- `af838b`: combining two original hit-test branches into a ternary
  call argument **failed** complete CODE equality (**1,081** vs original
  **1,077** bytes). Kept the two original call paths.
- `af838c`: separately named scan clock, collision bands, floor escape
  and 3-column strategy, complete physical source still exact twice.
- `af838d`: replacing the original direction-bit Boolean shift/OR with
  a seemingly equivalent ternary flag selected different TC4 output
  (**1,073** vs 1,077). Rejected; the original shift sequence remains.
- `af838e`: recompiled final current maintained source with restored
  exact branch and flag operations, twice through original TC4 4.02
  and complete normal TLINK; both rounds passed.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af838e --units p_cpu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af838e
```

Both final rounds match **all 1,077 original CODE bytes, 64 literal ordered
native FIXUPP fields, 4 PUBLICs**, original segment/storage ABI and
compiler-consumed current source, complete normal MAIN EXE/MAP, all
124,642 Japanese loaded program bytes and 1,553 ordered MZ relocations.
Independent standard MZ serialization recreates the 130,882-byte
Japanese MAIN.EXE. The other **98 original game objects and CRT** were
reused unchanged: no cold replay, input patch, object padding or target
substitution. Protected current-source report:
`.analysis/work/exatt-layout-af838e/report.json` SHA-256
`9bc84e3c7a184e130127c7ca85a90f8fbbba8d1d196c3ae1cf85d45808876e10`.

This is reverified **previously owned** CPU source, not newly distinct
original CODE ownership or canonical packed-file Factory acceptance.
