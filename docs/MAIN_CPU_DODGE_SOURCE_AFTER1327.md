# CPU dodge controller: exact floor-escape and retry state

The full CPU controller now checks the playfield floor first, and only
replaces a straight-down move with a sideways escape. The near hit flag,
strategy index, and retry radius are compared explicitly to zero. The
original unbounded nine-direction movement retry is spelled `for(;;)`;
its two different hit-test radii, original RNG draws and fallback
`attempt`/`radius_or_retry` order remain unchanged. The final fallback
is nested under the first direction-choice phase.

Original TC4/TLINK `af1327h` reproduced the whole **1,077-byte** CPU CODE,
64 ordered native fields and four PUBLICs, twice. The combined `af1327i`
recompiled CPU, player core and Hitbox: **4,478 CODE bytes, 357 ordered
fields, 26 PUBLICs** and both complete Japanese MAIN links matched.

Two tempting rewrites were rejected. `af1327b` reversed the careful/fast
strategy branch and changed the original `JA` to `JBE`, while moving the
near-call destinations. `af1327c` replaced the retry-column ternary with
`if/else`, lengthening the owner from 1,077 to 1,083 bytes and shifting
its native jump table. Both source changes were restored.

Scoped review:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1327h af1327i
```

## 2026-11-11: exact collision floor, RNG and retry predicates

The maintained CPU direction leaf now combines its two original floor
conditions in an ordered short circuit: only when the player is near
the bottom and the chosen direction is exactly DOWN does it select a
sideways escape. The x-coordinate split remains a native `if/else`,
not a conditional expression. Approach targeting explicitly gates the
one-in-four bomb RNG behind the original charged-gauge threshold; the
careful mode's word-sized four-frame scan uses a positive zero-remainder
predicate. Hit-flag and retry-radius checks use natural zero tests while
preserving the distinct close/wide hit-test calls and nine-direction
retry behavior.

Negative `af1357i`: the floor direction `if/else` changed to a ternary
expression, changing native CODE; reverted. Negative `af1357j`: dropped
the apparently unused `random_region` and discarded the result of the
original modulo; native CODE differed. That local and RNG draw remain.
Positive owner stages `af1357g`, `af1357h` and current `af1357k` each
rebuilt the complete **1,077 CODE bytes, 64 ordered native fields, four
PUBLICs** in two original compiler rounds. Joint `af1357l` recompiled
CPU, player core, Hitbox, input modes and VSYNC frame delay: **4,866
CODE bytes, 417 ordered fields, 36 PUBLICs**, both normal Japanese
MAIN links and MZ relocation vectors exact.

Current receipt: `.analysis/work/exatt-layout-af1357k/report.json`, SHA-256
`2e556ec20a84ca43e7ef102a71732c8b10140c08d54b4dbda517ebcd0fa52675`.
Joint receipt: `.analysis/work/exatt-layout-af1357l/report.json`, SHA-256
`717a42f0cf3090753de6125a40cfb7834690139f3e96450acbbf24c093802482`.
