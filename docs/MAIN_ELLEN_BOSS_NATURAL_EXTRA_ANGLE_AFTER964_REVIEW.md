# TH03 MAIN Ellen BOSS: natural byte-angle updates in both radial Extra volleys

Both independent radial Extra Attack bursts in the complete ellen_pattern_extra()
controller now express their mutable byte angle as ordinary C++ addition and
assignment:

    angle = angle + (ELLEN_EXTRA_FULL_TURN_UNITS / ellen_extra_count);

The first and last bursts still draw their own RNG word, use the original
byte-sized projectile count, divide the 256-unit turn at each iteration,
call the far ellen_extra_add() with their distinct signed mode, and update
the byte angle only after the spawn. The assignment preserves the original
integer division, unsigned-byte truncation/wrap, and per-projectile order.

This is a useful distinction from the other codegen-sensitive byte updates:
the earlier Ellen spread/pellet/intro angles already accepted the natural
assignment form, while Rikako's signed boss_spin_delta compound update
does not. The actual compiler result here confirms the same natural spelling
for both runtime-quotient radial volleys; it was not inferred from the
constant-step cases.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af964a --units ba_ellen
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af964a

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire 1,675-byte original Ellen BOSS and linked each object through the
complete normal MAIN response. Both reproduce all 213 literal ordered OMF
FIXUPP fields and nine PUBLIC offsets, the complete original Japanese
MAIN loaded image (124,642 bytes) and all 1,553 ordered MZ relocations.
The other 98 original game objects and original Borland CRT were reused;
no full cold replay.

Protected source-current report:
.analysis/work/exatt-layout-af964a/report.json, SHA-256
d0d4384d45de700bbe3f9fd7a0ff71a2b6d1684467331d41cb90e21bbca2b1fe.
