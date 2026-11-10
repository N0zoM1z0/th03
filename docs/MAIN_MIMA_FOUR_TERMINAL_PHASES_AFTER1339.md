# Mima BOSS: exact terminal gates of all four major attack families

The full Mima BOSS now describes completion as a *positive* state
transition for all four patterns, rather than an early return followed
by an unguarded tail. The repeated paired spread and pellet barrage
finishes only **after** its inclusive `MIMA_SPREAD_FIRE_END_AFTER` frame;
random bombs finish **at** frame `0x80`, trail bullets at `0x96`, and the
signed-angle orbital ring at `0x48`. Each update still happens after all
RNG draws, warning effects, `bullets_add()`, sound and render-template
flag restoration at that frame. There is no new guard or gameplay fix.

The random-bomb single 32-way ring and orbit-direction selection now use
the live unsigned-word `boss_frame` on the left of their equality tests.
Mima's renderer still tests both particle animation thresholds in their
original order; the second can change the renderer mode without skipping
the current carrier sprite. The original trail-mode `goto render_mode_2`
and separate particle, expand, flash branches are retained.

Positive original TC4/TLINK stages `af1339a` (four terminal windows)
and `af1339b` (renderer and timing comparisons) each exactly reproduced
the entire native 1,922-byte owner in two rounds. Final source-bound
`af1339d` matched **1,922 CODE bytes, 277 ordered OMF fields, nine
PUBLICs**, complete segment/MAP layout, two normal Japanese MAIN
images and ordered MZ relocations. Joint `af1339e` recompiled Mima,
Bullet and the two original shared BOSS owners: **5,556 CODE bytes,
579 ordered fields, 37 PUBLICs** and both entire normal links matched.
Only these affected objects were recompiled, without cold replay.

An unsuccessful `af1339c` inverted the far renderer's final explosion
choice into a positive `if/else`. It kept the same full CODE size and
field count but changed `JE` to `JNE` at offset `0x776` and swapped the
near-call destinations. That source was reverted; the historical
branch ordering remains necessary for exact native reconstruction.

Read-only source-bound proof:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1339d af1339e
```

This is a physical source-exact scope, not new gameplay CODE coverage or
Factory packed-file/whole-game acceptance.
