# Original Japanese CRT: twenty DOS/PC-98 BIOS and 8086 small algorithms

Twenty **actually selected original** Japanese Borland CRT programs now
have independent complete symbolic 8086 source in `src/mainl/crt/`:

| Original slot | Member | CODE | Function |
| ---: | --- | ---: | --- |
| 265 | `movedata` | 34 | Far segment data move |
| 215 | `dosext` | 34 | Extended DOS error query |
| 111 | `segread` | 34 | Real-mode segment-register read |
| 86 | `lrotr` | 33 | 32-bit rotate right |
| 85 | `lrotl` | 32 | 32-bit rotate left |
| 317 | `swab` | 31 | Byte-pair swapping |
| 63 | `getswit` | 31 | DOS switch-character get/set |
| 65 | `getverf` | 28 | DOS verify flag get/set |
| 496 | `pc98crt` | 27 | PC-98 CRT BIOS utility |
| 481 | `biosprin` | 24 | PC BIOS printer |
| 476 | `bios_prn` | 24 | PC BIOS printer variant |
| 507 | `pc98sfky` | 21 | PC-98 function key configuration |
| 503 | `pc98mem` | 21 | PC-98 memory BIOS |
| 500 | `pc98gfky` | 21 | PC-98 function key status |
| 482 | `dosvgadr` | 21 | DOS/V video-address query |
| 477 | `bioscom` | 20 | BIOS serial COM |
| 472 | `bios_com` | 20 | BIOS serial COM variant |
| 197 | `bdos` | 20 | DOS syscall |
| 492 | `dosvuscr` | 19 | DOS/V update screen |
| 549 | `cnecwhxy` | 18 | NEC text cursor position |

All source members have complete real 8086 instruction bodies, preserving
original segment registers, far pointer ABI, flags and true public offsets,
with no copied executable CODE bytes, padding or native object patches.
One original ModRM issue was resolved: the source orientation of `swab`'s
8-bit `XCHG` must assemble to the original **`86 E0` at CODE+21**, not the
semantically equivalent but byte-different `86 C4`.

Each original selected member assembles in native TASM 5.0
`/m /mx /kh32768 /t` to **all 513/513 original CODE bytes** with exact
original PUBLIC offsets, segment/group membership and empty DATA/BSS,
EXTDEF and **literally original empty OMF FIXUPP** inventories. The
complete original OMF record program is not claimed identical without
independent proof of every other record type.

`scripts/build_th03_mainl_after263_work.py pc98-dos-small-leaves` reuses
the source-bound **263-source Japanese CRT** and performs **two independent
normal TASM/TLIB/TLINK rounds**. Both produce the **entire original
67,372-byte decoded Japanese MAINL EXE and original MAP byte-for-byte**,
including **677 ordered MZ relocations**, while keeping **610 original
vendor member programs unchanged**. Working source becomes **283 members /
98,716 original-equal CODE bytes**. Formal accepted-ledger credit is
unchanged and no full cold replay was run.

Verification: `review_th03_mainl_after263_work.py pc98-dos-small-leaves`,
`tests.test_mainl_after263_work`, source-hash-bound receipts and actual
native OBJ/LIB/EXE/MAP vectors and tool writer logs under
`.analysis/work/after263-*` and `.analysis/work/mainl-after263-*`.
