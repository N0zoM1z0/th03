# TH03 MAIN Extra Attack target review

This review expands the authored MAIN frontier beyond the already exact
41-byte generic P_EXATT_TEXT owner. It is target-boundary evidence only:
the immutable TH03 MAIN.EXE is the byte oracle, while frozen ReC98 labels
supply stable names for observed starts. No source or exactness is inferred
from TH04 or ReC98.

The reproducible review is:

    python3 scripts/review_th03_main_exatt_family.py \
      --output .analysis/th03-main-exatt-family/target-review-v1.json

The target partitions into ten complete logical owners around the existing
generic P_EXATT_TEXT gap at 18FE:119E..11C6:

| Owner | MAP segment | Group offset | Bytes | Functions | MZ relocations |
| --- | --- | ---: | ---: | ---: | ---: |
| Chiyuri | P_EXATT_TEXT | 000A | 1029 | 5 | 23 |
| Ellen | P_EXATT_TEXT | 040F | 1078 | 5 | 14 |
| Kana | P_EXATT_TEXT | 0845 | 663 | 5 | 8 |
| Marisa | P_EXATT_TEXT | 0ADC | 676 | 5 | 7 |
| Kotohime | P_EXATT_TEXT | 0D80 | 1054 | 8 | 15 |
| shared | MAIN_06_TEXT | 11C7 | 215 | 2 | 4 |
| Reimu | MAIN_06_TEXT | 129E | 941 | 8 | 14 |
| Mima | MAIN_06_TEXT | 164B | 727 | 4 | 10 |
| Yumemi | MAIN_06_TEXT | 1922 | 1696 | 5 | 36 |
| Rikako | MAIN_06_TEXT | 1FC2 | 702 | 5 | 9 |

The new scope is **8781 bytes / 52 complete functions / 140 in-owner MZ
relocations**. Every owner is a function-only linear partition: there are no
unclassified producer bytes and no relocation crosses an owner edge.

The largest functions are intentionally part of the review rather than being
deferred: yumemi_1A9B0 is 1150 bytes, exatt_update_ellen 470,
exatt_update_mima 398, exatt_update_kotohime 351,
exatt_update_yumemi 324, exatt_update_rikako 300,
exatt_update_chiyuri 298 and exatt_update_reimu 281 bytes.

P_EXATT_TEXT and MAIN_06_TEXT share the MAIN_06 linker group. Therefore the
recorded offsets stay MAP/group-relative (000A..2280) rather than inventing a
zero-based MAIN_06 address space. The already exact generic exatt_add owner
remains a separate 41-byte extent at 119E..11C7.

This review does **not** claim natural source, compiler producer identity, or
exact acceptance for the ten new owners. Those require TC4 object-shape work,
carrier-state analysis, full-link MAP/ordered-relocation comparison and the
default aggregate replay.

## Yumemi natural TC4 producer

The first complete natural-source reconstruction on this frontier deliberately
targets the largest owner rather than a leaf. src/main/player/exatt_yumemi.cpp
covers all 1696 Yumemi bytes / five functions, including the 1150-byte renderer
and 324-byte update. The historical 16-slot, 32-byte-per-entity pool and shared
MAIN_06 helpers remain external; the C++ object emits no private DATA/BSS.

Object-shape replay:

    python3 scripts/probe_th03_main_exatt_yumemi_cpp.py \
      --run-id gpt-web-exatt-yumemi-v03x-20261007

Receipt:

    .analysis/th03-main-exatt-yumemi-cpp/gpt-web-exatt-yumemi-v03x-20261007/receipt.json

The TC4J object is exactly 1696 bytes and all five function starts, lengths,
instruction shapes and RET/RETF contracts match the TH03 target. Two
compiler-guided source corrections were needed after the first successful
compile: preserve the original grouped radius/top evaluation in the large
renderer, and delay the update loop-index initialization until after the
pid/collision-map setup.

This is object proof only. Yumemi is followed immediately by Rikako inside the
same physical MAIN_06_TEXT segment, so an honest linker carve cannot insert the
Yumemi object alone between carrier contributions. The next full-link path is
to reconstruct Rikako as well and replace the complete Yumemi+Rikako suffix
with two consecutive TC4J objects.
