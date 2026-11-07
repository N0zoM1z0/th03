# TH03 MAIN after861: complete Kotohime Extra Attack C++ emission and state

The full original physical `ex_koto` owner contains **eight genuine
original Turbo C++ 4.02 functions**: ordinary/special projectile spawn,
per-entity render/effects, distinct four- and ten-bullet ring emitters,
complete state/collision/event controller and ten-slot render traversal.
The original 8 ordinary + 2 special **32-byte entity slots** and
original DGROUP state remain unchanged. All these functions were compiled
together as one original physical object in every trial, not isolated
standalone leaves.

The four- and ten-projectile ring routines now use **natural C++ `while`
loops** with the original call order (`bullets_add`, 16-bit speed
increase, byte angle increase, integer index increase). The complete
rendering scan's ten-slot `for` also now uses an ordinary `while` with
its correct post-call pointer and signed index increments. These
modifications proved **all original native instructions and ordered
fixups**. The original randomized target range (0x1200 × 0x400),
initial/special flight speeds (0x5A/0x78), signed four-shot ±12 and
ten-shot ±7 angular deltas, 12-pixel collision stripes and signed
16-pixel hit half-width are now named C++ semantic constants. The
2-subpixel bullet speed growth is named in *both* emitters. All original
RNG draw and sound/effect/palette order remains the same.

## Real native TC4 alternatives, including rejected experiments

- `af861a`: both full four- and ten-shot emitters converted to natural
  `while`, exact original TC4/normal MAIN link in two independent rounds.
- `af861b`: ten-slot render dispatcher converted to typed `while`,
  whole original CODE still byte-exact in both native rounds.
- `af861c`: explicit physical target, speed, angle delta and collision
  constants passed original exact codegen in both rounds.
- `af861d`: named both `bullet_template.speed.v +=2` operations and
  retained exact original CODE and ordered fixups.
- `af861e`: changing the **mutable 8-bit event counter** from postfix
  `p->angle++` to prefix `++p->angle` emitted **1,059** candidate
  CODE bytes vs original **1,054**; the original postfix form remains.
- `af861f`: substituting `p->y = p->y + p->radius` for the original
  16-bit `p->y += p->radius` likewise **failed** native comparison,
  with **1,057** initialized bytes. The compound operation remains.
- Final `af861g`: retains all the proved natural loops/semantic constants
  and original byte/word update spellings, with fresh two-round
  original TC4 compiler and complete normal MAIN TLINK source proof.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af861g --units ex_koto
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af861g
```

Both independent genuine original Turbo C++ 4.02 compiler and complete
normal MAIN TLINK rounds match **all 1,054 original CODE bytes, 100
literal ordered native OMF FIXUPP fields, 8 PUBLIC offsets**, original
source/header dependency provenance and segment/ABI, both normal MAIN
EXE and path-normalized MAP, **all 124,642 Japanese loaded program bytes
and all 1,553 original ordered MZ relocations**. The independent reviewed
standard DOS MZ serializer matches all **130,882 original Japanese
MAIN.EXE bytes**. The **98 other original game objects and Borland CRT**
were reused unchanged, no whole cold replay, target patch or padding.

Protected actual compiler/TLINK/source-bound report:
`.analysis/work/exatt-layout-af861g/report.json`, SHA-256
`d57caeb9dd2199a4af0f1d75458ccc6b64fdbd4c9d474fefdfb9a4558b308c04`.
The physical owner was already historically source-covered. This is
**new verified natural C++ source**, not 1,054 newly distinct accepted
original bytes, historical vendor OMF packet identity or canonical
packed-game Factory unit acceptance.
