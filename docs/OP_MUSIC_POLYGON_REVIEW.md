# OP Music Room polygon contract

2026-10-28: the existing maintained `animation_and_menu.inl` now has an
independent executable contract for its complete polygon pair:

| Procedure | Decoded address | CODE bytes | ABI |
| --- | --- | --- | --- |
| `polygon_build` | `0990:0D14` | 143 | near Pascal, 12 argument bytes |
| `polygons_update_and_render` | `0990:0DA3` | 502 | near C, no arguments |

This is new diagnostic evidence for existing source, not new implementation
or source-acceptance credit. The historical 1,998-byte animation/menu unit and
the current OP publication retain their existing state. Renderer, initialized
DATA, BSS and the remaining Music Room procedures gain no ownership here.

## Native and source bindings

`scripts/review_th03_op_music_polygon_work.py` revalidates the entire unchanged
OP source-only cold graph, tool surfaces, all 32 outputs in both rounds, and
complete decoded/stored Japanese target equality. It does not rebuild the
product or replay ancestor runtime matrices. The actual Music Room producer's
complete source/include chain and consumed `mem.h`, `_defs.h`, `_null.h` are
bound through the existing state review's dependency checker.

The complete natural TC4 carrier's records, segment contributions, publics and
MAP allocations are checked before the pair's 54 OMF fields are independently
resolved. All 645 raw bytes, 219 instructions and 14 literal ordered MZ
relocations match both target and candidate. No executable or object is patched.
The target Ghidra database was re-attested before this investigation.

## Executed behavior

The scalar specification predicts native near/far frames, all ordered writes,
every DWORD register and six segments, defined flags including IF/DF, and all
1 MiB of memory. No stack byte is ignored. Actual IRAND and polar instructions
execute on the same Unicorn instance as the pair; their 68 bytes are context,
not new ownership. The random-state result additionally checks the independent
DWORD recurrence `seed * 22695477 + 1`. Only the external polygon renderer
receives a bounded reply, with varying volatile register results.

Preserved details include:

- The argument's Y WORD is shifted arithmetically in the real caller frame.
  The angle consumes only its low BYTE. `(i << 8)` wraps as a WORD before signed
  division, including the negative intermediate at vertex 128.
- The closing point duplicates the first point even for nonpositive counts.
  Signed radius multiplication and the actual sine/cosine tables remain live.
- All 16 polygons are built at their old positions before movement. Signed X
  reflects at `<= 0` or `>= 639`; signed updated Y resets at `>= 8000`.
  WORD position and BYTE angle overflow are preserved.
- Initialization and reset consume different random sequences. Zero horizontal
  velocity becomes 1; zero angle speed becomes 4. Reset Y is -1600 subpixels;
  radii are 64, 80, 96 and 112 pixels. The initialization flag persists between
  consecutive calls.

Each image executes 571 cases at each of load segments `1000` and `3000`:
304 complete build returns and 267 update returns, including three consecutive
frames. All 645 bytes execute; maximum checked stack depth is 40 bytes. The
matrix covers every independent angle BYTE, ignored argument high bytes,
counts -1/0/1/2/3..7/127/128/129/255/256, signed radius extremes, initialization
BYTE 0/1/128/255, DWORD seed extremes, eight independently varied position and
velocity profiles, IF/DF and stacks `0100`/`FFF0`. This is 2,284 complete
executions across the two images, not an exhaustive input-domain proof.

All 46 real-instruction mutations reject. Discriminating fixtures were needed:
SAR of -1 gives -1 for both shift counts, seed 0 misses the initial zero-velocity
replacement, and coupled position/velocity profiles miss the right-boundary
neighborhood. Those draft controls were corrected rather than counted as passes.
Constructor, scalar-prediction and unexpected hook exceptions propagate as
verifier failures. Fault injection exposed that a scalar `ContractError` could
otherwise be mistaken for 46 rejected guests. The runner now records whether
actual guest execution began; a failure before that phase is always fatal,
including an exception with the same type as a guest mismatch.

## TH04 source comparison

At the user's request, the local TH04 checkout was inspected read-only at
`09e80fdfabe5f0be8f19969a9f97adf9dec40707`. Its
`src/op/music/polygon_build.inl` and `polygons_update_and_render.inl` support the
same high-level geometry and thresholds. Their observed SHA256 values are
`cd7fec87645c3a91eee4ba25c2695986e0ed612d9e491dba85be0955310df828` and
`21858ec7ee93637491e921e7cb3bc3e20e5e34c35ef7e79bb186ac6e3d311f64`
respectively. These are source
leads, not TH03 target evidence or a new build dependency.

The TH04 update include still says the maximum radius is 96, although its
`((i & 3) * 16) + 64` expression and 16-iteration wrapper also produce 112.
TH03's existing correction is confirmed directly by the TH03 instructions.
TH04's `room.cpp` replaces `polygon_init` with a helper call; copying that
wrapper would introduce argument-evaluation/ABI questions around the random
sequence. TH03's macro expansion and its observed random-call order are retained.

For the next menu contract, TH04's branches also identify useful boundaries:
TH03 uses `op3.pi`, stops the previous song before loading, draws comments on
each page with a flip between them, and frees comment backgrounds on exit.
The TH04 branch uses `music.pi`, song fade and a different comment-animation
path, then reloads the main-menu song. These version branches must stay separate.

## Reproduction and remaining work

Run with the repository `.venv`, empty displays, one CPU and nice10:

```sh
.venv/bin/python scripts/review_th03_op_music_polygon_work.py
.venv/bin/python scripts/review_th03_op_music_polygon_work.py --check
.venv/bin/python -m unittest discover -s tests -p test_op_music_polygon_current.py -q
```

The tracked observation binds implementation, current cold report, producer,
SDK, native layout and unchanged acceptance publication. `--check` revalidates
those bindings and executes a two-load target/candidate signed-division and
consecutive-update smoke; it does not pretend to rerun the full matrix.

Source-scope publication integration and a reviewed owner split remain open.
The 476-byte Music Room menu and its remaining comment/copy/flip dependencies
still need current contracts before composing the full menu. Physical polygon
pixels, renderer execution and frame timing are outside this reply fixture.

The next menu's target instruction map is `0990:1306..14E1`, ending in an
actual far return. It frees 32 CDG slots. Selection 19 is the skipped blank,
20 is Quit, and Up/Down are two sequential tests rather than an `else if`.
Initial held-input polling begins at decoded load `ACC2`, control polling at
`ACD3`, and exit-release polling at `ADB0`. Shot tests low BYTE bit `20`, OK
high BYTE bit `20`, and Cancel high BYTE bit `10`. These are static entry/branch
observations; no closed-loop or composed-menu runtime acceptance is inferred.
