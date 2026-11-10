# Ellen BOSS: exact Extra Attack angles and intro flicker

The complete Ellen BOSS now uses natural byte-angle `+=` in both radial
Extra Attack bursts. Each burst still draws its own RNG word and divides
its 256-unit full turn by the original byte count on every iteration;
the angle changes *after* the far Extra Attack call. The paired-pellet
attack's separate 0x10-byte angle advance also accepts compound `+=` in
the current TC4 source. The intro sprite flicker is now an explicit
nested global-frame and intro-window gate, preserving earlier strip draws.

The original TC4 4.02 source-bound stage `af1331h` reproduces **all 1,675
physical CODE bytes**, 213 ordered OMF native fields and nine PUBLICs in
two independent rounds. The related `af1331i` stage jointly recompiles
Ellen, Bullet and both shared BOSS objects: **5,309 CODE bytes, 515 fields,
37 PUBLICs** and both complete normal Japanese MAIN links and ordered
MZ relocations match the original.

Compiler counterexamples matter here: `af1331d` made the spread-angle
advance compound `+=` and shortened the physical BOSS from 1,675 to
1,671 bytes, with 212 instead of 213 ordered fields. `af1331f` made
`boss_render_frame += 3` compile to a different memory ADD, also shrinking
the owner to 1,671 bytes. `af1331g` merged four render-strip decrements
with their negative tests and shrank CODE to 1,667 bytes. These changes
were individually rejected. Equal-looking C++ syntax in another BOSS
cannot substitute for the real owner-specific compiler proof.

Read-only verification of current native source:

```
PYTHONPATH=scripts .venv/bin/python scripts/review_th03_main_source_overlay.py --stage af1331h af1331i
```
