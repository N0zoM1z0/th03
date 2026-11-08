# TH03 MAIN shared BOSS explosion ring: natural loops and typed arithmetic

This pass continues the complete 348-byte near-Pascal
`boss_explosion_ring(int x, int y, int length)` in the separate original
`ba_sring` physical object. The companion `ba_srest` object was rebuilt
alongside it because both wrappers consume the same maintained
`src/main/boss/shared.cpp`.

## Natural C++ recovery

The primary 16-sprite and secondary 8-sprite manual `while` loops are now
natural `for` headers. Each header keeps the original post-draw update order:
first the signed index, then the byte angle:

```cpp
for(i = 0; i < BOSS_RING_PRIMARY_SPRITES;
    ++i, angle += BOSS_RING_PRIMARY_ANGLE_STEP) {
    // two polar coordinates and one sprite draw
}

for(i = 0; i < BOSS_RING_SECONDARY_SPRITES;
    ++i, angle += BOSS_RING_SECONDARY_ANGLE_STEP) {
    // double-radius polar coordinates and one sprite draw
}
```

Both X/Y pairs now use the natural negative half-sprite origin plus `polar()`.
The 16-bit Y conversion uses base-first `PLAYFIELD_TOP + (y >> 4)`.

The original `length *= 8` is now named
`length *= BOSS_RING_LENGTH_SCALE`. The secondary radius uses
`BOSS_RING_SECONDARY_RADIUS_SCALE * length`, with both factors named in the
shared compile-time limits. The primary angle narrowing and secondary
zero-minus byte wrap are expressed as explicit C++ casts:

```cpp
angle = static_cast<unsigned char>(length);
angle = static_cast<unsigned char>(
    0 - static_cast<unsigned char>(length)
);
```

The local angle is register-qualified. The start-sound, PID clip and finish
radius predicates now use constant-first comparisons.

## Negative controls and retained lifetimes

The following candidates were independently compiled and rejected:

- `length = length * BOSS_RING_LENGTH_SCALE` changes the complete `ba_sring`
  CODE; retain compound `length *= BOSS_RING_LENGTH_SCALE`.
- `register screen_x_t left` changes complete `ba_sring` CODE; keep ordinary
  `left`.
- `register screen_y_t top` also changes complete `ba_sring` CODE; keep
  ordinary `top`.
- Unary minus remains rejected for the secondary byte angle; the explicit
  zero-minus followed by byte truncation is retained.

The `register unsigned char angle` local is exact. The sprite draw count,
polar call order, angle increments, sound, clip selection, reward and return
values remain unchanged.

## Complete shared-owner verification

Stage `af1045r` rebuilt both separate shared physical objects in two
independent original Turbo C++ 4.02 rounds:

| Physical object | CODE | Ordered native fields | PUBLICs |
| --- | ---: | ---: | ---: |
| `ba_sring` | 348 | 22 | 1 |
| `ba_srest` | 601 | 84 | 7 |
| **Total** | **949** | **106** | **8** |

Both normal Japanese MAIN links reproduce the original loaded image and
ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1045r/report.json`

SHA-256: `e13a892a376ad5e29055c6364dbd21cbce8d6d0873cc2f3ba958b0a618c81b33`
