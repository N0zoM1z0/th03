# Complete original ostream FAR pointer insertion and ios flags — after504

Japanese Borland CL.LIB ostptr (slot 819) is recovered
as [maintained 8086 source](../src/mainl/crt/ostptr.asm).
This is the complete 135-byte FAR ostream::operator<<(void FAR*)
function. It saves the original stream ios flags, prepares
the real basefield/adjustfield masks with pointer-specific
formatting, calls the genuine far ios::setf, updates native
ios fill/width state, forwards the FAR pointer through the
original ulong ostream insertion operator, then invokes
the real ios::flags to restore the previous formatting.
The precise Borland 32-bit flag and FAR this/object ABI
is retained without host-side formatting substitutes.

All **135 original CODE bytes**, the sole public FAR
entry, five real imports, empty DATA/BSS and DATA-first
GROUP match the Japanese CL.LIB member. All **seven
logical original OMF FIXUPPs** match original segment,
site, target symbol, kind, width, frame and addend.
They include basefield high/low at +30/+33,
adjustfield low/high at +37/+44, ios::setf at +63,
ostream ulong insertion at +98, and flags restoration
at +116. Native TASM and Borland order those FIXUPP
records differently, so literal raw vendor OBJ identity
is not claimed. The source includes no target byte arrays
or post-assembly object modifications.

After504 verifies the unchanged after503 711-source
CRT parent and creates two fresh TASM/TLIB/TLINK
native output rounds, preserving all raw OBJ/LIB/EXE/MAP
artifacts, writer logs and source hashes. Both complete
decoded Japanese MAINL EXE and MAP are original-equal
(67,372 EXE bytes and 677 ordered MZ relocations).
Working CRT: **712/893** original source-linked members,
**186,946 source CODE bytes** and 181 remaining contextual
vendor members. No cold replay or formal Factory
accepted-source credit is implied.

Focused reviewer: scripts/review_th03_mainl_after504_work.py
(mode ostream-pointer-format-flags-boss).
Tests: tests.test_mainl_after504_work.
