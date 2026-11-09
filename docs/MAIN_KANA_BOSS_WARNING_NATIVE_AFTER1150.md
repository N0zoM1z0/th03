# Kana BOSS: native intro, warning renderer and attack phase boundaries

The full `ba_kana` owner now leaves an unfinished intro by an early return
and keeps the subsequent mode selection and collision work in source order.
The staged warning renderer expresses its active color-cel range with one
nested guard instead of an empty first case. Its sixteen-sprite intro loop
scopes its register index to the `for` header. The acceleration, cloud and
rotating attack finish thresholds use equivalent constant-first comparisons.

Original TC4/TLINK stage `af1150c` reproduced all 1,874 CODE bytes, 274
ordered native fields, and the complete Japanese MAIN image and relocations
in two compiler rounds. A focused `af1150d` trial replaced the rotating
attack's four-way AL-carried random-direction chain with a `switch`; the
compiler changed CODE, so the original chain and AL write remain intact.
