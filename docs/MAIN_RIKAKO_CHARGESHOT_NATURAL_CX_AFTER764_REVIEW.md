# TH03 MAIN Rikako Chargeshot: original CX/CL initialization now natural C++ after764

The complete original `cs_rika` physical Turbo C++ module owns **eleven
functions**: charging reset, four-projectile creation/extra modes, the
full orbit and homing/update state machine, charged hit detection and
rendering, and the special Gauge projectile emitter. Its original
initialized CODE length is **1,280 bytes**, with **137 ordered native
OMF FIXUPP fields and 11 PUBLIC offsets**. All functions were rebuilt
in the same real physical original translation unit, not a stand-alone
snippet.

## Genuine register-source reconstruction

Previously `chargeshot_add_rikako()` manually initialized `_CX=0`, tested
`((int)_CX) < RIKAKO_CHARGE_PROJECTILES`, incremented `_CX++` and
constructed projectile angles using `_CL << 6`. The original TC4 4.02
compiler **naturally reproduces the original CX and CL instructions**
from ordinary C++:

    register int i;
    for(i = 0; i < RIKAKO_CHARGE_PROJECTILES; (++i, p++)) {
        p->center.x.v = center_x_raw;
        p->center.y = center_y;
        p->angle = ((i << 6) + 0x20);
    }

There are no longer manual `_CX` or `_CL` register references in the
complete Rikako charged-shot source. The four positions and original
16-bit signed bounded loop index produce precisely the historical angles.
The whole orbit-update, hit-detection and sprite-render loops also
use native-exact local `++i`, leaving pointer increments postfix.
The original parity `static_cast<unsigned int>(i) % 2` in the four-shot
orbit was tested and recovered as ordinary `i & 1`, justified by the
0..3 loop bound. Natural truth tests now cover active/inactive fields,
and a local hit count uses `++hit_count`, without changing signedness,
projectile speed, player ownership or original RNG/phase order.

## Actual original compiler experiments

- `af764a`: first complete physical source with naturally allocated
  CX/CL and a 4-projectile signed loop, two original TC4 4.02 rounds,
  full original MAIN linking, exact code and all original OMF fields.
- `af764b`: extended to the complete 11-function owner, naturally
  incrementing its other loops and using the bounded 2-way angle mask.
  Both original compiler rounds remained exact.
- `af764c`: deliberately challenged register declaration order for
  pointer vs center X. In this case the original native output remained
  exact, demonstrating that this declaration pair is *not* a mandatory
  dependency; do not misrepresent it as a negative control.
- `af764d`: original ordering retained in the final source to minimize
  changes, explanatory actual-codegen comment added, and the complete
  maintained source was independently recompiled and linked again.
  Both native writer rounds match all original bytes and field records.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af764d --units cs_rika
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af764d

Both rounds reproduce **1,280 original CODE bytes, all 137 ordered
literal OMF FIXUPPs, all 11 PUBLIC offsets**, original segment/ABI and
native compiler source COMENT dependencies, complete full normal MAIN
EXE/normalized MAP, original Japanese **124,642-byte loaded program**,
all **1,553 ordered MZ relocations**, and standard-serialized original
**130,882-byte Japanese MAIN.EXE**. The other 98 project objects and
original Borland CRT were reused, no cold replay or target/OBJ patches.

Current-source two-round native receipt:
`.analysis/work/exatt-layout-af764d/report.json`, SHA-256
`8bdf3779b40a1262979b0e4e24cfff1da6f3c6edc9aae8b2ff5ff6483ac31f67`.
The original source and both compiler/EXE/MAP outputs remain retained.
This is substantial natural-source recovery of previously owned code,
**not** newly accepted Factory canonical packed-file units or historical
raw vendor OMF packet identity.
