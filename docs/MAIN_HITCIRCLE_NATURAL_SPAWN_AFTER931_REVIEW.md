# TH03 MAIN HitCircle: direct typed spawn coordinates

The original enemy and player HitCircle spawn sites now use explicit C++
`HitCircle::topleft` coordinate assignments instead of the statement macro
`hitcircle_set_topleft`. Both sites retain the same PC-98 playfield X
conversion and the original Y top margin and half-sprite offsets. They use
the real near `HitCircle` record, not an emulated register or byte array.

The genuine `af931b` native TC4 experiment compiled the **whole** original
`hitcirc` object twice and successfully re-linked the normal MAIN twice.
**445 original CODE bytes**, 30 literal ordered OMF FIXUPP fields and all
four PUBLICs match; the complete 124,642-byte Japanese program image,
normal MAP and all 1,553 ordered MZ relocations match. The other 98
original physical game objects and CRT were reused, without cold replay.
Native report: `.analysis/work/exatt-layout-af931b/report.json`, SHA-256
`b45ab57e8467c700c2c03f4840e5f82488d02438dd60ed13116af363bde74243`.

A failed `af931a` experiment instead encapsulated the same assignments in
an in-class `HitCircle::set_topleft()` method. TC4 unexpectedly changed the
original function prologue/register allocation, producing 468 rather than
445 CODE bytes. Keep the source-level direct stores, not the unverified
method extraction. This is maintainable source recovery of already-covered
CODE, not new distinct game bytes or canonical Factory acceptance.
