# MAINL maintained cutscene source checkpoint

The opt-in owner is `src/mainl/cutscene.cpp`, specialized to the active TH03
branches of ReC98 revision `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
It owns the complete reviewed 095F:0B3E candidate contribution: thirteen bodies
(3,122 bytes), a compiler-produced 72-byte switch table, and one observed
producer byte. These 3,195 bytes are **not exact or source-accepted credit** at
this checkpoint. The unit remains boundary-reviewed until independent native
compiler/runtime/reproducibility evidence satisfies the existing intake rules.

## Ownership and preserved behavior

- `src/mainl/cutscene.cpp`: script loading/freeing, picture copy/masked blits,
  text-box allocation/snapshot/free/restore, cursor movement, opcode dispatch,
  and the blocking text/command animation loop.
- `src/mainl/cutscene/script.inl`: first/second numeric parameter bodies and
  filename/BGM/fade/shake macros, included once at their original producer slot.
- `src/mainl/cutscene/egc_start_copy.inl`: the owned near EGC-start body, included
  under the original naming macro, with explicit compatibility register macros.
- `src/mainl/cutscene/cutscene.hpp`: near-call declarations.

Function/declaration order, `-zPgroup_01`, `-a2`, near/Pascal declarations,
ctype calls, far-offset arithmetic, input timing and redundant page changes
are retained. Allocation/read failures are still unchecked. Numeric parsing
still eagerly reads three bytes and rewinds unused bytes. NUL remains a skipped
control byte rather than EOF. The two gaiji calls retain differing IDs; carry
is path- and pointer-wrap-dependent, not universally set after every number.
No padding, target-byte insertion, object modification or relocation rewriting
has been introduced.

Mutable globals remain in frozen `th03/cutscene/cutscene[bss].asm`, and
`CUTSCENE_KANJI` remains in `th03_mainl.asm`. This is code ownership, not
closed data/BSS ownership.

The two new compatibility shims expose existing picture dimensions and EGC
register macros. Existing platform/master/PI/input/sound/text/frame-delay/color
compatibility dependencies remain explicit, not newly claimed as owned code.
The stage manifest lists all four owned and ten compatibility inputs. Full
archived transitive headers and libraries remain outside this owner.

## Focused checks

Run `python3 -m unittest discover -s tests -p 'test_mainl_cutscene_source.py'`
and the progress tests. The ten source/stage checks include frozen-reference
SHA binding and active-code equivalence for all four owned inputs, nested GAME
branch selection, consumed wrapper/manifest identity, no-overwrite staging,
and negative checks for missing/undeclared/symlinked inputs and lost group pragma.
This is source evidence only, not a native or physical-device test.

`python3 scripts/stage_th03_mainl_cutscene.py --output .analysis/NEW_CUTSCENE_OVERLAY`
creates an exclusive, source-only overlay. It changes no default build, invokes
no native tool, and never reads a target executable. Its `th03/cutscene.cpp`
wrapper consumes the maintained owner in the original compilation slot.

## Next native experiment

1. Materialize a fresh archive of the frozen ReC98 revision into a private run.
2. Merge the staged overlay's `th03`, `src`, and `compat` source trees into that
   archive, preserving all other source and build inputs. Do not copy `stage.json`
   into the compiler source graph; retain it with the run evidence instead.
3. Compile the existing `th03/cutscene.cpp` slot with the frozen MAINL GAME=3,
   BINARY='L', large-model compiler flags. Keep the module name and linker order;
   do not compile `src/mainl/cutscene.cpp` as a separate second module. First
   inspect the fresh OMF contribution before attempting the whole MAINL link.
4. Retain original OBJ/MAP/EXE and logs. Inspect CUTSCENE_TEXT's full 3,195-byte
   contribution, emitted tables and all 56 ordered relocation words. Compare
   both to the decoded target and to the retained reference candidate without
   normalizing or patching either. Repeat independently if the first run works.

Historical candidate bytes differ from the target at 095F:140A, 1414 and 144B,
calling cached PI entries 0529/054E rather than target 052A/054F. The source
checkpoint does not resolve these differences. The natural PI producer/linker
layout, full interpreter behavior, physical EGC/VRAM/input/timing, data/BSS,
packaging and whole-program Oracles remain open.

Retained review: `.analysis/sol-mainl-cutscene-review-20261006.json` and
`docs/reconstruction/MAINL_CUTSCENE_REVIEW.md`. Historical build paths in that
receipt are provenance, not a promise that the original build directories still
exist. The SVG shows this owner as native-proof-pending without increasing the
source/exact bars.
