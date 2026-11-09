# Explosion collision: native independent filter and rectangle passes

The full explosion hittest now traverses the original Enemy/Fireball pool
with explicit `continue` guards for inactive explosion states, the enemy-only
hit limit, player ownership, the original low-bit frame clock and all four
rectangle exclusion comparisons. Each rejection still advances the same
near pointer and signed index through the shared `for` header. Chain score,
charge mutation, the signed bonus adjustments and the unsigned hit counter
remain in their original order.

Successive original TC4/TLINK stages `af1198b`–`af1198g` matched all 630 CODE
bytes, 49 literal ordered native fields, the PUBLIC and complete Japanese
MAIN image and relocations in both rounds. Narrowing the signed pool index
to its `for` header (`af1198a`) changed CODE and was discarded.
