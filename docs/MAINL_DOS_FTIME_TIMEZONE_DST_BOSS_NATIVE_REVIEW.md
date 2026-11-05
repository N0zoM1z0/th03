# Complete DOS ftime, timezone and DST boss — after463

The original Japanese Borland member _ftime (CL.LIB index **183**)
is now real [8086 source](../src/mainl/crt/_ftime.asm).
It contains two private FAR DOS date/time helpers at CODE+0/+23
using the original INT 21h services 2Ah and 2Ch, plus the public
__ftime FAR routine at CODE+46. The full routine obtains the
local time/date, refreshes the day at the native midnight boundary,
adjusts the timezone in minutes via N_LDIV@, tests the original
daylight and __ISDST logic, converts DOS time to Unix seconds through
_dostounix and returns the native 10-millisecond field.

The entire **235 original CODE bytes**, segment definitions and
all seven relocation sites/targets/widths/addends match. The
private FAR routines are called through explicit PUSH CS followed
by a same-CODE **NEAR** call: initially naming them as FAR TASM
procedures inserted an extra PUSH CS per call, producing the
wrong source. The revised source specifies CALL NEAR PTR after
the original manual PUSH CS, yielding the original instructions,
branch offsets, and ABI without any padding or patching.

Five of seven original logical OMF FIXUPPs match completely.
The two imported NEAR calls to N_LDIV@ at CODE+119 and __ISDST
at +159 use Borland TARGET-frame method 5; TASM's equivalent
same-CODE NEAR calls use CODE segment-frame method 0. The
builder allows only these two exact site/import/width/addend pairs
and checks all other fields strictly. Literal Borland FIXUPP
chronology and complete raw OBJ identity are not claimed.

After463 verifies the retained after462 670-source parent, then
runs two fresh TASM/TLIB/TLINK native rounds preserving raw
OBJ/LIB/EXE/MAP, source hashes and writer logs. Both complete
Japanese decoded MAINL EXE and MAP match the original targets
byte-for-byte, preserving 67,372 EXE bytes and 677 ordered MZ
relocations. Working CRT now **671/893** source-linked members,
**180,230 original-equal CODE bytes**, 222 contextual vendor members.
This is not Factory formal acceptance or a full cold replay.

Focused reviewer: scripts/review_th03_mainl_after463_work.py
(mode dos-ftime-timezone-dst-boss);
tests: tests.test_mainl_after463_work.
