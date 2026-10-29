# TH03 handoff

## Current checkpoint

Use natural source recovery and exact native output with direct local tools.
Session preflight is complete for the unchanged environment. Revalidate the
unchanged cold pair; rebuild affected producers. No native writer remains running.

MAINL recovers complete program resolver/load preparation:871 CODE+40 DATA,
three procedures,all library. Previous183 owners/nested scopes unchanged;
authored bytes stay16,695. See [loader review](MAINL_LOADPROG_NATIVE_REVIEW.md).

New loadprog.asm has private far cdecl DBCS delimiter scan132/probe137 and near
cdecl coordinator602. Preserve DBCS trail-byte skipping,drive/separator PATH
suppression,COM/EXE/BAT order,COMSPEC routing,80-byte unchecked probe buffer,
156-byte coordinator frame,128-byte command threshold,named errno constants and
original argument-stack cleanup. Real DOSCMD/DOSENV prepare allocations; a far
buffer callback precedes a12-byte near executor callback matching recovered
__exec. No defensive checks or physical DOS behavior claim.

All40 DATA bytes are genuine PATH,separators,empty suffix,two BAT instances,
COM/EXE,COMSPEC and/c strings/NULs. Original DATA/BSS group order and explicit
DGROUP-qualified offsets reproduce full MAP naturally. Reversed GROUP order
had added an empty BSS row; source correction removes it,no MAP row masked.
Complete initialized CODE/DATA payload matches original;32 native fields are
independently resolved,including14 real far-call relaxations. Original compiler
and TASM field orders differ:retain both streams,compare geometry by site,never
sort MZ relocations. Only two exact equivalent near-constructor frames differ.
All scoped MZ vectors empty; full bodies/local branches/ABI callbacks checked.

Two actual TASM/TLIB/TLINK rounds compose loadprog with reused natural exec and
farheap plus six retained source providers:all nine coexist in one normal
library.893 positions/all890 other current member payloads unchanged;36 project
objects reused. Full raw OBJ/LIB/EXE/MAP vectors repeat; complete EXE/MAP equal
pinned Japanese decoded target/retained MAP.938 cold outputs/source/recipe/tools
unchanged. No full cold/DIET or ancestor runtime replay; older native pairs reused,
not reassembled. Full cold recipe remains six CRT replacements; this selected
combined recipe integrates the three newer providers without rewriting hashes.

Receipts:`mainl-loadprog-build.json`, `mainl-loadprog-native.json`,
`mainl-loadprog-progress.json` in`.analysis/work/`. Focused native/acceptance/status/
progress and tracking pass; finish with diff checks. Old183 owners/scopes unchanged;
OP acceptance reverified,OP/ZUN publications untouched. Only MAINL SVG region/
summary/source-present row refreshed. Whole-product source ownership stays open.

Earlier findings:exec933 has671 CODE+262 CS storage,97-byte copied continuation,
257 genuine uninitialized work bytes and near12-byte executor ABI. Farheap1115
has1103 CODE+12 CS state,14 entries,three DW? scratch WORDs. Joystick103 excludes
2AAD/2B15 zeros. CREATE/JS_END use proven far calls. CRT628+93 retains bridges and
FFFF resize collision. Palette EQU aliases XOR immediate18B8 without ORG. VSync
CS vector4 remains DW?;DATA0849 target90 vs EVEN00 uncredited. MAIN EC2D90 vs00,
MZ headers6240/7680/relocation offsets28/62 open;1553 entries agree. No padding.

## Accepted source scopes

| Product | Current scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 459 functions /78,737 CODE bytes /106 extents | Open |
| OP | 60 extents /92 procedures /13,221 CODE +1,764 DATA bytes | Open |
| MAINL | 185 extents /248 procedures or entries /29,039 CODE +1,886 DATA bytes | Open |
| ZUN | 77 extents /89 procedures or entries /6,179 CODE bytes | Open |

MAINL accepts30,925 bytes:16,695 authored +14,230 library. ZUN accepts8,635 bytes:
2,179 authored +1,390 original ASM +5,066 library. Whole-game source/function
denominators and completion percentage remain unknown. Canonical packed-unit
credit stays separate. OP/MAINL/ZUN retained cold pairs match decoded and DIET -B
stored targets with unowned reference/vendor context. MAIN repeats100 outputs/
98 project objects/1,553 ordered relocations; EC2D90 vs00 and MZ headers remain
open. Its original VS module is explicit vendor context.

Earlier scope notes remain useful: archive reader175/state5 independent modules
produce natural WORD link gaps; CODE19A3 is excluded/linker-gap,DATA05B5 uncredited.
BFNT preserves swapped SI/DI unwind. Hook29AE is source DW? with no LEDATA; only
those2 bytes use actual independent TLINK output,never invented zeros. SUPER
shared exits borrow frames; RotTbl is1024 DATA,not instructions. PI decoder has
four procedures and a shared11-byte exit. See the corresponding native reviews.

## Inputs and next work

Preserve pinned Japanese targets/assets (`candidate-local-attested`),Wine prefix,
TC4/TASM/JWasm,`.tools/ghidra`,`.tools/jdk`,`.venv`,`_reference/ReC98` and
`ghidra-project/`. Keep one working build per product:TH03WORK,TH03OP,TH03ML,
TH03ZUN. Actual source archive:
`.analysis/th03-main-exact/gpt-dots-mima-combined-cold-v02/reference.tar`.

Keep actual current proof inputs in `.analysis/work/`:

- Scanner:`input-nostring.json`, `input-nostring.obj`, `input-assembly.obj`.
- Sound:`sound-bodies.json`,two stripped `sound-bodyN.c` inputs/four OBJ outputs.
- Selection:`selection-build.json`,both `selection-roundN.obj/.exe/.map` vectors,
  `selection-tail.cpp/.lnk`.
- Resources:`mainl-resources-build.json`,both `resources-roundN.obj/.exe/.map`
  vectors,`resources-root.asm/.lnk`.
- Loader:`mainl-loadprog-build.json`,both `loadprog-roundN.obj/.lib/.exe/.map`
  vectors,actual `loadprog-source.asm`, `loadprog-errno.inc`, `loadprog-library.rsp`,
  `loadprog-link.lnk`; retain exec/farheap inputs.
- Overlay:`mainl-exec-build.json`,both `exec-roundN.obj/.lib/.exe/.map` vectors,
  actual `exec-source.asm`, `exec-library.rsp`, `exec-link.lnk`; retain farheap inputs.
- Far heap:`mainl-farheap-build.json`,both `farheap-roundN.obj/.lib/.exe/.map`
  vectors,actual `farheap-source.asm`, `farheap-library.rsp`, `farheap-link.lnk`.
- Resident:`mainl-resident-build.json`,both six-object `resident-mini-roundN-*`/
  EXE/MAP vectors,six actual `resident-mini-NAME.asm` wrappers and `resident-mini.lnk`.
- Display:`mainl-display-build.json`,both `display-roundN.obj/.exe/.map`
  vectors,`display-root.asm/.lnk`,both six-object `display-mini-roundN-*`/EXE/MAP
  vectors,the six actual `display-mini-NAME.asm` wrappers and `display-mini.lnk`.
- Graphics:`mainl-graphics-build.json`,both `graphics-roundN.obj/.exe/.map`
  vectors,`graphics-root.asm/.lnk`,both `graphics-mini-roundN-*`/EXE/MAP vectors,
  actual `graphics-mini-memory.asm`, `graphics-mini-copy.asm`, `graphics-mini.lnk`.
- Archive:`mainl-archive-build.json`,both `archive-roundN.obj/.exe/.map` vectors,
  `archive-root.asm/.lnk`,both `archive-mini-roundN-*`/EXE/MAP vectors.
- BFNT:`mainl-bfnt-build.json`,both `bfnt-roundN.obj/.exe/.map` vectors,
  `bfnt-root.asm/.lnk`.
- File:`mainl-file-build.json`,both `file-roundN.obj/.exe/.map` vectors,
  `file-root.asm/.lnk`; retain real links for the DW? sentinel proof.

Acceptance baseline remains3e7e9dd; do not rewrite historical runtime hashes.
Keep `scripts/lib/zun.py` unchanged unless deliberately updating its frozen MAIN
binding. OP's builder is shared by MAINL/ZUN. Remove obsolete diagnostics after
preserving actual inputs/outputs. Next work includes real DOSCMD/DOSENV and further CRT providers,remaining DATA/table
ownership and integration of demonstrated native TU/library boundaries. Old cutscene3195/regist2720/root2488
aggregate rows overlap accepted functions; never count them again. Integrate
maintained state/tables and native reader/page-copy boundaries when deliberately
changing full recipes; do not rewrite cold hashes or rebuild everything for
progress. TH04 is an authorized source reference,not a replacement target or
build dependency. Re-attest Ghidra databases before use.
