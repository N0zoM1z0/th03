# Complete 1,256-byte DOS strftime source, format tables and 52-source MAINL

The Borland DOS large-model far-cdecl strftime module (CRT member298)
is maintained as original 8086 source in src/mainl/crt/strftime.asm.
Its actual program interprets 22 supported ASCII format specifiers,
uses original weekday/month name pointer tables, stack-local format
buffer, and genuine __UTOA, strcat, strcpy, strlen, strncpy, atime CRT
helpers. No altered DOS/locale behavior or modern buffer guards.

The **1,256 original CODE bytes** comprise **1,168 genuine executable
8086 instruction bytes** plus **88 bytes of CODE-resident lookup
tables**: 22 ASCII format character WORDs and 22 symbol-resolved
branch target WORDs. The latter are native DW OFFSET references, not
embedded executable opcode arrays. Seven real C string fragments
account for the original **18 initialized DATA bytes**.

The native TASM output matches **all 1,256 original CODE and all
18 initialized DATA bytes**. All 12 imported symbol names and indices,
far public, true DATA/BSS group and **all 66 OMF relocation CODE sites,
targets, widths, addends and original literal writer order** match.
Original BCC emits first the descending fixups in the CODE prefix,
then 22 descending switch-table fixups, then four later-body fields.
The source uses non-overlapping symbolic instruction blocks at
original offsets to reproduce this writer order without executable
padding, object patches or copied machine-code arrays.

**Four raw OMF frame differences remain OPEN**: near __UTOA calls at
CODE+723, +774, +811 and +879 use original BCC TARGET-frame method5,
whereas TASM uses CODE-segment frame-method0. The independent reviewer
requires exactly those differences and rejects additional ones;
native original OMF equality is not claimed.

Installed at original member298 together with 51 preceding source
CRT modules (complete xx, both large qsort algorithms, scanner,
buffered putc, file/path utilities), **841 other original library
member program records remain unchanged**. Both native TASM/TLIB/TLINK
rounds reproduce the complete **67,372-byte decoded Japanese MAINL
EXE and original MAP byte-for-byte**, retaining all **677 original
MZ relocations**. The 52 simultaneous source modules yield
**26,971 original CODE bytes** in the working carrier.

The inherited fopen ordered OMF, fclose near frame and _timecvt
near frame gaps are separately open. The accepted28-provider library,
formal211-owner MAINL ledger, retained cold pair and original
candidate-local-attested Japanese target are unchanged. Source-only
normal-link exactness does not grant accepted ledger byte credit.
No full cold/DIET replay was executed.

Affected-only verification:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_strftime_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_strftime_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_strftime_work

Two complete raw native OBJ/LIB/EXE/MAP vectors, source/driver hashes
and actual TASM/TLIB/TLINK logs are retained under
.analysis/work/strftime-* and mainl-strftime-native-{build,review}.json.
