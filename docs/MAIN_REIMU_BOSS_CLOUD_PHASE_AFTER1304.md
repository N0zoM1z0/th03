# Reimu BOSS: moving cloud attack finish and template player condition

The complete Reimu BOSS now returns early on unfinished cloud-attack
frames, after performing both orbit position updates and the original
byte-speed acceleration. Only the actual finish tick resets the shared
attack mode. The template initializer uses natural byte truthiness when
selecting the second player's sprite offset. The three orbit projectile
loops, paired shot emission, clip renderer and hitbox logic remain in the
same original physical source owner.

Stages `af1304a` (cloud) and `af1304b` (template), followed by final
`af1304d`, matched all 2,020 original CODE bytes, 270 ordered native fields,
nine PUBLICs and the complete Japanese MAIN image and ordered relocations in
both TC4/TLINK rounds. A separate `af1304c` attempt moved the eight-sprite
intro render index declaration into its `for` header; TC4 changed CODE, so
the wider original lifetime was restored.
