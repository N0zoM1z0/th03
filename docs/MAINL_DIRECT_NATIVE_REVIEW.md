# Complete original DOS directory subsystem: 517 CODE, 9 DATA, 20 OMF fields

The original Japanese Borland DOS directory CRT translation unit,
library member214, is now maintained as native 8086 assembler
source src/mainl/crt/direct.asm. It owns **four original public far
functions**: opendir at CODE+0 (311 bytes), rewinddir at +311
(56 bytes), readdir at +367 (75 bytes) and closedir at +442
(75 bytes). These are not stand-in wrappers: the source
implements far path allocation, separator/DBCS checking,
DOS FindFirst and FindNext state, iteration reset and the
original allocated path/name buffer and DIR-handle release.

The source has **517 original CODE bytes and nine real
initialized DATA bytes**. The DATA bytes are two genuine
DOS wildcard search strings: backslash, star, dot, star, NUL
and star, dot, star, NUL. They are written as symbolic
initialized DATA rather than copied executable bytecode.
The original nine far/data external names and their order,
all four native far public offsets, empty BSS and literal
DATA-before-BSS group 08ff02ff03 are preserved.

**All 20 literal original OMF FIXUPPs** match exactly in
their original descending-site writer order:
504,493,467,405,384,348,259,248,230,205,194,177,165,
155,149,136,66,46,29,15. This includes original GROUP
frames on _errno and both initialized wildcard DATA
references (addends0 and5), plus the genuine far TARGET
frames for __dos_findfirst, __dos_findnext, _free, _malloc,
_strcat, _strcpy, _strlen and ___path_issbcs.

The maintained mnemonic source assembles disjoint,
non-overlapping, semantically labeled control-flow ranges
in original writer order using ORG at genuine instruction
boundaries. No filler bytes, embedded original CODE DB
arrays or binary object patches are present. All 192 real
instruction bodies and all original CODE/initialized DATA
bytes agree with actual native TASM output.

The scoped builder reuses the already verified **44-source
original CRT working carrier**, containing complete xx, two
sorting bosses, numeric/format scanners, file IO and DOS
small helper functions. The new source replaces precisely
original library member214 in a 893-member CRT, leaving
**848 other original program records byte-identical**.
Both actual TASM/TLIB/TLINK rounds reproduce the **entire
67,372-byte decoded Japanese MAINL EXE** and original
MAP byte-for-byte, with all **677 original MZ relocations**.
The simultaneous 45-module working CRT supplies **22,803
source-generated original CODE bytes**, plus the new nine
source-exact initialized DATA bytes.

Previously documented original native OMF discrepancies in
the *other* fopen/fclose members remain explicitly open:
the entire working linked product is byte exact, but not
every original source object is fully OMF metadata-exact.
The accepted28-provider CRT and formal211-owner MAINL
ledger remain frozen. These source-only results are not
new formally accepted bytes; the fixed target remains
candidate-local-attested. No full cold/DIET replay ran.

Affected-only verification:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_direct_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_direct_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_direct_work

The complete native OBJ/LIB/EXE/MAP output vectors, actual
TASM/TLIB/TLINK phase logs and source-bound original proof
receipts are retained in .analysis/work/direct-* and
mainl-direct-native-{build,review}.json.
