# Shared runtime near frames and original OP MAP after538

Five bounded shared TUs refine existing owners: `heap_break.asm`, `dos_write.asm`,
`execl.asm`, `load_program.asm` and `dos_resize.asm` in `src/shared/crt/`.
They contain **1,648 existing CODE / 42 DATA bytes**. No new function, compiler
member or CODE-extent credit is added. All frozen historical sources and native
receipts remain unchanged.

## Exact changes and explicit remaining limits

| Member / original slot | Original CODE / DATA | Literal fields | Change |
| --- | ---: | ---: | --- |
| `fbrk` / 167 | 352 / 2 | 33 | Six near frames, original eight-import order |
| `write` / 331 | 358 / 0 | 9 | Near `__IOERROR` frame at CODE+23 |
| `execl` / 346 | 35 / 0 | 2 | Near `__LoadProg` frame at CODE+26; complete ordered equality |
| `loadprog` / 891 | 871 / 40 | 32 | Near `__DOSCMD` / `__DOSENV` frames at +633/+754 |
| `setblock` / 363 | 32 / 0 | 1 | Original literal BSS/DATA GROUP restored; ordered equality retained |

The first four use the already pinned compatible JWasm emitter, with original
near/far declarations and actual call distances preserved. Moving heap helper
imports outside their CODE segment leaves their segment undefined until link,
producing original TARGET frame5. The data imports retain DATA/DGROUP ownership
and are declared in the real original import order. `setblock` instead retains
TASM: its original near error call correctly uses CODE frame0. Its reversed
TASM GROUP operands now emit original BSS/DATA membership.

The source explicitly selects the original full-width AX immediate forms and
near-jump widths. Internal `grow_break`, `find_path_separator` and `probe_program`
procedures are PRIVATE, preserving the original public namespace. These are
source language/encoding constraints, not inserted instructions or object edits.
All complete initialized bytes, true holes, segment order/attributes, public
identities/offsets, import order, literal GROUP and entry semantics match actual
installed CL.LIB. Every one of the **77 full fields** agrees at its original
site, including original numeric import indices and all frame/target/addend bits.

**Only `execl` and `setblock` have complete original ordered field equality.**
`fbrk`, `write` and `loadprog` still emit their correct fields in a different
order. The verifier retains both full lists, checks per-site attributes, and
reports these order gaps explicitly. It never turns a sorted comparison into
an ordered-equality claim or changes native FIXUPP output. Complete original
OMF-program identity is not claimed; record packing and name indices can differ.

The standard compiler/helper binary and source revision are re-attested through
`config/th03_zun_driver_jwasm.toml`. The bounded profile is
`config/th03_runtime_after538.json`. This is a compatible-emitter proof, not
identification of the original assembler.

## Two retained native rounds, two actual products

Two fresh four-JWasm/one-TASM/TLIB rounds replace five original slots, retaining
all **888 other source member programs and all 893 positions**. Both products
reuse after535's source-generated C0 and their current source-bound game objects.
After537's corrected shared exec initialization and 21 literal fields remain
unchanged. Every selected material segment is independently compared to actual
original CL.LIB, including bytes, holes, attributes and native MAP ownership.

Both **ten-file** five-OBJ/LIB/two-EXE/two-MAP vectors repeat byte-for-byte:

- MAINL: complete original **67,372-byte EXE / 677 ordered MZ relocations**.
- OP: complete original **63,866-byte EXE / 607 ordered MZ relocations**, plus
  complete raw equality to the historical **68,078-byte OP MAP**.
- MAINL's **80,967-byte MAP** differs from after537 only by omitting zero-sized
  `fbrk` BSS at existing `0E3F:2872` and adding original zero-sized `setblock`
  BSS at existing `0E3F:2880`. Every material row, address, size, flag and other
  MAP byte agrees. The comparator checks exactly those two literal rows.

Both actual original 36,041-byte packed OP proofs are reused from after537:
decoded input is identical and the pinned tool/context is unchanged. No new
DIET invocation or fresh packed output is claimed. No game objects, native
cold graph, ancestor runtime models or whole-product CI are rebuilt/replayed.

Producer: `scripts/build_th03_runtime_after538_work.py`.
Independent reviewer: `scripts/review_th03_runtime_after538_work.py`.
Root: `.analysis/work/runtime-after538-build.json`.
SHA-256: `7647b0fdf6bc43c769d526422cad48907d1e58c0d31260766b0a7936f61cbb07`.
MAINL MAP SHA-256:
`cca9d579087ba6bdf7eca0bdee9e2df03c7a50090377cc8f56e4db2e78f5b515`.
OP MAP SHA-256:
`2666a302659c05b2c7d949db089cf01383f2abc19ca3cc996be052138bcbb00a`.

All twenty whole native outputs and seventeen writer logs remain under
`.analysis/work/runtime-after538-*`. Actual consumed sources, ABI includes,
immutable recipe/profile, extracted inputs, source C0 and both library/link
responses remain in `TH03ML/probe/af538l` and `TH03OP/probe/af538l`.
All parent pairs and packed proof files remain at their original paths.

Earlier bounded probes af538a–k remain. Removing CS assumptions failed; far
declarations with explicit near calls did not fix TASM's frame choice. The
compatible emitter established the real target-derived frame. Native width,
import/GROUP ordering and helper visibility corrections were checked before
the final producer. The first link exposed three unintended helper exports;
that candidate, its exact MAP differences, sources, objects and logs remain
separate. No failed output was patched or adopted and no output cleanup ran.

Independent native review, progress/tracking and whitespace checks pass.
The updated diagnostic inventory
`.analysis/work/runtime-after538-selected-literal-field-audit.json` has 57
literal-equal selected OP members and 19 with order-only differences; no
per-site field attribute/import-index difference remains in those 76 members.
This is an investigation inventory, not new source-exact credit. C0's
58-field ordering gap and whole-product ownership limits remain. Formal
canonical Factory credit is unchanged; MAINL remains **0/250**.
