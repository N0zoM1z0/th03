# MAIN large enemy control via one natural C++ source (after572)

The original source-backed MAIN cold tree already compiled four physically
separate 16-bit enemy producer objects. Their original staged compiler sources
were repeated, flattened copies of a 1,030-line natural C++ implementation.
This stage adds four very small, first-use compiler translation units that
each define the original partition macros and include the *same* maintained
src/main/enemy/enemy.cpp file, without copying or changing its function
implementations, historical unchecked behavior or source acceptance guards:

| Original source slot | New C++ translation unit | Original CODE | PUBLIC functions | Ordered native fixups |
| --- | --- | ---: | ---: | ---: |
| eforna.cpp | src/main/enemy/producers/eforna.cpp | 729 | 8 | 58 |
| efornb.cpp | src/main/enemy/producers/efornb.cpp | 1,064 | 4 | 37 |
| eupda.cpp | src/main/enemy/producers/eupda.cpp | 372 | 3 | 24 |
| eupdb.cpp | src/main/enemy/producers/eupdb.cpp | 1,160 | 4 | 103 |
| **Four source-backed objects** | **One shared implementation** | **3,325** | **19** | **222** |

The shared implementation contains two particularly large and behaviorally
important non-leaf functions: **enemy_run (867 bytes)** interprets formation
scripts, movement patterns, waits, clipping and spawning, while
**enemy_hittest (848 bytes)** handles multi-entity collision processing.
The four producer objects also include smaller leaf and orchestration
functions. The original C++ keeps the existing landmines (including the
uninitialized previous-formation byte) and original 16-bit widths rather
than adding defensive or behavior-altering fixes.

## Actual native compiler and complete link

Two rounds of genuine Turbo C++ 4.02 compilation used the original flags
-O -b- -3 -Z -d -DGAME=3 -ml -DBINARY='M', with a *new, independent source
wrapper materialization in each round*. Every one of the eight resulting
objects has the complete original initialized CODE payload, all original
ordered OMF literal FIXUPP fields, PUBLIC names/offsets and segment geometry.

The OMF THEADR/COMENT/LNAMES dependency bookkeeping differs because the
maintained common C++ file is now included rather than copied into four
separate giant translation units. Full raw OMF packet identity and
historical compiler/source filename provenance are not claimed.

Each round then replaces **all four enemy objects simultaneously** in the
already verified source-native after567 MAIN link. That existing full link
also contains the nine large BOSS objects and natural TASM keyboard
scanner. Both normal TLINK runs emitted an *identical complete 132,322-byte*
source-native MAIN EXE and unchanged original MAP layout after normalizing
only the four compiler-source diagnostic paths. All **124,642 original
program bytes and 1,553 original ordered MZ relocations** remain equal.

Using the separately proven standard DOS MZ compact serializer (which does
not receive Japanese target bytes), both output files then reproduce the
**entire original 130,882-byte Japanese MAIN.EXE exactly**. This post-link
format step is explicitly separate from compiler/linker source provenance.

Driver: scripts/build_th03_main_enemy_four_after572_work.py
Native report: .analysis/work/main-enemy-four-after572-native-build.json
Read-only reviewer: scripts/review_th03_main_enemy_four_after572_work.py

    DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
      .venv/bin/python scripts/review_th03_main_enemy_four_after572_work.py

Both source C++ wrapper sets, eight compiled OMF files, two complete EXE/MAP
pairs, compact MZ results, ten writer logs and original source pin hashes
are retained; no 99-object cold replay or old receipt modification occurred.

These 19 functions were **already represented in the historical authored
function ledger**. This is an improved maintained source producer and
simultaneous native-link reproducibility proof, not an increase to the
canonical function denominator, whole-game source ownership or Factory
acceptance. Original Japanese target provenance remains
candidate-local-attested.
