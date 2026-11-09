# Chiyuri BOSS: natural inactive-attack guards

Two of the largest BOSS projectile controllers now explicitly return on
inactive ticks: the four-way cardinal volley and the 32-ring/side-pellet
sequence. This preserves the original byte-angle mutations, 16-bit ring
cadences, conditional extra pellets, sound and RNG draw order. The full
BOSS intro state also separates finished-entry, four-axis warning and
unfinished-entry return paths instead of nesting all outcomes in one chain.

The original TC4/TLINK stage `af1151d` reproduces all 2,654 CODE bytes,
381 ordered native fields, and the Japanese MAIN image/relocations in two
compiler rounds. A separate `af1151e` experiment narrowed the 16-sprite
ring renderer's register-index lifetime; original CODE changed, so that
variable and byte-angle initializer retain their earlier scope.
