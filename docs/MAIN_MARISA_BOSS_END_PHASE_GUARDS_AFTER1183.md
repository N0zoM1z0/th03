# Marisa BOSS: exact terminal phase guards in three complete attacks

The full `ba_maris` BOSS now treats the unfinished final frame of its wide
four-column, narrow three-column, and 32-frame ring attacks as an early
return. The original Extra Attack calls, per-volley RNG order, warning
renderer flags, signed bullet divisions and ring sprite/template mutations
all remain in their original phase order. The three finish paths only
reset mode and frame after the appropriate original threshold.

Successive original TC4/TLINK stages `af1183d` (ring), `af1183e` (wide
columns) and final `af1183f` (narrow columns) each matched the full 1,431
CODE bytes, 199 literal native fields, nine PUBLIC offsets, and complete
Japanese MAIN loaded image and ordered MZ relocations in both compiler
rounds.

An independent `af1183a` attempt moved the main sprite-strip temporary
into a narrower post-guard lifetime. Its CODE changed and was rejected;
the original renderer local remains in its proven scope.
