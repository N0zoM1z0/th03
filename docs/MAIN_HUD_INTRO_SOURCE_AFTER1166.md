# Round intro: exact native phase boundaries and particle traversals

The full HUD intro object owns the sliding sprite strip, story/versus
banner, 128-star setup/motion, and the assembly-based VRAM writers. The
seven physical particle traversals now use natural `for` headers with
prefix near-pointer updates and the original signed-index initializers.
Three active flag checks use natural byte truthiness. Update and render
phases can exit after completing their own work; this preserves the fact
that a newly selected phase cannot run until the following frame.

Two independent original TC4/TLINK rounds at `af1166i` reproduce all
1,478 CODE bytes, 145 ordered native fields, four PUBLICs, and the
Japanese MAIN image and MZ relocations. The near Pascal pixel/strip
helper register contracts and original RNG draws are unchanged.
