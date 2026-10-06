# MAIN character charge-shot / gauge owner review

This review expands the TH03 MAIN authored frontier beyond the currently exact
owners. It does not claim source or exact acceptance for these five modules yet.

## Target owner boundaries

scripts/review_th03_main_charge_gauge.py reads the immutable Japanese MAIN.EXE
and linearly decodes five complete character-local CODE segments. Function
boundaries are accepted only when the complete owner is partitioned without
gaps/overlaps and every function ends on its explicit RET/RETF contract. The
frozen th03_main.asm labels and MAP names are corroborating evidence, not the
boundary oracle.

| Owner | Segment | Bytes | Functions | Relocations |
| --- | --- | ---: | ---: | ---: |
| Chiyuri | MAIN_07_TEXT 1B26:0000 | 1011 | 9 | 9 |
| Ellen | MAIN_08_TEXT 1B65:0003 | 1530 | 10 | 22 |
| Kana | MAIN_09_TEXT 1BC4:000D | 1291 | 9 | 9 |
| Kotohime | MAIN_10_TEXT 1C15:0008 | 690 | 9 | 8 |
| Rikako | MAIN_11_TEXT 1C40:000A | 1280 | 11 | 12 |
| **Total** |  | **5802** | **48** | **60** |

The retained target review is
.analysis/th03-main-charge-gauge/target-review-v1.json.

The five owner ranges are disjoint. Each owner is a complete segment
contribution, so there is no unclassified tail/padding inside these reviewed
extents.

## Chiyuri first reconstruction target

Chiyuri's complete MAIN_07_TEXT owner is 1011 bytes / 382 decoded instructions
/ 9 functions. Its exact function partition is:

| Function | Offset | Bytes | Return |
| --- | ---: | ---: | --- |
| chiyuri_charge_setup | 0000 | 23 | RETF |
| chargeshot_add_chiyuri | 0017 | 75 | RETF 4 |
| chargeshot_update_chiyuri | 0062 | 157 | RETF |
| chiyuri_chargeshot_private | 00FF | 81 | RET |
| chargeshot_hittest_chiyuri | 0150 | 119 | RETF |
| chargeshot_render_chiyuri | 01C7 | 101 | RETF |
| gauge_pattern_chiyuri | 022C | 407 | RET 2 |
| gba_gauge_pattern_pellet_chiyuri | 03C3 | 24 | RETF |
| gba_gauge_pattern_bullet_chiyuri | 03DB | 24 | RETF |

The ordered owner relocation sequence is:

956, 892, 879, 794, 775, 434, 331, 299, 199

The current reconstruction hypothesis is a natural Turbo C++ character module,
not a TASM copy. Existing TH03 declarations already expose the player,
charge-shot function-pointer, hitbox, hit-circle, bullet-template, sprite16 and
gauge interfaces needed by this owner.

Target state indexing also gives useful source constraints before compiling:

- 1F54: two 16-bit gauge-pattern X positions (pid * 2)
- 1F58: two 8-bit gauge-pattern frame counters (pid)
- 1F5A: 96 bytes indexed as pid * 0x30, exactly 2 players * 8 charge shots * 6 bytes
- 1F84: 1F5A + 7 * 6, the last charge-shot element of each player block
- 1F51A: a separate near render scratch pointer
- 2D58: a per-player gauge timing record with stride 4

These are structural hypotheses for natural source recovery. They must be
confirmed by TC4 object shape and full-link behavior; no exact credit is
inferred from address arithmetic alone.

## Acceptance plan

For each character owner:

1. reconstruct natural C++ and compile with the pinned TC4J toolchain;
2. require the complete object CODE instruction offset/size/mnemonic shape to
   match the immutable target;
3. determine actual OMF producer and DATA/BSS ownership rather than assuming
   the root carrier layout is historical;
4. integrate the producer into the full MAIN cold build;
5. require raw owner bytes, exact MAP contribution and ordered MZ relocations;
6. rerun the full accepted MAIN aggregate twice and retain all existing exact
   owners.

Chiyuri is the first implementation target. Ellen/Kana/Kotohime/Rikako stay
reviewed candidates until their natural source and producer evidence pass the
same gates.

## Chiyuri natural TC4 producer

src/main/player/chargeshot_chiyuri.cpp now reconstructs the complete
MAIN_07_TEXT owner as natural Turbo C++. A fresh pinned TC4J object compile
produces one MAIN_07_TEXT CODE segment of exactly 1011 bytes, no private BSS,
382 decoded instructions, and all nine target return boundaries. Every
instruction offset, size and mnemonic matches the immutable target.

Three source-level details were material to reproducing TC4J's target shape:

- copying the charge-shot center as two independent 16-bit X/Y assignments
  rather than one struct assignment prevents -3 from collapsing it into
  32-bit EAX moves and also restores the target near conditional jump;
- initializing the hittest loop variable before the byte hit counter preserves
  the target XOR DI,DI / stack-byte-clear ordering;
- assigning flag_expected = flag_expected + ... rather than using +=
  prevents TC4J from folding the target load/add/store sequence into one memory
  ADD.

The reproducible object probe is:

    python3 scripts/probe_th03_main_chargeshot_chiyuri_cpp.py --run-id UNIQUE_ID

The retained receipt is
.analysis/th03-main-chargeshot-chiyuri-cpp/gpt-web-chiyuri-charge-v5-20261007/receipt.json.

This is intentionally not exact acceptance yet. The object contains 211 raw
pre-link byte differences, as expected for unresolved data/fixup operands.
The next gate is a full MAIN link that places this producer at
1B26:0000..03F2, restores the historical state bindings, and reproduces all
nine ordered owner relocations without weakening the existing aggregate.
