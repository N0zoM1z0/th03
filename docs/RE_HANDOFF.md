# TH03 handoff

## Current checkpoint

Use natural source recovery and exact native output with direct local tools.
Preflight and scoped compiler attestation are complete. Revalidate the
unchanged cold pair; rebuild affected producers. No native writer remains running.

Natural C++ new/xalloc/xmsg now passes exact native review. MAINL accepts211
extents/288 procedures/36,946 bytes. The six new owners2258 bytes contain1563
instruction bytes in16 far bodies,659 inline EH/type/cleanup DATA bytes,30 other
initialized DATA/INIT/EXIT bytes and6 uninitialized static-object file bytes.
Source presence stays240 extents/47,388 gross bytes. See
[C++ native review](MAINL_EXCEPTION_CPP_REVIEW.md).

The missing producer option was BCC4.5 `-O1`,not extra source variables or
register annotations. The nonoptimizing BCC4.5 payloads equal TCC4.02 and retain
735/502/935-byte gaps; optimizing native output reproduces754/513/955. BCC4.00
rejects -xc and emits a different initializer ABI. Original compiler installation
is unproved; the scoped optimizing producer's suitability is demonstrated by
complete actual output. `config/mainl_work/exception_toolchain.toml` pins its
private isolated BCC/RTM/DPMI files. Existing TC4/TASM/tools/targets stay pinned.

Preserve zero-to-one new size,retry through installed far handler,null-handler
return,static xalloc("Out of memory",0),deep string copies,throw-by-value and
delete-before-new assignment. Xmsg ctor167 is followed by a36-byte cleanup
record,not more code. New DATA24 has18 initializers and6 uninitialized object
bytes. The latter use actual two-round linked file bytes,without synthesized
zeros/source initializers. INIT/EXIT6 each remain separate contributions.
Summary initialized DATA2607 and uninitialized file DATA6 are separate; progress
image DATA2613 includes both. No BSS file credit is added.

Two actual optimizing compiler/TLIB/TLINK rounds repeat full three-OBJ/LIB/EXE/MAP
vectors; whole EXE/MAP match fixed Japanese decoded target/retained MAP. All122
literal fields,complete payloads,packing/group order/publics,independent linked
bytes and ordered MZ vectors pass. Xalloc/xmsg vectors descend; never sort or
rewrite them. Normal893-member library now composes28 source providers with19
validated reused natural pairs;871 other current members remain unchanged. All205
prior owners/scopes and938 cold outputs stay intact. No full cold/DIET or ancestor
runtime chain is replayed. Old failed CPP receipts are historical; their obsolete
tracked candidate verifier/tests have been replaced by native ownership review.

Current receipts:`mainl-exception-native-build.json`,
`mainl-exception-native-review.json` and publication/progress logs in`.analysis/work/`.
The xx dispatcher12622-byte contribution is still unowned. Continue natural
source recovery there or at another complete CRT/provider boundary; its inline
metadata also needs ownership classification. Earlier accepted buffered I/O1808
CODE+10 DATA/INIT retains its source and receipts.

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
| MAINL | 211 extents /288 procedures or entries /34,333 CODE +2,613 file DATA bytes | Open |
| ZUN | 77 extents /89 procedures or entries /6,179 CODE bytes | Open |

MAINL accepts36,946 bytes:16,695 authored +20,251 library. ZUN accepts8,635 bytes:
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
TC4/TASM/JWasm,scoped BC45 compiler/runtime,`.tools/ghidra`,`.tools/jdk`,`.venv`,`_reference/ReC98` and
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
- C++ native:`mainl-exception-native-build.json`,both three-object
  `exception-native-roundN-NAME.obj`/`.lib`/`.exe`/`.map` vectors,actual three
  `exception-native-source-NAME.cpp`, `exception-native-library.rsp`,
  `exception-native-link.lnk` and native phase logs; preserve19 reused natural
  pairs,recorded SDK headers and scoped BC45 installed/active tool files.
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
