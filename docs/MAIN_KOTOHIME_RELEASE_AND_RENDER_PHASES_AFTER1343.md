# Kotohime BOSS: original release timing, nested radial bursts and render gates

The complete `src/main/boss/kotohime.cpp` now expresses the last release
clock of the **randomized ring, two aimed rings, and nested radial burst**
through separate positive `boss_render_frame > KOTOHIME_RING_RELEASE_AFTER`
branches. During the warning period, the original sprite animation and
byte phase adjustments continue; each ring emits only after the inclusive
warning deadline. The random ring's gated RNG draws, aimed fast/slow pair
and the radial `O(orbit_count * burst_count)` nested 16-bit signed
multiplication, division, `polar()` offsets and launch order are unchanged.

The five-position pellet arc now resets the BOSS mode only once its
original `0x60` frame has been reached, **after** any arc emission on that
frame. The arrival renderer preserves its separate odd-global-frame and
intro clock guards; warning-ring flicker requires both warning render
mode and the original four-frame low-bit phase. The normal main sprite
renderer positively selects non-normal render modes for the original
near-Pascal ring function. There are no new RNG samples, safety checks,
collision calls or gameplay mechanics.

Incremental original Turbo C++ 4.02/TLINK source trials `af1343a` (pellet
arc), `af1343b` (random ring), `af1343c` (two aimed bursts), `af1343d`
(nested radial burst), `af1343e` (arrival blink), `af1343f` (warning
flicker) and `af1343g` (main render guard) each reconstructed the entire
physical BOSS owner and its normal Japanese MAIN link in two independent
rounds. Final current-source stage `af1343i` matches **all 1,840 CODE
bytes, 262 literal ordered OMF fields and 11 PUBLICs**. Related joint
stage `af1343j` recompiles Kotohime, Bullet and both shared BOSS owners:
**5,474 CODE bytes, 564 native fields, 39 PUBLICs** and two complete
Japanese MAIN links and ordered MZ relocation vectors remain original.

The deliberately rejected `af1343h` inverted the final far renderer into
explosion-first `if/else`. Although its CODE length and OMF field counts
were unchanged, TC4 changed `JE` to `JNE` near CODE offset `0x724` and
swapped the call targets; the source was restored. This comparison
explains why the final original render ordering is preserved rather
than treating source-level equivalence as native exactness.

No whole-source cold replay or target-byte changes were used. This updates
an existing physical owner, not 1,840 bytes of first-time game coverage
or canonical Factory packed-file acceptance.

Current source and dependent owner review:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1343i af1343j
```

## 2026-11-11: exact warning-period exits and native ring predicates

The current Kotohime BOSS exposes the release gate in all three large
ring attacks as a direct `<= KOTOHIME_RING_RELEASE_AFTER` early return.
A warning frame still updates `boss_render_frame`, `boss_move_phase`,
and the expanding radius where applicable; neither a random ring nor
an aimed ring nor the nested O(orbit_count * burst_count) radial launch
runs before the original warning deadline. Once elapsed, the same
bullet type/group, signed 16-bit polar divisions, speed calculations,
RNG draws, sound and SELECT transition execute in their original order.
The gate's negative form leaves the large radial loop's original DI/SI
index allocation and per-projectile division behavior intact.

`kotohime_render_ring()` now combines warning-render mode and the
four-frame animation phase with ordered `&&`, and the intro renderer
combines its odd-global-frame and introduction deadline in the same
way. The `kotohime_ring_emit()` signed 16-bit optional RNG argument
also accepts natural `if(randomize_angle)` without changing how many
random words are consumed.

Stages `af1354a` (warning sprite), `af1354b` (intro), `af1354c`
(random release), `af1354d` (aimed release), `af1354e` (nested radial
release), and `af1354f` (ring emitter RNG flag) each proved the
entire owner in two genuine original Turbo C++ 4.02 rounds. Current
source-bound `af1354g` proves **1,840 CODE bytes, 262 ordered native
fields, 11 PUBLICs**, normal Japanese MAIN images and ordered MZ
relocations. Its joint `af1354h` builds Kotohime BOSS, Bullet, both
shared BOSS owners and Kotohime Extra Attack together: **6,528 CODE
bytes, 664 ordered fields, 47 PUBLICs**, with both normal MAIN links
exact. This is improved natural source for existing ownership, not
new packed Factory acceptance.

Current receipt: `.analysis/work/exatt-layout-af1354g/report.json`, SHA-256
`a1b5ccc8eaca87248e471859387b9a86960dbd3647a71e65fbb70a575c4ca7e6`.
Joint receipt: `.analysis/work/exatt-layout-af1354h/report.json`, SHA-256
`13c8c56f1d2c5f3f928caf837a954f7d99d12dcb6b0c223dbd0c8241c74467d0`.
