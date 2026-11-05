# Original NEC PC-98 function-key BIOS and MBCS string-character search

Three complete original Japanese Borland CL.LIB members are recovered as
real 8086 source: `src/mainl/crt/pc98fkey.asm`, `MBSCHR.asm` and
`FMBSCHR.asm`. These implementations have genuine PC-98 system calls and
DBCS byte-scanning behavior, not placeholder wrappers or raw executable
machine-code arrays.

| Original CL.LIB slot | CODE | Full exported API |
| --- | ---: | --- |
| `pc98fkey` (499) | 80 bytes | `_pc98fkeyon`, `_pc98fkeyoff`, `_pc98fkeychk` |
| `MBSCHR` (602) | 116 bytes | `__mbschr` |
| `FMBSCHR` (658) | 116 bytes | `__fmbschr` |

`pc98fkey` preserves the original private far-to-near function-key sequence
writer, the actual 5-byte NEC control string `ESC [ > 1 NUL` at original
CODE+14, the real **INT DCh** BIOS command, its control-word option and
the hardware state read at physical ES:0711h. The three public far entry
points are exactly CODE+40,+51,+62. Its original CODE relocation at +6
points to the real control string at +14, with original TARGET frame5.

Both `__mbschr` variants scan a far DBCS string and compare entire
single-byte or two-byte characters while preserving the far DX:AX pointer
return. They reference the real `__mbctype+1` table with original DGROUP
frame1 and return the original null far pointer on failure. Every original
instruction, branch target, far ABI and imported table address is preserved.

All **312 original CODE bytes**, five far exported APIs, original segment
and group layouts, and **three original literal ordered FIXUPP fields**
match the pinned Japanese CL.LIB, including each frame/target/addend.
The original whole Borland OMF record serialization still differs from
TASM's metadata; full OBJ-record equality is not claimed.

`scripts/build_th03_mainl_after364_work.py pc98-function-key-and-mbschr`
reuses the exact original source/receipt-bound **428-member** parent,
recompiles just these three members and reconstructs the original 893-slot
Borland CRT library with native TASM/TLIB/TLINK in **two independent
rounds**. Both reproduce the complete decoded **67,372-byte Japanese
MAINL EXE and MAP byte-for-byte**, including all **677 original ordered DOS
MZ relocations**. The working CRT reaches **431 complete original-equal
source-backed members**, **462 unchanged contextual library programs** and
**136,836 original-equal CRT CODE bytes** (+312). All raw OBJ/LIB/EXE/MAP
writer rounds, phase logs, parent/source hashes and original member OMF
checks are retained under `.analysis/work/after364-*`. The independent
review/test entry points are `scripts/review_th03_mainl_after364_work.py`
and `tests/test_mainl_after364_work.py`.

This is working CRT reconstruction progress only: no full cold replay,
new Factory-accepted extent or canonical packed-game unit credit.
