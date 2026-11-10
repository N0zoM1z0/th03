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
