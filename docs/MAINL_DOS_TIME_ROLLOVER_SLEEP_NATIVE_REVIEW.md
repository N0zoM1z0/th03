# Original DOS sleep and real gettime polling — after510

Original Japanese Borland CL.LIB member sleep (slot 366) is now
maintained as [8086 source](../src/mainl/crt/sleep.asm).
Its complete FAR _sleep reads the original four-byte DOS clock
through _gettime, preserves the original word-sized argument,
waits for actual changes of the time field rather than using
host sleep, accounts for the original 5Ah seconds clamp
and final elapsed-time bound, and preserves the original
16-bit stack/register ABI.

All **109 original CODE bytes**, the sole FAR public,
single ordered FAR _gettime import, original empty DATA/BSS
and GROUP match Japanese CL.LIB. All three logical OMF
FIXUPPs match original site, kind, width, frame, target
and addend: CODE+14/+55/+87 all call _gettime.
Borland/TASM literal FIXUPP chronology differs, so
full raw OBJ identity is not claimed. There are no
target byte arrays, filler or object modifications.

After510 verifies the unchanged after509 717-source carrier,
then performs two fresh TASM/TLIB/TLINK native rounds.
Both full Japanese decoded MAINL EXE/MAP are original-equal
(67,372 EXE bytes and 677 ordered MZ relocations). All
raw OBJ/LIB/EXE/MAP vector outputs, logs and source
hashes are retained. Working CRT reaches **718/893**
complete source-linked original members, **187,626 CODE
bytes**, with 175 contextual vendor members.
No full cold replay or Factory accepted-source credit.

Reviewer: scripts/review_th03_mainl_after510_work.py,
mode original-dos-time-rollover-sleep-leaf.
Tests: tests.test_mainl_after510_work.
