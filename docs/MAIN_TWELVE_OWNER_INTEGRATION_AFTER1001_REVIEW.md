# TH03 MAIN: twelve complete BOSS and collision owners rebuilt together

Stage af1001e is one simultaneous two-round original compiler and complete
normal MAIN link for twelve maintained physical project objects. It combines
all nine major BOSSes with the full Hitbox, HitCircle and explosion-chain
collision owners.

| Original physical owner | Complete maintained scope | CODE bytes | Ordered OMF FIXUPPs | PUBLICs |
| --- | --- | ---: | ---: | ---: |
| ba_mima | Nine-function Mima BOSS | 1,922 | 277 | 9 |
| ba_reimu | Nine-function Reimu BOSS | 2,020 | 270 | 9 |
| ba_yumem | Nine-function Yumemi BOSS | 2,358 | 343 | 10 |
| ba_ellen | Nine-function Ellen BOSS | 1,675 | 213 | 9 |
| ba_kana | Nine-function Kana BOSS | 1,874 | 274 | 9 |
| ba_koto | Kotohime BOSS | 1,840 | 262 | 11 |
| ba_maris | Marisa BOSS | 1,431 | 199 | 9 |
| ba_rikak | Rikako BOSS | 1,677 | 215 | 8 |
| ba_chiyu | Chiyuri BOSS | 2,654 | 381 | 11 |
| hitbox | Complete shot-pair/explosion/Chargeshot/Bomb collision | 266 | 33 | 1 |
| hitcirc | Complete HitCircle spawn/update/render owner | 445 | 30 | 4 |
| e_expl | Complete explosion collision and chain engine | 630 | 49 | 1 |
| **Twelve original physical owners** | | **18,792** | **2,546** | **91** |

Both independent original Turbo C++ 4.02 rounds rebuilt all twelve owners
together and ran the complete normal MAIN TLINK. Both reproduce the complete
124,642-byte Japanese MAIN loaded image and all 1,553 ordered MZ relocations.
The other 87 original game objects and Borland CRT were reused; no full cold
replay was run.

This integrated source set includes the current HitCircle cel calculation
with its self-division assignment and named VRAM-derived stride, Mima's
explicit trail-byte narrowing and natural hit truth test, the nine-BOSS
cadence work, the combined Hitbox early guard and the natural Explosion
for-header/ordered collision prefilters.

## Reproduction

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1001e \
      --units ba_mima,ba_reimu,ba_yumem,ba_ellen,ba_kana,ba_koto,ba_maris,ba_rikak,ba_chiyu,hitbox,hitcirc,e_expl

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af1001e

Protected report:
.analysis/work/exatt-layout-af1001e/report.json, SHA-256
139acc3f4f193d073a638043e0d1f2323b8e7ff83b9612bd8c0844988d54eeb6
