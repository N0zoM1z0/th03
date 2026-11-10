# MAIN frame scheduler: rendering skip, VSYNC wait and victory decisions

The complete 3,050-byte original `entry` physical owner contains MAIN's
main entry, full round frame scheduler, stage setup and score completion.
`src/main/round/round_loop.inl` now makes three original scheduling
invariants explicit without changing machine code:

1. The hardware render skip occurs only when the stage timing flag is
   enabled **and** the current unsigned-word global round frame is even.
   The source expresses these as nested checks, preserving the original
   `frame_advance` goto and leaving the BOSS, bullet, and input updates
   ahead of it untouched.
2. After the HUD and background calls, the normal VSYNC wait always
   executes when timing is disabled; when timing is enabled, only even
   global frames reset the counter and use the two-frame delay. A nested
   `if` under the original `else` now visibly distinguishes the two paths.
   No hardware I/O or counter store moved across the render boundary.
3. The banner's round-victory check now spells out player 0 and player 1
   independently. Both branches go to the existing `match_result` label
   and preserve the same test order and three original round-return sites.

Stages `af1314a` (render skip), `af1314b` (VSYNC phase) and `af1314c`
(victory exit) were compiled with original Turbo C++ 4.02 in two independent
rounds each. The **entire physical entry object** and both genuine normal
MAIN links reproduced the complete 3,050 initialized CODE bytes, ordered
OMF relocation fields, PUBLICs, segment/MAP ownership, the original
Japanese program image and ordered MZ relocations. `af1314c` is the
current source-bound stage. The original large owner—not an isolated
branch fragment—was rechecked. No full cold replay was performed.

Read-only source-bound review:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1314c
```

This does not establish complete product ownership or Factory Oracle
packed-file acceptance. The unchanged frozen linker parent is still used.
