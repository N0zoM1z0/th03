# Player loss and defeat banner: natural source without changing bytes

The complete original `lose` owner contains loss countdown/state updates,
polar particle placement, three loss rings, and the defeated/winner banner.
The countdown and palette timing now use named source constants, the
particle X/Y coordinates initialize at their first use, and the banner
frame remainder initializes after its fixed defeated-player tiles. All
sprite/banner positions and bounce values are named compile-time geometry.

The original TC4/TLINK `af1163i` report matches all 664 CODE bytes,
61 ordered native fields, four PUBLICs, and the Japanese MAIN image and
ordered relocations in both independent rounds.

An initial all-constants trial (`af1163a`) differed. A separate `af1163f`
experiment identified the byte shake mask/cadence spelling as codegen-
sensitive. Preserve the original `(lose_anim_time & 3) < 2` rather than
substituting enum-valued byte terms. Numeric effects alone do not prove
that TC4 emits the same instructions.
