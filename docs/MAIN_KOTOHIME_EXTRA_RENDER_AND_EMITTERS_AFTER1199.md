# Kotohime Extra Attack: native render states and radial emitters

The ten-slot renderer now skips inactive entries with a natural `continue`.
Its beam and flying state handlers return directly, leaving the appearing
sprite as the final path. The frame byte initializes at first use, both
four- and ten-shot emitter indices live in their `for` headers, and the
special-slot near pointer uses a natural prefix increment.

Successive original TC4/TLINK stages `af1199a`–`af1199e` matched all 1,054
CODE bytes, 100 ordered native fields, eight PUBLICs and the Japanese MAIN
image/relocations in two independent rounds. A trial that collapsed the
four-shot directional `if`/`else` into a ternary (`af1199f`) changed CODE;
the original two branch stores remain. Projectile RNG, collision-map calls,
event-counter frame increments and shared entity storage remain unchanged.
