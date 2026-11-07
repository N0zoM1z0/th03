# TH03 MAIN Ellen: complete Extra Attack projectile trail and state machine, after746

The complete original `ex_ellen` physical Turbo C++ source comprises
**six functions**, not a single leaf: both ordinary/special projectile
creation paths, twelve-slot-per-player initialization, the 7-point
history and spiral-tail renderer, the substantial collision/movement
controller and the final full active-entity renderer. The original
complete CODE is **1,129 bytes**, with **79 ordered OMF FIXUPP fields**
and **six original PUBLIC offsets**. The unchanged DGROUP trailing-history
storage remains 30 bytes per slot, with the existing packed 32-byte
entity ABI intact.

## Natural source actually recovered

The maintained C++ now names the separate **free (0)** and **active
spiral-tail (1)** states, while preserving the original **flying (2)**
state and signed byte-angle increments. All five original slot-iteration
paths now use ordinary signed local prefix `++i`; the near pointers
`p0++`, `p1++`, `ellen_exatt_slot_p++` and `slot++` remain postfix so
the compiler keeps their original pointer-side effects. The state
allocator, update and full renderer use natural `if(!state)`/`if(state)`
checks where original TC4 emitted the identical code. The flight-update
result is tested via natural truthiness and the renderer's two-playfield
clip path uses `if(!ellen_exatt_slot_p->entity->pid)`. None of these
changes introduce new DATA/BSS or change the collision/history order.

Negative native trial: `af746b` also changed a mutable **8-bit local**
`added++` into `++added`; its original CODE differed. `af746c` reverted
just this prefix mutation and passed both original compiler rounds with
the new natural state, index and clip expressions intact. A final source
comment was added to preserve the finding and **the entire changed live
source was recompiled again** in `af746d`; both genuine TC4/TLINK rounds
were original-exact, not merely assumed code-equivalent to the earlier
writer stage. The failed `af746b` remains in protected ignored evidence.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af746d --units ex_ellen
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af746d

All **1,129 CODE bytes, 79 literal ordered original native FIXUPPs,
six PUBLIC offsets**, all OMF segments and original current-source
COMENT dependencies match both compiled original objects. Both
full 99-project-object normal MAIN EXE/MAP links reproduce the
Japanese **124,642-byte loaded program, all 1,553 ordered relocations**
and complete original **130,882-byte Japanese MAIN.EXE** after
independent standard MZ serialization. Other 98 project objects
and CRT were reused, not cold rebuilt.

Primary current-source proof:
`.analysis/work/exatt-layout-af746d/report.json`, SHA-256
`a6e65c562efdbba85497e07e3cac847a916de1efd29c43b43b00705a81890263`.
The two source-bound native OBJ/EXE/MAP rounds, original linker inputs,
compiler logs and retained negative controls remain intact. These are
existing original source-owned bytes, not new Factory canonical packed
acceptance, historical vendor raw OMF packet identity or full product
source ownership.
