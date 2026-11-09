# CPU control: native no-hit and collision retry guards

The complete four-function `p_cpu` owner now returns early from the
target-approach hit test if the player was not hit. The defensive retry
loop uses natural zero checks for the collision flag and signed radius,
while the conditional Bomb request uses the original short-circuit RNG
order with a natural zero-remainder predicate.

Both original TC4/TLINK rounds of `af1170d` matched 1,077 CODE bytes,
64 ordered native fields, four PUBLICs and the full Japanese MAIN image
and relocations. A distinct `af1170c` trial inverted the top-level CPU
safety/approach dispatcher and returned early; TC4 changed CODE, so its
original branch order remains intact.
