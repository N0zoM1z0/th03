# Rikako Extra Attack: original entity allocation and rendering

The complete `ex_rika` owner now scopes the signed indices of its eight-slot
normal allocator, fourteen-slot special allocator and fourteen-slot sprite
renderer to natural `for` headers. The renderer skips inactive records with
`continue`; individual flying sprites complete their draw with an early
return. Its animation frame initializes at first use. The full homing,
collision and shot-state update retains the original mutable byte values,
RNG draw order, two early-continue paths and signed angle division.

Original TC4/TLINK stages `af1301a`–`af1301f` each reproduce all 702 CODE
bytes, 46 ordered native fields, five PUBLICs and the complete Japanese MAIN
loaded image/ordered MZ relocations across two independent compilation rounds.
