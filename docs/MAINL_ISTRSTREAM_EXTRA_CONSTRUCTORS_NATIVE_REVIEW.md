# Original Japanese `istrstream` three extra far constructors (`isrctr2`)

Selected original Borland CRT member **747**, `isrctr2`, is not the previously
recovered distinct `isrctr1` member. It owns **1,016 original `_TEXTA` CODE
bytes**, **28 initialized DATA**, zero BSS and three distinct far public
constructor overloads at CODE+0/+192/+384, with the original 11 ordered
C++ imports and `08ff02ff03` DGROUP.

The new real source `src/mainl/crt/isrctr2.asm` reconstructs all three
far `istrstream` constructor implementations as **213 ordinary 8086
instructions**, preserving the original `ios` / `istream` /
`strstreambase` allocation, buffer initialization, reference cleanup,
exception destructor tracking and far calling conventions. The following
CODE+576..1015 region is *non-executable* Borland class RTTI and unwind
metadata: six genuine class names and typed `dw`/`dd` far pointers, not
copied executable machine-code arrays. The genuine 28-byte DATA contains
relocated C++ unwind fields rather than artificial target-sized padding.

Normal TASM 5.0 `/m /mx /kh32768 /t` reproduces **1,016/1,016 CODE bytes
and 28/28 DATA bytes**, the exact original segment names/classes, all three
publics and 11 ordered externs. All **43/43 original OMF fixups** agree at
their exact original site, type, target, addend and **frame method**, including
both CODE RTTI and DATA exception records. Original BCC/TASM FIXUPP *record
order* still differs, so complete literal original OMF identity is **not**
claimed; no generated OBJ patching, machine-byte source table or filler.

`scripts/build_th03_mainl_after201_work.py istrstream-more-constructors`
extends the source-bound **201-source** Japanese CRT at real library slot 747
in two independent normal TASM/TLIB/TLINK rounds. Both reproduce the
**complete 67,372-byte decoded Japanese MAINL EXE and original MAP byte-for-
byte**, with all **677 ordered original MZ relocations** and all **691 other
vendor member programs unchanged**. Working source reaches **202 modules
and 84,182 original-equal CODE bytes**. This is working source evidence,
not formally accepted-ledger credit; no full cold replay was performed.

Review: `review_th03_mainl_after201_work.py istrstream-more-constructors`,
`tests.test_mainl_after201_work`, and source-hash-bound raw native OBJ/LIB/
EXE/MAP vectors and writer phase logs under `.analysis/work/after201-*`.
