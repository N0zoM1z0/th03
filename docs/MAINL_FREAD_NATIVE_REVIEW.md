# Original DOS fread: complete 437-byte buffered I/O reconstruction

The original Borland C/C++ 4.5 large-model DOS CRT fread
(member229) is now maintained as native 8086 assembler source
at src/mainl/crt/fread.asm. This is a complete original
**437-byte translation unit**, not merely a far-call shim.

Its first **283 bytes** are a private near buffered-reading
helper with the original four-byte stack local, stream buffer
fill and read counts, direct byte fetch, EOF/error flags,
bulk read through __rtl_read, single-character fallback
through __fgetc, and genuine near Pascal RET 10 cleanup.
The remaining **154 bytes** form the public far-cdecl _fread
at original CODE+283. That entry multiplies requested record
size/count through the original 16-bit near N_LXMUL@ provider
and advances the far destination buffer through N_PADD@
while tracking partial record counts. It returns with the
original far RETF and preserves the original BCC4.5 ABI.

Borland TASM 5.0 produces **all 437 original CODE bytes**,
the exact one public _fread, original 08ff03ff02 BSS-before-
DATA group with empty DATA and BSS, and all four native OMF
fields **in literal original order**:
far __rtl_read at site135 (TARGET frame5),
far __fgetc at site245 (TARGET frame5),
near N_LXMUL@ at site313 (CODE segment frame0), and
near N_PADD@ at site385 (CODE segment frame0).
The original EXTDEF name order is
__fgetc, __rtl_read, N_LXMUL@, N_PADD@.
The compiler-level distinction between far and near imports
is preserved by real source declarations, not normalized
after assembly. No embedded CODE-byte arrays, artificial
padding or object patches are involved.

The scoped source-only builder reuses the previous **27 exact
original source CRT modules**, including complete exception/
RTTI xx, both qsort bosses, the original scanner, path
resolver, stateful tokenizer, long parsers and string helpers.
It substitutes fread at genuine library index229, preserving
the other **865 original member program records** untouched.
Two real TASM/TLIB/TLINK rounds independently produce
the **complete 67,372-byte Japanese decoded MAINL EXE** and
its entire original MAP bit-for-bit, with all **677 original
MZ relocations** unchanged. **28 simultaneous maintained
source CRT modules produce 18,702 exact original CODE bytes**.

The original accepted28-provider CRT, published211-owner
MAINL source ledger, pinned candidate-local-attested target
and retained cold pair stay frozen. This exact working
source library is not automatic formal accepted credit.
No full cold replay, DIET packing or ancestor runtime
chain is required for this affected source validation.

Affected-only native reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_fread_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_fread_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_fread_work

Two complete raw native OBJ/LIB/EXE/MAP rounds and actual
TASM/TLIB/TLINK phase logs are retained with source hashes
in .analysis/work/mainl-fread-native-{build,review}.json
and .analysis/work/fread-full-*.
