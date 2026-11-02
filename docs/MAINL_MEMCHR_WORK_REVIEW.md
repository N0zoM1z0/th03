# Original DOS memchr and cumulative four-member native MAINL CRT

A new maintained src/mainl/crt/memchr.asm restores the original Japanese DOS
large-model far-cdecl memchr at original CRT member index259. The real TASM
output reproduces **all37 original CODE bytes**, with exactly one public
_memchr entry, zero literal OMF fields and no imports. The original and
source objects have three matching segment extents (CODE37/DATA0/BSS0)
and the original BSS-before-DATA GRPDEF, literally 08ff03ff02.
The implementation uses original CLD / REPNE SCASB, tests the count before
loading the comparison byte, and returns either the first matching far
pointer or the original 0000:0000 not-found pointer. SI/DI and the original
far cdecl register/stack return ABI are retained. This is natural source,
not a CODE-byte array, patched object or artificial padding.

The cumulative builder inherits the already verified exact three-source
memcpy/memcmp/strcmp library and its two complete native output vectors,
then compiles just the new memchr source twice. The resulting **four
source members at original indices259/260/261/292** replace those original
positions in the 893-member native library; all **889 surrounding original
member program records** stay intact. The independent reviewer binds every
literal output byte, phase log and source to its current hash.

Both actual isolated TASM/TLIB/TLINK rounds produce an EXE **byte-identical
to all67,372 bytes of the fixed Japanese decoded MAINL**, a raw-identical
full original MAP, and the exact677 original MZ relocations. No cold/DIET
or ancestor runtime replay occurs; no other source/input or accepted28-source
normal library is overwritten. The cumulative four CRT sources own **161
native reconstructed CODE bytes** inside this diagnostic verified library.
This does not automatically update the frozen211-owner published accepted
MAINL ledger.

Affected-only rebuild and check:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_memchr_combo_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_memchr_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_memchr_work

Retain .analysis/work/mainl-memchr-combo-build.json and the corresponding
review, full memchr-combo-roundN-* raw pairs, native logs and literal
TLIB/TLINK response files, plus the inherited source-only CRT pairs.
