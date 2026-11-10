# Three original MAIN geometry and collision source scopes

The maintained 16-bit symbolic TASM sources now bind three additional
original physical objects in the 99-object Japanese TH03 MAIN link:

| Original object | Maintained source | CODE | Ordered fixups | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| `vectorfar` | `src/main/math/vector_far.asm` | 160 | 5 | 2 |
| `playfld` | `src/main/playfield/playfld.asm` | 118 | 3 | 3 |
| `collmap` | `src/main/collision/producers/collmap_native.asm` | 432 | 27 | 3 |
| **Total** | | **710** | **35** | **8** |

The vector owner preserves the two far Pascal 2D-vector constructions
and their EVEN alignment; playfield conversion and clipping retain the
three complete original far entries. The collision map comprises the
three near 386-bitstrip generator functions. Its producer includes the
real maintained `src/main/collision/map.asm`, and the scoped verifier
checks that the TASM worktree copy and the maintained file have identical
content and source hash. Both historical collision source objects
(`af591c` rounds 1 and 2) have identical complete physical semantics.

The current source-bound stage `af1332c` assembles all three using the
original TASM 5.0 in two independent rounds and substitutes them into
the unchanged original TLINK 6.10 response. Both complete Japanese
MAIN executables are byte-identical to the frozen original normal link,
with the full normalized MAP and ordered MZ relocation vector equal.
The strict object comparison checks all initialized CODE, literal ordered
native OMF fields, PUBLIC offsets and segment definitions. A separate
initial `af1332b` link independently combined all three objects and
matched the complete original image. No unrelated project objects or
CRT were recompiled.

This adds three distinct physical source-bound owners, not first-time
ownership of all underlying gameplay bytes or original historical
authorship. The separate input scanner link-provenance gap remains open.

Read-only current-source review:

```
PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_geometry_asm.py --stage af1332c --check
```
