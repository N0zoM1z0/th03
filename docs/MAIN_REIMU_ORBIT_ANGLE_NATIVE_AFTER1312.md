# Reimu BOSS: original radial division and byte-angle code generation

The three full radial distributions of `reimu_pattern_orbit_burst()` in
`src/main/boss/reimu.cpp` now compute their angle with the natural signed
`(i * 256) / reimu_orbit_count` followed by byte-angle addition. The
signed 16-bit product and division happen **before** truncation to the
native eight-bit angle; this matters for radial ordering and overflow.
The old `i << 8` shorthand produced the same original TC4 instructions.
The radial phase's two byte-angle advances are now compound `+=`, also
native-exact at both sites. The Reimu cloud similarly uses compound byte
angle adjustments for its opposite and signed negative quarter-turn, and
a named factor of two for the two projectile-angle expressions.

Independent positive experiments `af1312a` (three signed radial products),
`af1312b` (two phase-angle increments), `af1312c` (opposite-angle advance),
`af1312d` (negative quarter-turn advance), and `af1312g` (two projectile
angle multiplications) each compiled the entire 2,020-byte Reimu BOSS
object in two original TC4 rounds. The complete ordered native fields,
PUBLIC offsets, segments, normal MAIN links and original Japanese image
and ordered relocations passed. Current source binding: `af1312g`.

A negative original TC4 trial `af1312e` confirmed why the signed-looking
unary expression `angle = -angle` must **not** replace the existing
`angle = 0 - angle`. TC4 selected `NEG AL` instead of the original
`MOV AL,0; SUB AL,[byte local]`, shrinking the physical owner by two bytes
and shifting the subsequent offsets. It was reverted; no target padding
was added. This is a compiler-sensitive source distinction, not permission
to alter the original byte-angle behavior.

Recheck without a cold build:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1312g
```

The scope proves the full physical Reimu owner with the unchanged frozen
normal-link parent, not complete game source or Factory packed-file acceptance.
