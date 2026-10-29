# OP score file native source review

2026-10-29: the actual `op_02.cpp` and `scoredat.cpp` TC4 producers now have
complete CODE ownership:394 bytes/four procedures/33 native CODE fields/seven
literal ordered MZ relocations. The initialized11-byte filename contribution
is a separate accepted DATA owner. Its one native fixup is a16-bit near pointer,
with no MZ relocation. `hi` is206 bytes of BSS and adds no file-backed credit.

| Procedure | CS-relative offset | CODE | Native return cleanup |
| --- | --- | --- | --- |
| Encode and save | 1868 | 165 | Near Pascal2 |
| Decode | 190D | 60 | Near0 |
| Recreate | 1949 | 127 | Near0 |
| Invalid checksum | 19C8 | 42 | Near0; result in AL |

The existing107-byte loader at19F2 remains separately accepted through the
selection helper TU. Together these owners cover all five authored score-file
procedures/501 CODE bytes. IRAND42 remains vendor context and is not added to
authored progress.

## Actual native source and layout

Each native wrapper is a literal include of its maintained `.cpp`. Both consume
`src/op/formats/scorecrypt.hpp` through normal compilation. All dependency
paths and staged source bytes are checked against the unchanged current cold
graph. The codec TU also consumes the original TC4 `stddef.h`, `_defs.h` and
`_null.h`, which are covered by the current configuration SDK/toolchain audit.

The native group1 contains CODE and group2 contains DGROUP DATA/BSS. Both MAP
public tables and complete segment allocations are checked. All33 CODE fields
resolve independently from native addends and MAP addresses: local BSS offsets,
external near DGROUP references, the real near encode call and far library
calls. Complete raw CODE and the emitted-order MZ vector match the pinned
Japanese target and current candidate. No object or executable is patched.

At DGROUP:0A02, `SCOREDAT_FN_PTR` is a WORD pointing to0A04, followed immediately
by `YUME.NEM` and its NUL. The complete native DATA record contains an ordinary
DGROUP local WORD fixup. Treating this as a DWORD far pointer would invent a
segment relocation and change the layout. The following linker alignment byte
is excluded.

At DGROUP:2394, `_hi` owns the complete206-byte BSS contribution, without any
initializer. Its layout follows the actual GAME3/BINARY O declarations and
TC4 `-b-` enum representation:

| Field | Offset | Size |
| --- | --- | --- |
| Checksum | 0 | 2 |
| Names | 2 | 80 |
| Cleared enum | 82 | 1 |
| Random unknown byte | 83 | 1 |
| Scores | 84 | 100 |
| Characters | 184 | 10 |
| Stages | 194 | 10 |
| Key1 / key2 | 204 / 205 | 1 / 1 |

## Original algorithm and ABI

Encode/save draws three random low bytes for key1, key2 and the unknown byte.
The16-bit checksum sums all204 score bytes at hi offsets2..205, including both
keys. Encryption then visits offsets203 down to0, including the checksum,
while leaving the two keys clear. Each subtraction wraps to BYTE; feedback is
the encrypted byte rotated right by3 and XORed with key2. Decode visits0..202
using the following ciphertext byte as feedback, then handles203 using key2.
The checksum predicate compares the restored WORD and returns a native C++
BYTE bool in AL. The loader's BOOL16 result is a different ABI.

Recreate sets the original name/score glyphs, character and stage defaults,
then encodes/saves and decodes once for each of four ranks. Preserve this order:
each save chooses fresh keys/unknown, and `hi` is decoded again after every
write. The score offset multiplication wraps as16-bit size_t before widening
for the file seek. File append/seek/write/close results remain unchecked, as in
the target. No defensive product changes or artificial failure matrix was added.

## Checks

```sh
PYTHONPATH=scripts .venv/bin/python -m lib.op_score_native
.venv/bin/python -m unittest tests.test_op_score_native tests.test_op_select_native tests.test_op_work_acceptance
.venv/bin/python scripts/publish_th03_op_work_scopes.py
```

Use one CPU, nice10 and empty displays. The unchanged full native cold pair is
validated and reused. Focused checks reject identical corrupted checksum code,
identical incorrect near pointers and reordered MZ entries. Historical score
runtime observations retain their original timestamps; no new replay of those
models or full native build is claimed.
