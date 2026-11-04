# TH03 original C++ `ostream::outstr`: complete 815-byte output core

The selected Borland CRT member **818**, `ostoutst`, owns the entire
**815-byte `_TEXTA` CODE segment**, with the original far C++ public
`@ostream@outstr$qnxct1` at offset +0. Its empty `_DATA/_BSS`, original
`08ff02ff03` GROUP and five ordered imports (`ios::setstate`,
`streambuf::sputn`, `ostream::do_opfx`, `ostream::do_osfx`, `_strlen`)
are preserved. This is the genuine output core used by the previously
reconstructed long-integer formatter `ostint`, not an equivalent libc wrapper.

`src/mainl/crt/ostoutst.asm` reconstructs all original 280 8086
instructions with symbolic branches and original far C++ calling ABI.
It preserves sentry/prefix and suffix calls, string length and width,
streambuf write/padding, `ios` error-state propagation and the
**three real virtual far indirect calls** at CODE+218/+463/+708, encoded
by natural `call dword ptr [bx+18h]` instructions. No executable byte
arrays, artificial padding or post-assembly object patches were used.

Normal TASM `/m /mx /kh32768 /t` reproduces all **815/815 original CODE
bytes**, original segments/public/EXTDEFs and **11/11 OMF relocation
fields** including exact sites, targets, addends and frames. Original
BCC and TASM emit the FIXUPP records in different order, so original
literal native OBJ-record identity is **not** claimed.

`scripts/build_th03_mainl_after129_work.py ostoutst` normally compiles
this original selected slot atop the source-bound original Japanese
129-member CRT in two independent TASM/TLIB/TLINK rounds. Both reproduce
the entire original **67,372-byte decoded Japanese MAINL EXE** and MAP
byte-for-byte, including all **677 MZ relocations** and **763 untouched
vendor CRT program records**. Working native source coverage increases to
**130 members / 60,837 original-equal CODE bytes**. This is source-only
working evidence, not formal accepted-ledger credit. **No full cold replay.**

Proof: `review_th03_mainl_after129_work.py ostoutst`,
`tests.test_mainl_after129_work`, raw OBJ/LIB/EXE/MAP native vectors,
source-bound receipts and actual tool logs under `.analysis/work/after129-*`
and `.analysis/work/mainl-after129-*`.
