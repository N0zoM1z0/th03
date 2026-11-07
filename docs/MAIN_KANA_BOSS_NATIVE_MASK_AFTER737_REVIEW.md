# TH03 MAIN Kana complete BOSS attack / intro renderer after737

The maintained complete `ba_kana` physical original Turbo C++ 4.02 source
includes all Kana attack families (accelerating ring, 16-pellet staged ring,
random cloud ring and rotating ring), the full BOSS update/collision
controller and the main and sixteen-sprite intro renderers. This pass
was not restricted to a small isolated leaf.

The BOSS dispatcher has a named original 0x64 intro gate. The rotating
ring's unsigned 16-bit four-frame cadence is expressed as a natural
`!(boss_frame & (KANA_ROTATING_RING_PERIOD - 1))` test. The staged
ring's 16 pellets, intro renderer's 16 sprite operations and the intro
blink boundary are named original constants, not arbitrary magic numbers.
The renderer's four-frame cell choice now uses the natural unsigned
`(boss_frame >> KANA_RENDER_ANIMATION_SHIFT) & 3` computation, while
preserving the **original two successive sprite-offset multiplications**:
flattening those strides was an earlier original-codegen negative result.
The native sprite highlight thresholds (8, 16 and 24) and original
`KANA_MODE_INTRO` / `KANA_MODE_EXPLODE` dispatch are named explicitly.
The original angle RNG, unsigned-byte mutation, effect generation and
sprite composition order are unaltered.

Native experiments were **actually run**, not inferred from documentation.
`af737a` first passed the full source with natural `% 4` to bitmask, named
phase gates and render checks; `af737c` additionally proved a direct
unsigned right-shift frame quotient in the substantial intro renderer.
`af737b` tried eliminating the manual `asm { sub al, 10h }` by writing
`angle = static_cast<signed char>(randring_far_next16_and(0x1F) - 0x10)`;
real TC4 changed the initialized original CODE. This candidate was
**rejected and restored**: native encoding of the original AL subtraction
and the RNG side effect are preserved. The final current maintained
source is exactly the passing `af737c` source snapshot.

Genuine native original compiler, full normal MAIN TLINK and independent
read-only proof for the complete original `ba_kana` object:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af737c --units ba_kana
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af737c

Both rounds reproduce the entire original Kana CODE, all ordered native
OMF literal fixups, all original PUBLIC locations and segment declarations.
The whole normal MAIN EXE/MAP matches, including the original Japanese
124,642-byte loaded program and all 1,553 ordered MZ relocation entries.
Independent standard MZ serialization reproduces the original 130,882-byte
Japanese MAIN.EXE. The other 98 project objects and CRT are unchanged;
this was **not a full cold replay**.

Evidence: `.analysis/work/exatt-layout-af737c/report.json` SHA-256
`e60dd3a247a7da9c6edcf6492893f68f6572db0b25347018f09fd7b65324434f`.
The original native source, writer logs, compiler objects and full linker
products remain protected. Existing original byte ownership is not counted
again as new canonical Factory packed-game credit, and no historical
vendor-OMF packet identity or all-source completion is claimed.
