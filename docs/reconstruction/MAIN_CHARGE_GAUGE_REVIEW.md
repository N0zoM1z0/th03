# MAIN character charge-shot / gauge owner review

This review expands the TH03 MAIN authored frontier beyond the earlier exact
owners. Chiyuri and Ellen are now accepted exact; Kana, Kotohime and Rikako
remain boundary-reviewed source-reconstruction targets.

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

Chiyuri and Ellen have completed all six gates above. Kana/Kotohime/Rikako
stay reviewed candidates until their natural source and producer evidence pass
the same gates; Kana is the next implementation target.

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

The current object-shape receipt is
.analysis/th03-main-chargeshot-chiyuri-cpp/gpt-web-chiyuri-charge-linkfix-v7-20261007/receipt.json.

## Chiyuri exact full-link promotion

The full-link integration keeps an empty MAIN_07_TEXT anchor in the frozen
carrier and adds one cs_chiyu.cpp TC4J producer. Anonymous historical carrier
storage is not moved: the 102-byte block starting at DGROUP:1F54 is split into
semantic aliases for the two-word X array, two-byte frame array and 96-byte
charge-shot array; word_1F51A gains the render-pointer alias; and the first
eight bytes at DGROUP:2D58 gain the two-entry gauge timing alias.

The first full-link candidate was already structurally correct: MAP placement
and all nine ordered relocations matched, and 1010/1011 bytes were equal. Its
single mismatch was the render height immediate: sprite16_put_size.set(32, 24)
stores 12 because the helper converts pixel height to VRAM height. Using
set(32, 48) preserves the natural helper call while storing the target raw
height 24.

After that correction, the two-round candidate replay passes all 1011 owner
bytes, MAP placement, ordered relocations and all previously accepted owners:

    .analysis/th03-main-exact/gpt-web-chiyuri-charge-full-link-v2-20261007/receipt.json

The owner was then merged into the default exact manifest and a replay with no
candidate overlay also passes:

    .analysis/th03-main-exact/gpt-web-chiyuri-charge-promoted-default-v1-20261007/receipt.json

A post-ledger final-worktree default replay also passes:

    .analysis/th03-main-exact/gpt-web-chiyuri-charge-promoted-final-v2-20261007/receipt.json

At the Chiyuri promotion checkpoint, the default aggregate reached 136 exact
functions / 18871 function bytes / 19077 owned bytes with 20 products and 361
game objects deterministic. Chiyuri therefore has formal scoped exact CODE
acceptance; this does not claim that the surrounding anonymous BSS was
historically produced by the C++ object.

## Ellen natural TC4 producer

src/main/player/chargeshot_ellen.cpp now reconstructs the complete MAIN_08_TEXT owner as natural Turbo C++. A fresh pinned TC4J compile emits one 1530-byte MAIN_08_TEXT CODE segment, no private DATA/BSS, 534 decoded instructions, and all ten reviewed function end boundaries. Every instruction offset, size, and mnemonic matches the immutable target.

This owner required source-level compiler-shape corrections rather than byte patches: Ellen hyper keeps the shared near pointer as a global reload instead of caching it; the update routine preserves target local lifetimes and direct preliminary-scan exit; the hittest uses one compound four-bound comparison; the private renderer explicitly expresses the target SI/DI/AX lifetimes with the same Borland register-pseudo idiom already used by accepted src/main/bullet/bullet.cpp; and mirrored gauge X is preserved in DX so the helper call uses the target PUSH DX sequence.

The gauge helper contains a real internal early RET 2 on its initialization path in addition to its final RET 2. The object probe checks the complete target/candidate return sequence as well as each function final boundary, rather than assuming one return instruction per function.

Reproducible object probe:

    python3 scripts/probe_th03_main_chargeshot_ellen_cpp.py --run-id UNIQUE_ID

Current object-shape receipt:
.analysis/th03-main-chargeshot-ellen-cpp/gpt-web-ellen-charge-linkfinal-b01-20261007/receipt.json.

## Ellen exact full-link promotion

The default exact manifest keeps the historical MAIN_08_TEXT segment anchor in
the frozen carrier and adds one cs_ellen.cpp TC4J producer. Ellen's C++ object
emits no private DATA/BSS. Carrier aliases preserve the target storage layout:
two gauge X words at DGROUP:1FFE, two gauge Y words at 2002, two frame bytes at
2006, the 768-byte two-player charge-shot array at 2008, and the shared near
scratch pointer at 2308. The existing target-selection helper sub_16983 is
exported under a semantic Ellen name, while its two output coordinates remain
at their historical carrier words.

A default replay with no candidate overlay passes all 1530 owner bytes, the
exact MAIN_08_TEXT MAP contribution, and this 22-entry ordered relocation
sequence in both fresh rounds:

87,177,277,437,476,510,527,561,655,680,772,1218,1223,1257,1262,1304,1377,1382,1415,1420,1425,1465

Accepted technical receipt:

    .analysis/th03-main-exact/gpt-web-ellen-charge-default-b01-20261007/receipt.json

Post-ledger final-worktree regression:

    .analysis/th03-main-exact/gpt-web-ellen-charge-promoted-final-b02-20261007/receipt.json

That replay raises the aggregate to 146 exact functions / 20401 function bytes /
20607 owned bytes, with 20 deterministic products, 362 deterministic game
objects and the maintained DOS behavior probe. Ellen therefore has formal
scoped exact CODE acceptance. Physical historical ownership of the anonymous
carrier BSS remains a separate question, exactly as for the preceding character
owners.

## Kana natural TC4 producer

src/main/player/chargeshot_kana.cpp now reconstructs the complete MAIN_09_TEXT
owner as natural Turbo C++. A fresh pinned TC4J compile emits one 1291-byte
MAIN_09_TEXT CODE segment, no private DATA/BSS, 489 decoded instructions, and
all nine reviewed function boundaries. Every instruction offset, size and
mnemonic matches the immutable target.

The target indexing recovers a concrete trail layout rather than an anonymous
byte blob: each player owns four 54-byte trails, each trail stores thirteen X
words, thirteen Y words, one angle byte and one length byte. Rendering and
hittest sample history points 12/8/4/0 while update shifts the complete
12-point history. The only first-pass compiler-shape mismatch was register
allocation in update(): TC4J needed the outer four-trail loop to remain in DI
and the history-copy index to remain the stack word at BP-6. Declaring the
outer loop as register restores the exact target shape without assembly or
byte patching.

Reproducible object probe:

    python3 scripts/probe_th03_main_chargeshot_kana_cpp.py --run-id UNIQUE_ID

Retained receipt:

    .analysis/th03-main-chargeshot-kana-cpp/gpt-web-kana-charge-v2-20261007/receipt.json

## Kana exact full-link promotion

The accepted manifest now keeps the historical MAIN_09_TEXT segment anchor in
the frozen carrier and adds one cs_kana.cpp TC4J producer. The C++ object emits
no private DATA/BSS. Carrier aliases preserve the historical 2676/267A/267C/
282C/282E/2830 state slots without moving storage.

The two-round full-link candidate first passed all 1291 bytes, MAP placement
and the ordered relocation sequence:

228,467,500,646,1073,1090,1115,1132,1226

Retained candidate receipt:

    .analysis/th03-main-exact/gpt-web-kana-charge-full-link-f41a-20261007/receipt.json

After merging the owner into the accepted manifest, a replay with no candidate
overlay also passes:

    .analysis/th03-main-exact/gpt-web-kana-charge-promoted-default-d01-20261007/receipt.json

Post-ledger final-worktree regression:

    .analysis/th03-main-exact/gpt-web-kana-charge-promoted-final-d02-20261007/receipt.json

The aggregate is now 155 exact functions / 21692 function bytes / 21898 owned
bytes, with 20 deterministic products, 363 deterministic game objects and the
maintained DOS behavior probe. Kana therefore has formal scoped exact CODE
acceptance. Physical historical ownership of the surrounding anonymous carrier
BSS remains separate from this CODE claim.


## Kotohime natural TC4 producer

src/main/player/chargeshot_kotohime.cpp now reconstructs the complete
MAIN_10_TEXT owner as natural Turbo C++. A fresh pinned TC4J compile emits one
690-byte MAIN_10_TEXT CODE segment, no private DATA/BSS, 250 decoded
instructions, and all nine reviewed function boundaries. Every instruction
offset, size and mnemonic matches the immutable target.

The owner has a compact state model: two eight-byte per-player charge objects,
a two-byte gauge frame array, a shared near scratch pointer, and the already
shared four-byte-per-player gauge timing record. The hittest target contains a
material BX lifetime: after testing the active byte, TC4J reloads the shared
near pointer into BX before the coordinate comparisons. Pure expression
rewrites either retained BX across the branch or introduced an SI register
local. The accepted source uses the same Borland register-pseudo idiom already
present elsewhere in maintained natural source to express that one reload
without copying target assembly.

Reproducible object probe:

    python3 scripts/probe_th03_main_chargeshot_kotohime_cpp.py --run-id UNIQUE_ID

Retained receipt:

    .analysis/th03-main-chargeshot-kotohime-cpp/gpt-web-kotohime-charge-v5-20261007/receipt.json

This is source/producer-shape evidence only. Full-link acceptance must bind the
historical 28F8/28FA/290A state slots and the existing Kotohime gauge-spawn
helper, prove the exact MAIN_10_TEXT MAP contribution, all 690 linked bytes and
the eight-entry ordered relocation sequence, and retain all previously accepted
owners.
