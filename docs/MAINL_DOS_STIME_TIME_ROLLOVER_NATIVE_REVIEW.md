# Complete original DOS stime/time with date-rollover retry — after491

Japanese Borland CL.LIB member stime (original slot **121**) has
been recovered as maintained [8086 source](../src/mainl/crt/stime.asm).
It contains two complete FAR APIs: _stime at CODE+0
and _time at CODE+64.

The real _stime takes a caller-supplied FAR Unix timestamp,
calls the genuine _unixtodos with original far date/time
buffer pointers and passes both results to the actual
_setdate and _settime DOS wrappers. The real _time does
not simply call the host clock: it reads DOS date/time/date,
compares the original two date samples, and **retries when
the day changed between calls**. It converts the consistent
pair with the genuine _dostounix, optionally writes the
32-bit result to the caller's FAR pointer, and returns the
same DX:AX value. All stack and 16-bit FAR ABI details
remain unchanged.

The complete **170 original CODE bytes**, two public offsets,
original group/segment layout and six ordered FAR imports match.
All seven original OMF relocation sites/widths/frames/targets
and addends match the two fresh TASM outputs, including
CODE+29/+39/+49 for the setter and +78/+88/+98/+124 for
the getter. The Borland and TASM literal FIXUPP record
chronology still differs, so original raw OBJ record equality
is not claimed. There are no original executable-byte
fixtures, padding instructions or post-assembly patches.

After491 independently checks its inherited after490
698-source carrier and performs two real TASM/TLIB/TLINK
rounds, retaining the complete OBJ/LIB/EXE/MAP outputs,
logs and source/driver hashes. Both full decoded Japanese
MAINL EXE and MAP match their pinned originals byte-for-byte
(67,372 EXE bytes, 677 ordered MZ relocations). The
working CRT now has **699/893** source-linked original
members, **185,165 CODE bytes**, and 194 contextual
vendor members. No full cold replay or formal Factory
accepted-source credit is claimed.

Focused reviewer: scripts/review_th03_mainl_after491_work.py
(mode dos-settime-gettime-rollover-boss).
Tests: tests.test_mainl_after491_work.
