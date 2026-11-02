# DOS fopen 556-byte working source: whole product exact, OMF order still open

The original CRT fopen member226 is now represented by maintained
semantic 8086 assembly in src/mainl/crt/fopen.asm. It contains
four contiguous original code regions: a 212-byte private near
file-mode parser, 210-byte public near __OPENFP at CODE+212,
77-byte public near __GETFP at CODE+422, and 57-byte public far
_fopen at CODE+499. All 556 original CODE bytes match real TASM 5.0
output without copied CODE arrays, artificial padding or object patches.

The source implements real original text/binary/+ mode handling,
stream-table lookup, DOS opening, buffer creation, console testing,
_setvbuf and fclose cleanup, and setup of the process-exit cleanup
pointer. Its original nine external names and indices are preserved
in order, with genuine zero DATA/BSS and 08ff02ff03 group.
**All 12 original OMF logical relocation fields match in site,
width, target, frame method/index, addend and kind.**

An important limitation remains: the native FIXUPP RECORD ORDER is
not yet recovered. Original BCC4.5 writes sites
464,461,436,387,369,318,274,184,182,178,176,156.
Direct TASM writes sites in ascending order instead; organizing
the semantic source in descending non-overlapping blocks restores
the order between different instructions but leaves the two paired
relocations in each MOV at CODE+174 and CODE+180 reversed. Genuine
BCC inline-assembler experiments have shown that Borland's compiler
can produce the original within-instruction descending field order,
but a whole BCC source with the exact original instruction encoding
has not yet been reconstructed. In particular, the early parser
inline-asm candidate generated a 217-byte instead of the original
212-byte body. The current maintained TASM source retains the more
readable forward control flow and **does not claim native original
FIXUPP ordering**.

Nevertheless, the actual native source-only product link is now
verified: both independent TASM/TLIB/TLINK rounds replace fopen
at its original position inside the 893-member CRT together with
the 32 previously exact source modules (including full xx, both
qsort bosses, scanner, fread/fwrite, fseek/ftell, getc/fgetc and
the natural C++ fscanf). **All 860 other original library member
program records remain unchanged.** Both complete **67,372-byte
Japanese decoded MAINL EXEs** and entire MAPs match the fixed
Japanese original byte-for-byte, with all 677 MZ relocations.
There are **20,428 original CODE bytes from 33 source modules**
in this working link, but the fopen member itself is still
marked incomplete for *native ordered OMF exactness*.

The accepted28-provider CRT and 211-owner formal publication remain
frozen; source_acceptance=false and added_accepted_bytes=0.
No full cold replay, DIET packing or patched OMF target was used.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_fopen_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_fopen_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_fopen_work

Real native OBJ/LIB/EXE/MAP vectors, phase logs and independent receipts
are retained under .analysis/work/fopen-* and
mainl-fopen-native-{build,review}.json.
