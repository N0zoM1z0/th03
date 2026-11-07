# TH03 MAIN Kotohime BOSS ring renderer: native C++ without explicit AX — after762

This pass operates on the **entire original 11-function physical `ba_koto`
Turbo C++ object**, which owns the complete Kotohime attack patterns,
full BOSS update/collision state machine, ring and intro renderers.
The original `kotohime_render_ring(int count)` used a manual load of
`_AX = top`, `static_cast<int16_t>(_AX) >>= 4`, a redundant assignment
back to `top`, and `sprite16_put(left, _AX, sprite_offset)` in each loop.
These register manipulations are now replaced with original-codegen
exact, natural typed C++:

    top = static_cast<screen_y_t>(top >> 4);
    sprite16_put(left, top, sprite_offset);

This retains the original 16-bit signed polar Y shift, C++ local lifetime,
visible 16/8-sprite loop counts, BOSS sprite masks and the original
integer angle division (`(i * 256) / count`). No new helper, synthetic
CODE or unsupported 16-bit pointer coercion was introduced.

Native TC4 compiler exploration:

- `af762a` compiled and full-linked this naturally written BOSS
  renderer in two real original TC4 4.02 rounds, matching the complete
  original CODE, all native ordered fixups, PUBLICs and MAIN image.
- `af762b` challenged the shorter `top >>= 4` syntax. That source
  changes original TC4 machine instructions, and was rejected.
- `af762c` independently rebuilt the final current source with the
  explanatory codegen comment and the accepted explicit typed assignment.
  Again **both rounds** passed the whole original physical object and link.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af762c --units ba_koto
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af762c

Both final rounds match all **1,840 original CODE bytes, 262 literal
ordered OMF FIXUPP fields, 11 PUBLIC offsets**, all segments and compiler
source COMENTs, full normal MAIN EXE/normalized MAP, original Japanese
124,642-byte loaded game and all 1,553 ordered MZ relocations. Independent
standard MZ serialization reproduces the complete 130,882-byte original
Japanese MAIN.EXE. The other 98 original project objects and CRT were
reused; no full cold replay or target/code patching.

Receipt `.analysis/work/exatt-layout-af762c/report.json`, SHA-256
`849a70271c81be2198fd5dbfccd9201a251670ece983f00aa54b777d753ebd44`.
The failed `af762b` source/materialized object is retained as a negative
control. Original CODE remains already owned; this is genuine natural
C++ recovery, not extra canonical Factory accepted packed-game bytes or
historical raw vendor OMF packet identity.
