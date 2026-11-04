# Japanese TH03 MAINL original CRT `wild`: DOS argv/wildcard construction

The actual selected Borland CRT member is **151**, `wild`, exporting
`__wildargv` at original CODE+7. It owns an original **795-byte CODE segment**
with mutable CS scratch at +0/+1, an abort trampoline at +2 and the complete
DOS argument-rewriting logic at +7, as well as a **10-byte uninitialized
_DATA segment**. Its original library member program records, not just a
standalone vendor object, were used as the native oracle.

`src/mainl/crt/wild.asm` recreates the complete PC-98/DOS startup argument
reconstruction logic in symbolic 8086 assembly. It preserves PSP command
line, DOS environment, DBCS path lead-byte scanning, wildcard match/file
search, 16-bit allocation and stack switching, preservation of startup DS,
ES/SS segment ownership, and writes of original `__argc`, `__argv` and
Borland startup `__C0argc`, `__C0argv`. Far exits use the original `__abort`
path. The source contains no original executable byte arrays, patched objects
or artificial padding.

Two easily missed segment-override details were recovered from the genuine
instruction stream: `SS:LODSB` while scanning a DOS search result, and `ES:`
segment overrides on the far argument table stores. The original
`xchg si,dx` operand order likewise needs the right ModRM encoding. The
entire original CODE stream is reproduced, including both unmaterialized
scratch bytes at original CODE+0/+1. The DATA segment is **10 bytes in size**
but contains **zero initialized/LEDATA bytes**. This difference is explicitly
checked by the native evidence rather than normalizing it to an initialized
zero array.

Native TASM 5.0 `/m /mx /kh32768 /t` reconstructs all **793 materialized
CODE bytes**, the original complete 795 CODE extent, 10-byte DATA segment,
original single public +7, eleven ordered imports, one `_DATA` DGROUP and
**38/38 fixup locations, targets, kinds and frames**. Original BCC FIXUPP
record ordering differs from TASM's, so full literal OMF object identity is
not claimed.

`build_th03_mainl_after97_work.py lsetlocl-wild` uses the retained complete
97-source original Japanese MAINL carrier and recompiles `lsetlocl` plus
`wild` at their actual library slots. Two independent TASM/TLIB/TLINK rounds
reproduce the complete **67,372-byte original Japanese MAINL EXE** and full
original **MAP**, preserving all **677 ordered MZ relocations**. Working CRT
is now **99 source-built members / 44,010 original-equal CODE bytes**,
retaining **794** original vendor CRT program records. This is only working
source-native evidence, not an accepted-ledger promotion.

Review with `review_th03_mainl_after97_work.py lsetlocl-wild` and
`tests.test_mainl_after97_work`. Both raw OBJ/LIB/EXE/MAP output pairs,
source-hash-bound native receipts and real tool logs remain under
`.analysis/work/after97-lsetlocl-wild-*`. No full cold replay was run.
