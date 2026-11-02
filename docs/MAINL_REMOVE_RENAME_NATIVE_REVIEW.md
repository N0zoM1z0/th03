# Exact DOS remove and rename: two real syscall sources in a 44-module CRT

The original 28-byte Borland far-cdecl _remove (member104) and
31-byte far-cdecl _rename (member278) are fully reconstructed as
maintained 8086 source in src/mainl/crt/remove.asm and rename.asm.

Both implementations retain the original saved DS register and DOS
INT 21h calling convention: AH=41h deletes a far DS:DX path, and
AH=56h renames a DS:DX path to the far ES:DI target. On carry they
push the original DOS error AX and call genuine near __IOERROR,
preserving the original caller frame and far return. No extra
path validation, return conversions or binary object patches occur.

Actual Borland TASM output matches **28/28 and 31/31 original CODE
bytes**, their public symbols/offsets, original external __IOERROR
import, zero DATA/BSS and literal original group 08ff03ff02. Each
module reproduces its own original CODE-framed near error-call
FIXUPP (remove site22, rename site25) with exact target, width,
frame and writer order.

Both source units were compiled twice and inserted into the full
893-member native CRT along with 42 previous reconstructed source
modules, including 556-byte stat, 459-byte open, complete xx,
two quicksort algorithms and stream I/O. The other **849 library
program records** remain byte-identical to the original. Both
normal TASM/TLIB/TLINK rounds reproduce the whole **67,372-byte
decoded Japanese MAINL EXE** and complete original MAP byte-for-
byte, retaining all **677 MZ relocations**. The 44 source modules
now contribute **22,286 original exact CODE bytes**.

The inherited fopen OMF writer-order and fclose near-frame
differences are still open: the joint source-only CRT is exact
as a linked product, not 44 original-literal OMF member records.
The accepted28-provider library, formal211-owner MAINL ledger
and pinned Japanese target remain untouched, without full cold
replay, DIET repack or new accepted credit.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_postopen_work.py clearerr-rewind-remove-rename
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_postopen_work.py clearerr-rewind-remove-rename
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_postopen_work

Complete two-round native OBJ/LIB/EXE/MAP vectors and source-bound
command logs are retained in .analysis/work/postopen-*.
