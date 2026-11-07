# TH03 MAIN Yumemi full Extra Attack lifecycle/renderer: current-native after738

The complete source `src/main/player/exatt_yumemi.cpp` owns the **five
original 16-bit physical `ex_yume` functions**: ordinary and special
projectile creation, substantial cross-shaped GRCG beam/VRAM sprite
rendering, full 16-entity update/collision and the looped renderer.
This is not a leaf-only or truncated function test. Original entity slots
are partitioned into ordinary 0..7 and special 8..15, and the original
byte state machine moves from free (0) to flying (2) or appearing (3..40)
and later beam (1). The original 8-frame warning, duration, radius
geometry, renderer clip and actual random consumption remain intact.

This pass recovers a **named natural C++ lifecycle** (`YUME_EXATT_FREE`,
`YUME_EXATT_BEAM`, `YUME_EXATT_FLYING`, `YUME_EXATT_APPEARING_FIRST`) and
naturally tests inactive/active entities via `if(!p->state)` and
`if(exatt_entity_p->state)`. The flight-update result uses ordinary
truthiness rather than explicit `!= 0`. All four signed loop indices
in the two add functions, update and renderer naturally use prefix `++i`.
The byte *memory* increments (`p->frame++` and `p->state++`) and original
coordinate and sprite register lifetimes were deliberately preserved.

A real original TC4 4.02 first source experiment `af738a` passed the full
object with these changes. A second `af738b` additionally tried reducing
the two explicit renderer `pid_current == 1` clip-selection comparisons
to `if(pid_current)`. That *failed* actual CODE byte comparison: the
original clip-side Boolean shape is a compiler-visible choice. These
conditions were restored; final `af738c` still retains the named
lifecycle and now verifies its zero-state enum reset explicitly.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af738c --units ex_yume
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af738c

Both rounds of genuine Turbo C++ 4.02 and normal MAIN TLINK reproduce
**all 1,696 original CODE bytes, all 87 literal ordered native OMF FIXUPP
fields, all 5 PUBLICs, full segment definitions and source dependencies**.
The complete normal 99-object MAIN EXE/MAP remains the source-native
parent, with original Japanese 124,642-byte loaded program and all
1,553 ordered MZ relocations equal. Independent standard MZ serialization
reproduces the complete original 130,882-byte Japanese MAIN.EXE. The
other 98 project objects and original CRT were reused; no full cold replay.

Final current-source proof: `.analysis/work/exatt-layout-af738c/report.json`
SHA-256 `1d5a9c343a7d39f33f49cb9efe3981f003b13de45dd1eac47fdf3a154b80fb15`.
Both independent writer rounds, physical OBJ, full TLINK outputs, original
MZ serialization and source/OMF dependency receipts are retained.
`af738b` remains a rejected native compiler experiment, not an accepted
source. Existing original CODE ownership is not additional canonical
Factory packed-game credit, historical vendor-raw OMF packet identity or
whole-game completion.
