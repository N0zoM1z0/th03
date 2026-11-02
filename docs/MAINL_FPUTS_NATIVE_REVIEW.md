# Natural Borland fputs: original 85 CODE and complete mixed near/far ABI

The original DOS Borland C++ 4.5 large-model far-cdecl fputs,
CRT member228, is now naturally reconstructed as a maintained
high-level C++ source in src/mainl/crt/fputs.cpp, rather than
an inline opcode array or a prepatched object.

The genuine original code checks the far string pointer,
computes its byte length through far strlen, and calls the
near Pascal __FPUTN multi-byte FILE writer. A zero-length
string returns0; successful output returns the original last
unsigned string character; unsuccessful output returns EOF.
The original FPUTN is *near Pascal*, with caller arguments
pushed in the original left-to-right order and callee cleanup.
That distinction matters to its original 16-bit ABI.

In actual Borland compiler trials, seven initial C++ control-flow
forms produced 87-94 CODE bytes rather than the historical85.
We independently examined the generated 16-bit instruction
streams and varied the treatment of the far source pointer,
the last-character expression, and nested returns. The exact
original result uses an assignment inside the zero-length
branch followed by a successful-output branch, and
(unsigned char)*(s+length-1) semantics (spelled with correct
unsigned in the product source). This causes the real BCC
optimizer to emit LES BX,[BP+6], ADD BX,[BP-2] and
MOV AL,ES:[BX-1], instead of loading/adjusting a separate
index register before the far memory access.

The C declaration ordering also matters: the genuine original
EXTDEF order is __FPUTN followed by _strlen. Borland's Pascal
linkage name is written __FPUTN explicitly in the source.
Multiple real BCC4.5 variants with this declaration order
and the successful-output control-flow expression produced
**85/85 original CODE bytes** and **both original ordered
OMF FIXUPPs literally**: a TARGET-framed 2-byte near
__FPUTN at CODE+56, and a TARGET-framed 4-byte far
_strlen at CODE+23. The original one public far _fputs,
zero DATA/BSS, group 08ff02ff03 and all imports agree.
No return-value stub or binary relocation rewrite is used.

The scoped BCC/TLIB/TLINK builder reuses the previously
proved 50-source original CRT with its initialized perror
strings, far strlwr and 820-byte time converter, complete
xx, two qsort bosses, scanners, FILE streams and DOS directory
subsystem. Only fputs is compiled twice at original CRT slot228;
the other **842 original library member program records**
remain byte-identical. Both real BCC/TLIB/TLINK rounds
produce the entire **67,372-byte decoded Japanese MAINL EXE
and its original MAP bit-for-bit** with all677 ordered MZ
relocations. The 51 original source modules jointly supply
**25,715 exact CODE bytes**.

The previous timecvt near-TARGET-frame, fopen writer order
and fclose near-frame OMF discrepancies remain open in the
other modules; this fputs source OBJ itself is native-original.
The accepted28-provider CRT, formal211-owner MAINL ledger,
fixed candidate-local-attested original Japanese target and
cold pair remain unchanged. Source-only working exactness
does not automatically confer new ledger accepted credit,
and no full cold/DIET replay was performed.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_fputs_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_fputs_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_fputs_work

Retained complete repeated original BCC OBJ/TLIB CRT/EXE/MAP
raw vectors and writer logs are under .analysis/work/fputs-*,
with bound mainl-fputs-native-{build,review}.json receipts.
