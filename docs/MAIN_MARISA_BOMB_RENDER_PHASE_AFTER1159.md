# Marisa Bomb: native sprite-phase early exit and geometry

The complete original Bomb controller now exits immediately after restoring
EGC if the frame is outside the sprite-rendering phase. Its charged 48×48
sprite offset initializes at first use after that guard, while the GRCG
palette flash, frame-period explosions, random X/Y and hardware BX and MRS
calls remain in source order. The sprite center, animation offset and fade
rate have compile-time names; byte-page selection uses natural truthiness.

The two original TC4/TLINK rounds at `af1159d` matched all 449 CODE bytes,
50 ordered native fields and the complete Japanese MAIN image and ordered
relocations. This is a complete physical-owner comparison, not an extracted
snippet. The byte-valued shake masks and explicit widened sound parity test
are preserved because their original compiler lowering remains important.
