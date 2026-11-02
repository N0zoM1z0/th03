# One exact Japanese MAINL link with xx and seven source CRT modules

The native BCC 4.5 source at `src/mainl/crt/xx.cpp` and seven real
TASM CRT source files have now been combined in **the same 893-member
library** and normal MAINL link,not merely proven in eight separate
unit comparisons. This is the current `build_th03_mainl_xx_crt_combo_work.py`
scoped source-only carrier:it reuses two independent already-verified
compiler/assembler object pairs and performs two fresh TLIB/TLINK rounds.

| Source member | Original CRT member index | Exact CODE segment bytes |
| --- | ---: | ---: |
| memchr | 259 | 37 |
| memcmp | 260 | 40 |
| memcpy | 261 | 36 |
| memset (setmem + memset) | 263 | 72 |
| strchr | 291 | 63 |
| strcmp | 292 | 48 |
| strlen | 300 | 33 |
| xx (complete exception/RTTI TU) | 338 | 12,622 |
| **Total** | **8 source members** | **12,951** |

The `xx` member preserves every one of its 12,622 raw CODE bytes and all
187 original literal ordered OMF fixups,18 DATA bytes,10 BSS bytes and
its original 50 function bodies plus compiler-generated inline metadata.
Each of the seven other modules preserves its entire original native CODE,
public entry points,zero relocation fields and original CODE/DATA/BSS group
geometry. All **885 other original library member program records** remain
untouched,including the prior accepted source CRT members. The original
36 MAINL project objects and startup/EMU/MATHL inputs also remain unchanged.

Both independent combined TLIB/TLINK rounds reproduce the **entire original
67,372-byte Japanese decoded MAINL EXE byte-for-byte**,the complete
original MAP and all **677 ordered MZ relocations**. These are actual
native library operations,not recomposed CODE arrays or object patches.
The retained original cold pair,target,accepted28-provider CRT library
and existing211-owner accepted publication are not altered;no cold/DIET
replay or ancestor runtime chain is executed.

This establishes exact **simultaneous source-only native reconstruction of
12,951 original CODE-segment bytes**. It does **not** publish those bytes
to the formal accepted ledger;current review receipts continue to report
`source_acceptance=false` and `added_accepted_bytes=0`. Future formal
promotion must separately follow the repository's acceptance and ownership
rules;the whole-game source denominator is still unknown.

Scoped reproduction:

    PYTHONPATH=scripts .venv/bin/python scripts/build_th03_mainl_xx_crt_combo_work.py
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_mainl_xx_crt_combo_work.py
    PYTHONPATH=scripts .venv/bin/python -m unittest tests.test_mainl_xx_crt_combo_work

Retain `.analysis/work/mainl-xx-crt8-{build,review}.json`,two complete
`xx-crt8-roundN-{combined.lib,linked.exe,linked.map}` native raw vectors,
real TLIB/TLINK response files and phase logs,and both independent
source-compiler receipts. No full cold replay is required.
