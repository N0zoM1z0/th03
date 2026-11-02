# Original DOS tempnam: full 395 CODE, 6 DATA and 53-source MAINL

The original Borland DOS large-model far-cdecl tempnam module at CRT
member320 now has maintained native symbolic 8086 source in
src/mainl/crt/tempnam.asm. It implements the original filename
generation workflow: four candidate directory pointers including
the environment path, far string length/copy, DBCS-aware path
separator inspection, a dynamic far filename buffer, the real
__MKNAME near numeric suffix helper and DOS file attribute probing
until a usable name is found. Its native initialized DATA consists
of six actual bytes for the original TMP prefix and two NUL suffixes.

Real TASM5 generates **all 395 original CODE bytes and 6 DATA bytes**.
The far _tempnam public at CODE+0, all nine original imported CRT
names and indices, DATA-before-BSS group and all **14 original
ordered OMF relocation sites/targets/addends** match. Native source
uses actual symbolic labels and 147 8086 instructions in disjoint
original CODE ranges to preserve Borland's descending OMF writer
sequence. No executable opcode byte arrays, patching or synthetic
NOPs are used.

**One native OMF field still differs**: the near __MKNAME call at
CODE+309 uses TARGET-frame method5 in the original BCC4.5 object
but CODE-segment method0 in TASM. The source's instruction bytes
and relocation target agree, and all other 13 literal FIXUPPs
match. Independent review requires exactly this discrepancy rather
than reporting the OBJ as fully original-metadata-equal.

Both actual TASM/TLIB/TLINK rounds install tempnam in its genuine
original position in the 893-member CRT together with **52 previously
reviewed source modules**, leaving **840 other vendor program
records byte-identical**. Both complete **67,372-byte decoded
Japanese MAINL EXE** files and original MAPs match the pinned
Japanese target bit-for-bit, including all **677 original MZ
relocations**. The simultaneous 53-module working source CODE
scope reaches **27,366 exact original bytes**.

Inherited original frame/order gaps in strftime, _timecvt, fopen
and fclose remain separately OPEN. The original accepted28-provider
CRT and formal211-owner MAINL ledger are unchanged; this source-only
normal-link proof does not grant newly accepted byte credit.
The original reference is still candidate-local-attested. No full
cold replay or packed DIET repacking was run.

Affected-only verification:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_tempnam_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_tempnam_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_tempnam_work

Actual two-round native OBJ/LIB/EXE/MAP output vectors, TASM/TLIB/TLINK
command logs and bound source/build receipts remain under
.analysis/work/tempnam-* and mainl-tempnam-native-{build,review}.json.
