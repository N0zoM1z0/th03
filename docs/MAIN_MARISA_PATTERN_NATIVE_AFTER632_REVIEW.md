# Marisa full BOSS: original-native C++ volley periods and attack modes

Marisa's complete original 16-bit BOSS source contains nine functions:
the full `gba_boss_update_marisa` scheduler, four attack routines,
intro/rendering routines and template initialization. This recovery
makes its four distinct pattern families and their timing readable
without changing the original machine code or RNG sequence.

The large attack dispatch now names the 18 shared scheduler values
as Marisa-specific spread, wide-column, narrow-column and ring
patterns. The wide-column attack explicitly has four emissions and
finishes at frame 0x84; the narrow-column attack has three emissions
and finishes at 0x70. Their first three volley times are common
(0x40/0x50/0x60), and both begin after 0x38. The ring fires once every
32 frames until 0x82; its low/high boss-level pellet/bullet distinction
remains unchanged.

Two real *natural C++ arithmetic* improvements were separately
compiled from changed source: `boss_frame % 0x20 == 0` in the ring
and `boss_frame % 4 != 0` in the spread. Turbo C++ 4.02 lowers the
power-of-two unsigned modulo to the original bit-mask instructions.
The two source- and OMF-dependency-bound native controls `af632a`
and `af632b` each reproduced the full original BOSS object.

The final mode/phase-enum version `af632c` also passes two independent
original Turbo C++ compile and TLINK rounds:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af632c --units ba_maris
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af632c

**1,431 original CODE bytes, 199 ordered native FIXUPP fields, nine
PUBLIC symbols**, all OMF segment definitions, both complete normal
MAIN EXEs and path-normalized MAPs match original. The Japanese
program image, its 1,553 ordered MZ relocation vector and separately
serialized complete original 130,882-byte MAIN.EXE are exact.

Retained receipt:
`.analysis/work/exatt-layout-af632c/report.json`,
SHA-256 `2e45a7c582e0d8216f8b60a6161733fcbdf51ac63ac68340dcf51771c75031ca`.
Both writer rounds and real changed-source input are preserved. Only
this affected original OBJ slot was recompiled; no full cold replay.

This is maintainable source recovery and native exactness for already
tracked bytes. It does not assert historic Borland raw OMF packet
identity, new canonical packed-file Factory credit, or device runtime.
