# Japanese TH03 full `istrstream` / `ostrstream` constructor family

The actual selected original Borland CRT members **746 `isrctr1`** and
**800 `osrctr1`** are now complete native C++ 16-bit source. `isrctr1` owns
**1,001 CODE + 28 initialized DATA bytes** and three far public constructor
entries at CODE+0/+187/+374. `osrctr1` owns **1,211 CODE + 28 DATA bytes**
with three far public entries at +0/+257/+514. Both original `_TEXTA/_DATA/_BSS`
segments, the `08ff02ff03` DGROUP, and 11/12 ordered EXTDEFs are preserved.

The real source files `src/mainl/crt/isrctr1.asm` and `osrctr1.asm` reconstruct
all six distinct original far constructor bodies as **genuine symbolic 8086
instructions**: allocation, `ios` base construction, `strstreambase` and
`istream` / `ostream` setup, string buffer pointer ownership, proper C++
reference/destructor registration, and original `ostrstream` string-length
handling. The CODE regions +561 onward (`isrctr1`) and +771 onward (`osrctr1`)
are original **non-executable Borland class RTTI/destructor metadata** with
six class names each and typed relocatable far-pointer descriptors, not
machine-code byte arrays. Each 28-byte DATA section is also recovered as
original typed unwind pointers and descriptor fields, not arbitrary padded
source. All six original public names/offsets were obtained from the selected
Japanese library program records, not previous guesses.

A real 8086 ABI trap in the `ostrstream` source required three explicit
**far virtual calls** at original CODE+221/+478/+735. Untyped `call [bx+1Ch]`
compiled to near `FF /2`; restoring `call dword ptr [bx+1Ch]` yields the
original `FF 5F 1C` in all three constructor bodies without patches.

Normal TASM 5.0 `/m /mx /kh32768 /t` reconstructs the **complete 2,212/2,212
original CODE bytes and 56/56 initialized DATA bytes**, all six PUBLICs,
ordered external dependencies and original segment identities. **All 89 OMF
relocations (43 + 46)** match the original sites, kinds, target methods,
addends and **frame methods**, including references in CODE RTTI and DATA
exception tables. Literal native FIXUPP *record ordering* differs between
BCC and TASM, so original complete OBJ serialization equality is **not**
claimed. No copied executable CODE byte arrays, byte patches or artificial
CODE padding were used.

`scripts/build_th03_mainl_after151_work.py strstream-constructors` inherits
the fully source-bound original Japanese 151-source CRT and recompiles only
these two real member slots in **two independent TASM/TLIB/TLINK rounds**.
Both reproduce the **entire original 67,372-byte decoded Japanese MAINL EXE
and MAP byte-for-byte**, with all **677 ordered MZ relocations** and **740
untouched original vendor member programs**. Working CRT now has **153
source-built members / 70,118 original-equal CODE bytes**. This is working
source reconstruction, not formally accepted-ledger credit. No full cold
replay was run.

Proof: `review_th03_mainl_after151_work.py strstream-constructors`,
`tests.test_mainl_after151_work`, raw native OBJ/LIB/EXE/MAP pairs, phase logs
and source-hash-bound receipts under `.analysis/work/after151-*` and
`.analysis/work/mainl-after151-*`.
