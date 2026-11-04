# Japanese MAINL original PC-98 screen text read/write: `cibmgptx`

The **selected original** Japanese Borland CRT member **525**, `cibmgptx`,
exports three whole PC-98 screen routines at original CODE offsets:
`___ibm_gettext` +0, `___ibm_puttext` +227 and
`___ibm_getputtextsize` +527. The recovered
`src/mainl/crt/cibmgptx.asm` implements all **554 original CODE bytes** as
ordinary symbolic 8086 instructions. It restores text-buffer addressing,
rectangle validation, DBCS trail checks, cursor state, screen-fill and VRAM
operations, and original near dependencies on the already recovered
`cibmscrn` / `cibminit` / `cibmputn` family, with no executable machine-byte
initializer arrays or post-assembly OBJ edits.

Native TASM `/m /mx /kh32768 /t` reproduces **554/554 CODE bytes**, original
PUBLIC offsets, all ten ordered EXTDEF dependencies, empty DATA/BSS and the
original `08ff03ff02` DGROUP. All **25/25 original OMF FIXUPP fields also
match literally in original record order**, including sites, targets, frame
methods, addends, widths and relocation kinds. This assertion applies to
the actual FIXUPP records, not unexamined OMF record classes.

`build_th03_mainl_after133_work.py cibmgptx` replaces the real selected CRT
slot on the retained Japanese 133-source native carrier in **two independent
TASM/TLIB/TLINK rounds**, both reproducing the complete original
**67,372-byte decoded Japanese MAINL EXE and MAP byte-for-byte** with **677
MZ relocations**. Original 759 contextual vendor CRT program records remain
unchanged; working source expands to **134 members / 63,456 original-equal
CODE bytes**. There was no cold replay, and no formal accepted-ledger credit
is claimed.

## Ancestor verification improvement

A naive nested review on 133-source timed out after its two successful native
link rounds. The scoped builder now audits **all 62→133 source-bound receipts
once in topological order**, verifying original member positions, native raw
OBJ/LIB/EXE/MAP pairs, source/driver/parent hashes, original CODE/DATA/ABI,
recorded Borland writer logs, and the entire original Japanese EXE/MAP at
every layer. The audit takes seconds, not a repeated exponential chain. Two
new build rounds were then rerun with the **current driver hash**, rather
than changing or forging old receipt hashes.

Review using `review_th03_mainl_after133_work.py cibmgptx` and
`tests.test_mainl_after133_work`. Two raw native output vectors, exact source
binding and real writer logs remain under `.analysis/work/after133-*` and
`.analysis/work/mainl-after133-*`.
