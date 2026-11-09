# Warning/Gauge HUD: exact native pause and flash control

The complete `warning` physical owner now uses natural `while` loops for
both key-release polls and the pause/quit command loop, preserving each
original keyboard sense and VSync delay. Four word-frame gauge flashing
predicates use natural remainder truthiness. The 27-frame palette flash
scopes its register index to the `for` header; warning text clearing uses
prefix advancement for both signed row and attribute. The warning flag's
explicitly widened byte parity comparison is also naturally truthy.

Two original TC4/TLINK rounds at `af1160e` matched all 1,560 CODE bytes,
125 ordered native fields, seven PUBLICs and the Japanese MAIN image plus
ordered relocations. Hardware GRCG and far-return assembly entry sequences
remain unchanged; the warning completion still executes the first active
Gauge update during the same call.
