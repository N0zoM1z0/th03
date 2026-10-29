# TH03 handoff

## Current checkpoint

Use natural source recovery and exact native output with direct local tools.
Session preflight is complete for the unchanged environment. Revalidate the
unchanged cold pair; rebuild affected producers. No native writer remains running.

MAINL recovers complete933-byte DOS overlay exec:671 CODE+262 file-backed
CS storage,one574-byte near cdecl API and97-byte copied continuation. Both entry
kinds are explicit; no second C function claimed. All library; previous182 owners/
nested scopes unchanged; authored bytes stay16,695. See
[overlay review](MAINL_EXEC_NATIVE_REVIEW.md).

Typed uninitialized work fields occupy257 bytes:143-byte odd-top stack,PSP WORD,
80-byte path,two FCB bytes,24-byte MZ header,two loader WORDs,saved environment WORD.
Only those file bytes use actual repeated fresh links. Relative transfer vector4
and sticky environment flag1 are real initializers. No zero array/error string.
The copied region352 includes255 work bytes+97 instructions; entry255 and MZ
transfer references are relative to the copy. No native fixup occurs inside it.

__exec preserves PSP command-tail/FCB setup,DOS block query/resize,MZ/COM size and
entry/stack handling,environment scan/copy,unchecked path copy and sticky state.
The continuation loads via DOS4B03h,restores SS:SP/PSP and transfers without return.
Its failure write15 bytes from buffer start remains unchanged. Error unwind calls
real near callee-pop IOERROR. A genuine far __cexit call naturally relaxes through
TLINK. DGROUP@ reads the actual CS startup WORD at026D,not a segment constant.
No defensive fixes or physical DOS behavior claim.

Complete initialized payload matches original. All21 fields preserve literal
order/sites/targets/addends; four DOS globals use explicitly reviewed equivalent
DGROUP frames instead of target frames. BYTE CODE/WORD empty DATA,DGROUP,public
entry,full local branches/regions and empty scoped MZ vector checked.

Two actual TASM/TLIB/TLINK rounds compose exec with the reused,validated natural
farheap object and six retained source CRT providers:all eight now coexist in one
normal library.893 positions/all891 other current member payloads unchanged;
36 project objects reused. Whole raw OBJ/LIB/EXE/MAP vectors repeat; full EXE/MAP
match pinned Japanese decoded target/retained MAP. All938 cold outputs/source/
recipe/tools unchanged. No full cold/DIET or ancestor runtime replay; farheap is
reused,not reassembled. The full cold recipe still has six replacements; this
selected combined recipe demonstrates integration of two newer providers.

Receipts:`mainl-exec-build.json`, `mainl-exec-native.json`,
`mainl-exec-progress.json` in`.analysis/work/`. Focused native/acceptance/status/
progress and tracking pass; finish with diff checks. Previous182 owners and scopes
unchanged; OP acceptance reverified and OP/ZUN publications untouched. Only MAINL
SVG region/summary/source-present row refreshed. Whole-product source ownership
and physical devices remain open.

Earlier findings:farheap1115 has1103 CODE+12 CS state,14 procedures/ABI entries;
three scratch WORDs remain DW?. Joystick103 excludes2AAD/2B15 zeros. CREATE/JS_END
use proven far calls. CRT628+93 preserves near/far bridges andFFFF DOS resize
collision. Palette EQU aliases XOR immediate18B8 without ORG. VSync CS vector4
stays DW?;DATA0849 target90 vs EVEN00 uncredited. MAIN EC2D90 vs00 and MZ headers
6240/7680 bytes,relocation offsets28/62 remain open;1553 entries agree. No padding.

## Accepted source scopes

| Product | Current scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 459 functions /78,737 CODE bytes /106 extents | Open |
| OP | 60 extents /92 procedures /13,221 CODE +1,764 DATA bytes | Open |
| MAINL | 183 extents /245 procedures or entries /28,168 CODE +1,846 DATA bytes | Open |
| ZUN | 77 extents /89 procedures or entries /6,179 CODE bytes | Open |

MAINL accepts30,014 bytes:16,695 authored +13,319 library. ZUN accepts8,635 bytes:
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
preserving actual inputs/outputs. Next work includes further contextual CRT providers,remaining DATA/table
ownership and integration of demonstrated native TU/library boundaries. Old cutscene3195/regist2720/root2488
aggregate rows overlap accepted functions; never count them again. Integrate
maintained state/tables and native reader/page-copy boundaries when deliberately
changing full recipes; do not rewrite cold hashes or rebuild everything for
progress. TH04 is an authorized source reference,not a replacement target or
build dependency. Re-attest Ghidra databases before use.
