# Frame delay: native volatile VSYNC wait

The original `frmdely1` physical owner can express its interrupt-driven wait
as an explicit counter reset followed by a natural `while` loop. The counter
remains volatile and unsigned 16-bit; the signed 16-bit duration parameter
and original comparison order are preserved. No sleep, timeout, input poll,
or second counter reset was added.

Original TC4/TLINK stage `af1179a` matches all 21 CODE bytes, two ordered
native fields, the PUBLIC and complete Japanese MAIN image/relocations in
two independent rounds. Previous operand-reversal and forced-signed counter
variants do not preserve this original instruction stream.
