# TH03 MAIN: natural cadence predicates across nine complete BOSS owners

Nine complete BOSS translation units now express their periodic attack and
render gates with ordinary C++ equality or low-bit tests. The changes cover
24 predicates while preserving the original unsigned 16-bit frame clock,
variable intervals, firing phases, bullet order and renderer selection.

| BOSS owner | Native-exact source recovery |
| --- | --- |
| Mima | The six-frame pellet gate compares the unsigned remainder explicitly with zero. |
| Reimu | The variable cloud interval compares with zero; the two-frame acceleration and sixteen-frame mirror gates use low bits. |
| Yumemi | Four-, two- and sixteen-frame attack phases use low-bit masks, including the nonzero warning phases; both variable attack intervals compare with zero. |
| Ellen | Both two-frame spread gates use the unsigned-word low bit. |
| Kana | The variable cloud interval compares with zero; the four-frame rotating-ring gate and four-state intro animation index use low bits. |
| Kotohime | The four-frame warning flicker uses the low two frame bits. |
| Marisa | The four-frame spread and 32-frame ring gates use low-bit masks. |
| Rikako | Three eight-frame spin updates and both two-frame intro blink tests use low bits. |
| Chiyuri | The eight-frame bomb warning cadence uses a low-bit mask. |

A power-of-two period can be expressed as frame & (PERIOD - 1).
Zero/nonzero phases remain explicit where useful. Non-power-of-two or
level-dependent intervals stay as remainder expressions; Mima's six-frame
pellet cadence and the variable cloud intervals are examples. Mutable
byte animation counters are a separate compiler problem and are not
generalized from these 16-bit frame-clock results.

## Independent object experiments

The changes were first tried and checked against each complete original
physical BOSS object, then integrated together:

- Mima af990a: six-frame remainder equality.
- Reimu af990c and af992b: variable-interval equality and low-bit cloud
  acceleration/mirror gates.
- Ellen af990d and af992c: explicit remainder comparisons, then
  equivalent two-frame low-bit gates.
- Marisa af990e: spread and ring low-bit gates.
- Yumemi af991a and af993b: four power-of-two attack phases and both
  variable-interval zero comparisons.
- Rikako af991b: three spin clocks and two blink clocks.
- Kana af991c, af992d and af993c: rotating-ring, intro animation and
  variable cloud-interval phases.
- Kotohime af991d: warning flicker.
- Chiyuri af991e: trail-bomb warning cadence.

## Nine-object original compiler integration

The final af993d stage rebuilt all nine complete original BOSS objects
together in each of two independent Turbo C++ 4.02 rounds, followed by the
complete normal MAIN link:

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
| ba_chiyu | 2,654 | 381 | 11 |
| **Nine complete BOSS owners** | **17,451** | **2,434** | **85** |

Both rounds reproduce the complete 124,642-byte Japanese MAIN loaded image
and all 1,553 ordered MZ relocations. The other 90 original game objects
and the original Borland CRT were reused; no full cold replay was run.

## Reproduction

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/probe_th03_main_exatt_layout.py --stage af993d \
      --units ba_mima,ba_reimu,ba_yumem,ba_ellen,ba_kana,ba_koto,ba_maris,ba_rikak,ba_chiyu

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
      scripts/review_th03_main_source_overlay.py --stage af993d

Protected report:
.analysis/work/exatt-layout-af993d/report.json, SHA-256
32c364c85247438b143a39b5f22d54c9163caa1aceccfd5faa76b399dd214854
