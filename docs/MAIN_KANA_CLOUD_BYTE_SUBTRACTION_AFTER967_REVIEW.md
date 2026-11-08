# TH03 MAIN Kana cloud attack: byte subtraction and TC4 immediate selection

The cloud-angle subtraction remains the one explicit SUB AL,10h instruction
in the full Kana BOSS. Fresh source trials confirm why the earlier
"equivalent C++ subtraction" note was not just an optimizer quirk that could
be removed by spelling the same expression differently.

The original full-object bytes at the cloud call are:

    9A 00 00 00 00    far call randring_far_next16_and
    2C 10             sub al, 10h
    88 46 FF          mov [bp-1], al

The new af967a trial replaced the inline instruction with:

    _AL = randring_far_next16_and(0x1F);
    _AL -= 0x10;

Turbo C++ emitted ADD AL,F0 instead:

    9A 00 00 00 00    far call randring_far_next16_and
    04 F0             add al, 0F0h
    88 46 FF          mov [bp-1], al

The two arithmetic operations are equivalent modulo 256, but the original
machine-code bytes are not. af967b also tried assigning the function result
to the signed-byte local before subtracting; TC4 added an extra local store
and still selected ADD AL,F0. af968b tried a register-local signed byte;
the complete physical object still differed. The earlier af836c direct
expression has the same ADD AL,F0 substitution.

The explicit assembler instruction therefore remains. This is not an
unexplored "C++ equivalent" gap: the compiler's immediate selection has
been measured at the original instruction boundary and against the entire
BOSS object.

The current maintained Kana source remains the source-current af966a
version: two original TC4 rounds reproduce all **1,874 CODE bytes, 274
literal ordered OMF FIXUPPs and nine PUBLICs**, plus the complete normal
Japanese MAIN image and all 1,553 MZ relocations. See
MAIN_KANA_BOSS_NATURAL_TEMPLATE_LEVEL_AND_RENDER_AFTER966_REVIEW.md.
