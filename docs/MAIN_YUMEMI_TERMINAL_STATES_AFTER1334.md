# Yumemi BOSS: native-exact terminal state transitions

The complete Yumemi BOSS controller now expresses its ring, aimed,
cross, chase and rain attack completions as positive frame conditions.
Ring and aimed finish **after** their inclusive terminal frame; cross
and rain finish **at** their terminal frame. The chase returns to its
seek state only after the tracking clock has elapsed, and never before
its original double sine movement and conditional beam emission. The
first ring/aimed initialization and warning-phase comparisons place
the live unsigned-word frame/remainder on the left. All RNG draws,
bullet launches, audio callbacks and visual-state changes remain in
the original order.

The genuine TC4 source-bound stage `af1334f` matched the entire
**2,358-byte `ba_yumem` CODE**, 343 ordered OMF native fields and ten
PUBLICs in two rounds. The bounded joint `af1334g` recompiled Yumemi,
Bullet and both shared BOSS objects (**5,992 CODE bytes, 645 ordered
fields, 38 PUBLICs**), with identical complete Japanese MAIN images,
normalized MAPs and ordered MZ relocations.

Two complete-player-structure experiments show a meaningful remaining
source dependency constraint. `af1334a` included the real
`player_stuff_t` at the original collision header position. It compiled
identical machine code but moved `_players` from native EXTDEF index 38
to 22, changing literal OMF fixup targets. `af1334b` moved the full
header after other imports, preserving CODE and field counts but
shifting collision/RNG extdefs. Neither can replace the existing
128-byte player view under the strict complete-OMF check. Both trial
sources were reverted; no linker-output or target byte was patched.

Review the current source-scoped proof without a cold replay:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1334f af1334g
```
