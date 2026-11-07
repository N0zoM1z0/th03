# Chiyuri BOSS: native-exact natural C++ for cardinal/fan angle and speed (after644)

The real complete Chiyuri BOSS object contains 11 functions, among them
the large `chiyuri_pattern_cardinal()` and `chiyuri_pattern_fans()`
volley controllers, and the full major BOSS update/render path.
Previously, many eight-bit bullet and rotation operations were
written as explicitly staged AL loads, arithmetic and stores.

This source recovery replaces those sequences with **ordinary natural
C++ field operations**, validated incrementally against the whole
original 2,654-CODE-byte object:

- The cardinal angle increases and reverses by eight via
  `chiyuri_cardinal_angle += 8` and `-= 8`,
  preserving both 8-bit wrap and original directional turn triggers
  (`af644b`, `af644c`).
- The next three right-angle cardinal shots now use direct
  `bullet_template.angle += 0x40`, with precisely the original
  cumulative angle progression (`af644a`).
- Four fan-loop speed updates (two growing and two decreasing)
  use `bullet_template.speed.v += 2` or `-= 2`, removing four
  explicit AL intermediary sequences (`af644d`, `af644e`).
- Both mirrored fan projectiles use the natural expression
  `bullet_template.angle = (0 - bullet_template.angle)`.
  The seemingly simpler unary expression
  `bullet_template.angle = -bullet_template.angle` changed the
  original bytecode (`af644f`). Explicit binary zero-minus
  preserves the original load-zero/subtract/store register
  encoding (`af644g`, `af644h`).

These are real C++ source expression recoveries across two large
pattern-generation functions, not just enum renamings. All compiler
experiments were run with true v2 OMF-COMENT-attested modified
source binding; failed candidates were rejected and their raw
objects/logs retained, not patched.

Final two fresh original Turbo C++ 4.02 compiler and complete
normal MAIN TLINK rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af644h --units ba_chiyu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af644h

Both native objects reproduce **all 2,654 original CODE bytes, 381
literal ordered FIXUPP fields, 11 PUBLIC offsets** and segment
definitions. Both ordinary full MAIN EXEs and path-normalized
MAPs equal the original source-native ancestor; all 1,553 literal
ordered MZ relocations, original loaded program and separately
serialized 130,882-byte Japanese MAIN.EXE match.

Preserved proof:
`.analysis/work/exatt-layout-af644h/report.json`,
SHA-256 `e8c79fedb83599e6824f100f06d0299a9c0fb7491071a3a7e17cbfcce4ab5f18`.
Only this affected major BOSS source was freshly compiled, not the
complete game, and no original object bytes or target binaries
were edited.

These were previously source-owned original bytes. Raw historic
vendor OMF packet identity, whole packed-game provenance, canonical
Factory credit and real PC-98 behavior remain separate claims.
