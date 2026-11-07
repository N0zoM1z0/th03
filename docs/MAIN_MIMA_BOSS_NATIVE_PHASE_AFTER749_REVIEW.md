# TH03 MAIN Mima complete BOSS: original-native phase and intro codegen — after749

This is a new actual source experiment against the complete original
`ba_mima` physical 16-bit Turbo C++ module. Its nine PUBLIC functions
include the major spread/random-bomb/trail/orbit attack families, BOSS
startup/collision update, hit-state sprite rendering and the unusual
masked split-sprite entrance renderer. No function was tested in isolation.

## Source changes that match original native code

The large state controller now uses named original per-pattern gates:
`0x10` warning, `0x20` launch start, `0x80` random attack end,
`0x82` spread end, `0x96` trail end, and `0x64` intro end.
The original **unsigned 16-bit** even-frame spread, random-bomb and
orbit attack checks use `!(boss_frame & 1)`; the four-frame random-bomb
shot period uses `!(boss_frame & 3)`. The *six-frame* pellet subattack
still uses actual signed/unsigned integer modulo 6, not an invalid mask.
Main sprite hit-state is a natural `if(boss_hit)` and BOSS render routing
uses existing `MIMA_MODE_INTRO`/`MIMA_MODE_EXPLODE` enum states.
The substantial split-sprite renderer also uses the natural original
`boss_frame << 1` intro offset while preserving its two-phase sprite
interrupt masks, original polar radius local and automatic SI/DI register
assignment. The original original RNG order, byte-mutating angles and
fall/intro paths have not been flattened or changed.

## Native experiments, not inherited assumptions

- `af749a`: compiled the full current source with named BOSS gates,
  Boolean hit/mode tests and natural even/four-frame masks; both original
  compiler/linker rounds were exact.
- `af749b`: separately changed split intro offset from `boss_frame * 2`
  to `boss_frame << 1`; both native rounds retained exact original CODE.
- `af749c`: attempted to reuse the local `pid_other` in the update
  controller rather than recalculating `1 - pid_current` after
  `boss_target_update()`. This *changed* TC4 machine instructions, so the
  historical duplicate calculation remains. Failed writer outputs were
  retained without treating them as successful proof.
- `af749d`: final maintained source, including the revalidated local
  expression/negative-control comment, passed both original TC4 4.02
  compile and full normal MAIN link rounds again.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af749d --units ba_mima
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af749d

All **1,922 original CODE bytes, 277 literal ordered OMF FIXUPP fields,
9 PUBLIC offsets, segment definitions and native source COMENT paths**
match. The full normal MAIN executable and MAP, the original Japanese
**124,642-byte loaded program** and all **1,553 ordered MZ relocations**
remain identical. Independent standard MZ serialization reproduces all
**130,882 original Japanese MAIN.EXE file bytes** in each round.
Only `ba_mima` was recompiled; the other 98 project objects and original
CRT were reused unchanged. No full cold replay or binary patching.

Current-source proof `.analysis/work/exatt-layout-af749d/report.json`,
SHA-256 `62a3fb482ec61b17598a2ea42264c160fd1ce0371dce8efd376a531fded49b4b`.
Retained writer evidence includes source/header snapshots, original OMF
and exact literal fixup checks, two real compiler/linker results and both
full Japanese MZ outputs. The code is already original-owned; this is
improved natural source fidelity, **not** new Factory canonical packed-file
accepted bytes, historical vendor raw OMF identity or 99-unit ownership.
