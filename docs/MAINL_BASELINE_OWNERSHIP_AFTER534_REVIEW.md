# MAINL baseline source ownership closure after534

This read-only audit closes the four context entries left by after533's
incremental member dictionary. It recovers **no new source or CODE bytes**.
The complete library has 889 incremental source owners plus four earlier
baseline owners: **893 source-bound slots, 209,272 original-equal CODE bytes**.
The earlier incremental total remains 209,016; the baseline contributes 256.
These are compiler-library CODE extents, including members not linked into
MAINL, not authored game-code credit or a whole-game completion percentage.

| Original slot | Earlier owner | CODE | DATA | Retained producer |
| --- | --- | ---: | ---: | --- |
| 68 | `h_llsh` | 33 | 0 | frozen `mainl-build.json` |
| 72 | `h_padd` | 96 | 0 | frozen `mainl-build.json` |
| 79 | `ioerror` | 82 | 91 | frozen `mainl-build.json` |
| 87 | `lseek` | 45 | 0 | `mainl-stdio-build.json` |

`scripts/review_th03_mainl_after534_work.py` first reviews the unchanged after533
source receipt DAG, then binds these four maintained sources to earlier native
objects and the actual member programs of **both latest libraries**. All
segment extents, alignment/combine attributes, initialized bytes, public
identities/offsets, imports and individual literal relocation fields agree
with the independently pinned original compiler CL.LIB.

The audit retains both literal metadata profiles and explicitly rejects an
unqualified claim of original OBJ metadata equality:

- `h_padd` has a different PUBLIC record order. The frozen source's enumeration
  produces the retained target-equal MAP; the after529 original-PUBLIC-order
  diagnostic remains separate and receives no additional source credit.
- `ioerror` has different PUBLIC and GROUP record order. Its original FIXUPP
  sites are `22,28,45,39,51`; TASM emits `22,28,39,45,51`. Each full field agrees
  literally at its site, including frame, target and addend. The original and
  emitted streams are preserved separately; ordered equality is **false**.
- `h_llsh` and `lseek` preserve these literal field and metadata streams.
  This does not imply byte identity of every original OMF record.

The stdio source snapshots, include, ten-OBJ/LIB/EXE/MAP vectors and writer logs
are retained and checked for both native rounds. Only `lseek` is required to
equal its current maintained source: historical `setupio` was superseded at
after529, so the old stdio bank is bound to its original retained source
snapshots rather than falsely requiring that superseded source to be current.
The cold builder historically retained **one raw vector with equal two-round
inventories**. The audit checks its actual bytes against both inventories; it
does not manufacture two independently stored original cold outputs. Some
older pre-cold CRT manifests referenced by the historical CRT-link recipe no
longer exist and are not used as this audit's evidence.

Receipt: `.analysis/work/mainl-after534-baseline-ownership-review.json`.
Successful transcript: `.analysis/work/after534-independent-review-v2.txt`.
The first audit attempt stopped on superseded `setupio`; its transcript remains.
The latest native producer remains **after533**, with complete target-equal
67,372-byte decoded EXE, 80,893-byte retained MAP and 677 ordered MZ relocations.
No native writer, cold replay, runtime model or whole-product CI is launched.
Canonical Factory packed-file acceptance remains **0/250**.

Actual remaining external dependencies include the startup `C0L.OBJ` and
`EMU.LIB` / `MATHL.LIB`. The installed startup assembly is a hypothesis to
check against the actual pinned startup object and linked bytes; availability
of supplier source alone is not a reconstruction or source-acceptance proof.
