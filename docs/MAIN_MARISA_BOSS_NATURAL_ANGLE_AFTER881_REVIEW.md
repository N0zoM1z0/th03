# TH03 MAIN after881 — complete Marisa major BOSS and native byte-angle assignment

The whole original **nine-function `ba_maris`** Turbo C++ 4.02 physical
source owns Marisa's BOSS template, 4-frame symmetric spread, separate
wide/narrow paired-column Extra Attacks, 32-frame ring volleys, complete
update/collision scheduler, two-sided masked sprite intro and the full
render dispatcher. No BOSS-specific DAT/DGROUP fields were reallocated.

The unsigned 16-bit `boss_frame` gate now uses the natural nonzero
remainder `if(boss_frame % MARISA_SPREAD_PERIOD)` and the ring volley
uses `if(!(boss_frame % MARISA_RING_PERIOD))`. The important new
**actual compiler result** overturns a too-broad reading of an earlier
failed enum trial: the mutable byte `marisa_bullet_angle += 7` can be
naturally written as

```
marisa_bullet_angle = marisa_bullet_angle + MARISA_SPREAD_ANGLE_STEP;
```

with the original step named as `7` **without changing any original
TC4 instructions**. Earlier `angle += enum` changed AL/memory
selection, but an ordinary C++ byte assignment with an explicit binary
addition **does** match the native object. Separate trials with and
without `static_cast<unsigned char>` both reproduced the target.

The original 56×56 collision tiles, 32-pixel hit radius, normal 176×96
sprite, 48×80 damage overlay, signed screen offsets and three original
GRCG mask words (0xAAAA, 0x5555, 0xFFFF) now have named C++ values.
This retains the actual separate near/far sprite masks and the
original signed integer `256 / marisa_ring_count` before the byte-angle
increment, without changing projectile RNG draws or attack order.

## Independent original compiler trials

- `af881a/b`: natural unsigned-word spread and ring zero/nonzero
  remainder checks each matched the entire original BOSS twice.
- `af881c`: swapped operand order in the ring frame cutoff; native
  original CODE remained exact, although the readable original order
  was retained for the final source.
- `af881d`: named physical collision, sprite and masked intro geometry;
  all 1,431 original CODE bytes and full normal MAIN remained exact.
- `af881e`: mutable byte `angle = static_cast<unsigned char>(angle+7)`
  passed actual original TC4 and full MAIN twice.
- `af881f`: ordinary `angle = angle+7` also passed twice.
- `af881g`: ordinary `angle = angle+MARISA_SPREAD_ANGLE_STEP` passed
  twice, a genuinely different result from earlier failed
  `angle += ENUM` codegen.
- `af881h`: explicitly promoting `MARISA_RING_FULL_TURN` to **unsigned
  int** before division by the byte ring count changed original CODE
  at segment 4 offset 394. The original *signed 16-bit integer
  division* was restored. No assumption that unsigned is equivalent.
- Final `af881i`: full current source with accepted natural byte
  assignment and physical geometry, two original compiler and complete
  normal MAIN TLINK rounds byte exact.

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/probe_th03_main_exatt_layout.py --stage af881i --units ba_maris
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af881i
```

Both genuine original Turbo C++ 4.02 and complete normal MAIN TLINK
rounds match **all 1,431 CODE bytes, 199 literal ordered native OMF
FIXUPP fields, 9 PUBLIC offsets**, original physical segment/ABI and
compiler source dependencies, both normal MAIN EXE/MAP, **124,642
Japanese loaded program bytes** and **all 1,553 original ordered MZ
relocations**. Independently checked standard MZ serialization also
recreates the **130,882-byte original Japanese MAIN.EXE**; the
historical vendor header serializer remains unproved. **98 unchanged
original game objects and CRT reused**, no cold replay or target/OBJ
patching, synthetic machine-code buffer or NOP padding.

Protected real original source/compiler/OBJ/EXE/MAP native report:
`.analysis/work/exatt-layout-af881i/report.json`, SHA-256
`79d2a25b4e02b16b4157741f068b1624ef9cc6109ceb75b286b63c9489279984`.
These original CODE bytes had prior source-native coverage. This is
improved maintainable C++ and original compiler understanding, **not
additional distinct game CODE ownership, vendor raw OMF packet identity
or canonical Factory packed-game acceptance**.
