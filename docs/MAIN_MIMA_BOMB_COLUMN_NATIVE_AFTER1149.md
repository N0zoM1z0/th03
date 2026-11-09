# Mima Bomb: native column traversal and byte-cadence boundaries

The complete Mima Bomb owner retains its eight physical columns and
first-uninitialized-column render termination. The renderer now advances
its near pointer with prefix `++`, and the column-spawn cadence and explosion
color byte use natural zero-remainder / zero-value guards. The update's
signed column index, hardware BX fill, palette sequence, and sound calls stay
in their original order.

Original TC4/TLINK stage `af1149e` matched the complete 833 CODE bytes, 93
ordered native fields, and the Japanese MAIN image/relocations twice. A
separate `af1149d` experiment tried simplifying the explicitly widened
unsigned parity test to `!remainder`; the compiler emitted different code.
The original parity comparison therefore remains.
