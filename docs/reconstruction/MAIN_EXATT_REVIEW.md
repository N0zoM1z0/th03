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
      --run-id gpt-web-exatt-yumemi-v04x-20261007

Receipt:

    .analysis/th03-main-exatt-yumemi-cpp/gpt-web-exatt-yumemi-v04x-20261007/receipt.json

The TC4J object is exactly 1696 bytes and all five function starts, lengths,
instruction shapes and RET/RETF contracts match the TH03 target. The 81-byte
secondary helper is exported directly as YUMEMI_EXTRA_ADD so the already-exact
Yumemi boss owner can bind to the natural producer without a carrier alias. Two
compiler-guided source corrections were needed after the first successful
compile: preserve the original grouped radius/top evaluation in the large
renderer, and delay the update loop-index initialization until after the
pid/collision-map setup.

Yumemi is followed immediately by Rikako inside the same physical
MAIN_06_TEXT segment, so the accepted linker strategy is a two-producer suffix
carve rather than inserting Yumemi alone between carrier contributions.

## Rikako natural TC4 producer and suffix strategy

src/main/player/exatt_rikako.cpp reconstructs the complete 702-byte Rikako
owner as five natural TC4 functions, including the 300-byte update and 171-byte
renderer. The object also exports the 84-byte semantic rikako_extra_add helper
used by the already exact Rikako boss producer. It emits no private DATA/BSS.

Object-shape replay:

    python3 scripts/probe_th03_main_exatt_rikako_cpp.py \
      --run-id gpt-web-exatt-rikako-v03x-20261007

Receipt:

    .analysis/th03-main-exatt-rikako-cpp/gpt-web-exatt-rikako-v03x-20261007/receipt.json

All 702 bytes / five function starts, lengths, instruction shapes and return
contracts match. Together, the proven Yumemi and Rikako sources cover the final
2398 bytes of MAIN_06_TEXT. The physical carve retains the shared/Reimu/Mima
prefix in th03_main.asm, removes the Yumemi+Rikako suffix, then links ex_yume
followed by ex_rika immediately after the carrier. No interleaving inside one
ASM object is required.

## Yumemi + Rikako suffix full-link candidate

The combined suffix carve now passes the repository full-link oracle:

    python3 scripts/replay_th03_main_exact_units.py       --candidate-manifest config/th03_main_exatt_yumemi_rikako_candidate.toml       --run-id gpt-web-exatt-yumemi-rikako-full-link-c01x-20261007

Receipt:

    .analysis/th03-main-exact/gpt-web-exatt-yumemi-rikako-full-link-c01x-20261007/receipt.json

Both cold rounds are raw-byte identical for Yumemi (1696 bytes) and Rikako
(702 bytes), with exact MAIN_06_TEXT MAP placement and all 36 + 9 target
relocations in their original order. The aggregate reaches 44666 owned bytes /
43743 function bytes, produces 20 deterministic products / 379 game objects /
445 validated objects, and passes the maintained DOS behavior probe.

The receipt hashes match the current Yumemi/Rikako sources, headers and
candidate manifest. This is full-link candidate proof only; neither owner is
promoted exact until the same carve is merged into the default manifest and a
fresh no-candidate replay passes.
