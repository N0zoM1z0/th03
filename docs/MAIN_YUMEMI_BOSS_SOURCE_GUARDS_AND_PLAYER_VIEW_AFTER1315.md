# Yumemi BOSS: exact seek and visual-state guards, and player-view ABI constraint

The maintained Yumemi BOSS now expresses the two original positive seek
boundaries as nested tests. Before the chase enters tracking mode, the
sine movement and immediate return occur only when the center is strictly
between the left and right boundaries. An out-of-range center still resets
the clock and switches the move phase. This is not a clamped position or
an inverted early-exit approximation. The original compiler reproduces the
same branch sequence.

The ring and aimed random attacks now compare their unsigned 16-bit frame
on the left of each warning threshold, preserving the two distinct release
periods. The visual effect renderer now tests the effect radius and the
animation frame in separate nested guards: either nonzero value is enough
to keep the effect drawn. The original render and hardware call ordering,
projectile RNG draws, and chase-state transitions remain unchanged.

Native trials `af1315c` (positive nested chase boundaries), `af1315e`
(renderer state pair), `af1315f` (ring release), and `af1315g` (aimed warning
and seek enum) each reconstructed the complete 2,358-byte physical `ba_yumem`
object in two independent original TC4/TLINK rounds. The final bound source
stage `af1315h` matches all 2,358 initialized CODE bytes, 343 literal ordered
fixup fields, ten PUBLICs, native segments, normal MAIN/MAP and the full
Japanese program image plus ordered MZ relocations in both rounds. No full
cold replay or output patching was used.

Two unsuccessful experiments establish important boundaries:

- `af1315a` replaced the local 128-byte player view with the existing full
  `player_stuff_t`. Direct inclusion duplicated the unguarded collmap header
  and produced eleven native compiler errors. Removing the duplicate direct
  include (`af1315b`) restored the **entire 2,358-byte CODE** but changed
  the physical EXTDEF declaration order: `_players` moved from external
  index 38 to 10, and a fixup at CODE offset 1004 changed its literal
  target index from 16 to 22. Equal CODE alone did not justify accepting
  that candidate. The bounded view is retained pending a source-faithful
  dependency ordering, rather than weakening the native field comparison.
- `af1315d` changed the first aimed-attack target sample from two separate
  X/Y field assignments to one structure assignment. TC4 selected prefixed
  32-bit loads/stores instead of the original two 16-bit word reads, reducing
  CODE to 2,346 bytes and ordered fixups to 341. Both original field reads
  were restored. The chase path still performs the original independent
  center reads as well.

Recheck the complete physical owner without rebuilding the frozen parent:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1315h
```

This verifies the source-bound object and unchanged normal MAIN link, not
whole-game or Factory packed-file acceptance.
