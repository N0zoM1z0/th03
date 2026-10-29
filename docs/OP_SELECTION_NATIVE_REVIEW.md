# OP character selection native source review

2026-10-28: the actual two-TU producer now has complete CODE ownership:
`selhelp.cpp`155 bytes plus `seltail.cpp`2858 bytes,19 procedures/3013 CODE.
All287 emitted native fields and91 literal ordered MZ relocations resolve
independently through both compiled MAP public tables and match the fixed
Japanese target and current candidate. No source/recipe/output was changed.

| Procedure | CS-relative offset | CODE | Native return cleanup |
| --- | --- | --- | --- |
| Score load/decode | 19F2 | 107 | Near Pascal2 |
| Available-character count | 1A5D | 48 | Near0 |
| CDG loads1/2/3 | 1A8D / 1AC3 / 1AEF | 54 / 44 / 53 | Near0 |
| Initialize/load | 1B24 | 179 | Near0 |
| Free | 1BD7 | 28 | Near0 |
| VS/story pictures | 1BF3 / 1C35 | 66 / 48 | Near0 |
| Stats / names / extras | 1C65 / 1D36 / 1D70 | 209 / 58 / 80 | Near0 |
| Curve | 1DC0 | 135 | Near Pascal10 |
| Update/render curves | 1E47 | 351 | Near0 |
| Cursor | 1FA6 | 98 | Near Pascal4 |
| Player input/update | 2008 | 384 | Near Pascal4 |
| 1P vs2P menu | 2188 | 407 | Near0 |
| VS CPU menu | 231F | 379 | Near0 |
| Story menu | 249A | 285 | Near0 |

## Physical source and ownership

The compiler dependency records consume `src/op/formats/score_load.inl` and
`probe/select155_helper.inl` in the155-byte TU. The second TU consumes
`probe/select155_tail.inl`. Those two probe-named files are literal complete-
function slices: concatenating them reproduces every byte of maintained
`src/op/menu/character_selection.inl`. No function text is synthesized. The
unchanged current cold graph also binds both wrappers and all consumed headers.

The107-byte loader was maintained source but was not previously in current OP
acceptance. It now has its own existing unit accepted alongside a new48-byte
unlock unit and2858-byte tail unit. The historical2906-byte aggregate candidate
is retained separately and does not add duplicate current credit.

The old unsplit `op_sel.obj` notes include relocation-order failures for curves
and the VS menu. They do not describe today's actual155/2858-byte producers.
The complete current native field streams are checked in emitted order, without
sorting the MZ vector or patching an object. The helper has15 fields/seven MZ
entries; the tail has272 fields/84 entries. Each function fully decodes through
its genuine near return with the listed argument cleanup.

## Original behavior preserved

- Unlock scans four rank files. Any load/recreate error returns the locked
  count, even after an earlier clear; otherwise any cleared rank unlocks all.
  Loader returns BOOL16, while available-character count is a BYTE result.
- Initial loading waits for counter30 but does not reset the counter afterward.
  Preserve its first-frame trail decrement and held-Shot behavior.
- Curve phases wrap to BYTE before signed16 multiplication/division by256.
  Preserve truncation toward zero, trail order and the small-curve discontinuity.
- Up/Down and Shot/Bomb are independent tests. Original signed BYTE movement,
  input locking, palette-collision changes and unchecked indexing are retained.
- The native input callback uses DWORD offset/segment storage and far indirect
  calls, despite the `func_t_near` typedef name. Five pointer assignments emit
  separate WORD halves; both halves and their five segment relocations are
  checked. Three cross-TU score calls and the unlock call use real near E8 fields.
- The three menus retain their different initialization, confirmation, fade and
  timing order. Their polling bodies are compared as native code; no physical
  timing or emulator-loop termination claim is needed for this source scope.

This CODE proof excludes tail DATA227/BSS23 and following linker alignment.
The separate [storage review](OP_SELECTION_STORAGE_REVIEW.md) now recovers the
maintained declaration prefix, accepts all227 initialized bytes and reviews the
natural23-byte BSS layout without file-backed credit. It removes the frozen
prefix's unproved dummy BYTE declarations using scoped compiler alignment and
proves two actual selected compile/link rounds against unchanged context.
The earlier score menu entry remains a different accepted owner.

## Checks

```sh
PYTHONPATH=scripts .venv/bin/python -m lib.op_select_native
.venv/bin/python scripts/publish_th03_op_work_scopes.py
```

Use the workflow's one-CPU/nice10/empty-display environment. The current native
cold pair is revalidated without rebuilding. Three focused tests cover the
actual two TUs, identical corrupted menu images and a changed curve relocation
order with identical membership. No runtime matrix was added.
