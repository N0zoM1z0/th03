# TH03 MAIN Yumemi attack patterns: natural phases and RNG arithmetic

The five attack-family leaves in Yumemi's complete BOSS now use more natural
phase predicates and modulo expressions while retaining all original
projectile and RNG ordering.

## Aimed Random (266 B)

- Constant-first initialization, warning, fire-start and finish comparisons.
- Period-four warning and period-two firing expressed as unsigned-word
  `% period` tests.
- Zero is compared on the left for the even firing cadence.
- The speed expression is base-first, with the RNG call still evaluated
  exactly once; the random bullet type uses `1 + randring_far_next16_and(1)`.
- `bomb_axis_add`, explosion, sound, speed/type/group RNG draws and
  `bullets_add()` remain in their original order.

## Cross Rings (166 B)

- The variable interval uses a constant-first zero comparison.
- The random bullet type uses `1 + randring_far_next16_and(1)`.
- The inclusive finish frame is constant-first.
- The four independent random-angle draws and four bullet additions remain
  separate and in their original order.

## Chase (180 B)

- SEEK and TRACK frame tests are constant-first.
- The period-16 beam gate uses `% YUMEMI_CHASE_BEAM_PERIOD` instead of an
  explicit bit mask.
- The variable chase limit is expressed as `yumemi_chase_until < boss_frame`.
- The original positive short-circuit X-range test is unchanged; an earlier
  negative-control experiment showed that inverting it to an early exit
  changes native branching.
- The two consecutive `boss_move_sine()` calls and beam/extra emission order
  remain unchanged.

## Rain (161 B)

- The variable unsigned-word interval compares its remainder to zero
  constant-first.
- Spread-end, rain-begin and finish checks are constant-first.
- The random angle bias is placed before the single RNG result.
- The twelve-drop `for` loop, separate X and angle draws, and one bullet add
  per iteration remain unchanged.

## Ring (225 B)

The [separate Ring review](MAIN_YUMEMI_RING_PHASE_AND_SPEED_AFTER1036_REVIEW.md)
records its constant-first phase tests, modulo-four cadence, constant-first
RNG bit test and compound speed progression.

## Complete-owner verification

Stage `af1036s` rebuilt the complete `ba_yumem` physical owner in two
independent original Turbo C++ 4.02 rounds. All 2,358 CODE bytes, 343 ordered
native fields and ten PUBLIC offsets match. Both normal Japanese MAIN links
reproduce the original loaded image and ordered MZ relocations.

Protected report: `.analysis/work/exatt-layout-af1036s/report.json`

SHA-256: `55878e107ba9e9197ba01a19c099fd4b249dfa93d197d7ff346d83c1945259c5`
