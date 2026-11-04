# Original Japanese `filebuf` C++ constructors and virtual table

The genuinely selected Borland CRT members **708 `fsbctr1`** and **709
`fsbctr2`** contain two distinct complete far `filebuf` constructors,
exporting `@filebuf@$bctr$qv` and `@filebuf@$bctr$qi`. Their code is **359
+ 360 = 719 original bytes**, with **52 initialized DATA bytes each**, zero
BSS, and 19 ordered C++ imports per member.

`src/mainl/crt/fsbctr1.asm` and `fsbctr2.asm` are fully symbolic 8086
sources implementing original far object allocation, `streambuf` base
construction, buffer allocation/`setb`/`setp`/`setg`, reference destructor
registration, and native far return ABI. The remainder of CODE after
+233/+234 is original **non-executable** class RTTI, including `filebuf`
and `streambuf` strings and typed far destructor pointers. Original 52-byte
DATA sections contain the full filebuf **virtual method table** with 12
relocations, expressed as symbolic `dw`/`dd` entries, not copied bytes.
There are no executable machine-code arrays, artificial size padding or
patched native objects.

Independent normal TASM `/m /mx /kh32768 /t` reconstructs **all 719 CODE
and 104 DATA bytes**, the exact original `_TEXTA/_DATA/_BSS` layout and
DGROUP, all publics and ordered imports, and **46/46 original OMF fixups**
at exact sites, types, targets, addends, widths and frame methods. The
original compiler and TASM still serialize these fields in different record
order; literal whole-OBJ identity is **not** claimed.

`build_th03_mainl_after202_work.py filebuf-constructors` starts from the
source-bound original **202-source** Japanese CRT and replaces the two real
selected slots. **Two independent native TASM/TLIB/TLINK rounds** both
reproduce the complete original **67,372-byte decoded Japanese MAINL EXE
and full MAP byte-for-byte**, preserving **677 original MZ relocations** and
**689 untouched vendor CRT member programs**. Working source grows to
**204 members / 84,901 original-equal CODE bytes**. This does not grant
formal accepted-ledger credit. No full cold replay was performed.

Review using `review_th03_mainl_after202_work.py filebuf-constructors`,
`tests.test_mainl_after202_work` and source-hash-bound native OBJ/LIB/EXE/MAP
rounds and real Borland writer logs under `.analysis/work/after202-*`.
