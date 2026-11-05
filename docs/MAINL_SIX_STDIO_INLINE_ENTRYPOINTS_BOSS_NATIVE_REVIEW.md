# Original six stdio macro entrypoints — after457

The previously contextual Japanese Borland CL.LIB module iomacro
(index **80**) is recovered as maintainable 8086
[source](../src/mainl/crt/iomacro.asm). It contains **six entire FAR
entrypoints** with their original offsets and caller ABI: getc
(CODE+0), getchar (+51), putchar (+89), putc (+138), feof
(+196) and ferror (+215).

The byte-for-byte 8086 implementation uses the actual Borland 16-bit
FILE level/flags/curp/buffer-segment fields and __streams array,
preserving the getc decrement-fast-path, getchar stdin cursor,
putchar stdout cursor, putc buffer write, both exact __fgetc
and __fputc fallbacks, and the EOF/error bit masks. It does not
substitute high-level stdio calls for the six native interfaces.

The full **234 CODE bytes**, zero DATA/BSS, complete public/ordered
import ABI and original BSS-before-DATA GRPDEF 08ff03ff02 agree.
All **12 original OMF FIXUPPs match literally and in order**, including
the symbolic __streams offsets 0,12,20,32 and genuine far __fgetc
and __fputc call references. No target-byte-array CODE or post-OBJ
patching is used. As usual literal FIXUPP equality is narrower than
raw whole Borland object-record serialization.

The after457 source-bound producer verifies the inherited after456
664-source carrier and performs two new native TASM/TLIB/TLINK rounds.
Both full original Japanese decoded MAINL EXE and MAP match their
target files byte-for-byte (67,372 EXE bytes and 677 ordered MZ
relocations). Raw OBJ/LIB/EXE/MAP pairs, writer logs and source hashes
are preserved. Working CRT **665/893** original source-linked members,
**178,597 source CODE bytes**, **228** contextual vendor members.
This is not a full cold replay or new Factory accepted-source credit.

Focused review: scripts/review_th03_mainl_after457_work.py,
mode stdio-six-inline-entrypoints-boss.
Tests: tests.test_mainl_after457_work.
