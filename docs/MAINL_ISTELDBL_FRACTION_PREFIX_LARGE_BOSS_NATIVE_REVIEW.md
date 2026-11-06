# Large isteldbl long-double parser: first 754 original bytes reconstructed

**Historical partial, superseded by [complete after521 source/link proof](MAINL_ISTELDBL_FULL_SOURCE_LINK_AFTER521_NATIVE_REVIEW.md).**
The retained partial and its verifier remain unchanged.

Original Japanese Borland CL.LIB member isteldbl (slot 765) is a
**1,947-byte CODE** large Boss that parses 80-bit long-double values
from a real streambuf. The maintained
[partial native x87 source](../src/mainl/crt/isteldbl_fraction_prefix_partial.asm)
now extends the preceding 460-byte integer-prefix work through
**original CODE+0..753 (754 bytes)**. This adds the full decimal-point
and fractional-digit loops, including the same native streambuf
buffer read/virtual refill/snextc paths, real ctype digit table
checks, repeated x87 multiply-by-10 plus signed digit addition,
and the original 32-bit decremented fractional-exponent count.

**Exactness is deliberately bounded**: 752 of the 754 emitted
native CODE bytes equal original CL.LIB. The only exclusions remain
CODE+30/+31, the initial near jump's displacement to the not-yet-
recovered original parser exit at CODE+0x78F. The source binds this
as a genuinely unresolved near symbol, so TASM emits a symbolic
relocation with zero placeholder bytes. We do not fabricate this
displacement or fill in the omitted parser logic; this partial
OBJ is not used to link MAINL.

All **27 original OMF symbolic fields** in this prefix match
source locations, imported names, segment targets, widths and
addends. The 28th native relocation is specifically the
deliberately unresolved initial jump. Fifteen original Borland
x87 frame-method-4 references compile with TASM frame 5 and
are disclosed. The original DATA+0..3 typed 10.0f constant is
source-equal; the remaining ten original DATA bytes and
CODE+754..1946 have not been reconstructed here.

A useful source-level correction was discovered by comparing
the completed second digit loop: the backward near jump at
original CODE+751 targets the fractional digit arithmetic at
CODE+0x254, *not* the preceding digit-present flag at +0x24F.
Changing that natural target symbol corrected the final
original operand byte without inserting executable fixtures.

The [scoped verifier](../scripts/probe_th03_isteldbl_fraction_prefix_partial.py)
runs two independent native TASM rounds under the writer lock,
checks each of 752 original-equal CODE bytes, the two explicitly
unresolved operands, all 27 original symbolic fixups,
FPU metadata differences and nonvolatile native OMF stability.
Tests: tests.test_isteldbl_fraction_prefix_partial_native.

**Unfinished:** 1,193 CODE bytes including signed exponent
parsing, normalization, exception/errno paths and function return.
This remains a *partial* Boss, earns **zero complete CRT member
or formal Factory accepted units**, and is not a full MAINL link
or cold replay.
