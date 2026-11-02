# Original DOS strcspn: exact 73-byte rejection-span source

The maintained 16-bit Borland far-cdecl source
src/mainl/crt/strcspn.asm reconstructs the complete original
CRT member294. It uses the original four-byte stack local to
scan a far rejection-set string anew for every input character.
Unlike the strspn accept-set helper, a matching byte immediately
returns the current count. The source preserves the 16-bit CX
counter, original text-first ES:BX comparison, near local frame,
far RETF and original unchecked pointer behavior.

Real TASM generates **73/73 original CODE bytes**, public
_strcspn at offset0, empty DATA/BSS, original DATA-before-BSS
GRPDEF 08ff02ff03, and no original external imports or FIXUPPs.
This exact mnemonic-based implementation was not assumed from
similar-looking C code: multiple real BCC4.5 C++ trials generated
different lengths/temporary spills or compared the two far
characters in the wrong instruction order.

The scoped TASM/TLIB/TLINK builder combines this full new source
with scantol, strspn, the complete exception/RTTI xx module,
both sorting bosses and the preceding CRT sources, retaining
**21 actual original source members** and **872 unchanged
library programs out of893**. Two independent native links
produce the **entire original Japanese 67,372-byte decoded
MAINL EXE** and its original MAP bit-for-bit, preserving
**677 original ordered MZ relocations**. Joint source-built
original CODE now totals **16,406 bytes**.

The pinned Japanese target, accepted28-provider CRT, formal
211-owner publication and original cold pair remain unchanged:
the source-only working library is exact but does not automatically
increase formally accepted ledger credit. No full cold replay
or canonical DIET rebuild was performed.

Affected scope:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_native_extension_work.py scantol-strspn-strcspn
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_native_extension_work.py scantol-strspn-strcspn
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_native_extension_work

Two complete raw source OMF/LIB/EXE/MAP rounds and the actual
TASM/TLIB/TLINK logs remain under .analysis/work/native-extension-*.
