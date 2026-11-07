# TH03 MAIN full player state/controller: nested live-source native proof (after725)

`core` is one **original physical Turbo C++ translation unit**, not a
collection of tiny independent objects. It contains player movement,
Hyper for all nine characters, the **substantial 230-line `player_state_update()`
state machine**, rendering, overlay, knockback, bomb orchestration, hit test,
damage, and shot preparation. Its original complete physical CODE has **3,135
bytes, 260 literal ordered FIXUPP fields, 21 PUBLICs**.

## Closing the previously unproved nested input provenance

The previous scoped original-TC4 compiler only forced the current
`hyper.inl` through `core.cpp`; other unchanged-looking nested original
implementation sources could silently come from the older `TH03WORK/src`
checkout. The scoped compiler and independent reviewer now bind *all five*
root `core.cpp` inlined implementation files:
`move.inl`, `hyper.inl`, `state.inl`, `stuff.inl`, `shot_sprites.inl`.
In addition, they bind the five nested physical implementations included
from `state.inl`: `update.inl`, `render.inl`, `overlay.inl`, `knock.inl`,
`bomb.inl`. The staged `state.inl` has its **five original include strings
rewritten to fresh stage-local source snapshots**, not just copied as-is.
All ten implementations receive live source SHA identities, round-specific
source snapshots, and **mandatory actual compiler-emitted OMF COMENT
dependency checks**; read-only review rechecks nested include rewriting,
source identity, complete objects and full linker output.

The unchanged-source `af725a` control passed both original native rounds,
proving that forcing the nested sources still reproduces original CODE,
FIXUPPs and complete original TLINK MAIN/MAP.

## Large player update and small helper C++ recovered together

The long player controller's CPU target selectors and shot cadences now have
explicit **byte-sentinel and timer** names: formation 0, boss target 254,
no formation 255, and firing periods 6/7/32/10. Its charge and spell
branches keep distinct 0x180 warning, 0x400 charge shot, 0x800 portrait,
0xC00 gauge bullet and 10,240-point boss bonus constants; all unchanged
control-flow labels and RNG order remain intact. The `0xFF` no-launched-boss
sentinel has a separate name from the CPU no-formation marker despite sharing
its byte value. Natural boolean tests replace selected zero comparisons,
and the per-frame CPU counter now naturally uses `++player->cpu_frame`.
Original storage widths, shot-release counter, move-lock/knockback priority,
CPU targeting and the later collision-render state remain unchanged.

The changed-source `af725b` passed native byte equality. An additional
`af725c` tried replacing the hit damage write with natural compound
`player->halfhearts -= players_hit_damage_update(*player)`, alongside
prefix/Boolean changes. CODE **shrunk by 5 bytes** and the complete original
CODE equality failed; this experiment is a **retained negative control**.
The compound assignment was removed (its original read/call/store ordering
is kept). The final `af725d` source retained prefix CPU increment, natural
zero check and distinct boss sentinel; both native rounds passed again.

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af725d --units core
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af725d

Each genuine original Turbo C++ 4.02 and full normal MAIN TLINK round matched
all **3,135 original CODE bytes, 260 ordered OMF FIXUPP fields, 21 PUBLICs**,
all original segments and BSS, full normal MAIN/MAP, the **124,642-byte
original Japanese loaded image and all 1,553 ordered MZ relocations**.
Separate standard MZ serialization reproduces the original **130,882-byte
Japanese MAIN.EXE** in both rounds. The other 98 original project objects
and CRT were reused unchanged; no full cold replay was run.

Current-source receipt `.analysis/work/exatt-layout-af725d/report.json`
SHA-256 `1295b470eb8d8697ca25843638487c377a48aa330bd58abfafbd7cebd6c5de87`.
The stages and their actual compiler/OBJ/EXE/MAP/writer outputs are retained,
including the negative `af725c`. This is **original-source fidelity and
current deep source-binding progress**, not new canonical packed-file Factory
credit, historical vendor packet equality, or all-99-TU completion.
