# Kotohime BOSS: native radial indexing and ring phase gates

`src/main/boss/kotohime.cpp` now expresses the three expanding ring
variants with the live radius on the left of the threshold check, and
the first-frame and intro transitions with the live frame on the left.
The pellet-arc shot clock compares the unsigned-word modulo directly to
its phase, while the signed `randomize_angle` parameter explicitly tests
nonzero before drawing one RNG word per randomized projectile.

More importantly, the nested radial burst now calculates `center_i * 256`,
`bullet_i * 128` and `bullet_i * 0x30` before each original 16-bit signed
division. The resulting center angles are converted to bytes only after
division. The two nested `register int` loops, individual `polar()` calls,
RNG and bullet-add ordering, and positive expanded-radius branch remain
unchanged. This is an exact representation of the original speed and angle
stepping, not a floating-point approximation.

Positive trials `af1319a` (radius and intro guards), `af1319b` (radial
product order) and `af1319d` (ring initialization, random selector and arc
clock) all matched the entire physical BOSS object and original MAIN link.
Final live-source stage `af1319e` reproduced **1,840 CODE bytes, 262 ordered
native fields and 11 PUBLICs** in two independent TC4/TLINK rounds. A joint
`af1319f` recompiled Kotohime and its Bullet engine caller/consumer scope:
**4,525 CODE bytes, 458 ordered fields and 31 PUBLICs** also matched both
complete Japanese MAIN links and ordered MZ relocations.

Negative trial `af1319c` inverted the random ring's expanded-radius branch
into an early return. It did not change the byte count or fixup count but
changed the `JLE` into `JG` and moved the sine-motion path before the
warning-render work. The original branch layout was restored.

Revalidate only the current Kotohime object:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1319e
```
