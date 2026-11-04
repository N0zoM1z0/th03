# Japanese TH03 CRT: complete iostream and iostream_withassign destructors

Original selected Borland CRT slots **744 `iostdtr1`** (**433 CODE**) and
**745 `iostdtr2`** (**501 CODE**) now have entire symbolic 8086 source.
Each has **28 original initialized DATA bytes**, zero BSS, and one original
far C++ destructor PUBLIC at CODE+0, with 5/6 ordered imported dependencies
and authentic `_TEXTA/_DATA/_BSS` layout in `08ff02ff03` DGROUP.

The source files reconstruct the entire native `iostream` and
`iostream_withassign` destructor routines, including real `ios`/
`istream`/`ostream` ownership, exception unwinding, virtual base release,
reference accounting and far delete semantics. After the `RETF` in each
member there are **two genuine executable 12-byte far adjustment thunks**.
These are real 8086 `mov`, stack `add`, and far `EA` jump instructions.
`ASSUME CS:NOTHING` prevents TASM from shortening self-referential far
jumps to near `E9` calls. Subsequent nonexecutable Borland class RTTI
contains original class-name strings and symbolic `dw`/`dd` destructor
pointers; 28-byte DATA contains original typed far unwind entries.
No copied executable target CODE byte arrays, artificial padding or
post-assembly OBJ patches are present.

TASM `/m /mx /kh32768 /t` reproduces **934/934 original CODE** and **56/56
DATA** bytes, both original far publics, original ordered imports and
**48/48 OMF relocation sites, kinds, targets, addends and frame methods**.
BCC and TASM serialize their FIXUPP fields in different record order;
original full OMF OBJ byte identity is **not** claimed.

`build_th03_mainl_after304_work.py iostream-destructors` extends the
source-bound **304-source Japanese CRT** and rebuilds only two actually
selected original slots in two independent normal TASM/TLIB/TLINK rounds.
Both reconstruct the **entire original 67,372-byte decoded Japanese MAINL
EXE and MAP byte-for-byte**, preserving all **677 original MZ relocations**
and **587 untouched original vendor CRT program records**. Working native
source now spans **306 selected members / 102,315 original-equal CODE bytes**.
These are working-source proofs, not formal accepted-ledger credit or
whole-game source completion. No full cold replay was run.

Proof: `review_th03_mainl_after304_work.py iostream-destructors`,
`tests.test_mainl_after304_work`, retained raw OBJ/LIB/EXE/MAP pair,
source/driver/parent hashes and actual native writer phase logs under
`.analysis/work/after304-*` and `.analysis/work/mainl-after304-*`.
