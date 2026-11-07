# TH03 MAIN Kana BOSS: signed sprite Y conversion without handwritten AX — after761

The original 16-bit `ba_kana` is a complete nine-function physical TC4
translation unit (1,874 original CODE bytes, 274 literal ordered OMF
FIXUPP fields and 9 PUBLICs), not one introductory sprite function.
It owns Kana's accelerated/staged/cloud/rotating attacks, whole BOSS
collision/update and normal/entrance render paths. This pass recovers
**natural typed C++** in the sixteen-sprite ring entrance renderer.

The previous original-source implementation manually copied the polar
Y coordinate to `_AX`, performed a signed 16-bit `static_cast<int16_t>(_AX)
>>= 4`, wrote the register back to `top` and used `_AX` as the sprite
Y argument. The equivalent original native code is generated from:

    top = static_cast<screen_y_t>(top >> 4);
    sprite16_put(left, top, sprite_offset);

The complete source retains the original 16-bit radius and angle, fixed
16-sprite loop bound, sprite sheet and color-mask effects, natural signed
shift, register/stack local lifetime and the original RNG/hit state order.
This is genuinely eliminating a manually operated CPU register, not
renaming an already compiled constant.

Actual separate original TC4 compiler experiments:

- `af761a` compiled the new typed C++ local expression in the **complete
  physical BOSS** and matched original native CODE and full MAIN linking
  in both rounds.
- `af761b` tested an apparently simpler compound `top >>= 4`. It
  changed original TC4 CODE and was rejected. The shorter form is not
  accepted on the basis of semantics alone.
- `af761c` restored the exact typed assignment, documented this genuine
  compiler distinction and separately recompiled the **final current
  maintained source** in both original TC4/TLINK rounds.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af761c --units ba_kana
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af761c

Both original 16-bit compiler rounds reproduce all **1,874 CODE bytes,
274 original ordered OMF FIXUPP fields, 9 PUBLIC offsets**, original
segment and source dependency records, complete full normal MAIN EXE
and normalized MAP, Japanese 124,642-byte loaded program and all 1,553
MZ relocation words. Independent standard DOS MZ serialization matches
the original 130,882-byte Japanese MAIN.EXE. Other 98 project objects
and original CRT reused unchanged; no full cold replay.

Current-source proof: `.analysis/work/exatt-layout-af761c/report.json`
SHA-256 `4f8ec61382ac3c05ccf68106b3dccfbf4a01eb8e0893c79c129d7c422b132841`.
The rejected native trial and complete writer output remain preserved.
This is new natural-source fidelity of previously owned bytes, not
additional canonical Factory packed-game acceptance or historical raw
vendor-OMF packet identity.
