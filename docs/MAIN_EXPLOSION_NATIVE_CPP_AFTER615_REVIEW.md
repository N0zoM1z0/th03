# Explosion collision BOSS-sized function: source-bound native C++ (after615)

The complete `explosions_hittest()` producer owns 630 original CODE bytes
and all its collision iteration, chain hit accounting, score/charge bonus
calculations and fireball spawning. Its prior `chain_hits_inc_and_clamp`
macro was not a real returning function: the assignment expression before
`if` provided the value and a later expansion updated the chain count.
The source now spells the **saturating byte counter** directly as a read,
conditional increment below 255, and a write.

The original `pellet_and_fireball_val` and
`pellet_and_fireball_value_p` preprocessor aliases hid two distinct uses
of a **single** physical local byte and local near pointer. They are now
natural C++ assignments without a macro alias, retaining the reused stack
slots required for exact 16-bit code generation. The overlapping
`Subpixel radius/size` union now uses a single `extent` object, first
a radius and then doubled to diameter. The `against2` byte no longer
needs an extra single-byte enum/byte union.

The earlier v1 compiler overlay mistakenly compiled the unchanged
`TH03WORK/src` original. This result was **rebuilt with the corrected v2
explicit source path** and checked against actual Borland OMF COMENT
dependencies. The deliberately bad test field `chains.hitsue` failed
compilation in `af611a` after the driver was corrected. Adding extra
distinct locals in a separate negative experiment increased the stack
frame to 18 bytes and CODE to 634; this non-equal variant was not kept.

The accepted natural-source candidate incrementally passed genuine TC4:
`af611d` (saturating counter), `af611e` (macro aliases),
`af611f` (byte mode) and `af611g` (single extent), all using
forced compiler include paths. The read-only v2 reviewer checks the
retained writer logs, two native object/link rounds, full original CODE,
49 literal ordered native relocation fields, one PUBLIC symbol and
the original segment definitions:

    PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py \
      --stage af611g

Both normal MAIN EXEs and normalized MAPs equal the retained after596
complete source-native link; the 1,553 original ordered relocations and
the separate complete Japanese MAIN MZ serialization match the pinned
Japanese target. Full receipt and raw native outputs:
`.analysis/work/exatt-layout-af611g/report.json`, SHA-256
`9d3e3a9989ccc347ab6a608dcef1826f7051845d83c1d351923306ee2f72810e`.

This recovers cleaner natural C++ inside a substantial collision/chain
function. It does not re-credit previously maintained bytes or claim
original vendor packet identity, physical gameplay execution, or whole
packed-product Factory acceptance.
