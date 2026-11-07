# Three major BOSS C++ producers share the physical 32-byte state (after625)

Kana, Kotohime and Yumemi previously carried three separately maintained
copies of the same 32-byte DGROUP boss-template view. These were identical
in physical offsets but left ABI/stride drift invisible across large
character-specific update, bullet-pattern and rendering translation units.

The maintained `src/main/boss/template_state.hpp` now declares one
`boss_template_state_t`: eight 16-bit words through the sprite offset,
eight per-frame byte fields, the 16-bit effect radius, a signed Rikako
spin byte and reserved character tail. In original 16-bit Turbo C++,
compile-time size and `offsetof` checks enforce **32 bytes** and the
+0E sprite, +11 mode, +18 effect and +1A spin offsets. The last byte
meanings are not assumed universal: they can be interpreted by characters
that actually use them. Data and BSS remain owned by the preexisting
original root, not by these source-only compiler producers.

Both the compiler driver and read-only receipt verifier now force this
secondary header into each per-round native include tree **when consumed**
and require the emitted OMF COMENT dependency to name that path. This
addresses the historical v1 false-positive include bug: merely copying
a header and recording its hash without proving actual compiler use
is insufficient. Unrelated earlier receipts do not acquire a false
dependency on the new header.

Scoped original Borland TC4.02 and TLINK, two independent rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af625b --units ba_kana,ba_koto,ba_yumem
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af625b

All **6,072 original CODE bytes, 879 literal ordered native FIXUPPs,
30 PUBLICs, full segment layouts**, both complete normal MAIN EXEs
and normalized MAPs, Japanese program image and 1,553 ordered
relocations are equal. The separate standard MZ serializer also gives
the complete original Japanese MAIN.EXE. No full cold replay was run.
The verified source-controlled native receipt is
`.analysis/work/exatt-layout-af625b/report.json`,
SHA-256 `adf048a6e3e5244f93979e138d4fb5db2f0b0fc8d56a53b36b60796e79117740`.

This is shared source/ABI reconstruction, not 6,072 new target bytes,
original historical vendor OMF packet identity, physical gameplay
evidence or canonical Factory packed-file acceptance.
