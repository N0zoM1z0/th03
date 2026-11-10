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
