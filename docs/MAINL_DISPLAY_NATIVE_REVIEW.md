# MAINL palette, VSync and gaiji

This review adds 15 disjoint extents, 22 procedures and 1,439 library bytes:
1,362 CODE +77 file DATA. Previous 149 owners remain unchanged. The 58 bytes of
palette/VSync BSS add no file credit. Whole-product source ownership remains open.

## Native production

Two actual selected GAME3 TASM/TLINK rounds consume maintained palette, gaiji and
BSS declarations at their original root positions. Both complete EXEs equal the
pinned Japanese decoded target; both MAPs equal the retained MAP. Raw OBJ/EXE/MAP
vectors repeat. The 35 other project objects and CRT are reused. All 938 cold
outputs, source and recipe are restored and validated; no full cold, DIET or
ancestor runtime replay is needed.

`palette_show.inl` replaces `ORG $-1 / DB ?` with `PALSHOW_XORVAL EQU $-1` after
the real `XOR AH,0` instruction. The SMC writer needs explicit `BYTE PTR` for
TASM to retain its operand type. It writes the actual immediate at CODE:18B8;
the EQU emits no storage. Removing ORG changes LEDATA/FIXUPP packet boundaries.
Every initialized byte, complete public identity, segment/group metadata and
absolute ordered native field remain equal. Packet-local LOCAT encodings may
change; literal ordered MZ relocations remain equal. No object is patched.

Six independent native modules link twice against real providers: context,
VSync, black fade in/out, gaiji backup and BFNT gaiji entry. The maintained bodies
replace compatibility `nopcall` with ordinary `call`, without explicit NOPs.
External far declarations outside CODE emit 19 genuine five-byte calls with
FAR-pointer fields. Actual TLINK naturally emits the target's
`NOP / PUSH CS / near CALL`. Same-CODE far declarations retain the original
four-byte forms where required. The complete mini CODE/DATA and ordered MZ
vector are independently resolved, then every complete subject body is checked
at its product layout. No stub callee or target-byte array is introduced.

The frozen root retains contextual compatibility calls; a future full recipe
change must integrate the demonstrated TU boundaries. Mini context has a real
uninitialized stack and BSS; neither earns extra credit.

## Ownership and ABI

| Owner | CODE | File DATA | Procedures |
| --- | ---: | ---: | ---: |
| Black fades | 130 | 0 | 2 |
| Palette show / RGB | 332 | 0 | 2 |
| VSync wait / white fades | 166 | 0 | 3 |
| VSync IRQ bank | 246 | 4 | 4 |
| DOS vector setter / close | 54 | 0 | 2 |
| Gaiji backup / loader | 214 | 0 | 3 |
| Gaiji read / write | 220 | 0 | 6 |
| Initialized palette / VSync / backup / dimensions | 0 | 73 | 0 |

All 57 root native fields resolve in literal order. The sole scoped MZ entry is
0000:1FE5, the DS segment load in VSYNC_COUNT. CRTBIOS_COOK and VSYNC_COUNT end
with real IRET instructions. VSYNC_END and VSYNC_LEAVE alias one body; private
near GETFONTW/SETFONTW are separate procedures. Full bodies, outer EVEN bytes,
local branches, far Pascal cleanup and public MAP entries are checked.

The first four bytes of the VSync bank are original `DW ?` saved-vector storage
in CS, with no LEDATA initializer. Only those four bytes use actual independent,
repeated linked output in the comparison. No zero initializer is added.

## State and open alignment

The 56-byte palette state contains tone 100, 16 generated RGB colors and three
zero WORDs. REPT and bit formulas preserve FF/AA intensity and index-8 gray 77.
VSync callback DWORD, delay WORD and mask BYTE own seven bytes at DATA:0842.
Private gaiji state owns backup segment WORD 0 and dimensions WORDs 16,16,0,255.
All initialized bytes and public aliases are checked against native objects.
Palette/VSync BSS keeps its typed declarations and all aliases, without file
credit or a new initializer for delay_count.

Ordinary EVEN after the seven VSync bytes emits 00 in the independent TU; the
target byte at DATA:0849 is 90. The root retains its old contextual provider at
that position. DATA:0849 remains uncredited; the seven-byte owner uses the real
independent context object. Do not treat ordinary WORD alignment as proof of 90.

Preserve signed fade loops, unchecked RGB/header/allocation behavior, caller DF,
CLI/STI, GAME3 glyph ADC/caller-CF behavior, segment-only callback guard and delay
carry handling. Original BIOS/port waits may be unbounded. No defensive product
fix or physical graphics/IRQ/DOS execution claim is made.

Actual inputs in `.analysis/work/`: `mainl-display-build.json`,
`mainl-display-native.json`, both `display-roundN.obj/.exe/.map` vectors,
`display-root.asm/.lnk`, both six-object `display-mini-roundN-*`/EXE/MAP vectors,
the six `display-mini-NAME.asm` wrappers and `display-mini.lnk`.
