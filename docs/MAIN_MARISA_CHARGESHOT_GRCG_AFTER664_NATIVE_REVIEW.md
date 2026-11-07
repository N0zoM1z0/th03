# Marisa charged-shot GRCG beam: original native source after664

The complete nine-function `cs_mari` physical Turbo C++ producer
was recovered directly into the original 99-object MAIN link.
It owns the full charged-shot state machine, two distinct launch
paths, a 12-sample vertical beam history, collision testing,
a large three-band GRCG renderer and the two-sided Gauge attack.
This is the original 1,509-byte CODE object, not a small helper
or a separately invented projectile format.

## Actual source recovery and native negative controls

- All four charged-shot inactive checks in creation, update,
  collision and rendering now use natural `!active` C++.
  Changed-source native stage `af664c` reproduced every original
  CODE byte and literal fixup field.
- The physical shot has a single **50-byte** record per player,
  consisting of `active`, `frame`, 12 16-bit X coordinates
  at +02, and 12 16-bit Y coordinates at +1A. Original TC4
  compiles `sizeof` and `offsetof` assertions for these
  fields; the large history update, three GRCG color bands and
  collision scan now name their different original sample
  bounds and 24-/36-frame transitions (`af664d`).
- The original Gauge dispatcher emits mirrored five-bullet
  side volleys on phases 0 and 12 of its 24-frame period,
  with pre-warning effects at phases 8 and 20. True frame
  phases and five-shot count are distinct compile-time names,
  with original byte codegen (`af664f`, `af664g`).
- The initial signed random Y assignment
  `-(int)randring2_next16_and(31) * 16` **cannot** simply
  be rewritten to `-TO_SP(randring2_next16_and(31))`:
  original TC4 code differed (`af664b`). The real RNG
  consumption and signed multiply remain.
- More subtly, replacing the 8-bit pellet speed decrement
  literal `6` with an equal-valued enum changes original
  CODE (`af664e`, isolated to one occurrence by `af664h`).
  Both original literal decrements remain. In contrast, the
  named five-shot loop bound is native-exact (`af664g`).
  A correct source must respect original TC4 code generation
  rather than assuming all equal-valued C++ constants match.

The final modified-source/OMF-COMENT-attested native proof:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af664i --units cs_mari
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af664i

Both independent original Turbo C++ 4.02 and TLINK rounds
reproduced **all 1,509 CODE bytes, 152 literal ordered OMF
FIXUPP fields, 9 PUBLIC offsets**, full original OMF segment
definitions and complete normal MAIN EXE/path-normalized MAP.
The Japanese program image, all 1,553 ordered MZ relocations
and the separately serialized 130,882-byte original Japanese
MAIN.EXE are byte-for-byte identical.

Receipt: `.analysis/work/exatt-layout-af664i/report.json`;
SHA-256 `7d4b56f0bb7b5fab60b119230f4004af1880909eb95c7f3ede4c6556531ce3a4`.
Native writer logs, two actual compiler outputs, overlay source,
original project response, full EXEs and MAPs are retained.
Only this one complete original object was rebuilt twice; the
other 98 original project objects and startup/CRT were reused,
so no complete cold replay was performed.

**Limits:** This improves maintainable natural source for
previously tracked original CODE; it is not new canonical
Factory packed-game byte credit, historical vendor raw OMF
packet identity or real PC-98 hardware runtime proof.
