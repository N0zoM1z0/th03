# Original DOS strncpy source and thirteen simultaneous CRT source members

The maintained src/mainl/crt/strncpy.asm restores all **49 bytes** of the
original DOS Borland large-model far-cdecl strncpy. It performs the
original bounded REPNE SCASB scan before copying with REP MOVSB and
zero-filling the remainder with REP STOSB. The source preserves the
original DS/ES transfers and DI/SI, plus the caller's far destination
as the DX:AX return. The original TASM opcode is XCHG CX,BX (not
the alternate equivalent XCHG BX,CX encoding).

The actual native object has one public _strncpy at offset0, CODE49,
empty DATA and BSS, the exact 08ff03ff02 BSS-before-DATA GRPDEF,
no imported symbols and no ordered OMF fixups. Every CODE byte,
public symbol and segment boundary is compared to the original
Japanese vendor object;there is no target byte table or patch.

The scoped builder reuses the previously verified twelve-source CRT
working library including complete xx (12,622 bytes),signed/unsigned
integer conversion and stateful strtok. It replaces original library
member304 with the independent real TASM strncpy object and preserves
all880 other original member programs. Two complete real TASM/TLIB/TLINK
rounds reproduce the **entire 67,372-byte decoded Japanese MAINL EXE**
and original MAP byte-for-byte,with all677 MZ relocations. Thirteen
native source members now supply **13,832 exact CODE bytes**.

The accepted28-provider CRT and211-owner MAINL publication are
unchanged. This is a source-only normal-link reconstruction,not
automatic newly published ledger credit. No full cold or DIET replay.

Affected-only checks:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_crt_expand_work.py strncpy
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_crt_expand_work.py strncpy
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_crt_expand_work

The complete two raw native OBJ/LIB/EXE/MAP vectors are retained under
.analysis/work/crt-next-strncpy-*,with the current source-bound
mainl-crt-expand-strncpy-{build,review}.json receipts.
