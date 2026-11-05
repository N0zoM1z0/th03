# Complete original multibyte string tokenizer — after455

Original Japanese Borland `CL.LIB` member `MBSTOK` (index **633**)
is now recovered in maintained
[8086 source](../src/mainl/crt/MBSTOK.asm). Original source library
inspection independently established that its 230-byte CODE and
all 12 ordered logical OMF relocation sites are byte-/field-equivalent
to the distinct `FMBSTOK` member previously recovered as after454,
while its public `__mbstok` and near-string helper imports are
separately named. This is an independently checked original member,
not just a second filename assumed to represent the same code.

The complete FAR ABI implementation maintains its own persistent
four-byte DATA cursor, optionally resumes from that prior far pointer,
uses the original `__mbsspnp` and `__mbspbrk` helpers, honors the
`__mbctype` DBCS lead-byte classification and NUL-terminates the
selected token with the same offset-only arithmetic. All **230
CODE / 4 DATA bytes** and the true `_TEXT`/`_DATA`/`_BSS` layout,
DATA-first GROUP `08ff02ff03`, public/ordered imports and the **12
logical original OMF FIXUPPs** match. The literal Borland/TASM
FIXUPP chronology differs; full vendor OBJ record identity is not
claimed.

A generator mistake initially marked the native CODE segment
`_TEXTA` rather than the original `_TEXT`. The complete original
library and retained vendor OBJ were inspected independently;
correcting the source-bound builder's expected segment layout
resolved the strict failure. No native exception was introduced.

After455 validates the unchanged after454 parent and executes two
fresh native TASM/TLIB/TLINK rounds with full raw OBJ/LIB/EXE/MAP
pairs, logs and source hashes. Both Japanese decoded MAINL EXE/MAP
are byte-for-byte original-equal (67,372-byte EXE, 677 ordered
MZ relocations). The working CRT now covers **663/893** original
source-linked members, **178,132 CODE bytes** and 230 contextual
vendor members. No full cold replay or new Factory source-acceptance
credit is implied.

Focused reviewer: scripts/review_th03_mainl_after455_work.py
(mode multibyte-strtok-state-machine);
tests: tests.test_mainl_after455_work.
