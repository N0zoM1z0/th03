# TH03 MAIN Chiyuri major BOSS control/render state — after712

The complete maintained `src/main/boss/chiyuri.cpp` now names the separate
cardinal/ring **0x80** attack end gate, intro cross-warning at **0x50**, intro
transition at **0x60**, selection at **0x30**, and the two different render
palette modes **0x10** and **0x20**. The complete BOSS update switch keeps
its original order of the frame increment, warning effects, original RNG,
pattern counter, collision/hitbox updates and exit conditions. The render
helper's descending palette thresholds and the intro's 0x20/0x40 phases
are recorded with explicit source symbols rather than anonymous literals.

Natural C++ truth tests replaced explicit zero comparisons for the cardinal
reverse byte and selected hit/render state checks. The intro's low-bit
round-frame guard is also naturally boolean. These are **verified** exact
16-bit codegen choices, unlike the original mutable `boss_move_phase--`,
`boss_render_frame &= 3` and AL carry-chain animation, which remain intact
because earlier tests established codegen differences for naive rewrites.

Scoped genuine original TC4 4.02 / normal MAIN TLINK source verification:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af712a --units ba_chiyu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af712a

Both independent compiler/link rounds match the entire original **2,654 CODE
bytes**, **381 ordered literal OMF fixup fields**, **11 PUBLIC offsets**,
segment definitions, normal full MAIN/MAP, Japanese loaded image and all
**1,553 original MZ relocations**. Independent standard MZ serialization
matches original Japanese MAIN.EXE bytes. **Only** `ba_chiyu` was recompiled;
other objects and the original CRT are the unchanged frozen source-native
parent. Proof includes the current-source OMF dependency and both writer logs.

Evidence: `.analysis/work/exatt-layout-af712a/report.json`, SHA-256
`fbb630e5c3c67aeb00f638bc36f7ba81d9505193d34d728920f19c639c9165a9`.
This fresh natural-source verification changes no previously accepted
canonical packed-file/Factory unit credit or whole-product completion claim.
