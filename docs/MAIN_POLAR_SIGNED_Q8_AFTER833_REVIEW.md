# TH03 MAIN after833: exact signed-Q8 polar arithmetic leaf

The original physical `polar` translation unit is small but critical to
BOSS orbit geometry, Chargeshots and projectiles. This pass tested the
complete original far-`__cdecl` 26-byte SHARED CODE module under the
Japanese TH03 MAIN target, rather than replacing it with an
unproven runtime-math approximation.

The maintained natural C++ source now makes the physical width explicit:
`int far __cdecl polar(int center, int radius, int ratio)` takes three
**signed 16-bit** arguments, multiplies radius and trig ratio into a
**signed 32-bit `long`**, applies an **arithmetic right shift of eight**
(Q8 fractional precision), adds the signed 16-bit center, and explicitly
casts the return to the original **signed 16-bit** width. The cast is
accepted because original TC4 emits no extra instructions for it.

## Real native source experiment and non-equivalent alternative

- `af833a` changed the source to `((long)radius * ratio >> 8) + center`;
  both original native compiler/normal linker rounds remained byte-exact.
- `af833b` added an explicit outer `static_cast<int>` for the final
  16-bit result; again all **26 original CODE bytes** matched.
- `af833c` tested replacing the arithmetic `>>8` with the seemingly
  intuitive **signed `/256`**. This is **mathematically wrong for negative
  Q8 products**, because pinned TC4 arithmetic shifting rounds toward
  negative infinity while signed division truncates toward zero.
  Native CODE grew from **26** to **33** initialized bytes and failed
  exact comparison. This genuine trial was rejected, not accepted as
  an interchangeable expression.
- The final maintained source restores the arithmetic shift and documents
  these semantics. Fresh stage `af833d` compiled it twice through the
  authentic original Turbo C++ 4.02 and full normal MAIN TLINK.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af833d --units polar
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af833d
```

Both independent native rounds reproduced **all original 26 CODE bytes,
zero ordered OMF FIXUPP fields, one PUBLIC offset**, the original
SHARED segment and ABI, the complete normal MAIN EXE/MAP, the full
**124,642-byte Japanese loaded program and all 1,553 original MZ
relocation words**. Independently checked standard DOS MZ serialization
reproduces all **130,882 bytes** of the original Japanese MAIN.EXE.
The **98 other original game objects and Borland CRT** were reused:
no full cold replay or binary patching. Protected original-source-
bound report `.analysis/work/exatt-layout-af833d/report.json`, SHA-256
`a0efd7b5ef474975cafda2e4459f1fd873cead69b007569b98be556f5fbdec2d`.

This revalidates previously exact original source and records signed
rounding/ABI behavior; it is **not additional distinct CODE coverage,
original vendor raw OMF byte identity or canonical packed-file Factory
acceptance**.
