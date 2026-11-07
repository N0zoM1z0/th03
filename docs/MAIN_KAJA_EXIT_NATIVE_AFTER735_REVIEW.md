# TH03 MAIN sound driver/PC-98 shutdown: direct original source-native after735

The complete `snd_kaja` (30 original SHARED CODE bytes, 2 literal ordered
native fixups, one PUBLIC) and `exit` (67 original SHARED CODE bytes, 8
fixups, one PUBLIC) physical Turbo C++ translation units were directly
source-bound for this first-use proof in the current scoped workflow.
Both use the original 3-segment OMF code/empty DATA/BSS layouts and real
original `obj/th03/snd_kaja.obj` and `obj/th03/exit.obj` link positions.

The sound driver's `snd_kaja_interrupt()` is **not** a generic call to
an arbitrary interrupt value. It preserves the original state-dependent
choice between static PMD software interrupt **0x60** and MIDI software
interrupt **0x61**, including the inactive early return that preserves
caller-visible `_AX`. Those constants are now separate named compile-time
software vector enums without introducing runtime switching or DATA.

`game_exit()` retains its actual PC-98 hardware shutdown order: archive
close, display page 1 / graphics clear, page 0 / graphics clear,
reassert display page 0, access page 0, followed by VSYNC, DOS memory,
TRAM, joystick and EGC cleanup. The original distinct display page
register **0xA6** and access page register **0xA4** are now naturally
named compile-time C++ enums. No repeated I/O writes have been
combined or removed, and the explicit register `out dx, al` instructions
remain hardware-accurate.

The baseline source of all four newly recognized original sound/input/
PI/exit physical objects was tested at `af734a`. The **current modified**
source for exactly these two hardware producers was independently compiled
with genuine original Turbo C++ 4.02 and linked to full normal MAIN twice:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af735a --units snd_kaja,exit
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af735a

Both rounds exactly reproduce **all 97 original CODE bytes, all 10 literal
ordered OMF FIXUPP fields and 2 original PUBLIC offsets**, exact segment
metadata, full normal source-native MAIN EXE/MAP, Japanese 124,642-byte
loaded program and all 1,553 ordered MZ relocations. Independent standard
MZ serialization reproduces all **130,882 original Japanese file bytes**,
without claiming historical TLINK direct header equality. The other
97 original project objects and CRT were **reused**, no full cold replay.

Evidence: `.analysis/work/exatt-layout-af735a/report.json`, SHA-256
`adef3882992462a01c6aed789809104bd78bc3e58b171a990e6b21299c845d1e`.
Original target, linker response, source snapshot, actual compiler OMF
source dependencies, original and new object/EXE/MAP outputs and writer
logs for both independent rounds are retained, untouched. These are newly
**current directly source-attested physical TUs**, not newly accepted
canonical packed Factory game bytes, historical vendor raw OMF packet
identity or a complete source-owned MAIN build.
