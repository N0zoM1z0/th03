# TH03 MAIN Kotohime BOSS: named template, attack states and level scaling

The complete eleven-function ba_koto owner now expresses its template,
render-state protocol, attack-completion transitions and all seven
round-start level parameters with named C++ values.

The template leaf names Kotohime's initial center, horizontal velocity, HP,
sprite bank and player-two bank offset. The large random-ring, aimed-ring,
pellet-arc and nested radial-burst controllers now share explicit
NORMAL/EXPANDING/WARNING render states and the named SELECT scheduler
transition. All four attack sound calls share the original attack SFX ID.

The full update's seven formulas now name their half-level/orbit divisors
and independent base values: random-ring speed, orbit count, slow/fast
aimed speeds, pellet speed, pellet interval and radial burst count. Their
integer division, assignment widths and original round-start-only update
boundary are unchanged. The main renderer's hit byte is explicitly tested
as nonzero.

The two nested signed-16-bit radial loops, division-before-byte-angle
truncation, RNG-gated ring emitter, byte postfix event/frame counters,
AL-mediated signed phase changes and near-Pascal render helper remain in
their original order.

## Re-tested compiler alternative

An isolated attempt to replace the random-ring AL load/add/store with
boss_move_phase += 2 (af965c) failed the full object comparison:
the candidate became 1,838 CODE bytes and 261 ordered FIXUPPs, versus
the original 1,840 CODE bytes and 262 FIXUPPs. A local-byte temporary
variant (af965f) also failed the complete CODE comparison. The current
source retains the original AL-mediated phase sequence; no source or OBJ
patch was used to force equality.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af965e --units ba_koto
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af965e

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire 1,840-byte original Kotohime BOSS and linked each through the
complete normal MAIN response. Both reproduce all 262 literal ordered
OMF FIXUPP fields and eleven PUBLIC offsets, the full original Japanese
MAIN loaded image (124,642 bytes) and all 1,553 ordered MZ relocations.
The other 98 original game objects and original Borland CRT were reused;
no full cold replay.

Protected source-current report:
.analysis/work/exatt-layout-af965e/report.json, SHA-256
abbd5dbaeb972d3004e973dbce9f3a7cfdd0d0383cc0c70f665ad5a74675ee2c.
