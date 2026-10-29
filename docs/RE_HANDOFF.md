# TH03 handoff

## Current checkpoint

Use natural source recovery and exact native output with direct local tools.
Session preflight is complete for the unchanged environment. Revalidate the
unchanged cold pair; rebuild affected producers. No native writer remains running.

MAINL now recovers complete DOS command/environment constructors:311+365 CODE,
2 near entries. All previous185 owners/nested scopes unchanged; authored bytes
stay16,695. See [constructor review](MAINL_DOSCONSTRUCT_NATIVE_REVIEW.md).

Both use RET12 for three far pointer arguments. The loader correctly omits
caller cleanup at these two calls; deferred cleanup elsewhere concerns far C
calls. DOSCMD's third pointer only enables argv copying; argv still contributes
to allocation size when copying is disabled. Preserve wrapped sizes,spaces,
CR/NUL and low-byte command length. DOSENV aligns destination offset/unchanged
segment and separately stores raw allocation. Preserve offset-only alignment
and required-size arithmetic. Null env vector/null first entry writes two NULs;
first-entry empty string writes one. Null first entry counts only one byte but
writes two,so return is aligned-offset+1. One bounded native three-case probe with
only successful malloc hooked confirms terminators,return offsets and RET12.

Entire initialized payloads match original. Each module has five ordinary far
fields. Retain old/TASM emitted streams separately; compare geometry by site,
never sort MZ relocations. All10 call relaxations independently resolve; complete
CODE,local branches,near callee-pop12 returns and empty scoped MZ vectors checked.

Two actual TASM/TLIB/TLINK rounds compose all11 source CRT providers:two new,
reused natural farheap/exec/loadprog pairs and six retained providers.893 member
positions/all888 other current payloads unchanged;36 project objects reused.
Whole raw two-OBJ/LIB/EXE/MAP vectors repeat; full EXE/MAP equal pinned Japanese
decoded target/retained MAP.938 cold outputs/source/recipe/tools unchanged. No
full cold/DIET or ancestor runtime replay. Frozen cold recipe remains six CRT
replacements; bounded combined recipe establishes coexistence of eleven.

Receipts:`mainl-dosconstruct-build.json`, `mainl-dosconstruct-native.json`,
`mainl-dosconstruct-progress.json` in`.analysis/work/`. Focused checks and tracking
pass; finish with diff checks. Old185 owner records/scopes unchanged; OP acceptance
reverified,OP/ZUN publications untouched. Only MAINL SVG region/summary/source row
refreshed. Whole-product source ownership stays open.

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
| MAINL | 187 extents /250 procedures or entries /29,715 CODE +1,886 DATA bytes | Open |
| ZUN | 77 extents /89 procedures or entries /6,179 CODE bytes | Open |

MAINL accepts31,601 bytes:16,695 authored +14,906 library. ZUN accepts8,635 bytes:
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
- Constructors:`mainl-dosconstruct-build.json`,both `dosconstruct-roundN-doscmd.obj`/
  `dosconstruct-roundN-dosenv.obj`/`.lib`/`.exe`/`.map` vectors,actual
  `dosconstruct-source-doscmd.asm`, `dosconstruct-source-dosenv.asm`,
  `dosconstruct-library.rsp`, `dosconstruct-link.lnk`; retain all three reused pairs.
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
preserving actual inputs/outputs. Next work includes further CRT providers,remaining DATA/table
ownership and integration of demonstrated native TU/library boundaries. Old cutscene3195/regist2720/root2488
aggregate rows overlap accepted functions; never count them again. Integrate
maintained state/tables and native reader/page-copy boundaries when deliberately
changing full recipes; do not rewrite cold hashes or rebuild everything for
progress. TH04 is an authorized source reference,not a replacement target or
build dependency. Re-attest Ghidra databases before use.
