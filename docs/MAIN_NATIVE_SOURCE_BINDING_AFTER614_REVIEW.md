# Source binding audit: after614 verified Turbo C++ inputs

**2026-11-07 — correction to stages after598–610.** The earlier
`probe_th03_main_exatt_layout.py` copied modified source to
`TH03WORK/probe/af.../rN/src/...` while writing wrapper directives of the
form `#include "src/main/...cpp"`. Turbo C++ 4.02 resolved the directive
against the older `TH03WORK/src/...` first. The compiler's own OMF `COMENT`
dependency records say `src/main/...cpp`, *not* the copied overlay.
Consequently, previous after598–610 source-refresh records that reported
exact CODE/MAP and whole MAIN are **not evidence that the changed source was
compiled**. The old compiler output/receipts are retained as historical
controls, not erased, repinned or relabelled as current-source proof.

## Proven new compiler binding

The v2 native driver makes the include path **explicit** in the actual
wrapper: `#include "probe/<stage>/rN/src/...cpp"`. For the 32-byte
Extra Attack entity view it also binds the nested include to the copied
header in the same stage. A successful native compile is only accepted if
the *emitted OMF dependency records* contain the exact staged C++ source
and, when applicable, the staged shared header. The independent read-only
reviewer checks both recorded dependency paths and all consumed bytes; it
rejects old v1 receipts rather than quietly giving them current credit.

A negative control `af611a` deliberately retained an invalid
`chains.hitsue` field in modified Explosion C++; the original v1 compiler
had silently accepted that typo, while the corrected Turbo C++ 4.02 command
correctly rejected the new source at line 106. The unmodified original
Explosion and Bullet TUs passed the forced-source baseline controls
`af611c` and `af611i`. Exactness now requires complete raw source-produced
CODE/DATA, ordered FIXUPPs, PUBLIC offsets, segment definitions and both
original MAIN EXE/MAP links, *not just a copied snapshot plus a match*.

## Confirmed new-source Extra Attack integration

The shared Extra Attack `exatt_entity_t` includes character-specific
sub-byte and union views. Turbo C++ with default `-a2` inserts alignment
padding into nested union fields, causing all four source compile-time
size/offset assertions to fail (`af613a`). Applying byte packing **only
around the struct definition**, then restoring `-a2`, makes the original
32-byte entity/field offsets compile correctly (`af613c`).

The earlier natural-C++ Chiyuri Extra Attack branch and AX beam phase
changes, although semantic alternatives, differ from original machine code
(`af613f`, `af613g`). The exact original source forms are restored, keeping
the shared entity layout. The complete corrected **ten** Extra Attack TUs
were then rebuilt from their *actual staged sources*, two independent native
TC4/TLINK rounds, replacing all ten project OBJ slots simultaneously:

    PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py \
      --stage af614a \
      --units ex_yume,ex_mima,ex_rika,ex_rfly,ex_reup,ex_ellen,ex_koto,ex_chyu,ex_maris,ex_kana
    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af614a

Both rounds pass **8,781 CODE bytes, 563 original ordered native fields,
52 PUBLICs**, all segments and the full normal MAIN EXE/MAP, Japanese
124,642-byte program image and 1,553 ordered relocations. Standard DOS MZ
serialization gives the 130,882-byte Japanese MAIN.EXE. The complete native
v2 evidence with both outputs/writer logs and OMF dependency checks is at
`.analysis/work/exatt-layout-af614a/report.json`, SHA-256
`bb4c87b7837dd1322632cb3c90988be37e142c3686abb0dc89aff234eedfa746`.

This establishes the current natural shared 32-byte ABI source, not the
historical vendor raw OMF packet format or canonical packed-file Factory
acceptance. Previously reviewed original CODE bytes are **not recredited**.
The BOSS family and other v1 source refreshes need their own v2 reanalysis;
failed variants should be restored or documented, never claimed exact.
