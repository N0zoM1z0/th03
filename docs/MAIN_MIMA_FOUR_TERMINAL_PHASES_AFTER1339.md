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

## 2026-11-11: exact incomplete-frame exits in all four attack families

The maintained Mima source now ends spread, random-bomb, trail and orbit
patterns with independent *incomplete-frame* returns, then commits the
original SELECT/mode/frame reset. The spread's inclusive last volley
still fires before completion; the random barrage's single dense ring,
trail's signed byte angle and the orbital pellet pair likewise finish
all original effects before their respective terminal checks.

The complete `ba_mima` owner passed separate two-round original TC4/TLINK
stages `af1359c` (spread) and `af1359d` (all four), reproducing **1,922
CODE bytes, 277 ordered native fields and nine PUBLICs**. Dependent
`af1359f` rebuilt Mima BOSS, Bullet, both shared BOSS objects, Mima
Extra Attack and sound service together: **6,403 CODE bytes, 641 fields,
43 PUBLICs** and both complete normal Japanese MAIN links and ordered
MZ relocations original-exact.

Three negative compiler controls bound these recoveries. `af1359a`
reordered two trail subphase predicates, `af1359b` moved the random-bomb
warning into a new nested time window, and `af1359e` made the particle
renderer animation thresholds independent. All three changed the
complete original `ba_mima` CODE; these alternatives were restored,
including the original trail-to-particle `goto` and sprite call order.

Current proof: `.analysis/work/exatt-layout-af1359d/report.json`, SHA-256
`d702faebc2129ffe2be8c231300d916f1b5565c8109979ed0ba181d7fff7a272`.
Joint proof: `.analysis/work/exatt-layout-af1359f/report.json`, SHA-256
`aa75160e97c35a62f246b2316fc54c5ceed1431d4b0f8459512ccd33e2b16099`.
