# Native DOS strlen and cumulative six-source MAINL CRT

`src/mainl/crt/strlen.asm` recovers the actual original DOS large-model far
cdecl `_strlen` function at original CRT member300. Its **33 original 8086
CODE bytes** compile exactly under TASM,without literal OMF fixups or
external symbols. The source also preserves the original `_TEXT` owner,
two zero-length `_DATA`/`_BSS` owners and literal BSS-before-DATA GRPDEF.

The original compares the incoming far pointer's segment and offset to
zero before scanning:if both are null,AX remains zero. Otherwise it
executes the original `CLD / REPNE SCASB` with CX=FFFF and returns
`~CX-1` in AX. This condition and the far pointer ordering matter even
though many modern strlen implementations omit the original null check.
No target machine-code bytes are embedded or patched.

The cumulative source-only CRT builder now replaces six genuine original
library members:memchr259,memcmp260,memcpy261,memset263,strcmp292 and
strlen300. Their complete native CODE totals **266 bytes**,with exact
pubdefs,segment ownership,zero ordered fixups and original group records.
The other **887 of893 native library member program records** remain
unchanged. Two real TASM/TLIB/TLINK rounds reproduce the entire original
**67,372-byte Japanese decoded MAINL EXE** and the exact original MAP,
with all **677 MZ relocation entries**. This is actual native source
reconstruction in a working library,not new published accepted ownership.
The accepted28-provider CRT,211-owner MAINL publication,cold pair and
pinned Japanese target remain unchanged.

Bounded reproduction,without full cold replay:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_crt_growth_work.py memchr-memset-strlen
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_crt_growth_work.py memchr-memset-strlen
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_crt_growth_work

The matching raw pairs and phase logs are retained under
`.analysis/work/crt-growth-memchr-memset-strlen-*` with build/review receipts.
