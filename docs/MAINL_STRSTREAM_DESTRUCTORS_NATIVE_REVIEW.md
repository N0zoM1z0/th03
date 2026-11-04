# Original Japanese C++ `istrstream` / `ostrstream` destructors and RTTI

Two genuinely selected Borland large-model CRT members now have complete
symbolic 16-bit 8086 source in `src/mainl/crt/isrdtr.asm` (original member
**748**) and `osrdtr.asm` (original member **802**). Each recovers **579 CODE
bytes + 28 initialized DATA**, one original far C++ destructor PUBLIC at
CODE+0, seven original ordered imports and the original `_TEXTA/_DATA/_BSS`
segments with `08ff02ff03` DGROUP.

Each module's *executable* destructor is a complete 139-byte 8086 function
that unregisters C++ exception ownership, restores `streambuf`/`istream` or
`ostream`/`ios` state, tears down the `strstreambase`, and frees the original
far object conditionally. The remainder of CODE at +139..578 is **actual
non-executable Borland C++ class RTTI and destructor metadata**, with six
class names (`istrstream` / `ostrstream`, `ios`, `istream` / `ostream`,
`strstreambase`, `strstreambuf`, `streambuf`), typed `dw` descriptor fields
and symbolic far `dd` entries. Each 28-byte DATA segment is an original
unwind/destructor pointer record. Neither source contains copied executable
machine CODE arrays, arbitrary padding nor patched native OBJ bytes.

Native TASM 5.0 `/m /mx /kh32768 /t` independently reconstructs **all
579+579 = 1,158 original CODE bytes** and **28+28 = 56 DATA bytes**, original
public/EXTDEF identities and segment layout, and **54/54 real OMF relocated
fields (27 in each)** matching site, target, kind, addend, width and original
**frame method**. Only the literal BCC-versus-TASM FIXUPP record *order*
differs; no claim of complete byte-identical original OMF OBJ serialization.

The recovered destructors now join the already source-built six complete
`istrstream`/`ostrstream` constructors to preserve both sides of the
Borland C++ stream-object lifecycle. Actual source-bound product proof:
`scripts/build_th03_mainl_after153_work.py strstream-destructors` recompiles
both slots against the retained original Japanese **153-source CRT**, and
performs two independent normal TASM/TLIB/TLINK rounds. Both reproduce the
**complete original 67,372-byte decoded Japanese MAINL EXE and MAP byte-for-
byte**, all **677 original ordered MZ relocations**, and retain the other
**738 unchanged vendor CRT program records**. Working source reaches **155
members and 71,276 original-equal CODE bytes**. This does *not* grant formal
accepted-ledger credit or imply full program source ownership; no cold replay.

Verifier: `review_th03_mainl_after153_work.py strstream-destructors`,
`tests.test_mainl_after153_work`, two raw OBJ/LIB/EXE/MAP rounds and actual
compiler/linker phase logs under `.analysis/work/after153-*`, and source /
parent / driver-hash-bound receipts `.analysis/work/mainl-after153-*`.
