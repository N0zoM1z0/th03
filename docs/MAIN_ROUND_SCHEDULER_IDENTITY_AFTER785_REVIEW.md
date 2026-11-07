# TH03 MAIN whole entry / frame-scheduler playfield selection (after785)

The original source owner `entry` contains the main entry, a **200+-line
per-frame round scheduler**, stage setup and score/result finalization as
one genuine physical original Turbo C++ translation unit. Its native source
producer includes four real `.inl` implementation bodies; these are all
bound into the maintained native compiler's two private source snapshots.

The round scheduler switches between two independently allocated player
views several times each frame. They share the **semantic index** (left 0,
right 1), but not the physical storage: `pid_current` selects low-level
render/gameplay context, `pid.current` selects the player-state owner,
and `pid.so_attack` uses separate 0/40 sprite offsets. The maintained
source now assigns named, compiler-time values at all these selection
sites, while retaining the exact original order of BOSS/Extra Attack,
projectile, input, player, sprite and hardware-screen rendering calls.
No scheduler branches, byte counters or game timing were collapsed.

## Native C++ register-elimination negative control

`af785b` attempted `page_front = page_back;` after the original two
PC-98 hardware `OUT DX,AL` instructions. It is logically equivalent
at the machine state level here, but the original TC4 emits **two extra
CODE bytes**: it reloads `page_back` into AL before writing `page_front`.
The target uses AL left by the `OUT` (source `_AL`), which directly
writes the just-shown page. The original explicit AL use was restored.
The full CODE, not just a final program checksum, caught this difference.

## Current-source two-round original link validation

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af785c --units entry
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af785c
```

Genuine TC4 4.02 and normal MAIN TLINK independently ran twice and matched
**all 3,050 original initialized CODE bytes, 433 literal ordered OMF
FIXUPP fields, 8 PUBLIC offsets** and the whole normal MAIN EXE/MAP,
124,642-byte Japanese loaded program and all 1,553 literal ordered MZ
relocations. The 98 unchanged original project objects and CRT were reused;
**no cold replay** was run. Both native OMF COMENT source records bind the
current `entry.cpp` and four included `.inl` implementation files.

Protected local proof: `.analysis/work/exatt-layout-af785c/report.json`,
SHA-256 `4720f154dbbb26fc6bf6f31bc6afc517f6e81893239a5131c5079067a13da63c`.
The existing entry physical owner was previously proven historically; this
is **not** new distinct CODE ownership or canonical packed-game acceptance.
The rejected extra-AL-load is not accepted evidence.
