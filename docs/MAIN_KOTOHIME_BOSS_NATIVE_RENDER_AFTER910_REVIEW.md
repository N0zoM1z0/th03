# TH03 MAIN after910 — complete Kotohime BOSS native ring/render phase controls

The complete original eleven-function physical `ba_koto` Turbo C++ 4.02
source was recompiled: BOSS template, original random/aimed ring producer,
full nested radial barrage, five-position pellet arc, complete update/
hit scheduler, ring/main/intro renderers and full dispatch. The original
signed 16-bit divide-before-byte-angle truncation, RNG order and real
AL-mediated byte-phase update remain in the historical physical owner.

This session named physical collision (64×48 tiles, 32-pixel hit radius),
128×48 main sprite, 32×16 ring sprite, both placement margins and exact
0x502/0xA00 ring sprite offsets. Original `if(randomize_angle)` and
`if(boss_render_mode)` naturally read `if(value != 0)`. The original
unsigned-word pellet remainder-1 and flickering sprite remainder/threshold
comparisons are now naturally reversed operand order without any CODE
change. The full source retains natural loops in the ring producer,
original nested radial projectile burst, and sprite orbit renderer.

Genuine original compiler trials:

- `af910a`: reversed both modulo/remainder comparisons; complete physical
  original BOSS exact in two independent original compiler/linker rounds.
- `af910b`: named all original sprite, collision and ring geometry; exact.
- `af910c`: changed all three mutable byte `boss_render_frame++` into
  prefix. Original TC4 generated **1,852** CODE bytes rather than
  original **1,840**, first discrepancy CODE segment 4 offset 269;
  restored original postfix, without padding or fabricated machine code.
- `af910d`: natural explicit `!=0` on both signed-word random-selection
  and byte render-mode guards, full original CODE/normal MAIN exact.
- Final `af910e`: exact current maintained source with comments compiled
  in two real independent Turbo C++ 4.02 and full normal MAIN TLINK rounds.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af910e --units ba_koto
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af910e
```

Both original compiler/full normal linker rounds reproduce **all 1,840
CODE bytes, 262 literal ordered OMF FIXUPP fields and eleven PUBLIC
offsets**, source/segment/16-bit ABI, complete normal MAIN EXE/MAP,
**124,642 Japanese loaded program bytes and all 1,553 ordered MZ
relocations**. Independently checked standard DOS MZ serialization
reproduces the original 130,882-byte Japanese MAIN.EXE; this is not
proof of historical vendor MZ header byte serialization. **98 other
original game objects and original CRT reused**, no cold replay, target
patching or fake NOPs.

Protected source-bound native receipt:
`.analysis/work/exatt-layout-af910e/report.json` SHA-256
`c068dd6e0823929525e253b735857d15b515d8b9d2a31f8148f52dfedb185e0d`.
Historically source-covered original CODE, not new unique canonical
Factory game-byte credit, raw vendor packet-identical OMF or complete
historical source ownership.
