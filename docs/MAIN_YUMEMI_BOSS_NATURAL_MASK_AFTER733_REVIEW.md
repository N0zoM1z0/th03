# TH03 MAIN Yumemi BOSS: four attack families and two large render paths (after733)

The maintained complete `ba_yumem` physical TC4 source includes Yumemi's
ring, aimed-random, cross, chase and rain attack patterns, full 18-mode
BOSS update/collision controller and both main/arrival sprite renderers.
Its **2,358 CODE bytes, 343 ordered native OMF FIXUPPs and 10 PUBLICs**
are verified as one physical owner rather than checking leaves in isolation.

## Original-native natural C++ expressions

The independent frame clocks inside the substantial projectile handlers
are now expressed by natural mask arithmetic where their **unsigned 16-bit
periods** are powers of two: `(boss_frame & 3)` in the ring/aimed warning,
`!(boss_frame & 1)` for the aimed volley, and
`boss_frame & (YUMEMI_CHASE_BEAM_PERIOD - 1)` for the 16-frame chase
beam phase 15. The non-power-of-two cross and rain interval divisors
are **not** converted to masks; their actual original `% interval` math
and random-number draw order remain intact.

The following state-machine/renderer conditionals also became normal
C++ truth checks without changing original codegen: the chase move
phase, BOSS effect radius and render frame decay gates, main overlay
and hit sprite selection, combined zero-radius/zero-frame early return,
line/circle selection and the original named intro-mode dispatch.
The complete 16-bit subpixel polar operations, clip registration,
hitbox order, four entrance sprite loops and original generator phase
transitions remain unchanged.

`af733a` genuinely rebuilt **only the complete original `ba_yumem`**
source into two separate Turbo C++ 4.02 objects and linked each through
the original 99-project-object normal MAIN response:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af733a --units ba_yumem
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af733a

Both rounds matched **all 2,358 original CODE bytes, all 343 literal
ordered OMF fixup fields and 10 PUBLICs**, full segment declarations,
complete source-native normal MAIN EXE/MAP, Japanese loaded program
124,642 bytes and all **1,553 original MZ relocations**. Independent
standard MZ serialization reproduced every byte of the original
130,882-byte Japanese MAIN.EXE. The other 98 project objects and CRT
were reused, without a full cold replay.

A second *actual* native TC4 trial `af733b` challenged the renderer-frame
byte decrement, replacing `boss_render_frame--` with prefix
`--boss_render_frame`. The compiler generated **different original
CODE bytes**; the old postfix mutation was restored. The complete final
live maintained source is exactly the reviewed passing `af733a` snapshot;
failed trial output is retained, not counted as source proof.

Primary source-bound evidence:
`.analysis/work/exatt-layout-af733a/report.json`, SHA-256
`ba8b0564536056148de7b24bd629702e318b51e197a67eb79c1995a06f4a9f0b`.
Both complete writer rounds, genuine source/header OMF dependencies,
OBJ/EXE/MAP, original link responses, writer logs, and full Japanese
MZ are retained in ignored protected evidence. This improves source
fidelity for already owned original CODE, **not** canonical packed-game
Factory acceptance, historical vendor raw OMF packet identity, or
whole-game completion.
