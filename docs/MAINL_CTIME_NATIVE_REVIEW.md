# Japanese MAINL large `ctime` calendar CRT: original-source reconstruction

The selected Japanese large-model CRT library member `ctime` is slot **212** of
893 members. Its original OMF program records match the active CRT member (not
merely an alternate vendor OBJ). The original contains **1,278 CODE bytes,
451 initialized DATA bytes, 44 BSS bytes**, and six exported far entry points:

| CODE offset | Public symbol | Role |
| ---: | --- | --- |
| 510 | `_atime` | Format a decoded calendar into a supplied string buffer |
| 597 | `_gmtime` | Decode epoch seconds into the module's static `tm` |
| 626 | `_localtime` | Apply timezone adjustment and decode the resulting time |
| 686 | `_asctime` | Add a newline and terminator to the formatted calendar |
| 735 | `_ctime` | Compose localtime and asctime |
| 1178 | `_mktime` | Normalize calendar fields and encode epoch seconds |

`src/mainl/crt/ctime.asm` recovers both large unexported calendar arithmetic
routines (at CODE+0 and +764), all six public wrappers, and original named
data: abbreviated/full weekdays, abbreviated/full months, AM/PM, twelve month
lengths and cumulative day offsets, the `asctime` format string, 26 bytes of
static text and an 18-byte `tm` in BSS. The source uses symbolic labels and
real TASM 8086 instructions; it does **not** embed original CODE bytes, pad to
size, modify native OBJ bytes or patch the linked image. The code is a close
instruction-level reconstruction, not yet a high-level C recovery.

The native source compiler/assembler `TASM 5.0 /m /mx /kh32768 /t` reproduces:

- all 1,278/1,278 CODE bytes and 451/451 initialized DATA bytes;
- all six public offsets, nine imports, original segment sizes, 44 BSS bytes
  and the original `_BSS,_DATA` group;
- **101/101 relocations** by location, width, target method, imported/local
  symbol and addend: 61 CODE sites and 40 initialized DATA far-pointer sites.

**Open gap:** complete literal OMF FIXUPP records are *not* equal. The compiler
and TASM emit different field order, and **57** fields differ in frame metadata
(17 external near calls and 40 far pointers). Do not convert this bounded
logical relocation equivalence into a literal native-OBJ equality claim.

`build_th03_mainl_after62_work.py ctime` reconstructs this member by itself
at its original CRT index. `sprintf-calloc-puts-ctime` combines this boss with
three other new original-source CRT modules. For each mode, two independent
TASM/TLIB/TLINK source rounds preserve all remaining library members and
reproduce the **whole 67,372-byte original decoded Japanese MAINL EXE and MAP**,
including all **677 original MZ relocations**. The combined working CRT has
**66 source-built members / 30,215 original-equal CODE bytes**, plus `ctime`'s
source-built DATA and BSS. The other **827** original vendor member program
records remain unchanged. These are *working-source* proofs only; the formal
accepted source-ownership publication is not advanced.

Review with `scripts/review_th03_mainl_after62_work.py` in both modes, and
`tests.test_mainl_after62_work`. Both 2-round native object, library, EXE and
MAP vectors and writer phase logs are retained in `.analysis/work/after62-*`
with source-bound receipts. The existing original cold pair is reused;
**no full cold replay** was executed.
