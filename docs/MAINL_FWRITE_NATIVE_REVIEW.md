# Original DOS fwrite: complete native 153-byte source and 29-source link

The original Japanese Borland DOS far-cdecl fwrite (library index236)
is now maintained as real 8086 source at src/mainl/crt/fwrite.asm.
It preserves the original record-width/count multiplication using
near N_LXMUL@, writes with the real near __FPUTN provider, advances
far memory pointers with the original segment-aware N_PADD@ and
handles short partial-record writes and the large-block record loop.

Actual TASM5 emits **all 153 original CODE bytes**, one public
_fwrite at offset0, zero initialized DATA/BSS, original
BSS-before-DATA GRPDEF 08ff03ff02 and the exact ordered
four native OMF near fields at sites 28/63/95/125, with their
original CODE-segment frame and genuine EXTDEF indices:
N_LXMUL@, __FPUTN, __FPUTN, N_PADD@. The original import
ordering is __FPUTN, N_LXMUL@, N_PADD@. This is natural
typed assembler-source control flow; there are no stored
original opcode bytes, binary patches or filler.

The scoped builder reuses the complete 28-source original CRT
that already includes fread437, both sorting bosses, the
1282-byte scanner, original xx, two long parsers and string
functions. At original CRT member236, the source-compiled fwrite
object replaces the vendor object. All **864 remaining member
program records** are unchanged. Two real serialized
TASM/TLIB/TLINK rounds independently reproduce the **entire
67,372-byte decoded Japanese MAINL EXE**, its original MAP
and all **677 MZ relocations** byte-for-byte. The 29 joint
native source modules generate **18,855 original CODE bytes**.

The accepted28-provider CRT library, 211-owner published MAINL
ledger, retained original cold pair and candidate-local-attested
Japanese target remain unchanged; this working source-only
link is **not new formally accepted exactness credit**. No
full cold or DIET replay was required.

Affected-only validation:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_fwrite_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_fwrite_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_fwrite_work

Complete source-bound native OBJ/LIB/EXE/MAP vectors and logs:
.analysis/work/mainl-fwrite-native-{build,review}.json and
.analysis/work/fwrite-full-*.
