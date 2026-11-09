# TH03 MAIN — Rikako BOSS spin clocks, emission scopes and source register lifetimes (af1118e)

The full `ba_rikak` Turbo C++ 4.02 original owner contains the orbit spread,
entity launch/pellet ring, alternating burst, major BOSS update/collision, and
main/intro renderers. All three eight-frame **unsigned word** spin clocks
now use natural `% RIKAKO_SPIN_TICK_PERIOD` with a truthy zero-remainder
predicate. The original global unsigned-word `boss_frame` uses prefix
increment, whereas signed/byte spin increments retain their own codegen.
The alternating burst's byte remainder is initialized at first use after
the original `boss_move_sine()` call.

In the full entities/pellets attack, the two independent `for` passes now
have separate `register int i` declarations inside their headers; this is
a tested compiler-equivalent alternative to the previously shared index.
The orbit-spread's signed `angle_delta` also initializes at the actual
RNG decision site. This does not move any original RNG draws or change
signed angle arithmetic and 256-step integer division.

The incremental original TC4/full normal MAIN TLINK stages `af1118a`
(word clocks), `af1118b` (truthy remainder/byte scratch), `af1118c`
(two scoped entity/pellet indices), and final `af1118e` (signed angle delta)
each passed two complete independent rounds: 1,677 original CODE bytes,
215 literal ordered native fields, eight PUBLICs, the full Japanese MAIN
loaded image and all 1,553 ordered MZ relocations matched.
Source-linked report: `.analysis/work/exatt-layout-af1118e/report.json`.

A combined lifetime narrowing `af1118d` changed CODE; the separate
`af1118f` test isolated its cause to moving the unsigned orbit `angle`
into the polar loop. Its original function-wide declaration is retained.
No generated target bytes or canonical Factory acceptance are claimed.
