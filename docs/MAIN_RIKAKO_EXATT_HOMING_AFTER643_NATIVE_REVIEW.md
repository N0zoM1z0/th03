# Rikako Extra Attack: 14-slot homing window and native typed parity (after643)

Rikako's complete original 702-CODE-byte Extra Attack producer contains
the normal eight-slot spawner, the fourteen-slot explicit BOSS
attacker, the individual renderer, the long projectile homing,
collision and flight-state update, and batch rendering.

The true per-character state byte +0x17, already checked in the
shared 32-byte entity ABI, is named `homing_disabled`. A projectile
only re-aims when this byte is zero and its frame is within the
**inclusive 0x40..0x50 window**. The current source names that window,
the eight ordinary and fourteen total physical slots, the flying
state and the 0x1C emergence limit. The explicit BOSS spawner sets
frame 0x40 and disables homing; the ordinary spawner obtains a
one-bit RNG flag. No byte or runtime counter was added.

A new natural C++ rewrite identifies *unsigned* renderer frame parity:

    if((static_cast<unsigned int>(frame) % 2) != 0) { ... }

The unchecked `frame % 2` source variant (`af643a`) changed the
original Turbo C++ output despite numerical equivalence for this
unsigned byte. The explicit unsigned-width version `af643b`
compiled exact original CODE in two rounds.

An important **negative ABI/codegen control** is retained:
`angle_delta` is a signed 8-bit result of an angle subtraction
followed by `angle_delta /= 8` before adding to the projectile
angle. Replacing the divisor with an equal-valued C++ enum changes
TC4's actual signed 16-bit division instructions (`af643c`).
Restoring that exact literal (`af643d`) makes the full object
exact again. This limit is recorded beside the signed-divide
expression; no unverified arithmetic shortcut is asserted.

Final v2 source/OMF-dependency-attested dual native Turbo C++ 4.02
compiler and full normal MAIN TLINK:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af643e --units ex_rika
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af643e

All **702 original CODE bytes, 46 literal ordered FIXUPP fields,
five PUBLIC offsets**, original segments, both normal linked MAIN
EXEs and normalized MAPs match. The loaded Japanese program,
all 1,553 ordered MZ relocations and separately serialized
130,882-byte Japanese MAIN.EXE are original-equal. Native compiler
OMF COMENT records identify the actual staged maintained source
and shared packed entity header, not the old TH03WORK snapshot.

Retained report:
`.analysis/work/exatt-layout-af643e/report.json`,
SHA-256 `5bcbba531b07b6f0a457804fa7b597b2f80e5117c33ece029e4501915a68d124`.
The original target bytes, per-round writer logs, outputs and
negative evidence remain available without full cold replay.

This advances original source readability and typed 16-bit codegen,
not newly accepted canonical packed-game bytes, original historic
vendor OMF packet equality or physical PC-98 behavior proof.
