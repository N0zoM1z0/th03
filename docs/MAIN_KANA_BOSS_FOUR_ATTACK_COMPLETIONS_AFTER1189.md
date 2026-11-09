# Kana BOSS: four native terminal attack guards

All four full Kana attack controllers now return directly on unfinished
frames: accelerating ring, three-stage ring with its sixteen-pellet middle
burst, random cloud, and rotating ring. The warning and release frames keep
their original short-circuit returns; no projectile, RNG or sound call is
moved across a phase boundary. The rotating ring's AL-mediated signed angle
selection remains untouched because earlier native trials showed that a
C++ `switch` changes the instruction stream.

Scoped original TC4/TLINK stages `af1189a` (acceleration), `af1189b`
(staged), `af1189c` (cloud) and final `af1189d` (rotating) each reproduced
**1,874 CODE bytes**, 274 ordered native fields, nine PUBLIC offsets and
the complete Japanese MAIN image and ordered MZ relocations in both rounds.
