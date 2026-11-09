# Kana Chargeshot/Gauge: native pointer progression and byte cadence

In the complete `cs_kana` owner, all four trail-group traversals and
four-sprite render pass now use natural near-pointer prefix increments.
The initial angle assignment still walks the four 54-byte records in
reverse, but each step can likewise use `--p`. The byte-valued Gauge
volley interval accepts a natural zero-remainder predicate without moving
the symmetric bullet/sound events.

Original TC4/TLINK `af1141f` matches the entire 1,291-byte CODE owner,
117 ordered native fields, nine PUBLICs, full Japanese MAIN image and
relocations in two independently compiled rounds.

Two fresh negative controls distinguish source-equivalent but non-native
spellings: replacing the inclusive thirteen-point history bound with an
exclusive `i < KANA_CHARGE_SAMPLES` (`af1141c`) changed CODE, as did
narrowing the reverse-history loop's signed index (`af1141e`). Preserve
both original expressions in the update/hittest loops.
