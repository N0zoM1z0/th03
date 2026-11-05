# Original DOS packed date/time to UTC conversion — after467

Japanese Borland CL.LIB member dostimu (original index **37**) is
maintained in [8086 source](../src/mainl/crt/dostimu.asm).
It is the complete near __DOSTIMETOU converter, not a stub.
The routine interprets the DOS date/time bit packing and year/month
components, handles the original leap-year edge calculation,
uses the actual __monthDay word lookup with -2 addend, computes
the native 32-bit seconds value, adds the timezone offset and
optionally subtracts 3,600 seconds based on the genuine near
__ISDST result. The code preserves the original unchecked range
behavior, operand widths and near callee-pop-four ABI.

All **214 original CODE bytes** and all **five literal ordered
OMF FIXUPPs** match, as do the genuine four imported symbols,
near public name, SEGDEF/GROUP and absence of DATA/BSS.
The first source hypothesis used equivalent but nonoriginal
XCHG operand encodings for CX/AH and TASM selected different
machine bytes at CODE+57 and +134. Reversing those commutative
source operand orders restored the authentic Borland encodings.
A separate original fixup check established that the
__monthDay lookup at CODE+73 requires the true **TARGET-frame
method 5** with addend 65534, rather than a DGROUP-framed
reference. The source was corrected before native integration.
The native near __ISDST call at CODE+184 also retains original
CODE-frame method 0. No original executable-byte fixtures,
padding, or object postprocessing were used.

After467 validates the retained after466 674-source carrier and
performs two fresh native TASM/TLIB/TLINK rounds, preserving
raw OBJ/LIB/EXE/MAP outputs, writer logs and source hashes.
Both full Japanese decoded MAINL EXE and MAP match the original
(67,372 EXE bytes and 677 ordered MZ relocations).
Working CRT: **675/893** source-linked original members,
**181,074 CODE bytes**, 218 contextual vendor members.
This remains scoped source-build evidence, not full cold replay
or Factory formal accepted-source credit.

Focused reviewer: scripts/review_th03_mainl_after467_work.py
(mode dos-packed-time-to-utc-dst-boss).
Tests: tests.test_mainl_after467_work.
