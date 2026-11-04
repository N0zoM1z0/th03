# Japanese MAINL `istelng`: original 1,439-byte C++ integer-input boss

The selected original Borland CRT member is **766**, `istelng`, exporting
`@istream@$brsh$qml` at CODE+811. Its entire **1,439-byte `_TEXTA` CODE**
contains three preceding integer conversion routines plus the far public
`istream` input entry, preserving four complete internal control-flow
regions and the original near/far streambuf ABI. The other two native segments
are empty `_DATA` and `_BSS`, with `_BSS,_DATA` DGROUP.

`src/mainl/crt/istelng.asm` contains 507 genuine 8086 instructions and
symbolic branch labels rather than copied CODE bytes or ABI-substituted
C++ wrappers. It retains sign parsing, decimal/octal/hex digit scans, `__ctype`
classification flags, far `ios::clear`, `streambuf::do_snextc`, and
`istream::ipfx`, and the original far long multiply/shift helpers
`F_LXMUL@` and `F_LXLSH@` (six ordered original imports). Explicit
`dword ptr es:[...]` on all 35 original nested far `LES` operations preserves
the selected native instruction sequence without a binary object patch.

**Native proof:** original selected member source TASM `/m /mx /kh32768 /t`
reproduces **1,439/1,439 CODE bytes**, the original `_TEXTA/_DATA/_BSS`
segments and one C++ public offset, and **19/19 original OMF FIXUPP locations,
widths, targets, addends and even frame methods** (including `__ctype`
GROUP-frame references). Original BCC and native TASM serialize these
fixups in different **record order**; complete original OMF object identity
is **not** claimed from equivalent binary/link results.

`build_th03_mainl_after116_work.py istelng` starts from the fully verified
**116-source original Japanese MAINL CRT** and replaces only original member
766 in two independent normal TASM/TLIB/TLINK rounds. Both produce the
**complete original 67,372-byte decoded Japanese MAINL EXE and original MAP
byte-for-byte**, preserving **all 677 ordered MZ relocations** and **776
untouched original vendor member program records**. The working source CRT
reaches **117 members and 55,809 original-equal CODE bytes**. This is
source-only evidence, not an accepted-ledger promotion or whole-source
ownership. No complete cold replay ran.

Verifier: `review_th03_mainl_after116_work.py istelng` and
`tests.test_mainl_after116_work`. Native OBJ/LIB/EXE/MAP vectors,
source-hash-bound receipts and actual writer logs are retained under
`.analysis/work/mainl-after116-*` and `.analysis/work/after116-*`.
