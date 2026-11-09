# Fireball engine: native keyframes and complete entity index lifetimes

The complete `e_fireb` physical owner now expresses the explosion collision
keyframe transitions as individual finished-state returns rather than an
`else if` chain. Its 24-slot update and the reverse 24-slot fireball collision
scan declare their signed indices in their natural `for` headers. These
changes preserve the original transfer and clipping labels, the exact
RNG/chain reward order and the historically uninitialized `chain_slot` value;
the latter is gameplay-visible and was not initialized as a source cleanup.

The final `af1177g` native TC4/TLINK stage reproduces the complete 1,555
CODE bytes, 115 ordered native fields, ten PUBLICs and the Japanese MAIN
image/relocations in both original compiler rounds. The independent
`af1177d` trial showed that the **allocator** index cannot be narrowed,
although the complete movement and collision indices can (`af1177e`).
Similarly, narrowing the byte explosion cel local (`af1177f`) changed CODE.
