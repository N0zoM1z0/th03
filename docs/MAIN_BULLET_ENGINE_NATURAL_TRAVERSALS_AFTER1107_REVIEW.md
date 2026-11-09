# TH03 MAIN — complete Bullet engine traversal recovery (af1107c)

The entire `bullet` physical Turbo C++ 4.02 owner contains the original
pellet writer, velocity-group dispatcher, bullet allocation, trail history,
update/collision routine and separate sprite/pellet rendering passes.
Its full allocator and renderer remain the original physical owners.
`bullets_reset()` now expresses its complete signed-index flag walk as a
natural `for`; both main and cloud sprite passes use natural prefix index
updates. The first-free bullet allocator uses a prefix near-pointer advance
alongside its original signed-index/continue/break semantics. Signed group
progression, the low-level pellet register pointer and the unsigned
pellet index use natural prefix advancement without moving a single call.

Successful cumulative stages `af1107a` (reset loop), `af1107b` (alloc and
full-color/cloud renderer progression) and `af1107c` (group/pellet progress)
all passed the real TC4/native normal MAIN linker twice. The final source
reproduces all 2,685 initialized CODE bytes, 196 literal ordered OMF fields,
20 PUBLIC offsets, complete Japanese MAIN and all 1,553 ordered MZ relocations.
Current source-bound evidence: `.analysis/work/exatt-layout-af1107c/report.json`.

Fresh `af1107d` tested replacing the original 8x8 pellet `do/while` with
one bounded `for` scan over the same fixed slots. TC4 changed original CODE
although the visible scan order is equivalent for the nonzero bullet count;
that restructuring was rejected and the post-tested scan remains. No synthetic
code bytes, padding, full cold build or canonical Factory credit are claimed.
