# Original DOS splitpath/fnsplit: complete 850 CODE and 47-source MAINL

The original Japanese Borland CRT splitpth (member286) now has
maintained native 8086 assembler source in
src/mainl/crt/splitpth.asm. It owns two private near
Pascal helpers (92 and122 CODE bytes), the public far
___fnsplit at CODE+230, and public far __splitpath at
CODE+804. The actual path parser handles bounded far
component copying, Japanese DBCS-aware separator tests,
drive, directory, filename and extension extraction, and
the original caller-provided output pointers. It uses
genuine Borland far _strcpy, _strlen, _strncpy and
___path_issbcs provider imports in the original order.

There are two *genuine immutable lookup tables inside the
original CODE segment*, rather than distinct initialized
_DATA. The first, at CODE+214 through229 (16 bytes),
contains four slash/drive character WORD classes and
four symbolic local switch targets. The second, at
CODE+776 through803 (28 bytes), contains seven path
punctuation WORD classes and seven symbolic dispatch
targets. The maintained source encodes these as semantic
WORD character constants and DW OFFSET named branches:
they are not original executable opcode arrays or
hand-patched segment offsets. All remaining 806 CODE bytes
are real 8086 instructions in four original executable
regions of 92,122,546 and46 bytes. The two tables plus
those instructions cover **every one of the 850 original
CODE bytes**, without gaps or added alignment.

Actual Borland TASM 5.0 generates the entire **850/850
original CODE** byte stream, correct public offsets
230/804, all four import indices, zero DATA/BSS and
literal 08ff02ff03 group. Crucially **all 20 literal
ordered original OMF FIXUPPs** also match their original
record order, site, 16-bit/32-bit field kind, frame,
target, index and addend. Eleven of these are original
CODE-segment TARGET-framed switch table words (four at
222..228, seven at790..802). The other fields include
local CODE offsets and the genuine far string/
DBCS helper calls. Disjoint mnemonic source blocks
are positioned at actual instruction and WORD-table
boundaries so native TASM preserves the original
descending OMF emission order; no DB byte arrays
representing executable code are used.

The scoped source builder replaces splitpth at its real
original library slot286 alongside the **46 previously
reconstructed source CRT modules**, including full xx,
both quicksort bosses, the full directory subsystem,
974-byte buffered putc and DOS/CRT string and file
helpers. The other **846 of893 original library member
program records remain byte-identical**. Two independent
genuine TASM/TLIB/TLINK rounds recreate the complete
**67,372-byte original decoded Japanese MAINL EXE and
MAP bit-for-bit**, with all **677 ordered MZ relocations**.
Across 47 true source CRT modules, **24,627 original CODE
bytes** are emitted in a simultaneously exact source-only
working link.

The earlier fopen literal OMF field ordering and fclose
near-frame metadata gaps remain explicitly open in
their separate predecessor modules. The complete
47-source linked EXE/MAP is byte exact, but that does
not assert all 47 raw OMF metadata vectors equal the
original. Splitpth itself is original-complete in CODE,
imports, native public/owner geometry and ordered FIXUPPs.
The accepted28-provider CRT and211-owner formal MAINL
publication are frozen; original target provenance
remains candidate-local-attested, and no full cold or
DIET replay was run.

Affected-only reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_splitpth_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_splitpth_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_splitpth_work

Original two-round OBJ/LIB/EXE/MAP output vectors and
native phase logs remain under .analysis/work/splitpth-*,
with build/review receipts bound to source and original
target hashes.
