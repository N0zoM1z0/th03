# Yumemi Extra Attack: native beam state and sprite perimeters

The complete five-function `ex_yume` physical owner now uses natural `for`
loops for both first-free allocators, all 16 slots of the beam/flight update,
the complete render pass, and four independent sprite perimeters around
Yumemi's full-width beam. The inactive/arrived update paths share the original
index/pointer advance after each iteration. Both allocator indices and the two
controller indices are declared in their own loop headers. The renderer's
near entity pointer and screen-left register initialize at first use.

The current retained source passed two full original TC4/TLINK rounds at
`af1127g`, including all 1,696 original CODE bytes, 87 ordered native fields,
five PUBLICs and complete Japanese MAIN image and MZ relocations. All four
sprite edge loops keep the exact positive and negative 16-pixel steps;
signed quotient and byte frame increments remain untouched.
