# Complete original DOS fgets: 154-byte native source and 37-source link

The original Borland DOS far-cdecl fgets in CRT member220 is now
maintained as real 8086 assembler source, src/mainl/crt/fgets.asm.
The code preserves the original 4-byte far destination local
cursor, 16-bit requested character limit, newline stop condition,
and direct buffered FILE state reads. The genuine far __fgetc
provider is used when the stream buffer is exhausted. It stores
the terminating NUL byte, distinguishes EOF before any bytes
from EOF after partial input and obeys the original FILE error
flag and far DX:AX return convention. No new null guards,
modern library semantics or defensive failure branches are
introduced.

Actual Borland TASM emits **all 154 original CODE bytes**,
the original public _fgets at offset0 and the single original
far __fgetc FIXUPP at CODE+79 with its literal TARGET frame.
The real EXTDEF, empty DATA and BSS extents and literal
08ff02ff03 group record match. The initial full CODE/FIXUPP
match still had the opposite zero-sized DATA/BSS group:
changing only the genuine source-side group declaration
restored literal original OMF layout. No target executable
byte arrays, padding, patches or record rewriters are used.

The scoped source builder inherits the verified large 556-byte
stat source and its 4-byte DATA, whole xx, qsort/hqsort, scanner,
path searching and FILE I/O source members. Only fgets is
newly compiled at original CRT slot220. In a 893-member library,
**37 real maintained source objects are linked concurrently**,
with **856 other original program records untouched**.
Both genuine TASM/TLIB/TLINK rounds reproduce the complete
**67,372-byte Japanese decoded MAINL EXE and native MAP
bit-for-bit**, preserving all **677 original MZ relocations**.
The simultaneous working native-source CODE extent is now
**21,429 original bytes**. Previous fopen/fclose literal native
OMF gaps remain separately recorded, so these working-library
figures are not assertions that all 37 objects have identical
original OMF metadata.

The accepted28-provider CRT library, published211-owner MAINL
ledger and pinned candidate-local-attested Japanese target
remain unchanged. Source-only original product proof is not
automatic formal accepted exactness credit; no full cold or
DIET replay was needed.

Affected-only verification:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_poststat_work.py fgets
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_poststat_work.py fgets
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_poststat_work

Two complete original TASM OBJ/TLIB CRT/EXE/MAP output vectors and
their writer phase logs remain under .analysis/work/poststat-fgets-*,
with current source-bound build/review receipts.
