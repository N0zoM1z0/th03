# Eight more large MAIN boss C++ producers — corrected native packing probes

The current MAIN cold build compiles the full game boss TUs with TC4J
-O -b- -3 -Z -d -DGAME=3 -ml, **without** a global -a2 option.
Eight previous probing scripts used a contradictory global -a2 option,
even though local source struct-packing pragmas are separately maintained
in the actual product C++.

The spurious option was removed from seven unbound boss probes. The old
Marisa probe is an explicit historical input of OP, MAINL and ZUN cold
recipes, so its bytes were preserved exactly. A new independent
scripts/probe_th03_main_boss_marisa_native_corrected.py is used for
Marisa instead. No game product C++ or frozen dependency was modified. Each
affected **full translation unit** was then freshly compiled against
the pinned Japanese target and the actual retained native source object.
The entire OMF stream matches the current native object after narrowly
normalizing original dependency timestamps; all complete function shapes,
switch entries and PUBLICs also pass their per-game checks:

| Boss | Original CODE allocation | Complete functions | Inline switch bytes |
| --- | ---: | ---: | ---: |
| Yumemi | 2,358 | 10 | 80 |
| Kana | 1,874 | 9 | 80 |
| Mima | 1,922 | 9 | 81 |
| Reimu | 2,020 | 9 | 72 |
| Kotohime | 1,840 | 11 | 80 |
| Ellen | 1,675 | 9 | 81 |
| Rikako | 1,677 | 8 | 81 |
| Marisa | 1,431 | 9 | 81 |
| **Eight large modules** | **14,797** | **74** | **636** |

The preceding after559 Chiyuri boss also passed with the corrected flags:
**2,654 CODE bytes, 11 functions and an 81-byte switch table**.
Thus all nine individual boss modules total **17,451 original CODE bytes**
and **85 procedures**. These are large non-leaf logic bodies, not tiny
helpers. The numbers describe the nine already-maintained producers;
they do not imply that 85 new functions were added to the whole-game ledger.

First-round receipts for Yumemi, Kana, Mima, Reimu, Kotohime, Ellen and
Rikako are in their corresponding .analysis/th03-main-boss-*-cpp trees
under 560-native-r1 IDs. Marisa has an independent corrected-source receipt
at .analysis/th03-main-boss-marisa-cpp/gptweb-marisa-560-scoped-native-r1.
The initial exploratory checks and wrong-flag evidence are retained in
.analysis/work/probe/boss-packing560 and their original work directories.
The original acceptance status for OP, MAINL and ZUN was revalidated after
the history-bound Marisa script was restored; no prior proof input was
silently repinned.

**Important acceptance boundary:** This stage proves complete local
compiler-object identity after timestamp normalization, **not** yet a
simultaneous replacement link of all eight modules; that requires a
separate explicit normal TLINK comparison. MAIN's previously documented
header and EC2D load-image differences remain open. This is not a
canonical Factory or whole-game completion credit.
