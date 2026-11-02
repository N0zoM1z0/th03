# Original qsort boss: first native 46-byte near swap helper recovered

The original Japanese MAINL Borland CRT qsort member at index275 contains
756 CODE bytes,29 literal ordered OMF FIXUPPs and a real6-byte BSS
context:four bytes for the far comparator and a two-byte element width.
The full original has three routines:the private near element-swap
helper at0, a large private near quicksort/partition core at46 and the
public far qsort entry at712. The recursive body uses the genuine
N_LXMUL@ and N_LDIV@ near arithmetic helpers;these are original
imports,not stand-in math behavior. The recursive core is STILL OPEN.

The maintained bounded source src/mainl/crt/qswap.inl now reconstructs
all **46 original bytes** of the first helper and the first literal
OMF BSS-width reference at CODE+9. Actual TASM compilation twice
produced a complete identical 46-byte object CODE block, including
original DS/ES handling, an optional odd first-byte swap,
word-wise swaps and the original near callee-clean RET 8 ABI.
Its one original source field retains segment1,site9,WORD offset,
DGROUP frame and BSS target3/addend4;the real BSS6 geometry and
original 08ff03ff02 GRPDEF also agree in the isolated native object.

This recovery is source mnemonic control flow and the original
6-byte state-owner declaration, not an embedded target-byte
array, artificial padding or modified object. The scoped TASM
source wrapper exists only to compile the bounded helper; it is
not substituted for the entire qsort member in the MAINL library.

The comparison proves exactly the first **46 of756** original qsort
CODE bytes and **1 of29** original OMF fields. It does NOT assert
the recursive sorting body, full module CODE/fields, whole qsort
source exactness or new accepted-ledger credit. Earlier assumptions
about qsort's public entry and local ABI should always be checked
against real source and OMF records, rather than treating a generic
C qsort algorithm as authoritative.

Affected-only replay:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_mainl_qsort_swap.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_qsort_swap.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_qsort_swap

Two full raw partial TASM objects, source hashes, actual phase logs
and review receipts are retained under .analysis/work/qsort-swap-*.
The fixed Japanese target and existing accepted/cold artifacts are
not rebuilt.
