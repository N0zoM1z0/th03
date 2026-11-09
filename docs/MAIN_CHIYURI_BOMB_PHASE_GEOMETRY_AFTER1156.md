# Chiyuri Bomb: native palette and four-axis timing geometry

The complete Bomb owner now names the two shake tones, screen displacement,
palette/fade slopes, and the two successive signed distance scale factors
for the four Cartesian explosions. The **two-stage** `*2` then `*16`
multiplication remains intact, so rounding, 16-bit overflow and the
original TC4 instruction sequence are preserved. The signed axes and
hardware color/VRAM ordering are unchanged.

Original two-round TC4/TLINK `af1156b` matched all 490 CODE bytes,
48 ordered native fields and the full Japanese MAIN image and relocations.
The first trial `af1156a` exposed a real TC4 source limitation: long enum
identifiers that differ only at the end collided in the compiler's limited
identifier namespace. Names were shortened before acceptance. A separate
`af1156c` trial condensed the player-page shift into a ternary; CODE
changed, so the original conditional addition was restored.
