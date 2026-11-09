# Yumemi BOSS: five complete attack-phase terminal guards

The full `ba_yumem` physical owner now expresses the terminal frame
transitions of five different attack state machines as natural early
returns: expanding ring, aimed random shot, four-origin cross rings,
chasing beam, and raining projectiles. Each guard leaves the projectile
setup, independent RNG calls, byte-valued angle and velocity arithmetic,
mode selection and rendering updates in their original order. The chasing
attack still keeps its separate range-seek and periodic beam-return paths.

Successive original TC4/TLINK stages `af1185a` (ring), `af1185b` (aimed),
`af1185c` (cross), `af1185d` (rain), and final `af1185e` (chase) all matched
**2,358 CODE bytes**, 343 ordered native fields, ten PUBLICs and the full
Japanese MAIN loaded image plus ordered MZ relocations in both rounds.
These branches were tested individually because reversing superficially
equivalent BOSS conditions can change compiler output or signedness.
