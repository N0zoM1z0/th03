# TH03 Enemy: speed scaling and clipped movement

The four physical Enemy owners (`eforna`, `efornb`, `eupda`, `eupdb`)
retain the two independent signed divisions of the original velocity
formula; combining them changes rounding. Named numerator and divisor
constants now document both parts. The horizontal and bottom-edge
clipping checks use natural short-circuit C++ while preserving their
original `goto clip` and flag mutation.

`af1167c` links both original TC4 rounds with all 3,325 CODE bytes,
222 ordered native fields, and the full Japanese MAIN image/relocations.
A separate attempt to invert the ENEDAT VM `EO_MOVE` clipped branch
(`af1167b`) changed `efornb` CODE and was rejected. Other VM edge cases,
especially unused loop opcodes, should not be silently repaired.
