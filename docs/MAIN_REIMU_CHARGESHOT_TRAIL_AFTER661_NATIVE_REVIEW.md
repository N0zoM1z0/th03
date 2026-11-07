# Reimu seven-sample charged shot: original native full producer after661

The new v2 source-rooted compiler overlay covers Reimu's complete
ten-function physical charged-shot producer `cs_reimu`: normal and
hyper shooting, long seven-position trail update, collision,
individual rendering and full Gauge attack. Its unchanged native
control was included in `af660a`.

The original physical charge entity is **32 bytes**: one-byte
state/frame, seven 16-bit X positions at +02, seven 16-bit Y
positions at +10, and an eight-bit angle at +1E followed by speed.
Original 16-bit Turbo C++ checks size and offsets with compile-time
assertions. Importantly, **update and render scan twelve entries
per player, but hit testing scans only six**. This asymmetry is
in the original game, not a missing bounds check to repair.
The six-slot hitbox count, first four ordinary launch slots,
twelve-slot hyper pool, backward seven-position trail shift,
and sixty-four-frame stop condition now have distinct named
compiler-time constants.

The hit-testing parity gate:
    reimu_chargeshot_alternate_hit_frame &&
        (round_or_result_frame & 1)

now uses a natural signedness-correct C++ remainder:
    static_cast<unsigned int>(round_or_result_frame) % 2

The genuine modified-source Turbo C++ 4.02 control `af661b`
compiles it into **identical original bytes**, with the same
short-circuit and early return.

A separate naturalization attempt of the sprite frame's signed
`phase &= 3` to `static_cast<unsigned int>(phase) % 4`
**changed the original native code** (`af661a`). The original
mask operation remains in the source; it is not safe to substitute
a superficially equivalent expression when exact x86 opcodes
matter.

Final fresh complete physical source/OMF-COMENT-verified native pair:
    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af661c --units cs_reimu
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af661c

Both independent original compiler/TLINK rounds reproduce the
entire **1,448 CODE bytes, 138 ordered native FIXUPP fields and
ten PUBLIC offsets**, all OMF segment data, the complete normal
MAIN EXE and path-normalized MAP. The original Japanese loaded
program and all 1,553 MZ relocations match, with independent MZ
serialization reproducing exactly the 130,882-byte Japanese
MAIN.EXE.

Retained actual compiler inputs and two original writer rounds:
`.analysis/work/exatt-layout-af661c/report.json`,
SHA-256 `104002de959215a586695eea7ba7552703e037c61473c5239d74bade3b0e466d`.
The other 98 original project objects and CRT libraries were reused,
not recompiled by a whole cold replay.

All these target CODE bytes were previously source-owned.
The result is original-native C++ and physical layout recovery,
not new canonical Factory packed-file byte acceptance, original
historic vendor OMF packet-byte identity or real PC-98 runtime.
