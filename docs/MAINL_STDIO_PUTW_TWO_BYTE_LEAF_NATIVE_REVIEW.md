# Original Borland putw two-byte FILE buffer leaf — after473

The original Japanese CL.LIB putw member (slot **274**) is now
fully recovered as maintainable
[8086 source](../src/mainl/crt/putw.asm).
Its complete 125-byte FAR _putw(FILE FAR*) implementation
writes the original 16-bit value in little-endian order
using the actual Borland FILE buffer-level and cursor
fast paths. On each unavailable-buffer path it separately
calls the original FAR __fputc, returning the authentic
-1 EOF/error code if either byte write fails. The high-byte
fallback preserves the compiler's original unaligned
16-bit argument read from [BP+7], not a replacement
by a normalized unsigned-char temporary.

All **125 original CODE bytes** and both logical original
OMF FIXUPPs match at CODE+47 and CODE+101, with the same
symbolic FAR __fputc target, relocation kinds, frame,
widths and addends. The native _TEXT/_DATA/_BSS layout,
BSS-before-DATA GROUP, public name, lone ordered import,
and absent DATA/BSS payload match the original. Borland
and TASM literal FIXUPP packet order is different; full
vendor OBJ record identity is not claimed. No target
CODE-byte array, NOP padding, or post-assembly patches.

After473 independently checks the inherited after472
680-source CRT carrier, then runs two fresh
TASM/TLIB/TLINK native rounds preserving all complete
OBJ/LIB/EXE/MAP output vectors, logs and source hashes.
Both full Japanese decoded MAINL EXE and MAP exactly
equal their original targets (67,372 EXE bytes; 677
ordered MZ relocations). Working CRT now has
**681/893 original source-linked members**, **182,155
original-equal CODE bytes** and 212 contextual vendor
members. This is working-source proof, not full cold
replay or Factory canonical source acceptance.

Focused reviewer: scripts/review_th03_mainl_after473_work.py,
mode stdio-putw-two-byte-leaf;
tests: tests.test_mainl_after473_work.
