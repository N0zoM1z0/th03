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

The historical receipt hashes match the Yumemi/Rikako sources, headers and
candidate manifest at the time. That candidate manifest was merged into the
maintained default exact manifest during the subsequent promotion, then removed
as a redundant tracked overlay; its frozen copy survives in the candidate
receipt. The command above documents the historical candidate proof, not a
current runnable candidate path.

## Yumemi + Rikako default exact promotion (2026-10-08)

The consecutive 2398-byte suffix is now in
`config/th03_main_exact_units.toml`: `ex_yume` followed immediately by
`ex_rika` after the remaining MAIN_06 carrier prefix. Two unmodified natural
TC4J producers cover all ten reviewed functions, with no private DATA/BSS.
Both producers remain explicit game objects in the maintained link graph;
the frozen carrier retains original global state and the cross-owner helper
bindings. No byte-carrier substitution or relaxed comparator was used.

Fresh no-candidate default replay:

    python3 scripts/replay_th03_main_exact_units.py \
      --run-id gpt-web-exatt-suffix-default-p01-20261008

Receipt:

    .analysis/th03-main-exact/gpt-web-exatt-suffix-default-p01-20261008/receipt.json

Both serial cold rounds independently pass immutable-target raw bytes, exact
MAP contribution, and all ordered MZ relocations for each owner:

| Owner | Natural object / MAP contribution | Bytes / functions | Ordered relocations |
| --- | --- | ---: | ---: |
| Yumemi | `ex_yume`, `18FE:1922..1FC2` | 1696 / 5 | 36, exact order |
| Rikako | `ex_rika`, `18FE:1FC2..2280` | 702 / 5 | 9, exact order |

The second fresh no-candidate default aggregate was replayed *after* all exact
ledger and evidence updates and also passed:

    python3 scripts/replay_th03_main_exact_units.py \
      --run-id gpt-web-exatt-suffix-default-final-p02-20261008

Final receipt:

    .analysis/th03-main-exact/gpt-web-exatt-suffix-default-final-p02-20261008/receipt.json

The default repository Oracle increases from 268 functions / 42268 CODE bytes
to 278 functions / 44666 CODE bytes (43743 function bytes and 923 classified
producer-owned bytes), across 64 exact CODE extents / 57 maintained source
owners. The replay has 20 deterministic products, 379 game objects, 445
validated OMF objects, and passing DOS behavior probes. Nine Research-only
diagnostic objects retain normalized drift outside the accepted game vector.

**Limits:** This proves scoped MAIN CODE extents through the repository-local
Oracle, not whole-game closure, independently attested pristine target origin,
historical physical DATA/BSS ownership, or Factory Truth Kernel acceptance.
The remaining eight Extra Attack owners are boundary-reviewed only. The
contiguous shared/Reimu/Mima MAIN_06 prefix is the next physical-carve target.

## Mima complete natural source and exact promotion (2026-10-08)

The adjacent **Mima** owner at `18FE:164B..1922` (727 bytes) is now complete,
including its 398-byte update, 193-byte renderer helper, 89-byte add and
47-byte render dispatcher. It is reconstructed as natural TC4J source in
`src/main/player/exatt_mima.cpp`; the producer exports all four function
boundaries, near/far returns and ten relocation sites. No private DATA/BSS
is emitted, and the frozen entity storage remains separate.

The compiler-guided reconstruction deliberately included the 398-byte update.
Initial natural code produced 733 bytes; adjusting register allocation and
source branch grouping produced all 727 target-sized bytes with matching
instruction shape. The first full-link candidate still showed eight byte
differences, all in the renderer's BP-relative stack offsets. Swapping the
declaration order of `left` and `top` restored those offsets without using
literal target bytes or relaxing the comparison. The full-link candidate
`gpt-web-exatt-mima-link-c03-20261008` then passed both rounds: all raw
bytes, MAIN_06 MAP `M=th03/ex_mima.cpp`, ordered relocation sites
`43,52,111,244,432,525,563,591,614,657`, and maintained DOS behavior.

Independent pinned TC4 object-shape proof for the final maintained source:

    python3 scripts/probe_th03_main_exatt_mima_cpp.py \
      --run-id gpt-web-mima-shape-final-v06-20261008

Final no-candidate default source replay:

    python3 scripts/replay_th03_main_exact_units.py \
      --run-id gpt-web-mima-default-p02-20261008

Receipt:

    .analysis/th03-main-exact/gpt-web-mima-default-p02-20261008/receipt.json

The Mima carve removes only the frozen Mima CODE range from the carrier.
The real `ex_mima` object links before the existing `ex_yume` and
`ex_rika` producers. The resulting contiguous 3125-byte MAIN_06_TEXT
suffix (`164B..2280`) is exact within the repository Oracle scope.
The default aggregate now covers **282 functions, 44470 function bytes and
45393 owned bytes** (923 classified non-function producer bytes), 65 exact
CODE extents / 58 maintained source owners; both cold builds produce
20 deterministic products, 380 game objects and 446 generated OMF objects.
All remaining seven character Extra Attack owners retain boundary-only state.

This is not a claim of historical physical DATA/BSS producer ownership,
whole-product closure, independent pristine-target provenance, or Factory
Truth Kernel acceptance. The next contiguous frontier is Reimu plus the
shared 215-byte MAIN_06_TEXT helper prefix.

Post-ledger final no-candidate replay also passes both cold rounds:

    python3 scripts/replay_th03_main_exact_units.py \
      --run-id gpt-web-mima-default-final-p03-20261008

Receipt: `.analysis/th03-main-exact/gpt-web-mima-default-final-p03-20261008/receipt.json`.

## Reimu two-producer exact promotion (2026-10-08)

The complete **Reimu** MAIN_06_TEXT owner is reconstructed in natural
`src/main/player/exatt_reimu.cpp`: 941 CODE bytes, eight complete functions.
It includes the 281-byte game-state update, 205-byte renderer, an 80-byte
add function, the 92-byte far helper used by the already exact Reimu boss,
both shared 77-byte near renderer helpers, the 79-byte near collision-map
helper, and the 50-byte render dispatcher. Those shared routines are
owned by this original CODE interval rather than being duplicated in
their callers. Both near Pascal RET 6 and far Pascal RETF 6 contracts
remain explicit, as do the C++ far cdecl update/render calls.

Natural TC4J source reconstruction was compiler-guided against the
immutable TH03 target. The 941-byte compiled semantic object passed all
eight function starts, sizes, instruction shapes, and RET/RETF contracts.
The pinned object-shape command is:

    python3 scripts/probe_th03_main_exatt_reimu_cpp.py \
      --run-id gpt-web-reimu-exatt-shape-final-v06-20261008

The first full-link candidate `gpt-web-reimu-exatt-link-c01-20261008`
reproduced all 941 raw target bytes, exact MAP placement and all fourteen
relocation **sites**, but failed the original relocation **order**. The
single TC4J object produced the order in two swapped groups, so byte/site
identity was deliberately not accepted as exact.

The corrected source has two conditional physical producer builds, *not*
two unrelated semantic owners: `ex_repre` produces the first 610 bytes
(`18FE:129E..1500`, six functions), and `ex_reup` produces the final
331 bytes (`18FE:1500..164B`, update and dispatcher). Both objects use
the same maintained natural C++ source with only preprocessor visibility
controlled; their combined CODE and ABI are identical to the earlier
single-producer source. They precede the existing Mima/Yumemi/Rikako
physical producers in linker order. The original ordered MZ relocation
sequence for Reimu is:

    604, 593, 570, 493, 348, 319, 242, 153, 52, 43,
    855, 811, 801, 767

Candidate two-round cold replay `gpt-web-reimu-exatt-link-c03-20261008`
passed all raw bytes, both exact MAP contributions, the complete ordered
relocation sequence, existing exact owners, and the maintained DOS behavior
probe. The default manifest now contains the same tested physical carve:

    python3 scripts/replay_th03_main_exact_units.py \
      --run-id gpt-web-reimu-default-p01-20261008

Receipt:

    .analysis/th03-main-exact/gpt-web-reimu-default-p01-20261008/receipt.json

The default aggregate at this checkpoint has 290 exact functions /
45411 function bytes / 46334 owned CODE bytes (923 classified
producer-owned non-function bytes), 66 exact CODE extents / 59 maintained
source owners. All 20 game products, 382 game objects and 448 validated
OMF objects are present in each cold build. The contiguous Reimu+Mima+
Yumemi+Rikako suffix now covers **4066 exact CODE bytes** at
`18FE:129E..2280` across five physical producers. Six Extra Attack
owners remain boundary-reviewed without exact acceptance.

The physical identity of original DATA/BSS producers, independently
pristine target provenance, whole-game build closure and Factory
Truth Kernel acceptance remain explicitly open. No emulator/device
model or byte patch is treated as a substitute for the repository
raw/MAP/ordered-relocation Oracle.

Final post-ledger no-candidate aggregate replay:

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-reimu-default-final-p02-20261008

Receipt: .analysis/th03-main-exact/gpt-web-reimu-default-final-p02-20261008/receipt.json

Both cold rounds pass all earlier exact owners and the new Reimu owner with
raw bytes, exact MAP, ordered relocations and maintained DOS behavior.
The available post-unittest CI gates pass (see the retained
.analysis/th03-reimu-ci-postgates-20261008.log), but full CI remains
blocked by missing Python unicorn: 632 tests with 125 import errors
and 167 skips (.analysis/th03-reimu-ci-20261008.log).

## Shared flight owner exact (2026-10-08)

The complete remaining shared MAIN_06_TEXT prefix at 18FE:11C7..129E
is reconstructed as a natural Turbo C++ source under
src/main/player/exatt_shared.cpp (215 CODE bytes / 2 complete functions).
It exports a 70-byte near cdecl exatt_fly_update with plain near RET
and a 145-byte near Pascal exatt_fly_init with RET 0x0C. The calls from
still-carried P_EXATT_TEXT code and the already exact character producers
bind directly to the natural object. Frozen 32-byte entity storage stays
unchanged. There is no newly produced private BSS.

The first candidate compiled to precisely 215 bytes but had divergent
control-flow shape in exatt_fly_update. Reorganizing the signed boundary
comparison and branch targets into the observed semantic arrival/movement
paths restored the original 70-instruction-byte shape without target-byte
carriers. The 145-byte initializer already matched the full target
instruction shape. The final independent TC4J shape probe is:

    python3 scripts/probe_th03_main_exatt_shared_cpp.py --run-id gpt-web-exatt-shared-shape-final-v04-20261008

The two-round full-link candidate gpt-web-exatt-shared-link-c01-20261008
passed raw bytes, exact MAIN_06 map contribution ex_shfly at
18FE:11C7 with size 00D7, all four ordered MZ relocation sites
116,139,192,204 and maintained DOS behavior. The same natural producer
now precedes both Reimu physical producers in the maintained default
manifest. Initial no-candidate default replay:

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-exatt-shared-default-p01-20261008

Receipt:

    .analysis/th03-main-exact/gpt-web-exatt-shared-default-p01-20261008/receipt.json

The default scoped exact aggregate now reaches 292 functions /
45626 function bytes / 46549 owned CODE bytes, with 67 exact extents
and 60 maintained semantic source owners. Both cold builds preserve
20 products, 383 game objects, 449 generated OMF objects and
passing DOS behavior. All 4281 contiguous bytes at
18FE:11C7..2280 now come from natural C++ compiled by TC4J
across six physical producers: shared flight, two Reimu,
Mima, Yumemi and Rikako. The remaining five reviewed Extra
Attack character owners are within P_EXATT_TEXT and are *not*
promoted exact here. Whole-game build closure, independently
pristine original target provenance, physical DATA/BSS producer
ownership and Factory Truth Kernel acceptance remain open.

Post-ledger final no-candidate replay:

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-exatt-shared-default-final-p02-20261008

Receipt: .analysis/th03-main-exact/gpt-web-exatt-shared-default-final-p02-20261008/receipt.json

Both cold builds still pass with the source/evidence ledger and full
existing-owner acceptance frozen. The available CI checks after
unittest pass (.analysis/th03-shared-flight-postgates-20261008.log).
Full CI remains blocked by the missing host Python unicorn
module: 632 tests, 125 import errors and 167 skips. The failed
CI output is retained at .analysis/th03-shared-flight-ci-20261008.log.

## Ellen natural TC4J producer shape (2026-10-08; not exact)

The complete Ellen character Extra Attack owner at P_EXATT_TEXT
18FE:040F..0845 has now been reconstructed as natural C++ in
src/main/player/exatt_ellen.cpp and exatt_ellen.hpp.
The original five functions total 1078 CODE bytes: add 186,
boss-facing secondary add 103, renderer 269, update 470 and dispatcher 50.

The 470-byte update is deliberately in scope. It moves seven x/y history
samples for each of twelve 30-byte trajectory slots, computes polar
coordinates and velocity, processes playfield clipping and hitbox/collmap
events, and advances the original flight/state machine. The source
declares historical slot storage and the global cursor as external;
no private DATA/BSS is emitted. The original compiler's local variable
placement, branch form and slot dereference sequence were calibrated
against the immutable TH03 instructions, not guessed from ReC98 labels.

Pinned TC4 object-shape proof:

    python3 scripts/probe_th03_main_exatt_ellen_cpp.py --run-id gpt-web-exatt-ellen-v04-20261008

Receipt: .analysis/th03-main-exatt-ellen-cpp/gpt-web-exatt-ellen-v04-20261008/receipt.json

The object contains exactly 1078 CODE bytes, all five correct function
starts/lengths/instruction shapes/RET contracts and zero private BSS.
This does not establish exact linked bytes, MAP placement or ordered MZ
relocations. The owner remains boundary-reviewed and no exact byte
credit was added.

Important physical-link constraint: Ellen is in the middle of
P_EXATT_TEXT. Simply appending an Ellen object after the frozen carrier
would shift the Kana/Marisa/Kotohime suffix and existing generic P_EXATT
object. Planned suffix-to-prefix carve order: Kotohime, Marisa, Kana,
Ellen, Chiyuri, retaining the original P_EXATT_TEXT group layout at
each stage. Failed trials must not weaken existing owner comparisons.

At this source-shape checkpoint, preflight and the focused five-test
Extra Attack review suite pass. Full /usr/bin/python3 CI is still blocked
by the absent host unicorn module (632 tests, 125 import errors,
167 skips). Logs: .analysis/th03-ellen-shape-ci-20261008.log and
.analysis/th03-ellen-shape-postgates-20261008.log. All available
post-unittest CI gates pass, including the Ghidra/Oracle controls.

## Kotohime complete P_EXATT_TEXT natural-source exact promotion (2026-10-08)

Kotohime is the final complete character CODE owner in P_EXATT_TEXT, at
18FE:0D80..119E. All 1054 bytes now come from natural maintained
src/main/player/exatt_kotohime.cpp. This includes eight complete original
functions (115 + 87 + 207 + 38 + 104 + 104 + 351 + 48 bytes) and the
351-byte update with shot patterns, hitbox/collision and flight-state logic.
The source uses external historical 32-byte Extra Attack entities,
player state and Kotohime pattern settings; it emits no private DATA/BSS.

Pinned compiler-shape proof:

    python3 scripts/probe_th03_main_exatt_kotohime_cpp.py --run-id gpt-web-exatt-kotohime-shape-v05-20261008

The original P_EXATT_TEXT suffix was removed from the frozen ASM carrier
without shifting other owners or changing the CODE comparator. ex_koto.cpp
was inserted immediately before p_exatt.cpp in the maintained linker list.
The existing exact charge-gauge source previously invoked the carrier
KOTOHIME_GAUGE_SPAWN alias. It is now rebound directly to the original
far Pascal helper kotohime_extra_add, so the obsolete ASM alias is removed
rather than left as a dangling export. No change to accepted CODE bytes was
needed. The historical DGROUP pattern parameters are exposed as a
location-preserving alias of the existing gauge_pattern_timing storage.

The first complete candidate produced the correct 1054-byte CODE shape,
all 15 ordered MZ relocation sites and correct MAP placement, but differed
from the original in eight linked bytes in kotohime_extra_add. Comparing
the full-link target showed reversed SI/DI register initialization; the
natural source initialization order was corrected, not patched with raw
machine code. A later two-round candidate
gpt-web-exatt-kotohime-link-c04-20261008 passed full raw bytes, exact
P_EXATT_TEXT MAP at 18FE:0D80 size 041E, and all 15 ordered relocation
sites, while all previously exact owners and DOS probes remained passing.

First no-candidate default aggregate:

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-kotohime-exatt-default-p01-20261008

Receipt:

    .analysis/th03-main-exact/gpt-web-kotohime-exatt-default-p01-20261008/receipt.json

The local exact aggregate increases to 300 functions / 46680 function bytes
and 47603 owned bytes, across 68 exact CODE extents and 61 maintained
semantic source owners. Two fresh cold builds produce 20 product outputs,
384 game objects and 450 generated OMF objects. Four reviewed P_EXATT_TEXT
character owners remain non-exact: Marisa, Kana, Ellen and Chiyuri.
Ellen's complete five-function 1078-byte TC4 source shape is already proven,
including its 470-byte update, but it must not be promoted before the
intervening physical objects and original ordered relocations are resolved.
Historical physical DATA/BSS producer identity, whole-game closure and
Factory Truth Kernel acceptance remain open.

Final default aggregate after source, evidence and ledger updates:

    python3 scripts/replay_th03_main_exact_units.py --run-id gpt-web-kotohime-exatt-default-final-p02-20261008

Receipt: .analysis/th03-main-exact/gpt-web-kotohime-exatt-default-final-p02-20261008/receipt.json

Both cold compilations and links continue to pass exact bytes, MAP and all
15 ordered Kotohime relocation sites alongside previously accepted owners
and the DOS probe. The available CI post-unittest gates pass at
.analysis/th03-kotohime-exatt-postgates-20261008.log, including Ghidra and
Oracle negative controls. Full CI remains blocked by the missing unicorn
host module (632 tests, 125 import errors and 167 skips), recorded at
.analysis/th03-kotohime-exatt-ci-20261008.log. Do not report full CI PASS.
