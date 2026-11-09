# TH03 MAIN — shared BOSS ring and scheduler semantics (af1109c)

The original shared BOSS prefix has two physical owners: the 24-sprite
explosion ring and the remaining movement/launch/hit-test/target/pattern
scheduler. Their full source is verified as one affected two-OBJ scope.
Both primary/secondary sprite orbit loops now use natural prefix signed-index
increments and compound byte-angle updates in their `for` headers. The ring
angle initializes at first use after the original signed length multiplication,
and the pattern selector's byte RNG scratch is scoped to its active waiting
branch. The boss-launch sound has a named original value without moving its
call relative to state copying and the palette reset.

Stages `af1109a` (loops/launch sound), `af1109b` (angle and RNG lifetimes),
and `af1109c` (byte angle compound steps) all reproduce both original
Turbo C++ 4.02 objects across two independent full normal MAIN links.
Their total original CODE is 949 bytes, with 106 ordered native fields,
eight PUBLICs, the complete original Japanese MAIN loaded image and all
1,553 ordered MZ relocations intact. Final current-source evidence:
`.analysis/work/exatt-layout-af1109c/report.json`.

Original register-mediated template copying, signed multiplication and byte
postincrement of `boss_angle`/`boss_pattern_i` stay unchanged, since their
machine instructions are part of the target. Source-native matches are not
canonical Factory packed-product acceptance.
