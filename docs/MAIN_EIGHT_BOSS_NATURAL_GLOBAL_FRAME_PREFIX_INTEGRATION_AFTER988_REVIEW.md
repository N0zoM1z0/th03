# TH03 MAIN: eight major BOSS frame clocks in one native integration

All eight maintained major-BOSS update functions now use the natural
prefix increment for the shared 16-bit boss_frame. The old value is not
consumed, and original Turbo C++ 4.02 emits the same complete object code
for each prefix form.

This is a simultaneous source integration, not the sum of eight isolated
claims. Each of two independent original compiler rounds rebuilt all eight
physical BOSS objects together, then performed the complete normal MAIN
link while reusing the other 91 original game objects and Borland CRT.

| Physical owner | CODE bytes | Ordered OMF FIXUPPs | PUBLICs |
| --- | ---: | ---: | ---: |
| ba_mima | 1,922 | 277 | 9 |
| ba_reimu | 2,020 | 270 | 9 |
| ba_yumem | 2,358 | 343 | 10 |
| ba_ellen | 1,675 | 213 | 9 |
| ba_kana | 1,874 | 274 | 9 |
| ba_koto | 1,840 | 262 | 11 |
| ba_maris | 1,431 | 199 | 9 |
| ba_rikak | 1,677 | 215 | 8 |
| **Eight original physical BOSS owners** | **14,797** | **2,053** | **74** |

Both rounds reproduce the complete 124,642-byte Japanese MAIN loaded image
and all 1,553 ordered MZ relocations. The other 91 original game objects
and the original Borland CRT were reused; no full cold replay was run.

## Original compiler commands

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af988b \
      --units ba_mima,ba_reimu,ba_yumem,ba_ellen,ba_kana,ba_koto,ba_maris,ba_rikak

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af988b

Protected report:
.analysis/work/exatt-layout-af988b/report.json, SHA-256
409055acc70a43c445e26039d863ee9da88f40f7897a5ac58468178d61bc355e.
