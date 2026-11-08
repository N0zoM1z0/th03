# TH03 MAIN Marisa BOSS: natural flicker mask and split-radius scaling

The complete Marisa BOSS now expresses two renderer operations more directly:

- The unsigned four-frame flicker phase uses frame & (period - 1) instead
  of % period. Since the source frame is unsigned and the period is four,
  this is the same low-bit phase and original TC4 emits identical CODE.
- The split-sprite intro radius uses boss_frame * 2 instead of boss_frame
  << 1. TC4 emits the same signed-width arithmetic and original call
  argument.

The split renderer's first register local is now typed as
register screen_x_t signed_offset = offset, before the register screen_x_t
left local. screen_x_t is the project's signed screen-coordinate type
(int in this 16-bit target). The declaration order still causes TC4 to
allocate SI to the offset and DI to the screen coordinate, replacing the
original manual _SI write with natural register allocation.

A fresh negative control removed register from signed_offset; the full
BOSS CODE comparison failed, so the qualifier remains. This confirms that
the register allocation is not incidental and that the earlier declaration
order finding still matters.

## Original compiler verification

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af975d --units ba_maris
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af975d

Two independent genuine original Turbo C++ 4.02 rounds recompiled the
entire nine-function, 1,431-byte original Marisa BOSS. Both preserve
all 199 literal ordered OMF FIXUPP fields and nine PUBLIC offsets;
both complete normal MAIN links reproduce the 124,642-byte Japanese
loaded image and all 1,553 ordered MZ relocations. The other 98
original game objects and Borland CRT were reused.

Protected current-source report:
.analysis/work/exatt-layout-af975d/report.json, SHA-256
138823acc2036573271773d98d3cd367e96c092c8dde16e8c65b6501d0b420e5.
