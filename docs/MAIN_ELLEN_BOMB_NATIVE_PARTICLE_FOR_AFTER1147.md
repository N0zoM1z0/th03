# Ellen Bomb: complete native eight-particle controller

The original `b_ellen` physical owner now expresses its eight-slot initial
fill, full motion/clip/respawn controller and two-sentinel sprite renderer
using bounded natural `for` loops. The real `goto respawn` remains: it joins
the same original per-particle initialization and final pointer/index
advance as the ordinary clipping path. All skipped particles and both
separate sentinel comparisons now use the common for-header progression.
The color-flash parity uses natural unsigned-word remainder truthiness;
byte frame and hardware/BX operations are unchanged.

Original TC4/TLINK `af1147c` reproduces all 1,023 CODE bytes, 116 ordered
native fields, three PUBLICs and full Japanese MAIN image/relocations twice.
A separate `af1147b` attempt declared independent signed indices inside
both update for headers, changing the original compiler output; the shared
function-wide index therefore remains.
