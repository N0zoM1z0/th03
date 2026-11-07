# TH03 MAIN after844: complete Fireball controller native C++ timebases

The `e_fireb` original physical source owns the full 576-line Fireball
module: red/blue projectile spawning and aim, transfer-to-fall physics,
16×16/32×32 sprite rendering, explosion stages, collision, chain charge
and update. Its two global and local clocks have **different C++ integer
widths**; this matters to the original Turbo C++ 4.02 machine code.

The **16-bit global** `round_or_result_frame` 512-tick targeting cycle
is now written as a natural unsigned `% FIREBALL_AIM_PERIOD`, preserving
the original two 256-frame halves for random-vs-player-guided aim and
all RNG draw order. The physically **byte-valued** `p.frame` 8-tick
sprite animation retains its original mask, and its sprite cel condition
retains its exact `<= (FRAMES_PER_CEL-1)` spelling; a blanket cleanup
would produce non-identical TC4 instructions. The exact explosion
sprite, hit, fade and expiry frames (12, 14, 32, 36) and the separate
fly/fall sprite half sizes now have explicit C++ semantic names.

## Genuine compiler experiments, not inferred equivalences

- `af844a`: the real whole `e_fireb` object with global `%512` passed
  two independent original TC4/normal TLINK rounds.
- `af844b`: replacing the **byte** sprite animation mask with `%8`
  changed the complete original CODE, even though the global modulo
  was native exact. The byte mask was restored.
- `af844c`: rewriting both sprite cel comparisons from `<= 3` to
  `< 4` also changed the original byte-level CODE/branch lowering;
  the original conditional form remains.
- `af844d`: named the distinct fireball explosion frames, hit/expiry
  stages and exact *byte-valued* frame division, preserving original
  16-bit widths and byte truncation. The full owner passed twice.
- `af844e`: combining the falling fireball's consecutive `next = x;
  next += vx;` operations into `next = x + vx` emitted different
  original instructions. The two original 16-bit update stages were
  restored, preserving the original transfer/fall sequencing.
- Final **`af844f`** recompiles the whole actual current maintained
  source (including proven half-size constants and compiler quirks)
  in two original TC4 and full normal TLINK rounds, all exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af844f --units e_fireb
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af844f
```

Both current-source-bound native rounds reproduced **all 1,555 original
CODE bytes, 115 literal ordered native OMF FIXUPP fields and ten
PUBLIC offsets**, original 1-byte DATA/BSS source storage, complete
normal MAIN EXE/MAP, the **124,642-byte original Japanese loaded
program** and **all 1,553 ordered original MZ relocations**. The
independently checked standard MZ serializer also reproduces all
130,882 original Japanese MAIN.EXE bytes. **98 other original project
objects and the original CRT were reused**, no full cold replay, fake
instruction padding, target substitution or OBJ patching.

Protected genuine source-bound proof with both independent compiler/TLINK
writer rounds: `.analysis/work/exatt-layout-af844f/report.json`, SHA-256
`76ef4bb8a67c0b83b1aa22ca04b42564a78f92b8743f1cdcd908cb206ef37a69`.
These were previously native-covered original CODE bytes. Fresh source
reconstruction/verification must **not** be double-counted as unique
original coverage or canonical packed-file Factory accepted credit.
Raw vendor OMF packet identity and true original historical source
text remain separate, unproved claims.
