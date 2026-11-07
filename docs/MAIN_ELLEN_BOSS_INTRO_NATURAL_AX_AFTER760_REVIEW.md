# TH03 MAIN Ellen BOSS 4x8 intro sprites: AX shifts recovered in natural C++ after760

The original physical `ba_ellen` translation unit comprises nine public
BOSS functions, including radial Extra Attack patterns, the full update
and collision controller, the rotating strip renderer and the large
**4-by-8-sprite entrance renderer**. In the latter nested 32-sprite loop,
the previous maintained source explicitly loaded `_AX = top`, shifted
`static_cast<int16_t>(_AX) >>= 4`, wrote back `top = _AX` and passed
`_AX` to the sprite function. That hand-coded register dependency is
now genuinely **removed** and represented by native exact typed C++:

    top = static_cast<screen_y_t>(top >> 4);
    sprite16_put(left, top, sprite_offset);

All 32 sprite positions remain computed in their original order, with
unchanged sin/cos polar calls, signed shift, original register-local `i`
and sprite palette and clip side effects. It was actually compiled against
the original complete physical object; this is not cosmetic rewriting of
an isolated function or injection of the original instruction bytes.

Separate native original Turbo C++ 4.02 compiler experiments:

- `af760a`: the natural local shift/assignment in the complete Ellen BOSS
  compiled and full-linked twice with original CODE and all OMF fields.
- `af760b`: inlined the shifted `top` expression directly into
  `sprite16_put(...)`. Real original CODE changed, proving that the
  intermediate stack-local lifetime is codegen-visible. Rejected.
- `af760c`: restored the successful natural local assignment, added
  the source explanation and independently recompiled the **final current
  maintained product**. Both actual native TC4/TLINK rounds passed:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af760c --units ba_ellen
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af760c

Both rounds exactly reproduce **all 1,675 original CODE bytes, all 213
literal ordered original OMF FIXUPPs, all 9 PUBLICs**, original full
segment/group/source-dependency contracts and complete normal MAIN
EXE/MAP. Japanese 124,642-byte loaded program and 1,553 ordered MZ
relocations match; independent standard MZ serializer reproduces the
complete original 130,882-byte Japanese MAIN.EXE. 98 other original
project objects and CRT reused, no full cold replay.

Live source proof `.analysis/work/exatt-layout-af760c/report.json`, SHA-256
`1777a926ce68d7b3a276fc02845633a16479af34e68917a1959e69abe05d2a1a`.
Native rejected writer stage `af760b` is retained separately. This is
natural source recovery for already owned original bytes, **not** extra
canonical Factory packed-file acceptance or vendor raw OMF identity.
