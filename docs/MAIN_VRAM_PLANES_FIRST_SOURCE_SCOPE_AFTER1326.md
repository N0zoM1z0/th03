# Four PC-98 VRAM plane pointers: new original native source scope

The existing `src/main/hardware/vram_planes.cpp` is now bound to the original
`th01/vplanset.obj` from the Japanese TH03 MAIN normal-link response.
The source assigns the four original B, R, G and E segment-based far plane
pointers, without creating new runtime state. This previously unselected
physical owner was added to the scoped TC4/TLINK comparison by naming
its original `obj/th01/vplanset.obj` linker slot, the source TU and its
three original CODE/DATA/BSS MAP rows. No other compiler or link input
was changed.

The original TC4 4.02 produced all **41 initialized CODE bytes**, **four
literal ordered OMF fixup fields**, **one PUBLIC** and original segment
layout in two rounds at `af1326e`. The actual native OMF source dependency
binds the maintained file, and the complete normal Japanese MAIN loaded
image and ordered MZ relocations match the original in both links. A
bounded joint `af1326g` test also recompiled the already-proven shared
VSYNC frame-delay leaf: **62 CODE bytes, six native fields, two PUBLICs**
and complete MAIN links matched. This adds one distinct physical original
source-bound scope to the selected MAIN inventory, not 41 new target bytes.

A deliberately incorrect `af1326f` trial pointed the E plane at the G
segment; the full-object comparison correctly rejected the changed CODE.
The source was restored and the original passing receipt re-reviewed.
Canonical packed-file or whole-game ownership remains a separate gate.

Read-only source-bound verification:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1326e af1326g
```

## 2026-11-11: native PC-98 segment-pointer assignments

`vram_planes_set()` now uses four ordinary 16-bit C-style segment-pointer
casts, `(dots8_t __seg *)SEG_PLANE_*`, rather than more modern
`reinterpret_cast` expressions. TC4 4.02 still emits the exact original
writes for B, R, G and E planes, with no new pointer temporaries or DATA.
Stage `af1359g` proves all **41 CODE bytes, four ordered native fields,
one PUBLIC**, both independent native compiler rounds and full normal
MAIN links. Joint `af1359k` also rebuilds DOS handoff, initializer,
shutdown and VSYNC delay: **270 CODE bytes, 32 ordered fields, 5 PUBLICs**,
with original image and relocations.

Independent proof: `.analysis/work/exatt-layout-af1359g/report.json`, SHA-256
`cbd264c7ed11834268e206a228c0803a7439bf2118ebf203e720ef43d9b6c93f`.
Joint proof: `.analysis/work/exatt-layout-af1359k/report.json`, SHA-256
`9394c3161407b9da6afb47a1e841eb95f9665f3bd4aca68a6492c63dc6cbc70b`.

The independent `af1359h` trial inverted `game_init_main()` to enclose
all successful hardware-startup calls in a positive allocation gate.
Although the output length remained 62 CODE bytes, the instruction
stream differed; the original early-failure exit was retained.
