# TH03 MAIN HitCircle update: explicit SI record pointer

`hitcircles_update()` now declares its six-byte record cursor as a register
near pointer:

```cpp
register HitCircle near* p = hitcircles;
int i;
```

The target's 38-byte update function loads the first record address into SI,
keeps the thirteen-record signed loop count in AX, tests the byte age at
`[SI]`, increments/clears it, then advances SI by six bytes per record. The
explicit register pointer records the recovered SI allocation without
changing the signed index or the paired `(++i, ++p)` loop-header ordering.

Stage `af1027f` rebuilt the complete `hitcirc` owner in two independent
original Turbo C++ 4.02 rounds. All 445 CODE bytes, 30 ordered native fields
and four PUBLIC offsets match. Both normal MAIN links reproduce the original
Japanese loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1027f/report.json`

SHA-256: `f30f312eaea6842d320320627c28156e3a07f4b9e7f4ddc22171167dbdda8eb9`

## Additional `HitCircle::cel()` type experiments

The renderer's inline cel calculation was inspected directly in the target
object. It zero-extends the byte age, decrements the word, shifts right by two,
multiplies by two, then performs three additions before adding the sprite
base. Three natural unsigned-source attempts were compiled and rejected:

- `af1027c`: `register unsigned int cel`, sequential `/ 4` and `* 2`; 447 CODE
  bytes rather than the original 445.
- `af1027d`: ordinary `unsigned int cel` with `>>= 2`; 443 CODE bytes.
- `af1027e`: a direct unsigned expression for `(age - 1) / 4 * 6`; 413 CODE
  bytes.

All three experiments were reverted. The explicit BX expression remains;
none of these C++ locals reproduces the original native register traffic.
