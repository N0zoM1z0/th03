# Native VSYNC polling and DOS initialization leaves

`frame_delay()` now expresses the original volatile VSYNC wait as a natural
`for` loop. Its initializer sets `vsync_Count1` to zero exactly once; the
condition rereads the interrupt-updated unsigned 16-bit counter on every
iteration, retaining the original comparison against a signed 16-bit frame
parameter. There is no software increment, sleep, timeout, or extra port
access. The original TC4 emits the same full 21-byte `frmdely1` CODE owner,
with both native fixup fields and its far-Pascal return unchanged.

`game_init_main()` now treats the nonzero result of the 18,000-paragraph
(288,000-byte) DOS allocation as the early failure condition. The source
still returns 1 before hardware startup on allocation failure, otherwise
initializing VRAM planes, VSYNC, EGC, 400-line graphics, joystick and the
archive in the original order before returning zero. The original TC4
produces the same complete 62-byte `initmain` CODE with seven native fields.

Both affected owners compiled and linked together in two independent original
TC4/TLINK rounds (`af1316d`): 83 CODE bytes, nine literal ordered native
fields, two PUBLIC offsets, the complete original normal Japanese MAIN
image/MAP and ordered MZ relocation vector. Separate current source-bound
stages `af1316e` (frame delay) and `af1316f` (DOS initializer) likewise
reproduced the full objects and normal MAIN links in two rounds apiece. Only
the affected original physical objects were recompiled; no full cold replay.

A related signed-Q8 math experiment (`af1316b`) tried a named 32-bit
intermediate for `polar()`. TC4 emitted `ENTER 4,0` and a stack-local DWORD
store in place of the original plain `PUSH BP; MOV BP,SP` and direct
arithmetic shift. The function grew from 26 to 31 CODE bytes, so the
original expression in `src/main/math/polar.cpp` was restored. The
original signed 32-bit multiply and arithmetic shift remain necessary;
this negative result adds no `polar` acceptance credit.

Verify the two current leaf scopes without building the frozen ancestor:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1316e af1316f
```

These are source-bound native comparisons; they do not establish
whole-product or canonical Factory packed-file acceptance.
