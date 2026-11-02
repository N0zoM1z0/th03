# Original qsort far entry: 44-byte native control and three BSS fields

**Historical bounded checkpoint.** This document records a partial
native experiment completed before the full source recovery.
The current qsort.asm now reproduces all 756 original CODE bytes,
29 literal fields and the complete Japanese MAINL EXE/MAP with 17
simultaneous source CRT members. See
[complete native qsort review](MAINL_QSORT_NATIVE_REVIEW.md).
The partial complete_qsort=false refers only to that earlier
limited diagnostic and is not the current reconstruction status.


The original Japanese qsort Borland CRT member has 756 CODE bytes,
29 literal ordered OMF fields,6 bytes of comparator/element-width BSS,
a 46-byte private near swap routine,666-byte near sort core and a
44-byte public far qsort entry at original CODE offset712.

The maintained bounded 8086 source in src/mainl/crt/qentry.inl now
reconstructs the entire *shape* of the original public far entry:
original stack frame/preserved SI+DI,element-width check,comparison
far-pointer storage,the original far base and element count parameter
push order,one real near call to qsort_core at CODE+46,and far RETF.
All three BSS ownership fields at entry-relative offsets9,23,26
agree literally with the original target,including their frame
and distinct BSS addends4,2,0. The original qswap.inl also matches
all46 near helper bytes and its width field at CODE+9.

Two genuine TASM runs compile a deliberately limited source-only
context:the actual 46-byte swap,an isolated 3-byte callee-clean
qsort_core stub,then the recovered public entry. The stub exists only
to validate the near call ABI and **does not pretend to reconstruct
the original sorting algorithm**. The public 44-byte body matches
the original in all **42 non-CALL-operand bytes**. The remaining two
CALL displacement bytes naturally differ because the original
core contains 666 bytes rather than the 3-byte scoped ABI stub.
Both native CALL instructions resolve to the actual semantic
near core start at CODE+46,not an invented target address.

This source-only original ABI/layout result advances the large
qsort boss but is **not** full qsort reconstruction. The real
666-byte recursive sort/partition core with the other25 OMF fields
remains open. No original module object is patched,and the partial
source is not linked into the actual Japanese MAINL in place of
qsort. All original targets and accepted ledger bytes remain unchanged.

Affected-only run:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_mainl_qsort_entry.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_qsort_entry.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_qsort_entry

The full raw two native scoped OBJ outputs plus source-bound
build/review receipts remain under .analysis/work/qsort-entry-*.
