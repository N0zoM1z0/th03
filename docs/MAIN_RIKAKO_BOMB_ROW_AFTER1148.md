# Rikako Bomb: native explosion-row traversal

The eight-frame randomized explosion row now uses a natural `for` header
for the signed X-coordinate traversal, preserving the original RNG draw
before the first explosion and 96-pixel spacing after each call. Both
player-side checks use byte truthiness and the word-valued live line-offset
reset compares its unchanged threshold from the constant side.

Original TC4/TLINK `af1148f` reproduces the full `b_rika` owner: 546 CODE
bytes, 56 ordered native fields, and the Japanese MAIN image/relocations
in two independent rounds. A fresh negative `af1148e` showed that replacing
`(frame & 3) < 2` with `(frame & 3) <= 1` changes TC4 instructions, so the
original byte shake predicate remains intact.
