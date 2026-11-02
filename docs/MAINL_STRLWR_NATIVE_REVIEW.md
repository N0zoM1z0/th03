# Exact DOS strlwr: 38-byte native source and 49-source Japanese MAINL

The maintained src/mainl/crt/strlwr.asm is the complete original
Borland DOS large-model far-cdecl strlwr implementation at CRT
member301. It temporarily loads DS:SI from the original far string,
uses actual LODSB to scan, transforms ASCII A..Z in-place while
preserving the original NUL termination, and returns its original far
pointer in DX:AX after restoring DS/SI/DI. This retains the original
unchecked behavior without extra C-library wrappers or guards.

The native TASM object reproduces **all 38 original CODE bytes**,
the single public _strlwr at offset0, zero imports and zero OMF
FIXUPPs, empty DATA/BSS and literal BSS-before-DATA group
08ff03ff02. No original executable byte array or artificial
alignment is needed; the original instruction and register encodings
come from typed mnemonic source.

The scoped builder inherits the previous 48-source working CRT,
including the full 820-byte two-function DOS/Unix time converter,
whole xx, sorting bosses, scanner and file/path routines. It replaces
strlwr at original member301 in the actual 893-program CRT, leaving
**844 original member program records** byte-identical. Two genuine
TASM/TLIB/TLINK rounds independently reconstruct the entire original
**67,372-byte decoded Japanese MAINL EXE** and native MAP byte for
byte, with all **677 original MZ relocation entries**. The current
49-source working library emits **25,485 exact original CODE bytes**.

The inherited timecvt near-TARGET-frame, fopen OMF field-order and
fclose near-frame differences remain explicitly open. The accepted
28-provider CRT, 211-owner formal MAINL ledger, original Japanese
target and cold pair remain unchanged. These source-only normal-link
receipts are not formal accepted byte credit. No full cold or DIET
replay was run.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_posttimecvt_work.py strlwr
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_posttimecvt_work.py strlwr
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_posttimecvt_work

The two complete native source OBJ/LIB/EXE/MAP vectors, source-bound
proof receipts and writer phase logs remain under
.analysis/work/posttimecvt-strlwr-*.
