# TH03 MAIN Reimu BOSS: named cloud-angle and player-sprite semantics

The complete nine-function original `ba_reimu` BOSS remains ordinary
maintained C++ and now gives its cloud-orbit byte arithmetic more precise
names. `REIMU_CLOUD_INITIAL_SPEED` identifies the initial 16-byte speed;
`REIMU_CLOUD_OPPOSITE_ANGLE` identifies the half-turn added for the second
cloud projectile; and the signed `REIMU_CLOUD_ANGLE_ROTATION` names the
separate -0x40 center-orbit adjustment. These are distinct operations and
remain in their original order: projectile emission, second angle update,
acceleration, then center-Y motion. The small template-init leaf also names
the 0x28 sprite offset applied only to the second player.

## Original compiler verification

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/probe_th03_main_exatt_layout.py --stage af944a --units ba_reimu
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af944a
```

Both independent genuine original Turbo C++ 4.02 rounds recompiled the
**entire 2,020-byte** original BOSS object and ran the complete normal MAIN
link. All **270 literal ordered OMF FIXUPP fields and nine PUBLIC offsets**
match; both complete Japanese MAIN EXE/MAP outputs reproduce all **124,642
loaded program bytes and 1,553 ordered MZ relocations**. The other **98
original game objects and CRT were reused**; no cold replay. The final
current-source report is `.analysis/work/exatt-layout-af944a/report.json`,
SHA-256 `2691ea3727c53fc41646c5d7c9408324d2e874c8f2a38aae79efa946f9cf99c6`.

The earlier `af943a` cloud-only pass is superseded as a source-current
receipt by `af944a`, which also includes the named player-two sprite offset.
This BOSS had historical native source coverage already: the work improves
natural C++ semantics and current-source provenance, not distinct CODE-byte
ownership, vendor raw OMF packet identity or canonical Factory acceptance.
