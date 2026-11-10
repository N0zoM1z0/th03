# Reimu BOSS: historical cloud-attack source checkpoint

The full `ba_reimu` BOSS owner now selects the second player's sprite
resources with natural PID truthiness. The orbiting-cloud attack returns on
unfinished frames after its usual bullet and movement operations; only its
terminal tick resets the attack mode and BOSS frame. The original cloud
radius, extra-projectile RNG and draw ordering are unchanged.

Both TC4/TLINK rounds at `af1204a` reproduced 2,020 CODE bytes, 270 ordered
native fields, nine PUBLICs and the complete Japanese MAIN loaded image and
ordered relocations.

This is the earlier `af1204a` native experiment. Subsequent natural source
refinement is currently bound by `af1304d` in
`MAIN_REIMU_BOSS_CLOUD_PHASE_AFTER1304.md`.
