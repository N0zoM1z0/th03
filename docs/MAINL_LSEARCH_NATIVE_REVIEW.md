# Original DOS lsearch/lfind: complete 202 CODE bytes and 59-source MAINL

The original large-model DOS CRT lsearch module (member247) now has
maintained symbolic 8086 source in src/mainl/crt/lsearch.asm. It has
three real contiguous routines: the 117-byte private near Pascal
search worker, the 43-byte far public _lsearch at CODE+117 and the
42-byte far public _lfind at CODE+160. The internal worker uses the
caller-supplied original far comparator function pointer at BP+6,
walks fixed-size array elements, returns the actual DX:AX far result
and, only for lsearch, calls the genuine far _movmem provider and
increments the original element count. Its stack, near Pascal
RET 14h and original far wrapper calling convention are preserved.
No artificial guards, stubs, copied machine code or object patches.

Actual TASM5 emits **all 202 original CODE bytes** and exactly the
original literal ordered OMF FIXUPP: the far _movmem call at CODE+84
with original TARGET frame. Both public symbols, the one EXTDEF,
true empty DATA/BSS extents and literal 08ff02ff03 group match.
An explicit symbolic CALL DWORD PTR [BP+6] preserves the original
indirect far comparator instruction; the two far publics call the
private near Pascal worker without adding a non-original PUSH CS.

The scoped builder inherits the original 58-source CRT with the
fully native four-segment tzset/ISDST module and all prior large
boss/source CRT modules. It replaces lsearch at the genuine
position in the original 893-member library and leaves **834
other original CRT program records unchanged**. Both real native
TASM/TLIB/TLINK rounds reproduce the entire **67,372-byte decoded
Japanese MAINL EXE and full original MAP byte-for-byte** with all
**677 original MZ relocations**. The 59-source working library
contributes **28,413 original CODE bytes**.

The previous fopen/fclose/timecvt/strftime/tempnam original OMF
metadata gaps remain separately OPEN. The accepted28-provider
CRT, formal211-owner MAINL ledger and pinned Japanese original
remain unchanged. The original cold pair is retained; no full
cold replay, DIET repacking or newly credited accepted bytes.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_posttzset_work.py lsearch
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttzset_work.py lsearch
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_posttzset_work

Both complete original native OBJ/LIB/EXE/MAP vectors, compiler logs
and source-bound build/review receipts are under
.analysis/work/posttzset-lsearch-*.
