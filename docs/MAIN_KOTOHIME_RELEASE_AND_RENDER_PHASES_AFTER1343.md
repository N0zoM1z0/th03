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
