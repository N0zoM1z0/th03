# DOS fclose: all192 machine-code bytes, original OMF near frame open

The original Borland DOS large-model far-cdecl fclose (CRT member217)
is now a maintained 8086 source TU in src/mainl/crt/fclose.asm.
All **192 original CODE bytes** are emitted by actual Borland TASM5,
not copied as an executable DB array or patched into an OBJ file.
The function validates the original far FILE owner, conditionally
flushes buffered output, handles temporary files, closes the DOS
descriptor and clears the original stream state. Its actual near
__MKNAME call obtains a name for the original far _unlink helper.
The original BP/stack frame, far public offset0, original five
CRT imports, zero DATA/BSS and DATA-before-BSS GRPDEF are preserved.

All **five original logical OMF relocations** agree in location,
target/EXTDEF index, width and addend, with sites168,163,112,89,60.
The four far calls (unlink, close, free, fflush) match their
original literal native FIXUPP records exactly. The one near
__MKNAME call at site163 remains a genuine **OMF frame mismatch**:
original BCC emits TARGET frame-method5; real TASM emits CODE
frame-method0, though the instruction bytes and relocation target
are identical. This is explicitly marked native_original_OMF_equal=false,
not silently normalized into source accepted bytes.

We tried a genuine BCC4.5 inline-assembly function with the original
single 2-byte local, far ABI and near __MKNAME call to recover the
compiler's TARGET frame; Borland's inline assembler rejected the
original ES:[BX] word immediate compare. Ten differently typed native
operand forms were tested without constructing a byte array or
patching OMF. Those trials remain private and do not constitute a
complete native-original fclose OBJ.

For actual product evidence the source is built in the normal
893-member CRT at original index217 alongside the 34 preceding
original source modules (full xx, qsort/hqsort, scanner/scantol,
fread/fwrite, fseek/ftell/getc/fscanf, full closeall and working
fopen). The other **858 original CRT member programs** are wholly
unchanged. Two complete native TASM/TLIB/TLINK rounds reproduce
the **entire 67,372-byte original Japanese decoded MAINL EXE**
and native MAP byte-for-byte, including **677 ordered MZ
relocations**. The cumulative source-only working CODE extent
is now **20,719 original bytes across35 source modules**.

The previously known fopen ordered-FIXUPP gap is still open as
well. Hence the complete 35-source linked product is exact, but
not every source module has original-literal OMF metadata.
The published211-owner MAINL ledger, accepted28-provider CRT,
retained cold pair and pinned candidate-local-attested Japanese
target are unchanged; source_acceptance=false and
added_accepted_bytes=0. No full cold or DIET replay ran.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_fclose_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_fclose_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_fclose_work

Full native two-round OBJ/LIB/EXE/MAP vectors and actual phase logs
are retained under .analysis/work/fclose-* and
mainl-fclose-native-{build,review}.json.
