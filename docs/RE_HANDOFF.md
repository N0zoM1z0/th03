# TH03 handoff

## Current checkpoint

Use natural source recovery and exact native output with direct local tools.
Preflight and scoped compiler attestation are complete. Revalidate the
unchanged cold pair; rebuild affected producers. No native writer remains running.

Latest work is `xx_dispatch.inl` plus `xx_abi.h`: a bounded include in the
original xx.cpp TU,not a new product TU. Its original bank72B3..78CF is1565
bytes:1533 instructions in five complete procedures and32 CS table/tag bytes.
Main dispatcher is880 bytes,local_unwind447; do not count the whole public-symbol
gap as dispatcher code. Source presence is241 extents/48,953 gross bytes;
accepted MAINL stays211 extents/288 procedures/36,946 bytes.
See [xx dispatch review](MAINL_XX_DISPATCH_REVIEW.md).

Two actual BCC4.5 -O2-pg -Os -Z- -S / TASM / miniature TLINK rounds repeat
full generated ASM/two-OBJ/mini-EXE/MAP vectors. Candidate CODE1566 has the
original three public entry offsets,but fails whole-bank raw equality. Seven
surrounding helper interfaces remain unresolved for full-TU integration. Trap
providers are diagnostic-only and must never be treated as runtime replacements.
The whole product/library was not linked; no exact credit is added. All211
accepted owners/publication/verifier inputs and938 cold outputs remain unchanged.

Preserve DOS ABI: SS:14 near chain,SS:16 far runtime pointer,registration DS/SI
at14/16,DWORD initial dtor count at26,descriptor free DS at24 and far callback26.
Header describes used prefixes,not every original allocation size. ES indirect
callback operands require explicit OFFSET DGROUP framing. Near destructor table
pointers take the context table's segment. One actual target/source negative
constant C-filter probe confirms noncontinuable context0010->0006,return0 and
far cdecl SS/register traffic; no helper is executed. Other runtime branches and
physical DOS behavior remain unproved. Retain original unchecked descriptor use.

A private `TH03-mainl-decoded-fixed` Ghidra database was independently attested
against the existing67372-byte decoded Japanese target before observations.
Current receipts:`mainl-xx-dispatch-build.json`, `mainl-xx-dispatch-review.json`,
`mainl-decoded-fixed-attestation.json`; the old packed MAINL DB is not a decoded
runtime analysis. Ghidra sizes/signatures remain hypotheses. Next recover the
surrounding xx helpers and integrate the whole TU; do not normalize the candidate.

Earlier natural C++ new/xalloc/xmsg exact ownership retains six owners2258
bytes:1563 CODE,659 inline DATA,30 other initialized DATA and6 genuinely
uninitialized file-storage bytes. The suitable scoped producer is BCC4.5 -O1,
using pinned TC4 headers. Keep its recipe separate from the xx diagnostic profile.
Preserve zero-to-one new size,retry through installed far handler,null-handler
return,static xalloc("Out of memory",0),deep copies,throw-by-value and
delete-before-new assignment. New DATA24 has18 OMF initializers and6 source
reserve bytes supplied by the two real links; no initializer or BSS credit is
invented. Summary initialized DATA2607 and uninitialized file DATA6 stay separate;
progress DATA2613 includes both.

The accepted28-provider normal893-member library composes19 validated reused
natural pairs with871 other current members unchanged. Both whole raw native
vectors and EXE/MAP equality remain valid; validate/reuse them rather than
rebuilding. Retain `mainl-exception-native-build.json` and
`mainl-exception-native-review.json`,all accepted owners/scopes and938 cold
outputs. Earlier buffered I/O1808 CODE+10 DATA/INIT and its receipts remain valid.
See [C++ native review](MAINL_EXCEPTION_CPP_REVIEW.md).

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

- XX candidate:`mainl-xx-dispatch-build.json`, `mainl-xx-dispatch-review.json`,
  both `xx-dispatch-roundN-xxdisp.asm/.obj`, `xx-dispatch-roundN-xxctx.obj`,
  `xx-dispatch-roundN-xxmini.exe/.map`; actual `xx-dispatch-wrapper.cpp`,
  `xx-dispatch-source-xxbank.inl`, `xx-dispatch-source-xx_abi.h`,
  `xx-dispatch-context.asm`, `xx-dispatch-mini.lnk` and native phase logs.
  Preserve the scoped BC45 files and all64 bound available SDK headers.
  Retain the derived decoded database/attestation and original xx OMF context.

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
