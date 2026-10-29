# TH03 handoff

## Current checkpoint

Use natural source recovery and exact native output with direct local tools.
Session preflight is complete for the unchanged environment. Revalidate the
unchanged cold pair; rebuild affected producers. No native writer remains running.

MAINL now recovers buffered stream/position/write bank:10 TUs,1808 CODE+10
DATA/INIT bytes,12 extents,13 procedures. Previous193 owners/nested scopes unchanged;
authored bytes stay16,695. See [buffered I/O review](MAINL_STDIO_NATIVE_REVIEW.md).

Fseek492 contains near pop4 buffered-byte helper137,far fseek130/ftell225.
Preserve signed levels,text LF expansion,relative seek adjustment and append tell's
seek-end/restore behavior. FILE20 constants are an actual consumed shared include;
token checks use offset only. Setvbuf289 retains signed mode<=2,unsigned size<=7FFF,
first-stream flags,unchecked original ownership and ignored fseek return.

Write358 retains invalid-handle-first check,WORD count0/FFFF fast return,unchecked
append seek,CR/LF translation and short-write accounting. The128-byte threshold
is checked after both CR/LF bytes:127 ASCII+LF causes one129-byte DOS write and
returns input count128. A bounded native probe runs real translated/raw writers
with only successful DOS AH40h hooked,checking bytes,DS,stack and handle flags.
Raw write91,seek45 and isatty21 retain original DOS/carry/error behavior.

Fflush209 resets pending count/cursor before write; terminal short writes retain
success. Flushall76 counts open streams visited regardless of individual failure.
Exit flush63 visits exactly four slots. Setupio164 is a near startup callback;
its real INIT6 is type0/priority2/near offset/zero segment. Setvbuf's private flags4
are genuine initialized DATA. Sole new MZ relocation is CODE4EA7,the far exit-buffer
callback segment assignment. Near startup/callback offset words do not relocate.
All58 fields/payloads reviewed;20 far calls relax and3 near IOERROR calls consume2.
Only write+23 has the exact equivalent target-derived versus explicit same-CODE
frame. Retain both literal field streams; never sort MZ relocations.

Two actual TASM/TLIB/TLINK rounds compose25 source CRT providers:10 new,nine
validated reused natural pairs and six retained providers.893 positions/874 other
current members unchanged;36 project objects reused. Whole ten-OBJ/LIB/EXE/MAP
vectors repeat; full EXE/MAP equal pinned Japanese decoded target/retained MAP.
All938 cold outputs/source/recipe/tools unchanged. No full cold/DIET or ancestor
runtime replay. Frozen cold recipe remains six CRT replacements.

Receipts:`mainl-stdio-build.json`, `mainl-stdio-native.json`,
`mainl-stdio-progress.json` in`.analysis/work/`. Focused checks and tracking pass;
finish with diff checks. Old193 owners/scopes unchanged; OP acceptance reverified,
OP/ZUN publications untouched. Only MAINL SVG region/summary/source row refreshed.
Whole-product source ownership stays open; stream/handle table storage is contextual.

Earlier constructors retain RET12; null-first-entry DOSENV counts one byte but
writes two and returns aligned-offset+1. Do not generalize null-vector and
first-empty-string branches. See [constructor review](MAINL_DOSCONSTRUCT_NATIVE_REVIEW.md).

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
| MAINL | 205 extents /272 procedures or entries /32,770 CODE +1,918 DATA bytes | Open |
| ZUN | 77 extents /89 procedures or entries /6,179 CODE bytes | Open |

MAINL accepts34,688 bytes:16,695 authored +17,993 library. ZUN accepts8,635 bytes:
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
- Buffered I/O:`mainl-stdio-build.json`,both ten-object `stdio-roundN-NAME.obj`/
  `.lib`/`.exe`/`.map` vectors,actual ten `stdio-source-NAME.asm`, `stdio-layout.inc`,
  `stdio-library.rsp`, `stdio-link.lnk`; retain all nine reused natural pairs.
- Paths:`mainl-path-build.json`,both four-object `path-roundN-NAME.obj`/
  `.lib`/`.exe`/`.map` vectors,actual `path-source-NAME.asm` for fullpath,getdcwd,
  _pathops,dosgdriv, `path-library.rsp`, `path-link.lnk`; retain all five reused pairs.
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
