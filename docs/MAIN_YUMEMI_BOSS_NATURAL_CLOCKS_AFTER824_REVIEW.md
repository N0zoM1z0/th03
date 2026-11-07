# TH03 MAIN after824: complete Yumemi major BOSS natural C++ clocks

The original physical `ba_yumem` owner contains **ten complete BOSS functions**:
original template initialization, ring, aimed-random, cross, chase and rain
patterns, full BOSS update/hitbox, two renderers and render dispatcher.
This round changed the actual maintained source `src/main/boss/yumemi.cpp`
(not a narrow sidecar leaf or synthetic code-byte array), with exact Turbo
C++ 4.02 codegen confirmed against the Japanese original object.

The original `boss_frame` is an **unsigned 16-bit frame counter**. Its ring
cadence `&3 == 0`, aimed warning `&3 == 1`, aimed shots `!(frame & 1)`, and
chase beam `(frame & 15) == 15` all now use **ordinary C++ `%4`, `%2` and
`%16`** with named original period and phase constants. This retains exactly
the same native instructions, execution order and RNG consumption. The
introduction's two separate sound frames and completion frame are explicitly
named rather than merged into a range; the four 112-pixel entrance raster
phases have the same eight-pixel signed left/right step, also now named. Its
**two-stage shift expression** remains unchanged: collapsing shifts to
one expression was historically shown to alter TC4 instructions, and no
new claim is made that it can be simplified.

Three genuinely compiled incremental experiments progressively checked the
whole original physical BOSS and complete MAIN link:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af824a --units ba_yumem
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af824b --units ba_yumem
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af824c --units ba_yumem
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af824c
```

In the final `af824c`, both independent original TC4 4.02 compiler and
complete normal TLINK rounds matched **all 2,358 original CODE bytes, 343
literal ordered native OMF FIXUPP fields and ten PUBLIC offsets**, exact
segment ownership, full original normal MAIN EXE/MAP, every byte of the
**124,642-byte Japanese loaded program**, and **all 1,553 ordered MZ
relocations**. Independently checked standard DOS MZ serialization matches
the entire **130,882-byte Japanese MAIN.EXE**. The unchanged 98 original
project objects and Borland CRT were reused: **no full cold replay**.

The immutable evidence DAG remains at
`.analysis/work/exatt-layout-af824c/report.json`, SHA-256
`208fe1aa46036cdadbb300709dea1dd5238b07b4c4c598d139a56ec8fd65fbca`,
including the actual two-round source snapshots, original native OBJ/EXE/MAP,
linker response and logs. The present scope revalidates **previously
covered** original CODE bytes; it is not incremental unique source ownership,
raw vendor OMF packet identity, or canonical packed-file Factory acceptance.
