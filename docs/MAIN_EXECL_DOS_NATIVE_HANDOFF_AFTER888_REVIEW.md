# TH03 MAIN after888 — original large-memory-model DOS resource handoff leaf

The complete original physical `execl` Turbo C++ 4.02 object contains one
**79-CODE-byte** far-Pascal `main_exec(const char far *binary_fn)` routine
in the original HITCIRC_TEXT segment. It frees original PI graphics,
sprites, TRAM/gaiji and the **two distinct MRS archive slots**, calls
`game_exit()` and finally performs the large-memory-model DOS
`execl()` handoff. Its segmented far-pointer ABI and resource release
order must be preserved without inventing new runtime state.

The two original literal MRS archive indices 0 and 1 are now named as
`MAIN_EXEC_FIRST_MRS` and `MAIN_EXEC_SECOND_MRS`. These are compile-time
C++ enum values; they allocate no DATA and reproduce the original
**two individual** far-Pascal call sequences. The `execl` argument
casting deliberately retains the original 16-bit near filename view
and **four-byte `void far *` NULL vararg terminator**. This is not the
same call ABI as passing an ordinary two-byte integer zero.

## Genuine original Turbo C++ experiments

- `af888a`: named both original MRS archive indices without changing
  original instructions; both normal MAIN original TC4/TLINK rounds
  passed.
- `af888b`: replaced the two independent MRS calls by a natural
  `for(int slot=0; slot<=1; ++slot) mrs_free(slot)`. Although the
  resource calls were equivalent in intent, original TC4 generated
  **83 CODE bytes** instead of the target's **79**, with first difference
  at CODE segment 4 offset 3. Rejected; two calls retained.
- `af888c`: replaced the original far-NULL `execl` vararg with ordinary
  integer `0`. Real original TC4 emitted **78 CODE bytes** instead of
  **79**, first difference at CODE segment 4 offset 56: the argument
  *width* is actually different. Rejected and restored `void far *`.
- Final `af888d`: original exact MRS calls, far-null and cleanup order
  with named source constants, recompiled in two independent genuine
  original TC4/full normal MAIN TLINK rounds with byte equality.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af888d --units execl
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af888d
```

Both genuine original compiler/complete normal linker rounds reproduced
**all 79 original CODE bytes, 11 literal ordered OMF FIXUPP fields,
one PUBLIC offset**, original segment/source/large-memory ABI, entire
normal MAIN EXE/MAP, **124,642 Japanese loaded program bytes and all
1,553 original ordered MZ relocations**. Independently checked standard
DOS MZ serialization reproduced the **130,882-byte pinned Japanese
MAIN.EXE**, not evidence of historic vendor header serialization.
The other **98 original project objects and CRT were reused unchanged**;
no cold replay, inserted assembly, fake NOPs or object/target patches.

Protected actual source-bound original writer evidence:
`.analysis/work/exatt-layout-af888d/report.json`, SHA-256
`0db9c63c239d571f85032acf51362e31b20b553a4b6be151be22dc53ee89fe8c`.
This historically source-covered leaf now has clearer native C++
ABI reasoning; **no newly distinct original CODE, raw vendor OMF packet
identity or canonical Factory packed-file acceptance** is claimed.
