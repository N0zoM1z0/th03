# TH03 handoff

## Current checkpoint

Use natural source recovery and exact native output with direct local tools.
Session preflight is complete for the unchanged environment. Revalidate the
unchanged cold pair; rebuild affected producers. No native writer remains running.

MAINL now recovers the complete1115-byte paragraph far heap:1103 CODE+12
file-backed CS storage,14 procedures/ABI entries,all library. Previous181 owners
and nested scopes unchanged; authored bytes stay16,695. See
[far-heap review](MAINL_FARHEAP_NATIVE_REVIEW.md).

New natural farheap.asm covers circular rover allocation,physical neighbor
coalescing,top/interior free,heap start/growth and realloc shrinking/moving.
Returned pointer offset4/header layout is preserved. free/farfree alias one body;
word/long malloc and realloc entries share far-return bodies. Free insertion
temporarily accesses the rover through SS under CLI,restoring SS before POPF.
Realloc growth copies12 initial bytes,then up to64KiB chunks. Keep global scratch,
16-bit wrapping,ignored offset words,CLD,partial-growth failures and pre-brk state
writes; no defensive fixes or physical DOS execution claim.

Three real zero CS WORDs first/last/rover occupy6 bytes. Three scratch WORDs
(saved DGROUP,pending resize high/low) remain DW? with no LEDATA. Only those6
file bytes use actual independently repeated selected links,never invented zeros
or new source initializers. TASM needs explicit DS: to disambiguate constant
node offsets; emitted default-DS instructions have no extra prefixes.

Complete native initialized payload and all49 absolute ordered native fields
match the original member. Packetization may differ; field order is never sorted.
BYTE CODE/WORD empty DATA/DGROUP,all public state/API aliases,complete physical
bodies/shared exits and empty literal scoped MZ vector checked. Two actual
TASM/TLIB/TLINK rounds replace only farheap,retain all893 positions/892 other
current member payloads and reuse36 project objects. Whole raw OBJ/LIB/EXE/MAP
vectors repeat; full EXE/MAP equal pinned Japanese decoded target/retained MAP.
All938 cold outputs/source/recipe/tools restored and unchanged. No full cold,
DIET or ancestor runtime replay. The full cold recipe still replaces six CRT
members; this selected recipe demonstrates the seventh natural source provider.
Integrate deliberately when changing full recipes,without rewriting cold hashes.

Receipts:`mainl-farheap-build.json`, `mainl-farheap-native.json`,
`mainl-farheap-progress.json` in`.analysis/work/`. Focused native/acceptance/status/
progress and tracking pass; finish with diff checks. OP acceptance reverified;
OP/ZUN publications untouched. Only MAINL SVG region/summary/source-present row
refreshed. Whole-product source ownership and physical devices remain open.

Earlier findings:joystick103 has four bodies and three EVENs;2AAD/2B15 zeros
stay uncredited. CREATE/JS_END use proven ordinary far calls. CRT628+93 six
members retain near/far bridges and FFFF DOS resize collision. Palette EQU aliases
XOR immediate18B8 without ORG. VSync CS vector4 stays DW?;DATA0849 target90 vs
ordinary EVEN00 is uncredited. MAIN EC2D90 vs00 and MZ headers6240/7680 bytes,
relocation offsets28/62 remain open;1553 ordered entries agree. No padding fixes.

## Accepted source scopes

| Product | Current scopes | Whole-product source exactness |
| --- | --- | --- |
| MAIN | 459 functions /78,737 CODE bytes /106 extents | Open |
| OP | 60 extents /92 procedures /13,221 CODE +1,764 DATA bytes | Open |
| MAINL | 182 extents /243 procedures /27,497 CODE +1,584 DATA bytes | Open |
| ZUN | 77 extents /89 procedures or entries /6,179 CODE bytes | Open |

MAINL accepts29,081 bytes:16,695 authored +12,386 library. ZUN accepts8,635 bytes:
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
