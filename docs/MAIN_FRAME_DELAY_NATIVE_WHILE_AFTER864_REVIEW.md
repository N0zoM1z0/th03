# TH03 MAIN after864: original volatile 16-bit VSYNC wait leaf

The original **TH02 shared physical `frmdely1`** project object is
consumed unchanged by TH03's normal MAIN linker response. It owns one
real far-Pascal `frame_delay(int)` entrypoint with **21 original CODE
bytes, two ordered OMF FIXUPPs and one PUBLIC**. The original volatile
`vsync_Count1` is an **unsigned 16-bit counter** updated externally by
interrupts; the caller's `frames` is an original **signed 16-bit `int`**.
The function does not sleep or emulate VSYNC. Its actual busy loop
repeatedly polls the volatile word until the original C++ comparison
stops, after resetting the counter to zero.

The maintained C++ now uses a natural empty `while(vsync_Count1 < frames)`
loop. A file-scope **Turbo C++ 4.02-compatible typedef constraint**
verifies the original 16-bit word/parameter widths without generating
DATA or affecting the original ABI. The hardware side effect, signed/
unsigned promotions and far Pascal boundary remain unchanged.

## Independent real native compiler variants

- `af864a`: changed the original typed `for` to natural `while`;
  both actual original TC4/full normal MAIN TLINK rounds byte-exact.
- `af864b`: challenged the branch by swapping operands to
  `while(frames > vsync_Count1)`. Although comparison-equivalent for
  equal widths, real TC4 generated **22** initialized CODE bytes,
  versus **21** original; the initial difference is CODE offset 9.
  The original volatile-first comparison stays.
- `af864c`: forcing `vsync_Count1` to *signed* `int` in the comparison
  changed original codegen (equal 21-byte length but discrepancy at
  CODE offset 15), and could change behavior once bit 15 is set.
  The original unsigned volatile counter stays.
- Final `af864d`: original counter comparison and natural `while`,
  plus a real legacy-compatible compile-time width proof. Both actual
  TC4/compiler and complete normal MAIN TLINK rounds were exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af864d --units frmdely1
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af864d
```

Both genuine original compiler/normal linker rounds reproduce **all
21 CODE bytes, two literal ordered native OMF FIXUPP fields, one
PUBLIC, original SHARED segment/ABI/source identity**, complete original
normal MAIN EXE/MAP, **124,642 loaded Japanese program bytes and all
1,553 original ordered MZ relocations**. Independent standard DOS MZ
serialization recreates every byte of the **130,882-byte Japanese
MAIN.EXE**. The **98 other unchanged original game project objects
and CRT were reused**, not cold rebuilt, patched or padded.

Protected original-source/OBJ/EXE/MAP two-round report:
`.analysis/work/exatt-layout-af864d/report.json`, SHA-256
`335a57e3401b6e9e2dc6945934dbfe7b55ffa3f447725944983338e4c6ab146a`.
This is exact current maintained C++ for an already source-backed
physical leaf, **not additional distinct original CODE coverage,
raw historic vendor OMF packet identity or canonical packed-game
Factory accepted byte credit**.
