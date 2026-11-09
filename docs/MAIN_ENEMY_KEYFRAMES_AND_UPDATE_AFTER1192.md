# Enemy engine: native explosion keyframes and 40-slot update state

The four physical Enemy owners now express explosion hit/decay keyframes as
completed-state returns. Both 40-entity render and update traversals use
natural prefix near-pointer advances, and the full update has explicit
`continue` exits for free entities, explosion state updates and terminated
ENEDAT scripts. Only still-running spawned enemies contribute collision-map
stripes and per-player alive counts. The original script pointer and
cross-segment call contracts remain unchanged.

Stages `af1192a` (keyframes), `af1192b` (complete traversals), `af1192c`
(update control) and final `af1192d` matched all four original OBJ owners:
**3,325 CODE bytes**, 222 ordered native fields, 19 PUBLICs, and the full
Japanese MAIN loaded image and ordered MZ relocations in both TC4/TLINK
rounds. An independent `af1192e` trial inverted the ENEDAT
`EO_MOVE_WITH_SPEED` clip test into an early return; `efornb` CODE differed,
so that opcode retains its proven conditional branch.
