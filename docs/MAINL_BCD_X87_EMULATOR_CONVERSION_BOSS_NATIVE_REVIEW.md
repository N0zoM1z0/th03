# Complete original BCD/x87 emulation conversion boss — after460

The original Japanese Borland CL.LIB bcd1 member (slot **195**)
is now recovered as maintained natural
[8086 + x87 source](../src/mainl/crt/bcd1.asm). This had previously
been blocked by unfamiliar FIDRQQ/FIERQQ/FIWRQQ OMF emulation fields.
Independent experiments established that **TASM 5 EMUL**, not the
invalid EMULATOR directive, is the correct native source directive.
EMUL automatically declares the original three emulator externals,
and actual x87 instructions generate the authentic target-relocation
fields and word addends without a manually fabricated OMF record.
The original fwait instructions use the real FIWRQQ emulation
sequence; no native CODE byte array, padding, or binary patching.

The module contains the 89-byte private near exponent power helper,
then four original FAR exports: __BCD_TOBINARY (CODE+89),
__BCD_TODECIMAL (+145), __BCD_LOG10 (+264) and __BCD_POW10 (+305).
The actual FILD/FLD/FMULP/FDIVP/FISTP arithmetic, signed/special
BCD class branches, original INT 3Eh floating shortcut, flags
and stack cleanup remain real 16-bit source instructions.

Original **398 CODE and 140 initialized DATA bytes** are exactly
reproduced. DATA has eight 32-bit integer powers (0..31), ten real
80-bit x87 extended powers of ten (32..131), and two genuine IEEE
single-precision infinity/quiet-NaN constants (132..139).
Comparative TASM experiments established that its decimal DT
conversion rounds some large powers differently from Borland.
The source therefore preserves the **actual 64-bit x87
significands and biased exponent words** as typed DQ/DW
constants with semantic 10^(8*2^n) comments; these are meaningful
original mathematical DATA, not executable target-byte fixtures.

All **23 original logical OMF FIXUPPs** match at full original
site, width, frame, target and addend, including target FIDRQQ at
CODE+40, FIERQQ at +97, FIWRQQ at +256 and +297, and the real
integer/extended-power DATA references at +38 and +48.
The native first attempt exposed an original BSS-before-DATA
GROUP 08ff03ff02 mismatch; source membership was corrected
before native acceptance. Original TASM/Borland literal FIXUPP
packet chronology and full raw OMF program serialization
remain different, and are not misreported as equal.

After460 validates the unchanged after459 667-source carrier,
then performs **two fresh TASM/TLIB/TLINK rounds**, retaining
actual raw OBJ/LIB/EXE/MAP outputs, source hashes and logs.
Both complete decoded Japanese MAINL EXE/MAP match the original
targets byte-for-byte (67,372-byte EXE, 677 ordered MZ
relocations). The working CRT reaches **668/893** original
source-built members, **179,416 CODE bytes**, with 225 contextual
vendor members. No full cold replay or Factory accepted-source
credit is implied.

Focused reviewer: scripts/review_th03_mainl_after460_work.py,
mode bcd-x87-emulation-conversion-boss;
tests: tests.test_mainl_after460_work.
