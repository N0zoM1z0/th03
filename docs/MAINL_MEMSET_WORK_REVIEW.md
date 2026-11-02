# Native DOS memset and setmem: two entry points in an exact CRT member

The real 8086 source `src/mainl/crt/memset.asm` reconstructs the original
Japanese MAINL library member `memset` (index263 in the 893-member CRT).
It is **72 complete CODE bytes**, split into an original38-byte far `_setmem`
helper at offset0 and a34-byte far `_memset` wrapper at offset38. Both symbols
and the relative near CALL at wrapper offset0x38 retain their exact original
instruction encodings. The original empty `_DATA`/`_BSS` segments and the
literal BSS-before-DATA GRPDEF `08ff03ff02` also match,with no imported
symbols or native relocation fields.

`_setmem` preserves its original far cdecl stack and SI/DI,loads ES:DI with
the output pointer,AL/AH with the fill byte and CX with the WORD length,
and executes `CLD`. It fills an odd-aligned leading byte only when CX is
nonzero,then uses forward REP STOSW and an optional odd trailing byte.
The original `_memset` pushes its far destination,fill and length in native
cdecl order,executes PUSH CS plus a genuine near CALL to the far helper,and
returns its original far destination in DX:AX. The source retains the
original unchecked behavior;no object-byte tables or patched targets.

`build_th03_mainl_crt_growth_work.py memchr-memset` assembles all five
independent real DOS sources (memchr,memcmp,memcpy,memset,strcmp),verifies
their complete CODE/public/segment/GRPDEF/ordered-field profiles against
the original native members,and replaces precisely their original CRT slots
259/260/261/263/292. The other **888 complete library member program
records** remain unchanged. Two real TASM/TLIB/TLINK rounds independently
repeat the raw source OBJ/LIB/EXE/MAP vectors. Both produce an EXE identical
to the complete **67,372-byte original Japanese decoded MAINL**,with the
identical original MAP and **677 MZ relocations**. The total five-source
CODE coverage is **233 bytes**,not additional accepted-ledger credit.

The original accepted28-provider library,211-owner publication,retained
cold pair,original project objects and Japanese target are unchanged.
No full cold replay,canonical DIET repack or ancestor runtime replay occurs.

Focused builder,re-review and tests:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_crt_growth_work.py memchr-memset
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_crt_growth_work.py memchr-memset
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_crt_growth_work

Retain the two complete `crt-growth-memchr-memset-roundN-*` vectors and
source/driver/target-bound build and review receipts in `.analysis/work`.
