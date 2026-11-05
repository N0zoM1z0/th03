# Original bidirectional Shift-JIS multibyte conversion boss — after459

The original Japanese Borland CL.LIB member MBTOMB (index **638**)
is now fully recovered as natural [8086 source](../src/mainl/crt/MBTOMB.asm).
It contains two complete FAR conversion functions: __mbbtombc
(CODE+0) converts printable ASCII/halfwidth Katakana bytes to
fullwidth Shift-JIS; __mbctombb (CODE+59) converts back, preserving
the native hiragana adjustments, invalid-code fallthrough, direct
ASCII reverse search and exceptional punctuation fallbacks.

The associated **432 initialized DATA bytes** are not unexplained
padding or target executable byte arrays: they are five separately
named and semantically typed tables, recovered from the original
Japanese character encoding:
- 95 Shift-JIS words for ASCII 20h..7Eh (190 bytes);
- 64 Shift-JIS words for halfwidth A0h..DFh (128 bytes);
- 87 halfwidth reverse-code bytes for 8340h..8396h;
- 9 special fullwidth punctuation words (18 bytes);
- 9 corresponding special single-byte symbols (9 bytes).

All **207 original CODE** and **432 DATA** bytes match. One disassembly
hypothesis initially skipped the required AH clearing after a
special-symbol lookup; the native CODE comparison detected the
single wrong branch displacement at CODE+192 and the source label
was corrected to follow the true original zero-high-byte path.
DATA labels were also expressed as TASM word/byte labels, rather
than CODE-style colon labels; no target machine CODE arrays, NOP
padding or object patching were used.

Original _TEXT/_DATA/_BSS, DATA-first GROUP 08ff02ff03,
both publics, zero imports and **all six logical OMF relocation
sites/targets/frames/addends** are exact. They point to the typed
tables at DATA+0, +190, +318, +405 and +423.
The original Borland vs TASM *literal FIXUPP chronology* differs
and raw original OBJ-program equality is not claimed.

After459 verifies the retained after458 666-source carrier, then
produces two fresh native TASM/TLIB/TLINK rounds with complete
raw OBJ/LIB/EXE/MAP output pairs, logs and source hashes.
Both complete decoded Japanese MAINL EXE/MAP are target-equal
(67,372 EXE bytes, 677 ordered MZ relocations). The working CRT
now has **667/893 source-linked original members**, **179,018
source-built original-equal CODE bytes**, with 226 contextual
vendor programs remaining. These are scoped working-source
results, not new formal Factory acceptance or a full cold replay.

Focused reviewer: scripts/review_th03_mainl_after459_work.py
(mode mbcs-fullwidth-mapping-boss); tests:
tests.test_mainl_after459_work.
