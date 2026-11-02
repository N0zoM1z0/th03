# Native DOS scantol: complete 465-byte integer-scanning source

The original Borland CRT integer scanner at library member110 is now
maintained as natural 16-bit 8086 assembler source at
src/mainl/crt/scantol.asm. This is the actual provider used by the
previously reconstructed signed/unsigned strtol and strtoul adapters,
not just a character-conversion leaf.

The first 47 CODE bytes form a private near digit-for-radix helper,
taking a character in BL and radix in CL. A valid digit returns BX
and clears carry;invalid input sets carry. The unusual original
two INC SP instructions drop saved BX on the successful path.
The next 418 bytes are the real public near __scantol at CODE+47:
it preserves whitespace/sign handling, base inference and explicit
radix, 16/32-bit multiplication/addition, overflow saturation,
input and unget callbacks, and the far count/status outputs.

Actual TASM5 generates **all465 original CODE bytes**, its
one public __scantol at47, the sole __ctype external, empty
DATA/BSS and exact BSS-before-DATA OMF group 08ff03ff02.
Crucially the only literal OMF FIXUPP at CODE site95 is identical:
a segment-relative 16-bit offset with **TARGET-frame method5**,
external target1 and addend1. Placing the external declaration
inside CODE generated an otherwise identical instruction stream
but the incorrect segment-frame method0. Moving the declaration
before the CODE SEGDEF restores original native field identity
without patching OMF. One equivalent XCHG operand-order choice
also had to be restored as an actual source instruction.

The scoped builder reuses the complete prior 18-source working CRT
with both sorting bosses, the full xx exception/RTTI runtime and
the signed/unsigned integer adapters. It compiles this source twice,
preserves **874 of893 other original CRT member programs** and
runs actual TASM/TLIB/TLINK twice. Both rounds reproduce the
**complete 67,372-byte original Japanese decoded MAINL EXE**,
its native MAP and all **677 original MZ relocations** byte-for-byte.
The exact joint source CODE scope is **16,251 bytes in19 members**.

This is natural assembler-level original source recovery, not
rediscovery of historical Borland C code. The original accepted
28-provider CRT and211-owner published MAINL ledger remain
frozen. No new formally accepted source credit, cold replay or
DIET rebuild is claimed.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_native_extension_work.py scantol
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_native_extension_work.py scantol
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_native_extension_work

Private source-bound build/review receipts and two complete native
OBJ/LIB/EXE/MAP vectors are in .analysis/work/mainl-native-extension-scantol-*
with the original real phase logs and fixed Japanese target.
