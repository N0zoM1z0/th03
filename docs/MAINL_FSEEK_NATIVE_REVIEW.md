# Real selected CRT fseek/ftell: complete 492 CODE and 31-source MAINL

The existing maintained 8086 translation unit
src/mainl/crt/fseek.asm, with its typed
src/mainl/crt/stdio_layout.inc, is now independently verified
as a complete source-only replacement of the original large-model
Borland DOS CRT file-position module at library index232.

The original contains three distinct semantic functions:
a **137-byte private near buffered-byte adjustment helper**
for text-mode LF expansion, the **130-byte far _fseek**
at original CODE+137 and the **225-byte far _ftell**
at CODE+267. These functions preserve the real FILE
stream-level, buffer-position and DOS seek flags,
the original three imports (_fflush, _lseek, __openfd),
far-cdecl ABI, near RET4 and far returns. Actual TASM
compilation reproduces **all492 original CODE bytes**,
the original far PUBLIC coordinates, empty DATA/BSS,
and original DATA-before-BSS DGROUP record 08ff02ff03.
No raw CODE-byte arrays, padding or binary object
patches are used.

An important original-evidence discrepancy was independently
discovered, rather than trusting historical records. The
standalone vendor/fseek.obj and the fseek member program
inside the actual Japanese CRT library have **identical
complete CODE bytes and the same six logical relocations**
but different raw OMF writer order:

| Original evidence | Literal OMF FIXUPP CODE-site order |
| --- | --- |
| Actual selected in-library member232 | 342,149,239,293,365,409 |
| Separate standalone vendor/fseek.obj | 409,365,342,293,239,149 |

The native readable maintained TASM source generates the
**exact in-library ordered six fields**, not the
standalone-file variant. An experiment that reassembled
reordered ORG source blocks to match the standalone
record was rejected after checking the actual selected
library program. The original readable source is retained,
and the scoped builder verifies the two original variants
separately, including their equal literal field sets
and unequal chronological writer order. This is source
selection based on true MAINL link provenance.

The independently reviewed native producer inherits the
preceding 30-source CRT exact working carrier, including
complete fread/fwrite/getc and scanner, whole xx and
both qsort algorithms. It assembles the maintained fseek
source and original FILE layout twice, replaces only the
genuine library slot232, and retains all **862 other
original member program records** in the 893-member
CRT unchanged. Two real TASM/TLIB/TLINK rounds
produce the **complete 67,372-byte decoded Japanese
MAINL EXE and its original MAP byte-for-byte**, with
all **677 MZ relocation entries** intact. The combined
**31 source modules generate 19,832 original CODE bytes**.

The accepted28-provider CRT and frozen211-owner MAINL
publication remain untouched: working source equality is
not formal accepted ledger promotion. The original
Japanese target remains candidate-local-attested, no
full cold replay/DIET repack or ancestor reconstruction
was run.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_fseek_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_fseek_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_fseek_work

Retained source/FILE-layout hashes and both complete
raw TASM OBJ/TLIB CRT/EXE/MAP vectors, actual native
writer logs and both original selected/standalone
member receipts are under .analysis/work/fseek-full-*
and mainl-fseek-native-{build,review}.json.
