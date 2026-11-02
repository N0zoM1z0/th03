# Complete original DOS format scanner: 1,282 CODE + 128 initialized DATA

The original Borland MAINL CRT member scanner at library index109
is now recovered as maintained 16-bit 8086 source in
src/mainl/crt/scanner.asm. Its public near __scanner owns a
42-byte original stack frame, a callback-driven input/format
processor with width, assignment suppression, length modifiers,
literal/whitespace handling and numeric/string/character
conversion paths. It calls the real original __scantod,
__scantol, __scanpop and __scanrslt providers in the exact
original EXTDEF order. No original function CODE bytes are
embedded as DB arrays, and no binary OBJ patch is used.

The source has **523 actual 8086 instructions** in the first
1,238 CODE bytes. It then defines the original **22-entry
44-byte relocation-bearing near format-switch table** using
DW OFFSET of actual assembly control labels, not copied numeric
jump pointers. All 22 targets are verified against real
instruction boundaries. The original 128-byte _DATA segment
is separately encoded as **128 semantic ASCII format-character
classification entries** using named constants: default
characters, whitespace, percent, suppression star, digits,
numeric length bases, letters for integer/float/string/character
conversions, brackets and pointer/count conversions.
This is true program DATA, not a machine-opcode byte array.
BSS remains zero;the original BSS-before-DATA group is preserved.

Real TASM 5.0 produces exactly the fixed original:
- **1,282 / 1,282 CODE bytes**, all raw-equal;
- **128 / 128 initialized DATA bytes**, all raw-equal;
- **33 / 33 ordered OMF literal FIXUPPs**, all site,
  frame/target type/index, addend and writer order equal;
- one public __scanner at0, original four near imported
  scanner helpers, original _TEXT/_DATA/_BSS segments and
  literal GRPDEF 08ff03ff02.

These properties were verified rather than assumed from a
compiler/decompiler listing. The first TASM source generated
LIDATA records for repeated DATA-class values and changed the
OMF writer order of forward references. Replacing the repeated
initializer with individual **symbolic DATA classification
entries** restored real LEDATA,while defining the DATA owner
before emitting the CODE scanner allowed actual DS register
operations and original relocation frames. A zero-length
ORG $ source boundary just before the forward CODE dispatch
switch makes TASM emit the 33 native FIXUPPs in the literal
original chronological order. It **adds zero executable or
initialized bytes**, unlike filler or synthetic alignment.
The actual instruction/data bytes and original semantic
targets are unchanged;the local TASM LEDATA block boundaries
can legitimately differ from the original BCC object.

The scoped source-only builder inherits the previously verified
22-member CRT with complete xx, both full sorting bosses,
465-byte scantol and strspn/strcspn/strpbrk,then compiles
the complete scanner source twice and inserts it at genuine
member109 in the original893-member library. All **870 other
CRT member program records** are preserved byte-for-byte.
Two actual TASM/TLIB/TLINK rounds both produce the **entire
67,372-byte Japanese decoded MAINL EXE** and the complete
original native MAP raw-equal, with **677 ordered MZ
relocations**. The 23 naturally source-built original CRT
CODE segments now total **17,768 bytes**; this scanner also
adds a real source-exact 128-byte DATA owner.

This is assembler-level source reconstruction and a complete
normal-link proof,not a claim to possess the original historical
Borland C scanner source or to have formally accepted more
ledger units. The original28-provider accepted CRT,
211-owner published MAINL scope, fixed target provenance
candidate-local-attested and unchanged cold pair remain
frozen. The receipts report source_acceptance=false and
added_accepted_bytes=0. No full cold, DIET or ancestor
runtime chain was performed.

Affected-only commands:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_scanner_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_scanner_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_scanner_work

Retain .analysis/work/mainl-scanner-native-{build,review}.json,
both complete scanner-full-roundN native OBJ/LIB/EXE/MAP
raw vectors, original CRT/link responses and actual writer
phase logs. The complete original pinned Japanese target
is never overwritten.
