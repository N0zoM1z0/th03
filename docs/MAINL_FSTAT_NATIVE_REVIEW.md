# Original DOS fstat: 147-byte native source and 39-source MAINL

The original Borland DOS far-cdecl _fstat, CRT member233, is
now maintained as real 8086 assembler source in
src/mainl/crt/fstat.asm. It interrogates the original DOS
file descriptor with INT 21h IOCTL, inspects the actual
__openfd descriptor mode byte, calls the far _filelength
provider, reads native DOS dates/times and invokes the
near __DOSTIMETOU converter. It populates the original
DOS struct stat in fourteen consecutive 16-bit word stores,
and preserves the original character-device and error
branches via the real near __IOERROR provider.

Actual TASM produces **all147 original CODE bytes**, the
one public far _fstat at0, zero DATA/BSS and literal
BSS-before-DATA group 08ff03ff02. All **four ordered OMF
FIXUPPs** are original-literal: group-framed __openfd+1 at
CODE site39, far _filelength at53, CODE-framed near
__DOSTIMETOU at74 and CODE-framed near __IOERROR at141.
Their original EXTDEF order is _filelength, __IOERROR,
__DOSTIMETOU, __openfd. The first source trial produced
identical CODE bytes and wrong external target indices;
correcting the actual symbolic declaration order restores
the original four literal native relocation records.
No embedded machine-code bytes, alignment padding or
object-format editing were used.

The scoped builder assembles this unit and previous fgets
and gets sources, inserting all three at original CRT
member positions alongside the complete stat, xx,
qsort/hqsort, scanner/scantol and previously recovered
file/string CRT units. **39 genuine original source
modules** produce **21,711 exact CODE bytes** in the
working library, leaving **854 of893 original CRT
member program records** untouched. Both serialized
TASM/TLIB/TLINK rounds reproduce the entire **67,372-byte
Japanese decoded MAINL EXE** and its original native MAP
bit-for-bit, with **677 original MZ relocation entries**.

The predecessor fopen/fclose native OMF metadata gaps
remain explicitly open. The original accepted28-provider
CRT, frozen211-owner formal MAINL publication and pinned
candidate-local-attested Japanese targets remain unchanged.
Normal-link source exactness is not automatic accepted
ledger promotion. No full cold/DIET replay was run.

Affected-only validation:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_poststat_work.py fgets-gets-fstat
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_poststat_work.py fgets-gets-fstat
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_poststat_work

All real native compiler/library/linker logs and both complete
raw OBJ/LIB/EXE/MAP output vectors are retained in
.analysis/work/poststat-fgets-gets-fstat-* and source-bound receipts.
