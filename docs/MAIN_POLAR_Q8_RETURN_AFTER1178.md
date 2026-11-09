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
