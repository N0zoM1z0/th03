# DOS strrev: exact 52-byte far in-place reversal source

The maintained src/mainl/crt/strrev.asm recovers all **52 bytes**
of original Borland DOS large-model far-cdecl _strrev at CRT
member309. It temporarily loads DS from the far input pointer,
mirrors that segment in ES, locates the NUL terminator using
forward REPNE SCASB and reverses original characters with
two cursor registers and XCHG/STOSB. It preserves DS, SI, DI,
the original pointer ABI and the far return in DX:AX.

Original native TASM CODE, one public _strrev at0, empty DATA/BSS,
zero imports/fixups and literal BSS-before-DATA GRPDEF 08ff03ff02
all match the fixed original. During genuine native compilation
the equivalent XCHG DI,SI expression emitted a different ModR/M
byte. Using the original XCHG SI,DI restores the exact opcode
without inserting alignment bytes or patching any object.

This real source is inserted at its original native library
slot309 with the previous25 exact source owners, including
the full exception/RTTI xx, two qsort sorting algorithms,
the large scanner and the 322-byte path search. All
**867 other original member program records** remain unchanged.
Two native TASM/TLIB/TLINK rounds reproduce the **complete
67,372-byte decoded Japanese MAINL EXE**, its original MAP
and all **677 MZ relocations** byte-for-byte. Twenty-six
simultaneous source members now generate **18,219 original
CODE bytes**.

The pinned Japanese target, accepted28-provider library and
published211-owner MAINL accepted ledger remain frozen.
Source-only working exactness is not automatic formal accepted
credit. No full cold replay or DIET repack was executed.

Affected-only validation:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_postscanner_work.py strrchr-srchstr-strrev
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_postscanner_work.py strrchr-srchstr-strrev
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_postscanner_work

Complete native raw TASM OBJ, TLIB source CRT, EXE/MAP vectors,
source-bound receipts and phase logs are retained in .analysis/work.
