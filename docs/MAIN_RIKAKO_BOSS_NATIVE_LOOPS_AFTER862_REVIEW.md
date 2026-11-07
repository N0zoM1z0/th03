# TH03 MAIN after862: entire Rikako BOSS C++ emitter and sprite loops

The actual original **eight-function 1,677-CODE-byte `ba_rikak`**
physical Turbo C++ 4.02 owner contains the full BOSS initializer,
orbital and pellet/entity attacks, alternating bursts, full update/
collision, eight-sprite orbit renderer, 16-sprite intro and dispatch.
All code experiments compiled this **complete original BOSS**, not
one convenient leaf function.

## Recovered natural C++ and physical geometry

The **two separate attack ring emitter loops** now express their
original signed `i` traversal and 256-angle-unit division as ordinary
`while` loops, preserving the first emitter's projectile calls and the
second emitter's original RNG result that is consumed then overwritten.
The **eight-sprite normal renderer and sixteen-sprite intro renderer**
also now use natural `while` loops with explicit post-call `++i`
and original byte-angle updates. Both **byte** angle increments
(+0x20 normal, +0x10 intro) are now named semantic C++ constants, with
genuine original bytecode equality proven rather than guessed from
other BOSS characters' register allocation.

The original ring projectile's **signed 48-pixel subpixel radius**,
four pellet volleys and their 8-subpixel speed increase, and the
alternating burst's opposite half-turn are now explicit named compile-
time values. The renderer still uses an *explicit unsigned conversion*
of signed `int i` before `% RIKAKO_RING_ANIM_PERIOD` in both places.
Source-level signed modulo and shortened unary-minus expressions are
**not interchangeable with the original TC4 instruction encoding**.

## Fresh original compiler negative controls and exact retained forms

- `af862a`: both orbit/entity ring `for` emitters changed to natural
  `while` with post-call index updates; original TC4 + complete MAIN
  TLINK passed in both independent native rounds.
- `af862b`: both eight-sprite and sixteen-sprite renderer `for` loops
  changed to `while` with ordered angle/index updates; whole original
  BOSS remained exact in both real compiler rounds.
- `af862c`: named live byte-angle +0x20/+0x10 values passed native
  code equality (unlike some other BOSS memory-angle updates).
- `af862d`: re-challenged the intro's `angle = (0 - angle)` with
  natural unary `angle = -angle`; **failed** original CODE, candidate
  **1,674** vs **1,677** bytes, first discrepancy CODE segment 4
  offset 1429. Binary zero-minus remains exact.
- `af862e`: named exact orbit subpixel radius, four pellet volleys,
  additive speed and opposite-angle constants; the whole original
  CODE and ordered FIXUPPs remained equal twice.
- `af862f`: re-challenged the orbit sprite index with **signed**
  `i % 4`, instead of `(unsigned int)i % 4`. Genuine original TC4
  emitted **1,684 CODE bytes** vs target **1,677**, first difference
  at CODE segment 4 offset 1263. Explicit unsigned conversion is
  required even though the live loop indices happen to be 0..7.
- Final `af862g`: fully restored exact byte-angle and unsigned index
  semantics; **both complete original TC4 4.02 and normal MAIN TLINK
  rounds** match the full maintained current source.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af862g --units ba_rikak
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af862g
```

Both actual original compiler and full normal linker rounds reproduce
**all 1,677 initialized CODE bytes, 215 literal ordered native OMF
FIXUPP fields, 8 PUBLIC offsets**, original segment/source ABI,
complete normal MAIN EXE/MAP, **124,642 Japanese loaded program bytes
and all 1,553 ordered original MZ relocations**. Separately checked
standard DOS MZ serialization recreates every byte of the **130,882-byte
pinned Japanese MAIN.EXE**. **98 other unchanged original project
objects and CRT were reused**, without a full cold replay, patched
original object, synthesized byte array or NOP padding.

Protected genuine current-source native report and two compiler/TLINK
writer rounds: `.analysis/work/exatt-layout-af862g/report.json`, SHA-256
`4088eced3a2cac4ec15b0f552f8de768d3244c841f33a5b42a5049bf33d7cfe9`.
This physical BOSS source was already historically native-covered;
this advances exact maintainable C++ and independently verifies older
hypotheses, **not new distinct original CODE ownership, raw historical
OMF packet identity or canonical Factory packed-file acceptance**.
