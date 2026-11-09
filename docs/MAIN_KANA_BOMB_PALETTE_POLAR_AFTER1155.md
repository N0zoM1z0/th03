# Kana Bomb: circular explosions and byte-timed phase guards

The complete original `b_kana` owner now uses natural zero-remainder tests
for the initial center effect and the four-frame mirrored explosions. The
first pair of polar coordinates initializes at its actual first use; the
second mirrored pair still reassigns the same signed coordinates. The
screen-page check uses byte truthiness without disturbing the MRS caller's
AX contract. The original AL-mediated angular increment and byte `&3`
shake condition remain unchanged.

Two original TC4/TLINK rounds at `af1155b` reproduced all 526 CODE bytes,
53 ordered native fields, one PUBLIC and the complete Japanese MAIN image
and relocations. A separate `af1155c` experiment replaced the screen-page
conditional addition with a ternary expression; the output was different,
so that candidate was restored.
