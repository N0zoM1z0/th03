# TH03 handoff

## Current checkpoint

Use natural source recovery and exact native output with direct local tools.
Session preflight is complete for the unchanged environment. Revalidate the
unchanged cold pair; rebuild affected producers. No native writer remains running.

MAINL now accepts graphics1439/heap628/stack-memory76 CODE and66 DATA:18 new
extents/26 procedures/2,209 bytes. ZUN's no-Y-clip writer202 is authored; remaining
2,007 bytes are library code/storage. Generated EDGES17 WORDs/BYTE_MASK8 BYTEs use
bit recurrences,not target literals. Clip16/heap8 initialized state and heap8 BSS
have maintained declarations; BSS adds no file bytes. See
[graphics/heap review](MAINL_GRAPHICS_NATIVE_REVIEW.md).

GRCG rectangle bank has two APIs and a shared6-byte return. Both packed writers
have one API plus shared6-byte clip exit. EGC_END aliases EGC_START:three bodies,
not four. Page copy has one far API and a private near plane helper. Heap has
eight APIs; HMEM_ALLOCBYTE tail-enters allocation,free can borrow its unwind.
Stack memory has two APIs and a shared6-byte ASSIGNALL continuation. Complete
near/far cleanup,all93 root fields and empty scoped MZ vectors are checked.
Sixteen genuine CS WORD fields read the already accepted RotTbl; they are not SMC.

New `page_copy.inl` replaces compatibility nopcall with ordinary calls. Independent
far declarations must be outside CODE:inside the same segment,TASM prematurely
optimizes them to four bytes. Outside CODE,it emits real five-byte9A calls and
FAR-pointer fields. Two actual mini links against the real heap/stack-memory
provider naturally emit NOP/PUSH CS/near CALL,matching the entire108 product bytes.
No source NOP padding is added. The frozen root retains compatibility calls as
contextual transport; integrate the demonstrated TU boundary in a future full
recipe change. Mini context has a real uninitialized32-byte stack and8-byte BSS.

Two actual selected GAME3 root assembly/link rounds reuse35 project objects/CRT;
whole raw OBJ/EXE/MAP vectors repeat and equal the pinned Japanese decoded target/
retained MAP. Five maintained state/table includes occupy original positions.
Complete native payload/public records and literal FIXUPP order agree. All938
cold outputs/source/recipe are restored and unchanged; no full cold/DIET replay.

Current acceptance validates the complete source/tool/library/cold graph,then
preserves old97 owner/native/runtime observations from3e7e9dd and six library
origin corrections. Decoder/resources/file/BFNT/archive/graphics reviews extend
it. All previous131 owner records and nested scopes remain unchanged this step.
No ancestor runtime matrices. OP acceptance reverified; OP/ZUN publications
untouched. Only MAINL SVG region/summary/source-present row were refreshed.

Receipts: `.analysis/work/mainl-graphics-build.json`, `mainl-graphics-native.json`,
`mainl-graphics-progress.json`. Focused native/acceptance/status/progress checks,
tracking and bounded generated-region checks PASS. `git diff --check` is clean.
Preserve caller DF where original code assumes it,CLD where present,GRCG's
CLI/stack extraction/STI and GAME3 glyph ADC/caller-CF quirk. No physical graphics,
DOS/heap execution or defensive product fixes are claimed.

## Accepted source scopes

| Product | Current scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 459 functions /78,737 CODE bytes /106 extents | Open |
| OP | 60 extents /92 procedures /13,221 CODE +1,764 DATA bytes | Open |
| MAINL | 149 extents /181 procedures /23,845 CODE +1,384 DATA bytes | Open |
| ZUN | 77 extents /89 procedures or entries /6,179 CODE bytes | Open |

MAINL accepts25,229 bytes:16,619 authored +8,610 library. ZUN accepts8,635 bytes:
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
preserving actual inputs/outputs. Next providers include palette/vsync/gaiji,
remaining resident/math/text and CRT scopes. Old cutscene3195/regist2720/root2488
aggregate rows overlap accepted functions; never count them again. Integrate
maintained state/tables and native reader/page-copy boundaries when deliberately
changing full recipes; do not rewrite cold hashes or rebuild everything for
progress. TH04 is an authorized source reference,not a replacement target or
build dependency. Re-attest Ghidra databases before use.
