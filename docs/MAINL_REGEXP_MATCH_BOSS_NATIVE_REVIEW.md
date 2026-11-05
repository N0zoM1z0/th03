# Complete Borland regexp matcher: 2,522 CODE bytes, four far methods

The original Japanese Borland C++ CRT member **409** (`match`) has been
recovered as one complete readable native 8086 source file:
`src/mainl/crt/match.asm`. It is not a reduced matching wrapper. It includes
**2,522 CODE bytes** in two original CODE segments (`_TEXT` **5 bytes**,
`_TEXTC` **2,517 bytes**), zero initialized DATA/BSS, three imports and
four complete public matching API bodies:

| Original `_TEXTC` offset | Native public | Original algorithm |
| ---: | --- | --- |
| 0 | `@makepat$qnxcnucui` | compile pattern syntax and character classes |
| 911 | `@matchs$qnxcnxucnnc` | scan and return pattern matches |
| 1087 | `@patcmp$qnxcnxuct1` | compare compiled pattern elements and advance |
| 1761 | `@esc$qnnxc` | parse escapes, hex and octal characters |

The entire nonexported implementation is present too: its original far
empty unwind thunk, internal scanning helpers, far calls, 16-bit bounds and
three *typed CODE-resident jump-dispatch table regions*. A flat disassembler
mistakenly treats these original tables as machine instructions. They were
separated by inspecting the actual original OMF LEDATA and FIXUPP program,
not by guessing from adjacent source or using packed-game bytes:

| Typed CODE-region offsets | Original content | Relocated pointers |
| --- | --- | ---: |
| `_TEXTC+540..588` | `makepat` class/character keys and case dispatch labels | 12 |
| `_TEXTC+1686..1702` | `patcmp` class keys and branch labels | 4 |
| `_TEXTC+2477..2517` | escaped-character keys and branch labels | 10 |

All **46** original OMF relocation fields match by segment, site, location,
width, frame, target and addend: 26 relocated jump-table words, four
internal table-base references, eight local immediate-far targets, four
external far calls and four DGROUP-framed `__ctype+1` uses. The exported
public offsets, all source CODE, source group layout and import ordering
match the original Japanese library member.

## One genuine assembler-codegen discrepancy

At `_TEXTC+1628`, the original Borland instruction is `TEST DX,AX` with
bytes `85 C2`. TASM 5 canonicalizes the symmetric `test dx,ax` mnemonic into
`85 D0` (equivalent flags but not original bytes). The source explicitly
specifies **just that one documented 8086 instruction** as `db 085h,0C2h`.
This is not a machine-code array, object patch, invented filler or copied
executable payload. Similarly, the original direct far `9A` calls to the
other functions in the same CODE segment use the original single opcode
followed by naturally relocatable symbolic far pointers, because TASM
otherwise rewrites them to `PUSH CS` plus near `CALL`.

## Native source-bound verification

`scripts/build_th03_mainl_after335_work.py regexp-match-boss` takes the
complete earlier **360-member** original-source/receipt-bound carrier,
validates every retained inherited native round, substitutes the whole
source-produced `match` member, rebuilds the original **893-slot** CRT library
and executes **two independent native TASM/TLIB/TLINK rounds**, without a
cold replay. Both rounds are exact against the original decoded Japanese
MAINL **67,372-byte EXE and MAP** and all **677 ordered DOS relocations**.
There are now **361** complete source members, **532** contextual original
library members and **117,677** source-compiled, original-equal CRT CODE
bytes (increase **2,522**). The complete OBJ/LIB/EXE/MAP binaries and tool
logs are retained under `.analysis/work/after335-*`; hashes bind the source,
original OMF, original executable, parent receipts and native producer.
Direct OMF and native link regressions are in `tests.test_mainl_after335_work`.

The original **ordered OMF FIXUPP record program** still differs from TASM,
and the complete Borland OBJ record serialization is not claimed equal.
This is verified working CRT source, **not** a new Factory-accepted decoded
extent, packed-file unit or whole-game source-ownership claim.
