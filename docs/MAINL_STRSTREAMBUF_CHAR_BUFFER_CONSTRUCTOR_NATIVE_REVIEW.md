# Complete char-pointer strstreambuf constructor — after450

The original Japanese Borland `CL.LIB` member `srbctr6` (slot 839)
provides `@strstreambuf@$bctr$qncit1` and is now maintained in
[src/mainl/crt/srbctr6.asm](../src/mainl/crt/srbctr6.asm).
A new live original member comparison with both `srbctr4` and `srbctr5`
confirmed its 239 CODE / 52 DATA payload, original 16-symbol import
ABI and 20 full logical OMF FIXUPPs before using sibling source as
an independent assembly candidate. All recovered original bytes,
relocation targets and sites were then checked against this member,
not merely against the previously recovered sibling.

The complete 50-byte object constructor optionally allocates `this`,
constructs the actual `streambuf` base, assigns the true class virtual
table, forwards the original far buffer and size arguments into
`strstreambuf::init`, and increments the original destructor counter.
CODE+107/+179 contain genuine typed `strstreambuf`/`streambuf` RTTI,
with all 11 symbolic virtual slots preserved in DATA+8..48.
The original logical CODE+50 -> DATA+8 and DATA+0 -> CODE+107
OMF relocation targets match, as do all 18 other fields. TASM and
Borland literal FIXUPP order differs; raw OMF identity is not claimed.

After450 validates its unchanged after449 parent and performs two
fresh TASM/TLIB/TLINK rounds. Both full decoded Japanese MAINL EXE
and MAP match their targets, including the 67,372-byte executable
and all 677 ordered MZ relocations. The working CRT has **658/893**
source-linked original members, **177,083 CODE bytes** and 235
contextual vendor members. This is not whole-product source
acceptance or a full cold replay.

Focused check: scripts/review_th03_mainl_after450_work.py
(strstreambuf-char-far-buffer-constructor-boss) and
tests.test_mainl_after450_work.
