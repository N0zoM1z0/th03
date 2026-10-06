# MAINL text-box CPU diagnostics

The guarded cutscene candidate review is extended with actual instructions for
box allocate/snapshot, free, restore, cursor advance and the `n/s` command paths.
Seventy-two top-level calls across decoded target and both cached images have
identical observations. This adds runtime-model evidence to the existing
cutscene candidate, with no new unit, maintained source or exact credit.

```sh
python3 scripts/review_th03_mainl_box.py --output .analysis/NEW_BOX_REVIEW.json
python3 -m unittest discover -s tests -p test_mainl_box_review.py -v
```

Receipt: `.analysis/sol-mainl-box-review-20261006.json`. The prior complete
cutscene receipt is pinned by its SHA-256, and all of its consulted input hashes
are rechecked before/after execution. Canonical Japanese MAINL is independently
read through the target manifest. No Ghidra database observation is used.

## Explicit model and execution boundary

The relocated images load at segment `2000h`, CS=`295Fh`, DS=`2E3Fh`, SS=`4000h`.
Root instructions execute under Unicorn 1.0.2rc4. The model supplies initialized
DGROUP plane pointers at `1C60/64/68/6C`, pointing to four **flat** 32-KiB
regions at segments A800/B000/B800/E000. Distinct constructed word patterns fill
those regions; no game assets are imported. Actual initialization of these
pointers and PC-98 GRCG/EGC modes remain outside this scope.

Port A6 byte writes are logged, with no bank switching or hardware effects.
Consequently, the two restore calls overwrite the same modeled regions; their
instruction/access/port order is observed, but equality of two physical VRAM
pages is not proved. Font, EGC, tearing and actual pixels remain open.

Only allocator, free, input wait and ASCII tolower are substituted. Allocation
returns constructed segments 6000 or zero; free returns AX=FFFF/CF=1 without
actual DOS side effects; wait records its word argument and returns. Interfaces
preserve the other registers in the model. Actual library/kernel ABI effects
and successful/failed allocation semantics require separate evidence.

Each invocation resets its return sentinel and has an 800000-instruction limit.
Unknown bodies/imports, segment aliases, interrupts, input ports and output
ports other than byte A6 are rejected. Callback errors are raised outside the
FFI boundary. Near stack cleanup and BP/SI/DI preservation are checked after
every return. An exhausted budget is a failure, never a terminal success.

## Complete transfer observations

Snapshot reads the x=80..559, y=320..383 rectangle: 64 rows, thirty word cells
per row, B/R/G/E order per cell. It writes exactly 7680 words (`3C00h` bytes) to
the backup, with no leading/trailing padding. All 15360 ordered read/write
events are checked against an independent coordinate/layout specification.
Full constructed backup bytes are checked, rather than only first/last words.

The four snapshot cases per image combine absent/nonzero prior pointers and
successful/zero allocation. Existing backup is freed by its segment, and the
full far pointer is cleared **before** the allocator is called. Even when the
constructed free fails, allocation proceeds. Segment-zero allocation still
performs the full snapshot to linear `00000h..03BFFh`; the model permits these
writes, so this is a failure-path CPU observation, not evidence of safe DOS
execution or a reachable game-script condition. The resulting NULL pointer
causes the later free to be skipped.

Restore cases use `6000:0000`, `6000:FF00`, and `0000:0000`. There is no NULL
check. Every read and plane write is checked; the full four regions confirm
that only the rectangle changes while the A5 guard outside it remains intact.
The backup pointer itself remains unchanged. At FF00 the offset wraps within
segment 6000; no segment normalization occurs. The NULL case reads constructed
low-memory words and writes them to the rectangle, without claiming actual
IVT/BIOS data or hardware behavior.

Separate free cases distinguish `0000:0000`, `0000:0007` and `6100:0011`:
the test uses the complete far pointer, but only the segment reaches free.
Thus a nonzero offset with segment zero still calls free(0). In every modeled
failed-free case the pointer is cleared without testing the returned result.

## Cursor and box-change commands

Six cursor cases per image cover ordinary advance, a line break, full-box
advance with/without fast-forward, and constructed signed overflow inputs.
At 544/352, advance moves to 144/368, reserving the name area. At 544/368 it
waits with argument zero unless fast-forward is set, resets to 80/320, writes
A6=1 and restores, then writes A6=0 and restores. Constructed x=FFFF becomes
15; x=7FFF becomes 800F, and the signed comparison suppresses wrapping. These
invalid positions are arithmetic controls, not proved valid caller states.

Four `script_op` cases per image execute newline at the bottom with tail `7!`,
box change with `-!`, and box change with `12!` with/without fast-forward.
Newline falls into the box-change parser and waits for 7; `-` skips waiting;
ordinary `s12` waits for 12 unless fast-forward is set. All reset the cursor and
perform the same two ordered restores. Wait implementation/timing is modeled.

Each image runs four snapshots and their four frees, three direct restores,
three standalone frees, six cursor cases and four command cases: 24 calls,
72 across the three images. Five synthetic controls reject budget exhaustion,
stale return sentinels, callback errors, aliased interfaces and incomplete or
reordered transfers. Whole interpreter/picture/device execution, dependencies,
natural PI entry producer, cold maintained compiler and stored packing remain
open. The complete cutscene still has its three raw call-operand failures.
