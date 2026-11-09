# Ellen BOSS: native terminal exits across three attack families

The full Ellen BOSS controller now expresses the final frames of the
spread, Extra Attack and paired-pellet patterns with natural early-return
guards. The spread's original `fire_single` and `done` labels still preserve
the independent sound and bullet call order. The last radial Extra Attack
retains a distinct local scope for its signed index and mutable byte angle;
no RNG draw is moved. The paired-pellet pattern retains its two-stage bullet
speed calculation before the final mode transition.

Original TC4/TLINK stages `af1187a` (pellets), `af1187b` (spread), `af1187c`
(last Extra burst), and final `af1187e` match all **1,675 CODE bytes**,
213 ordered native fields, nine PUBLICs and the complete Japanese MAIN
loaded image/ordered MZ relocations in two independent rounds. An isolated
`af1187d` experiment removed the final Extra burst's enclosing C++ scope;
TC4 changed CODE, so that register-lifetime block remains.
