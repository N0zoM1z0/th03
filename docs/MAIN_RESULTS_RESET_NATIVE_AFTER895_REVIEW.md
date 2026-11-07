# TH03 MAIN after895 — real round reset leaf and native 32-bit score amortization

The complete original physical `results` source consists of maintained
`src/main/round/results.cpp`, its `objects_reset.inl` and the large
`results.inl` scoreboard. All three real source files and their OMF
compiler dependency records belong to the **same original 1,060-CODE-byte
physical owner**, not three fake per-function replacements.

The small but important original `round_objects_and_counters_reset()` now
uses two **ordinary typed `while` loops** to clear every original shot
pair and every physical Enemy/Fireball combined EFE slot, in that order.
Both signed indexes and near pointers advance *after* the corresponding
original slot mutations. All original round timers and reset flags remain
original 16-bit/byte storage with their original values.

The complete five-category **round result/score HUD renderer** still
uses its original signed 32-bit bonus accounting, once-per-eight-frame
sampling, 192-frame amortization, decimal high/low splitting, score-add
order and original `65535UL` clamp. Its last 32-bit bonus comparison can
be written naturally as `result_bonus_remaining > (long)result_bonus_step`
in place of its reversed operand order without changing any original
TC4 4.02 machine instructions. The actual codegen rejects an otherwise
mathematically equivalent rewrite of the original unsigned-long cap.

## Actual independent original compiler experiments

- `af895a`: both complete EFE/shot-pair `for` reset traversals changed
  to natural `while`, the full original `results` object and normal
  MAIN exact in two independent genuine compiler/linker rounds.
- `af895b`: changed the **32-bit signed value compared against unsigned
  long 65535UL** from `value >65535UL` to `value >=65536UL`. The real
  original TC4 emitted different CODE at segment 4 offset 610 (despite
  retaining 1,060 initialized CODE bytes). Reverted the target's strict
  `>` and original 32-bit comparison spelling.
- `af895c`: swapped the operands of the **signed 32-bit bonus remaining
  versus unsigned 16-bit step** comparison while preserving the explicit
  `(long)` cast. This genuinely compiled to exactly the original TC4
  CODE and normal MAIN in both independent rounds.
- Final `af895d`: current source with comments, both reset loops and
  natural signed 32-bit comparison passed two real original TC4 4.02
  compiler and complete normal MAIN TLINK rounds, all full-scope exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af895d --units results
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af895d
```

Both genuine original compiler/complete normal linker rounds reproduce
**all 1,060 CODE bytes, 89 literal ordered native OMF FIXUPP fields and
three PUBLIC offsets**, original source/includes/physical segment ABI,
complete normal MAIN EXE/MAP, **124,642 Japanese loaded program bytes
and all 1,553 ordered original MZ relocations**. Independently
verified standard DOS MZ serialization reproduces all **130,882 bytes
of the original Japanese MAIN.EXE**, not historical vendor header
serialization. **98 other original game objects and CRT reused**, no
full-project cold replay, patched original OBJ/target or fake padding.

Protected original current-source-bound compiler/link proof:
`.analysis/work/exatt-layout-af895d/report.json`, SHA-256
`29be5a3f8b9d6c0e9868ee28163fe89ce91e8e28c34fea0e573af0edfa9f713a`.
These were historically source-owned original bytes: the improvement
is native C++ control/ABI fidelity, **not new distinct CODE, raw vendor
packet identity or canonical Factory packed-file credit**.
