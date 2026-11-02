# Complete original DOS stat: 556 CODE, four initialized DATA and 36-source link

The original Borland C/C++ 4.5 large-model CRT stat member289
now has complete maintained 8086 assembler source in
src/mainl/crt/stat.asm. Its first 132 CODE bytes implement an
original private far DOS path-character delimiter finder with
Japanese DOS double-byte character handling. The public far _stat
starts at CODE+132 and owns another 424 bytes. The real program
uses DOS Int 21h FindFirst and temporary DTA storage, resolves
and releases far fullpath buffers, handles DOS file attributes,
records the original FILE metadata and calls the genuine near
DOS timestamp/conversion and IO-error helpers. Its source also
defines four real, initialized DATA bytes for the DOS path
characters backslash/slash/period/terminator; these are program
DATA, not copied executable machine opcodes.

The native assembler emits **all 556 original CODE bytes and
all 4 initialized DATA bytes** byte-for-byte. Both original
function boundaries, one public _stat at offset132, five real
external names/indices, empty BSS and literal BSS-before-DATA
GRPDEF 08ff03ff02 are restored. All **nine original ordered
OMF FIXUPPs** agree in location, field width, frame method/index,
target method/index, addend and record sequence. The real
near __IOERROR and __DOSTIMETOU calls are CODE framed, while
far __fullpath, _free and Japanese path-lead-byte helpers use
their actual far TARGET frames.

Several actual TASM source forms were compiled rather than
trusting earlier assumptions. With the private path finder
declared FAR, an unrestricted CALL stat_find_delimiter
incorrectly added a second PUSH CS, shifting the remaining
CODE and field sites by one. Keeping the genuine manually
pushed CS followed by explicit CALL NEAR PTR
stat_find_delimiter restores all original bytes without any
padding or object manipulation. The original group and DS
register assumptions required defining DATA/BSS and DGROUP
before emitting the CODE body; this also preserves true
initialized DATA rather than reclassifying or faking it.
No original CODE-byte tables or postprocessing patches
are present in the maintained source.

The scoped builder inherits the existing verified 35-source
original Japanese MAINL carrier including complete xx,
both qsort bosses, scanner/scantol, path searching and file
I/O. Recompiling only stat and rebuilding the real 893-member
CRT twice leaves **857 original member program records**
unchanged. Both native TASM/TLIB/TLINK rounds reproduce
the **entire original 67,372-byte Japanese decoded MAINL
EXE and its original MAP byte-for-byte**, with all 677
ordered MZ relocations. This brings the simultaneous exact
working-source CODE extent to **21,275 bytes across 36
original CRT source modules**, plus four exact new DATA
bytes. The existing fopen/fclose native FIXUPP discrepancies
are explicitly inherited: they do not affect this fully
native-original stat module or product-link equality.

This does not automatically increase the formal accepted
211-owner MAINL ledger. The pinned candidate-local-attested
target, original accepted28-provider CRT and retained cold
pair remain unchanged; source_acceptance=false and
added_accepted_bytes=0. No full cold, DIET or ancestor replay.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_stat_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_stat_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_stat_work

Actual raw native OBJ/LIB/EXE/MAP rounds and source-bound
writer logs/receipts are retained at .analysis/work/stat-*
and mainl-stat-native-{build,review}.json.
