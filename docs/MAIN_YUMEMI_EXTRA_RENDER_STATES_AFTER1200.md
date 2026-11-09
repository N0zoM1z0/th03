# Yumemi Extra Attack: native 16-slot rendering and flight states

The complete Yumemi Extra Attack now skips inactive slots with a natural
`continue` in its sixteen-entity renderer. The single-entity renderer exits
after the flying state, and otherwise falls through to the appearing-state
sprite helper. Its update controller initializes the opposing player byte at
first use. The four-sided beam geometry, signed radius divisions, hardware
GRCG/EGC ordering and collision-map updates are unchanged.

Original TC4/TLINK stages `af1200a` (slot traversal), `af1200b` (render
states), and `af1200c` (player-byte lifetime) each matched all 1,696 CODE
bytes, 87 ordered native fields, five PUBLICs and the full Japanese MAIN
loaded image and MZ relocations in two rounds. Narrowing the beam sprite
offset's lifetime into the rendering branch (`af1200d`) changed TC4 CODE,
so its original wider declaration remains.
