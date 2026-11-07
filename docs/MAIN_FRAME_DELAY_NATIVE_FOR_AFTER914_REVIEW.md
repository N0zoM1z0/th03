# TH03 MAIN after914 — original PC-98 frame-delay volatile counter leaf

The historical `frmdely1` physical Turbo C++ 4.02 object owns the
original **21-CODE-byte far-Pascal** `frame_delay(int frames)` service.
It resets the real externally owned, interrupt-updated **volatile
unsigned 16-bit** `vsync_Count1` and busy-polls it against the original
signed 16-bit duration. It must not be replaced by platform sleeps,
a timeout, a cached counter value or signed/unsigned reinterpretation.

The original source can naturally put the once-only reset into the
`for` initializer and use a real original volatile compare each
iteration, with no increment:

```
for(vsync_Count1 = 0; vsync_Count1 < frames; ) {
}
```

The genuine original TC4 machine output remains exactly the target.
However, the old compiler is sensitive even to apparently equal
comparison forms and signedness of the polled hardware counter.

Actually compiled original compiler experiments:

- `af914a`: original reset + `while` became natural `for` with the
  initialization in the header; two full original TC4/MAIN TLINK
  rounds reproduced all original CODE and hardware read ordering.
- `af914b`: swapped `vsync_Count1 < frames` to `frames > vsync_Count1`;
  real TC4 rejected the complete original CODE comparison. Restored.
- `af914c`: cast the unsigned volatile interrupt counter to signed
  `int` before comparing; original CODE changed. Restored unsigned
  volatile operand and mixed original comparison semantics.
- Final `af914d`: exact current source and old-TC4 compile-time
  16-bit ABI guard passed two independent genuine original TC4 4.02
  and full normal MAIN TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af914d --units frmdely1
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af914d
```

Both independent real compiler/linker rounds reproduce all **21
original CODE bytes, two literal ordered native OMF FIXUPP fields,
one PUBLIC offset**, original SHARED/16-bit ABI, full normal MAIN
EXE/MAP, **124,642 Japanese loaded bytes and all 1,553 ordered
MZ relocations**. Independent standard DOS MZ serialization reproduces
all 130,882 original Japanese MAIN.EXE bytes, not historical vendor
linker header-byte identity. **98 unchanged other original project
objects and CRT reused**; no full cold replay, target patch, byte
array workaround or fake NOP padding.

Protected real source-bound original compiler and TLINK report:
`.analysis/work/exatt-layout-af914d/report.json` SHA-256
`7f14f031f8b535eced22a206f134a5e032978b50704b68095ab02796dcd66999`.
Already source-covered original leaf CODE; no new distinct game CODE
or canonical Factory packed-file credit.
