# Original DOS gets: complete 135-byte stdin reader and 38-source link

The original Borland DOS far-cdecl gets is now maintained as
src/mainl/crt/gets.asm. Its 135-byte implementation directly
accesses the original global __streams stdin buffer, falling
back to the real far __fgetc provider when the buffered count
is exhausted. It retains the original far destination cursor,
linefeed/EOF termination, NUL insertion, FILE error flag and
far DX:AX return, including original unchecked gets behavior.
No modern buffer limit or defensive fault handling was inserted.

Native TASM5 produces all **135 original CODE bytes**, the
original one public _gets at0, genuine __streams/__fgetc
EXTDEF order and the original empty DATA/BSS group
08ff02ff03. It reproduces all **six original OMF FIXUPPs in
literal order**: sites112/58/54/43/39/33, including
GROUP-framed offsets +2/+12/+0 into the original stream
table and TARGET-framed far __fgetc. The source uses
non-overlapping original instruction blocks at their
original CODE addresses to preserve the Borland descending
FIXUPP record ordering, with genuine symbolic branches
and no byte arrays, alignment padding or object patches.

Its source is placed at actual CRT member241 alongside the
original-source fgets, stat, xx, two qsort sorting bosses,
scanner, fseek/ftell/fread/fwrite and previous CRT modules.
**38 source modules** collectively provide **21,564 exact
CODE bytes**, while **855 of893 original CRT member program
records** remain unchanged. Two normal TASM/TLIB/TLINK
rounds both reproduce the complete **67,372-byte original
Japanese decoded MAINL EXE and MAP** bit-for-bit with
all **677 original MZ relocations**.

The earlier source-only fopen/fclose OMF gaps remain explicit:
these source-linked results do not claim all 38 OBJ metadata
records are original-literal. The accepted28-provider CRT,
211-owner formal MAINL publication and fixed Japanese target
are unchanged; no newly credited accepted bytes or full cold
replay are claimed.

Affected-only validation:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_poststat_work.py fgets-gets
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_poststat_work.py fgets-gets
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_poststat_work

Two complete native TASM OBJ/TLIB/EXE/MAP rounds and phase logs
remain under .analysis/work/poststat-fgets-gets-*, with bound
build/review receipts.
