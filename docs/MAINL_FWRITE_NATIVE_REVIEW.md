# Original DOS fwrite: 153-byte far buffered-output source and 29-source link

The maintained original-8086 source at src/mainl/crt/fwrite.asm
reconstructs every byte of the Borland DOS large-model
far-cdecl fwrite CRT member236. The original routine is
**153 CODE bytes** across 61 natural x86/8086 instructions,
a complete public _fwrite at CODE+0 with original RETF.
It checks the record size and count, computes total unsigned
byte extent via the genuine N_LXMUL@ near provider, calls
the original __FPUTN buffered writer, advances the far
source through N_PADD@ for multi-record output, and returns
the number of completed records on partial write.

Native TASM5 emits **153/153 original CODE bytes**,
the exact public entry, original empty DATA/BSS and
literal BSS-before-DATA GRPDEF 08ff03ff02. Three genuine
EXTDEF imports retain their original sequence:
__FPUTN, N_LXMUL@ and N_PADD@. All **four literal
ordered OMF fields** are byte- and type-exact, at
sites28 (near N_LXMUL@),63 (near __FPUTN),
95 (near __FPUTN) and125 (near N_PADD@), with
original CODE-frame near displacements and indices.
No byte arrays, alignment filler or object patches
are needed for natural assembler source equality.

The scoped producer inherits the previously exact
28 native source CRT members, including the 437-byte
two-function fread TU, 322-byte srchstr, 1,282-byte
scanner with 128 initialized DATA bytes, complete
12,622-byte xx and both large sorting algorithms.
It newly assembles fwrite at real original CRT index236
in the 893-member library. All **864 other original
member programs** are identical. Both actual
TASM/TLIB/TLINK rounds reproduce the **entire
67,372-byte decoded Japanese MAINL EXE** and the
complete original MAP raw-equal, including all677
ordered DOS MZ relocations. The simultaneous exact
source-built CODE scope is **18,855 bytes in
29 original library members**.

The accepted28-provider CRT and frozen211-owner
MAINL publication have not been updated; source
working-link equality does not automatically add
formal accepted ledger credit. The fixed original
Japanese target remains candidate-local-attested.
No full cold replay, DIET stage or ancestor chain ran.

Affected-only commands:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_fwrite_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_fwrite_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_fwrite_work

Retain the two complete native raw OBJ/LIB/EXE/MAP
pairs, TASM/TLIB/TLINK logs and bound source hashes
under .analysis/work/mainl-fwrite-native-{build,review}.json
and .analysis/work/fwrite-full-*.
