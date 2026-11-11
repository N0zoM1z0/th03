# MAIN shared BOSS core / explosion ring source recovery (after623)

TH03's nine major BOSSes call a shared native helper producer, reconstructed
from two **separate physical Turbo C++ TUs** consuming the maintained
`src/main/boss/shared.cpp`:

- `ba_sring.obj`: the entire 348-byte `boss_explosion_ring` render/hit
  completion function (22 literal native fields; one PUBLIC).
- `ba_srest.obj`: the complete 601-byte helper controller (84 fields,
  seven PUBLICs): `boss_move_sine`, `boss_fall`, `boss_update_start`,
  `boss_hittest_end`, `boss_target_update`, `boss_pattern_next`,
  and `boss_explosion_render`.

The original source partition macros and the actual original normal MAIN
link slots were reconstructed into the current scoped *v2* native driver.
Both source wrappers force `probe/<stage>/rN/src/main/boss/shared.cpp`
as the compiler-consumed path; emitted Borland OMF COMENT source-dependency
records are validated. The read-only reviewer also verifies the consumed
input, all original CODE, ordered fixups, PUBLICs, segments, writer logs,
full normal MAIN EXE and MAP, Japanese image and relocations.

The maintained game C++ now names shared physical limits that previously
appeared as anonymous literals across several large BOSS controllers:
the horizontal bounce interval (0x300–0xF00), 0x20 horizontal/descending
steps, the 0x1A00 despawn Y, the 0x50-frame pattern wait and the 5120-point
boss award. They are **compiler-time enum constants**, not extra state or
new DATA objects. The exact two-object source-controlled proof is:

    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af623c

Both genuine native TC4/TLINK rounds retain the entire 949 CODE bytes,
106 literal ordered fixup fields, eight PUBLIC offsets, every original
segment, complete normal MAIN EXE/MAP, 1,553 Japanese ordered MZ fixups
and the separately serialized full 130,882-byte original Japanese file.
Receipt:
`.analysis/work/exatt-layout-af623c/report.json`,
SHA-256 `8f2912343d9e5ea4dccc16520cf31751b91c5902777c0734b4a6124a637a2413`.

A substantive negative compiler experiment attempted to replace the large
`boss_update_start()` 32-byte state-copy sequence with natural
`boss_state = boss_character_template[pid_current]`. The real compiler
emitted a FAR struct-copy call (with source/destination stack pushes),
rather than the original inlined SI/DI/ES/CX and `REP MOVSW`; the first
control produced a 597-byte helper unit instead of 601. A second attempt
with a register `boss_state_t near*` and the indexed source also
changed machine code (even though its total length remained 601).
Both negative controls remain in `af623b` and `af623d`; the original
inlined register/REP MOVSW contract is preserved, not masked by padding
or byte arrays.

This is source readability and native compiler provenance work for
already owned CODE. No canonical packed-file Factory credit, historical
vendor packet identity or physical runtime compatibility is inferred.

## 2026-11-11: exact HP exit and active target-tracking predicates

The shared `boss_hittest_end()` leaf now expresses its two terminal exclusions
as one ordered short-circuit test: positive HP or the original exploding
mode. Both must skip the original reset, palette, award and boss-level
update. The `boss_target_update()` leaf uses a positive not-descending
condition around the two target-coordinate assignments; descending frames
still leave the previous target untouched. No register-copy or RNG path in
the larger shared controller was changed.

`af1351c` and `af1351d` each proved the 601-byte controller in two genuine
original TC4 rounds. The final source-bound `af1351g` compiled **both**
physical shared objects: **949 CODE bytes, 106 ordered native fields and
8 PUBLICs** reproduce the original, with two full normal MAIN links and
ordered relocations. The joint Mima/shared test `af1351f` additionally
passes at 2,871 CODE bytes without a full cold rebuild.

Current receipt: `.analysis/work/exatt-layout-af1351g/report.json`, SHA-256
`993df2c7b82bf6dfff107ca34acfde0058c03d300059421ed3c76e58f1e19891`.
