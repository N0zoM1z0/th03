# TH03 MAIN Mima BOSS: complete-object natural C++ clock recovery (after786)

The complete original physical `ba_mima` source contains a shared-template
initializer, four attack pattern families, the whole BOSS update/collision
path, the split-sprite renderer and render dispatcher. This pass recovers
**real natural unsigned C++ modulo expressions**, not just symbolic names.

The native original `boss_frame` is an **unsigned 16-bit** counter. In the
Mima BOSS's spread emitter, random-bomb sound clock and rotating-orbit
emitter, the original handwritten bit check `!(boss_frame & 1)` can be
expressed naturally as `(boss_frame % 2) == 0`. The random-fire cadence
`!(boss_frame & (4-1))` can likewise become
`(boss_frame % MIMA_RANDOM_BOMB_FIRE_PERIOD) == 0`. Genuine original
Turbo C++ 4.02 generates the **same CODE and OMF relocations** in all
four cases. In contrast, the separate six-frame secondary spread remains
real `% 6` division; no byte-valued clock's C++ lowering is inferred from
this 16-bit unsigned result.

The four attack state machines now also name the 2-frame spread setup,
three distinct random-bomb warning frames (0x20/0x24/0x28), the 0x30
wait deadline and the 0x40 ring. This preserves the exact three warning
center additions, RNG draw sequence, 0x80 end transition and movement/
render/update sequencing instead of approximating them with a continuous
range or an alternate clock.

## Exact genuine native experiments

- `af786a`: the first natural unsigned `%4` conversion alone passed two
  full original compiler/linker rounds (complete `ba_mima` CODE exact).
- `af786b`: all three original `&1` gates additionally converted to `%2`;
  the complete owner still passed two original TC4/TLINK rounds.
- **`af786c`**: the same four genuine natural modulo expressions plus the
  named pattern phases/geometry deadlines; two independent exact rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af786c --units ba_mima
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af786c
```

Both complete original compiler/full normal linker rounds match **all 1,922
CODE bytes, 277 ordered OMF FIXUPP fields, 9 PUBLIC offsets** and original
segment/source information; the complete 124,642-byte loaded Japanese MAIN
and all 1,553 ordered MZ relocation words match. The other 98 project
objects and CRT were reused; **no cold replay** or binary patches.
Independently reviewed original source-bound proof:
`.analysis/work/exatt-layout-af786c/report.json`, SHA-256
`319f9b206341894ee5b44b681b6a932b050cc5773b0ad07885d55484ae97606f`.
This is a current-source reproof of an already covered physical owner, not
additional distinct covered bytes or canonical packed-game Factory credit.
