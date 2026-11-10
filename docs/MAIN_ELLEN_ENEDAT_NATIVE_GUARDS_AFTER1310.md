# Ellen spread exit and ENEDAT script-table indexing — exact native source

Ellen's BOSS spread controller has three attack periods: warning/angle setup,
regular even-frame fire and the eight-shot `0x24` burst, followed by an
inclusive `0x2C` completion gate. In `src/main/boss/ellen.cpp`, the two
post-burst early exits now express the natural ordered short-circuit guard
`frame > 0x2C || frame % 2`, while preserving the original call order and the
separate `fire_single` and `done` edges. These are still distinct native
branches. The more aggressive branch inversion in negative trial `af1310a`
changed three bytes at the first even-frame decision (the `JNE` and `JE`
instruction direction), despite retaining the same 1,675-byte owner size.
The complete Ellen owner is byte-exact with the ordered relocations and normal
Japanese MAIN link in two TC4/TLINK rounds at `af1310g`.

The ENEDAT loader's formation scripts are a segmented array of 16-entry
script-pointer blocks, not one flat arithmetic index in original TC4's code
generation. `src/main/enemy/enemy.cpp` now expresses this as
`(formation_scripts + formation_i * 16)[enemy_i]`: pointer arithmetic
selects the block first, then the enemy within it. The C++-equivalent
`formation_scripts[formation_i * 16 + enemy_i]` in negative trial `af1310b`
made TC4 add the enemy index *before* element scaling. This removed the
original separate `MOV AX,DI; ADD AX,AX; ADD BX,AX` sequence, shortening
the physical eforna object from 729 to 725 bytes. It cannot replace the
original order for byte-exact reconstruction. The parenthesized block-first
form passes both complete compiler rounds and the entire normal MAIN link.

The four independently compiled enemy physical owners (`eforna`, `efornb`,
`eupda`, `eupdb`) collectively retain 3,325 initialized CODE bytes, 222
ordered native fields and 19 PUBLICs in stage `af1310h`. Ellen adds 1,675
CODE bytes, 213 native fields and nine PUBLICs in `af1310g`. The combined
five-owner proof `af1310e` independently passed 5,000 CODE bytes, 435 ordered
fields, 28 PUBLICs and two complete Japanese MAIN links. Every case reused
only the frozen unchanged linker parent, not an all-source cold replay.

Review the retained current reports with:

```
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts .venv/bin/python \
  scripts/review_th03_main_source_overlay.py --stage af1310g af1310h
```

These establish original-source native scopes, not canonical packed-file
Factory Oracle credit or whole-game source ownership.
