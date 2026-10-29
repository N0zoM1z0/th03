# OP title animation native source review

2026-10-29: the current `th03/op_main.cpp` TC4 producer has complete CODE
ownership: five contiguous procedures,902 bytes,97 native fields and53 literal
ordered MZ relocations. The unchanged cold pair's complete source/tool/output
bindings are revalidated. No new native build or runtime matrix is claimed.

| Procedure | CS-relative offset | CODE | Native return cleanup |
| --- | --- | --- | --- |
| Opening animation | 14E2 | 550 | Near0 |
| Fade-in animation | 1708 | 167 | Near0 |
| Main to submenu box | 17AF | 44 | Near0 |
| Submenu to main box | 17DB | 47 | Near0 |
| Restore16-pixel column | 180A | 94 | Near Pascal2 |

The first four functions are the complete808-byte
`src/op/menu/title_animation.inl` owner. The final94 bytes belong separately to
`src/op/menu/column_restore.inl`. The wrapper includes `th03/op/m_main.cpp`,
whose two literal includes consume these maintained files. Every native
dependency is checked against the current source graph and staged file.

The compiler's sole OMF group is DGROUP over DATA/BSS; CODE is allocated by
the linker into GROUP_01. Do not apply the selection producer's group2 DATA
assumption here. All97 fields are resolved independently from both MAP public
tables, including ordinary external DGROUP fields, private string-pool offsets,
far calls and four actual self-relative near calls to selection CDG loads.
No object or executable is patched. The complete linked contribution and each
function's real near return/argument cleanup are checked against the pinned
Japanese target and current candidate. Native field and MZ order are retained.

## Superseded column mismatch

The old title ledger described a three-byte raw encoding difference in the
column helper. That is historical evidence from an earlier producer. The
current maintained symbolic raster source already emits all94 target bytes
without fixups, including `ADD DI,AX`, `XOR AL,AL` and the compiler-owned
BP/SI/DI saves and Pascal argument cleanup. The current full cold graph consumes
that source. The new review establishes ownership; it does not claim a new
codegen fix or rerun the old raster diagnostic.

## Original animation behavior

The opening550-byte function retains its initial page0 displacement by2 pixels,
then72 page-flipped shifts by4 pixels, for2 pixels of visible motion per frame.
Brightness advances from0 to144 in that loop. The shadow stops at128; the
background continues through254 in the completion loop. Palette calls that
appear redundant remain, as do both eight-flash sequences, the counter wait,
CDG loading and the BGM stop/load/play order. Fade-in retains its separate
0..100 step4 sequence and page/load order.

The column helper deliberately uses the original bottom-coordinate bound
rather than BOX_H. It reads blue/red/green/extra words from page1, switches to
page0 and writes in reverse plane order, subtracting80 until carry. This can
reach beyond VRAM; the unchecked original behavior is preserved. The two box
animations keep their asymmetric starting coordinates and restore-column
arguments. Native byte equality supports these source observations; no physical
VRAM banking, interrupt timing or completed emulator polling loop is inferred.

The containing DATA31 string pool remains unaccepted. BSS is empty. Whole OP
source ownership and canonical packed-file unit credit remain open.

## Checks

```sh
PYTHONPATH=scripts .venv/bin/python -m lib.op_title_native
.venv/bin/python -m unittest tests.test_op_title_native tests.test_op_work_acceptance
.venv/bin/python scripts/publish_th03_op_work_scopes.py
```

Run with the workflow's one-CPU/nice10/empty-display environment. The focused
checks include equal corrupted target/candidate column images and swapped
intro relocation entries, so image equality and relocation membership alone
cannot establish native ownership.
