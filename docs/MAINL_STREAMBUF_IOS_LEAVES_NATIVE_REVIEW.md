# Original Japanese C++ streambuf and ios core: 12 native leaf methods

Twelve **distinct selected** members of the original 893-member Borland
large-model CRT have complete authored 8086 source in `src/mainl/crt/`:

| Selected slot | Original member | Complete CODE | Method |
| ---: | --- | ---: | --- |
| 864 | `stbsetg` | 107 | `streambuf::setg` |
| 865 | `stbsetp` | 80 | `streambuf::setp` |
| 868 | `stbskpos` | 39 | `streambuf::seekpos` |
| 856 | `stbdnext` | 48 | `streambuf::do_snextc` |
| 871 | `stbsync` | 80 | `streambuf::sync` |
| 873 | `stbuflow` | 55 | `streambuf::underflow` |
| 884 | `stsetst` | 42 | `ios::setstate` |
| 874 | `stclear` | 62 | `ios::clear` |
| 878 | `stflags` | 81 | `ios::flags` |
| 888 | `stunset` | 86 | `ios::unsetf` |
| 885 | `stskip` | 73 | `ios::skip` |
| 879 | `stinit` | 90 | `ios::init` |

All 12 functions are real symbolic 8086 instructions, preserving original
Borland C++ mangled PUBLICs, far stack/segment behavior, `_TEXTA` CODE and
empty `_DATA/_BSS` in `08ff02ff03` DGROUP. The modules directly implement
stream buffer pointer management, virtual seek/sync/read, stream flags and
initialization used by the large `strstreambuf`, `ostream` and `istream`
Boss modules already recovered. They are not original executable CODE-byte
arrays, source placeholders or object patches.

A meaningful ABI trap was fixed during independent TASM checks: the original
virtual calls inside `stbskpos` at CODE+29 and `stbdnext` at CODE+17 are
**far indirect calls** with genuine original opcodes `FF 5F 1C` and
`FF 5F 0C`. Untyped `call [bx+...]` encoded incorrect near-call `FF /2`;
using `call dword ptr [bx+...]` correctly restores original `FF /3` in
fully authored source.

For all 12 *real selected original CRT members*, TASM 5.0
`/m /mx /kh32768 /t` reproduces the **entire 843/843 CODE bytes**, segment
sizes/classes, original PUBLICs and empty EXTDEF lists. All 12 native objects
have **zero OMF relocation fields**, and TASM preserves the **literally
original empty FIXUPP inventory**; this is stronger than a frame-ignored
relocation comparison. We do not claim every other OMF record type is
serialized identically without that independent proof.

`build_th03_mainl_after137_work.py streambuf-ios-leaves` validates the
entire **62→137 original Japanese CRT receipt DAG topologically**—actual
selected member positions, source/driver/parent hashes, two independent
original normal OBJ/LIB/EXE/MAP vectors and real Borland tool logs—without
rerunning a historical cold product. Then it recompiles these 12 members
in two independent normal TASM/TLIB/TLINK rounds. Both reproduce the
**complete original 67,372-byte decoded Japanese MAINL EXE and MAP byte-for-
byte**, retaining **all 677 ordered MZ relocations** and **744 untouched
vendor CRT program records**. The working source CRT now has **149 members,
66,008 original-equal CODE bytes**. This is working source reconstruction,
not formally accepted-ledger credit or whole-program source completion.

Proof: `review_th03_mainl_after137_work.py streambuf-ios-leaves`,
`tests.test_mainl_after137_work`, two raw native OBJ/LIB/EXE/MAP vectors,
actual writer logs and source-bound receipts under
`.analysis/work/after137-*` and `.analysis/work/mainl-after137-*`.
