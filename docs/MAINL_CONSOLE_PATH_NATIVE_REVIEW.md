# TH03 Japanese MAINL CRT: console, printf and current-directory source

Seven selected original Borland large-model CRT members were independently
verified against their **active 893-member Japanese MAINL library program
records**, recovered in native 8086 assembly and joined with the existing
source-original `utime` carrier:

| Original slot | Recovered source | CODE bytes | Important original ABI |
| ---: | --- | ---: | --- |
| 561 | `kbhit.asm` | 22 | `_kbhit` and DATA+0 `__cFlag`, DATA+1 `__cChar` |
| 557 | `getch.asm` | 29 | `_getch`, DOS input without echo, buffered key |
| 558 | `getche.asm` | 52 | near `__Ngetche` +0, far `_getche` +3 |
| 566 | `ungetch.asm` | 37 | near `__Nungetch` +0, far `_ungetch` +3 |
| 563 | `putch.asm` | 25 | `_putch`, near `__CPUTN` output bridge |
| 270 | `printf.asm` | 31 | `_printf`, stdout `__streams+20`, `__VPRINTER` callback |
| 238 | `getcwd.asm` | 142 | `_getcwd`, DOS path, errno and optional far allocation |

These are genuine 16-bit source functions, not original CODE/data byte arrays
or patched objects. The original `kbhit` module contributes an initialized
**2-byte DATA** buffer with two exported symbols; the other six modules have
zero initialized DATA/BSS. The original 68-byte temporary stack path buffer
in `getcwd` and the corresponding `ERANGE` / `ENOMEM` handling are kept rather
than replaced with a different modern implementation.

All seven native modules independently assemble to their **complete original
CODE bytes** and exact original segment sizes, group order, public offsets,
ordered external symbol dependencies and all logical original relocation
sites, kinds, targets and addends. `kbhit`, `getch`, `getche` and `ungetch`
reproduce their entire **literal ordered OMF FIXUPP fields**, including frame
methods. In contrast, `getcwd` has the original compiler's descending record
order, whereas TASM uses ascending order. `printf` and `putch` use original
TARGET frame5 for near external helpers but TASM emits CODE frame0. These
object-level gaps are explicit, and no original literal OBJ identity is
claimed from the target-equal link alone.

`build_th03_mainl_after89_work.py utime-console` extends the retained
source-bound 89-member Japanese CRT by the `utime` and seven console/path
sources in **two independent normal TASM/TLIB/TLINK rounds**. The whole
**67,372-byte original decoded Japanese MAINL EXE and original MAP** match
byte-for-byte, including all **677 ordered DOS MZ relocations**. Working CRT
source coverage is now **97 actual member positions / 38,563 original-equal
CODE bytes**; **796 contextual vendor member programs** remain unchanged.

Proofs: `review_th03_mainl_after89_work.py utime-console`, the two raw
OBJ/LIB/EXE/MAP vectors, source/driver hash receipts and writer logs under
`.analysis/work/after89-utime-console-*`, and `tests.test_mainl_after89_work`.
These are **working native source proofs**, not additional formal accepted
ledger credit. All original cold-product vectors were reused and hash-audited;
**no full cold replay** was performed.
