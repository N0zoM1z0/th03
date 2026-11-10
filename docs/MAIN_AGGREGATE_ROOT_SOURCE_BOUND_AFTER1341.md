# Original 32-segment MAIN aggregate root: exact TASM physical source

The original `obj/th03/main.obj` has 32 physical segment definitions,
including zero-size placeholders for the separately reconstructed
character and engine objects. Its actual initialized contents comprise
**896 executable CODE bytes** (748 in `_TEXT`, 148 in `MAIN_04_TEXT`),
**1,289 initialized DATA bytes** in the 1,294-byte DATA segment, and
a 104-byte BSS segment. It owns **64 ordered OMF fixup fields** and
**127 PUBLICs**. These counts have their own physical-object denominator;
the source ledger's game CODE and this mixed vendor/game root are not
interchangeable totals.

The symbolic build composition is saved in
`config/main_work/root_carriers/th03_main.asm`, outside `src/main`
because it is an IDA-era root/foreign-library build carrier rather than a
newly decompiled standalone game translation unit. Its 57 recursive
includes are pinned against the TASM toolchain worktree. Three important
specialized includes use actual maintained game sources rather than the
older vendor versions:

- `th03/math/randring.inc` binds to `src/main/math/randring_getters.inl`
- `th03/hardware/sprite16_copy.asm` binds to `src/main/graphics/sprite16_copy.inl`
- `th03/formats/pfopen.asm` binds to `src/main/formats/pfopen.inl`

All remaining includes match the retained ReC98 reference. The original
1990s game target and vendor inputs are never edited; the independently
kept vendor reference is a required external build dependency, not
silently copied as authored game source.

Original TASM/TLINK stage `af1341b` reassembles only the complete root
physical object in two rounds. Both original 99-object normal links yield
the complete **byte-identical Japanese MAIN.EXE**, original normalized
MAP and ordered MZ relocation vector. Strict OMF comparisons bind every
initialized CODE/DATA byte, literal ordered fixup, PUBLIC offset and
all 32 original SEGDEFs, including the zero-length segment scaffolding.
No full cold replay of the source graph was run.

Negative `af1341c` changed just the first initialized value in the
story CPU safety frame table (`0x64` to `0x65`) in an isolated TASM input.
TASM succeeded but the strict initialized payload comparison rejected
it. The tracked source and Japanese target were unaffected.

Current read-only source and normal-link proof:

```
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_root_carrier.py --stage af1341b --check
```

This is a physical-object source-and-link receipt, not canonical Factory
packed-file or whole-game original-source authorship acceptance.
