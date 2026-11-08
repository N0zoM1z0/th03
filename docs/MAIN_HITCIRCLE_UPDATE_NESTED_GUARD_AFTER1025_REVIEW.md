# TH03 MAIN HitCircle update: nested active-record guard

`hitcircles_update()` now keeps the age increment and expiration test inside
one positive active-record guard:

```cpp
if(p->age) {
    p->age++;
    if(HITCIRCLE_FRAMES < p->age) {
        p->age = 0;
    }
}
```

This replaces the zero-age `continue` with the direct record-state condition.
The signed thirteen-record index and near-pointer increments remain in the
original `for` header; byte age increment and the strict frame-expiration
comparison remain unchanged.

The complete `hitcirc` physical object is source-bound to `af1025d`. Two
independent original Turbo C++ 4.02 rounds reproduce all 445 CODE bytes, 30
ordered native fields and four PUBLIC offsets. Both normal MAIN links
reproduce the original Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1025d/report.json`

SHA-256: `6f687da2688a861ee63e1943b7eb362691a48bd2f4665410075afe1f122809e6`

## Additional `HitCircle::cel()` leaf probes

Two more natural-local variants were tested against the complete `hitcirc`
object after this update:

- `af1025e`: a sequential `register int cel` local for `(age - 1)`, `/ 4`,
  `* 2`, then three additions. The complete CODE payload differed.
- `af1025f`: the same sequential arithmetic with an ordinary signed `int`
  local. The complete CODE payload differed.

Both experiments were reverted. The existing explicit `_BX` sequence remains
in the source; neither local-variable form is a valid native replacement. The
leaf is still open for further disassembly-led exploration, not considered
semantically finished merely because its current bytes are exact.
