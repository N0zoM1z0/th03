# Original Japanese MAINL CRT: eight complete directory, file and stream leaves

Eight original Borland CRT members were reconstructed in natural, executable
8086 TASM syntax rather than accepted on the basis of guessed CRT behavior:

| Original member | CODE | Complete far entry and original behavior |
| --- | ---: | --- |
| `mkdir` (88) | 28 | `_mkdir`: INT 21h AH=39h, far path, Borland `__IOERROR` |
| `rmdir` (105) | 28 | `_rmdir`: INT 21h AH=3Ah, far path, original error path |
| `tell` (133) | 28 | `_tell`: far `_lseek` to offset 0 with SEEK_CUR |
| `umask` (134) | 25 | `_umask`: complemented `__notUmask` read/write via original DGROUP |
| `ostendl` (698) | 43 | `endl(ostream&)`: output newline then flush, returns same stream |
| `ostends` (699) | 32 | `ends(ostream&)`: output NUL, returns same stream |
| `ostmflsh` (700) | 28 | `flush(ostream&)`: call original far flush method |
| `fsetpos` (49) | 36 | `_fsetpos`: forward stored far 32-bit position to `_fseek` with SEEK_SET |

The three ostream manipulators uniquely own original `_TEXTA` CODE segments;
all other members own `_TEXT`, along with zero-length DATA/BSS and the
original DGROUP ordering. Each full member has its original public/import
interfaces and every source-produced CODE byte matches the original pinned
Japanese CL.LIB member. All original relocation sites, widths, frames,
targets and addends match exactly. Literal FIXUPP *ordering* differs only
for `umask` and `ostendl` (two fields each, TASM forward versus original
Borland reverse); complete original OMF program record identity is not
claimed for any of the eight.

`scripts/build_th03_mainl_after334_work.py stream-path-leaves` extends the
352-source working CRT carrier. Both native TASM/TLIB/TLINK rounds produce
byte-identical original Japanese MAINL EXE (67,372 bytes), MAP and ordered
677 MZ relocations. All 893 original CRT slots are preserved: **360** are
source-backed complete members, **533** remain unchanged original contextual
programs, and source-compiled original-equal CRT CODE totals **115,155 bytes**
(**+248**). Retained raw dual-round OBJ/LIB/EXE/MAP programs, phase logs,
source hashes, parent receipts and reviewer are under `.analysis/work/after334-*`
and `scripts/review_th03_mainl_after334_work.py`. Direct OMF and native
product assertions are in `tests.test_mainl_after334_work`.

No full cold replay, synthetic executable CODE arrays, patched object records,
Factory-accepted scope promotion or packed-file unit credit is claimed.
