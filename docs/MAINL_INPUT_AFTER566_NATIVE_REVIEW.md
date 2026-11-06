# MAINL held-key scanner: full natural TASM source and true EVEN (after566)

The previous after549 417-byte PC-98 input scanner candidate was not adopted
because the next native byte at the original address was 90h; omitting it
changed every subsequent link coordinate. The original first-use Turbo C++
module had an explicit codestring trailer, which was not a satisfactory
natural-source explanation.

The after565 MAIN reconstruction identified that byte as a normal
word-aligned CODE boundary. Its natural source TU
src/main/hardware/input_scan.asm contains all 115 original 8086
instructions (417 bytes), symbolic references and named control-flow labels,
followed by TASM 5.0 EVEN. The assembler itself emits the 90h CODE NOP.
There is no handwritten target-code array, NOP padding directive, binary
patch, or claim that the byte is an additional instruction.

MAINL now uses a maintained forwarding translation unit
src/mainl/hardware/input_scan_exact.asm to build that proved common scanner
independently for the MAINL product. This cross-product source equivalence
is backed by complete native object and final-link comparisons, not
just by similar C++ semantics.

## Original MAINL source and OMF evidence

The native TASM emitter produces 418 initialized CODE bytes. All 418 bytes
match the original contextual MAINL object exactly, including the naturally
generated last 90h. All four external mutable keyboard-state symbols, the
far input entrypoint, all 42 original OMF fixup sites and the original
CODE/DATA/BSS segment lengths agree. The held-key function itself ends at
its RETF at offset416; the final byte is a distinct assembler alignment.

Because this is a natural sequential assembler TU, TASM's packet-level
OMF FIXUPP order does not reproduce the original historical Turbo C++
emitter's order. Neither the complete original OMF stream nor historical
assembler/compiler identity is claimed. However, the final **ordered MZ
relocation stream** is checked completely and does match.

## Two complete original EXE links

In two independent TASM/TLINK native rounds, after558's real source C0,
CRT, root DATA/C++, text/picture banks, vector and sound C/C++ objects
were reused unchanged. Only the old input project object was replaced.
Every output file and writer log from both rounds has been retained.

Each round exactly reproduced the complete **67,372-byte Japanese decoded
MAINL EXE**, including every one of its **677 ordered MZ relocations**.
All original MAP contribution lengths and locations agree. The sole MAP
text difference is the new assembler module's filename.

The original stored DIET MAINL target is a separate 37,975-byte file.
No DIET repacking or complete native cold replay was done for this
local source-bound substitution; no new canonical stored-unit or full
source-project acceptance is asserted.

Local affected native verification:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_mainl_input_after566_work.py

Native builder: scripts/build_th03_mainl_input_after566_work.py
Retained root: .analysis/work/mainl-input-after566-native-build.json
Review: .analysis/work/mainl-input-after566-native-review.json

This resolves the old unowned byte source/layout question for the complete
MAINL input producer; it does not promote previously unpublished source
units or alter the older after554 canonical publication.
