# Kotohime Extra Attack: original event-counter and projectile ownership (after640)

Kotohime's complete Extra Attack source contains eight original functions:
projectile creation, explicit special attack creation, the render path,
collision/explosion effect, two bullet generators, the long ten-slot update
state machine and batch rendering.

A key recovered state meaning is that after the projectile reaches its
Y destination, the historical `angle` byte ceases to be a geometric
angle in the update code. It is incremented once per update and used as
an **event counter** with explosion/bullet pulses at 4, 8, 12 and 16.
On the final pulse the state becomes free. This physical reuse of one
byte is intentional and not a new struct field.

The maintained source now names those four pulse values and the real
slot-count policy: eight ordinary slots plus two explicit attack slots,
ten per-player update/render slots, four-shot and ten-shot generation,
and the arrival state boundary. The fixed constants remain compiler-time
C++ enums, not new DATA, runtime tables or extra state.

A candidate replacing the four-shot direction selection with a natural
signed ternary **changed native CODE** (`af640a`); the original
conditional assignment was restored and passed the source-rooted
negative/positive control `af640b`. The accepted event-counter
and slot policy is `af640c`, compiled from the actual modified
C++ source with original Turbo C++ 4.02 in two independent rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af640c --units ex_koto
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af640c

The Borland OMF COMENT dependency records bind the staged current source
and the byte-packed shared Extra Attack header, rather than an old
TH03WORK copy. Both rounds reproduce **all 1,054 original CODE bytes,
100 literal ordered native fixup fields, eight PUBLIC offsets**,
all original segment definitions, complete normal MAIN EXEs and
path-normalized MAPs. The original Japanese program image, all
1,553 ordered MZ relocations and separately serialized exact
130,882-byte original Japanese MAIN.EXE match.

The preserved proof is
`.analysis/work/exatt-layout-af640c/report.json`,
SHA-256 `162d22d74cf59a3c5e866ad8d78c9104057ca7f9c61885721ce86551291c8765`.
Both real compiler/linker rounds and source overlays are retained.
This validates existing source-owned bytes and clarifies gameplay
semantics; it is not new packed-file Factory credit, historical
vendor raw OMF packet-byte identity, or device runtime proof.
