# MAINL root DATA — after556 native reconstruction

The originally contextual `obj/th03/mainl.obj` contains **10,944 CODE,
2,036 DATA and 5,108 BSS** bytes. The previous after555 stage rebuilt two
public-domain trigonometric table contributions from their mathematical
formulas. This after556 stage recovers and recompiles **another 963 DATA bytes**
from thirteen maintained, semantically named `.inl` files plus the already
maintained CDG reservation declaration. The 16 disjoint source extents now
cover **1,859 bytes of DATA**: 900 authored and 959 library-origin.

The new source covers the stage/shot filename and title/name strings, mutable
story pointers, sound state and priorities, shared file/graphics/random/VRAM
state, BFNT scratch header and sprite pool, archive extension, masked-image
lookup words, and cutscene/continue text. The Japanese source strings are
transported from UTF-8 to CP932 and the native wrapper is kept in the retained
stage for direct comparison. The 12-byte `_SHOT_FN` remains a buffer, not just
a string constant; the two initial pointers retain their actual local DATA
relocations.

## Disproved and corrected hypothesis

The archived, **unbuilt** after555 draft had omitted the supplier `GRP`
module's explicit initialized word-alignment byte after `graph_MeshByte`.
An actual TASM run shifted subsequent DATA offsets by one byte, yielding
68 changed PUBLIC coordinates and corresponding CODE fixup addends. A proposed
`evendata` alignment was tested and restored the sizes and addresses but did
**not** emit the original initialized byte. Reading the original public-domain
`grp[data].asm` established its actual `db 0 ; word alignment` declaration,
which now appears in the maintained `src/shared/data/graphics.inl`. This
supplier alignment byte is **not** credited as a recovered data owner.

The other uncredited alignment sites remain DATA+04A3, 0737, 076F and 07F3.
The file-backed reserved 32-byte BFNT header at DATA+0748..0767 and 2-byte
`_cdg_noalpha` state at DATA+0782..0783 have no OMF initializer; they count
as 34 reserved **file-backed** bytes, not 34 initialized zero bytes or BSS.
Total source-bound DATA is **1,825 initialized + 34 reserved**. The remainder
of the contextual DATA allocation, all contextual CODE and all BSS are
still outside this specific source claim.

## Native acceptance boundary

`build_th03_mainl_root_data_work.py` reassembled the complete contextual root
with the maintained sources and linked two complete independent native rounds.
Both rounds matched the original root object's full initializer map, all **392
literal ordered OMF fixups**, all **363 PUBLIC name/offset definitions** and
all non-variable segment/metadata records. The new PUBLIC packet *ordering*
is not asserted to be identical to the original assembler's packetization.

Both 67,372-byte decoded EXE outputs matched the original, including **677
literal ordered MZ relocation entries**. MAP contributions, lengths and
addresses matched; source filename paths naturally differ. The raw two-round
OBJ/EXE/MAP files, editor-independent inputs, response files and native writer
logs are retained. Only one project object was recompiled, and neither the
native cold source chain nor its CRT library were replayed.

Read-only affected review:

```sh
DISPLAY= WAYLAND_DISPLAY= PYTHONPATH=scripts \
  .venv/bin/python scripts/review_th03_mainl_root_data_work.py
```

This remains a **bounded, source-bound decoded DATA proof**, not a declaration
of identical original OBJ bytes, fully owned MAINL project source, canonical
packed EXE acceptance or whole-game completion. The full 2,036-byte DATA
allocation contains additional contextual material. No new authored CODE
or function count is claimed by this stage.
