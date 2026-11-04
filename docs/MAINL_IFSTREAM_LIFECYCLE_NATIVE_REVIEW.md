# Original Japanese Borland `ifstream` complete constructor/destructor lifecycle

Five actually selected original large-model CRT members have now been
recovered as whole symbolic 8086 source, not just constructor prologues:

| Original CRT slot | Source | CODE | DATA | Original C++ public |
| ---: | --- | ---: | ---: | --- |
| 726 | `ifsctr1` | 596 | 28 | `@ifstream@$bctr$qv` |
| 727 | `ifsctr2` | 612 | 28 | `@ifstream@$bctr$qnxcii` |
| 728 | `ifsctr3` | 599 | 28 | `@ifstream@$bctr$qi` |
| 729 | `ifsctr4` | 608 | 28 | `@ifstream@$bctr$qinci` |
| 730 | `ifsdtr` | 569 | 28 | `@ifstream@$bdtr$qv` |

`src/mainl/crt/ifsctr*.asm` and `ifsdtr.asm` reconstruct the exact far
Borland C++ calling conventions and actual `ios`/`istream`/`fstreambase`/
`filebuf` multiple-inheritance construction, ownership, release and
exception-cleanup routines. Each member has **two real 12-byte executable
multiple-inheritance destructor-adjustor thunks** between the executable
public method and the subsequent non-executable class RTTI. These are
**genuine 8086 instructions** (`mov bx,sp`, stack pointer adjustment,
`jmp far ptr`), not copied machine-byte arrays or size padding. The six
original class-name strings and exception metadata are separately expressed
as symbolic `dw`/`dd` descriptors; the 28-byte initialized DATA is the
original four far unwind/type pointers and header.

A real ABI mistake was found in the destructor's self-referential thunks:
TASM shortened original far `EA` jumps into near `E9` when CS remained
assumed as `_TEXTA`. Adding `ASSUME CS:NOTHING` immediately before the
adjustor thunks reproduces the original **far control transfer** without
patching any native output. This is the same verified technique previously
required for `fstream` and `strstream`, and its actual effect was checked
against the selected original `ifsdtr` OBJ rather than assumed from those
prior cases.

Normal TASM 5.0 `/m /mx /kh32768 /t` reconstructs **2,984/2,984 original
CODE bytes and 140/140 initialized DATA bytes**, all five original PUBLICs,
11/7 ordered imported symbols, the original `_TEXTA/_DATA/_BSS` and
`08ff02ff03` DGROUP, and **135/135 original OMF relocation sites, targets,
widths, addends, kinds and frame methods**. BCC and TASM still order FIXUPP
records differently, so complete literal original OMF OBJ identity is **not**
claimed.

`scripts/build_th03_mainl_after204_work.py ifstream-lifecycle` starts from
the retained actual **204-source Japanese CRT** and assembles the five selected
members in **two independent normal TASM/TLIB/TLINK rounds**. Both reproduce
the complete original **67,372-byte decoded Japanese MAINL EXE and original
MAP byte-for-byte**, preserving all **677 ordered MZ relocations** and
**684 untouched original vendor CRT member program records**. Working source
reaches **209 members / 87,885 original-equal CODE bytes**. This is working
source evidence, not formally accepted-ledger credit, and no full cold replay
was run.

Proof: `review_th03_mainl_after204_work.py ifstream-lifecycle`,
`tests.test_mainl_after204_work`, and the source-hash-bound native OBJ/LIB/
EXE/MAP pair and actual tool logs under `.analysis/work/after204-*` and
`.analysis/work/mainl-after204-*`.
