# Marisa Extra Attack: beam, flight and inactive render states

The complete Marisa Extra Attack owner now skips inactive entities with a
natural `continue` in the fourteen-slot sprite pass. Its single-entity
renderer uses early returns for the beam and flying states, leaving the
appearing-state draw as the final path. The beam frame-dependent sprite
choices, live far-pointer aliases and common entity advance order are
unchanged.

Original TC4/TLINK stages `af1196b` and `af1196d` matched all 676 CODE
bytes, 35 ordered native fields, five PUBLICs and the full Japanese MAIN
loaded image and relocations in two independent rounds. Replacing the
player-side sprite clip equality with byte truthiness (`af1196c`) or
moving the full update's signed index into its `for` header (`af1196e`)
changed native CODE; both variants were restored.
