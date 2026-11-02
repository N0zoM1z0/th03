# Exact natural Borland DOS ftime and 57-source Japanese MAINL

The DOS large-model far-cdecl ftime wrapper, original CRT member234,
has exact maintained high-level source in src/mainl/crt/ftime.cpp.
It forwards the original caller-supplied far time buffer to the real
far __ftime provider without introducing any stack locals, return-value
conversion, modern behavior or new error handling.

Real Borland C++ 4.5 produces **all 22 original CODE bytes**,
the original far _ftime public at0, single original TARGET-framed
four-byte far __ftime call FIXUPP at CODE+12, correct EXTDEF
name/index and original empty DATA/BSS group 08ff02ff03.
The C source prototype uses the original single-underscore C
declaration _ftime, which the compiler correctly exports as the
double-underscore __ftime import. An initially plausible
double-underscore C prototype emitted a triple-underscore
external name despite equal CODE; corrected source and actual
native OMF metadata are now fully original-identical.

The original 893-member CRT has **57 simultaneous source units**
after adding this independently reconstructed module alongside
the natural Pascal tmpnam and the exact chdir/unlink sources
plus the 53-source original time/FILE/path/scanner/xx carrier.
**836 other original CRT program records remain unchanged**.
Two native BCC/TASM/TLIB/TLINK rounds independently reproduce
the complete **67,372-byte Japanese decoded MAINL EXE and
original MAP byte-for-byte**, with all **677 MZ relocations**.
Joint working-source CODE reaches **27,467 original bytes**.

Existing fopen, fclose, _timecvt, strftime and tempnam original OMF
metadata differences remain OPEN in those separate modules. The
accepted28-provider CRT, formally published211-owner MAINL
ledger, pinned candidate-local-attested Japanese target and
original cold pair are unchanged; no full cold replay or DIET
packing, and no new formal accepted credit.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_posttempnam_work.py dirs-tmpnam-ftime
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttempnam_work.py dirs-tmpnam-ftime
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_posttempnam_work

The two complete native OBJ/LIB/EXE/MAP vectors and actual compiler
phase logs are retained at .analysis/work/posttempnam-dirs-tmpnam-ftime-*.
