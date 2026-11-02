# MAINL original DOS memcmp and combined source-only CRT reconstruction

The 8086 translation unit src/mainl/crt/memcmp.asm reconstructs the
original Japanese CRT library member at index260 (zero-based). It uses
far cdecl parameters: first far pointer, second far pointer, then WORD
length. The routine saves/restores DS, skips dereferencing either pointer
for a zero count, compares forward with CLD/REPE CMPSB and returns the
unsigned difference of the final compared bytes in AX. The routine leaves
the original unchecked behavior unchanged.

The native TASM output has **40 CODE bytes** identical to the original
vendor/memcmp.obj, one public _memcmp, no external symbols, zero literal
fixups, and original empty DATA/BSS segments. Declaring DGROUP before
the empty segments restores the original BSS-then-DATA OMF GRPDEF
sequence, required for the complete linked MAP owner list.
These are semantic assembler instructions, not a target-byte array or
binary patch.

The paired native test reuses the independently validated earlier
memcpy.asm source and its two-round retained library. Original members
260 and261 are replaced with native memcmp and native memcpy at their
original positions; **all891 other members** retain their original
program records. Two real serialized TASM/TLIB/TLINK rounds rebuild only
the affected CRT source member and link all original36 project objects,
startup and runtime inputs. Both outputs match the **entire67,372-byte
decoded Japanese MAINL EXE** and its **entire MAP** byte-for-byte.
All677 MZ relocation entries are present. The two raw OBJ/LIB/EXE/MAP
vectors repeat.

This is bounded native-source equality for two distinct CRT units inside
a real exact product link, not an extra published source owner. The accepted
211-owner MAINL publication and28-provider accepted library remain unchanged.
No full cold replay, canonical DIET recompression, or ancestor runtime
sequence was performed. The target provenance is candidate-local-attested.

Reproduce the affected code:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_memcmp_combo_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_memcmp_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_memcmp_work

Keep scoped reports .analysis/work/mainl-memcmp-combo-{build,review}.json,
the memcmp-combo-roundN-* complete raw outputs and native phase logs, and
the retained original native memcpy source-only proof pair.
