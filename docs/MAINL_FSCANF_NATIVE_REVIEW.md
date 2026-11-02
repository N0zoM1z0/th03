# Natural Borland DOS fscanf: 40-byte full TU and 32-source MAINL

The maintained src/mainl/crt/fscanf.cpp reproduces the complete original
Borland C++ 4.5 large-model variadic far-cdecl fscanf from genuine C++
source. The function takes a far stream, far format and unspecified
additional arguments; the original scanner receives a FAR pointer to
the first extra stack argument, the two original near callbacks
__Nfgetc / __Nungetc and the original near __scanner provider.

The expression (void far *)(&format + 1) is crucial: it directly forms
the actual far SS:BP+14 start of the variadic arguments. BCC emits
the original PUSH SS / LEA AX,[BP+0Eh] / PUSH AX, then all original
stream/format and near callback addresses with no extra BP locals.
In actual compiler trials, a conventional va_list/va_start was
semantically plausible but generated an extra four-byte local frame,
15 more machine-code bytes, and non-original callback sites.
The natural far stack-address expression instead produces **all
40 original CODE bytes** and exactly the original **three ordered OMF
FIXUPPs**: CODE+31 near __scanner, CODE+27 near __Nfgetc,
CODE+23 near __Nungetc. The original __scanner near-call requires
a TARGET frame (method5), whereas direct TASM attempts used a
CODE-segment frame (method0) despite identical CODE. Genuine BCC
emits the original TARGET frame and original import numbering.
The original public _fscanf at0, empty DATA/BSS and literal
08ff02ff03 DATA/BSS group also match.

The scoped builder uses the existing verified 31-source normal
MAINL library including complete xx, both qsort sorting bosses,
full scanner/scantol, original FILE fseek/ftell/getc/fread/fwrite,
path searching and CRT string functions. Only this new real BCC
source object is compiled twice at original CRT slot231.
**861 of893 other CRT member programs remain original.**
Two actual BCC/TLIB/TLINK rounds independently reproduce the complete
**67,372-byte decoded Japanese MAINL EXE and original MAP**,
with all **677 original MZ relocations**. The simultaneous
exact source-built scope rises to **19,872 CODE bytes across32 owners**.

The original accepted28-provider CRT, 211-owner formal accepted
MAINL publication, pinned candidate-local-attested Japanese target
and original cold pair remain unchanged. This is source-only
normal-link exactness, not newly credited accepted ledger bytes.
No full cold replay or DIET rebuilding was needed.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_fscanf_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_fscanf_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_fscanf_work

Complete two-run native OBJ/LIB/EXE/MAP vectors, tool command logs,
source/driver hashes and review receipts live under
.analysis/work/fscanf-* and mainl-fscanf-native-{build,review}.json.
