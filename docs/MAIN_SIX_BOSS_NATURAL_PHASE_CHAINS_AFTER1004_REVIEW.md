# TH03 MAIN: natural early-exit phase chains across six complete BOSSes

Six complete BOSS translation units now use ordinary C++ else-if chains
where each preceding timed phase already exits the function. The changes
make the mutually exclusive attack/render phases explicit without changing
the original TC4 4.02 output.

The core form is straightforward:

    if(frame < FIRST_PHASE_END) {
        // first phase
        return;
    } else if(frame < SECOND_PHASE_END) {
        // second phase
        return;
    }

The same form applies to exact-frame events when every earlier event path
returns. It does not apply blindly to sequential checks that intentionally
fall through or mutate shared state before the next check.

## Complete physical owners and individual compiler proofs

Each source was tested independently as its complete original physical
BOSS object in two independent original Turbo C++ 4.02 rounds, with the
complete normal MAIN link in both rounds.

| BOSS owner | Natural phase-chain recovery | CODE | Ordered OMF FIXUPPs | PUBLICs | Stage |
| --- | --- | ---: | ---: | ---: | --- |
| Mima | Spread setup/fire phases; particle/expand/flash/trail renderer modes | 1,922 | 277 | 9 | af1002d |
| Reimu | Narrow/medium spread phases; orbit-burst expand/hold/release phases | 2,020 | 270 | 9 | af1003a |
| Yumemi | Ring warning/fire phases; aimed-shot warning/fire phases | 2,358 | 343 | 10 | af1003c |
| Ellen | Extra-attack pre-warning, warning, first-burst and final-burst phases | 1,675 | 213 | 9 | af1003d |
| Kana | Staged ring start, warning, emission and finish phases | 1,874 | 274 | 9 | af1003e |
| Marisa | Wide- and narrow-column warmup, four emission frames and finish | 1,431 | 199 | 9 | af1003f |

All six reports bind to the final maintained source hashes and reproduce
the complete original CODE and ordered native fields. Each pair of normal
MAIN links also reproduces the 124,642-byte Japanese loaded image and all
1,553 ordered MZ relocations.

## Mima renderer detail

The particle, expand, flash and trail modes are now expressed as one
mutually exclusive if / else-if chain. The trail mode still resets its
byte render frame and uses the original backward goto render_mode_2,
which enters the shared particle body. Making the modes exclusive in the
source does not require replacing that compiler-sensitive label.

Mima's spread setup and firing gates are likewise expressed as an
if / else-if pair because the setup phase returns before the firing
phase can be considered.

## Additional complete-object experiments

- Mima af1002a moved trail normalization before the particle test and
  combined particle/trail into one condition. Complete CODE changed.
- Mima af1002c reversed the trail phase branch predicate and assignments.
  Complete CODE changed.
- Mima af1002e replaced the sprite-offset compound increment with an
  explicit self-assignment. Complete CODE changed.
- The successful else-if transformations are deliberately limited to
  branches whose preceding path returns; the failed alternatives above
  were restored before the final source proofs.

## Simultaneous twelve-owner integration

Stage af1004a rebuilt all nine major BOSSes together with the complete
Hitbox, HitCircle and explosion-chain owners in each of two independent
original compiler rounds, then ran the complete normal MAIN link twice.

| Scope | Exact original result |
| --- | ---: |
| Complete physical owners | 12 |
| CODE | 18,792 bytes |
| Ordered OMF FIXUPPs | 2,546 |
| PUBLICs | 91 |
| Japanese MAIN loaded image | 124,642 bytes |
| Ordered MZ relocations | 1,553 |

All twelve complete owner scopes match their original CODE and ordered
native fields in both rounds. Both full normal MAIN links reproduce the
complete original loaded image and relocations. The other 87 original game
objects and Borland CRT were reused; no full cold replay was run.

## Reproduction

Individual owner checks:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1002d --units ba_mima
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1003a --units ba_reimu
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1003c --units ba_yumem
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1003d --units ba_ellen
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1003e --units ba_kana
    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1003f --units ba_maris

Simultaneous integration:

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af1004a \
      --units ba_mima,ba_reimu,ba_yumem,ba_ellen,ba_kana,ba_koto,ba_maris,ba_rikak,ba_chiyu,hitbox,hitcirc,e_expl

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af1004a

Protected integration report:
.analysis/work/exatt-layout-af1004a/report.json, SHA-256
958570ce186dc75e33a10d0b63d6a90edfd8c7ef1f63defbc2626e41c4b646c9
