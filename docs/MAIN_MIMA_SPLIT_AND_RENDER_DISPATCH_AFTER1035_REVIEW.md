# TH03 MAIN Mima split and top-level render dispatch

The 223-byte Pascal `mima_render_split()` and 101-byte far
`gba_boss_render_mima()` now use two more natural source forms while retaining
the original TC4 output.

The split renderer advances the byte-valued opposite-half angle with compound
assignment:

```cpp
angle += MIMA_RENDER_SPLIT_OPPOSITE_ANGLE;
```

This still advances the angle only after the first masked sprite draw and
before the second pair of `polar()` lookups. The `register int split_distance`
local remains before `register screen_x_t left`; it keeps the Pascal distance
in SI and the first polar X result in DI. The top coordinate remains an
ordinary `screen_y_t` local.

The complete far render controller now expresses the launched-player path as
a positive scope:

```cpp
if(pid_current == gba_boss_launched_by) {
    pid_other = (1 - pid_current);
    sprite16_clip_set_for_pid(pid_other);

    if(MIMA_MODE_INTRO == boss_mode) {
        mima_render_split(...);
        return;
    }
    if(MIMA_MODE_EXPLODE != boss_mode) {
        mima_render_main();
        return;
    }
    boss_explosion_render();
}
```

Both mode comparisons are constant-first. INTRO still uses the split renderer
and returns; ordinary modes still use `mima_render_main()` and return; EXPLODE
still reaches the explosion renderer. The launched-player guard encloses the
complete active render path.

Compiler experiments against the complete `ba_mima` owner:

- `af1034x`: `angle = angle + ...` to `angle += ...`; exact.
- `af1034y`: positive launched-player scope around the far render controller;
  exact.
- `af1035a`: constant-first EXPLODE comparison; exact.
- `af1035b`: constant-first INTRO comparison; exact.
- `af1034w`: initializing `pid_other` in its declaration in the split leaf
  changed complete CODE; retain the separate assignment.
- `af1034z`: replacing the ordinary-mode negative test/return with a positive
  EXPLODE `if/else` changed complete CODE; retain the negative ordinary-mode
  guard and early return.
- `af1035c`: making the split renderer's `top` local a register changed
  complete CODE; retain the ordinary local.

Stage `af1035d` rebuilt the complete `ba_mima` physical owner in two
independent original TC4 4.02 rounds. All 1,922 CODE bytes, 277 ordered native
fields and nine PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1035d/report.json`

SHA-256: `daa5a3383fa33beac8938d9c6261a99da6b5f56a244ff5de314a9a480767f685`
