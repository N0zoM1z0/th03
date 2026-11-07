# TH03 MAIN Mima complete major BOSS attack cadence and current-source codegen after749

The previously uncommitted but actually modified maintained source
`src/main/boss/mima.cpp` was **continued, reviewed and preserved** rather
than ignored, stashed or overwritten. It is the complete original `ba_mima`
physical Turbo C++ 4.02 owner: **1,922 original initialized CODE bytes,
277 ordered literal OMF FIXUPP fields and nine PUBLICs**, containing
full BOSS template init, spread, random-bomb, trail and orbital attacks,
whole update/collision/HP controller, normal/split/intro sprite rendering.

## Natural source changes in the whole BOSS

The original unsigned 16-bit clocks have named original **0x10/0x20/0x64**
warning/intro gates, **0x82/0x80/0x96** separate finish conditions,
a four-frame random-bomb clock and two-frame spread/orbit/sound clocks.
The power-of-two clocks use natural `!(boss_frame & 1)` and
`!(boss_frame & (MIMA_RANDOM_BOMB_FIRE_PERIOD - 1))`. The six-frame
side-pellet emission deliberately remains `% 6`; it is **not**
incorrectly converted to a bit mask. The original hit flag uses ordinary
truthiness, and renderer dispatch uses named original Mima intro/explode
mode values. The split renderer's signed 16-bit frame*2 entrance offset
is naturally `boss_frame << 1` while its **four polar radius calculations**
retain the prior native-exact register-local SI allocation. The
original byte spinning, RNG sequence, projectile output order and hitbox
side effects remain unchanged.

## Genuine native experiments and a rejected shortcut

- `af749a` and `af749b` retained source-compiled original-native rounds
  for preceding versions of these modified BOSS attacks/intro expressions.
  Each has a distinct immutable source snapshot. These older receipts
  are historical once source comments and gates are changed again.
- `af749c` tried eliminating the repeated opponent-ID calculation after
  `boss_target_update()` by using the already assigned local
  `bullet_template.pid = pid_other`. This apparently cleaner C++ changes
  the original codegen and **fails the exact original CODE check**.
  The final source deliberately retains
  `bullet_template.pid = (1 - pid_current)` *after* the helper call; its
  separate computation is compiler-visible and not collapsed.
- `af749d` is the final **current live maintained source** with that
  failed ID reuse removed. The independent read-only source-binding
  reviewer confirms both real original TC4 4.02 compiler/full normal
  MAIN TLINK rounds reproduce all the original object/link outputs:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af749d --units ba_mima
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af749d

Both rounds match all **1,922 original CODE bytes, 277 ordered literal
native OMF FIXUPP fields, nine PUBLIC offsets**, all original segments,
current-source OMF input dependencies, complete full normal MAIN EXE/MAP,
original Japanese **124,642-byte loaded program and 1,553 ordered MZ
relocations**, plus independently serialized full **130,882-byte original
Japanese MAIN.EXE**. Only `ba_mima` was rebuilt; the other 98 project
objects and original CRT were reused. No full cold replay or object
padding/patches were used.

Current-source proof `.analysis/work/exatt-layout-af749d/report.json`
SHA-256 `62a3fb482ec61b17598a2ea42264c160fd1ce0371dce8efd376a531fded49b4b`.
The rejected `af749c` native writer stage, all original source/OMF/OBJ,
linker inputs, EXE/MAP and complete native compiler logs are retained.
This is natural C++ progress for **already-owned original CODE**, not
newly accepted canonical Factory packed-file bytes, historical raw vendor
OMF packet identity or whole-product source completion.
