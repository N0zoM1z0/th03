# TH03 MAIN Marisa: exact native full BOSS attack cadence and split-frame shift — after745

The full original `ba_maris` physical C++ owner contains **nine complete
PUBLIC functions** and 1,431 original initialized CODE bytes: BOSS template
initialization, spread/bullet rings, both vertical Extra Attack column
controllers, the whole update/hitbox/collision dispatcher, and normal,
split and entrance render paths. No function was validated in isolation.

The two original power-of-two **unsigned 16-bit attack periods** now have
natural C++ bit masks: `boss_frame & (MARISA_SPREAD_PERIOD-1)` for the
four-frame spread pattern, and `!(boss_frame & (MARISA_RING_PERIOD-1))`
for the 32-frame ring generator. The main renderer's four-frame sprite
flicker uses a named two-frame half-period and bit mask; the hit sprite
uses natural `if(boss_hit)`. The original intro frame gate, explosion and
intro dispatcher cases use actual named original BOSS enum values.
The signed 16-bit split-sprite entrance offset also now computes the
exact original `boss_frame << 1` in natural C++, preserving the two
sprite masks and the previously recovered automatic SI/DI allocation
from local declaration order. RNG draw order, the different wide/narrow
column termination frames, hardware sprite mask interrupts, byte-sized
mutable angle and actual BOSS hitbox calls remain unchanged.

Separate genuine Turbo C++ 4.02 codegen experiments (not assumptions):

- `af745a` accepted the entire current major BOSS with natural period
  masks and source-mode checks, with complete original CODE/OMF/linker
  results in two rounds.
- `af745b` attempted to turn the low-speed paired spray's original
  `marisa_bullet_speed / 2` into `>> 1`. That *failed* CODE comparison,
  despite equivalent unsigned byte arithmetic; the original division
  and distinct pair-of-bullets state machine were restored.
- `af745c` separately changed the entrance two-way sprite offset
  `boss_frame * 2` into `boss_frame << 1` and passed both complete original
  compiler/linker rounds. `af745d` retained this and formatted the
  renderer's four-frame mask while independently recompiling the final
  current maintained source in two further original TC4/TLINK rounds.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af745d --units ba_maris
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af745d

Both final rounds match **all 1,431 original CODE bytes, all 199 literal
ordered original OMF fixup fields, all 9 PUBLIC offsets**, segment
metadata, and native current-source input/OMF COMENT dependencies. Both
full original normal MAIN EXE/MAP links reproduce the Japanese
124,642-byte loaded image and all 1,553 ordered relocations; independent
standard MZ serialization reproduces the entire original 130,882-byte
Japanese MAIN.EXE. The other 98 project objects and original CRT were
reused, not cold-replayed. Failed `af745b` native writer outputs remain
protected as a real negative control, not accepted source exactness.

Final current-source receipt:
`.analysis/work/exatt-layout-af745d/report.json`, SHA-256
`6390f2e290dad794b54f9676c2ca0a577c5557411234d933a825ff8df8b395ec`.
This is substantial maintainable natural C++ and current original codegen
progress for *existing* original code owners; it adds no canonical Factory
packed-game accepted bytes, historical vendor raw OMF packet identity,
or completed original whole-product source ownership.
