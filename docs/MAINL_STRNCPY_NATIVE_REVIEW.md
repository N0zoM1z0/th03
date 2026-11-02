# Original DOS strncpy native exact source in the 13-source MAINL carrier

The maintained src/mainl/crt/strncpy.asm implements the original Borland
large-model counted string copy,including its original count-limited
REPNE SCASB scan,far DS/ES transfer,REP MOVSB and REP STOSB zero fill.
It preserves the original far cdecl stack/return DX:AX and source/buffer
behavior,without adding guards or embedding target opcodes in data.

Actual TASM compilation produces all **49 original CODE bytes** exactly,
one public _strncpy at offset0,zero native FIXUPPs,empty DATA/BSS and the
original literal BSS-before-DATA segment group 08ff03ff02.

The dedicated native CRT expansion builder reuses the complete exact
twelve-source MAINL carrier,extracts all893 original library members,
replaces just the original strncpy member at304 alongside those
twelve previous genuine sources,and performs two actual TASM/TLIB/TLINK
rounds. All **880 unchanged original member program records** agree.
Both rounds generate the complete original **67,372-byte Japanese decoded
MAINL EXE** and native MAP raw-equal,with all677 original relocations.
The current source-built CODE total is **13,832 bytes**.

This is reproducible natural source evidence,not accepted ledger promotion.
The accepted28-provider library and formal211-owner MAINL publication
remain frozen;no cold/DIET replay or ancestor runtime pipeline was run.

Focused reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_crt_expand_work.py strncpy
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_crt_expand_work.py strncpy
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_crt_expand_work
