# Stage and round setup: native player and resource initialization

The full `entry` physical owner now advances both real player pointers
with natural prefix increments in the stage and round initializers. Demo
and transition state checks use natural byte truthiness. The full
per-player Extra Attack reset derives its sixteen-slot bound from the
actual `exatt_entities` array type. The separate CPU safety index cap and
per-player charge thresholds now have named constants; the original
`IRand()` call and the two-stage bit shift remain in their original order.

Original two-round TC4/TLINK stage `af1171d` matches all 3,050 CODE
bytes, 433 ordered native fields and the entire Japanese MAIN image and
relocations. An `af1171b` attempt to replace the stage-result waiting
`if`/`else` with a ternary assignment changed CODE; that branch is kept.
