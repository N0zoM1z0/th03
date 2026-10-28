# OP Music Room comment, copy and flip dependencies

2026-10-28: seven complete procedures required by the 476-byte Music Room menu
now have a shared physical execution contract. The two long comment-background
loops are included in full; no owned helper is replaced with a synthetic return.
The menu itself still needs its composed contract.

| Procedure | Decoded address | CODE | Callee argument cleanup |
| --- | --- | --- | --- |
| `nopoly_B_put` | `0990:0CF6` | 30 | 0 |
| `music_update_render_and_flip` | `0990:0F99` | 54 | 0 |
| `cmt_bg_snap` | `0990:0FCF` | 315 | 0 |
| `cmt_load` | `0990:110A` | 73 | 2 |
| `cmt_bg_free` | `0990:1153` | 41 | 0 |
| `cmt_unput` | `0990:117C` | 285 | 0 |
| `cmt_load_unput_and_put` | `0990:1299` | 109 | 2 |

These are new contracts for existing maintained source. The 907 CODE bytes,
315 instructions, 63 native OMF fields and 14 literal ordered relocations match
the natural TC4 producer, target and candidate completely. The containing
producer's full records, publics, MAP allocation, literal include chain and
actual consumed SDK dependencies remain checked. The entire unchanged OP
source-only cold graph and decoded/stored Japanese identities are revalidated;
no native cold pair is rebuilt. Target provenance stays `candidate-local-attested`.

Current source-scope publication, canonical unit credit and whole-product
acceptance remain unchanged. The 30-byte copy body has a separate ledger row
from the 877-byte tail. Neither this evidence nor the earlier polygon contract
grants initialized DATA/BSS or menu ownership.

## Preserved native behavior

- The B-plane restore executes all 16,000 actual REP MOVSW iterations. It
  preserves incoming DF and reloads the saved segment-only heap pointer.
  Backward copies touch the WORD-wrapped offsets above the declared plane
  size. Overlap remains live, including source segment `A801` beside `A800`.
- Background capture allocates four unchecked 12,800-byte buffers and writes
  each far pointer's segment before clearing its offset. A zero allocator
  result is used directly. Title rows 64..79 and comment rows 80..383 share one
  continuous cursor: 320 rows, ten DWORDs per row, 3,200 DWORDs per plane.
- Every copy reloads both far pointers. WORD offset arithmetic wraps before
  the four-byte memory access; the DWORD itself spans physical bytes normally.
  Plane/source/destination aliasing is checked as ordered live operations.
- `cmt_load` multiplies the full track WORD by 840 with a 16-bit result, then
  sign-extends it for `file_seek`. Track 39 yields 32760; track 40 yields -31936;
  `8000` yields 0 and `FFFF` yields -840. Open, seek, short-read and close
  replies are unchecked. All 20 records have stride 42, column 40 is cleared,
  and column 41 retains the bytes left by the supplied file reply.
- TH03 draws all 20 comment lines, including lines beginning with a semicolon.
  Title color/effect is 31, comment color/effect 29. The actual load, B restore
  and four-plane unput execute before drawing; all 8,000 DWORD recapture
  iterations execute afterward. A bounded first-text write to B is visible in
  the final saved B snapshot.
- The four background segments are reloaded before each free. A bounded first
  free callback can change the second pointer; the actual second call observes
  the changed segment. Free does not clear the pointers.
- Flip executes the actual restore and polygon update, requests B-plane GRCG,
  then switches display/access pages before executing the complete owned
  `frame_delay_2` body. The page is an unsanitized BYTE. Counter replies are
  finite WORD values and the loop comparison is unsigned.

## Executed evidence and controls

The scalar model checks all DWORD registers, six segment registers, defined
flags/IF/DF, real near/far caller frames, ordered stores/ports and all 1 MiB of
memory. Every stack byte is checked; maximum observed depth is 44 bytes.
Actual polygon, IRAND and polar bodies execute on the same Unicorn, bound to
the previous complete polygon observation. The actual owned delay body also
executes. Heap, text, file, renderer, GRCG and counter replies are explicit
fixtures; no physical file/heap/pixel/page-banking/timing result is inferred.

Both images run 421 cases at each of loads `1000` and `3000`, for 1,684 complete
executions. Each load has put18, flip27, capture18, load299, free9, unput17 and
comment33 full returns. Cases cover all low track BYTEs plus signed/high-WORD
boundaries; short reads 0/1/39/40/41/839/840; null, aliased and overlapping
allocations; far offsets 0/1/FFFF; IF/DF; extreme mapped caller stacks; page
BYTE edges and delayed/large counter replies. A five-call capture/comment/
flip/comment/free chain retains static buffers, comments, VRAM and polygon
state on the same physical UC across independently supplied caller frames.

All 65 actual instruction mutations reject. Constructor, scalar prediction and
unexpected hook exceptions are fatal; the pre-execution phase guard includes
an explicit injected `ContractError`. One draft restore-coordinate mutation
304->305 was observably equivalent because both map to byte offset 38 and DI
is restored; moving eight pixels supplies a discriminating address mutation.
It was corrected rather than counted as a rejected guest.

## TH04 reference and reproduction

The user-authorized TH04 source was consulted read-only. Its `cmt_load.inl`
uses `_MUSIC.TXT`; TH03's native pointer selects `MUSIC.TXT`. TH04's comment
animation uses `cmt_shown_initial`, a rectangle background operation and a
different fade/flip path; it cannot replace TH03's four allocated planar
buffers and per-page recapture. Observed reference SHA256 values:

- `cmt_load.inl`: `c53f203b0e66e1a4a8941c533585d9048b7ec22695c74393f66e40c3fa811049`
- `cmt_load_unput_and_put_both_animate.inl`:
  `ace19067fcb30dc829db731b4c89497c946e5f9c74df4aec8b76a02fd9ac7aa6`

These references add no TH03 target proof or build dependency. Reproduce with
empty displays, one CPU, nice10 and the repository Python:

```sh
.venv/bin/python scripts/review_th03_op_music_comment_work.py
.venv/bin/python scripts/review_th03_op_music_comment_work.py --check
.venv/bin/python -m unittest discover -s tests -p test_op_music_comment_current.py -q
```

The tracked observation binds current implementation, complete cold report,
producer/SDK, prior polygon evidence and unchanged accepted publication.
`--check` revalidates those bindings and executes an eight-case-per-image
two-load dependency chain. It does not claim to rerun the full matrix.
The next menu contract must compose these bodies with actual owned input,
sound and delay code, and prove polling prefixes from their native CFG/live
invariants rather than an instruction-budget timeout.
