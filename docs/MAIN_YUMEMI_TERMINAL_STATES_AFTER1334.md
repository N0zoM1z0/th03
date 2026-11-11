# Yumemi BOSS: native-exact terminal state transitions

The complete Yumemi BOSS controller now expresses its ring, aimed,
cross, chase and rain attack completions as positive frame conditions.
Ring and aimed finish **after** their inclusive terminal frame; cross
and rain finish **at** their terminal frame. The chase returns to its
seek state only after the tracking clock has elapsed, and never before
its original double sine movement and conditional beam emission. The
first ring/aimed initialization and warning-phase comparisons place
the live unsigned-word frame/remainder on the left. All RNG draws,
bullet launches, audio callbacks and visual-state changes remain in
the original order.

The genuine TC4 source-bound stage `af1334f` matched the entire
**2,358-byte `ba_yumem` CODE**, 343 ordered OMF native fields and ten
PUBLICs in two rounds. The bounded joint `af1334g` recompiled Yumemi,
Bullet and both shared BOSS objects (**5,992 CODE bytes, 645 ordered
fields, 38 PUBLICs**), with identical complete Japanese MAIN images,
normalized MAPs and ordered MZ relocations.

Two complete-player-structure experiments show a meaningful remaining
source dependency constraint. `af1334a` included the real
`player_stuff_t` at the original collision header position. It compiled
identical machine code but moved `_players` from native EXTDEF index 38
to 22, changing literal OMF fixup targets. `af1334b` moved the full
header after other imports, preserving CODE and field counts but
shifting collision/RNG extdefs. Neither can replace the existing
128-byte player view under the strict complete-OMF check. Both trial
sources were reverted; no linker-output or target byte was patched.

Review the current source-scoped proof without a cold replay:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1334f af1334g
```

## 2026-11-11: source-exact chase, renderer and projectile cadence

The current Yumemi physical owner has two large-function control-flow
recoveries. `yumemi_pattern_chase()` expresses the seek corridor as an
ordered short-circuit conjunction, avoiding two nested condition blocks
while keeping the original left-then-right boundary tests before the
sine movement. `yumemi_render_main()` uses one short-circuit exit only
when both the effect radius and render-frame timer are zero, with the
original clipping, circle and line draw paths unchanged.

The ring, aimed, cross and rain patterns now express their unsigned-word
projectile cadence with an explicit zero-remainder condition. The common
attack timings and all RNG/emission order remain unchanged. Native stages
`af1350a` (chase), `af1350b` (renderer), `af1350c` (ring) and `af1350d`
(all four cadences) each rebuilt the *complete* Yumemi 2,358-byte source
owner in two independent original TC4 rounds. The confirmed current-source stage `af1350e` (including explanatory
comments) reproduces all 343 ordered native fields, 10 PUBLICs, both original normal Japanese
MAIN links and the ordered MZ relocations.

Current proof: `.analysis/work/exatt-layout-af1350e/report.json`, SHA-256
`d7c3b5bc3a767651d398ad1d0d2cb8b90c4935b7372bb406caf3a4f58709eb07`.
The full-player-structure EXTDEF-order issue described above was subsequently
resolved in the source-bound stage `af1350l`, explained below.

## Original complete player state without EXTDEF drift (2026-11-11)

Yumemi's maintained boss source now uses the genuine 128-byte
`player_stuff_t` from `src/main/player/stuff.hpp`, rather than the former
handwritten center-plus-padding view. Original TC4 emits externals in
source declaration order: importing the player header at the collision
header's position moved `_players` from EXTDEF 38 to EXTDEF 22 even
though the complete CODE matched. Ordered original fixups therefore
referred to different external indices, and `af1334a` / `af1350j`
correctly failed the strict OMF reviewer.

The recovered source includes the full player header where its collmap
and layout types are needed, temporarily renames *only the header's*
`players` declaration, and then declares the genuine
`extern player_stuff_t players[PLAYER_COUNT]` at the original slot after
collision, graphics and sound imports. The renamed unused declaration
creates no EXTDEF. Both independent TC4 rounds now place `_players` at
original EXTDEF **38**, retain all **66 ordered external names**, and
emit the exact original code and literal FIXUPPs. This scoped approach
avoids changing shared player headers or every consumer's inputs.

A naive late header include (`af1350i`) failed compilation because the
original collmap declarations were included twice and the packing state
had changed. Merely moving the header early (`af1350j`) compiled exact
CODE but shifted the `_players` EXTDEF. `af1350k` first established full
object and normal-link equality, but its new header still came from the
unchanged historical compiler work tree. Stage **`af1350l`** explicitly
roots the current maintained `src/main/player/stuff.hpp` in both compiler
rounds, recording its SHA and confirming the compiler's OMF dependency
COMENT. Its current source-native reviewer passes while the unbound
`af1350k` report is correctly rejected by that reviewer.

The final independent source-bound stage reproduces the complete
**2,358 CODE bytes, 343 ordered native fields, 10 PUBLICs**, both normal
Japanese MAIN images and ordered MZ relocations, without target padding,
new product storage, object patches or full cold replay.

Current proof: `.analysis/work/exatt-layout-af1350l/report.json`, SHA-256
`abf8f76dbdab9ad04b3979fddab9fc28a3d76fba71b5d9894eab9b308c8196bc`.
Current pinned layout header SHA-256:
`204d1bf8db3ce39dbb3af8966ccfb521bc93f35445e305ab524f48bf026c4912`.

## 2026-11-11: mutually exclusive chase beams and direct completion exits

`yumemi_pattern_chase()` now expresses the tracked beam firing and chase
termination as one `if/else if` pair. A beam frame still draws the warning,
emits the Extra Attack and suppresses terminal reset even after the chase
clock expires. Otherwise the terminal path resets the beam animation,
SELECT mode and seek phase in the original order. Both sine movement calls
still precede this decision, with the original player position and RNG
consumption unchanged.

The expanding ring and aimed-random attack controllers now return on
incomplete frames, committing their original `YUMEMI_MODE_SELECT` resets
only *after* their inclusive terminal clocks. The cross-ring and rain
attacks likewise return before their respective terminal frames, with
all four random ring angles, twelve rain-drop positions/angles and the
final-frame emissions kept before mode completion.

Stages `af1358i` (chase), `af1358j` (ring finish), `af1358k` (aimed
finish) and current `af1358l` (cross/rain finish) each reproduced the
complete **2,358-byte** Yumemi BOSS object in two original TC4 rounds,
including **343 ordered fields, ten PUBLICs** and exact normal Japanese
MAIN links. Joint `af1358o` recompiles Yumemi BOSS, Yumemi Extra Attack,
Bullet, both shared BOSS objects, PI loader, Polar and SE: **7,904 CODE
bytes, 756 fields, 47 PUBLICs**, with complete original normal MAIN
image and ordered MZ relocations in both rounds.

Current BOSS proof: `.analysis/work/exatt-layout-af1358l/report.json`,
SHA-256 `0127b48a578226662b37efbe9001c491397708f7b8a5f2d6a979048b49e7b3e2`.
Joint proof: `.analysis/work/exatt-layout-af1358o/report.json`,
SHA-256 `fc11fa573456b79b4ff40c42914cb085414637c47ad0598095a7e1a5a256b5ca`.

## Native rain and entrance raster traversals (2026-11-11)

`yumemi_pattern_rain()` now uses a pre-tested signed-index loop for
all twelve droplets per wave. Each iteration consumes exactly the
original random X word and angle word, launches one bullet, and only
then advances the index. The enclosing word-frame cadence, the two
opening spreads, and the terminal SELECT transition remain separate.

`yumemi_render_arrival()` also uses four independent pre-tested loops.
The first two sweep rightward, and the last two leftward, preserving
each phase's inclusive pixel bounds and the original 8-pixel step
only after `sprite16_put()`. The third phase's extra fixed sprite,
two-stage coordinate scaling, clipping and PC-98 overlap interrupts
remain in their original order.

Stages `af1366a`–`af1366e` proved each change. Current source stage
`af1366f` rebuilds all **2,358 CODE bytes, 343 ordered native fields
and 10 PUBLICs** in two original TC4 rounds with exact normal MAIN
links. Joint `af1366g` compiles Yumemi BOSS, Yumemi Extra Attack,
Bullet, both shared BOSS objects, PI loader, Polar and SE: **7,904
CODE bytes, 756 fields, 47 PUBLICs**, with identical normal Japanese
MAIN images and ordered MZ relocations in both rounds.

Owner proof: `.analysis/work/exatt-layout-af1366f/report.json`, SHA-256
`b3fcbdd0e29d5726ed5a012ffe0bf75d54deb5c50e07e428c860b3ea601377ca`.
Joint proof: `.analysis/work/exatt-layout-af1366g/report.json`, SHA-256
`99455e961b85be95bffaa0eedeee928e2c9940a599304c6832dd90c509f4bcb2`.
