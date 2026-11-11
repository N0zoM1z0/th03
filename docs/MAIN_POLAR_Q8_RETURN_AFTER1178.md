# Polar geometry: exact implicit 16-bit return

The complete `polar` far-`__cdecl` leaf can return the widened Q8 sum
naturally without an explicit `static_cast<int>`. The original 16-bit return
ABI performs that truncation, and the signed 32-bit multiplication and
arithmetic `>> 8` are unchanged. Replacing the shift with signed `/256`
would be incorrect for negative products: division truncates toward zero,
while the target's arithmetic shift rounds down.

The original TC4/TLINK stage `af1178a` matches all 26 CODE bytes, zero OMF
fixups, the PUBLIC and the Japanese MAIN image/relocations in two independent
rounds. This is the exact low-level polar routine used throughout the BOSS,
Chargeshot and projectile geometry.

## Direct 32-bit product remains compiler-visible (2026-11-11)

Two genuine TC4 trials checked whether the existing direct
`center + ((long(radius) * ratio) >> 8)` expression could name its
signed widened intermediate. A `const long signed_product` local
(`af1356i`) and a `register long signed_product` local (`af1356j`)
both emitted **31 instead of the original 26 CODE bytes**. Both were
rejected; the maintained `polar.cpp` still expresses the product and
arithmetic Q8 shift directly, before 16-bit return truncation.
The unchanged leaf was jointly recompiled with Gauge, shared Extra
Attack, Marisa BOSS and Bullet at `af1356m`, reproducing the original
normal MAIN image and ordered relocations without a full cold replay.
