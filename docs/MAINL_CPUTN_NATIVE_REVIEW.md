# Japanese PC-98 MAINL CRT `cputn`: native console counted output engine

Recovered selected Borland CRT member **553** `cputn` using natural 8086
assembly `src/mainl/crt/cputn.asm`. It contains a **546-byte CODE segment**,
**2 bytes initialized DATA**, and **4 bytes BSS**. The only original CODE
public `__CPUTN` is a near counted console-output callback at offset +450.
Two additional original BSS publics are `___col` at +0 and `___row` at +2.
These exported data symbols are separately checked; merely matching the CODE
bytes would miss part of the active CRT ABI.

The source restores native PC-98 text display behavior including cursor and
window-row management, scrolling, character/bell output, DBCS/Kanji state,
VRAM access transitions and hardware video helpers. All **15 ordered EXTDEFs**,
the original `_BSS,_DATA` group, native calling conventions, and unsigned
16-bit cursor arithmetic are preserved. An original seven-entry special
output **CODE dispatch table at +436** is expressed as real symbolic `dw`
function offsets, not embedded machine CODE bytes or post-assembly changes.

TASM 5.0 `/m /mx /kh32768 /t` reproduces **all 546/546 original CODE bytes**,
**2/2 DATA bytes**, BSS extents/publics and all **76/76 original OMF fixup
sites, kinds, targets and addends**. Of these, **18** external near calls
use the original compiler's TARGET frame5 but TASM's CODE frame0, and the
record order differs; the remaining site-sorted fixups including the seven
CODE table references have original frames. Complete literal original OMF
object-record identity is **not** claimed.

Integration uses `build_th03_mainl_after103_work.py cputn` against the
retained original Japanese **103-source** CRT. Two independent normal
TASM/TLIB/TLINK rounds preserve every previously recovered source and **789**
other original vendor CRT program records, while reproducing the **entire
67,372-byte decoded Japanese MAINL EXE** and full original MAP byte-for-byte,
including **677 ordered DOS MZ relocations**. Working source reaches **104
original selected members and 45,964 original-equal CODE bytes**. This is
source-only working evidence, not formally accepted-ledger promotion, and
no complete cold replay was performed.

Source-bound receipts, two raw OBJ/LIB/EXE/MAP vectors and native writer logs
are retained under `.analysis/work/mainl-after103-cputn-*` and
`.analysis/work/after103-cputn-*`. Reviewer:
`review_th03_mainl_after103_work.py cputn`, and
`tests.test_mainl_after103_work`.
