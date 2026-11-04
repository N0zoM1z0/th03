# Original Japanese CRT: sixteen complete PC-98, DOS and C++ core leaves

Sixteen genuine *selected original* Borland CRT members have been recovered
as full symbolic 8086 assembler source. They cover exact native DOS/PC-98
BIOS and port APIs, as well as essential C++ stream flags and buffer state:

| Selected slot | Module | Original CODE | Recovered native operations |
| ---: | --- | ---: | --- |
| 883 | `stsetf2` | 106 | C++ `ios::setf` two arguments |
| 845 | `srbsbuf` | 44 | `strstreambuf::setbuf` |
| 842 | `srbfreez` | 40 | `strstreambuf::freeze` |
| 60 | `getfat` | 104 | DOS FAT date and free-space helpers (3 exports) |
| 497 | `pc98disk` | 82 | PC-98 BIOS disk access |
| 470 | `bion_key` | 81 | NEC PC-98 BIOS keyboard |
| 471 | `bion_prn` | 73 | NEC PC-98 BIOS printer |
| 97 | `outport` | 66 | Four DOS port-write APIs |
| 78 | `inport` | 56 | Four DOS port-read APIs |
| 502 | `pc98key` | 48 | PC-98 keyboard |
| 506 | `pc98prnt` | 32 | PC-98 printer |
| 480 | `bioskey` | 41 | IBM PC BIOS keyboard |
| 478 | `biosdisk` | 62 | IBM PC BIOS disk |
| 474 | `bios_equ` | 51 | BIOS equipment/memory/time (3 exports) |
| 28 | `dosgdate` | 62 | DOS get-date/get-time |
| 531 | `cibmsond` | 59 | IBM PC sound/no-sound (2 exports) |

The source modules preserve every original public entry offset, segment
register, native 16-bit `INT`/port I/O instruction and unchecked DOS/Borland
large-model caller convention. Three C++ modules retain original `_TEXTA`
CODE and `_BSS,_DATA` group; the other original `_TEXT` units preserve their
native original DGROUP ordering. These are complete instructions with
symbolic branches rather than original executable CODE-byte arrays,
forced padding or binary object patching.

`pc98disk` illustrates an exact-original distinction: the three original
8-bit `XCHG` instructions at CODE+11/+32/+48 encode `86 C4` / `86 D6` /
`86 C4`. Swapping the source operand order while retaining identical
execution semantics originally produced different ModRM bytes; writing the
original source orientation restores all 82 original CODE bytes naturally.

Standalone TASM 5.0 `/m /mx /kh32768 /t` reconstructs **all 1,007 original
CODE bytes**, every true original PUBLIC and the complete original empty
DATA/BSS/EXTDEF inventories. All 16 members have **no OMF FIXUPP fields**;
TASM preserves the literally original empty field stream, including the
absence of relocation frames. No whole-OBJ byte identity of unrelated OMF
record classes is asserted without checking those separate records.

`scripts/build_th03_mainl_after185_work.py hardware-io-leaves` inherits the
original 185-source Japanese CRT through its source-bound receipt DAG and
assembles 16 genuine selected member slots in **two independent normal
TASM/TLIB/TLINK rounds**. Both produce the **entire 67,372-byte decoded
Japanese MAINL EXE and original MAP byte-for-byte**, including all **677
ordered DOS MZ relocations** and **692 original vendor CRT program records
left unchanged**. Working source reaches **201 members / 83,166
original-equal CODE bytes**. This is working-source evidence only, not
accepted-ledger promotion or full game source completion; **no full cold
replay** was run.

Proof: `review_th03_mainl_after185_work.py hardware-io-leaves`,
`tests.test_mainl_after185_work`, two raw OBJ/LIB/EXE/MAP native vectors,
actual Borland writer logs and source-hash-bound receipts under
`.analysis/work/after185-*` and `.analysis/work/mainl-after185-*`.
