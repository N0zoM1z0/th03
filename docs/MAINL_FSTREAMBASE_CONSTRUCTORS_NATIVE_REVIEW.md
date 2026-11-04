# Japanese MAINL: four full Borland `fstreambase` constructors

Recovered actual selected CRT slots **719–722**, `fsctr1` (421 CODE),
`fsctr2` (444), `fsctr3` (424) and `fsctr4` (433), with 20 initialized
DATA bytes each and zero BSS. These implement all four original far C++
`fstreambase` constructor overloads, owning the native `ios` and `filebuf`
base state, heap/reference bookkeeping, and exception cleanup. Each
`src/mainl/crt/fsctr*.asm` uses genuine symbolic 8086 instructions, not
embedded executable machine-code arrays, patches or size padding.

Crucially CODE contains **an executable 12-byte far destructor adjustor**
after each constructor's `RETF` before original non-executable Borland RTTI.
The adjustor is expressed as `mov bx,sp`, `add word ptr ss:[bx+4],...`,
and `jmp far ptr @fstreambase@$bdtr$qv`. Four genuine class names
(`fstreambase`, `filebuf`, `ios`, `streambuf`) and typed symbolic `dw`/`dd`
RTTI follow. Original 20-byte DATA sections carry real far exception
cleanup pointers; all original ordered imports and PUBLIC offsets survive.

Independent TASM 5.0 `/m /mx /kh32768 /t` reproduces **1,722/1,722 original
CODE bytes**, **80/80 DATA bytes**, actual selected segment structure and
**73/73 OMF relocations at their original sites, targets, types, addends and
frame methods**. Original BCC FIXUPP record ordering differs from TASM,
so complete byte-identical OMF OBJ serialization is **not** claimed.

`scripts/build_th03_mainl_after252_work.py fstreambase-constructors`
extends the source-bound original **252-member Japanese CRT** in two
independent normal TASM/TLIB/TLINK rounds. Both reconstruct the **entire
original 67,372-byte decoded Japanese MAINL EXE and original MAP byte for
byte**, preserving **677 ordered MZ relocations** and **637 untouched
vendor CRT member programs**. Working-source CRT reaches **256 members
and 95,192 original-equal CODE bytes**. No full cold replay ran, and
no accepted-ledger credit is asserted.

Proofs: `review_th03_mainl_after252_work.py fstreambase-constructors`,
`tests.test_mainl_after252_work`, source-bound OBJ/LIB/EXE/MAP pair and
actual native writer logs in `.analysis/work/after252-*`.
