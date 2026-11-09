# Round results: native object reset and 32-bit bonus ownership

The full `results` object contains two physical reset traversals and the
entire match-result display and bonus accumulation. Shotpair flags and the
combined Enemy/Fireball carrier now use natural bounded `for` loops with
the same signed index and near pointer updates after their stores. The
winner's player record and the 32-bit bonus calculation value initialize
at their actual first use inside the result-display phase.

The original TC4/TLINK stage `af1164e` reproduced all 1,060 CODE bytes,
89 ordered native fields, three PUBLICs, and the Japanese MAIN loaded
image and ordered relocations twice. A `for` index experiment `af1164b`
failed compilation because TC4 retained both declarations in the same
function scope; the two loops must share the original signed `i`.

The signed 32-bit bonus cap and final `score_add` sequence remain unchanged.
They should be independently verified before more aggressive arithmetic
simplification.
