# TH03 MAIN: combined early collision guard and explicit far callback dispatch

The two early exits in hitbox_hittest() now share one natural C++ short-
circuit guard:

    if(
        (hitbox.origin.center.y.v < to_sp(0.0f)) ||
        (defeat_flag == DF_BANNER)
    ) {
        return 0;
    }

The negative-Y test remains first, so the round-banner test is only read
when the first condition is false. Original TC4 emits the same complete
hitbox object for this combined form.

The two-player Chargeshot dispatch remains two explicit far-callback
branches. Replacing them with the compact indexed expression

    damage += chargeshot_hittest[hitbox.pid]();

changed complete CODE in af998b. Both the original if(!pid) and the
explicit if(hitbox.pid == 0) forms emit the original callback sequence;
the maintained source uses the explicit zero comparison.

The segment-local explosion bridge also remains explicit:
NOP; PUSH CS; CALL near, followed by the original AL damage accumulation.

## Original TC4 experiments

- af986b verified the earlier split early-return guards.
- af998a combined the negative-Y and banner checks; the complete object
  remained exact.
- af998b tried direct indexed far-callback dispatch and changed complete
  CODE; the explicit two-branch form was restored.
- af998c changed if(!pid) to if(pid == 0), preserving complete CODE.
- af998d is the final maintained-source proof with updated source comments.

## Complete original-object verification

Two independent original Turbo C++ 4.02 rounds rebuilt the complete
hitbox physical owner and linked the complete normal MAIN:

| Scope | Exact original result |
| --- | ---: |
| CODE | 266 bytes |
| Ordered OMF FIXUPPs | 33 |
| PUBLICs | 1 |
| Japanese MAIN loaded image | 124,642 bytes |
| Ordered MZ relocations | 1,553 |

The other 98 original game objects and Borland CRT were reused. The
complete physical object, ordered native fields and both normal MAIN
images/relocations match. This is a new current-source proof for an
already historically source-covered object, not additional distinct CODE
ownership or canonical packed-file acceptance.

Reproduction:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af998d --units hitbox

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af998d

Protected report:
.analysis/work/exatt-layout-af998d/report.json, SHA-256
71e32d8a441ad584c96ac721e90e6852b867b751bd82e761278a627deec203b3
