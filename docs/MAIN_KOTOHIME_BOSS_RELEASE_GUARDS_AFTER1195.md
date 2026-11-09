# Kotohime BOSS: exact release guards in three attacks

The random ring, aimed double ring and pellet-arc attack controllers now
return before releasing projectiles or changing attack modes when their
respective frame thresholds have not elapsed. The expanding-ring animation,
original AL-mediated byte-phase updates, two separate aimed emissions and
all five pellet-arc positions remain in their original source order.

Incremental original TC4/TLINK stages `af1195a` (random ring), `af1195b`
(aimed ring), `af1195c` (flattened release bodies), and `af1195d` (pellet
arc) each matched all 1,840 CODE bytes, 262 ordered native fields, eleven
PUBLICs, and the Japanese MAIN loaded image and ordered relocations in two
independent compiler rounds.
