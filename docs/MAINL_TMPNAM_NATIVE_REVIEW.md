# Natural Borland DOS tmpnam: exact 23-byte source and 56-source MAINL

The original far-cdecl DOS CRT tmpnam wrapper (member323) is
reconstructed naturally in src/mainl/crt/tmpnam.cpp. It calls the
real near Pascal __TMPNAM with the caller's far destination and
the far DS:offset address of the original __tmpnum global counter.
Both Borland's unusual near Pascal callee-cleanup stack order
and far DX:AX return convention are preserved.

Real Borland C++ 4.5 compiles the high-level source to **all 23
original CODE bytes**, one original PUBLIC _tmpnam at0, exact
EXTDEF sequence __TMPNAM then __tmpnum, DATA-before-BSS group
08ff02ff03 and **both original literal ordered OMF fields**:
a TARGET-framed near __TMPNAM call at CODE+17 and a
GROUP-framed __tmpnum offset at CODE+13. This result required
the actual two-underscore imported name and intentional
declaration ordering. Earlier plausible naming emitted the
same CODE but incorrect import names and indexes; the current
source is full original OMF, not just byte-equivalent.

The scoped builder adds this independent original CRT member
after the previously verified chdir/unlink pair, producing
**56 maintained native source members** and preserving all
**837 other original vendor member program records**. Two
actual BCC/TASM/TLIB/TLINK rounds independently reconstruct
the complete **67,372-byte Japanese decoded MAINL EXE and
original MAP byte-for-byte**, with **677 original MZ relocations**.
The working source CODE extent now reaches **27,445 original
bytes**. The same original library also retains large
strftime, timecvt, tempnam, exception handling, qsort and
file/path native source modules.

Prior original metadata gaps in the separate fopen, fclose,
timecvt, strftime and tempnam members remain explicitly OPEN.
The accepted28-provider CRT, formal211-owner MAINL ledger,
candidate-local-attested Japanese target and original cold pair
are unchanged. No new formal accepted credit or full cold replay.

Affected-only validation:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_posttempnam_work.py dirs-tmpnam
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttempnam_work.py dirs-tmpnam
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_posttempnam_work

Complete native two-round OBJ/LIB/EXE/MAP vectors, source-bound receipts
and real Borland writer logs are retained under
.analysis/work/posttempnam-dirs-tmpnam-*.
