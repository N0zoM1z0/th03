# TH03 MAIN VSYNC frame delay and resource handoff: direct source-native after740

Two original physical source slots used by TH03's normal MAIN are now
directly bound to the maintained C++ source in the scoped compiler:

- **`frmdely1`** — `src/main/hardware/frame_delay.cpp`, original shared
  TH02 object `obj/th02/frmdely1.obj` linked into TH03 MAIN. The complete
  **21-byte SHARED CODE** has two literal ordered OMF fixups and one
  original far-Pascal `frame_delay(int)` PUBLIC. The real original MAP
  source identity is `th02/frmdely1.cpp`, not a synthesized TH03 one.
- **`execl`** — `src/main/core/execl.cpp`, original TH03 source object
  `obj/th03/execl.obj`, with **79-byte HITCIRC_TEXT CODE**, original
  empty EXECL_TEXT/DATA/BSS sections, eleven ordered literal fixups and
  one original far-Pascal `main_exec` PUBLIC. The full routine frees
  PI, sprite, TRAM, gaiji and MRS resources and calls `game_exit()`
  before the original large-model executable handoff.

The unchanged current-source direct compiler/TLINK control `af740a`
rebuilt **both original physical objects** in two genuine Turbo C++
4.02 rounds and matched the original CODE/FIXUPP/PUBLIC/segment contracts,
full normal MAIN/MAP and original Japanese loaded program.

The VSYNC wait now uses a natural `for(; vsync_Count1 < frames; )` loop
instead of the old `while`. The counter remains **volatile unsigned
16-bit**, the caller's original signed frame argument is left intact,
no delays or timeout checks are added, and the empty busy loop still
observes the real PC-98 interrupt-updated counter.

One alternative C++ modernization **failed** in `af740b`: replacing
`main_exec`'s historical casted far/near `execl` parameters and the
original four-byte far null vararg with `reinterpret_cast` and
`static_cast` produced real original TC4 compile errors (incompatible
const/address-space pointer conversions and integer-to-far-pointer cast).
The original C-style casts remain intact because they model the
historical large-memory-model compiler/ABI behavior. The accepted
`af740c` source retains the original `main_exec` implementation and
the natural frame-delay loop, and both native rounds succeeded:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af740c --units frmdely1,execl
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af740c

Both complete actual original compiler and normal full MAIN TLINK
rounds match **all 100 CODE bytes, 13 ordered literal OMF FIXUPP
fields, two PUBLIC offsets and all segment definitions**, original
99-object normal MAIN EXE/MAP, the complete **124,642-byte Japanese
loaded program and 1,553 ordered MZ relocations**. Independent standard
MZ serialization matches the **130,882-byte Japanese MAIN.EXE**.
The other 97 game objects and original CRT were reused, **not cold-
rebuilt**. No code patches or fabricated original object bytes were used.

Current original-source proof:
`.analysis/work/exatt-layout-af740c/report.json` SHA-256
`ce27b432c73776a0229c52197ace2291d9991ea21545841929883e5e118fbeb0`.
Actual native source/OMF input comments, OBJ, full EXE/MAP/linker response,
compiler logs, original MZ bytes and the failed `af740b` source experiment
are retained. These are **new direct current-source attestation scopes**,
not canonical Factory accepted packed-game byte credit, historical raw
vendor OMF packet identity or complete 99-object source ownership.
