# Eight full original DOS path and ostream manipulator CRT leaves

This working-source addition recovers eight entire original Japanese Borland
CL.LIB members as natural 8086 `src/mainl/crt/*.asm` source, with their
original exported far APIs, unmodified 16-bit stack conventions, complete
CODE, no DATA/BSS, original DGROUP/segment layout and full imported
relocation fields.

| Original CRT member | CODE | Native original behavior |
| --- | ---: | --- |
| `mkdir` (88) | 28 bytes | DOS INT 21h AH=39h create directory, original `_IOERROR` path |
| `rmdir` (105) | 28 bytes | DOS INT 21h AH=3Ah remove directory, original `_IOERROR` path |
| `tell` (133) | 28 bytes | Current file offset from original far `_lseek` call |
| `umask` (134) | 25 bytes | Far `_umask` get/set via original `__notUmask` DGROUP global |
| `ostendl` (698) | 43 bytes | Far C++ `endl`: write newline and flush original ostream |
| `ostends` (699) | 32 bytes | Far C++ `ends`: output terminating NUL |
| `ostmflsh` (700) | 28 bytes | Far C++ `flush`: invoke original `ostream::flush` |
| `fsetpos` (49) | 36 bytes | Far `fsetpos`: forward original stored 32-bit position to `_fseek` |

The three C++ manipulator members use original `_TEXTA` CODE segments,
not the ordinary `_TEXT` segment. `mkdir` and `rmdir` preserve DGROUP
`08ff03ff02`, while the other six members retain `08ff02ff03`. Every
materialized byte, original public/import entry, segment definition and
logical fixup including **the actual frame fields** matches the original
member. Two OMF serialization differences are recorded rather than
normalized: the imported global `umask` fields are ordered `[17,7]` in
the original and `[7,17]` in TASM; `ostendl`'s original far call FIXUPP
sites are `[26,15]` rather than TASM's `[15,26]`. All their individual
frames, targets and addends agree. The six other original members match
their ordered FIXUPP sequences. Complete original OBJ program-record
serialization is not claimed.

`scripts/build_th03_mainl_after334_work.py stream-path-leaves` retains the
validated 352-member native source-bound parent, then compiles all eight
members in two independent, serialized TASM/TLIB/TLINK rounds. Both reproduce
**all 893 CRT library slots**, with **360 source-backed** and **533 original
contextual** members, and the entire Japanese decoded **67,372-byte MAINL
EXE and MAP**, including the **original ordered 677 DOS MZ relocation
entries**. The increase is **248 original-equal CODE bytes**, for a total
of **115,155 working-source CRT CODE bytes**. Complete raw OBJ/LIB/EXE/MAP
outputs and writer logs are retained under `.analysis/work/after334-*`,
SHA-bound to the actual source files, both original native rounds and the
entire parent receipt DAG.

The narrow original-OBJ/OMF regression is
`tests/test_mainl_after334_work.py`; the scope reviewer is
`scripts/review_th03_mainl_after334_work.py`. The unchanged cold baseline is
reused, not rebuilt. This expands working-source reconstruction only; no new
Factory-accepted extent, original packed-file canonical credit or whole-game
source-ownership claim is implied.
