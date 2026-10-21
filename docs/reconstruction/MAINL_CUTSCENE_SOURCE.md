# MAINL maintained cutscene source checkpoint

The opt-in owner is `src/mainl/cutscene.cpp`, specialized to the active TH03
branches of ReC98 revision `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`.
It owns the complete reviewed 095F:0B3E candidate contribution: thirteen bodies
(3,122 bytes), a compiler-produced 72-byte switch table, and one observed
producer byte. These 3,195 bytes now have a source-present checkpoint, not exact-byte credit.
The default MAINL build remains unchanged. Two independently materialized TCC
compilations produced byte-identical maintained objects; both hybrid TLINK runs
used 32 retained nonowned objects and preserved the entire raw EXE, MAP and all
677 ordered relocation records of the reviewed carrier. This is not a cold
whole-program build.

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

## Native recipe for a new independent experiment

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

## Earned proof (2026-10-21)

- Maintained objects: 7,592 bytes, both raw SHA-256
  `39e0d5d7cca8fc696da8bcb555751cc1b39ed80ea975eae84095c4a6e30d2b58`.
- Linked MAINL images: 67,372 bytes, both raw SHA-256
  `ff315af6f9cd197f78292d8c834a90afad7b4d6c9bda0a9f8b09d4bdbc12a1ad`.
- Both MAP files: raw SHA-256
  `f262e1d8e78d353f29e5f2d9a1cd39be91f934d48b0839b5ab55be6d9e033568`.
- Full fresh frozen baseline object is raw-identical to the retained frozen
  candidate. Maintained versus frozen object differences are only explicitly
  enumerated source-path/time dependency records; every ordered code, fixup,
  public, external, segment and other nondependency record is unchanged.
- Second maintained source mtimes were declared from observations of the first
  materialization before compiling. Neither object nor image was normalized.
- Both fresh linked images execute 53 selected scenarios / 65 entry calls using
  the existing numeric-parser, loader, gaiji and cursor contracts. Their runtime
  observation digest is `5acb86a213580c076b37bfc2e954e6ab732114b5817253e8442b36ffa553645d`.
  File/heap/ASCII tolower and gaiji-tail interfaces remain explicit models.
- All 56 cutscene relocation records and word values equal the decoded target.
  Raw bytes still differ exactly at 095F:140A, 1414 and 144B. Exact credit is zero.

`python3 scripts/replay_th03_mainl_cutscene.py --output .analysis/NEW_CUTSCENE_SOURCE_REPLAY.json`
revalidates the retained compiler/linker provenance, current maintained inputs,
raw products, scope and selected CPU observations. Use the project virtualenv
for Capstone/Unicorn. This command does not invoke native tools or claim a fresh
whole build. The original opt-in source stager remains the producer entry point.

Proof roots: `.analysis/mainl-cutscene-native-output-20261021-v01` and
`.analysis/mainl-cutscene-link-output-20261021-v02`. The source replay receipt is
`.analysis/mainl-cutscene-proof-checkpoint-20261021-v01/source-replay.json`.
Historical review: `.analysis/sol-mainl-cutscene-review-20261006.json` and
`docs/reconstruction/MAINL_CUTSCENE_REVIEW.md`. The source ledger and SVG count
only the disjoint 3,195-byte source extent, not the retained carrier or exactness.
