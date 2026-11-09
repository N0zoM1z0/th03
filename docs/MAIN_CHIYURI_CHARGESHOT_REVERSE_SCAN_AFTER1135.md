# Chiyuri Chargeshot: reverse eight-projectile state and five-continue collision

The complete nine-function original `cs_chiyu` physical owner now expresses
its reset, spawn, reverse update, five-way collision rejection and sprite
render as natural `for` loops. The unusual reset still clears only the first
physical slot sixteen times, just as the original machine code does. The
update's clip `continue` and collision's five `continue` exits now join one
near-pointer/index advance in their respective for headers, without moving
byte animation, hit-circle callbacks, sound or shot-state mutations.

Original TC4/TLINK source-native `af1135h` independently reproduced all 1,011
CODE bytes, 96 ordered fields, nine PUBLICs and the full Japanese MAIN image
and ordered relocations twice. The earlier `af1135d` trial failed because it
also moved the collision index declaration into its for header; separate
`af1135g` isolated that source-lifetime change as non-exact. The original
collision index declaration remains outside the loop.
