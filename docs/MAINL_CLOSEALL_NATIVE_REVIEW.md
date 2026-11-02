# Original DOS fcloseall: 99-byte exact source and normal MAINL link

The original Borland DOS far-cdecl fcloseall member206 is now
maintained as natural 8086 source at src/mainl/crt/closeall.asm.
It skips the original first five reserved stream slots, uses a
real 4-byte SS local as a far pointer into DGROUP:__streams+100,
compares each active FILE descriptor against original __nfile,
calls the original far _fclose provider and retains the original
close count/error return conventions. No modern null/stream
guard, stub, opcode byte array or object patch has been added.

The actual TASM5 output is **all99 original CODE bytes**,
the original one public _fcloseall at offset0, empty DATA/BSS
and literal DATA-before-BSS GRPDEF 08ff02ff03.
**All three ordered literal OMF FIXUPPs** agree in site,
location width, TARGET/GROUP frame, target and addend:
__nfile at75, far _fclose at43 and DGROUP __streams+100
at19. The assembly arranges four non-overlapping original
instruction ranges in descending writer order with actual
control-flow labels and ORG at true instruction boundaries;
no executable filler is emitted.

The source was compiled twice and installed at its original
CRT slot206 alongside 33 preceding source modules, including
complete xx, qsort/hqsort, scanner/scantol, fread/fwrite,
fseek/ftell, getc, fscanf and the working fopen path.
**859 of893 other original library member program records**
remain unchanged. Both native TASM/TLIB/TLINK rounds reproduce
the full **67,372-byte decoded Japanese MAINL EXE and MAP
byte-for-byte**, retaining all **677 original MZ relocations**.
The 34 simultaneous source modules supply **20,527 original
CODE bytes**.

The newly recovered closeall OBJ is fully native-original,
but the predecessor fopen module is deliberately still marked
as an OPEN *original ordered OMF* case: its 556 original CODE
bytes, logical 12 field contents and whole-product source link
are exact, but its raw BCC FIXUPP ordering differs from TASM.
Do not conflate this source-only working CRT with a fully
native-original 34-member OMF carrier or formal ledger credit.
The accepted28-provider CRT, 211-owner published MAINL scope,
pinned Japanese target and retained cold pair are untouched.
No full cold/DIET replay was run.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_closeall_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_closeall_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_closeall_work

The two complete original native OBJ/LIB/EXE/MAP vectors, real
writer phase logs and source-bound receipts are retained under
.analysis/work/closeall-* and mainl-closeall-native-{build,review}.json.
