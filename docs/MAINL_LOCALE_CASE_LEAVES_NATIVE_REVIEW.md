# Eight original Japanese Borland locale case/collation CRT members

This increment **authors eight complete original 8086 members**, rather than
promoting stubs or replacing original functions with target-binary arrays.
The original Japanese CL.LIB members and exact native ABI are:

| Original member | CODE | Complete far export and real behavior |
| --- | ---: | --- |
| `lstrcoll` (249) | 33 | `__lstrcoll`, far locale collation callback at +0x1A0 |
| `lstrxfrm` (252) | 36 | `__lstrxfrm`, far locale transform callback at +0x1A4 |
| `ltolower` (254) | 43 | `__ltolower`, locale per-byte mapping table at +0x156 |
| `ltoupper` (255) | 43 | `__ltoupper`, locale per-byte mapping table at +0x15A |
| `lstrlwr` (250) | 47 | `__lstrlwr`, original far string in-place lowercase conversion, DS saved/restored |
| `lstrupr` (251) | 47 | `__lstrupr`, original far string in-place uppercase conversion, DS saved/restored |
| `ftolower` (463) | 48 | `__ftolower`, original `__ctype+1` bit map and ASCII fold |
| `ftoupper` (462) | 48 | `__ftoupper`, original `__ctype+1` bit map and ASCII fold |

Each standalone `src/mainl/crt/<member>.asm` is source-backed: the full
machine CODE payload matches the actual original Japanese CL.LIB member,
with correct public and import identities, original group and empty DATA/BSS,
and a **literally equal original single FIXUPP record, including frame**.
The six locale routines reference the real `__pLocale` far pointer; two
in-place functions require the **original TARGET frame5** (no forced group
qualifier) and the others require **DGROUP frame1**. The `__ctype` routines
use DGROUP frame1 with addend +1. The compiler's original `CMP DX,-1` uses
an `83 FA FF` sign-extended immediate; the TASM `byte -1` spelling compiled
an incorrect byte. Writing the natural `cmp dx,-1` mnemonic retains the
original instruction and preserves exact 43/48-byte lengths. No object or
EXE was patched to repair this codegen difference.

`scripts/build_th03_mainl_after339_work.py locale-string-case-leaves`
extends the source/receipt-bound **364-member** Japanese MAINL CRT carrier.
Both independent native TASM/TLIB/TLINK rounds produce the entire original
Japanese decoded **67,372-byte MAINL EXE and MAP**, with all **677 original
ordered DOS MZ relocations**. All 893 original CRT slots remain intact:
**372 source-backed members**, **521 contextual original members**, and
**120,173 original-equal logical CRT CODE bytes** (+345). Raw native
OBJ/LIB/EXE/MAP and tool logs are retained under `.analysis/work/after339-*`,
SHA-bound to all previous source/receipt evidence and reviewed by
`scripts/review_th03_mainl_after339_work.py` and
`tests/test_mainl_after339_work.py`.

All eight source OBJ full **literal FIXUPP fields** equal the pinned original.
Their original full Borland OMF record programs still differ from TASM
metadata, so no full OMF program identity is claimed. This working-source
progress creates no new Factory-accepted extent, packed-file unit credit or
whole-game exactness claim, and no full cold replay was run.
